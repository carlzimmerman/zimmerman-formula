#!/usr/bin/env python3
"""RF4_lensing_native_template (criteria 5632124ef4): separability of the data-built two-halo; arms E, N, Z and the law on TL1's stack (G1), SI3's Delta_c with more clones (G2) and GH1's matched hosts (G3).
GH2's text and SI3's text (through si3_a2.py's own replacements) are executed, never re-coded; only the file names of the clone sums change.
    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 -I rf4_grade.py <work_dir>      RF4_MUTATE=1: far range and counts from the mutated runs, halos x 0.5
kappa = 1/2 FITTED; c_f EXTERNAL in arm E; footings graded separately; cold dark energy is a gravitating field component, never a particle; not theory closed."""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
import io, json, math, time, contextlib, resource
RF4 = os.path.dirname(os.path.abspath(__file__)); REB0 = os.path.dirname(RF4); SI3D = os.path.join(REB0, "SI3_nested_isolation"); sys.path.insert(0, SI3D); sys.path.insert(0, os.path.join(REB0, "X76_galaxy_fair_share_halos"))
import numpy as np
from scipy import stats
from scipy.special import i0e
from scipy.spatial import cKDTree
from scipy.optimize import brentq
T00 = time.time(); RF4_WORK = sys.argv[1]; RF4_MUT = os.environ.get("RF4_MUTATE") == "1"; RF4_TAG = "_MUTATE" if RF4_MUT else ""; R4 = dict(lane="RF4_lensing_native_template", criteria="5632124ef4", mutate=RF4_MUT, K={}, TS={}); RF4_OUT = []
def W_(s=""): print(s, flush=True); RF4_OUT.append(str(s))
def tk(): return f"[{time.time() - T00:.0f} s, {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9:.2f} GB]"
RF4_K = {}
def K_(n, ok, v): RF4_K[n] = bool(ok); R4["K"][n] = str(v); W_(f"{n}: {'PASS' if ok else 'FAIL'}  {v}")
# ============================================================ GH2's machinery (X78, X53's smooth halos), read-only
GH2F = os.path.join(REB0, "GH2_cgm_extent_discriminator", "gh2_discriminator.py"); T = open(GH2F).read(); CUT = "# ------------------------------------------------------------ K1 / K2 (KiDS identities) and MUTATE"; assert T.count(CUT) == 1
D2 = {"__file__": GH2F, "__name__": "gh2_ro"}; exec(compile(T[:T.index(CUT)], GH2F, "exec"), D2); G = D2["G"]; NSX, XPM, AQ2, RG, fitX, IDX_ALLX, RnX, INVX, LMGX, H_N = G["NS"], G["XP"], D2["AQ"], G["RG_ALL"], G["fit"], G["IDX_ALL"], G["Rn"], G["INV"], G["LMG"], G["H_NAT"]; hot_of = D2["hot_of"]; g09_chi2 = D2["g09_chi2"]; W_(f"GH2 machinery {tk()}")
k1 = {}
for k_, ref in ((1, (437.9, 66.2)), (3, (140.6, 757.8))):
    mH_, mL_ = D2["lens_models"]("canonical", hot_of(k_)); g_ = D2["lens_grade"](mH_, mL_); k1[k_] = (g_["H2H_b34"], g_["L2H_b34"], ref)
K_("K1_GH2_TL1_numbers", all(abs(v[0] - v[2][0]) <= 0.1 and abs(v[1] - v[2][1]) <= 0.1 for v in k1.values()), k1)
g9 = g09_chi2("canonical", 1); K_("K6a_GH2_G09", abs(g9["H"] - 17.7) <= 0.1 and abs(g9["L"] - 10.1) <= 0.1, g9)
# ============================================================ arms: M(r) on RG, per catalogue lg M* l
BMAP = G["baryons"]; ST = dict(d=0.0); FACT = 0.5 if RF4_MUT else 1.0
def bar_shift(l, hot):
    Ms, Mc, Mh = BMAP(l, hot); return Ms * 10 ** ST["d"], Mc, Mh
G["baryons"] = bar_shift
RGT = json.load(open(os.path.join(REB0, "RG1_native_n_regrade", "rg1_rule_table.json"))); FC = RGT["fc"]; LGR = np.array(RGT["lg"]); LSA = np.log10(np.array(RGT["A"]))
BGA = NSX["BG"]["A_c2b_refit"]; BGH = BGA["h"]; RHOC0 = 2.775e11 * BGH ** 2 / 1e18; OMN = NSX["OM_NAT"]
ZNJ = json.load(open(os.path.join(REB0, "ZN1_zooms_to_z0", "zn1_shapes.json"))); ZX = np.log(np.array(ZNJ["x"]))
def Bs(x): x = np.asarray(x, float); return 4 * (np.arcsinh(x) - x / np.sqrt(1 + x * x))
def r0_of(M, R, S): return NSX["solve_r0"](M, R, S)                      # X38's compact root, saturation counted, as FC1 and RG1
def em1(l, hot):
    Ms, Mc, Mh = bar_shift(l, hot); return 10 ** (BGA["a"] + BGA["b"] * (math.log10(Ms + Mc) - 10.0)), Ms, Mc, Mh
def zshape(lg, snap):
    Tb = sorted(((ZNJ[m][snap]["lgM"], np.array(ZNJ[m][snap]["lnm"]), ZNJ[m][snap]["x_edge"]) for m in ("1e12", "1e13", "1e14")), key=lambda t: t[0])
    if lg <= Tb[0][0]: return Tb[0][1], Tb[0][2]
    if lg >= Tb[-1][0]: return Tb[-1][1], Tb[-1][2]
    i = next(j for j in range(2) if Tb[j][0] <= lg <= Tb[j + 1][0]); w = (lg - Tb[i][0]) / (Tb[i + 1][0] - Tb[i][0]); return (1 - w) * Tb[i][1] + w * Tb[i + 1][1], min(Tb[i][2], Tb[i + 1][2])
