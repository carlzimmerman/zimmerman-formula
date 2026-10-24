# ZT_zstar_tests: the first three decisive tests of design Z★ (v3s-OC)

Run exactly as frozen in `Z1_successor_design/TEST_PLAN.md` (0d1959a4f5). This lane's implementation choices are in
`FROZEN_CRITERIA.md` (fe73a8eae1, committed alone before any script or number). κ = ½ FITTED. Footings canonical / alt
(9.3603e-11 / 1.1312e-10 m/s²), never pooled. No dark-matter particle. Not "theory closed". Nothing here says the data
favour the framework.

## Verdict

| test | frozen result | kills Z★? |
|---|---|---|
| **Z-T1** hosted retention | **UNDECIDED (coverage)** on both footings. No class is outside its band, and the control passes. But no class has both band edges on disk. | no (not FAIL) |
| Z-T1 Coma UDG side line | **PASS** on both footings: predicted +0.361 dex, observed +0.325 / +0.285 ± 0.114 (z −0.31 / −0.66) | — |
| **Z-T2** cluster terciles | **FAIL** at R_own = 200ρ_c and **PARTIAL** at R_own = 18π²ρ̄_m, on both footings. Each class holds in both h cells and for both r_s definitions. | no (records the cluster row) |
| **Z-T3** two-sided obstacle | **PASS** on both footings and both brackets (pinned and released). One qualifier: the zero-dust edge has no finite rate. | no |

**Z★ survives all three tests**: Z-T1 is not FAIL and Z-T3 is not FAIL. That is weaker than passing them. Z-T1 cannot be
decided from the inputs on disk, and the cluster row stays red.

## Z-T1: hosted retention (`zt1_hosted_retention.py`)

**The test.** The observed value is X1's bootstrap class median of Δ[iso AQUAL L*0] ± its bootstrap sd. The band is
[Δ_lo − 2σ, Δ_hi + 2σ], where:
- Δ_lo = ½ log₁₀(1 + matched isolated-dwarf gas ratio), using RAW HI from LVD flux and distance and M_gas = 1.33 M_HI;
- Δ_hi = ½ log₁₀ L_MDF from P1.

| class | canonical: obs ± σ, [Δ_lo, Δ_hi] → status | alt |
|---|---|---|
| MW classical (8) | +0.277 ± 0.148, [+0.039, —] → UNDETERMINED | +0.235 ± 0.150, [+0.039, —] → UNDETERMINED |
| bright M31 (25) | +0.249 ± 0.092, [+0.140, —] → UNDETERMINED | +0.211 ± 0.090, [+0.140, —] → UNDETERMINED |
| MW ultra-faints (31) | +0.625 ± 0.111, [—, +0.654] → UNDETERMINED | +0.585 ± 0.109, [—, +0.654] → UNDETERMINED |
| M31 others (5) | +0.644 ± 0.283, [—, —] → UNDETERMINED | +0.587 ± 0.284, [—, —] → UNDETERMINED |
| control: isolated LG field (13) | +0.055 ± 0.080 vs own Δ_lo +0.101 (z −0.58) → **PASS** | +0.017 ± 0.080 vs +0.101 (z −1.06) → **PASS** |

The frozen rule needs ≥ 3 classes IN for PASS, and ≥ 2 OUT (or a control failure) for FAIL. Here IN = 0 and OUT = 0 on
both footings, so the result is UNDECIDED. Every defined edge is respected. Where a class has values for less than half
its members, the median over the members that have one still sits inside the band (bright M31 Δ_hi +0.575 / +0.560 from
3 / 4 systems; ultra-faint Δ_lo +0.236 from 1 system).

**Missing inputs.** Each leg was stopped, not substituted, and these inputs are what it needs:
1. **P1 has no L_MDF for 8 / 8 MW classical, 22 / 25 (canonical) or 21 / 25 (alt) bright M31, 5 / 5 M31 others, and 5 / 31
   ultra-faints** (Carina III, Grus I, Pictor II, Tucana II, Tucana IV).
   - In LVD, 9 of the uncovered bright M31 have no MDF width (And II, IX, XIV, XV, XXI, XXV, Cas III, Lac I, Per I), and 6 have
     no mean [Fe/H] (And VI, XVII, XXIII, XXVII, Cas II, LGS 3).
   - All 5 M31 others have no [Fe/H] (And XI, XIII, XX, XXII, XXVI).
2. **X1's isolated LG dwarfs stop at log M★ 5.43 (Leo T).** 30 / 31 ultra-faints and 4 / 5 M31 others have no isolated
   dwarf within ±0.5 dex. This is a gap in the sample, not a missing file. LVD lists 8 local-field dwarfs below 10^5.4 M☉
   (3 with HI detections, 2 with HI limits), but none has a measured σ, so none is in X1's control.
   - The plan's Δ_lo construction restricts the window to X1's control. Filling it at UFD masses would need a change to
     the plan, not a new file.

