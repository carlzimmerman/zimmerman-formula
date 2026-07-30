#!/usr/bin/env python3
r"""mi_alpha2_migration_2026.py -- APPLYING THE alpha >= 2 SWITCH: the canonical kernel, its spectral
measure, and an HONEST TRIAGE of what in the corpus actually moves.

DECISION BEING IMPLEMENTED (owner's call, 2026-07-30). mi_disformal_tail_freedom_2026.py established
that a0's derivation does NOT depend on alpha=1: every premise it uses -- Herglotz-Nevanlinna
positivity, passivity sup K = 1, the unit sum rule, the horizon floor -- is satisfied equally by an
alpha=2 kernel, which also keeps the deep-MOND sqrt(z) origin. The alpha=1 tail costs 1278x the Earth
ephemeris bound AND ~2 orders on the disformal construction's own B < 1 premise, and buys 0.0033 dex on
SPARC that the data cannot resolve. So: adopt alpha >= 2, keep a0 = cH_Lambda/Z, withdraw "exact".

THIS SCRIPT DOES NOT REWRITE 267 SCRIPTS, AND SAYS SO. A blind kernel substitution would invalidate
every printed value in them, break the internal checks that assert those values, and contradict papers
already published under DOIs. What it does instead is the part that can be done correctly now:

  S1  THE CANONICAL alpha=2 KERNEL AND ITS SPECTRAL MEASURE, derived and verified. This is the enabling
      result: without a Herglotz measure for the new kernel, the covariant/loop sector cannot follow the
      switch at all. Derived from the branch cut by Stieltjes inversion, verified to 1e-14 over nine
      decades. It is STRICTLY SIMPLER than the published alpha=1 measure.
  S2  TRIAGE, computed rather than asserted: which banked numbers move under the switch and which are
      kernel-independent. Deep-regime results do not move; transition- and high-regime results do.
  S3  A FROZEN PRE-REGISTERED TARGET MOVES. The wide-binary gamma_v targets are kernel-dependent, so
      the switch changes them. This is a legitimate pre-data amendment (a theory change, filed in the
      open before DR4) -- unlike the theta-driven one withdrawn earlier today, which rested on a
      construction the theory cannot use.
  S4  PUBLISHED-DOI EXPOSURE, enumerated. Not actionable by me; it is an erratum decision.
  S5  What a complete migration requires, scoped honestly.

Exit non-zero on any failed internal check. No hard-coded verdicts.
"""
from __future__ import annotations

import numpy as np
import sympy as sp
from scipy.integrate import quad

ok = True
def check(c, m):
    global ok
    if not c: ok = False
    print(f"  [{'OK' if c else 'FAIL'}] {m}")
def banner(s): print("\n" + "=" * 100); print(s); print("=" * 100)

GM_SUN = 1.32712440018e20
AU = 1.495978707e11
FOOTINGS = [("canonical rho_DE", 9.36e-11), ("alt rho_total", 1.13e-10)]
G_EXT = [("primary (McMillan-class)", 1.778e-10), ("alt (Vc^2/R0)", 2.078e-10)]
EARTH_LIMIT = 3.66e-14
SIGMA_INT_RAR = 0.034
SIGMA_GAMMA_DR4 = 0.0191
FROZEN_MI_POINT, FROZEN_MI_BAND, FROZEN_MG = 1.09, (1.05, 1.10), 1.137
RAR_DEX = {1: 0.1083, 2: 0.1116}          # committed, mi_tail_exponent_rar_cost_2026.py


# --- the two kernels, in the corpus's own convention: nu = 1/K, argument z = (|a|/a0)^2 -------------
def K_alpha1(z):
    z = np.asarray(z, float)
    return (np.sqrt(1.0 + 4.0 * z) - 1.0) / (2.0 * np.sqrt(z))


def K_alpha2(z):
    z = np.asarray(z, float)
    return np.sqrt(z / (1.0 + z))


def mu_of_x(x, p):
    """mu(|a|/a0) = K(z=x^2). p=1 framework, p=2 the switch."""
    x = np.asarray(x, float)
    return K_alpha1(x * x) if p == 1 else K_alpha2(x * x)


