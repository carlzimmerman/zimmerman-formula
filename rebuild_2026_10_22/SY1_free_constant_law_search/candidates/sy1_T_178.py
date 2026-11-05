"""SY1 arm T, W3, seed 6, complexity 22, 2 fitted floats frozen at train. A description of data, not a theory; no action. kappa = 1/2 FITTED."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import sy1_leaves as _L
EXPR = 'log1p((inv1p(f) + square(log1p(square(log1p(square(square(square(square(inv1p(-5.638753866773053e-6 / ell)))))))))) + inv1p(square(-4.717217369820379e-8 / ell)))'; WRAP = 3; NAME = "SY1 arm T " + EXPR; VERTICAL = ("R",); TRAINED_ON = ("xcop_train", "sparc_train")
def g(Q): return _L.g_of_Q(EXPR, WRAP, Q)
