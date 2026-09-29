"""Shared library for lane N2 (declared in N2_PREREGISTRATION.md). No physics is decided here beyond the declared conventions.
Read-only imports of lane B's rg_common.py inputs. Never writes bytecode.
"""
import sys, math
sys.dont_write_bytecode = True
from fractions import Fraction as Fr
import numpy as np
from scipy.optimize import brentq

import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "B_rg_asymptotic_safety"))
import rg_common as RC                      # read only: ALPHA_INV0, ALPHA_INV_MZ, S2W, ALPHA_S, MZ, MPL_RED, DELTA_0_MZ, B_Y, B_2, B_3

MZ = RC.MZ
M_RED = RC.MPL_RED
MPL = RC.MPL
DELTA0 = RC.DELTA_0_MZ
ALPHA_INV0 = RC.ALPHA_INV0
N0 = 118
TWO_PI = 2 * math.pi
MEAS = RC.alpha_inv_boundaries()            # (1/alpha_Y, 1/alpha_2, 1/alpha_3) at M_Z, MSbar, alpha_Y unnormalised
NAMES = ("Y", "2", "3")

# ---------------- group theory (exact) ----------------
def T3(d3):  return {1: Fr(0), 3: Fr(1, 2), 8: Fr(3)}[d3]
def T2(d2):  return {1: Fr(0), 2: Fr(1, 2), 3: Fr(2)}[d2]

def index_vec(d3, d2, Y):
    """(T_Y, T_2, T_3) of a rep (d3, d2, Y): Y is the hypercharge with Q = T3 + Y (unnormalised)."""
    Y = Fr(Y)
    return (Y * Y * d3 * d2, T2(d2) * d3, T3(d3) * d2)

# kinds and their coefficient per unit T
KIND = {"vector": Fr(-11, 3),      # massless gauge boson in a real rep
        "mvector": Fr(-7, 2),      # massive vector in a real rep: vector + eaten real adjoint scalar (-11/3 + 1/6)
        "weyl": Fr(2, 3), "cscalar": Fr(1, 3), "rscalar": Fr(1, 6)}
DOF = {"vector": 2, "mvector": 3, "weyl": 2, "cscalar": 2, "rscalar": 1}

def coeff(kind, d3, d2, Y, mult=1, real_rep=True):
    """b-vector (Y,2,3) of `mult` copies of a field. For complex vectors give real_rep=False: the real rep is R + Rbar (index doubled)."""
    t = index_vec(d3, d2, Y)
    f = KIND[kind] * mult * (1 if real_rep else 2)
    return tuple(f * ti for ti in t)

def dof(kind, d3, d2, mult=1, real_rep=True):
    return DOF[kind] * d3 * d2 * mult * (1 if real_rep else 2)

def add(*vs):
    return tuple(sum(c) for c in zip(*vs))

def scale(v, s):
    return tuple(s * c for c in v)

# ---------------- the SM content (Weyl LH fields per generation) ----------------
GEN = 3
WEYL_PER_GEN = [("Q", 3, 2, Fr(1, 6)), ("uc", 3, 1, Fr(-2, 3)), ("dc", 3, 1, Fr(1, 3)), ("L", 1, 2, Fr(-1, 2)), ("ec", 1, 1, Fr(1))]
HIGGS = ("H", 1, 2, Fr(1, 2))

def b_weyl(mult=GEN):
    return add(*[coeff("weyl", d3, d2, Y, mult) for _, d3, d2, Y in WEYL_PER_GEN])
def dof_weyl(mult=GEN):
    return sum(dof("weyl", d3, d2, mult) for _, d3, d2, _ in WEYL_PER_GEN)
def b_higgs():
    return coeff("cscalar", *HIGGS[1:])
def dof_higgs():
    return dof("cscalar", HIGGS[1], HIGGS[2])
# SM gauge: (Y: U(1), SU(2) adjoint, SU(3) adjoint)
def b_sm_gauge(kind="vector"):
    return add(coeff(kind, 1, 1, 0), coeff(kind, 1, 3, 0), coeff(kind, 8, 1, 0))
def dof_sm_gauge(kind="vector"):
    return dof(kind, 1, 1) + dof(kind, 1, 3) + dof(kind, 8, 1)
def b_sm_adjoint_massive():          # massive SM-adjoint vectors (12 of them) -> (0, -7, -21/2)
    return b_sm_gauge("mvector")

