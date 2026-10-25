# X32_bullet_cold_sector: FROZEN CRITERIA (committed alone, before any script or number of this lane)

κ = ½ FITTED. Footings canonical a₀ 9.3603e-11 / alt 1.1312e-10 m s⁻², never pooled. The cold sector ("cold energy",
Ω_c/Ω_b = 5.364) is gravitating field mass, never a particle; that holds in the collisionless reading too, even where it
behaves like dark matter. Theory frozen as v3s (`covariant_push_2026_10_22/V3S_FINAL_VERDICT_2026-10-24.md` §7–8); target =
X26's scenario-B sheet (`rebuild_2026_10_22/COLD_SECTOR_SPEC_2026-10-24.md` R6 and §4 "collisionless heat"). Nothing is
fitted. Never "theory closed". Never "the data favour the framework". No downloads; no lensing map exists on disk.

**Question.** In the Bullet Cluster (1E 0657-56, z = 0.296), does a cold sector at the X26 sheet's sound speed end up with
the X-ray gas or with the galaxies? How does that depend on its micro-nature, (F) collisional fluid or (C) collisionless with
the same equilibrium? Which reading, if either, is compatible with the observed lensing offset?

**Seen before freezing.** COLD_SECTOR_SPEC; V3S verdict §7–8; X26 README, `.out` (energy and A2 lines) and JSON (`energy`,
`A2_direct`); X23_late_heated_cold README Bullet note and its `vcoll = 4500` line; X30 criteria §1 (ρ_b convention);
`hunt_2026/h57_bullet_peaks.py` and `.out`; `opus_48_extended_research/reviews/bullet/bullet_data_table.py` (and its printed
output); `deepseek_push/G110_bullet_audit.out` (parts A–D header); `fable_independent_2026/L85_BULLET_CLUSTER_LENSING.md`;
`qwen_claude_field_theory/closure_2026/condensate_pincer_2026/merger_gate_supported_media_2026.py`;
FAILURES_EXECUTIVE_SUMMARY row B6; `rebuild_2026_10_22/F2_outer_lensing/f2_aqual.py` header (v3 kernel). No number of this
lane's model exists.

## 1. Numbers used (record line, or PROVISIONAL)

| quantity | value | source |
|---|---|---|
| sheet c_s at the KT-cluster median (σ 517.1 km/s, ρ_b 1.35e-5 M☉ pc⁻³) | canonical 556–736, alt 595–761 km/s | X26 JSON `energy[f]["KT cluster median"]["cs_kms"]`; `.out` l. 417/419; README table |
| sheet points | 19 (canonical) / 16 (alt) (c_*, r, q) | X26 JSON `A2_direct` rows with `allowed: true` |
| baryon model (Plummer M, a, x, y), model frame | GAS 4 comps, GAL 2 comps; BCG1 (0,0), BCG3 (820,220) kpc | h57 l. 46–49 (Famaey 2026 Table 1 as transcribed) |
| lensing M_2D(<300 kpc) at BCG1 / BCG3 | 3.5e14 / 2.3e14 M☉ | h57 l. 50 (Rihtaršič+2026 via Famaey 2026) |
| Σ_crit | 1.827e9 M☉ kpc⁻² | h57 l. 42 |
| h57 reproduction targets (Route A, a₀ 9.36e-11 / 1.13e-10) | M_bar 4.203e13 / 2.359e13; M_ph 6.826e13 / 4.934e13 (can.), 7.659e13 / 5.508e13 (alt) | h57.out l. 15, 24–27 |
| Clowe 2006 Table 2 (J2000; κ̄ in 100 kpc) | BCG/plasma coordinates; κ̄ main BCG 0.36±0.06, main plasma 0.05±0.06, sub BCG 0.20±0.05, sub plasma 0.02±0.06 | bullet_data_table.py l. 56–61 |
| plate scale | 4.413 kpc/″ | bullet_data_table.py l. 39 |
| derived galaxy–plasma offsets; BCG–BCG | 209.4 / 194.1 kpc; 721.5 kpc | bullet_data_table.py l. 87–93 (recomputed in step 0) |
| offset significance | ~8σ each peak; peaks "within 1σ of the galaxies" | bullet_data_table.py l. 101–104 |
| collision speeds | bulk 2700 km/s (Springel & Farrar 2007); bow shock 4740 (+710/−550) km/s, Mach 3.0 ± 0.4, T 14.1 keV (Markevitch 2006) | bullet_data_table.py l. 23, 141–144 |
| halo masses for the passage wells | M200 main 1.5e15, bullet 1.5e14 M☉ (SF07 sims); fallback bullet total 2.3e14 (Markevitch 2002) | bullet_data_table.py l. 125–127 |
| cosmology for r_200 | H₀ 70, Ω_m 0.3, Ω_Λ 0.7 (Clowe 2006 plate-scale cosmology) | bullet_data_table.py l. 44 |
| impact parameter | b = 0 graded (most destructive for retention); b = 150 kpc reported only | **PROVISIONAL** (from memory; order of the value in Springel & Farrar 2007 / Mastropietro & Burkert 2008) |
| aperture-mass error for O3 | 15 % | **PROVISIONAL** (from memory; typical of the JWST lens-model aperture masses, Rihtaršič+2026) |

