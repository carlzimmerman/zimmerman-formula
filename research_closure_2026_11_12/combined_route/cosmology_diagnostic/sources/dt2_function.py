#!/usr/bin/env python3
"""CLOSE-1 / DT2: the single engineered kinetic function with a narrow interval of
changed compressibility.  Definitions + the audit's exact identities.

No physics results here: this module only defines the function and checks the
algebraic statements of research_closure_2026_11_10/DT2_response_audit/tradeoff_audit.md S4.
"""
import numpy as np
from scipy.optimize import brentq
from scipy.integrate import quad

# ---------------------------------------------------------------- constants
G_SI = 6.6743e-11
C_SI = 299792458.0
K_SI = 4.0 * np.pi * G_SI
MSUN = 1.98892e30
KPC = 3.0856775814913673e19          # m
MPC = 1000.0 * KPC

A0_CANON = 9.3603e-11
A0_ALT = 1.1312e-10

# cosmological normalisation (DT1's, as used by the audit S3)
H0 = 70.0 * 1.0e3 / MPC                     # s^-1
OMEGA_C = 0.26
RHO_CRIT = 3.0 * H0 ** 2 / (8.0 * np.pi * G_SI)     # kg/m^3
RHO_C0 = OMEGA_C * RHO_CRIT                          # kg/m^3, today's cold mean

# n0 in Mpc^-2 :  n = K rho / c^2, 1/Mpc^2
N0 = K_SI * RHO_C0 / C_SI ** 2 * MPC ** 2

# ---------------------------------------------------------------- the function
M_SLOPE = 400.0          # Mpc^-2, pinned (P1)
Q1, Q2 = 2.0, 26.0       # band edges in q = n/n0, free
L_JUMP = 8.0e-6          # offset jump across the band, free (tied by x(14)=phi)
Q_CENTRE = 14.0          # where B' is maximal
PHI_DEEPEST = 4.0e-6     # P2
CAP_GALAXY = 216.0       # P3


def S(t):
    """Quintic smoothstep, C^2 at both joins."""
    t = np.clip(t, 0.0, 1.0)
    return 10.0 * t ** 3 - 15.0 * t ** 4 + 6.0 * t ** 5


def Sp(t):
    return 30.0 * t ** 2 - 60.0 * t ** 3 + 30.0 * t ** 4


def Spp(t):
    return 60.0 * t - 180.0 * t ** 2 + 120.0 * t ** 3


def B(q):
    q = np.asarray(q, dtype=float)
    t = (q - Q1) / (Q2 - Q1)
    out = np.where(q <= Q1, 0.0, np.where(q >= Q2, 1.0, S(t)))
    return out


def Bp(q):
    """dB/dq."""
    q = np.asarray(q, dtype=float)
    t = (q - Q1) / (Q2 - Q1)
    return np.where((q <= Q1) | (q >= Q2), 0.0, Sp(t) / (Q2 - Q1))


def A_jump():
    """A = L - 26 n0/M : the audit S4 coefficient, so that x(27) = L exactly."""
    return L_JUMP - Q2 * N0 / M_SLOPE


def x_of_q(q):
    """Clock offset x = Q-1 as a function of the density ratio q = n/n0."""
    q = np.asarray(q, dtype=float)
    return (N0 / M_SLOPE) * (q - 1.0) + A_jump() * B(q)


def dxdq(q):
    return N0 / M_SLOPE + A_jump() * Bp(q)


def nprime_of_q(q):
    """n'(x) = dn/dx at the point x = x(q)."""
    return N0 / dxdq(q)


# ---------------------------------------------------------------- fast tabulation
# n(x) requires inverting x(q); do it once on a grid in x and interpolate.
_XTAB = None
_NTAB = None
_VTAB = None
_NPTAB = None


