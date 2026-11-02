#!/bin/bash
# HF1 gates 2-3, numbers only. m 5 by R3; m 11.8 is a reported comparator (README). omega values read from hf1_g1_results.json.
cd "$(dirname "$0")"; export PYTHONHASHSEED=0 OMP_NUM_THREADS=1
V=$(python3 -I -c "import json;j=json.load(open('hf1_g1_results.json'))['rows'];print(j['FDY']['FDY_m5']['omega_f'],j['FDY']['FDY_m5']['omega_b'],j['FD']['FD_m11.8']['omega_f'],j['FD']['FD_m11.8']['omega_b'])"); set -- $V
nice -n 10 python3 -I hf1_g23.py run 5 $1 $2 > run_g23_m5.log 2>&1 &
HF1_SFX=_m11p8 nice -n 10 python3 -I hf1_g23.py run 11.8 $3 $4 > run_g23_m11p8.log 2>&1 &
nice -n 10 python3 -I hf1_g23.py mutate 5 $1 $2 > run_g23_mut.log 2>&1 &
wait; echo G23DONE > run_g23.done
