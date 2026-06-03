#!/usr/bin/env python3
"""
PROJECT 2: can the horizon foundation FORCE the AeST cosmological function K(Q)?
================================================================================
AeST (Skordis-Zlosnik 2021) has two free functions: J(Y) [the MOND/local part, ~Y^3/2 -- DERIVED from
the horizon in clean_slate_field_theory.py] and K(Q) [the cosmological part that makes the scalar mimic
COLD DARK MATTER: dust at the background, clusters at perturbation level, supplies Omega_DM~0.265]. The
clean-slate field theory forced ~80% of AeST (field content, q^munu=g+AA, CMB-safety, the Y^3/2 power).
K(Q) is the residual. Project 2 asks: is K(Q) forced by the horizon too, or is it a separate input?
This file gives the honest, quantitative answer -- and it is a NEGATIVE/scoping result, stated plainly.
Needs numpy.
"""
import numpy as np

Mpc = 3.0857e22
H0 = 67.4e3/Mpc
Om, OL = 0.315, 0.685
zrec = 1100


def main():
    print("#"*92); print("# PROJECT 2 -- is the AeST cosmological function K(Q) forced by the horizon?"); print("#"*92)
    print()
    print("="*92); print("THE TEST: what scale must K(Q) carry, and does the horizon supply it?"); print("="*92)
    print("""  K(Q) must make the AeST scalar behave like COLD DARK MATTER -- it has to cluster since EARLY
  times so the CMB acoustic peaks and the matter power spectrum come out right. A canonical scalar of
  mass m behaves like pressureless matter (oscillates) only once H drops below m. So the scale buried in
  K(Q) is a MASS, and that mass decides whether the scalar is dark MATTER or dark ENERGY.""")
    Hrec_over_H0 = np.sqrt(Om*(1+zrec)**3 + OL)
    print(f"""
  The ONLY scale the de Sitter horizon supplies is m ~ H0 (the Hubble/horizon scale). Test it:
    * a scalar with m ~ H0 starts oscillating at H ~ H0, i.e. at z ~ 0 (NOW). Before now it is frozen by
      Hubble friction -> equation of state w = -1 -> it behaves like DARK ENERGY, not dark matter. It
      does NOT cluster, so it cannot make the CMB peaks. The horizon scale gives the WRONG component.
    * to be cold dark matter it must already oscillate by recombination (z~{zrec}), i.e. m > H(z_rec):
         H(z_rec)/H0 = sqrt(Om(1+z)^3 + OL) = {Hrec_over_H0:.2e}
      so K(Q) needs a scale ~{Hrec_over_H0:.0e} x H0 -- four orders of magnitude ABOVE the horizon scale.""")
    print()
    print("="*92); print("VERDICT (a NEGATIVE result, stated honestly)"); print("="*92)
    print(f"""  The horizon forces the LOCAL MOND function J(Y) (a0~cH, the Y^3/2 power) but it does NOT force the
  cosmological function K(Q): the CDM-like mode K(Q) must carry a scale ~{Hrec_over_H0:.0e} H0, which the de
  Sitter horizon does not provide -- the horizon's own scale (H0) yields dark ENERGY, not dark matter.

  => K(Q) is the SEPARATE cosmological dark sector -- the framework's 'second dark thing' (galaxy phantom
     from J(Y), PLUS a cosmological clustering mode from K(Q)). Project 2 therefore does NOT close from
     the horizon alone. It REDUCES to Project 9 (is the cosmic dark mode ALSO emergent?), whose only known
     route is the CONTESTED volume-law de Sitter entropy (Verlinde 2016). Until that is settled, the honest
     statement is: the framework derives the MOND sector; the cosmological-CDM sector (K(Q)) is extra input.

  This is the right boundary to have mapped -- it says precisely how much of AeST the horizon buys (the
  ~80% J(Y) MOND part) and what it does not (the K(Q) cosmological dust), with no overclaim either way.""")
    print("="*92)


if __name__ == "__main__":
    main()
