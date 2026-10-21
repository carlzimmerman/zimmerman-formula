#!/bin/bash
# CFG935 runner: one part per process, one at a time, one core, nice 10 (FROZEN_CRITERIA §7, A0.3; A1, A2 code).
# K and MUTATE first, then the main runs, the post-hoc P0_L control, then the summary. Log: parts/run_935.log
cd "$(dirname "$0")" || exit 2
mkdir -p parts
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 MKL_NUM_THREADS=1
LOG=parts/run_935.log
run() {
  echo "=== $(date '+%F %T') part $1 ===" >> "$LOG"
  nice -n 10 python3 cfg935.py "$1" >> "$LOG" 2>&1
  rc=$?
  echo "=== $(date '+%F %T') part $1 rc $rc ===" >> "$LOG"
}
PARTS_LIST=${PARTS_LIST:-"K0 K2 ETH PHYS MUTATE Ra2_L Ra2_I Ra2_S Rd_L Rd_I Rd_S Rb_L Rb_I Rb_S Rc_L Rc_I Rc_S Ra1_L Ra1_I Ra1_S Ra1x100_I P0_L PHou_L PHou_I"}
for p in $PARTS_LIST; do
  if [ "$p" = MUTATE ]; then
    echo "=== $(date '+%F %T') MUTATE ===" >> "$LOG"
    CFG935_MUTATE=1 nice -n 10 python3 cfg935.py >> "$LOG" 2>&1
    rc=$?
    echo "=== $(date '+%F %T') MUTATE rc $rc (1 = all teeth bite) ===" >> "$LOG"
  else
    run "$p"
  fi
done
run summary
echo "=== $(date '+%F %T') DONE ===" >> "$LOG"
