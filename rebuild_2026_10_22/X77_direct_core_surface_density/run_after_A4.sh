#!/bin/bash
# Waits for all 18 A4 seeds, then reruns X77 on every snapshot (incl. ng 64 at 1e13/1e14) and grades the all-ng-64
# native eta table in X74's grader at both f*. Outputs renamed A4_*; nothing committed automatically.
cd "$(dirname "$0")"
R=../X48_native_cf_zoom/runs
while [ "$(ls $R/M1e1[34]_s?_ng64/done.json 2>/dev/null | wc -l | tr -d ' ')" -lt 18 ]; do sleep 600; done
sleep 1800   # let X72/X74's watcher take its turn first
PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x77_direct_eta.py > A4_x77.log 2>&1
cp x77_results.json A4_x77_results.json; cp x77.out A4_x77.out
python3 - <<'PY'
import json
S = json.load(open("A4_x77_results.json"))["summary"]
t = {"note": "X77 native eta, all ng 64 (A3 1e12 + A4 1e13/1e14), as c_f-equivalent",
     "cf_by_mass": {f"1e+{e}": S[f"1e+{e}_ng64"]["cf_equiv"] for e in (12, 13, 14)}}
json.dump(t, open("A4_x77_native_table.json", "w"), indent=1); print(t)
PY
cd ../X74_all_measured_native_cf
for fs in 0.034 0.0615; do
  X74_CF=../X77_direct_core_surface_density/A4_x77_native_table.json X73_FSTAR=$fs PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x74_native_cf.py > ../X77_direct_core_surface_density/A4_grade_fs$fs.log 2>&1
  for f in x74_results_fs${fs}_nat_s2.7774.json x74_fs${fs}_nat_s2.7774.out; do mv $f ../X77_direct_core_surface_density/A4grade_$f; done
done
echo "X77 A4 rerun done $(date)"
