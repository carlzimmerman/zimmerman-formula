# Independent review and claim boundaries

Review scopes below are separate from implementation reports. The coordinator
reconciled them against actual sources, records, and fresh scoped checks.
They are not certifications of the microscopic physics or full continuum PDE.

| Review scope | Outcome and limitation |
| --- | --- |
| Energy, entropy and quiet gating | Independently checked shared-flux cancellation, stress/heating work balance, nonnegative entropy production, and zero local inactive terms. Moving interfaces and actual forest observables remain distinct obligations. |
| Selected outward gated flux | Independently checked monotonicity in supplying/receiving K and the global minimum principle for valid geometry. A cold center with only an outer heater is a counterexample to automatic seeding. A positive central-prefix bound needs guard control. |
| Thermal alternative | Persistent transport equilibrates physical T rather than K and allows an integrable ordered cusp with K tending to zero. Neither entropy production nor damping alone proves a core. |
| Raw refinement and settling | Independent reconstruction of real absolute windows, cell-prefix/guard mapping, four-grid metrics, source hashes, restart joins and original-energy lineage. No solver-output extrapolation to infinite N or t. |
| Cold invariant phase | Independent source/regression audit of the exact pre-heating dust subsystem and warm handoff. Coupled-solver leakage motivates this path; its isolated numerical cause is not certified. |
| Perturbation continuations | Verified preparation work, retained capped statuses, exact-state restarts, actual SciPy BDF and unchanged physical RHS/parameters. All requested endpoints completed; this is controlled radial relaxation, not a full spectral stability calculation. |
| Isentropic predictor | Independent pressure/mass ODE and energy quadrature agree with the regular mass/energy-only endpoint. Envelope and stationary-ordering arguments are conditional; global branch admissibility, order preservation and convergence are open. |
| Final analysis | Independently recomputed density span/drift, floor mapping, restart SHA/continuity, and sampled energy errors. Review identified that accepted-state bounds did not bound dense-output samples. V2 preserves v1 and reports both diagnostics accurately. |

The final read-only analysis audit validates the v2 manifest, exactly
reproduces its saved summary, and checks its actual sample starts and
preparation exclusions. Accepted-state and sampled energy errors pass the
declared finite tolerance. The tighter-time energy diagnostics were directly
reviewed; its automatic criterion only gates profile agreement.

The previous frozen-entropy radial stability theorem cannot simply be applied
to this transport: at neutral K ordering an arbitrarily small adverse entropy
perturbation can activate flux at first order. Positive fixed-K stiffness,
semidiscrete dissipation, and the measured relaxation tests are the evidence
claimed here. A full coupled-mode or global nonlinear stability theorem is
not supplied.

Final mathematical self-proofreading covers the new README, methods,
conditional endpoint and status documents. Routine notation/link consistency
is distinct from the independent correctness audits above. All exact
numerical claims are attributed to the linked finite records, not to a
literature theorem. See [VERIFICATION.md](VERIFICATION.md) for fresh commands.
