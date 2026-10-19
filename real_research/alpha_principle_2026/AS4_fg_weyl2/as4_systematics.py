"""AS4 helper: the two-loop and reduced-Planck systematics, identical in method to AS3's as3_trial.py (lane B's b2 rhs and b3 module by import).
Kept as a separate small module so that importing it does not run AS3's trial."""
import sys
sys.dont_write_bytecode = True
import numpy as np
from scipy.integrate import solve_ivp
import as4_common as A

C1 = A.C1
RG = C1.RG


def two_loop_P(gYs, b2):
    y0 = np.array([np.sqrt(4 * np.pi / b2.a1), np.sqrt(4 * np.pi / b2.a2), np.sqrt(4 * np.pi / b2.a3), 0.94])
    up = solve_ivp(b2.rhs, [np.log(RG.MZ), np.log(RG.MPL)], y0, args=(True,), rtol=1e-11, atol=1e-13)
    yP = up.y[:, -1].copy()
    yP[0] = np.sqrt(5 / 3) * gYs
    out = {}
    for tl in (True, False):
        dn = solve_ivp(b2.rhs, [np.log(RG.MPL), np.log(RG.MZ)], yP, args=(tl,), rtol=1e-11, atol=1e-13)
        out[tl] = (5 / 3) * 4 * np.pi / dn.y[0, -1]**2 + C1.laneB_b3().a2_mz + RG.DELTA_0_MZ
    return out[True], out[False]


def reduced_planck_P(fg):
    b3 = C1.laneB_b3()
    saved = b3.MPL
    try:
        b3.MPL = RG.MPL_RED
        return C1.downstream_P(fg)
    finally:
        b3.MPL = saved
