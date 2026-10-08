# Metrics Guide — Linux Monitoring System

## 1. Purpose

This guide explains the system metrics collected by the Linux Monitoring System, why each metric matters, which tools can be used to inspect it manually, and how to interpret the results.

Understanding normal system behavior helps an administrator identify unusual activity and investigate performance problems.

## 2. CPU Utilization

**Purpose:** Measures how much processor capacity is being used.

High CPU utilization can occur when applications perform intensive calculations, several processes run simultaneously, or a process behaves unexpectedly.

Useful commands:

```bash
top
```

```bash
htop
```

```bash
vmstat 1 5
```

**How to interpret it:**

* Low utilization usually means the processor has spare capacity.
* High utilization may be normal during intensive workloads.
* Sustained high utilization may indicate a performance bottleneck.

The project uses a default CPU alert threshold of **80%**. This is a configurable warning level, not a universal definition of a problem.

## 3. System Load Average

**Purpose:** Shows the average system workload over different periods.

Check load average with:

```bash
uptime
```

Or:

```bash
cat /proc/loadavg
```

Linux reports load averages for approximately 1, 5, and 15 minutes. The values include runnable tasks and tasks waiting in certain uninterruptible states, so load average is not the same as CPU utilization.

**How to interpret it:**

* Compare the load average with the number of available CPU cores.
* A load average below the core count generally suggests that the runnable workload may fit within available CPU capacity.
* A sustained load above the core count can indicate contention, but the cause requires further investigation.

The project uses the number of available CPU cores as its default one-minute load threshold.

Check the available CPU count with:

```bash
nproc
```

## 4. Memory Usage

**Purpose:** Tracks RAM consumption and helps identify potential memory pressure.

Useful commands:

```bash
free -h
```

```bash
top
```

```bash
ps aux --sort=-%mem | head
```

**How to interpret it:**

* Linux uses available memory for caching, so low `free` memory alone does not necessarily mean the server is running out of RAM.
* The `available` value reported by `free -h` is generally more useful for assessing how much memory can be used by applications without significant memory pressure.
* Investigate processes consuming unusually large amounts of memory if available memory becomes low.

The default memory alert threshold is **80%**. Review the script's calculation to understand exactly how its percentage is defined.

## 5. Disk Usage

**Purpose:** Measures how much filesystem capacity is occupied.

Check filesystem usage with:

```bash
df -h
```

To inspect the size of a directory:

```bash
du -sh ~/linux-monitoring-system
```

**How to interpret it:**

* High disk utilization leaves less space for logs, applications, temporary files, and system updates.
* A filesystem approaching capacity may cause applications or system services to fail.
* Identify large files and directories before deleting anything.

The default disk alert threshold is **85%**.

Check which filesystem contains a directory before investigating its usage. A directory may reside on a different mounted filesystem than expected.

## 6. Network Sockets

**Purpose:** Provides information about listening services and network connections.

List listening TCP and UDP sockets with:

```bash
ss -tuln
```

Show established TCP connections:

```bash
ss -tn state established
```

Show listening sockets with process information where permissions allow:

```bash
sudo ss -tulpn
```

**How to interpret it:**

* Listening sockets can indicate services waiting for connections.
* Established connections indicate active TCP sessions.
* An unfamiliar socket is not automatically malicious; compare it with the services expected on the server.

Investigate unexpected listening services, unfamiliar ports, and connections that do not match the system's intended role.

## 7. Process Activity

**Purpose:** Helps identify running processes and possible resource-intensive tasks.

Useful commands:

```bash
ps aux
```

Sort processes by CPU usage:

```bash
ps aux --sort=-%cpu | head
```

Sort processes by memory usage:

```bash
ps aux --sort=-%mem | head
```

For an interactive view:

```bash
htop
```

**How to interpret it:**

Look for processes consuming unusually high CPU or memory, repeated failures, unexpected applications, and zombie processes.

A resource-intensive process may be legitimate. Check its purpose before terminating it.

## 8. System Uptime

**Purpose:** Shows how long the system has been running since its last boot.

Check uptime with:

```bash
uptime
```

For a concise value:

```bash
uptime -p
```

Uptime helps provide context when reviewing system behavior, recent restarts, and monitoring records. A recent reboot is not automatically a problem, but it may be relevant during an investigation.

## 9. Default Alert Thresholds

| Metric                  |             Default threshold | Recommended response                                                    |
| ----------------------- | ----------------------------: | ----------------------------------------------------------------------- |
| CPU utilization         |                           80% | Check CPU-heavy processes and determine whether high usage is sustained |
| Memory usage            |                           80% | Inspect available memory and processes consuming RAM                    |
| Disk utilization        |                           85% | Identify large files and assess remaining filesystem capacity           |
| One-minute load average | Number of available CPU cores | Compare load with CPU capacity and investigate waiting tasks            |

These values are starting points for a lab. Adjust them to suit the server's workload and test the resulting alert behavior.

## 10. Establishing a Baseline

Collect a baseline before evaluating monitoring results:

```bash
uptime
free -h
df -h
ss -tuln
vmstat 1 5 | tee docs/baseline.txt
```

Save the output and record the conditions under which it was collected.

A useful baseline provides a reference for comparing later measurements. It should reflect normal activity on the particular virtual machine rather than an assumed universal value.

## 11. Reviewing Logs

Inspect Bash metrics:

```bash
tail -n 20 logs/metrics.log
```

Inspect alerts:

```bash
tail -n 20 logs/alerts.log
```

Inspect Python metrics:

```bash
tail -n 20 logs/metrics.jsonl
```

Review recent system journal messages from the Bash monitoring script:

```bash
journalctl -t linux-monitor --no-pager -n 10
```

Review recent Python monitoring messages:

```bash
journalctl -t linux-monitor-py --no-pager -n 10
```

Use the relevant log to confirm what the monitoring script recorded and whether the result matches the system's observed state.

## 12. Important Notes

* A single high reading does not always indicate a fault.
* Compare measurements over time where possible.
* Investigate alerts before changing system settings.
* Confirm the monitoring script's calculations and output format.
* Use controlled tests to verify alerts.
* Do not delete files or terminate processes solely because a metric is high.

## Related Documentation

* [`architecture.md`](architecture.md)
* [`testing.md`](testing.md)
* [`troubleshooting.md`](troubleshooting.md)
