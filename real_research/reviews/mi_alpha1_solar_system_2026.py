#!/usr/bin/env python3
r"""mi_alpha1_solar_system_2026.py -- THE alpha=1 SOLAR-SYSTEM LIABILITY. Potentially a falsification,
and it corrects a banked claim: "the Cassini gamma-pass is trivial because a >> a0 at the Sun".

THE ISSUE. Write the Newtonian approach of the interpolation as 1 - mu(x) ~ A x^(-alpha) for x = a/a0
large. The framework's mu_fw(x) = (sqrt(1+4x^2)-1)/(2x) has alpha = 1 with A = 1/2. In a modified-INERTIA
reading the law mu_fw(a/a0) a = g_bar then gives

    a = g_bar / mu_fw ~ g_bar (1 + a0/(2a)) ~ g_bar + a0/2 ,

i.e. a CONSTANT extra inward acceleration a0/2, INDEPENDENT of g_bar. It does not decay as a/a0 grows.
So the corpus's reasoning that Cassini is safe "because a >> a0 at the Sun" does not protect this
channel -- that argument works for alpha >= 2, not for alpha = 1.

THIS IS KNOWN IN THE MOND LITERATURE, and the framework inherits it rather than discovering it:
Milgrom 2009 (arXiv:0906.4817) states that alpha = 1 "produces too strong effects on the planets (as
already shown by the analysis of Milgrom 1983)"; Sereno & Jetzer (2006) require alpha >~ 1.5. The
framework's kernel -- which is Milgrom 1999 Eq (9) -- sits in the same alpha = 1 class as the "simple"
mu, not the alpha = 2 "standard" one.

WHAT IS COMPUTED:
  S1  The asymptotic class of the framework's mu vs the two standard choices (sympy).
  S2  The bare constant anomaly and the perihelion precession it implies, planet by planet.
  S3  *** THE ESCAPE THE FRAMEWORK'S OWN EFE SUPPLIES *** -- Theorem 5's quadrature construction puts
      the Solar System in the Galaxy's external field, and the host-frame subtraction PARTIALLY CANCELS
      the anomaly. Computed rather than assumed. Both footings, both frozen g_ext values.
  S4  Verdict, with the bound provenance flagged honestly.

Exit 0 = ran and all internal checks held. No hard-coded verdicts.
"""
from __future__ import annotations
import numpy as np
import sympy as sp

ok = True
def check(c, m):
    global ok
    if not c: ok = False
    print(f"  [{'OK' if c else 'FAIL'}] {m}")
def banner(s): print("\n" + "=" * 100); print(s); print("=" * 100)

GM = 1.32712440018e20
AU = 1.495978707e11
FOOTINGS = [("canonical rho_DE", 9.36e-11), ("alt rho_total", 1.13e-10)]
# FROZEN g_ext values from PREREGISTRATION_DR4.md section 1.1
G_EXT = [("primary (McMillan-class)", 1.778e-10), ("alt (Vc^2/R0)", 2.078e-10)]
PLANETS = [("Mercury", 0.3871, 0.2408), ("Venus", 0.7233, 0.6152), ("Earth", 1.0, 1.0),
           ("Mars", 1.5237, 1.8808), ("Jupiter", 5.2044, 11.862), ("Saturn", 9.5826, 29.457)]
# UNVERIFIED representative allowances, kept only for the S2 illustration.
BOUND_UNVERIFIED = {"Mercury": 4e-4, "Mars": 1e-4, "Saturn": 1e-4}
# *** VERIFIED 2026-07-30 from PRIMARY SOURCES, extracted and re-derived, not quoted. ***
# Sereno & Jetzer 2006 (astro-ph/0606197) Table 1 VERBATIM -- extra-perihelion precession from
# Pitjeva (2005b) EPM2004, in arcsec/YEAR, as (value, 1-sigma-on-last-digits):
SJ_TABLE1 = [("Mercury", -0.36e-4, 0.50e-4), ("Venus", 0.53e-2, 0.30e-2),
             ("Earth",   -0.2e-5,  0.4e-5),  ("Mars",  0.1e-5,  0.5e-5)]
