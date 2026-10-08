# System Architecture — Linux Monitoring System

## 1. Overview

The Linux Monitoring System is designed to collect important performance metrics from an Ubuntu Server virtual machine, evaluate resource usage against configurable thresholds, and record monitoring results and alerts.

The project provides two monitoring implementations:

* **Bash:** Uses native Linux commands and system information to collect metrics and write human-readable logs.
* **Python:** Uses Python and the `psutil` library to collect metrics and produce structured JSON Lines output.

Both implementations follow the same general workflow, but they can be run and scheduled independently.

## 2. Architecture Diagram

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
             Bash Version  Python Version
                  |            |
                  v            v
             Linux Tools     psutil
                  |            |
                  +-----+------+
                        |
                        v
                Collect System Metrics
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

**Note:** Bash and Python are alternative implementations. Cron can be configured to run either version. Running both is optional and may create duplicate monitoring records.

## 3. Components

### 3.1 Ubuntu Server

Ubuntu Server provides the operating system on which the monitoring scripts run. It supplies information about processor activity, memory, storage, running processes, system load, uptime, and network sockets.

### 3.2 Bash Monitoring Script

File: `scripts/monitor.sh`

The Bash script collects system information using Linux utilities and system interfaces. It evaluates configured thresholds and records metrics and alerts.

The script is intended to write:

* `logs/metrics.log` — human-readable monitoring results.
* `logs/alerts.log` — threshold alerts.
* System journal messages through `logger`, when alert conditions occur.

### 3.3 Python Monitoring Script

File: `scripts/monitor.py`

The Python implementation uses `psutil` to retrieve system information and supports configurable thresholds through command-line arguments.

Its structured metrics output is written to:

* `logs/metrics.jsonl` — metrics stored as JSON Lines.
* `logs/alerts.log` — alert messages.

The exact output depends on the implementation and its configuration.

### 3.4 Threshold Evaluation

The monitoring scripts compare collected values with configured thresholds. For example, a CPU warning can be generated when utilization reaches the configured limit.

The default thresholds are:

| Resource                |                     Threshold |
| ----------------------- | ----------------------------: |
| CPU utilization         |                           80% |
| Memory usage            |                           80% |
| Disk utilization        |                           85% |
| One-minute load average | Number of available CPU cores |

Thresholds can be adjusted to suit the server and the purpose of the test.

### 3.5 Logging

The project keeps monitoring data and alerts in log files so that results can be reviewed after each run.

The Bash implementation produces human-readable records, while the Python implementation produces structured JSON Lines records. System journal messages can also be inspected with `journalctl`.

### 3.6 Cron Scheduler

Cron can run the selected monitoring script every five minutes. This makes recurring monitoring possible without manually starting the script each time.

Cron jobs should use absolute paths and redirect errors to a log file to make failures easier to investigate.

## 4. Monitoring Workflow

1. Ubuntu Server starts or continues running.
2. The monitoring script is launched manually or by cron.
3. The script collects the configured system metrics.
4. The script evaluates the metrics against the configured thresholds.
5. The script records the collected metrics.
6. If a threshold condition is met, the script records an alert.
7. The administrator reviews logs and investigates unusual readings.

## 5. Data Flow

| Input                      | Processing                            | Output                                |
| -------------------------- | ------------------------------------- | ------------------------------------- |
| CPU and load information   | Collect and evaluate resource usage   | Metrics and possible alerts           |
| Memory information         | Calculate or retrieve memory usage    | Metrics and possible alerts           |
| Filesystem information     | Inspect disk utilization              | Metrics and possible alerts           |
| Network socket information | Inspect socket states and connections | Monitoring records                    |
| Process information        | Inspect running processes             | Monitoring records                    |
| Threshold configuration    | Compare values with limits            | Alert records when conditions are met |

## 6. Design Considerations

* **Separation of concerns:** Scripts, configuration examples, documentation, and evidence are stored in separate directories.
* **Configurable thresholds:** Alert limits can be changed without permanently editing the monitoring logic.
* **Readable logs:** Human-readable Bash logs are convenient for terminal inspection.
* **Structured output:** JSON Lines output from Python is useful for later processing and integration.
* **Scheduled execution:** Cron supports recurring monitoring.
* **Safe testing:** Threshold tests should be performed in the virtual machine before considering deployment elsewhere.

## 7. Limitations

This project is a lightweight monitoring lab rather than a full monitoring platform. It does not automatically provide a graphical dashboard, long-term analytics, or remote alert delivery unless those features are implemented separately.

The monitoring scripts, cron configuration, logging, and alert behavior must be tested before the project is considered complete.

## 8. Related Documentation

* [`metrics-guide.md`](metrics-guide.md)
* [`testing.md`](testing.md)
* [`troubleshooting.md`](troubleshooting.md)
* [`../README.md`](../README.md)
