#!/usr/bin/env python3
"""WM1 gate 0, SEEDING (AMENDMENT_A2 c830b470e0; criteria 6e40130dfa, A1 5cba17a249). CLASS transfers at z 1000 / 950 (Silk-damped
baryons, the relic's own free-streaming cut) -> the two-fluid ODE (law on with A1's nu from the cold reference power; Newton beside)
-> P_b, P_m vs the cold reference at k 0.5-5 h/Mpc, z 3 and 0; Press-Schechter n(>M) (sharp-k c 2.5 graded; top-hat reported) at
1e10-1e12 Msun, z 2 and 0; KA-S1/S2/S3; the outside source's round-16 numbers checked (never adopted).
    SS1_FOOT=<f> python3 wm1_seed.py   -> parts/seed_<footing>.json (+ prints)
kappa = 1/2 FITTED; not theory closed; adopts nothing."""
import os, sys, json, math, time, resource
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[v] = "1"
sys.dont_write_bytecode = True
import warnings; warnings.filterwarnings("ignore")
import numpy as np
from scipy.optimize import brentq
from scipy.special import erfc
from classy import Class
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
A2 = "c830b470e0"; CRIT = "6e40130dfa"; FOOT = os.environ.get("SS1_FOOT", "canonical"); T0 = time.time()
def P(s): print(s, flush=True)
Q15 = json.load(open(os.path.join(REPO, "closure_2026_11_06", "QX15_cmb_primary_likelihood", "qx15.json")))
th = Q15["footings"][FOOT]["main"]["theta"]; h = float(Q15["footings"][FOOT]["main"]["h"]); OB, OD = th["omega_b"], th["omega_d"]
AS = math.exp(th["lnAs1e10"]) / 1e10; A0 = {"canonical": 9.360324825027975e-11, "alt": 1.1312035414413022e-10}[FOOT]
Om = (OB + OD) / h ** 2; Orad = 2.469e-5 * (1 + 0.2271 * 3.046) / h ** 2; OL = 1 - Om - Orad; H0 = 100 * h * 1e3 / 3.0857e22
RHOM = Om * 2.77536627e11 * h ** 2                                                     # Msun / Mpc^3 comoving
MHM0 = (0.050 ** (-1 / 1.16) - 1) * 4.060e11
def viel_Mhm(mk):
    al = 0.049 * mk ** -1.11 * ((OD / h ** 2) / 0.25) ** 0.11 * (h / 0.7) ** 1.22 / h; lam = 2 * math.pi * al * (2 ** (1.12 / 5) - 1) ** (-1 / (2 * 1.12)); return 4 * math.pi / 3 * RHOM * (lam / 2) ** 3
def m_for(Mhm): return 1000 * brentq(lambda x: math.log(viel_Mhm(x) / Mhm), 1e-3, 100.0, xtol=1e-12)
RELICS = {"W": m_for(MHM0), "MW1": m_for(10 * MHM0), "MW2": m_for(MHM0 / 10), "SRC107.5": 107.5}
ZREC = [1000.0, 950.0, 3.0, 2.0, 0.0]
def run(m_ev=None, cl=False):
    p = {'output': 'mTk,mPk' + (',tCl,pCl,lCl' if cl else ''), 'h': h, 'omega_b': OB, 'A_s': AS, 'n_s': th["n_s"], 'tau_reio': th["tau"], 'N_ur': 3.046, 'T_cmb': 2.7255,
         'P_k_max_1/Mpc': 60.0, 'z_max_pk': 1000.0}
    if cl: p.update({'lensing': 'yes', 'l_max_scalars': 2600})
    if m_ev is None: p['omega_cdm'] = OD
    else: p.update({'omega_cdm': 1e-7, 'N_ncdm': 1, 'm_ncdm': m_ev, 'T_ncdm': 0.71611 * (OD * 93.14 / m_ev) ** (1 / 3), 'deg_ncdm': 1.0, 'tol_ncdm_bg': 1e-10})
    M = Class(); M.set(p); M.compute(); return M
