# CFG914: is there one common density threshold for the law's open excesses? NO COMMON ORDERING (frozen and A1, both footings, both density variables, every variant)

Criteria: `FROZEN_CRITERIA.md` (6ec526287, committed alone before any script; orchestrator block CFG910–919).
`AMENDMENT_A1.md` (c043249ac) is **post hoc**. It was written after the frozen MUTATE-INJECT failed and was committed before the
amended method was run on the real data. See Controls.
κ = ½ FITTED; footings 9.3603e-11 / 1.1312e-10, never pooled; raw data and framework-native mass models; no dark-matter particle;
not theory closed.

## Question
Are the law's three open failures one phenomenon: extra cold mass kept where matter is DENSE?
- The three failures are faint dwarfs, red/spheroidal isolated lenses and eRASS1 cluster cores.
- Under the hypothesis, diffuse systems (SPARC rotators, blue lenses, cluster outskirts) follow the law.
- **Prediction:** the excess E = ln(g_obs/g_law) orders, in every sector, by one common local density, with a threshold ρ*.
- Globulars are dense and have no excess over their class-E Newton baseline (CFG883). They were declared a test sector beforehand,
  not excluded.

**Density variables, computed the same way in every sector:**
- **Primary:** ρ̄_law(<r) = 3 g_law/(4πG r). This is the law's own total density (baryons + the law's cold energy) inside the
  measurement radius. It does not contain the observed excess.
- **Graded variant V1:** the baryonic ρ̄_b(<r) = 3 g_bar/(4πG r).

**Sectors and inputs.** Each sector uses its source lane's own law kernel, baryon model and estimator, reproduced exactly (K1–K5):
| sector | source | units |
|---|---|---|
| DW dwarfs | CFG880 | 83 dwarfs, 8 equal-count bins |
| SS SPARC small (M_b ≤ 3e9) | CFG828 points, CFG870 split | 555 points / 56 galaxies |
| SL SPARC large | same | 2141 points / 91 galaxies |
| LR red lenses | B21 Fig-8, CFG850 M★ shift +0.123 | 9 points |
| LB blue lenses | same, unshifted | 8 points |
| CL eRASS1 clusters | CFG687 per-cluster arrays, MID+OUTER | 318 clusters × 5 radii |
| GC globulars | CFG883 tidally safe, outermost RV bin | 31 clusters, 5 bins |

## Result: CLASS **NO COMMON ORDERING**
It holds under the frozen method and under A1, on both footings, for both density variables, and in all ten reported variants.

| case | frozen: violators (greedy order, z) → survivors | A1 (post hoc): violators → survivors |
|---|---|---|
| canonical, ρ̄_law (headline) | CL 5.0, DW 5.0, LR 2.8, SL 2.5 → SS, LB, GC (no valid threshold) | SL 4.0, CL 4.4, DW 4.0, LR 2.8 → SS, LB, GC (none) |
| alt, ρ̄_law | CL 5.6, DW 4.8, LR 2.7 → SS, SL, LB, GC (none) | CL 4.6, DW 4.3, LR 2.5 → SS, SL, LB, GC (none) |
| canonical, ρ̄_b (V1) | CL 6.5, DW 5.1, LR 2.4 → SS, SL, LB, GC (none) | CL 5.8, DW 3.6, LR 2.8 → SS, SL, LB, GC (none) |
| alt, ρ̄_b (V1) | CL 6.5, DW 4.9, LR 2.2 → SS, SL, LB, GC (none) | CL 6.2, DW 3.9, LR 2.3 → SS, SL, LB, GC (threshold valid, but 0 failing sectors survive) |

**All three failing sectors violate every common fit.** The survivors are always the diffuse controls plus the globulars, and among
them there is nothing for a threshold to explain.

