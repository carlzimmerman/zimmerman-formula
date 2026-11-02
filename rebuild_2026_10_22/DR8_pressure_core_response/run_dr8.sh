#!/bin/bash
# DR8 part B: core seeds 1-5, NFW 1-3, each with and without the disc; one no-disc core to 13.8 Gyr; MUTATE M_d x 2. Ten at a time, one thread each, nice 15. SIGTERM -> checkpoint, exit 75; rerun this script to resume.
cd "$(dirname "$0")/runs"; export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
J=(); add() { J+=("$*"); }
add core 1 _nodisc 0 13.8; add core 1 "" 1 7.7; add core 1 _MUTATE 2 7.7
for s in 2 3; do add core $s _nodisc 0 7.7; add core $s "" 1 7.7; done
add nfw 1 _nodisc 0 7.7; add nfw 1 "" 1 7.7
for s in 4 5; do add core $s _nodisc 0 7.7; add core $s "" 1 7.7; done
for s in 2 3; do add nfw $s _nodisc 0 7.7; add nfw $s "" 1 7.7; done
runone() { set -- $1; k=$1; s=$2; if [ $# -eq 5 ]; then t=$3; m=$4; T=$5; else t=""; m=$3; T=$4; fi; W=${k}_s${s}${t}; mkdir -p $W; exec nice -n 15 python3 ../dr8_live.py --kind $k --seed $s --work $W --T $T --md-mult $m --centre com --stops 3.85,7.7 --resume >> $W/run.log 2>&1; }
export -f runone
printf '%s\n' "${J[@]}" | xargs -P 10 -I{} bash -c 'runone "{}"' &
P=$!; trap 'pkill -TERM -P $P; pkill -TERM -f "dr8_live.py"; wait; exit 75' TERM INT; wait $P; echo "DR8 runs finished $(date)"
