"""MOCK, not a proposal. Returns NaN. Must read NOT COMPUTABLE on every row, zero PASS."""
import numpy as np
NAME = "mock nan"; VERTICAL = ("R", "A")
def g(Q): return np.full_like(np.asarray(Q["gb"], float), np.nan)
