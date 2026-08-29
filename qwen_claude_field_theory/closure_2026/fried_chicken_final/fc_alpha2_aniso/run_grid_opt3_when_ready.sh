#!/bin/bash
cd /Users/carlzimmerman/new_physics/zimmerman-formula/qwen_claude_field_theory/closure_2026/fried_chicken_final/fc_alpha2_aniso
until [ -f L2dc_methodB_opt3_cache.pkl ]; do sleep 5; done
echo "opt3 cache ready" > grid_opt3_status.txt
python3 -u drive_methodB.py fc_alpha2_methodB_opt3 > grid_opt3.out 2>&1
echo "GRID_OPT3_DONE" >> grid_opt3_status.txt
