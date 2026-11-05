"""SY1 arm Z, W3, seed 8, complexity 27, 0 fitted floats frozen at train. A description of data, not a theory; no action. kappa = 1/2 FITTED."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import sy1_leaves as _L
EXPR = 'square(inv1p(inv1p(log1p(square(log1p(square(square(square(square(square(y * square(f * pi_)) * log1p(square(f / s) * two)))))))))) * two)'; WRAP = 3; NAME = "SY1 arm Z " + EXPR; VERTICAL = ("R",); TRAINED_ON = ("xcop_train", "sparc_train")
def g(Q): return _L.g_of_Q(EXPR, WRAP, Q)
