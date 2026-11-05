"""SY1 arm T, W3, seed 3, complexity 21, 2 fitted floats frozen at train. A description of data, not a theory; no action. kappa = 1/2 FITTED."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import sy1_leaves as _L
EXPR = 'log1p((sqrt(sqrt(sqrt(ell)) + log1p(square(square(square(log1p(square(ell / (-5.571613320203218e-6 + ell)))))))) / 0.07423912573770805) - f)'; WRAP = 3; NAME = "SY1 arm T " + EXPR; VERTICAL = ("R",); TRAINED_ON = ("xcop_train", "sparc_train")
def g(Q): return _L.g_of_Q(EXPR, WRAP, Q)
