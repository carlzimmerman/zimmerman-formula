# CFG516: the round enclosed-mass rule for cold energy (RM). ROBUST as frozen, with three limits stated plainly

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (b35642ca6).
- **Scripts:**
  - `cfg516_mw.py` (Part 1, Milky Way K_z). Outputs `cfg516_mw.out` and `cfg516_mw_results.json`. The MUTATE is `CFG516_MUTATE=1`; outputs `cfg516_mw_MUTATE.out` / `_MUTATE.json`; exit 1 = DETECTED.
  - `cfg516_sparc.py` (Parts 2–3: SPARC and the edge-on predictions). Outputs `cfg516_sparc.out` / `.json`. Post-run variant V2 is `CFG516_INNER=exp` (`_INNEREXP`).
  - `cfg516_figure.py` → `cfg516_round_rule.png`.
  - Each run takes under 30 s.
- **Re-used, not edited:** CFG514's solver, McMillan17 baryons and data loaders. They are executed from its committed file.
- **Settings:**
  - κ = ½ is FITTED. Both footings are used: 9.36e-11 / 1.13e-10.
  - The kernel is ν_mono.
  - Only data already on disk were used. Nothing was downloaded.
  - The cold energy's MASS is still required. This is not "theory closed".

## The rule

**RM:** the cold energy is spherical, with M_cold(<r) = M_law(<r) − M_b(<r), where M_b(<r) is the 3-D sphere-enclosed baryon mass. "The law's enclosed mass" is ambiguous for a disc, so the rule was run in two definitions:
- **RM-φ:** the QUMOND phantom's own enclosed mass, i.e. its shell average. This is CFG514's MUTATE.
- **RM-v:** M_law(<r) = r v_law²/G, where v_law is the algebraic law applied to the in-plane Newtonian field.

The comparator is **PD**, the full QUMOND field (the phantom disc), computed on the same baryons.

## Bottom line

1. **Round beats disc on the MW K_z data in every cell: 32 of 32.**
   - The cells cover 4 baryon models × 2 footings × F0/FA × 2 definitions. Δχ²(RM − PD) runs from −64 to −450.
   - The MUTATE puts RM's enclosed mass into a q = 0.3 homeoid. It brings the rejection back in all 32 cells (Δχ² +185 to +1490). So the vertical-force verdict is set by the shape, not the mass.
   - CFG514's result is therefore not specific to one baryon model.
2. **SPARC: RM fits as well as full QUMOND under both definitions.** RM's rms is within 0.02 dex of PD's at both footings and with a₀ free; in fact it is better or equal in five of six clauses.
   - **RM-φ** gives in-plane accelerations within 0.5% of PD's (median). A round phantom and a disc phantom with the same M(<r) pull almost identically in the plane.
   - **RM-v moves κ by −0.078 dex against PD.** This crosses the frozen 0.05 dex "κ moves" flag (−0.047 dex against the algebraic law).
