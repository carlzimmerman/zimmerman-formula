#!/usr/bin/env python3
r"""LANE 5 -- the CLUSTER eta(R500) missing-mass ratio RE-SOLVED under Route A's exponential kernel.

WHAT THIS FILE IS.  Route A replaced the framework's POWER-LAW approach to Newton with an EXPONENTIAL one
(nu = 1/(1 - e^-sqrt(y))).  The cluster front is kernel-dependent, so the committed eta(R500) standing has to
be re-solved rather than rescaled.  This file does that on the same data, the same sample cuts and the same
estimator as the committed audit, so the two numbers are comparable by construction.

  ANCHOR (single source of truth for the data + sample):  real_research/reviews/clusters_eta_audit.py
  KERNEL (single source of truth for Route A):            real_research/reviews/mi_route_a_kernel.py
  Neither is modified.  The anchor's loader is exec'd up to its first banner, exactly as
  real_research/reviews/mi_aqual_alt_footing_rerun_2026.py does for the AQUAL solver.

THE COMMITTED STANDING BEING RE-SOLVED (clusters_eta_audit.out, corrected 2026-07-30):
  eta(R500) = 2.334 median / 2.542 geomean on the alpha=1 kernel nu = sqrt(1 + 1/y), canonical a0;
  +0.4052 dex; floor-limited 4.05 / 2.70 / 2.03 sigma against a 0.10 / 0.15 / 0.20 dex floor.
  The framework's IN-FORCE kernel immediately before Route A was alpha=2, not alpha=1, so the number Route A
  actually supersedes is the alpha=2 one, and it is computed here too.  Both are carried.

*** THE HEADLINE, AND IT CONTRADICTS THE EXPECTATION THIS LANE WAS HANDED. ***
The lane was set up on the premise that "the exponential kernel is WEAKER than a power law at intermediate
accelerations, which plausibly makes the cluster deficit WORSE."  That premise is FALSE, and the script proves
it as a check rather than asserting it.  Expand both kernels in u = sqrt(y) at small y:

      nu_exp(y) = 1/u + 1/2 + u/12 + ...            nu_alpha1(y) = 1/u + u/2 + ...

The exponential's subleading term is a CONSTANT 1/2; the power law's is O(u).  So deep in the MOND regime the
exponential is the STRONGER kernel, and it stays stronger until y ~ 8.52 (vs alpha=1) / y ~ 10^2 (vs alpha=2).
It is weaker ONLY on the NEWTONIAN side -- which is precisely the property that bought the solar system.
Clusters at R500 sit at y ~ 0.037, i.e. two and a half decades DEEP of the crossover.  Route A therefore
HELPS clusters.  Not by much, and nowhere near enough, but the sign of the effect is favourable and reporting
it as a cost of Route A would be manufacturing a deficit.

WHAT IT DOES NOT DO, by a bounded-ratio argument that is exact rather than asymptotic.  eta is inversely
proportional to nu at fixed data, so pointwise

      eta_RouteA(y) / eta_alpha(y) = nu_alpha(y) / nu_exp(y)

and the reduction Route A can supply is therefore capped by max_y nu_exp/nu_alpha over ALL of acceleration
space -- 1.245x against alpha=2, 1.140x against alpha=1.  Closing eta needs 2.36x.  So no choice of cluster
radius, mass or footing lets Route A close this front: the ceiling is ~1.9x short of what closure requires.
That is a statement about the kernel FAMILY's shape, not about one radius.

BOTH a0 FOOTINGS on every dimensional number, as required:
  canonical  A0_CANON = 9.3614e-11 m/s^2  (rho_DE, c H_Lambda / Z, kappa = 1/2)
  alternative A0_ALT  = 1.1300e-10 m/s^2  (rho_total, c H_0 / Z)
a0 is an INPUT throughout.  The one place an a0 multiplier is solved for (section 6) is a REQUIREMENT
calculation -- "what would it take" -- explicitly labelled, and it is not adopted anywhere.

Checks are structural or falsifiable comparisons.  None of them encodes a verdict, several of them run
AGAINST the framework's interest (C9, C11, C13), and the file exits non-zero if any fails.

Data: eRASS1 primary cluster catalogue v3.2 (Bulbul et al. 2024), N = 9830 after the anchor's cuts.
"""
from __future__ import annotations

import pathlib
import sys

import numpy as np
from scipy.optimize import brentq

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parent.parent
sys.path.insert(0, str(HERE))

from mi_route_a_kernel import (  # noqa: E402  -- the ONE definition of Route A's kernel
    A0_ALT,
    A0_CANON,
    mu,
    nu,
    nu_alpha1,
    nu_alpha2,
)

# ----------------------------------------------------------------------------------------------------------
# reuse the committed audit's loader verbatim, so the sample is identical by construction
# ----------------------------------------------------------------------------------------------------------
ANCHOR = REPO / "real_research/reviews/clusters_eta_audit.py"
_src = ANCHOR.read_text()
_G = {"__name__": "anchor"}
exec(compile(_src[: _src.index("# ====")], str(ANCHOR), "exec"), _G)  # noqa: S102
load = _G["load"]
A0_ALT_ANCHOR = _G["A0_ALT"]          # the anchor COMPUTES c H0 / Z = 1.1311e-10; the module hard-codes 1.13e-10

FOOTINGS = (("canonical rho_DE  (cH_Lambda/Z)", A0_CANON), ("alt rho_total     (cH_0/Z)", A0_ALT))
KERNELS = (("Route A  exp", nu), ("alpha=2 (superseded)", nu_alpha2), ("alpha=1 (committed row)", nu_alpha1))

A0_MOND = 1.20e-10                    # McGaugh+2016 galaxy g_dagger -- the denominator of the published "17x"
G_DDAG, G_DDAG_ERR = 2.02e-9, 0.11e-9  # Tian+2020 ApJ 896 70, 20 CLASH clusters, 100-600 kpc, slope fixed 1/2

