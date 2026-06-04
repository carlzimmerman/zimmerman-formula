#!/usr/bin/env python3
"""
CALCULATION OFFENSIVE on the Zimmerman formula: a0(z) = cH(z)/Z = c^2 sqrt(Lambda/32pi), Z=2sqrt(8pi/3).
=======================================================================================================
Every distinctive quantitative consequence of the EVOLVING, GEOMETRIC a0 -- the things that separate THIS
formula from constant-a0 MOND -- computed from first principles with hard numbers. Deep-MOND relations used:
  BTFR        V_flat^4 = G M_b a0          -> V proportional to a0^(1/4) proportional to E(z)^(1/4)
  Faber-Jack  sigma^4  = (4/9) G M a0       -> sigma proportional to E(z)^(1/4)
  Freeman     Sigma_M  = a0/(2 pi G)        -> Sigma proportional to E(z)
  phantom DM  rho_ph proportional to sqrt(a0)-> rho proportional to sqrt(E(z))
  MOND radius r_M = sqrt(GM/a0)             -> r_M proportional to 1/sqrt(E(z))
  EFE         eta = g_ext/a0               -> eta proportional to 1/E(z)
  deep-MOND   g_obs = sqrt(g_bar a0)        -> at fixed g_bar, g_obs proportional to sqrt(E(z))
Needs numpy.
"""
import numpy as np

c = 2.998e8; G = 6.674e-11; hbar = 1.055e-34; Msun = 1.989e30; Mpc = 3.086e22; kpc = 3.086e19
Om, OL = 0.315, 0.685
H0 = 67.4e3/Mpc
Z = 2*np.sqrt(8*np.pi/3)
a0 = 1.2e-10
E = lambda z: np.sqrt(Om*(1+z)**3 + OL)
ZS = (0, 0.5, 1, 2, 3, 6, 10)


