# AT2_a0z_on_disk_samples: every on-disk high-z sample is BLOCKED under AT1's rule; no sample on disk can decide a₀ tracking ρ_DE vs a₀ ∝ H(z)

**Verdict: 22 in-domain samples, 52 (sample, z*) cells, 52 BLOCKED. No DECIDES-law, no DECIDES-rival, no NEITHER, no
INCONCLUSIVE. No a₀ ratio was formed anywhere.** The binding failures are the same in every cell: no same-estimator z < 0.1
reference exists on disk, and every sample's common mode (0.30-0.60 dex) is 4-11x above the largest e_3σ (0.084 dex).

Criteria `FROZEN_CRITERIA.md` (e453a3ad83), committed alone first. Script `at2.py`; outputs `at2.out`, `at2.json`,
`at2_MUTATE.out`, `at2_MUTATE.json`. Stdlib only, one process, about 2 s, peak RSS about 25 MB. No download.
**Not blind** (every sample was read by earlier lanes). κ = ½ FITTED. Footings never pooled. Not theory closed. Nothing here
says the data favour the framework. The cold sector stays retired.

## What was done

AT1's rule (`../AT1_a0z_tracking_decision/`, 4c5c84576a) unchanged: ȳ = log10(a₀(z*)/a₀,ref) against a same-estimator
z < 0.1 reference, gates G1-G4 before ȳ, outcomes from CFG689's primary quantiles (BAO + SN, curvature free; no ΛCDM input,
no Planck 5.364). This lane fixed only what AT1 left open, before any count: z* bins (1.0: 0.90-1.10; 1.2: 1.10-1.35;
1.5: 1.35-1.915; 2.33: 1.915-2.75), the reference-match rule R1-R5, and each sample's common mode c. AT1 has no pooling rule,
so nothing is pooled.

## Per-sample table (`at2.out`)

c_primary is CFG685's `e_est` lower edge for the sample or its class (with no same-estimator reference none of it cancels).
e_3σ is 0.055 / 0.072 / 0.074 / 0.084 dex at z* 1.0 / 1.2 / 1.5 / 2.33.

| # | sample | z (file) | N in bins 1.0 / 1.2 / 1.5 / 2.33 | gas (G2) | c_primary (c_optimistic) | reference | label |
|---|---|---|---|---|---|---|---|
| 1 | KURVS-CDFS rotation-supported | 1.33-1.61 | - / 1 / 9 / - | none | 0.45 | SPARC anchor: fails R2-R5 | BLOCKED |
| 2 | Genzel+2017 deep curves | 0.85-2.38 | - / - / 2 / 3 | scaling | 0.45 | none | BLOCKED |
| 3 | RC41 (Price+2021) | 0.66-2.45 | 5 / 3 / 7 / 17 | scaling | 0.45 | none | BLOCKED |
| 4 | KMOS3D TF (Übler+2017) | 0.60-2.53 | 34 / 1 / 23 / 46 | scaling | 0.45 | none | BLOCKED |
| 5 | KMOS3D raw-cube fits | 2.00-2.68 | - / - / - / 192 | none | 0.50 | none | BLOCKED |
| 6 | SINS/zC-SINF AO | 1.45-2.52 | - / - / 3 / 35 | none | 0.50 | none | BLOCKED |
| 7 | SINS 2009 | 1.36-2.58 | - / - / 14 / 33 | SFR inversion | 0.45 | none | BLOCKED |
| 8 | RC100 (CORRECTED) | 0.61-2.52 | 13 / 4 / 24 / 41 | mixed | 0.40 (0.10, CFG218) | none | BLOCKED |
| 9 | MSA-3D | 0.58-1.68 | 7 / 9 / 7 / - | scaling | 0.60 | none | BLOCKED |
| 10 | NOEMA3D | 1.12-1.63 | - / 6 / 4 / - | **CO (+dust)** | 0.40 (**0.043**, CFG218) | Girard DYNAMO: fails R5, R2 | BLOCKED |
| 11 | ALPAKA I | 0.56-3.63 | - / - / 7 / 5 | CO/[CI] | 0.50 | none | BLOCKED |
| 12 | ALPAKA-JWST | 0.56-2.10 | - / - / 1 / 1 | CO/[CI] | 0.50 | none | BLOCKED |
| 13 | Lelli+2023 | 1.47-2.24 | - / - / 1 / 1 | CO | 0.50 | none | BLOCKED |
| 14 | Amvrosiadis+2025 | 1.36-4.45 | - / - / 3 / 6 | CO | 0.50 | none | BLOCKED |
| 15 | PHIBSS (Tacconi+2013) | 1.00-2.43 | 10 / 18 / 10 / 15 | CO | 0.50 | none | BLOCKED |
| 16 | Girard+2021 compilation | 1.04-2.32 | 2 / 3 / 4 / 1 | mixed | 0.50 | DYNAMO: fails R5, R2 | BLOCKED |
| 17 | KROSS (Harrison+17; Tiley+19) | 0.58-1.04 | 177 / - / - / - | none | 0.45 | Tiley SAMI_matched: fails R3 | BLOCKED |
| 18 | KROSS GS21b (Sharma+2024) | 0.76-1.04 | 77 / - / - / - | scaling | 0.45 | none | BLOCKED |
| 19 | Mancera Piña+2026 | 0.79-1.03 | 18 / - / - / - | none | 0.45 | none | BLOCKED |
| 20 | ZFIRE 2018 | 2.06-2.44 | - / - / - / 44 | none | 0.45 | none | BLOCKED |
| 21 | SIGMA (Simons+2016) | 1.31-2.44 | - / 5 / 23 / 21 | none | 0.45 | none | BLOCKED |
| 22 | MUSE-DARK | 0.28-1.44 | 36 / 18 / 10 / - | modelled | 0.30 | none | BLOCKED |

