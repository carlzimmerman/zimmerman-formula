#!/usr/bin/env python3
"""SRF1 (FROZEN_CRITERIA.md, fa73352ceb): halo-model tables per (z, footing).
SRH1's srh1_hm.py is executed read-only up to its "checkpointed run" marker (it executes FRZ1's frz1_hm.py prefix and reads
FLD1's run files); its lay_S gives the settled profile. For every f in the table list: U_S(f) on FRZ3R's KT grid for the
whole mass grid; turnaround-scope spectra P_S,ta, I_S; record-convention R_cold (FRZ1's convention); painted-bin mean
profiles (FRZ3R's 0.1 dex bins, log M 8 to 15). Written to parts/tables_z<z>.npz (temporary; deleted at the end).
kappa = 1/2 FITTED; not theory closed. Adopts nothing."""
import os, sys, io, math, contextlib, warnings
warnings.filterwarnings("ignore")
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
SRH = os.path.join(REPO, "closure_2026_11_10", "SRH1_settled_radius_history", "srh1_hm.py")
PARTS = os.path.join(HERE, "parts"); os.makedirs(PARTS, exist_ok=True)
FOOTS = ("canonical", "alt")
KT = np.concatenate([[0.0], np.geomspace(1e-3, 400.0, 900)])      # FRZ3R's table grid (frz3r_core.KT)
SRH1_GRID = [0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80, 0.90, 1.00, 1.25, 1.50, 2.00]
FLUX_GRID = [0.30, 0.50, 0.70, 0.80, 0.90, 1.00, 1.10, 1.20, 1.30, 1.40, 1.50, 2.00, 3.00, math.inf]
TAB_F = sorted(set(SRH1_GRID + FLUX_GRID + [0.0]))
def fkey(f): return "finf" if math.isinf(f) else f"f{f:.2f}"
KEYS = [fkey(f) for f in TAB_F] + ["MU2"]

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
    layout, lay_S = SN["layout"], SN["lay_S"]; orig_rset = SN["rset_com"]
    HB = L["HB"]; LM = L["LM"]; RHO = L["RHO_M"]; W = L["W_M"]; B = L["BIAS"]; D = F["S"]["D"]
    k = KT[1:]; PL = L["P_lin"](k) * D * D
    nM = len(HB)
    def U_of_fn(fn):
        U = np.empty((nM, len(KT)))
        for i, hb in enumerate(HB):
            r, Mc, _ = fn(hb); U[i] = Uk(r, Mc, KT)
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
        US = {}; spec = {}
        for f in TAB_F:
            U = U_of_fn(lay_S(ft, z, f)); US[fkey(f)] = U
        SN["rset_com"] = lambda hb, foot, zz, fac=1.0, zfold=None: min(2.0 * orig_rset(hb, foot, zz, fac, zfold), hb["rta"])
        try:
            US["MU2"] = U_of_fn(lay_S(ft, z, 1.0))
        finally:
            SN["rset_com"] = orig_rset
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
        def binmean(U):
            o = np.zeros((nb, len(KT)))
            for i in range(nb):
                m = bid == i; Ne = Wp[m]
                if Ne.sum() > 0: o[i] = np.sum((Ne / Ne.sum())[:, None] * U[idx][m], 0)
            return o
        UbR = binmean(UR); Ub = {key: binmean(U) for key, U in US.items()}
        pad = lambda a: np.concatenate([[a[0]], a])
        p1_Rb_painted = np.sum(Wp[:, None] * (UR[idx] / RHO) ** 2, 0)
        out[ft] = dict(RHO=RHO, D=D, Mta_sum_painted=float(np.sum(Wp * UR[idx][:, 0])), p1_Rb=p1_Rb_painted,
                       PRta=pad(PR), Pstd=pad(Pstd), PLt=pad(PLt), bins=bins, UbR=UbR,
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
