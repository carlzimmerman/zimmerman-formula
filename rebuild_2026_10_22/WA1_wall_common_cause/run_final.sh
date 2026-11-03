#!/bin/bash
# fit -> rows at the fit -> checks -> MUTATE checks -> final -> byte-identical rerun of final -> report. One thread, nice 19.
cd "$(dirname "$0")"; export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
nice -n 19 python3 wa1_fit.py fit > final.log 2>&1; echo "fit $?" > final.status
for c in LAW UX3 P3 P7 MX1 BK2 CAL; do for f in canonical alt; do nice -n 19 python3 wa1_hat.py $c $f >> final.log 2>&1; done; done; echo "hat $?" >> final.status
nice -n 19 python3 wa1_fit.py k > wa1_checks.out 2>&1; echo "checks $?" >> final.status
WA1_MUTATE=1 nice -n 19 python3 wa1_fit.py k > wa1_checks_MUTATE.out 2>&1; echo "mutate $?" >> final.status
nice -n 19 python3 wa1_fit.py final >> final.log 2>&1; echo "final $?" >> final.status
python3 -c "import hashlib;print('sha1', hashlib.sha256(open('wa1_results.json','rb').read()).hexdigest())" >> final.status
nice -n 19 python3 wa1_fit.py final >> final.log 2>&1; echo "rerun $?" >> final.status
python3 -c "import hashlib;print('sha', hashlib.sha256(open('wa1_results.json','rb').read()).hexdigest())" >> final.status
nice -n 19 python3 wa1_report.py >> final.log 2>&1; echo "report $?" >> final.status; echo finished >> final.status
