# QX28: two-phase superfluid cold dark energy sector (Berezhiani-Khoury class). FAILS at G3, G4, G5, G6 and G8

Kappa = 1/2 FITTED; not theory closed. **This lane adopts nothing.**

- **TEST lane.** The owner's no-particle rule is relaxed for this lane only, as it was for HF1. The sector is written
  as a scalar condensate field, the COLD DARK ENERGY sector. No LCDM inputs are used.
- **Criteria:** FROZEN_CRITERIA.md (c5852ac12f), committed and pushed alone before any script or number.
- **Scripts:** qx28.py (static gates, about 30 s) and qx28_growth.py (G6, about 5 s), one thread each. Logs are
  run_main.txt, run_growth.txt and run_mutate.txt. MUTATE outputs are qx28_MUTATE.json and qx28_MUTATE.out.
- **The law:** only the framework's g_N = g^2/(g + a0), on canonical 9.3603e-11 and alt 1.1312e-10 m/s^2.
- **KA0 PASS:**
  - The script scan finds no standard-MOND a0 literal; the script exits if one appears.
  - Each law function satisfies g_N = g^2/(g + a0) to 5.7e-16.
  - The library a0 equals the footing values to 3.5e-6.
- **Background, not reused:** the quarantined LCDM_FRIED_CHICKEN A22 / recipe24 work.

## The class as built

**Condensed phase.**
- The sector follows BK's X^(3/2) equation of state, P = K rho^3, in Thomas-Fermi equilibrium in the Newtonian
  potential of the baryons plus itself.
- Total mass is the cosmic share, R M_b with R = 5.562; the host keeps the part inside r_ta.
- Phonons give the law's force on baryons and are sourced by the baryons only. So g = glaw(g_N,b) + G M_X/r^2: the
  condensate's own mass adds Newtonian pull and does not enter the law.

**Normal phase.**
- No phonons, so no law force.
- The sector is cold Newtonian mass at R M_b(<r), tracing the baryons, as in QX12 iter_2.

**Phase rule (BK virialisation overlap).**
- A host is condensed if M_b,tot <= M_c.
- M_c = 2.689e11 Msun, the largest calibration host (a SPARC galaxy). It comes from galaxies only.

**K from galaxies only.**
- The rule takes the smallest grid K at which SPARC G5 (C1) and KiDS (C2) pass, at that K and every larger grid
  value.
- K_min = 1.585e-6 (canonical) and 1.0e-6 (alt), in (km/s)^2 kpc^6 Msun^-2.
- The condensate core is then R_TF ≈ 0.15-0.26 r_ta, with every bit of R M_b kept.
- Implied BK constants (reported only):
  - m ≈ 0.57 / 0.55 eV
  - Lambda ≈ 0.11 / 0.15 meV
  - alpha ≈ 3.5 / 3.0
  - These sit in BK's own eV / meV range.

## Labels

| Gate | canonical | alt | key numbers |
|---|---|---|---|
| G1 SPARC exact field | PASS | PASS | rms 0.0591 @ U 0.58 / 0.0621 @ 0.51 (line 0.110, U 0.50-0.80; alt U sits near the edge) |
| G2 KiDS (calibration) | PASS | PASS | shift -0.049 / -0.049 (line 0.05; set K_min) |
| G3 X-ray ellipticals | **FAIL** | **FAIL** | D -0.161 / -0.172 (line 0.15; 3 of 7 condensed). Other phase: +0.203 / +0.181, also FAIL |
| G4 X-COP | **FAIL** | **FAIL** | +0.120 / 0.139 (the normal phase is Newtonian, so the value is the same on both footings) |
| G5 groups | **FAIL** | **FAIL** | band [+0.129, +0.430], strict 0-1 / 20 |
| G6 T1 + growth | **FAIL** | **FAIL** | G6a: lambda_J(z 1089) 4.2e5 / 3.3e5 Mpc, w(1089) 3e4 / 2e4. G6b: Delta chi^2 140 / 70 (line 4). G6c forest: 0.34 / 0.27 Mpc, PASS |
| G7 dSphs | PASS | PASS | median shift 0.0000 |
| G8 Cassini | **FAIL** (inherited) | **FAIL** (inherited) | The static phonon field is AQUAL-type with this law, so AX1's grade applies: Q2 2.44-4.55x Hees. No screen is derived here |
| G9 Bullet offset | NOT EVALUABLE | NOT EVALUABLE | Needs a merger run with the phase transition and the sector's self-interaction cross-section (BK's thermalisation) |

**Overall: FAILS at G3, G4, G5, G6 and G8, on both footings. G9 is NOT EVALUABLE.**

