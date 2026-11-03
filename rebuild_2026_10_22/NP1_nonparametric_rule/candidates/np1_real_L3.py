"""NP1 real L3. Frozen Gaussian-process rule, W3, per footing. A description of data, not a theory; no action. kappa = 1/2 FITTED."""
import os, sys
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import np1_cand as _C
_R = _C.load('real_L3')
NAME = 'NP1 real L3'; VERTICAL = ("R",); TRAINED_ON = ("xcop_train", "sparc_train")
def g(Q): return _C.g_of_Q(_R, Q)
