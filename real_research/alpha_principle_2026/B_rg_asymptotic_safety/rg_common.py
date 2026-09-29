"""Shared inputs and helpers for lane B (declared in B_PREREGISTRATION.md)."""
import numpy as np
from scipy.integrate import solve_ivp

ALPHA_INV0 = 137.035999177
ALPHA_INV_MZ = 127.930
S2W = 0.23122
ALPHA_S = 0.1180
MZ = 91.1876
MT = 172.57
MPL = 1.220890e19
MPL_RED = 2.435e18
DELTA_0_MZ = ALPHA_INV0 - ALPHA_INV_MZ   # 9.106, measured hadronic-inclusive offset

# (name, mass GeV, N_c Q^2)
def fermions(setno):
    lq = (0.00216, 0.00467, 0.0934) if setno == 1 else (0.336, 0.336, 0.5)
    return [("e", 0.000510999, 1.0), ("mu", 0.1056584, 1.0), ("tau", 1.77686, 1.0),
            ("u", lq[0], 3 * 4 / 9), ("d", lq[1], 3 * 1 / 9), ("s", lq[2], 3 * 1 / 9),
            ("c", 1.27, 3 * 4 / 9), ("b", 4.18, 3 * 1 / 9), ("t", MT, 3 * 4 / 9)]

# one-loop SM (alpha_Y = 3/5 alpha_1): d alpha^-1 / d ln mu = -b/(2 pi)
B_Y, B_2, B_3 = 41 / 6, -19 / 6, -7.0

def alpha_inv_boundaries():
    aY = ALPHA_INV_MZ * (1 - S2W)      # alpha_Y^-1 = alpha^-1 cos^2
    a2 = ALPHA_INV_MZ * S2W
    a3 = 1.0 / ALPHA_S
    return aY, a2, a3

def run_oneloop(M):
    aY, a2, a3 = alpha_inv_boundaries()
    L = np.log(M / MZ)
    return (aY - B_Y / (2 * np.pi) * L, a2 - B_2 / (2 * np.pi) * L, a3 - B_3 / (2 * np.pi) * L)

# ---- Harst-Reuter NGFP2 toy: du/dt = -A(k) + c g(k) u, u = 1/alpha, t = ln k
def hr_run(thresholds, gstar, Phi=1.0, k_end=None, sign=+1.0, kUV_over_Mpl=1e4, mpl=MPL):
    """thresholds: list of (mass, A_contribution) with A(k)=sum_{m<k} contribution.
    Start on the fixed point at kUV, integrate down; return 1/alpha at k_end (default lowest mass)."""
    c = sign * 6.0 / np.pi * Phi
    G0 = 1.0 / mpl**2
    g = lambda k: G0 * k**2 / (1 + G0 * k**2 / gstar)
    ths = sorted(thresholds, key=lambda x: -x[0])
    masses = [m for m, _ in ths]
    if k_end is None:
        k_end = min(masses)
    Atot = sum(a for _, a in ths)
    kUV = kUV_over_Mpl * mpl
    u = Atot / (c * gstar)             # fixed-point value u* = A/(c g*)
    edges = [kUV] + [m for m in masses if m < kUV and m >= k_end] + [k_end]
    edges = sorted(set(edges), reverse=True)
    for k0, k1 in zip(edges[:-1], edges[1:]):
        # A just below k0: include thresholds with mass <= (k0 with tolerance)
        kmid = np.sqrt(k0 * k1)
        A = sum(a for m, a in ths if m < kmid)
        f = lambda t, y: [-A + c * g(np.exp(t)) * y[0]]
        sol = solve_ivp(f, [np.log(k0), np.log(k1)], [u], rtol=1e-11, atol=1e-13, method="LSODA")
        u = sol.y[0, -1]
    return u

def hr_closed(A, gstar, Phi, ratio):
    """Harst-Reuter eq (5.6): 1/alpha = (A/2)[2 ln(Mpl/m) + ln g* - gamma_E - psi(3 Phi g*/pi)]."""
    import mpmath as mp
    return float(A / 2 * (2 * np.log(ratio) + np.log(gstar) - float(mp.euler) - float(mp.digamma(3 * Phi * gstar / np.pi))))
