#!/bin/bash
# FRZ6R: frozen stages in order (FROZEN_CRITERIA.md section 4). One job, nice 19, 2 threads. Restartable.
# S1 = primary seeds 0, 1, 2 (all 12 bins); S2 = primary seed 3; S3 = brackets (anchors, seeds 0, 1).
cd "$(dirname "$0")"
check() {
  free=$(df -g . | awk 'NR==2{print $4}')
  swap=$(sysctl -n vm.swapusage | sed -E 's/.*used = ([0-9.]+)M.*/\1/')
  echo "check before $1: free disk ${free} GB, swap used ${swap} MB"
  if [ "$free" -lt 8 ]; then echo "STOP: free disk below 8 GB"; exit 2; fi
  if [ "$(echo "$swap > 8192" | bc)" = "1" ]; then echo "STOP: swap used above 8 GB"; exit 3; fi
}
stage() {
  for i in $(seq 1 300); do
    check "$*"
    nice -n 19 python3 -I -B frz6r_run.py "$@"; rc=$?
    [ $rc -eq 0 ] && return 0
    [ $rc -ne 75 ] && { echo "stage $* exited $rc"; exit $rc; }
    :
  done
  exit 4
}
stage prim 0 1 2
stage prim 3
stage br
touch run_all.done
