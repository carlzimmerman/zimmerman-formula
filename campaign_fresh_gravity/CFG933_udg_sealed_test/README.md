# CFG933: CFG928's sealed P2 prediction scored on the ultra-diffuse galaxies on disk

**Bottom line.** Under the frozen rule, the UDGs on disk neither exclude P2 nor support it. The class on both footings is
**NOT DIAGNOSTIC**, labelled **FRAGILE**.

- **Coma UDGs.** The 9 admitted Coma UDGs sit at ⟨E_obs⟩ = **+0.760 / +0.669 ln**. P2's sealed prediction for the same
  galaxies is **+0.072 / +0.053**.
  - The gap is about 10× the prediction and about 0.8 of the LVD dwarf class mean that P2 was calibrated on.
  - With the record's conservative unweighted se, it is **z = +2.62 / +2.35**. The kill line needs 3.
- **NGC 1052-DF2 and -DF4.** Both sit far **below** the isolated law, at E = −1.71 / −2.17 (canonical). P2 cannot go there
  (E_pred ≥ 0).
  - Per galaxy: z −3.22 / −2.79 canonical, −3.37 / −2.88 alt. With N = 2 they are not graded by the kill line.
- **Pooled sample.** The two environments differ by 4.9σ, so the heterogeneity rule fires. The pooled mean (z +0.56 / +0.36)
  is a cancellation and is not read as consistency.
- **Power.** The sample lacks the power to certify consistency: 3 se_c = 0.789 against a target of 0.784 (canonical).

**FRAGILE.** Two declared sensitivity variants turn the class into **P2 EXCLUDED** on both footings:
- M* −0.2 dex (Coma z +3.42 / +3.17; the alt kill is MARGINAL);
- σ +15% for aperture (z +3.68 / +3.41).

**Reported, no class weight:**
- L23's inverse-variance weighting excludes P2 at z +5.8 / +5.4. This estimate has no scatter term.
- All 11 Coma UDGs (adding DF44 and J125904.06) give z +3.21 canonical (EXCLUDED) and +2.89 alt.
- The literal Υ = 2 on the band luminosity gives z +1.1 / +0.8.

**CFG31's disclosed offset holds under the sealed estimator.** Per galaxy the two estimators are identical (K5, to 4e-15). The
L23-weighted mean of the 11 Coma UDGs is +0.913 / +0.822 ln = **+0.397 / +0.357 dex**. What keeps P2 alive is the sealed
kill line's unweighted mean and the record's se convention, applied to a sample whose dispersion errors are large.

| footing | class | N | Coma ⟨E_obs⟩ | Coma ⟨E_pred⟩ (sealed band +0.02–0.14 / +0.016–0.105) | Coma se_c | Coma z | pool z | DF2 / DF4 z | H (Coma − group) |
|---|---|---|---|---|---|---|---|---|---|
| canonical (9.3603e-11) | **NOT DIAGNOSTIC** (FRAGILE) | 11 (9 + 2) | +0.760 (+0.330 dex) | +0.072 | 0.263 | **+2.62** | +0.56 | −3.22 / −2.79 | +2.67 ± 0.55 (4.9σ) |
| alt (1.1312e-10) | **NOT DIAGNOSTIC** (FRAGILE) | 11 (9 + 2) | +0.669 (+0.291 dex) | +0.053 | 0.262 | **+2.35** | +0.36 | −3.37 / −2.88 | +2.67 ± 0.55 (4.9σ) |

κ = ½ is FITTED. The footings are never pooled. Raw data and framework-native quantities only. The extra mass is cold energy,
not a particle. Not "theory closed". Nothing here says the data favour the framework.

- **Kind:** test of a SEALED prediction (CFG928 seal 3fa5a2bfc). Block 930–939.
- **Criteria:** `FROZEN_CRITERIA.md`, dd6dc4f35, committed alone before any script or E.
- **Amendment A1:** ea8ac96eb. It is post hoc, made after the K-only run and before any test number was printed. It changes
  the control tolerance only: K1's CFG31-R1 sub-check now runs through CFG31's own tabulated ν_mono kernel.
