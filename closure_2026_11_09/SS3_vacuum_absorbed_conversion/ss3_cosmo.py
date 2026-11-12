#!/usr/bin/env python3
"""SS3 (FROZEN_CRITERIA.md 3a8a5a9fce): variant J's cosmology on SS1 A's machinery (ss1_cosmo.py prefix, read-only): the
converted matter becomes w = -1 vacuum (MJ1: radiation), h re-solved to hold theta_s; gate 6 (BAO + SN), N1 (rho_DE(z) against
CFG689's BAO + SN posterior nodes), N2 (a0 drift), growth (A's scale-free two-fluid ODE on J's background, fine-grid
fsigma8), 7(b) reading, forest.
    SS1_FOOT=<f> [SS3_MMIN=2e11] [SS3_W=1/3 for MJ1] [SS3_V=MJ2] python3 ss3_cosmo.py   -> parts/vcosmo_<V>_<f>.json
kappa = 1/2 FITTED; not theory closed; footings never pooled; adopts nothing."""
import os, sys, json, math, io, contextlib
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
SS1 = os.path.join(REPO, "closure_2026_11_09", "SS1_self_shielded_conversion"); sys.path.insert(0, SS1); sys.path.insert(0, HERE)
sys.dont_write_bytecode = True
import numpy as np
from scipy.special import erfc
FOOT = os.environ.get("SS1_FOOT", "canonical"); MMIN = float(os.environ.get("SS3_MMIN", "1e6")); WPROD = float(os.environ.get("SS3_W", "-1")); V = os.environ.get("SS3_V", "J")
TAG = V + ("_rad" if WPROD > -1 else "") + ("_mmin2e11" if MMIN > 1e6 else "")
_a = sys.argv; sys.argv = ["ss3.py", "none", V]
with contextlib.redirect_stdout(io.StringIO()):
    import ss3 as S3
sys.argv = _a
SV, C = S3.SV, S3.C
src = open(os.path.join(SS1, "ss1_cosmo.py")).read(); cut = src.index("# ================================================================== run")
ns = {"__file__": os.path.join(SS1, "ss1_cosmo.py"), "__name__": "ss1c_ss3"}; a_ = sys.argv; sys.argv = ["ss1_cosmo.py"]
with contextlib.redirect_stdout(io.StringIO()): exec(compile(src[:cut], "ss1c", "exec"), ns)
sys.argv = a_
p = S3.vparJ(V, FOOT); F = p["F"]; C.Z_DEC = p["z_dec"]; C.TAU_TOT = p["alpha"]             # J's onset and budget for A's background()
M = ns["M"]; OD, OB, H_REF = ns["OD"], ns["OB"], ns["H_REF"]; REFBG = ns["REFBG"]; ZSTAR = ns["ZSTAR"]; RD = ns["RD"]
def P(s): print(s, flush=True)
# ---------------- Press-Schechter nodes at J's z_dec and the cosmic converted fraction
kk = ns["kk"]; Pk = np.array([M.pk_lin(k, p["z_dec"]) for k in kk]); RHO_M0 = ns["RHO_M0"]
def sig(Mm):
    R = (3 * Mm / (4 * math.pi * RHO_M0)) ** (1 / 3); x = kk * R; W = 3 * (np.sin(x) - x * np.cos(x)) / x ** 3; return math.sqrt(np.trapz(Pk * W * W * kk ** 3 / (2 * math.pi ** 2), np.log(kk)))
MED = np.logspace(6, 16, 41); MN = np.sqrt(MED[:-1] * MED[1:]); Fc = erfc(1.686 / (math.sqrt(2) * np.array([sig(m) for m in MED]))); dF = np.where(MN >= MMIN, Fc[:-1] - Fc[1:], 0.0)
TAUS = np.linspace(0, p["alpha"], 61); FB = []
for m in MN:
    Mb = m / (1 + C.F_CAP * F["R"]); H = C.halo(Mb, F["R"], F["h"], F["Om"], M200=m, Mchi=m * C.F_CAP * F["R"] / (1 + C.F_CAP * F["R"]), z=p["z_dec"]); H["M500"] = float(H["Menc"](H["R500"])) / H["fchi"]
    FB.append([float(np.sum(S3.h_profileJ(p, H, t)[1] * S3.h_profileJ(p, H, t)[2]) / np.sum(S3.h_profileJ(p, H, t)[1])) for t in TAUS])
