# Focused independent computation reviews

Reviewer: existing `/root/envelope_data_review` subagent; read-only reviews requested under the code-review skill. No owner jobs or publications edited.

1. Conditional energy screen: reviewer independently integrated the target potentials with adaptive quadrature, agreeing with all four canonical target energies to 1.8e-11 in the stated dimensionless units. Virial signs, Gaussian initial kinetic term, Plummer amplitude term and common-infall threshold checked. Scope restricted to these complete stationary candidate profiles under the stated isolation/source assumptions.
2. Centered/Cayley and P9: mean endpoint gauge and energy/reversal controls checked. Unitarity does not imply arbitrary-frequency phase accuracy. RMS phase-span guard is not a spectral support theorem. P9's slower finite result retained; failed degree8 stiff-order control retained.
3. Solver acceptance fix: existing residual acceptance is 1e-10, and early exit at that threshold preserves it. Three controls independently passed against `kernel_gated.py`.
4. Continuation: initial review found missing wall-only, carrier and physical-source checks. Before any continuation started, added explicit wall-only status, exact carrier/grid checks, physical-unit matching, parent-source hashes, finite-state checks and instantaneous invariant gates. Reviewer then checked both registered parent checkpoints, exact complex restart, original invariant references, cumulative maxima and trailing history: no remaining blocker. Stellar continuation from a truncated post-birth run is not supported.

These reviews do not certify actual galaxy formation, full resolution, a cosmological chronology, or the parent action. The final packet records the executable audit separately.

5. Final-method review identified the missing fluctuation-binding term for a time-averaged density. ENERGY_SCOPE_CORRECTION.md narrows that interpretation while retaining the original frozen producer contract. Reviewer confirmed the correction and the finite sampled quadratic identity. Added deduplicated full-window/first-birth/history checks and lineage comparisons were re-reviewed.
6. Valid-prefix prolongation: independent reviewer reproduced the complex cubic reference-field transfer to 8.45e-17. This specific mass/energy transfer fails the stated limits. This is not physical mass loss, proof that every refinement method fails, or a proof that the earlier coarse trajectory is invalid. Corrected V2 differs from the retained failed serialization attempt only by conversion of NumPy Boolean to Python bool.

Self-proofreading covered MECHANISM.md and ENERGY_SCOPE_CORRECTION.md: checked notation, energy factors, density/current conventions and cross-references. No mathematical-token typo changes were needed; the fluctuation correction is a substantive separately documented review correction.

7. Final claim review checked RESULTS.md against all12 producers,208 profile rows,92 PM rows,33 comparisons,806 successful integrity/control checks and19 valid evidence records. No blocker found; late fine coverage, inactive stellar tests, numerical failures and lack of a parent-action bridge remain explicit.
