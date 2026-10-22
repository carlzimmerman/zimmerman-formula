# Pre-DR4 note, 2026-10-22: how the law-first vs medium-first fork is scored

**Status: PRE-DATA. Owner-approved 2026-10-22 ("yes to all"). Written before Gaia DR4 (release 2 December 2026).**
This is a new file. It **adds one fork reading**. It does **not** edit `PREREGISTRATION_DR4.md`, any amendment,
any `*_HASH.txt`, `wide_binary_pipeline.py` or any other frozen file. It changes **no** existing frozen statistic,
estimator, cut, decision row or verdict line. Arms A/B/C, the Amendment 22 R rule (CFG825) and the guard zones stay as
they are. Source of every number: `doors_push_2026_10_22/D2_wide_binary_fork/` (commit c27b941b99,
`d2_wide_binary_fork_results.json`). κ = ½ is FITTED. Footings are never pooled.

## 1. The fork
- **Law-first**: the canonical law g_N = g²/(g + a₀) holds at every scale, read with the Galactic external field.
  This is Arm A's reading.
- **Medium-first**: the P-sector crossover is physical, so wide binaries are Newtonian (γ_v = 1.000).

## 2. The statistic
- The fork is scored on the **whole-catalogue γ̂**: the registered estimator's global fit on the full frozen-cut DR4
  catalogue, both footings.
- It is **not** scored on the single 18–22 kAU bin. On the DR3 frozen-cut catalogue that bin holds 0.69 % of pairs
  (43 / 6,210), about 208 at N = 30,000. That gives only 0.8–2.6σ, so the bin is reported as information only.

## 3. The pre-declared systematics condition
- **Definition.** σ_sys = max(0.020 frozen allowance, ½ × full spread of γ̂ across the frozen robustness ladder and
  the NSS-off probe).
- **Condition.** The fork may be scored only if σ_sys < **0.054 (canonical)** or **< 0.064 (alt)**. These are one
  third of Arm A's floor minus 1 (0.1614 / 0.1917). Above them, 3σ is unreachable at any N.
- **If the condition fails**, the fork is reported as **UNDECIDED** on that footing. It is never reported as
  law-first or as medium-first. The raw γ̂ and both distances are still printed.
- **If the condition holds**, the fork is scored by these rows. "≥ 3σ" means ≥ 3 × √(σ_fit² + σ_sys²):
  - γ̂ − 1.000 ≥ 3σ and γ̂ not below Arm A's floor by ≥ 3σ: medium-first excluded.
  - Arm A floor − γ̂ ≥ 3σ: law-first excluded.
  - Otherwise: UNDECIDED.

## 4. Predictions per frozen g_ext
These are for a single 1+1 M☉ circular binary at 20 kAU, orientation-averaged, QUMOND. They illustrate the
prediction; they are **not** a new target. The scored target remains Arm A's registered band.

| g_ext (frozen, PREREG §1.1) | canonical (9.36e-11) | alt (1.13e-10) |
|---|---|---|
| primary 1.778e-10 m/s² | **1.175** | **1.210** |
| alternative 2.078e-10 m/s² | **1.151** | **1.182** |

Medium-first predicts 1.000 on both footings at every g_ext.

## 5. Expected separation at DR4's expected pair count
At N = 30,000 (the frozen error model) and σ_sys = 0.020, Arm A's floor is separated from 1.000 by:

| σ_fit model | canonical | alt |
|---|---|---|
| registered mock, σ_fit 0.019 | 5.85σ | 6.95σ |
| DR3-calibrated, 0.055 × √(6210/N) = 0.025 | 5.04σ | 5.98σ |

N needed for 3σ (canonical) is 4,300–7,500 at σ_sys 0.02 and 8,400–14,500 at σ_sys 0.04. The record's demonstrated
inter-group disagreement is 0.174 in γ_v, which is 3.2× the canonical ceiling. DR4's NSS/RV screening of triples,
not N, therefore decides whether the fork can be scored.

---

## AMENDMENT A1 (2026-10-22, pre-data, append-only)

Requested by the coordinator after lane E2. Everything above is kept unchanged. `PREREGISTRATION_DR4.md` and the hash
files are untouched.

**Why.** Lane E2 (`doors_push_2026_10_22/E2_field_equation/`, commits 021ee82abb and 474050bcd8) derives the action's
own field equation at L★ → 0. It is **AQUAL** with μ = x/(1+x), not QUMOND. The §4 numbers above came from QUMOND.

**AQUAL predictions** (E2 `e2_field_equation_results.json` → `R2.*.gamma_AQUAL_anch`; verified there). Same setup as
§4: 1+1 M☉, circular, 20 kAU, orientation-averaged.

| g_ext (frozen) | canonical | alt |
|---|---|---|
| primary 1.778e-10 m/s² | **1.167** (QUMOND 1.175) | **1.199** (QUMOND 1.210) |
| alternative 2.078e-10 m/s² | **1.145** (QUMOND 1.151) | **1.173** (QUMOND 1.182) |

Two further readings:
- **Screened reading.** At L★ = 24 pc it gives γ_v − 1 = 8.1e-6 (lane D7d, `D7d_screened_q2/README.md`). That is
  medium-first-like: indistinguishable from 1.000.
- **Medium-first** stays at 1.000.

**Separations recomputed, using the AQUAL value itself as the law-first expectation.** N = 30,000 and σ_sys = 0.020.
"3σ ceiling" is the σ_sys above which 3σ is unreachable at any N.

| footing / g_ext | z (σ_fit 0.019 mock) | z (DR3-calibrated 0.025) | N for 3σ (mock / DR3-cal) | 3σ ceiling on σ_sys |
|---|---|---|---|---|
| canonical / primary | 6.04 | 5.20 | 4,031 / 6,991 | 0.0556 |
| alt / primary | 7.20 | 6.20 | 2,720 / 4,718 | 0.0662 |
| canonical / alternative | 5.25 | 4.52 | 5,614 / 9,738 | **0.0483** |
| alt / alternative | 6.27 | 5.40 | 3,701 / 6,420 | **0.0577** |

**Effect on §3.**
- **The scoring rule is unchanged**: whole-catalogue γ̂, raw γ̂ and both distances printed, UNDECIDED if the condition
  fails. The decision rows still use the registered Arm A floor.
- **The recompute gives a tighter ceiling.** With the AQUAL value at the alternative g_ext, the condition for the fork
  to be scoreable on every frozen g_ext becomes **σ_sys < 0.048 (canonical) / < 0.058 (alt)**, not 0.054 / 0.064.
  This pre-data amendment adopts the tighter values. They can only move outcomes to UNDECIDED, never to a verdict.
- No frozen statistic, estimator, cut or verdict line of the pre-registration is changed.