# SU(5) leftovers
def b_X_massive():                   # X,Y vectors: complex (3,2,-5/6) as a massive vector
    return coeff("mvector", 3, 2, Fr(-5, 6), real_rep=False)
def dof_X_massive():
    return dof("mvector", 3, 2, real_rep=False)
def b_triplet_higgs():               # colour-triplet complex scalar (3,1,-1/3)
    return coeff("cscalar", 3, 1, Fr(-1, 3))
def dof_triplet_higgs():
    return dof("cscalar", 3, 1)

def b_SM():
    return add(b_weyl(), b_higgs(), b_sm_gauge("vector"))

GRAV_DOF = 5
YNORM = Fr(5, 3)                      # b_Y = (5/3) b_1 ; the lane-A slip used 3/5

# ---------------- the towers ----------------
class Tower:
    def __init__(self, name, level_fn):
        self.name = name; self.level_fn = level_fn   # level_fn(j, grav) -> (dof, bvec) for j >= 1

def _ta(j, grav):
    b = add(scale(b_weyl(), 2), b_higgs())       # Dirac = 2 Weyl
    d = 2 * dof_weyl() + dof_higgs() + (GRAV_DOF if grav else 0)
    return d, b
def _tb(j, grav):
    d, b = _ta(j, grav)
    return d + dof_sm_gauge("mvector"), add(b, b_sm_adjoint_massive())
def _tc(j, grav):
    if j % 2 == 0:
        return dof_sm_gauge("mvector") + dof_higgs() + (GRAV_DOF if grav else 0), add(b_sm_adjoint_massive(), b_higgs())
    return dof_X_massive() + dof_triplet_higgs(), add(b_X_massive(), b_triplet_higgs())

TA = Tower("TA matter tower", _ta)
TB = Tower("TB universal tower", _tb)
TC = Tower("TC orbifold-GUT gauge/Higgs tower", _tc)
TOWERS = (TA, TB, TC)

def level_patterns(tw, grav):
    """Return the distinct (period-2) level data: dof/bvec for even and odd j."""
    return {"even": tw.level_fn(2, grav), "odd": tw.level_fn(1, grav)}

_LEV = {}
def _lev(tw, par, grav):
    key = (tw.name, par, grav)
    if key not in _LEV:
        d, b = tw.level_fn(2 if par == 0 else 1, grav)
        _LEV[key] = (d, b, tuple(float(c) for c in b))
    return _LEV[key]

def cum_counts(tw, k, grav):
    """Exact number of levels of each parity up to k, cumulative dof, and cumulative b-vector (sum b_j, Fractions)."""
    ne, no = k // 2, k - k // 2
    de, be, _ = _lev(tw, 0, grav); do, bo, _ = _lev(tw, 1, grav)
    dof_tot = de * ne + do * no
    bsum = add(scale(be, ne), scale(bo, no))
    return ne, no, dof_tot, bsum, (de, be, do, bo)

def _lnfact(n):
    return math.lgamma(n + 1)

def tower_sum(tw, k, x, grav=True):
    """Sum_{j<=k} b_ij ln(x/j) as floats (i = Y,2,3): closed form with lgamma, x = Lambda/M_c."""
    if k <= 0:
        return (0.0, 0.0, 0.0)
    ne, no = k // 2, k - k // 2
    be = _lev(tw, 0, grav)[2]; bo = _lev(tw, 1, grav)[2]
    lnx = math.log(x)
    ln_even = ne * math.log(2) + _lnfact(ne)          # sum_{even j<=k} ln j
    ln_all = _lnfact(k)
    ln_odd = ln_all - ln_even
    Se = ne * lnx - ln_even                            # sum_{even} ln(x/j)
    So = no * lnx - ln_odd
    return tuple(be[i] * Se + bo[i] * So for i in range(3))

def tower_sum_brute(tw, k, x, grav=True):
    out = [0.0, 0.0, 0.0]
    for j in range(1, k + 1):
        _, b = tw.level_fn(j, grav)
        for i in range(3):
            out[i] += float(b[i]) * math.log(x / j)
    return tuple(out)

def N_of(tw, k, grav=True, n0=N0):
    ne, no = k // 2, k - k // 2
    return n0 + _lev(tw, 0, grav)[0] * ne + _lev(tw, 1, grav)[0] * no