def arm(name, foot, l, k, zs=0.25):
    hot = hot_of(k)
    if name == "L": return G["mass_law"](foot, l, hot)
    if name == "B": Ms, Mc, Mh = bar_shift(l, hot); return Ms + Mc + Mh
    if name == "E":
        Mtot = G["mass_route_e"](foot, l, 0.285, hot)[0]; Ms, Mc, Mh = bar_shift(l, hot); return Ms + Mc + Mh + FACT * (Mtot - Ms - Mc - Mh)
    M200, Ms, Mc, Mh = em1(l, hot)
    if name in ("N", "Nta"):
        R200 = (3 * M200 / (4 * math.pi * 200 * RHOC0)) ** (1 / 3); S = 10 ** float(np.interp(math.log10(M200), LGR, LSA)); r0 = r0_of(M200, R200, S); rc = R200 if name == "N" else max(R200, XPM.rta_pc(Ms + Mc + float(np.interp(R200, RG, Mh)), 0.285)); Mo = math.pi * S * r0 ** 2 * Bs(np.minimum(RG, rc) / r0); return Ms + Mc + Mh + FACT * Mo
    if name in ("Z", "Z0"):
        Mt = M200 / FC; snap = "0.25" if name == "Z" else "0.00"; Ez2 = OMN * (1 + float(snap)) ** 3 + 1 - OMN; Rt = (3 * Mt / (4 * math.pi * 200 * RHOC0 * Ez2)) ** (1 / 3); ln, xe = zshape(math.log10(Mt), snap); x = np.minimum(RG / Rt, xe); lx = np.log(np.maximum(x, 1e-300)); return Ms + Mc + Mh + FACT * M200 * np.exp(np.where(lx >= ZX[0], np.interp(lx, ZX, ln), ln[0] + 2 * (lx - ZX[0])))
    raise KeyError(name)
# ============================================================ SI3's text, with si3_a2.py's own replacements; clone sums and catalogue names swapped to this lane's
A2T = open(os.path.join(SI3D, "si3_a2.py")).read(); blk = A2T[A2T.index("    gs = open(SG).read()"):A2T.index('    if MODE == "grade":')]; SG = os.path.join(SI3D, "si3_grade.py")
blk = "\n".join(x[4:] if x.startswith("    ") else x for x in blk.splitlines()); _sv = dict(SG=SG); exec(compile(blk, "si3_a2_block", "exec"), _sv); gs = _sv["gs"]
gs = gs.replace("si3_cats_a2", "rf4_cats").replace("si3_a2_{r}", "rf4_meas_{r}"); CUTV = 'VARS = (("D", "Delta = L - I"), ("L", "raw L"))'; assert gs.count(CUTV) == 1
_lane_argv = sys.argv; sys.argv = [SG, RF4_WORK]; __file__ = SG; exec(compile(gs[:gs.index(CUTV)], "si3_grade_head", "exec")); sys.argv = _lane_argv; WORK = RF4_WORK; W_(f"SI3 head done {tk()}")
for k_ in ("K0_F2_law_amplitudes", "K1_FC1_kids_chi2_and_b", "K2_tables_and_M200", "K_H1_estimator_vs_record", "K_H3_patches_and_weight_ratio", "K_H4_cross_null", "K_H5_halves_of_I"): K_("K3_SI3_" + k_, KOK.get(k_, False), RES["K"].get(k_))
# K2: the old 4-clone sums through this path reproduce SI3's Delta_c on S_strict, R2, canonical, FC1's rule
SI3WD = os.path.join(os.path.dirname(RF4_WORK), "si3_work"); _o = [dict(np.load(os.path.join(SI3WD, f"si3_a2_{r}.npz"))) for r in ("north", "south")]; _H0 = HOLE["I_S_strict"]; HOLE["I_S_strict"] = {q: _o[0][f"I_S_strict_{q}"] + _o[1][f"I_S_strict_{q}"] for q in ("WG", "WX", "WW", "NN")}; DV.pop(("S_strict", "D"), None)
_a = line("canonical", "R2", "S_strict", "D")["all"]; _r = json.load(open(os.path.join(SI3D, "si3_a2_results.json")))["lines"]["canonical"]["D"]["R2"]["S_strict"]["all"] if "lines" in json.load(open(os.path.join(SI3D, "si3_a2_results.json"))) else None
K_("K2_old_clones_reproduce_SI3", _r is not None and abs(_a["dchi2"] - _r["dchi2"]) <= 0.5, f"dchi2 {_a['dchi2']:+.2f} vs {None if _r is None else round(_r['dchi2'], 2)}"); HOLE["I_S_strict"] = _H0; DV.pop(("S_strict", "D"), None)
# ============================================================ miscentring operator on LRT (Mpc)
RM = np.exp(LRT); DL_ = LRT[1] - LRT[0]; NRT = len(RM)
def mis_matrix(sig):
    """K with DS_off = K DS on LRT: Gaussian offset of width sig (Mpc). Sigma-bar from DS by integration with an R^-1.5 tail past 8 Mpc; mass inside the first node handled as an offset point mass."""
    Sb = np.zeros((NRT, NRT))
    for i in range(NRT):
        for j in range(i, NRT): Sb[i, j] = 2 * DL_ * (0.5 if j in (i, NRT - 1) else 1.0) * math.tanh(DL_) / DL_        # trapezoid made exact for R^-2 cells
        Sb[i, -1] += 2 / 1.5
    S = Sb - np.eye(NRT); Min = math.pi * RM[0] ** 2 * Sb[0]
    q = RM[None, :] * RM[:, None] / sig ** 2; Gk = np.exp(-(RM[None, :] - RM[:, None]) ** 2 / (2 * sig ** 2)) * i0e(q) / sig ** 2 * RM[None, :] ** 2 * DL_
    So = Gk @ S + np.exp(-RM ** 2 / (2 * sig ** 2))[:, None] @ Min[None, :] / (2 * math.pi * sig ** 2); Sbo = np.zeros_like(So)
    cum = 0.5 * RM[0] ** 2 * So[0]; Sbo[0] = So[0]
    for i in range(1, NRT): cum = cum + 0.5 * math.tanh(DL_) * (RM[i] ** 2 * So[i] + RM[i - 1] ** 2 * So[i - 1]); Sbo[i] = 2 * cum / RM[i] ** 2
    return Sbo - So
