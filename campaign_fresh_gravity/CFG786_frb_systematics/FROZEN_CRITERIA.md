# CFG786 FROZEN CRITERIA: does CFG779's FRB exclusion survive its own assumptions?

Committed alone, before any script. 2026-10-14. Block CFG780–789. Owner: "did we look for any assumptions that would skew the
result? ... keep calculating".

## Question
CFG779 found B = 1.064 [1.010, 1.122] and excluded baryon-eating black-hole dark energy (P2, s_b,0 = 0.70) at 7.8σ. Re-fit B
with each assumption varied, one at a time, using CFG779's code (`cfg779.py` functions, imported read-only):
- V1, h: mean DM ∝ 1/h at fixed Ω_b h². h = 0.67 and 0.73 (B̂ scales by h/0.70).
- V2, star/gas fraction: Salpeter MD14 f_d (CFG632 `mean_dm(imf="salpeter")`) instead of Chabrier.
- V3, host prior: the authors' box widened to μ ∈ [3.5, 6.5], s ∈ [0.1, 1.3].
- V4, BBN Ω_b h²: ±2σ (0.02218 ± 0.0011; mean DM scales linearly).
- V5, sample: Sharma "yes" only (drop "unclear").
- V6, all of V1–V4 at their worst case for the exclusion (h 0.73, Salpeter, wide host box, Ω_b h² −2σ) combined.

## Escape-route check (analytic, declared)
- Could the converted baryons be ones the bursts never see (already condensed)? The condensed budget is
  ∫ψ dt / ρ_b,BBN ≈ 0.12 (MD14 Salpeter) to 0.24 (Croker's ×2 SFRD).
- P2 needs 30% of all baryons. Report the fraction of P2's depletion that could at most come from the condensed phase, and
  the residual diffuse deficit this implies (B_pred,escape).

## Classes
- **ROBUST** if P2 stays ≥ 3σ excluded in every variant V1–V5 AND in V6, with the escape-route B_pred.
- **WEAKENED** if V6 or the escape route takes it below 3σ but ≥ 2σ.
- **NOT ROBUST** if any variant is below 2σ.

## Controls
- K1: the V0 re-run reproduces CFG779's ln B = +0.062 (+0.010, +0.115) to 0.005.
- MUTATE (CFG786_MUTATE=1): mocks with B = 0.71 under the V6 settings. The fit must recover ln B within 0.1 of ln 0.71.

## Hand estimate
V6 moves B̂ by ~5–8%, so the P2 exclusion becomes ~5σ. The escape route closes at most half the deficit. **ROBUST**,
or WEAKENED at worst.

## Machine
Run after T1x (~5 min). κ fitted; not theory closed.
