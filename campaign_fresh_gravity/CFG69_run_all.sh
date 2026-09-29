#!/bin/bash
# Runs CFG69's main harness FIRST, then the MUTATE control: the MUTATE run's C5 line reads the un-mutated results JSON that the main run writes.
cd "$(dirname "$0")/.."
python3 campaign_fresh_gravity/CFG69_lcdm_comparator.py > /dev/null 2>&1; echo "main rc=$? (expected 0)"
MUTATE=1 python3 campaign_fresh_gravity/CFG69_lcdm_comparator.py > /dev/null 2>&1; echo "mutate rc=$? (expected 1, from the declared C5)"
