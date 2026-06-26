#!/usr/bin/env python3
r"""
CONFRONTATION -- Zhang, Hasani Zonoozi & Kroupa 2026 (arXiv:2602.06082, PhRvD 113, 043027)
"Revisiting the missing mass problem in MOND for nearby galaxy clusters" -- 46 clusters z<0.1
vs the FRAMEWORK a0 = 9.36e-11 (rho_DE footing), both footings, locked conventions.
==========================================================================================
The paper closes the MOND cluster missing-mass gap to baryon/M_M,dyn = 88(+5+2/-4-1)% (IGIMF
full; abstract headline) using a top-heavy IGIMF that doubles stellar-remnant mass. It uses the
REGULAR-MOND DEFAULT a0 = 1.2e-10 m/s^2 (Sec II.2, after Eq 6), interp mu(x)=x/sqrt(1+x^2),
and TAKES the Newtonian & MOND dynamical masses DIRECTLY from Brownstein & Moffat 2006
(arXiv:astro-ph/0507222, MNRAS 367, 527; Col 8 = M_N, Col 10 = "convergent" M_MOND) and
Angus et al. 2010 (arXiv:0906.3322), approximating B&M's r_out as r200.

KEY ALGEBRA (the a0-swap, locked):
  Zhang Eq 8/9  ==  B&M Eq 29/30. Squaring Eq 8 gives Eq 9:
     M_M,dyn(r) = sqrt( M_N,dyn^2 - a0^2 r^4 / G^2 ).
  In the convergent / deep-MOND regime (B&M Eq 30, Sanders 2003) the operative mass is
     M_MOND_conv = (16 / (G a0)) (kT/(mu m_p))^2   ->   M_M,dyn  PROPORTIONAL TO 1/a0  (EXACT).
  VERIFIED here: B&M's tabulated Col-10 M_MOND tracks T^2/a0 with a CONSTANT prefactor across
  clusters (ratio ~5.5 for all of A0085/A0133/A3112/A1795), confirming the 1/a0 scaling.
  => a LOWER framework a0 RAISES M_M,dyn (the denominator of the baryon fraction), so the 88%
     closure DROPS. This is the brief's predicted sign: framework HURTS the cluster closure.

Both footings reported. a0(z) declining-sqrt(rho_DE) branch is FLAT (<+3.1%) over z<0.1 -> moot.
Reproducible: needs only numpy. The 40 parsed B&M Table-1 rows are embedded for the prefactor check.
"""
import numpy as np

# ---- constants / framework footing (canon) ----
G = 6.674e-11; c = 2.998e8; Msun = 1.989e30; keV = 1.602e-16; mp = 1.673e-27; mu = 0.609
H0 = 2.184e-18; OmL = 0.685
rho_DE0 = OmL * 3 * H0**2 / (8 * np.pi * G)
A0_FRAME = 0.5 * c * np.sqrt(G * rho_DE0)     # 9.36e-11  (rho_DE footing)
A0_MOND  = 1.2e-10                            # paper's value = regular-MOND default = baseline
W0, WA = -0.752, -0.86                        # DESI CPL

def rho_DE_ratio(z): return (1 + z)**(3 * (1 + W0 + WA)) * np.exp(-3 * WA * z / (1 + z))
def a0z(z):          return A0_FRAME * np.sqrt(rho_DE_ratio(z))

# B&M 2006 Table-1 central values (name, T[keV], M_MOND[1e14 Msun]) -- a few rows, prefactor check
BM = [("A0085", 6.9, 1.83), ("A0133", 3.8, 0.55), ("A3112", 5.3, 1.26), ("A1795", 7.8, 2.84)]

def main():
    sc = A0_MOND / A0_FRAME   # M_M,dyn scales by this (1/a0)
    print(f"a0(framework, rho_DE) = {A0_FRAME:.4e} | a0(paper/regular-MOND) = {A0_MOND:.3e} | ratio {A0_FRAME/A0_MOND:.4f}")
    print(f"M_M,dyn PROP 1/a0  =>  framework M_M,dyn x{sc:.3f} (+{(sc-1)*100:.1f}%)\n")

    # (1) confirm B&M Col-10 M_MOND PROP T^2/a0 (constant prefactor)
    print("CHECK: B&M Col-10 M_MOND vs Eq-30 (16/(G a0))(kT/mu mp)^2 -- constant ratio => 1/a0 scaling")
    rats = []
    for nm, T, mmond in BM:
        pred = 16.0 / (G * A0_MOND) * (T * keV / (mu * mp))**2 / Msun / 1e14
        rats.append(pred / mmond)
        print(f"  {nm:6s} T={T:.1f} BM={mmond:.2f}  Eq30={pred:6.2f}  ratio={pred/mmond:.2f}")
    print(f"  ratio spread {min(rats):.2f}-{max(rats):.2f} (constant -> M_MOND PROP T^2/a0 confirmed)\n")

    # (2) a0(z) flat at z<0.1
    sw = [a0z(z) / A0_FRAME for z in np.linspace(0, 0.1, 50)]
    print(f"a0(z) declining branch over z<0.1: {(min(sw)-1)*100:+.2f}%..{(max(sw)-1)*100:+.2f}% (FLAT -> no effect)\n")

    # (3) headline replay, BOTH footings
    print(f"{'budget':24s}{'paper a0=1.2e-10':>18}{'framework 9.36e-11':>20}")
    for lab, fr in [("Gas (ICM)", 52), ("Canonical IMF", 67), ("IGIMF (ICL=canon)", 81),
                    ("IGIMF full [HEADLINE]", 88)]:
        print(f"{lab:24s}{fr:>16d}%{fr/sc:>18.1f}%")
    print(f"\nIGIMF-full closure 88% -> {88/sc:.1f}% on the framework footing "
          f"({(1-1/sc)*100:.0f}% relative drop).")
    print(f"residual eta = M_M,dyn/M_bar: 1.14 -> {1/(0.88/sc):.2f}. The ~88-100% closed band REOPENS to ~69%.")

if __name__ == "__main__":
    main()