KH = np.geomspace(0.01, 40.0, 140); KM = KH * h                                         # h/Mpc and 1/Mpc
def transfers(M, warm):
    out = {}
    for z in ZREC:
        t = M.get_transfer(z); k = t['k (h/Mpc)']; dc = t['d_ncdm[0]'] if warm else t['d_cdm']
        out[z] = dict(b=np.interp(np.log(KH), np.log(k), t['d_b']), c=np.interp(np.log(KH), np.log(k), dc), tot=np.interp(np.log(KH), np.log(k), t['d_tot']))
    return out
# ---------------- reference (cold) and nu (A1: cold reference power)
Mc = run(); TC = transfers(Mc, False)
ZT = np.concatenate([np.linspace(0, 3, 61), np.linspace(3.1, 20, 85)]); LP = np.log(np.array([[Mc.pk_lin(k, z) for z in ZT] for k in KM]))
def nu_at(z):
    zz = min(z, 20.0); j = min(max(np.searchsorted(ZT, zz), 1), len(ZT) - 1); w = (zz - ZT[j - 1]) / (ZT[j] - ZT[j - 1])
    Pk = np.exp((1 - w) * LP[:, j - 1] + w * LP[:, j]) * (((1 + 20.0) / (1 + z)) ** 2 if z > 20 else 1.0)
    y = np.maximum(1.5 * H0 ** 2 * Om * np.sqrt(KM ** 3 * Pk / (2 * math.pi ** 2)) / ((1 / (1 + z)) ** 2 * (KM / 3.0857e22)) / A0, 1e-30); return 0.5 + np.sqrt(0.25 + 1 / y)
def Hs(a): return H0 * math.sqrt(Om / a ** 3 + Orad / a ** 4 + OL)
def ode(T, newton):
    """two-fluid from z 1000 with CLASS IC (finite difference 1000 -> 950 for d/d ln a); returns delta_b, delta_chi at z 3, 2, 0."""
    l1, l2 = math.log(1 / 1001.0), math.log(1 / 951.0)
    y = np.stack([T[1000.0]["c"], (T[950.0]["c"] - T[1000.0]["c"]) / (l2 - l1), T[1000.0]["b"], (T[950.0]["b"] - T[1000.0]["b"]) / (l2 - l1)], axis=1)
    rec = [3.0, 2.0, 0.0]; want = {float(math.log(1 / (1 + z))): z for z in rec}
    grid = np.unique(np.concatenate([np.linspace(l1, 0.0, 8001), list(want)])); out = {}; I4 = np.eye(4)[None]; nk = len(KH)
    for n in range(len(grid) - 1):
        hh = grid[n + 1] - grid[n]; a = math.exp(0.5 * (grid[n] + grid[n + 1])); z = 1 / a - 1; Ha = Hs(a)
        dl = (-1.5 * Om / a ** 3 - 2 * Orad / a ** 4) * H0 ** 2 / Ha ** 2; Oc = OD / h ** 2 / a ** 3 * H0 ** 2 / Ha ** 2; Ob = OB / h ** 2 / a ** 3 * H0 ** 2 / Ha ** 2
        nu = np.ones(nk) if newton else nu_at(z)
        A = np.zeros((nk, 4, 4)); A[:, 0, 1] = 1; A[:, 1, 0] = 1.5 * Oc; A[:, 1, 2] = 1.5 * Ob; A[:, 1, 1] = -(2 + dl)
        A[:, 2, 3] = 1; A[:, 3, 0] = 1.5 * Oc * nu; A[:, 3, 2] = 1.5 * Ob * nu; A[:, 3, 3] = -(2 + dl)
        y = np.linalg.solve(I4 - 0.5 * hh * A, ((I4 + 0.5 * hh * A) @ y[:, :, None]))[:, :, 0]
        g = float(grid[n + 1])
        if g in want: out[want[g]] = dict(b=y[:, 2].copy(), c=y[:, 0].copy(), m=(OD * y[:, 0] + OB * y[:, 2]) / (OD + OB))
    return out
def pk_model(Mref, z, dm):                                                             # absolute linear power of the model's delta_m
    Pr = np.array([Mref.pk_lin(k, z) for k in KM]); return Pr * (dm / TC[z]["tot"]) ** 2
