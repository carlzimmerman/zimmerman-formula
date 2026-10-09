# CFG527: law-respecting engine (shell draw outside the census edge, unfiltered source). Verdict PARTIAL on both footings: LAW-CONSISTENT and L200 GROWTH OK, but small-box r(k) NOT converged

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (a97f36491).
- **Engine:** `cfg527_pm.py`, a copy of cfg524_pm.py. Launcher: `run_527.py` (claim-based queue, 4 workers, 4 threads each, nice 10).
- **Scripts:**
  - `cfg527_profiles.py` (Gate 1). It imports cfg526_profiles.py and changes only the run table, the work directory and each run's mix.
  - `cfg527_analysis.py` (Gates 2–3, stability, decision) writes `cfg527_analysis.out` and `cfg527_results.json`.
  - `cfg527_posthoc.py` gives the declared concentration ratio.
- **Arrays and logs:** `../_external_data/cfg527_work/`.
- **Settings:** κ = ½ FITTED; footings 9.3603e-11 / 1.1312e-10, never pooled; flat a0; ν_mono; 256³, seed 359. The cold energy's MASS is still required. Not "theory closed". Nothing was downloaded.

## The rule (exact)

Each force call:
- The excess is unchanged: e = f_sw max(s_ph − s_c, 0), inside the census edge.
- **Draw region:** D = turnaround catchment AND NOT census edge.
- **Draw:** comp = q_C s_c on D. Per catchment component, q_C = Σ_C e / Σ_{D_C} s_c.
- **Cap:** the existing 1/q cap applies when q_C > 1. Nothing is drawn inside the census edge. Σ_C (e − comp) = 0.

**Why the s_c weight is forced.** f_sw is zero outside the census edge, so on the shell CFG524's literal reservoir R2 equals s_c exactly.

**What "unfiltered" means in code.** The MIX-A filter W(k) on the MOND input g_b is replaced by W = 1 (mix `NOFILT`), so g_b is the plain PM field of the retained baryons f_ret(x)(1 + δ).

## Gate 1: law consistency (CFG526 statistic, unchanged)

R = M_grav / M_law is a median over the 100 densest scored hosts. Tolerance is 0.1 dex. Values are from `cfg527_profiles.json`.

| run | core R, L50 | core R, L25 | every scored radius within 0.1 dex | core R, L100 / L200 |
|---|---|---|---|---|
| **LR-can** | **0.961** | **0.976** | yes (0.912–1.132) | 0.965 / 0.975 |
| **LR-alt** | **0.957** | **0.942** | yes (0.830–1.038) | 0.956 / 0.965 |
| MUTATE A (old draw + filter) | 0.728 | 0.773 | no (down to 0.494) | – |
| SHF (shell draw + filter) | 0.894 | 0.931 | yes | – |
| K1 (f_ret = 1) | 0.933 | 0.785 | no | – |
| MUTATE B (no compensation, L200) | – | – | – | 0.976 (L200) |

**Convergence.**
- At fixed physical radius (median log R), L50 → L25:
  - canonical: Δ = +0.079 at r = 0.23 Mpc/h and −0.026 at r = 0.39 Mpc/h;
  - alt: Δ = +0.032 at r = 0.23 Mpc/h.
- L100 → L50: Δ = +0.010 at r = 0.46 Mpc/h on both footings.
- In cell units, core R spans 0.975 / 0.965 / 0.961 / 0.976 from L200 to L25 (canonical, spread 0.007 dex) and 0.965 / 0.956 / 0.957 / 0.942 (alt, 0.011 dex).

**Frozen verdict: LAW-CONSISTENT on both footings.**
- The CFG526 shortfall (0.51–0.77) is gone. MUTATE A reproduces it exactly (0.728 / 0.773), so the statistic has teeth.
- Attribution:
  - Moving the draw out of the census edge does most of the work: SHF lifts core R from 0.73 / 0.77 to 0.89 / 0.93.
  - Dropping the filter brings it to 0.96 / 0.98.

