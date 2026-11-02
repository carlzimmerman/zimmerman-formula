#!/bin/bash
# One thread, nice 19, one cell after another; Bullet is computed in mx1_bullet.py with the cold placed, so the harness's map row is off here.
cd "$(dirname "$0")"
for c in "$@"; do OMP_NUM_THREADS=1 nice -n 19 python3 mx1_acc.py cand_$c.py --no-bullet > acc_$c.log 2>&1; echo "$c $?" >> acc_status.log; done
