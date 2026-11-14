#!/usr/bin/env python3
"""XJ1R (FROZEN_CRITERIA.md sections 2, 3 and 5): COPY of FWN1's fwn1_tables.py (closure_2026_11_13/
FWN1_forest_flux_split_f_ceiling) with the split keys changed to S5.00 (control: FWN1's case, SRH1's lay_S at f = 5 inside
FWN1's split, unchanged), SEc2 and SEc3 (the exact junction at R_set = R_k, k = 2, 3, from this lane's shell runs through
xj1r_rk.rk_kpc with FZS1's rules, FZS1's Mb_fold, x 1e-3 (1 + z) h, capped at r_ta; reference above v*(z)). The profile
known answers KP1 to KP7 are evaluated per z and footing while the tables are built. Everything else is FWN1's code unchanged.
FWN1's docstring follows.
FWN1 (FROZEN_CRITERIA.md fab8a8ee0e, section 2): COPY of FRZ6's frz6_tables.py (closure_2026_11_13/
FRZ6_forest_flux_candidate_graded) with the split keys changed to S3.00 (control), S5.00, S10.00 and Sinf (f = inf: SRH1's
lay_S at f = inf, R_set = r_ta, below v*; the reference above). Adds the known-answer (g1) table check per footing.
Everything else is FRZ6's code unchanged. FRZ6's docstring follows.
FRZ6 (FROZEN_CRITERIA.md, section 2): COPY of FRZ4's frz4_tables.py (closure_2026_11_13/FRZ4_forest_flux_graded) with three
added table keys S1.25, S2.00, S3.00: the crossing-speed split of JNT2 (jnt2_common.py lines 7 to 18, vstar_kms mode "main";
jnt2_hm.py lines 29 to 45, above() and lay_J): a halo with FRZ1's v_vir(hb) > v*(z) keeps the reference layout (mode "Rb")
at every radius, every other halo gets SRH1's lay_S at f. Every U / f = inf key and every other array is FRZ4's code
unchanged. FRZ4's docstring (from SRF1) follows.
FRZ4: halo-model tables per (z, footing). COPY of SRF1's srf1_tables.py
(closure_2026_11_12/SRF1_settled_radius_flux_window, commit f9c71956d9) with the table list cut to f = 0, 1, 2, 3, inf and
no R_set-doubled key; nothing in the profile builder changes. SRF1's docstring follows.
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
PARTS = os.path.join(HERE, "tmp"); os.makedirs(PARTS, exist_ok=True)       # temporary tables (deleted at the end)
FOOTS = ("canonical", "alt")
KT = np.concatenate([[0.0], np.geomspace(1e-3, 400.0, 900)])      # FRZ3R's table grid (frz3r_core.KT)
SRH1_GRID = [0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80, 0.90, 1.00, 1.25, 1.50, 2.00]
CASES = [1.00, 2.00, 3.00, math.inf]
TAB_F = [0.0] + CASES
def fkey(f): return "finf" if math.isinf(f) else f"f{f:.2f}"
KEYS = [fkey(f) for f in TAB_F]
SPLIT_F = [5.00]                                                 # XJ1R: control S5.00 (FWN1's case)
def skey(f): return "Sinf" if math.isinf(f) else f"S{f:.2f}"
XK = (2, 3)                                                      # XJ1R: the exact junction at R_k, k = 2, 3
def xkey(k): return f"SEc{k}"
SKEYS = [skey(f) for f in SPLIT_F] + [xkey(k) for k in XK]
sys.path.insert(0, HERE)
import xj1r_rk as RK
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

# ------------------------------------------------------------------ XJ1R: the exact junction (FROZEN_CRITERIA.md section 2)
def rset_k(SN, hb, foot, z, k):
    """R_set = R_k(z, M_b) in FRZ1's comoving Mpc/h, FZS1's Mb_fold and conversion, capped at r_ta; no constant."""
    h = SN["h"]; R = RK.rk_kpc(foot, z, math.log10(SN["Mb_fold"](hb, foot) / h), k) * 1e-3 * (1 + z) * h
    return min(R, hb["rta"])
def junction(SN, hb, foot, R):
    """M(r) = M_B(r) for r <= R; Bar + C_B(R) + t [C_R(r) - C_R(R)] outside, t = [C_tot - C_B(R)] / [C_tot - C_R(R)]."""
    layout, CUR, Bar = SN["layout"], SN["CUR"], SN["Bar"]
    if R <= 0:
        CUR[0] = 0.0; rR, MR, inf = layout(hb, foot, mode="Rb"); return rR, MR, dict(inf, R_set=0.0, t=None)
    CUR[0] = R
    rB, MB, inf = layout(hb, foot, mode="B"); rR, MR, _ = layout(hb, foot, mode="Rb"); CUR[0] = 0.0
    if inf["regime"] == "L": return rR, MR, dict(inf, R_set=R, t=None)
    assert len(rB) == len(rR) and np.array_equal(rB, rR)
    assert abs(rB[-1] / hb["rta"] - 1) < 1e-12
    if R >= rB[-1] * (1 - 1e-12): return rB, MB.copy(), dict(inf, R_set=R, t=None, all_inside=True)
    bar = Bar(hb, foot, rB); CB, CR = MB - bar, MR - bar
    i = int(np.argmin(abs(rB - R))); assert abs(rB[i] / R - 1) < 1e-12
    Ctot = CR[-1]; t = (Ctot - CB[i]) / (Ctot - CR[i])
    M = np.where(rB <= rB[i], MB, bar + CB[i] + t * (CR - CR[i]))
    return rB, M, dict(inf, R_set=R, t=float(t), i_set=i)
def lay_X(SN, foot, z, k, KP=None):
    """the statement: reference at every radius above v*(z); the exact junction at R_k below. KP collects KP1-KP4, KP7."""
    def fn(hb):
        if above(SN, hb, foot, z):
            SN["CUR"][0] = 0.0; return SN["layout"](hb, foot, mode="Rb")
        R = rset_k(SN, hb, foot, z, k); r, M, inf = junction(SN, hb, foot, R)
        if KP is not None:
            Mta = hb["Mta"]
            if inf.get("t") is not None:
                CUR = SN["CUR"]; CUR[0] = R; rB, MB, _ = SN["layout"](hb, foot, mode="B"); CUR[0] = 0.0
                ins = r <= R * (1 + 1e-12); KP["kp1"] = max(KP["kp1"], float(np.max(np.abs(M[ins] - MB[ins]))))
                KP["t"].append(inf["t"]); KP["kp4_min_t"] = min(KP["kp4_min_t"], inf["t"])
            KP["kp2"] = max(KP["kp2"], abs(M[-1] - Mta) / Mta)
            KP["kp3"] = min(KP["kp3"], float(np.min(np.diff(M)) / Mta) if len(M) > 1 else 0.0)
            KP["rset"][id(hb)] = R; KP["rset_over_rta"].append(R / hb["rta"])
        return r, M, inf
    return fn

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
        for f in SPLIT_F:
            U = U_of_fn(lay_split(SN, ft, z, f)); US[skey(f)] = U
        nab = sum(1 for hb in HB if above(SN, hb, ft, z))
        abv = np.array([above(SN, hb, ft, z) for hb in HB], bool)
        KPS = {}
        for kk in XK:
            KP = dict(kp1=0.0, kp2=0.0, kp3=0.0, kp4_min_t=math.inf, t=[], rset={}, rset_over_rta=[])
            US[xkey(kk)] = U_of_fn(lay_X(SN, ft, z, kk, KP)); KPS[kk] = KP
        # KP5: R_set forced to r_ta (law's layout = FWN1's finf row), to 0 (reference, exact), to the first grid node (continuity)
        U0 = U_of_fn(lambda hb: (SN["layout"](hb, ft, mode="Rb") if above(SN, hb, ft, z) else junction(SN, hb, ft, 0.0)))
        Uta = U_of_fn(lambda hb: (SN["layout"](hb, ft, mode="Rb") if above(SN, hb, ft, z) else junction(SN, hb, ft, hb["rta"])))
        cont = 0.0
        for i, hb in enumerate(HB):
            if abv[i]: continue
            SN["CUR"][0] = 0.0; r0 = SN["layout"](hb, ft, mode="Rb")[0][0]
            rj, Mj, _ = junction(SN, hb, ft, r0); rR, MR, _ = SN["layout"](hb, ft, mode="Rb")
            if len(rj) == len(rR): cont = max(cont, float(np.max(np.abs(Mj - MR))) / hb["Mta"])
            else: cont = math.inf
        bl = ~abv
        kp5 = dict(ta_vs_finf_rel=float(np.max(np.abs(Uta[bl] - US["finf"][bl]) / np.abs(US["finf"][bl][:, :1]))) if bl.any() else 0.0,
                   zero_vs_ref_abs=float(np.max(np.abs(U0 - UR))), first_node_vs_ref_over_Mta=cont)
        kp5["pass_"] = bool(kp5["ta_vs_finf_rel"] <= 1e-12 and kp5["zero_vs_ref_abs"] == 0.0 and kp5["first_node_vs_ref_over_Mta"] <= 1e-6)
        kp6 = {xkey(kk): float(np.max(np.abs(US[xkey(kk)][abv] - UR[abv]))) if abv.any() else 0.0 for kk in XK}
        kp7 = all(KPS[3]["rset"][id(hb)] <= KPS[2]["rset"][id(hb)] for hb in HB if id(hb) in KPS[3]["rset"] and id(hb) in KPS[2]["rset"])
        kp = {}
        for kk in XK:
            K_ = KPS[kk]; tt = np.array(K_["t"]) if K_["t"] else np.array([np.nan])
            kp[xkey(kk)] = dict(KP1_max_abs_inside=K_["kp1"], KP2_max_rel_Mta=K_["kp2"], KP3_min_diff_over_Mta=K_["kp3"], KP4_min_t=K_["kp4_min_t"],
                                t_min=float(np.nanmin(tt)), t_median=float(np.nanmedian(tt)), t_max=float(np.nanmax(tt)), n_t=len(K_["t"]),
                                rset_over_rta_median=float(np.median(K_["rset_over_rta"])) if K_["rset_over_rta"] else None,
                                rset_over_rta_max=float(np.max(K_["rset_over_rta"])) if K_["rset_over_rta"] else None,
                                n_capped=int(sum(1 for x in K_["rset_over_rta"] if x >= 1 - 1e-12)),
                                KP6_above_vs_ref_abs=kp6[xkey(kk)])
            kp[xkey(kk)]["pass_"] = bool(K_["kp1"] == 0.0 and K_["kp2"] <= 1e-9 and K_["kp3"] >= -1e-9 and K_["kp4_min_t"] >= -1e-12 and kp6[xkey(kk)] == 0.0 and kp5["pass_"] and kp7)
        g1 = dict(KP=kp, KP5=kp5, KP7=bool(kp7), n_below=int(bl.sum()), n_above=int(abv.sum()))
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
        out[ft] = dict(RHO=RHO, D=D, n_above=nab, g1=g1, kp=g1, n_grid=nM, vstar=JC.vstar_kms(ft, z, "main"), Mta_sum_painted=float(np.sum(Wp * UR[idx][:, 0])), p1_Rb=p1_Rb_painted,
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
# kappa = 1/2 FITTED; not theory closed. Adopts nothing.