def nps(Pk, filt):
    """cumulative PS n(>M) [Mpc^-3] at M 1e10, 1e11, 1e12; k grid KM extended below 0.01 h/Mpc with the reference power x (boost at the first node)^2."""
    kl = np.geomspace(1e-4, KM[0], 60, endpoint=False); Pl = np.array([Mc.pk_lin(k, 0.0) for k in kl]) * (Pk[0] / Mc.pk_lin(KM[0], 0.0))
    kk = np.concatenate([kl, KM]); PP = np.concatenate([Pl, Pk]); MG = np.geomspace(1e8, 1e16, 161); sig = []
    for Mm in MG:
        R = (3 * Mm / (4 * math.pi * RHOM)) ** (1 / 3)
        if filt == "sharpk": Rk = R / 2.5; m = kk <= 1 / Rk; sig.append(math.sqrt(np.trapz((kk ** 3 * PP / (2 * math.pi ** 2))[m], np.log(kk[m]))) if m.sum() > 1 else 0.0)
        else: x = kk * R; W = 3 * (np.sin(x) - x * np.cos(x)) / x ** 3; sig.append(math.sqrt(np.trapz(kk ** 3 * PP * W * W / (2 * math.pi ** 2), np.log(kk))))
    sig = np.maximum(np.array(sig), 1e-12); F = erfc(1.686 / (math.sqrt(2) * sig)); dF = -np.gradient(F, MG)
    dn = RHOM / MG * np.maximum(dF, 0); cum = np.concatenate([np.cumsum((0.5 * (dn[1:] + dn[:-1]) * np.diff(MG))[::-1])[::-1], [0.0]])
    return {f"{M_:.0e}": float(np.interp(math.log(M_), np.log(MG), cum)) for M_ in (1e10, 1e11, 1e12)}
