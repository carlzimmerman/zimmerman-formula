#!/usr/bin/env python3
"""
PROJECT 9: the dark-sector budget -- does the framework supply Omega_DM, or is 'dark matter' two things?
=======================================================================================================
LambdaCDM's dark sector is two substances (CDM, Omega_DM~0.265; Lambda, Omega_L~0.685). What is the
framework's? This file states the honest structure: the dark sector is TWO ROLES OF ONE SCALAR (the AeST
field) -- a galaxy 'phantom' that is NOT an energy density (it is modified gravity) plus a cosmological
K(Q) dust mode that IS a real Omega_DM-supplying component. The framework EXPLAINS the galaxy-scale dark
matter but only RELOCATES the cosmological Omega_DM (its value stays fitted). No overclaim. Needs numpy.
"""
import numpy as np

Ob, Om, OL = 0.049, 0.315, 0.685
OnonbaryonicDM = Om - Ob


def main():
    print("#"*92); print("# PROJECT 9 -- the dark-sector budget, stated honestly"); print("#"*92 + "\n")

    print("="*92); print("THE TWO ROLES OF THE ONE SCALAR"); print("="*92)
    print(f"""  ROLE A -- the GALAXY PHANTOM (the J(Y) gradient mode). In a galaxy the MOND boost makes baryons move
  as if inside a dark halo of 'phantom' density rho_ph = (a0/4 pi G)/r^2 ... but rho_ph is NOT a real energy
  density: it is the modified-gravity RESPONSE to the baryons. It does not gravitate cosmologically, does
  not appear in the background Friedmann budget, and vanishes where baryons vanish. It is geometry, not stuff.

  ROLE B -- the COSMOLOGICAL DUST (the K(Q) mode). To make the CMB peaks and grow structure, the AeST scalar
  ALSO carries a mode that redshifts like pressureless matter (w=0) and supplies the cosmological
  Omega_DM ~ {OnonbaryonicDM:.3f}. This IS a real energy density. It is the 'second dark thing' that Project 2 found
  the horizon does NOT force (it needs a scale ~1e4 H0, which the horizon does not supply).
""")

    print("="*92); print("WHAT THIS DOES AND DOES NOT BUY"); print("="*92)
    print(f"""  EXPLAINED (a genuine win): the GALAXY-scale 'dark matter' is not a substance at all -- it is the
  phantom from modified gravity, with NO free density per galaxy (set by the baryons and a0). LambdaCDM
  needs a tuned halo per galaxy; the framework needs none. That is real economy where the data are best.

  ONLY RELOCATED (no win, stated plainly): the COSMOLOGICAL Omega_DM ~ {OnonbaryonicDM:.3f} is still an input -- it
  is now the amplitude of the K(Q) dust mode instead of a particle abundance, but its VALUE is fitted, not
  derived (Project 2: not from the horizon). The framework does not explain WHY Omega_DM ~ 0.265 any better
  than LambdaCDM explains the relic abundance. Same number, different shelf.

  ECONOMY vs LambdaCDM: comparable, arguably slightly better -- ONE field plays both dark roles (phantom +
  dust), where LambdaCDM has a separate CDM particle. But the cosmological abundance is equally unexplained.
""")

    print("="*92); print("PROJECT 9 VERDICT"); print("="*92)
    print(f"""  'Dark matter' in the framework is TWO ROLES OF ONE SCALAR: a galaxy phantom (modified gravity, not an
  energy density -- genuinely explained) and a cosmological K(Q) dust mode (a real Omega_DM~{OnonbaryonicDM:.2f} component,
  only relocated, its value still fitted). The framework SOLVES the galaxy-scale dark-matter problem and
  RE-PACKAGES, but does not solve, the cosmological dark-matter budget. The honest one-liner: the win is at
  galaxy scales (no halos), not in the cosmic census (Omega_DM is still put in by hand, via K(Q)).
  This closes the loop with Project 2 and is the truthful statement of what the dark sector costs.""")
    print("="*92)


if __name__ == "__main__":
    main()
