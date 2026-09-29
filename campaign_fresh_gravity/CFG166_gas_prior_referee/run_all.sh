#!/bin/bash
# CFG166 full re-run (about 6 min).  export ZF_REPO=<repo> first (or run inside the repo tree).
set -u
cd "$(dirname "$0")"
python3 CFG166_gas_prior_referee.py > CFG166_main.out; echo "main rc=$? (0 = C1-C3 and counts pass)"
for k in 0a 0b 1 2 3 4 5 6; do MUTATE=$k python3 CFG166_gas_prior_referee.py > CFG166_MUTATE_$k.out; echo "MUTATE $k rc=$? (1 = bites; 6 always 0)"; done
python3 CFG166_attacks_abcd.py > CFG166_attacks.out; echo "attacks rc=$?"
python3 CFG166_post_comparison.py > CFG166_post_comparison.out; echo "post-comparison rc=$? (needs CFG164_gas_prior_results.json in the repo)"