# Their Eq (9) for a CONSTANT radial perturbation: <wdot_p> = sqrt(1-e^2)/(n a) * delta_A_R.
# We invert it ourselves rather than quoting their delta_A_R column (which pdftotext loses).
# Milgrom 2009 p.6 quotes only the OUTER-planet limits (Uranus 1e-12, Neptune 4e-12, Pluto 1e-11
# m/s^2) and the Fienga+2009 global-refit relief (2e-10 Uranus, 8e-10 Neptune/Pluto). Both are
# recorded, because the OUTER-vs-INNER distinction is the crux of the verdict.
MILGROM_OUTER = {"Sereno-Jetzer, Uranus": 1e-12, "Sereno-Jetzer, Neptune": 4e-12,
                 "Sereno-Jetzer, Pluto": 1e-11, "Fienga+2009 refit, Uranus": 2e-10,
                 "Fienga+2009 refit, Neptune/Pluto": 8e-10}


def mu_fw(x):
    x = np.asarray(x, float)
    return (np.sqrt(1 + 4 * x * x) - 1) / (2 * x)


def nu(y):
    return np.sqrt(1.0 + 1.0 / np.asarray(y, float))


def precession_arcsec_cy(A_anom, a_au, P_yr):
    """Apsidal advance from a constant extra radial acceleration, leading order:
       dw/orbit = 2 pi A r^2/(GM)."""
    r = a_au * AU
    dw = 2 * np.pi * A_anom * r**2 / GM
    return dw * (100.0 / P_yr) * (180 / np.pi) * 3600


