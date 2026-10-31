#!/usr/bin/env python3
"""ZK1: x48_zoom with the compiled force kernel. x48_zoom.py isn't edited; only its accel is replaced. Same arguments as x48_zoom.py.
    python3 x48_fast.py --mass 1e14 --seed 1 --ng 64 --work DIR --resume
ZK1_THREADS sets threads per run (default 1). kappa = 1/2 FITTED; not theory closed."""
import ctypes, importlib.util, os, sys
from concurrent.futures import ThreadPoolExecutor
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE)
_sp = importlib.util.spec_from_file_location("x48_zoom", os.path.join(REB, "X48_native_cf_zoom", "x48_zoom.py")); X = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(X)
NUMPY_ACCEL = X.accel
_L = ctypes.CDLL(os.path.join(HERE, "x48_force.dylib")); _D = ctypes.POINTER(ctypes.c_double)
_L.x48_accel.argtypes = [_D, _D, _D, ctypes.c_long, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_long, ctypes.c_long, _D, _D, _D]; _L.x48_accel.restype = None
_T = int(os.environ.get("ZK1_THREADS", "1")); _EX = ThreadPoolExecutor(_T) if _T > 1 else None; _EPSX = float(os.environ.get("ZK1_MUT_EPS", "1"))
def accel(x, m, eps, OLH2, chunk=512):
    """Same sum as x48_zoom.accel, in compiled code."""
    N = len(x); xx, yy, zz = (np.ascontiguousarray(x[:, k], dtype=np.float64) for k in range(3)); ax, ay, az = np.empty(N), np.empty(N), np.empty(N)
    P = lambda a: a.ctypes.data_as(_D); Gm = X.G * m; e2 = (eps * _EPSX) ** 2
    def job(r): _L.x48_accel(P(xx), P(yy), P(zz), N, Gm, e2, OLH2, r[0], r[1], P(ax), P(ay), P(az))
    if _EX is None: job((0, N))
    else:
        cuts = np.linspace(0, N, 8 * _T + 1).astype(int); list(_EX.map(job, [(int(a), int(b)) for a, b in zip(cuts[:-1], cuts[1:])]))
    return np.stack([ax, ay, az], axis=1)
X.accel = accel
if __name__ == "__main__":
    sys.exit(X.main())
