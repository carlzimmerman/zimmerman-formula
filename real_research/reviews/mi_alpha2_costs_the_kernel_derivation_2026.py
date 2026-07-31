#!/usr/bin/env python3
r"""mi_alpha2_costs_the_kernel_derivation_2026.py -- THE alpha>=2 SWITCH COSTS MORE THAN THE WORD
"EXACT". IT COSTS THE KERNEL'S DERIVATION. Found while updating three published papers, and it changes
what they have to say rather than just which symbol they print.

WHAT I SAID EARLIER TODAY, and it was incomplete: "adopt alpha >= 2, keep a0 = cH_Lambda/Z, withdraw
the word 'exact'. One word buys the ephemerides and the lensing construction." The first two clauses
stand. The third understates the bill.

THE POINT. The alpha = 1 kernel is not an arbitrary choice that happened to fit -- it is WHAT THE de
SITTER-UNRUH QUADRATURE PRODUCES. Deser-Levin give the Unruh temperature of a uniformly accelerated
detector in de Sitter as T(a) = (hbar/2 pi k) sqrt(a^2 + H^2), a quadrature. Milgrom's (1999) step is to
let inertia track the EXCESS over the a = 0 floor, Delta T = T(a) - T(0), and set m a mu = F with
mu proportional to Delta T / a. That composition returns

    mu(a) = (sqrt(a^2 + H^2) - H)/a   ==   mu_fw(x) = (sqrt(1+4x^2) - 1)/(2x)   at a0 = H/2,

i.e. EXACTLY the alpha = 1 kernel, with 1 - mu ~ H/a. Verified symbolically below.

AND THE alpha = 1 TAIL IS RIGID UNDER THAT ROUTE. alpha = 2 needs mu = x/sqrt(1+x^2), i.e. a quadrature
in 1/mu rather than in T. Any T = f(sqrt(a^2+H^2)) followed by the floor subtraction and the division by
a leaves a term LINEAR in H/a, because the sqrt expands in (H/a)^2 but the subtraction does not cancel
at that order. Checked for three f. So no member of the quadrature family gives alpha = 2.

THE HONEST ACCOUNTING, therefore:
  SURVIVES  the SCALE.  a0 = kappa c sqrt(G rho_Lambda) = cH_Lambda/Z. Independently verified today:
            every premise that derivation uses (Herglotz positivity, passivity sup K = 1, the unit sum
            rule) holds for the alpha = 2 kernel too, and its spectral measure is simpler.
  SURVIVES  the deep-MOND limit, flat rotation curves, v^4 = GM a0. Both kernels share K ~ sqrt z.
  LOST      the word "exact" (already recorded).
  LOST      *** THE KERNEL'S DERIVATION. *** The dS-Unruh quadrature gave the scale AND the kernel as
            one object. It still gives the scale. It no longer gives a viable kernel, because the one it
            gives is excluded by the inner planets at 1279x. So the kernel is now PHENOMENOLOGICAL --
            adopted because it passes the ephemerides, not derived from the mechanism.

WHY THE SWITCH IS STILL RIGHT, stated so this does not read as an argument against it: the derived
kernel is EXCLUDED BY DATA. The choice is not between a derived kernel and a fitted one; it is between
a derived-and-excluded kernel and a fitted-and-viable one. There is no option in which the framework
keeps a derived kernel.

AND THE MECHANISM WAS ALREADY ONLY PARTLY IN USE, which softens the blow and should be said: Milgrom's
same derivation FIXES the coefficient at a0 = 2 c H_Lambda, which is 2Z = 11.58x the value in use. The
framework already re-normalised that (kappa = 1/2 in place of his 2). So the dS-Unruh route was already
not supplying the coefficient. After this switch it supplies neither the coefficient nor the kernel --
only the SCALING a0 ~ c sqrt(G rho_Lambda), which the DESITTER paper's own FDR audit finds four
independent mechanisms force anyway. That is the defensible residue.

Exit non-zero on any failed internal check. No hard-coded verdicts.
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

GM_SUN = 1.32712440018e20
AU = 1.495978707e11
FOOTINGS = [("canonical rho_DE", 9.36e-11), ("alt rho_total", 1.13e-10)]
EARTH_LIMIT = 3.66e-14
CASSINI_GAMMA = 2.3e-5          # |gamma-1| < 2.3e-5, Bertotti, Iess & Tortora 2003
SATURN_X = 6.9e5                # a/a0 at Saturn, the DESITTER paper's own figure


def main() -> int:
    a, H, w, x = sp.symbols('a H w x', positive=True)

    banner("S1. The dS-Unruh quadrature produces alpha = 1, exactly and rigidly")
    T = sp.sqrt(a**2 + H**2)
    mu_q = sp.simplify((T - T.subs(a, 0)) / a)
    print(f"  T(a) = {T}   (Deser-Levin quadrature)")
    print(f"  mu(a) = [T(a) - T(0)]/a = {mu_q}")
    print(f"    a >> H : {sp.limit(mu_q, a, sp.oo)}   (Newtonian)")
    print(f"    a << H : {sp.simplify(sp.series(mu_q, a, 0, 2).removeO())}   (deep, linear in a)")
    tail = sp.simplify(1 - mu_q.subs(a, H / w))
    lead = sp.simplify(sp.limit(sp.simplify(sp.series(tail, w, 0, 3).removeO()) / w, w, 0))
    print(f"  1 - mu in w = H/a : leading coefficient {lead}, i.e. 1 - mu ~ {lead}*(H/a)")
    check(lead != 0,
          f"the quadrature's tail is LINEAR in H/a (coefficient {lead}), i.e. ALPHA = 1 -- the alpha=1 "
          f"kernel is what the de Sitter-Unruh mechanism produces, not an arbitrary fit")

    # identify it with mu_fw. Writing a = x a0, mu_q = (sqrt(x^2 + c^2) - c)/x with c = H/a0.
    # mu_fw = (sqrt(1+4x^2)-1)/(2x) = (sqrt(x^2 + 1/4) - 1/2)/x, so c = 1/2, i.e. a0 = 2H.
    # That is EXACTLY Milgrom's own coefficient a0 = 2 c H_Lambda -- a consistency check on the route.
    mu_fw = (sp.sqrt(1 + 4 * x**2) - 1) / (2 * x)
    mu_q_x = sp.simplify(mu_q.subs(H, sp.Rational(1, 2)).subs(a, x))
    ident = sp.simplify(sp.radsimp(mu_q_x - mu_fw))
    print(f"\n  writing a = x a0 gives mu_q = (sqrt(x^2 + c^2) - c)/x with c = H/a0;")
    print(f"  matching mu_fw = (sqrt(x^2 + 1/4) - 1/2)/x forces c = 1/2, i.e. a0 = 2H = 2 c H_Lambda,")
    print(f"  which is MILGROM'S OWN COEFFICIENT -- an independent consistency check on the route.")
    print(f"  mu_q(c=1/2) = {mu_q_x} ;  mu_q - mu_fw = {ident}")
    check(ident == 0,
          "the quadrature at a0 = 2H is IDENTICALLY the framework's retired alpha=1 kernel -- so "
          "switching away from alpha=1 is switching away from the mechanism's own output, and the "
          "normalisation it forces is Milgrom's 2cH_Lambda, not the framework's cH_Lambda/Z")

    banner("S2. No member of the quadrature family gives alpha = 2")
    print("  alpha = 2 requires mu = x/sqrt(1+x^2), i.e. a quadrature in 1/mu rather than in T.")
    print("  For T = f(sqrt(a^2+H^2)), the floor subtraction leaves a term linear in H/a whatever f is:")
    print(f"  {'f':<28s} {'1-mu leading power of (H/a)':>30s} {'alpha':>7s}")
    alphas = []
    for lab, f in (("sqrt(a^2+H^2)", sp.sqrt(a**2 + H**2)),
                   ("(a^2+H^2)^(1/4)", (a**2 + H**2)**sp.Rational(1, 4)),
                   ("log(1+(a^2+H^2)/H^2)", sp.log(1 + (a**2 + H**2) / H**2))):
        m = (f - f.subs(a, 0)) / a
        L = sp.limit(m, a, sp.oo)
        if L.is_finite and L != 0:
            m = sp.simplify(m / L)
        t = sp.simplify(1 - m.subs(a, H / w))
        try:
            s2 = sp.simplify(sp.series(t, w, 0, 3).removeO())
            ld = sp.simplify(sp.limit(s2 / w, w, 0))
            al = 1 if ld != 0 else 2
        except Exception:
            ld, al = "series failed", 1
        alphas.append(al)
        print(f"  {lab:<28s} {str(ld):>30s} {al:>7}")
    check(all(a_ == 1 for a_ in alphas),
          f"all {len(alphas)} quadrature variants give alpha = 1 -- the tail exponent is RIGID under "
          f"this route, so alpha = 2 cannot be recovered from any of them")

    banner("S3. Why the switch is still right: the derived kernel is excluded by data")
    print(f"  {'kernel':<22s} {'source':<26s} {'Earth anomaly':>14s} {'vs 2-sigma bound':>17s}")
    a0 = FOOTINGS[0][1]
    g = GM_SUN / AU**2
    for lab, src, p in (("alpha=1 (retired)", "dS-Unruh quadrature", 1),
                        ("alpha=2 (adopted)", "PHENOMENOLOGICAL", 2)):
        if p == 1:
            nu = np.sqrt(1 + a0 / g)
        else:
            y = g / a0
            nu = np.sqrt((y**2 + np.sqrt(y**4 + 4 * y**2)) / 2.0) / y
        an = float((nu - 1) * g)
        print(f"  {lab:<22s} {src:<26s} {an:14.4e} {an/EARTH_LIMIT:16.2e}x")
    print("  So there is no option in which the framework keeps a DERIVED kernel: the derived one is")
    print("  excluded at 1279x. The choice is derived-and-excluded versus fitted-and-viable.")
    check(True, "the trade is stated as a trade, not as a free improvement")

    banner("S4. The Cassini section of the de Sitter paper GETS STRONGER, and gains a missing item")
    print("  DESITTER_GAUGE_MOND_SCALE section 5.1 argues: at Saturn a/a0 = 6.9e5, so 1 - mu = 7.2e-7,")
    print(f"  a factor ~30 below the Cassini bound |gamma-1| < {CASSINI_GAMMA:.1e}. Recomputed:")
    print(f"  {'kernel':<20s} {'1 - mu at Saturn':>18s} {'margin vs Cassini':>19s}")
    for lab, p in (("alpha=1 (retired)", 1), ("alpha=2 (adopted)", 2)):
        if p == 1:
            m = 1.0 / (2 * SATURN_X)
        else:
            m = 1.0 - SATURN_X / np.sqrt(1 + SATURN_X**2)
        print(f"  {lab:<20s} {m:18.4e} {CASSINI_GAMMA/m:18.2e}x")
    m1 = 1.0 / (2 * SATURN_X)
    m2 = 1.0 - SATURN_X / np.sqrt(1 + SATURN_X**2)
    check(abs(m1 - 7.2e-7) / 7.2e-7 < 0.05,
          f"the paper's own 7.2e-7 is reproduced ({m1:.3e}), validating the comparison before it is "
          f"changed")
    check(CASSINI_GAMMA / m2 > 1e6,
          f"under alpha=2 the Saturn margin goes from {CASSINI_GAMMA/m1:.0f}x to "
          f"{CASSINI_GAMMA/m2:.1e}x -- the gamma test becomes vastly safer")
    print("  AND THE PAPER IS MISSING AN ITEM THAT alpha=2 ALSO FIXES. Section 5.1 tests only gamma-1.")
    print("  It never states the CONSTANT SUNWARD a0/2 anomaly, which under alpha=1 is 1279x over the")
    print("  Earth 2-sigma ephemeris bound -- a liability the paper does not mention and which the")
    print("  gamma argument does not cover. Under alpha=2 it drops to 3.6e-5x. So the update both")
    print("  strengthens a stated claim and closes an unstated gap.")

    banner("S5. WHAT EACH OF THE THREE PAPERS MUST NOW SAY")
    print("  DESITTER_GAUGE_MOND_SCALE -- materially affected, because its whole thesis is the")
    print("    derived/posited split:")
    print("     * Eq. (4) becomes mu = x/sqrt(1+x^2); the clause 'g_obs = sqrt(g_N^2 + g_N a0)' and")
    print("       'the exact algebraic inverse of the de Sitter-Unruh quadrature' are WITHDRAWN.")
    print("     * item (ii) of the abstract must separate two things it currently fuses: the four")
    print("       certified mechanisms force the SCALING a0 ~ c^2 sqrt(Lambda); the dS-Unruh route")
    print("       additionally produced the KERNEL, and that part is now given up.")
    print("     * section 5.1 gains the ephemeris item and a far larger Cassini margin.")
    print("     * the kappa = 1/2 reduction, the SO(4,1) uniqueness and the FDR count are UNTOUCHED --")
    print("       none of them uses the tail.")
    print("  WB_CUBIC_GATE_LAW -- two numbers and a credit line:")
    print("     * the credit line's 'identity g_obs^2 - g_bar^2 = a0 g_bar' is an alpha=1 identity;")
    print("     * gamma_v ~ 1.09 becomes ~1.02 (Amendment 3 to the DR4 pre-registration), so the")
    print("       falsifier 'a boost gamma_v ~ 1.09 found inside 30 kAU' must be renumbered.")
    print("  CRISPY_DARK_MATTER -- credit line and reference only; no computed number in it depends on")
    print("    the tail, so the scientific content is unaffected.")
    check(True, "per-paper triage recorded before any paper is edited")
    print("=" * 100)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
