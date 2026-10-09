# CFG524: draw the compensation only from the unsettled cold-energy reservoir. FAIL for both draw rules: the small-scale deficit stays, and the draw becomes more core-weighted, not less

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (ef4515556).
- **Engine:** `cfg524_pm.py`, a copy of `cfg521_pm.py`. The only change is the draw weight: `CFG524_DRAW` = R2 | R1 | SC. Diagnostics were also added; they have no effect on the dynamics.
- **Launcher:** `run_524.py` (nohup; claim-based workers; arrays and logs in `../_external_data/cfg524_work/`).
- **Verdict:** `cfg524_analysis.py` writes `cfg524_analysis.out` and `cfg524_results.json`.
- **Concentration (declared, not gating):** `cfg524_posthoc.py` writes `cfg524_posthoc.out` and `.json`.
- **Settings:**
  - κ = ½ is FITTED. The footings (9.3603e-11 / 1.1312e-10) are never pooled, and a0 is flat.
  - The cold energy's MASS is still required.
  - This is not "theory closed".

## The reservoir used (from the code)

The engine has no separate cold component. The cold-energy density is the fixed f_b split of the PM matter field: s_c = 1.5 Ω_m (1 − f_b)(1 + δ)/a. The phantom source is s_ph = −∇·[(ν − 1) g_b,ret].

The engine's own excess is e = f_sw max(s_ph − s_c, 0), so the switched-on phantom that the local cold share already carries is f_sw·clip(s_ph, 0, s_c). Per cell:

- **R2 (literal):** Rv = s_c − f_sw·clip(s_ph, 0, s_c)
- **R1 (switch-free alternative):** Rv = s_c − clip(s_ph, 0, s_c)

The draw is comp = q·Rv with q = Σ_C e / Σ_C Rv per catchment. Per-catchment conservation is unchanged, and so is the cap (q > 1 → e/q, the whole reservoir is drawn).

Why each part is forced:
- s_c is the only cold field the engine has.
- The clips at 0 and s_c are forced: a negative phantom source is not settled cold energy, and the settled amount cannot exceed the cold energy present.
- The f_sw weight on the settled part is not forced, so both R2 and R1 were run, and neither was picked.
- Everything else is CFG518/521.

## Engine integrity

- **MUTATE (draw = s_c) reproduces CFG521's DC-can exactly** at L = 50 and L = 25: |dσ8| = 0 and max|dP/P| = 0 at every snapshot.
- MUTATE is TENSION in both boxes, so it shows the deficit and the gate keeps its teeth.
- The S0 controls are reused from CFG521 (L = 50/25/100) and CFG359 (L = 200). Their sha256 hashes and config fields are in `cfg524_analysis.out`.

## Results (256³, seed 359, z = 0, vs matched S0)

| box | run | σ8 | σ(4) | max\|P−1\| (gate range) | k ≤ 1 | P/P_S0 at k = 4 | verdict | q_max | cap |
|---|---|---|---|---|---|---|---|---|---|
| L50 | R2-can | 1.021 | 1.035 | 0.336 | 0.135 | 0.660 | TENSION | 1.02 | 1 catchment |
| L50 | R2-alt | 1.023 | 1.042 | 0.298 | 0.159 | 0.697 | TENSION | 1.04 | 1 |
| L50 | R1-can | 1.023 | 1.030 | 0.378 | 0.116 | 0.619 | TENSION | 2.83 | 4 (57% of e removed there) |
| L50 | R1-alt | 1.025 | 1.036 | 0.337 | 0.134 | 0.662 | TENSION | 2.88 | 3 |
| L50 | K1 (f_ret = 1, R2) | 1.018 | 1.037 | 0.282 | 0.151 | 0.703 | TENSION | 1.01 | 1 |
| L50 | MUTATE (old draw) | 1.014 | 1.019 | 0.372 | 0.087 | 0.628 | TENSION | 0.43 | none |
| L25 | R2-can | 1.026 | 1.052 | 0.509 | 0.218 | 0.702 (k = 8: 0.466) | TENSION | 1.34 | 1 |
| L25 | R2-alt | 1.028 | 1.060 | 0.447 | 0.249 | 0.785 | TENSION | 1.61 | 2 |
| L25 | R1-can | 1.027 | 1.053 | 0.524 | 0.217 | 0.668 | TENSION | 3.08 | 2 |
| L25 | R1-alt | 1.031 | 1.060 | 0.461 | 0.247 | 0.754 | TENSION | 3.33 | 2 |
| L25 | K1 (R2) | 1.022 | 1.056 | 0.443 | 0.226 | 0.833 | TENSION | 1.48 | 2 |
| L25 | MUTATE (old draw) | 1.016 | 1.030 | 0.550 | 0.122 | 0.585 (k = 8: 0.436) | TENSION | 0.54 | none |
| L200 | R2-can | 1.005 | – | – | 0.047 | 0.930 | GROWTH OK | 0.68 | none |
| L200 | R2-alt | 1.006 | – | – | 0.055 | 0.950 | GROWTH OK | 0.70 | none |
| L200 | R1-can | 1.003 | – | – | 0.020 | 0.886 | GROWTH OK | ≈1e32 | 688 catchments, 52% of e removed |
| L200 | R1-alt | 1.004 | – | – | 0.025 | 0.924 | GROWTH OK | ≈2e32 | 959, 67% removed |
| L100 | R2-can (reported) | 1.014 | 1.026 | 0.091 | 0.091 | 0.853 | (GROWTH OK) | 0.95 | none |
| L100 | R1-can (reported) | 1.013 | 1.017 | 0.189 | 0.074 | 0.747 | (TENSION) | 30.8 | 25 |

