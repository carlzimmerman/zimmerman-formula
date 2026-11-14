#!/usr/bin/env python3
"""BJ1 library (FROZEN_CRITERIA.md, 9e7ce0dfe6, section 1): the charge-budget junction on FRZ1's halo model.
XJ1's xj1_lib2.py (closure_2026_11_14/XJ1_exact_junction_zero_velocity_surface) is imported read-only: its install()
(XJ1's shell runs, FLD1's five series columns plus R_1, R_2, R_3 in columns 5, 6, 7), its caustic reader rsurf_com and,
through it, FWN1R's library (FZS1's fzs1_hm.py prefix: FRZ1's layouts, Bar, the CUR node device). New here, and only this:
  - rgrid_B: FZS1's rgrid_S (which inserts CUR[0] as a node) wrapped once more, in memory, to insert the nodes listed in
    EXTRA as well (R_k and R_set). With EXTRA empty it returns FZS1's grid unchanged. The layouts are pointwise analytic
    functions of r on the grid (no integration along r, no interpolation), so a node added at r gives C_B(r) and C_R(r)
    exactly as the layout defines them, and every other node keeps its value.
  - budget_fn: the layout of criteria section 1 at the k-th caustic. Per halo: R_k = XJ1's reader (column 5, 6, 7 for
    k = 1, 2, 3; capped at r_ta). R_k is inserted as a node; Q_k = C_R(R_k).
      "under" (C_B(R_k) >= Q_k): R_set = the first root of C_B(r) = Q_k in (0, R_k]: bracketed by the first node with
        C_B >= Q_k, refined by brentq on the layout's own C_B evaluated at the trial radius through EXTRA (no
        interpolation), then stepped down by one float at a time until C_B(R_set) <= Q_k so the layout is non-decreasing
        to the last bit.
      "over" (C_B(R_k) < Q_k): R_set = the first radius beyond R_k where C_B = C_R: the first node beyond R_k with
        C_B - C_R > 1e-12 C_tot brackets it with the last node before it where C_B - C_R < 0, refined by brentq on the
        layout's own C_B - C_R at the trial radius; none inside r_ta -> R_set = r_ta (the law's layout everywhere).
    The row is then rebuilt with both R_k and R_set as nodes: C = C_B for r <= R_set, C_R(max(r, R_k)) beyond,
    M = Bar + C. No factor multiplies anything.
  - tables: XJ1's tables() (itself FWN1R's) with the kind "B" (budget junction at caustic k) in place of E / Z / K.
Adopts nothing. kappa = 1/2 FITTED; not theory closed."""
import os, sys, math
import numpy as np
from scipy.optimize import brentq
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
XJ1 = os.path.join(REPO, "closure_2026_11_14", "XJ1_exact_junction_zero_velocity_surface")
sys.path.insert(0, XJ1)
import xj1_lib2 as XL                                       # read-only
sys.path.pop(0)
X = XL.X
FOOTS, ZB, ANCH, KT = X.FOOTS, X.ZB, X.ANCH, X.KT
COL_K = {1: 5, 2: 6, 3: 7}                                  # XJ1's shell runs: R_1_kpc (= R_fold), R_2_kpc, R_3_kpc
COL_FOLD = XL.COL_FOLD
EXTRA = []
_INST = [False]
def install():
    """XJ1's install() (shell runs in place of FLD1's loaded series), then the extra-node wrapper on FZS1's rgrid_S."""
    dev = XL.install()
    if not _INST[0]:
        Z = X.rec(); F = Z["F"]; _rgS = F["rgrid"]
        def rgrid_B(hb, rmax):
            r = _rgS(hb, rmax); ex = [x for x in EXTRA if 0 < x < rmax]
            return np.unique(np.concatenate([r, ex])) if ex else r
        F["rgrid"] = rgrid_B; _INST[0] = True
    return dev

def _node(r, R):
    i = int(np.argmin(np.abs(r - R))); assert abs(r[i] / R - 1) < 1e-12, (r[i], R); return i