- **Results:** 87b15752e (script and all outputs).
- **Not blind with respect to the record:**
  - CFG31's +0.397 / +0.357 dex, the Coma table and CFG655's DF2/DF4 table were seen before freezing.
  - The expectations disclosed in criteria section 0 matched the outcome: Coma near the kill line, DF2/DF4 below the law.

## What this means for CFG928's survivor

- **The test did not settle P2.** P2's galaxy-scale survival in CFG928 stands, and with it the conditions CFG928 already
  attached: post hoc, C1-dependent, FRAGILE, failing on clusters. This sealed test did not kill it, but it could not
  confirm it either.
- **The UDGs point against P2.**
  - The admitted Coma UDGs carry a dwarf-like excess, residual +0.69 / +0.62 ln. P2 predicts that UDGs at σ_law ≈ 14–21 km/s
    carry almost none.
  - The NGC 1052 UDGs sit below the law, where no P2 solution exists.
  - Neither reaches the sealed 3σ under the frozen se, and the result flips to EXCLUDED under two of six declared
    sensitivity variants.
- **The honest status:** "P2 not excluded by the UDGs on disk; a 2.4–2.6σ excess in the direction the seal said would kill
  it; FRAGILE".
- **What would decide.** Halving the Coma σ errors, a larger set of pressure-supported UDGs with measured σ, or an independent
  M*/aperture calibration. The seal's own power example assumes se_obs ≈ 0.10; the sample on disk has 0.26.
- **DF2/DF4 are not a P2-specific failure.** They sit below the isolated, EFE-free law itself; the record already labels
  them collision debris (CFG655). Under the seal they count against P2 only in so far as P2 adds no host variable.

## Sample (rules S1–S5 of the criteria, applied mechanically; K4 confirms the expected membership)

| galaxy | env | M* (M☉) | R_e (kpc) | σ_obs (km/s) | σ_law (canon.) | E_obs (canon.) | sE | E_pred (canon.) | status |
|---|---|---|---|---|---|---|---|---|---|
| DFX1 | Coma | 2.47e8 | 3.6 | 30 ± 7 | 20.78 | +0.735 | 0.467 | +0.032 | admitted |
| J125848.94+281037.1 | Coma | 5.02e7 | 1.5 | 18 ± 13 | 13.97 | +0.507 | 1.444 | +0.093 | admitted |
| J125904.20+281507.7 | Coma | 6.49e7 | 1.6 | 17 ± 10 | 14.92 | +0.261 | 1.176 | +0.078 | admitted |
| J125929.89+274303.0 | Coma | 1.37e8 | 2.9 | 21 ± 7 | 17.89 | +0.320 | 0.667 | +0.049 | admitted |
| J125937.23+274815.2 | Coma | 5.80e7 | 1.8 | 22 ± 8 | 14.45 | +0.840 | 0.727 | +0.086 | admitted |
| J130005.40+275333.0 | Coma | 5.99e7 | 1.8 | 37 ± 6 | 14.57 | +1.864 | 0.324 | +0.084 | admitted |
| J130026.26+272735.2 | Coma | 1.33e8 | 3.7 | 19 ± 5 | 17.69 | +0.143 | 0.526 | +0.051 | admitted |
| J130028.34+274820.5 | Coma | 5.61e7 | 2.1 | 23 ± 7 | 14.28 | +0.953 | 0.609 | +0.090 | admitted |
| J130038.63+272835.3 | Coma | 6.15e7 | 1.9 | 27 ± 5 | 14.66 | +1.222 | 0.370 | +0.083 | admitted |
| NGC 1052-DF2 | group | 2.00e8 | 2.0 | 8.5 +2.3/−3.1 | 19.98 | −1.709 | 0.541 | +0.034 | admitted |
| NGC 1052-DF4 | group | 1.50e8 | 1.6 | 6.3 +2.5/−1.6 | 18.65 | −2.170 | 0.794 | +0.041 | admitted |
| DF44 | Coma | 3.90e8 | 4.7 | 33 ± 3 | | | | | out: S4 (M* > 3e8) |
| J125904.06+281422.4 | Coma | 6.36e7 | 1.4 | 25 ± 7 | | | | | out: S1 (R_e < 1.5) |
| NGC 1052-DF9 | group | 1.40e8 | 1.1 | 6.5 | | | | | out: S1, no UDG label |
| LEDA 4014647 | group | 9.55e7 | 0.60 | 15.8 | | | | | out: S1, no UDG label |