_s = 0.2; _K = mis_matrix(_s); _p = _K @ (1.0 / (math.pi * RM ** 2)); _x = RM ** 2 / (2 * _s ** 2); _e = (1 - np.exp(-_x)) / (math.pi * RM ** 2) - np.exp(-_x) / (2 * math.pi * _s ** 2); _m = (RM >= 0.1 * _s) & (RM <= 3.0); _d = float(np.max(np.abs(_p - _e)[_m] / (np.abs(_e[_m]) + 1e-3 * np.abs(_e).max())))
K_("K5_miscentring_closed_form", _d <= 0.01, f"max rel dev {_d:.4f} on R >= 0.1 sigma to 3 Mpc")
# sigma_off and the satellite fraction from G3C members, G09
import csv
EXTD = os.path.join(os.path.dirname(os.path.dirname(REB0)), "_external_data"); G75 = G["G75"]; ZGr = np.linspace(0, 1.5, 3001); _E = np.sqrt(OMN * (1 + ZGr) ** 3 + 1 - OMN); CHIn = np.r_[0, np.cumsum(0.5 * (1 / _E[1:] + 1 / _E[:-1]) * np.diff(ZGr))] * 299792.458 / (100 * H_N); DAn = lambda z: np.interp(z, ZGr, CHIn) / (1 + z)
import pandas as pd
gg = pd.read_csv(os.path.join(EXTD, "cfg519_work", "G3CGalv10.csv")); fg = pd.read_csv(os.path.join(EXTD, "cfg519_work", "G3CFoFGroupv10.csv")); gk = pd.read_csv(os.path.join(EXTD, "gama_dr4_gkv", "gkv_stellarmass_g09.csv"), usecols=["CATAID", "logmstar"]); gm = gg.merge(gk, on="CATAID").merge(fg[["GroupID", "Nfof", "IterCenRA", "IterCenDec", "IterCenCATAID", "BCGCATAID"]], on="GroupID", how="left")
_b = (gm["logmstar"] >= 10.5) & (gm["logmstar"] < 11.0) & (gm["Z"] > 0.02) & (gm["Z"] < 0.5); _sat = _b & (gm["GroupID"] > 0) & (gm["Nfof"] >= 3) & (gm["CATAID"] != gm["IterCenCATAID"]); _anyg = _b & (gm["GroupID"] > 0) & (gm["CATAID"] != gm["IterCenCATAID"])
_R = np.hypot((gm["RA"][_sat] - gm["IterCenRA"][_sat]) * np.cos(np.radians(gm["Dec"][_sat])), gm["Dec"][_sat] - gm["IterCenDec"][_sat]) * np.pi / 180 * DAn(gm["Z"][_sat].values); SIG_OFF = float(np.sqrt(np.mean(_R ** 2) / 2)); FSAT_G3C = float(_anyg.sum() / _b.sum())
_bc = fg[(fg["Nfof"] >= 5) & (fg["BCGCATAID"] != fg["IterCenCATAID"])]; R4["miscentring"] = dict(sigma_off_Mpc=SIG_OFF, n_sat=int(_sat.sum()), fsat_G3C_G09=FSAT_G3C, f_primary=0.28, band=[0.12, 0.49], frac_groups5_BCG_not_itercen=float(len(_bc) / max((fg["Nfof"] >= 5).sum(), 1))); W_(f"sigma_off {SIG_OFF:.3f} Mpc from {int(_sat.sum())} G3C members; G3C satellite fraction in G09 at lg M* 10.5-11: {FSAT_G3C:.3f}")
json.dump(R4["miscentring"], open(os.path.join(RF4, "rf4_miscentring.json"), "w"), indent=1); KOFF = mis_matrix(SIG_OFF)
# ============================================================ tables
LGC = np.arange(8.5, 11.81, 0.1); RGPC = RM * 1e6; TABC = {}
def tab_of(name, foot, k, rung="R0"):
    key = (name, foot if name in ("E", "L") else "any", k, rung)
    if key not in TABC:
        ST["d"] = 0.0 if rung == "R0" else SHIFT; c = np.array([AQ2.delta_sigma(RGPC, RG, arm(name, foot, float(l), k), "const") for l in LGC]); ST["d"] = 0.0; TABC[key] = np.array([np.interp(LMG, LGC, c[:, j]) for j in range(NRT)]).T
    return TABC[key]
def blend(tab, f): return (1 - f) * tab + f * tab @ KOFF.T
def perlens(name, foot, k, rg, f):
    m0 = perlens_model(blend(tab_of(name, foot, k, "R0"), f), REST)
    return m0 if rg == "R0" else np.where(RED[:, None], perlens_model(blend(tab_of(name, foot, k, "R2"), f), REST), m0)
# ============================================================ template and amplitude
CZ = np.load(os.path.join(RF4_WORK, f"rf4_counts{RF4_TAG}.npz")); EDG = CZ["EDG"]; RCE = np.sqrt(EDG[1:] * EDG[:-1]); AR = math.pi * (EDG[1:] ** 2 - EDG[:-1] ** 2); FZ = np.load(os.path.join(RF4_WORK, f"rf4_far{RF4_TAG}.npz")); RFE = FZ["REDG"]; RFC = np.sqrt(RFE[1:] * RFE[:-1]); FAR = RFC > 3.0; NFR = int(FAR.sum())
def Eprof(s, name, cut=0, patch=None):
    C = CZ[f"{s}_{name}_C"][cut]; Wt = CZ[f"{s}_{name}_W"]
    if patch is not None: C = C.sum(0) - C[patch]; Wt = Wt.sum(0) - Wt[patch]
    else: C = C.sum(0); Wt = Wt.sum(0)
    return C / np.maximum(Wt[:, None], 1e-300) / AR
def Tprof(s, comp, cut=0, Rx=0.15, patch=None):
    Ee = Eprof(s, "L", cut, patch) - Eprof(s, comp, cut, patch); Ee = np.where(RCE < Rx, 0.0, Ee); cum = np.cumsum(Ee * AR, axis=1) / np.cumsum(AR); return np.where(RCE < Rx, 0.0, cum - Ee)
def sig_far(s, comp, q="WG"):
    W_L, W_C = FZ[f"{s}_L_WW"], FZ[f"{s}_{comp}_WW"]; G_L, G_C = FZ[f"{s}_L_{q}"], FZ[f"{s}_{comp}_{q}"]
    with np.errstate(all="ignore"):
        d = G_L.sum(0) / W_L.sum(0) - G_C.sum(0) / W_C.sum(0); dj = (G_L.sum(0)[None] - G_L) / (W_L.sum(0)[None] - W_L) - (G_C.sum(0)[None] - G_C) / (W_C.sum(0)[None] - W_C)
    return d, dj
_lw = {}
def far_1h(name, foot, s="S10"):
    """arm's own one-halo at the far radii: lens-weighted mean over mass bins, at five lg M* quantiles per bin"""
    key = (name, foot, s)
    if key in _lw: return _lw[key]
    o = np.zeros((4, NFR)); Rf = RFC[FAR] * 1e6
    for b in range(4):
        m = SAMP[s] & (LBIN == b); ls = np.quantile(logMs70[m] + 2 * np.log10(0.70 / H_N), [0.1, 0.3, 0.5, 0.7, 0.9]); o[b] = np.mean([AQ2.delta_sigma(Rf, RG, arm(name, foot, float(l), 1), "const") for l in ls], axis=0)
    _lw[key] = o; return o
