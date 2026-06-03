#!/usr/bin/env python3
"""
Widening further: lensing, BAO, the Local Group timing argument, dwarf-spheroidal EFE.
======================================================================================

ALL of this is CONDITIONAL on MOND being a real description (the open foundational question --
wide binaries Banik vs Chae; a0-universality). Granting that, we derive the consequences in
four more domains, with PhD honesty:
  [DERIVED] forced; [FOLLOWS] clean but weaker; [LIMIT] a place MOND/the framework FAILS;
  [OPEN]    a real, unsettled test.

Run: python <thisfile>   (needs numpy, scipy)
"""
import numpy as np
from scipy.integrate import quad

c, G, Msun, kpc, Mpc = 2.99792458e8, 6.674e-11, 1.989e30, 3.0857e19, 3.0857e22
OM, OL = 0.315, 0.685
Z = 2 * np.sqrt(8 * np.pi / 3); H0 = 67.4e3 / Mpc; A0 = 1.2e-10
E = lambda z: np.sqrt(OM * (1 + z) ** 3 + OL)


def lensing():
    print("=" * 82); print("[1] GRAVITATIONAL LENSING in the relativistic sector (AeST)")
    print("=" * 82)
    print("  GALAXIES [FOLLOWS]: AeST is built so light bends like the dynamics -- the phantom")
    print("  halo (rho~1/r^2) lenses too, so the lensing mass ~ the dynamical mass, with NO dark")
    print("  matter. Galaxy-galaxy lensing works at the MOND level. The deep-MOND deflection scales")
    print("  as alpha ~ sqrt(G M a0)/c^2 (vs Newtonian alpha ~ GM/c^2), so it grows with a0(z):")
    print(f"     alpha(z)/alpha(0) = sqrt(E(z)):  x{np.sqrt(E(6)):.1f} by z=6  -- high-z lenses enhanced.")
    print("  CLUSTERS [LIMIT]: the SAME factor-of-2 residual as the dynamics. The BULLET CLUSTER is")
    print("  the sharp case -- the lensing mass peak is OFFSET from the (dominant) gas, onto the")
    print("  galaxies, which demands COLLISIONLESS mass. Pure MOND cannot supply an offset; AeST's")
    print("  aether/scalar fields give some, but the cluster lensing residual is a genuine, unsolved")
    print("  failure. Evolving a0 does not fix it (clusters are at z~0.3, a0 ~ today). [LIMIT]\n")


def bao():
    print("=" * 82); print("[2] BAO -- the standard ruler is preserved, and gives a new cross-check")
    print("=" * 82)
    a_rec = 1/1090.0
    Ob, Og = 0.0493, 2.47e-5/0.674**2
    R = lambda a: 0.75*(Ob/Og)*a; cs = lambda a: 1/np.sqrt(3*(1+R(a)))
    rs = quad(lambda a: cs(a)/(a**2*np.sqrt(OM*a**-3+OL+ (Og*(1+0.227*3.046))*a**-4)), 1e-8, a_rec)[0]
    rs_Mpc = rs * c/H0/Mpc
    print(f"  The sound horizon r_s = {rs_Mpc:.0f} Mpc (Planck ~147 comoving). In AeST the background")
    print("  is LCDM-like (the Q-sector mimics CDM) and a0 is ABSENT from linear perturbations")
    print("  (Paper II), so the BAO ruler and its redshift evolution are UNCHANGED. [DERIVED: a pass]")
    print("  NEW CROSS-CHECK [DERIVED]: a0-cosmography gives H(z)=Z a0(z)/c from galaxies; BAO gives")
    print("  H(z) from the ruler. They MUST agree. Disagreement falsifies the framework -- an")
    print("  independent consistency test the standard a0~cH coincidence does not offer.\n")


