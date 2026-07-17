#!/usr/bin/env python3
"""
fire_occam.py -- E3 FIRED: the Occam/Bayes evidence ratio, M0 (a0 == cH_Lambda/Z, ZERO
free parameters) vs M1 (a0 free, one parameter, honest prior), on the gas-dominated
SPARC a0-line slope. Both footings. Prior-sensitivity table.
==========================================================================================
Closed form (sympy-derived and quadrature-verified in bayes_setup.py Part 1):

    B01 = [ W / (sqrt(2 pi) s) ] * exp(-t^2/2),   t = (ln a0* - ln a0_hat)/sqrt(s^2+s0^2)
           '---- Occam factor ----'  '- fit penalty -'

with W = prior log-width, s = total fractional slope error, s0 = Planck anchor width.
This script recomputes it by NUMERIC QUADRATURE (no closed-form shortcut, no hard-coded
check values) from fire_slope_results.json.

WHAT THIS IS: a FORMALIZATION of predicted-not-fitted -- no new data. HONESTY RAILS:
the likelihood width is the SYSTEMATICS-inflated sigma_tot (incl. estimator-choice
spread); the median-estimator and full-sample variants are scored as sensitivity rows;
the M0canon-vs-M0alt likelihood ratio is reported and (spoiler) does NOT decide the
footing fork; Jeffreys-scale language only, 'decisive' banned unless >2 bans, 'proof'
banned always. Exit 0 != verdict.
"""
import numpy as np, os, json
from fire_common import A0C, A0A, SC, SA, HERE

bar = "=" * 94
res = json.load(open(os.path.join(HERE, "fire_slope_results.json")))
bg, bf = res["budget_gas"], res["budget_full"]


def logB(xhat, s_meas, astar, s_anchor_frac, lo, hi, linear=False):
    """log10 evidence ratio M0/M1 by numeric quadrature."""
    xg = np.linspace(np.log(lo), np.log(hi), 200001)
    s_eff = np.hypot(s_meas, s_anchor_frac)
    lnZ0 = -0.5 * ((np.log(astar) - xhat) / s_eff) ** 2 - np.log(np.sqrt(2 * np.pi) * s_eff)
    Lx = np.exp(-0.5 * ((xg - xhat) / s_meas) ** 2) / (np.sqrt(2 * np.pi) * s_meas)
    if linear:
        prior = np.exp(xg) / (hi - lo)
    else:
        prior = np.full_like(xg, 1.0 / (np.log(hi) - np.log(lo)))
    lnZ1 = np.log(np.trapz(Lx * prior, xg))
    return (lnZ0 - lnZ1) / np.log(10.0), (np.log(astar) - xhat) / s_eff


cases = [
    ("GAS GLS (primary)", bg["a0hat"], bg["tot"] / bg["a0hat"]),
    ("GAS median (variant)", bg["a0med"], bg["tot"] / bg["a0hat"]),
    ("FULL GLS (cross-check)", bf["a0hat"], bf["tot"] / bf["a0hat"]),
]
priors = [
    ("log-flat [1e-11,1e-9]  (default, 2 dec)", 1e-11, 1e-9, False),
    ("log-flat [1e-12,1e-8]  (4 dec)", 1e-12, 1e-8, False),
    ("log-flat [3e-11,3e-10] (1 dec)", 3e-11, 3e-10, False),
    ("linear-flat [1e-11,1e-9]", 1e-11, 1e-9, True),
]

print(bar)
print("E3 -- OCCAM/BAYES: M0 {a0 == cH_Lambda/Z, 0 params} vs M1 {a0 free, 1 param}")
print(bar)
print("  M0 carries the Planck anchor width (+/-1%); likelihood = the slope measurement,")
print("  Gaussian in ln a0 with the FULL systematics-inflated fractional error.")
print(f"\n  {'case':<24} {'a0_hat':>10} {'s_ln':>6} | {'prior':<40} "
      f"{'B(canon)':>9} {'B(ALT)':>8}   [bans, + = M0]")
summary, sens_c, sens_a = {}, [], []
for label, ah, sm in cases:
    xh = np.log(ah)
    for pl, lo, hi, lin in priors:
        bC, tC = logB(xh, sm, A0C, SC / A0C, lo, hi, lin)
        bA, tA = logB(xh, sm, A0A, SA / A0A, lo, hi, lin)
        star = ""
        if label.startswith("GAS GLS") and pl.startswith("log-flat [1e-11,1e-9]"):
            star = " <-- HEADLINE"
            summary = dict(bans_canon=float(bC), bans_alt=float(bA),
                           t_canon=float(tC), t_alt=float(tA))
        if label.startswith("GAS"):
            sens_c.append(bC); sens_a.append(bA)
        print(f"  {label:<24} {ah:>10.3e} {sm:>6.3f} | {pl:<40} {bC:>+9.2f} {bA:>+8.2f}{star}")
    print()