def amp(name, foot, s="S10", comp="R", cut=0, q="WG", per_bin=False):
    d, dj = sig_far(s, comp, q); df = d[:, FAR]; djf = dj[:, :, FAR]; var = JKF * np.sum((djf - djf.mean(0)) ** 2, axis=0); one = far_1h(name, foot, s) if q == "WG" else 0.0; rf = RFC[FAR]
    def Tf(T): return np.array([np.interp(np.log(rf), np.log(RCE), T[b]) for b in range(4)])
    tf = Tf(Tprof(s, comp, cut)); w = 1 / var
    def sol(y, tt, sel=np.ones((4, NFR), bool)): return float(np.sum((w * tt * y)[sel]) / np.sum((w * tt * tt)[sel]))
    a = sol(df - one, tf); aj = np.array([sol(djf[p] - one, Tf(Tprof(s, comp, cut, patch=p))) for p in range(NP_)]); sa = float(math.sqrt(JKF * np.sum((aj - aj.mean()) ** 2))); o = dict(a=a, sa=sa)
    if per_bin:
        o["bins"] = []
        for b in range(4):
            sel = np.zeros((4, NFR), bool); sel[b] = True; ab = sol(df - one, tf, sel); abj = np.array([sol(djf[p] - one, Tf(Tprof(s, comp, cut, patch=p)), sel) for p in range(NP_)]); o["bins"].append((ab, float(math.sqrt(JKF * np.sum((abj - abj.mean()) ** 2)))))
    return o
A_E = {f: amp("E", f, per_bin=True) for f in FOOTS}; AX = {f: amp("E", f, q="WX") for f in FOOTS}; Ab = amp("E", "canonical", cut=1); Af = amp("E", "canonical", cut=2); AMPS = {f: {nm: amp(nm, f) for nm in ("N", "Z", "L")} for f in FOOTS}; AOWN = {s: amp("E", "canonical", s=s) for s in ("S_strict", "S_x300")}
R4["amplitude"] = dict(E=A_E, N_Z_L=AMPS, cross=AX, bright=Ab, faint=Af, own_samples=AOWN); W_(f"a (E, S10 L-R, 3-15 Mpc): {A_E['canonical']['a']:.4g} +- {A_E['canonical']['sa']:.3g}; per bin {[(round(x, 5), round(y, 5)) for x, y in A_E['canonical']['bins']]}; law {AMPS['canonical']['L']}; cross {AX['canonical']}; own S_strict {AOWN['S_strict']}, S_x300 {AOWN['S_x300']} {tk()}")
# K4: the pixel estimator against the record path at 1.1-3 Mpc on S10 L - R
dF, djF = sig_far("S10", "R"); _nearF = RFC < 3.0; fm = float(np.sum(dF[:, _nearF] / (JKF * np.sum((djF - djF.mean(0)) ** 2, 0))[:, _nearF]) / np.sum(1 / (JKF * np.sum((djF - djF.mean(0)) ** 2, 0))[:, _nearF])); fmj = np.sum(djF[:, :, _nearF] / (JKF * np.sum((djF - djF.mean(0)) ** 2, 0))[:, _nearF], (1, 2)) / np.sum(1 / (JKF * np.sum((djF - djF.mean(0)) ** 2, 0))[:, _nearF])
dR, djR, vR = dvec("S10", "LR"); sO2 = RAN["O2"] & np.isfinite(dR) & (vR > 0); rm_ = float(np.sum(dR[sO2] / vR[sO2]) / np.sum(1 / vR[sO2])); rmj = np.sum(np.where(sO2, djR / np.where(vR > 0, vR, 1), 0), (1, 2)) / np.sum(1 / vR[sO2]); _lrf = np.log(RFC[_nearF]); _vR = np.where(vR > 0, vR, np.inf)
def _pix_at(dv): return np.array([np.interp(np.log(np.maximum(RMED[b], 1e-3)), _lrf, dv[b, _nearF]) for b in range(4)])
_rr = float(np.sum((_pix_at(dF) / _vR)[sO2]) / np.sum((dR / _vR)[sO2])); _rj = np.array([np.sum((_pix_at(djF[p]) / _vR)[sO2]) / np.sum((djR[p] / _vR)[sO2]) for p in range(NP_)]); _srr = float(math.sqrt(JKF * np.sum((_rj - _rj.mean()) ** 2)))
K_("K4_pixel_vs_record_1p1_3Mpc", RF4_MUT or abs(_rr - 1) <= 0.15 or abs(_rr - 1) <= 2 * _srr, f"pixel ring profile read at the record cells' median radii against the record, ivar-weighted, O2: ratio {_rr:.3f} +- {_srr:.3f} (ring-mean pixel {fm:.3f}, record {rm_:.3f}, different radii)")
# ============================================================ separability
nzj = json.load(open(os.path.join(RF4, "rf4_tracer_nz.json"))); zmean = 0.30; ic = np.searchsorted(nzj["ez"], zmean) - 1; dNdz = np.array(nzj["nz"][ic - 2:ic + 3]).mean() / 0.02; AREA = 1006.0 / 41253.0; dVdz = 4 * math.pi * AREA * float(np.interp(zmean, ZGr, CHIn)) ** 2 * 299792.458 / (100 * H_N * math.sqrt(OMN * (1 + zmean) ** 3 + 1 - OMN)); nbar = dNdz / dVdz; RHOM = OMN * 2.775e11 * H_N ** 2
def bimp(a): return RHOM / (a * 1e12 * nbar) if a > 0 else float("inf")
TSS = {}
for f in FOOTS:
    a, sa = A_E[f]["a"], A_E[f]["sa"]; ts = {}; ts["TS1"] = dict(v=a / sa, ok=bool(a / sa >= 3)); bb = np.array(A_E[f]["bins"]); ch = float(np.sum(((bb[:, 0] - a) / bb[:, 1]) ** 2)); ts["TS2"] = dict(chi2=ch, p=float(stats.chi2.sf(ch, 3)), ok=bool(stats.chi2.sf(ch, 3) >= 0.01))
    def rho_of(patch=None):
        Tb_, Tf_ = Tprof("S10", "R", 1, patch=patch), Tprof("S10", "R", 2, patch=patch); m = (RCE > 0.5) & (RCE < 3.0); return float(Ab["a"] * Tb_[:, m].sum() / (Af["a"] * Tf_[:, m].sum()))
    rho = rho_of(); rj = np.array([rho_of(p) for p in range(NP_)]); sr = float(math.sqrt(JKF * np.sum((rj - rj.mean()) ** 2))); ts["TS3"] = dict(rho=rho, s=sr, a_b=Ab["a"], a_f=Af["a"], ok=bool(abs(rho - 1) <= 0.3 or abs(rho - 1) <= 2 * sr))
    T150, T400 = Tprof("S10", "R", 0, 0.15), Tprof("S10", "R", 0, 0.40); shift = max(float(np.max(np.abs(a * (np.interp(np.log(RMED[b][RAN["O2"][b]]), np.log(RCE), T150[b]) - np.interp(np.log(RMED[b][RAN["O2"][b]]), np.log(RCE), T400[b]))) / np.sqrt(vR[b][RAN["O2"][b]]))) for b in range(4)); ts["TS4"] = dict(max_shift_sigma=float(shift), ok=bool(shift < 1))
    ax = AX[f]; rotz = 0.0
    if "S10_Lrot_C" in CZ.files:
        El = CZ["S10_Lrot_C"][0]; Wl = CZ["S10_Lrot_W"]; Cr = CZ["S10_R_C"][0]; Wr = CZ["S10_R_W"]; d0 = El.sum(0) / np.maximum(Wl.sum(0)[:, None], 1e-300) - Cr.sum(0) / np.maximum(Wr.sum(0)[:, None], 1e-300); dj0 = (El.sum(0)[None] - El) / np.maximum((Wl.sum(0)[None] - Wl)[..., None], 1e-300) - (Cr.sum(0)[None] - Cr) / np.maximum((Wr.sum(0)[None] - Wr)[..., None], 1e-300); v0 = JKF * np.sum((dj0 - dj0.mean(0)) ** 2, 0); mk = (RCE >= 0.3) & (RCE < 3.0); rotz = float(np.max(np.abs(d0[:, mk]) / np.sqrt(v0[:, mk])))
    ts["TS5"] = dict(cross_z=abs(ax["a"]) / ax["sa"], rot_mean_E_offset=float(np.mean(d0[:, mk])) if "S10_Lrot_C" in CZ.files else None, rot_maxz=rotz, ok=bool(abs(ax["a"]) / ax["sa"] < 3 and rotz < 3 and "S10_Lrot_C" in CZ.files)); bt = bimp(a); ts["TS6"] = dict(b_t=bt, nbar=nbar, ok=bool(0.3 <= bt <= 4)); TSS[f] = ts; W_(f"[{f}] TS: " + "; ".join(f"{k} {'PASS' if v['ok'] else 'FAIL'} " + json.dumps({x: (round(y, 3) if isinstance(y, float) else y) for x, y in v.items() if x != "ok"}) for k, v in ts.items()))
