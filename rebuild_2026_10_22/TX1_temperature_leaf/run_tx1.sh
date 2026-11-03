#!/bin/bash
# python3 -I, nice 19, one chain per footing; at most 2 processes. kappa = 1/2 FITTED; not theory closed.
F=$1; L=$2; shift 2
for a in "$@"; do
  nice -n 19 python3 -I tx1_search.py $F $a $L > chunks/log_${L}_${F}_$a.search 2>&1 && nice -n 19 python3 -I tx1_read.py $F $a $L > chunks/log_${L}_${F}_$a.read 2>&1
done
