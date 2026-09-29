#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG182 part C -- the POINT-LEVEL Gaussian-noise null (reported, not a pass line): 100 generative mock SPARC samples with
NO dipole, each run through the full profile pipeline, to give the distribution of the free-direction dipole A_hat that
pure measurement noise plus the declared nuisance priors produce at the real sky positions.

Mock recipe (FROZEN_QUESTION.md, "The null"): for each clean galaxy the true nuisances are drawn from the LML 2018 priors
(Upsilon_disk, Upsilon_bul log-normal about 0.5 and 0.7 with 0.1 dex; distance ~ N(D_SPARC, e_D); inclination
~ N(Inc, e_Inc)), a0 is the same for every galaxy (the primary no-dipole fit, a0_bar), the velocities are the nu_mono law
at those values plus Gaussian noise of width sqrt(s_i) e_V (s_i the galaxy's Birge factor from the real data), the
profile curves are rebuilt on a 0.02-dex grid, Birge-scaled, and the free-direction dipole is fitted at the real
positions.  The real data's A_hat is recomputed on the same 0.02-dex subgrid for a like-for-like comparison.
Also reported: the galaxy-level reduced chi2 and the ML extra scatter tau of the mocks, next to the real data's.

MUTATE=1: the mocks carry an injected dipole A = 0.20 in a random direction (seed 182); the mock A_hat distribution must
move up (median A_hat of the MUTATE mocks above the median of the no-dipole mocks).
Run:  python3 campaign_fresh_gravity/CFG182_a0_sky_dipole/cfg182_c_gaussnull.py      (MUTATE=1 for the control)
"""
import os
import sys
import math
import numpy as np
from scipy.optimize import minimize

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cfg182_common as C

R = C.Run("cfg182_c_gaussnull")
P, banner, check = R.P, R.banner, R.check
P(__doc__.split("Run:")[0].strip())
NMOCK = 100
GRID2 = np.round(np.arange(-11.30, -8.9999, 0.02), 2)
ST7 = [np.zeros(3)] + [0.3 * s * e for e in np.eye(3) for s in (1, -1)]

z = np.load(os.path.join(C.HERE, "cfg182_a_profiles.npz"))
sel = z["clean"]
names = list(z["names"][sel])
n = z["n"][sel]
npt = z["npt"][sel]
cv = C.Curves(z["grid"], z["chi_nu_mono"][sel], npt, birge=True)
L0 = C.fit_const(cv)["L"]
sub = np.isin(np.round(z["grid"], 2), GRID2)
cv2 = C.Curves(z["grid"][sub], z["chi_nu_mono"][sel][:, sub], npt, birge=True)
r_real = C.fit_template(cv2, n, starts=ST7)
A_real = float(np.linalg.norm(r_real["theta"]))
P(f"\n  real data on the 0.02-dex subgrid: log a0_bar = {L0:.4f} (0.01 grid), A_hat = {A_real:.4f}")


def tau_ml(c):
    xh, sg = c.xhat, c.sig
    L_ = C.fit_const(c)["L"]
    f = lambda q: np.sum((xh - q[0]) ** 2 / (sg ** 2 + math.exp(2 * q[1])) + np.log(sg ** 2 + math.exp(2 * q[1])))
    r = minimize(f, [L_, math.log(0.1)], method="Nelder-Mead", options=dict(xatol=1e-6, fatol=1e-8, maxiter=4000))
    t = math.exp(r.x[1])
    return (0.0 if t < 1e-3 else t), float(np.sum((xh - L_) ** 2 / sg ** 2) / (c.N - 1))


tau_real, rchi_real = tau_ml(cv2)
P(f"  real data: galaxy-level reduced chi2 {rchi_real:.2f}, extra scatter tau = {tau_real:.3f} dex")

G = {g["name"]: g for g in C.load_galaxies()}
gals = [G[nm] for nm in names]
rng = np.random.default_rng(1830 + (1 if C.MUTATE else 0))
D_inj = None
if C.MUTATE:
    D_inj = 0.20 * C.random_unit(np.random.default_rng(182))
    P(f"  *** MUTATE=1: mocks carry D_inj = {np.round(D_inj, 4).tolist()} (A = 0.20 toward "
      f"{tuple(round(v, 1) for v in C.lb_of(D_inj))}) ***")

banner(f"C1  {NMOCK} GENERATIVE MOCKS through the full profile pipeline (0.02-dex grid)")
A_m, tau_m, rchi_m = [], [], []
for k in range(NMOCK):
    Vm = []
    for i, g in enumerate(gals):
        lo, hi = C._bounds(g)
        p_true = np.clip(rng.normal(0, 1, 4), lo + 1e-6, hi - 1e-6)
        if g["eInc"] <= 0:
            p_true[3] = 0.0
        a0 = 10 ** L0 * (1.0 if D_inj is None else (1.0 + float(D_inj @ g["n"])))
        Vt = C.model_velocity(g, p_true, a0, "nu_mono")
        Vm.append(Vt + rng.normal(0, 1, len(Vt)) * math.sqrt(cv.s[i]) * g["eV"])
    chi, _ = C.compute_profiles(gals, "nu_mono", GRID2, V_override=Vm)
    cm = C.Curves(GRID2, chi, npt, birge=True)
    r = C.fit_template(cm, n, starts=ST7)
    A_m.append(float(np.linalg.norm(r["theta"])))
    t, rc = tau_ml(cm)
    tau_m.append(t)
    rchi_m.append(rc)
    if (k + 1) % 20 == 0:
        P(f"    {k + 1} mocks {R.el()}: A_hat median so far {np.median(A_m):.3f}")
A_m = np.array(A_m)
pG2 = (1 + np.sum(A_m >= A_real)) / (1 + NMOCK)
P(f"  mock A_hat: median {np.median(A_m):.3f}, 84% {np.percentile(A_m, 84):.3f}, 95% {np.percentile(A_m, 95):.3f}, max "
  f"{A_m.max():.3f}; real A_hat = {A_real:.3f} -> p = {pG2:.3f} (resolution 0.01)")
P(f"  mocks: galaxy-level reduced chi2 median {np.median(rchi_m):.2f} (real {rchi_real:.2f}); tau median {np.median(tau_m):.3f} "
  f"(real {tau_real:.3f})")
R.num("mocks", {"N": NMOCK, "A_real_0p02grid": A_real, "A_mock_p50_p84_p95_max": [np.median(A_m), np.percentile(A_m, 84),
                np.percentile(A_m, 95), A_m.max()], "p": pG2, "rchi_mock_median": np.median(rchi_m), "rchi_real": rchi_real,
                "tau_mock_median": np.median(tau_m), "tau_real": tau_real, "A_mock": A_m})
check("G1 the error model alone reproduces the real galaxy-to-galaxy scatter of a0 (mock reduced chi2 within 30% of real)",
      f"mock {np.median(rchi_m):.2f} vs real {rchi_real:.2f}", abs(np.median(rchi_m) / rchi_real - 1) < 0.3, load_bearing=False,
      reading="if this fails the Gaussian null is narrower than the data's own scatter, so its p is anti-conservative and the "
              "permutation null (which keeps the real scatter) is the right one")
if C.MUTATE:
    zb = os.path.join(C.HERE, "cfg182_c_gaussnull_results.json")
    import json
    base = json.load(open(zb))["numbers"]["mocks"]["A_mock_p50_p84_p95_max"][0] if os.path.exists(zb) else float("nan")
    check("GM the injected dipole moves the mock A_hat distribution up (median above the no-dipole mocks' median)",
          f"MUTATE median {np.median(A_m):.3f} vs no-dipole median {base:.3f}", np.median(A_m) > base)
sys.exit(R.finish())
