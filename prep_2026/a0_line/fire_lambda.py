#!/usr/bin/env python3
"""
fire_lambda.py -- E2 FIRED: measure the a0-line slope in gas-rich dwarfs, PREDICT the
cosmological constant, compare Planck.
==========================================================================================
The framework's scale is a0 = c^2 sqrt(Lambda/3)/Z (canonical footing). Inverting
(sympy-verified in bayes_setup.py Part 3):

        Lambda = 3 Z^2 a0^2 / c^4 ,   Z = sqrt(32 pi/3) = 5.78881.

So the gas-dominated SPARC slope a0_hat is a MEASUREMENT of Lambda from galaxy rotation
curves. This script reads fire_slope_results.json (recomputable from raw data by
fire_slope.py), propagates the honest systematics-inflated error band, and compares to
Planck. Both footings: the ALT footing (rho_total/cH0) has its own inversion constant
Lambda_alt-equivalent shown as the a0-space comparison (the Lambda inversion is DEFINED
on the canonical footing; ALT ties a0 to H0 and rho_total, i.e. to Lambda only through
Omega_L -- stated, not blurred).

HONESTY RAILS: sigma_lnLambda = 2*sigma_ln(a0) -- the error DOUBLES in log space; the
result is the banked a0 ~ cH/Z coincidence REFRAMED as an inversion (same information
content, sharper falsification target), NOT new cosmological data. Exit 0 != verdict.
"""
import numpy as np, os, json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from fire_common import ZVAL, HL, CLIGHT, A0C, SC, HERE

bar = "=" * 94
res = json.load(open(os.path.join(HERE, "fire_slope_results.json")))
bg = res["budget_gas"]
a0_gls, a0_med, sig = bg["a0hat"], bg["a0med"], bg["tot"]

print(bar); print("E2 -- THE LAMBDA INVERSION: Lambda = 3 Z^2 a0_hat^2 / c^4"); print(bar)
lam_planck = 3 * HL**2 / CLIGHT**2          # Planck Lambda via the banked H_Lambda anchor
s_ln_a0 = sig / a0_gls
s_ln_lam = 2 * s_ln_a0                       # exact log-space propagation of a0^2
print(f"  inputs: gas-dominated slope a0_hat(GLS) = {a0_gls:.3e} +/- {sig:.2e} "
      f"(16%, systematics-inflated),")
print(f"          median-estimator variant {a0_med:.3e}; Z = {ZVAL:.6f}; "
      f"Planck anchor H_Lambda = {HL:.4e} s^-1")
rows = {}
for lab, a0v in (("GLS  (primary)", a0_gls), ("median (variant)", a0_med)):
    lam = 3 * ZVAL**2 * a0v**2 / CLIGHT**4
    t = np.log(lam / lam_planck) / s_ln_lam
    rows[lab] = (lam, t)
    print(f"\n  {lab}:  Lambda_pred = {lam:.3e} m^-2   (Planck: {lam_planck:.3e})")
    print(f"      ratio = {lam/lam_planck:.2f};  sigma_lnLambda = {s_ln_lam:.2f} "
          f"==> {t:+.2f} sigma")
lam_gls = rows["GLS  (primary)"][0]
lo = 3 * ZVAL**2 * (a0_gls - sig) ** 2 / CLIGHT**4
hi = 3 * ZVAL**2 * (a0_gls + sig) ** 2 / CLIGHT**4
print(f"\n  honest 1-sigma band (GLS): Lambda in [{lo:.2e}, {hi:.2e}] m^-2")
print(f"  Planck {'INSIDE' if lo <= lam_planck <= hi else 'OUTSIDE'} the 1-sigma band"
      f" (GLS); median variant lands at {rows['median (variant)'][1]:+.2f} sigma.")
print("\n  READING (honest, both directions): rotation curves of gas-rich dwarfs 'predict'")
print(f"  the cosmological constant to a factor {rows['GLS  (primary)'][0]/lam_planck:.2f}"
      f" (GLS) / {rows['median (variant)'][0]/lam_planck:.2f} (median) across ~52")
print("  a-priori orders of magnitude -- within ~1.5 sigma of the honest error either")
print("  way. This is the banked a0 ~ cH_Lambda/Z coincidence REFRAMED as an inversion:")
print("  the same information content, but a sharper falsification target -- a future")
print("  gas-dwarf slope at 3e-10 (or 3e-11) would BREAK the identity outright.")
print("  ALT-footing note: on rho_total/cH0 the tie is to H0 (a0_alt = 1.131e-10, which")
print("  the GLS slope matches at +0.27 sigma); it reaches Lambda only through Omega_L,")
print("  so the clean Lambda inversion is a CANONICAL-footing statement. Both shown.")

# ------------------------------------------------------------------------------- figure
fig, ax = plt.subplots(figsize=(8.6, 5.2), dpi=160)
lg = np.log10(np.geomspace(lo * 0.5, hi * 1.6, 400))
ax.axvspan(np.log10(lo), np.log10(hi), color="#1f77b4", alpha=0.18,
           label="gas-slope 1$\\sigma$ band (GLS, systematics-inflated)")
ax.axvline(np.log10(lam_gls), c="#1f77b4", lw=2.2,
           label=f"$\\Lambda$ from gas dwarfs (GLS) = {lam_gls:.2e}")
ax.axvline(np.log10(rows["median (variant)"][0]), c="#1f77b4", lw=1.6, ls="--",
           label=f"median-estimator variant = {rows['median (variant)'][0]:.2e}")
ax.axvline(np.log10(lam_planck), c="#d62728", lw=2.4, ls="-.",
           label=f"Planck $\\Lambda$ = {lam_planck:.2e} m$^{{-2}}$")
ax.set_xlabel(r"$\log_{10}\ \Lambda\ \ [{\rm m}^{-2}]$")
ax.set_yticks([])
ax.set_title("E2: the $\\Lambda$ inversion  $\\Lambda = 3Z^2\\hat a_0^2/c^4$ from the\n"
             "gas-dominated SPARC $a_0$-line slope, vs Planck "
             f"(GLS: {rows['GLS  (primary)'][1]:+.2f}$\\sigma$, "
             f"median: {rows['median (variant)'][1]:+.2f}$\\sigma$)")
ax.legend(fontsize=8.5, loc="upper left")
ax.grid(alpha=0.25, axis="x")
txt = ("a-priori range for a 'random' vacuum energy:\n"
       r"$\sim$52 orders of magnitude; the gas slope lands within a factor "
       f"{lam_gls/lam_planck:.1f}")
ax.text(0.985, 0.04, txt, transform=ax.transAxes, ha="right", fontsize=8,
        bbox=dict(fc="#fffbe6", ec="#d4b106", alpha=0.9))
fig.tight_layout()
fp = os.path.join(HERE, "fire_lambda_fig.png")
fig.savefig(fp)
print(f"\n[figure written: {fp}]")

json.dump(dict(lam_pred_gls=float(lam_gls), lam_pred_med=float(rows["median (variant)"][0]),
               lam_planck=float(lam_planck), band=[float(lo), float(hi)],
               t_gls=float(rows["GLS  (primary)"][1]),
               t_med=float(rows["median (variant)"][1]), sig_ln_lam=float(s_ln_lam)),
          open(os.path.join(HERE, "fire_lambda_results.json"), "w"), indent=1)
print("[fire_lambda_results.json written]")
print("EXIT 0: inversion computed. Exit code is not a verdict.")
