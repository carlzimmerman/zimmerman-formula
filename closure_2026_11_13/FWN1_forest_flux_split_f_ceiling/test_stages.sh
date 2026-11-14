#!/bin/bash
# FWN1: test the first part of each later stage before the runner reaches it (criteria section 10): run the part until its
# base box and one forced box are written, then SIGTERM (it stops between boxes, exit 75); the runner resumes it later.
cd "$(dirname "$0")"
export FWN1_THREADS=3 FWN1_MEM_GB=16
t() {
  tag="$1_z$2_s$3_$4"
  nice -n 19 python3 -I -B fwn1_run.py "$@" & pid=$!
  echo "test $tag pid $pid ($(date +%H:%M))"
  while kill -0 $pid 2>/dev/null; do
    if [ -f tmp/$tag/base.json ]; then kill -TERM $pid; break; fi
    sleep 5
  done
  wait $pid; echo "test $tag rc $? ($(date +%H:%M)); files: $(ls tmp/$tag 2>/dev/null | tr '\n' ' ')"
}
t fin 2.2 0 canonical
t oz 3.0 0 canonical
t bracketF 2.2 0 canonical
t clusteredF 2.2 0 canonical
