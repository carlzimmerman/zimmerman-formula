"""SY1 arm T, W2, seed 6, complexity 18, 2 fitted floats frozen at train. A description of data, not a theory; no action. kappa = 1/2 FITTED."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import sy1_leaves as _L
EXPR = 'sqrt(square((1.2954975139261908 - square(square(inv1p(square(square(square(ell / 3.2825294043904257e-6))))))) / inv1p(pi_)) - half)'; WRAP = 2; NAME = "SY1 arm T " + EXPR; VERTICAL = ("R",); TRAINED_ON = ("xcop_train", "sparc_train")
def g(Q): return _L.g_of_Q(EXPR, WRAP, Q)
