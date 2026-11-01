#!/usr/bin/env python3
"""RM1 rerun on NR2 MEDIAN (AMENDMENTS A1). RM1_PART G, I. f, delta FITTED; kappa = 1/2 FITTED, unused; not theory closed."""
import os, sys
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, H); import rm1n_lib
rm1n_lib.run_lane(H, "rm1n", "rm1_tail_add.py", os.environ["RM1_PART"])