SEP = {f: all(v["ok"] for v in TSS[f].values()) for f in FOOTS}; R4["TS"] = TSS; R4["separable"] = SEP; STATUS = {f: ("BUILT" if SEP[f] else "two-halo UNSEPARABLE") for f in FOOTS}; W_(f"\nTWO-HALO STATUS: {STATUS} {tk()}")
# ============================================================ G1: TL1's stack, B21's bins
KG1 = [1, 1.5, 2, 3, 5]; IDX300 = [i for i in IDX_ALLX if all(RnX[b][i] <= 0.3 for b in range(4))]
def stackX(tab):
    o = np.empty((4, 15))
    for b in range(4):
        lMn = INVX[b]["logMs70"] + 2 * np.log10(0.70 / H_N) + 2 * np.log10(INVX[b]["qDA"]); w = INVX[b]["w"]; rows = np.array([np.interp(lMn, LMG, np.interp(np.log(RnX[b][i]), LRT, tab.T, )) for i in range(0)]) if False else None
        lg = np.clip(lMn, LMG[0], LMG[-1]); ix = np.clip(((lg - LMG[0]) / (LMG[1] - LMG[0])).astype(int), 0, len(LMG) - 2); fr = (lg - LMG[ix]) / (LMG[1] - LMG[0]); yR = np.array([[np.interp(np.log(RnX[b][i]), LRT, tab[j]) for j in np.unique(ix)] for i in range(15)]); ui = {u: q for q, u in enumerate(np.unique(ix))}; yR1 = np.array([[np.interp(np.log(RnX[b][i]), LRT, tab[j + 1]) for j in np.unique(ix)] for i in range(15)]); idx = np.array([ui[u] for u in ix]); o[b] = ((1 - fr)[None] * yR[:, idx] + fr[None] * yR1[:, idx]) @ w / w.sum()
    return o
def Tx(T): return np.array([np.interp(np.log(RnX[b]), np.log(RCE), T[b]) for b in range(4)])
TS10 = Tprof("S10", "R"); G1 = {}
for foot in FOOTS:
    G1[foot] = {}; ao = A_E[foot]["a"]
    for k in KG1:
        mL = stackX(blend(tab_of("L", foot, k), 0.28)); aL = AMPS[foot]["L"]["a"]; row = {}
        fL0, _ = fitX(mL, IDX_ALLX, True, T=Tx(TS10)); rL = mL + max(aL, 0) * Tx(TS10); cL = fitX(rL, IDX_ALLX, False)[0]; cL300 = fitX(mL, IDX300, False)[0]
        for nm in ("E", "N", "Nta", "Z"):
            mH = stackX(blend(tab_of(nm, foot, k), 0.28)); fH0, _ = fitX(mH, IDX_ALLX, True, T=Tx(TS10)); an = (A_E[foot]["a"] if nm == "E" else AMPS[foot][nm[0]]["a"]) if nm in ("E", "N", "Z") else AMPS[foot]["N"]["a"]; cH = fitX(mH + max(an, 0) * Tx(TS10), IDX_ALLX, False)[0]; cH300 = fitX(mH, IDX300, False)[0]; f0 = stackX(tab_of(nm, foot, k))
            d34 = sum(cH["per_bin"][2:]) - sum(cL["per_bin"][2:]); dfree = sum(fH0["per_bin"][2:]) - sum(fL0["per_bin"][2:]); row[nm] = dict(fixed_b34=sum(cH["per_bin"][2:]), fixed_all=cH["chi2"], free_b34=sum(fH0["per_bin"][2:]), free_all=fH0["chi2"], b_free=fH0["b"], d_fixed_b34=d34, d_free_b34=dfree, cls_fixed=("LAW" if d34 >= 9 else "ROUTE E" if d34 <= -9 else "NOT DIAGNOSTIC"), cls_free=("LAW" if dfree >= 9 else "ROUTE E" if dfree <= -9 else "NOT DIAGNOSTIC"), chi2_300=cH300["chi2"], n300=cH300["n"], d300=cH300["chi2"] - cL300["chi2"], f0_free_b34=sum(fitX(f0, IDX_ALLX, True, T=Tx(TS10))[0]["per_bin"][2:]))
        G1[foot][str(k)] = dict(law=dict(fixed_b34=sum(cL["per_bin"][2:]), fixed_all=cL["chi2"], free_b34=sum(fL0["per_bin"][2:]), free_all=fL0["chi2"], b_free=fL0["b"], chi2_300=cL300["chi2"], f0_free_b34=sum(fitX(stackX(tab_of("L", foot, k)), IDX_ALLX, True, T=Tx(TS10))[0]["per_bin"][2:])), arms=row)
    W_(f"G1 [{foot}] done {tk()}")
    for k in KG1:
        q = G1[foot][str(k)]; W_(f"  k {k}: law fixed/free b34 {q['law']['fixed_b34']:.1f}/{q['law']['free_b34']:.1f}; " + "; ".join(f"{n} {v['fixed_b34']:.1f}/{v['free_b34']:.1f} ({v['cls_free']}), <=300 kpc d {v['d300']:+.1f}" for n, v in q["arms"].items()))
