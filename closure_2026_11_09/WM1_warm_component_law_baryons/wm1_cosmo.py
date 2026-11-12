#!/usr/bin/env python3
"""WM1 cosmology (FROZEN_CRITERIA.md 6e40130dfa): the warm relic in CLASS, SS5's D1 two-fluid growth with the baryons on the law,
gates 6 (BAO+SN), 7b-L (CMB lensing with the law on the web), 8 (forest + fsigma8), CS (S8 line, P(k) ratios), KA-W2 (SS5 D1
reproduced), KA-W3 (CLASS omega and half-mode), MN0 / MN-W (baryons Newtonian).
    WM1_V=<W|W3|Wthird|MW1|MW2> SS1_FOOT=<canonical|alt> python3 wm1_cosmo.py   -> parts/cosmo_<V>_<footing>.json
Read-only: ss1_cosmo.py's prefix (CLASS cold reference, BAO+SN, limber4_bg, forest, DESI fsigma8 rows), SS5's ss5.py prefix (D1, KA
only), QX3 iter2 (PR4 lensing statistic), QX15 / F1A footings. CLASS RSS disclosed. kappa = 1/2 FITTED; not theory closed; adopts nothing."""
import os, sys, json, math, time, io, contextlib, resource
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[v] = "1"
sys.dont_write_bytecode = True
import warnings; warnings.filterwarnings("ignore")
import numpy as np
from scipy.optimize import brentq
T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
SS1 = os.path.join(REPO, "closure_2026_11_09", "SS1_self_shielded_conversion"); SS5 = os.path.join(REPO, "closure_2026_11_09", "SS5_baryon_component_segregation")
PARTS = os.path.join(HERE, "parts"); os.makedirs(PARTS, exist_ok=True)
CRIT = "6e40130dfa"; V = os.environ.get("WM1_V", "W"); FOOT = os.environ.get("SS1_FOOT", "canonical")
def P(s=""): print(s, flush=True)
def rss(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9
def clean(o):
    if isinstance(o, dict): return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [clean(v) for v in o]
    if isinstance(o, (np.floating, np.integer)): return o.item()
    if isinstance(o, np.bool_): return bool(o)
    if isinstance(o, np.ndarray): return clean(o.tolist())
    if isinstance(o, float) and not math.isfinite(o): return str(o)
    return o
# ---------------------------------------------------------------- ss1_cosmo prefix (read-only, own namespace)
sys.path.insert(0, SS1); src = open(os.path.join(SS1, "ss1_cosmo.py")).read(); cut = src.index("# ================================================================== run")
ns = {"__file__": os.path.join(SS1, "ss1_cosmo.py"), "__name__": "ss1c_wm1"}; _a = sys.argv; sys.argv = ["ss1_cosmo.py"]
with contextlib.redirect_stdout(io.StringIO()): exec(compile(src[:cut], "ss1c", "exec"), ns)
sys.argv = _a
M, KG, ZG, PREF, REFBG, Q3, X0, c0 = ns["M"], ns["KG"], ns["ZG"], ns["PREF"], ns["REFBG"], ns["Q3"], ns["X0"], ns["c0"]
BASE, OB, OD, H_REF, Class, CHI2_LINE = ns["BASE"], ns["OB"], ns["OD"], ns["H_REF"], ns["Class"], ns["CHI2_LINE"]
limber4_bg, forest_setup, forest_eval, bao_sn, DESI, ZSTAR, RD = ns["limber4_bg"], ns["forest_setup"], ns["forest_eval"], ns["bao_sn"], ns["DESI"], ns["ZSTAR"], ns["RD"]
CLIGHT = 299792.458
Q15 = ns["Q15"]; th = Q15["footings"][FOOT]["main"]["theta"]; AS_FIT = math.exp(th["lnAs1e10"]) / 1e10; AS_RATIO = AS_FIT / BASE["A_s"]
A0 = {"canonical": 9.360324825027975e-11, "alt": 1.1312035414413022e-10}[FOOT]
RES = dict(criteria=CRIT, variant=V, footing=FOOT, note="TEST lane, quarantined; adopts nothing; kappa = 1/2 FITTED; not theory closed")
P(f"[{FOOT}] {V}: reference loaded (h {H_REF:.5f}, omega_b {OB:.6f}, omega_chi {OD:.6f}, R {OD/OB:.4f}); lensing baseline {c0:.4f}  [{time.time()-T0:.0f}s {rss():.2f}GB]")

# ---------------------------------------------------------------- the relic (frozen rule)
MHM0 = (0.050 ** (-1 / 1.16) - 1) * 4.060e11
MHM = {"W": MHM0, "W3": 3 * MHM0, "Wthird": MHM0 / 3, "MW1": 10 * MHM0, "MW2": MHM0 / 10}[V]
h = H_REF; OmC = OD / h ** 2; Om = (OB + OD) / h ** 2; RHOM = Om * 2.77536627e11 * h ** 2; NUV = 1.12
def viel(mk):
    al = 0.049 * mk ** -1.11 * (OmC / 0.25) ** 0.11 * (h / 0.7) ** 1.22 / h; lam = 2 * math.pi * al * (2 ** (NUV / 5) - 1) ** (-1 / (2 * NUV)); return 4 * math.pi / 3 * RHOM * (lam / 2) ** 3, lam, al
M_KEV = brentq(lambda x: math.log(viel(x)[0] / MHM), 1e-3, 100.0, xtol=1e-12); M_EV = 1000 * M_KEV; TNCDM = 0.71611 * (OD * 93.14 / M_EV) ** (1 / 3)
_, LAM_HM, ALPHA = viel(M_KEV); KHM_FIT = 2 * math.pi / LAM_HM
RES["relic"] = dict(M_hm=MHM, m_eV=M_EV, T_ncdm=TNCDM, lambda_hm_Mpc=LAM_HM, k_hm_fit_hMpc=KHM_FIT / h, alpha_Viel_Mpc=ALPHA, omega_target=OD)
P(f"[{FOOT}] {V}: M_hm {MHM:.4g} -> m {M_EV:.2f} eV, T_ncdm {TNCDM:.4f}, k_hm (Viel) {KHM_FIT/h:.3f} h/Mpc")
WP = dict(BASE, omega_cdm=1e-7, N_ncdm=1, m_ncdm=M_EV, T_ncdm=TNCDM, deg_ncdm=1.0, tol_ncdm_bg=1e-10)
t1 = time.time(); Mw = Class(); Mw.set(WP); Mw.compute(); t_class = time.time() - t1
onc = float(Mw.Omega_nu) * h * h
derw = Mw.get_current_derived_parameters(['z_star', 'rs_d', '100*theta_s', 'rs_star']); derc = M.get_current_derived_parameters(['z_star', 'rs_d', '100*theta_s', 'rs_star'])
PW = np.array([[Mw.pk_lin(k, z) for z in ZG] for k in KG]); T2 = PW / PREF
kz0 = np.logspace(-2, 1.5, 400); r0 = np.array([Mw.pk_lin(k, 0.0) / M.pk_lin(k, 0.0) for k in kz0]); j = np.where(r0 < 0.25)[0]
KHM_CLASS = float(np.interp(0.25, r0[::-1], kz0[::-1])) if len(j) else float("nan")
RES["KA_W3"] = dict(omega_ncdm_CLASS=onc, omega_target=OD, omega_pass=bool(abs(onc / OD - 1) <= 0.01), k_hm_CLASS_hMpc=KHM_CLASS / h, k_hm_Viel_hMpc=KHM_FIT / h,
                    k_hm_ratio=KHM_CLASS / KHM_FIT, disclose_25pct=bool(abs(KHM_CLASS / KHM_FIT - 1) > 0.25), class_seconds=t_class,
                    Pk_ratio_z0={f"{k} h/Mpc": float(Mw.pk_lin(k * h, 0.0) / M.pk_lin(k * h, 0.0)) for k in (0.1, 0.3, 1.0, 3.0, 10.0)})
P(f"[{FOOT}] KA-W3: CLASS omega_ncdm {onc:.5f} vs {OD:.5f} -> {'PASS' if RES['KA_W3']['omega_pass'] else 'FAIL'}; half-mode k (P ratio 1/4) CLASS {KHM_CLASS/h:.3f} vs Viel {KHM_FIT/h:.3f} h/Mpc (ratio {KHM_CLASS/KHM_FIT:.3f}); P_w/P_c z0 "
  + " ".join(f"{k}:{v:.3f}" for k, v in RES["KA_W3"]["Pk_ratio_z0"].items()) + f"; CLASS {t_class:.0f} s  [{time.time()-T0:.0f}s {rss():.2f}GB]")

# ---------------------------------------------------------------- D1: two-fluid growth with nu(k, z) (SS5's equations, vectorised)
H0 = 100 * h * 1e3 / 3.0857e22; Orad = 2.469e-5 * (1 + 0.2271 * 3.046) / h ** 2; OL = 1 - Om - Orad
def Hs(a): return H0 * math.sqrt(Om / a ** 3 + Orad / a ** 4 + OL)
ZT = np.concatenate([np.linspace(0, 3, 61), np.linspace(3.1, 20, 85)])
def ptab(pk):
    return np.log(np.array([[max(pk(k, z), 1e-300) for z in ZT] for k in KG]))
def make_nu(LP, amp=AS_RATIO, kvec=KG):
    def nu_at(z):
        zz = min(z, 20.0); j = np.searchsorted(ZT, zz); j = min(max(j, 1), len(ZT) - 1); w = (zz - ZT[j - 1]) / (ZT[j] - ZT[j - 1])
        Pk = np.exp((1 - w) * LP[:, j - 1] + w * LP[:, j]) * amp * (((1 + 20.0) / (1 + z)) ** 2 if z > 20 else 1.0)
        drms = np.sqrt(kvec ** 3 * Pk / (2 * math.pi ** 2)); a = 1 / (1 + z); y = 1.5 * H0 ** 2 * Om * drms / (a * a * (kvec / 3.0857e22)) / A0
        y = np.maximum(y, 1e-30); return 0.5 + np.sqrt(0.25 + 1.0 / y)
    return nu_at
ZF = np.linspace(0.0, 1.2, 241)
def d1(nu_at, nk, rec_z, newton=False, nstep=8001):
    ai = 1 / 1091.0; grid = np.unique(np.concatenate([np.linspace(math.log(ai), 0.0, nstep), np.log(1 / (1 + np.asarray(rec_z)))]))
    want = {}
    for i, x in enumerate(np.log(1 / (1 + np.asarray(rec_z)))): want.setdefault(float(x), []).append(i)      # duplicates (ZG and ZF share epochs) all filled
    y = np.zeros((nk, 4)); y[:, 0] = ai; y[:, 1] = ai; out = np.zeros((len(rec_z), nk, 4)); I4 = np.eye(4)[None]
    for n in range(len(grid) - 1):
        hh = grid[n + 1] - grid[n]; lm = 0.5 * (grid[n] + grid[n + 1]); a = math.exp(lm); z = 1 / a - 1; Ha = Hs(a)
        dl = (-1.5 * Om / a ** 3 - 2 * Orad / a ** 4) * H0 ** 2 / Ha ** 2; Oc = OD / h ** 2 / a ** 3 * H0 ** 2 / Ha ** 2; Obb = OB / h ** 2 / a ** 3 * H0 ** 2 / Ha ** 2
        nu = np.ones(nk) if newton else nu_at(z)
        A = np.zeros((nk, 4, 4)); A[:, 0, 1] = 1; A[:, 1, 0] = 1.5 * Oc; A[:, 1, 2] = 1.5 * Obb; A[:, 1, 1] = -(2 + dl)
        A[:, 2, 3] = 1; A[:, 3, 0] = 1.5 * Oc * nu; A[:, 3, 2] = 1.5 * Obb * nu; A[:, 3, 3] = -(2 + dl)
        y = np.linalg.solve(I4 - 0.5 * hh * A, ((I4 + 0.5 * hh * A) @ y[:, :, None]))[:, :, 0]
        g1 = float(grid[n + 1])
        for i_ in want.get(g1, ()): out[i_] = y
    assert np.all(np.isfinite(out)) and np.all(out[..., 0] != 0), 'D1: unfilled or non-finite record'
    return out                                                            # [z, k, (dchi, dchi', db, db')]
def dm_of(o): return (OD * o[..., 0] + OB * o[..., 2]) / (OD + OB)
# KA-W2 (main W only): SS5's own D1 (executed read-only) vs this solver with SS5's settings (cold CLASS at the fitted A_s)
if V == "W":
    s5 = open(os.path.join(SS5, "ss5.py")).read(); c5 = s5.index("# ================================================================ background clock for D2")
    n5 = {"__file__": os.path.join(SS5, "ss5.py"), "__name__": "ss5_wm1"}; os.environ["SS1_FOOT"] = FOOT
    with contextlib.redirect_stdout(io.StringIO()): exec(compile(s5[:c5], "ss5", "exec"), n5)
    kv = np.array([0.1, 0.3, 1.0, 3.0]) * h; LP5 = np.log(np.array([[n5["M"].pk_lin(k, z) for z in ZT] for k in kv]))
    o5 = d1(make_nu(LP5, amp=1.0, kvec=kv), len(kv), [3.0, 1.2, 0.0]); rows = []; worst = 0.0
    for i, kh in enumerate((0.1, 0.3, 1.0, 3.0)):
        for jz, z in enumerate((3.0, 1.2, 0.0)):
            mine = o5[jz, i, 2] / o5[jz, i, 0]; ref = n5["d1"][f"k {kh} h/Mpc"][f"z {z}"]["delta_b_over_delta_chi"]; worst = max(worst, abs(mine / ref - 1))
            rows.append(dict(k=kh, z=z, mine=float(mine), ss5=float(ref)))
    n5["M"].struct_cleanup(); n5["M"].empty()
    RES["KA_W2"] = dict(rows=rows, max_rel_dev=worst, pass_=bool(worst <= 0.01))
    P(f"[{FOOT}] KA-W2 (SS5 D1 reproduced): max rel dev {worst:.2e} -> {'PASS' if worst <= 0.01 else 'FAIL'}; z0 b/chi " + " ".join(f"{r['k']}:{r['mine']:.3g}({r['ss5']:.3g})" for r in rows if r['z'] == 0.0) + f"  [{time.time()-T0:.0f}s]")
LPR = ptab(M.pk_lin); nuW = make_nu(LPR)                              # A1 (5cba17a249): graded nu from the cold reference power (SS5's convention)
KB = np.array([0.01, 0.03, 0.1, 0.3, 1.0]) * h; ZB_ = [3.0, 1.2, 0.3, 0.02]                       # A1 bracket: the frozen warm-P nu, k <= 1 h/Mpc
LPWb = np.log(np.array([[max(Mw.pk_lin(k, z), 1e-300) for z in ZT] for k in KB])); nuWb = make_nu(LPWb, kvec=KB)
obL = d1(nuWb, len(KB), ZB_); obN = d1(nuWb, len(KB), ZB_, newton=True); BmB = dm_of(obL) / dm_of(obN)
RES["A1_bracket_warm_nu"] = {f"k {kb/h:g} h/Mpc": {f"z {z}": dict(B_m=float(BmB[j, i]), delta_b_over_delta_chi=float(obL[j, i, 2] / obL[j, i, 0]), nu=float(nuWb(z)[i])) for j, z in enumerate(ZB_)} for i, kb in enumerate(KB)}
P(f"[{FOOT}] A1 bracket (warm-P nu, reported): B_m z 0.02 " + " ".join(f"{k.split()[1]}:{v['z 0.02']['B_m']:.2f}" for k, v in RES["A1_bracket_warm_nu"].items()))
recz = np.concatenate([ZG, ZF]); oL = d1(nuW, len(KG), recz); oN = d1(nuW, len(KG), recz, newton=True)
Bm = dm_of(oL) / dm_of(oN); Bb = oL[..., 2] / dm_of(oN); BmG, BmF = Bm[:len(ZG)].T, Bm[len(ZG):].T; BbG = Bb[:len(ZG)].T     # [k, z]
PWF = np.array([[Mw.pk_lin(k, z) for z in ZF] for k in KG]); PrefF = np.array([[M.pk_lin(k, z) for z in ZF] for k in KG]); T2F = PWF / PrefF
RmG = np.sqrt(T2) * BmG; RmF = np.sqrt(T2F) * BmF; RbG = np.sqrt(T2) * BbG
def at(arr, k, z, zg=ZG): return float(np.exp(np.interp(math.log(k), np.log(KG), np.log([np.interp(z, zg, arr[i]) for i in range(len(KG))]))))
RES["D1"] = {f"k {kh} h/Mpc": {f"z {z}": dict(B_m=at(BmG, kh * h, z), delta_b_over_delta_chi=float(np.interp(math.log(kh * h), np.log(KG), [np.interp(z, ZG, (oL[:len(ZG), i, 2] / oL[:len(ZG), i, 0])) for i in range(len(KG))])),
                                              nu=float(np.interp(math.log(kh * h), np.log(KG), nuW(z)))) for z in (3.0, 1.2, 0.3, 0.02)} for kh in (0.01, 0.03, 0.1, 0.3, 1.0, 3.0)}
P(f"[{FOOT}] D1 (graded, A1: nu from the cold reference P): B_m at z 0.02: " + " ".join(f"{k.split()[1]}:{v['z 0.02']['B_m']:.2f}" for k, v in RES["D1"].items()) + "; delta_b/delta_chi z 0.02: " + " ".join(f"{k.split()[1]}:{v['z 0.02']['delta_b_over_delta_chi']:.2f}" for k, v in RES["D1"].items()) + f"  [{time.time()-T0:.0f}s {rss():.2f}GB]")

# ---------------------------------------------------------------- gate 6: BAO + SN (CLASS backgrounds, fixed h)
def class_bg(Mx):
    b = Mx.get_background(); z = b['z'][::-1]; Hh = b['H [1/Mpc]'][::-1] * CLIGHT; DM = b['comov. dist.'][::-1]; m = z <= 3600
    return dict(z=z[m], H=Hh[m], DM=DM[m])
bgc, bgw = class_bg(M), class_bg(Mw); bc = bao_sn(bgc, rd=derc['rs_d']); bw = bao_sn(bgw, rd=derw['rs_d']); d6 = bw["tot"] - bc["tot"]
RES["G6"] = dict(status="PASS" if d6 <= 4 else "FAIL", dchi2=d6, dchi2_bao=bw["bao"] - bc["bao"], dchi2_sn=bw["sn"] - bc["sn"], rd_warm=derw['rs_d'], rd_cold=derc['rs_d'],
                 theta_s100_warm=derw['100*theta_s'], theta_s100_cold=derc['100*theta_s'], z_star_warm=derw['z_star'], z_star_cold=derc['z_star'])
P(f"[{FOOT}] G6 BAO+SN: Delta chi2 {d6:+.4f} (BAO {RES['G6']['dchi2_bao']:+.4f}, SN {RES['G6']['dchi2_sn']:+.4f}); r_d {derw['rs_d']:.3f} vs {derc['rs_d']:.3f}; 100 theta_s {derw['100*theta_s']:.5f} vs {derc['100*theta_s']:.5f} -> {RES['G6']['status']}")

# ---------------------------------------------------------------- gate 7b-L: lensing with the law on the web (and the Newtonian warm reading)
Xw = Q3["X_of"](Mw); cN, AN = Q3["best_amp_chi2"](Xw)
SB = limber4_bg(REFBG, RmG) / limber4_bg(REFBG, np.sqrt(T2)); cL, AL = Q3["best_amp_chi2"](Xw * SB)
RES["G7bL"] = dict(status="PASS" if cL <= CHI2_LINE else "FAIL", chi2=float(cL), line=CHI2_LINE, A_refit_over_newton=float(AL / AN), S_B={f"L {L}": float(SB[L]) for L in (10, 40, 100, 200, 400) if L < len(SB)},
                   newton_warm_chi2_footing_point=float(cN), baseline_cold=float(c0))
P(f"[{FOOT}] G7b-L lensing, law on the web: chi2 {cL:.2f} (line {CHI2_LINE}); S_B " + " ".join(f"{k}:{v:.1f}" for k, v in RES['G7bL']['S_B'].items()) + f"; amplitude refit x {AL/AN:.4f}; Newtonian warm at the footing point {cN:.3f} (cold {c0:.3f}) -> {RES['G7bL']['status']}")

# ---------------------------------------------------------------- gate 8: forest + fsigma8; CS
FD = forest_setup(); frL = forest_eval(FD, REFBG, RmG); frB = forest_eval(FD, REFBG, RbG); frN = forest_eval(FD, REFBG, np.sqrt(T2)); fr0 = forest_eval(FD, REFBG, np.ones_like(T2))
hh = h; R8 = 8.0 / hh; lk = np.log(KG); W8 = lambda x: 3 * (np.sin(x) - x * np.cos(x)) / x ** 3; w2k3 = W8(KG * R8) ** 2 * KG ** 3 / (2 * np.pi ** 2)
s8F = lambda RR: np.sqrt(np.trapz(PrefF * RR ** 2 * w2k3[:, None], lk, axis=0)); s8G = lambda RR: np.sqrt(np.trapz(PREF * RR ** 2 * w2k3[:, None], lk, axis=0))
def fs8(RF):
    rrF = np.gradient(s8F(RF), ZF * 0 + np.log(1 / (1 + ZF))) / np.gradient(s8F(np.ones_like(RF)), np.log(1 / (1 + ZF))); rows = []
    for (tb, zb, r1, p1, m1, r2, p2, m2) in DESI:
        e1, e2 = 0.5 * (p1 + m1), 0.5 * (p2 + m2); x = float(np.interp(zb, ZF, rrF)); rows.append(dict(bin=tb, z=zb, Rf=x, in_sf=bool(abs(x - r1) <= 2 * e1), in_sfb=bool(abs(x - r2) <= 2 * e2), s8dir=bool(x <= 1.001)))
    return dict(rows=rows, pass_=bool(all(r["in_sf"] and r["in_sfb"] and r["s8dir"] for r in rows)))
FSL = fs8(RmF); FSN = fs8(np.sqrt(T2F))
RES["G8"] = dict(status="PASS" if (FSL["pass_"] and frL["status"] == "PASS") else "FAIL", forest=frL, fsigma8=FSL, forest_baryon_tracer_reported=frB,
                 newton_warm_reported=dict(forest=frN, fsigma8=FSN), KA_forest_R1=fr0)
s8_0 = float(M.sigma8()); Om0 = (OB + OD) / h ** 2
def cs(R):
    r = float(s8G(R)[0] / s8G(np.ones_like(R))[0]); S8 = s8_0 * r * math.sqrt(Om0 / 0.3); S8r = s8_0 * math.sqrt(Om0 / 0.3)
    pk = {f"k {k} h/Mpc z {z}": float(at(R, k * h, z) ** 2) for k in (0.3, 1.0, 3.0) for z in (0.3, 0.5)}
    return dict(sigma8_ratio=r, S8=S8, S8_ref=S8r, change=S8 / S8r - 1, P_ratio=pk, status="PASS" if abs(S8 / S8r - 1) <= 2 * 0.0225 / 0.759 else "FAIL")
RES["CS"] = cs(RmG); RES["CS"]["newton_warm_reported"] = cs(np.sqrt(T2)); RES["CS"]["line_frac"] = 2 * 0.0225 / 0.759
P(f"[{FOOT}] G8 forest (law, matter) dchi2 {frL['dchi2']:.4g} -> {frL['status']}; baryon tracer {frB['dchi2']:.4g}; Newtonian warm {frN['dchi2']:.4g} ({frN['status']}); R=1 {fr0['dchi2']:.1e}")
P(f"[{FOOT}] G8 fsigma8 (law): " + " ".join(f"{r['bin']} {r['Rf']:.3f}" for r in FSL["rows"]) + f" -> {'PASS' if FSL['pass_'] else 'FAIL'}; Newtonian warm " + " ".join(f"{r['bin']} {r['Rf']:.3f}" for r in FSN["rows"]) + f" ({'PASS' if FSN['pass_'] else 'FAIL'}); G8 {RES['G8']['status']}")
P(f"[{FOOT}] CS: sigma8 ratio {RES['CS']['sigma8_ratio']:.3f}, S8 {RES['CS']['S8']:.3f} vs {RES['CS']['S8_ref']:.3f} ({100*RES['CS']['change']:+.1f} %, line +-5.9 %) -> {RES['CS']['status']}; P/P_ref " + " ".join(f"{k}:{v:.3g}" for k, v in RES['CS']['P_ratio'].items())
  + f"; Newtonian warm S8 {100*RES['CS']['newton_warm_reported']['change']:+.1f} %, P " + " ".join(f"{k}:{v:.3g}" for k, v in RES['CS']['newton_warm_reported']['P_ratio'].items()))
# ---------------------------------------------------------------- MN: baryons Newtonian
MN0 = dict(forest_dchi2=fr0["dchi2"], lensing_chi2=float(Q3["best_amp_chi2"](X0 * limber4_bg(REFBG, np.ones_like(T2)))[0]), lensing_ref=float(c0))
MN0["pass_"] = bool(abs(MN0["forest_dchi2"]) <= 1e-6 and abs(MN0["lensing_chi2"] - c0) <= 1e-6)
RES["MN"] = dict(MN0_cold_limit=MN0, MNW_forest=frN, MNW_forest_fails=bool(frN["status"] == "FAIL"), MNW_note="FAIL required; a PASS = NO POWER on gate 8's forest half at this cutoff")
P(f"[{FOOT}] MN0 cold limit: forest {MN0['forest_dchi2']:.1e}, lensing {MN0['lensing_chi2']:.6f} vs {c0:.6f} -> {'PASS' if MN0['pass_'] else 'FAIL'}; MN-W forest {frN['dchi2']:.4g} -> {'FAILS (power)' if RES['MN']['MNW_forest_fails'] else 'PASSES (NO POWER)'}")
Mw.struct_cleanup(); Mw.empty(); M.struct_cleanup(); M.empty()
RES["peak_rss_GB"] = rss(); RES["seconds"] = time.time() - T0
json.dump(clean(RES), open(os.path.join(PARTS, f"cosmo_{V}_{FOOT}.json"), "w"), indent=1)
P(f"cosmo {V} {FOOT} done {RES['seconds']:.0f} s, peak RSS {RES['peak_rss_GB']:.2f} GB (CLASS included). kappa = 1/2 FITTED; not theory closed.")