FB = np.array(FB); CONV = (dF[:, None] * (1 - FB)).sum(0)                                 # converted fraction of the component vs tau
Sfun = lambda tau: 1 - np.interp(tau, TAUS, CONV)
# ---------------- background (theta_s held), gate 6, N1, N2
h_J = ns["h_hold"](Sfun, WPROD); BG = ns["background"](h_J, Sfun, WPROD); bs = ns["bao_sn"](BG); bs0 = ns["bao_sn"](REFBG)
KAJ3_h = ns["h_hold"](lambda tau: np.ones_like(tau), WPROD)
z = BG["z"]; omDE = BG["om_L"] + BG["om_p"] * (WPROD == -1) + 0.0
omDE_ref = float(REFBG["om_L"])
CF = json.load(open(os.path.join(REPO, "campaign_fresh_gravity", "CFG689_native_ruler_bao", "cfg689.json")))["BAO+SN"]
NODES = [0, 0.4, 0.7, 1.0, 1.5, 2.33]; mean = np.array(CF["posterior"]["node_mean"]); std = np.array(CF["posterior"]["node_std"])
J_nodes = np.array([float(np.interp(zz, z, omDE)) for zz in NODES]) if WPROD == -1 else np.full(len(NODES), float(BG["om_L"]))
chiJ = float(np.sum(((J_nodes - mean) / std) ** 2)); c_best = float(np.sum(mean / std ** 2) / np.sum(1 / std ** 2)); chiC = float(np.sum(((c_best - mean) / std) ** 2))
n1_within = bool(np.all(np.abs(J_nodes - mean) <= 2 * std)); n1 = bool(n1_within and chiJ - chiC <= 4)
rise = float(np.interp(0.0, z, omDE) / np.interp(p["z_dec"], z, omDE) - 1) if WPROD == -1 else 0.0
# ---------------- growth on J's background (A's scale-free two-fluid ODE, fine-grid epochs for fsigma8)
ZG = ns["ZG"]; ZF = np.linspace(0.0, 1.2, 241)
def growth(bg):
    lna_t = np.log(1 / (1 + bg["z"])); o = np.argsort(lna_t); lna_t = lna_t[o]; lnH = np.log(bg["H"][o]); dlnH = np.gradient(lnH, lna_t); Sg = bg["S"][o]
    ai = 1 / 3401.0; adec = 1 / 1091.0; EP = np.concatenate([ZG, ZF]); grid = np.unique(np.concatenate([np.linspace(math.log(ai), 0.0, 8001), np.log(1 / (1 + EP))])); tset = set(float(x) for x in np.log(1 / (1 + EP)))
    y = np.array([ai, ai, 0.0, 0.0]); rec = {}; I4 = np.eye(4)
    for n in range(len(grid) - 1):
        h_ = grid[n + 1] - grid[n]; lm = 0.5 * (grid[n] + grid[n + 1]); a = math.exp(lm); E2 = math.exp(2 * np.interp(lm, lna_t, lnH)) / 100.0 ** 2
        S_ = float(np.interp(lm, lna_t, Sg)); Od = OD * a ** -3 * S_ / E2; Ob = OB * a ** -3 / E2; dl = float(np.interp(lm, lna_t, dlnH))
        A = np.zeros((4, 4)); A[0, 1] = 1; A[1, 0] = 1.5 * Od; A[1, 1] = -(2 + dl)
        if a > adec: A[1, 2] = 1.5 * Ob; A[2, 3] = 1; A[3, 0] = 1.5 * Od; A[3, 2] = 1.5 * Ob; A[3, 3] = -(2 + dl)
        y = np.linalg.solve(I4 - 0.5 * h_ * A, (I4 + 0.5 * h_ * A) @ y)
        if float(grid[n + 1]) in tset: rec[float(grid[n + 1])] = y.copy()
    keys = [float(x) for x in np.log(1 / (1 + EP))]
    Sz = np.interp(EP, bg["z"], bg["S"]); db = np.array([rec[k_][2] for k_ in keys]); dc = np.array([rec[k_][0] for k_ in keys])
    srcv = OB * db + OD * Sz * dc; dm = srcv / (OB + OD * Sz); n = len(ZG); return srcv[:n], dm[:n], dm[n:]
src_J, dm_J, dmF_J = growth(BG); src_R, dm_R, dmF_R = growth(REFBG)
s8_ref = float(M.sigma8()); s8_ratio = float(dmF_J[0] / dmF_R[0]); h2 = h_J ** 2; Om_J = (OB + OD * float(BG["S"][0])) / h2
lnaF = np.log(1 / (1 + ZF)); rrF = np.gradient(dmF_J, lnaF) / np.gradient(dmF_R, lnaF); rows = []
for (tb, zb, r1, p1, m1, r2, p2, m2) in ns["DESI"]:
    e1, e2 = 0.5 * (p1 + m1), 0.5 * (p2 + m2); x = float(np.interp(zb, ZF, rrF)); rows.append(dict(bin=tb, z=zb, Rf=x, in_sf=bool(abs(x - r1) <= 2 * e1), in_sfb=bool(abs(x - r2) <= 2 * e2), s8dir=bool(x <= 1.001)))
