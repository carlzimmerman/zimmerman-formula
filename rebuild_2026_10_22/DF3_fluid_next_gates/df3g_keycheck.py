#!/usr/bin/env python3
"""A2 control: the keys harness against a known answer. A central point mass, passed through soften(), must give the same Delta Sigma R^2 at the key radii as a resolved profile at large R, within 1 %. Unsoftened, it gives nothing. kappa = 1/2 FITTED; not theory closed."""
import json, math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import df3g_run as R, numpy as np
C = R.C; M0 = 1e15 * R.MSUN; RF = C.RF; X = (0.18, 0.3, 1.0, 2.6); i = [int(np.argmin(abs(RF - x))) for x in X]
def dS(M):
    Sg = C.sigma_of(M); y = Sg * RF; cum = 0.5 * Sg[0] * RF[0] ** 2 + C.cumtrap(y, RF); return (2 * cum / RF ** 2 - Sg)[i] * RF[i] ** 2
ref = dS(M0 * C.RM ** 3 / (C.RM ** 2 + (0.05 * R.MPC) ** 2) ** 1.5)[-1]; raw = dS(np.full(C.RM.size, M0)) / ref; soft = dS(R.soften(np.full(C.RM.size, M0), C.RM)) / ref
o = dict(R_Mpc=X, raw_point=raw.tolist(), softened_point=soft.tolist(), passed=bool(np.all(np.abs(soft - 1) < 0.01) and np.all(raw < 0.01))); print(o); json.dump(o, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "df3g_keycheck.json"), "w"), indent=1, default=float)
