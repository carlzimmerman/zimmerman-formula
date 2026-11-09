#!/usr/bin/env python3
"""WM1 gate 7b-N and KA-W1 (FROZEN_CRITERIA.md 6e40130dfa): HC1 G9's statistic exactly (cfg917_lib raw PR4 lensing, 9 bandpowers,
A_s fitted analytically, 8 corners), with (KA-W1) HC1's 11.1377 eV relic and (7b-N) WM1's relic: m fixed from the frozen rule at the
canonical footing, omega_chi = 5.41 omega_b at each corner, T_ncdm from omega. Footing-free (linear CLASS has no a0 term).
    python3 wm1_hc1.py <mode>   mode in hc1, W, MW1, MW2, W3, Wthird   -> parts/g9_<mode>.json
kappa = 1/2 FITTED; not theory closed; adopts nothing."""
import os, sys, json, math, itertools, time
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[v] = "1"
sys.dont_write_bytecode = True
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(REPO, "campaign_fresh_gravity/CFG917_cmb_lensing_gate"))
import cfg917_lib as LIB
from classy import Class
CRIT = "6e40130dfa"; MODE = sys.argv[1]; T0 = time.time(); LINE = 18.48
D = LIB.load_pr4(); LMAX = LIB.LMAX; Larr = np.arange(LMAX + 1.0); AS0 = 2.0e-9
REL = json.load(open(os.path.join(HERE, "parts", "cosmo_W_canonical.json")))["relic"]          # the frozen rule's m (canonical footing)
MULTM = {"W": 1.0, "MW1": 10.0, "MW2": 0.1, "W3": 3.0, "Wthird": 1 / 3}
def P(s): print(s, flush=True)
def m_of(mode):
    if mode == "hc1": return 93.14 * 0.11958060485606123
    from scipy.optimize import brentq
    h, OD, OB = 0.6740779913310114, 0.12094000633665247, 0.02235817066393584; rho = (OB + OD) * 2.77536627e11
    def Mhm(mk):
        al = 0.049 * mk ** -1.11 * ((OD / h ** 2) / 0.25) ** 0.11 * (h / 0.7) ** 1.22 / h; lam = 2 * math.pi * al * (2 ** (1.12 / 5) - 1) ** (-1 / (2 * 1.12)); return 4 * math.pi / 3 * rho * (lam / 2) ** 3
    return 1000 * brentq(lambda x: math.log(Mhm(x) / (REL["M_hm"] * MULTM[mode])), 1e-3, 100.0, xtol=1e-12)
MEV = m_of(MODE)
def run(ob, H0, ns):
    om = 0.11958060485606123 if MODE == "hc1" else 5.41 * ob; T = 0.71611 if MODE == "hc1" else 0.71611 * (om * 93.14 / MEV) ** (1 / 3)
    p = {'output': 'tCl,lCl', 'l_max_scalars': LMAX + 100, 'h': H0 / 100, 'omega_b': ob, 'A_s': AS0, 'n_s': ns, 'tau_reio': 0.06, 'N_ur': 3.046, 'T_cmb': 2.7255,
         'omega_cdm': 1e-7, 'N_ncdm': 1, 'm_ncdm': MEV, 'T_ncdm': T, 'deg_ncdm': 1.0, 'ncdm_fluid_approximation': 3, 'tol_ncdm_bg': 1e-10}
    M = Class(); M.set(p); M.compute(); pp = M.raw_cl(LMAX)['pp']; M.struct_cleanup(); M.empty(); X = (Larr * (Larr + 1)) ** 2 * pp / (2 * np.pi)
    u = LIB.wsum(D["W"], X) + LIB.wsum(D["M"], X); a = LIB.qform(u, D["Cinv"], D["d"] + D["F"]); b = LIB.qform(u, D["Cinv"]); A = a / b
    r = A * u - D["F"] - D["d"]; return float(LIB.qform(r, D["Cinv"])), float(A), [float(x / y) for x, y in zip(A * u, D["d"] + D["F"])], om, T
rows = []
for ob, H0, ns in itertools.product((0.0215, 0.0230), (65.0, 75.0), (0.95, 0.98)):
    c, A, rb, om, T = run(ob, H0, ns); rows.append(dict(omega_b=ob, H0=H0, n_s=ns, omega_chi=om, T_ncdm=T, chi2=c, A_s=A * AS0, model_over_data_bp=rb))
    P(f"  [{MODE} m {MEV:.2f} eV] ob {ob} H0 {H0:g} ns {ns}: chi2 {c:.2f}; model/data {[round(x, 3) for x in rb]}  [{time.time()-T0:.0f}s]")
worst, best = max(r["chi2"] for r in rows), min(r["chi2"] for r in rows)
out = dict(criteria=CRIT, mode=MODE, m_eV=MEV, corners=rows, worst=worst, best=best, line=LINE, note="footing-free; TEST lane; kappa = 1/2 FITTED; not theory closed")
if MODE == "hc1": out["KA_W1"] = dict(ref_worst=194.2, ref_best=166.0, pass_=bool(abs(worst - 194.2) <= 0.2 and abs(best - 166.0) <= 0.2))
else: out["status"] = "PASS" if worst <= LINE else "FAIL"
json.dump(out, open(os.path.join(HERE, "parts", f"g9_{MODE}.json"), "w"), indent=1)
P(f"[{MODE}] worst {worst:.2f} best {best:.2f} line {LINE} -> " + (("KA-W1 " + ("PASS" if out["KA_W1"]["pass_"] else "FAIL")) if MODE == "hc1" else out["status"]) + f"  [{time.time()-T0:.0f}s]")
