"""The a0 law, nu(y) = 1/2 + sqrt(1/4 + 1/y). kappa = 1/2 FITTED. RQ2_MUTATE=1: a0 x 1.5, still labelled the law, must fail KA1."""
import os
import numpy as np
NAME = "a0 law"; VERTICAL = ("R", "A"); AX = 1.5 if os.environ.get("RQ2_MUTATE") == "1" else 1.0
def g(Q):
    gb = np.asarray(Q["gb"], float); a = Q["a0"] * AX
    with np.errstate(all="ignore"): return np.where(gb > 0, gb * (0.5 + np.sqrt(0.25 + a / np.where(gb > 0, gb, 1.0))), gb)
