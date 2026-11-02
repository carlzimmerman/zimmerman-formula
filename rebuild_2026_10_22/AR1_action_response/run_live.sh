#!/bin/bash
# AR1 live validation, DR8's kernel, N 30000: arg mass 1e10, 1e13; seed 1 is the frozen run, seeds 2, 3 added for scatter because the cost turned out small; disc and no disc. Four at a time, one thread each, nice 15. SIGTERM -> checkpoint; rerun resumes.
cd "$(dirname "$0")"; mkdir -p runs; export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
for T in 1e10 1e13; do for s in 1 2 3; do echo "$T $s 1 D"; echo "$T $s 0 _nodisc"; done; done | xargs -P 4 -L 1 bash -c 'T=$0; s=$1; m=$2; t=$3; [ "$t" = D ] && t=""; W=runs/${T}_s${s}${t}; mkdir -p $W; exec nice -n 15 python3 ar1_live.py $T --kind core --seed $s --work $W --T 7.7 --md-mult $m --N 30000 --centre com --stops 3.85,7.7 --resume >> $W/run.log 2>&1'
echo "AR1 live done"
