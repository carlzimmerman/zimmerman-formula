"""NV1 MUTATE L3+E2 (E shuffled). Frozen admissible GP rule on (log y, log ell, f, E), W3, per footing. A description of data, not a theory; no action. kappa = 1/2 FITTED."""
import os, sys
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import nv1_cand as _C
_R = _C.load('mutate_E2', 'E2_table_MUTATE')
TABLE = _R[1]
NAME = 'NV1 MUTATE L3+E2 (E shuffled)'; VERTICAL = ("R",); TRAINED_ON = ("xcop_train", "sparc_train")
def g(Q): return _C.g_of_Q(_R, Q)
