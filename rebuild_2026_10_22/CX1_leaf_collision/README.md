# CX1_leaf_collision: the leaves don't put the wall in one place. X-COP, the ultra-faint dwarfs and IC 1613 have no gradable leaf neighbour, so there is no data-level no-go for them. L3 reads NO-GO by the frozen rule, but only through lensing against SPARC, and that rests on the innermost lensing radius

Criteria `FROZEN_CRITERIA.md` (39e61ccb9c), committed alone. `AMENDMENT_A1.md` (390871bd3f), pre-result, committed alone. Scripts `cx1_rows.py` (rows, error budgets, Monte Carlo) and `cx1.py` (modes `controls`, `real`, `mutate`). `cx1_post.py` is POST-RESULT. Outputs `cx1_controls.*`, `cx1_real.*`, `cx1_MUTATE.*`, `cx1_post.*`. Run with `PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 10 python3 -I cx1.py <mode>`, RSS 0.2 GB.

**Not blind.** κ = ½ FITTED. No cold component, no particle; the cold sector stays retired. Not theory closed. Nothing here says the data favour the framework. A no-go here applies to these leaves, these inputs and these error budgets, and only to rules that vary smoothly on the scale of the errors.

## What was asked
BF1 and SY1 search for a rule built from class-blind leaves. Is there a pair of measured points, from different systems, with the same leaves within errors but different required boosts B = g_obs/g_law(g_b) beyond errors? If so, no smooth function of those leaves can fit both.

- **Leaves:** SY1's own (`sy1_leaves`), at a0 canonical on both footings.
- **B:** computed per footing.
- **Rows:** RS1's (`rs1_rows.table`), with every error propagated by Monte Carlo (400 draws).
- **Distance:** leaf-space Mahalanobis d_L. A pair counts as near at d_L ≤ 1.
- **Point collision:** z ≥ 3 on the boost gap. It is strong at z ≥ z_LEE, the look-elsewhere threshold.
- **Line collision:** the intercept of the boost gap regressed on the leaf gap over near pairs. It must exceed 3 sd (bootstrap over systems) and the sum of the two lines' tolerances, with at least 3 systems on each side.

## Verdicts (line level is the primary verdict; both footings agree in every cell)

| Arm | Rows | Line level, all rows | X-COP dropped | X-COP −0.12 dex | Point level |
|---|---|---|---|---|---|
| **L3** (y, ell, f) | 3394 | **NO-GO IN LEAF SPACE**: L\|S only | same | same | UNDETERMINED |
| **L5** (+ s, D implied) | 3229 | NO COLLISION | same | same | NO COLLISION |
| **L3+E** (+ basin mass) | 3341 | NO COLLISION | same | same | UNDETERMINED |
| **L5+E** | 3185 | UNDETERMINED: the planted control fails | same | same | NO COLLISION |

- **X-COP is never near any other line**, so dropping it or lowering it by 0.12 dex changes nothing. Its smallest d_L to any row of another line:
  - L3: 8.6 to SPARC, 8.3 to lensing, 23 to groups.
  - L5: 9.9 to SPARC.
  - With E: 15-17.
- **Reported variants:**
  - Lensing and groups dropped: L3 reads UNDETERMINED (LT\|S), L3+E NO COLLISION.
  - Υ at RS1's low reading: L3 is still NO-GO through L\|S (−0.254 ± 0.080). Point level reads NO-GO too, through one strong point collision:
    - SPARC IC2574's innermost point against LG field dwarf Pegasus dIrr.
    - Gap −0.67 ± 0.13 (Pegasus dIrr needs more), z 5.3, d_L 0.58.
    - A single innermost point; the ASSUMED × 2 check isn't run on this variant.
  - L5 point level at the low Υ reading is UNDETERMINED.
- **L5 grades only SPARC, X-COP and lensing.** The other lines are single-radius systems whose s is SY1's stand-in, so they are NOT GRADED in L5.

## The one line-level collision: lensing against SPARC (L3)

| | Pairs | Systems (L, S) | Intercept A−B (dex) | sd | Line | Robust to ASSUMED × 2 |
|---|---|---|---|---|---|---|
| L\|S, canonical | 46 | 3, 13 | **−0.234** | 0.071 (3.3σ) | 0.08 | yes |
| L\|S, alt | 46 | 3, 13 | −0.234 | 0.071 | 0.08 | yes |

