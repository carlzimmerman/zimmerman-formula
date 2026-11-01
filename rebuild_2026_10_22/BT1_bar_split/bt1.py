#!/usr/bin/env python3
"""BT1 (FROZEN_CRITERIA.md): per-galaxy Upsilon on NR2 MEDIAN. kappa = 1/2 FITTED, unused; not theory closed."""
import os, sys
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(os.path.dirname(H), "RM1_response_strength_map")); import rm1n_lib
rm1n_lib.run_lane(H, "bt1", "bt1_tail_add.py", "RUN")
