#!/usr/bin/env python3
"""
PROJECT 6c: RETRACTING the 6b 'CMB breakthrough' -- it was wrong. The CMB does not constrain rising a0.
======================================================================================================
Last turn project 6b claimed a gas-independent CMB test that 'strongly disfavors' rising a0 (a ~5x linear
over-driving of the acoustic peaks). On harder examination that is an ERROR, and integrity requires
retracting it as plainly as it was asserted. This file documents the mistake, the correct AeST physics, and
the corrected conclusion: AeST's CMB-safety is STRUCTURAL and holds for rising a0 -- there is NO clean
gas-independent CMB constraint on a0(z). Project 6 (the 2nd-order 'tension') shared the same bad premise.
This is the verify-before-asserting discipline applied to my own exciting result. Needs nothing but text.
"""


def the_error():
    print("="*92); print("THE ERROR IN 6b"); print("="*92)
    print("""  6b applied the GALAXY MOND boost nu = sqrt(a0/g) ~ 24 to the CMB acoustic perturbations, concluding
  the baryon self-gravity is over-driven ~5x at recombination. That boost is REAL for a galaxy -- because a
  galaxy SOURCES an order-1 scalar field, so the MOND invariant Y = (grad phi)^2 is order 1 and J(Y)=Y^{3/2}
  is an order-1 modification. It is NOT valid for the CMB, where the scalar is a tiny PERTURBATION.\n""")


def the_correct_physics():
    print("="*92); print("THE CORRECT AeST PHYSICS"); print("="*92)
    print("""  In AeST the MOND kinetic invariant is Y = q^{mu nu} d_mu phi d_nu phi, with q^{mu nu} = g^{mu nu} +
  A^mu A^nu the projector ORTHOGONAL to the unit-timelike aether A. So Y is the SPATIAL gradient of phi.
    * BACKGROUND (homogeneous phi = phibar(t)): the spatial gradient vanishes -> Ybar = 0.
    * PERTURBATION: Y = (grad delta-phi)^2 -> SECOND order in perturbations.
    * MOND term: J(Y) = Y^{3/2} = |grad delta-phi|^3 -> THIRD order in perturbations.
  So the MOND term contributes to the CMB at THIRD order -- utterly negligible -- and this is true REGARDLESS
  of the value (or evolution) of a0. The deep-MOND REGIME (g_acoustic/a0 << 1) is real, but for a SMALL
  perturbation 'deep MOND' means Y^{3/2} of a tiny number = even tinier, not a 24x amplification. The
  amplification 6b invoked requires an order-1 sourced field (a galaxy), which the CMB perturbations are not.\n""")


def aest_design():
    print("="*92); print("WHY AeST IS BUILT THIS WAY (a0 is a galaxy-sector quantity)"); print("="*92)
    print("""  AeST cleanly separates two functions:
    * K(Q): the COSMOLOGICAL function. Q has a background value (~phidot), so K(Q) drives the background and
      the linear CMB -- it is what makes the scalar mimic cold dark matter. The CMB lives here.
    * J(Y): the MOND function. Ybar = 0, so J(Y) is a quasi-static GALAXY effect, higher-order cosmologically.
      a0 lives HERE.
  So a0 is structurally a galaxy-sector parameter; the linear CMB (the K(Q) sector) is BLIND to it. Making a0
  rise (a0 in J) does not touch the CMB, because J is third-order in CMB perturbations. AeST's CMB-safety is
  a structural identity, and rising a0 inherits it. (Even implementing the framework's a0~sqrt(rho) by making
  a0(t) time-dependent inside J leaves J third-order -> still CMB-safe.)\n""")


def verdict():
    print("="*92); print("PROJECT 6c VERDICT -- 6b retracted"); print("="*92)
    print("""  The 'gas-independent CMB test that disfavors rising a0' (6b) is WITHDRAWN. The CMB does NOT cleanly
  constrain a0(z): a0 is a galaxy-sector (J(Y)) quantity, the linear CMB is the K(Q) sector, and J(Y) is
  third-order in CMB perturbations because Ybar=0. Project 6's '2nd-order tension/discriminator' shared the
  same wrong premise (it expanded Y^{3/2} about a nonzero Ybar) and is likewise overstated -- the true leading
  CMB effect of a0 is third-order, negligible. So there is NO existing-data CMB shortcut to the verdict.
  CONSEQUENCE FOR THE STANDING: the empirical case reverts to what the galaxy data say -- gas-limited and
  inconclusive, central leaning constant (projects 10b-d). Rising a0 is NOT additionally disfavored by the
  CMB; it is also not rescued by it. The decisive test remains the gas-clean #17 measurement.
  META: this is the discipline working on my own work -- an exciting 'breakthrough' asserted one turn, found
  wrong the next, and retracted as plainly as it was claimed. Better a withdrawn result than a fabricated one.""")
    print("="*92)


def main():
    print("#"*92); print("# PROJECT 6c -- retracting the 6b CMB 'breakthrough' (it was wrong)"); print("#"*92 + "\n")
    the_error(); the_correct_physics(); aest_design(); verdict()


if __name__ == "__main__":
    main()