The lensing rows need less boost than SPARC outer points at the same y, ell and f. The SPARC side is NGC5033, UGC05253, NGC6674, UGC06787, UGC03205, NGC2841 and others, at log y between −1.2 and −0.8, log ell about −5.95, f 0.13-0.31.

**Checked as hard as a win. These checks are POST-RESULT (`cx1_post.out`) and change no verdict:**
- **One radius carries it.** 45 of the 46 pairs use the innermost lensing radius, R = 35 kpc (bins 3 and 4: log B −0.21 and −0.19).
  - Dropping that radius: −0.048 ± 0.046, with one lensing system left. No collision.
  - At 35 kpc, a point-mass baryon model and the SIS conversion g = 4GΔΣ are at their weakest.
- **The 3-system minimum is met by a single pair.** Bin 2 contributes one pair. Dropping bin 2, 3 or 4 leaves two lensing systems, so the line can't read collision. The offset itself stays: −0.23, −0.20 and −0.35 respectively.
- **The bootstrap runs over 3 stacked bins,** so its sd is a weak estimate. The per-row lensing errors are the diagonal of the published covariance, not the full matrix.
- **The lensing line is PROVISIONAL and ASSUMED-GAS** (f = 0.2 ± 0.1, M* ± 0.15 dex assumed).
- The frozen conditional gap gives the same result: −0.223 ± 0.073 (3.0σ).

**Reading.** By the frozen rule, L3 reads NO-GO IN LEAF SPACE on both footings. It is not the wall the lane was opened for. It is a 0.2 dex tension between the innermost KiDS lensing radius and SPARC outer discs, carried by one radius of two stacks.

## The wall itself (X-COP, ultra-faint dwarfs, IC 1613): no gradable collision

| Line pair | Near pairs | Systems | Gap (dex) | Status |
|---|---|---|---|---|
| X-COP with anything | 0 | | | d_L ≥ 8.3 in L3, ≥ 9.9 in L5: **no neighbour** |
| Dw-UFD \| S (L3) | 6 | 6 UFDs, 1 galaxy (DDO064, innermost point) | +0.28 (UFDs need more) | not gradable: one SPARC system |
| IC1613 \| S (L3) | 3 | 1, 1 (F583-1, outer points) | −0.61 (IC 1613 needs less) | not gradable: one SPARC system; best point z 3.3 < z_LEE 4.69 |
| LT \| S (L3) | 12 | 5, 10 | −0.165 ± 0.171 | UNDETERMINED: above the line but not significant |
| Dw \| S (L3) | 34 | 17, 12 | +0.03 ± 0.15 | no collision |

**What this means for the record's wall:**
- **X-COP:** in these leaves, X-COP's need for more gravity is not a collision. Nothing measured sits at its (y, ell, f): it is about 8 or more error-units from every disc, group and lensing row. A rule can lift X-COP without touching any graded row near it. This is the "clusters are big" room BF1's near misses used. Gates fail elsewhere, through the form, not because the data contradict themselves.
- **UFDs and IC 1613:** they touch SPARC in L3 only through one galaxy each, DDO064 and F583-1. That is too thin to grade, so the record's opposite needs (UFDs more, IC 1613 less) can't be turned into a data-level no-go here.

## Strongest point collisions (L3, all rows, canonical; alt within 0.01)
No cross-line pair reaches z_LEE = 4.69, out of 18,493 near pairs. The three strongest:

1. **SPARC UGC02259 (r index 3) against LITTLE THINGS NGC 1569.**
   - log y −0.98/−1.03, log ell −6.91/−7.01, f 0.29/0.36, d_L 0.94.
   - log B +0.21 ± 0.17 against −0.57 ± 0.12; gap +0.79 ± 0.20, z 3.9.
2. **SPARC UGC07603 (7) against NGC 1569.** d_L 0.76, gap +0.77 ± 0.21, z 3.6.
3. **SPARC F583-1 (7) against IC 1613.**
   - log y −1.57/−1.41, log ell −7.16/−7.21, f 0/0, d_L 0.95.
   - log B +0.18 ± 0.20 against −0.54 ± 0.10; gap +0.72 ± 0.22, z 3.3.

There are 6 cross-line z ≥ 3 pairs, against a smooth-null 99th percentile of 1. There are 37 near cross-line pairs with a gap ≥ 0.3 dex below z_LEE, which is why point level reads UNDETERMINED.