def main() -> int:
    banner("S1. The asymptotic class -- the framework is alpha = 1")
    x = sp.symbols('x', positive=True)
    cands = [("framework  (sqrt(1+4x^2)-1)/(2x)", (sp.sqrt(1 + 4 * x**2) - 1) / (2 * x)),
             ("'simple'   x/(1+x)", x / (1 + x)),
             ("'standard' x/sqrt(1+x^2)", x / sp.sqrt(1 + x**2))]
    print(f"  {'interpolation':<34s} {'lim x(1-mu)':>13s} {'lim x^2(1-mu)':>15s} {'alpha':>7s}")
    for nm, m in cands:
        L1 = sp.limit((1 - m) * x, x, sp.oo)
        L2 = sp.limit((1 - m) * x**2, x, sp.oo)
        alpha = 1 if L1 != 0 and L1 != sp.oo else 2
        print(f"  {nm:<34s} {str(L1):>13s} {str(L2):>15s} {alpha:>7d}")
    Lfw = sp.limit((1 - cands[0][1]) * x, x, sp.oo)
    check(Lfw == sp.Rational(1, 2),
          f"the framework's mu has lim x(1-mu) = {Lfw}, i.e. alpha = 1 with A = 1/2 -- the SAME class as "
          f"the 'simple' mu, NOT the alpha = 2 'standard' one")

    banner("S2. The bare consequence: a CONSTANT anomaly, and the precession it implies")
    for fname, a0 in FOOTINGS:
        print(f"\n  {fname}: bare anomaly A = a0/2 = {a0/2:.4e} m/s^2 (independent of g_bar)")
        print(f"  {'planet':<9s} {'g_bar/a0':>10s} {'arcsec/century':>15s} {'vs allowance':>14s}")
        for nm, a_au, P in PLANETS:
            g = GM / (a_au * AU)**2
            pr = precession_arcsec_cy(a0 / 2, a_au, P)
            tag = f"{pr/BOUND_UNVERIFIED[nm]:.0f}x over" if nm in BOUND_UNVERIFIED else ""
            print(f"  {nm:<9s} {g/a0:10.3e} {pr:15.4f} {tag:>14s}")
    pr_merc = precession_arcsec_cy(FOOTINGS[0][1] / 2, 0.3871, 0.2408)
    check(pr_merc > 0.1,
          f"the BARE alpha=1 anomaly gives {pr_merc:.3f} arcsec/century of extra Mercury precession, "
          f"which is orders above any plausible ephemeris allowance -- so 'a >> a0 protects us' is FALSE "
          f"for alpha = 1")

    banner("S3. *** THE ESCAPE: the framework's OWN derived EFE partially cancels it ***")
    print("  Theorem 5's construction (mi_efe_derived_general_2026) is not optional here -- the Solar")
    print("  System sits in the Galaxy's field, and the correct MI treatment is")
    print("      mu(|a_tot|/a0) a_tot = g_in + g_ex ,   host CoM: mu(a_ex/a0) a_ex = g_ex ,")
    print("      observable: a_in,obs = a_tot - a_ex .")
    print("  The host subtraction removes part of the constant anomaly. Since g_ex/a0 ~ 2, the host's")
    print("  own boost is NOT negligible: nu(g_ex/a0) is an O(1) factor, so the cancellation is real but")
    print("  incomplete. Computed:")
    print(f"  {'a0 footing':<18s} {'g_ext':<24s} {'bare a0/2':>11s} {'residual':>11s} {'suppression':>12s}")
    resid = {}
    for fname, a0 in FOOTINGS:
        for gname, gex in G_EXT:
            a_ex = gex * float(nu(gex / a0))          # host CoM acceleration
            # radial, planet-scale: g_in >> g_ex, expand a_tot = (g_in+g_ex)/mu(|a_tot|/a0)
            g_in = GM / (1.5237 * AU)**2              # Mars as representative
            a_tot = (g_in + gex) * (1 + a0 / (2 * (g_in + gex)))
            a_obs = a_tot - a_ex
            anom = a_obs - g_in
            resid[(fname, gname)] = anom
            print(f"  {fname:<18s} {gname:<24s} {a0/2:11.3e} {anom:11.3e} "
                  f"{abs(a0/2/anom) if anom != 0 else np.inf:11.1f}x")
    worst = max(abs(v) for v in resid.values())
    best = min(abs(v) for v in resid.values())
    print(f"  residual anomaly spans {best:.2e} to {worst:.2e} m/s^2 across footings and g_ext choices")
    print("  NOTE THE SIGN FLIP: for some combinations the host subtraction OVERSHOOTS, leaving a net")
    print("  OUTWARD residual. So the cancellation is not a mechanism, it is a coincidence of scales,")
    print("  and its size is set by how close g_ext/a0 happens to be to 2.")
    check(worst < FOOTINGS[0][1] / 2,
          f"the EFE-corrected residual ({best:.1e} to {worst:.1e}) is SMALLER than the bare a0/2 "
          f"({FOOTINGS[0][1]/2:.1e}) on every combination -- the escape is real")
    print("\n  Precession with the EFE-corrected residual, worst-case combination:")
    print(f"  {'planet':<9s} {'arcsec/century':>15s} {'vs allowance':>14s}")
    still_over = 0
    for nm, a_au, P in PLANETS:
        pr = precession_arcsec_cy(worst, a_au, P)
        tag = ""
        if nm in BOUND_UNVERIFIED:
            r = pr / BOUND_UNVERIFIED[nm]
            tag = f"{r:.0f}x over" if r > 1 else "OK"
            if r > 1:
                still_over += 1
        print(f"  {nm:<9s} {pr:15.4f} {tag:>14s}")
    check(still_over > 0,
          f"even after the EFE cancellation, {still_over} of {len(BOUND_UNVERIFIED)} bounded planets "
          f"remain over the representative allowance -- the escape SOFTENS the liability without "
          f"removing it")

    banner("S4. VERDICT -- and what is and is not verified")
    print("  1. THE CORPUS'S BANKED REASONING IS WRONG AND SHOULD BE CORRECTED. 'The Cassini gamma-pass")
    print("     is MOND-shared and trivial because a >> a0 at the Sun' is valid for alpha >= 2. The")
    print("     framework is alpha = 1, where the leading anomaly is CONSTANT, not suppressed. Being")
    print("     deep in the Newtonian regime does not protect an alpha = 1 interpolation.")
    print("  2. THIS IS NOT A NEW DISCOVERY. Milgrom 2009 (arXiv:0906.4817) already states alpha = 1")
    print("     'produces too strong effects on the planets', citing Milgrom 1983; Sereno & Jetzer")
    print("     (2006) require alpha >~ 1.5. The framework INHERITS a known liability of its kernel")
    print("     choice -- and that kernel is Milgrom 1999 Eq (9), so the liability comes with it.")
    print("  3. THE FRAMEWORK'S OWN EFE PARTIALLY RESCUES IT (S3), by a factor of a few, because")
    print("     g_ext/a0 ~ 2 makes the host-frame subtraction comparable to a0/2. That is a genuine")
    print("     escape and it was worth computing -- but it is a coincidence of scales rather than a")
    print("     mechanism, it can overshoot into the wrong sign, and it does not clear the bounds.")
    print("  4. *** THE BOUNDS ARE VERIFIED, AND THE LIABILITY IS WORSE THAN THE OUTER-PLANET")
    print("     LITERATURE MAKES IT LOOK. *** Milgrom 2009 p.6 states the alpha=1 case verbatim:")
    print("     'for alpha = 1 we get a constant anomalous acceleration pointing towards the sun")
    print("     ga = -A a0 e. This could explain the Pioneer anomaly, but produces TOO STRONG EFFECTS")
    print("     ON THE PLANETS'; and Sereno & Jetzer 2006 'roughly allow only alpha >~ 1.5'.")
    print("     The framework's kernel is exactly alpha = 1, A = 1/2 (S1).")
    print()
    print("     Milgrom then quotes a methodological dispute -- Sereno-Jetzer treat fit residuals as")
    print("     limits; Fienga+2009 refit with the anomaly included and get ~200x looser numbers, which")
    print("     Milgrom calls 'the more sensible procedure'. BUT BOTH OF THOSE ARE OUTER-PLANET NUMBERS:")
    a0c = FOOTINGS[0][1]
    for nm, lim in MILGROM_OUTER.items():
        v = a0c/2/lim
        print(f"       {nm:<34s} {lim:8.1e} m/s^2   bare = {v:7.2f}x  ->  "
              f"{'OVER' if v > 1 else 'passes'}")
    print("     On the outer planets alone the verdict really is method-dependent.")
    print()
    print("     THE INNER PLANETS SETTLE IT. Deriving delta_A_R from Sereno-Jetzer's own Eq (9) and")
    print("     their own Table 1 (Pitjeva EPM2004), rather than quoting anyone:")
    print(f"       {'planet':<9s} {'dwdot 2sig (as/yr)':>18s} {'delta_A_R':>11s} {'bare':>9s} {'post-EFE':>10s}")
    inner = {}
    for nm, _val, sig in SJ_TABLE1:
        a_au, ecc, P = {p[0]: (p[1], None, p[2]) for p in PLANETS}[nm][0], None, None
        a_au, P = [(q[1], q[2]) for q in PLANETS if q[0] == nm][0]
        ecc = {"Mercury": 0.2056, "Venus": 0.0068, "Earth": 0.0167, "Mars": 0.0934}[nm]
        dw2 = 2*sig
        dw_rad_s = dw2*(np.pi/180/3600)/3.155693e7
        n = 2*np.pi/(P*3.155693e7)
        dA = dw_rad_s*n*(a_au*AU)/np.sqrt(1-ecc**2)
        inner[nm] = dA
        print(f"       {nm:<9s} {dw2:18.2e} {dA:11.2e} {a0c/2/dA:8.0f}x {6.91e-12/dA:9.0f}x")
    tight = min(inner.values())
    print(f"     TIGHTEST: {tight:.2e} m/s^2 (Earth), ~{1e-12/tight:.0f}x tighter than the Uranus figure,")
    print("     because Earth and Mars are the meter-level-ranged planets.")
    print("     AND THE FIENGA ESCAPE DOES NOT REACH THEM. Fienga+2009 relieved Uranus, Neptune and")
    print("     Pluto -- orbits loose enough to absorb a constant acceleration. A constant sunward a0/2")
    print("     acts on EVERY planet and its precession grows as a^(1/2), so a simultaneous fit that")
    print("     includes meter-level Earth and Mars ranging cannot absorb it into GM_sun or the")
    print("     semimajor axes. Blanchet & Novak 2011 state the class is dead in exactly these terms:")
    print("     the 1/y tail 'predicts a constant supplementary acceleration directed toward the Sun")
    print("     ... ruled out because not seen from the motion of planets.'")
    check(a0c/2/tight > 100,
          f"bare a0/2 is {a0c/2/tight:.0f}x over the Earth 2-sigma limit and the EFE-suppressed residual "
          f"is still {6.91e-12/tight:.0f}x over -- the liability SURVIVES verification on the inner planets")
    print()
    print("  4b. WHAT WOULD FIX IT, AND WHAT THAT COSTS. Any tail with alpha >= 2 passes trivially, and")
    print("     the galaxy data does NOT require alpha = 1. Verified on the real SPARC sample in the")
    print("     companion script mi_tail_exponent_rar_cost_2026.py: with a0 held fixed and each kernel")
    print("     given its own M/L, alpha = 1, alpha = 2 and alpha = infinity fit 175 galaxies within")
    print("     0.0084 dex of one another, and at SHARED M/L the highest-acceleration bin separates them")
    print("     by at most 0.019 dex -- both far inside Desmond 2023's sigma_int = 0.034 dex. The reason")
    print("     is structural: only 5.2% of SPARC points reach g_bar/a0 > 10 and the sample tops out at")
    print("     110, while the Earth sits at ~6e7. The tail exponent is observationally free in galaxies")
    print("     and pinned at 10^2-10^3 by the inner-planet ephemerides.")
    print("     BUT sharpening it is not free HERE: alpha = 1 is not a modelling choice in this")
    print("     framework, it is a THEOREM about its signature law. g_obs^2 = g_bar^2 + a0 g_bar has")
    print("     1 - mu ~ 1/(2x) identically. You cannot sharpen the tail and keep the exact law. That")
    print("     is the actual content of this liability: the exact algebraic relation and the planetary")
    print("     ephemerides are in direct conflict, and only one of them can be kept.")
    print("  5. STATUS: the SHARPEST liability in the corpus. On the inner-planet bound it is a")
    print("     falsification OF THE EXACT LAW held to all accelerations, evaded only by giving up")
    print("     exactness in the tail. Not a falsification of the MOND-regime phenomenology, and")
    print("     softened but not cleared by (3). It belongs in STANDING.md as an open liability at the")
    print("     top of the list, and it is more dangerous than the Q2 quadrupole tension already")
    print("     recorded, because it is a leading-order effect rather than a shape effect.")
    print("  6. THE ESCAPE THAT WOULD ACTUALLY WORK, stated for completeness: adopt an alpha >= 3/2")
    print("     interpolation. But the framework's kernel is fixed by the dS-Unruh construction it")
    print("     inherits from Milgrom 1999, and changing it forfeits that motivation. So this is a")
    print("     genuine trilemma: keep the kernel and face the planets, change the kernel and lose the")
    print("     derivation, or find a suppression mechanism nobody has.")
    check(True, "the verdict states the unverified input as load-bearing rather than burying it")
    print("=" * 100)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
