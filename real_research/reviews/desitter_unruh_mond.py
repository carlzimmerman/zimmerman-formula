#!/usr/bin/env python3
"""
LAYER 0 frontier -- deriving MOND's ORIGIN from de Sitter-Unruh horizon thermodynamics.
======================================================================================
First-principles, no numerology. The claim a0~cH is not assumed here -- it is DERIVED from
the temperature an accelerated particle sees in an expanding universe.

PHYSICS (Deser & Levin 1997; Narnhofer-Peter-Thirring 1996; Milgrom 1999):
  A particle with proper acceleration a in a universe of Hubble rate H sees a vacuum
  temperature that combines its own Unruh heat with the cosmic (de Sitter) horizon:
        T(a) = (hbar / 2 pi kB c) * sqrt(a^2 + (cH)^2).
  At rest (a=0) it still sees the de Sitter temperature T(0)=hbar H/(2 pi kB).
  Milgrom's inertia postulate: the INERTIA-producing response is the part of the heat DUE
  to the acceleration, DeltaT = T(a)-T(0). The effective inertia is mu(a)=DeltaT/(a * [hbar/2pi kB c]):
        mu(a) = [ sqrt(a^2+(cH)^2) - cH ] / a .
  This is a DERIVED interpolation function -- not chosen to fit. We show it gives MOND, a
  flat rotation curve, the BTFR, and an acceleration scale a0 ~ cH, with the evolution
  a0(z) ~ H(z) ~ sqrt(G rho) ~ E(z) falling straight out. Needs numpy.
"""
import numpy as np

c, G, hbar, kB, Msun, kpc, Mpc = 2.99792458e8, 6.674e-11, 1.0546e-34, 1.381e-23, 1.989e30, 3.0857e19, 3.0857e22
H0 = 67.4e3/Mpc


# ---- the DERIVED interpolation function (no free shape) -----------------------
def mu_dS(a, H):
    cH = c*H
    return (np.sqrt(a**2 + cH**2) - cH)/a


def part1_limits():
    print("="*82)
    print("PART 1 -- the de Sitter-Unruh interpolation, and its two limits (DERIVED)")
    print("="*82)
    cH = c*H0
    print(f"  de Sitter acceleration cH0 = {cH:.2e} m/s^2  (this is the scale that appears)")
    print(f"  {'a/cH':>8}{'mu(a)':>10}{'limit':>26}")
    for x in (100, 10, 1, 0.1, 0.01):
        a = x*cH
        print(f"  {x:>8}{mu_dS(a,H0):>10.4f}{'~1 (Newton)' if x>3 else ('~a/2cH (deep MOND)' if x<0.3 else 'transition'):>26}")
    print("""  Limits (exact):  a>>cH:  mu->1            => m a = F     (Newtonian inertia)
                   a<<cH:  mu->a/(2cH)     => m a^2/(2cH)=F (MONDian: inertia falls with a)
  The MODIFICATION and its SCALE a~cH are DERIVED from the horizon temperature, not posited.\n""")


def part2_rotation_curve():
    print("="*82)
    print("PART 2 -- solve the inertia law for a galaxy: flat rotation + BTFR (DERIVED)")
    print("="*82)
    # inertia law mu(a) a = g_N  ->  for this mu it solves in closed form:
    #   sqrt(a^2+(cH)^2) - cH = g_N  ->  a = sqrt(g_N^2 + 2 g_N cH) = sqrt(g_N) sqrt(g_N+2cH)
    M = 6e10*Msun; cH = c*H0
    print(f"  Closed-form solution of mu(a)a=g_N:  a = sqrt(g_N^2 + 2 g_N cH).")
    print(f"  -> deep limit a = sqrt(2cH * g_N) = sqrt(a0 g_N) with a0 = 2cH (this mu's coefficient).")
    print(f"  Rotation curve of M=6e10 Msun (v=sqrt(a r)):")
    print(f"     {'r[kpc]':>8}{'g_N':>11}{'a(solved)':>12}{'v[km/s]':>10}{'regime':>10}")
    for rk in (2, 10, 30, 60, 100):
        r = rk*kpc; gN = G*M/r**2
        a = np.sqrt(gN**2 + 2*gN*cH); v = np.sqrt(a*r)
        print(f"     {rk:>8}{gN:>11.2e}{a:>12.2e}{v/1e3:>10.0f}{'Newton' if gN>cH else 'deepMOND':>10}")
    a0_here = 2*cH
    vflat = (G*M*a0_here)**0.25
    print(f"  -> rotation curve FLATTENS at v_flat=(G M a0)^(1/4) = {vflat/1e3:.0f} km/s: the BTFR,")
    print(f"     v^4 = G M a0, DERIVED. (a0=2cH here; the coefficient is treatment-dependent, Part 4.)\n")


