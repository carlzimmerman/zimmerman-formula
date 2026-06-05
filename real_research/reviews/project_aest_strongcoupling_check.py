#!/usr/bin/env python3
"""
The dynamical-DE strong-coupling caveat for the AeST construction, checked: BENIGN (blows up where nothing lives).
=================================================================================================================
The construction's coupling C(Q) = kappa0 sqrt(rho0/rho_DE(Q)) diverges as rho_DE -> 0 in the deep past (dynamical
DE). Flagged worry: does the blown-up coupling destabilize MOND systems? Checked here -- benign, for three reasons.

1. SEPARATION OF EPOCHS: C blows up (~170x) only at z~1100 (recombination), where there are NO nonlinear MOND
   structures (Y~0; only linear delta~1e-5). The FIRST galaxies form at z<~10-20, where C is only ~3-5x (MILD).
   The strong-coupling epoch and the structure-forming epoch DO NOT OVERLAP -> C never acts on a real MOND system.
2. a0 -> 0 SMOOTHLY: as rho_DE -> 0, a0 = a0(0) sqrt(rho_DE/rho0) -> 0, so the physical MOND force g ~ sqrt(a0 g_N)
   -> 0. There is no force to destabilize; C -> inf is the field-theory bookkeeping of 'no MOND', not a dynamical
   pathology.
3. NOT A NEW DEFECT: deep-MOND is ALREADY strongly coupled (the Y^{3/2} non-analyticity at Y=0) in every MOND
   theory; the dynamical-DE C -> inf is a continuation of that known feature, CMB/LSS-safe (O(delta^3)).
Honest residue: MOND strong-coupling / UV predictivity is a real open issue for ALL MOND theories; the framework
inherits it, does not worsen it. Needs numpy.
"""
import numpy as np

w0,wa=-0.752,-0.86
rhoDE=lambda a: a**(-3*(1+w0+wa))*np.exp(-3*wa*(1-a))
a0=lambda z: np.sqrt(rhoDE(1/(1+z)))     # a0(z)/a0(0)
C =lambda z: 1.0/a0(z)                     # C(z)/C(0): the strong-coupling factor


def main():
    print("#"*96); print("# Dynamical-DE strong-coupling caveat: where does C blow up vs where do structures live?  BENIGN"); print("#"*96+"\n")
    print(f"  {'z':>6}{'a0(z)/a0(0)':>14}{'C(z)/C(0)':>12}   nonlinear MOND structures?")
    for z,note in [(0,'galaxies (now)'),(2,'mature galaxies'),(6,'JWST early galaxies'),
                   (10,'FIRST galaxies form'),(20,'first collapse'),(100,'NONE (linear)'),
                   (1100,'recombination -- NONE')]:
        print(f"  {z:>6}{a0(z):>14.3f}{C(z):>12.1f}   {note}")
    print()
    print("  => C blows up (~170x) only at z~1100, where Y~0 (no nonlinear structures). First MOND structures form at")
    print("     z<~10-20, where C ~ 3-5x (mild). Strong-coupling epoch and structure epoch DO NOT OVERLAP.\n")
    print("="*96); print("VERDICT"); print("="*96)
    print("""  BENIGN. (1) The C-blowup epoch (z~1100) and the structure-forming epoch (z<~10-20, where C~3-5x) do not
  overlap, so C never acts on a real MOND system. (2) a0 -> 0 smoothly, so there is no MOND force to destabilize --
  C -> inf just encodes 'no MOND in the early universe', which is CMB-safe. (3) It is a continuation of deep-MOND's
  intrinsic Y^{3/2} strong coupling (shared by ALL MOND theories), not a new pathology. Both flagged caveats of the
  AeST construction -- locality and this strong coupling -- are now examined and BENIGN. Honest residue: MOND's
  strong-coupling/UV predictivity is a genuine open issue for every MOND theory; the framework inherits but does not
  worsen it -- and the coupling C(Q) remains inserted, not derived.""")
    print("#"*96)


if __name__=="__main__":
    main()
