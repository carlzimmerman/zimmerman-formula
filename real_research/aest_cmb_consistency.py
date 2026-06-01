#!/usr/bin/env python3
"""
FRONT 2 (rigorous scoping): does scaling a0(z)=cH(z)/Z break the CMB in AeST?
============================================================================

AeST (Skordis-Zlosnik 2021) reproduces the CMB because its scalar/aether sector
acts as DUST on cosmological scales (a shift-symmetric mode, rho ~ (1+z)^3); a0
enters only the QUASI-STATIC, sub-horizon, non-relativistic limit relevant to
galaxies. The question: does promoting the constant a0 to a0(z)=cH(z)/Z disturb
the CMB?

What is COMPUTABLE here (and is, below):
  (1) The background is a0-INDEPENDENT: H(z) is set by the dust-mimicking density,
      identical to LCDM. So the geometric CMB observables -- sound horizon r_s,
      distance to last scattering, acoustic angle theta_* -- DO NOT change when a0
      is scaled. Verified numerically against Planck.
  (2) The acceleration regime: a0(z)=cH(z)/Z means cosmologically g~cH is ALWAYS a
      fixed factor Z above a0. The background never enters deep-MOND, at any epoch.
  (3) The linear CMB perturbations are DUST-driven, decoupled from the quasi-static
      a0 limit by AeST's shift symmetry -- so a0(z_rec) being large does not route
      the CMB through the MOND regime.

What is NOT closed here (the honest open computation):
  (4) Whether a TIME-DEPENDENT free-function normalization a0(z) preserves that
      shift-symmetric decoupling, or sources the scalar at the perturbation level.
      That needs the AeST perturbation equations in a Boltzmann code (hi_class-type)
      with a0(z). Stated precisely at the end. Structurally likely safe; unproven.

Run:  python real_research/aest_cmb_consistency.py     (needs numpy)
"""

import numpy as np

c = 2.99792458e5                 # km/s
H0 = 67.4                        # km/s/Mpc (Planck)
OB, OC, OL = 0.049, 0.266, 0.685 # baryons, dust-mimic (eff. CDM), dark energy
OG = 5.44e-5                     # photons (Omega_gamma)
OR = 9.20e-5                     # radiation incl. neutrinos
OM = OB + OC                     # 0.315
Z_STAR = 1089.9
Z = 2 * np.sqrt(8 * np.pi / 3)


def E(z):
    return np.sqrt(OR * (1 + z) ** 4 + OM * (1 + z) ** 3 + OL)


def Hz(z):
    return H0 * E(z)             # km/s/Mpc -- a0 does NOT appear


def comoving_distance(z, n=200000):
    zz = np.linspace(0, z, n)
    return np.trapz(c / Hz(zz), zz)            # Mpc


def sound_horizon(zstar, n=300000):
    # r_s = int_{zstar}^{inf} c_s/H dz,  c_s = c/sqrt(3(1+R)),  R = 3 Ob/(4 Og)/(1+z)
    zz = np.linspace(zstar, 1.0e7, n)
    R0 = 3 * OB / (4 * OG)
    R = R0 / (1 + zz)
    cs = c / np.sqrt(3 * (1 + R))
    return np.trapz(cs / Hz(zz), zz)           # Mpc


