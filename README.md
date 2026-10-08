![Linux](https://img.shields.io/badge/OS-Ubuntu%20Server-E95420?logo=ubuntu\&logoColor=white)
![Bash](https://img.shields.io/badge/Scripting-Bash-4EAA25?logo=gnubash\&logoColor=white)
![Python](https://img.shields.io/badge/Language-Python-3776AB?logo=python\&logoColor=white)
![Monitoring](https://img.shields.io/badge/System-Monitoring-blue)
![Cron](https://img.shields.io/badge/Automation-Cron-orange)
![VirtualBox](https://img.shields.io/badge/Lab-VirtualBox-183A61?logo=virtualbox\&logoColor=white)
![Status](https://img.shields.io/badge/Project-Portfolio%20Lab-yellow)

# Linux Monitoring System

A lightweight Linux system monitoring tool built on Ubuntu Server to collect system performance metrics, record results, and generate alerts when resource usage reaches configurable thresholds.

This project demonstrates practical Linux administration skills, including performance monitoring, Bash scripting, Python automation, log management, scheduled tasks, and troubleshooting in a virtualized lab environment.

## Table of Contents

* [Project Overview](#project-overview)
* [Objectives](#objectives)
* [Technologies and Tools](#technologies-and-tools)
* [System Architecture](#system-architecture)
* [Metrics Monitored](#metrics-monitored)
* [Features](#features)
* [Project Structure](#project-structure)
* [Installation and Setup](#installation-and-setup)
* [Usage](#usage)
* [Alert Configuration](#alert-configuration)
* [Automation with Cron](#automation-with-cron)
* [Testing and Verification](#testing-and-verification)
* [Screenshots and Evidence](#screenshots-and-evidence)
* [Challenges and Lessons Learned](#challenges-and-lessons-learned)
* [Future Improvements](#future-improvements)
* [Disclaimer](#disclaimer)

## Project Overview

System administrators need to understand how a server behaves under normal conditions before they can identify performance problems. High CPU usage, limited available memory, increasing disk consumption, and unexpected network connections can affect system reliability if they go unnoticed.

The purpose of this project is to build a lightweight monitoring solution that collects important Linux system metrics, compares selected values against predefined thresholds, and records alerts when those thresholds are reached.

The monitoring system is developed in two versions:

* **Bash:** Uses native Linux utilities and system information to collect metrics and generate human-readable logs.
* **Python:** Uses `psutil` to collect system information and writes structured JSON Lines data for easier analysis and future integration.

The system can also be scheduled with cron so that monitoring runs automatically instead of relying on manual execution.

## Objectives

The main objectives of this project are to:

* Establish a healthy baseline for an Ubuntu Server virtual machine.
* Monitor CPU utilization, system load, memory usage, disk usage, network sockets, processes, and uptime.
* Develop a reusable Bash monitoring script.
* Implement a Python alternative for structured metric collection.
* Configure adjustable thresholds for resource usage.
* Generate alerts when configured thresholds are reached.
* Record monitoring results in log files and the system logging service.
* Automate monitoring with cron.
* Test alert behavior under controlled conditions.
* Document the architecture, testing results, troubleshooting steps, and lessons learned.

## Technologies and Tools

| Technology                | Purpose                                           |
| ------------------------- | ------------------------------------------------- |
| Ubuntu Server             | Linux environment used for the monitoring lab     |
| VirtualBox                | Runs the Ubuntu Server virtual machine            |
| Bash                      | Implements the primary monitoring script          |
| Python 3                  | Implements the alternative monitoring script      |
| psutil                    | Provides structured access to system metrics      |
| `top` and `htop`          | Inspect running processes and resource usage      |
| `free`                    | Check memory and swap usage                       |
| `df` and `du`             | Inspect filesystem capacity and directory usage   |
| `vmstat`                  | Observe system performance and resource activity  |
| `ss`                      | Inspect listening sockets and network connections |
| `ps`                      | Inspect processes and identify resource consumers |
| cron                      | Schedules recurring monitoring runs               |
| `logger` and `journalctl` | Send and inspect system log messages              |
| `stress-ng`               | Generate controlled load for lab testing          |
| Git and GitHub            | Version control and project documentation         |

## System Architecture

The monitoring workflow follows this sequence:

```text
             Ubuntu Server VM
                    |
                    v
             Cron Scheduler
              (Every 5 Min)
                    |
                    v
          Monitoring Script
             /          \
            v            v
       Bash Version   Python Version
            |            |
            v            v
       Linux Tools      psutil
            |            |
            v            v
       Collect Metrics and System State
                    |
                    v
          Evaluate Thresholds
                    |
             +------+------+
             |             |
             v             v
        Metrics Logs   Alert Logs
                           |
                           v
                    System Journal
```

The Bash and Python scripts are alternative implementations of the monitoring process. They can be scheduled independently, depending on which version is being used.

**Why this design?**

Separating metric collection, threshold checks, and logging makes the system easier to understand and troubleshoot. Recording results also provides evidence of what the server was doing when an alert occurred.

An architecture diagram is available in [`diagrams/architecture.png`](diagrams/architecture.png), once the diagram has been created and added to the repository.

## Metrics Monitored

| Metric           | Purpose                                                      | Example Tool        |
| ---------------- | ------------------------------------------------------------ | ------------------- |
| CPU utilization  | Identifies high processor activity                           | `/proc/stat`, `top` |
| System load      | Shows runnable and waiting workload relative to CPU capacity | `uptime`            |
| Memory usage     | Identifies potential memory pressure                         | `free`, `psutil`    |
| Disk usage       | Detects filesystems approaching capacity                     | `df`                |
| Network sockets  | Counts listening and established connections                 | `ss`, `psutil`      |
| Process activity | Identifies resource-intensive and zombie processes           | `ps`, `htop`        |
| System uptime    | Shows how long the server has been running                   | `uptime`            |

Monitoring these metrics helps establish a baseline and provides a starting point for investigating performance problems.

## Features

### 1. System Performance Monitoring

The scripts collect important resource metrics, including CPU utilization, memory usage, system load, and disk capacity.

### 2. Configurable Thresholds

The Bash implementation uses environment variables to adjust alert thresholds without modifying the script.

The Python implementation accepts command-line arguments for threshold configuration.

### 3. Logging and Alerting

The Bash version writes human-readable metrics to `logs/metrics.log` and alerts to `logs/alerts.log`. It also sends alert messages to the system logging service using `logger`.

The Python version records structured metrics in `logs/metrics.jsonl` and writes alerts to the alert log.

### 4. Scheduled Monitoring

Cron can execute the selected monitoring script every five minutes, allowing the system to collect metrics automatically.

### 5. Controlled Testing

Thresholds can be temporarily lowered to verify alert generation without deliberately overloading the server. A separate controlled CPU load test can be used to observe how the monitoring system behaves under higher utilization.

### 6. Log Management

Log rotation can be configured to limit the accumulation of monitoring logs over time, helping prevent the monitoring system from consuming excessive disk space.

## Project Structure

The repository is organized to separate scripts, configuration examples, documentation, logs, and visual evidence.

```text
linux-monitoring-system/
├── README.md
├── .gitignore
├── LICENSE
├── scripts/
│   ├── monitor.sh
│   └── monitor.py
├── configs/
│   ├── crontab.example
│   └── logrotate.example
├── docs/
│   ├── baseline.txt
│   ├── architecture.md
│   ├── metrics-guide.md
│   ├── testing.md
│   └── troubleshooting.md
├── sample-logs/
│   ├── metrics.sample.log
│   └── alerts.sample.log
├── screenshots/
│   ├── 01-baseline-commands.png
│   ├── 02-htop.png
│   ├── 03-monitor-script-output.png
│   ├── 04-alert-triggered.png
│   ├── 05-cron-running.png
│   ├── 06-stress-test.png
│   └── 07-python-output.png
└── diagrams/
    └── architecture.png
```

*Note: The structure above represents the intended repository layout. Add files as you create and verify them; do not include empty placeholder files merely to make the repository appear complete.*

## Installation and Setup

### Prerequisites

* An Ubuntu Server virtual machine.
* Terminal or SSH access to the VM.
* Sudo privileges for package installation and system-level configuration.
* Git for version control.

### Step 1: Update the system

```bash
sudo apt update
sudo apt upgrade -y
```

This updates package information and installs available upgrades, helping provide a current environment for the lab.

### Step 2: Install the monitoring tools

```bash
sudo apt install -y htop sysstat stress-ng iproute2 procps tree git
```

Install the Python monitoring dependency:

```bash
sudo apt install -y python3-psutil
```

### Step 3: Create the project directory

```bash
mkdir -p ~/linux-monitoring-system/{scripts,docs,configs,screenshots,diagrams,logs}
cd ~/linux-monitoring-system
```

### Step 4: Record the baseline

Before implementing the monitoring scripts, collect the system's initial state:

```bash
uptime
free -h
df -h
ss -tuln
vmstat 1 5 | tee docs/baseline.txt
```

A baseline is important because resource usage varies between systems. Without knowing what is normal for the VM, it is harder to determine whether a later reading indicates a genuine problem.

### Step 5: Add the monitoring scripts

Place the Bash implementation in `scripts/monitor.sh` and the Python implementation in `scripts/monitor.py`, following the project documentation.

Make the scripts executable:

```bash
chmod +x scripts/monitor.sh scripts/monitor.py
```

## Usage

### Run the Bash monitoring script

```bash
./scripts/monitor.sh
```

View the collected metrics:

```bash
cat logs/metrics.log
```

View recorded alerts:

```bash
cat logs/alerts.log
```

### Override Bash thresholds

For example, to lower the CPU alert threshold for a single test:

```bash
CPU_WARN=70 ./scripts/monitor.sh
```

This changes the threshold for that invocation without permanently modifying the script.

### Run the Python monitoring script

```bash
./scripts/monitor.py
```

View the structured metrics:

```bash
tail -n 5 logs/metrics.jsonl
```

To test its alert logic with low thresholds:

```bash
./scripts/monitor.py --cpu 1 --mem 1 --disk 1
```

These low values are intended for testing. They should not be used as normal production thresholds.

## Alert Configuration

The Bash implementation uses the following default thresholds:

| Resource                |             Default Threshold |
| ----------------------- | ----------------------------: |
| CPU utilization         |                           80% |
| Memory usage            |                           80% |
| Disk utilization        |                           85% |
| One-minute load average | Number of available CPU cores |

The Python implementation uses equivalent default thresholds and allows them to be overridden through command-line arguments.

Thresholds should be adjusted to match the server's workload. For example, a short CPU spike may be normal on a busy application server, whereas sustained high disk utilization may require immediate investigation.

To inspect Bash alerts in the system journal:

```bash
journalctl -t linux-monitor --no-pager -n 10
```

For the Python version:

```bash
journalctl -t linux-monitor-py --no-pager -n 10
```

## Automation with Cron

To schedule the Bash script:

```bash
crontab -e
```

Add the following line, replacing `YOUR_USERNAME` with the actual Linux username:

```cron
*/5 * * * * /home/YOUR_USERNAME/linux-monitoring-system/scripts/monitor.sh >/dev/null 2>>/home/YOUR_USERNAME/linux-monitoring-system/logs/cron-errors.log
```

Verify the schedule:

```bash
crontab -l
```

After allowing enough time for multiple executions, inspect the log:

```bash
tail -n 5 ~/linux-monitoring-system/logs/metrics.log
```

Cron runs jobs in a limited environment, which is why absolute paths are used. Redirecting standard error to a dedicated file also makes scheduling problems easier to investigate.

**Important:** Schedule only one monitoring implementation at a time unless you intentionally want both to run. This avoids duplicate monitoring runs and potentially confusing alert records.

## Testing and Verification

The monitoring system should be tested before it is considered ready for use.

| Test                | Verification Method                                      | Expected Result                                                     |
| ------------------- | -------------------------------------------------------- | ------------------------------------------------------------------- |
| Baseline collection | Run `uptime`, `free -h`, `df -h`, and `ss -tuln`         | System information is displayed                                     |
| Bash execution      | Run `./scripts/monitor.sh`                               | Metrics are collected and logged                                    |
| Python execution    | Run `./scripts/monitor.py`                               | Structured metrics are printed and recorded                         |
| Threshold alerts    | Run a script with temporarily low thresholds             | Alert messages are generated                                        |
| System logging      | Inspect the relevant `journalctl` tag                    | Alert messages appear in the journal                                |
| Cron scheduling     | Inspect the crontab and timestamped logs                 | Recurring execution is demonstrated                                 |
| CPU load test       | Run a controlled `stress-ng` test in the lab             | Resource usage rises and alerts trigger when thresholds are crossed |
| Log rotation        | Verify the log rotation configuration and test it safely | Old logs can be rotated according to the configured policy          |

Record the actual result of each test in [`docs/testing.md`](docs/testing.md), including failures and the steps used to resolve them.

A test should be marked as passed only after the expected behavior has been observed.

## Screenshots and Evidence

Screenshots provide visual evidence that the scripts ran and the features were verified.

### 1. Baseline Metrics

![Baseline metrics](screenshots/01-baseline-commands.png)

Shows the initial CPU/load, memory, disk, and network socket information collected before monitoring begins.

### 2. System Resource Overview

![HTOP monitoring](screenshots/02-htop.png)

Shows CPU utilization, memory and swap usage, load average, uptime, and running processes.

### 3. Bash Monitoring Output

![Monitoring script output](screenshots/03-monitor-script-output.png)

Demonstrates execution of the Bash script and the metrics recorded in the log.

### 4. Threshold Alerts

![Alert verification](screenshots/04-alert-triggered.png)

Shows the alert messages generated during threshold testing and the corresponding log or journal output.

### 5. Cron Automation

![Cron monitoring](screenshots/05-cron-running.png)

Provides evidence of the scheduled job and monitoring records generated at recurring intervals.

### 6. Controlled Load Test

![Stress test](screenshots/06-stress-test.png)

Shows the lab VM under controlled CPU load and the resulting monitoring behavior.

### 7. Python Monitoring Output

![Python monitoring](screenshots/07-python-output.png)

Shows structured metric output and alert generation from the Python implementation.

*Screenshot images must be added to the `screenshots/` directory using the filenames above. If an image is not yet available, its preview will not render until the file is added.*

## Challenges and Lessons Learned

This project provides practical opportunities to develop skills beyond simply running Linux commands.

* **Establishing a baseline:** A normal reading is necessary to distinguish ordinary activity from unusual resource consumption.
* **Interpreting memory correctly:** Linux uses available memory for caching, so the `available` value is more useful than the `free` value alone when assessing memory pressure.
* **Measuring CPU usage:** CPU utilization is calculated over a period of time, which is why the Bash script samples CPU counters more than once.
* **Testing alerts safely:** Temporarily lowering thresholds can verify alert logic without unnecessarily overloading the virtual machine.
* **Automating reliably:** Cron's limited execution environment makes absolute paths and error logging important.
* **Managing monitoring data:** Log rotation helps prevent accumulated logs from consuming excessive disk space.
* **Comparing Bash and Python:** Bash is useful for combining native Linux tools, while Python makes structured output and future integrations easier to develop.

Document at least one genuine troubleshooting incident in `docs/troubleshooting.md`, including the symptoms, investigation, root cause, fix, and verification. This demonstrates the diagnostic process behind the final result.

## Future Improvements

Potential extensions include:

* Sending alerts through email or a secure messaging webhook.
* Requiring repeated threshold breaches before alerting to reduce false positives.
* Adding historical trend analysis and summary reports.
* Building a dashboard for visualizing CPU, memory, disk, and load trends.
* Integrating Prometheus Node Exporter and Grafana.
* Replacing cron with a systemd timer.
* Adding automated tests for threshold calculations and error handling.

These are possible future enhancements, not claims about functionality already implemented.

## Disclaimer

This project is intended for educational and portfolio purposes in a controlled Ubuntu Server lab environment. Review the scripts, thresholds, permissions, logging configuration, and operational requirements before adapting them for production systems.

Load testing should be performed only on a disposable or otherwise authorized lab machine, never on a production server without appropriate authorization and safeguards.

---

**Project focus:** Linux System Administration | Performance Monitoring | Bash Scripting | Python Automation | Log Management | Troubleshooting

**Repository:** [linux-monitoring-system](.)
