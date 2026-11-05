"""SY1 arm T, W3, seed 1, complexity 18, 2 fitted floats frozen at train. A description of data, not a theory; no action. kappa = 1/2 FITTED."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import sy1_leaves as _L
EXPR = 'log1p(log1p(inv1p(f) + square(square(square(log1p(square(square(square(inv1p(-5.413311450653678e-6 / ell)))))))))) + 0.5232245672831082'; WRAP = 3; NAME = "SY1 arm T " + EXPR; VERTICAL = ("R",); TRAINED_ON = ("xcop_train", "sparc_train")
def g(Q): return _L.g_of_Q(EXPR, WRAP, Q)