print(f"  HEADLINE: B01 = {summary['bans_canon']:+.2f} bans (canonical) / "
      f"{summary['bans_alt']:+.2f} bans (ALT footing)")
print(f"  fit tensions inside B01: t(canon) = {summary['t_canon']:+.2f} sigma, "
      f"t(ALT) = {summary['t_alt']:+.2f} sigma")
print(f"  prior/estimator sensitivity envelope (gas rows): canonical "
      f"[{min(sens_c):+.2f}, {max(sens_c):+.2f}] bans, ALT [{min(sens_a):+.2f}, {max(sens_a):+.2f}] bans")
dfoot = (summary["t_canon"] ** 2 - summary["t_alt"] ** 2) / 2 / np.log(10.0)
print(f"\n  footing fork (pure likelihood ratio M0canon vs M0alt): {dfoot:+.2f} bans toward")
print("  ALT -- UNDER 1 ban: NOT decided by SPARC, consistent with the banked 21%-apart")
print("  non-diagnosticity. Do not cite either footing as 'selected by the data'.")


def jeffreys(b):
    b = abs(b)
    return ("barely worth mentioning" if b < 0.5 else
            "substantial" if b < 1.0 else
            "strong" if b < 1.5 else
            "very strong" if b < 2.0 else "decisive")


print(f"\n  Jeffreys reading: canonical '{jeffreys(summary['bans_canon'])}', "
      f"ALT '{jeffreys(summary['bans_alt'])}' -- positive but MODEST; the Occam factor")
print("  is capped by the honest 16% systematics error.")
print("\n  ERROR-REDUCTION LEVER (forecast, NOT a result; cuts BOTH ways). x2/x3 smaller")
print("  error (e.g. TRGB distances for the gas dwarfs):")
print("    - if the central value STAYS at the GLS 1.181e-10:")
for red in (2.0, 3.0):
    sm = (bg["tot"] / bg["a0hat"]) / red
    bC, _ = logB(np.log(bg["a0hat"]), sm, A0C, SC / A0C, 1e-11, 1e-9)
    bA, _ = logB(np.log(bg["a0hat"]), sm, A0A, SA / A0A, 1e-11, 1e-9)
    print(f"        error /{red:.0f}: B01 = {bC:+.2f} bans (canon) / {bA:+.2f} bans (ALT)")
print("      i.e. the canonical footing would be DISFAVORED (its -1.45 sigma tension")
print("      sharpens faster than the Occam factor grows) while ALT strengthens --")
print("      the lever is a genuine falsification risk for canonical, stated plainly.")
print("      [This CORRECTS the loose bayes_setup.py line 'the same agreement would be")
print("       worth ~+1.5-2 bans': true only if the central value also moves.]")
print("    - if the central value moved ONTO each footing's prediction:")
for red in (2.0, 3.0):
    sm = (bg["tot"] / bg["a0hat"]) / red
    bC, _ = logB(np.log(A0C), sm, A0C, SC / A0C, 1e-11, 1e-9)
    bA, _ = logB(np.log(A0A), sm, A0A, SA / A0A, 1e-11, 1e-9)
    print(f"        error /{red:.0f}: B01 = {bC:+.2f} bans (canon@canon) / {bA:+.2f} bans (ALT@ALT)")
print("\n  WHAT THIS ADDS: nothing observational -- it formalizes that M0's a0 was")
print("  PREDICTED from (c, H_Lambda, Z) before the fit, so the zero-parameter model is")
print("  rewarded for landing within ~1.5 sigma of a value it never saw. The bans are")
print("  real model-comparison currency, but they are a REFRAMING of the banked")
print("  coincidence, not new data. No 'proof'.")

json.dump(dict(headline=summary,
               sensitivity_canon=[float(min(sens_c)), float(max(sens_c))],
               sensitivity_alt=[float(min(sens_a)), float(max(sens_a))],
               footing_bans_toward_alt=float(dfoot)),
          open(os.path.join(HERE, "fire_occam_results.json"), "w"), indent=1)
print("\n[fire_occam_results.json written]")
print("EXIT 0: evidence computed. Exit code is not a verdict.")
