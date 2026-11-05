"""SY1 arm T, W3, seed 8, complexity 22, 2 fitted floats frozen at train. A description of data, not a theory; no action. kappa = 1/2 FITTED."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import sy1_leaves as _L
EXPR = 'square(inv1p(log1p(log1p(square(square((ell / square(square(ell / -7.757326467390685e-5))) - sqrt(ell / 3.1999595844785746e-5)))))) + one) - half'; WRAP = 3; NAME = "SY1 arm T " + EXPR; VERTICAL = ("R",); TRAINED_ON = ("xcop_train", "sparc_train")
def g(Q): return _L.g_of_Q(EXPR, WRAP, Q)
