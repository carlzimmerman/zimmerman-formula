#!/usr/bin/env python3
"""
PROJECT 14: wide binaries -- the single highest-stakes test of whether there is an a0 at all.
=============================================================================================
Wide binaries (separations ~2000-30000 AU) reach internal accelerations ~ a0 with NO dark matter possible
(too small to hold a halo). So they test pure MOND vs Newton directly. Chae (2023+) reports a ~20% low-
acceleration boost consistent with MOND; Banik (2024) reports a 16-19 sigma NULL (Newtonian). This file
lays out, with numbers, WHY the test is hard (the Galactic external field puts them in mild EFE, so the
predicted signal is only ~15-20%), WHY the two camps disagree, and what Gaia DR4 resolves. No Gaia data in
repo -> this is the physics + the decision protocol. Needs numpy.
"""
import numpy as np

G, Msun, kpc, AU, c = 6.674e-11, 1.989e30, 3.0857e19, 1.496e11, 2.998e8

# Framework a0 = (c/2) sqrt(G rho_Lambda) = c^2 sqrt(Lambda/32pi): the dark-energy-fixed
# acceleration scale, NOT textbook MOND's 1.2e-10. rho_Lambda = Omega_Lambda * rho_crit.
H0, Omega_Lambda = 2.184e-18, 0.685          # H0 in s^-1 (=67.4 km/s/Mpc); Planck Omega_Lambda
rho_crit = 3 * H0**2 / (8 * np.pi * G)
rho_Lambda = Omega_Lambda * rho_crit
a0 = (c / 2) * np.sqrt(G * rho_Lambda)       # = 9.36e-11 m/s^2 (kappa=1/2, pure-Lambda)


def main():
    print("#"*92); print("# PROJECT 14 -- wide binaries: is there an a0 at all?"); print("#"*92 + "\n")
    g_ext = (230e3)**2/(8.2*kpc)
    print("="*92); print("THE REGIME -- why the predicted signal is small"); print("="*92)
    print(f"  Galactic external field at the Sun:  g_ext = V^2/R = {g_ext:.2e} = {g_ext/a0:.2f} a0.")
    print(f"  So wide binaries are NOT isolated deep-MOND -- they sit in a MILD external field ~{g_ext/a0:.1f} a0, which")
    print(f"  SUPPRESSES the MOND boost. Internal acceleration vs separation:")
    for s in (2000, 5000, 10000, 20000):
        gi = G*1.5*Msun/(s*AU)**2
        print(f"     s={s:>6} AU:  g_int = {gi:.2e} = {gi/a0:5.2f} a0")
    print(f"""  At the s~5000-20000 AU sweet spot, g_int ~ a0 ~ g_ext/{g_ext/a0:.1f}. The predicted MOND excess in orbital
  velocity is therefore only ~15-20% -- a small signal riding on top of large astrophysical confusion.\n""")

    print("="*92); print("WHY CHAE AND BANIK DISAGREE (it is systematics, not the gravity law)"); print("="*92)
    print("""  Both use Gaia; the ~20% effect is small enough that the answer is set by sample construction:
    * UNDETECTED TERTIARIES: a hidden third star inflates the velocity and FAKES a MOND boost. Chae models
      and subtracts them; Banik argues the residual contamination still drives Chae's signal.
    * ECCENTRICITY PRIOR: the deprojection from sky-plane to 3D velocity depends on the assumed e-distribution;
      different priors shift the inferred boost by ~the size of the signal.
    * THE EFE ITSELF: whether g_ext is added scalar or vector, and its exact value, changes the predicted
      amplitude by tens of percent.
  So this is a measurement-systematics fight, not (yet) a clean law test -- exactly the situation where more
  and better data decides.\n""")

    print("="*92); print("WHAT GAIA DR4 RESOLVES + WHERE IT BEARS ON THE FRAMEWORK"); print("="*92)
    print("""  DR4 brings: more astrometric epochs (tighter proper motions), epoch RVs (third velocity component +
  tertiary flags), and better faint-end completeness (cleaner triple rejection). That is precisely the data
  needed to kill the tertiary + eccentricity systematics and turn ~20% into a clean detection or a clean null.
  FRAMEWORK STAKES: this is the most direct test of whether an a0 EXISTS in a regime with no dark-matter
  escape hatch. A clean MOND-consistent boost is strong support for the whole premise (is MOND real? -> yes);
  a clean Newtonian null at the EFE-corrected prediction would be the most serious single blow to it. The
  framework's rising a0 does NOT change the LOCAL (z=0) wide-binary prediction -- so this tests the FOUNDATION,
  not the distinctive bet. Either way it is the highest-leverage 'is there an a0' experiment now running.""")
    print("="*92)


if __name__ == "__main__":
    main()