**Reported extensions (declared, no verdict weight).**
- E3 runs P1's own `lmdf()`, exec'd from its source, on LVD for the uncovered members. It reproduces all 63 of P1's
  committed values exactly (K3).
- That supplies **MW classical Δ_hi = +0.383**, so the class goes IN on both footings: Fornax L 1.00 (UNDER), Leo I 1.76,
  Carina 2.31, Draco 5.77, Leo II 5.89, Sculptor 6.27, UMi 6.69, Sextans 8.17.
- E1 (empty window → 0) and E2 (empty window → nearest isolated dwarf, +0.236) put the **ultra-faints IN**.
- Bright M31 reaches only 10 / 25 coverage (Δ_hi +0.411 over those) and M31 others 0 / 5. Even the most generous reading
  is therefore **UNDECIDED: 2 IN, 2 UNDETERMINED, 0 OUT**, with the control passing.
- HI upper limits at the limit (E4) change nothing.
- The control leave-one-out (E5) gives Δ_lo +0.070 (z −0.19 / −0.66).

**Coma UDG side line (frozen).**
- Predicted: Δ_pred = ½ log₁₀(1/(1 − 0.81)) = +0.361 dex.
- Observed: S1's isolated AQUAL excess, +0.325 / +0.285 dex.
- σ = S1's statistical se, 0.114 dex. z = −0.31 / −0.66, so **PASS** on both footings. With σ_sys added: z −0.18 / −0.38.
- Reported: CFG948's unrounded 0.8136 gives +0.365. Its Υ_g brackets give +0.251 (Υ_g 2) and +0.494 (Υ_g 0.5). The test has
  little power: σ_tot is 0.20 dex.

## Z-T2: cluster terciles under the capacity-truncated law (`zt2_cluster_terciles.py`)

**Setup.**
- Baseline: X2's C* without the EFE ("C*_own", because the owner frame removes it): CFG814 gas, reduced shear,
  systematics (e).
- Data: X2's eRASS1 × raw KiDS stack, boost convention, both native-h cells.
- Z★ profile per cluster: the AQUAL law inside r_t = min(r_s, R_own). Beyond r_t it is M_b + f_s M_b,own, or, when supply
  is rich (R_own < r_s), the law stops at R_own and the free excess follows CFG930's debris profile.
- f_s = 5.364, as recorded. No constant was fitted.

A = data / model, ± s_tot. Each range spans h 0.672 / 0.686 and r_s (capacity / closed form). Z = (A − 1)/s_tot.

| footing, R_own | T1 MID / OUTER | T2 MID / OUTER | T3 MID / OUTER | class |
|---|---|---|---|---|
| canonical, 200ρ_c | 1.53–1.64 (Z +1.0) / 1.97–2.24 (+0.8) | 1.64–1.73 (+1.8…+2.0) / **1.50–1.61 (+2.0…+2.5)** | **1.45–1.47 (+2.9…+3.1)** / **1.47–1.48 (+3.4…+4.0)** | **FAIL** |
| canonical, 18π²ρ̄_m | 1.13–1.20 (+0.4) / 1.18–1.39 (+0.3) | 1.70–1.76 (+1.9…+2.1) / 0.91–0.99 (−0.6…−0.1) | **1.68–1.71 (+3.9…+4.1)** / 1.18–1.21 (+1.8…+1.9) | **PARTIAL** |
| alt, 200ρ_c | 1.49–1.60 (+1.0) / 1.97–2.27 (+0.8) | 1.55–1.65 (+1.6…+1.9) / **1.48–1.60 (+1.9…+2.5)** | **1.41–1.43 (+2.7…+2.9)** / **1.42–1.43 (+3.1…+3.7)** | **FAIL** |
| alt, 18π²ρ̄_m | 1.07–1.13 (+0.3) / 1.18–1.42 (+0.3) | 1.52–1.58 (+1.6…+1.8) / 0.90–1.00 (−0.6…0.0) | **1.62–1.65 (+3.6…+3.9)** / 1.13–1.15 (+1.3…+1.4) | **PARTIAL** |
| *reference: untruncated law, C*_own* | 1.01–1.12 / 0.45–0.53 | 1.70–1.92 / 0.70–0.78 | 1.69–1.88 / 1.22–1.37 | — |

- **The core excess stays.** T3 MID is 1.41–1.71, Z +2.7…+4.1 *with* systematics (e), in every cell and convention. The
  plan's forecast is confirmed for T3.
  - T2 MID passes in most cells only because its s_tot is about 0.35.
  - The small MID improvement over the law in T3 comes from the rich clusters' free excess, carried on CFG930's
    concentrated debris profile.
