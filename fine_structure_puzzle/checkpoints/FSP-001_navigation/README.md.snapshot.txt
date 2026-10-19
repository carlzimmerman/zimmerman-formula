# Fine structure puzzle

Launched **18 October 2026**, America/New_York. Checkpoint **FSP-001**.

**We have not derived the fine structure constant.** This first investigation produced a more precise set of possible mechanisms and several checks that distinguish an actual prediction from a numerical fit. Three research agents worked on separate routes, the coordinator did a fourth route, and a fresh agent reviewed the UV mathematics and numerical result. The programme remains open; completed assignments are recorded work, not background jobs still running.

## The most useful new lead

A [paper published in 2026 on mixed Abelian gauge fields and gravity](https://arxiv.org/abs/2512.12044) provides a concrete advance over the old scalar-coupling toys. Under its one-loop matter and phenomenological gravity assumptions, the fully interacting fixed point determines the **relative couplings and mixing** from the charged spectrum. We independently reconstructed this as `H*=16 pi^2 f_g B^-1`. The unresolved overall strength is the gravity coefficient `f_g`; the paper calibrates it using empirical hypercharge data. It therefore does not predict alpha's absolute value.

We went further than identifying that freedom: in a separate, restricted Standard Model calculation, we fitted gravity parameters to the top and bottom Yukawa couplings while withholding an explicit alpha/hypercharge number. It predicted `gY(mt)=0.312663`, versus a withheld reference `0.358735`, about **13% low**. Changing the assumed gravity crossover changed the prediction by about 2.5%. This is a useful failed correlation test at the stated approximation, not an exclusion of all asymptotic-safety models. The numerical inputs are phenomenological matched couplings, with dependencies that prevent treating this as a first-principles alpha derivation. The latest checked full-flavor model also has an additional relevant top-quark trajectory datum, so the restricted model's parameter closure cannot simply be carried over.

Read the [UV route](uv_selection/REPORT.md), [independent matrix review](reviews/UV_MATRIX_REVIEW.md), and [fresh numerical/algebra review](reviews/independent_uv/REVIEW.md). The fresh implementation evolves squared Yukawas and gauge inverse squares as ODE states; its central coupling agrees within about 4e-11. This checks the numerical result, not the model's physical completeness.

## What the other routes established

| Route | Executed result | What is still missing |
|---|---|---|
| [Archive audit](archive_audit/REPORT.md) | Reconstructed the scopes of the previous failures, reran two decisive scripts, and checked a hypothetical quantum-lifting potential. Found several overbroad or stale summary statements. | A changed physical premise that fixes the residual datum. Old failures are not a universal impossibility theorem. |
| [Spectral/emergence route](spectral_route/REPORT.md) | Derived and checked dispersion, screening, a finite spectral-band model, and local-coefficient counterfamilies. Checked modern bootstrap and exact string-emergence sources. | A UV theory and selected vacuum fixing the finite Maxwell coefficient and threshold ratios. Positivity and an integer charge lattice alone do not fix them. |
| [Physical normalization](normalization_gate/CLAIM.md) | Derived the massless propagator residue and showed that giving a hidden photon a mass changes the relevant coupling formula. Fixed kinetic eigenvalues alone can leave the physical charge coupling variable. Independently reviewed. | A candidate must fix the projected kinetic coefficient in its actual charge basis after symmetry breaking and matching. |

The prior plain summary's `Lambda*lP^2≈10^-12` is a transcription error: the archived calculation gives about `2.85×10^-122`. More substantively, its dimensional-analysis result concerns monomials; it does **not** forbid a physical mechanism selecting a pure number. Prior files were left in place; corrections are documented here.

The extra-dimensional stabilization continuation was also pursued to an actual quantum source, rather than left at a suggested ansatz: see [the Q3 source check](archive_audit/Q3_QUANTUM_SOURCE.md). Symmetric supersymmetric examples can have vanishing computed loop lifting; added brane/flux models introduce additional matching data. This is a scoped source result, not a general proof that quantum stabilization cannot work.

## Evidence and next step

The [target contract](TARGET.md) defines what would count as a solution. The [measurement baseline](sources/MEASUREMENT_BASELINE.md) keeps the Thomson limit and the conflicting atom-recoil determinations explicit. [Current run validation](reviews/MANIFEST_VALIDATION.json) checks the authoritative computation records and the intentionally failing controls. Historical launch/numerical failures are retained and labelled in their route reports. Counts of checks are not counts of independent physics proofs.

The next useful question is whether an explicit UV theory fixes the **remaining physical combination**, including its relevant trajectory and vacuum data, without using alpha. The exact unresolved steps and resumption conditions are in [HANDOFF.md](HANDOFF.md). [STATUS.md](STATUS.md) is the live programme view; [CHECKPOINT.json](CHECKPOINT.json) and [ARTIFACTS.sha256](ARTIFACTS.sha256) pin this launch investigation.
