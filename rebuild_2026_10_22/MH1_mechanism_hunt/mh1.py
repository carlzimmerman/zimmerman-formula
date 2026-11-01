#!/usr/bin/env python3
"""MH1 (FROZEN_CRITERIA.md): MB and VDI rows on NR3's path, NR2 MEDIAN. Env MH1_PART RUN or MUTATE. kappa = 1/2 FITTED, unused; not theory closed."""
import os, sys
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(os.path.dirname(H), "RM1_response_strength_map")); import rm1n_lib
rm1n_lib.run_lane(H, "mh1", "mh1_tail_add.py", os.environ.get("MH1_PART", "RUN"))
