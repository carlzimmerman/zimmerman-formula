# CFG521: CFG518's census placement in small boxes. NOT ACHIEVED: the galaxy regime is never the catchment majority. Every run lands in TENSION on a small-scale power deficit that the compensation rule causes; the census placement does not

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (841d4910c).
- **Engine:** `cfg521_pm.py`, a copy of `cfg518_pm.py`. It adds the box size `CFG521_L`, resolution r_ON ≥ 2 cells (`CFG521_RMIN` = 2L/256) and diagnostics. Nothing else changed.
- **Launcher:** `run_521.py` (detached with nohup; arrays and logs in `../_external_data/cfg521_work/`).
- **Verdict:** `cfg521_analysis.py` writes `cfg521_analysis.out` and `cfg521_results.json`. `CFG521_MUTATE=1` writes the `_MUTATE` versions.
- **Post-hoc, not gating:** `cfg521_posthoc.py` writes `cfg521_posthoc.out`.
- **Settings:** κ = ½ is FITTED. The footings (9.3603e-11 / 1.1312e-10) are never pooled, and a0 is flat. Nothing was downloaded. The cold energy's MASS is still required (no particle). This is not "theory closed".

## Setup

- **Grid:** 256³ particles and mesh, seed 359, NSEED 256.
- **Boxes:**
  - L = 50 Mpc/h is the primary box. Cell 0.195 Mpc/h; it resolves hosts down to log M_ta = 11.62 (about 650 particles).
  - L = 25 Mpc/h is the declared fallback. It resolves hosts down to log M_ta = 10.93.
  - L = 100 Mpc/h is reported only.
- **Reference:** every run is compared with a matched S0 (Newtonian) run in the same box, same seed and same resolution, made with the same engine.
- **Gate:** σ8 (box modes) and σ(4 Mpc/h) both within 5%, and max|P/P_S0 − 1| ≤ 0.10 over k ≤ k_Nyq/4. That limit is k ≤ 4.02 h/Mpc at L = 50 and k ≤ 8.04 at L = 25.

## Engine integrity (K0)

- At L = 200 and 128³, cfg521_pm.py reproduces cfg518_pm.py exactly: |dσ8| = 0 and max|dP/P| = 0 at every snapshot. That run had 1178 catchments active.
- cfg521's S0 at L = 200, 128³ also reproduces CFG359's S0 N128 exactly.

## Was the galaxy regime reached? (the frozen achievement test)

The test asks for a catchment mass-weighted mean f_ret ≤ 0.20 at z = 0. Neither scored box meets it.

| box | mean f_ret in catchments, z = 1 / 0.5 / 0 | catchment mass with f_ret ≤ 0.2 (z = 0) | f_ret weighted by phantom excess (z = 0) | achieved? |
|---|---|---|---|---|
| L = 100 | 0.448 / 0.521 / 0.592 | 0.140 | 0.844 | (reported) |
| L = 50 | 0.381 / 0.465 / **0.535** | 0.198 | 0.789 | **NO** |
| L = 25 | 0.311 / 0.392 / **0.466** | 0.336 | 0.657 | **NO** |

- **Galaxy hosts are resolved, but they are not the catchment majority.**
  - At L = 50 there are about 1600 resolved peaks with log M_ta 11.6–12.4.
  - Catchments (turnaround balls, the largest host wins) hold 61% of the box mass in 7% of the volume.
  - 54% of that catchment mass sits in group-scale balls with f_ret ≥ 0.55. Galaxy turnaround regions are embedded in groups.
  - The phantom excess is even more group-dominated, as the excess-weighted f_ret of 0.66–0.79 shows.
- Shrinking the box from 50 to 25 Mpc/h lowers the mean only from 0.535 to 0.466.

**Frozen verdict: NOT ACHIEVED.** No galaxy-regime growth verdict is issued, and 512³ stays PENDING (not run).

## Growth numbers (z = 0, against the matched S0; reported because the regime was not reached)

| box / run | σ8 ratio | σ(4) ratio | max\|P−1\| (k ≤ k_Nyq/4) | max\|P−1\| (k ≤ 1) | P/P_S0 at 0.3 / 1 / 3 | category |
|---|---|---|---|---|---|---|
| L50 census, canonical | 1.0138 | 1.0187 | 0.372 (k 3.65) | 0.087 | 1.041 / 1.024 / 0.677 | TENSION |
| L50 census, alt | 1.0149 | 1.0224 | 0.379 | 0.102 | 1.044 / 1.046 / 0.672 | TENSION |
| L50 MUTATE (no compensation) | 1.0761 | 1.0967 | 0.308 (k 0.89) | 0.308 | 1.206 / 1.308 / 0.943 | TENSION |
| L50 K1 (f_ret = 1) | 1.0118 | 1.0184 | 0.358 | 0.091 | 1.037 / 1.048 / 0.685 | TENSION |
| L25 census, canonical | 1.0156 | 1.0297 | 0.550 (k 7.8) | 0.122 | 1.033 / 1.077 / 0.685 | TENSION |
| L25 census, alt | 1.0169 | 1.0341 | 0.574 | 0.138 | 1.036 / 1.091 / 0.682 | TENSION |
| L25 MUTATE | 1.0776 | 1.1185 | 0.586 | 0.452 | 1.165 / 1.370 / 1.394 | TENSION |
| L25 K1 (f_ret = 1) | 1.0135 | 1.0307 | 0.594 | 0.119 | 1.028 / 1.086 / 0.687 | TENSION |
| L100 census, canonical | 1.0099 | 1.0141 | 0.152 (k 1.95) | 0.056 | 1.040 / 0.985 / – | TENSION |

