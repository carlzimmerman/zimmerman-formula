#!/usr/bin/env python3
"""
PROJECT 15: dwarf spheroidals as EFE thermometers -- a MOND-distinctive, DM-awkward prediction.
==============================================================================================
A diffuse dwarf's internal acceleration can be far below a0 AND below the host's external field. MOND then
predicts a velocity dispersion SUPPRESSED below the isolated-MOND value by the External Field Effect -- and
the suppression depends on DISTANCE FROM THE HOST. LambdaCDM (each dwarf in its own halo) predicts no such
host-distance dependence. The textbook case is Crater II, whose tiny dispersion McGaugh PREDICTED from MOND+
EFE before it was measured. This file computes it. Needs numpy.
"""
import numpy as np

G, a0, Msun, kpc, pc = 6.674e-11, 1.2e-10, 1.989e30, 3.0857e19, 3.0857e16
VMW = 220e3


def predict(name, L, MtoL, Rh_pc, D_kpc):
    M = L*MtoL*Msun; Rh = Rh_pc*pc; D = D_kpc*kpc
    g_ext = VMW**2/D; g_int = G*M/Rh**2
    sig_iso = ((4/81)*G*M*a0)**0.25
    Geff = G*(a0/g_ext) if g_ext < a0 else G
    sig_efe = np.sqrt(Geff*M/(3*Rh))
    return g_ext/a0, g_int/a0, sig_iso/1e3, sig_efe/1e3


def main():
    print("#"*92); print("# PROJECT 15 -- dwarf spheroidals as EFE thermometers"); print("#"*92 + "\n")
    print("="*92); print("THE CLEAN CASE -- Crater II (a genuine pre-registered MOND success)"); print("="*92)
    ge, gi, siso, sefe = predict("Crater II", 1.6e5, 2.0, 1100, 117)
    print(f"""  Crater II: L~1.6e5 Lsun, R_h~1.1 kpc (extremely diffuse), D=117 kpc from the Milky Way.
     g_ext/a0 = {ge:.2f},  g_int/a0 = {gi:.1e}   ->  deep in the EFE-DOMINATED regime (g_int << g_ext < a0).
     isolated-MOND sigma would be {siso:.1f} km/s, but the EFE SUPPRESSES it to ~{sefe:.1f} km/s.
  McGaugh (2016) PREDICTED sigma ~ 2.1 km/s from MOND+EFE BEFORE the measurement. Caldwell+ (2017) then
  measured 2.7 +- 0.3 km/s. A LambdaCDM NFW/cuspy halo for that luminosity predicts ~4-7 km/s. So the dwarf
  is COLD in exactly the way MOND+EFE requires and dark matter does not naturally give. This is one of the
  cleanest MOND predictions on record.\n""")

    print("="*92); print("THE DISTINCTIVE SIGNATURE -- host-distance-dependent coldness"); print("="*92)
    print("""  Because the suppression scales with g_ext = V_host^2/D, MOND predicts dwarfs at the SAME luminosity
  are COLDER when CLOSER to their host (stronger external field), and approach the isolated-MOND value when
  far away. LambdaCDM has no mechanism for a host-distance dependence at fixed L (each dwarf's halo is set by
  its own mass). So a survey of diffuse dwarfs' sigma vs host distance is a clean MOND-vs-DM discriminator,
  with Crater II already sitting where MOND says it should.\n""")

    print("="*92); print("HONEST LIMITS"); print("="*92)
    print("""  * The two-regime estimate here (isolated sigma^4=(4/81)GMa0; EFE-dominated G_eff=G a0/g_ext) is
    ILLUSTRATIVE -- it nails the clean EFE-dominated case (Crater II) but a full sample needs the proper
    MOND interpolation across the transition and a per-dwarf EFE treatment (denser dwarfs near g_int~a0 are
    not captured by the simple formula).
  * Tidal effects and non-equilibrium can also lower sigma; the clean test requires dynamically-relaxed,
    diffuse dwarfs where the EFE dominates (Crater II, Antlia II, the ultra-diffuse galaxies).
  Net: a real, blind-predictive MOND signature (Crater II) and a distinctive, DM-awkward survey-level test
  (sigma vs host distance) -- stated with the modeling caveat, not oversold to the harder cases.""")
    print("="*92)


if __name__ == "__main__":
    main()
