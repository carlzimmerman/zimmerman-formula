"""MOCK, not a proposal. The law, doubled if the sample label says cluster. Must carry [LABEL]."""
import numpy as np
NAME = "mock label"; VERTICAL = ("R",)
def g(Q):
    gb = np.asarray(Q["gb"], float); a = Q["a0"]
    with np.errstate(all="ignore"): L = np.where(gb > 0, gb * (0.5 + np.sqrt(0.25 + a / np.where(gb > 0, gb, 1.0))), gb)
    return L * 2.0 if Q["sample"] == "cluster" else L