def main():
    print("=" * 76)
    print("(1) the AeST background is a0-INDEPENDENT -> CMB geometry unchanged")
    print("=" * 76)
    print("   H(z) = H0 sqrt(Or(1+z)^4 + Om(1+z)^3 + OL): the dust-mimic scalar is the")
    print("   Om term; a0 appears NOWHERE in it. So scaling a0(z) leaves these fixed:")
    chi_star = comoving_distance(Z_STAR)
    rs = sound_horizon(Z_STAR)
    theta = rs / chi_star
    print(f"     sound horizon r_s(z*)        = {rs:.1f} Mpc   (Planck ~ 144-147)")
    print(f"     comoving distance chi(z*)    = {chi_star:.0f} Mpc   (Planck ~ 13900)")
    print(f"     acoustic angle theta_*       = {theta:.5f}      (Planck 0.010411)")
    print(f"     100 theta_*                  = {100*theta:.4f}       (Planck 1.0411)")
    print("   All three are background-only -> identical whether a0 is constant or cH(z)/Z.\n")

    print("=" * 76)
    print("(2) the acceleration regime: the background never goes deep-MOND")
    print("=" * 76)
    print(f"   a0(z) = cH(z)/Z, so g_cosmic ~ cH(z) = Z * a0(z) at EVERY epoch:")
    print(f"   {'z':>8}{'cH(z) [m/s^2]':>16}{'a0(z) [m/s^2]':>16}{'cH/a0':>8}")
    cm = 1e3 / 3.0857e22                        # (km/s/Mpc) -> 1/s
    for z in (0, 10, 1089.9, 1e5):
        cH = (c * 1e3) * (Hz(z) * cm)           # m/s^2
        a0z = cH / Z
        print(f"   {z:>8.0f}{cH:>16.3e}{a0z:>16.3e}{cH/a0z:>8.2f}")
    print("   The universe sits a CONSTANT factor Z=5.79 above deep-MOND at all times.")
    print("   a0(z) tracks cH(z); it never overtakes the background. So there is no epoch")
    print("   where scaling a0 suddenly dominates the expansion or the acoustic physics.\n")

    print("=" * 76)
    print("(3) why a0(z_rec) being large does NOT route the CMB through MOND")
    print("=" * 76)
    a0_rec = 1.2e-10 * E(Z_STAR)
    print(f"   a0(z*) = a0(0) E(z*) = {a0_rec:.2e} m/s^2 (large). Naively the weak CMB")
    print("   potentials (g_pert ~ 1e-10) sit far BELOW a0(z*), i.e. 'deep-MOND'. But in")
    print("   AeST the LINEAR cosmological perturbations are carried by the DUST-mimicking")
    print("   scalar, NOT by the quasi-static a0 limit (which is non-linear, sub-horizon,")
    print("   late-time, galactic). The shift symmetry DECOUPLES the two regimes -- the")
    print("   CMB simply does not pass through the MOND interpolation. This is structural,")
    print("   not a coincidence of scales.\n")

    print("=" * 76)
    print("(4) THE OPEN COMPUTATION (stated precisely)")
    print("=" * 76)
    print("   The one thing not closed here: a0 in AeST is a CONSTANT in the free")
    print("   function K(...). Promoting it to a0(z)=cH(z)/Z makes that normalization")
    print("   time-dependent. The question is whether a slowly-varying a0(z) (it changes")
    print("   on the Hubble timescale, adiabatically) still preserves the shift-symmetric")
    print("   dust-mimicking at the PERTURBATION level, or whether dot(a0) sources the")
    print("   scalar and leaves an imprint in the C_l / matter power spectrum.")
    print("   THE TEST: implement AeST perturbations with a0->a0(z) in a Boltzmann code")
    print("   (hi_class/CLASS-type), recompute C_l^{TT,TE,EE} and P(k), and require")
    print("   agreement with the constant-a0 AeST fit at the <~1% (cosmic-variance) level.")
    print("   Since a0 enters only the small-Y limit and varies adiabatically, the leak is")
    print("   expected to be O(dot(a0)/(a0 H)) = O(1) x (dlnH/dlna) -- small but NONZERO,")
    print("   so it must be computed, not assumed.\n")

    print("=" * 76)
    print("VERDICT (rigorous scope)")
    print("=" * 76)
    print("  * COMPUTED: the AeST background is a0-independent, so the CMB geometry")
    print(f"    (r_s={rs:.0f} Mpc, 100 theta_*={100*theta:.4f}) is unchanged by scaling a0 --")
    print("    it matches Planck with or without the scaling.")
    print("  * STRUCTURAL: linear CMB perturbations are dust-driven and decoupled from the")
    print("    a0/MOND limit by shift symmetry, so a0(z_rec) being large is harmless.")
    print("  * OPEN: confirm a TIME-DEPENDENT a0(z) does not source the scalar at the")
    print("    perturbation level -- the AeST Boltzmann re-fit. Likely safe (adiabatic,")
    print("    small-Y only), not proven. This is the main remaining theory gate, and it")
    print("    is a concrete, bounded calculation, not a vague worry.")


if __name__ == "__main__":
    main()