RES = dict(amendment=A2, criteria=CRIT, footing=FOOT, relics=RELICS, note="TEST lane; adopts nothing; kappa = 1/2 FITTED; not theory closed")
# KA-S2: Newton from the cold CLASS IC vs CLASS cold
oc = ode(TC, True); ks = [0.5, 1.0, 2.0, 5.0]
def atk(arr, k): return float(np.interp(math.log(k), np.log(KH), arr))
ka2 = {f"k {k}": atk(oc[0.0]["m"] / TC[0.0]["tot"], k) for k in ks}; RES["KA_S2"] = dict(ratio_ode_over_class_z0=ka2, pass_=bool(all(abs(v - 1) <= 0.02 for v in ka2.values())))
P(f"[{FOOT}] KA-S2 cold Newton ODE / CLASS at z 0: " + " ".join(f"{k}:{v:.4f}" for k, v in ka2.items()) + f" -> {'PASS' if RES['KA_S2']['pass_'] else 'FAIL'}  [{time.time()-T0:.0f}s]")
ref_n = {z: dict(sharpk=nps(pk_model(Mc, z, oc[z]["m"]), "sharpk"), tophat=nps(pk_model(Mc, z, oc[z]["m"]), "tophat")) for z in (2.0, 0.0)}
RES["reference_n"] = ref_n
RES["KA_S3"] = {f"z {z}": dict(sharpk_1e12=ref_n[z]["sharpk"]["1e+12"], tophat_1e12=ref_n[z]["tophat"]["1e+12"], ratio=ref_n[z]["sharpk"]["1e+12"] / max(ref_n[z]["tophat"]["1e+12"], 1e-300)) for z in (2.0, 0.0)}
P(f"[{FOOT}] reference n(>M) [Mpc^-3] z 0 sharp-k " + " ".join(f"{k}:{v:.3g}" for k, v in ref_n[0.0]['sharpk'].items()) + "; top-hat " + " ".join(f"{k}:{v:.3g}" for k, v in ref_n[0.0]['tophat'].items()) + f"; KA-S3 ratio at 1e12 z0 {RES['KA_S3']['z 0.0']['ratio']:.2f}")
for V, mev in RELICS.items():
    Mw = run(mev, cl=(V == "SRC107.5")); TW = transfers(Mw, True); oL = ode(TW, False); oN = ode(TW, True); r = dict(m_eV=mev)
    kz = np.geomspace(0.05, 20, 300); rr = np.array([Mw.pk_lin(k * h, 0.0) / Mc.pk_lin(k * h, 0.0) for k in kz]); r["k_hm_CLASS_hMpc"] = float(np.interp(0.25, rr[::-1], kz[::-1]))
    r["KA_S1"] = {f"k {k}": atk(oN[0.0]["m"] / TW[0.0]["tot"], k) for k in ks}
    r["KA_S1_pass"] = bool(all(abs(r["KA_S1"][f"k {k}"] - 1) <= 0.05 for k in (0.5, 1.0)) and abs(r["KA_S1"]["k 2.0"] - 1) <= 0.25)
    r["IC_z1000"] = {f"k {k}": dict(delta_b_over_cold_tot=atk(TW[1000.0]["b"] / TC[1000.0]["tot"], k), delta_chi_over_cold_tot=atk(TW[1000.0]["c"] / TC[1000.0]["tot"], k)) for k in ks}
    pw = {}
    for z in (3.0, 0.0):
        for k in ks:
            pw[f"z {z} k {k}"] = dict(Pb_law=atk((oL[z]["b"] / TC[z]["tot"]) ** 2, k), Pm_law=atk((oL[z]["m"] / TC[z]["tot"]) ** 2, k), Pb_newton=atk((oN[z]["b"] / TC[z]["tot"]) ** 2, k),
                                      Pm_newton=atk((oN[z]["m"] / TC[z]["tot"]) ** 2, k), Pm_CLASS_warm=atk((TW[z]["tot"] / TC[z]["tot"]) ** 2, k))
    r["power_vs_cold"] = pw
    nn = {}; ok = True
    for z in (2.0, 0.0):
        nl_s = nps(pk_model(Mc, z, oL[z]["m"]), "sharpk"); nl_t = nps(pk_model(Mc, z, oL[z]["m"]), "tophat"); nn_s = nps(pk_model(Mc, z, oN[z]["m"]), "sharpk"); nb_s = nps(pk_model(Mc, z, oL[z]["b"]), "sharpk")
        nn[f"z {z}"] = dict(sharpk_law=nl_s, tophat_law_reported=nl_t, sharpk_newton_reported=nn_s, sharpk_baryon_power_reported=nb_s,
                            ratio_to_ref_sharpk_law={m_: nl_s[m_] / ref_n[z]["sharpk"][m_] for m_ in nl_s})
        for m_ in ("1e+10", "1e+11"): ok &= nl_s[m_] >= 0.5 * ref_n[z]["sharpk"][m_]
    r["halo_abundance"] = nn; r["gate0"] = "PASS" if ok else "FAIL"
    if V == "SRC107.5":
        cw = Mw.lensed_cl(2500); cc = Mc_cl.lensed_cl(2500); pw_ = Mw.raw_cl(2500)['pp']; pc_ = Mc_cl.raw_cl(2500)['pp']
        r["source_check"] = dict(TT_maxabs_l_lt_800=float(np.max(np.abs(cw['tt'][2:800] / cc['tt'][2:800] - 1))), TT_l2500=float(cw['tt'][2500] / cc['tt'][2500] - 1),
                                 pp_ratio={f"L {L}": float(pw_[L] / pc_[L]) for L in (100, 300, 1000)})
    Mw.struct_cleanup(); Mw.empty(); RES[V] = r
    P(f"[{FOOT}] {V} m {mev:.1f} eV (k_hm CLASS {r['k_hm_CLASS_hMpc']:.3f} h/Mpc): KA-S1 Newton/CLASS z0 " + " ".join(f"{k}:{v:.3f}" for k, v in r['KA_S1'].items()) + f" ({'PASS' if r['KA_S1_pass'] else 'FAIL'})")
    P("    IC z1000 delta_b/cold " + " ".join(f"{k}:{v['delta_b_over_cold_tot']:.3g}" for k, v in r['IC_z1000'].items()) + "; delta_chi/cold " + " ".join(f"{k}:{v['delta_chi_over_cold_tot']:.3g}" for k, v in r['IC_z1000'].items()))
    for z in (3.0, 0.0): P(f"    z {z}: P_b/P_ref law " + " ".join(f"{k}:{pw[f'z {z} k {k}']['Pb_law']:.3g}" for k in ks) + " | P_m law " + " ".join(f"{k}:{pw[f'z {z} k {k}']['Pm_law']:.3g}" for k in ks) + " | P_m Newton " + " ".join(f"{k}:{pw[f'z {z} k {k}']['Pm_newton']:.3g}" for k in ks))
    for z in (2.0, 0.0): P(f"    n(>M)/ref sharp-k law z {z}: " + " ".join(f"{m_}:{v:.3g}" for m_, v in nn[f'z {z}']['ratio_to_ref_sharpk_law'].items()) + "; Newton " + " ".join(f"{m_}:{nn[f'z {z}']['sharpk_newton_reported'][m_]/ref_n[z]['sharpk'][m_]:.3g}" for m_ in ('1e+10', '1e+11', '1e+12')))
    P(f"    gate 0: {r['gate0']}" + (f"; source check: TT max|d| l<800 {r['source_check']['TT_maxabs_l_lt_800']:.4f}, l 2500 {r['source_check']['TT_l2500']:+.4f}; pp warm/cold " + " ".join(f"{k}:{v:.3f}" for k, v in r['source_check']['pp_ratio'].items()) if 'source_check' in r else "") + f"  [{time.time()-T0:.0f}s {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1e9:.2f}GB]")
    if V == "W": pass
    if V == "MW2":                                                                      # cold CL run for the source check comes next
        Mc_cl = run(None, cl=True)