**Inputs.**
- M* is the source's stellar mass: L × SSP M/L for Coma, and CFG655's value for DF2/DF4. The seal's M* = 2 L_V could not be
  applied because no L_V is on disk; this was declared before any E was computed.
- All admitted galaxies are gas-free, so w = 1.
- The law is the isolated, EFE-free ν_e law: no Coma or NGC 1052 external field.
- The LVD dwarfs (P2's calibration set) and the Virgo dEs are not in the universe.

## Sensitivity set S (FRAGILE label) and reported rows R

| variant | canonical | alt |
|---|---|---|
| primary | NOT DIAGNOSTIC (Coma z +2.62) | NOT DIAGNOSTIC (Coma z +2.35) |
| S-M+ (M* +0.2 dex) | NOT DIAGNOSTIC (+1.78) | NOT DIAGNOSTIC (+1.50) |
| **S-M− (M* −0.2 dex)** | **P2 EXCLUDED** (+3.42) | **P2 EXCLUDED, MARGINAL** (+3.17) |
| S-D− (Coma ×0.95, DF2 17.6 Mpc, DF4 ×0.95) | NOT DIAGNOSTIC (+2.80) | NOT DIAGNOSTIC (+2.53) |
| S-D+ (×1.05, DF2 21.7 Mpc) | NOT DIAGNOSTIC (+2.45) | NOT DIAGNOSTIC (+2.18) |
| S-A− (σ ÷ 1.15) | NOT DIAGNOSTIC (+1.56) | NOT DIAGNOSTIC (+1.28) |
| **S-A+ (σ × 1.15)** | **P2 EXCLUDED** (+3.68) | **P2 EXCLUDED** (+3.41) |
| R1 L23 weighting (sE⁻², no scatter term), Coma 9 | z +5.77 | z +5.38 |
| R2a source label only (+J125904.06) | NOT DIAGNOSTIC (Coma 10: +2.94) | NOT DIAGNOSTIC (+2.65) |
| R2b no M* window (+DF44) | NOT DIAGNOSTIC (Coma 10: +2.90) | NOT DIAGNOSTIC (+2.59) |
| R2c both | P2 EXCLUDED (Coma 11: +3.21) | NOT DIAGNOSTIC (+2.89) |
| R2d all 11 Coma alone | P2 EXCLUDED (+3.21) | P2 CONSISTENT, 2–3σ tension (+2.89) |
| R3 Υ = 2 on band L (Coma) | NOT DIAGNOSTIC (Coma +1.12) | NOT DIAGNOSTIC (+0.82) |
| R4 DF2 Emsellem+19 10.8 / DF4 stars 8.0 km/s | z −2.13 / −3.01 | z −2.27 / −3.15 |
| R5 CFG31's 11, sealed estimator | unweighted +0.780 ln; L23-weighted +0.913 ln (= +0.397 dex) | +0.689; +0.822 (= +0.357 dex) |

In the table, z is the kill-line z of the Coma sample (or of the sample named).

**Reading the variants.**
- The class turns on the coherent systematics: M*/Υ and aperture.
  - A 0.2 dex lower M*, or dispersions 15% low, would exclude P2.
  - A higher M* (S-M+, R3) or an aperture correction downward (S-A−) moves the Coma excess toward P2.
- The sample rule matters at the margin. Admitting the two objects the frozen rules removed (DF44 by M*, J125904.06 by size)
  gives z +3.21 canonical.

## Controls

| control | result |
|---|---|
| K0 | cfg921.py exec'd read-only to its MAIN section, exactly as cfg928.py does: its 7 checks pass |
| K1 (A1) | **L23's committed isolated offsets reproduced** by this lane's own code: +0.3965 / +0.3573 (printed +0.3965 / +0.357). CFG31 C1 is reproduced exactly; CFG31 R1 is reproduced exactly through CFG31's own ν_mono kernel. The analytic-ν_e path is within 1.6e-9 / 1.9e-9 dex of it |
| K2 | **CFG928's sealed band reproduced from CFG928's code** (udg_* exec'd from cfg928.py's text): 18 rows equal the JSON (max rel diff 0); θ 6.9503 / 6.4575; band ends +0.022 / +0.140 and +0.016 / +0.105, as sealed |
| K3 | this lane's standalone P2 solver equals CFG928's path to 4e-16 (grid and all 15 universe galaxies, θ and θ±) |
| K4 | DF2/DF4 equal cfg657's GAL dict and CFG655's printed table; G, M☉ and pc equal L23's; membership equals criteria section 3 (11 admitted); no overlap with P2's calibration set |
| K5 | per galaxy, the sealed E_obs = ln 10 × L23's isolated offset (11 Coma UDGs, to 4e-15): the estimators coincide |
| MUTATE plus04 | **BEHAVES.** Planted +0.4 dex: P2 EXCLUDED on both footings (pool z +3.68 / +3.76; Coma +3.23 / +3.31) |
| MUTATE onlaw | **FAILS, as a power limit.** Planted on the law: NOT DIAGNOSTIC (z −0.27 / −0.20), because Coma's measurement-only 3 se_c (0.789 / 0.787) exceeds the power target (0.784 / 0.712). Per criteria section 8, CONSISTENT is unavailable to the main run; it would have read NOT DIAGNOSTIC, CONTROL-LIMITED. The main class is NOT DIAGNOSTIC on other grounds, and EXCLUDED is unaffected |

## Limitations

- **Small sample, large errors.** The sample is small (9 + 2), and the Coma σ errors are large: two galaxies have
  sE > 1.1 ln. The record's se convention takes the larger of the scatter and measurement terms. This is deliberately
  conservative, and it is the reason the inverse-variance reading (z +5.8 / +5.4) and the frozen reading (+2.6 / +2.4)
  disagree.
- **M* is not the seal's literal convention.** M* is the source's SSP mass, not 2 L_V; Υ = 2 on R/I-band light (R3) would
  lower the excess. The S-set brackets this at ±0.2 dex only.
- **The aperture correction is unmeasured here.** It is carried as L23's ±15% coherent factor.
- **DF2/DF4 are admitted by the seal's wording but come from another formation channel** (the record's class E). They
  dominate the pooled scatter and the H rule.
