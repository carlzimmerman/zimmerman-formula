# CFG447: does Gaia DR3 already exclude the law acting as a force with NO external-field effect? FROZEN before any script exists

Owner chat 10-06 ("keep going"). κ = ½ fitted; both footings. No DM particle. Read-only use of the frozen DR4 pipeline: `prep_2026/gaia_dr4_prep/wide_binary_pipeline.py` is imported, never edited. **This is not a DR4 result and not an amendment.** It uses the record's DR3 dry-run numbers only.

**Why.** Three readings of the law meet three facts:
- cm14b: cluster satellites keep the full phantom; the host-EFE reading is excluded at χ² 99.7/5.
- wide binaries: the DR3 dry run (dr4_ready_1/DRY_RUN_2026-10-03.md, builder build of 6,210 pairs) gives γ̂ = 1.0750 ± 0.0550 canonical / 1.0775 ± 0.0512 alt; literal build 1.1175 ± 0.0625 / 1.0875 ± 0.0537.
- A force reading must take the EFE in wide binaries but not in satellites. Without the EFE, the isolated law's velocity boost √ν(y) grows without limit at low y.

This lane measures what the frozen estimator would return for an EFE-blind force.

**Injection (the only change, made in this lane's own code).** Mock pairs come from the pipeline's `make_population` with DR3 noise (`dr4=False`), N = 6,210 kept. The velocity boost is applied to the TRUE relative velocity at the TRUE 3-D acceleration exactly as `vtilde_of` does, but with γ(y) = √ν(y_true) in place of the EFE-saturated `gamma_of_y`.
- ν = ν_mono (CFG4_common), primary; ν_P2 (√(1/4 + 1/y) + 1/2 form) reported.
- Both footings.

**Recovery.** The pipeline's own `model_medians` (master from `make_population(…, dr4=True)`, as catalog runs use) and `run_fit` / `fit_gamma` on GRID 0.90–1.50, unchanged. Master size NM = 1,000,000 (declared; the pipeline uses 3e6, but the machine is shared). 10 independent mock realisations, seeds 47001–47010; report the median recovered γ̂ and its spread.

**Verdict.** EFE-BLIND FORCE EXCLUDED BY DR3 if (median recovered γ̂ − 1.0750) / √(0.0550² + spread²) > 5 on the canonical footing, and the alt equivalent against 1.0775 / 0.0512, using the builder build (the literal build reported). A recovery pinned at the grid top (1.50) counts as γ̂ ≥ 1.50. NOT EXCLUDED otherwise.

**Controls.**
- K1: injecting the pipeline's own EFE-saturated boost at Arm A's 1.1614 (canonical) recovers within max(2σ, 0.02), as the pipeline's GATE requires, with the same master and noise.
- K2: the pipeline file's sha256 is recorded before and after the run (unchanged).

**MUTATE (`--mutate`).** Inject ν = 1 (Newton). The recovered γ̂ must be within 0.03 of 1.00; exit 1 when detected.
