# CFG809 clarification, addendum D (2026-10-21; before any programme 2025.1.01377.L data; nothing frozen edited)

**Why.** Addenda B and C tried to score the true run's mask in the shifted window against a null. Every version inherits the same
problem: that mask was selected on the true window. B's null had the wrong scale. C's null depends on which source model is
injected (CFG942, 88db01f47: Gaussian copy +3.36, thin-disc copy +2.35). Both statistics are withdrawn for the verdict.

**Ruling (replaces B and C for MUTATE).** MUTATE re-runs G1 itself in the shifted window, exactly as CFG806-U4 does:
1. grow a fresh ≥ 2σ mask at the shifted window;
2. take the continuum per addendum A §2, with true-line channels excluded;
3. compute the S/N against the selection-aware null of A-G13.

The control bites if that S/N is below 3. This is FROZEN_CRITERIA §5's "the shifted flux must drop below 3σ", read with a mask
grown where the flux is measured. It uses the same machinery for both targets, and no reused mask is involved.

The A, B and C statistics, and the mask sizes, are printed as information.

If G1 fails at the true redshift, MUTATE is non-diagnostic (§5). If the shifted window falls outside the spectral window, the A-G11
fallback applies.

**Cross-reference.** CFG806 addendum A's sentence "if a selection-aware null shows the same continuum-selection bias as CFG809
addendum B describes, the same null-calibrated statistic applies here" is superseded. U4's MUTATE is decided by G1's
selection-aware S/N, as it already was. In U4 that coincides with this ruling.

κ = ½ fitted; footings never pooled; cold energy mass required; not theory closed.
