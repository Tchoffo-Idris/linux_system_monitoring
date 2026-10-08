# Testing and Verification — Linux Monitoring System

## 1. Purpose

This document describes how to verify that the Linux Monitoring System collects metrics, records monitoring results, generates alerts, and runs on a schedule.

Run these tests in the Ubuntu Server virtual machine. Record the actual outcome of each test rather than assuming that a feature works because its script or configuration exists.

## 2. Testing Environment

The lab uses the following tools:

* Ubuntu Server running in VirtualBox.
* Bash and Python 3.
* `psutil` for Python-based system monitoring.
* Linux utilities such as `uptime`, `free`, `df`, `ss`, and `vmstat`.
* Cron for scheduled execution.
* `journalctl` for reviewing system journal messages.
* `stress-ng` for optional controlled load testing.

Confirm that the scripts and required dependencies are present before starting.

```bash
ls -l scripts/
python3 --version
```

For the Python dependency:

```bash
python3 -c "import psutil; print(psutil.__version__)"
```

## 3. Test 1 — Baseline Collection

**Objective:** Record the system's initial state before evaluating monitoring results.

Run:

```bash
uptime
free -h
df -h
ss -tuln
vmstat 1 5 | tee docs/baseline.txt
```

**Expected result:**

* Uptime and load averages are displayed.
* Memory and swap information is displayed.
* Filesystem capacity is displayed.
* Listening sockets are listed.
* Five `vmstat` samples are collected, including the initial report.

**Verification:** Open `docs/baseline.txt` and confirm that it contains the command output.

## 4. Test 2 — Bash Monitoring

**Objective:** Verify that the Bash monitoring script executes and records metrics.

Run:

```bash
chmod +x scripts/monitor.sh
./scripts/monitor.sh
```

Inspect the metrics log:

```bash
tail -n 20 logs/metrics.log
```

Inspect the alert log if it exists:

```bash
tail -n 20 logs/alerts.log
```

**Expected result:** The script runs without unexpected errors and records metrics in the configured output file.

**Verification:** Confirm that the log contains new entries from the latest execution. Check the script's output and exit status if no records appear.

## 5. Test 3 — Python Monitoring

**Objective:** Verify that the Python implementation collects metrics and writes structured output.

Run:

```bash
python3 scripts/monitor.py
```

Inspect the output file:

```bash
tail -n 5 logs/metrics.jsonl
```

**Expected result:** The script executes and writes monitoring records in JSON Lines format if configured to do so.

**Verification:** Confirm that the records are new and correctly formatted. If the script fails to import `psutil`, install the appropriate package and repeat the test.

## 6. Test 4 — Threshold Alert Generation

**Objective:** Verify that an alert is recorded when a monitored value crosses a configured threshold.

### Bash test

Run the script with a temporarily low CPU threshold:

```bash
CPU_WARN=1 ./scripts/monitor.sh
```

Inspect the alert log:

```bash
tail -n 20 logs/alerts.log
```

### Python test

Run:

```bash
python3 scripts/monitor.py --cpu 1 --mem 1 --disk 1
```

Inspect the alert log:

```bash
tail -n 20 logs/alerts.log
```

**Expected result:** If the actual measured values exceed the temporary thresholds and the scripts implement these options as described, corresponding alerts should be generated.

**Verification:** Confirm that the alert matches a measured value and the relevant threshold. A test can legitimately fail to generate a particular alert if its condition is not met.

**Important:** These commands are for testing, not normal operation. Restore your intended thresholds after testing.

## 7. Test 5 — System Journal Logging

**Objective:** Verify that alert messages reach the system journal.

For the Bash implementation:

```bash
journalctl -t linux-monitor --no-pager -n 10
```

For the Python implementation:

```bash
journalctl -t linux-monitor-py --no-pager -n 10
```

**Expected result:** Relevant alert messages appear if the script sends them to the journal and the system accepts the messages.

**Verification:** Match the journal entries with the alert generated during the previous test. If no entries appear, confirm that the script uses the expected logger tag and that the alert condition was triggered.

## 8. Test 6 — Cron Scheduling

