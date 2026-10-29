#!/bin/bash
# Light watcher (one ls every 10 min): when all 18 A4 seeds (ng64, 1e13/1e14) have done.json, run X72's frozen
# post-A4 script (it builds the A4 c_f table), then X74's. Log to watch_A4.log. No heavy work while A4 is live.
cd "$(dirname "$0")"
R=../X48_native_cf_zoom/runs
while [ "$(ls $R/M1e1[34]_s?_ng64/done.json 2>/dev/null | wc -l | tr -d ' ')" -lt 18 ]; do sleep 600; done
echo "A4 complete $(date)"
bash ../X72_smooth_core_native_cf/run_after_A4.sh
bash run_after_A4.sh
echo "post-A4 regrades done $(date)"
