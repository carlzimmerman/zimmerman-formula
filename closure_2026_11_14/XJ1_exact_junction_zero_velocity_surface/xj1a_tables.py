#!/usr/bin/env python3
"""XJ1 build A (FROZEN_CRITERIA.md ef8ccdde98, sections 1 and 8): halo-model tables. COPY of FWN2 build A's fwn2a_tables.py
(closure_2026_11_14/FWN2_forest_flux_split_f4), itself FWN1's fwn1_tables.py (closure_2026_11_13/
FWN1_forest_flux_split_f_ceiling), with the split keys changed to:
  SE0.5 the crossing-speed split with the EXACT JUNCTION at R_set = 0.5 R_fold (FZS1's rset_com at fac 0.5, capped at r_ta)
        (graded in build A since the lead's amendment A4, 2026-11-14, which replaced SEzv in build A's box run)
  SE2   the crossing-speed split with the EXACT JUNCTION at R_set = 2 R_fold (FZS1's rset_com at fac 2, capped at r_ta)
  SEzv  (table level only since amendment A4; not in the box run) the crossing-speed split with the EXACT JUNCTION at R_set = R_zv (FLD1's turnaround radius of the clock, capped)
  S5.00 control: FWN1's lay_split at f = 5 (FZS1's junction; SRH1's lay_S), must reproduce FWN1's parts.
The U and C keys (f 0, 1, 2, 3, inf through SRH1's lay_S) and every other array are FWN1's code unchanged, so the forced set
(FRZ4's rule over the U and C cases), the base box and the reference field R are FWN1's.

The exact junction E (criteria section 1), written here from the criteria text (build B's code was not read):
  above v*(z) (FRZ1's v_vir > v*(z), JNT2's vstar_kms mode main): the reference layout (mode "Rb") at every radius.
  otherwise, with M_B = FRZ1's mode "B", M_R = mode "Rb", Bar = FZS1's Bar, C_B = M_B - Bar, C_R = M_R - Bar on the same
  radial grid, R_set inserted as a grid node (SRH1's rgrid_S through CUR, exactly as lay_S), C_tot = C_R(r_ta):
    r <= R_set : M_E(r) = M_B(r)
    r >  R_set : M_E(r) = Bar(r) + C_B(R_set) + t [C_R(r) - C_R(R_set)],  t = [C_tot - C_B(R_set)] / [C_tot - C_R(R_set)]
  R_set = r_ta (no node beyond it) gives M_B; R_set <= 0 or FRZ1 regime "L" gives M_R (as lay_S).
The zero-velocity surface reader rcol_kpc(foot, z, lM, col) is FZS1's rfold_kpc with the series column as a parameter
(col 2 = R_fold_kpc, col 3 = R_ta_kpc), FLD1's primary run files, linear in z, log R linear in log M_b between the 12 table
masses, M_b^(1/3) beyond; M_b = FZS1's Mb_fold; comoving Mpc/h as FZS1's rset_com; capped at the halo's r_ta.
Written to tmp_a/tables_z<z>.npz (temporary; deleted at the end).
kappa = 1/2 FITTED; not theory closed. Adopts nothing."""
import os, sys, io, math, json, contextlib, warnings
warnings.filterwarnings("ignore")
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
SRH = os.path.join(REPO, "closure_2026_11_10", "SRH1_settled_radius_history", "srh1_hm.py")
FLD = os.path.join(REPO, "fable52_push", "FLD1_fold_reach")
PARTS = os.path.join(HERE, "tmp_a"); os.makedirs(PARTS, exist_ok=True)     # temporary tables (deleted at the end)
FOOTS = ("canonical", "alt")
KT = np.concatenate([[0.0], np.geomspace(1e-3, 400.0, 900)])      # FRZ3R's table grid (frz3r_core.KT)
CASES = [1.00, 2.00, 3.00, math.inf]
TAB_F = [0.0] + CASES
def fkey(f): return "finf" if math.isinf(f) else f"f{f:.2f}"
KEYS = [fkey(f) for f in TAB_F]
SPLIT_F = [5.00]                                                 # control S5.00 (FWN1's lay_split, FZS1's junction)
def skey(f): return "Sinf" if math.isinf(f) else f"S{f:.2f}"
EKEYS = ["SE0.5", "SE2", "SEzv"]                                 # exact-junction table keys (graded in build A: SE0.5, SE2)
SKEYS = [skey(f) for f in SPLIT_F] + EKEYS
sys.path.insert(1, os.path.join(REPO, "closure_2026_11_13", "JNT2_crossing_speed_joint"))
import jnt2_common as JC                                         # read-only: constants, E(z), vstar_kms
def above(SN, hb, foot, z):
    """JNT2's above(): FRZ1's v_vir(hb) (after set_z(z)) > v*(z), mode main."""
    return SN["v_vir"](hb) > JC.vstar_kms(foot, z, "main")
