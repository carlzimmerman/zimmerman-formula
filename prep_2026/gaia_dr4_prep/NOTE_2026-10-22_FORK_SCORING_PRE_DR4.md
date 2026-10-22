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

---

## AMENDMENT A2 (2026-10-22, pre-data, append-only)

**Origin.** The owner asked that every candidate σ_sys definition be tried ("we need to try all of them"). The text of
§3 and of A1 is kept. **This amendment replaces their single-definition condition with the ruling below.**
`PREREGISTRATION_DR4.md` and the hash files are untouched.

**Source.** Script `doors_push_2026_10_22/D2_wide_binary_fork/d2_sigma_sys_defs.py` (3/3 checks; MUTATE bites),
results in `d2_sigma_sys_defs_results.json`. It runs the frozen pipeline's own estimator, imported read-only, on the
DR3 frozen-cut catalogue on disk. The baseline γ̂ = 1.0750 ± 0.0550 canonical reproduces the record's dry run. **All
DR3 values below are NON-SCORING.**

**What is compared.** Screened γ_v − 1 = 8.1e-6 (D7d) against AQUAL law-first (E2), at N = 30,000. The four
separations per row are, in order:
1. primary g_ext, mock σ_fit 0.019;
2. primary g_ext, DR3-calibrated σ_fit;
3. alternative g_ext, mock σ_fit 0.019;
4. alternative g_ext, DR3-calibrated σ_fit.

"N for 3σ" uses the same four cases, and "never" means 3σ is unreachable at any N.

**DR3 inputs.** Implementable ladder rungs and their γ̂ shifts from the baseline:

| footing | R_chance < 0.001 | 3–20 kAU | NSS-off probe | jackknife |
|---|---|---|---|---|
| canonical | +0.015 | +0.033 | +0.075 | 0.016 |
| alt | −0.013 | −0.025 | +0.058 | 0.018 |

RUWE 1.4 → 1.2 and the RV-screened subsample cannot be implemented on DR3. They are declared, not substituted.

**Canonical footing** (law-first 1.167 primary / 1.145 alternative g_ext)

| definition | σ_sys (DR3) | z at N = 30k (cases 1–4) | N for 3σ |
|---|---|---|---|
| (a) frozen allowance | 0.020 | 6.04 / 5.20 / 5.25 / 4.52 | 4,031–9,739 |
| (b) max(0.02, ½ ladder + NSS-off spread) | 0.0375 | 3.96 / 3.70 / 3.44 / 3.21 | 6,445–20,360 |
| (c) max(0.02, full spread) | 0.075 | 2.15 / 2.11 / 1.87 / 1.83 | never |
| (d) record inter-group spread | 0.174 | 0.95 / 0.95 / 0.83 / 0.82 | never |
| (e) jackknife over implementable cut variants | 0.016 | 6.67 / 5.59 / 5.80 / 4.86 | 3,835–9,093 |
| (f) quadrature budget (ecc 0.015, footing 0.005, shape 0.0373, NSS-off, triples 0 / 0.05 / 0.10) | 0.085 / 0.099 / 0.131 | 1.91–1.08 | never |
| (g1) Amdt 3 one-sided, δ_up 0 / 0.05 / 0.10 | 0.020 | 6.04–4.52 / 4.23–2.96 / 2.42–1.40 | 4,031–9,739 / 9,735–31,411 / 115,291–199,980, and never at the alternative g_ext |
| (g2) Amdt 18 σ_build in quadrature | 0.0217 | 5.78 / 5.03 / 5.02 / 4.37 | 4,139–10,105 |
| (g3) PREREG §1.5 stability gate | 0.020 | as (a) | as (a) |

On DR3 the stability gate **FAILS**: the largest ladder shift is 0.075, above σ_fit 0.055.

**Alt footing** (law-first 1.199 primary / 1.173 alternative g_ext)

| definition | σ_sys (DR3) | z at N = 30k (cases 1–4) | N for 3σ |
|---|---|---|---|
| (a) | 0.020 | 7.20 / 6.46 / 6.27 / 5.63 | 2,720–5,575 |
| (b) | 0.041 | 4.37 / 4.19 / 3.81 / 3.65 | 4,042–10,044 |
| (c) | 0.0825 | 2.35 / 2.32 / 2.04 / 2.02 | never |
| (d) | 0.174 | 1.13 / 1.13 / 0.99 / 0.99 | never |
| (e) | 0.018 | 7.54 / 6.71 / 6.57 / 5.85 | 2,675–5,449 |
| (f) triples 0 / 0.05 / 0.10 | 0.070 / 0.086 / 0.122 | 2.73–1.39 | never |
| (g1) δ_up 0 / 0.05 / 0.10 | 0.020 | 7.20–5.63 / 5.39–4.00 / 3.57–2.38 | 2,720–5,575 / 5,276–12,732 / 15,936–84,876 |
| (g2) | 0.0217 | 6.89 / 6.24 / 6.00 / 5.43 | 2,769–5,712 |
| (g3) | 0.020 | as (a) | as (a) |

On DR3 the stability gate **FAILS** (0.0575 > 0.0512).

**Ruling (replaces the single condition of §3 and A1).**
1. At DR4 the fork is scored under **every** definition (a)–(g3). It is reported **per definition and per footing,
   never pooled**.
2. A verdict (law-first excluded, or medium-first/screened excluded) is issued **only if every definition gives the
   same verdict at ≥ 3σ**.
3. Otherwise the fork is **UNDECIDED**, and the full table is reported.
4. A definition's σ_sys is measured on the DR4 catalogue itself, with the same recipe as here.

**Consequence, stated before data.** Definitions (c), (d) and (f) cap the separation below 3σ at any N, on both
footings. So **under this ruling the fork cannot be decided by Gaia DR4** unless those definitions' DR4 values fall
below the 3σ ceilings:
- canonical: 0.0556 (primary g_ext) and 0.0483 (alternative g_ext);
- alt: 0.0662 and 0.0577.

Definition (d) is a fixed record number, 0.174, and cannot fall. **Therefore, as written, the fork is UNDECIDED at
DR4 by construction.** This is reported, not repaired. Dropping (d) would need its own dated, pre-data owner
decision.

No frozen statistic, estimator, cut or verdict line of the pre-registration is changed.