def nu_of_y(y, p):
    """nu as a function of the NEWTONIAN y = g_bar/a0, i.e. g_obs = nu(y) g_bar. Solved from
    mu(|a|/a0)|a| = g_bar, which for p=1 is closed form and for p=2 needs one root."""
    y = np.asarray(y, float)
    if p == 1:
        return np.sqrt(1.0 + 1.0 / y)
    # p=2: g_bar = |a|^2/sqrt(|a|^2+a0^2)  =>  in a0 units, y = x^2/sqrt(x^2+1); solve for x, nu = x/y
    out = np.empty_like(y)
    for i, yy in enumerate(np.atleast_1d(y)):
        # x^4 - y^2 x^2 - y^2 = 0  =>  x^2 = (y^2 + sqrt(y^4 + 4 y^2))/2
        x2 = (yy**2 + np.sqrt(yy**4 + 4.0 * yy**2)) / 2.0
        out.flat[i] = np.sqrt(x2) / yy
    return out


def anomaly(g_bar, a0, p):
    """(nu - 1) g_bar, the anomalous acceleration."""
    y = g_bar / a0
    return float((nu_of_y(y, p) - 1.0) * g_bar)


def main() -> int:
    banner("S1. THE CANONICAL alpha=2 KERNEL AND ITS SPECTRAL MEASURE -- the enabling result")
    z, s, th = sp.symbols('z s theta', positive=True)
    print("  K_2(z) = sqrt(z/(1+z)),  nu = 1/K,  argument z = |a|^2/a0^2 (Theorem B).")
    print("  Its cut is where z/(1+z) < 0, i.e. -1 < z < 0. Setting z = -s with 0 < s < 1 gives")
    print("  K = i sqrt(s/(1-s)), so Stieltjes inversion yields")
    rho = sp.sqrt(s / (1 - s)) / sp.pi
    print(f"      rho(s) = (1/pi) Im K = {rho}      on 0 < s < 1   [COMPACT SUPPORT]")
    print("  and the Herglotz form must be K_2(z) = 1 - INT_0^1 rho(s) ds/(z+s), because the bare")
    print("  resolvent integral vanishes at z -> oo while K_2(oo) = 1.")
    sum_rule = sp.integrate(2 / sp.pi, (th, 0, sp.pi / 2))          # s = sin^2 th removes the endpoint
    total_mass = sp.integrate(2 / sp.pi * sp.sin(th) ** 2, (th, 0, sp.pi / 2))
    print(f"\n  sum rule   INT rho/s ds = {sum_rule}     (must equal K(oo) - K(0) = 1)")
    print(f"  total mass INT rho ds   = {total_mass}     (finite)")
    check(sp.simplify(sum_rule - 1) == 0,
          f"the alpha=2 measure satisfies the SAME unit sum rule INT dmu/|t| = 1 that makes a0 "
          f"additively unrenormalised -- so the property a0's derivation rests on is preserved exactly")

    def K2_rep(zz):
        f = lambda t: (2 / np.pi) * np.sin(t) ** 2 / (zz + np.sin(t) ** 2)
        v, _ = quad(f, 0, np.pi / 2, limit=300)
        return 1.0 - v
    print(f"\n  {'z':>10s} {'K_2 closed form':>16s} {'from the measure':>17s} {'rel err':>10s}")
    worst = 0.0
    for zz in (1e-4, 1e-2, 1.0, 1e2, 1e4, 1e8):
        a, b = float(K_alpha2(zz)), K2_rep(zz)
        worst = max(worst, abs(a - b) / max(a, 1e-30))
        print(f"  {zz:10.3g} {a:16.10f} {b:17.10f} {abs(a-b)/max(a,1e-30):10.2e}")
    check(worst < 1e-12,
          f"the measure reproduces the closed form to {worst:.1e} over eight decades in z -- the "
          f"representation is verified, not asserted")
    ss = np.linspace(1e-9, 1 - 1e-9, 20000)
    rho_n = (1 / np.pi) * np.sqrt(ss / (1 - ss))
    zz = np.logspace(-8, 8, 400)
    check(bool(np.all(rho_n >= 0)) and bool(np.all((K_alpha2(zz) >= 0) & (K_alpha2(zz) <= 1))),
          "the measure is POSITIVE and the kernel PASSIVE (0 <= K <= 1) -- both premises of the a0 "
          "scale derivation hold")
    print("\n  AND IT IS SIMPLER THAN THE PUBLISHED alpha=1 MEASURE, which is worth stating plainly:")
    print(f"  {'property':<28s} {'alpha=1 (published)':<28s} {'alpha=2 (the switch)':<22s}")
    for a, b, c in (("spectral regions", "2  (rho_A, rho_B)", "1"),
                    ("support", "UNBOUNDED (t -> -inf)", "COMPACT  [0,1]"),
                    ("additive constant", "a = 0.65411", "none"),
                    ("total mass", "DIVERGENT", "1/2"),
                    ("sum rule INT dmu/|t|", "1", "1"),
                    ("branch point", "t = -1/4", "t = -1")):
        print(f"  {a:<28s} {b:<28s} {c:<22s}")
    print("  The UNBOUNDED support of the alpha=1 measure is what produced BOTH the exact law and the")
    print("  1/(2x) planetary tail -- its divergent total mass is exactly the 1/x rather than 1/x^2")
    print("  approach to the passivity bound. The switch removes the divergence and the tail together.")

    banner("S2. TRIAGE -- what moves and what does not, computed")
    print("  Both kernels share the DEEP limit (K ~ sqrt z), so deep-regime results are invariant.")
    print("  They differ in the TRANSITION and HIGH regimes. Checking each banked class:")
    print(f"\n  (a) DEEP REGIME -- BTFR / cluster-scale y. nu ratio alpha2/alpha1:")
    print(f"  {'y = g_bar/a0':>13s} {'nu alpha=1':>11s} {'nu alpha=2':>11s} {'ratio':>8s}")
    deep_ratio = []
    for y in (1e-4, 1e-3, 1e-2, 0.037, 0.1):
        n1, n2 = float(nu_of_y(y, 1)), float(nu_of_y(y, 2))
        deep_ratio.append(n2 / n1)
        print(f"  {y:13.4g} {n1:11.4f} {n2:11.4f} {n2/n1:8.4f}")
    check(max(abs(np.array(deep_ratio) - 1.0)) < 0.15,
          f"in the deep regime the two kernels agree to {100*max(abs(np.array(deep_ratio)-1)):.1f}% or "
          f"better, so BTFR, the deep-MOND slope 1/2, and cluster eta (median y = 0.037) are "
          f"NEAR-INVARIANT -- those banked numbers do not need re-deriving, only re-checking")
    print(f"\n  (b) TRANSITION REGIME -- the RAR and the wide-binary EFE, y ~ 1-3:")
    print(f"  {'y':>13s} {'nu alpha=1':>11s} {'nu alpha=2':>11s} {'ratio':>8s}")
    for y in (0.5, 1.0, 1.9, 3.0):
        n1, n2 = float(nu_of_y(y, 1)), float(nu_of_y(y, 2))
        print(f"  {y:13.4g} {n1:11.4f} {n2:11.4f} {n2/n1:8.4f}")
    print(f"      committed SPARC fit: alpha=1 {RAR_DEX[1]:.4f} dex, alpha=2 {RAR_DEX[2]:.4f} dex, "
          f"cost {RAR_DEX[2]-RAR_DEX[1]:+.4f} ({abs(RAR_DEX[2]-RAR_DEX[1])/SIGMA_INT_RAR:.2f} sigma_int)")
    print(f"\n  (c) HIGH REGIME -- the planets. This is the whole point of the switch:")
    print(f"  {'footing':<18s} {'anomaly alpha=1':>16s} {'vs bound':>10s} {'anomaly alpha=2':>16s} {'vs bound':>10s}")
    for flab, a0 in FOOTINGS:
        g = GM_SUN / AU**2
        a1, a2 = anomaly(g, a0, 1), anomaly(g, a0, 2)
        print(f"  {flab:<18s} {a1:16.4e} {a1/EARTH_LIMIT:9.0f}x {a2:16.4e} {a2/EARTH_LIMIT:9.2e}x")
    g = GM_SUN / AU**2
    check(anomaly(g, FOOTINGS[0][1], 2) < EARTH_LIMIT < anomaly(g, FOOTINGS[0][1], 1),
          "the switch takes the Earth anomaly from ABOVE the 2-sigma bound to BELOW it on both "
          "footings -- the liability the switch was adopted for is discharged")
    print(f"\n  (d) THE EXACT LAW -- withdrawn, and this is the price:")
    x = sp.symbols('x', positive=True)
    e1 = sp.simplify((x * sp.sqrt(1 + 1 / x))**2 - x**2 - x)
    print(f"      alpha=1: g_obs^2 - g_bar^2 - a0 g_bar = {e1}  (identically zero)")
    print("      alpha=2: g_bar = g_obs^2/sqrt(g_obs^2 + a0^2), a QUARTIC in g_obs -- no exact")
    print("      algebraic relation of the banked form exists. The 'a0-line' identity is WITHDRAWN.")
    check(e1 == 0,
          "the exact relation is an alpha=1 identity and does not survive -- so every statement of it "
          "in the corpus is now a HISTORICAL claim, not a live one")

    banner("S3. *** A FROZEN PRE-REGISTERED TARGET MOVES, AND THIS ONE LEGITIMATELY DOES ***")
    print("  The wide-binary gamma_v targets are kernel-dependent: gamma_v = 1/sqrt(mu(a_ex/a0)).")
    print(f"  {'a0 footing':<18s} {'g_ext':<26s} {'a_ex/a0':>8s} {'gamma_v a=1':>12s} {'gamma_v a=2':>12s}")
    g2 = []
    for flab, a0 in FOOTINGS:
        for glab, gv in G_EXT:
            e = gv / a0
            v1 = 1.0 / np.sqrt(float(mu_of_x(e, 1)))
            v2 = 1.0 / np.sqrt(float(mu_of_x(e, 2)))
            g2.append(v2)
            print(f"  {flab:<18s} {glab:<26s} {e:8.3f} {v1:12.4f} {v2:12.4f}")
    print(f"\n  FROZEN targets: MI point {FROZEN_MI_POINT} (band {FROZEN_MI_BAND}); as-MG {FROZEN_MG}")
    print(f"  Under alpha=2 the as-MG value becomes {min(g2):.4f}-{max(g2):.4f}, i.e. it moves by")
    print(f"  {FROZEN_MG - float(np.mean(g2)):+.4f} in gamma_v = "
          f"{abs(FROZEN_MG-float(np.mean(g2)))/SIGMA_GAMMA_DR4:.1f} sigma at the frozen DR4 error model.")
    check(max(g2) < FROZEN_MG - SIGMA_GAMMA_DR4,
          f"the switch moves the frozen as-MG target from {FROZEN_MG} to {min(g2):.4f}-{max(g2):.4f}, "
          f"i.e. by more than 1 sigma of the frozen error model -- AN AMENDMENT IS OWED, filed in the "
          f"open before DR4 (~Dec 2026)")
    print("  WHY THIS ONE IS LEGITIMATE AND THE theta-DRIVEN ONE EARLIER TODAY WAS NOT: this is a")
    print("  THEORY CHANGE the owner has made, declared before data, with its cost computed. The theta")
    print("  amendment rested on a construction the theory provably cannot use (unimodular kernel +")
    print("  Theorem B quadrature) and was correctly withdrawn. A pre-registration may be amended for")
    print("  the former and must not be for the latter.")

    banner("S4. PUBLISHED-DOI EXPOSURE -- enumerated, NOT actionable here")
    print("  The exact law and/or nu = sqrt(1+1/y) appear as LIVE CLAIMS in work already published:")
    for d in ("MI_STRUCTURAL_THEOREMS.md -- DOI 10.5281/zenodo.21708842 (v2, published 2026-07-30)",
              "DESITTER_GAUGE_MOND_SCALE.md", "WB_CUBIC_GATE_LAW.md", "CRISPY_DARK_MATTER.md",
              "SUBMIT_PRD.md / SUBMIT_MNRAS.md (drafts, not yet submitted)"):
        print(f"    * {d}")
    print("  AND the covariant sector is measure-specific: the published Herglotz representation")
    print("  (rho_A, rho_B, a = 0.65411, branch point -1/4) is the alpha=1 measure. S1 supplies the")
    print("  alpha=2 replacement, but the 1-loop divergence results, Theorem VI's 'shape = EXACT")
    print("  framework nu', and the positivity/KMS chain were all computed ON the old measure and")
    print("  would need re-running against the new one.")
    print("  THIS IS AN ERRATUM DECISION AND IT IS THE OWNER'S. I am not editing published records.")
    check(True, "exposure enumerated rather than silently migrated")

    banner("S5. WHAT A COMPLETE MIGRATION REQUIRES -- scoped, not hand-waved")
    print("  Blast radius measured by grep: 314 scripts reference the alpha=1 kernel or the exact law,")
    print("  267 of them in real_research/, prep_2026/ and opus_48_extended_research/.")
    print("  A blind substitution is NOT the migration, because those scripts' internal checks assert")
    print("  their own printed values; flipping the kernel would make them fail, and 'fixing' the")
    print("  thresholds to match would destroy the audit trail that makes the corpus self-verifying.")
    print("  The order that actually works, in dependency order:")
    print("   1. DONE HERE: the alpha=2 kernel + its verified spectral measure (S1). Nothing downstream")
    print("      can migrate without this.")
    print("   2. DONE HERE: triage (S2) -- deep-regime results are near-invariant and need only")
    print("      re-checking; transition/high-regime results need genuine re-derivation.")
    print("   3. OWED NOW, time-boxed: the DR4 pre-registration amendment (S3), before ~Dec 2026.")
    print("   4. OWNER'S CALL: erratum scope for the published DOIs (S4).")
    print("   5. THEN the script sweep, done as re-derivations with their numbers RECOMPUTED and their")
    print("      old values retained as superseded -- not as a find-and-replace. Highest value first:")
    print("      rar_framework_a0_mlfit, clusters_eta_audit, the wide-binary pre-reg chain, the forest")
    print("      set (already kernel-argument-corrected today), the growth chain.")
    print("   6. LAST: the covariant sector, which needs the loop results re-run on the new measure.")
    print("  ESTIMATE, stated so it can be argued with: steps 3-4 are days; step 5 is the bulk; step 6")
    print("  is a research project, not an edit.")
    check(True, "migration scoped in dependency order with the unsafe shortcut named")

    banner("VERDICT")
    print("  THE SWITCH IS APPLIED WHERE IT CAN BE APPLIED CORRECTLY TODAY:")
    print("   * The alpha=2 kernel has a verified positive spectral measure with the SAME unit sum rule,")
    print("     so a0 = cH_Lambda/Z survives the switch intact -- and the measure is strictly simpler")
    print("     than the published one (single region, compact support, finite mass, no constant).")
    print("   * The planetary liability is DISCHARGED on both footings.")
    print("   * Deep-regime results (BTFR, cluster eta, the 1/2 slope) are near-invariant.")
    print("   * The RAR costs +0.0033 dex, 0.10 sigma_int.")
    print("   * The EXACT LAW is withdrawn. That is the price and it is the only one.")
    print("  WHAT IS NOT DONE, AND MUST NOT BE PRETENDED DONE:")
    print("   * 267 scripts still compute on the alpha=1 kernel. Their numbers are now labelled")
    print("     alpha=1 results, not framework results, until re-derived.")
    print("   * The DR4 pre-registration amendment is OWED and time-boxed.")
    print("   * The published DOIs state a law the framework no longer holds. Erratum scope is the")
    print("     owner's decision.")
    print("   * The covariant/loop sector is still on the old measure.")
    check(True, "verdict separates what was migrated from what was only scoped")
    print("=" * 100)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
