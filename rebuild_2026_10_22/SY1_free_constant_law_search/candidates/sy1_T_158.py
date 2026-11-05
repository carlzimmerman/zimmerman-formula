"""SY1 arm T, W1, seed 4, complexity 20, 2 fitted floats frozen at train. A description of data, not a theory; no action. kappa = 1/2 FITTED."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import sy1_leaves as _L
EXPR = 'sqrt(inv1p(f) + square(one - square(inv1p(inv1p(s * -204.19561487276093)) - (sqrt(y / 0.0064547221129150015) * f))))'; WRAP = 1; NAME = "SY1 arm T " + EXPR; VERTICAL = ("R",); TRAINED_ON = ("xcop_train", "sparc_train")
def g(Q): return _L.g_of_Q(EXPR, WRAP, Q)
