#!/usr/bin/env python3
"""KL1 (FROZEN_CRITERIA.md 99a42c78ef) row A1, second half: the target sigma8 with the neutrino floor (CLASS, total matter),
from the refits in parts/fit_nu_<footing>.json. CLASS set-up copied from CO2's co2_rows.class_B (one 0.06 eV neutrino: N_ur 2.0328,
N_ncdm 1, T_ncdm 0.71611; massless: N_ur 3.046).
  KA1 (ii)  CO2's bracket: sigma8 with the neutrino at CO2's pinned parameters = 0.8152 (0.0005).
  A1s       reported: [P_lin,nu(k) / P_lin,0(k)] (sigma8_0 / sigma8_nu)^2 at z 0 at the refit (massless twin: same parameters).
  MA1       (MUTATE) one 0.6 eV neutrino at the refit must lower sigma8 by >= 0.03 -> kl1_nu_MUTATE.json.

  OMP_NUM_THREADS=1 nice -n 10 python3 kl1_nu.py     -> kl1_nu.json, kl1_nu.out, kl1_nu_MUTATE.json
kappa = 1/2 FITTED; footings never pooled; not theory closed; adopts nothing."""
import os, json, math, time
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np
from classy import Class
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
CO2 = os.path.join(REPO, "closure_2026_11_09", "CO2_form_b_amplitude_pinned")
FOOTS = ("canonical", "alt"); OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
T0 = time.time()
def class_B(pr, mnu=0.0):
    M = Class()
    d = {'output': 'mPk', 'h': pr["h"], 'omega_b': pr["ob"], 'omega_cdm': pr["oc"], 'A_s': math.exp(pr["lnA"]) * 1e-10,
         'n_s': pr["ns"], 'tau_reio': pr["tau"], 'N_ur': 3.046, 'T_cmb': 2.7255, 'P_k_max_1/Mpc': 60.0, 'z_max_pk': 3.0}
    if mnu > 0: d.update({'N_ur': 2.0328, 'N_ncdm': 1, 'm_ncdm': mnu, 'T_ncdm': 0.71611})
    M.set(d); M.compute(); return M
ROWS = json.load(open(os.path.join(CO2, "co2_rows.json")))
KG = np.geomspace(1e-3, 40.0, 300)                         # h / Mpc
RES = dict(lane="KL1", row="A1 sigma8", criteria="99a42c78ef", note="kappa = 1/2 FITTED; not theory closed; adopts nothing", k_hMpc=KG.tolist(), KA={}, A1={}, MUT={})
P("KL1 A1: the target sigma8 with one 0.06 eV neutrino (CLASS, total matter). kappa = 1/2 FITTED; not theory closed.")
for ft in FOOTS:
    F2 = json.load(open(os.path.join(CO2, "parts", f"fit_{ft}.json"))); M = class_B(F2["pars"], 0.06); s = M.sigma8(); M.struct_cleanup()
    ref = ROWS["brackets"][ft]["one_0p06eV_neutrino"]["sigma8"]
    RES["KA"][ft] = dict(KA1_ii=s, ref=ref, d=s - ref, pass_=bool(abs(s - ref) <= 5e-4))
    P(f"[{ft}] KA1 (ii) sigma8 with the neutrino at CO2's pinned parameters {s:.5f} (CO2 {ref:.5f}) -> {'PASS' if abs(s - ref) <= 5e-4 else 'FAIL'}")
    F = json.load(open(os.path.join(HERE, "parts", f"fit_nu_{ft}.json"))); pr = F["pars"]
    Mn = class_B(pr, 0.06); M0 = class_B(pr, 0.0); sn, s0 = Mn.sigma8(), M0.sigma8(); hh = pr["h"]; Om = Mn.Omega_m()
    pn = np.array([Mn.pk_lin(k * hh, 0.0) for k in KG]); p0 = np.array([M0.pk_lin(k * hh, 0.0) for k in KG]); Mn.struct_cleanup(); M0.struct_cleanup()
    shape = (pn / p0) * (s0 / sn) ** 2
    Mm = class_B(pr, 0.6); sm = Mm.sigma8(); Mm.struct_cleanup()
    RES["A1"][ft] = dict(pars=pr, sigma8_nu=sn, sigma8_massless_twin=s0, S8_nu=sn * math.sqrt(Om / 0.3), Omega_m=Om, shape_factor=shape.tolist(),
                         shape_at={str(k): float(np.interp(k, KG, shape)) for k in (0.01, 0.1, 0.3, 1.0, 3.0, 10.0)},
                         d_total_vs_CO2=F["d_total_vs_CO2"], adequate=F["adequate"], CO2_sigma8=ROWS["P2"][ft]["sigma8"])
    RES["MUT"][ft] = dict(sigma8_0p6=sm, drop=sn - sm, bites=bool(sn - sm >= 0.03))
    P(f"[{ft}] A1 refit: tau {pr['tau']:.4f}, ln A_s {pr['lnA']:.4f}, omega_d {pr['oc']:.5f}, h {pr['h']:.5f}; CMB total {F['d_total_vs_CO2']:+.2f} against CO2's pinned fit "
      f"({'adequate' if F['adequate'] else 'PINNED FIT INADEQUATE WITH THE FLOOR'}); sigma8 {sn:.4f} (massless twin {s0:.4f}; CO2 pinned {ROWS['P2'][ft]['sigma8']:.4f}); S8 {sn * math.sqrt(Om / 0.3):.4f}, Omega_m {Om:.4f}")
    P(f"      A1s shape factor (unit at sigma8): " + ", ".join(f"k {k}: {v:.4f}" for k, v in RES['A1'][ft]['shape_at'].items()))
    P(f"      MA1 (MUTATE) 0.6 eV: sigma8 {sm:.4f}, drop {sn - sm:.4f} -> {'bites' if sn - sm >= 0.03 else 'DOES NOT BITE'}")
RES["KA_ok"] = bool(all(v["pass_"] for v in RES["KA"].values()))
P(f"Known answer KA1 (ii) passes: {RES['KA_ok']}   ({time.time() - T0:.0f} s)")
mut = RES.pop("MUT")
json.dump(RES, open(os.path.join(HERE, "kl1_nu.json"), "w"), indent=1, default=float)
json.dump(dict(lane="KL1", arm="MA1 (MUTATE): one 0.6 eV neutrino at the A1 refit", note="kappa = 1/2 FITTED; not theory closed", rows=mut), open(os.path.join(HERE, "kl1_nu_MUTATE.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, "kl1_nu.out"), "w").write("\n".join(OUT) + "\n")
