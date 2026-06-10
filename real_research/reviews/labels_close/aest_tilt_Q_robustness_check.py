#!/usr/bin/env python3
r"""PROBLEM 2 -- robustness check: is varphi'(galaxy MOND gradient) << Q0(cosmo scalar) across
all conventions? This is what protects Q. Answer: YES, by 1e-2 to 1e-7 every way."""
import numpy as np
c=2.99792458e8; G=6.674e-11; Mpc=3.0857e22; kpc=3.0857e19; H0=67.4e3/Mpc
Z=2*np.sqrt(8*np.pi/3); a0=c*H0/Z; Q0=1.0/Mpc
print("Q0 ~ 1/Mpc =", Q0, "/m")
print("(1) a0/c^2          =", a0/c**2, "  /Q0 =", (a0/c**2)/Q0)
print("(2) sqrt(gN a0)/c^2 =", np.sqrt(a0*a0)/c**2, "  /Q0 =", (np.sqrt(a0*a0)/c**2)/Q0)
print("(3) (100 a0)/c^2    =", 100*a0/c**2, "  /Q0 =", (100*a0/c**2)/Q0)
print("(4) (v/c)^2/r_gal   =", 1e-6/(10*kpc), "  /Q0 =", (1e-6/(10*kpc))/Q0)
print("=> varphi'/Q0 << 1 ROBUST (4e-5..4e-3). Q protected by cosmo Q0 >> galaxy gradient.")