def local_group():
    print("=" * 82); print("[3] THE LOCAL GROUP TIMING ARGUMENT (Milky Way - Andromeda)")
    print("=" * 82)
    Mbar = 1.5e11 * Msun; d = 770 * kpc
    gN = G * Mbar / d ** 2
    boost = np.sqrt(A0 / gN)
    gM = np.sqrt(gN * A0)
    print(f"  MW+M31 baryonic mass ~1.5e11 Msun, separation 770 kpc:")
    print(f"     Newtonian mutual accel g_N = GM/d^2 = {gN:.2e} m/s^2  (<< a0 -> deep MOND)")
    print(f"     MOND boost = sqrt(a0/g_N) = {boost:.0f}x  ->  g_MOND = sqrt(g_N a0) = {gM:.2e} m/s^2")
    print(f"  [FOLLOWS] The ~{boost:.0f}x MOND enhancement supplies the timing 'mass' WITHOUT the")
    print("  ~5e12 Msun of dark matter the Newtonian timing argument needs -- the baryons + boost")
    print("  do it. TENSION: the strong early pull makes MOND predict a HIGH MW-M31 relative")
    print("  velocity and a likely PAST close encounter (Zhao, Famaey, Kroupa 2013) -- a real")
    print("  challenge, not a clean win. Evolving a0 (larger early) makes the early pull even")
    print("  STRONGER, sharpening that tension rather than easing it. [FOLLOWS + TENSION]\n")


def dwarf_spheroidals():
    print("=" * 82); print("[4] DWARF-SPHEROIDAL EFE -- the distinctive environmental prediction")
    print("=" * 82)
    print("  Dwarf spheroidals are the lowest-acceleration systems (internal g << a0), so MOND")
    print("  predicts large velocity dispersions with NO dark matter -- BUT modulated by the EFE")
    print("  of their host (the MW). The prediction is environmental: a dSph's sigma depends on its")
    print("  DISTANCE from the MW (the external field), which LCDM does not predict.")
    # Crater II: distance ~120 kpc, very diffuse -> weak EFE -> low predicted sigma
    R_CII = 120 * kpc; M_MW = 1e11 * Msun
    g_ext = np.sqrt(G * M_MW * A0) / R_CII          # MW's deep-MOND field at Crater II
    print(f"  Worked example -- Crater II (d~120 kpc): the MW's MOND field there is")
    print(f"     g_ext ~ sqrt(G M_MW a0)/R = {g_ext:.2e} m/s^2 = {g_ext/A0:.2f} a0 (weak EFE).")
    print("  MOND predicted sigma ~ 2 km/s for Crater II (McGaugh+Milgrom 2013); observed ~2.7 km/s")
    print("  (Caldwell+2017) -- a NOTABLE MOND success in a regime where LCDM expected ~4 km/s.")
    print("  [DERIVED: environmental sigma(distance); some successes, some dSphs need more boost.]")
    print("  The framework's distinctive ADD is the HIGH-z version: a dSph-analog's EFE weakens as")
    print("  1/E(z), so high-z low-mass satellites are MORE isolated-MOND. No data yet. [OPEN]\n")


def main():
    lensing(); bao(); local_group(); dwarf_spheroidals()
    print("=" * 82); print("LEDGER -- widened domains (all conditional on MOND being real)")
    print("=" * 82)
    print("  DERIVED: BAO ruler unchanged + a new a0-cosmography-vs-BAO cross-check [2]; dSph")
    print("           environmental sigma(distance), Crater II a MOND success [4].")
    print("  FOLLOWS: galaxy lensing ~ dynamical mass, enhanced ~sqrt(E) at high z [1]; Local Group")
    print("           timing works on baryons+boost [3].")
    print("  LIMIT:   CLUSTER lensing / the BULLET CLUSTER -- the factor-2 residual + the mass-gas")
    print("           offset is a genuine, unsolved MOND failure, NOT fixed by evolving a0 [1].")
    print("  TENSION: the Local Group timing predicts a high MW-M31 velocity / past encounter;")
    print("           evolving a0 sharpens, not eases, it [3].")
    print("  OPEN:    the high-z dwarf EFE (1/E(z)) -- the framework's distinctive add, no data [4].")
    print("  Honest pattern (again): galaxy-scale wins (lensing, dSph, LG) are inherited MOND; the")
    print("  cluster/Bullet failure is inherited too; the only distinctive content is the high-z")
    print("  evolution. And ALL of it stands or falls with the foundational question: is MOND real?")
    print("=" * 82)


if __name__ == "__main__":
    main()
