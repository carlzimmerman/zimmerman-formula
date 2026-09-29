#!/bin/bash
# CFG167 re-run (under two minutes). export ZF_REPO=<repo root> first. Exit codes: main 0; MUTATE 1-4 exit 1 (bite); MUTATE 5 exit 0 (informational).
cd "$(dirname "$0")"
python3 CFG167_referee_diff_p4.py > CFG167_main.out; echo "main rc=$?"
for k in 1 2 3 4 5; do MUTATE=$k python3 CFG167_referee_diff_p4.py > CFG167_MUTATE_$k.out; echo "MUTATE $k rc=$?"; done
python3 CFG167_attacks_ac.py 167 > CFG167_attacks_ac.out; echo "attacks 167 rc=$?"
python3 CFG167_power_bd.py 167 > CFG167_power_bd.out; echo "power 167 rc=$?"
python3 CFG167_attacks_ac.py 168 > CFG167_attacks_ac_seed168.out; echo "attacks 168 rc=$?"
python3 CFG167_power_bd.py 168 > CFG167_power_bd_seed168.out; echo "power 168 rc=$?"
python3 CFG167_diag_post.py > CFG167_diag_post.out; echo "diag rc=$?"