def kstar(foot, nm, st="d_free_b34"):
    ds = [G1[foot][str(k)]["arms"][nm][st] for k in KG1]
    for i in range(len(KG1) - 1):
        if ds[i] * ds[i + 1] < 0: return float(KG1[i] + (KG1[i + 1] - KG1[i]) * ds[i] / (ds[i] - ds[i + 1]))
    return None
R4["G1"] = G1; R4["kstar"] = {f: {n: kstar(f, n) for n in ("E", "N", "Z")} for f in FOOTS}; W_(f"k*: {R4['kstar']}")
# ============================================================ G2: Delta_c
def amask(d, dj, var, m, mj, mask):
    sel = mask & np.isfinite(d) & (var > 0); w = np.where(sel, m / var, 0.0); A = float(np.sum(w * d) / np.sum(w * m)); Aj = np.sum(w[None] * dj, axis=(1, 2)) / np.sum(w[None] * mj, axis=(1, 2)); return A, float(math.sqrt(JKF * np.sum((Aj - Aj.mean()) ** 2)))
def shape(d, bk, m):
    t = sum(float(m[b, ix] @ Ci @ m[b, ix]) for b, ix, Ci, p in bk); A = sum(float(m[b, ix] @ Ci @ d[b, ix]) for b, ix, Ci, p in bk) / t; c = chi2b(bk, d - A * m); n = sum(x[3] for x in bk); return dict(A=A, sA=1 / math.sqrt(t), chi2=c, p=float(stats.chi2.sf(c, n - 1)), n=n)
def Tlens(T):
    Rnl = R70 * (0.70 / H_N) * qB[:, None]; o = np.empty_like(R70)
    for b in range(4):
        q_ = LBIN == b; o[q_] = np.stack([np.interp(np.log(Rnl[q_, k]), np.log(RCE), T[b]) for k in range(15)], 1)
    return o
def g2line(foot, nm, k, rg, s, f, afac=0.0, cut=0, v="D", tmask=None, half=None):
    """afac: multiplies a; 0 = no template (raw one-halo), 1 = a."""
    d, dj, var = dvec(s, v); bk = blocks_J(d, dj, var, RALL if tmask is None else tmask); mm, mmj = mstack(s, perlens(nm, foot, k, rg, f)); ml, mlj = mstack(s, perlens("L", foot, k, rg, f)); comp = "I" if v == "D" else "R"; Tl = None
    if afac != 0:
        Tl = Tlens(Tprof(s, comp, cut)); tt, ttj = mstack(s, Tl); an = A_E[foot]["a"] if nm == "E" else AMPS[foot][nm[0]]["a"]; al = AMPS[foot]["L"]["a"]; mm, mmj = mm + afac * max(an, 0) * tt, mmj + afac * max(an, 0) * ttj; ml, mlj = ml + afac * max(al, 0) * tt, mlj + afac * max(al, 0) * ttj
    c = compare(d, bk, ml, mm); aa = amps(d, dj, var, mm, mmj); aA = amask(d, dj, var, mm, mmj, RALL); al_ = amps(d, dj, var, ml, mlj); sh = shape(d, bk, mm); return dict(chi2=c["chi2_H"], chi2_L=c["chi2_L"], p=c["p_H"], p_L=c["p_L"], dchi2=c["dchi2"], D=c["D"], Q=c["Q"], cls=c["cls"], A_all=aA[0], sA_all=aA[1], A_in=aa["A_in"], sA_in=aa["sA_in"], A_O1=aa["A_O1"], sA_O1=aa["sA_O1"], A_O2=aa["A_O2"], sA_O2=aa["sA_O2"], law_A_in=al_["A_in"], law_sA_in=al_["sA_in"], law_A_O1=al_["A_O1"], law_A_O2=al_["A_O2"], shape=sh, n=c["n"])
G2 = {}; ARMS2 = (("E", 1), ("E", 3), ("N", 1), ("N", 3), ("Z", 1), ("Z", 3)); SM2 = ("S10", "S20", "S30", "S_strict", "S_x300"); R300 = RAN["in"]
for foot in FOOTS:
    G2[foot] = {}
    for nm, k in ARMS2:
        for rg in RUNGS:
            for s in SM2:
                key = f"{nm}{k}|{rg}|{s}"; G2[foot][key] = dict(no_T=g2line(foot, nm, k, rg, s, 0.28), T=g2line(foot, nm, k, rg, s, 0.28, 1.0), in300=g2line(foot, nm, k, rg, s, 0.28, tmask=R300))
    W_(f"G2 lines [{foot}] {tk()}")
    for nm, k in ARMS2:
        for s in ("S10", "S_strict", "S_x300"):
            q = G2[foot][f"{nm}{k}|R2|{s}"]; W_(f"  {nm}{k} R2 {s}: T: chi2 {q['T']['chi2']:.1f} (p {q['T']['p']:.2g}), law {q['T']['chi2_L']:.1f}, d {q['T']['dchi2']:+.1f} D {q['T']['D']:.1f}; A_all {q['T']['A_all']:.2f}+-{q['T']['sA_all']:.2f} A_in {q['T']['A_in']:.2f} A_O1 {q['T']['A_O1']:.2f} A_O2 {q['T']['A_O2']:.2f}; shape p {q['T']['shape']['p']:.2g} | no T: d {q['no_T']['dchi2']:+.1f} A_all {q['no_T']['A_all']:.2f} | <=300 kpc: d {q['in300']['dchi2']:+.1f} A {q['in300']['A_in']:.2f}+-{q['in300']['sA_in']:.2f}")
