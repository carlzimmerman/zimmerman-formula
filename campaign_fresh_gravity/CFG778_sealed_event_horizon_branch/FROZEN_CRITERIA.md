# CFG778 FROZEN CRITERIA: seal the event-horizon a0 branch for the November ALMA releases

Committed alone, before any script or number. 2026-10-14. Block CFG770–779.

## Why
Astra's follow-through of CFG775 (`sol61_push/claude_bh_followthrough_2026_10_14/REPORT.md` and `HORIZON_TREND_PROOF.md`) proves
the following.
- When matter converts to vacuum with total stress-energy conserved, a0 ∝ √ρ_V and a0 ∝ c²/R_E evolve **oppositely** (R_E is
  the actual future event horizon).
- At z = 2 its model gives 0.85 vs 1.44.

CFG571 sealed F-flat, F-DESI, R-H (a0 ∝ H) and L-fb; CFG775 sealed BH-k3. The event-horizon branch is not sealed. Seal it now,
before the U4_27928 (2026-11-06) and GS4_24110 (2026-11-28) releases.

## Declared calculation
- **Branch E (primary).**
  - a0(z)/a0(0) = R_E(0)/R_E(z), with R_E(z) = c a(z) ∫_t^∞ dt′/a(t′) in the framework's own constant-Λ background
    (flat, Ω_m = 0.308; this branch alone does not produce vacuum).
  - Exact integral in a: R_E(a) = c a ∫_a^∞ da′/(a′² H(a′)).
- **Branch E-CCBH (reported).** Astra's normalised event-horizon column from its conserved MD14 history: 1.3070 at z = 1.5,
  1.4399 at z = 2. Interpolated linearly in z at 1.419 and 1.997. Quoted from its REPORT.md, not recomputed here.
- **Predictions.** Required gas for GS4_24110 (log M* 10.89, 10.76) and the U4_27928 V_c grid (150–300 km/s), both footings,
  using CFG571's `predict` (imported read-only) with MODELS = {E, E-CCBH, F-flat, F-DESI, BH-k3, R-H}. Written to
  `SEALED_EVENT_HORIZON.json` with its sha256 in the README.

## Controls
- K1: R_E(0) for Ω_m 0.308 and h = 0.70 lies between c/H0 and c/H∞ (positive Λ). Also check dR_E/dln a = R_E − c/H at
  z = 0, 1, 2 to 1e-6.
- K2: the F-flat, F-DESI and R-H predictions reproduce CFG571's committed numbers for GS4_24110 to 1e-3 dex. This proves the
  import is unchanged.

## MUTATE (CFG778_MUTATE=1)
Ω_Λ → 0 (Einstein–de Sitter): R_E diverges, so the branch must be undefined (flagged), not silently finite.

## Hand estimate
Branch E ≈ 1.3–1.45 at z = 2, between flat (1.0) and a0 ∝ H (≈ 3.0). GS4_24110 required gas lies between those branches'
values.

κ fitted; not theory closed.