### Excess vs density, canonical, ρ̄_law (log M☉/pc³ : E ± σ; full tables for every case in `cfg914.out`)
| sector | bins |
|---|---|
| DW dwarfs | −2.51: +0.20±0.26; −1.84: +1.53±0.35; −1.63: +0.73±0.27; −1.50: +1.00±0.27; −1.36: +1.46±0.28; −1.17: +0.66±0.29; −0.96: +1.20±0.28; −0.69: +1.57±0.44 |
| SS SPARC small | −2.57: +0.09±0.12; −2.20: +0.13±0.05; −1.79: +0.07±0.07; −1.31: +0.14±0.09; −0.82: +0.25±0.09 |
| SL SPARC large | −3.13: +0.03±0.06; −2.67: +0.03±0.04; −2.23: +0.07±0.03; −1.75: +0.10±0.03; −1.29: +0.06±0.03; −0.78: −0.09±0.05; −0.26: −0.15±0.07; +0.18: −0.02±0.05; +0.66: −0.05±0.06 |
| LR red lenses | −5.07: +0.57±0.10; −4.70: +0.43±0.08; −4.20: +0.26±0.09; −3.69: +0.26±0.08; −3.18: +0.10±0.09 |
| LB blue lenses | −4.71: −0.08±0.24; −4.33: +0.28±0.11; −3.83: −0.09±0.16; −3.32: −0.16±0.16; −2.94: −0.49±0.31 |
| CL clusters | −5.60: +0.41±0.47; −5.15: −0.19±0.13; −4.80: +0.29±0.09; −4.32: +0.79±0.08; −3.94: +1.00±0.14 |
| GC globulars | −0.89: +1.15±0.42; −0.33: +0.31±0.26; −0.03: +0.47±0.26; +0.29: −0.16±0.26; +1.35: +0.03±0.26 |

(σ are the statistical errors. The 0.05-dex floor is added, correlated within each sector, in the tests.)

**What breaks the hypothesis:**
1. **Same density, different excess.**
   - Over ρ̄_law ≈ 10^−2.6 to 10^−0.7 M☉/pc³, the dwarfs carry E ≈ +0.2 to +1.6 (mostly +0.7 to +1.6, i.e. ×2–5 in mass).
     SPARC discs at the same densities sit at −0.15 to +0.25, with errors of 0.03–0.1.
   - At ≈ 10^−4.3 to 10^−3.9, the cluster cores carry +0.8 to +1.0, the blue lenses −0.1 to +0.3, and the red lenses +0.26.
   - Density does not decide the excess. System type does.
2. **The within-sector trends have opposite signs.** These are GLS slopes dE/dlog ρ̄_law, canonical, with the post-hoc
   permutation p from 200 within-sector shuffles:
   - **clusters rise**, +0.96 ± 0.16 (p < 0.005), in all four cases;
   - **red lenses fall**, −0.23 ± 0.06 (p < 0.005), in all four cases;
   - dwarfs rise in ρ̄_law, +0.57 ± 0.20 (p 0.01), but are flat in ρ̄_b (p 0.7);
   - blue lenses fall, −0.35 ± 0.15 (p 0.055–0.095), and globulars fall, −0.35 ± 0.18 (p 0.05–0.06); both are marginal;
   - SPARC is flat (p ≥ 0.18).
   - A common monotone law needs the same sign everywhere. Two failing sectors trend in opposite directions.
3. **No cross-sector ordering at all.** The pooled Spearman of (log ρ, E) over all 42 bins is −0.03 (permutation p 0.86)
   canonical and +0.04 (p 0.80) alt; for ρ̄_b, −0.11 (p 0.44) and −0.04.
4. **Globulars, the densest systems** (ρ̄ 10^−1.3 to 10^+1.9), show no density-driven excess.
   - Their bins fall from +1.15 ± 0.42 at the low-density end to +0.03 ± 0.26 at the high end.
   - The low end holds Pal 5 (+2.3, tidally disrupting), Pal 13 (+2.0, 20 stars), NGC 1851 (+1.0), Pyxis and Pal 14 (+0.6/+0.7
     against Newton at Υ 1.6), and NGC 2419 (−0.75).
   - They do not violate the generous common fit (z 1.2), because its high level is only +0.2. They do not support a dense-side
     excess either.

**Reported fits (not graded):**
- **Strict step (one common level):** ρ* = 10^−5.11, E_hi = +0.20 canonical (alt 10^−5.09, +0.12). Violators are the same three
  failing sectors, plus SL canonical.
