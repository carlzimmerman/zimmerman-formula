#!/usr/bin/env python3
"""
PROJECT 6: the second-order CMB signature of evolving a0 -- a DISCRIMINATOR and an honest TENSION.
=================================================================================================
Linear CMB C_l are a0-free in AeST (delta q^00 = 0; the peaks are driven by the K(Q) dust mode, not the
MOND part). So the a0 physics enters the CMB only at SECOND order, through the NON-ANALYTIC J(Y)=Y^3/2
term. This file does two rigorous things: (1) determines the MOND REGIME at recombination for rising vs
constant a0 -- they are OPPOSITE; (2) derives the second-order coupling from Y^3/2 and shows the
non-analyticity AMPLIFIES it in the deep-MOND (small-Ybar) regime. Net: a potential discriminator AND a
potential tension for the rising-a0 reading, both flagged honestly. Needs numpy.
"""
import numpy as np

c, G, Mpc = 2.99792458e8, 6.674e-11, 3.0857e22
H0, Om, OL = 67.4e3/Mpc, 0.315, 0.685
a0 = 1.2e-10
E = lambda z: np.sqrt(Om*(1+z)**3 + OL)
zrec = 1100


def part1_regime():
    print("="*92); print("PART 1 -- [rigorous] which MOND regime is recombination in? Rising vs constant a0"); print("="*92)
    Phi = 3e-5; lam = 147*Mpc/(1+zrec)            # acoustic sound-horizon wavelength, physical
    g_ac = 2*np.pi/lam*Phi*c**2                    # g ~ k Phi c^2 on the first acoustic scale
    ar, ac = a0*E(zrec), a0
    print(f"""  The MOND modification turns on when the perturbation's gravitational acceleration g < a0(z). On the
  first acoustic scale at recombination, g_ac ~ k Phi c^2 = {g_ac:.2e} m/s^2 (Phi~3e-5, lambda=r_s/(1+z)).
  Compare to a0 at recombination under each reading [E(z_rec)={E(zrec):.2e}]:
     RISING  a0(z_rec) = a0 E(z_rec) = {ar:.2e}  ->  g_ac/a0 = {g_ac/ar:.1e}   => DEEP MOND
     CONST   a0(z_rec) = a0          = {ac:.2e}  ->  g_ac/a0 = {g_ac/ac:.1e}   => NEWTONIAN
  The two readings put recombination in QUALITATIVELY OPPOSITE regimes. Standard (constant-a0) MOND/AeST
  sits in the SAFE Newtonian regime there -- which is why AeST passes Planck. The framework's RISING a0
  drives recombination DEEP into MOND. That is the crux of this project.\n""")
    return g_ac


def part2_second_order():
    print("="*92); print("PART 2 -- [derivation] the second-order coupling, and why Y^3/2 amplifies it in deep MOND"); print("="*92)
    print("""  Expand the deep-MOND kinetic function J(Y)=Y^3/2 about the background Ybar (Y = Ybar + dY):
     J = Ybar^3/2 [ 1 + (3/2)(dY/Ybar) + (3/8)(dY/Ybar)^2 - (1/16)(dY/Ybar)^3 + ... ]
   * LINEAR term  (3/2)Ybar^1/2 dY : its CMB contribution is killed by AeST's delta q^00 = 0. So the
     linear C_l are a0-free -- established, and true for BOTH readings.
   * SECOND-ORDER term (3/8) Ybar^(-1/2) (dY)^2 : a source QUADRATIC in perturbations -> it generates a
     BISPECTRUM (CMB non-Gaussianity), the leading channel through which a0 touches the CMB.
  The NON-ANALYTICITY is the key: the coefficient (3/8) Ybar^(-1/2) DIVERGES as Ybar -> 0 -- and Ybar is
  SMALL precisely in the deep-MOND regime. So a reading that drives recombination deep into MOND (small
  Ybar) AMPLIFIES the second-order, non-Gaussian signal by Ybar^(-1/2). Rising a0 does exactly that.
  => rising a0 predicts a LARGER second-order CMB / non-Gaussian amplitude than constant a0. Rigorous in
     structure; the number needs a second-order Boltzmann code.\n""")


def part3_verdict(g_ac):
    print("="*92); print("PROJECT 6 VERDICT -- a discriminator AND an honest tension"); print("="*92)
    print(f"""  OPPORTUNITY (discriminator): the linear CMB cannot tell rising from constant a0 (both a0-free), but
  the SECOND-ORDER CMB can -- rising a0 (deep MOND at recombination, Ybar small) gives a larger
  non-Gaussian bispectrum than constant a0 (Newtonian at recombination). A second-order Boltzmann
  calculation + the Planck/CMB-S4 f_NL bounds is a real, independent test of the apparent-vs-event question.

  TENSION (honest risk to the framework): driving recombination DEEP into MOND is NOT obviously safe. It
  is protected at LINEAR order by delta q^00 = 0, but the amplified second-order term could overproduce
  CMB non-Gaussianity and run into the existing f_NL ~ O(1) bounds. Standard constant-a0 AeST avoids this
  by being Newtonian at recombination. So the framework's distinctive rising-a0 carries a distinctive CMB
  RISK that constant-a0 MOND does not -- this must be checked, not assumed away.

  HONEST STATUS: the linear CMB is safe (delta q^00=0). The second-order amplitude -- whether it is a
  detectable discriminator or a fatal overproduction -- is UNCOMPUTED here; it requires extending the
  Skordis-Zlosnik linear AeST analysis to second order. This is the single most important CMB calculation
  for the framework, and it could go either way. Flagging it openly is the point.""")
    print("="*92)


def main():
    print("#"*92); print("# PROJECT 6 -- second-order CMB: a0's only CMB channel, and what it risks"); print("#"*92 + "\n")
    g_ac = part1_regime(); part2_second_order(); part3_verdict(g_ac)


if __name__ == "__main__":
    main()
