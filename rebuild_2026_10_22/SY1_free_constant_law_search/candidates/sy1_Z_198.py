"""SY1 arm Z, W3, seed 1, complexity 27, 0 fitted floats frozen at train. A description of data, not a theory; no action. kappa = 1/2 FITTED."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import sy1_leaves as _L
EXPR = 'square(inv1p(square(square(square(log1p(log1p(log1p(log1p(((f / y) - f) - f)))))) / inv1p(sqrt(sqrt(D)) - (s * pi_)))) + f)'; WRAP = 3; NAME = "SY1 arm Z " + EXPR; VERTICAL = ("R",); TRAINED_ON = ("xcop_train", "sparc_train")
def g(Q): return _L.g_of_Q(EXPR, WRAP, Q)
