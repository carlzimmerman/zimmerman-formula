#!/usr/bin/env python3
"""
CLOCK-GRADE, TRACER-FREE LOCAL RAR: run the Sun's directly-measured Galactic
acceleration (binary-pulsar timing, Chakrabarti et al. 2021 ApJL 907 L26 = arXiv:2010.04018)
through the framework kernel g_obs = sqrt(g_bar^2 + g_bar*a0), with the best-measured
baryon budget anywhere (McKee et al. 2015). Two channels; both a0 footings. Honest verdict.
"""
import numpy as np
c=2.99792458e8; G=6.67430e-11; KPC=3.0856776e19; MSUN=1.98892e30; PC=3.0856776e16
A0_C, A0_A = 9.355e-11, 1.1305e-10          # canonical / alt footings

print("="*74); print("CHANNEL 1 -- VERTICAL / Oort-limit (Chakrabarti's clean measurement)")
print("="*74)
# Chakrabarti: az = -alpha1 z, log10(alpha1/Gyr^-2)=3.69 (+0.19/-0.12) -> Oort limit rho_dyn
GYR=3.1557e16
alpha1 = 10**3.69 / GYR**2                   # s^-2
rho_oort = alpha1/(4*np.pi*G)                # midplane total dynamical density (Poisson)
print(f"  alpha1 = 10^3.69 Gyr^-2 -> rho_dyn(midplane) = {rho_oort/(MSUN/PC**3):.3f} Msun/pc^3  (paper: 0.08 +0.05/-0.02)")
rho_bar = 0.084                              # McKee 2015 midplane baryonic (Chakrabarti's own subtraction gives DM=-0.004)
print(f"  McKee 2015 baryonic midplane rho_bar = {rho_bar:.3f} Msun/pc^3")
print(f"  => measured local DM = {rho_oort/(MSUN/PC**3)-rho_bar:+.3f} (+0.05/-0.02) Msun/pc^3 -- CONSISTENT WITH ZERO")
# az at z=1.1 kpc (linear regime) as an a0-scale marker
for z_kpc in (1.0,):
    az = alpha1 * z_kpc*KPC
    print(f"  vertical accel at z={z_kpc} kpc: a_z = {az:.2e} m/s^2 = {az/A0_C:.2f} a0_canon / {az/A0_A:.2f} a0_alt (transitional)")
print("  FRAMEWORK READ: a no-real-DM kernel wants rho_dyn ~ rho_bar + a small MOND-EFE phantom.")
print("  At the Sun the radial field is ~2.3 a0 (nu~1.20), so the vertical EFE phantom is ~0.005-0.02")
print("  Msun/pc^3 -> framework total ~0.089-0.104, INSIDE the measured 0.08(+0.05) band. PASS, but")
print("  the +0.05 error also fully allows LCDM's ~0.01 local DM -> NON-DIAGNOSTIC (errors straddle).")
print("  The clock-grade central value (DM~0) is mildly favorable to no-DM, not decisive.")

print("\n" + "="*74); print("CHANNEL 2 -- RADIAL galactocentric RAR at the Sun")
print("="*74)
R0 = 8.178*KPC                               # GRAVITY 2019
for Vc in (229e3, 233e3, 240e3):
    g_obs = Vc**2/R0
    print(f"  V_circ={Vc/1e3:.0f} km/s -> g_obs,R = V^2/R0 = {g_obs:.3e} m/s^2 = {g_obs/A0_C:.2f} a0_canon")
g_obs = 233e3**2/R0
print(f"  (adopt g_obs,R = {g_obs:.3e}; clean centripetal, but Chakrabarti flag radial as less clean than vertical)")
print("  baryonic radial contribution is MODEL-DEPENDENT (V_bar=160-210 km/s across MW mass models):")
for Vb in (170e3, 190e3, 210e3):
    g_bar = Vb**2/R0; y=g_bar/A0_C
    g_fw  = np.sqrt(g_bar**2 + g_bar*A0_C)
    print(f"    V_bar={Vb/1e3:.0f} -> g_bar={g_bar:.3e} (y={y:.2f}) -> framework g_obs={g_fw:.3e} = {g_fw/g_obs:.2f}x measured")
print("  => the framework matches the measured g_obs,R ONLY for V_bar~205-210 km/s (high end); at")
print("  V_bar~170 it UNDER-predicts by ~30%. So the radial channel is M_bar-MODEL-HOSTAGE (same")
print("  disease as every a0-scale test): PASS within the MW baryonic uncertainty, non-diagnostic.")

print("\n" + "="*74); print("VERDICT (both ways)")
print("="*74)
print("  WIN-SIDE: the ONLY clock-grade, tracer-free, steady-state-robust LOCAL acceleration test.")
print("  The framework PASSES both channels; the vertical clock-limit finds local DM ~ 0 (central),")
print("  which a no-real-DM reading likes; the Sun sits at y~1.2-2.3 (transitional, where nu is most")
print("  distinctive). NON-DIAGNOSTIC BOTH WAYS: the vertical +0.05 error allows LCDM's ~0.01 DM, and")
print("  the radial is hostage to the MW baryonic V_bar (160-210 km/s). a0's value + Z stay POSITED;")
print("  this tests consistency at y~1, not a0's value. Sharpening = a tighter Oort limit (Gaia/pulsar")
print("  timing arrays) + a pinned MW V_bar -> the same 'one ~5-8% number' lever as the triangle.")
print("EXIT 0")
