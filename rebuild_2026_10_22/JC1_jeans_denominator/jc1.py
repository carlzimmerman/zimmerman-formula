#!/usr/bin/env python3
"""JC1 (FROZEN_CRITERIA.md): Jeans denominator on NR2 MEDIAN. JC1_MUTATE=1 twin. kappa = 1/2 FITTED, unused; not theory closed."""
import os, sys
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(os.path.dirname(H), "RM1_response_strength_map")); import rm1n_lib
rm1n_lib.run_lane(H, "jc1", "jc1_tail_add.py", "MUTATE" if os.environ.get("JC1_MUTATE") == "1" else "RUN")
