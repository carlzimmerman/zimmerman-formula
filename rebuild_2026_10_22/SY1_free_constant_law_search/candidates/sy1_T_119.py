"""SY1 arm T, W3, seed 6, complexity 19, 2 fitted floats frozen at train. A description of data, not a theory; no action. kappa = 1/2 FITTED."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import sy1_leaves as _L
EXPR = 'log1p((log1p(square(square(square(square(square(inv1p(-5.634538866083792e-6 / ell))))))) + inv1p(3.2945426828746815e-8 / ell)) + inv1p(f))'; WRAP = 3; NAME = "SY1 arm T " + EXPR; VERTICAL = ("R",); TRAINED_ON = ("xcop_train", "sparc_train")
def g(Q): return _L.g_of_Q(EXPR, WRAP, Q)
