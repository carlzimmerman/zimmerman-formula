#!/bin/bash
cd /Users/carlzimmerman/new_physics/zimmerman-formula/qwen_claude_field_theory/closure_2026/fried_chicken_final/fc_alpha2_aniso
until [ -f L2dc_methodB_cache.pkl ]; do sleep 5; done
echo "opt1 cache ready, launching grid" > grid_opt1_status.txt
python3 -u drive_methodB.py fc_alpha2_methodB_2026 > grid_opt1.out 2>&1
echo "GRID_OPT1_DONE" >> grid_opt1_status.txt
