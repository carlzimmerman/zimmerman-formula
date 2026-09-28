#!/usr/bin/env python3
"""AS005 complement: footing bookkeeping per FRAMEWORK_CONTRACT.
- kappa=1/2 ADOPTED on both footings => alternative footing has CHANGED density.
- If instead rho_Lambda were held fixed at canonical, the alternative a0 implies an
  effective kappa; record it. Same for the reverse direction. Never share fixed
  density AND fixed kappa across footings.
- Also record which H each expression uses (H_L with framework rho_Lambda, not H0,
  not critical-density H_Lambda) and the c/H0 comparison value (NOT a prediction).
"""
import json
import mpmath as mp
mp.mp.dps = 50

G = mp.mpf("6.67430e-11")
c = mp.mpf("299792458")
H0 = mp.mpf("67.4") * mp.mpf("1000") / mp.mpf("3.085677581491367e22")
a0_can = mp.mpf("9.3619e-11")
a0_alt = mp.mpf("1.1279e-10")
KAPPA = mp.mpf("0.5")

rho_can = 4 * a0_can ** 2 / (G * c ** 2)
rho_alt = 4 * a0_alt ** 2 / (G * c ** 2)

out = {}
# kappa=1/2 fixed -> changed density (this is the adopted reading)
out["kappa_fixed_half"] = {
    "rho_canonical_kg_m3": mp.nstr(rho_can, 12),
    "rho_alternative_kg_m3": mp.nstr(rho_alt, 12),
    "rho_alt_over_rho_can": mp.nstr(rho_alt / rho_can, 12),
    "note": "kappa=1/2 held fixed: the alternative footing is a DIFFERENT vacuum density (factor (a0_alt/a0_can)^2)."}
# rho held fixed instead -> effective kappa
kappa_eff = a0_alt / (c * mp.sqrt(G * rho_can))
out["rho_fixed_canonical"] = {
    "effective_kappa_for_alt_a0": mp.nstr(kappa_eff, 12),
    "note": "If rho were held at the canonical value, alternative a0 implies kappa != 1/2; the two footings cannot share both."}
kappa_eff2 = a0_can / (c * mp.sqrt(G * rho_alt))
out["rho_fixed_alternative"] = {
    "effective_kappa_for_can_a0": mp.nstr(kappa_eff2, 12),
    "note": "Reverse bookkeeping (illustrative only; adopted cell keeps kappa=1/2)."}
# which H
Lam_can = 8 * mp.pi * G * rho_can / c ** 2
HL_can = c * mp.sqrt(Lam_can / 3)
out["which_H"] = {
    "H_L_used": "c*sqrt(Lambda_eff/3) with framework rho_Lambda = 4 a0^2/(G c^2) and Einstein coupling G_E (taken = G_N for the numerics; ratio carried symbolically)",
    "H_L_canonical_s": mp.nstr(HL_can, 12),
    "H0_note_s": mp.nstr(H0, 12),
    "H0_comparison": "H0 = 67.4 km/s/Mpc is NOT H_L; quoted for reference only.",
    "critical_density_H_comparison": "H_sqrt(rho_crit) = sqrt(8 pi G rho_crit/3) = H0 = " + mp.nstr(H0, 12) + " s^-1 by definition of rho_crit (not used in H_L; H_L uses framework rho_Lambda, not critical density)",
    "R_dS_c_over_H0_m": mp.nstr(c / H0, 12),
}
print(json.dumps(out, indent=1))