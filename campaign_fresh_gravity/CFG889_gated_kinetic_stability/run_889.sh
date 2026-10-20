#!/bin/bash
# CFG889 runner: one part per process, one core, niced; each part < 10 min, < 2 GB.  Log: parts/run_889.log
cd "$(dirname "$0")"
export OMP_NUM_THREADS=1
log=parts/run_889.log; mkdir -p parts; : > "$log"
for p in K G1a G1b G2a G2b U1 U2 N1 N2 H1 H3; do
  echo "== part $p $(date +%H:%M:%S)" >> "$log"
  timeout 900 nice -n 10 python3 cfg889.py "$p" >> "$log" 2>&1 || echo "part $p exit $?" >> "$log"
done
echo "== MUTATE part M $(date +%H:%M:%S)" >> "$log"
CFG889_MUTATE=1 timeout 900 nice -n 10 python3 cfg889.py M >> "$log" 2>&1 || echo "part M exit $?" >> "$log"
CFG889_MUTATE=1 nice -n 10 python3 cfg889.py S >> "$log" 2>&1; echo "MUTATE summary exit $? (1 = tooth bites, by design)" >> "$log"
echo "== summary $(date +%H:%M:%S)" >> "$log"
nice -n 10 python3 cfg889.py S >> "$log" 2>&1; echo "summary exit $?" >> "$log"
echo "== done $(date +%H:%M:%S)" >> "$log"
