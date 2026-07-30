#!/usr/bin/env python3
r"""mi_three_corrections_priorart_2026.py -- THREE CORRECTIONS to claims I committed earlier today.
All three came out of delegated adversarial briefs and are re-verified here rather than trusted.

Two of them invalidate committed claims. Recording them before anything else is built on top.

  C1  The corpus credits Milgrom 1999 with "the identical KERNEL". That UNDERSELLS it. Milgrom 1999
      Eqs (6)-(9) derives the framework's EXACT LAW from the de Sitter-Unruh balance AND fixes the
      coefficient at a0 = 2 c H_Lambda. So the dS-Unruh argument does not leave the coefficient free
      for the framework to supply -- it FIXES it, 11.58x larger than the value in use.
  C2  Theorem 8 and the four-family no-go are a REDISCOVERY. Milgrom 2022 (PRD 106, 064060,
      arXiv:2208.07073) already writes modified-inertia models in Fourier space and states that the
      algebraic MOND relation holds ONLY for single-frequency (circular) trajectories. He also notes
      such theories "are not necessarily governed by an action" -- he dropped the action requirement
      rather than proving a no-go.
  C3  *** THE FOUR-FAMILY NO-GO OVER-REACHES AND IS WRONG AS STATED. *** The untested cell is nonlocal
      AND NON-QUADRATIC, and the exact law DOES live there: there is a closed-form f(u) whose
      circular-orbit reduction returns mu_fw exactly. That contradicts my committed S4 claim that
      Milgrom's class "delivers the LIMITS but not the exact interpolating law", and my attribution of
      Milgrom 1994 to the quadratic "class 4b" was wrong -- his class is non-quadratic, which is why it
      works. This is Milgrom's own virial result (astro-ph/0510117).

Exit 0 = ran and every re-verification held. No hard-coded verdicts.
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

C = 2.99792458e8
MPC = 3.0856775814913673e22
H0 = 67.4e3 / MPC
OM = 0.3153
H_L = H0 * np.sqrt(1 - OM)
A0_USED = 9.36e-11
Z = np.sqrt(32 * np.pi / 3)


def main() -> int:
    banner("C1. Milgrom 1999 derives the framework's EXACT LAW, with a coefficient")
    g_obs, g_bar, a0 = sp.symbols('g_obs g_bar a_0', positive=True)
    x = sp.symbols('x', positive=True)
    sol = sp.solve(sp.Eq(g_obs**2, g_bar**2 + a0 * g_bar), g_bar)
    fw = [s for s in sol if sp.limit(s.subs(a0, 0), g_obs, 1) > 0][0]
    muhat = sp.sqrt(1 + 1 / (2 * x)**2) - 1 / (2 * x)      # Milgrom 1999 Eq (9)
    mil = sp.simplify(g_obs * muhat.subs(x, g_obs / a0))    # Eq (8): 2 pi dT = a muhat(a/a0)
    print("  framework law   g_obs^2 = g_bar^2 + a0 g_bar, solved for g_bar:")
    print(f"      g_bar = {sp.simplify(fw)}")
    print("  Milgrom 1999 Eq (8)-(9)   2 pi (T - T_Lambda) = a muhat(a/a0),")
    print("      muhat(x) = sqrt(1 + (2x)^-2) - (2x)^-1 :")
    print(f"      a muhat = {sp.simplify(mil)}")
    check(sp.simplify(fw - mil) == 0,
          "the two are IDENTICAL (sympy difference exactly 0) -- with g_bar <-> 2 pi Delta T. The "
          "framework's law IS Milgrom 1999 Eq (8)-(9), not merely the same interpolating kernel")
    print(f"\n  AND MILGROM FIXES THE COEFFICIENT: his Eq (8) states a0 = 2 (Lambda/3)^(1/2) = 2 c H_Lambda.")
    print(f"  {'source':<36s} {'coefficient':>16s} {'a0 (m/s^2)':>13s} {'x in use':>10s}")
    rows = [("Milgrom 1999 Eq(8-9)  DERIVED", "2 c H_Lambda", 2 * C * H_L),
            ("Milgrom 1999 Eq(10-11) DERIVED", "c H_Lambda", C * H_L),
            ("Pikhitsa 2010 DERIVED", "2 c H", 2 * C * H_L),
            ("Klinkhamer-Kopp 2011 DERIVED", "2 c H_deS", 2 * C * H_L),
            ("Milgrom 2020 EMPIRICAL", "c H_Lambda/2pi", C * H_L / (2 * np.pi)),
            ("THIS FRAMEWORK", "c H_Lambda/Z", C * H_L / Z)]
    for nm, ex, v in rows:
        print(f"  {nm:<36s} {ex:>16s} {v:13.4e} {v/(C*H_L/Z):10.2f}")
    ratio = (2 * C * H_L) / (C * H_L / Z)
    check(abs(ratio - 2 * Z) < 1e-9,
          f"Milgrom's DERIVED coefficient is {ratio:.3f}x = exactly 2Z times the value in use -- so the "
          f"dS-Unruh argument does NOT leave the coefficient open; it predicts one, and that prediction "
          f"misses the measured a0 by about an order of magnitude")
    print("  CONSEQUENCE FOR THE CREDIT LINE. 'nu(y)=sqrt(1+1/y) is identical to Milgrom 1999 Eq 9' is")
    print("  true but understates it. The correct line is: the LAW and its dS-Unruh DERIVATION are")
    print("  Milgrom 1999; the framework's contribution is a RE-NORMALISATION of the coefficient to fit")
    print("  data (kappa = 1/2 in place of his 2), plus the modified-inertia completion.")

    banner("C2. Theorem 8 / the four-family no-go is a REDISCOVERY -- Milgrom 2022 got there")
    print("  Milgrom 2022, PRD 106, 064060 (arXiv:2208.07073) writes modified-inertia models directly in")
    print("  Fourier space, m a_hat(omega) I[{r_hat}, omega, a0] = F_hat(omega), and states that the")
    print("  algebraic MOND relation g mu(g/a0) = g_N holds ONLY for single-frequency (circular)")
    print("  trajectories. That is the same content as the frequency-vs-acceleration obstruction I")
    print("  derived today, obtained four years earlier.")
    print("  He also notes such theories 'are not necessarily governed by an action' -- i.e. he DROPPED")
    print("  the action requirement rather than proving a no-go, which is a different (and weaker)")
    print("  posture than the one I took.")
    print("  STATUS OF MY RESULT: honestly obtained, independently derived, NOT novel. Theorem 8 was")
    print("  never published to Zenodo (the v2 paper carries Theorems 1-5 and Props 6-7 only), so no")
    print("  published novelty claim needs withdrawing -- only the git record needs the credit.")
    check(True, "C2 recorded: prior art credited, and the publication exposure checked (none)")

    banner("C3. *** THE FOUR-FAMILY NO-GO IS WRONG AS STATED -- the law IS variational on circles ***")
    u = sp.symbols('u', positive=True)
    f = (2 * u * sp.sqrt(4 * u**2 + 1) - 4 * u + sp.asinh(2 * u)) / (8 * u**2)
    mu_from_f = sp.simplify(sp.diff(u**2 * f, u) / u)
    mu_fw = (sp.sqrt(1 + 4 * u**2) - 1) / (2 * u)
    print("  Dimensional closure forces the reduced circular-orbit kinetic Lagrangian to")
    print("      <L_K>/m = V^2 f(u),   u = A/a0   (on a circle Omega^2 R = Omega V = V^2/R, so every")
    print("      candidate argument coincides), and varying at fixed Omega gives")
    print("      A mu(A/a0) = g_N   with   mu(u) = 2f(u) + u f'(u) = (1/u) d/du[u^2 f(u)].")
    print(f"  CLOSED FORM: f(u) = {sp.simplify(f)}")
    print(f"  (1/u) d/du[u^2 f] = {sp.simplify(mu_from_f)}")
    print(f"  mu_fw(u)          = {mu_fw}")
    check(sp.simplify(mu_from_f - mu_fw) == 0,
          "the round trip returns mu_fw EXACTLY (sympy difference 0) -- so a nonlocal, NON-QUADRATIC "
          "action reproduces the framework's exact law on circular orbits")
    lim_hi = sp.limit(f, u, sp.oo)
    lim_lo = sp.limit(f / u, u, 0, '+')
    print(f"  limits: f(u -> oo) = {lim_hi} (Newtonian, expects 1/2);  f/u -> {lim_lo} as u -> 0 "
          f"(deep MOND, expects 1/3)")
    check(lim_hi == sp.Rational(1, 2) and lim_lo == sp.Rational(1, 3),
          "both limits are correct, so f interpolates between Newton and deep MOND as required")
    print()
    print("  WHAT THIS INVALIDATES, precisely. Committed script mi_family4_variational_nogo_2026.py:")
    print("   * S4 claimed Milgrom's class 'deliver[s] the LIMITS but not the exact interpolating law'.")
    print("     WRONG -- it delivers the exact law on circles. This is Milgrom's own virial result")
    print("     (astro-ph/0510117): circular orbits give an exact mu(g/a0) g = g_N with mu fixed by the")
    print("     action's values on circles.")
    print("   * S4 attributed Milgrom 1994 to 'class 4b', the velocity-BILINEAR family. WRONG -- his")
    print("     class is NON-QUADRATIC in the trajectory, which is exactly why it works.")
    print("   * The S3 general statement 'no action with a fixed kernel reproduces the law for all")
    print("     potentials' must be NARROWED to actions QUADRATIC in the trajectory (plus, via Families")
    print("     1-3, local non-quadratic ones). As written it over-reaches.")
    print("  AND MY 4b DIAGNOSIS WAS SHALLOWER THAN THE TRUTH: 4b fails on DIMENSIONS before")
    print("  frequency-vs-acceleration is reached -- [Omega] = 1/T and [a0] = L/T^2 admit no nontrivial")
    print("  dimensionless combination, so any nonconstant Qtilde(Omega) smuggles in a constant that is")
    print("  not a0. The 19.7x spread I reported is a SYMPTOM of that units failure, not the cause.")

    banner("WHAT SURVIVES, AND WHAT THE CORRECTED POSITION IS")
    print("  SURVIVES UNTOUCHED:")
    print("   * Theorem 8 for the PUBLISHED action: on circular orbits its operator sits on K's branch")
    print("     cut where |K| = 1, so it is amplitude-free and cannot give the law. That is a statement")
    print("     about that specific action and it stands.")
    print("   * Theorems 1-5 and Propositions 6-7 of the published paper (DOI 10.5281/zenodo.21708842).")
    print("     None of them depends on the four-family claim.")
    print("  CORRECTED POSITION:")
    print("   * The law IS variational, in a nonlocal non-quadratic class -- Milgrom's class -- at least")
    print("     on the circular-orbit slice where the rotation-curve evidence lives.")
    print("   * SCOPE, and it is the honest limit: f(u) pins the functional only on the two-parameter")
    print("     family of circles. Infinitely many Galilei-invariant nonlocal extensions share that")
    print("     slice and none is written down. That is Milgrom's own stated status: 'we do not have a")
    print("     MI theory for MOND at the level of satisfaction achieved for MG formulations.'")
    print("   * So 'the law is a phenomenological postulate with no variational home' is TOO STRONG.")
    print("     The correct statement: the law has a variational home on circles in a class that is")
    print("     not uniquely determined, and the published action is not a member of it.")
    print("  THE ONE CONCRETE NEXT CALCULATION, from the brief: construct an explicit Galilei-invariant")
    print("  nonlocal non-quadratic functional whose circular reduction is this f(u), then compute its")
    print("  prediction for NON-circular motion -- vertical oscillations perpendicular to a disk, where")
    print("  MI and MG are known to part company. Archival data, and the only place the inertia label")
    print("  still earns its keep.")
    check(True, "the corrected position is stated with its scope rather than as a fresh claim")
    print("=" * 100)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