# ---------------- the source's M_hm and capture f (checked, never adopted)
src = {}
for mev in (105.0, 107.5, 110.0, RELICS["W"]):
    src[f"{mev:.1f} eV"] = dict(source_formula=1.19e10 * (mev / 1000) ** -3.33, viel_halfmode=viel_Mhm(mev / 1000))
def fcap(Mhm, Mtot): return (1 + (Mhm / (2 * Mtot)) ** 0.8) ** -1.5
Ms = viel_Mhm(0.1075)
cap = {"lenses_logMstar": {f"{lm}": dict(f_source_Mhm=fcap(1.19e10 * 0.1075 ** -3.33, 6.41 * 10 ** lm), f_viel_107p5=fcap(Ms, 6.41 * 10 ** lm), f_at_W=fcap(MHM0, 6.41 * 10 ** lm)) for lm in (10.5, 11.0, 11.3, 11.5)},
       "groups_M500": {f"{M5:.1e}": dict(f_source_Mhm=fcap(1.19e10 * 0.1075 ** -3.33, M5), f_viel_107p5=fcap(Ms, M5), f_at_W=fcap(MHM0, M5)) for M5 in (2.1e13, 4.5e13, 1.4e14)}}
RES["source_check"] = dict(M_hm=src, capture=cap)
P(f"[{FOOT}] source M_hm: " + "; ".join(f"{k}: formula {v['source_formula']:.3g} vs Viel {v['viel_halfmode']:.3g}" for k, v in src.items()))
P(f"[{FOOT}] source capture f (its M_hm / Viel 107.5 / W): lenses " + "; ".join(f"{k}: {v['f_source_Mhm']:.3f}/{v['f_viel_107p5']:.3f}/{v['f_at_W']:.3f}" for k, v in cap['lenses_logMstar'].items()) + " | groups " + "; ".join(f"{k}: {v['f_source_Mhm']:.3f}/{v['f_viel_107p5']:.3f}/{v['f_at_W']:.3f}" for k, v in cap['groups_M500'].items()))
Mc.struct_cleanup(); Mc_cl.struct_cleanup()
RES["peak_rss_GB"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9; RES["seconds"] = time.time() - T0
json.dump(RES, open(os.path.join(HERE, "parts", f"seed_{FOOT}.json"), "w"), indent=1, default=float)
P(f"seed {FOOT} done {RES['seconds']:.0f} s, peak RSS {RES['peak_rss_GB']:.2f} GB. kappa = 1/2 FITTED; not theory closed.")
