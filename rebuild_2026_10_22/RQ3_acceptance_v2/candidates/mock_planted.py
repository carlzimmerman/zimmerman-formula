"""MOCK, not a proposal. The law, with g x 10^0.25 below g_b = a0/10. Must fail A9, which the law passes. Reads no label."""
import numpy as np
NAME = "mock planted"; VERTICAL = ("R",)
def g(Q):
    gb = np.asarray(Q["gb"], float); a = Q["a0"]
    with np.errstate(all="ignore"): L = np.where(gb > 0, gb * (0.5 + np.sqrt(0.25 + a / np.where(gb > 0, gb, 1.0))), gb)
    return np.where(gb < a / 10, L * 10 ** 0.25, L)