def rows_at(hb, foot, nodes):
    """FRZ1's layouts B and Rb on FZS1's grid with `nodes` inserted: r, M_B, M_R, Bar, C_B, C_R, info of B."""
    Z = X.rec(); layout, Bar, CUR = Z["layout"], Z["Bar"], Z["CUR"]
    CUR[0] = 0.0; EXTRA[:] = [float(x) for x in nodes]
    try:
        rB, MB, inf = layout(hb, foot, mode="B"); rR, MR, _ = layout(hb, foot, mode="Rb")
    finally:
        EXTRA[:] = []
    if inf["regime"] == "L": return rR, None, MR, None, None, None, inf
    assert np.array_equal(rB, rR)
    bar = Bar(hb, foot, rB)
    return rB, MB, MR, bar, MB - bar, MR - bar, inf

def CB_at(hb, foot, r):
    rr, MB, MR, bar, CB, CR, _ = rows_at(hb, foot, [r]); i = _node(rr, r); return float(CB[i])
def D_at(hb, foot, r):
    rr, MB, MR, bar, CB, CR, _ = rows_at(hb, foot, [r]); i = _node(rr, r); return float(CB[i] - CR[i])

def budget_row(hb, foot, Rk):
    """the budget junction for one halo below v*, capture at R_k (comoving Mpc/h, already capped at r_ta)."""
    rta = hb["rta"]
    if Rk <= 0:
        rr, MB, MR, bar, CB, CR, inf = rows_at(hb, foot, [])
        return rr, MR, dict(inf, branch="none", R_k=0.0, R_set=0.0)
    r, MB, MR, bar, CB, CR, inf = rows_at(hb, foot, [Rk])
    if inf["regime"] == "L": return r, MR, dict(inf, branch="L")
    ik = _node(r, Rk); Q = float(CR[ik]); Ctot = float(CR[-1])
    if CB[ik] >= Q:
        branch = "under"
        j = int(np.nonzero(CB[: ik + 1] >= Q)[0][0])
        if CB[j] == Q or j == 0: Rs = float(r[j])
        else:
            f = lambda x: CB_at(hb, foot, x) - Q
            Rs = brentq(f, float(r[j - 1]), float(r[j]), xtol=1e-15 * float(r[j]), rtol=4 * np.finfo(float).eps, maxiter=200)
            n = 0
            while Rs > r[j - 1] and CB_at(hb, foot, Rs) > Q and n < 64: Rs = float(np.nextafter(Rs, 0.0)); n += 1
    else:
        branch = "over"
        D = CB - CR; thr = 1e-12 * Ctot
        js = np.nonzero((np.arange(len(r)) > ik) & (D > thr))[0]
        if len(js) == 0: Rs = rta
        else:
            j = int(js[0]); neg = np.nonzero((np.arange(len(r)) > ik - 1) & (np.arange(len(r)) < j) & (D < 0))[0]
            i0 = int(neg[-1]); i1 = i0 + 1
            if D[i1] == 0: Rs = float(r[i1])
            else:
                Rs = brentq(lambda x: D_at(hb, foot, x), float(r[i0]), float(r[i1]), xtol=1e-15 * float(r[i1]), rtol=4 * np.finfo(float).eps, maxiter=200)
    Rs = min(Rs, rta)
    nodes = [Rk] + ([Rs] if 0 < Rs < rta else [])
    r, MB, MR, bar, CB, CR, inf2 = rows_at(hb, foot, nodes)
    ik = _node(r, Rk); Qn = float(CR[ik]); assert Qn == Q
    if Rs >= rta * (1 - 1e-14): C = CB.copy(); iS = len(r) - 1
    else:
        iS = _node(r, Rs) if Rs > 0 else 0
        C = np.where(np.arange(len(r)) <= iS, CB, np.where(r < Rk, Q, CR))
    info = dict(inf, branch=branch, R_k=float(Rk), R_set=float(Rs), i_set=int(iS), i_k=int(ik), Q=Q, C_tot=Ctot,
                CB_at_Rk=float(CB[ik]), D_k=float(Q / CB[ik]) if CB[ik] > 0 else float("inf"),
                capped=bool(Rs >= rta * (1 - 1e-14)))
    return r, bar + C, info