3. **Verdict as frozen: ROUND RULE ROBUST.** Both definitions are ROBUST.
4. **The win, checked as hard as a fail would be. Three limits:**
   - **(i) Beating PD is not the same as fitting K_z.** RM comes within +4 of the NFW's χ² in only 6/16 cells (RM-φ) and 9/16 cells (RM-v).
     - The K_z scale length stays long: h = 3.5 kpc against the data's 2.72 ± 0.15 for McMillan17 and the L172 baryons. That is the same miss as the NFW's, and it comes from the baryon model.
     - The short disc (R_d 2.15) brings h down to 3.05.
   - **(ii) RM-φ needs heavier baryons to fit the rotation curve.**
     - At A = 1 it runs as low as PD (χ²_RC 426 against Eilers on McMillan17, canonical).
     - Fitted to the RC, it needs A = 1.15–1.35 on McMillan17/L172. Those extra baryons push K_z back up: +28 to +112 above the NFW in those FA cells.
     - RM-v's in-plane speed is about 9% higher in g, so it fits the RC with A ≈ 1.0–1.15. It is the more comfortable definition on the MW (FA cells +1 to +28 vs NFW on B1/B2; −19 to −40 on B2b/B3).
   - **(iii) Full QUMOND itself fits SPARC worse than the algebraic RAR.** At fixed a₀, PD's rms is +0.006–0.008 dex above ALG's, and with a₀ free PD prefers a₀ +0.031 dex higher.
     - The reason is physical, not numerical. Control S5 (a near-Kuzmin disc) shows QUMOND's in-plane force sits 20% → 0.3% below the radial-only algebraic law from R = 1 to 30 kpc. The ν of a thin disc sees the vertical field 2πGΣ.
     - This matters for any κ quoted from a "law" (CFG493's point). The law definition moves the fitted κ: ALG 1.34e-10, PD 1.44e-10, RM-φ 1.52e-10, RM-v 1.20e-10.
     - The absolute a₀ of this statistic (CFG476's weighted rms, Υ 0.5) is high for every model. It matches CFG476's data value of 1.37e-10 and is NOT a calibrated κ. Only the shifts between models are the result.

## MW robustness table

Δχ² on Bovy & Rix's 43 K_z,1.1 MAPs (σ ⊕ 5%). Values are RM − PD, with RM − NFW in brackets.

| baryons | foot | var | PD − N | RM-φ − PD (− N) | RM-v − PD (− N) | homeoid − RM-φ / RM-v |
|---|---|---|---|---|---|---|
| B1 McMillan17 (6.64e10) | can | F0 | +101 | −98 (+3.0) | −101 (+0.1) | +267 / +679 |
| | can | FA | +381 | −309 (+71) | −368 (+13) | +713 / +891 |
| | alt | F0 | +167 | −166 (+0.6) | −164 (+2.1) | +390 / +888 |
| | alt | FA | +335 | −307 (+28) | −334 (+1.1) | +713 / +853 |
| B2 L172 6.0e10 | can | F0 | +80 | −64 (+16) | −76 (+3.9) | +185 / +558 |
| | can | FA | +477 | −365 (+112) | −450 (+28) | +791 / +996 |
| | alt | F0 | +137 | −127 (+11) | −135 (+2.3) | +292 / +747 |
| | alt | FA | +425 | −370 (+54) | −418 (+6.8) | +796 / +957 |
| B2b L172 7.3e10 | can | F0 | +268 | −288 (−20) | −249 (+18) | +554 / +1194 |
| | can | FA | +431 | −365 (+66) | −450 (−19) | +790 / +996 |
| | alt | F0 | +389 | −399 (−10) | −354 (+35) | +728 / +1476 |
| | alt | FA | +378 | −370 (+7.5) | −417 (−39) | +794 / +957 |
| B3 short disc 2.15 (8.07e10) | can | F0 | +207 | −201 (+6.0) | −154 (+53) | +613 / +1194 |
| | can | FA | +146 | −153 (−7.2) | −170 (−24) | +553 / +668 |
| | alt | F0 | +301 | −283 (+18) | −228 (+73) | +810 / +1493 |
| | alt | FA | +119 | −141 (−22) | −139 (−20) | +550 / +643 |

More detail:
- **K_z(R₀, 1.1) on B1 F0** (canonical / alt), against the measured 66.4 ± 2.2:
  - PD 90.0 / 94.8;
  - RM-φ 70.3 / 71.6;
  - RM-v 74.1 / 75.5;
  - NFW 75.2.
- **Scale length h:** PD 3.9–4.0; RM 3.5 (B1/B2) or 3.05 (B3); NFW 3.47 (B1) or 3.01 (B3); data 2.72.
- **Negative cold density** (RM-v only): 0.2–0.5% of the |dM| inside 30 kpc, near the bulge. It is disclosed, not hidden.
- **Controls C1–C3 and M1: all pass.**
  - C2: the phantom flux mass agrees with the cell sum to 0.1–0.6%.
  - C3: the homeoid at q = 1 reproduces the spherical field to 0.19%.
  - CFG514's PD Δχ² (+101.2 / +166.5) is reproduced exactly. RM-φ gives +3.0 / +0.6 against CFG514's MUTATE +1.9 / +0.1; the difference is Gauss-flux vs cell-sum enclosed mass, 0.5%.
- **Other K_z data:** none are on disk. The table's Σ_1.1 column comes from the same fits and was not scored.

## SPARC comparison

163 galaxies with Q ≤ 2, 3,244 points, Υ 0.5 / 0.7. The statistic is CFG476's weighted rms, in dex.

| model | rms, canonical | rms, alt | a₀ free | rms (free) | κ_Λ / κ_crit |
|---|---|---|---|---|---|
| ALG (rotmod V_bar, record's RAR) | 0.1117 | 0.1005 | — | — | — |
| ALG (grid baryons) | 0.1125 | 0.1014 | 1.341e-10 | 0.0978 | 0.716 / 0.593 |
| PD (full QUMOND) | 0.1203 | 0.1073 | 1.441e-10 | 0.1004 | 0.770 / 0.638 |
| RM-φ | 0.1205 | 0.1060 | 1.520e-10 | 0.0957 | 0.812 / 0.673 |
| RM-v | 0.1062 | 0.0999 | 1.204e-10 | 0.0995 | 0.643 / 0.533 |

- **Rule (≤ PD + 0.02 dex):**
  - RM-φ: +0.0003 / −0.0013 / −0.0047, PASS;
  - RM-v: −0.0141 / −0.0074 / −0.0009, PASS.
- **Median in-plane g ratios:** RM-φ/PD 1.005; RM-v/PD 1.092; PD/ALG 0.94.
- **Controls:**
  - S1 (grid V_bar vs rotmod) median 4.4%, PASS. The 90th percentile is 11%: the inner points miss because Σ★ is held constant inside R₁.
  - S2: 0.012 dex, PASS.
  - S3 (QUMOND Plummer, scale-free grid): 0.09%, PASS.
  - S4 (RM-φ identity): 1.9%, PASS.
- **Post-run variants** (added after a 14-galaxy smoke run put S1 at 5.2%; disclosed):
  - V1 keeps only points with grid V_bar within 5% (2,872 points);
  - V2 lets Σ★ rise inward with R_disk inside R₁ (S1 drops to 2.9%).
  - Every clause passes in both, and the κ shifts are unchanged to ±0.002 dex.

## Edge-on predictions (Part 3; prediction only)

Medians of PD/RM over 163 galaxies (canonical; alt is 3–7% larger):

| where | ν_z² PD/RM-φ | σ_z PD/RM (at fixed scale height) | HI thickness RM/PD (at fixed σ_HI) |
|---|---|---|---|
| 2 R_d, HSB (72) | 1.60 [1.28–1.87] | 1.22 | 1.26 |
| 2 R_d, LSB (91) | 3.30 [2.55–4.26] | 1.66 | 1.82 |
| R_last, HSB | 2.36 | 1.48 | 1.54 |
| R_last, LSB | 3.55 [2.74–4.78] | 1.75 | 1.89 |

RM-v is within 2–7% of RM-φ.

- **The difference is large.** The round rule predicts:
  - vertical restoring forces 1.6–3.6× weaker;
  - stellar σ_z 20–75% lower at a given scale height;
  - HI layers 25–90% thicker, i.e. stronger flaring, especially in LSB discs and outer discs.
- **None of it can be tested on disk.**
  - DiskMass: only the sample tables are present (Bershady+2010 flags, DMS XI Hα parameters). There are no σ_z profiles, which confirms CFG492.
  - No edge-on HI flaring data are on disk.

## Consistency (Part 4)

- **The vertical-force front.**
  - The record's earlier pass, full AQUAL on McMillan17 (6fb320dd: Σ_dyn 71.4 / 74.8 against McMillan's 73.9), used the α=2 kernel.
  - CFG514's PD is the first full-field ν_mono K_z, and it fails (90 / 95).
  - RM brings ν_mono back to the AQUAL-α=2 level: 70–76.
  - The two results do not contradict each other. What RM changes is the ratio of vertical to radial boost. QUMOND and AQUAL boost both directions alike (front: ν_vert/ν_rad = 1.024; PD here 1.45 vs 1.43 at R₀). Under RM, K_z is boosted only ×1.13 while v_c² is boosted ×1.43.
  - So RM is a round dark component carrying the law's mass. It is not a MOND-type field, and that is exactly what separates candidate B from QUMOND.
- **The growth rule (CFG424 engine).**
  - The PM sources the phantom on a Mpc/h mesh from a pressure-filtered baryon field, and the edge is fixed by M(<r).
  - RM keeps M(<r) and moves mass only inside a disc's vertical scale (sub-kpc), which is far below one mesh cell.
  - RM-φ and RM-v both become exact spherical QUMOND at r ≫ r_M.
  - So the mesh-level source and the edge are unchanged, and no PM rerun is needed. This is argued, not run.

## Needs an owner go (not on disk)

- DiskMass σ_z profiles (Martinsson+13, DMS VI/VII).
- HI flaring curves of edge-on discs (e.g. O'Brien+10, HALOGAS edge-ons).
- Gaia DR3 K_z(R, z) maps beyond Bovy & Rix's |z| = 1.1.

## Caveats

- **Recalled and unverified:** B3's R_d of 2.15 kpc, and the SPARC stellar thickness h_z = 0.196 R_d^0.633.
- **Gas inversion:** gas is inverted from V_gas, with thickness 0.1 kpc.
- **Bulges:** treated as spherical.
- **MW models:** isotropic and static. MI-law curl effects are not tested.
- **RM-v's definition** uses the radial-only algebraic law, so it inherits the ~6% in-plane offset from QUMOND (limit iii).
