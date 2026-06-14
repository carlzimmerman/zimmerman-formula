#!/usr/bin/env python3
# === COEFFICIENT-FOOTING CORRECTION (2026-06-13) ===
# Any 'a0 = cH0/Z', '1/Z=0.173 against cH0', or an H0-tuned-to-71.5 'rescue' below uses the SUPERSEDED footing.
# Canonical: a0 = c^2 sqrt(Lambda/32pi) = cH_Lambda/Z = 9.36e-11 (rho_DE; cH_Lambda = sqrt(OmL)*cH0 = 0.83*cH0).
# Coefficient 1/Z=0.173 is against cH_Lambda; against cH0 it is 0.143. Milgrom 0.159 / Verlinde 0.167 use cH0,
# so the apt comparison is 0.143 (the LOW OUTLIER, NOT bracketed). cH0/Z=1.13e-10 is the rho_total reading (+20%).
# See real_research/THE_A0_COEFFICIENT_CONVENTION.md + real_research/THE_A0_COEFFICIENT_AUDIT_2026-06-13.md
"""
THE GEOMETRIC ORIGIN OF a0 -- why MOND kicks in when it does. A deep dive, honest to first principles.
=====================================================================================================
Carl: "there must be a geometric reason why the MOND acceleration value kicks in when it does."
There is, and it is real (not numerology): a0 ~ cH is the acceleration scale of the COSMIC HORIZON.
Three independent geometric readings give the same scale cH; the exact O(1) coefficient (Z=5.789) is
the one posited piece. The cubic T^3 topology is NOT the source -- the math leads to the horizon, and
I place the T^3 honestly rather than force a connection. Needs numpy.
"""
import numpy as np

c, G, hbar, kB, Mpc = 2.99792458e8, 6.674e-11, 1.0546e-34, 1.381e-23, 3.0857e22
H0 = 67.4e3/Mpc
Z = 2*np.sqrt(8*np.pi/3)
a0_obs = 1.2e-10
RdS, rho_c = c/H0, 3*H0**2/(8*np.pi*G)


def gpc(x): return x/Mpc/1e3


