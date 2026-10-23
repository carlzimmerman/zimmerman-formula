#!/bin/bash
# Re-run SE-20261023's code (byte copies in this folder) with its recorded command lines.
# Run from this folder: bash run_repro.sh. Interpreter = the one SE's manifests record (Python 3.9.6, NumPy 1.26.2, SciPy 1.11.4).
set -e
PY=/usr/bin/python3
cd "$(dirname "$0")/spatial_expansion_2026_10_23"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
run(){ name=$1; shift; mkdir -p $name; /usr/bin/time -p $PY run_v2.py --output $name/result.json "$@" 2> $name/time.txt; }
run base
run space --n 12 --amp 0.001 --zi 1100 --cfl 0.6
run time --n 8 --amp 0.001 --zi 1100 --cfl 0.3
run strong --n 8 --amp 0.03 --zi 1100 --cfl 0.6
run strong_space --n 12 --amp 0.03 --zi 1100 --cfl 0.6
run strong_fine --n 16 --amp 0.03 --zi 1100 --cfl 0.6
run strong_time --n 8 --amp 0.03 --zi 1100 --cfl 0.3
run early --n 8 --amp 0.0005002271694684235 --zi 2200 --cfl 0.6
run earlier --n 8 --amp 0.0002501704158145876 --zi 4400 --cfl 0.6
mkdir -p check force summary
$PY check.py --output check/result.json
$PY force_check.py --output force/result.json
$PY summarize.py --output summary/result.json
