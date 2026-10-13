#!/bin/sh
# CFG679D unattended chain: KiDS twin (main + MUTATE), then the metacal source download after the stellar-mass one ends.
cd "$(dirname "$0")"
nice -n 10 python3 cfg679_kids_twin.py > cfg679_kids_twin.out 2>&1
CFG679_MUTATE=1 nice -n 10 python3 cfg679_kids_twin.py > cfg679_kids_twin_MUTATE.out 2>&1
echo TWIN_DONE