def lay_split(SN, foot, z, f):
    """JNT2's lay_J: reference layout at every radius above v*(z); SRH1's lay_S at f below."""
    layout, lay_S, CUR = SN["layout"], SN["lay_S"], SN["CUR"]; settled = lay_S(foot, z, f)
    def fn(hb):
        if above(SN, hb, foot, z):
            CUR[0] = 0.0; return layout(hb, foot, mode="Rb")
        return settled(hb)
    return fn

# ------------------------------------------------------------------ the zero-velocity surface reader (criteria section 1)
MASSES = [6.5, 7, 8, 9, 9.4, 10, 10.45, 10.7, 10.9, 11.2, 11.5, 12]
_FT = {}
def _series(foot, M):
    if (foot, M) not in _FT:
        d = json.load(open(os.path.join(FLD, "runs", f"hubble_{foot}_M{M:g}_zi10_N2400.json")))
        assert d["series_cols"][1] == "z" and d["series_cols"][2] == "R_fold_kpc" and d["series_cols"][3] == "R_ta_kpc"
        _FT[(foot, M)] = np.array(d["series"])
    return _FT[(foot, M)]
_RC = {}
def rcol_kpc(foot, z, lM, col):
    """FZS1's rfold_kpc with the series column as a parameter (2 = R_fold_kpc, 3 = R_ta_kpc); physical kpc."""
    key = (foot, round(z, 6), col)
    if key not in _RC:
        vals = []
        for M in MASSES:
            S = _series(foot, M); o = np.argsort(S[:, 1]); vals.append(float(np.interp(z, S[o, 1], S[o, col])))
        _RC[key] = np.array(vals)
    R = _RC[key]
    if lM < MASSES[0]: return float(R[0] * 10 ** ((lM - MASSES[0]) / 3))
    if lM > MASSES[-1]: return float(R[-1] * 10 ** ((lM - MASSES[-1]) / 3))
    if np.any(R <= 0): return float(np.interp(lM, MASSES, R))
    return float(10 ** np.interp(lM, MASSES, np.log10(R)))
def rcol_com(NS, hb, foot, z, col, fac=1.0, cap=True):
    """the surface in FRZ1's comoving Mpc/h (FZS1's conversion), times fac, capped at r_ta (FZS1's cap)."""
    R = fac * rcol_kpc(foot, z, math.log10(NS["Mb_fold"](hb, foot) / NS["h"]), col) * 1e-3 * (1 + z) * NS["h"]
    return min(R, hb["rta"]) if cap else R
def rset_fn(NS, foot, z, which):
    """which: 'f0.5' / 'f2' -> FZS1's rset_com at fac 0.5 / 2 (unchanged); 'zv' -> R_zv (column R_ta_kpc), capped at r_ta."""
    if which == "f0.5": return lambda hb: NS["rset_com"](hb, foot, z, 0.5)
    if which == "f2": return lambda hb: NS["rset_com"](hb, foot, z, 2.0)
    if which == "zv": return lambda hb: rcol_com(NS, hb, foot, z, 3)
    raise ValueError(which)

