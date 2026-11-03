#!/bin/bash
# After the first queue: Gamma 5/3 N cells again under A2, then the Bullet, its twin, the run twin, controls. Two at a time.
cd "$(dirname "$0")"
until [ -f cells.done.tmp ]; do sleep 20; done
( nice -n 19 python3 -I df3g_run.py cell 5/3 100 N > run_cell_5_3_100_N.log 2>&1; nice -n 19 python3 -I df3g_run.py cell 5/3 30 N > run_cell_5_3_30_N.log 2>&1; nice -n 19 python3 -I df3g_run.py mutate > run_mutate.log 2>&1 ) &
( nice -n 19 python3 -I df3g_bullet.py > run_bullet.log 2>&1; DF3G_MUTATE=1 nice -n 19 python3 -I df3g_bullet.py > run_bullet_MUTATE.log 2>&1; nice -n 19 python3 -I df3g_controls.py > run_controls.log 2>&1; DF3G_MUTATE=1 nice -n 19 python3 -I df3g_controls.py > run_controls_MUTATE.log 2>&1 ) &
wait; echo done > rest.done.tmp