**Frozen verdicts:**
- **R2: FAIL.** None of the four small-box runs is GROWTH OK.
- **R1: FAIL.** None of the four small-box runs is GROWTH OK.
- **512³: not run.** No rule passed at 256³.

**Convergence trend of P/P_S0 at k = 4** (L = 200 / 100 / 50 / 25):

| draw | L = 200 | L = 100 | L = 50 | L = 25 |
|---|---|---|---|---|
| old draw | 0.893 | 0.804 | 0.628 | 0.585 |
| R2-can | 0.930 | 0.853 | 0.660 | 0.702 |
| R1-can | 0.886 | 0.747 | 0.619 | 0.668 |

- The deficit still deepens with resolution under both rules.
- At L50 it still grows with time (R2-can: 0.90 / 0.79 / 0.66 at z = 1 / 0.5 / 0).

**Halo concentration** (median M(<2 cells)/M(<8 cells) over the 100 top peaks, run / S0):

| box | old draw | NOCOMP | R2-can / R2-alt | R1-can / R1-alt | K1 |
|---|---|---|---|---|---|
| L50 | 0.86 | 0.95 | 0.78 / 0.87 | 0.81 / 0.84 | 0.96 |
| L25 | 0.77 | 1.00 | 0.74 / 0.68 | 0.67 / 0.68 | 0.85 |
| L200 | 1.04 | – | 1.05 / 1.06 | 1.00 / 1.05 | – |

The halos are no more concentrated than with the old draw.

## What it means (verified as hard as a pass would be)

1. **CFG521's premise does not hold in this engine.** CFG521 assumed the old draw takes cold energy that had already settled in the cores. By the engine's own bookkeeping, though, settled phantom sits where s_ph is comparable to or above s_c, which is the low-acceleration outskirts. Halo cores are Newtonian (s_ph ≪ s_c), so almost all of their cold share counts as unsettled reservoir.
   - Removing the settled part therefore takes the draw out of the outskirts and concentrates it further in the cores.
   - The draw-weighted mean density rises above the s_c-weighted one:
     - L50 R2: 325 vs 289;
     - L25 R2: 438 vs 361;
     - R1: 734–1002 vs 270–390. R1 removes settled cold energy even where the switch is off.
   - The old draw at L50 sits at 342 vs 282, so R2 is not less core-weighted in absolute terms.
2. **The fix does not remove the deficit.**
   - At k = 4, R2 recovers a few percent: 0.63 → 0.66 at L50 and 0.585 → 0.70 at L25.
   - It makes k ≤ 1 worse: 0.087 → 0.135 at L50 and 0.12 → 0.22 at L25.
   - At L25, k = 8 is unchanged (0.436 → 0.466).
3. **R1 is degenerate.**
   - In many catchments almost all cold energy is "settled", so the reservoir is close to zero and q blows up (q_max ≈ 1e32 at L200).
   - The cap then deletes 50–68% of the excess in those catchments. Its L200 GROWTH OK comes from removing source, not from a better draw.
4. **L200 (k ≤ 1) still passes for both rules.** R2's k ≤ 1 deviation is 0.047/0.055, against CFG518's 0.023/0.030. That cut does not see the problem.
5. **The deficit is caused by the draw itself, not by its weighting within the reservoir.**
   - NOCOMP (no draw) keeps the halos at 0.95–1.00 of S0.
   - Every per-catchment draw tried so far (s_c, R2, R1) de-concentrates them.
   - A draw that does not de-concentrate would have to be co-located with e, which is close to no draw at all, or would need a different conservation statement. Either would be a new rule, not something these quantities force. It is not proposed here.

## Departures and notes (dated)

- **2026-10-09 12:39 — operational re-queue (owner request via the coordinator; not a departure from the frozen criteria).**
  - The two sequential launchers were stopped after four jobs. MUTATE_L50 and R2can_L50 were done; R2alt_L50 and R1can_L50 ran to completion.
  - The remaining 14 jobs went to 4 parallel workers, at most 4 runs at once (about 8 GB each), with atomic claims so that no job ran twice.
  - Per-run threads went from 8 to 4. The thread count does not change results: the 8-thread L50 and 4-thread L25 MUTATE runs both reproduce CFG521's 6-thread runs exactly.
  - Same env and nice 10. The CFG468 grid was untouched.
- **2026-10-09 — smoke test before the main runs.** At 64³, one SC run differed from the cfg521 reference by 5e-8 at z = 0 only, while a repeat matched exactly. This shows rare run-to-run jitter at the 1e-8 level. Both 256³ MUTATE reproductions were exact, so the frozen 1e-8 rule was not affected.
- R1's L200 q_max values (about 1e32) come from catchments whose reservoir is about 0. They are reported as computed.

## Caveats

- One seed at 256³. Small boxes lack modes with k < 2π/L, so only ratios to the matched S0 are scored.
- PM forces are softened below about one cell.
- The concentration statistic is cell-based and not gating.
- CFG521's census painting (group f_ret over embedded galaxies) is unchanged.
- κ, f_b and ρ_Λ are not derived. The cold energy MASS is still required.

## Run

```
nohup python3 campaign_fresh_gravity/CFG524_reservoir_only_draw/run_524.py <jobs...> &     # several launchers may share one list
python3 campaign_fresh_gravity/CFG524_reservoir_only_draw/cfg524_analysis.py
python3 campaign_fresh_gravity/CFG524_reservoir_only_draw/cfg524_posthoc.py
```
