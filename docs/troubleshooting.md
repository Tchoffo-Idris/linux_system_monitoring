# Troubleshooting Guide — Linux Monitoring System

## 1. Overview

During the development of the Linux Monitoring System, several issues can occur when collecting system metrics, configuring alert thresholds, setting up cron jobs, and managing log files.

This document describes common problems, how they can be investigated, and the steps used to resolve them.

## 2. Issue 1: Bash Script Permission Denied

**Problem**

When attempting to execute the monitoring script, the terminal displayed a `Permission denied` error.

**Possible Cause**

The script did not have execute permission.

**Investigation**

I checked the file permissions using:

```bash
ls -l scripts/monitor.sh
```

The output showed that the script did not have execute permission.

**Solution**

I added execute permission to the script:

```bash
chmod +x scripts/monitor.sh
```

I then executed the script again:

```bash
./scripts/monitor.sh
```

**Verification**

The script executed without the previous permission error.

**Lesson Learned**

Linux file permissions determine whether a user can execute a script. Checking permissions is an important first step when troubleshooting execution errors.

## 3. Issue 2: Python Script Could Not Import psutil

**Problem**

The Python monitoring script failed to start because the `psutil` module was unavailable.

**Possible Cause**

The required Python dependency had not been installed in the environment used to run the script.

**Investigation**

I tested whether Python could import the module:

```bash
python3 -c "import psutil; print(psutil.__version__)"
```

The command returned a module import error.

**Solution**

I installed the required package on Ubuntu Server:

```bash
sudo apt update
sudo apt install python3-psutil
```

**Verification**

I repeated the import test and ran the Python monitoring script:

```bash
python3 -c "import psutil; print(psutil.__version__)"
python3 scripts/monitor.py
```

The dependency was available, allowing the script to proceed.

**Lesson Learned**

Python scripts may depend on external libraries. Checking dependencies early helps prevent avoidable execution failures.

## 4. Issue 3: Monitoring Logs Were Not Being Created

**Problem**

The monitoring script ran, but the expected log files were missing.

**Possible Cause**

The logs directory did not exist, or the script was configured to write to a different path.

**Investigation**

I checked the project directory and its contents:

```bash
pwd
ls -la
ls -la logs/
```

This helped determine whether the expected directory and log files were present.

**Solution**

I created the logs directory if it was missing:

```bash
mkdir -p logs
```

I then checked the script's configured output paths and ensured they matched the project structure.

**Verification**

I ran the monitoring script again and inspected the log directory:

```bash
./scripts/monitor.sh
ls -la logs/
```

The expected log file was present after the issue was corrected.

**Lesson Learned**

Scripts depend on correct file paths and directory permissions. Verifying output locations makes logging problems easier to diagnose.

## 5. Issue 4: Alerts Were Not Triggered

**Problem**

The monitoring script collected metrics, but no alert appeared during normal testing.

**Possible Cause**

The system's actual resource usage had not exceeded the configured alert threshold.

**Investigation**

I reviewed the monitoring output and compared the collected values with the configured thresholds.

```bash
tail -n 20 logs/metrics.log
tail -n 20 logs/alerts.log
```

**Solution**

To test the alert logic without deliberately overloading the virtual machine, I temporarily lowered the CPU threshold:

```bash
CPU_WARN=1 ./scripts/monitor.sh
```

This test assumes that the Bash script supports the `CPU_WARN` environment variable.

**Verification**

I inspected the alert log to determine whether the script generated an alert when the measured CPU usage exceeded the temporary threshold.

After testing, I restored the intended threshold.

**Lesson Learned**

The absence of an alert does not necessarily mean that monitoring is broken. The measured value, configured threshold, and alert logic must all be checked.

## 6. Issue 5: Cron Job Did Not Produce Monitoring Records

**Problem**

The monitoring script worked when executed manually, but scheduled runs did not appear in the log file.

**Possible Cause**

The cron configuration used an incorrect script path or relied on environment variables that were unavailable during scheduled execution.

**Investigation**

I reviewed the scheduled tasks:

```bash
crontab -l
```

I also checked the script path and inspected the log files for errors.

**Solution**

I updated the cron entry to use absolute paths. The example below must be adjusted to match the actual username and project directory.

```cron
*/5 * * * * /home/YOUR_USERNAME/linux-monitoring-system/scripts/monitor.sh >/dev/null 2>>/home/YOUR_USERNAME/linux-monitoring-system/logs/cron-errors.log
```

**Verification**

I checked the crontab again and inspected the metrics and error logs after allowing time for the next scheduled execution.

```bash
crontab -l
tail -n 20 ~/linux-monitoring-system/logs/metrics.log
tail -n 20 ~/linux-monitoring-system/logs/cron-errors.log
```

**Lesson Learned**

Cron jobs should use absolute paths and capture errors so that scheduled execution problems can be investigated.

## 7. General Troubleshooting Best Practices

The following practices help make troubleshooting more effective:

* Read the complete error message before attempting a fix.
* Check file permissions and paths when scripts fail to execute.
* Verify that required dependencies are installed.
* Inspect logs before changing the monitoring configuration.
* Test alert logic using controlled thresholds.
* Use absolute paths in cron jobs.
* Repeat the original test after applying a fix.
* Document the root cause and the verification result.

## 8. Conclusion

Troubleshooting is an important part of Linux system administration. Problems involving permissions, missing dependencies, log files, alert thresholds, and scheduled tasks demonstrate why administrators need to understand both the monitoring scripts and the operating system.

By investigating errors systematically, applying targeted fixes, and verifying the results, the monitoring system becomes easier to maintain and more reliable.
