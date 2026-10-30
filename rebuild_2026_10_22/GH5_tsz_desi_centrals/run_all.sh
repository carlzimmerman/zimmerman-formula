#!/bin/bash
# Selection, then K2, then PRIMARY, then the reported tiers, then MUTATE (one at a time).
export PYTHONHASHSEED=0 OMP_NUM_THREADS=1
D=ComptonY_deproj_cib_1.0_10.7
nice -n 15 python3 gh5_select.py
GH5_TIER=kids nice -n 15 python3 gh5_tsz_desi.py > /dev/null 2>&1; echo "kids exit $?"
for t in central clean iso3 comp08 passive sf; do GH5_MAP=$D GH5_TIER=$t nice -n 15 python3 gh5_tsz_desi.py > /dev/null 2>&1; echo "$t exit $?"; done
GH5_MAP=ComptonY GH5_TIER=central nice -n 15 python3 gh5_tsz_desi.py > /dev/null 2>&1; echo "std central exit $?"
GH5_MAP=$D GH5_TIER=central GH5_MUTATE=1 nice -n 15 python3 gh5_tsz_desi.py > /dev/null 2>&1; echo "mutate exit $?"
echo ALLDONE
