# CFG530: fixed-box resolution study of the CFG527 engine. P(k) converges at fixed box; the law ratio does not (canonical); L200 512^3 growth is TENSION on both footings

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (194cb6560).
- **Engine:** CFG527's `cfg527_pm.py`, imported unchanged. Its sha256 (aeabd0ba…) is checked before every job, and only its output folder is redirected.
- **Launcher:** `run_530.py`. It runs a claim-based queue with 4 workers at 4 threads each for jobs up to 256^3, then the 512^3 jobs alone at 8 threads, one at a time, all at nice 10.
- **Scripts:**
  - `cfg530_profiles.py`: the CFG526 law statistic, imported with the declared changes only.
  - `cfg530_analysis.py`: all verdicts.
  - `cfg530_s0reuse.py`: the S0 512^3 reuse check.
  - `cfg530_posthoc.py`: a matched-mass check, reported only.
- **Arrays and logs:** `../_external_data/cfg530_work/`.
- **Settings:**
  - κ = ½ is FITTED.
  - Footings 9.3603e-11 and 1.1312e-10 are judged separately, never pooled.
  - a0 is flat; ν_mono; seed 359.
  - NSEED = 512 at every N, so every N sees the same realization.
  - RMIN is fixed in physical units per box: 0.78125 at L100 and 1.56 at L200.
- The cold energy's MASS is still required. Not "theory closed". Nothing was downloaded.

## Controls (all pass)

| control | result |
|---|---|
| REP: CFG527 L100 and L200 256^3 reproduced, both footings | \|dσ8\|/σ8 = 0 and max\|dP/P\| = 0 at every snapshot |
| Law-statistic identity: patched CFG526 on CFG527's caches | core R reproduced exactly (difference 0) |
| S0 512^3 reuse (CFG411 S0 N512) | S0 code path identical; zi snapshot exact (0 difference); z0 P re-measured from the saved positions to 3e-8 |
| MUTATE: CFG521 old draw (SC + MIX-A), L100 N256 | core R 0.746, NOT law-consistent, so the statistic has teeth |
| Stability: all 16 NOFILT runs | finite; P/P_S0 at k_Nyq/2 ≤ 2 |

## 1. Fixed-box resolution convergence (N256 vs N512)

Tolerances: |Δr| ≤ 0.05 at resolved k, and |Δ log core R| ≤ 0.05 dex. Values are from `cfg530_results.json`.

| footing | box | r(k=1), N128 / 256 / 512 | r(k=2), N256 / 512 | r(k=4), N512 only | core R, N256 → N512 (Δ dex) | verdict |
|---|---|---|---|---|---|---|
| canonical | L100 | 1.064 / 1.146 / 1.132 | 1.023 / 1.027 | 0.952 | 0.968 → 1.128 (+0.066) | **NOT CONVERGED** (core R) |
| canonical | L200 | – / 1.070 / 1.100 | – / 0.990 | – | 0.973 → 1.142 (+0.070) | **NOT CONVERGED** (core R) |
| alt | L100 | 1.071 / 1.143 / 1.150 | 1.018 / 1.036 | 0.958 | 0.961 → 1.042 (+0.035) | CONVERGED |
| alt | L200 | – / 1.073 / 1.107 | – / 0.987 | – | 0.966 → 1.060 (+0.040) | CONVERGED |

**Frozen verdicts:** canonical **NOT CONVERGED**; alt **CONVERGED**.

**The power spectrum converges on both footings.**
- Every resolved P-ratio item moves by at most 0.037 between N256 and N512.
- At fixed L = 100, r(k = 2) stays at 1.02–1.04. CFG527 found r(k = 2) = 1.37–1.43 at L25.
- k = 4 is resolved only at N512 in the L100 box (0.95), so it is reported and not judged.

**The law ratio moves on both footings.** Halo cores go from slightly under the law to over it at N512:
- canonical core R is 1.13–1.14 at N512;
- alt core R is 1.04–1.06 at N512.

