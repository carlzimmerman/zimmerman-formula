#!/bin/bash
cd /Users/carlzimmerman/new_physics/zimmerman-formula/qwen_claude_field_theory/closure_2026/fried_chicken_final/fc_alpha2_aniso
# wait for opt2 cache
until [ -f L2dc_methodB_opt2_cache.pkl ]; do sleep 5; done
echo "opt2 cache ready, launching grid" > grid_opt2_status.txt
python3 -u drive_methodB.py fc_alpha2_methodB_opt2 > grid_opt2.out 2>&1
echo "GRID_OPT2_DONE" >> grid_opt2_status.txt
