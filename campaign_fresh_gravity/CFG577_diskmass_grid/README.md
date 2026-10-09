# CFG577: DiskMass σ_z with the grid solver. INCONCLUSIVE as frozen (calibration gate fails again); the Υ gate works

- **Criteria:** `FROZEN_CRITERIA.md`, committed alone first (d0473b924). (owner chat 10-09, "yes set it up")
- **Script:** `cfg577_diskmass_grid.py` → `cfg577_diskmass_grid.out`, `cfg577_results.json`; MUTATE `CFG577_MUTATE=1` (a0 × 10 in RM) → `_MUTATE`; `cfg577_calib.out` from the calibration-only run. About 90 s.
- **Re-used by execution, unedited:** CFG576's table parsing (data in `../CFG576_diskmass_sigz/data/`) and CFG516's grid models (CFG514 solver, ν_mono, PD = full QUMOND, RM-φ).
- **New relative to CFG576:** exact line-of-sight-weighted vertical Jeans integral with each model's full K_z(R, z); Υ_K fitted to each model's own in-plane speed; Υ_K plausibility gate.
- κ = ½ fitted; both footings, never pooled; cold energy's mass still required; not theory closed.

## Result (median σ_pred/σ_meas, 30/30 galaxies fitted in every primary cell, bootstrap 68%)

| footing | radius | RM (median Υ_K) | PD (median Υ_K) |
|---|---|---|---|
| canonical | 1.5 h_R | 1.342 [1.272, 1.377] (0.52) | 1.551 [1.476, 1.626] (0.55) |
| canonical | 2.2 h_R | 1.303 [1.162, 1.400] (0.46) | 1.579 [1.455, 1.737] (0.46) |
| alt | 1.5 h_R | 1.315 [1.242, 1.341] (0.48) | 1.557 [1.481, 1.632] (0.51) |
| alt | 2.2 h_R | 1.273 [1.147, 1.362] (0.41) | 1.586 [1.466, 1.749] (0.41) |

Newtonian reference (C2): 1.508 at Υ_K 0.90. Variants (canonical 1.5 h_R): h_z × 0.75 → RM 1.152, PD 1.343; no gas →
RM 1.288, PD 1.492.

## Verdict as frozen: INCONCLUSIVE
- **G-cal FAILS:** PD alt median 1.557, outside [1.15, 1.45]. The exact Jeans integral raises every model by ≈5–7%
  over CFG576's one-zone estimate, moving PD further from the window.
- **C3 FAILS (6%, tolerance 5%):** on a finite Newtonian exponential disc at 1.5 h_R the Jeans integral gives
  20.73 km/s against the infinite-slab 1.5 π G Σ h_z value of 22.08. DMS's slab k = 1.5 is itself ≈6% optimistic here.
- **MUTATE DETECTED:** a0 × 10 in RM reaches r ≈ 1.05–1.07 only at Υ_K 0.065–0.085 with 21–24/30 fitted; the new
  Υ gate rejects it. CFG576's weakness is fixed.
- C1 passes (grid stellar mass to 0.06%).

## Reading (not a verdict)
- Every model over-predicts σ_z at DiskMass's adopted scale heights: RM by ≈30%, PD by ≈55%, Newton by ≈50%,
  all at plausible Υ_K. RM is the closest, at every radius and footing.
- The calibration window was mis-specified: Angus et al. 2015's "≈1.3" is a summary of fits in which h_z was free
  (they needed h_z of 200–400 pc, about half the adopted values). At the adopted h_z, PD's 1.56 is what their
  finding implies (halving h_z scales σ by 0.71 → ≈1.1). Re-anchoring the gate to their actual per-galaxy fits
  would be a new, separately frozen lane; it is not done post hoc here.
- Whether RM's remaining ≈30% is physics or DiskMass's σ_z/h_z systematics (young-tracer contamination of σ_z;
  inferred h_z) cannot be decided here. Do not cite this lane as a round-rule win.
