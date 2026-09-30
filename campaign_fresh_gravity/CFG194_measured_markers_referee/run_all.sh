#!/bin/bash
# CFG194 re-run: ZF_REPO=<repo> bash run_all.sh   (whole set ~ 12 min; the two mock runs are the bulk)
set -u
cd "$(dirname "$0")"
: "${ZF_REPO:?set ZF_REPO}"
export ZF_REPO
python3 CFG194_referee_main.py > CFG194_main.out 2> CFG194_main.err; echo "main rc=$? (0 = own controls pass)"
python3 CFG194_referee_main.py > CFG194_main_rerun.out 2>/dev/null; cmp CFG194_main.out CFG194_main_rerun.out && echo "main deterministic (byte-identical)"; rm -f CFG194_main_rerun.out
for k in 1 2 3 4 5 6; do MUTATE=$k python3 CFG194_referee_main.py > CFG194_MUTATE_$k.out 2> CFG194_MUTATE_$k.err; echo "MUTATE $k rc=$? (1 = bites)"; done
python3 CFG194_attacks_a.py > CFG194_attacks_a.out 2> CFG194_attacks_a.err; echo "attacks_a rc=$?"
python3 CFG194_attacks_c.py 194 > CFG194_attacks_c_seed194.out 2> CFG194_attacks_c_seed194.err; echo "attacks_c 194 rc=$?"
python3 CFG194_attacks_c.py 195 > CFG194_attacks_c_seed195.out 2> CFG194_attacks_c_seed195.err; echo "attacks_c 195 rc=$?"
# post-comparison (written after CFG189's and CFG184's files were opened; labelled, not part of any frozen result)
[ -f CFG194_bs_post.py ] && { python3 CFG194_bs_post.py > CFG194_bs_post.out 2> CFG194_bs_post.err; echo "bs_post rc=$?"; }
[ -f CFG194_diag_post.py ] && { python3 CFG194_diag_post.py > CFG194_diag_post.out 2> CFG194_diag_post.err; echo "diag_post rc=$?"; }
grep -l "/Users/" CFG194_*.out CFG194_*.json 2>/dev/null && echo "HOME PATH LEAK" || echo "no absolute home path in any output"
