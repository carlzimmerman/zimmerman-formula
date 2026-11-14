#!/bin/bash
# FWN1: the runner stopped at its swap guard (criteria section 10: stop above 8 GB swap used). Wait, checking every 2 min,
# until swap used <= 8 GB and free disk >= 8 GB, then relaunch run_all.sh (it skips finished parts and resumes box files).
# Repeats after any further guard stop (exit 4 / 3), until run_all.done exists. Logs every check.
cd "$(dirname "$0")"
while [ ! -f run_all.done ]; do
  swap=$(sysctl -n vm.swapusage | sed -E 's/.*used = ([0-9.]+)M.*/\1/'); avail=$(df -g . | awk 'NR==2 {print $4}')
  if [ "$(echo "$swap <= 8192" | bc)" -eq 1 ] && [ "$avail" -ge 8 ]; then
    echo "relaunch $(date +%H:%M): swap ${swap} MB, disk ${avail} GB"
    ./run_all.sh >> logs/run_all.log 2>&1 & echo $! > logs/run_all.pid; wait $!; rc=$?
    echo "runner rc $rc $(date +%H:%M)"
    if [ $rc -ne 3 ] && [ $rc -ne 4 ] && [ ! -f run_all.done ]; then echo "runner stopped with rc $rc: not relaunching"; exit $rc; fi
  else
    echo "wait $(date +%H:%M): swap ${swap} MB, disk ${avail} GB"; sleep 120
  fi
done
echo "run_all.done $(date +%H:%M)"
