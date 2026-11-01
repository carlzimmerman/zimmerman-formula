#!/usr/bin/env python3
"""JC2 (FROZEN_CRITERIA.md): stellar term on NR2 MEDIAN. JC2_MUTATE=1 twin. kappa = 1/2 FITTED, unused; not theory closed."""
import os, sys
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(os.path.dirname(H), "RM1_response_strength_map")); import rm1n_lib
rm1n_lib.run_lane(H, "jc2", "jc2_tail_add.py", "MUTATE" if os.environ.get("JC2_MUTATE") == "1" else "RUN")
