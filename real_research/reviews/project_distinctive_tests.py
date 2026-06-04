#!/usr/bin/env python3
"""
What actually distinguishes the framework from LambdaCDM -- and where to push next.
==================================================================================
Key reorganizing fact (A0Z_STATUS_CORRECTED.md): a0 EVOLVES and rises ~x3 from z=0 to z=2, but LambdaCDM hydro
sims (Mayer 2023) give the SAME x3. So the a0(z) evolution is NOT a framework-vs-LCDM discriminator -- both
predict it. The framework's distinctive, LCDM-impossible content is the MODIFIED-GRAVITY signatures and the
a0-H0 coefficient link. Those are where the next push belongs.

DISTINCTIVE #1 -- the EXTERNAL FIELD EFFECT (the cleanest LCDM-killer).
  LambdaCDM obeys the strong equivalence principle: a uniform external field does NOT affect a system's internal
  dynamics (shell theorem for the halo). NO EFE. MOND/this framework VIOLATE it: internal gravity is modified by
  nu(g_ext/a0). Chae et al. (2020/2021) DETECT the EFE in SPARC at ~4-5 sigma (the RAR turns down at low
  acceleration for galaxies in strong external fields, as MOND predicts and LCDM forbids). Our own SPARC EFE
  test was systematics-limited (inconclusive, not a refutation). => the single most distinctive evidence, and it
  currently FAVORS the framework.

DISTINCTIVE #2 -- the deep-MOND BOOST in wide binaries (z=0, no dark matter, no cosmology).
  LambdaCDM: 0% (pure Newton at ~kAU). Framework: a small, EFE-suppressed boost. The framework's DERIVED (sharp)
  interpolation predicts the SMALL end (~5%), between LCDM (0) and standard-MOND simple-mu (~18%). Gaia DR4
  decides. A clean force-law test with no dark sector at all.

DISTINCTIVE #3 -- the a0-H0 COEFFICIENT LINK: a0 = cH0/Z, Z = 2 sqrt(8pi/3).
  LambdaCDM has NO relation between a0 (a galaxy-formation outcome) and H0 (cosmic). The framework predicts they
  are one quantity. It EXPLAINS the old a0 ~ cH0 coincidence that LCDM treats as accidental. Not yet sharp
  (observed a0 = 1.2 +- 0.26 => H0 = 72 +- 15, spans the Hubble tension); decisive test = a 6% a0 + 1% H0.

THE REDIRECT: stop testing a0(z) (shared with LCDM, established). Push the EFE (re-do Chae's test with the
framework's derived interpolation + environment data), the wide-binary boost (Gaia DR4), and the a0-H0
coefficient (precise a0 + H0). Those are the LCDM-impossible predictions -- the framework's real distinctive
content. Needs numpy.
"""
import numpy as np

c = 2.998e8; Mpc = 3.086e22; Z = 2*np.sqrt(8*np.pi/3)


def nu_simple(y):   return (1+np.sqrt(1+4/y))/2
def nu_standard(y): return np.sqrt((1+np.sqrt(1+4/y**2))/2)


def main():
    print("#"*90)
    print("# Framework vs LambdaCDM: the DISTINCTIVE tests (a0 evolution is shared -- dropped)")
    print("#"*90 + "\n")

    print("="*90); print("#1  EXTERNAL FIELD EFFECT -- LCDM-impossible (strong equivalence principle); Chae 4-5 sigma"); print("="*90)
    print("  LCDM: no EFE (shell theorem). Framework/MOND: internal gravity modified by nu(g_ext/a0).")
    print("  Detected in SPARC (Chae 2020/21, ~4-5 sigma); our SPARC test inconclusive (systematics). FAVORS framework.\n")

    print("="*90); print("#2  WIDE-BINARY deep-MOND boost -- z=0, no dark matter (Gaia DR4 decides)"); print("="*90)
    y = 1.86
    print(f"  LCDM: 0%.  standard MOND (simple mu)+EFE: +{(np.sqrt(nu_simple(y))-1)*100:.0f}%."
          f"  framework derived (sharp): +{(np.sqrt(nu_standard(y))-1)*100:.0f}% (its specific small call).\n")

    print("="*90); print("#3  a0-H0 COEFFICIENT LINK: a0 = cH0/Z (LCDM: no relation)"); print("="*90)
    for H0 in (67.4, 71.5, 73.0):
        print(f"  H0={H0}: framework predicts a0 = {c*(H0*1e3/Mpc)/Z/1e-10:.3f}e-10")
    H0c = Z*1.2e-10/c*Mpc/1e3; H0e = Z*0.26e-10/c*Mpc/1e3
    print(f"  observed a0=1.2+-0.26 -> H0 = {H0c:.0f}+-{H0e:.0f} (spans the tension). Explains a0~cH0; decisive: 6% a0 + 1% H0.\n")

    print("="*90); print("THE REDIRECT"); print("="*90)
    print("""  a0(z) rising ~x3 is now established AND shared with LambdaCDM (Mayer 2023 sims), so it no longer tests the
  framework against the mainstream. The framework's real, LCDM-impossible content is: the EXTERNAL FIELD EFFECT
  (detected, Chae 4-5 sigma -- strongest current evidence), the WIDE-BINARY deep-MOND boost (Gaia DR4), and the
  a0-H0 COEFFICIENT link (explains the coincidence; needs precise a0+H0). The next push belongs there, not on
  more a0(z).""")
    print("="*90)


if __name__ == "__main__":
    main()
