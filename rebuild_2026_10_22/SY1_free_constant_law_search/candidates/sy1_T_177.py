"""SY1 arm T, W1, seed 1, complexity 22, 2 fitted floats frozen at train. A description of data, not a theory; no action. kappa = 1/2 FITTED."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import sy1_leaves as _L
EXPR = 'sqrt((D * log1p(log1p(square(log1p(square(square(ell / 3.7731208030519516e-6))))))) + log1p(square(log1p(ell / 2.5714471491554914e-8)))) * inv1p(f)'; WRAP = 1; NAME = "SY1 arm T " + EXPR; VERTICAL = ("R",); TRAINED_ON = ("xcop_train", "sparc_train")
def g(Q): return _L.g_of_Q(EXPR, WRAP, Q)
