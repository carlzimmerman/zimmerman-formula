# CFG555: the growth statistic on the gravitating field. PAPER45's growth claim FAILS at 512³

Criteria were frozen first (`FROZEN_CRITERIA.md`, commit 43496a6ec). Date: 2026-10-10.

**Verdict.**
- PAPER45 v2.0/v2.1 (DOI 10.5281/zenodo.23237726 / 23240853): **CLAIM FAILS ON GRAVITATING FIELD.**
  - 12 of its 15 rule runs pass on the gravitating field. These are all the 256³ runs: max|P−1| 0.063–0.082, σ8 ratio 1.0141–1.0193.
  - All three 512³ runs fail (TENSION): canonical 1.0405 / **0.163**, alternative 1.0459 / **0.193**, a₀ tracking dark energy 1.0429 / **0.167**.
- The 512³ second realisation (CFG460) fails too: 1.0333 / 0.184.
- The published table (0.033 / 0.040 / 0.033 at 512³) is right for the particle density. It is not the matter (gravitating) density.

## 1. Which density each lane scored (all particles only)

| lane | where P(k), σ8 are measured | what the analysis reads |
|---|---|---|
| CFG361 (the statistic) | `cfg361_pm.py:322` `measure_pk(pmesh, pmesh.deposit(pos), …)` | `cfg361_pm_growth_T5.py:35-36` `snap[z]["P"]`, `["sigma8"]` |
| CFG424 / 425 / 426 / 427 / 439 / 460 | `cfg424_pm.py:474` (particles), stored at `:478` | `cfg424_analysis.py:6-8`, `cfg425_analysis.py:6-8`, `cfg426_analysis.py:6-8`, `cfg427_analysis.py:6-8`, `cfg439_analysis.py:6-8`, `cfg460_analysis.py:5-8` |
| CFG518 | `cfg518_pm.py:503`, stored at `:507` | `cfg518_analysis.py:14-16` |
| CFG527 | `cfg527_pm.py:541`, stored at `:545` | `cfg527_analysis.py:47-49` |
| CFG530 | the same engine (`cfg527_pm.py:541`) | `cfg530_analysis.py:30`, `:75` (growth gate `:192-197`) |

In every engine the source e − comp enters only the potential (`cfg424_pm.py:420,426`). It is never in the field that P(k) is measured on.

## 2. Recomputation on the gravitating density

Method (`cfg555_compute.py`):
- Load each run's saved z = 0 state.
- Call the run's own engine `forces` (diag = True, imported unchanged, the run's own settings).
- Capture the total potential from the three acceleration transforms (the CFG526 method).
- Form δ_grav = −k²φ_k/(1.5Ω_m), which is particles + (e − comp)/(1.5Ω_m).
- Score with the CFG361 cuts against the matched S0 JSON. S0 has no source, so its gravitating field is its particle field.

Every run passes every reproduction gate:
- q_max and e_mean/e_sum to ≤ 4.5e-7 relative; n_catch exact; src_sum within 1e-6 Σe.
- Particle P to ≤ 7e-8 and σ8 to ≤ 6e-9 against the run JSON.
- mean(δ_grav − δ_p) ≤ 4e-9.

All numbers below come from `cfg555_results.json`.

