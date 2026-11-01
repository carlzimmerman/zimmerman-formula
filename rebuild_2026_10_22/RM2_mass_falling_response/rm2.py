#!/usr/bin/env python3
"""RM2 (FROZEN_CRITERIA.md): f falling with baryon mass on NR2 MEDIAN. All numbers FITTED; kappa = 1/2 FITTED, unused; not theory closed."""
import os, sys
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(os.path.dirname(H), "RM1_response_strength_map")); import rm1n_lib
rm1n_lib.run_lane(H, "rm2", "rm2_tail_add.py", "MUTATE" if os.environ.get("RM2_MUTATE") == "1" else "RUN")
