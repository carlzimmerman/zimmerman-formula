#!/usr/bin/env python3
"""BF2 step 3: RQ3's scorecard on a candidate, outputs in this lane. Usage: bf2_accept.py path [--no-keys] [--no-bullet]. kappa = 1/2 FITTED; not theory closed."""
import os, sys
from bf2_common import *
A = rq3(); p = [a for a in sys.argv[1:] if not a.startswith("--")][0]; o = A.scorecard(p, "--no-keys" not in sys.argv, "--no-bullet" not in sys.argv); print("\n".join(A.write(o, os.path.basename(p)[:-3])))