# ------------------------------------------------------------------ the exact junction (criteria section 1)
def exact_profile(NS, hb, foot, R):
    """M_E on FRZ1's grid with R inserted as a node. NS: a namespace with layout, Bar, CUR (FZS1's or SRH1's prefix).
    Returns (r, M_E, info); info carries t, the index of R, C_B(R), C_R(R), C_tot, and the B and Rb rows for checks."""
    layout, Bar, CUR = NS["layout"], NS["Bar"], NS["CUR"]
    CUR[0] = R
    rB, MB, inf = layout(hb, foot, mode="B"); rR, MR, _ = layout(hb, foot, mode="Rb"); CUR[0] = 0.0
    if R <= 0 or inf["regime"] == "L":
        return rR, MR, dict(inf, R_set=R, t=None, ref=True, MB=MB, MR=MR)
    assert len(rB) == len(rR) and np.array_equal(rB, rR)
    assert abs(rB[-1] / hb["rta"] - 1) < 1e-12
    bar = Bar(hb, foot, rB); CB, CR = MB - bar, MR - bar
    i = int(np.argmin(abs(rB - R))); assert abs(rB[i] / R - 1) < 1e-12
    Ctot = CR[-1]
    if i == len(rB) - 1:
        t = None; M = MB.copy()
    else:
        den = Ctot - CR[i]; assert den != 0
        t = (Ctot - CB[i]) / den
        M = np.where(rB <= rB[i], MB, bar + CB[i] + t * (CR - CR[i]))
    return rB, M, dict(inf, R_set=R, t=(None if t is None else float(t)), i=i, CB_R=float(CB[i]), CR_R=float(CR[i]), Ctot=float(Ctot),
                       ref=False, MB=MB, MR=MR, bar=bar, CB=CB, CR=CR)
def lay_E(NS, foot, z, which, above_fn):
    """the crossing-speed split with the exact junction: reference above v*(z), exact junction at rset_fn(which) below."""
    rfun = rset_fn(NS, foot, z, which)
    def fn(hb):
        if above_fn(hb):
            NS["CUR"][0] = 0.0; r, M, inf = NS["layout"](hb, foot, mode="Rb"); return r, M, dict(inf, split_ref=True, R_set=0.0, t=None)
        R = rfun(hb); r, M, inf = exact_profile(NS, hb, foot, R)
        return r, M, dict(regime=inf["regime"], R_set=R, t=inf["t"], capped=bool(R >= hb["rta"]), split_ref=False)
    return fn
EWHICH = {"SE0.5": "f0.5", "SE2": "f2", "SEzv": "zv"}

_SN = None
def srh1():
    global _SN
    if _SN is None:
        src = open(SRH).read(); cut = src.index("# ------------------------------------------------------------------ checkpointed run\n")
        ns = {"__file__": SRH, "__name__": "srh1_lib_srf1"}
        with contextlib.redirect_stdout(io.StringIO()):
            exec(compile(src[:cut], SRH, "exec"), ns)
        _SN = ns
    return _SN

def Uk(r, Mc, k):
    dM = np.diff(Mc); rm = 0.5 * (r[1:] + r[:-1]); x = np.outer(k, rm)
    j0 = np.where(x > 1e-6, np.sin(x) / np.maximum(x, 1e-30), 1.0)
    return Mc[0] + j0 @ dM

