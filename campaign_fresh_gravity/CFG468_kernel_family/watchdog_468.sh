#!/bin/bash
# Keeps CFG468's resumable zero-field grid running until it finishes, even if the launching session ends.
# The grid skips finished arrays, so a relaunch resumes where it stopped.
cd "$(dirname "$0")/../.."
LOG=campaign_fresh_gravity/CFG468_kernel_family/cfg468_run.log
while true; do
  if ! pgrep -f "cfg468_zero_field_runs.py" >/dev/null; then
    if [ "$(tail -1 "$LOG" | cut -c1-8)" = "all done" ]; then echo "watchdog: grid finished $(date)" >> "$LOG.watchdog"; exit 0; fi
    echo "watchdog: relaunching $(date)" >> "$LOG.watchdog"
    nohup nice -n 15 python3 campaign_fresh_gravity/CFG468_kernel_family/cfg468_zero_field_runs.py >> "$LOG" 2>&1 &
  fi
  sleep 600
done