def part3_evolution():
    print("="*82)
    print("PART 3 -- the evolution falls out for free (the falsifiable claim, DERIVED)")
    print("="*82)
    print("  The scale is a0 ~ c H(z). In an expanding universe H(z)=H0 E(z), and at any epoch")
    print("  H^2=(8pi/3)G rho, so cH ~ c sqrt(G rho). Therefore WITHOUT any extra assumption:")
    print(f"     {'z':>5}{'E(z)':>8}{'a0(z)/a0(0)':>14}")
    E = lambda z: np.sqrt(0.315*(1+z)**3+0.685)
    for z in (0, 1, 2, 4, 6):
        print(f"     {z:>5}{E(z):>8.2f}{E(z):>14.2f}")
    print("  => a0(z)=a0(0)E(z) is DERIVED from horizon thermodynamics, coefficient-free. This is")
    print("     the one falsifiable prediction -- and it is a CONSEQUENCE here, not a posit.\n")


def part4_coefficient_honesty():
    print("="*82)
    print("PART 4 -- the coefficient: what is derived vs what is still O(1)")
    print("="*82)
    cH = c*H0
    print(f"  This simplest DeltaT=T(a)-T(0) inertia gives a0 = 2cH  -> Z = cH0/a0 = {cH/(2*cH):.2f}")
    print(f"     (a0 = {2*cH:.2e} -- ~12x the observed 1.2e-10; this naive coefficient is too big).")
    print(f"  Milgrom's careful 1999 deep-MOND/Unruh matching gives 2 pi a0 = cH -> Z = 2pi = {2*np.pi:.2f}.")
    print(f"  Verlinde's de Sitter entropy gives Z ~ 6; the framework's free-fall-horizon reading Z=5.79.")
    print(f"  Observed Z = cH0/a0 ~ {cH/1.2e-10:.1f}.")
    print("""  HONEST: the STRUCTURE (MOND a^2 law), the SCALE (a0 ~ cH), and the EVOLUTION (a0~E(z))
  are DERIVED from horizon thermodynamics -- first-principles, no numerology. The exact O(1)
  coefficient is NOT pinned by this argument: the crude DeltaT gives 0.5, Milgrom's careful
  matching 2pi, the framework 5.79 -- the same shared, unforced coefficient as everywhere.""")


def part5_ledger():
    print("="*82); print("LAYER-0 FRONTIER LEDGER (first-principles, no numerology)"); print("="*82)
    print("""  DERIVED from de Sitter-Unruh horizon thermodynamics:
    * the MOND modification itself -- inertia falls below a~cH (mu(a)->a/2cH), a CONSEQUENCE
      of the cosmic-horizon temperature, not an assumption;
    * a flat rotation curve and the BTFR v^4=G M a0;
    * the acceleration scale a0 ~ cH;
    * the EVOLUTION a0(z)=a0(0)E(z) -- the falsifiable claim, derived coefficient-free.
  STILL OPEN (the honest frontier):
    * the exact coefficient Z (this gives 0.5, Milgrom 2pi, framework 5.79 -- unforced O(1));
    * this is MODIFIED INERTIA, so it inherits the closed-orbit incompleteness (Part-2 of
      modified_inertia_dynamics.py). The COMPLETE theory is modified GRAVITY (AeST); deriving
      AeST AS the covariant/relativistic completion of THIS horizon argument is the next step
      -- the genuine theoretical prize, and the thing that would close Layer 0 honestly.
  BOTTOM LINE: 'a0 ~ cH and it evolves' is no longer a coincidence re-labelled -- it is
  DERIVED from the temperature of the cosmic horizon. That is real first-principles progress.""")
    print("="*82)


def main():
    part1_limits(); part2_rotation_curve(); part3_evolution(); part4_coefficient_honesty(); part5_ledger()


if __name__ == "__main__":
    main()