Every cell also fails G4 (the record places each sample's radius in the Newtonian or g_bar/a₀ ≈ 1-4 regime, or does not show
it). G3 (median v/σ ≥ 6) passes in 13 cells (KMOS3D z* 1.0 / 1.2, SINS-AO z* 1.5, RC100 z* 1.0 / 1.2, NOEMA3D both,
ALPAKA I both, Amvrosiadis z* 2.33, Girard three); the cells and medians are in `at2.out`.

- **Only one sample has a same-estimator low-z partner on disk:** KROSS with Tiley+2019's resolution-matched SAMI (186 rows).
  It fails R3: neither side has gas, so no a₀ estimator can be formed on either side.
- **Nearest to passing: NOEMA3D.** It has measured CO gas (G2 pass) and v/σ 8-9 (G3 pass), and CFG218's route-bias systematic
  (0.043 dex) would open G1. But that number is a bias estimate, not the full common mode (CFG685: 0.40). Its radius is R_e,
  at g_bar/a₀ ≈ 1-4 (G4 fail), and there is no z < 0.1 CO reference reduced the same way. N is 6 + 4.
- **N is not the problem.** With the common mode set to zero (K2c), every cell with N ≥ 7 at z* 1.0 or N ≥ 4 at z* 1.2-2.33 would recover both planted laws (law
  0.96-1.00, rival 0.78-0.98). The common mode and the missing reference are what block.
- **Not graded:** 5 single discs (CFG970 Refsdal host, Übler+2018, GS4_24110, U4_27928 / U4_28473, Big Wheel); AT1 does not
  apply to one disc (CFG806 / CFG809). There are also 8 samples with no galaxy in any z* bin: CRISTAL, Roman-Oliveira+23,
  Danhaive+25, ALPINE ×2, MIGHTEE-HI z > 0.25, BUDHIES, PHIBSS2.

## The record's earlier lean to the rival: neither confirmed nor changed

The record leaned to the rival on KURVS: CFG160 / CFG189, under Kretschmer+2021's pressure calibration. Its governing
wording is "a weak, normalisation-dependent lean; not a detection". It flips with gas (CFG164 / CFG166) and with the
pressure strength (CFG162).

