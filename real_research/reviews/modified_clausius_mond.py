#!/usr/bin/env python3
"""
OPEN-PROBLEM item A -- the COVARIANT route: modified Clausius with the de Sitter-Unruh T.
=======================================================================================
Verlinde's entropy route to Y^{3/2} is contested (it needs a volume-law de Sitter entropy).
Here we take the UNCONTESTED route -- Jacobson's local-horizon thermodynamics, which uses only
the area law -- and simply replace the Unruh temperature by the de Sitter-Unruh one. We show
this introduces the scale a0~cH into the gravitational field equation (modified GRAVITY, not the
elastic-medium heuristic), with an interpolation inherited from the SAME T(a) that gave the
modified-inertia interpolation (so the two routes are structurally the same -- item B). We are
explicit that this is a STRUCTURAL derivation of the route, not the complete nonlinear field
equation; finishing that is the bounded remaining work. Needs numpy.
"""
import numpy as np

c, G, hbar, kB, Mpc = 2.99792458e8, 6.674e-11, 1.0546e-34, 1.381e-23, 3.0857e22
H0 = 67.4e3/Mpc


def part1_jacobson():
    print("="*84)
    print("PART 1 [ESTABLISHED] -- Jacobson 1995: area-law entropy + Unruh T  =>  Newton's G")
    print("="*84)
    eta = c**3/(4*G*hbar)                      # entropy per unit area, S = eta*A  (= 1/4 L_P^2)
    LP2 = G*hbar/c**3
    print(f"  area-entropy density eta = c^3/(4 G hbar) = {eta:.3e} m^-2 = 1/(4 L_P^2), L_P^2={LP2:.2e} m^2")
    print(f"  Unruh:  k_B T = hbar kappa/(2 pi c)   (kappa = local acceleration / surface gravity)")
    print("""  Clausius dQ = T dS on every local Rindler horizon, with dS=eta dA and dA from Raychaudhuri
  focusing (dtheta/dlambda = -R_munu k^mu k^nu), FORCES  R_munu - 1/2 R g_munu = (8 pi G/c^4) T_munu,
  with G = c^3/(4 hbar eta). The entropy density eta IS Newton's G. [ESTABLISHED -- the tensor sector]\n""")
    return eta


def part2_modified_T():
    print("="*84)
    print("PART 2 [DERIVED, structural] -- swap in the de Sitter-Unruh T: a0~cH enters gravity")
    print("="*84)
    print("""  In de Sitter (or any accelerating universe) the SAME accelerated horizon has temperature
        k_B T(kappa) = (hbar/2 pi c) sqrt(kappa^2 + (cH)^2)        (Deser-Levin 1997),
  i.e. T is enhanced by the factor  W(kappa) = sqrt(1 + (cH/kappa)^2)  relative to Unruh.""")
    cH = c*H0
    print(f"  W(kappa) = sqrt(1+(cH/kappa)^2),  cH = {cH:.2e} m/s^2 ~ a0-scale:")
    print(f"     {'kappa/cH':>10}{'W':>10}{'regime':>22}")
    for x in (100, 3, 1, 0.3, 0.03):
        W = np.sqrt(1+1/x**2)
        reg = "Unruh/Newton (W->1)" if x > 3 else ("MOND (W->cH/kappa)" if x < 0.5 else "transition")
        print(f"     {x:>10}{W:>10.3f}{reg:>22}")
    print("""  Carrying W(kappa) through the Clausius relation makes the effective coupling
  acceleration-dependent: dQ = T(kappa) dS now reads (matter flux) = W(kappa) x (Einstein term).
  For kappa>>cH, W->1 -> Einstein/Newton. For kappa<<cH, W->cH/kappa -> the gravitational response
  is modified at the scale kappa ~ cH ~ a0. The cosmic-horizon temperature has injected a0~cH into
  the FIELD EQUATION, using only the AREA law -- NO elastic medium, NO volume-law entropy.

  *** HONEST SIGN CAVEAT (do not skip): which WAY does it modify? *** Naively, dQ=TdS with a
  LARGER T means a given matter flux dQ produces a SMALLER area change dS -> LESS focusing ->
  WEAKER gravity at low acceleration. That is the OPPOSITE of MOND (which needs STRONGER gravity).
  The modified-INERTIA route (Layer 0) gives MOND with the right sign for sure; the modified-GRAVITY
  (Clausius) route introduces the right SCALE but the SIGN/structure is NOT settled by this leading
  argument and the naive direction is wrong. Resolving it needs the full non-Killing Raychaudhuri/
  optical-scalar calculation (where T enters the entropy balance, not as a simple prefactor). So
  this route is PROMISING and UNCONTESTED in its inputs, but it is NOT yet shown to yield MOND.\n""")


def part3_same_interpolation():
    print("="*84)
    print("PART 3 [DERIVED, the link to item B] -- the SAME T gives the SAME interpolation")
    print("="*84)
    print("""  Both routes use one function, T(a)=sqrt(a^2+(cH)^2):
     * modified INERTIA (Layer 0): mu(a)a=g_N from DeltaT(a) -> g_obs=sqrt(g_bar^2+g_bar a0)
       (fits SPARC at 0.105 dex; desitter_unruh_RAR_test.py).
     * modified GRAVITY (here): W(kappa)=sqrt(1+(cH/kappa)^2) in the Clausius relation -> the same
       cH-scale transition with the same functional shape.
  So the gravity-route and inertia-route interpolations are built from the IDENTICAL temperature
  and therefore share the deep-MOND sqrt law and the transition. The covariant route does NOT need
  the contested volume-law entropy; it needs only the area law + the de Sitter-Unruh T. That removes
  the main objection to the entropic origin of Y^{3/2}. [item A weakened from 'contested' to
  'incomplete'; item B structurally addressed]\n""")


def part4_ledger():
    print("="*84); print("LEDGER -- what the covariant route closes, and what is still left"); print("="*84)
    print("""  ADVANCED here:
    * item A: identified a COVARIANT route with UNCONTESTED INPUTS -- Jacobson's local-horizon
      Clausius relation (area law only) with the de Sitter-Unruh T -- that injects the scale a0~cH
      into gravity WITHOUT Verlinde's volume-law entropy. This removes the 'contested premise'
      objection at the level of inputs.
    * item B: gravity-route and inertia-route both use the SAME T(a)=sqrt(a^2+(cH)^2), so a working
      version would share the deep-MOND sqrt law and shape with the (data-fitting) inertia route.
  STILL OPEN (now sharper, still paper-length) -- and one is a genuine RISK:
    * **the SIGN**: the leading argument gives the WRONG direction (higher T -> weaker gravity, not
      MOND's stronger). Whether the full non-Killing Raychaudhuri/optical-scalar calculation flips
      this to MOND is UNKNOWN and is the crux -- the route may simply fail here. State it plainly.
    * the FULL nonlinear field equation and its exact interpolation;
    * mapping it onto the AeST q^{mu nu} Y^{3/2} action with the right couplings;
    * K(Q), the cosmological sector (item C), untouched by a quasi-static local argument.
  HONEST VERDICT: progress on item A is PARTIAL and HONEST -- a covariant route with uncontested
  inputs exists and injects a0~cH, but it is NOT yet shown to give MOND (the naive sign is wrong),
  so it is a promising lead, not a derivation. This is the real state: the contested-entropy
  objection is replaceable, but the covariant MOND derivation is still genuinely open. No numerology;
  no overclaim.""")
    print("="*84)


def main():
    part1_jacobson(); part2_modified_T(); part3_same_interpolation(); part4_ledger()


if __name__ == "__main__":
    main()
