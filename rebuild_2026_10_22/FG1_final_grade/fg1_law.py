#!/usr/bin/env python3
"""FG1 (FROZEN_CRITERIA.md): the law's Tl and LT on UR2's path. FG1_MUTATE=1 twin. kappa = 1/2 FITTED; not theory closed."""
import os, sys
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(os.path.dirname(H), "RM1_response_strength_map")); import rm1n_lib
rm1n_lib.run_lane(H, "fg1law", "fg1_law_tail_add.py", "MUTATE" if os.environ.get("FG1_MUTATE") == "1" else "RUN")