Under AT1's frozen rule, KURVS is BLOCKED five ways:
- no same-estimator z < 0.1 reference (SPARC is a different tracer, gas route and pressure recipe);
- G1: c 0.45 against e_3σ 0.074;
- G2: no gas;
- G3: median v/σ 1.8;
- G4: g_bar/a₀ reaches 0.67.

**So the lean was never a decision this rule could make, and AT2 neither confirms nor changes it.** The same holds for the
record's opposite within-sample reading, RC100's W-flat (CFG216), which is a slope within one sample, not AT1's ratio to a
z < 0.1 reference. RC100 is BLOCKED: c 0.40 (0.10 optimistic) > 0.084, no reference, G2 and G4 fail.

## Checks (`at2.out`: 13/13 pass; `at2_MUTATE.out`: bites, exit 1)

- **K1 known answer:** gap, σ_E, σ_X and e_3σ equal `at1.json` to 1e-12 and CFG689 within 0.001 dex. The values are 0.0546 /
  0.0724 / 0.0744 / 0.0843.
- **K2a planted recovery, powered control** (N 1000, c 0): law and rival recovered 0.999-1.000 in every bin.
- **K2b:** at every cell's own N and c_primary the gate blocks 100 % of planted draws. G0: no ȳ is formed in any cell.
- **K3 MUTATE** (law and rival labels swapped): K2a falls to 0.000 in every bin and the script exits 1. K5 also fails under the
  swap, as a consequence of it. The gate labels are unchanged (52 BLOCKED), as expected, because the gates do not depend on
  the labels.
- **K4 byte-identical rerun:** sha256 of `.out` and `.json` are identical. The check is printed in `at2.out`.
- **K5 scrambled z:** rival recovery falls 1.00 → 0.00 in every bin, and overall recovery falls 1.00 → 0.50. Law mocks do not
  drop, as stated before the run: √X₅₀ is nearly flat (0.91-0.94).
- **K6 footings** (canonical 9.3603e-11, alt 1.1312e-10, used only here): ȳ differs by 0.0 and the labels are identical. Both
  footings are reported; they cancel exactly. The footing values are never passed to the grader.
- **K7:** RC100 is read only from the `_CORRECTED` file, and the script has no Planck or ΛCDM literal. **K8:** the domain
  counts.
- **Disclosed:**
  - The first two invocations crashed before writing any output: a wrong KROSS column name, and a scrambled-z code bug.
    Both were fixed, and nothing graded had been computed.
  - The v/σ columns used for G3 were chosen at run time; the criteria named G3's threshold but not the columns. The KROSS
    v/σ uses `vc_kms_intrinsic_at_2Rhalf / sigma0_kms`.

## What would decide it (none is on disk; nothing fetched; the owner approves downloads)

AT1 needs both halves, observed and reduced the same way:
1. **A z* sample with a common mode below 0.055-0.084 dex.** The spec is CFG685's proposal target:
   - z 1.0-1.6 discs, log M* 9.8-10.5;
   - CO(2-1)/(3-2) kinematics at 0.2-0.3″ with v/σ ≥ 6;
   - gas from three tracers (CO, [CI], dust);
   - JWST NIRCam + MIRI resolved M/L;
   - outskirts at g_bar ≤ 0.5 a₀;
   - N ≈ 25-50, about 500-1,500 ALMA hours.

   **No public sample meets this.** The 2026-11-06 ALMA release (U4_28473) and GS4_24110 (public 2026-11-28) are single discs
   and cannot decide under AT1.
2. **A z < 0.1 reference with the same tracer, radius definition, gas route and M/L recipe.** These are named from memory;
   sizes are provisional and not checked:
   - CO rotation curves with measured gas at z < 0.1: PHANGS-ALMA (~90 nearby discs) or EDGE-CALIFA (~100+);
   - for an Hα route, SAMI DR3 or MaNGA gas kinematics. Only SAMI's stellar-kinematics table is on disk. An Hα route still
     fails G2 at high z unless every disc gets a direct gas tracer.

Until both exist, the a₀(z) fork stays open. Galaxies on disk cannot close it under the frozen rule. κ = ½ FITTED; not theory
closed.
