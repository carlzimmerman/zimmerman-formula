"""Newton: g = g_b. A known-answer candidate, not a proposal. Reads no a0."""
import numpy as np
NAME = "Newton"; VERTICAL = ("R",)
def g(Q): return np.asarray(Q["gb"], float) * 1.0
