#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
L317 -- THE REGISTERED tSZ TEST SCORED UNDER ITS ORIGINAL RULES, on the published Planck-SZ pressure of the
same 12 X-COP clusters.

THE REGISTRATION (deepseek_push/G129_tsz_proposal.py + TSZ_PROPOSAL.md sec. 5, commit fe4ea03a3, 2026-09-16
00:30 -0400).  Statistic: the log-slope of the Compton-y profile over theta in [theta_500, 2 theta_500].
    PASS  sample-median slope in (-1.7, -0.9)          (G113 V2a: phantom zone isothermal at T_inf = 2 T_floor,
                                                         so y ~ b^-(q-1) with the gas envelope q in (2.0, 2.5))
    F1    slope steeper than -2.0 at >= 3 sigma          (kills the G095 virial-T extension outside R500)
  Nine hours later (G177, commit 1af573473, 02:52) the pass window was REWRITTEN to (-2.94, -2.14) before any map
  was read, putting the old kill line inside the new pass band (PAPER30 sec. 4.9; the CLOSURE_MAP rule: score the
  ORIGINAL rules).  Both are scored here; only the original is the registered test.

THE DATA (published, not re-derived here): Ghirardini et al. 2019, A&A 621, A41 (arXiv:1805.00042) -- XMM + Planck
  SZ (MILCA) pressure of the X-COP sample out to ~2.5 R500.  Read from the paper's own tables:
    Table 3 GNFW "ALL":  P0 = 5.68 +/- 1.77, c500 = 1.49 +/- 0.30, gamma = 0.43 +/- 0.10, alpha = 1.33 (fixed),
                         beta = 4.40 +/- 0.41
    Table 2 piecewise:   pressure slope B = -3.21 +/- 0.40 over x in [1.29, 2.65];
                         temperature slope B = -0.31 +/- 0.11 over x in [0.88, 1.90]
  Cross-checks (standard literature GNFW, not X-COP): Arnaud et al. 2010 (P0 8.403, c500 1.177, gamma 0.3081,
  alpha 1.0510, beta 5.4905); Planck 2013 Int. V (P0 6.41, c500 1.81, gamma 0.31, alpha 1.33, beta 4.13).
  HONEST CAVEAT: these data were PUBLIC (2019) before the window was registered (2026), so this is a
  confrontation with pre-existing data, not a blind outcome.

  S1 the projected Compton slope of the X-COP GNFW over [R500, 2 R500] (two area-averaged annuli, line of sight
     to 5 R500 and to infinity), Monte-Carlo over the published parameter errors (independent sampling -- wider
     than the true posterior, i.e. conservative for any exclusion).
  S2 the model-independent route: the piecewise 3D pressure slope projects to y ~ b^(B+1).
  S3 the temperature channel: the phantom-zone isotherm predicts d ln T/d ln r = 0 beyond R500.
  S4 THE SCORE under the original rules, and under the rewritten ones.
  MUTATE=1 replaces the measured pressure by the framework's own phantom-zone prediction (P ~ rho_gas ~ r^-2.25,
     isothermal): the "original window is missed" finding must then FAIL (rc = 1).