# committed standing, for the side-by-side (clusters_eta_audit.out, 2026-07-30)
COMMITTED = dict(med_a1=2.334, gm_a1=2.542, dex_a1=0.4052, ratio_lens=21.58, ladder_lo=3.88, ladder_hi=23.50)

_FAILS: list[str] = []
_RUN: list[str] = []


def chk(label, condition, detail=""):
    ok = bool(condition)
    _RUN.append(label)
    print("   [%s] %s%s" % ("OK" if ok else "FAIL", label, ("  -- " + detail) if detail else ""))
    if not ok:
        _FAILS.append(label)
    return ok


# ----------------------------------------------------------------------------------------------------------
def eta_of(b, a0, kern):
    """eta = M_dyn / M_pred = g_obs / (nu(y) g_bar).  Spherical, so the MI and AQUAL readings coincide (C3)."""
    return b["gobs"] / (kern(b["gbar"] / a0) * b["gbar"])


def stats(e):
    le = np.log10(e)
    return dict(med=float(np.median(e)), gm=float(10 ** le.mean()), q=np.percentile(e, [25, 75]),
                dex=float(le.mean()), sd=float(le.std()), N=le.size)


def boost(kern, y):
    """B(y) = nu(y)^2 y = g_dagger_eff / a0 -- the acceleration scale a slope-1/2 fit recovers from the kernel."""
    y = np.asarray(y, float)
    return kern(y) ** 2 * y


FLOORS = (0.10, 0.15, 0.20, 0.30)     # this corpus's OWN floor range (cluster_rar_throttle_2026/lane2_data.py)


