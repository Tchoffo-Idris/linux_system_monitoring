#!/usr/bin/env python3
"""Linux Monitoring System (Python version).
Read-only: collects metrics, appends JSON lines to a log, raises threshold alerts."""
import argparse
import json
import os
import subprocess
from datetime import datetime
from pathlib import Path

import psutil

IGNORED_FS = {"squashfs", "tmpfs", "devtmpfs", "overlay"}


def parse_args():
    p = argparse.ArgumentParser(description="Collect system metrics and raise alerts.")
    p.add_argument("--cpu", type=float, default=80, help="CPU percent threshold")
    p.add_argument("--mem", type=float, default=80, help="memory percent threshold")
    p.add_argument("--disk", type=float, default=85, help="disk percent threshold")
    p.add_argument("--load", type=float, default=float(os.cpu_count() or 1),
                   help="1-minute load average threshold")
    p.add_argument("--log-dir",
                   default=str(Path.home() / "linux-monitoring-system" / "logs"))
    return p.parse_args()


def disk_usage():
    result = {}
    for part in psutil.disk_partitions(all=False):
        if part.fstype in IGNORED_FS:
            continue
        try:
            result[part.mountpoint] = psutil.disk_usage(part.mountpoint).percent
        except PermissionError:
            continue
    return result


def process_stats():
    procs = list(psutil.process_iter(["name", "status"]))
    for p in procs:
        try:
            p.cpu_percent(None)  # prime the per-process counters
        except psutil.Error:
            pass
    cpu = psutil.cpu_percent(interval=1)  # sample overall CPU for one second
    top_name, top_cpu, zombies = "n/a", 0.0, 0
    for p in procs:
        try:
            usage = p.cpu_percent(None)
            if p.info["status"] == psutil.STATUS_ZOMBIE:
                zombies += 1
            if usage > top_cpu:
                top_name, top_cpu = p.info["name"], usage
        except psutil.Error:
            continue
    return cpu, top_name, top_cpu, zombies


def network_stats():
    conns = psutil.net_connections(kind="inet")
    listening = sum(1 for c in conns if c.status == psutil.CONN_LISTEN)
    established = sum(1 for c in conns if c.status == psutil.CONN_ESTABLISHED)
    return listening, established


def alert(message, log_dir, now):
    line = f"[{now}] ALERT: {message}"
    print(line)
    with open(log_dir / "alerts.log", "a") as f:
        f.write(line + "\n")
    subprocess.run(["logger", "-t", "linux-monitor-py", "-p", "user.warning", message],
                   check=False)


def main():
    args = parse_args()
    log_dir = Path(args.log_dir)
    log_dir.mkdir(parents=True, exist_ok=True)
    now = datetime.now().isoformat(timespec="seconds")

    cpu, top_name, top_cpu, zombies = process_stats()
    mem = psutil.virtual_memory().percent  # based on available memory, not "free"
    load1 = os.getloadavg()[0]
    listening, established = network_stats()
    disks = disk_usage()
    uptime_h = round((datetime.now().timestamp() - psutil.boot_time()) / 3600, 1)

    metrics = {
        "time": now, "cpu_percent": cpu, "mem_percent": mem, "load_1min": load1,
        "disks": disks, "tcp_listening": listening, "tcp_established": established,
        "zombies": zombies, "top_process": f"{top_name}:{top_cpu}%", "uptime_hours": uptime_h,
    }
    with open(log_dir / "metrics.jsonl", "a") as f:
        f.write(json.dumps(metrics) + "\n")
    print(json.dumps(metrics, indent=2))

    if cpu >= args.cpu:
        alert(f"CPU at {cpu}% (threshold {args.cpu}%). Top process: {top_name}", log_dir, now)
    if mem >= args.mem:
        alert(f"Memory at {mem}% (threshold {args.mem}%)", log_dir, now)
    if load1 >= args.load:
        alert(f"Load average {load1} (threshold {args.load})", log_dir, now)
    if zombies > 0:
        alert(f"{zombies} zombie process(es) detected", log_dir, now)
    for mount, pct in disks.items():
        if pct >= args.disk:
            alert(f"Disk {mount} at {pct}% (threshold {args.disk}%)", log_dir, now)


if __name__ == "__main__":
    main()