#!/bin/bash
# XJ1R: test the first part (prim z 2.2 seed 0 canonical) before the runner is left unattended (criteria section 9): run it
# until its base box and one forced box are written, then SIGTERM (it stops between boxes, exit 75); run_r.sh resumes it.
# kappa = 1/2 FITTED; not theory closed. Adopts nothing.
cd "$(dirname "$0")"; mkdir -p logs
export XJ1R_THREADS=3 XJ1R_MEM_GB=16 XJ1R_FOOT_GB=14
tag=prim_z2.2_s0_canonical
nice -n 19 python3 -I -B xj1r_run.py prim 2.2 0 canonical & pid=$!
echo "test $tag pid $pid ($(date +%H:%M))"
while kill -0 $pid 2>/dev/null; do
  if [ -f tmp/$tag/base.json ] && [ "$(ls tmp/$tag/b*.json 2>/dev/null | wc -l)" -ge 1 ]; then kill -TERM $pid; break; fi
  sleep 5
done
wait $pid; echo "test $tag rc $? ($(date +%H:%M)); files: $(ls tmp/$tag 2>/dev/null | tr '\n' ' ')"
# kappa = 1/2 FITTED; not theory closed. Adopts nothing.
