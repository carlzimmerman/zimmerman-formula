"""SY1 arm T, W2, seed 4, complexity 17, 2 fitted floats frozen at train. A description of data, not a theory; no action. kappa = 1/2 FITTED."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import sy1_leaves as _L
EXPR = 'square(square(inv1p(inv1p(square(square((6.562064269572786e-6 / ell) - 1.1757574830390323)) - log1p(log1p(half)))) - two))'; WRAP = 2; NAME = "SY1 arm T " + EXPR; VERTICAL = ("R",); TRAINED_ON = ("xcop_train", "sparc_train")
def g(Q): return _L.g_of_Q(EXPR, WRAP, Q)