# ==========================================================================================================
def main():
    W = 106
    print("=" * W)
    print("LANE 5 -- CLUSTER eta(R500) RE-SOLVED UNDER ROUTE A (exponential kernel), eRASS1 Bulbul+2024")
    print("  canonical a0 = %.4e   alt a0 = %.4e   spread %.4fx = %.4f dex"
          % (A0_CANON, A0_ALT, A0_ALT / A0_CANON, np.log10(A0_ALT / A0_CANON)))
    print("  Route A kernel: nu(y) = 1/(1 - e^-sqrt(y)).  Superseded: alpha=2.  Committed row: alpha=1.")
    print("=" * W)

    try:
        base = load(fstar=0.20)
    except Exception as exc:                                                          # pragma: no cover
        print("\nFATAL: cannot read the eRASS1 catalogue via the anchor loader: %r" % exc)
        print("No eta number can be quoted without it.  NOT fabricating output.")
        sys.exit(2)

    print("\nSample (anchor's cuts verbatim: 0<z<1, M500>0, Mgas>0, 0.01<fgas<0.30, fstar=0.20): N = %d"
          % base["N"])
    yq = {}
    for lab, a0 in FOOTINGS:
        y = base["gbar"] / a0
        yq[lab] = np.percentile(y, [5, 25, 50, 75, 95])
        print("  %-34s y=g_bar/a0  median %.5f   5-95%%: %.5f - %.5f"
              % (lab, np.median(y), yq[lab][0], yq[lab][-1]))

    # ------------------------------------------------------------------ 0. WHY THE PREMISE WAS BACKWARDS
    print("\n" + "-" * W)
    print("0. WHERE THE EXPONENTIAL IS STRONGER AND WHERE IT IS WEAKER -- the sign of Route A's cluster effect")
    print("-" * W)
    print("  nu_exp = 1/u + 1/2 + u/12 + ...   vs   nu_a1 = 1/u + u/2 + ...   (u = sqrt(y)).  The exponential's")
    print("  subleading term is a CONSTANT, the power law's vanishes with u, so DEEP the exponential is STRONGER.")
    print("  %-12s %12s %12s %12s %10s %10s" % ("y", "nu_exp", "nu_a1", "nu_a2", "exp/a1", "exp/a2"))
    for y in (1e-3, 1e-2, 0.037, 0.1, 0.3, 1.0, 3.0, 8.52, 30.0, 1e3):
        print("  %-12.4g %12.6f %12.6f %12.6f %10.5f %10.5f"
              % (y, nu(y), nu_alpha1(y), nu_alpha2(y), nu(y) / nu_alpha1(y), nu(y) / nu_alpha2(y)))
    yg = np.logspace(-8, 4, 400001)
    r1, r2 = nu(yg) / nu_alpha1(yg), nu(yg) / nu_alpha2(yg)
    above = yg[r1 > 1.0]
    y_cross = float(above.max())
    ceil1, ceil2 = float(r1.max()), float(r2.max())
    y_ceil1, y_ceil2 = float(yg[r1.argmax()]), float(yg[r2.argmax()])
    print("\n  CROSSOVER exp = alpha=1 at y = %.3f.  Below it the exponential is stronger, above it weaker." % y_cross)
    print("  The clusters sit at y ~ %.4f (95th pct %.4f) -- %.0fx DEEP of the crossover, entirely on the"
          % (np.median(base["gbar"] / A0_CANON), yq[FOOTINGS[0][0]][-1], y_cross / np.median(base["gbar"] / A0_CANON)))
    print("  stronger side.  So the property that bought the solar system costs clusters NOTHING; it pays them.")
    print("  CEILING on the help: max_y nu_exp/nu_a1 = %.5f at y = %.3f;  max_y nu_exp/nu_a2 = %.5f at y = %.3f."
          % (ceil1, y_ceil1, ceil2, y_ceil2))

    # ------------------------------------------------------------------ 1. (a) THE eta HEADLINE
    print("\n" + "-" * W)
    print("1. (a) eta(R500) UNDER ROUTE A vs THE SUPERSEDED KERNELS -- both footings")
    print("-" * W)
    S = {}
    for lab, a0 in FOOTINGS:
        print("  %s   a0 = %.4e" % (lab, a0))
        print("    %-26s %8s %8s %16s %10s %9s" % ("kernel", "median", "geomean", "[q25,q75]", "mean dex", "sd dex"))
        for kn, kf in KERNELS:
            s = stats(eta_of(base, a0, kf))
            S[(lab, kn)] = s
            print("    %-26s %8.4f %8.4f   [%.3f, %.3f] %10.5f %9.5f"
                  % (kn, s["med"], s["gm"], s["q"][0], s["q"][1], s["dex"], s["sd"]))
    can, alt = FOOTINGS[0][0], FOOTINGS[1][0]
    rA, a2, a1 = S[(can, "Route A  exp")], S[(can, "alpha=2 (superseded)")], S[(can, "alpha=1 (committed row)")]
    rA_alt, a2_alt = S[(alt, "Route A  exp")], S[(alt, "alpha=2 (superseded)")]
    print("\n  ROUTE A vs THE SUPERSEDED alpha=2 (the kernel actually in force before the switch):")
    print("    canonical  eta median %.4f -> %.4f  (%.2f%% LOWER, -%.4f dex)"
          % (a2["med"], rA["med"], 100 * (1 - rA["med"] / a2["med"]), a2["dex"] - rA["dex"]))
    print("    alt        eta median %.4f -> %.4f  (%.2f%% LOWER, -%.4f dex)"
          % (a2_alt["med"], rA_alt["med"], 100 * (1 - rA_alt["med"] / a2_alt["med"]), a2_alt["dex"] - rA_alt["dex"]))
    print("  ROUTE A vs the COMMITTED alpha=1 row (%.3f median, %.3f geomean, %+.4f dex):"
          % (COMMITTED["med_a1"], COMMITTED["gm_a1"], COMMITTED["dex_a1"]))
    print("    canonical  eta median %.4f -> %.4f  (%.2f%% LOWER)   geomean %.4f -> %.4f"
          % (a1["med"], rA["med"], 100 * (1 - rA["med"] / a1["med"]), a1["gm"], rA["gm"]))
    print("  DIRECTION: Route A makes the cluster front BETTER, not worse.  The improvement is REAL and SMALL:")
    print("    the missing-mass factor goes from %.0f%% to %.0f%% (median) / %.0f%% to %.0f%% (geomean) missing."
          % (100 * (a2["med"] - 1), 100 * (rA["med"] - 1), 100 * (a2["gm"] - 1), 100 * (rA["gm"] - 1)))
    print("    A ~2.15x residual is still a ~2.15x residual.  This is a softening, not a resolution, and no")
    print("    cluster claim in the corpus flips sign on it.")

    # ------------------------------------------------------------------ 2. SIGNIFICANCE, FULL FLOOR RANGE
    print("\n" + "-" * W)
    print("2. SIGNIFICANCE -- FLOOR-LIMITED, over this corpus's OWN full 0.10-0.30 dex floor range")
    print("-" * W)
    print("  Never the statistical sigma: eta is an ABSOLUTE-SCALE ratio and N = %d does not average down a"
          % base["N"])
    print("  common mass-calibration offset.  And never the 0.10-dex end alone -- truncating a systematic")
    print("  range at its tight end is how a 1.2 sigma becomes a 3.7 sigma.")
    sig = {}
    print("  %-34s %-24s %10s %9s | %s" % ("footing", "kernel", "mean dex", "sd dex",
                                           "  ".join("%.2f dex" % f for f in FLOORS)))
    for lab, a0 in FOOTINGS:
        for kn, kf in KERNELS:
            s = S[(lab, kn)]
            row = {f: s["dex"] / f for f in FLOORS}
            sig[(lab, kn)] = row
            print("  %-34s %-24s %10.5f %9.5f | %s"
                  % (lab, kn, s["dex"], s["sd"], "  ".join("%7.2f s" % row[f] for f in FLOORS)))
    print("\n  THE NUMBER TO QUOTE UNDER ROUTE A, canonical footing:")
    print("    %+.4f dex -> %.2f / %.2f / %.2f / %.2f sigma across the 0.10 / 0.15 / 0.20 / 0.30 dex floor range."
          % (rA["dex"], *[sig[(can, "Route A  exp")][f] for f in FLOORS]))
    print("    Alt footing: %+.4f dex -> %.2f / %.2f / %.2f / %.2f sigma."
          % (rA_alt["dex"], *[sig[(alt, "Route A  exp")][f] for f in FLOORS]))
    print("    vs the superseded alpha=2: %.2f / %.2f / %.2f / %.2f sigma (canonical)."
          % tuple(sig[(can, "alpha=2 (superseded)")][f] for f in FLOORS))
    print("    So Route A moves the tight end from %.2f to %.2f sigma and the loose end from %.2f to %.2f."
          % (sig[(can, "alpha=2 (superseded)")][0.10], sig[(can, "Route A  exp")][0.10],
             sig[(can, "alpha=2 (superseded)")][0.30], sig[(can, "Route A  exp")][0.30]))
    print("    At the loose end the offset was never a tension and still is not; at the tight end it was a")
    print("    real few-sigma offset and still is.  Route A does not change which of those is true anywhere.")
    print("  AGAINST INTEREST: the log-eta SCATTER is slightly LARGER under Route A (%.5f vs %.5f dex, +%.1f%%),"
          % (rA["sd"], a2["sd"], 100 * (rA["sd"] / a2["sd"] - 1)))
    print("    because the kernel's boost varies faster with y.  Reported as a descriptive fact only -- it is")
    print("    NOT converted into a significance here, since a relation's scatter is not its parameter error.")

    # ------------------------------------------------------------------ 3. BARYON BUDGET
    print("\n" + "-" * W)
    print("3. BARYON-BUDGET SWEEP UNDER ROUTE A -- does the softening plus a generous fstar reach eta = 1?")
    print("-" * W)
    print("  %-8s %12s %12s %12s %12s" % ("fstar", "RouteA canon", "a2 canon", "RouteA alt", "a2 alt"))
    fstar_rows = {}
    for fs in (0.0, 0.10, 0.20, 0.30, 0.50):
        b = base if abs(fs - 0.20) < 1e-12 else load(fstar=fs)
        r = [stats(eta_of(b, a0, k))["med"] for a0 in (A0_CANON, A0_ALT) for k in (nu, nu_alpha2)]
        fstar_rows[fs] = r
        print("  %-8.2f %12.4f %12.4f %12.4f %12.4f" % (fs, r[0], r[1], r[2], r[3]))
    print("  Even fstar = 0.50 -- implausibly generous -- leaves eta = %.3f (canonical) / %.3f (alt) under"
          % (fstar_rows[0.50][0], fstar_rows[0.50][2]))
    print("  Route A.  The baryon-budget escape is no more open under Route A than it was under alpha=2.")

    # ------------------------------------------------------------------ 4. (c) THE g_ddagger FRONT
    print("\n" + "-" * W)
    print("4. (c) THE CLUSTER g_ddagger UNDER ROUTE A -- and which half of it the kernel can even touch")
    print("-" * W)
    print("  Tian+2020 (ApJ 896 70; 20 CLASH clusters, 100-600 kpc, slope fixed at 1/2) measure the cluster")
    print("  acceleration scale g_ddagger = (%.2f +/- %.2f)e-9 m/s^2.  Two DIFFERENT objects get confused here:"
          % (G_DDAG * 1e9, G_DDAG_ERR * 1e9))
    print("    (i)  the MEASURED ratio g_ddagger / a0 -- pure measurement over an INPUT.  No kernel appears in")
    print("         it, so Route A leaves it EXACTLY unchanged.  This half of the front is NON-DIAGNOSTIC of")
    print("         the kernel switch, and any claim that Route A improved it would be false.")
    print("    (ii) the framework's OWN predicted effective scale g_ddagger_eff = a0 B(y), B = nu^2 y, which a")
    print("         slope-1/2 fit would recover from the kernel.  This one IS kernel-dependent and DOES move.")
    print("\n  (i) MEASURED, unchanged by Route A:")
    for lab, a0 in FOOTINGS:
        r = G_DDAG / a0
        print("    %-34s g_ddagger/a0 = %.2f (%.3f dex) +/- %.2f" % (lab, r, np.log10(r), G_DDAG_ERR / a0))
    print("    committed canonical value %.2f -> %.2f  (identical; the published 'seventeen times' is still"
          % (COMMITTED["ratio_lens"], G_DDAG / A0_CANON))
    print("    %.2f = 2.02e-9/1.20e-10, a ratio to STANDARD MOND's a0, not to the framework's)." % (G_DDAG / A0_MOND))
    print("\n  (ii) PREDICTED, and this is where Route A moves the front.  Medians over the eRASS1 sample:")
    gpred, short = {}, {}
    print("    %-34s %-24s %14s %10s %12s %12s"
          % ("footing", "kernel", "g_dd_eff pred", "/a0", "shortfall", "sqrt(shortf)"))
    for lab, a0 in FOOTINGS:
        y = base["gbar"] / a0
        for kn, kf in KERNELS:
            gp = float(np.median(kf(y) ** 2 * base["gbar"]))
            sh = G_DDAG / gp
            gpred[(lab, kn)], short[(lab, kn)] = gp, sh
            print("    %-34s %-24s %14.4e %10.4f %12.3fx %12.3fx"
                  % (lab, kn, gp, gp / a0, sh, np.sqrt(sh)))
    print("    canonical: the framework's own predicted cluster scale rises %.4f a0 -> %.4f a0, so the"
          % (gpred[(can, "alpha=2 (superseded)")] / A0_CANON, gpred[(can, "Route A  exp")] / A0_CANON))
    print("    shortfall against Tian's 2.02e-9 falls %.2fx -> %.2fx (%.1f%% better), and the deep-limit g_obs"
          % (short[(can, "alpha=2 (superseded)")], short[(can, "Route A  exp")],
             100 * (1 - short[(can, "Route A  exp")] / short[(can, "alpha=2 (superseded)")])))
    print("    shortfall %.3fx -> %.3fx.  Alt footing: %.2fx -> %.2fx."
          % (np.sqrt(short[(can, "alpha=2 (superseded)")]), np.sqrt(short[(can, "Route A  exp")]),
             short[(alt, "alpha=2 (superseded)")], short[(alt, "Route A  exp")]))
    gdreq = float(np.median(base["gobs"] ** 2 / base["gbar"]))
    print("    (the sample's OWN required scale, median g_obs^2/g_bar = %.4e = %.2f a0 canonical / %.2f alt --"
          % (gdreq, gdreq / A0_CANON, gdreq / A0_ALT))
    print("     lower than Tian's because R500 is OUTSIDE their 100-600 kpc window and the discrepancy grows")
    print("     inward; the two are not the same measurement and are not averaged together here.)")
    print("\n  AGAINST INTEREST -- Route A makes the 'convention-clean' wording WEAKER, not stronger.")
    print("  The committed audit's justification for calling the g_ddagger entry convention-clean is that a")
    print("  slope-1/2 fit's DEEP ASYMPTOTE is kernel-independent.  That is still true asymptotically, but the")
    print("  APPROACH to it is now the slowest of the three: B(y) - 1 goes as sqrt(y) under Route A, y/2 under")
    print("  alpha=2, y under alpha=1.  Over a finite window the framework's own predicted scale is therefore")
    print("  further from a0 than before:")
    print("    %-10s %14s %14s %14s" % ("y", "B_exp - 1", "B_a1 - 1", "B_a2 - 1"))
    for y in (0.01, 0.037, 0.1, 0.3, 1.0):
        print("    %-10.3f %14.5f %14.5f %14.5f"
              % (y, boost(nu, y) - 1, boost(nu_alpha1, y) - 1, boost(nu_alpha2, y) - 1))
    print("  At the CLASH-relevant y ~ 0.1-0.3 the framework now predicts %.2f-%.2f a0 rather than %.2f-%.2f a0."
          % (boost(nu, 0.1), boost(nu, 0.3), boost(nu_alpha2, 0.1), boost(nu_alpha2, 0.3)))
    print("  So the entry is less cleanly kernel-free under Route A than the committed text claims.  That cuts")
    print("  against the framework's own preferred framing of this front and is recorded as such.")

    # ------------------------------------------------------------------ 5. (b) THE LADDER
    print("\n" + "-" * W)
    print("5. (b) THE METHOD-AND-RADIUS LADDER RE-RUN -- what moves, and what provably cannot")
    print("-" * W)
    H0_KMS = 67.4
    ladder = [
        ("lensing 100-600 kpc, 20 CLASH", 2.02e-9, "Tian+2020 ApJ 896 70 (slope fixed 1/2)"),
        ("dynamics, member gals (29 HIFLUGCS) lo", 0.8e-9, "Tian+2021; own headline 'about ten times'"),
        ("dynamics, member gals (29 HIFLUGCS) hi", 2.2e-9, "Tian+2021; factor-2.8 internal band"),
        ("dynamics, 54 BCG stellar MVDR", 1.7e-9, "Tian+2024 A&A 684 A180 (+/-0.7e-9)"),
        ("X-ray HSE pooled, 52 non-cool-core", 9.5e-10, "Chan&DelPopolo 2020 (McGaugh-nu loaded)"),
        ("X-ray HSE at r_c", 1.9e-9, "Chan&DelPopolo 2020 -- grows inward"),
        ("X-ray HSE at 2 r_c", 1.2e-9, "Chan&DelPopolo 2020"),
        ("X-ray HSE at 3 r_c", 3.9e-10, "Chan&DelPopolo 2020 -- outer bin"),
        ("Coma MOND model (LOWER BOUND)", 2.0e-10 * (H0_KMS / 50.0) ** 2, "The&White 1988, at this H0"),
    ]
    print("  %-40s %11s | %8s %8s | %8s %8s" % ("probe", "g [m/s^2]", "x canon", "dex", "x alt", "dex"))
    ratios = []
    for name, g, _ in ladder:
        ratios.append(g / A0_CANON)
        print("  %-40s %11.3e | %8.2f %8.3f | %8.2f %8.3f"
              % (name, g, g / A0_CANON, np.log10(g / A0_CANON), g / A0_ALT, np.log10(g / A0_ALT)))
    lo, hi = min(ratios), max(ratios)
    print("\n  SPREAD, canonical footing: %.2fx to %.2fx (%.3f to %.3f dex), a factor %.1f range -- IDENTICAL to"
          % (lo, hi, np.log10(lo), np.log10(hi), hi / lo))
    print("  the committed %.2fx-%.2fx.  These rungs are measurements divided by an INPUT a0; no nu enters, so"
          % (COMMITTED["ladder_lo"], COMMITTED["ladder_hi"]))
    print("  Route A CANNOT move them.  The ladder is NON-DIAGNOSTIC of the kernel switch -- stated plainly,")
    print("  because re-quoting it as a Route A result would be double-counting the a0 footing.")
    print("\n  WHAT ROUTE A DOES MOVE: the eta each rung implies, eta_equiv = sqrt(R / B(y)) with R = g/a0.")
    print("  (identity: g_obs = sqrt(R a0 g_bar) and g_pred = nu g_bar, so eta = sqrt(R/B) exactly.)")
    print("  y is NOT known per rung -- inner rungs sit at higher y -- so the whole cluster range is scanned")
    print("  rather than one value invented.  Route A's help is exactly nu_exp/nu_a2 and GROWS with y, i.e.")
    print("  grows INWARD, which is where the ladder is worst.  It is still capped at %.4fx." % ceil2)
    yscan = (0.01, 0.037, 0.1, 0.3, 1.0)
    print("\n  %-40s %s" % ("probe", "  ".join("y=%-5.3g  RtA / a2" % y for y in yscan)))
    for name, g, _ in ladder:
        R = g / A0_CANON
        cells = []
        for y in yscan:
            cells.append("%5.2f /%5.2f" % (np.sqrt(R / boost(nu, y)), np.sqrt(R / boost(nu_alpha2, y))))
        print("  %-40s %s" % (name, "   ".join(cells)))
    print("\n  Read the top row: at the R500-like y = 0.037 the lensing rung needs eta = %.2f under Route A vs"
          % np.sqrt((G_DDAG / A0_CANON) / boost(nu, 0.037)))
    print("  %.2f under alpha=2; at y = 0.3 it is %.2f vs %.2f.  Real relief, bounded, and the ladder's factor"
          % (np.sqrt((G_DDAG / A0_CANON) / boost(nu_alpha2, 0.037)),
             np.sqrt((G_DDAG / A0_CANON) / boost(nu, 0.3)), np.sqrt((G_DDAG / A0_CANON) / boost(nu_alpha2, 0.3))))
    print("  %.1f METHOD spread swamps it -- the dominant uncertainty on this front is not the kernel." % (hi / lo))

    # ------------------------------------------------------------------ 6. WHAT CLOSURE WOULD STILL REQUIRE
    print("\n" + "-" * W)
    print("6. WHAT CLOSURE WOULD STILL REQUIRE UNDER ROUTE A  (requirement calculations, NOT fits)")
    print("-" * W)
    print("  a0 IS AN INPUT.  The multiplier below is solved for only to state a REQUIREMENT and is adopted")
    print("  nowhere; the canonical a0 = %.4e is used unchanged in every eta above." % A0_CANON)
    lam = {}
    for lab, a0 in FOOTINGS:
        f = lambda L, a0=a0: float(np.median(eta_of(base, L * a0, nu))) - 1.0
        L = brentq(f, 1.0, 1e3, xtol=1e-10, rtol=1e-12)
        lam[lab] = L
        print("  %-34s median eta = 1 needs a0 x %.3f  (= +%.3f dex), i.e. a0 = %.3e"
              % (lab, L, np.log10(L), L * a0))
    print("    NOT A MISPRINT that both footings land on the same absolute a0: the multiplier differs (%.3f vs"
          % lam[can])
    print("    %.3f) precisely because the a0 it multiplies differs, and what the DATA fix is the absolute scale"
          % lam[alt])
    print("    %.3e -- so this requirement is footing-INVARIANT, and the footing spread cannot be spent on it."
          % (lam[can] * A0_CANON))
    print("    Under alpha=2 the canonical requirement was a0 x %.3f; Route A lowers it to x %.3f -- still far"
          % (a2["med"] ** 2, lam[can]))
    print("    above anything the galaxy RAR admits, so the a0-boost escape is not opened by Route A.")
    print("    (deep-limit eta ~ sqrt(a0) would have guessed x %.2f; the exact solve gives x %.2f, and the"
          % (rA["med"] ** 2, lam[can]))
    print("     difference is Route A's larger subleading term -- another reason to solve rather than rescale.)")
    need = 100 * (rA["gm"] - 1)
    print("\n  THE MI-DISTINCTIVE CHANNEL, repriced against the new residual.  The relational sigma-spread --")
    print("  the one genuinely modified-inertia, non-adiabatic effect this corpus has derived -- is")
    print("  1.45-2.21%% max-min.  Needed to close Route A's geomean eta = %.3f: ~%.0f%%.  Shortfall %.0fx-%.0fx"
          % (rA["gm"], need, need / 2.21, need / 1.45))
    print("  (was %.0fx-%.0fx against the alpha=2 residual).  A ~2%% effect still cannot close a ~%.0f%% residual."
          % (100 * (a2["gm"] - 1) / 2.21, 100 * (a2["gm"] - 1) / 1.45, need))
    print("\n  STILL OPEN on this front, unchanged by Route A and not closed by it: the weak-lensing mass")
    print("  calibration axis (Li+2024 have WL running ~110%% above hydrostatic AND kinematic, which agree with")
    print("  each other), the 0.10-0.30 dex absolute-scale floor itself, the Kelleher & Lelli Eq. (5)")
    print("  order-of-magnitude caveat for modified inertia, and real extra baryons/neutrinos.  Route A is a")
    print("  kernel change and speaks to none of them.")

    # ------------------------------------------------------------------ CHECKS
    print("\n" + "=" * W)
    print("CHECKS -- falsifiable comparisons and structural identities; C9, C11, C13 run AGAINST interest")
    print("=" * W)

    # C1 -- the premise this lane was handed, tested rather than assumed
    deep = np.logspace(-8, np.log10(8.0), 20001)
    newt = np.logspace(np.log10(9.0), 4, 20001)
    chk("C1 the exponential is STRONGER than alpha=1 deep (y<8) and WEAKER Newtonian (y>9), so the lane's "
        "'weaker at intermediate accelerations' premise is FALSE",
        np.all(nu(deep) > nu_alpha1(deep)) and np.all(nu(newt) < nu_alpha1(newt)),
        "crossover at y = %.3f; min deep ratio %.6f, max Newtonian ratio %.6f"
        % (y_cross, float((nu(deep) / nu_alpha1(deep)).min()), float((nu(newt) / nu_alpha1(newt)).max())))

    # C2 -- and the clusters are on the favourable side of it
    ymax = max(float((base["gbar"] / a0).max()) for _, a0 in FOOTINGS)
    chk("C2 every cluster in the sample lies DEEP of the crossover on both footings, so the sign of Route A's "
        "cluster effect is favourable for the whole sample, not just the median",
        ymax < y_cross, "max y over both footings = %.4f vs crossover %.3f (margin %.0fx)"
        % (ymax, y_cross, y_cross / ymax))

    # C3 -- MI reading == AQUAL reading for spherical clusters (so the number is realization-invariant)
    ys = base["gbar"] / A0_CANON
    x_alg = nu(ys) * ys                        # MI / algebraic route
    resid = np.abs(mu(x_alg) * x_alg / ys - 1.0)   # AQUAL spherical field equation mu(x) x = y
    chk("C3 the MI (algebraic nu) and AQUAL (mu field-theory) readings give the SAME cluster eta -- clusters "
        "are modelled spherically, where the two forms are exact inverses",
        float(resid.max()) < 1e-10, "worst |mu(x)x/y - 1| over the 9830 clusters = %.2e" % float(resid.max()))

    # C4 -- the improvement is exactly the pointwise kernel ratio (this is what caps it)
    worst = 0.0
    for lab, a0 in FOOTINGS:
        y = base["gbar"] / a0
        for kn, kf in (("alpha=2 (superseded)", nu_alpha2), ("alpha=1 (committed row)", nu_alpha1)):
            got = eta_of(base, a0, nu) / eta_of(base, a0, kf)
            worst = max(worst, float(np.abs(got - kf(y) / nu(y)).max()))
    chk("C4 eta_RouteA/eta_alpha equals nu_alpha/nu_exp pointwise on the real data -- the identity that turns "
        "the kernel ratio into a CEILING on Route A's cluster help",
        worst < 1e-12, "worst absolute deviation from the identity = %.2e" % worst)

    # C5 -- Route A really does lower eta, on both footings, against both superseded kernels
    chk("C5 Route A LOWERS eta on both footings against both superseded kernels (the direction, measured not "
        "assumed)",
        all(S[(lab, "Route A  exp")]["med"] < S[(lab, k)]["med"] and
            S[(lab, "Route A  exp")]["dex"] < S[(lab, k)]["dex"]
            for lab, _ in FOOTINGS for k in ("alpha=2 (superseded)", "alpha=1 (committed row)")),
        "canonical %.4f < %.4f (a2) and < %.4f (a1); alt %.4f < %.4f"
        % (rA["med"], a2["med"], a1["med"], rA_alt["med"], a2_alt["med"]))

    # C6 -- the CEILING: Route A cannot close clusters at ANY acceleration
    chk("C6 CEILING -- the largest eta reduction Route A can supply anywhere in acceleration space is far "
        "short of closure, so no radius/mass/footing choice closes this front",
        ceil2 < a2["gm"] and ceil2 < a2["med"] and ceil1 < a1["med"],
        "ceiling %.4fx (vs alpha=2, at y=%.2f) against a residual of %.3fx -> short by %.2fx"
        % (ceil2, y_ceil2, a2["gm"], a2["gm"] / ceil2))

    # C7 -- the ladder is kernel-free
    chk("C7 the ladder's measured g/a0 ratios reproduce the committed 3.88x-23.50x bit-for-bit, i.e. no "
        "kernel enters them and Route A provably cannot move them",
        abs(lo - COMMITTED["ladder_lo"]) < 0.01 and abs(hi - COMMITTED["ladder_hi"]) < 0.01,
        "%.2fx - %.2fx vs committed %.2fx - %.2fx" % (lo, hi, COMMITTED["ladder_lo"], COMMITTED["ladder_hi"]))

    # C8 -- the reason it is kernel-free: the deep asymptote nu sqrt(y) -> 1 for all three
    dq = [float(k(1e-12) * np.sqrt(1e-12)) for _, k in KERNELS]
    chk("C8 all three kernels share the deep asymptote nu sqrt(y) -> 1, which is WHY a slope-1/2 fit's "
        "g_ddagger is convention-clean and why a0 keeps its meaning under Route A",
        all(abs(v - 1.0) < 1e-5 for v in dq), "nu sqrt(y) at y=1e-12: " + ", ".join("%.8f" % v for v in dq))

    # C9 -- AGAINST INTEREST: Route A is the LEAST convention-clean of the three over a finite window
    ysm = np.logspace(-4, -0.3, 4001)
    chk("C9 AGAINST INTEREST -- Route A's approach to that asymptote is the SLOWEST (B-1 ~ sqrt(y) vs y/2 and "
        "y), so its own predicted g_ddagger_eff departs from a0 fastest and the committed 'convention-clean' "
        "wording is WEAKER under Route A, not stronger",
        np.all(boost(nu, ysm) - 1 > boost(nu_alpha1, ysm) - 1)
        and np.all(boost(nu_alpha1, ysm) - 1 > boost(nu_alpha2, ysm) - 1),
        "at y=0.1: B-1 = %.4f (exp) > %.4f (a1) > %.4f (a2)"
        % (boost(nu, 0.1) - 1, boost(nu_alpha1, 0.1) - 1, boost(nu_alpha2, 0.1) - 1))

    # C10 -- the g_ddagger identity: required/predicted scale IS eta^2
    y = base["gbar"] / A0_CANON
    ident = np.abs((base["gobs"] ** 2 / base["gbar"]) / (nu(y) ** 2 * base["gbar"])
                   - eta_of(base, A0_CANON, nu) ** 2)
    chk("C10 the g_ddagger framing and the eta framing are the SAME statement: required/predicted "
        "acceleration scale = eta^2 exactly, so neither is independent evidence of the other",
        float((ident / eta_of(base, A0_CANON, nu) ** 2).max()) < 1e-12,
        "worst relative deviation %.2e" % float((ident / eta_of(base, A0_CANON, nu) ** 2).max()))

    # C11 -- AGAINST INTEREST: the residual survives every floor, footing and baryon budget
    chk("C11 AGAINST INTEREST -- Route A does NOT close the front: eta stays above 1 on both footings, at "
        "every fstar out to an implausible 0.50, and the tight-floor offset stays above 3 sigma",
        min(fstar_rows[f][i] for f in fstar_rows for i in (0, 2)) > 1.0
        and sig[(can, "Route A  exp")][0.10] > 3.0 and rA["med"] > 1.9,
        "min eta over the whole fstar sweep and both footings = %.3f; tight-floor sigma %.2f"
        % (min(fstar_rows[f][i] for f in fstar_rows for i in (0, 2)), sig[(can, "Route A  exp")][0.10]))

    # C12 -- floor arithmetic, over the FULL range including the loose end
    chk("C12 the floor-limited sigma is mean/floor at all four floors including the 0.30-dex loose end that "
        "the committed ladder originally stopped short of",
        all(abs(sig[(lab, kn)][f] - S[(lab, kn)]["dex"] / f) < 1e-12
            for lab, _ in FOOTINGS for kn, _ in KERNELS for f in FLOORS),
        "canonical Route A: %.2f / %.2f / %.2f / %.2f sigma"
        % tuple(sig[(can, "Route A  exp")][f] for f in FLOORS))

    # C13 -- AGAINST INTEREST: the scatter grew
    chk("C13 AGAINST INTEREST -- the log-eta scatter is LARGER under Route A than under alpha=2 (recorded as "
        "a description; NOT converted into a significance, since a scatter is not a parameter error)",
        rA["sd"] > a2["sd"] and rA_alt["sd"] > a2_alt["sd"],
        "canonical %.5f > %.5f dex (+%.1f%%); alt %.5f > %.5f dex"
        % (rA["sd"], a2["sd"], 100 * (rA["sd"] / a2["sd"] - 1), rA_alt["sd"], a2_alt["sd"]))

    # C14 -- footing bookkeeping, including the module-vs-anchor a0_alt discrepancy
    d_alt = abs(A0_ALT / A0_ALT_ANCHOR - 1)
    e_mod = stats(eta_of(base, A0_ALT, nu))["med"]
    e_anc = stats(eta_of(base, A0_ALT_ANCHOR, nu))["med"]
    chk("C14 the module's hard-coded A0_ALT and the anchor's computed cH0/Z differ by <0.15%, and that "
        "difference moves the alt-footing eta by <0.1% -- so the footing spread quoted here is the physics, "
        "not a bookkeeping artefact",
        d_alt < 1.5e-3 and abs(e_mod / e_anc - 1) < 1e-3,
        "a0_alt %.5e (module) vs %.5e (anchor) = %.3f%%; eta %.4f vs %.4f"
        % (A0_ALT, A0_ALT_ANCHOR, 100 * d_alt, e_mod, e_anc))

    # C15 -- the requirement solve is a real root, and it is not the deep-limit guess
    chk("C15 the a0 multiplier that would close eta is a genuine root of median eta(lambda a0) = 1 and is "
        "NOT equal to the deep-limit eta^2 guess -- the reason this lane re-solved instead of rescaling",
        all(abs(float(np.median(eta_of(base, lam[lab] * a0, nu))) - 1.0) < 1e-8 for lab, a0 in FOOTINGS)
        and abs(lam[can] / rA["med"] ** 2 - 1) > 0.02,
        "canonical lambda = %.3f vs the sqrt(a0) guess %.3f (%.1f%% apart)"
        % (lam[can], rA["med"] ** 2, 100 * abs(lam[can] / rA["med"] ** 2 - 1)))

    # C16 -- the closure requirement is footing-INVARIANT (the two multipliers land on one absolute a0)
    chk("C16 the a0 that would close clusters is the SAME absolute number on both footings, so the "
        "canonical-vs-alt spread is not a resource that can be spent on this front",
        abs(lam[can] * A0_CANON / (lam[alt] * A0_ALT) - 1) < 1e-6,
        "canonical %.3f x %.4e = %.4e; alt %.3f x %.4e = %.4e"
        % (lam[can], A0_CANON, lam[can] * A0_CANON, lam[alt], A0_ALT, lam[alt] * A0_ALT))

    # ------------------------------------------------------------------ VERDICT
    print("\n" + "=" * W)
    if _FAILS:
        print("RESULT: %d of %d CHECK(S) FAILED -> %s" % (len(_FAILS), len(_RUN), "; ".join(_FAILS)))
        print("=" * W)
        sys.exit(1)
    print("RESULT: all %d checks passed." % len(_RUN))
    print("-" * W)
    print("LANE 5 VERDICT -- ROUTE A HELPS CLUSTERS, MODESTLY, AND THE LANE'S STATED EXPECTATION WAS BACKWARDS.")
    print("  (a) eta(R500) = %.3f median / %.3f geomean canonical (was %.3f/%.3f under alpha=2, %.3f/%.3f under"
          % (rA["med"], rA["gm"], a2["med"], a2["gm"], a1["med"], a1["gm"]))
    print("      the committed alpha=1 row); alt footing %.3f/%.3f.  %+.4f dex ->" % (rA_alt["med"], rA_alt["gm"], rA["dex"]))
    print("      %.2f / %.2f / %.2f / %.2f sigma over the FULL 0.10-0.30 dex floor range, never the tight end alone."
          % tuple(sig[(can, "Route A  exp")][f] for f in FLOORS))
    print("  (b) the method+radius ladder is UNCHANGED at %.2fx-%.2fx: those rungs are measurements over an"
          % (lo, hi))
    print("      input a0 and contain no kernel, so the ladder is NON-DIAGNOSTIC of Route A.  What Route A")
    print("      moves is the eta each rung implies, by nu_exp/nu_a2, which grows inward and caps at %.3fx." % ceil2)
    print("  (c) g_ddagger MEASURED / a0 = %.2f canonical, %.2f alt -- identical to the committed %.2f."
          % (G_DDAG / A0_CANON, G_DDAG / A0_ALT, COMMITTED["ratio_lens"]))
    print("      The framework's PREDICTED scale rises %.4f a0 -> %.4f a0, cutting the shortfall %.2fx -> %.2fx."
          % (gpred[(can, "alpha=2 (superseded)")] / A0_CANON, gpred[(can, "Route A  exp")] / A0_CANON,
             short[(can, "alpha=2 (superseded)")], short[(can, "Route A  exp")]))
    print("  (d) HELPS -- about %.0f%% off eta, %.4f dex, tight-floor %.2f -> %.2f sigma.  It does not resolve"
          % (100 * (1 - rA["med"] / a2["med"]), a2["dex"] - rA["dex"],
             sig[(can, "alpha=2 (superseded)")][0.10], sig[(can, "Route A  exp")][0.10]))
    print("      the front and by the ceiling above it cannot: %.3fx available anywhere vs %.3fx needed."
          % (ceil2, a2["gm"]))
    print("      Two things go the other way and are on the record: the log-eta scatter grows %.1f%%, and the"
          % (100 * (rA["sd"] / a2["sd"] - 1)))
    print("      'convention-clean g_ddagger' wording weakens because Route A leaves the deep asymptote slowest.")
    print("  The cluster front stays the framework's hardest in-hand problem; the weak-lensing calibration, the")
    print("  absolute-scale floor, the KL Eq. (5) MI caveat and real extra baryons all remain open axes here.")
    print("=" * W)


if __name__ == "__main__":
    main()
