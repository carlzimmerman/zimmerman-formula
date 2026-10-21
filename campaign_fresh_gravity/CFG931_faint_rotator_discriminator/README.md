# CFG931: do faint rotators carry the dwarf excess? Energy picture (E) vs kinematic picture (K) at matched g_bar

**Bottom line.**
- **CLASS: NOT DIAGNOSTIC (DATA)**, both footings. The primary split M* = 1e7 has **zero** rotators to test: no SPARC
  rotator with M* < 1e7 passes the quality cuts and reaches g_bar < 10^−11.5.
- **Extended splits (secondary, labelled E′):** 3e7 → NOT DIAGNOSTIC (DATA) (only 3 faint rotators); 1e8 → NOT DIAGNOSTIC
  (NO LEVER) (the matched-M* dSphs stand only +0.17 ± 0.09 dex above bright rotators in the overlap cell, z 1.85 < 2).
- **No variant changes a class** (sub-labels only), so nothing is FRAGILE.
- **What the point estimates show (no class weight):** where faint rotators exist they sit close to the law, about where
  bright rotators sit, while dSphs of matched M* sit higher. At 1e8: E(i) +0.02, E(ii) +0.00, E(iii) +0.17 dex
  (canonical). At 3e7: d_E = +0.26 ± 0.11 (z 2.3) with only 3 galaxies. That is the K pattern, but it does not reach a
  frozen bar. It is not a K-FAVOURED result.
- **Power was the binding limit, as stated in advance.** In the only SPARC overlap cell, [10^−12, 10^−11.5), the dSph lever
  (≈ 0.17 dex) is below the realised minimum detectable differences (MDD_K 0.32, MDD_E 0.33 dex). The dSph excess that
  matters (+0.3 to +0.7 dex) lives below 10^−12, where SPARC has 3 rotators and no faint ones.
- **Inventory correction (AMENDMENT A2, post hoc).** LITTLE THINGS curves are on disk (Oh+2015, Iorio+2017; CFG442/CFG449
  data). They add at most 4 rotators with M* < 1e7 at g_bar < 10^−11.5, below the frozen N ≥ 5, and they cannot be pooled
  with SPARC (CFG442/449 overlap offsets). The lane class is unchanged. A labelled INFO look at them is below.

κ = ½ is FITTED. Footings 9.3603e-11 / 1.1312e-10 m/s² are never pooled. Raw data and framework-native quantities only. Cold
energy, not a particle. Not "theory closed". Nothing here says the data favour the framework.

- **Kind:** DATA DISCRIMINATOR (pre-registered). Block 930–939.
- **Criteria:** `FROZEN_CRITERIA.md`, cad92ca1c, committed alone before any script or residual.
- **Amendments:**
  - `AMENDMENT_A1.md`, 165bb5c71: post-freeze, before any run. The I-30 recovery needs the lever gate too; implementation
    details; one UGCA 444 INFO line.
  - `AMENDMENT_A2.md`, f2fe987af: POST HOC, after the main run and before any LITTLE THINGS residual. The inventory correction
    and the LITTLE THINGS INFO analysis.
- **Not blind:** CFG919's V0 cells (SPARC Mb ≤ 3e9 near the law at [−12, −11.5), dwarfs +0.175 dex) were seen before
  freezing, along with an outcome-blind inventory count. Disclosed in criteria section 9. The expected outcome was written
  down there: "primary NOT DIAGNOSTIC (DATA); extended splits NOT DIAGNOSTIC". That is what happened.

## The test

- **Groups:**
  - (i) SPARC rotators with M* < split, M* = 0.5 L[3.6];
  - (ii) SPARC rotators with M* ≥ split;
  - (iii) CFG880's 83 LVD dSphs with M* < split (Υ_V = 2, gas inside r½ counted).
- **SPARC cuts:** Q ≤ 2, Inc ≥ 30°, errV/V < 0.10.
- **Residual:** Δ = log10(g_obs/g_law), kernel ν_e. Gas counted in g_bar everywhere.
- **Window:** W = [10^−12.5, 10^−11.5), the two CFG914/919 0.5-dex cells. Cells are weighted by group (i)'s counts.
  Eligible cells hold all three groups (≥ 1 / ≥ 3 / ≥ 3).
- **Differences:** d_K = E(i) − E(ii) (K predicts 0); d_E = E(iii) − E(i) (E predicts 0); lever = E(iii) − E(ii).
- **Errors:** system bootstraps (4000) plus a 0.05 dex floor per group mean.
- **Classes:**
  - data gate: N_i ≥ 5, N_ii ≥ 5, N_iii ≥ 3;
  - lever gate: z(lever) ≥ 2;
  - **E-FAVOURED:** z(d_K) ≥ 2 and z(d_E) < 2;
  - **K-FAVOURED:** z(d_E) ≥ 2 and z(d_K) < 2;
  - otherwise NOT DIAGNOSTIC.