The record has no per-subcluster temperature; the 14.1 keV value is used only in the reported Bullet-own c_s.

## 2. The two readings

- **(F) perfect fluid**, isothermal sound speed c_s (P = ρ c_s²): X23/X26's hydrostatic profile ln ρ = ∫ g dr / c_s².
- **(C) collisionless**, isotropic Maxwellian with σ_1D = c_s, i.e. σ_3D = √3 c_s. This is the mapping that gives the same
  equilibrium (isotropic Jeans with σ_1D² = P/ρ). No other mapping is graded.

Graded c_s values per footing: the two ends of the KT-median sheet range (canonical 556, 736; alt 595, 761 km/s, read from
the JSON, not rounded). Graded speeds: v = 2700 and 4740 km/s. Graded b = 0.

## 3. Method (derived from stated assumptions; small jobs only)

1. **Law (both readings).** v3 kernel μ(x) = x/(1+x), ν(y) = ½(1 + √(1 + 4/y)) (f2_aqual.py header). QUMOND-type phantom
   ρ_ph = ∇·[(ν − 1) g_N]/4πG (the record's h57 estimator, stated: not the AQUAL solve), sourced by baryons + cold (X26
   convention: cold self-mass sources the law and lenses). Aperture masses by h57's divergence-theorem surface integral;
   the map by finite differences on a 3-D grid (10 kpc in x, y), projected. h57's negligible g_ext = a₀/1000 kept.
2. **Passage wells (C).** Two rigid Hernquist spheres, M_main = 1.5e15, M_sub = 1.5e14; scale radii solved so that the summed
   projected mass within 300 kpc of each centre (centres 849 kpc apart, the model-frame BCG separation) equals 3.5e14 /
   2.3e14. If no solution, M_sub = 2.3e14; if still none, step 0 fails.
3. **Cold equilibrium.** ρ_c ∝ exp(−[Φ_H(r) − Φ_H(0)]/c_s²) for r < r_200(M_H, z = 0.296); velocities Maxwellian σ_1D = c_s
   truncated at v_esc(r) = √(2[Φ(r_200) − Φ(r)]). N = 20 000 test particles per halo.
4. **Passage (C).** Rigid wells on a straight line in the sky plane at constant relative speed v, CM frame; start 4000 kpc
   before pericentre, stop at 849 kpc after. Leapfrog dt = 0.5 Myr. Isolated controls (no partner) for the same time.
   - f_ret,i = (halo-i particles within projected 300 kpc of its own centre at the end) / (same in its control).
   - Δx_c,i = mean projected offset, along the axis, of those particles from the centre (positive = toward the partner).
5. **C map.** Cold of halo i = f_ret,i × A_i × (equilibrium shape), centred at its galaxy centre (BCG1, BCG3) shifted by Δx_c,i.
   A_i (pre-merger cold mass) solved so the model M_2D(<300 kpc) at BCG1, BCG3 = 3.5e14, 2.3e14 (baryons + cold + phantom).
   This fixes the amount from the aperture masses, not from the offset; O3 is therefore not a test of C.
