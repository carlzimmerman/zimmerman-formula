#!/bin/bash
# CFG239 re-run (scratch mirror; nothing in the repo is written).  Usage: ZF_REPO=<repo> CFG239_WORK=<scratch dir outside the repo> ./CFG239_run_all.sh
# Wall time about 75 min at 10 fit jobs on a 16-core machine (fits dominate: about 30 s each, 500 of them); the pipeline fits are cached by CSV hash.
set -u
cd "$(dirname "$0")"
export CFG239_JOBS=${CFG239_JOBS:-10}
r() { echo ">>> $*"; "$@"; echo "exit=$?"; }
r python3 -B CFG239_c1_mechanism.py
MUTATE=2 r python3 -B CFG239_c1_mechanism.py   # expected exit 1 (control bites)
MUTATE=3 r python3 -B CFG239_c1_mechanism.py   # expected exit 1
r python3 -B CFG239_c2_flips.py
MUTATE=4 r python3 -B CFG239_c2_flips.py       # expected exit 1
MUTATE=5 r python3 -B CFG239_c2_flips.py       # expected exit 1
r python3 -B CFG239_c3_fits.py --part g100
r python3 -B CFG239_c3_fits.py --part ladder
r python3 -B CFG239_c3_fits.py --part mu1
MUTATE=1 r python3 -B CFG239_c3_fits.py        # expected exit 1
r python3 -B CFG239_c3_fits.py --part thin
MUTATE=6 r python3 -B CFG239_c3_fits.py        # expected exit 1
r python3 -B CFG239_c4_streams.py
MUTATE=7 r python3 -B CFG239_c4_streams.py     # expected exit 1
# POST HOC (written after the runs above were saved)
r python3 -B CFG239_c3_fits.py --part thin2
r python3 -B CFG239_c5_posthoc.py
# POST-RUN UNBLINDING COMPARE (opens the calc chat's on-disk per-build catalogues; run last)
r python3 -B CFG239_post_compare.py