- **Split:** M* = 1e7 is primary. 3e7 and 1e8 are labelled E′: a K result there would not exclude E at its declared
  ≲ 1e6–1e7 threshold.
- **E_SN/E_bind: NOT COMPUTED.** CFG930's declared form was not on disk at freeze. The M* split stands in (E_SN ∝ M* at a
  fixed IMF).

## Data inventory (on disk; nothing downloaded)

| source | rotators | M* < 1e7 | M* < 1e7 and g_bar < 10^−11.5 | used |
|---|---|---|---|---|
| **SPARC** (Lelli+16), after cuts | 147 (2696 pts) | 1 (UGC 4483, 6.5e6; floor 10^−11.32) | **0** | graded |
| SPARC UGCA 444 (= WLM), 6.0e6 | all 36 points fail errV/V < 0.10 | — | reaches 10^−12.33 without the cut | INFO (A1-3) |
| SPARC M* < 3e7 / < 1e8 | 4 / 15 | | 3 (D564-8, DDO 154, NGC 3741) / 8 (+ CamB, D631-7, NGC 3109, UGC 5764, UGCA 442) | E′ splits |
| **LITTLE THINGS Oh+2015** (CFG442/data; VizieR J/AJ/149/180) | 26 AD-corrected curves; 20 with M*_SED | 5 (DDO 210, CVn I dwA, UGC 8508, DDO 154, DDO 53) | 4 at R_max (single point) | INFO (A2) |
| **LITTLE THINGS Iorio+2017** (CFG449/data, 28.6 kB zip) | 17 curves + Σ_HI, no mass models | the same 5 | — (needs mass models) | not used |
| Hunter+2012 LITTLE THINGS table (CFG442/data) | 41 galaxies, no curves | | | — |
| Lelli+15 tidal dwarfs (`real_research/data/tdg`) | 6 single points | 0 (M* 3e7–1.1e8) | | INFO |
| UNGC (Karachentsev+13) | W50, i, vAmp; no radius on disk | | no g_bar | — |
| ALFALFA a100 / Durbala+20 / Leisman+17 HUDs, FASHI DR2, MIGHTEE-HI | unresolved widths | | no resolved radius | — |
| LVD local-field dIrrs | no rotation column; WLM, NGC 6822, IC 1613, Leo A, Sag dIrr, Pegasus dIrr carry no rotation data | | | — |

- Matched-M* dSphs per cell, for M* < 1e7 / < 1e8: 15 / 17 in [−12.5, −12); 8 / 10 in [−12, −11.5).
- **M\* conventions disagree right at the split.** DDO 154 is 2.6e7 in SPARC (0.5 L[3.6]) but 8.3e6 by Oh+2015 SED. WLM is
  6.0e6 in SPARC but 1.6e7 by SED.

## Main result (V0; dex)

| split | footing | N i/ii/iii | E(i) | E(ii) | E(iii) | d_K | d_E | lever (z) | MDD_K / MDD_E | class |
|---|---|---|---|---|---|---|---|---|---|---|
| **1e7** | both | 0 / – / – | — | — | — | — | — | — | — | **NOT DIAGNOSTIC (DATA)** |
| 3e7 | canonical | 3 / 28 / 9 | −0.052 | +0.014 | +0.204 | −0.066 ± 0.108 | +0.256 ± 0.110 (z 2.3) | +0.190 ± 0.092 (2.1) | 0.31 / 0.31 | NOT DIAGNOSTIC (DATA) |
| 3e7 | alt | 3 / 28 / 9 | −0.091 | −0.024 | +0.165 | −0.066 ± 0.108 | +0.256 ± 0.110 | +0.190 ± 0.092 (2.1) | 0.31 / 0.31 | NOT DIAGNOSTIC (DATA) |
| 1e8 | canonical | 8 / 23 / 10 | +0.022 | +0.002 | +0.175 | +0.020 ± 0.114 | +0.153 ± 0.118 (z 1.3) | +0.173 ± 0.093 (1.85) | 0.32 / 0.33 | NOT DIAGNOSTIC (NO LEVER) |
| 1e8 | alt | 8 / 23 / 10 | −0.016 | −0.036 | +0.136 | +0.020 ± 0.114 | +0.153 ± 0.118 | +0.172 ± 0.093 (1.85) | 0.32 / 0.33 | NOT DIAGNOSTIC (NO LEVER) |

