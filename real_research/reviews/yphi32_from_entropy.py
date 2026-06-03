#!/usr/bin/env python3
"""
THE FRONTIER -- can the Y^{3/2} MOND term be DERIVED from horizon entropy?
=========================================================================
This is the one genuinely open, paper-length step. We do the real thing: reconstruct the only
existing route (Verlinde 2016, 'Emergent Gravity and the Dark Universe'), which derives the
deep-MOND sqrt-law -- hence the Y^{3/2} kinetic power -- from the entropy of de Sitter space,
and we mark precisely what is derived, what is CONTESTED, and what is still open. No claim is
made beyond what the calculation supports. Needs numpy.
"""
import numpy as np

c, G, hbar, kB, Mpc = 2.99792458e8, 6.674e-11, 1.0546e-34, 1.381e-23, 3.0857e22
H0 = 67.4e3/Mpc


def part1_scale_from_entropy():
    print("="*86)
    print("PART 1 [DERIVED, scale] -- a0 ~ cH is the de Sitter ENTROPY/temperature scale")
    print("="*86)
    R_dS = c/H0
    S_dS = np.pi*R_dS**2*c**3/(G*hbar)        # de Sitter horizon entropy A/4G (in units of kB)
    T_dS = hbar*H0/(2*np.pi*kB)               # de Sitter temperature
    a_from_T = 2*np.pi*c*kB*T_dS/hbar         # acceleration whose Unruh T equals T_dS: a=cH
    print(f"  de Sitter horizon: R_dS=c/H={R_dS:.2e} m, entropy S_dS=A/4G={S_dS:.2e} (x kB),")
    print(f"     temperature T_dS=hbar H/2pi kB = {T_dS:.2e} K.")
    print(f"  The acceleration whose Unruh temperature equals T_dS is a = cH = {a_from_T:.2e} m/s^2.")
    print(f"  => the ENTROPY/temperature of the cosmic horizon sets the scale a0 ~ cH (Z=O(1)).")
    print(f"     observed a0=1.2e-10 => Z=cH0/a0={c*H0/1.2e-10:.1f}. The SCALE is entropic; the O(1) is the posit.\n")


def part2_sqrt_law_from_displacement():
    print("="*86)
    print("PART 2 [DERIVED-but-CONTESTED] -- the sqrt law (=> Y^{3/2}) from entropy displacement")
    print("="*86)
    print("""  Verlinde's argument (reconstructed):
    (i)  de Sitter space carries, besides the area-law horizon entropy, a BULK entropy that scales
         with VOLUME: S_DE(r) ~ (r/L_dS) x (area entropy), L_dS=c/H. This 'dark energy' entropy
         behaves like an incompressible elastic medium of modulus set by a0~cH.
    (ii) Baryonic mass M REMOVES entropy from this medium (matter = order). The removed entropy
         delta S_M ~ M c^2 / T_dS is DISPLACED outward, straining the medium.
    (iii)The elastic restoring response to the strain is an EXTRA acceleration g_D ('apparent dark
         matter'). Balancing the displaced volume of entropy against the strain energy gives, in
         the deep regime, Verlinde's relation
                      g_D(r) = sqrt( a0 * g_B(r) ),     a0 = cH,  g_B = G M/r^2.
         i.e. the MOND sqrt law DROPS OUT of entropy displacement -- not assumed.""")
    # numerical check: for a galaxy, g_D=sqrt(a0 g_B) reproduces a flat rotation curve
    a0 = c*H0/(2*np.pi)                        # Verlinde's de Sitter coefficient Z=2pi
    M = 6e10*1.989e30; kpc = 3.0857e19
    print(f"\n  Check (Verlinde a0=cH/2pi={a0:.2e}): g_D=sqrt(a0 g_B) for M=6e10 Msun:")
    print(f"     {'r[kpc]':>8}{'g_B':>11}{'g_D=sqrt(a0 g_B)':>18}{'v=sqrt(g_D r)[km/s]':>20}")
    for rk in (10, 30, 100):
        r = rk*kpc; gB = G*M/r**2; gD = np.sqrt(a0*gB); v = np.sqrt(gD*r)
        print(f"     {rk:>8}{gB:>11.2e}{gD:>18.2e}{v/1e3:>18.0f}")
    print("     -> flat rotation curve, v=(G M a0)^(1/4): the BTFR, from ENTROPY. [the deep-MOND core]\n")


