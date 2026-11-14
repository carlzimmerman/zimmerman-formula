#!/bin/bash
# XJ1R light steps after the shell runs (FROZEN_CRITERIA.md section 9): caustic known answers, containment (b), tables for the
# twelve z bins (with KP1-KP7), the c0 chain per footing. nice 19, single thread. kappa = 1/2 FITTED; not theory closed. Adopts nothing.
cd "$(dirname "$0")"; mkdir -p logs
[ -f logs/shells.done ] || { echo "shell runs not complete"; exit 2; }
nice -n 19 python3 -I -B xj1r_rk.py || exit 3
nice -n 19 python3 -I -B xj1r_rc.py || exit 4
nice -n 19 python3 -I -B xj1r_tables.py 2.2 3.0 4.4 2.6 3.4 3.8 2.4 2.8 3.2 3.6 4.0 4.2 || exit 5
for f in canonical alt; do nice -n 19 python3 -I -B xj1r_c0.py $f || exit 6; done
touch logs/light.done
# kappa = 1/2 FITTED; not theory closed. Adopts nothing.
