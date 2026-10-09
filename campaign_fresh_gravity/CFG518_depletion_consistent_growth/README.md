# CFG518: growth with the depletion-consistent (census) placement of cold energy. PASS at 256³ on both footings; CONFIRMED at 512³ (canonical)

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (9014750d1).
- **Engine:** `cfg518_pm.py`, a copy of CFG424's `cfg424_pm.py` (RC = 0). The changes are listed in full in the criteria.
- **Launcher:** `run_518.py` (detached with nohup; logs in `../_external_data/cfg518_work/`).
- **Verdict:** `cfg518_analysis.py` writes `cfg518_analysis.out` and `cfg518_results.json`. `CFG518_MUTATE=1` writes the `_MUTATE` versions.
- **Settings:** κ = ½ is FITTED. The footings (9.3603e-11 / 1.1312e-10) are never pooled, and a0 is flat. Nothing was downloaded. The cold energy's MASS is still required (no particle). This is not "theory closed".

## The question

This is the run CFG515 specified. CFG424/425 passed growth with f_ret = 1: the phantom is sourced by all PM baryons and stops at the f_ret = 1 edge. Real galaxies need the census f_ret, which puts the edge 2.2–3.5× farther out. CFG515 showed the settled amount is the same but the placement is not. Does growth still pass with the placement that is consistent with depletion?

## What changed in the engine

1. **f_ret per host.** Each resolved host gets CFG416's `fret_of(M_ta)` from its own PM turnaround mass. This is painted over its turnaround ball; the largest host wins overlaps, and f_ret = 1 outside the catchments.
2. **Phantom source.** The MOND input is the retained baryons f_ret(x)(1 + δ). Only that part sources the phantom.
3. **Expelled baryons (declared).** They stay as gravitating mass where the particles are. The Newtonian potential still uses the full δ, so nothing is removed or moved.
4. **Edge.** The census edge is r_M(M_b,now)/ln(1 + f_ret f_b/(1 − f_b)), capped at r_ta.
5. **Unchanged from CFG424.** Per-catchment mass conservation is kept.
6. **Cap.** Added: on a catchment with q > 1, e is scaled by 1/q. It never acted.

## Results (256³, seed 359, vs CFG359 S0 N256, CFG361 cuts)

| run | σ₈ ratio | max\|P−1\| (k ≤ 1) | P/P_S0 at 0.1 / 0.3 / 1 | verdict |
|---|---|---|---|---|
| DC-can (census) | 1.0028 | **0.023** | 1.001 / 1.011 / 0.993 | GROWTH OK |
| DC-alt (census) | 1.0036 | **0.030** | 1.002 / 1.013 / 1.004 | GROWTH OK |
| MUTATE (census, no compensation) | 1.0292 | 0.139 | 1.035 / 1.081 / 1.106 | TENSION (the control works) |
| K1 (f_ret = 1, new code path) | 1.0033 | 0.0273 | 1.001 / 1.012 / 1.004 | GROWTH OK |

**Diagnostics:**
- q_max is 0.294 (can) and 0.276 (alt), against 0.302 at f_ret = 1.
- There is no overdraw, and the cap never acted.
- **K1 control.** K1 reproduces CFG424 TA-can to 9e-9 in max|P−1| and 1e-9 in the σ₈ ratio, so the engine change is clean.
- **MUTATE analysis** (`_MUTATE.out`). With the no-compensation run in the DC-can slot, the lane drops to PARTIAL, so the decision rule has teeth.

**512³ canonical** (seed 359, NSEED 512, against CFG411's 512³ S0):

| run | σ₈ ratio | max\|P−1\| (k ≤ 1) | P/P_S0 at 0.1 / 0.3 / 1 | verdict |
|---|---|---|---|---|
| DC-can 512³ (census) | 1.0047 | **0.0285** | 1.004 / 1.019 / 0.981 | GROWTH OK |

- The f_ret = 1 run at 512³ (CFG425 R3) gave 0.033.
- q_max is 0.49. There is no overdraw, and the cap never acted.
- The mass-weighted mean f_ret in the catchments is 0.70 at z = 0, with a minimum of 0.43.

**Frozen verdict: PASS (256³), CONFIRMED (512³).**

## What it means

- **Growth is not hurt by the census placement.** The excess goes 0.027 → 0.023 (canonical) and 0.029 → 0.030 (alt) at 256³, and 0.033 → 0.0285 at 512³.
- **The result sits at the bottom of CFG515's argued bracket (0.027 to 0.08–0.10), not in the middle.** Two things keep it there:
  - The per-catchment compensation still removes the large-scale source.
  - The retained-baryon phantom is smaller. The total excess Σe, relative to f_ret = 1, is 0.99 at z = 1, 0.83 at z = 0.5 and 0.71 at z = 0.
  - The farther edge therefore does not add net source.
- **The main limit: the PM's hosts are groups, not galaxies.**
  - The hosts the PM resolves have r_ON ≥ 1.56 Mpc/h.
  - Their census f_ret runs from 0.44 to 0.90. The mass-weighted mean in the catchments is 0.72 at z = 0.
  - So this run tests the census placement for groups and clusters. It does not test the f_ret ≈ 0.10 regime of KiDS lenses and the MW, where the edge moves 2.9× out.
  - The 200 Mpc/h box cannot resolve those hosts. A galaxy-scale test needs a smaller box or a finer mesh.

## Caveats

- One seed at 256³. The 512³ run is canonical only.
- The expelled baryons are a declared bookkeeping choice: they stay as gravitating mass where they are. No outflow is modelled.
- The cold energy is bookkeeping, not moved particle by particle.
- The census relation is CFG416's declared step-and-ramp, applied at every z with the host's current M_ta.
- κ, f_b and ρ_Λ are not derived.

## Compute

- **256³:** four runs at 4 threads each under nice 10, two at a time. Each took about 38 min on a loaded 16-core machine (2.3 ks per run).
- **512³:** one run at 8 threads. It took 33.1 ks wall time (about 9.2 h) on a heavily loaded machine, with about 1.2 cores used on average and a peak RSS of about 21 GB.

## Run

```
nohup python3 campaign_fresh_gravity/CFG518_depletion_consistent_growth/run_518.py &        # 256^3: DC-can+DC-alt, then MUTATE+K1
nohup python3 campaign_fresh_gravity/CFG518_depletion_consistent_growth/run_518.py 512 &    # 512^3 DC-can (only if no other 512^3 job)
python3 campaign_fresh_gravity/CFG518_depletion_consistent_growth/cfg518_analysis.py
CFG518_MUTATE=1 python3 campaign_fresh_gravity/CFG518_depletion_consistent_growth/cfg518_analysis.py
```