| run (lane) | N | foot | particle σ8 / max\|P−1\| | **gravitating** σ8 / max\|P−1\| (k) | verdict | r_grav at k = 0.5 / 1 / 2 |
|---|---|---|---|---|---|---|
| TA-can (424) | 256 | can | 1.0033 / 0.027 | 1.0158 / 0.075 (0.35) | GROWTH OK | 1.062 / 0.948 / 0.846 |
| TA-alt (424) | 256 | alt | 1.0031 / 0.029 | 1.0156 / 0.077 (0.41) | GROWTH OK | 1.072 / 0.964 / 0.876 |
| R1 s360 (425) | 256 | can | 1.0024 / 0.022 | 1.0141 / 0.063 | GROWTH OK | |
| R2 s361 (425) | 256 | can | 1.0026 / 0.017 | 1.0175 / 0.075 | GROWTH OK | |
| D1 DE (426) | 256 | can | 1.0035 / 0.029 | 1.0157 / 0.074 | GROWTH OK | |
| D2 DE (426) | 256 | alt | 1.0032 / 0.030 | 1.0154 / 0.075 | GROWTH OK | |
| A1 s360 (426) | 256 | alt | 1.0023 / 0.025 | 1.0149 / 0.068 | GROWTH OK | |
| A2 s361 (426) | 256 | alt | 1.0030 / 0.023 | 1.0193 / 0.082 | GROWTH OK | |
| E1 / E2 eps (427) | 256 | can | 1.0033 / 0.027 | 1.0158 / 0.075; 1.0159 / 0.075 | GROWTH OK | |
| G1 MIXB / G2 HOT1 (427) | 256 | can | 1.0027 / 0.026; 1.0038 / 0.031 | 1.0153 / 0.072; 1.0160 / 0.076 | GROWTH OK | |
| **R3 (425)** | **512** | can | 1.0045 / 0.033 | **1.0405 / 0.163** (0.32) | **TENSION** | 1.130 / 0.847 / 0.666 |
| **A alt (439)** | **512** | alt | 1.0054 / 0.040 | **1.0459 / 0.193** (0.41) | **TENSION** | 1.160 / 0.872 / 0.682 |
| **B DE (439)** | **512** | can | 1.0045 / 0.033 | **1.0429 / 0.167** (0.32) | **TENSION** | 1.135 / 0.851 / 0.669 |
| **seed 360 (460)** | **512** | can | 1.0037 / 0.040 | **1.0333 / 0.184** (0.97) | **TENSION** | 1.098 / 0.803 / 0.633 |
| MUTATE, no compensation (424) | 256 | can | 1.0326 / 0.154 | 1.1730 / 0.505 | TENSION | |
| DC-can / DC-alt (518) | 256 | | 1.0028 / 0.023; 1.0036 / 0.030 | 1.0145 / 0.067; 1.0171 / 0.080 | GROWTH OK | |
| **DC-can (518)** | **512** | can | 1.0047 / 0.029 | **1.0358 / 0.150** | **TENSION** | 1.115 / 0.832 / 0.639 |
| K1 f_ret = 1 / NOCOMP (518) | 256 | can | | 1.0158 / 0.075; 1.1596 / 0.461 | OK / TENSION | |
| LR-can / LR-alt L200 (527) | 256 | | 1.0071 / 0.090; 1.0071 / 0.097 | **1.0565 / 0.341; 1.0623 / 0.408** | **TENSION** | |
| MUTB, no compensation (527) | 256 | can | 1.0456 / 0.213 | 1.2751 / 0.808 | FAIL | |
| CFG530 L200 N128 / 256 / 512, can | | | 0.061 / 0.080 / 0.113 | 0.360 / 0.336 / 0.544 | TENSION (all) | |
| CFG530 L200 N128 / 256 / 512, alt | | | 0.047 / 0.086 / 0.121 | 0.370 / 0.388 / 0.596 | TENSION (all) | |

CFG530 L100 is also TENSION at every N, both footings (0.31–0.66).

**Per-lane verdicts.**
- CFG424: **HOLDS** (256³ only; its MUTATE stays non-passing).
- CFG426: **HOLDS** (256³).
- CFG427: **HOLDS** (256³).
- CFG425: **FAILS** (R3 512³: 0.163).
- CFG439: **FAILS** (0.193 / 0.167).
- CFG460: **FAILS** (0.184).
- CFG518: **FAILS** (512³ DC-can: 0.150; 256³ passes).
- CFG527: **FAILS** (0.341 / 0.408).
- CFG530: **FAILS** (every N).
- No lane is NOT EVALUABLE. Every z = 0 state was on disk; nothing needed re-running.

**The failure is not an artefact. Checks (`cfg555_srccheck.out`, TA-can 256³ and R3 512³):**
- The captured source is e − comp:
  - zero outside the catchments (2e-5 of |src|);
  - summing to zero on every catchment (≤ 1e-5);
  - its positive part is 0.79–0.80 of the engine's Σe, because e and comp overlap in the same cells.
- Where the excess comes from:
  - at 512³, k = 0.32: r_grav 1.163 = particles 1.022 + source auto-power 0.017 + cross term 0.124;
  - the source is positively correlated with the particles (correlation 0.47 at 512³, 0.36 at 256³). The settled cold energy concentrates mass toward the hosts on catchment scales.
- The resolution trend matches the particle-side warnings PAPER45 already gave:
  - catchment draw 0.30 → 0.49–0.57;
  - source σ8 share 0.046 → 0.105 of the particles' σ8.
- Deconvolving the CIC window from the particle part only changes max|P−1| by ≤ 0.004 (reported).
- At 512³ the gravitating field also falls 13–20% below S0 at k = 1 (r 0.80–0.87). So the miss is a reshaping of the spectrum on both sides of the cut, not a single bin.

