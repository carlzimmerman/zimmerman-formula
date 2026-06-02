#!/usr/bin/env python3
"""
The #1 open check, scoped honestly: does running a0 disturb the CMB at SECOND order?
===================================================================================

What is already SETTLED (do not re-litigate):
  * LINEAR CMB is exactly a0-independent. theta_3H_coupling.py [C] proves Ybar=0 on FRW,
    so the a0-term is O(dphi^3) -- absent from every linear equation; the theta-dressing
    (1/theta, thetabar=3Hbar!=0) does not lower that order. bridge1_linear_boltzmann.py
    confirms numerically: peak positions (r_s=144 Mpc, l_A=301) and the transfer function
    are a0-invariant. So running a0 does NOT move the peaks and does NOT change linear P(k).

What is OPEN (this file): the a0-term first acts at SECOND order in perturbations. Two facts
make that non-trivial rather than obviously negligible, and this file quantifies both:
  (1) a0 is ~2e4x LARGER at recombination (a0(z) = a0(0) E(z)); and
  (2) the MOND term is the NON-ANALYTIC Y^{3/2}, and the cosmological background sits exactly
      at Y=0 -- the non-analytic point -- so naive delta-power-counting is unreliable there.

DISCIPLINE (this is where overreach historically crept in):
  [SOLID]    proven / numerically verified elsewhere, restated.
  [ESTIMATE] an order-of-magnitude scaling; explicitly NOT a Boltzmann result.
  [OPEN]     a calculation I do NOT do and will not fake.
  [SPEC]     the exact computation that would close it.

Run:  python real_research/reviews/nonlinear_cmb_scoping.py
"""
import math

c = 2.99792458e8
Mpc = 3.0857e22
Z = 2 * math.sqrt(8 * math.pi / 3)
H0 = 67.4e3 / Mpc
OM, OL = 0.315, 0.685
A0_obs = 1.2e-10
z_rec = 1090.0
E = lambda z: math.sqrt(OM * (1 + z) ** 3 + OL)


def solid():
    print("=" * 78)
    print("[SOLID] linear order: settled, a0-independent")
    print("=" * 78)
    print("   * Ybar=0 on FRW => a0-term is O(dphi^3) => absent from linear EOMs (theorem).")
    print("   * peak positions r_s, l_A and the transfer T(k) are a0-free (bridge1 verified).")
    print("   => running a0 leaves the LINEAR CMB exactly invariant. Peaks do not move.\n")


def regime():
    print("=" * 78)
    print("[ESTIMATE] the recombination regime -- why 2nd order is not trivially zero")
    print("=" * 78)
    a0_rec = A0_obs * E(z_rec)
    print(f"   E(z_rec={z_rec:.0f}) = {E(z_rec):.0f};  a0(z_rec) = {a0_rec:.2e} m/s^2 "
          f"(~{E(z_rec):.0f}x today's a0)")
    # typical gravitational acceleration on acoustic scales at recombination:
    #   g ~ c^2 * Phi * k_phys,  Phi ~ 2e-5,  k_phys = k_comoving*(1+z_rec)
    Phi = 2e-5
    print(f"   typical acoustic-scale acceleration  g ~ c^2 * Phi * k_phys  (Phi~{Phi:.0e}):")
    print(f"     {'k_com[1/Mpc]':>13}{'k_phys[1/m]':>14}{'g[m/s^2]':>12}{'g/a0(z_rec)':>13}")
    for k_com in (0.02, 0.06, 0.2):                 # 1st peak .. damping tail (comoving)
        k_phys = k_com / Mpc * (1 + z_rec)
        g = c ** 2 * Phi * k_phys
        print(f"     {k_com:>13.2f}{k_phys:>14.2e}{g:>12.2e}{g / a0_rec:>13.2e}")
    print("   => CMB acoustic scales sit at g/a0 ~ 1e-4..1e-3: formally DEEP-MOND (g<<a0),")
    print("      because a0 is huge at recombination. That is exactly the Y->0 corner where")
    print("      the Y^{3/2} non-analyticity lives -- so the 2nd-order size is not reliably")
    print("      guessable by hand. It is small, but 'small' here needs the real calc.\n")


def size_estimate():
    print("=" * 78)
    print("[ESTIMATE] the plausible size of the 2nd-order CMB correction")
    print("=" * 78)
    print("   Generic 2nd-order CMB effects are suppressed ~ delta ~ 1e-5 vs linear. The a0")
    print("   term adds the ratio (MOND term)/(analytic kinetic) ~ sqrt(Y)/a0 ~ g/a0:")
    a0_rec = A0_obs * E(z_rec)
    Phi = 2e-5
    k_phys = 0.06 / Mpc * (1 + z_rec)
    g = c ** 2 * Phi * k_phys
    print(f"     g/a0(z_rec) ~ {g/a0_rec:.1e}  at the 1st-acoustic scale.")
    print("   So the leading a0-dependent correction to C_ell is plausibly ~1e-4..1e-3 in")
    print("   FRACTION -- i.e. 0.01%..0.1%. Planck measures C_ell to ~0.3-1% near the 3rd peak.")
    print("   VERDICT [ESTIMATE]: most likely BELOW Planck sensitivity (CMB survives), but it")
    print("   is within ~1 order of magnitude of it and the non-analyticity makes the estimate")
    print("   soft. NOT dismissible by hand -> the Boltzmann calc is genuinely required.\n")


def spec():
    print("=" * 78)
    print("[SPEC] the exact computation that closes this (un-faked)")
    print("=" * 78)
    print("   A CLASS/hi_class patch (NOT done here):")
    print("    1. add the unit-timelike aether A_mu + Lagrange multiplier lambda;")
    print("    2. implement F(Y,Q): the Y^{3/2} MOND term + K(Q)=-2L+K2(Q-Q0)^2 dust term;")
    print("    3. carry a0 = c*theta/(3Z) into the Y^{3/2} coefficient (theta=div A);")
    print("    4. evolve to 2ND order in perturbations (the linear order is a0-free, [SOLID]);")
    print("       handle the Y^{3/2} non-analyticity with the AeST quasi-static matching.")
    print("   OBSERVABLE + FALSIFIER:")
    print("    * compute C_ell^TT with running a0 vs constant a0; the discriminating number is")
    print("      the 3rd-peak height (the K(Q) dust tracer).")
    print("    * FALSIFIED if |Delta C_ell / C_ell| > Planck error (~0.3-1% near l~800).")
    print("    * If the shift is <~0.1% (the estimate), theta-coupled AeST inherits AeST's CMB")
    print("      fit WITH the evolving a0, and Bridge 1 closes. If not, the running is bounded")
    print("      by the CMB -- itself a real, publishable constraint on p.\n")


def main():
    solid()
    regime()
    size_estimate()
    spec()
    print("=" * 78)
    print("BOTTOM LINE")
    print("=" * 78)
    print("  Linear: rigorously safe -- the peaks do not move, T(k) unchanged ([SOLID]).")
    print("  2nd order: the a0-term switches on and is ~2e4x larger at recombination, but sits")
    print("  deep in the g<<a0 corner; the fractional CMB correction is ESTIMATED at ~1e-4..1e-3")
    print("  -- probably below Planck, not provably so. The honest status: most likely the CMB")
    print("  survives the running, and the decisive test is the 2nd-order Boltzmann run specified")
    print("  above. This is scoped, bounded, and falsifiable -- not claimed as already passed.")
    print("=" * 78)


if __name__ == "__main__":
    main()
