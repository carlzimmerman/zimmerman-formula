#!/bin/bash
# FRZ3 driver: one heavy job at a time, nice 19; restartable (finished parts are skipped). Writes run_all.done at the end.
# kappa = 1/2 FITTED; not theory closed. Adopts nothing.
cd "$(dirname "$0")" || exit 1
rm -f run_all.done
nice -n 19 python3 frz3_fields.py anchor 2.2,3.0,4.4 0,1,2,3 >> logs/fields_anchor.log 2>&1 || exit 1
nice -n 19 python3 frz3_fields.py primary 2.4,2.6,2.8,3.2,3.4,3.6,3.8,4.0,4.2 0,1 >> logs/fields_primary.log 2>&1 || exit 1
nice -n 19 python3 frz3_fields.py primary 2.4,2.6,2.8,3.2,3.4,3.6,3.8,4.0,4.2 2,3 >> logs/fields_primary.log 2>&1 || exit 1
touch run_all.done