def budget_fn(foot, z, vst, k, force=None):
    """reference layout for v_vir > vst; else the budget junction at the k-th caustic. force = 'rta' | 'zero' sets R_k
    (known answer vi)."""
    Z = X.rec(); F = Z["F"]; layout, CUR = Z["layout"], Z["CUR"]
    def fn(hb):
        CUR[0] = 0.0; EXTRA[:] = []
        if F["v_vir"](hb) > vst: return layout(hb, foot, mode="Rb")
        Rk = hb["rta"] if force == "rta" else 0.0 if force == "zero" else XL.rsurf_com(hb, foot, z, COL_K[int(k)], 1.0)
        r, M, inf = budget_row(hb, foot, Rk)
        if "R_set" in inf and inf.get("branch") in ("under", "over"):
            inf["R_fold"] = XL.rsurf_com(hb, foot, z, COL_FOLD, 1.0)
        return r, M, inf
    return fn

def tables(z, cases):
    """XJ1's tables() copied (FWN1R's), with the kind 'B' (budget junction at caustic k = f) in place of E / Z / K.
    cases: {name: (kind, f, vst_mode)}; kinds R, C, J (FWN1R's split_fn) unchanged."""
    install()
    Z = X.rec(); F, L = Z["F"], Z["L"]; layout, CUR = Z["layout"], Z["CUR"]
    Z["set_z"](z); D = F["S"]["D"]
    KKs, PLs = L["KK"], L["PL"]
    L["KK"] = KT.copy(); L["PL"] = L["P_lin"](np.maximum(KT, 1e-5)) * D * D
    out = {}
    try:
        for ft in FOOTS:
            vs = X.vstar(ft, z)
            t = dict(vstar=vs, n_above=int(sum(1 for hb in L["HB"] if F["v_vir"](hb) > vs)), n=len(L["HB"]),
                     lM=np.log10(L["MM"]), M=L["MM"].copy(), W=L["W_M"].copy(), RHO=L["RHO_M"], PL=L["PL"].copy(), U={}, I={}, P={}, p1={}, info={})
            t["mask_above"] = np.array([F["v_vir"](hb) > vs for hb in L["HB"]])
            for name, (kind, f, vm) in cases.items():
                CUR[0] = 0.0
                vst = {"main": vs, "inf": math.inf, "zero": 0.0}[vm]
                if kind == "R": fn = lambda hb: layout(hb, ft, mode="Rb")
                elif kind == "C": fn = lambda hb: layout(hb, ft, mode="B")
                elif kind == "J": fn = X.split_fn(ft, z, f, vst)
                elif kind == "B": fn = budget_fn(ft, z, vst, int(f))
                else: raise ValueError(kind)
                U, inf = L["U_set"](fn); CUR[0] = 0.0
                P, p1, I = L["spectra_ta"](U)
                t["U"][name] = U; t["P"][name] = P; t["p1"][name] = p1; t["I"][name] = I
                if kind == "B":
                    b = [i_ for i_ in inf if isinstance(i_, dict) and i_.get("branch") in ("under", "over")]
                    t["info"][name] = dict(n_under=sum(1 for i_ in b if i_["branch"] == "under"), n_over=sum(1 for i_ in b if i_["branch"] == "over"),
                                           n_over_capped_at_rta=sum(1 for i_ in b if i_["branch"] == "over" and i_["capped"]),
                                           Rset_over_Rk_min_max=[float(min(i_["R_set"] / i_["R_k"] for i_ in b)), float(max(i_["R_set"] / i_["R_k"] for i_ in b))] if b else None,
                                           Rset_over_Rfold_min_max=[float(min(i_["R_set"] / i_["R_fold"] for i_ in b)), float(max(i_["R_set"] / i_["R_fold"] for i_ in b))] if b else None)
            t["Mta"] = t["U"]["R"][:, 0].copy()
            out[ft] = t
    finally:
        L["KK"] = KKs; L["PL"] = PLs
    return out
# kappa = 1/2 FITTED; not theory closed. Adopts nothing.
