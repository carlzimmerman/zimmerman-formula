#!/bin/bash
cd "$(dirname "$0")"
export PYTHONWARNINGS=ignore
python3 cfg120_A_linearity_theorem.py > cfg120_A_stdout.txt 2>&1; echo "A main rc=$?" >> rc_log.txt
MUTATE=a python3 cfg120_A_linearity_theorem.py > cfg120_A_mut_a_stdout.txt 2>&1; echo "A a rc=$?" >> rc_log.txt
MUTATE=b python3 cfg120_A_linearity_theorem.py > cfg120_A_mut_b_stdout.txt 2>&1; echo "A b rc=$?" >> rc_log.txt