6. **F placement (same A_i).** Gunn–Gott: the sub's fluid is retained inside r_s where ρ_sub,c(r_s) c_s² = ρ_main,c(0) v²;
   f_core = M_sub,c(<r_s)/A_sub, centred at the bullet gas (670,170). The stripped sub fluid and all the main fluid go to:
   - **F-a** the main-gas centre (190,90);
   - **F-b** the inelastic-merger point BCG1 + 849 kpc × m_s/(m_m + m_s) along the axis (m_s stripped sub fluid, m_m main
     fluid; gravity's pull-back ignored, an upper bound on the drift).

   F is graded at whichever of F-a / F-b is more favourable to it (smaller worst |Z|) at each combination. Mach numbers
   v/c_s and the Gunn–Gott ratio are reported.
7. **Observables** (model frame: BCG1 (0,0), main gas (190,90), BCG3 (820,220), bullet gas (670,170)):
   - **O1, offset.** δ_i = d(peak_i, gas_i) / d(BCG_i, gas_i). peak_i = the maximum of Σ_tot within 350 kpc of the
     BCG_i–gas_i midpoint. Observed δ = 1 (peaks on the galaxies). σ_δ = √((1/8)² + 0.15²): 1/8 from the 8σ offset
     significance; 0.15 is this toy's model floor. Z = (δ − 1)/σ_δ. Absolute offsets are reported against 209.4 / 194.1 kpc
     (the model frame's galaxy–gas separations are 210 / 158 kpc).
   - **O2, mass contrast near each subcluster.** Δκ_i = κ̄_100(BCG_i) − κ̄_100(gas_i). Observed main +0.31 ± 0.085, sub
     +0.18 ± 0.078 (Table 2, errors in quadrature). Clowe's κ normalisation (source redshifts, mass sheet) differs from
     Σ_crit 1.827e9, so **only the sign is graded**: Δκ_pred,i ≤ 0 fails (the observed values are positive at 3.6σ / 2.3σ).
     The amplitudes and the ratio κ̄_100(BCG3)/κ̄_100(bullet gas) (observed 0.20 / 0.02) are reported.
   - **O3, aperture masses** (F only): M_2D(<300 kpc) at BCG1, BCG3 vs 3.5e14 / 2.3e14, σ = 15 % (PROVISIONAL).
   - **Amount admissibility** (C only, graded): A_main + A_sub ≤ 5.364 × M_b(model total). The per-halo split is reported.

## 4. Verdict classes

Per reading and footing, at each graded combination (2 c_s × 2 v, b = 0):
- **ALLOWED**: every graded observable passes (O1 |Z| ≤ 2 both peaks; O2 positive both; O3 |Z| ≤ 2 both for F; cap for C)
  at every combination.
- **EXCLUDED**: at every combination, at least one graded observable fails (O1 |Z| > 3, an O2 sign wrong, O3 |Z| > 3, or the
  cap violated).
- **TENSION**: otherwise.

Lane verdict:
- **FLUID EXCLUDED, COLLISIONLESS ALLOWED**: F EXCLUDED and C ALLOWED on both footings.
- **BOTH EXCLUDED**: both EXCLUDED on both footings.
- **BOTH ALLOWED**: both ALLOWED on both footings.
- **UNDECIDED**: anything else, including a step-0 failure, any TENSION, a footing split, or F allowed with C excluded.

## 5. Step 0 (stop rule: all must pass, else UNDECIDED and no graded number)

- **K0a.** The X26 sheet: the `A2_direct` allowed counts are 19 / 16. Recomputing c_s = c_* (517.1/100)^r (1.35e-5/1e-3)^{q/2}
  over those points matches the JSON `energy` KT-median range to ≤ 1 % (the inputs are rounded in the `.out`).
- **K0b.** This lane's surface integral, with Route A at h57's a₀, reproduces the h57.out M_bar and M_ph at BCG1 / BCG3 on
  both footings to ≤ 1 %.
- **K0c.** The Clowe Table 2 coordinates give 209.4 / 194.1 / 721.5 kpc to ≤ 0.1 kpc.
- **K0d.** Every transcribed number of §1 appears verbatim in its record file (string search).
- **K0e.** The well calibration (§3.2) has a solution.

## 6. Checks

- K1: the surface integral vs the exact deep-MOND cylinder mass of a point mass (≤ 1 %).
- K2: isolated control equilibrium: each halo's fraction within 300 kpc at the end is ≥ 0.95 of the start.
- K3: map phantom vs surface integral in the BCG1 300 kpc aperture (≤ 8 %).
- K4: the A_i normalisation residual is ≤ 1 %.
- K5: peak RSS < 1 GB.
- K6: f_ret at dt vs dt/2 (one combination) agree to ≤ 0.02.

## 7. MUTATE (`X32_MUTATE=1`; outputs `*_MUTATE.out/json`; exit 1 required)

- m1: Plummer gas masses × 2 in the step-0 reproduction ⇒ **K0b must FAIL**.
- m2: plate scale 3.413 instead of 4.413 ⇒ **K0c must FAIL**.
- m3: the well force's sign flipped in the passage ⇒ **K2 must FAIL**.

## 8. Reported only (never graded)

- The law alone (baryons + phantom, no cold, v3 kernel): where its peaks sit (h57 57-F analogue).
- Bullet-own c_s per sheet point: σ from 14.1 keV (X26 convention σ = (kT/0.6 m_p)^½), and ρ_b = M_b(<548 kpc)/(4π 548³/3)
  from the Plummer model (X30 §1 convention).
- c_s at z = 0.296 for p = 3, 4, 6 (factor a^{p−½}; X26 grades clusters at the z = 0 value).
- b = 150 kpc; the M_sub fallback; a CDM-like comparator (σ_1D = V_c(300 kpc)/√2 of each well).
- The micro-nature reading. Whether a collisionless, late-heated cold sector is distinguishable from dark matter in any test
  the record has (R3 / SPARC, X22 forest and σ₈, X29 late S8, X30 cluster profile).
