#!/bin/bash
# CFG183 re-run. usage: ZF_REPO=<repo> bash run_all.sh   (run inside the directory holding these scripts)
# expected exit codes: main 0; stability 0; MUTATE 1-8 exit 1 (each bites); attacks 0; onset 0; mocks 0; compare 0 (phase 2, post-comparison)
set -u
cd "$(dirname "$0")"
python3 CFG183_referee_main.py > CFG183_main.out 2> CFG183_main.err; echo "main rc $?"
for k in 1 2 3 4 5 6 7 8; do MUTATE=$k python3 CFG183_referee_main.py > CFG183_MUTATE_$k.out 2> CFG183_MUTATE_$k.err; echo "MUTATE $k rc $?"; done
python3 CFG183_attacks_abc.py > CFG183_attacks_abc.out 2> CFG183_attacks_abc.err; echo "attacks_abc rc $?"
python3 CFG183_onset_d.py > CFG183_onset_d.out 2> CFG183_onset_d.err; echo "onset_d rc $?"
python3 CFG183_null_e.py 183 > CFG183_null_e_seed183.out 2> CFG183_null_e_seed183.err; echo "null_e seed 183 rc $?"
python3 CFG183_null_e.py 184 > CFG183_null_e_seed184.out 2> CFG183_null_e_seed184.err; echo "null_e seed 184 rc $?"
python3 CFG183_null_e_stability.py > CFG183_null_e_stability.out 2> CFG183_null_e_stability.err; echo "stability rc $?"
python3 CFG183_compare.py > CFG183_compare.out 2> CFG183_compare.err; echo "compare rc $? (post-comparison; opens the CFG175 files)"