**Controls.**
- C0 / MUTATE: with the source off (`cfg555_analysis_MUTATE.out`), every lane's committed particle number is reproduced to ≤ 2e-8, and PAPER45 returns 15/15 exactly as published.
- C1: a synthetic fixed-amplitude source with P = 0.05 P_S0 is recovered bin by bin to 2.9e-7.
- C2: the S0 capture gives δ_grav = δ_p to 1.9e-7 of the peak; an injected (1.05)δ returns the factor 1.1025 to 5.3e-7.
- The independent rebuild of CFG530 LR-can L200 N256 agrees with CFG530's cache (and CFG539's 0.336) to 2.4e-9.

## 3. Which field the observations need

- **Galaxy clustering** traces the baryons. In the PM the baryons are the f_b share of the particles, so clustering corresponds to the particle field (up to bias).
- **Weak lensing, cosmic-shear S8, CMB lensing, cluster counts and "the matter power spectrum"** all respond to the total gravitating mass. In candidate B the settled cold energy is matter.
- PAPER45's claim is "structure growth within 10% of ΛCDM-equivalent growth", supported by the "excess in the matter power spectrum" and by σ8. The control's growth is that of all matter. So the claim refers to the **gravitating** field.
- Its wording survives only at 256³. At 512³ (the resolution PAPER45 headlines in bold) the gravitating excess is 16–19%, against the 10% limit.

## Draft correction text for the owner (not applied; the paper is NOT edited, nothing published)

**Abstract**, replace "With this rule the excess is $2.7\%$ at $256^3$ and $3.3\%$ at $512^3$, with $\sigma_8$ within $0.6\%$ of a control run without the law" with:

> With this rule the excess in the particle (baryon-tracing) power spectrum is $2.7\%$ at $256^3$ and $3.3\%$ at $512^3$. In the gravitating matter density, which includes the cold fluid the rule settles into each halo and is what lensing measures, the excess is $7.5\%$ at $256^3$ but $16$--$19\%$ at $512^3$ (σ$_8$ $+4$--$5\%$), above the $10\%$ limit.

Also in the abstract, after "It holds in three random realisations, …", add: "on the particle density; on the gravitating density it holds at $256^3$ only."

**Results**, after the table add:

> Correction (2026-10-10). The table's spectra were measured on the particle density. The rule moves cold fluid within each catchment, and that moved mass gravitates, so the matter power spectrum is that of particles plus the settled source. Re-measured on that density from the same saved states (CFG555): $256^3$ runs $\max|P-1| = 0.063$--$0.082$, σ$_8$ ratio $1.014$--$1.019$ (pass); $512^3$ canonical $1.0405 / 0.163$, alternative $1.0459 / 0.193$, $a_0$ tracking dark energy $1.0429 / 0.167$, second realisation $1.0333 / 0.184$ (all fail). The mass-conservation control (no compensation) is $1.1730 / 0.505$ on this density.

**What this shows**, replace the first sentence with:

> Within this framework, the rule keeps the particle (baryon-tracing) spectrum within $10\%$ of $\Lambda$CDM-equivalent growth at $256^3$ and $512^3$. It does not keep the gravitating matter spectrum within $10\%$ at $512^3$, and the gap grows with resolution. Structure growth as seen by lensing is therefore not fixed by this rule.

**Title.** "Fixes Structure Growth" no longer holds as stated. Suggested: "… Keeps Particle Clustering Near ΛCDM-Equivalent Growth at 256³ but Not the Gravitating Matter Spectrum at 512³", or the owner's choice.

**Scope.** The comparison rows (hand-set edge, census edge, and the abstract's +15.3/+19.3/+17.4% "law everywhere" numbers) are also particle-based. They are not re-measured here.

## Caveats (dated 2026-10-10)

- The source is the engine's z = 0 snapshot diagnostic. Its in-cover mask is recomputed at the snapshot; during the run it was cached for up to 10 steps. This is the same state the runs' own q_max/e_sum come from, and those are reproduced.
- The cuts and the S0 controls are CFG361's, imported unchanged; no knob was touched.
- κ = ½ is fitted, and the cold energy mass is still required. Nothing here is "theory closed".

## Reproduce

```
nice -n 10 python3 campaign_fresh_gravity/CFG555_growth_on_gravitating_field/cfg555_compute.py        # ~10 s per 256^3, ~100 s per 512^3 (38 GB peak), caches in ../_external_data/cfg555_work
python3 campaign_fresh_gravity/CFG555_growth_on_gravitating_field/cfg555_analysis.py
CFG555_MUTATE=1 python3 campaign_fresh_gravity/CFG555_growth_on_gravitating_field/cfg555_analysis.py
nice -n 10 python3 campaign_fresh_gravity/CFG555_growth_on_gravitating_field/cfg555_srccheck.py 424_TAcan 425_R3_can_512
```