Alt passes only because its shift (+0.035 / +0.040 dex) is under the 0.05 dex tolerance, and it moves in the same direction as canonical. Every N512 core R is still within CFG526's 0.1 dex law tolerance.

**Matched mass (post-hoc, `cfg530_posthoc.out`).** Restricting to the common log M_ta window, core R still rises by +0.076 / +0.081 dex (canonical, L200 / L100) and +0.084 / +0.044 dex (alt). The rise is therefore not a change in which hosts are sampled.

## 2. Box-size effect at matched cell size and RMIN

| footing | P1: BX L100/N128 vs L200/N256 | P2: BX L100/N256 vs L200/N512 | verdict |
|---|---|---|---|
| canonical | r(1): 1.058 vs 1.070 | r(1): 1.105 vs 1.100; r(2): 1.000 vs 0.990; core R: 0.969 vs 1.142 (−0.071 dex) | **YES** (core R only) |
| alt | r(1): 1.056 vs 1.073 | r(1): 1.103 vs 1.107; r(2): 1.001 vs 0.987; core R: 0.962 vs 1.060 (−0.042 dex) | **NO** |

- The realization floor F compares NSEED 256 with NSEED 512 at N256 in the same box:

  | item | canonical | alt |
  |---|---|---|
  | r(k=1) | 0.061 | 0.082 |
  | r(k=2) | 0.024 | 0.063 |
  | core R | 0.002 dex | 0.002 dex |

- **Power spectrum.** At matched cell size, L100 and L200 agree to 0.018 or better on r(k ≤ 2) on both footings. On P(k) there is no box-size effect between 100 and 200 Mpc/h.
- **Canonical YES.** It comes from core R alone and survives the matched-mass window (0.987 vs 1.141, +0.063 dex). At matched dx and RMIN, the L200/N512 cores sit above the law and the L100/N256 cores do not.
- **What core R tracks.** Across these runs core R follows N more than dx: L100/N512 is 1.128 and L200/N512 is 1.142, against 0.97 for every N256 run. **The mechanism is not identified (2026-10-10).** It is not:
  - host mass;
  - percolation (no catchment spans the box; the largest catchment holds ≤ 0.15 of catchment mass);
  - an empty shell (none in any run).
- The L50/L25 boxes were not re-run, so whether CFG527's L25 k = 2 excess is purely a box effect is shown here only indirectly: k = 2 converges at fixed L100 and agrees between L100 and L200.

## 3. Growth gate: L200 512^3 (CFG361 cuts at z = 0, k ≤ 1, against S0 N512)

| footing | σ8 ratio | max\|P/P_S0 − 1\|, k ≤ 1 | verdict |
|---|---|---|---|
| canonical | 1.0101 | 0.113 at k = 0.69 | **TENSION**, so CFG527's 256^3 GROWTH OK is **NOT CONFIRMED** |
| alt | 1.0101 | 0.121 at k = 0.82 | **TENSION**, NOT CONFIRMED |

I checked the fail as hard as a pass would be checked:
- The S0 is verified (exact ICs, identical code path), and the realization is the same as the N256 study run.
- At N256 with NSEED 512 the same box gives 0.080 / 0.086 (GROWTH OK). The excess over k = 0.4–1.0 grows from N256 to N512, for example r(0.69) goes from 1.077 to 1.113 (canonical).
- It also grows with time: canonical max|P − 1| is 0.036 at z = 1, 0.071 at z = 0.5 and 0.113 at z = 0.
- It grows in step with the cap: cap mass share 0.06 → 0.45 → 0.41 and Σe removed 0.006 → 0.094 → 0.194 at z = 1 → 0.5 → 0. At 256^3 the cap reached only 3% of mass.
- CFG527 anticipated this: finer resolution pushes L200 into the rule's capped regime.

## 3b. Cap use and percolation against N and L

Values are the maximum over snapshots, from `cfg530_results.json` and `cfg530_profiles.json`.

