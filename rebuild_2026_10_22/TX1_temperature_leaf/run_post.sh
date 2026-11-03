#!/bin/bash
# POST and sensitivities, after run_keys.sh. One driver at a time. kappa = 1/2 FITTED; not theory closed.
until [ -f chunks/keys.done ]; do sleep 30; done
for F in canonical alt; do
  [ -f tx1_keys_${F}_post.json ] || nice -n 19 python3 -I tx1_keys.py $F real chunks/lists/${F}_post.json tx1_keys_${F}_post.json > chunks/log_keys_${F}_post 2>&1
  [ -f tx1_keys_${F}_top3_median.json ] || nice -n 19 python3 -I tx1_keys.py $F real chunks/lists/${F}_top3.json tx1_keys_${F}_top3_median.json median > chunks/log_keys_${F}_top3_median 2>&1
  [ -f tx1_keys_${F}_top3_cut.json ] || TX1_TAILCUT=1 nice -n 19 python3 -I tx1_keys.py $F real chunks/lists/${F}_top3.json tx1_keys_${F}_top3_cut.json > chunks/log_keys_${F}_top3_cut 2>&1
done; echo done > chunks/post.done
