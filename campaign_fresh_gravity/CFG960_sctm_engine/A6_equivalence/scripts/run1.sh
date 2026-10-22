#!/bin/bash
# run1.sh ENGINE OUTDIR N [MAXSTEPS] [extra env...]
ENG=$1; OUT=$2; N=$3; MX=${4:-100000}; shift 4
mkdir -p $OUT
env CFG960_OWNB=fret MallocSpaceEfficient=1 OMP_NUM_THREADS=1 CFG596_THREADS=1 CFG596_MODE=lean CFG596_L=100 CFG596_NSEED=$N CFG596_RMIN=0.78125 CFG596_CKPT=1 CFG596_SPILL=1 CFG960_RSSMAX=6 CFG596_WORK=$OUT CFG654_INPUTS=native_cmb CFG960_CONVERT=1 CFG960_M3=1 CFG960_MUTATE=none CFG596_MAXSTEPS=$MX "$@" nice -n 10 /usr/bin/time -l python3 $ENG SCT canonical $N > $OUT/engine.log 2>&1
echo "rc $?" >> $OUT/engine.log
