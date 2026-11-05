"""SY1 arm T, W3, seed 1, complexity 22, 2 fitted floats frozen at train. A description of data, not a theory; no action. kappa = 1/2 FITTED."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import sy1_leaves as _L
EXPR = '0.6268828928586322 + log1p(log1p(square(inv1p(f) - square(square(log1p(square(square(square(inv1p(-5.185953027091412e-6 / ell)))))))) * sqrt(inv1p(y))))'; WRAP = 3; NAME = "SY1 arm T " + EXPR; VERTICAL = ("R",); TRAINED_ON = ("xcop_train", "sparc_train")
def g(Q): return _L.g_of_Q(EXPR, WRAP, Q)
