"""SY1 arm T, W1, seed 7, complexity 20, 2 fitted floats frozen at train. A description of data, not a theory; no action. kappa = 1/2 FITTED."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import sy1_leaves as _L
EXPR = '(log1p(square(log1p(square(square(square(square(square(square(f / -0.2957763838460539) * y)) / s)))))) + 0.5104498336152261) * two'; WRAP = 1; NAME = "SY1 arm T " + EXPR; VERTICAL = ("R",); TRAINED_ON = ("xcop_train", "sparc_train")
def g(Q): return _L.g_of_Q(EXPR, WRAP, Q)
