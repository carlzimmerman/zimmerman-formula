"""LE1 MUTATE candidate: twice the a0 law's g, so the lensing mass and Delta Sigma double. A control, not a proposal. kappa = 1/2 FITTED."""
import numpy as np
NAME = "LE1 MUTATE law x 2"; VERTICAL = ("R",)
def g(Q):
    gb = np.asarray(Q["gb"], float); a = Q["a0"]
    with np.errstate(all="ignore"): return 2.0 * np.where(gb > 0, gb * (0.5 + np.sqrt(0.25 + a / np.where(gb > 0, gb, 1.0))), gb)