## The key question: does the halo condensate over-predict KiDS?

**No, with the BK force structure.** Galaxies hold all of R M_b inside 300 kpc, and the KiDS shift is still only
-0.049. The phonons are sourced by baryons alone, so the condensate adds only Newtonian G M_X/r^2. At KiDS radii
g_bar << a0/R^2 ≈ 3e-12 m/s^2, and there that pull is small against the law's sqrt(a0 g_N).

QX7 and QX10 got 0.15-0.27 dex because their sector sat inside the law, glaw(G(M_b + M_X)/r^2). T2 at KiDS is
therefore not the corner that kills this class.

## What kills it

1. **T3 (G4, G5): the phase boundary cannot put clusters and groups right.**
   - Normal phase, with no phonons and Newtonian (1 + R) M_b: X-COP +0.120 / 0.139 and groups [+0.13, +0.43]. That
     is too little mass.
   - Always condensed (M1), with the law plus the condensate: X-COP -0.21 / -0.26. That is too much. Groups
     [-0.19, +0.01] pass there.
   - The measured clusters sit between the two phases. Only a partial condensate fraction in clusters could reach
     them, and nothing from galaxies fixes that fraction. Setting it from clusters would be cluster-set.
   - Any M_c from 2.69e11 up to the lightest group (1.35e12) leaves every group (f_st 0) and every X-COP host normal,
     so the T3 result does not hang on where M_c sits.
2. **The ellipticals (G3) fail in either phase.**
   - Condensed ellipticals are over-massed by the compact core, because g there is near a0 and the Newtonian R M_X
     matters. The graded D is -0.16 / -0.17.
   - Normal-phase ellipticals keep the law's deficit, +0.20 / +0.18.
3. **T1 (G6).**
   - The condensed equation of state at the cosmic mean has c_s ∝ rho_bar ∝ a^-3. As posed, the sector is stiff and
     superluminal before recombination: c_s(1089) ≈ 9e7 km/s.
   - Even holding it cold for z > 10, which is generous, growth after z = 10 fails: Delta chi^2 140 / 70.
   - Growth passes only for K <= 1e-7. KiDS needs K >= 1e-6 (K = 1e-8 gives C2 -0.089, M3). That is a gap of about
     10 in K, the same T1-against-T2 squeeze as QX27.
   - For G6a, cold at recombination needs K below about 4e-18. The condensate would then be compact, and C1/C2 fail.
4. **G8.** The class's static limit is AQUAL with the law's interpolation, so AX1's Cassini Q2 failure carries over.
   BK's EFT-breakdown screening is asserted in the literature, not derived here.

## MUTATE and controls

- **M1, always condensed: BITES** on both footings. It fails G3 (+0.20 / +0.18) and G4 (-0.207 / 0.290 and
  -0.264 / 0.320). Groups pass, [-0.19, +0.01] and [-0.24, -0.04].
- **M2, always normal: BITES.** C1 4.61; C2 +0.76 / +0.80; G1 rms 0.36; G3 -0.40.
- **M3, K = 1e-8: BITES.** C1 0.425, C2 -0.089 / -0.082.
- **G6 controls:**
  - K = 1e-30 gives Delta chi^2 0, the cold limit.
  - K = 1e3 gives 657, so the gate has power.
- **Known answers, all PASS:**
  - KA1: Lane-Emden n = 1/2 gives xi_1 2.75270 and omega_1 3.78865. The solver's R and rho_c agree within 0.07 %.
  - KA2: ellipticals +0.2099 / +0.1887, matching QX18.
  - KA3: R = 0 gives X-COP +0.4675 / +0.4345.
  - KA4: R = 0 gives SPARC 0.0560 @ 0.58 / 0.0558 @ 0.52, matching QX8.
  - KA5: K = 1e4 gives C2 0.0000.

## Disclosures

- Simplifications of the model:
  - The condensate feels Newtonian gravity only; the phonon back-reaction on it is ignored.
  - The normal-phase profile traces the baryons (QX12 iter_2's frozen rule), not a collapse profile.
  - The phase is set per host, not per radius. BK's partially condensed cluster cores are not modelled. They are
    the natural next iteration, but their fraction would have to come from a coherence rule fixed by galaxies.
- G6 uses QX27's copy of the QX3 iter2 solver with the fluid Jeans term from c_s(a), at iter2's worst corner.
- G8 is inherited from AX1 and was not recomputed.
- The alt G1 median U, 0.51, sits near the 0.50 edge.
- The git-ignored data (KiDS Brouwer+2021, the PR4 bandpowers) was read from the existing local copies.