- **OUTER depends on the owner radius.**
  - At 18π²ρ̄_m (R_own 1.0 / 1.7 / 2.2 Mpc), the truncation turns the law's T1/T2 deficit (0.45–0.78) into 0.90–1.42.
    OUTER then passes in every tercile.
  - At 200ρ_c (R_own 0.6 / 1.0 / 1.4 Mpc), the truncation is too strong: T2 and T3 OUTER sit 1.4–1.6× above the model.
  - Design/law enclosed mass at 2 Mpc, tercile medians:
    - 200ρ_c: 0.18 / 0.41 / 0.69 canonical; 0.17 / 0.38 / 0.66 alt;
    - 18π²ρ̄_m: 0.27 / 0.66 / 1.00 canonical; 0.25 / 0.60 / 1.00 alt.
- **The C0 + (e) baseline gives the same classes in every cell.**
- The capacity and closed-form r_s agree to ≤ 0.15 Mpc at the tercile medians. The 6–7 % "negative-density" cells are all
  beyond the 3 Mpc gas cut, at |ρ| ≤ 1e-39 against a peak of 1e-21 kg/m³: roundoff zeros, floored as zeros.

## Z-T3: the two-sided obstacle 0 ≤ D·P ≤ ρ_d (`zt3_two_sided_obstacle.py`)

