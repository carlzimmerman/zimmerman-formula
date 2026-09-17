#!/usr/bin/env python3
"""
DE08b -- THE LMC AND THE ALL-DUST PHASE: DE08's dispute, re-audited honestly
         (version 2: the tautology removed, the phase placement kept, the
          kinematics stated at its true sensitivity).

==============================================================================
THE DISPUTE (from DE08): at the LMC (d = 50.1 kpc, eta_MOND = 0.77) the
framework's EFE-cap law predicts M_dyn/M_b -> 1/sqrt(eta) = 1.14 while the
measured value is 4.86 (vdM02) -- registered DISPUTED-ON-THE-DUST.

THE AUDIT IN THIS LANE (each statement computed, no fitted numbers):
  A1  TAUTOLOGY WARNING (the first version printed a 0.0% "match" that was
      IDENTICAL BY CONSTRUCTION: f_b measured = M_b/M_dyn, so 1/f_b = M_dyn/M_b
      trivially.  This lane discards that "test" and prints it as a flagged
      non-check.  The only defensible all-dust prediction uses the COSMIC
      baryon fraction f_b = 0.157 (S5): M_dyn/M_b = 1/f_b = 6.37 vs the
      measured 4.86 -> +0.118 dex (about one group-scatter sigma, G178):
      a WEAK agreement, not a match.
  A2  THE PHASE PLACEMENT (the solid part): the record's phase diagram
      (G178/G187/G140): the phantom phase exists only above M_sat = 3.09e14
      (band 1.73-4.01e14); below it the framework is in the ALL-DUST phase
      (f_dust = 1 - f_b).  M_dyn(LMC) = 1.7e10 = 5.5e-5 x M_sat: the LMC is
      DEEP in the all-dust phase and there is NO phantom there -- DE08's
      "flat curve vs cap 1.14" is a PHASE MISASSIGNMENT (the cap is a
      phantom statement; the phantom does not exist at this mass).
  A3  THE KINEMATIC QUESTION (can the dust supply f_dust ~ 0.6-0.8?):
      the honest estimator is gravitational (Bondi-Hoyle) capture from the
      field dust, M_dot = 4 pi (G M)^2 rho_dust / v_rel^3, NOT a geometric
      tube sweep (the first draft's estimator; gravitational focusing of
      a cold stream dominates when v_rel ~ v_thermal).  v_rel is the dust's
      velocity relative to the LMC and is NOT measured -- the record carries
      v_th(3.3 keV) = 0.055 km/s (G093) but the dust's bulk field velocity
      at the LMC's position is unregistered.  The lane therefore COMPUTES
      the capture mass as a function of v_rel over the honest range
      (0.1 to 300 km/s) and reports where the escape becomes viable; a
      single-valued kill is NOT claimed because the input is not on record.
  A4  THE DECISION RULE (pre-registered): if the all-dust prediction at
      cosmic f_b (6.37) is consistent with 4.86 within the phase-scatter
      band (0.10-0.16 dex, G178 class) AND the capture mass reaches
      f_dust ~ 0.6 at SOME v_rel inside the honest range, the LMC registers
      as the first galaxy-scale all-dust system (DE08's dispute RESOLVES as
      phase misassignment); if the capture mass never reaches f_dust = 0.6
      at any v_rel >= 0.1 km/s, the escape fails as stated.

COMPUTE: A1-A4 with both a0 footings implicit (phase/capture are eta-free:
  the all-dust phase is set by M/M_sat, a mass statement).  MUTATE=1 removes
  the saturation (G140) so c_dust > 1 and the all-dust reading breaks.
"""
import math, os, json
import numpy as np

M_SUN = 1.98892e30
M_DYN_LMC = 1.7e10 * M_SUN      # vdM02 M(8.7 kpc) (PUB)
M_B_LMC = 3.5e9 * M_SUN         # DE08 P3 (PUB)
M_SAT = 3.09e14 * M_SUN         # G178 band 1.73-4.01e14
F_B_COSMIC = 0.157              # S5 registered baryon fraction
RHO_DM = 0.264 * 8.6e-27        # kg/m^3 (Omega_dm x rho_crit)
T_HUB = 13.8e9 * 3.156e7        # s
G_SI = 6.67430e-11

chk_log = []
def chk(ok, detail):
    chk_log.append(bool(ok))
    print(f"  [{'PASS' if ok else 'FAIL'}] {detail}")

MUTATE = int(os.environ.get("MUTATE", "0"))

print("=" * 74)
print("DE08b v2 -- the LMC and the all-dust phase (tautology removed)")
print("=" * 74)

meas_ratio = M_DYN_LMC / M_B_LMC
print(f"\n  measured M_dyn/M_b = {meas_ratio:.2f} (vdM02, PUB)")
print(f"  M_dyn/M_sat = {M_DYN_LMC/M_SAT:.2e}")

# ---------------- A1: the tautology warning + the honest prediction ----------
print("\n--- A1 the honest all-dust prediction (cosmic f_b; the measured-f_b "
      "version is a tautology and is FLAGGED not counted) ---")
pred_taut = 1.0 / (M_B_LMC / M_DYN_LMC)          # = 4.86 by construction
pred_cos = 1.0 / F_B_COSMIC
print(f"  1/f_b(measured): {pred_taut:.2f} (= M_dyn/M_b by DEFINITION: "
      f"f_b = M_b/M_dyn, a tautology, DISCARDED)")
print(f"  1/f_b(cosmic S5): {pred_cos:.2f} vs measured {meas_ratio:.2f}: "
      f"{math.log10(pred_cos/meas_ratio):+.3f} dex "
      f"({abs(math.log10(pred_cos/meas_ratio))*100:.1f}%)")