- **Inverted fit (excess only BELOW a threshold):** ρ* ≈ 10^−0.3 (ρ̄_law) / 10^−0.8 (ρ̄_b). Only CL and DW violate (z 5–6). The
  survivors SS, SL, LR, LB and GC are all compatible with "excess, if any, at low density". The direction the data lean is the
  opposite of the hypothesis, but even the inverted form fails for the clusters and dwarfs.

## Variants (reported; frozen / A1 classes, both footings)
All 40 variant classifications (10 variants × 2 footings × 2 methods) are NO COMMON ORDERING. In every one, CL and DW are among
the violators.
| variant | canonical frozen violators | note |
|---|---|---|
| R1 g_bar as the ordering variable | CL 8.3, DW 6.3, GC 3.9, LR 2.7 | no valid threshold; the dwarfs' and red lenses' excess sits at LOW g_bar (as CFG828/851) |
| R2 ρ̄_obs (circular: contains E) | DW 9.3, CL 5.3, SS 4.1, LR 3.0 | even with E built into the density, no common ordering |
| R3 floor 0 / 0.1 dex | CL, DW, LR (+SL) / CL, SL, SS, LR | A1 with floor 0 equals the frozen method (no offsets) |
| R4 lens masses ∓0.3 dex | CL, DW, LR, SL | — |
| R5 red lenses without the M★ shift | CL, DW, SL | A1 alt: LR survives, but only 1 failing sector remains |
| R6 globulars ≥ 50 RV stars / R7 vs law+EFE | CL, DW, LR, SL | globulars never violate |
| R8 cluster INNER band included | CL 5.3, DW 5.0, LR 2.8, SL 2.5 | — |

## ρ* and framework scales (POST HOC; no common threshold exists, so nothing here is a result)
The all-sector fit's ρ*_eff is 10^−5.11 (canonical ρ̄_law), which is simply where the cluster bins turn positive. For comparison:
- ρ_crit(h 0.70) = 10^−6.87;
- ρ_DE ≡ 4a0²/(Gc²) = 10^−7.06 / 10^−6.90 (κ = ½ fitted);
- 3a0/(4πG L) = 10^+0.19 (L = 104 pc), 10^−0.80 (1 kpc), 10^−2.80 (100 kpc);
- CFG870's clump centre: 10^−0.22.

ρ*_eff matches none of them, and since the threshold model fails there is no ρ* to interpret. The inverted fit's ρ* ≈ 10^−0.3
lies near 3a0/(4πG·104 pc) and the clump centre. That is a post-hoc coincidence in a model that also fails, and it is not claimed.

