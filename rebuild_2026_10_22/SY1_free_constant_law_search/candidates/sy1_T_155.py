"""SY1 arm T, W3, seed 5, complexity 20, 2 fitted floats frozen at train. A description of data, not a theory; no action. kappa = 1/2 FITTED."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import sy1_leaves as _L
EXPR = 'square(square(inv1p((square(square(square(s))) + 0.07624682094112065) + square(square(square(f + (D * -0.0005744334570540981)))))) + one)'; WRAP = 3; NAME = "SY1 arm T " + EXPR; VERTICAL = ("R",); TRAINED_ON = ("xcop_train", "sparc_train")
def g(Q): return _L.g_of_Q(EXPR, WRAP, Q)