Run from the repository root:  python3 real_research/tsz_score_2026/L317_tsz_original_window_score.py
"""
import os, sys, json, math
import numpy as np
from scipy.integrate import quad

HERE = os.path.dirname(os.path.abspath(__file__))
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "L317_tsz_original_window_score"
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "L317", "mutate": MUTATE, "checks": {}, "numbers": {}}
ORIG = (-1.7, -0.9)
F1_LINE = -2.0
REWRITTEN = (-2.94, -2.14)


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok)
    CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    P(f"         measured: {measured}")
    if reading:
        P(f"         reading:  {reading}")
    return ok


def banner(t):
    P("\n" + "=" * 104); P(t); P("=" * 104)


P(__doc__)


def gnfw(x, c500, gamma, alpha, beta):
    cx = c500 * x
    return 1.0 / (cx**gamma * (1 + cx**alpha)**((beta - gamma) / alpha))


def pressure(x, pars):
    if MUTATE:
        return x**-2.25                      # the framework's phantom-zone isotherm x gas envelope (q = 2.25)
    return gnfw(x, *pars)


def y_of_b(b, pars, lmax):
    f = lambda l: pressure(math.sqrt(b * b + l * l), pars)
    val, _ = quad(f, 0, lmax, limit=400, epsrel=1e-8)
    return 2 * val


def annulus_mean(b1, b2, pars, lmax, n=24):
    bs = np.linspace(b1, b2, n)
    ys = np.array([y_of_b(b, pars, lmax) for b in bs])
    return np.trapz(ys * bs, bs) / np.trapz(bs, bs)


def two_bin_slope(pars, lmax):
    y1 = annulus_mean(1.0, 1.5, pars, lmax); y2 = annulus_mean(1.5, 2.0, pars, lmax)
    return math.log(y2 / y1) / math.log(math.sqrt(1.5 * 2.0) / math.sqrt(1.0 * 1.5))


XCOP = (1.49, 0.43, 1.33, 4.40)
XCOP_ERR = (0.30, 0.10, 0.0, 0.41)
LIT = {"Arnaud+2010": (1.177, 0.3081, 1.0510, 5.4905), "Planck 2013 Int.V": (1.81, 0.31, 1.33, 4.13)}

# ============================================================================================ S1
banner("S1  THE PROJECTED COMPTON SLOPE OF THE MEASURED X-COP PRESSURE, [R500, 2 R500]")
s_best = {L: two_bin_slope(XCOP, L) for L in (5.0, 50.0)}
P(f"    X-COP GNFW best fit: 2-bin slope = {s_best[5.0]:+.3f} (LOS to 5 R500), {s_best[50.0]:+.3f} (LOS to 50 R500)")
for nm, pr in LIT.items():
    P(f"    {nm:18s}: 2-bin slope = {two_bin_slope(pr, 5.0):+.3f}")
rng = np.random.default_rng(17)
mc = []
for _ in range(600 if not MUTATE else 20):
    c = rng.normal(XCOP[0], XCOP_ERR[0]); g = rng.normal(XCOP[1], XCOP_ERR[1]); bta = rng.normal(XCOP[3], XCOP_ERR[3])
    if not (0 < c < 5 and 0 <= g < 0.8 and 2 < bta < 8):
        continue
    mc.append(two_bin_slope((c, g, 1.33, bta), 5.0))
mc = np.array(mc)
med, lo, hi = float(np.median(mc)), float(np.percentile(mc, 16)), float(np.percentile(mc, 84))
sig = 0.5 * (hi - lo)
OUT["numbers"]["S1"] = dict(best_L5=s_best[5.0], best_L50=s_best[50.0], mc_median=med, mc_16=lo, mc_84=hi,
                            lit={k: two_bin_slope(v, 5.0) for k, v in LIT.items()})
P(f"    Monte Carlo over the published errors: median {med:+.3f}, 16-84% [{lo:+.3f}, {hi:+.3f}] (N = {len(mc)})")
check("S1 the measured X-COP pressure projects to a Compton slope over [theta_500, 2 theta_500] that lies OUTSIDE "
      "the original pass window (-1.7, -0.9)",
      f"{med:+.3f} (+{hi-med:.3f}/-{med-lo:.3f}); best fit {s_best[5.0]:+.3f}; literature {', '.join(f'{k} {v:+.2f}' for k, v in OUT['numbers']['S1']['lit'].items())}",
      hi < ORIG[0], "the outer pressure falls as the ordinary universal profile does, not as the phantom-zone isotherm")

# ============================================================================================ S2
banner("S2  MODEL-INDEPENDENT ROUTE: the piecewise 3D pressure slope over [1.29, 2.65] R500")
B, eB = (-2.25, 0.0) if MUTATE else (-3.21, 0.40)
ys, eys = B + 1, eB
z_orig = (ORIG[0] - ys) / eys if eys > 0 else float("inf")
OUT["numbers"]["S2"] = dict(pressure_slope=B, err=eB, y_slope=ys, sigma_below_window=z_orig)
check("S2 the piecewise pressure slope %.2f +/- %.2f projects to y ~ b^(%.2f +/- %.2f): below the original window's "
      "steep edge by %.1f sigma" % (B, eB, ys, eys, z_orig),
      f"y-slope {ys:+.2f} +/- {eys:.2f}", ys < ORIG[0],
      "a pure power law projects exactly as B + 1; the piecewise fit is independent of the GNFW form", load_bearing=False)

# ============================================================================================ S3
banner("S3  THE TEMPERATURE CHANNEL: the phantom zone is predicted ISOTHERMAL beyond R500")
bT, ebT = (0.0, 0.11) if MUTATE else (-0.31, 0.11)
zT = abs(bT) / ebT
OUT["numbers"]["S3"] = dict(T_slope=bT, err=ebT, z_vs_isotherm=zT)
check("S3 measured d ln T/d ln r = %.2f +/- %.2f over [0.88, 1.90] R500 vs the registered isotherm (0): %.1f sigma"
      % (bT, ebT, zT), f"{zT:.1f} sigma", zT > 2,
      "the gas cools outward where the framework's T_inf = 2 T_floor reading holds it flat", load_bearing=False)

# ============================================================================================ S4
banner("S4  THE SCORE -- original rules (the registered test) and the rewritten rules (recorded only)")
in_orig = ORIG[0] < med < ORIG[1]
f1_sig = (F1_LINE - med) / sig
in_rew = REWRITTEN[0] < med < REWRITTEN[1]
z_window = (ORIG[0] - med) / sig
OUT["numbers"]["S4_sigma_outside_pass_window"] = z_window
verdict = ("PASS" if in_orig else ("KILLED (F1 at >= 3 sigma)" if f1_sig >= 3 else "NOT PASSED; F1 not fired at 3 sigma"))
OUT["numbers"]["S4"] = dict(original=verdict, f1_sigma=f1_sig, rewritten_contains=in_rew)
P(f"    ORIGINAL: median {med:+.3f} vs pass window {ORIG}: {'inside' if in_orig else 'OUTSIDE'}; "
  f"F1 (steeper than -2.0): {f1_sig:.1f} sigma -> {verdict}")
P(f"    REWRITTEN (post hoc, not the registered test): window {REWRITTEN}: {'inside' if in_rew else 'outside'}")
check("S4 UNDER THE ORIGINAL RULES the registered tSZ prediction is NOT passed; the measured slope sits beyond the "
      "F1 line (steeper than -2.0), at %.1f sigma" % f1_sig,
      verdict, (not in_orig) and med < F1_LINE,
      "the rewritten window contains the data because it IS the ordinary universal-pressure-profile band")

# ============================================================================================ verdict
banner("VERDICT")
P(f"""  Scored under its ORIGINAL registered rules on the published Planck-SZ pressure of the same 12 clusters, the
  framework's tSZ prediction (a flat outer Compton profile from the isothermal phantom zone, slope in (-1.7, -0.9))
  is NOT PASSED: the measured slope is {med:+.2f} (+{hi-med:.2f}/-{med-lo:.2f}), {z_window:.1f} sigma outside the pass window and steeper than the F1 line -2.0 at
  {f1_sig:.1f} sigma (F1 required 3 sigma to KILL, so the registered outcome is 'not passed, not formally killed').
  The temperature falls outward ({bT:+.2f} +/- {ebT:.2f}) where the prediction holds it flat ({zT:.1f} sigma).
  The post-hoc window (-2.94, -2.14) contains the data because it is the ordinary universal profile -- it tests
  nothing the framework adds. Caveat: the data predate the registration; a blind map-level score (ACT DR6 / Planck
  y-maps, the Z06 pipeline) would upgrade this from a confrontation to a registered outcome.""")

n_fail = sum(1 for _, ok, lb in CH if lb and not ok)
OUT["n_checks"], OUT["n_fail_load_bearing"] = len(CH), n_fail
outname = f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json"
json.dump(OUT, open(os.path.join(HERE, outname), "w"), indent=1, default=str)
P(f"\n  {len(CH) - n_fail}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {outname}")
sys.exit(0 if n_fail == 0 else 1)