**Symbol (X3's B2-S plus the upper wall; sympy).**
- c² = (s₀ + ρ_d)(γ_L/2)F″(s₀).
- In the saturated set, approached from below, **c² = 2γ_Lρ_d > 0**.
- On the penalty side, c² = γ_Lρ_d(1 + P)(2 + t) ≥ 0 for every P ≥ 0.
- In the soft region it is 0: the wall does not reach it.
- Both footings (γ_L = 4πG L★²/2 at 21.68 / 22.85 pc) give c² ≥ 2.5e4 / 2.8e4 m²/s² over ρ_d 1e-3 to 1 M☉/pc³.
- The branch bookkeeping matches the Piecewise forms to 6e-17.

**Slab (X3's `slab()`, exec'd from source; K0 reproduces X3's C2 ladder to 4e-14).**
- Setup: ρ_d = 0.1, X3's unaligned grid, N 64–1024, both brackets.
  - Released: saturated nodes keep γ_L.
  - Pinned: δ(D·P) = 0 there. γ_sat = 1e6 agrees with 1e4 to 3e-6.
- γ_L by footing: 2.35e-2 / 2.35e-4 (canonical) and 2.61e-2 / 2.61e-4 (alt), for λ 0.1 / 1 kpc.
- **All 8 primary ladders converge to Γ = 1.18321**, the localised-mode value √1.4. That is X3's C2 value: the wall
  leaves the ρ_τ < 0 region untouched.
- Finest ratios are 0.99999–1.00001. Γ ≤ 1.511 (X3's rigorous bound) at every level, and there are 0 sign violations.
- 303 / 1024 nodes are saturated.

**Qualifiers (diagnostics, no verdict weight).**
1. **The zero-dust edge has no finite rate in the pinned bracket.**
   - At ρ_d = 0 the wall coincides with X3's switch. A pinned node then sits next to a ρ_τ < 0 face, and Γ grows as
     N^0.499 (aligned grid, 1.15e4 → 4.57e4).
   - Γ also scales as √γ_sat: 324 / 3236 / 32360 at γ_sat 1e2 / 1e4 / 1e6.
   - The unaligned grid alternates with node placement, like X3's C3a.
   - The released bracket stays at 1.22474. At ρ_d = 0.01 both brackets converge (1.22065).
   - So Z★'s well-posedness needs a dust buffer ρ_d > 0 between saturated and ρ_τ < 0 regions, as X3's switch did. The
     pinned limit makes the knife edge sharper: X3's C3b grew as N^½ at fixed γ_L, and here the rate also grows without
     bound as γ_sat increases.
2. **Smoothing.** A smoothed upper wall whose support reaches s < −ρ_d puts c² < 0 in the soft region (−2.4e-12 to
   −1.9e-4 at ε 1e-3 to 1e-1). A penalty starting at ρ_d − ε is safe iff ε ≤ 2ρ_d. The wall, like the switch, must be
   exact.
3. **R1's literal lower bound D·P ≥ 0** clamps ρ_τ ≥ ρ_d > 0 everywhere, so Γ = 0. But it forbids v3s's D·P < 0 lobes:
   two-body saddles, and the outer-globular EFE lobes at 180–1555 pc where non-owners sit in an owner's field. X3's
   statics lemma does not cover those. The design text reads the lower bound as X3's switch; this lane tested that reading,
   as the plan says.
4. Only the 1D slab and the frozen-coefficient symbol are tested. The dust is a fixed background (as in X3), and R1's
   held/free exchange dynamics (non-variational) is not modelled. The 2D/3D gap of X3 remains.

## Checks and mutation

| script | normal | `--mutate` |
|---|---|---|
| Z-T1 | 6/6 PASS. K1 RAW HI vs LVD 0.005 dex; K2 X1 class table; K3 P1 L_MDF reproduced, 63 rows to 0; K4 the ½ retention identity 1.7e-4; K5 Coma inputs; K6 0.41 GB | K1 (0.38 dex) and K4 (0.65 dex) FAIL, as required |
| Z-T2 | 6/6 PASS. K0 X2's terciles to 0.0; K1 inactive truncation equals the law to 2.8e-15; K2 r_s(cap) = closed form to 1.1e-8; K3 bookkeeping 4.4e-16; K4 reduced shear; K5 0.37 GB | K0 (3.2) and K3 (1.6e3) FAIL, as required |
| Z-T3 | 6/6 PASS. B2-Z; K0 X3 to 4e-14; K1 copy without the wall equals X3 to 0; K2 pinning converged; C-Z; K3 0.887 GB | C-Z FAILS (ratio 2.00, bound broken, 41–647 violations), as required |

## Amendments and development fixes (disclosed)

- **Z-T2 A1 (post-RUN1, check only).**
  - RUN1's K1 used f_s = 1e6. That also moves R_own inside 30 Mpc for light clusters and makes them supply-rich with a huge
    free excess. That is the frozen model behaving as specified, not the law limit, so K1 failed (2e25) on cluster 294.
  - K1 now removes the capacity and the owner boundary together, and compares on each cluster's max |ΔΣ|.
  - Every verdict number is identical between RUN1 (`zt2_cluster_terciles_RUN1.out`, kept) and the final run.
  - A reporting-only column (the negative-cell fraction) was added.
- **Z-T3 (development).**
  - The first attempt stopped in sympy (a Piecewise limit) before printing any number. The branches are now evaluated per
    region and cross-checked against the Piecewise forms.
  - The second run printed B2-Z PASS and C-Z PASS. It then hit this lane's 0.95 GB guard in the N = 2048 *diagnostic*
    ladders and aborted. Its exact peak is unknown, between 0.95 GB and the guard's next check.
  - Diagnostic ladders are now capped at N = 1024 (aligned 768). A γ_sat scan was added. The final peak is 0.887 GB.
- **Z-T1:** a control-key bug in the E5 classifier was fixed before the first run printed anything.

## What this does not show

- **Z-T1 is not a pass.** It is undecidable on disk. The band is also wide (≈ 0.04 to 0.65 dex): with E1–E3, every class
  median that has edges sits inside it, but a band that wide constrains little.
  - Δ_hi rests on P1's *minimum* processed-baryon reading (the plan's choice).
  - Δ_lo matches gas ratios only at log M★ ≥ 5.4.
- **Z-T2** uses X2's spherical, β-model, h-rescaled catalogue machinery. CFG930's debris form is NFW with C = 3000, a
  convention. R_own is K10's (1 + f_s)M_b definition at the cluster's redshift. The two R_own conventions give different
  classes. Both are reported, as frozen, and neither is preferred here.
- **Z-T3** is 1D and linear about a fixed background. Owner boundaries (R2) are not analysed.
- R2 (ownership) and R1's dynamics still have no action. No test here builds one.

## Run

```
OMP_NUM_THREADS=1 nice -n 15 python3 rebuild_2026_10_22/ZT_zstar_tests/zt1_hosted_retention.py [--mutate]    # 5 s, 0.41 GB
OMP_NUM_THREADS=1 nice -n 15 python3 rebuild_2026_10_22/ZT_zstar_tests/zt2_cluster_terciles.py [--mutate]    # 71 s, 0.37 GB
OMP_NUM_THREADS=1 nice -n 15 python3 rebuild_2026_10_22/ZT_zstar_tests/zt3_two_sided_obstacle.py [--mutate]  # seconds, 0.89 GB
```

One thread each, run one at a time. Read-only inputs, pinned in `FROZEN_CRITERIA.md` §1. Nothing was downloaded. No
input file was edited.

## Files

- `FROZEN_CRITERIA.md`: criteria and assumption ledger.
- `zt1_hosted_retention.py` → `.out`, `_results.json`, `zt1_per_owner.csv`, plus the `_MUTATE` pair.
- `zt2_cluster_terciles.py` → `.out`, `_results.json`, `_RUN1.out`, plus the `_MUTATE` pair.
- `zt3_two_sided_obstacle.py` → `.out`, `_results.json`, plus the `_MUTATE` pair.
