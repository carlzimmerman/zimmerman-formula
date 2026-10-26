# IC1_inner_cluster_band — RESULT: F-ISO FAILS (both footings); the INNER miss is a uniform 2× shape problem, not a subset or centring artefact

Frozen criteria 4bf9ef4e51 (committed alone). Amendment A1 c8177a5313 is POST-RESULT and numerics only: the Lane–Emden
table goes from 6000 to 30000 points, and the K1 threshold is unchanged. κ = ½ FITTED; footings calibrated and scored
separately, never pooled; cold dark energy, not matter; nothing here says the data favour the framework or ΛCDM; not
"theory closed".

The id IC1 is also used by the finished lane `IC1_inner_column_cores/`. This lane's files carry the prefix `ic1b_`.

**Target.** OS1's single out-of-sample cluster miss: G-IN-Mall (INNER band, 0.15–0.46 Mpc, all 326 eRASS1 clusters,
MGAS500 binning), Z −2.41 (canonical) / −2.06 (alt) at h 0.672. It is an over-prediction.

## 1. Diagnostics (post-run on OS1, labelled, not graded; `ic1b_diagnostics.out`)

`ic1b_lib` (SC1 → X38 → EM1/X30 read-only, as OS1 loads them) reproduces OS1's cells exactly (|Δpred| 0).

| suspect | finding | verdict |
|---|---|---|
| MGAS500 terciles | Every tercile is over-predicted ≈ 2×. Canonical h 0.672: M1 / M2 / M3 Z −1.90 / −2.90 / −1.58; KT terciles −1.65 / −2.81 / −1.19. M3 carries ~50% of the excess, M2 ~29%, M1 ~20%. | not one tercile |
| INNER error and weighting | s_IN is dominated by the cross-shear term (A_x ≈ −1.0; s_STAT 0.29; Z on s_STAT alone would be −8.6). The KT-only cell (G-IN-all) is over-predicted by **more** (pred/meas 2.4–2.6 vs 2.1–2.2). It passes only because its s_IN is 1.67 vs 1.05; at M-all's error it would give −2.90 / −2.54. | the KT-only "pass" is error size |
| miscentring / BCG | The record's catalogue miscentring is already applied. Offsets ×0 make it worse (−2.78); ×2 would pass (−1.84), but that is a knob. A 10¹² M☉ central point mass does nothing at R ≥ 0.15 Mpc. | not the driver |
| σ tercile fill | Filled (n 220) and KT (n 106) clusters are over-predicted alike (Z −2.06 vs −1.81). A regression fill leaves −2.47. | not the driver |
| Burkert inner shape | Swapping the shape moves INNER to a pass (next section). | **the driver** |

## 2. The fix tried (frozen): F-ISO, LN1 T7's isothermal core

T7's premise, the non-singular isothermal sphere (King r0, ρ0 r0² = 9σ²/4πG), replaces X38's posited Burkert at the same
Σ = ρ0 r0 = Σ_a0 (σ/σ_ref)^q and the same mass rule. It is applied to SPARC and clusters alike, and q is re-calibrated once
on SPARC by OS1's rule.

| | canonical | alt |
|---|---|---|
| q (SPARC only) | **0.722** (Burkert 0.892) | **0.534** (Burkert 0.748) |
| SPARC A rms @ Υ | 0.0703 @ 0.70 (Burkert 0.0605) — line PASS | 0.0727 @ 0.64 (Burkert 0.0591) — line PASS |
| SPARC B | 0.0680 @ 0.69 | 0.0702 @ 0.61 |
| **G-IN-Mall** | **−2.41 → +0.21** | **−2.06 → +0.22** |
| OS1-passing cells now failing | **7**: MID T2 +3.01, MID T3 +5.11, MID slope +2.39, OUT T3 +2.41, OUT M-all +4.91, OUT M2 +2.52, OUT M3 **+7.89** | same 7 (OUT M3 +7.77) |
| q_iso ± 0.05 | same 7 fails | same 7 fails |
| **class (frozen)** | **FAILS** | **FAILS** |

**Verdict: FAILS** (both footings agree), as expected and disclosed before the run.
- Checks 4/4: K0 (the Burkert path re-derives OS1's q_f and cells exactly), K1 (isothermal table vs quadrature 1.2e-7),
  K2 (peak RSS 0.59 GB).
- Run 1 failed K1 at 1.8e-6. Its file is kept as `ic1b_fix_run1_K1FAIL.out`. After A1, the cells moved by ≤ 3e-6 in Z
  and q did not move.
- **MUTATE** replaces the core with the singular isothermal sphere: K1 fails, exit 1, as frozen. Its cluster cells are
  almost unchanged (G-IN-Mall +0.47, OUT M3 +7.68, the same 7 fails), and SPARC fails its line (0.111).

## What it means

1. **The miss is a shape problem, and the shape trades INNER against MID/OUTER.** With the mass fixed at M_fair inside r_ta:
   - the Burkert r⁻³ tail packs the mass into 0.15–3 Mpc, so INNER comes out 2× high while MID/OUTER pass;
   - the isothermal r⁻² tail spreads it to r_ta, so INNER is right and MID/OUTER come out ≈ 2× low.

   Neither tail fits all three bands.
2. **Under F-ISO the core law is inactive in clusters.** Outside the core, the isothermal profile is ρ ≈ M_fair/(4π r_ta r²)
   whatever Σ is. That is why q ± 0.05, and even removing the core (MUTATE), barely moves a cluster cell. The cluster
   successes of OS1 therefore come from the Burkert outskirts plus Σ(σ) setting a compact r0, not from an isothermal core.
3. **No principled one-step repair closes INNER without breaking the rest.**
   - The KT-only subset only hides the same 2× behind a larger error.
   - Miscentring is already at the record's convention; ×2 would be a fitted knob.
   - The T7 shape breaks seven cells.

   The data want a profile that is flat (or lower) at 0.15–0.46 Mpc but keeps r⁻³-like mass at 0.5–3 Mpc. That points to
   a larger cluster core at fixed outskirts than the compact-root Burkert gives. That is a reading for a future lane, not
   derived here.
4. **OS1's standing is unchanged.** It keeps 14/15 out of sample; INNER M-all stays its one cluster miss, now diagnosed as
   a uniform inner over-prediction of the posited Burkert shape.

## Files

| file | content |
|---|---|
| `FROZEN_CRITERIA.md`, `AMENDMENT_A1.md` | criteria; post-result table-resolution amendment |
| `ic1b_lib.py` | read-only loader, generic halo shape, isothermal table, cell builder (OS1's arithmetic) |
| `ic1b_diagnostics.py` / `.out` / `_results.json` | D0–D5 (not graded) |
| `ic1b_fix.py` / `.out` / `_results.json` | graded run (after A1) |
| `ic1b_fix_MUTATE.out` / `_results_MUTATE.json` | control |
| `ic1b_fix_run1_K1FAIL.out` / `_results_run1_K1FAIL.json` | run 1, before A1 |

Run with `PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 ic1b_fix.py [--mutate]` (about 1 min, < 0.6 GB, one thread).