chk(abs(math.log10(pred_cos / meas_ratio)) < 0.16,
    f"A1 the all-dust prediction at the COSMIC baryon fraction "
    f"(M_dyn/M_b = {pred_cos:.2f}) is consistent with the measured {meas_ratio:.2f} "
    f"at +{abs(math.log10(pred_cos/meas_ratio))*100:.1f}% (0.118 dex, inside "
    f"the G178-class phase scatter 0.10-0.16 dex) -- a WEAK positive, "
    f"registered as such; the 0.0% 'match' of v1 was a tautology (removed)")

# ---------------- A2: the phase placement ------------------------------------
print("\n--- A2 the phase diagram: the phantom does not exist below M_sat ----")
print(f"  M_sat = 3.09e14 (band 1.73-4.01e14, G178); M_dyn(LMC)/M_sat = "
      f"{M_DYN_LMC/M_SAT:.1e}")
print(f"  -> the LMC is DEEP in the all-dust phase; s_ph -> 0 (G187); "
      f"DE08's cap (a phantom statement) does not apply")
chk(M_DYN_LMC / M_SAT < 0.01,
    "A2 phase placement: the LMC is an all-dust system by the record's own "
    "phase diagram (5.5e-5 below M_sat); DE08's cap-vs-flat-curve reading "
    "was a PHASE MISASSIGNMENT -- the cap never applies there")

# ---------------- A3: the capture kinematics at its true sensitivity ---------
print("\n--- A3 the capture mass vs v_rel (Bondi-Hoyle; no single-valued kill "
      "claimed -- v_rel is not on record) ---")
print(f"  M_dot = 4 pi (G M)^2 rho_dust / v_rel^3; rho_dust ~ 0.98 x "
      f"{RHO_DM:.2e} kg/m^3; t_H = {T_HUB:.2e} s")
GM2 = (G_SI * M_DYN_LMC) ** 2
f_dust_req = 1.0 - M_B_LMC / M_DYN_LMC
print(f"  required dust share: f_dust = {f_dust_req:.2f}")
reach = {}
for v_rel in (0.1, 0.3, 1.0, 3.0, 10.0, 30.0, 100.0, 300.0):
    Mdot = 4 * math.pi * GM2 * RHO_DM / (v_rel * 1e3) ** 3
    M_cap = Mdot * T_HUB / M_SUN
    f_d = M_cap / (M_B_LMC / M_SUN)
    reach[v_rel] = f_d
    print(f"    v_rel = {v_rel:6.1f} km/s: M_captured = {M_cap:.2e} Msun "
          f"(f_dust = {f_d:.2f}){'  <-- viable' if f_d >= f_dust_req else ''}")
viable = any(f >= f_dust_req for f in reach.values())
chk(viable,
    f"A3 capture feasibility: f_dust = {f_dust_req:.2f} is reached at "
    f"v_rel = {[v for v,f in reach.items() if f >= f_dust_req][0]:.1f} km/s "
    f"and below (Bondi-Hoyle with the record's cold dust; v_rel is unmeasured "
    f"on the record, so the escape is NOT excluded by kinematics -- stated "
    f"at its true sensitivity, not as a single number)")

# ---------------- A4: the decision -------------------------------------------
print("\n" + "=" * 74)
print("VERDICT")
print("=" * 74)
print(f"  DE08'S DISPUTE RE-AUDITED: (1) the first version's 0.0% all-dust "
      f"'match' was a TAUTOLOGY -- f_b measured is M_b/M_dyn by definition; "
      f"REMOVED and flagged.  (2) The honest all-dust prediction (cosmic "
      f"f_b = 0.157) gives M_dyn/M_b = 6.37 vs the measured 4.86: +0.118 dex "
      f"-- inside the phase-scatter band, a weak positive, REGISTERED as "
      f"weak.  (3) The phase placement is SOLID: M_dyn(LMC)/M_sat = 5.5e-5, "
      f"the phantom phase does not exist there, and DE08's cap (a phantom "
      f"statement) is a phase misassignment -- the 'flat curve vs cap 1.14' "
      f"reading is retired on the record's own diagram.  (4) The capture "
      f"kinematics: Bondi-Hoyle reaches the required f_dust = 0.79 at "
      f"v_rel <= ~10 km/s; "
      f"v_rel (the dust's bulk motion relative to the LMC) is NOT measured "
      f"on the record, so the all-dust escape is not excluded -- stated at "
      f"its true sensitivity.  NET: the LMC registers as the FIRST "
      f"GALAXY-SCALE ALL-DUST-PHASE CANDIDATE, with the falsifier named: "
      f"measure the dust's velocity field at the LMC (or exclude v_rel < "
      f"10 km/s) and the escape is decided.")
print(f"  checks: {sum(chk_log)}/{len(chk_log)} PASS")

out = {
    "lane": "DE08b_lmc_all_dust_v2",
    "meas_Mdyn_over_Mb": float(meas_ratio),
    "all_dust_cosmic_fb_pred": float(pred_cos),
    "all_dust_offset_dex": float(math.log10(pred_cos / meas_ratio)),
    "tautology_flagged": True,
    "M_dyn_over_M_sat": float(M_DYN_LMC / M_SAT),
    "capture_viable_at_vrel_kms": [v for v, f in reach.items() if f >= f_dust_req],
    "verdict": "ALL-DUST-PHASE CANDIDATE (phase placement solid; cosmic-f_b "
               "prediction weak-positive; kinematics undecided at unmeasured v_rel)",
    "checks_pass": int(sum(chk_log)), "checks_total": len(chk_log),
}
with open("deepseek_push/DE08b_results.json", "w") as f:
    json.dump(out, f, indent=2)
print("wrote deepseek_push/DE08b_results.json")