def part3_connect_to_Y32():
    print("="*86)
    print("PART 3 [DERIVED, the link] -- sqrt law  <=>  L ~ Y^{3/2}  (the kinetic term)")
    print("="*86)
    print("""  A scalar with action INT f(Y), Y=(grad phi)^2, sources a point-mass field grad phi ~
  rho^{1/(2n-1)} for f~Y^n (Part-5 of clean_slate_field_theory.py). The entropy-derived deep-MOND
  law g_D ~ sqrt(g_B) ~ sqrt(rho) is the 1/2 power, forcing 2n-1=2 -> n=3/2. Therefore the
  entropy-displacement sqrt law IS the field-theoretic statement  L ~ Y^{3/2}  ( = |grad phi|^3,
  the AQUAL cubic). So: de Sitter ENTROPY -> sqrt law -> Y^{3/2}. The MOND kinetic POWER is
  derived (modulo Verlinde's contested premises), with a0 set by the de Sitter temperature.\n""")


def part4_KQ():
    print("="*86)
    print("PART 4 [OPEN] -- the cosmological function K(Q)")
    print("="*86)
    print("""  AeST needs a SECOND function, K(Q) (Q a temporal-derivative scalar of the same fields),
  whose job is to make the cosmological background + linear perturbations behave like CDM (so the
  CMB and growth match). The entropy-displacement argument is QUASI-STATIC and galaxy-scale; it
  says nothing about K(Q). In the entropy picture K(Q) should be the de Sitter bulk entropy's
  CONTRIBUTION TO THE BACKGROUND (the 'dust' mode = the unstrained dark-energy medium acting as a
  pressureless fluid), but deriving its exact form from entropy is NOT done. This is the larger,
  more open half of the problem.\n""")


def part5_ledger():
    print("="*86); print("FRONTIER LEDGER -- the honest state of Y^{3/2}/K(Q)-from-entropy"); print("="*86)
    print("""  [DERIVED]   a0 ~ cH as the de Sitter entropy/temperature scale (Part 1).
  [DERIVED]   the link: deep-MOND sqrt law <=> Y^{3/2} kinetic power (Part 3).
  [DERIVED-but-CONTESTED] the sqrt law itself from de Sitter entropy DISPLACEMENT (Verlinde 2016,
              Part 2). Real, and it gives the BTFR -- but it rests on premises that are NOT
              established: (a) a VOLUME-law bulk entropy for de Sitter (most derivations give only
              the area law); (b) modelling dark energy as a linear ELASTIC medium; (c) the
              quasi-static, spherical, deep-regime approximation. Many relativists reject (a)-(b).
              So the Y^{3/2} term is derivable IF Verlinde's entropy picture is right -- a real but
              unsettled IF.
  [OPEN]      a clean COVARIANT derivation (not the heuristic elastic medium); the full
              INTERPOLATION function (Verlinde gives only the deep tail); and K(Q), the cosmological
              sector (Part 4). These are the genuine, paper-length unsolved pieces.

  BOTTOM LINE: the frontier is PARTIALLY bridged. The MOND kinetic POWER Y^{3/2} and the scale
  a0~cH DO follow from de Sitter horizon entropy via Verlinde's displacement argument -- so the
  framework's deep-MOND term is not arbitrary; it has an entropic origin. But that origin is
  CONTESTED (the volume-law entropy) and INCOMPLETE (no covariant form, no interpolation, no K(Q)).
  Closing it -- a rigorous, covariant, uncontested entropy derivation of the FULL Y^{3/2}+K(Q)
  structure -- is exactly the open research program, now stated to the term. It is real physics
  with a real literature (Jacobson, Padmanabhan, Verlinde, Skordis-Zlosnik), and zero numerology.""")
    print("="*86)


def main():
    part1_scale_from_entropy(); part2_sqrt_law_from_displacement(); part3_connect_to_Y32()
    part4_KQ(); part5_ledger()


if __name__ == "__main__":
    main()
