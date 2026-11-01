"""SR2: UR3's common code plus SR1's saturated rule. kappa = 1/2 FITTED, unused; not theory closed."""
import os, sys
_H = os.path.dirname(os.path.abspath(__file__)); _U = os.path.join(os.path.dirname(_H), "UR3_direct_weighing"); sys.path.insert(0, _U)
from ur3_common import *
SAT = dict(ms=1.0, on=True)
def sat_contract(r, Mb, Mst, M0, F):
    lr = np.log(r); at = lambda y, x: np.interp(np.log(np.maximum(x, r[0])), lr, y); rf = r.copy()
    for _ in range(100):
        chi = at(Mst * SAT["ms"], rf) / np.maximum(M0, 1e-300) if SAT["on"] else 0.0; rn = r * M0 * (1 + F) / np.maximum(at(Mb, rf) / (1 + chi ** 2) + M0, 1e-300); rf = 0.5 * rf + 0.5 * rn
    return np.interp(lr, np.log(np.maximum.accumulate(rf)), M0, left=0.0, right=M0[-1])
