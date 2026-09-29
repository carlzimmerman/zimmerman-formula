# CFG170 — the two-epoch gas-ratio test: the gas evolution each a₀ law needs between KROSS (z ≈ 0.85) and KURVS (z ≈ 1.5), against the measured evolution. FROZEN CRITERIA

Written 2026-09-29, at the orchestrator's go, before any break-even of this lane has been computed. Nothing below may change after a result is seen; any later deviation goes in the README as a disclosed departure.

## Forking paths and multiplicity (stated first)

- **This lane analyses data already seen.** Six earlier lanes have analysed these same two samples: CFG140, CFG141, CFG160, CFG161, CFG162 and CFG164. There are also the single-disc gas tests CFG142 and CFG163, and the Opus chat's referees CFG165–CFG168.
- **What was known before freezing:**
  - CFG161's post-hoc rows: at a common μ = 0.67 under P4, flat fits KROSS and the rival fits KURVS;
  - CFG162's break-evens for KURVS (μ = 2.11 flat and 0.62 rival at s = 1);
  - a hand estimate that flat needs R ≈ 3, from my proposal.
- **The commitment:** R_flat, R_rival and R_obs are reported whatever they show, for every prescription listed below. A wide R_obs bracket that makes the test non-diagnostic is a valid answer.

## The question

Each law fits a sample only at its own break-even gas fraction μ_be. So each law needs the gas to change by R_law = μ_be(KURVS)/μ_be(KROSS) between z ≈ 0.85 and 1.5. Is that consistent with the measured evolution, R_obs?

## The statistic (declared)