- **The power rule's margin is thin.** It uses the dwarf class mean F0 as the alternative to be excluded, and on the canonical
  footing it fails by 0.005.
- **No new data were downloaded.** Everything is the record's: the Freundlich+2022 table as used by L23 and CFG31, and
  CFG655's DF2/DF4 table.

## Reproduce

One core, under 0.4 GB, a few seconds each; nothing downloaded. Run order: K, MUTATE onlaw, MUTATE plus04, main.
- `CFG933_MODE=K OMP_NUM_THREADS=1 nice -n 10 python3 cfg933.py` → `cfg933_K.out`, `cfg933_results_K.json` (exit 0)
- `CFG933_MODE=onlaw ...` → `cfg933_MUTATE_onlaw.out`, `cfg933_results_MUTATE_onlaw.json` (exit 1: required class not
  reached)
- `CFG933_MODE=plus04 ...` → `cfg933_MUTATE_plus04.out`, `cfg933_results_MUTATE_plus04.json` (exit 0: behaves)
- `OMP_NUM_THREADS=1 nice -n 10 python3 cfg933.py` → `cfg933.out`, `cfg933_results.json` (exit 0). It reads the two MUTATE
  JSONs for the CONTROL-LIMITED rule.

No other lane's files were edited. Several files are only read or exec'd read-only:
- cfg921.py and cfg928.py;
- cfg928_results.json;
- L23_udg_verify.py / .out;
- CFG31's JSON;
- cfg657_capture.py;
- FP1_static_sector.py (the ν_mono slice, for K1).
