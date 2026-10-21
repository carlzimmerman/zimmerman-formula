# W4-12: can one stellar-mass or gas-mass correction reconcile the four κ facts? (frozen criteria, committed alone)

**Status: FROZEN 2026-10-20, before any W4-12 script exists.** Append-only. Rules: CFG894 `KAPPA_CAMPAIGN_RULES.md`.
Observational/consistency lane (`obs`). **κ = ½ is FITTED.** Not theory closed.

## The four facts (committed, this session)

- **F1** gas-dominated rotation curves (p64 B, ten TRGB galaxies, E2): κ_Λ = 0.557. Nearly insensitive to stellar M/L.
- **F2** isolated blue lenses (W4-06 / W4-10): κ_Λ = 0.520. In the deep regime κ ∝ 1/M_bar.
- **F3** within-galaxy gas versus star points (p64 A, eleven galaxies): Δ_g = −0.408 ± 0.085 dex at Υ_d 0.5, f_gas 1.
- **F4** red versus blue lenses (W4-10): 1.293 vs 0.520.

## Question

Is there one universal correction that makes all four consistent? The correction is a stellar-mass factor k (Υ_d = 0.5k
for SPARC; lens stellar masses × k) and a gas-mass factor f (SPARC V_gas² × f; lens gas × f).

## Method (fixed)

- **Grid:** log₁₀k ∈ [−0.2, 0.6] and log₁₀f ∈ [−0.6, 0.2], step 0.05 (17 × 17 cells).
- **F1:** p64 B's E2 recomputed at (Υ_d = 0.5k, f_gas = f), with the S0 sample and gas-point classification fixed at the
  fiducial as p64 froze them. σ from a 500-resample galaxy bootstrap (seed 64).
- **F3:** p64 A's Δ_g recomputed at (0.5k, f), point classes fixed at the fiducial. σ from a 500-resample bootstrap (seed 64).
  This is 500 rather than p64's 2000, declared to keep the 289-cell grid light.
- **F2 and F4:** W4-06's committed estimator (CFG829 window, ν_simple, ρ_DE) refitted with lens g_bar × (S k + (1−S) f), where
  S is the stellar share of B21's g_bar. B21's public RAR files give only the total, so S is bracketed: **S = 1.0 and S = 0.7**,
  both reported.
- **Code identity (K1):** the copied p64 functions reproduce p64's fiducial Δ_g (−0.408) and E2 log a₀ (−9.9816) to 1e-3. The
  W4-06 import reproduces blue 0.520 and red 1.293 to 2e-3.

## Conditions per cell (frozen)

- **C1:** |Δ_g| < 2σ (the within-galaxy gap closes).
- **C2:** |log κ_F1 − log κ_F2| < 2σ_comb (rotation curves and blue lenses agree), with σ_comb from the two σ's in dex.
- **C3:** |log κ_red − log κ_blue| < 2σ_comb (the type split closes).
- **Plausible region:** k ∈ [0.8, 1.6] (Υ_d 0.4–0.8, population synthesis) and f ∈ [0.85, 1.15] (CFG493's gas-scale band).

## Verdict (frozen)

- **ONE CORRECTION FITS ALL:** some cell satisfies C1, C2 and C3 (both S brackets). Report whether it is in the plausible region.
- **NO SINGLE CORRECTION:** no cell satisfies all three.
  - Also report the best cell for C1 ∧ C2 alone and for C2 ∧ C3 alone, with their (k, f).
  - Also report whether C3 can pass anywhere. Hand expectation: never, because a universal k or f rescales red and blue alike.
- Also report: at the best C1 ∧ C2 cell, is ½ within 2σ of κ_F1?

**Hand expectation (disclosed):** NO SINGLE CORRECTION.
- C3 is structurally fixed under a universal correction.
- C1 needs Υ_d ≈ 1.3, extrapolated from p64's grid slope, or f ≈ 0.35.
- Either breaks C2: κ_F2 ∝ 1/k drops at large k, and κ_F1 ∝ 1/f rises at small f.

## Controls (`W4_12_MUTATE=1`, separate outputs, exit 1 when they bite)

- **M1, mock early-type IMF:** red lens g_bar × 10^0.4 before the analysis. C3 must then pass in some cell. This shows C3 can
  pass when the data allow it.
- **M2, mock radial M/L:** SPARC star-dominated points' stellar terms × 10^0.43 (about 2.7). C1 must then pass near k = 1, f = 1.
- Each must change its condition's pass map relative to the normal run.

## Register

One `obs` row, then `kappa_campaign_lee.py` rerun. Nothing downloaded.