def main():
    print("#"*98)
    print("# CALCULATION OFFENSIVE -- a0(z)=cH(z)/Z, Z=2sqrt(8pi/3)=%.3f. Every distinctive consequence." % Z)
    print("#"*98 + "\n")

    print("="*98); print("PART 1 -- THE CONSEQUENCE CASCADE (ratios to z=0; constant-a0 MOND would give all 1.00)"); print("="*98)
    hdr = ["z", "E(z)=a0/a0_0", "V/V0 (BTFR)", "sig/sig0", "Sig/Sig0", "rho_ph/0", "r_M/r_M0", "eta/eta0", "RAR shift"]
    print("  " + "".join(f"{h:>12}" for h in hdr))
    for z in ZS:
        e = E(z)
        row = [z, e, e**0.25, e**0.25, e, e**0.5, e**-0.5, 1/e, e**0.5]
        print("  " + "".join(f"{row[0]:>12}" if i == 0 else f"{row[i]:>12.3f}" for i in range(len(row))))
    print("  reading: at z=2 a galaxy of FIXED baryonic mass rotates 32% faster, sits in disks 3x denser,")
    print("           hosts phantom halos 1.74x denser, turns MOND at 0.58x the radius, and is 3x more isolated-MOND.\n")

    print("="*98); print("PART 2 -- ABSOLUTE PREDICTIONS: V_flat(z) for fixed baryonic mass (the JWST/ALMA test)"); print("="*98)
    print(f"   V_flat = (G M_b a0(z))^(1/4).  THIS formula vs constant-a0 MOND:")
    print(f"   {'M_b [Msun]':>12}{'z':>5}{'V_flat (this) [km/s]':>22}{'V_flat (const-a0)':>20}")
    for logM in (9, 10, 11):
        Mb = 10**logM * Msun
        V0 = (G*Mb*a0)**0.25/1e3
        for z in (0, 2, 6):
            Vz = (G*Mb*a0*E(z))**0.25/1e3
            print(f"   {'1e'+str(logM):>12}{z:>5}{Vz:>22.1f}{V0:>20.1f}")
    print("   => fixed-mass galaxies rotate FASTER at high z (x1.32 at z=2, x1.80 at z=6). Constant MOND: flat.\n")

    print("="*98); print("PART 3 -- THE GEOMETRIC / Lambda STRUCTURE (this formula's specific coefficient)"); print("="*98)
    H0_pred = Z*a0/c*Mpc/1e3
    Lam = 3*OL*H0**2/c**2
    print(f"   a0-cosmography:  H0 = Z a0/c = {H0_pred:.1f} km/s/Mpc  (read off galaxy rotation curves)")
    q0 = 0.5*(Om - 2*OL)
    print(f"   deceleration:    q0 = (Om - 2 OmL)/2 = {q0:.3f}  (dark energy read from a0's slope; = LCDM)")
    print(f"   the seesaw:      a0 = c E_Lambda^2/(2 hbar E_Planck),  E_Lambda = (rho_L)^(1/4) = 2.24 meV")
    print(f"   one scale:       a0 = c^2 sqrt(Lambda/32pi) AND rho_Lambda = Lambda c^2/8piG  (whole dark sector)")
    # secular drift of a0 today
    drift = 0.5*(-3*Om*H0)/1.0          # d ln a0/dt = (1/2) dE^2/dt / E^2 at z=0
    print(f"   secular drift:   d(a0)/a0/dt = {drift*3.156e7:.2e} /yr  (a0 is shrinking now; unmeasurable but real)\n")

    print("="*98); print("PART 4 -- THE EFE-WEAKENING PREDICTION (LCDM-forbidden; this formula's distinctive z-shape)"); print("="*98)
    print(f"   external-field ratio eta(z)=g_ext/a0(z) proportional 1/E(z): high-z galaxies are cleaner isolated-MOND.")
    print(f"   {'z':>5}{'eta(z)/eta0':>14}{'-> rotation curves at high z are':>40}")
    for z in (0, 1, 2, 3):
        print(f"   {z:>5}{1/E(z):>14.3f}{'more MOND-like (less EFE suppression)':>40}")
    print(f"   LCDM has NO external field effect at all -> any z-trend in the EFE is a clean LCDM kill.\n")

    print("="*98); print("PART 5 -- THE DENSITY READING: a0 = (c/2) sqrt(G rho) in overdensities (clusters)"); print("="*98)
    rho_crit0 = 3*H0**2/(8*np.pi*G)
    for delta, name in [(1, "field (cosmic mean)"), (200, "cluster (~200x)"), (1e5, "galaxy core")]:
        a0_env = (c/2)*np.sqrt(G*delta*rho_crit0)
        print(f"   delta={delta:>7.0f} ({name:<20}): a0_env = {a0_env:.2e} = {a0_env/a0:>6.1f} a0_cosmic")
    print(f"   => clusters (200x overdense) -> a0 ~ sqrt(200) ~ 14x larger -> less missing mass. (Honest: this")
    print(f"      environmental reading is DISFAVORED by the tight field-galaxy RAR; the cosmic a0(z) form stands.)\n")

    print("="*98); print("OFFENSIVE SUMMARY -- what is distinctive to THIS formula"); print("="*98)
    print(f"""  Every row of Part 1 is FLAT (=1) for constant-a0 MOND and EVOLVING for this formula: a fixed-mass galaxy
  rotates faster, is denser, and turns MOND sooner at high z, all set by ONE function E(z) with NO free
  parameters (H0 and Z both cancel in the ratios). The geometric coefficient also fixes H0=71.5 and q0=-0.53
  off galaxy dynamics, and ties a0 to the 2.24 meV vacuum scale. HONEST TAGS: the z-evolution cleanly beats
  *constant* MOND but is amplitude-degenerate with LCDM (both rise); the clean LCDM kills are the EFE z-shape
  (Part 4) and the a0=cH(z)/Z amplitude measured HALO-FREE at z>2 (Part 2). All numbers first-principles, this formula only.""")
    print("#"*98)


if __name__ == "__main__":
    main()