- At 1e8 only the cell [−12, −11.5) is eligible; [−12.5, −12) has 3 faint rotators but no bright one.
- Group (i) at 1e8, window-mean Δ (canonical): NGC 3741 +0.09, D564-8 −0.18, DDO 154 −0.01, CamB −0.39, UGC 5764 +0.45,
  UGCA 442 +0.08, NGC 3109 +0.01, D631-7 +0.06.
- **Variants** (V1 floor 0; V2 floor 0.10; V3 rotator pressure bracket +2·(8 km/s)²; V4 CFG828 dwarfs; V5 window to
  10^−11.0; V6 pairwise cells; V7 M*-matched dSphs): no class changes.
  - At 1e8, V1, V4 and V6 pass the lever gate (z 2.3–2.8) but neither difference reaches z 2: UNRESOLVED.
  - V3, which pushes toward E, gives d_K +0.066 ± 0.111.
  - V7 has no eligible cell.
- **Advance vs realised power:** the predicted σ(d_K) was 0.086; the realised value is 0.114, because the faint-rotator
  scatter is larger than assumed (CamB −0.39, UGC 5764 +0.45).

## Controls

| control | result |
|---|---|
| K1 CFG828 | reproduced exactly (max diff 0): N_in 8, D +0.051 ± 0.073 dex, out-of-range +0.438, SPARC median +0.031 |
| K2 CFG919 SPARC | SS +0.137 ± 0.084, SL +0.002 ± 0.050 (ln), W2 ρ −0.172, p 0.038, both footings, max diff 0 |
| K3 CFG919 DW | +0.856 ± 0.102 ln (+0.372 dex) canonical, +0.765 alt, max diff 0 (CFG880 slice exec'd read-only) |
| K4 inventory | 2696 points / 147 galaxies; lowest-M* Table 1 galaxy UGCA 444 at 6.0e6 |
| MUTATE I-30 pipeline | d_K moves by exactly +0.300000000000 at every split with an eligible cell; σ and lever unchanged: PASS |
| MUTATE I-30 recovery | **required nowhere** (A1-1): 1e7 has no cell, 3e7 fails the data gate, 1e8 fails the lever gate (z 1.85) and the power clause (MDD_K 0.32 > 0.30). For the record, at 1e8 the injected +0.30 shows as d_K = +0.32 ± 0.11 (z 2.8) |
| MUTATE I-E (E world) | at 1e8, E(i) set equal to E(iii) gives d_K +0.17 ± 0.11 (z 1.5): **the E picture's own prediction is not detectable on SPARC at this g_bar** |
| MUTATE shuffle S1 | on the I-30 data, 1000 label shuffles at 1e8: median d_K +0.001 vs +0.320 true; E-FAVOURED 0 % (trivially, because the lever gate blocks every shuffle): BITES |
| S2 (real data) | permutation p of d_K at 1e8: 0.40 one-sided, 0.80 two-sided (no class weight) |

## INFO lines (no class weight)

- **UGCA 444 (= WLM), M\* 6.0e6, no point cut (A1-3):**
  - [−12.5, −12): Δ +0.20 (3 points), against bright rotators −0.05 (3) and dSphs +0.32 (15);
  - [−12, −11.5): −0.02 (7 points), against +0.01 (31) and +0.22 (8).
  - One galaxy, errors ≥ 10 % per point.
- **LITTLE THINGS single point at R_max (A2, `cfg931_lt_info.out`):**
  - Faint rotators (M*_SED < 1e7) in W: CVn I dwA −0.09, DDO 154 +0.01 and UGC 8508 +0.61 in [−12.5, −12); DDO 210 −0.08 in
    [−12, −11.5). DDO 53 (−0.14) lies above W. Three of four sit on the law. UGC 8508 sits high; it has a fallback distance
    and is the galaxy that hit the upper bound in CFG442.
  - Within LITTLE THINGS at split 1e7: d_K +0.11 ± 0.20, d_E +0.18 ± 0.18, lever +0.29 ± 0.13 (z 2.2), N 4/11/23.
  - At 3e7: d_K −0.04 ± 0.17, d_E +0.25 ± 0.13 (z 1.9), N 10/5/25.
  - At 1e8 the bright LITTLE THINGS group has one galaxy in the cell (DDO 50, −0.55), so that row is uninformative.
  - **Overlap with SPARC in this statistic:** LITTLE THINGS sits +0.05 to +0.20 dex higher (DDO 154 +0.01 vs −0.04, DDO 168
    +0.22 vs +0.02, WLM +0.08 vs +0.04). This matches the record's CFG442/449 offset, and is why the two are never pooled.
- **Lelli+15 tidal dwarfs** (M* 3e7–1.1e8, log g_bar −11.7 to −11.0): Δ = −0.69 dex mean (−0.40 to −0.89).
  - The bare isolated law over-predicts all six. Their hosts' external fields are comparable to their internal fields
    (Lelli+15 Table 5), so this is not a test of the law here. See CFG441/448 for the record's treatment.
  - Relevant here only because no M* ≲ 1e8 tidal rotator shows an excess.

## What would decide it (for the owner's download decision; nothing downloaded)

**The decisive regime is g_bar < 10^−12.** There the matched-M* dSphs sit +0.26 to +0.32 dex above the law (cell
[−12.5, −12): +0.318 canonical for M* < 1e7). At [−12, −11.5) the lever is only about 0.17–0.21 dex.

**Need, from the realised scatters:**
- about 10–15 rotators with M* < 1e7, resolved rotation curves (asymmetric-drift corrected) and per-radius mass models,
  reaching g_bar < 10^−12;
- at least 5 brighter rotators in the same cell, from the same reduction, as the control. SPARC has only 3 rotators there.
- One homogeneous reduction, so that the per-group floor can stay at about 0.05 dex.

Even then the dSph side caps σ(d_E) near 0.10 (15 dwarfs, scatter about 0.3 dex), so MDD_E ≈ 0.3 dex, which is about the
lever. The test would be marginal unless the faint-rotator sample is large.

| data set | on disk? | size (source of the number) | what it adds |
|---|---|---|---|
| Iorio+2017 LITTLE THINGS curves | **yes** (CFG449/data, 28,572 B zip) | 17 galaxies (on-disk listing) | the 5 M* < 1e7 galaxies above, resolved. Needs mass models (gas ring integrator + stellar disc). CFG449's integrator failed K0b only inside 0.75 R_d. **Still ≤ 4–5 faint rotators: cannot pass N ≥ 5 in W by itself** |
| Oh+2015 LITTLE THINGS | **yes** (CFG442/data) | 26 curves (VizieR ReadMe) | per-radius baryons exist only as figure paths (CFG442 digitisation, `_external_data/cfg442`, git-ignored) |
| BIG-SPARC | no (not released as of 2026-10-07, CFG449 README) | ~4000 homogeneous HI curves + mass models (CFG449 README) | the natural homogeneous sample with both faint and bright rotators at g_bar < 10^−12, if it reaches M* < 1e7 |
| SHIELD (Cannon+2011; McNichols+2016) | no | ~12 galaxies, M_HI ~10^6.5–10^7.5 (recall; not in on-disk notes; verify) | faint gas-rich rotators, M* ~1e6–1e7 |
| FIGGS (Begum+2008) | no | 65 faint dIrrs (recall; verify); curves for a subset | the largest faint-dIrr HI sample |
| VLA-ANGST (Ott+2012) | no | 35 galaxies (recall; verify) | nearby dwarfs with HI kinematics |
| Leo P (Giovanelli+2013; Bernstein-Cooper+2014) | no | 1 galaxy | M* ~ 5e5 with HI rotation; one object |

Table sizes for the "no" rows are not in on-disk notes. Rotation-curve tables are usually kB to MB; HI cubes are much larger.

## Limitations

- **M\* conventions differ:** 3.6 μm Υ 0.5 for SPARC, V-band Υ 2 for the dSphs. Faint rotators can cross the split on
  convention alone (DDO 154, WLM).
- **Pressure support in faint rotators.** SPARC curves are taken as given. V3 brackets an unmodelled asymmetric-drift term
  and changes no class.
- **Lever source.** The dSph lever comes from Wolf-estimator dispersions with gas inside r½. The CFG828 Υ_SFH sample (V4)
  gives a larger lever (+0.24) but the same class.
- **E′ splits** test an energy threshold above the E picture's declared range.

## Reproduce

All runs use one core and < 0.15 GB, take seconds, and download nothing:
- `CFG931_KONLY=1 OMP_NUM_THREADS=1 nice -n 10 python3 cfg931.py` → `cfg931_K.out`, `cfg931_results_K.json`
- `CFG931_MUTATE=inject ...` → `cfg931_MUTATE_inject.out`, `cfg931_results_MUTATE_inject.json` (exit 0)
- `CFG931_MUTATE=shuffle ...` → `cfg931_MUTATE_shuffle.out`, `cfg931_results_MUTATE_shuffle.json` (exit 0)
- `OMP_NUM_THREADS=1 nice -n 10 python3 cfg931.py` → `cfg931.out`, `cfg931_results.json` (exit 0)
- `OMP_NUM_THREADS=1 nice -n 10 python3 cfg931_lt_info.py` → `cfg931_lt_info.out`, `cfg931_lt_info.json` (POST-HOC INFO, A2)

No other lane's files were edited. CFG880's input slice was exec'd read-only with writes refused. The CFG828, CFG919, CFG824,
CFG827, CFG442 and CFG449 files were only read. CFG930's directory was not touched.
