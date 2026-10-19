# Self-review and delivery boundary

Proofread: REPORT.md and RAW_DERIVATION.md in this lane, including the displayed formulas and source locators. This is a self-review, not an independent proof audit.

- Routine edits: removed a dangling introduction before the Euclidean vacuum identity and clarified the general-path sign derivation.
- Mathematical-token correction: in the newly added sign paragraph, replaced the ambiguous statement `M_alpha=H_p[K]` with `dM/dalpha=H_p[X]` for a general path with action derivative X, followed explicitly by zero when X=K is the constrained path. The preceding definitions already distinguish the nonzero partial M_alpha from the zero constrained total derivative.
- Unresolved physical obligations: the QCD vacuum insertion, quark/proton matching derivatives and sphere charged-state prescription have not been evaluated. The regularity/interchange conditions for the small-H limit remain conditional.
- Validation: run_001 has 19 passing exact symbolic checks and 2 passing numerical checks. Its v2 manifest validates with current file hashes. All eight supplied input hashes remain unchanged.
- Source checks: exact primary versions and geometry/formula locators were read. Public PDFs are temporary only; SOURCES.json holds observed PDF/text hashes. No novelty claim was made.
- Provenance limitation: Git commands were excluded. The manifest explicitly marks the commit unavailable and its dirty Boolean conservative rather than observed.
- Numerical limitation: the Ewald omitted-sum bound is analytic; floating roundoff is not interval-certified.

The finite-volume calibration cancellation is exact for the difference of the flat baselines. It does not assume an intrinsic vacuum response is absent, and therefore does not exclude one. The report's A_art is the coefficient in evaluated energy/stress, while a total metric derivative along retuned couplings would generate a different, inappropriate pseudo-stress coefficient.