fs_pass = all(r["in_sf"] and r["in_sfb"] and r["s8dir"] for r in rows)
Rz = src_J / src_R; Rkz = np.tile(Rz, (len(ns["KG"]), 1)); Sx = ns["limber4_bg"](BG, Rkz); cl, Al = ns["Q3"]["best_amp_chi2"](ns["X0"] * Sx)
FD = ns["forest_setup"](); fr = ns["forest_eval"](FD, BG, Rkz)
out = dict(variant=V, footing=FOOT, M_min=MMIN, w_product=WPROD, criteria=S3.CRIT, z_dec=p["z_dec"], alpha=p["alpha"], v_stiff=p["v_stiff"],
           F_conv_today=float(CONV[-1]), lambda_today_Mpc=0.0, h=h_J, h_ref=H_REF, KA_J3_h_no_conversion=KAJ3_h,
           G6=dict(status="PASS" if bs["tot"] - bs0["tot"] <= 4 else "FAIL", dchi2=bs["tot"] - bs0["tot"], dchi2_bao=bs["bao"] - bs0["bao"], dchi2_sn=bs["sn"] - bs0["sn"],
                   DM_over_rd_051=float(np.interp(0.51, BG["z"], BG["DM"]) / RD), DM_over_rd_051_ref=float(np.interp(0.51, REFBG["z"], REFBG["DM"]) / RD), Omega_DE0=float(omDE[0] / h2), Omega_DE0_ref=omDE_ref / H_REF ** 2),
           N1=dict(status="PASS" if n1 else "FAIL", J_nodes=J_nodes, cfg689_mean=mean, cfg689_std=std, pulls=(J_nodes - mean) / std, chi2_J=chiJ, chi2_const_best=chiC, best_const=c_best, within_2sigma=n1_within, rho_DE_rise_zdec_to_0=rise),
           N2=dict(status="NOT EVALUABLE", a0_drift_since_zdec=math.sqrt(1 + rise) - 1, a0_today_shift_vs_footing=math.sqrt(float(omDE[0]) / omDE_ref) - 1,
                   note="AT2's on-disk high-z a0 cells are BLOCKED and CFG689's native a0(z) bands are 0.3-0.6 dex wide at z >= 1: a 3-4 % drift is not testable; kappa is fitted, so a0 today is calibrated by SPARC, not predicted"),
           sigma8=s8_ref * s8_ratio, sigma8_ref=s8_ref, sigma8_ratio_z0=s8_ratio, S8=s8_ref * s8_ratio * math.sqrt(Om_J / 0.3), Omega_m0=Om_J,
           fs8=dict(rows=rows, pass_=bool(fs_pass)), forest=fr, G8=dict(status="PASS" if (fs_pass and fr["status"] == "PASS") else "FAIL"),
           lensing_reading=dict(chi2=float(cl), status="NO VERDICT (no validated method; A / SS2 rule)"))
def clean(o):
    if isinstance(o, dict): return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [clean(v) for v in o]
    if isinstance(o, np.ndarray): return clean(o.tolist())
    if isinstance(o, (np.floating, np.integer)): return o.item()
    if isinstance(o, np.bool_): return bool(o)
    return o
json.dump(clean(out), open(os.path.join(HERE, "parts", f"vcosmo_{TAG}_{FOOT}.json"), "w"), indent=1)
P(f"[{FOOT}] {TAG}: converted {CONV[-1]:.3f} of the component; h {H_REF:.4f} -> {h_J:.4f} (KA-J3 no-conversion h {KAJ3_h:.6f}); Omega_DE0 {omDE[0]/h2:.4f} (ref {omDE_ref/H_REF**2:.4f}); rho_DE rise since z_dec {rise:+.2%}; "
  f"G6 Delta chi2 {bs['tot']-bs0['tot']:+.2f} -> {out['G6']['status']}; D_M/r_d(0.51) {out['G6']['DM_over_rd_051']:.3f}; N1 pulls " + " ".join(f"{pp:+.2f}" for pp in out['N1']['pulls']) + f", chi2 {chiJ:.2f} vs const {chiC:.2f} -> {out['N1']['status']}; "
  f"a0 drift {out['N2']['a0_drift_since_zdec']:+.2%}; sigma8 {out['sigma8']:.3f} S8 {out['S8']:.3f}; Rf " + " ".join(f"{r['bin']} {r['Rf']:.3f}" for r in rows) + f" -> {out['G8']['status']}; lensing reading {cl:.2f}; forest {fr['dchi2']:.3f}")
