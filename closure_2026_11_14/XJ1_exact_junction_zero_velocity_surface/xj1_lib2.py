#!/usr/bin/env python3
"""XJ1 library, second pass (AMENDMENT_A5): a copy of xj1_lib.py with one added kind, "K" (the exact junction at the k-th caustic, k = 2 or 3), read from this lane's shell runs (shells/xj1_shells_<footing>_M<logMb>.json: FLD1's five series columns, checked equal to FZS1's loaded FLD1 series, plus R_1, R_2, R_3 in columns 5, 6, 7). install() swaps FZS1's loaded series for these 8-column arrays in memory; nothing on disk changes. The first pass's docstring follows. XJ1 library (FROZEN_CRITERIA.md, ef8ccdde98, section 1). FWN1R's library (closure_2026_11_14/FWN1R_blind_split_f_ceiling/
fwn1r_lib.py) is imported read-only; it executes FZS1's fzs1_hm.py prefix (FRZ1's halo model and layouts) read-only.
New here, and only this:
  - surf_kpc / rsurf_com: FZS1's rfold_kpc and rset_com with the series column as an argument (2 = R_fold_kpc,
    3 = R_ta_kpc, FLD1's turnaround radius = the zero-velocity surface); interpolation, M_b and units unchanged.
  - exact_fn: the exact junction. Inside R_set the law's layout M_B unscaled; outside
    Bar + C_B(R_set) + t [C_R - C_R(R_set)], t = [C_tot - C_B(R_set)] / [C_tot - C_R(R_set)].
  - tables: a copy of FWN1R's tables() with two added kinds, "E" (exact junction at f R_fold) and "Z" (exact junction at
    R_zv). Kinds R, C, J and A are FWN1R's lines unchanged (J goes through FWN1R's own split_fn).
Adopts nothing. kappa = 1/2 FITTED; not theory closed."""
import os, sys, math
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(REPO, "closure_2026_11_14", "FWN1R_blind_split_f_ceiling"))
import fwn1r_lib as X                                      # read-only
FOOTS, ZB, ANCH, KT = X.FOOTS, X.ZB, X.ANCH, X.KT
COL_FOLD, COL_ZV = 2, 3                                    # FLD1 series columns: R_fold_kpc, R_ta_kpc
COL_K = {2: 6, 3: 7}                                       # this lane's shell runs: R_2_kpc, R_3_kpc
SHELLS = os.path.join(HERE, "shells"); _INST = [False, 0.0]
def install():
    """swap FZS1's loaded FLD1 series for this lane's shell runs (first five columns checked equal to 1e-9 relative)."""
    if _INST[0]: return _INST[1]
    import json
    Z = X.rec(); dev = 0.0
    for ft in FOOTS:
        for M in Z["MASSES"]:
            S = np.array(json.load(open(os.path.join(SHELLS, f"xj1_shells_{ft}_M{M:g}.json")))["series"]); old = Z["FT"][ft][M]
            assert S.shape[0] == old.shape[0] and S.shape[1] == 8 and old.shape[1] == 5
            dev = max(dev, float(np.max(np.abs(S[:, :5] - old) / np.maximum(np.abs(old), 1e-30))))
            Z["FT"][ft][M] = S
    assert dev <= 1e-9, dev
    _INST[0] = True; _INST[1] = dev; _ST.clear(); Z["_RT"].clear()
    return dev

_ST = {}
def surf_kpc(foot, z, lM, col):
    """FZS1's rfold_kpc with the series column as an argument (physical kpc)."""
    Z = X.rec(); MASSES = Z["MASSES"]; FT = Z["FT"]
    key = (foot, round(z, 6), col)
    if key not in _ST:
        def at(S):
            o = np.argsort(S[:, 1]); return float(np.interp(z, S[o, 1], S[o, col]))
        _ST[key] = np.array([at(FT[foot][M]) for M in MASSES])
    R = _ST[key]
    if lM < MASSES[0]: return float(R[0] * 10 ** ((lM - MASSES[0]) / 3))
    if lM > MASSES[-1]: return float(R[-1] * 10 ** ((lM - MASSES[-1]) / 3))
    if np.any(R <= 0): return float(np.interp(lM, MASSES, R))
    return float(10 ** np.interp(lM, MASSES, np.log10(R)))

