"""SY1 arm T, W2, seed 6, complexity 21, 2 fitted floats frozen at train. A description of data, not a theory; no action. kappa = 1/2 FITTED."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import sy1_leaves as _L
EXPR = 'square((log1p(inv1p(square(log1p(square(square(square(square(f) * (log1p(y) / -0.07609580031996174))))) / s))) - 1.1942089580798196) / half)'; WRAP = 2; NAME = "SY1 arm T " + EXPR; VERTICAL = ("R",); TRAINED_ON = ("xcop_train", "sparc_train")
def g(Q): return _L.g_of_Q(EXPR, WRAP, Q)