**Objective:** Verify that the selected monitoring script can run automatically.

Open the user's crontab:

```bash
crontab -e
```

For the Bash version, add a schedule using the actual absolute path to the script:

```cron
*/5 * * * * /home/YOUR_USERNAME/linux-monitoring-system/scripts/monitor.sh >/dev/null 2>>/home/YOUR_USERNAME/linux-monitoring-system/logs/cron-errors.log
```

Replace `YOUR_USERNAME` and the example project path with the actual values on your VM.

Verify the schedule:

```bash
crontab -l
```

After allowing enough time for scheduled runs, inspect the log:

```bash
tail -n 20 logs/metrics.log
```

Inspect any captured errors:

```bash
tail -n 20 logs/cron-errors.log
```

**Expected result:** New monitoring records appear after scheduled executions, provided the job is configured correctly.

**Verification:** Compare log timestamps and check for cron-related errors. A crontab entry alone does not prove that the scheduled job ran successfully.

## 9. Test 7 — Controlled CPU Load

**Objective:** Observe system behavior and alert generation during increased CPU activity.

This is an optional test. Use only your authorized lab VM and save a VirtualBox snapshot before testing.

First, inspect the available `stress-ng` options:

```bash
stress-ng --help
```

Run a short, controlled CPU test:

```bash
stress-ng --cpu 1 --timeout 30s --metrics-brief
```

Observe the system in another terminal:

```bash
top
```

Or:

```bash
htop
```

Run the monitoring script during or immediately after the test and review its logs.

**Expected result:** CPU activity should increase during the test. An alert should occur only if the monitoring script samples a value that crosses its configured threshold.

**Verification:** Compare the observed CPU activity with the monitoring logs and the configured threshold.

Do not run load tests on production systems or on machines without authorization. Avoid excessive workloads.

## 10. Test 8 — Log Rotation

**Objective:** Verify the log rotation configuration, if log rotation has been implemented.

Inspect the example configuration:

```bash
cat configs/logrotate.example
```

Check the available logrotate options:

```bash
logrotate --help
```

If logrotate is installed and a configuration has been created for the project's actual log paths, test that configuration using its supported debug or dry-run option before applying changes.

**Expected result:** The configuration identifies the intended log files and defines a rotation policy.

**Verification:** Confirm that the configuration matches the actual log paths. Do not claim that rotation works until it has been safely tested.

## 11. Test Results Checklist

Update the status and notes after performing each test.

| Test                       | Status  | Evidence                            |
| -------------------------- | ------- | ----------------------------------- |
| Baseline collection        | Pending | `docs/baseline.txt`                 |
| Bash monitoring            | Pending | `logs/metrics.log` and screenshot   |
| Python monitoring          | Pending | `logs/metrics.jsonl` and screenshot |
| Threshold alert generation | Pending | `logs/alerts.log`                   |
| System journal logging     | Pending | Relevant `journalctl` output        |
| Cron scheduling            | Pending | Crontab and timestamped log records |
| Controlled CPU load        | Pending | Screenshot and monitoring records   |
| Log rotation               | Pending | Configuration and test result       |

Replace `Pending` with `Passed`, `Failed`, or `Not Tested` as appropriate. Explain any failures and document the fixes.

## 12. Evidence to Capture

Suggested screenshots:

1. Baseline commands and output.
2. Bash monitoring execution.
3. Python monitoring output.
4. A verified alert and its corresponding log entry.
5. Crontab configuration and evidence of recurring runs.
6. Controlled CPU load with monitoring output.
7. Log rotation test, if implemented.

Save screenshots in the `screenshots/` directory using the filenames referenced in the project README.

## 13. Completion Criteria

The project should be considered verified only after:

* The scripts execute successfully.
* Metrics are recorded in the expected format.
* Threshold alert behavior is tested.
* System journal logging is checked if used.
* Cron scheduling is verified if configured.
* Failures and troubleshooting steps are documented.
* Evidence is saved and the test results reflect actual observations.

## Related Documentation

* [`architecture.md`](architecture.md)
* [`metrics-guide.md`](metrics-guide.md)
* [`troubleshooting.md`](troubleshooting.md)