def rsurf_com(hb, foot, z, col, mult=1.0):
    """FZS1's rset_com with the column as an argument: comoving Mpc/h, capped at r_ta."""
    Z = X.rec()
    if mult == 0: return 0.0
    if math.isinf(mult): return hb["rta"]
    R = mult * surf_kpc(foot, z, math.log10(Z["Mb_fold"](hb, foot) / Z["h"]), col) * 1e-3 * (1 + z) * Z["h"]
    return min(R, hb["rta"])

def exact_fn(foot, z, vst, col, mult=1.0, force=None):
    """reference layout for v_vir > vst; else the exact junction at R_set = mult x (FLD1 column col), capped at r_ta.
    force = 'rta' or 'zero' overrides R_set (known answer KA-E v)."""
    Z = X.rec(); F = Z["F"]; layout, Bar, CUR = Z["layout"], Z["Bar"], Z["CUR"]
    def fn(hb):
        CUR[0] = 0.0
        if F["v_vir"](hb) > vst: return layout(hb, foot, mode="Rb")
        R = hb["rta"] if force == "rta" else 0.0 if force == "zero" else rsurf_com(hb, foot, z, col, mult)
        if R <= 0: return layout(hb, foot, mode="Rb")
        CUR[0] = R
        rB, MB, inf = layout(hb, foot, mode="B"); rR, MR, _ = layout(hb, foot, mode="Rb"); CUR[0] = 0.0
        if inf["regime"] == "L": return rR, MR, inf
        assert np.array_equal(rB, rR)
        bar = Bar(hb, foot, rB); CB, CR = MB - bar, MR - bar
        i = int(np.argmin(np.abs(rB - R))); assert abs(rB[i] / R - 1) < 1e-12
        den = CR[-1] - CR[i]
        if den <= 0: return rB, MB, dict(inf, t=1.0, s=1.0, R_set=R, i_set=i)        # R_set at r_ta: the law's layout at every radius
        t = (CR[-1] - CB[i]) / den
        return rB, np.where(rB <= rB[i], MB, bar + CB[i] + t * (CR - CR[i])), dict(inf, t=float(t), s=float(CR[i] / CB[i]), R_set=R, i_set=i)
    return fn

def tables(z, cases):
    """FWN1R's tables() copied, with kinds 'E' (exact junction at f R_fold) and 'Z' (exact junction at R_zv) added.
    cases: {name: (kind, f, vst_mode)}."""
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
                elif kind == "E": fn = exact_fn(ft, z, vst, COL_FOLD, f)
                elif kind == "Z": fn = exact_fn(ft, z, vst, COL_ZV, 1.0)
                elif kind == "K": fn = exact_fn(ft, z, vst, COL_K[int(f)], 1.0)
                else: raise ValueError(kind)
                U, inf = L["U_set"](fn); CUR[0] = 0.0
                P, p1, I = L["spectra_ta"](U)
                t["U"][name] = U; t["P"][name] = P; t["p1"][name] = p1; t["I"][name] = I
                if kind in ("E", "Z", "K"):
                    tt = [i_["t"] for i_ in inf if isinstance(i_, dict) and "t" in i_]; ss = [i_["s"] for i_ in inf if isinstance(i_, dict) and "s" in i_]
                    cap = [1.0 if abs(i_["R_set"] / hb["rta"] - 1) < 1e-12 else 0.0 for i_, hb in zip(inf, L["HB"]) if isinstance(i_, dict) and "R_set" in i_]
                    t["info"][name] = dict(t_min_max=[float(min(tt)), float(max(tt))] if tt else None, s_min_max=[float(min(ss)), float(max(ss))] if ss else None,
                                           n_settled=len(tt), frac_capped_at_rta=float(np.mean(cap)) if cap else None)
            t["Mta"] = t["U"]["R"][:, 0].copy()
            out[ft] = t
    finally:
        L["KK"] = KKs; L["PL"] = PLs
    return out
