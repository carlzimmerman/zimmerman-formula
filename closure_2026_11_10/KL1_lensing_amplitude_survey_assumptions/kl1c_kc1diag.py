#!/usr/bin/env python3
"""KL1 PART C, AMENDMENT C2 (post hoc, 2fd0710da0): the KC1 diagnostic on DES Y3 alt. Part A's ALL settings for DES (A1's target,
A3's gas at r_ta, A2's covariance at the model with gamma 2) refitted through Part A's own code path (kl1_lib.fit's objective and
L-BFGS-B settings) from three starts: Part A's stored nuisance vector, Part C's replay vector, and kl1_lib.fit's default starts.

  OMP_NUM_THREADS=1 nice -n 10 python3 kl1c_kc1diag.py     -> parts/kc1diag.json, parts/kc1diag.out
kappa = 1/2 FITTED; not theory closed; adopts nothing."""
import os, sys, json, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from scipy.optimize import minimize
import kl1_lib as K1
HERE = K1.HERE; FT = "alt"; G, SURV = K1.G, K1.SURV
NU = json.load(open(os.path.join(HERE, "kl1_nu.json"))); GAS = json.load(open(os.path.join(HERE, "kl1_gas.json")))
PA = json.load(open(os.path.join(HERE, "parts", f"rows_{FT}.json"))); PC = json.load(open(os.path.join(HERE, "parts", f"partc_{FT}_deskids.json")))
S8 = NU["A1"][FT]["sigma8_nu"]; Rg = np.array(GAS["rows"][FT]["rta_table"]["R_tot"]); Rco1 = np.array(K1.HM["primary"][FT]["R_tot"])
def Pm_of(Rk, s8): K1.setP(K1.PZ0); return K1.Pmat(K1.run_of(Rk, (s8 / K1.S8E) ** 2, "resp"), "F")
sn = "DES"; S = SURV[sn]; pub = np.where(S["pubkeep"])[0]; fid = PA["rows"]["A0"][sn]["best_sigma8"]
Pf = Pm_of(Rco1, fid); G1, N1 = K1.gauss_cov(S, pub, K1.cell_full(S, Pf)); Cp = S["cov"][np.ix_(pub, pub)]
nf = np.diag(N1) / np.diag(G1); nd = nf >= 0.8; area = float(1.0 / np.median(np.diag(Cp)[nd] / np.diag(G1)[nd])); Rr = Cp - G1 / area; xif = K1.xi_nominal(S, Pf)
km = K1.keep_mask(sn); D = K1.subset(S, km); kept = np.where(km)[0]; pos = {int(g): i for i, g in enumerate(pub)}; kp = np.array([pos[int(g)] for g in kept])
Pm = Pm_of(Rg, S8); Gm, _ = K1.gauss_cov(S, kept, K1.cell_full(S, Pm)); s = np.clip(K1.xi_nominal(S, Pm)[kept] / xif[kept], 0.5, 3.0)
C = Gm / area + Rr[np.ix_(kp, kp)] * np.outer(s, s); Ci = np.linalg.inv(C)
x0, lo, hi, unpack, prior = G["nuis_spec"](S, 1.0, True)
def f(x):
    r = D["d"] - G["theory"](S, D, unpack(x), Pm, "PM"); return float(r @ Ci @ r) + prior(x)
out = {}
for tag, xs in (("PartA_stored", PA["rows"]["ALL"][sn]["at_target"]["x"]), ("PartC_replay", PC["rows"]["KC1|DES"]["at_target"]["x"])):
    v0 = f(np.array(xs)); r = minimize(f, np.array(xs), method="L-BFGS-B", bounds=list(zip(lo, hi)), options=dict(maxiter=400, ftol=1e-12, gtol=1e-8))
    out[tag] = dict(chi2_at_start=v0, chi2_refit=float(r.fun), message=str(r.message))
d = K1.fit(S, D, Pm, Cinv=Ci); out["default_starts"] = dict(chi2_refit=d["chi2"])
low = min(v["chi2_refit"] for v in out.values()); out["lowest"] = low; out["PartA_stored_value"] = PA["rows"]["ALL"][sn]["at_target"]["chi2"]
out["optimiser_floor_shown"] = bool(low <= 64.61)
lines = [f"KC1 diagnostic, DES Y3 alt at Part A's ALL settings (area {area * (180 / math.pi) ** 2:.1f} deg^2, fiducial {fid:.4f}):"]
for k in ("PartA_stored", "PartC_replay"):
    lines.append(f"  from {k}: chi2 at the start {out[k]['chi2_at_start']:.3f}, refit {out[k]['chi2_refit']:.3f} ({out[k]['message']})")
lines.append(f"  default starts (kl1_lib.fit): {out['default_starts']['chi2_refit']:.3f};  lowest {low:.3f} against Part A's stored {out['PartA_stored_value']:.3f} -> "
             f"{'optimiser floor shown: KC1 for DES read with tolerance 0.2 under C2' if out['optimiser_floor_shown'] else 'NOT shown: KC1 stays failed under C2'}")
print("\n".join(lines))
json.dump(out, open(os.path.join(HERE, "parts", "kc1diag.json"), "w"), indent=1)
open(os.path.join(HERE, "parts", "kc1diag.out"), "w").write("\n".join(lines) + "\n")
