#!/usr/bin/env python3
"""
GATE 2, scoped: does scaling a0(z)=cH(z)/Z break the CMB?  (honest partial)
==========================================================================

The full pass/fail is a modified Boltzmann run (Skordis-Zlosnik RelMOND with
a0(z)=cH(z)/Z, demand Planck TT/EE/lensing). I cannot run that here. But I can
SCOPE it rigorously and pin down exactly what the full calculation must check.
Three honest pieces:

  (1) SELF-SIMILARITY (robust): a0/cH = 1/Z and the MOND transition scale
      lambda_MOND/R_H = 2/Z are CONSTANT at every epoch. Recombination is not a
      special danger epoch -- it looks like every other epoch in a0/cH terms.
      Scaling a0 REMOVES the epoch-dependence that constant-a0 has.

  (2) WHERE the acoustic scales sit (crude, caveated): at recombination the
      sound horizon r_s straddles the MOND transition. So any MOND effect lands
      at LARGE scales (low ell), negligible at the high-ell damping tail.

  (3) THE SZ MECHANISM (structural): SZ fits the CMB because the scalar's ENERGY
      DENSITY mimics CDM at early times; a0 enters the QUASI-STATIC (galaxy)
      limit. The open question is precisely: does a0 enter the cosmological
      BACKGROUND/linear evolution? If not, scaling a0 is ~safe for the CMB.

Verdict: SCOPED, not passed. Self-similarity says 'not obviously fatal'; the full
SZ re-fit remains the real gate, now well-defined. Pure stdlib.
Run:  python reviews/gate2_cmb_scaling_a0.py
"""

import math

C = 2.99792458e8
MPC = 3.0857e22
A0 = 1.20e-10
Z = 2 * math.sqrt(8 * math.pi / 3)     # 5.78881
H0 = 71.5e3 / MPC
OM, OL = 0.315, 0.685
Z_REC = 1089.9
R_S_COMOV_MPC = 144.4                   # comoving sound horizon at last scattering


def E(z):
    return math.sqrt(OM * (1 + z) ** 3 + OL)


def Hz(z):
    return H0 * E(z)


def part1_self_similar():
    print("=" * 80)
    print("(1) SELF-SIMILARITY (robust): recombination is NOT a special epoch")
    print("=" * 80)
    print("   With a0(z)=cH(z)/Z, two ratios are CONSTANT at every redshift:")
    print(f"     a0 / (cH)            = 1/Z         = {1/Z:.4f}")
    print(f"     lambda_MOND / R_H    = 2/Z         = {2/Z:.4f}")
    print("   (lambda_MOND = scale where g=(4pi/3)G rho lambda equals a0; R_H=c/H.)")
    print()
    print(f"   {'z':>8}{'cH(z) [m/s^2]':>16}{'a0(z) [m/s^2]':>16}{'a0/cH':>9}{'lam_M/R_H':>11}")
    for z in (0, 1, 100, Z_REC):
        cH = C * Hz(z)
        a0 = cH / Z
        print(f"   {z:>8.0f}{cH:>16.3e}{a0:>16.3e}{a0/cH:>9.3f}{2/Z:>11.3f}")
    print("   => the a0-physics is SELF-SIMILAR across cosmic history. Constant-a0")
    print("      MOND has a special low-acceleration epoch; SCALING a0 does NOT --")
    print("      it removes that epoch-dependence. A point in the scaling's favor.\n")


def part2_acoustic_scales():
    print("=" * 80)
    print("(2) WHERE the acoustic scales sit at recombination (crude, caveated)")
    print("=" * 80)
    H = Hz(Z_REC)
    R_H_proper = (C / H) / MPC                # c/H(z) IS the physical Hubble radius (Mpc)
    lam_M_proper = (2 / Z) * R_H_proper       # physical MOND transition scale
    r_s_proper = R_S_COMOV_MPC / (1 + Z_REC)  # comoving sound horizon -> proper
    print(f"   at z_rec={Z_REC:.0f}:  (proper/physical Mpc)")
    print(f"     Hubble radius R_H      = {R_H_proper:.4f} Mpc")
    print(f"     MOND transition lam_M  = (2/Z) R_H = {lam_M_proper:.4f} Mpc")
    print(f"     sound horizon r_s      = {r_s_proper:.4f} Mpc")
    print(f"     r_s / R_H   = {r_s_proper/R_H_proper:.2f}   "
          f"r_s / lam_M = {r_s_proper/lam_M_proper:.2f}")
    print("   Scales > lam_M are MONDian; < lam_M Newtonian. r_s sits ABOVE lam_M, so")
    print("   the FIRST-peak / large-scale region is mildly MONDian; the high-ell")
    print("   damping tail (small scales) is Newtonian and ~unaffected.")
    print("   CAVEAT: g~(4pi/3)G rho lambda is Newtonian; near the horizon you need")
    print("   relativistic perturbation theory + the SZ field dynamics. This LOCATES")
    print("   the effect (low ell), it does not size it. That needs the Boltzmann run.\n")


def part3_sz_mechanism():
    print("=" * 80)
    print("(3) THE SZ MECHANISM: why a0 may not even enter the CMB-setting physics")
    print("=" * 80)
    print("   Skordis-Zlosnik (2021) fit the CMB because their scalar's ENERGY DENSITY")
    print("   redshifts like CDM (dust) at early times -- a BACKGROUND + linear effect")
    print("   set by the field's kinetic/potential structure. The MOND scale a0 enters")
    print("   the QUASI-STATIC, deep-sub-horizon, late-time GALAXY limit (the free")
    print("   function's argument), which is a DIFFERENT regime from recombination.")
    print()
    print("   So the precise open question Gate 2 must answer is:")
    print("     DOES a0 appear in the cosmological background / linear perturbation")
    print("     equations at recombination, or only in the quasi-static limit?")
    print("       * if a0 enters ONLY the quasi-static limit -> promoting a0->a0(z)")
    print("         leaves the CMB-setting dust-mimicking UNTOUCHED -> Gate 2 PASSES")
    print("         almost trivially (the scaling is invisible to the CMB).")
    print("       * if a0 ALSO enters the linear/background evolution -> the scaling")
    print("         changes recombination and the full TT/EE re-fit is mandatory.")
    print("   This is a definite, answerable question about the SZ field equations.\n")


def main():
    part1_self_similar()
    part2_acoustic_scales()
    part3_sz_mechanism()
    print("=" * 80)
    print("VERDICT -- Gate 2 SCOPED (not passed, not failed)")
    print("=" * 80)
    print("  ROBUST: scaling a0=cH/Z makes the cosmology self-similar in a0/cH, so")
    print("  recombination is not a special danger epoch -- the scaling is, if")
    print("  anything, MORE natural than constant-a0 (no preferred low-a epoch).")
    print("  LOCATED: any CMB effect lands at LARGE scales (low ell), not the damping")
    print("  tail. SHARPENED: the full pass/fail reduces to ONE question -- whether a0")
    print("  enters the SZ cosmological background or only the quasi-static limit.")
    print()
    print("  NEXT (the actual Gate 2 calculation): take the SZ field equations, check")
    print("  if a0 appears in the background/linear system; if it does, run a modified")
    print("  hi_class with a0(z)=cH(z)/Z and compare TT/EE/lensing to Planck. I have")
    print("  scoped it honestly; I have NOT passed it, and I will not claim to.")


if __name__ == "__main__":
    main()