def _build_tables():
    global _XTAB, _NTAB, _VTAB, _NPTAB
    if _XTAB is not None:
        return
    qg = np.concatenate([
        np.geomspace(1.0e-3, Q1, 4000),
        np.linspace(Q1, Q2, 400000),          # dense through the band
        np.geomspace(Q2, 1.0e9, 60000),
    ])
    qg = np.unique(qg)
    xg = x_of_q(qg)
    # enforce strict increase (guards round-off in the near-flat cold branches)
    keep = np.concatenate([[True], np.diff(xg) > 0])
    qg, xg = qg[keep], xg[keep]
    ng = N0 * qg
    npg = N0 / dxdq(qg)
    # resample onto a strictly increasing x-grid
    xb = np.unique(np.concatenate([
        np.linspace(xg[0], 0.0, 400),
        np.geomspace(1.0e-13, 1.0e-7, 3000),
        np.linspace(1.0e-7, L_JUMP, 30000),
        np.geomspace(L_JUMP, xg[-1], 20000),
    ]))
    j = np.searchsorted(xg, xb) - 1
    j = np.clip(j, 0, len(xg) - 2)
    w = (xb - xg[j]) / (xg[j + 1] - xg[j])
    _XTAB = xb
    _NTAB = ng[j] + w * (ng[j + 1] - ng[j])
    _NPTAB = npg[j] + w * (npg[j + 1] - npg[j])
    _VTAB = np.concatenate([[0.0], np.cumsum(0.5 * (_NTAB[1:] + _NTAB[:-1]) * np.diff(xb))])


def x_of_q_direct(q):
    return (N0 / M_SLOPE) * (np.asarray(q, dtype=float) - 1.0) + A_jump() * B(q)


def n_of_x(xv):
    """n(x) = n0 q(x).  Units Mpc^-2.  Linear continuation outside the table."""
    _build_tables()
    xv = np.asarray(xv, dtype=float)
    out = np.interp(xv, _XTAB, _NTAB)
    # below the table: x = n0(q-1)/M  ->  n = n0 + M x
    lo = xv < _XTAB[0]
    if np.any(lo):
        out = np.where(lo, N0 + M_SLOPE * xv, out)
    return out


def nprime_of_x(xv):
    _build_tables()
    xv = np.asarray(xv, dtype=float)
    return np.interp(xv, _XTAB, _NPTAB)


def V_of_x(xv):
    """V(Q) = int_1^Q n  with V(1) = 0, as a function of x = Q-1.  Units Mpc^-2."""
    _build_tables()
    xv = np.asarray(xv, dtype=float)
    return np.interp(xv, _XTAB, _VTAB)


def c_ad2_of_x(xv):
    """c_ad^2 = n/(Q n'),  Q = 1 + x  (dimensionless, c = 1)."""
    xv = np.atleast_1d(np.asarray(xv, dtype=float))
    return n_of_x(xv) / ((1.0 + xv) * nprime_of_x(xv))


def w_of_x(xv):
    """w = p/rho = V/(Q n - V)."""
    xv = np.atleast_1d(np.asarray(xv, dtype=float))
    Qn = (1.0 + xv) * n_of_x(xv)
    return V_of_x(xv) / (Qn - V_of_x(xv))


# ---------------------------------------------------------------- derived scales
def r_M(M_b, a0):
    """form B's r_M = sqrt(G M_b / a0),  M_b in kg, returns m."""
    return np.sqrt(G_SI * M_b / a0)


def X_formB(x):
    return (np.sqrt(1.0 + 4.0 * x ** 2) - 1.0) / 2.0


def n_SI(xv):
    """n in m^-2 (from Mpc^-2)."""
    return np.atleast_1d(n_of_x(xv)) / MPC ** 2


def rho_dust_of_x(xv):
    """rho_dust = (Q n - V) c^2 / K  in kg/m^3  (exact stress-energy; = n c^2/K at dust order)."""
    xv = np.atleast_1d(np.asarray(xv, dtype=float))
    Qn_V = (1.0 + xv) * n_SI(xv) - V_of_x(xv) / MPC ** 2
    return Qn_V * C_SI ** 2 / K_SI


def h_enthalpy_SI(xv):
    """The enthalpy h = c^2 x, in SI units of (m/s)^2 = specific enthalpy."""
    return np.atleast_1d(np.asarray(xv, dtype=float)) * C_SI ** 2