## Gate 2: growth (z = 0, vs matched S0; from `cfg527_results.json`)

| box | run | σ8 ratio | max\|P−1\| (k ≤ 1) | P/P_S0 at k = 1 / 2 / 4 | verdict |
|---|---|---|---|---|---|
| L200 (CFG361, gating) | LR-can | 1.0071 | 0.090 | 1.074 / 1.015 / 1.061 | **GROWTH OK** |
| L200 | LR-alt | 1.0071 | 0.097 | 1.077 / 0.996 / 1.064 | **GROWTH OK** |
| L200 | MUTATE B | 1.0456 | 0.213 | 1.167 / 1.091 / 1.136 | TENSION (control works) |
| L100 (reported) | LR-can / LR-alt | 1.014 / 1.015 | 0.117 / 0.118 | 1.085 / 1.000 / 0.963; 1.061 / 0.955 / 0.951 | TENSION / TENSION |
| L50 (CFG521 gate, information) | LR-can / LR-alt | 1.013 / 1.012 | 0.155 / 0.183 | 1.172 / 0.991 / 0.878; 1.205 / 0.995 / 0.856 | TENSION / TENSION |
| L25 (information) | LR-can / LR-alt | 1.020 / 1.022 | 0.181 / 0.198 | 1.167 / 1.367 / 1.185; 1.181 / 1.428 / 1.227 | TENSION / TENSION |

L200 passes, but only narrowly: 0.090 and 0.097 against the 0.10 cut.

**Small-box framework-native gate: FAIL on both footings.** r(k) is not converged at k = 2 or k = 4 (rule: |r50 − r25| ≤ 0.05 and |r100 − r50| ≤ 0.05):

| k | canonical (L100 / L50 / L25) | alt (L100 / L50 / L25) |
|---|---|---|
| 2 | 1.000 / 0.991 / 1.367 | 0.955 / 0.995 / 1.428 |
| 4 | 0.963 / 0.878 / 1.185 | 0.951 / 0.856 / 1.227 |

The old k = 4 deficit trend (0.89 / 0.80 / 0.63 / 0.59) is replaced by 1.06 / 0.96 / 0.88 / 1.19 (canonical). It is no longer a monotone deepening, but it is not a converged prediction either.

**Why it fails (mechanism, checked in the run JSONs).** In the small boxes the rule runs in its capped regime:
- **Where the cap acts.** At z = 0 the cap acts in 4–7 catchments holding 65–69% (L50) and 79–80% (L25) of the catchment mass.
- **What it removes.** It removes 46–52% (L50) and 74–75% (L25) of Σe.
- **What it empties.** Those catchments percolate across the box, so their shell holds only 28–43% of the catchment's cold energy. With q capped at 1, the whole shell cold share is drawn.
- **L200 by contrast.** The cap touches 3% of catchment mass and removes 1% of Σe, and the shell holds 62–67%.

The excess at k = 1–2 grows with time and with resolution in step with the cap. At L25 the cap's mass share runs 0.84 → 0.84 → 0.79 and its Σe removal 0.45 → 0.65 → 0.75 (z = 1 → 0.5 → 0), while r(k = 2) goes 1.08 → 1.14 → 1.37.

SHF shows the same small-box excess (L25 k = 2: 1.355), so the excess comes from the shell draw in its capped regime, not from dropping the filter.

Because the regime is driven by resolved-host percolation, a 512³ L200 run would also move toward it. This is a statement about the rule's capped regime, not a physics prediction against S0.

## Gate 3: controls and stability

| check | result |
|---|---|
| MUTATE A reproduces CFG521 DC-can (L50, L25) | \|dσ8\|/σ8 = 0 and max\|dP/P\| = 0 at every snapshot: PASS |
| MUTATE A fails law consistency | yes (core R 0.728 / 0.773) |
| MUTATE B (NOCOMP, NOFILT, L200) not GROWTH OK | TENSION, 0.213: OK |
| Stability (every NOFILT run finite, P/P_S0 at k_Nyq/2 ≤ 2) | all STABLE, 0.53–1.09 |