Within SPARC, 3 strong within-line pairs: CamB–NGC3741, NGC2903–UGC09133 (innermost points), NGC2998–UGC09037. Reported only; they don't enter a verdict.

## Does the environment leaf remove them?
E = log M_basin, BS1's values.

| E value | Basin |
|---|---|
| 12.39 | Local Group: satellites, IC 1613, field dwarfs inside R0 |
| 14.7 | X-COP |
| 11.8-12.1 | Lensing bins |
| 12.0-12.6 | SPARC, from KT2017 groups |

- **E does not resolve L\|S.** In L3+E it still reads −0.255 ± 0.097 (2.6σ). The lensing bins (E 11.9-12.1) sit beside the SPARC galaxies they meet (NGC2841 12.1, UGC06787 11.9).
- **The label changes only because the pairs thin.** Bin 2's single pair falls out, leaving 2 lensing systems below the 3-system minimum.
- **E does separate the dwarfs.** UFDs and IC 1613 (12.39) move away from the low-E SPARC dwarfs: Dw-UFD\|S d_L 9.6, IC1613\|S 4.3. The near pairs go, along with the evidence.
- **Not computable:** E for 9 of 19 LITTLE THINGS galaxies and 2 SPARC galaxies (no basin in BS1).
- **Answer:** one more variable empties the neighbourhoods but doesn't reconcile the one tension that is measured.

## Controls, run and read before the real result (`cx1_controls.out`)

**K units against SY1's `build("real")` rows:**
- X-COP train, 20 rows: y within 9.4e-7 relative, ell exact, f within 3e-7, s within 3e-6.
- SPARC odd train, 1531 rows: exact.
- Law known answer: X-COP mean log B +0.4675 (record +0.4675); LITTLE THINGS median −0.0252 (record −0.0252).

**Smooth null, 20 seeds each, F1 = BF1's planted form, F2 linear in the arm's leaves:**

| | Seeds with a strong cross-line point | Seeds with a line collision |
|---|---|---|
| Every arm and footing | 0/20 | 0 or 1/20 (alt L3 F2, alt L3+E F1 and F2) |

Every cell is within the ≤ 1 rule.

**Planted class** (+δ on odd SPARC names):

| Arm | δ = 0.3, line level | δ = 1.0, strong points |
|---|---|---|
| L3 | −0.300 ± 0.012 | 4190 |
| L5 | −0.299 ± 0.043 | 79 |
| L3+E | −0.289 ± 0.014 | 1053 |
| L5+E | **not found** (14 near pairs; bootstrap fails) | 12 |

Because L5+E's line-level planted control fails, its line level reads UNDETERMINED, by the frozen rule. LT + 0.5 against S in L3 is recovered: +0.45 ± 0.06.

**MUTATE** (`cx1_MUTATE.out`), log B permuted across rows: the collision count changes. Within-line z ≥ 3 goes from 75 to 729 in L3. Bites.

## Departures, all disclosed
1. **AMENDMENT_A1, pre-result.** Smoke tests on synthetic data showed two frozen statistics flag smooth data:
   - The conditional gap was replaced by the marginal gap.
   - The line mean was replaced by a regression intercept.
   - F2 now uses only the arm's own leaves.
   - Invalid draws now include g_obs ≤ 0.

   Per-class medians of real log B were printed during the Monte Carlo check before A1; no real pair was computed.
2. **K units match, a bug in my check, fixed before the real run.** The first version matched SPARC rows by radius alone, which is ambiguous, and read a false deviation. It now matches by galaxy name; controls were rerun, and nothing else changed.
3. **L5+E line level** reads UNDETERMINED from its own failed planted control, as frozen.
4. **`cx1_post.py` is post-result.** It drops lensing radii and bins and changes no label.
5. **A cache file in another lane.** An early test import wrote `RS1_required_source/__pycache__/rs1_rows.cpython-313.pyc` (gitignored). I removed it; nothing else in another lane was written.
6. **Limits:**
   - Lensing errors use the diagonal of the covariance only.
   - Groups use one row with f 0.45 ± 0.15 in place of RS1's G3/G6 pair.
   - E for X-COP extrapolates the EM1 galaxy relation.
   - Single-radius systems use s = −2 stand-ins (excluded from L5).
   - Smoothness: a collision excludes only rules that change by less than the boost error across the pair's leaf-error ellipse.

κ = ½ FITTED. Not theory closed.
