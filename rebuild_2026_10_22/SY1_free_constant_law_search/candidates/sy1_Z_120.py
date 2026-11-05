"""SY1 arm Z, W1, seed 2, complexity 24, 0 fitted floats frozen at train. A description of data, not a theory; no action. kappa = 1/2 FITTED."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import sy1_leaves as _L
EXPR = 'half + log1p(square(inv1p(f) - square(log1p(square(square(square((two / s) * square(square(square(f * pi_) * y)))))))))'; WRAP = 1; NAME = "SY1 arm Z " + EXPR; VERTICAL = ("R",); TRAINED_ON = ("xcop_train", "sparc_train")
def g(Q): return _L.g_of_Q(EXPR, WRAP, Q)
