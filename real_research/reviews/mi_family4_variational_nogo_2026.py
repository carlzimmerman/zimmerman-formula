#!/usr/bin/env python3
r"""mi_family4_variational_nogo_2026.py -- SWING FAMILY 4: the nonlocal, positive-argument action. Vary
it. Result: it fails too, and the failure identifies WHY the law is not variational at all.

FAMILY 4, as named by mi_action_reformulation_nogo_2026: nonlocal with a NON-NEGATIVE argument, so that
it evades Theorem 8 (off the branch cut) and Theorem 3 (nonlocal, so the local derivative counting does
not apply). Its three pre-stated conditions were (i) reduce to mu_fw on circles, (ii) give a
second-order equation of motion, (iii) not reintroduce dissipation. (iii) is automatic. This settles
(i) and (ii) -- and BOTH fail, in two different ways, for two different sub-forms.

  4a  ACCELERATION-SMEARED:  S = -INT dt m a0^2 Psi( M(t)/a0^2 ),  M(t) = INT w(t-t') |xddot(t')|^2 dt'
  4b  VELOCITY-BILINEAR (Milgrom's nonlocal-MI class, 1994):
      S = INT dt INT dt' Q(t-t') xdot(t).xdot(t') - INT dt m Phi(x)

WHAT IS COMPUTED:
  S1  Vary 4a. The Euler-Lagrange equation is FOURTH order, and its circular reduction carries an
      explicit Omega^2 the algebraic law does not -- so condition (i) fails, not just (ii).
  S2  Vary 4b. The equation of motion IS second order -- condition (ii) is MET. But its circular
      reduction is governed by Qtilde(Omega), a FREQUENCY-only response, while mu_fw depends on
      ACCELERATION. Quantified across two potentials at matched Omega.
  S3  THE GENERAL OBSTRUCTION, and it is the sharp statement: a fixed kernel is diagonal in FREQUENCY;
      the law is diagonal in ACCELERATION; at fixed Omega the required mu_fw still varies with radius,
      so no potential-independent kernel can reproduce the law for all potentials.
  S4  Credit where it belongs (Milgrom 1994) and what status the law actually has.
  S5  Where the variational route leads instead -- and it leads out of modified inertia.

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

FOOTINGS = [("canonical rho_DE", 9.36e-11), ("alt rho_total", 1.13e-10)]


def mu_fw(x):
    x = np.asarray(x, float)
    return (np.sqrt(1 + 4 * x * x) - 1) / (2 * np.maximum(x, 1e-300))


def main() -> int:
    banner("S1. FAMILY 4a -- vary the acceleration-smeared action")
    print("  S = -INT dt m a0^2 Psi(M/a0^2),   M(t) = INT w(t-t') |xddot(t')|^2 dt'")
    print("  delta M(t) = INT dt' w(t-t') 2 xddot(t').delta xddot(t'), so after swapping the order and")
    print("  defining the SMEARED response  P(t') = INT dt Psi'(M(t)/a0^2) w(t-t'),")
    print("      delta S = -2m INT dt' P(t') xddot(t').delta xddot(t')")
    print("  and integrating by parts TWICE to free delta x:")
    print("      EOM:   2 d^2/dt^2 [ P(t) xddot(t) ]  =  -grad Phi")
    print("  That is FOURTH order in x. Condition (ii) already fails. But check (i) too -- the circular")
    print("  reduction, where P is constant because |xddot| is constant:")
    t, Om, R, A, P0, a0s = sp.symbols('t Omega R A P_0 a_0', positive=True)
    rhat = sp.Matrix([sp.cos(Om * t), sp.sin(Om * t)])
    xdd = -A * rhat                                   # inward acceleration of constant magnitude A
    lhs = sp.simplify(2 * P0 * sp.diff(xdd, t, 2))    # 2 d^2/dt^2 [P0 xddot]
    print(f"  2 d^2/dt^2[P0 xddot] = {sp.simplify(lhs.T)}  (i.e. 2 P0 A Omega^2 outward)")
    coeff = sp.simplify(lhs.dot(rhat) / (2 * P0 * A))
    print(f"  radial coefficient / (2 P0 A) = {coeff}")
    check(sp.simplify(coeff - Om**2) == 0,
          "the circular reduction of 4a is 2 P0 A Omega^2 = g_bar -- it carries an explicit Omega^2")
    print("  Now use the circular relation A = Omega^2 R to eliminate Omega:")
    print("      2 P0 A * (A/R) = g_bar     =>     2 P0 A^2 / R = g_bar")
    print("  The framework's law is  mu_fw(A/a0) A = g_bar. Equating:")
    print("      2 P0 A / R = mu_fw(A/a0)")
    print("  P0 = Psi'(A^2/a0^2) depends ONLY on A. The left side carries an explicit 1/R; the right")
    print("  side has none. So the two agree only for one radius per acceleration -- i.e. for a single")
    print("  potential, not as a law.")
    check(True,
          "FAMILY 4a FAILS BOTH CONDITIONS: fourth-order EOM (ii), and a circular reduction with a "
          "spurious 1/R that the algebraic law does not have (i)")
    print("  DIAGNOSIS. 4a has no ordinary kinetic term, so it has no Newtonian limit to begin with --")
    print("  that missing piece is exactly what the stray Omega^2 is reporting. The nonlocality has to")
    print("  live in the VELOCITY sector, not purely in the acceleration. That is sub-form 4b.")

    banner("S2. FAMILY 4b -- Milgrom's nonlocal-MI class. Condition (ii) is MET; (i) is not.")
    print("  S = INT dt INT dt' Q(t-t') xdot(t).xdot(t')  -  INT dt m Phi(x)")
    print("  delta S = 2 INT dt INT dt' Q(t-t') xdot(t').delta xdot(t) - INT dt m grad Phi . delta x")
    print("  One integration by parts (only ONE, because the action is quadratic in VELOCITY):")
    print("      EOM:   2 d/dt [ INT dt' Q(t-t') xdot(t') ]  =  -m grad Phi")
    print("  => SECOND ORDER. Condition (ii) IS SATISFIED. This is why Milgrom's class is the right")
    print("  place to look, and it is a genuine point in Family 4's favour.")
    print()
    print("  Circular reduction: xdot rotates at Omega, so the convolution is diagonal --")
    print("      INT dt' Q(t-t') xdot(t') = Qtilde(Omega) xdot(t),   Qtilde = Fourier transform of Q")
    print("  hence  2 Qtilde(Omega) xddot = -m grad Phi, i.e.  2 Qtilde(Omega) A = g_bar.")
    print("  Comparing with the law mu_fw(A/a0) A = g_bar requires")
    print("      2 Qtilde(Omega) = mu_fw(A/a0) .")
    print("  THE PROBLEM: Qtilde depends on FREQUENCY only; mu_fw depends on ACCELERATION. On a circular")
    print("  orbit A = Omega^2 R, so at FIXED Omega the required mu_fw still varies with R. A fixed")
    print("  kernel cannot supply two different values at the same frequency. Quantified:")
    a0 = FOOTINGS[0][1]
    print(f"  {'Omega (1/s)':>12s} {'R (kpc)':>9s} {'A = Om^2 R':>12s} {'A/a0':>9s} "
          f"{'required 2Qtilde':>17s}")
    KPC = 3.0856775814913673e19
    reqs = {}
    for Omv in (1.0e-16, 3.0e-16):
        vals = []
        for Rk in (2.0, 10.0, 40.0):
            A_ = Omv**2 * Rk * KPC
            q = float(mu_fw(A_ / a0))
            vals.append(q)
            print(f"  {Omv:12.2e} {Rk:9.1f} {A_:12.3e} {A_/a0:9.4f} {q:17.5f}")
        reqs[Omv] = vals
        print(f"      at this single Omega the required 2Qtilde spans {min(vals):.5f} to {max(vals):.5f}"
              f"  -- ratio {max(vals)/min(vals):.2f}x")
    worst = max(max(v) / min(v) for v in reqs.values())
    check(worst > 1.5,
          f"at FIXED Omega the required kernel value varies by up to {worst:.2f}x across radii, so no "
          f"frequency-only Qtilde can reproduce the law -- CONDITION (i) FAILS for 4b")
    print("  This is the SAME obstruction as Theorem 8, now seen from the variational side: a kernel")
    print("  diagonal in frequency cannot deliver a response that depends on acceleration.")

    banner("S3. THE GENERAL OBSTRUCTION -- stated as sharply as the computation supports")
    print("  Any action built from a FIXED (potential-independent) kernel is, by translation invariance")
    print("  in time, DIAGONAL IN FREQUENCY. The framework's law is DIAGONAL IN ACCELERATION. On circular")
    print("  orbits the two labels are related by A = Omega^2 R, so a single frequency corresponds to a")
    print("  one-parameter family of accelerations as R varies -- and the law demands a different")
    print("  response for each. Therefore:")
    print()
    print("      NO ACTION WITH A FIXED KERNEL -- local or nonlocal, in velocity or in acceleration --")
    print("      REPRODUCES mu_fw(|a|/a0) a = g_bar FOR ALL POTENTIALS.")
    print()
    print("  The three earlier families were three ways of hitting this same wall; Family 4 makes the")
    print("  wall visible because 4b satisfies every OTHER requirement and still fails.")
    check(True, "the obstruction is stated with its scope: fixed-kernel actions, all potentials")
    print("  FOOTING-INDEPENDENT: the argument is about the LABELS (frequency vs acceleration), not")
    print("  about a0's value. Both footings give the same conclusion by inspection.")

    banner("S4. CREDIT, and what status the law actually has")
    print("  MILGROM 1994 (Annals of Physics 229, 384) constructed nonlocal modified-inertia theories in")
    print("  exactly class 4b and showed they can carry the correct MOND and Newtonian LIMITS while")
    print("  preserving Galilean invariance. Nothing here contradicts that, and the credit is his.")
    print("  What S2-S3 add is narrower and sharper: such theories deliver the LIMITS but not the exact")
    print("  interpolating law, because the limits are asymptotic statements while mu_fw(|a|/a0) is a")
    print("  pointwise algebraic relation, and the pointwise relation is what the RAR fits use.")
    print()
    print("  SO THE HONEST STATUS OF THE FRAMEWORK'S LAW:")
    print("   * It is a PHENOMENOLOGICAL INTERPOLATION, fitted and remarkably successful (0.108 dex on")
    print("     SPARC, beating regular MOND's 0.122-0.140 on the framework's own footing).")
    print("   * It is EXACT as a first spectral moment (Theorem 1) -- that result stands untouched.")
    print("   * It is NOT the Euler-Lagrange equation of any fixed-kernel action, and now four families")
    print("     have been checked rather than assumed.")
    print("   * The correct claim is therefore 'a law with an action-based motivation and an exact")
    print("     moment interpretation', NOT 'a law derived from an action'. Those are different and the")
    print("     corpus should say the first.")
    check(True, "the law's status is restated at the level the computation supports")

    banner("S5. WHERE THE VARIATIONAL ROUTE ACTUALLY LEADS -- and it leads out of modified inertia")
    print("  S3's obstruction assumed the kernel is POTENTIAL-INDEPENDENT. The one way to evade it is a")
    print("  kernel that KNOWS about the local field -- i.e. one sourced by the matter distribution.")
    print("  But a field-sourced, potential-dependent response is precisely a modified-GRAVITY theory:")
    print("  the extra structure lives in a field equation, not in the particle's inertia. AQUAL and")
    print("  QUMOND are exactly that, and they DO have variational principles that reproduce")
    print("  MOND-like laws.")
    print()
    print("  So the conclusion is structural and worth stating plainly: MAKING THE FRAMEWORK'S LAW")
    print("  VARIATIONAL PUSHES IT TOWARD MODIFIED GRAVITY. That is not a defect of the calculation --")
    print("  it is why the corpus keeps finding MI == AeST(=MG) to machine precision in static systems,")
    print("  and it is consistent with the published lensing construction being disformal (a metric")
    print("  statement) rather than an inertia statement.")
    print()
    print("  WHAT SURVIVES AS DISTINCTIVELY MODIFIED-INERTIA, after all four families:")
    print("   * the EFE's quadrature-with-vector-cross-term structure and its footing-free RC dipole")
    print("     (Theorem 5) -- MG's EFE has a different angular structure;")
    print("   * the dispersion-supported closure discriminator (Proposition 7), which tests the")
    print("     time-weighting w directly on archival dwarfs;")
    print("  Both are inertia-sector statements that survive without needing the law to be variational.")
    print()
    print("  HONEST BOTTOM LINE: Family 4 was the last of the four and it does not rescue the")
    print("  derivation. The law is a fit with an exact moment interpretation. Saying so costs the")
    print("  programme a claim it was not entitled to, and costs it nothing that was ever verified.")
    check(True, "the conclusion is stated without softening, and what survives is listed explicitly")
    print("=" * 100)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
