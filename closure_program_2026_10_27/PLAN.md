# Closure corrections and M6 population test

User-authorized execution, 2026-10-27. Base checkpoint:
`eee9769579834ae78531ee37adc3970090ac81da`. Specification:
`reviews/claude_closure_audit_2026_10_27/REPORT.md` and the user's instruction
to fix its issues and execute the closure sequence, starting with M6.

**Target.** Determine whether the population of galaxies requiring M6 can fit
inside a physically allowed depleted-patch baryon budget without violating
measured forest data. A template upper limit alone is not a physical exclusion;
an empirical feasible profile alone is not a complete mechanism.

**Implementation.** Preserve historical frozen artifacts and results with
explicit post-result corrections. Use disjoint write scopes in the existing
research checkout because live results and untracked observational inputs are
shared here. Do not alter running P1D2 or X48 jobs. New evidence and scripts live
under this program or explicitly labelled correction files in their own lanes.
No blanket staging, commits, external messages, or expensive replacement jobs.

**Work packages and owners.**

- [x] `r4b_c6` agent: correct X57's band-entry/positivity inference, and X64's
  same-radius C6 proxy. First demonstrate failures using the saved inputs and
  analytic point-mass invariant; implement scoped fixes; run bounded corrected
  computations into separately named outputs. Own X57 and X64 only, plus
  `closure_program_2026_10_27/gate_fixes/`.
- [x] `population` agent: construct independently sourced lower bounds and
  explicitly conditional estimates for the baryons in the required galaxy
  population. Inspect local data before querying primary literature. Own
  `closure_program_2026_10_27/population/`. Record cosmology, IMF, selection,
  cold-gas conventions and uncertainties; never treat all galaxies as the
  required isolated subset without justification.
- [x] `forest_convergence` agent: fix P1D1's interpretation and independent
  sign-check, keeping its completed NOT DIAGNOSTIC result historical; add and
  test a nested-mode IC generator for future X48 convergence checks without
  changing running jobs. Own P1D1, X48 correction files and
  `closure_program_2026_10_27/technical_fixes/`.
- [x] Coordinator: repair headline/selector scope summaries, inspect P1D2's
  independent physical response, assemble the population-versus-forest test,
  and pursue the next discriminating check if no valid forest limit exists.
- [x] Coordinator: execute the necessary boundary-admissibility gate for the
  next common-profile dependency. The literal X38/SC1 cluster cutoff fails
  under the declared regular isotropic no-wall equilibrium interpretation;
  a positive local distribution-function witness shows a possible boundary
  repair, not a global fitted completion.
- [ ] Full common-profile observational feasibility: remains open. A replacement
  must specify a globally admissible distribution/potential and its changed
  outer projection before a joint fit can certify it. No independent per-object
  fit or arbitrary shell is substituted for this deliverable.
- [x] Independent review of material new implications and correction results;
  update this program's status/handoff with precise remaining obligations.

**Checkpoint outcome.** Corrections and the first M6 population decision are
recorded in `RESULTS.md`. M6 remains unresolved because its required selected
population and calibrated physical forest limit are both absent. The full
closure sequence remains open; `HANDOFF.md` records the exact next dependencies.
Technical run 001 is superseded by 002 after independent review found and fixed
the Fourier-support mismatch in the constraint covariance.

**Decision rules.** Close the specified M6 branch only if a justified required
population exceeds a calibrated allowed population on the same conventions,
or a separate physical obstruction applies to its actual model. An inadequate
forward model, weak sensitivity, finite failed scan or absent selection fraction
is not exclusion. Positive completion additionally requires dynamics from
admissible initial conditions, conservation, stable profiles, and independent
galaxy/cluster predictions. Kappa remains fitted unless separately derived.

**Verification focus.** Meaningful regression cases target band boundaries,
positive-shell shear, point-mass same-radius invariance, independent injection,
and shared Fourier modes across resolutions. Research runs record input hashes,
commands, ranges and outcomes. Avoid repository-wide test collection: this
repository contains executable research scripts with output side effects.
