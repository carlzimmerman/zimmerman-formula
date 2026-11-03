#!/bin/bash
# Keys one driver at a time: LW1's path writes x74 by-products in the lane root (gitignored). kappa = 1/2 FITTED; not theory closed.
for F in canonical alt; do for a in real c1 c2 c3 label; do
  [ -f tx1_keys_${F}_$a.json ] || nice -n 19 python3 -I tx1_keys.py $F $a chunks/lists/${F}_$a.json tx1_keys_${F}_$a.json > chunks/log_keys_${F}_$a 2>&1
done; done; echo done > chunks/keys.done