**Diagnostics:**
- No overdraw, and the cap never acted.
- q_max is 0.43 / 0.50 (L50 canonical / alt) and 0.54 / 0.58 (L25).
- The total phantom excess, census over K1, is 0.89 / 0.88 / 0.99 at z = 1 / 0.5 / 0 for L50, and 0.68 / 0.77 / 0.88 for L25.

## What it means

1. **The question cannot be answered with this rule in a periodic box.** The census paints f_ret per turnaround ball with the largest host winning. Galaxies sit inside group turnaround regions, so even a 25 Mpc/h box gives a catchment mean f_ret of about 0.47. A test of the "f_ret ≈ 0.1" placement would need:
   - an isolated-galaxy (field) set-up, or
   - a per-galaxy f_ret that is not overwritten by the enclosing group.

   Either one is a new rule, not CFG518's.
2. **Large scales are fine in every box.** σ8 and σ(4) stay within 1–3.5%, and P/P_S0 at k ≤ 1 is within 0.06–0.14 for census and K1. MUTATE is clearly worse at k ≈ 1 (0.31 / 0.45), so the compensation still does its large-scale job.
3. **Small scales fail, and the census placement is not the cause.**
   - **The deficit.** Once host interiors are resolved, P/P_S0 drops well below 1 at k ≳ 2: 0.63 at k = 4 for L50, 0.44 at k = 8 for L25.
   - **K1 (f_ret = 1) shows the same deficit** (0.632 / 0.397), so the cause is CFG424's per-catchment compensation, not the census placement.
   - **The mechanism.** The compensation q·s_c is drawn in proportion to local density, so it takes most from host cores. The excess e is added where s_ph > s_c, in the low-density outskirts. Halos therefore become less concentrated.
   - **Evidence.** MUTATE (no compensation) stays at 0.89–0.94 at k = 3–8 (L50), and the deficit grows with time (k = 4: 0.90 at z = 1, 0.76 at z = 0.5, 0.63 at z = 0; `cfg521_posthoc.out`).
   - **It is not converged.** It deepens as the cells shrink: at k ≈ 4 it is 0.89 at L200 (CFG518, beyond its k ≤ 1 cut), 0.80 at L100, 0.63 at L50 and 0.59 at L25.
   - **Consequence for CFG518.** CFG518's PASS / CONFIRMED holds only at k ≤ 1 h/Mpc. Its own 256³ run already had P/P_S0 = 0.89 at k = 3–4 (K1: 0.91–0.93), outside its frozen cut.
4. **MUTATE is not GROWTH OK in any box**, so the decision rule keeps its teeth. Over the full declared k range, though, it does not separate from the census runs, because both are TENSION for different reasons. They separate only at k ≤ 1 (0.31 vs 0.09 at L50).

## Departures and notes (dated)

- **2026-10-09.** The L = 25 fallback was launched as soon as L = 50 failed the achievement test, as the frozen rule says. The L = 100 secondary (S0 + census canonical) was also run.
- **2026-10-09.** The post-hoc file `cfg521_posthoc.out` covers three things, none of them gating:
  - P ratios out to k = 8, including CFG518's L = 200 runs beyond its cut;
  - the z-growth of the deficit;
  - a recount of the catchment-mass breakdown with the engine's own in_cover, which matches the engine's diagnostic (0.535).
- "Resolved host" counts are counts of resolved density peaks. Many peaks share one large region, so they are not distinct halos.

## Caveats

- One seed at 256³. Small boxes lack modes with k < 2π/L. The S0 box σ8 is 0.80 / 0.63 / 0.86 at L = 50 / 25 / 100. Only ratios to the matched S0 are scored.
- PM forces are softened below about one cell. The small-scale deficit is not resolution-converged, so its size at the true galaxy scale is unknown. Its sign and its growth with resolution are robust across L200 → L25.
- fret_of below 10^12.5 is CFG416's constant 0.10. The expelled baryons stay as gravitating mass, as in CFG518.
- κ, f_b and ρ_Λ are not derived. The cold energy's mass is still required.

## Compute

- 15 runs at 256³ (plus two at 128³), 6 threads each under nice 10, two at a time.
- S0 runs took about 7–8 min. RES runs took about 10–17 min on a loaded 16-core machine.
- No 512³ run was made.

## Run

```
nohup python3 campaign_fresh_gravity/CFG521_small_box_galaxy_regime/run_521.py k0 50a 50b 50c k0s &
nohup python3 campaign_fresh_gravity/CFG521_small_box_galaxy_regime/run_521.py 25a 25b 25c 100 &
python3 campaign_fresh_gravity/CFG521_small_box_galaxy_regime/cfg521_analysis.py
CFG521_MUTATE=1 python3 campaign_fresh_gravity/CFG521_small_box_galaxy_regime/cfg521_analysis.py
python3 campaign_fresh_gravity/CFG521_small_box_galaxy_regime/cfg521_posthoc.py
```
