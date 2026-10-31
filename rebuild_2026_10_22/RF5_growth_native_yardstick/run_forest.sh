#!/bin/bash
# RF5 forest + shear channels: at most four single-thread processes, high z_on first; each cell resumes per table.
cd "$(dirname "$0")"
export PYTHONHASHSEED=0 OMP_NUM_THREADS=1
printf '%s\n' "$@" | xargs -P 4 -I{} nice -n 15 python3 -I rf5.py channel {} >> forest.log 2>&1
