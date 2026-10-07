#!/usr/bin/env bash
# Linux Monitoring System - collects metrics and raises threshold alerts.
# Read-only: this script never modifies the system.
set -euo pipefail

# ---- Thresholds (override with environment variables) ----
CPU_WARN="${CPU_WARN:-80}"      # % CPU busy
MEM_WARN="${MEM_WARN:-80}"      # % memory used
DISK_WARN="${DISK_WARN:-85}"    # % disk used (any filesystem)
LOAD_WARN="${LOAD_WARN:-$(nproc)}"  # 1-min load average

LOG_DIR="${LOG_DIR:-$HOME/linux-monitoring-system/logs}"
METRICS_LOG="$LOG_DIR/metrics.log"
ALERT_LOG="$LOG_DIR/alerts.log"
mkdir -p "$LOG_DIR"

ts() { date '+%F %T'; }

alert() {
    local msg="$1"
    echo "[$(ts)] ALERT: $msg" | tee -a "$ALERT_LOG"
    logger -t linux-monitor -p user.warning "$msg"
}

cpu_usage() {
    # Sample /proc/stat twice, one second apart
    read -r _ u1 n1 s1 i1 w1 q1 sq1 st1 _ < /proc/stat
    sleep 1
    read -r _ u2 n2 s2 i2 w2 q2 sq2 st2 _ < /proc/stat
    local t1=$((u1+n1+s1+i1+w1+q1+sq1+st1))
    local t2=$((u2+n2+s2+i2+w2+q2+sq2+st2))
    local idle=$(( (i2+w2) - (i1+w1) ))
    local total=$(( t2 - t1 ))
    echo $(( 100 * (total - idle) / total ))
}

mem_usage() {
    # used% = (total - available) / total
    free | awk '/^Mem:/ {printf "%d", ($2-$7)*100/$2}'
}

load_1min() { awk '{print $1}' /proc/loadavg; }

CPU="$(cpu_usage)"
MEM="$(mem_usage)"
LOAD="$(load_1min)"
UPTIME="$(uptime -p)"
LISTEN="$(ss -tuln | tail -n +2 | wc -l)"
ESTAB="$(ss -tan state established | tail -n +2 | wc -l)"
ZOMBIES="$(ps -eo stat= | awk '/^Z/{c++} END{print c+0}')"
TOP_PROC="$(ps -eo comm=,%cpu= --sort=-%cpu | head -1 | awk '{print $1":"$2"%"}')"

echo "[$(ts)] cpu=${CPU}% mem=${MEM}% load=${LOAD} listen=${LISTEN} established=${ESTAB} zombies=${ZOMBIES} top=${TOP_PROC} uptime=\"${UPTIME}\"" | tee -a "$METRICS_LOG"

# ---- Threshold checks ----
if (( CPU >= CPU_WARN )); then alert "CPU at ${CPU}% (threshold ${CPU_WARN}%). Top process: ${TOP_PROC}"; fi
if (( MEM >= MEM_WARN )); then alert "Memory at ${MEM}% (threshold ${MEM_WARN}%)"; fi
if awk -v l="$LOAD" -v t="$LOAD_WARN" 'BEGIN{exit !(l >= t)}'; then
    alert "Load average ${LOAD} (threshold ${LOAD_WARN})"
fi
if (( ZOMBIES > 0 )); then alert "${ZOMBIES} zombie process(es) detected"; fi

# Check every real filesystem
while read -r pct mount; do
    if (( pct >= DISK_WARN )); then
        alert "Disk ${mount} at ${pct}% (threshold ${DISK_WARN}%)"
    fi
done < <(df -P -x tmpfs -x devtmpfs -x squashfs -x overlay | awk 'NR>1 {gsub("%","",$5); print $5, $6}')