R4["G2"] = G2
# bands on the graded arms: f; a +- s; tracer half; rung
BANDS = {}
for foot in FOOTS:
    BANDS[foot] = {}
    for nm, k in (("E", 3), ("E", 1), ("N", 1), ("Z", 1)):
        for s in ("S10", "S_strict", "S_x300"):
            base = lambda **w: g2line(foot, nm, k, w.get("rg", "R2"), s, w.get("f", 0.28), w.get("afac", 1.0), w.get("cut", 0)); sa = A_E[foot]["sa"] / max(abs(A_E[foot]["a"]), 1e-300); rows = dict(primary=base(), f0p12=base(f=0.12), f0p49=base(f=0.49), f0=base(f=0.0), a_up=base(afac=1 + sa), a_dn=base(afac=max(1 - sa, 0.0)), bright=base(cut=1), faint=base(cut=2), R0=base(rg="R0"), noT=base(afac=0.0)); vals = [r["A_all"] for r in rows.values()]; BANDS[foot][f"{nm}{k}|{s}"] = dict(A_primary=rows["primary"]["A_all"], s=rows["primary"]["sA_all"], A_lo=min(vals), A_hi=max(vals), dchi2_lo=min(r["dchi2"] for r in rows.values()), dchi2_hi=max(r["dchi2"] for r in rows.values()), rows={k_: dict(A=r["A_all"], d=r["dchi2"], chi2=r["chi2"], pshape=r["shape"]["p"]) for k_, r in rows.items()})
    W_(f"bands [{foot}] {tk()}")
R4["bands"] = BANDS
B300 = {}
for foot in FOOTS:
    B300[foot] = {}
    for nm, k in (("E", 3), ("E", 1), ("N", 1), ("Z", 1)):
        for s in SM2:
            rows = {f"{rg}|f{f_}": g2line(foot, nm, k, rg, s, f_, tmask=R300) for rg in RUNGS for f_ in (0.28, 0.12, 0.49, 0.0)}; v_ = [r["A_in"] for r in rows.values()]; d_ = [r["dchi2"] for r in rows.values()]; pm = rows["R2|f0.28"]
            B300[foot][f"{nm}{k}|{s}"] = dict(A=pm["A_in"], s=pm["sA_in"], A_lo=min(v_), A_hi=max(v_), d=pm["dchi2"], D=pm["D"], d_lo=min(d_), d_hi=max(d_), pshape=pm["shape"]["p"], cls=pm["cls"], law_A=pm["law_A_in"], law_s=pm["law_sA_in"], law_A_lo=min(r["law_A_in"] for r in rows.values()), law_A_hi=max(r["law_A_in"] for r in rows.values()), p=pm["p"], p_L=pm["p_L"])
    W_(f"bands <= 300 kpc [{foot}] {tk()}")
R4["bands_300"] = B300
# catalogue noise: two halves of I_c on Delta_c
NOISE = {}
_d0 = {k_: v_ for k_, v_ in DV.items()}
for s in ("S10", "S_strict", "S_x300"):
    dl, djl = ratio(LSUM[s]["sg"], LSUM[s]["sw"], fdat); da, dja = ratio(*hsum("I_" + s, half=0), fdat); db, djb = ratio(*hsum("I_" + s, half=1), fdat); d, dj, var = dvec(s, "D"); bk = blocks_J(d, dj, var, RALL); mm, _ = mstack(s, perlens("N", "canonical", 1, "R2", 0.28)); ml, _ = mstack(s, perlens("L", "canonical", 1, "R2", 0.28)); X = lambda v: chi2b(bk, v - mm) - chi2b(bk, v - ml); dp = np.array([X(djl[p] - dja[p]) - X(djl[p] - djb[p]) for p in range(NP_)]); NOISE[s] = dict(half_A=X(dl - da), half_B=X(dl - db), sig=0.5 * float(math.sqrt(JKF * np.sum((dp - dp.mean()) ** 2))))
R4["catalogue_noise_N_R2"] = NOISE; W_(f"catalogue noise {NOISE}")
# ============================================================ G3: GH1's matched hosts
E1 = np.load(os.path.join(EXTD, "gh1_work", "gh1_esd.npz")); RB1 = np.geomspace(30, 3000, 13); RC1 = np.sqrt(RB1[1:] * RB1[:-1]); hb, lmH, zH1, pg, pr = E1["hbin"], E1["lm"], E1["z"], E1["pg"], E1["pr"]; NP1 = 30
def esd1(sl, sr, q="WG"): return np.array([E1[q][sl & (hb == b)].sum(0) / E1["WW"][sl & (hb == b)].sum(0) - E1["r" + q][sr].sum(0) / E1["rWW"][sr].sum(0) for b in range(4)])
DS1 = esd1(np.ones(len(hb), bool), np.ones(len(pr), bool)); JK1 = np.array([esd1(pg != p, pr != p) for p in range(NP1)]); GR1 = (RC1 >= 50) & (RC1 <= 300); FARG = RC1 >= 1100; v1 = JK1[:, :, GR1].reshape(NP1, -1); C1 = (NP1 - 1) / NP1 * (v1 - v1.mean(0)).T @ (v1 - v1.mean(0)); n1 = v1.shape[1]; Ci1 = np.linalg.inv(C1) * (NP1 - n1 - 2) / (NP1 - 1); d1 = DS1[:, GR1].ravel(); err1 = np.sqrt(np.diag(C1)).reshape(4, -1)
GH1J = json.load(open(os.path.join(REB0, "GH1_matched_lensing_satellites", "gh1_results.json"))); K_("K6b_GH1_stack", float(np.max(np.abs(DS1[:, GR1] - np.array(GH1J["DS"])[:, GR1]))) < 1e-12, "stacks equal GH1's")
# template on G09: GAMA tracers, uniform randoms over the box
ra_t, de_t, z_t = gg["RA"].values, gg["Dec"].values, gg["Z"].values; b09 = (ra_t > 129) & (ra_t < 141) & (de_t > -2) & (de_t < 3) & (z_t > 0.02) & (z_t < 0.6); TRg = cKDTree(np.c_[ra_t[b09] * np.cos(np.radians(0.5)), de_t[b09]]); ztg = z_t[b09]
raH1, deH1 = G75["ra"][G75["H"]], G75["dec"][G75["H"]]; rngg = np.random.default_rng(20261031 + 9); REG = RB1 / 1e3; RCg = RC1 / 1e3; ARg = math.pi * (REG[1:] ** 2 - REG[:-1] ** 2); Cg = np.zeros((2, 4, 12)); Wg = np.zeros((2, 4))
for kind in (0, 1):
    nr = 10 if kind else 1
    for rep_ in range(nr):
        rr = raH1 if kind == 0 else rngg.uniform(129, 141, len(raH1)); dd = deH1 if kind == 0 else rngg.uniform(-2, 3, len(raH1)); pts = np.c_[rr * math.cos(math.radians(0.5)), dd]; thd = np.degrees(3.0 / DAn(zH1))
        for i in range(len(rr)):
            js = np.array(TRg.query_ball_point(pts[i], thd[i]), int)
            if js.size == 0: continue
            js = js[np.abs(ztg[js] - zH1[i]) / (1 + zH1[i]) * 299792.458 <= 2000]
            if js.size == 0: continue
            R_ = np.radians(np.hypot(*(TRg.data[js] - pts[i]).T)) * DAn(zH1[i]); kk = np.searchsorted(REG, R_, "right") - 1; ok = (kk >= 0) & (kk < 12) & (R_ > 1e-5); np.add.at(Cg[kind, hb[i]], kk[ok], 1.0)
        np.add.at(Wg[kind], hb, 1.0)
