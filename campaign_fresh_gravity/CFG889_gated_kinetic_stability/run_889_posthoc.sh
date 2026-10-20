#!/bin/bash
# CFG889 POST-HOC runner (added after the frozen parts): re-run part K to check the edited script reproduces it, then P1, P2, summary.
cd "$(dirname "$0")"
export OMP_NUM_THREADS=1
log=parts/run_889_posthoc.log; : > "$log"
for p in K P1 P2; do
  echo "== part $p $(date +%H:%M:%S)" >> "$log"
  timeout 900 nice -n 10 python3 cfg889.py "$p" >> "$log" 2>&1 || echo "part $p exit $?" >> "$log"
done
echo "== summary $(date +%H:%M:%S)" >> "$log"
nice -n 10 python3 cfg889.py S >> "$log" 2>&1; echo "summary exit $?" >> "$log"
echo "== done $(date +%H:%M:%S)" >> "$log"