On stability, the filter is not a numerical regulator here. P/P_S0 at k_Nyq/2 is 0.800 / 0.852 for SHF against 0.826 / 0.878 for LR-can (L50 / L25).

## Decision (frozen)

**Both footings: PARTIAL.** Gate 1 is LAW-CONSISTENT, L200 is GROWTH OK and MUTATE B behaves as required, but the small-box r(k) is not converged at k = 2 or 4.

**512³: not run.** The frozen rule requires both footings to PASS first.

## Reported

- **Concentration c/c_S0** (`cfg527_posthoc.out`):

  | box | LR-can / LR-alt | MUTATE A | SHF | K1 |
  |---|---|---|---|---|
  | L200 | 1.098 / 1.116 | – | – | – |
  | L100 | 0.953 / 0.983 | – | – | – |
  | L50 | 0.978 / 0.962 | 0.859 | 1.049 | 0.910 |
  | L25 | 1.022 / 0.999 | 0.765 | 1.017 | 0.970 |

- **Matched-S0 deficit.** The law-consistent halos are not de-concentrated relative to S0: core D_law is 1.01–1.32 and D_eng is 1.00–1.25.
- **Cap use (z = 0, at most over snapshots).**
  - q_max: 1.41 / 1.24 at L200, 3.03 / 2.33 at L50, 5.67 / 4.87 at L25.
  - Catchments with an empty shell: none in any run.
  - comp inside the census edge: 0 (by construction; checked).

## Departures and notes (dated)

- **2026-10-09.** MUTATE A fails CFG526's K1 implementation on one diagnostic key that the frozen K1 list does not include: `cap_e_removed_frac`. When the cap is inactive this is float32 round-off of 1 − Σe/E_pre (absolute 2e-8 to 6e-7), so its relative difference is meaningless.
  - Every frozen K1 item passes: e_sum ≤ 1.2e-7, q_max ≤ 1.2e-8, n_catch exact.
  - src_sum is a float32 sum of a zero-mean field (|d| 1.6e-3 / 5.1e-2, compared with e_sum ~1e6).
  - MUTATE A is a control. Its law verdict is identical to CFG526's.
- **2026-10-09.** The L50 → L25 physical convergence rests on 11–12 L25 hosts per radius (two radii evaluable for canonical, one for alt). L100 → L50 adds one radius with 33–75 hosts.
- **2026-10-09.** The profile caches keep CFG526's `cfg526_<run>.npz` file names, in `_external_data/cfg527_work/profiles/`.

## Caveats

- One seed at 256³. Halo cores are 1–2 cells.
- The draw is bookkeeping of the cold share s_c. The cold energy's mass is still required.
- The census still paints group f_ret over galaxies inside group turnaround balls.
- κ, f_b and ρ_Λ are not derived. Not "theory closed".

## Run

```
nohup python3 campaign_fresh_gravity/CFG527_law_respecting_engine/run_527.py LRcan_L50 LRcan_L25 LRalt_L50 LRalt_L25 MUTA_L50 MUTA_L25 LRcan_L200 LRalt_L200 MUTB_L200 LRcan_L100 LRalt_L100 K1_L50 K1_L25 SHF_L50 SHF_L25 &   # x4
nice -n 10 python3 campaign_fresh_gravity/CFG527_law_respecting_engine/cfg527_profiles.py compute
python3 campaign_fresh_gravity/CFG527_law_respecting_engine/cfg527_profiles.py
python3 campaign_fresh_gravity/CFG527_law_respecting_engine/cfg527_analysis.py
python3 campaign_fresh_gravity/CFG527_law_respecting_engine/cfg527_posthoc.py
```