Eg = (Cg[0] / Wg[0][:, None] - Cg[1] / Wg[1][:, None]) / ARg; Eg = np.where(RCg < 0.15, 0, Eg); Tg = np.where(RCg < 0.15, 0, np.cumsum(Eg * ARg, 1) / np.cumsum(ARg) - Eg); vf = (NP1 - 1) / NP1 * np.sum((JK1 - JK1.mean(0)) ** 2, 0); ag = float(np.sum((DS1 * Tg / vf)[:, FARG]) / np.sum((Tg * Tg / vf)[:, FARG])); neg = np.abs(ag * Tg[:, GR1]).mean(1) / (err1.mean(1) / math.sqrt(GR1.sum())); R4["G3_template"] = dict(a=ag, neg_sigma=neg.tolist(), negligible=bool(np.all(neg < 0.5))); W_(f"G3 template: a {ag:.3g}, |a T| in 50-300 kpc / sigma of stacked mean per bin {np.round(neg, 2).tolist()}: {'negligible' if np.all(neg < 0.5) else 'NOT negligible'}")
def g3model(tab):
    return np.array([np.array([np.interp(np.log(RC1 / 1e3), LRT, np.array([np.interp(l_, LMG, tab[:, j]) for j in range(NRT)])) for l_ in lmH[hb == b]]).T @ np.ones((hb == b).sum()) / 1 for b in range(4)], dtype=object) if False else None
def stackG(tab):
    o = np.zeros((4, 12))
    for j in range(12):
        col = np.array([np.interp(np.log(RC1[j] / 1e3), LRT, tab[i]) for i in range(tab.shape[0])]); v = np.interp(lmH, LMG, col)
        for b in range(4): m = hb == b; o[b, j] = np.sum(v[m] * E1["WW"][m, j]) / E1["WW"][m, j].sum()
    return o
G3 = {}
for foot in FOOTS:
    G3[foot] = {}
    for f in (0.28, 0.12, 0.49, 0.0):
        for nm, k in (("E", 1), ("E", 3), ("N", 1), ("Z", 1), ("L", 1)):
            m = stackG(blend(tab_of(nm, foot, k), f)); mb = stackG(blend(tab_of("B", foot, k), f)); r = d1 - m[:, GR1].ravel(); c = float(r @ Ci1 @ r); h = (m - mb)[:, GR1].ravel(); y = d1 - mb[:, GR1].ravel(); o = dict(chi2=c, n=n1, p=float(stats.chi2.sf(c, n1)))
            if nm != "L":
                t = float(h @ Ci1 @ h); Ah = float(h @ Ci1 @ y) / t; o.update(A_h=Ah, sA_h=1 / math.sqrt(t), lg_A_h=math.log10(Ah) if Ah > 0 else None, chi2_at_A=float((y - Ah * h) @ Ci1 @ (y - Ah * h)))
            G3[foot][f"{nm}{k}|f{f}"] = o
    W_(f"G3 [{foot}], f 0.28: " + "; ".join(f"{a}: chi2 {G3[foot][a + '|f0.28']['chi2']:.1f}" + (f", A_h {G3[foot][a + '|f0.28']['A_h']:.2f}+-{G3[foot][a + '|f0.28']['sA_h']:.2f}" if a != "L1" else "") for a in ("E1", "E3", "N1", "Z1", "L1")) + f" {tk()}")
R4["G3"] = G3
# K8
_me = open(os.path.abspath(sys.argv[0])).read(); K_("K8_no_outside_inputs", ("5." + "364") not in _me and "/Us" + "ers/" not in _me, "grep of this script")
if RF4_MUT:
    cE = G2["canonical"]["E1|R2|S10"]["no_T"]["chi2"]; R4["mutate_chi2_E1_S10"] = cE; W_(f"MUTATE: chi2 E1 R2 S10 {cE:.1f}; separability {SEP}; TS1 {TSS['canonical']['TS1']}, TS5 {TSS['canonical']['TS5']}")
    KP = not SEP["canonical"]
else:
    KP = all(RF4_K.values())
R4["checks_pass"] = KP; R4["elapsed_s"] = time.time() - T00
json.dump(R4, open(os.path.join(RF4, f"rf4_results{RF4_TAG}.json"), "w"), indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else (float(o) if isinstance(o, (np.floating,)) else str(o))); open(os.path.join(RF4, f"rf4_grade{RF4_TAG}.out"), "w").write("\n".join(RF4_OUT) + "\n")
W_(f"\nchecks {'PASS' if KP else 'FAIL'} {tk()}"); sys.exit(0 if (KP if not RF4_MUT else not KP) is False else (0 if KP or RF4_MUT else 1)) if False else None
if RF4_MUT: sys.exit(1 if not SEP["canonical"] else 0)
sys.exit(0 if KP else 1)