## Controls
| control | result |
|---|---|
| K1 dwarfs: σ_law = CFG880's committed `law` (83 × 2 footings); CFG880 `pred_univ` from its committed σ̄_univ | exact (max rel 0) |
| K2a SPARC: CFG828 n_sparc 2696 and overall median (+0.0309 / +0.0054 dex) | exact |
| K2b SPARC: CFG870 sparc_D and its bootstrap σ with the committed V_x | exact |
| K3 lensing: CFG850 (+0.123, 0) A_red / A_blue / z_colour (both footings), CFG829 blue window A; lens medians 10.81 / 10.45 parsed from cfg912_colour.out | exact |
| K4 clusters: recomputed canonical law = the npz PL (318 × 8); CFG687 primary A (INNER/MID/OUTER, value + jackknife σ) on both footings | exact (after using CFG687's own FP0 a0, see Disclosures) |
| K5 globulars: CFG883 primary rows (R_pc, s_obs, s_B at Υ 1.6) for the tidally safe set; 31 per footing | exact |
| **MUTATE-SHUFFLE (frozen): FAILED its ≤ 0.15 bar** (200 within-sector density shuffles per footing × variable) | Shuffled median \|z_slope\| is 0.67–1.18 in every sector. The fraction with \|z\| ≥ 2 is 0.045–0.135 for DW, SS, SL and GC and for CL in 3 of 4 cases, but **0.170–0.195 for red lenses**, 0.130–0.165 for blue lenses (3 of 4 cases above 0.15) and 0.18 for CL (alt, ρ̄_b). Post-hoc permutation p of the real slope: CL 0/200 and LR 0/200 in all four cases; DW 0.010 (ρ̄_law), 0.71–0.73 (ρ̄_b); LB 0.055–0.095; GC 0.050–0.060; SS/SL 0.18–1.0. A shuffled realisation is still classed NO COMMON ORDERING, as expected, since within-sector shuffling keeps each sector's density range. |
| **MUTATE-INJECT (frozen): FAILED** (seed 914, one draw per case, E_hi 0.7 at the median bin density) | 3 of 4 cases PARTIAL (SPARC small/large flagged at z 2.3–13); alt ρ̄_b COMMON THRESHOLD, but ρ* missed by 1.6 dex |
| A1 re-score of the same four draws | COMMON THRESHOLD in all 4. ρ*_eff is exact in 3 (−2.02, −3.18, −1.99) and off by 1.66 dex in alt ρ̄_b; ρ*_half is within 0.2 dex in all 4 |
| A1 power (100 injected common thresholds per case; frozen classifier in brackets) | COMMON THRESHOLD: canonical ρ̄_law **83%** [21%], canonical ρ̄_b **78%** [41%], alt ρ̄_law **79%** [17%], alt ρ̄_b **77%** [43%]. NO COMMON ORDERING: A1 1–9% [14–23%]. ρ*_eff within 0.5 dex 47–71%; ρ*_half 99–100% |
| A1 false-positive check (each sector its own threshold, median ± U(1.5) dex) | COMMON THRESHOLD in 16 / 20 / 19 / 16% [frozen 8 / 11 / 6 / 10%]: unrelated per-sector thresholds within ±1.5 dex sometimes pass as one |

**Why the frozen MUTATE failed, and what A1 changes.**
- The frozen fit weights each bin by 1/(SE² + σ_floor²), i.e. it treats the floor as independent per bin. The sector test treats it
  as one offset per sector.
- With a true threshold injected, each sector draws its own offset (seed 914: SPARC small +0.22, SPARC large −0.21). The frozen fit
  then misplaced the threshold by one bin and lowered the high level to 0.58. The precise SPARC bins "violated" at z 5–13.
- Over 100 injections the frozen classifier recovered a true common threshold only 17–43% of the time and returned NO COMMON
  ORDERING 14–23% of the time. **So the frozen fail is weak evidence on its own.**
- A1 fits the per-sector offsets with the floor as their prior. The test is unchanged. A1 recovers a true common threshold in
  77–83% of injections, against a nominal 85% for seven 2σ tests.
- **The real data give NO COMMON ORDERING under both methods.** The violations are level conflicts at the same density (dwarfs vs
  SPARC, cluster cores vs lenses), not threshold-placement artefacts. Under A1 the fit even absorbs sizeable per-sector offsets
  (canonical: DW +0.28, SL −0.43, SS −0.28, LB −0.28, CL +0.15) and five sectors still violate.

## Reading
1. **The three open excesses are not one density-driven phenomenon.**
   - At matched density, faint dwarfs carry ×2–5 more mass than the law while SPARC discs carry none.
   - Cluster cores carry ×2.2–2.7 while blue lenses at the same density carry none and red lenses ×1.3.
   - Within sectors the trend with density has opposite signs (clusters and dwarfs up; lenses and globulars down).
   - No single ρ*, or any monotone function of one local density (law-total or baryonic), fits the dwarfs, the cluster cores and the
     red lenses together with the diffuse controls.
2. **Globulars:** the densest sector shows no dense-side excess. It is compatible with the common fit only because that fit's level
   is small.
3. **What stays open (unchanged):**
   - the dwarf excess (CFG880/890: mass-like, per-dwarf scatter ×1.3);
   - the red-lens excess (CFG850/885/912: not M★, not distances, not environment);
   - the cluster-core excess (CFG687: ×1.9, with T2 following Newton).
   CFG914 removes one candidate unifying cause, local density, for all three. A unifying variable would have to separate system
   types at the same density, e.g. pressure support or formation history; this lane does not test that.
4. Nothing here says the data favour the framework. The law itself is what fails in the three sectors.

## Disclosures
- **Not blind.** Every sector's excess was known from its source lane. No density had been computed before the criteria were
  committed. The pre-freeze order-of-magnitude hand estimate (listed in the criteria) anticipated that SPARC overlaps the dwarfs in
  density, and it did.
- **Development runs.**
  - Run 1 failed K4a/K4b at 1.3e-6 / 1.5e-6 relative. This lane had used the rounded footing a0 for the cluster law, while CFG687
    uses FP0's unrounded value (9.360325e-11 / 1.131204e-10, +2.7e-6 / +3.1e-6; `CFG4_common.A0`). The cluster law now uses the
    source lane's constant.
  - Run 2 is identical to run 1 apart from those K4 lines (diffed).
  - The A1 code was then added. The frozen numbers in the committed run are byte-identical to run 2 apart from line labels (diffed).
  - After the frozen shuffle run, one POST-HOC reported quantity was added: the permutation p of the real slope. The shuffle was
    re-run and every frozen number is identical (diffed).
  - The primary was re-run with the final script and is identical apart from timing. The committed inject output comes from the
    script before that shuffle-only edit; the inject code path did not change.
- **The A1 scratch diagnostics** (frozen and A1 power over 100 injections) were run before A1 was written. They are disclosed in
  `AMENDMENT_A1.md`, and the committed inject run reproduces them exactly.
- **Frozen MUTATE-SHUFFLE recorded as FAILED.** The ≤ 0.15 expectation assumed a calibrated slope z. With only 4–6 bins and real
  scatter in E beyond the errors (which a shuffle keeps), the lens sectors give |z| ≥ 2 in 13–20% of shuffles. The ordering still
  collapses (median |z| ≈ 1 against a real 3.7), and the post-hoc permutation p values above are the calibrated statement.
- **Frozen MUTATE-INJECT recorded as FAILED**, as frozen. Its ρ*-recovery requirement (±0.5 dex) is also too strict for ρ*_eff
  under A1 (within 0.5 dex in only 47–71% of A1 injections). A1's ρ*_half recovers within 0.5 dex in 99–100%.
- **Proxies and approximations.**
  - Lens radii use the median lens mass of the record's B21 reconstruction (u−r 2.0 classes on LePhare MAG_ABS), not B21's
    u−r 2.5 split. R4 brackets ±0.3 dex.
  - For lensing and clusters the 3D radius is set equal to the projected radius.
  - Disc densities use the spherical-equivalent 3g/(4πGr) as defined.
  - Each sector keeps its source lane's kernel (ν_e; ν_mono for clusters; Newton for globulars), Υ and baryon model.
  - No EFE for dwarfs (as CFG880). The globular E uses SPS Υ_V 1.6 with its 0.15-dex prior width as an error.
- **Statistics.**
  - Sector z uses n_bins degrees of freedom with no parameter subtraction (generous to the hypothesis).
  - The fit uses diagonal weights. SPARC, lensing and cluster bins carry bootstrap, analytic and jackknife covariances in the test.
  - Greedy removal order is reported. Seven sectors at 2σ give a nominal 15% false-violation rate, which the A1 power figure reflects.
- **Compute.** One core, nice 10, peak RSS ≈ 120 MB. Primary run ≈ 20 s; inject ≈ 195 s; shuffle ≈ 30 s. Run beside
  the live 1024³ job; no other process was touched. No downloads.

## Files and rerun
- `FROZEN_CRITERIA.md`, `AMENDMENT_A1.md`
- `cfg914.py`. It execs read-only: CFG880's sample and law code, CFG829's B21 loader and amplitude, and CFG883's tracer and
  Baumgardt parser. It copies CFG687's `law()` / projector and CFG870's SPARC D. It imports `CFG4_common.nu_mono` / `A0`.
- Outputs: `cfg914.out`, `cfg914_results.json` (all bins with covariances, per-system rows, fits, variants, classes);
  `cfg914_MUTATE_shuffle.{out,json}`; `cfg914_MUTATE_inject.{out,json}`.
- Rerun from this directory with `OMP_NUM_THREADS=1 nice -n 10 python3 cfg914.py`, then the same command with
  `CFG914_MUTATE=shuffle` and with `CFG914_MUTATE=inject`.