- **The pipeline:** CFG141's, exec'd read-only and unmutated except by this lane's own MUTATE. The P4 functions are CFG160's, copied verbatim. The cell is δ = 0, canonical, anchor-corrected by SPARC with its measured gas at the same s.
- **KURVS:** the ten discs with CFG141's measured σ_out.
- **KROSS:** the 390 discs (CFG140's selection), with σ₀, at R = 2r_im.
- **The prescriptions:** s ∈ {0, 1.00, 1.42, 1.62, 1.69, 3.00} × Kretschmer's α, i.e. CFG162's placements of none, Kretschmer, Dalcanton & Stilp, fixed height, Price and self-gravitating.
- **μ_be:** the root in μ ∈ [0.01, 30] of Δ′(μ) = 0, found by brentq on a log-bracketed grid. If no root exists in the range, that is reported as "no break-even".
- **The root-find error:** the roots of Δ′ = ±σ_Δ′, giving a 1σ interval on μ_be.
- **R_law** = μ_be(KURVS)/μ_be(KROSS). Its interval is conservative: [μ_lo(KURVS)/μ_hi(KROSS), μ_hi(KURVS)/μ_lo(KROSS)].
- **The calibration scatter:** for Kretschmer's prescription, R_law is also given at s = 0.6 and 1.4.

## R_obs, the measured gas evolution (declared)

- **In-repo (primary).** The PHIBSS fit (CFG166; checked in the CFG164-corr row) on the 51 clean rows is log μ = a − 0.30 (log M* − 10.5) + e log(1+z), with e = +0.23 ± 0.52.
  - So R_obs = [(1 + z_KURVS)/(1 + z_KROSS)]^e × (M*_KURVS/M*_KROSS)^(−0.30), using the samples' median z and M* computed at run time.
  - At the median redshifts 1.53 and 0.85, the redshift factor is 1.3676^e: 1.08, with 1σ [0.91, 1.27] and 2σ [0.78, 1.49].
  - **The "1.1 ± 0.6" in my proposal was shorthand, not derived.** The derived bracket is the one used.
  - The PHIBSS z ≈ 1.2 and 2.2 samples were selected differently, so e is not a clean evolution measure. That is a caveat, not a correction.
- **The literature value, abstract-level only.** The abstract of Tacconi et al. 2018 (arXiv:1702.01140, read as the arXiv HTML abstract page) states μ_gas ∝ (1+z)^2.5 × δ_MS^0.52 × M*^−0.36, and that "the redshift dependence of mu_gas requires a curvature term".
  - The full relation with its curvature term could not be read: there is no HTML full text; ar5iv redirects and arXiv HTML returns 404.
  - So R_obs,lit = 1.3676^2.5 × (M*_KURVS/M*_KROSS)^−0.36, with δ_MS assumed equal. It is labelled ABSTRACT-LEVEL.
  - It carries a declared ±20% allowance for the unread curvature term and δ_MS. This is an allowance, not a measured error.

## The pass/fail rule (as the orchestrator set it)

- **A law is "disfavoured" against a bracket** only if its required R lies outside the R_obs bracket by more than its root-find error. That is, the gap between R_law and the nearest edge of the bracket exceeds R_law's 1σ half-interval on that side.
- **The in-repo bracket** is the 2σ interval [0.78, 1.49] × the mass factor. **The literature bracket** is R_obs,lit ± 20%.
- **Both brackets are applied, and each law is reported against each,** at every s.

## What cancels and what does not (stated before the data)

- **Cancels in the ratio, largely:**
  - the α_CO and M* scale systematics, common to both epochs;
  - the SPARC anchor, applied identically;
  - part of the pressure prescription's normalisation.
- **Does NOT cancel:**
  - the pressure at different radii: KROSS at x = 1 (α = 2.53 s), KURVS at x = 1.0–3.5 (α = 2.6–3.9 s);
  - the different selections: KROSS from Hα narrow-band and spectroscopic samples at z ≈ 0.85; KURVS from KGES/KMOS3D rotation-supported discs;
  - the different instruments and velocity definitions: KROSS's model velocity at 2 R_half against KURVS's outermost measured point;
  - the dispersion input: KROSS's σ₀ against KURVS's measured σ_out;
  - the different stellar-mass pipelines.

## Checks

- **C1 CONTROL:** KURVS's break-evens at s = 1 reproduce CFG162's committed values (2.109 flat, 0.621 rival; to 1e-3).
- **C2 CONTROL:** at μ = 0.67 and s = 1, KROSS's anchor-corrected Δ′ reproduces CFG161's post-hoc row (flat −0.004, rival −0.082; 3 decimals).
- **R0 POWER** (printed before any comparison): |log R_flat − log R_rival| at s = 1, against the log-width of the in-repo 2σ bracket.
- **H1 [HEADLINE, reported]:** the matrix of disfavoured/not for each law, bracket and s. The declared summary is:
  - at s = 1, a law is "disfavoured by both brackets" only if both flag it;
  - the test is DIAGNOSTIC only if exactly one law is disfavoured by both brackets at s = 1;
  - otherwise it is NON-DIAGNOSTIC.

## MUTATE (two pinned controls of the evaluator)

- **MUTATE=1:** R_obs is replaced by R_flat(s = 1) with the in-repo bracket's relative width. Flat must then be "not disfavoured".
- **MUTATE=2:** R_obs is replaced by 10 × R_flat(s = 1). Flat must then be "disfavoured".
- Each run exits 0 when it behaves as required.

## Readings (declared)

- **Diagnostic** means the two epochs' break-evens are consistent with the measured gas evolution for one law and not the other. This is conditional on the prescription, the selections and R_obs's definition, and it is not a kill line.
- **Non-diagnostic** is a valid answer: for example, when the R_obs bracket is wide or when the two brackets disagree.
- **Untested (declared):**
  - the curvature term of the literature relation;
  - δ_MS differences between the samples;
  - the KROSS gas (only the break-even is used);
  - pressure beyond the placed prescriptions;
  - the COSMOS half of KURVS.

κ = ½ and Ω_c h² stay fitted. Nothing here says the data favour either model, or that the theory is closed.