def build(z):
    SN = srh1(); F = SN["F"]; L = SN["L"]; SN["set_z"](z)
    layout, lay_S = SN["layout"], SN["lay_S"]
    HB = L["HB"]; LM = L["LM"]; RHO = L["RHO_M"]; W = L["W_M"]; B = L["BIAS"]; D = F["S"]["D"]
    k = KT[1:]; PL = L["P_lin"](k) * D * D
    nM = len(HB)
    def U_of_fn(fn, infos=None):
        U = np.empty((nM, len(KT)))
        for i, hb in enumerate(HB):
            r, Mc, inf = fn(hb); U[i] = Uk(r, Mc, KT)
            if infos is not None: infos.append(inf)
        return U
    def p1I(U, norm):
        p1 = np.sum(W[:, None] * (U[:, 1:] / RHO) ** 2, 0); I = np.sum(W[:, None] * B[:, None] * U[:, 1:] / RHO, 0)
        return p1, I / norm
    SN["CUR"][0] = 0.0
    Ustd = np.empty((nM, len(KT)))
    for i, hb in enumerate(HB):
        r = L["rgrid"](hb, hb["r200"]); Ustd[i] = Uk(r, L["M_L"](hb, r), KT)
    p1s, Is = p1I(Ustd, 1.0); Is = Is + L["A_MISS"]; Pstd = p1s + PL * Is ** 2
    out = {}
    for ft in FOOTS:
        UL = U_of_fn(lambda hb: layout(hb, ft, mode="L")); p1, I = p1I(UL, L["NORM_TA"]); PLt = p1 + PL * I ** 2
        UR = U_of_fn(lambda hb: layout(hb, ft, mode="Rb")); p1R, IR = p1I(UR, L["NORM_TA"]); PR = p1R + PL * IR ** 2
        US = {}; spec = {}; einfo = {}
        for f in TAB_F:
            U = U_of_fn(lay_S(ft, z, f)); US[fkey(f)] = U
        for f in SPLIT_F:
            U = U_of_fn(lay_split(SN, ft, z, f)); US[skey(f)] = U
        for key in EKEYS:
            inf = []; US[key] = U_of_fn(lay_E(SN, ft, z, EWHICH[key], lambda hb: above(SN, hb, ft, z)), inf)
            ts = [d["t"] for d in inf if d["t"] is not None]; bel = [d for d in inf if not d["split_ref"]]
            einfo[key] = dict(t_min=float(min(ts)) if ts else None, t_max=float(max(ts)) if ts else None, n_below=len(bel),
                              n_capped=int(sum(d["capped"] for d in bel)), n_regime_L=int(sum(d["regime"] == "L" for d in bel)),
                              R_set=[float(d["R_set"]) for d in inf], t=[d["t"] for d in inf])
        nab = sum(1 for hb in HB if above(SN, hb, ft, z))
        for key, U in US.items():
            p1S, IS = p1I(U, L["NORM_TA"]); PS = p1S + PL * IS ** 2
            spec[key] = dict(PSta=PS, D2h=PL * (IS ** 2 - IR ** 2), D1h=p1S - p1R,
                             Rcold=(1 + (PS - PLt) / Pstd) / (1 + (PR - PLt) / Pstd), Rta=PS / PR)
        # painted bins (FRZ3R's halo_parts binning on log M 8..15)
        sel = (LM >= 8.0 - 1e-9) & (LM <= 15.0 + 1e-9); idx = np.nonzero(sel)[0]; lM = LM[idx]
        edges = np.arange(8.0 - 1e-9, lM[-1] + 0.1, 0.1); bid = np.digitize(lM, edges) - 1
        nb = bid.max() + 1; Wp = W[idx]; bp = B[idx]
        bins = dict(lM_lo=np.array([edges[i] for i in range(nb)]), Wsum=np.array([Wp[bid == i].sum() for i in range(nb)]),
                    bias=np.array([np.sum(Wp[bid == i] * bp[bid == i]) / max(Wp[bid == i].sum(), 1e-300) for i in range(nb)]))
        ab_p = np.array([above(SN, HB[j], ft, z) for j in idx], float)
        bins["frac_above"] = np.array([ab_p[bid == i].mean() if np.any(bid == i) else 0.0 for i in range(nb)])
        def binmean(U):
            o = np.zeros((nb, len(KT)))
            for i in range(nb):
                m = bid == i; Ne = Wp[m]
                if Ne.sum() > 0: o[i] = np.sum((Ne / Ne.sum())[:, None] * U[idx][m], 0)
            return o
        UbR = binmean(UR); Ub = {key: binmean(U) for key, U in US.items()}
        pad = lambda a: np.concatenate([[a[0]], a])
        p1_Rb_painted = np.sum(Wp[:, None] * (UR[idx] / RHO) ** 2, 0)
        out[ft] = dict(RHO=RHO, D=D, n_above=nab, n_grid=nM, vstar=JC.vstar_kms(ft, z, "main"), Mta_sum_painted=float(np.sum(Wp * UR[idx][:, 0])), p1_Rb=p1_Rb_painted,
                       PRta=pad(PR), Pstd=pad(Pstd), PLt=pad(PLt), bins=bins, UbR=UbR, einfo=einfo,
                       Ub={key: (Ub[key] - UbR) for key in Ub}, spec={key: {q: pad(v) for q, v in s.items()} for key, s in spec.items()})
    return out

def tables(z):
    f = os.path.join(PARTS, f"tables_z{z:.1f}.npz")
    if os.path.exists(f): return np.load(f, allow_pickle=True)["T"].item()
    T = build(z); tmp = f + ".tmp.npz"; np.savez(tmp, T=np.array(T, dtype=object)); os.replace(tmp, f)
    return T

if __name__ == "__main__":
    import time
    for z in [float(x) for x in sys.argv[1:]]:
        t0 = time.time(); T = tables(z)
        print(f"tables z {z:.1f}: {time.time() - t0:.0f} s", flush=True)
