# CFG161 — a consistency check of CFG160's P4: the KURVS − KROSS differential under Kretschmer et al.'s pressure support. FROZEN CRITERIA

Written 2026-09-29, at the orchestrator's go, before any number of this check has been computed. CFG140's committed differentials under P0 and P1 are known: +0.017 ± 0.058 and +0.273 ± 0.070. It runs in parallel with CFG165 (the Opus chat's independent re-derivation of CFG160). CFG165's outputs are not read until this result is committed. Nothing below may change after a result is seen; any later deviation goes in the README as a disclosed departure.

## The question

Does the KURVS − KROSS differential under P4 land on one reading's prediction, or does P4 manufacture evolution?
- A P4-manufactures outcome counts against P4, not against either a₀ law.
- **Power, stated before the data:** σ_D is about 0.06–0.07 dex, against a separation of about 0.083 dex between the two predictions. That is about 1.2σ.
  - The likely outcome is "consistent with both".
  - A pass does NOT validate P4; a fail counts against it.

## Why

- CFG140's KROSS control (390 KROSS discs at median z ≈ 0.85, run through the same pipeline) gave a differential of +0.273 ± 0.070 under the constant-σ Burkert correction (P1). That is about 2.7σ beyond even the rival's prediction: an "evolution" neither reading predicts. It was the first hint that P1/P2 over-correct.
- CFG160's P4 applies to both samples. The check is whether P4 removes that manufactured evolution.

## Inputs (CFG140's KROSS machinery, verbatim)

- **The pipelines:** CFG141's, exec'd read-only (it exec's CFG140's). This gives KU (the ten KURVS discs with the tabulated σ₀), KU2 (the same with CFG141's measured σ_out), KR (the 390 KROSS discs: RT/RT+, v/σ₀ ≥ 1, R = 2 r_im, R_d = r_im/1.68, tabulated σ₀), gbar, gpred, pooled and CFG140's error model.
- **The cell:** μ = 0.67, δ = 0, canonical footing, the flat reading's Δ with no anchor. The anchor cancels in a differential, as in CFG140's R3.
- **The P4 functions** (α(x) = −0.146x² + 1.204x + 1.475, x = R/R_e − 1 clipped to [0, 4], R_e = 1.68 R_d, V_c² = V² + α σ², and the same error propagation) are copied verbatim from CFG160.
  - For KROSS, x = 2r_im/r_im − 1 = 1, so α = 2.533.
- **KURVS primary:** KU2 (σ_out), as CFG160.
- **KURVS variant (reported):** KU (σ₀), for parity with KROSS, which has only σ₀.

## The statistic and the predictions

- **D** = Δ_flat(KURVS) − Δ_flat(KROSS), pooled, with σ_D the two pooled errors in quadrature. This is CFG140's R3 definition.
- **The flat prediction:** D_flat = 0.
- **The rival's prediction (primary),** computed exactly through the pipeline: D_H = [Δ_flat − Δ_H]_KURVS − [Δ_flat − Δ_H]_KROSS. That is the differential the flat statistic would show if the rival held exactly in both samples. CFG140's deep-regime approximation, ½ log₁₀[E(z_KURVS)/E(z_KROSS)] ≈ +0.083, is reported beside it.

## Decision rule

- **Lands on flat:** |D| ≤ 2σ_D and |D − D_H| > 2σ_D.
- **Lands on the rival:** |D − D_H| ≤ 2σ_D and |D| > 2σ_D.
- **Consistent with both:** both within 2σ_D. This is the expected outcome at this power.
- **P4 manufactures evolution:** D lies more than 2σ_D from both predictions, on either side. This counts against P4, not against either a₀ law.

## Checks

- **C1 CONTROL:** the pipeline reproduces CFG140's committed R3 differentials exactly (to the 3-decimal print): P0 +0.017 ± 0.058 and P1 +0.273 ± 0.070, from KU and KR.
- **C2 CONTROL:** the copied P4 functions reproduce CFG160's committed decision cell: Δ′_flat = +0.144, Δ′_H = −0.006 (3-decimal print).
- **R0 POWER** (printed before D): σ_D, |D_H| and |D_H|/σ_D.
- **H1 [HEADLINE; MUTATE must change it]:** P4 does not manufacture evolution, i.e. D lies within 2σ_D of at least one prediction.

## Reported rows

- **R1:** D under P0, P1, P2 (KU2 with σ_out, and KR with σ₀ at 2R/R_d), P3 and P4. Each with σ_D, D_H and the rule's verdict.
- **R2:** the P4 band (α × 0.6, × 1.4) and the KURVS σ₀ variant.
- **R3:** the two samples' own pooled Δ_flat and Δ_H under P4 (unanchored).

## MUTATE

MUTATE=1 multiplies every KURVS v_last by 10^0.3 (g_obs × 4), inherited from CFG140's exec'd prefix. D rises by about 0.6 dex, so H1 must fail and the script exits 1.

## Readings (declared)

- **Consistent with both:** P4 does not manufacture evolution between z ≈ 0.85 and 1.5. That is a weak consistency pass, not a validation of P4, and it says nothing about a₀.
- **Lands on one reading:** reported as that, at about 1.2σ power. It is not a verdict on a₀.
- **Manufactures evolution:** counts against P4, and so against CFG160's lean, not against either law.
- **Untested (declared):**
  - KROSS's own outer σ profile (only σ₀ exists);
  - the KROSS gas;
  - the different radii of the two samples (KROSS at 2 r_im, x = 1; KURVS at R_max, x = 1.0–3.5), which place them at different points of Kretschmer's α curve;
  - VELA's applicability to either sample.

κ = ½ and Ω_c h² stay fitted. Nothing here says the data favour either model, or that the theory is closed.