def species_cutoff(Mc, tw, M=M_RED, grav=True, selfcons=True, n0=N0):
    """Lambda_sp with Lambda^2 N(Lambda) = M^2, N counting tower states with m_j <= Lambda.
    Returns (Lambda, k, N, pinned). If no exact solution exists (step in N), Lambda is pinned at the threshold k*Mc (declared)."""
    if not selfcons:
        L = M / math.sqrt(n0); k = int(L / Mc + 1e-12)   # MUTATE path: cutoff from the fixed N_0 (tower states below it are still summed and counted in N)
        return L, k, N_of(tw, k, grav, n0), False
    # smallest k >= 0 with Lambda_k < (k+1) Mc ; Lambda_k = M/sqrt(N_k) decreasing in k, (k+1)Mc increasing
    def lam(k): return M / math.sqrt(N_of(tw, k, grav, n0))
    if lam(0) < Mc:
        return lam(0), 0, n0, False
    lo, hi = 0, 1
    while lam(hi) >= (hi + 1) * Mc:
        lo = hi; hi *= 2
        if hi > 10 ** 13:
            raise RuntimeError("k overflow")
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if lam(mid) >= (mid + 1) * Mc: lo = mid
        else: hi = mid
    k = hi
    L = lam(k)
    if L >= k * Mc:
        return L, k, N_of(tw, k, grav, n0), False
    return k * Mc, k, N_of(tw, k, grav, n0), True

BSM = tuple(float(c) for c in b_SM())

def F_pred(Mc, tw, M=M_RED, grav=True, selfcons=True, shift_sign=0.0, kappa=0.0):
    """Predicted 1/alpha_i(M_Z) if 1/alpha_i(Lambda_sp) = 0 (i = Y,2,3): (1/2pi)[b_SM ln(Lambda/M_Z) + sum_j b_ij ln(Lambda/m_j)] (+ optional scheme shift kappa*shift_sign*sum b)."""
    L, k, N, pinned = species_cutoff(Mc, tw, M, grav, selfcons)
    lnL = math.log(L / MZ)
    ts = tower_sum(tw, k, L / Mc, grav)
    if k > 0:
        ne, no = k // 2, k - k // 2
        be = _lev(tw, 0, grav)[2]; bo = _lev(tw, 1, grav)[2]
        bsum = [be[i] * ne + bo[i] * no for i in range(3)]
    else:
        bsum = [0.0, 0.0, 0.0]
    F = [ (BSM[i] * lnL + ts[i]) / TWO_PI + kappa * shift_sign * (BSM[i] + bsum[i]) for i in range(3)]
    return F, dict(Lambda=L, k=k, N=N, pinned=pinned, x=L / Mc, tower_sum=ts, bsum=bsum, lnL=lnL)

def find_roots(i, tw, target=None, M=M_RED, grav=True, selfcons=True, shift_sign=0.0, kappa=0.0, lo=5.0, npts=6000):
    """All roots in log10 M_c in [lo, log10(Lambda_0)+0.3] of F_i(M_c) = target_i (default: measured 1/alpha_i(M_Z))."""
    tgt = MEAS[i] if target is None else target
    hi = math.log10(M / math.sqrt(N0)) + 0.3
    grid = np.linspace(lo, hi, npts)
    vals = np.array([F_pred(10 ** g, tw, M, grav, selfcons, shift_sign, kappa)[0][i] - tgt for g in grid])
    roots = []
    for a, b, fa, fb in zip(grid[:-1], grid[1:], vals[:-1], vals[1:]):
        if fa == 0: roots.append(a)
        elif fa * fb < 0:
            roots.append(brentq(lambda g: F_pred(10 ** g, tw, M, grav, selfcons, shift_sign, kappa)[0][i] - tgt, a, b, xtol=1e-13, rtol=1e-14))
    return [10 ** g for g in roots], (float(vals.min() + tgt), float(vals.max() + tgt))

def summarize(Mc, tw, M=M_RED, grav=True, selfcons=True, shift_sign=0.0, kappa=0.0):
    F, info = F_pred(Mc, tw, M, grav, selfcons, shift_sign, kappa)
    em = F[0] + F[1]
    resid = [MEAS[i] - F[i] for i in range(3)]          # 1/alpha_i at Lambda_sp implied by the measured M_Z values
    return dict(F=F, em_MZ=em, em_0=em + DELTA0, s2=F[1] / em, resid=resid, resid_em=resid[0] + resid[1], Mc=Mc, **info)
