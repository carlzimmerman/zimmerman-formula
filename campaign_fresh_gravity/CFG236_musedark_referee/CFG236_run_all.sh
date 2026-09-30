#!/bin/bash
# CFG236: re-run everything from the scratch directory.  ZF_REPO=<repo> if the repo is not found automatically.
# main exits 0; MUTATE exits 1 when the control bites (so a non-zero exit is expected for M1, M2, M4, M5, M6, M7 and 0 for M3, whose frozen prediction failed).
cd "$(dirname "$0")"
python3 CFG236_main.py
SEED=237 CFG236_SUFFIX=_seed237 python3 CFG236_main.py
for k in 1 2 3 4 5 6 7; do MUTATE=$k python3 CFG236_MUTATE.py; echo "MUTATE M$k exit $?"; done
python3 CFG236_attack_b.py
python3 CFG236_attack_c.py
python3 CFG236_attack_d.py
python3 CFG236_attack_e.py
python3 CFG236_attack_f.py
# post-run only (opens CFG198 / CFG199 scripts and outputs; written after all of the above were saved):
# python3 CFG236_compare.py