| run | q_max | cap mass share | Σe removed | largest catchment's share of catchment mass | spanning |
|---|---|---|---|---|---|
| LR L100 N128 / 256 / 512 (canonical) | 0.89 / 1.85 / 3.23 | 0 / 0.22 / 0.71 | 0 / 0.15 / 0.52 | 0.08 / 0.08 / 0.15 | no |
| LR L200 N128 / 256 / 512 (canonical) | 1.89 / 1.16 / 2.36 | 0.01 / 0.03 / 0.45 | 0.003 / 0.004 / 0.19 | 0.03 / 0.03 / 0.04 | no |
| LR L100 N512 / L200 N512 (alt) | 2.90 / 2.57 | 0.73 / 0.37 | 0.48 / 0.17 | 0.15 / 0.04 | no |
| BX L100 N128 / 256 (canonical) | 0.83 / 1.68 | 0 / 0.44 | 0 / 0.12 | 0.10 / 0.12 | no |

- **Cap use is driven by resolution, not by percolation.** At L100 and L200 no catchment spans the box at any N, yet the cap's reach grows steeply with N in both boxes.
- **What the cap does at higher N.** It is the same capped regime CFG527 saw in L50/L25. Higher resolution makes cores denser, q > 1 in more catchments, and the whole shell cold share is drawn.

## Departures and notes (dated)

- **2026-10-09, CFG526 integrity K1.** It fails on the same float32 round-off keys CFG527 disclosed, in LRcan/LRalt L100 N128, BXcan L100 N128 and MUTA L100 N256:
  - `cap_e_removed_frac`, about 1e-7 in absolute terms when the cap is inactive;
  - `src_sum`, a float32 sum of a zero-mean field.
  The frozen keys pass: e_sum ≤ 1.3e-7, q_max ≤ 7e-7, n_catch exact. K is not part of this lane's verdicts.
- **2026-10-09, profile pass alongside a 512^3 job.** The 512^3 law-profile pass (analysis, not a simulation) ran alongside the S0 L100 512^3 job, and free memory dipped to 36%. The other 512^3 profiles ran after all simulations had finished. No simulation overlapped another 512^3 simulation.
- **2026-10-09, post-hoc script added.** `cfg530_posthoc.py` was added after the first 512^3 profile, to test a host-mass explanation of the core R shift. It is reported only.
- **2026-10-09, launcher edit.** `run_530.py` was edited while the queue workers were running: the serial launcher also waits for queue workers. The job logic did not change.
- **2026-10-09, N128.** At N128 fewer than 20 halos are scored in several runs, so core R is not evaluable there. The verdicts use N256 vs N512, as frozen.

## Caveats

- One realization per (L, NSEED). Cores are 1–2 cells, so core R at different N is measured at different physical radii.
- The 150-step time grid is fixed at every N.
- The draw is bookkeeping of the cold share s_c. The cold energy's mass is still required.
- κ, f_b and ρ_Λ are not derived. Not "theory closed".

## Run

```
nohup python3 campaign_fresh_gravity/CFG530_fixed_box_convergence/run_530.py queue <21 jobs> &          # x4
nohup python3 campaign_fresh_gravity/CFG530_fixed_box_convergence/run_530.py serial LRcan_L200_N512 S0_L100_N512 LRcan_L100_N512 LRalt_L200_N512 LRalt_L100_N512 &
python3 campaign_fresh_gravity/CFG530_fixed_box_convergence/cfg530_s0reuse.py
python3 campaign_fresh_gravity/CFG530_fixed_box_convergence/cfg530_profiles.py identity
nice -n 10 python3 campaign_fresh_gravity/CFG530_fixed_box_convergence/cfg530_profiles.py compute
python3 campaign_fresh_gravity/CFG530_fixed_box_convergence/cfg530_profiles.py
python3 campaign_fresh_gravity/CFG530_fixed_box_convergence/cfg530_analysis.py
python3 campaign_fresh_gravity/CFG530_fixed_box_convergence/cfg530_posthoc.py
```
