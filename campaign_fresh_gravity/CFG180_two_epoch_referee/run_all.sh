#!/bin/bash
# CFG180 full re-run.  Usage: ZF_REPO=<repo> bash run_all.sh   (run in the directory holding these scripts; ~6 min)
: "${ZF_REPO:?set ZF_REPO to the repo root}"
cd "$(dirname "$0")"
export PYTHONDONTWRITEBYTECODE=1
python3 CFG180_two_epoch_referee.py > CFG180_main.out;                echo "main rc=$? (0 = C1,C2 pass)"
for k in 1 2 3 4 5 6; do MUTATE=$k python3 CFG180_two_epoch_referee.py > CFG180_MUTATE_$k.out; echo "MUTATE $k rc=$? (1 = bites)"; done
python3 CFG180_attacks_A.py > CFG180_attacks_A.out;                   echo "attacks A rc=$?"
SEED=181 python3 CFG180_attacks_A.py > CFG180_attacks_A_seed181.out;  echo "attacks A seed181 rc=$?"
python3 CFG180_attacks_B.py > CFG180_attacks_B.out;                   echo "attacks B rc=$?"
for s in 1.42 1.00; do for sd in 180 181; do SEED=$sd python3 CFG180_null_mocks.py $s > CFG180_null_mocks_s${s}_seed${sd}.out; echo "mocks s=$s seed=$sd rc=$?"; done; done
for s in 1.42 1.00; do MU_K=1.5 SEED=180 python3 CFG180_null_mocks.py $s > CFG180_null_mocks_s${s}_seed180_muK1.5_POSTHOC.out; echo "mocks POSTHOC muK=1.5 s=$s rc=$?"; done
python3 CFG180_diag_post.py > CFG180_diag_post.out;                   echo "diag_post rc=$?  (post-comparison; opens CFG170 outputs)"
python3 CFG180_diag_B_nobe.py > CFG180_diag_B_nobe.out;               echo "diag_B_nobe rc=$?"
if grep -l "/Users/" CFG180_*.out CFG180_*results*.json 2>/dev/null; then echo "HOME PATH FOUND IN OUTPUT"; else echo "no absolute home path in any output"; fi
shasum -a 256 CFG180_FROZEN_CRITERIA.md CFG180_*.py run_all.sh CFG180_*.out CFG180_*results*.json > CFG180_manifest.txt
