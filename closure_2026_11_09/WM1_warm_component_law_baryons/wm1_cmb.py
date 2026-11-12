#!/usr/bin/env python3
"""WM1 gate 7a (FROZEN_CRITERIA.md 6e40130dfa): CMB primary with the warm relic. CLASS lensed TT/TE/EE at each footing's QX15 main
point, cold (omega_cdm) and warm (ncdm, same omega), graded by QX15's qx15_like PA (Pcut + ACT DR6 CMB-only, nuisances profiled),
Delta = chi2(warm) - chi2(cold), no refit. Lines: <= 4 PASS, 4-25 TENSION, > 25 FAIL. Footing-free in the law (linear CLASS).
    SS1_FOOT=<f> python3 wm1_cmb.py   -> parts/cmb7a_<footing>.json   (W, MW1, MW2, W3, Wthird)
kappa = 1/2 FITTED; not theory closed; adopts nothing."""
import os, sys, json, math, time, resource
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[v] = "1"
sys.dont_write_bytecode = True
import numpy as np
from scipy.optimize import brentq
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
Q15D = os.path.join(REPO, "closure_2026_11_06", "QX15_cmb_primary_likelihood"); sys.path.insert(0, Q15D)
import qx15_like as QL
from classy import Class
CRIT = "6e40130dfa"; FOOT = os.environ.get("SS1_FOOT", "canonical"); T0 = time.time(); LPAD = 9001; LM = 8600
def P(s): print(s, flush=True)
m = json.load(open(os.path.join(Q15D, "qx15.json")))["footings"][FOOT]["main"]; th = m["theta"]; h = float(m["h"]); OB, OD = th["omega_b"], th["omega_d"]
MHM0 = (0.050 ** (-1 / 1.16) - 1) * 4.060e11; MULT = {"W": 1.0, "MW1": 10.0, "MW2": 0.1, "W3": 3.0, "Wthird": 1 / 3}
def relic(V):
    Om = (OB + OD) / h ** 2; rho = Om * 2.77536627e11 * h ** 2
    def Mhm(mk):
        al = 0.049 * mk ** -1.11 * ((OD / h ** 2) / 0.25) ** 0.11 * (h / 0.7) ** 1.22 / h; lam = 2 * math.pi * al * (2 ** (1.12 / 5) - 1) ** (-1 / (2 * 1.12)); return 4 * math.pi / 3 * rho * (lam / 2) ** 3
    mk = brentq(lambda x: math.log(Mhm(x) / (MHM0 * MULT[V])), 1e-3, 100.0, xtol=1e-12); mev = 1000 * mk; return mev, 0.71611 * (OD * 93.14 / mev) ** (1 / 3)
def spectra(V):
    p = {'output': 'tCl,pCl,lCl', 'lensing': 'yes', 'l_max_scalars': LM, 'h': h, 'omega_b': OB, 'A_s': math.exp(th["lnAs1e10"]) / 1e10, 'n_s': th["n_s"],
         'tau_reio': th["tau"], 'N_ur': 3.046, 'T_cmb': 2.7255}
    if V == "cold": p['omega_cdm'] = OD
    else:
        mev, T = relic(V); p.update({'omega_cdm': 1e-7, 'N_ncdm': 1, 'm_ncdm': mev, 'T_ncdm': T, 'deg_ncdm': 1.0, 'tol_ncdm_bg': 1e-10})
    M = Class(); M.set(p); M.compute(); cl = M.lensed_cl(LM - 100); M.struct_cleanup(); M.empty()
    l = np.arange(len(cl['tt'])); f = l * (l + 1) / (2 * np.pi) * (2.7255e6) ** 2; D = {}
    for X in ("tt", "te", "ee"): a = np.zeros(LPAD); a[:len(l)] = cl[X] * f; D[X] = a
    return D
RES = dict(criteria=CRIT, footing=FOOT, point=dict(h=h, **th), note="TEST lane; adopts nothing; kappa = 1/2 FITTED; not theory closed")
Dc = spectra("cold"); gc = QL.grade_spectra(Dc); RES["cold"] = dict(PA=gc["PA"], Pcut=gc["Pcut"]["chi2"], A=gc["A"]["chi2"], QX15_CAMB_PA_reported=m["chi2_PA"])
P(f"[{FOOT}] 7a cold (CLASS) PA {gc['PA']:.2f} (QX15 CAMB {m['chi2_PA']:.2f}, reported)  [{time.time()-T0:.0f}s {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1e9:.2f}GB]")
for V in ("W", "MW1", "MW2", "W3", "Wthird"):
    mev, T = relic(V); g = QL.grade_spectra(Spec := spectra(V)); d = g["PA"] - gc["PA"]
    lab = "PASS" if d <= 4 else ("TENSION" if d <= 25 else "FAIL")
    RES[V] = dict(m_eV=mev, T_ncdm=T, PA=g["PA"], delta=d, delta_Pcut=g["Pcut"]["chi2"] - gc["Pcut"]["chi2"], delta_A=g["A"]["chi2"] - gc["A"]["chi2"], label=lab, status="PASS" if lab == "PASS" else "FAIL",
                  TT_ratio={f"L {L}": float(Spec["tt"][L] / Dc["tt"][L]) for L in (30, 300, 1000, 2000, 3000, 5000)})
    P(f"[{FOOT}] 7a {V} (m {mev:.1f} eV): PA {g['PA']:.2f}, Delta {d:+.3f} (Pcut {RES[V]['delta_Pcut']:+.3f}, ACT {RES[V]['delta_A']:+.3f}) -> {lab}; TT warm/cold " + " ".join(f"{k}:{v:.5f}" for k, v in RES[V]['TT_ratio'].items()) + f"  [{time.time()-T0:.0f}s]")
RES["peak_rss_GB"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9; RES["seconds"] = time.time() - T0
json.dump(RES, open(os.path.join(HERE, "parts", f"cmb7a_{FOOT}.json"), "w"), indent=1, default=float)
P(f"7a {FOOT} done {RES['seconds']:.0f} s, peak RSS {RES['peak_rss_GB']:.2f} GB (CLASS included)")
