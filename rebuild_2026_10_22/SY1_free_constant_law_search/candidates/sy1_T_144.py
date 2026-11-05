"""SY1 arm T, W3, seed 7, complexity 20, 2 fitted floats frozen at train. A description of data, not a theory; no action. kappa = 1/2 FITTED."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import sy1_leaves as _L
EXPR = 'sqrt(log1p(square(square(log1p(square(square(square(square((square(f) / -0.07519557163710225) * log1p(y))) / s)))) + -1.3263867702678112)))'; WRAP = 3; NAME = "SY1 arm T " + EXPR; VERTICAL = ("R",); TRAINED_ON = ("xcop_train", "sparc_train")
def g(Q): return _L.g_of_Q(EXPR, WRAP, Q)