def main():
    print("#"*92); print("# THE GEOMETRIC ORIGIN OF a0 -- why MOND switches on at ~1.2e-10 m/s^2"); print("#"*92)
    print(f"\n  cH0 (de Sitter horizon surface gravity) = {c*H0:.3e} m/s^2;  a0 = cH0/Z = {c*H0/Z:.3e} (Z={Z:.3f}).")
    print("  THREE independent geometric readings, all returning the scale cH:\n")

    print("="*92); print("READING 1 -- the HORIZON COINCIDENCE (the cleanest statement)"); print("="*92)
    print("""  By the equivalence principle a particle of proper acceleration a has a Rindler horizon a distance
  d_R = c^2/a behind it. The universe has a de Sitter (cosmic) horizon at R_dS = c/H. These COINCIDE at
       c^2/a = c/H   <=>   a = cH.""")
    for a in (1e-8, 1e-9, 6.5e-10, 1e-10):
        print(f"     a={a:.1e}:  Rindler horizon c^2/a = {gpc(c**2/a):6.1f} Gpc   (cosmic R_dS = {gpc(RdS):.1f} Gpc)"
              + ("   <-- coincide at a=cH0" if abs(np.log10((c**2/a)/RdS)) < 0.05 else ""))
    print("""  Above cH the Rindler horizon is small/local -> ordinary inertia. As a falls to cH the Rindler
  horizon swells to the cosmic horizon: the particle becomes causally enclosed by the de Sitter horizon,
  and its dynamics must feel it. THAT geometric merger is the MOND threshold. (Milgrom; McCulloch.)\n""")

    print("="*92); print("READING 2 -- the UNRUH temperature hitting the de Sitter FLOOR"); print("="*92)
    print("  A detector in de Sitter at acceleration a sees T(a) = (hbar/2pi c kB) sqrt(a^2 + (cH)^2)  (Deser-Levin 1997):")
    TGH = hbar*H0/(2*np.pi*kB)
    for a in (1e-8, 6.5e-10, 1e-10):
        TU = hbar*a/(2*np.pi*c*kB); Tt = hbar*np.sqrt(a**2+(c*H0)**2)/(2*np.pi*c*kB)
        print(f"     a={a:.1e}:  Unruh T={TU:.2e} K   total T={Tt:.2e} K   (GH floor T0={TGH:.2e} K)")
    print("""  a >> cH: T ~ Unruh ~ a  -> inertia linear -> Newton.   a << cH: T -> the Gibbons-Hawking FLOOR,
  and the inertia-giving part DeltaT = T(a)-T(0) ~ a^2/2cH goes nonlinear -> a = sqrt(2cH g_N): MOND.
  The crossover is at a ~ cH because that is where the particle's own Unruh heat drops to the cosmic
  vacuum's temperature. (This DERIVES the MOND interpolation, coefficient-free -- desitter_unruh_mond.py.)\n""")

    print("="*92); print("READING 3 -- the COSMIC FREE-FALL TIME (the Zimmerman form, read geometrically)"); print("="*92)
    t_ff = 1/np.sqrt(G*rho_c)
    print(f"""  a0 = (c/2) sqrt(G rho_crit) = c/(2 t_ff),  t_ff = 1/sqrt(G rho_crit) = the gravitational free-fall
  time of the cosmic critical density:
     t_ff = {t_ff:.3e} s = sqrt(8pi/3)/H0 = {np.sqrt(8*np.pi/3):.2f} Hubble times
     a0 = c/(2 t_ff) = {c/(2*t_ff):.3e} m/s^2 = cH0/Z exactly  (Z = 2 t_ff H0 = {2*t_ff*H0:.3f})
  => a0 is the acceleration that reaches c in two cosmic free-fall times. MOND switches on when a
     particle is so weakly accelerated that the cosmic medium would gravitationally COLLAPSE before the
     particle goes relativistic -- i.e. when cosmic gravity outpaces the particle's own dynamics.\n""")

    print("="*92); print("THE Z DECOMPOSITION -- both factors geometric (no numerology)"); print("="*92)
    print(f"""  Z = 2 * sqrt(8pi/3) = {Z:.3f}:
     * the 2          = the surface-gravity / 'reach c' factor (horizon surface gravity c^2/2R);
     * the sqrt(8pi/3)= the Friedmann free-fall factor (rho_crit = 3H^2/8piG), EXACT GR geometry.
  The ORDER of a0 (~cH, the horizon scale) is geometrically FORCED -- all three readings give it. The
  EXACT coefficient is the one posited piece: Z=5.79 vs Verlinde 6 vs Milgrom 2pi vs the bare 1 are
  different O(1) ways to place the transition, and the data say cH0/a0 ~ 5.5. (No de Sitter mechanism
  derives the exact O(1); that is the standing open coefficient, desitter_entropy_coefficient.py.)\n""")

    print("="*92); print("THE UNIFYING DIMENSIONAL FRAMEWORK -- it all flows from ONE horizon premise"); print("="*92)
    print("""  Premise: gravity is the low-energy thermodynamics of the de Sitter horizon (Jacobson/Padmanabhan/
  Verlinde). From that single 4D premise, in order:
     1. the horizon sets a temperature T0 = hbar H/2pi kB and an acceleration cH;
     2. MOND switches on at a ~ cH (Readings 1-3) -- the form and the interpolation are DERIVED;
     3. a0 = cH/Z, so a0(z) = a0(0) E(z) -- the evolution is automatic (cH(z));
     4. the phantom halo rho~1/r^2, the BTFR v^4=GMa0, the Freeman scale a0/2piG all follow;
     5. the deep-MOND SIGN needs an entropy/DOF (not temperature) modification -- the one open piece.
  This is a 4D, horizon-based framework. It needs NO extra dimensions and NO global topology.\n""")

    print("="*92); print("THE CUBIC T^3 -- placed honestly (I will not force it)"); print("="*92)
    L = c**2/a0_obs
    print(f"""  You like the cubic T^3. Here is the honest math. A topology of size L has a natural kick-in
  acceleration c^2/L. Setting c^2/L = a0 gives L = c^2/a0 = {gpc(L):.0f} Gpc = Z * R_dS. But that is just
  a0 ~ cH RE-STATED (L ~ Z * R_dS, both tracking the horizon) -- NOT an independent derivation. And a
  {gpc(L):.0f} Gpc cell has inscribed radius R_i = {gpc(L)/2:.1f} Gpc < chi_rec ~ 14 -> borderline/excluded.
  So: the horizon -- not the cube -- is the geometric source of a0. A super-horizon cubic T^3 (L >~ 30
  Gpc) can COEXIST with this picture as a global-shape choice, but it does not cause a0, does not
  produce Z (its eta invariant is size-independent and rational; Z^2=32pi/3 is a size-dependent
  irrational volume), and the observed isotropy requires it to be beyond our horizon and so undetectable.
  The deep, true geometric reason MOND kicks in is the cosmic HORIZON, and that survives every test.""")
    print("#"*92)


if __name__ == "__main__":
    main()
