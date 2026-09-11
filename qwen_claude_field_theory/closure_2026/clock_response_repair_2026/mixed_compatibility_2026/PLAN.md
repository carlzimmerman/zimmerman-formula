# Attribute the mixed clock derivative before changing evolution

Base `38cb06700`. Previous goal turn: progress (fresh-state evidence, same-action
constraint energy, Lean leaves, and numerical cancellation regression).
Full single-action relativistic MOND closure remains the objective.

The 513-point curvature-rate tangency error and mixed chi derivative defect
both increase. Correlation is not causation. Differentiate the actual radial
constraint ODE again and replace only the supplied time derivative of chi_rr
by the action's mixed-derivative value. All other rates, coefficients, source
profiles, and center data stay fixed. Integrate a sign-reversed forcing control
alongside it to test linear response and indexing.

This is an error-attribution experiment, NOT a physical corrected trajectory:
independently replacing a derivative jet need not come from an integrable
chi_r time-rate function. If it removes most of the discrepancy, construct a
compatible spatial discretization and re-evolve; do not promote the injected
jet to a physical solution. If not, isolate other field/metric jet differences.

Inputs are the current-action fresh offset states at 257 and 513, with the
129 state as a resolution control. Float64/complex128, t=.02, directional
step1e-5, original background and source parameters. Individual runs capped
at120s with one cooperative numerical-library thread. No empirical fit,
coefficient reconstruction, or new Lean gravity certificate is implied.

Completed: component attribution; exact integrated primitive; conditioned
staggered primitive; fresh three-grid evolution; shared-product origin probe;
exact symbolic spline-join matrix; two Lean algebra implications. See REPORT.md.
The full-origin convergence gate still fails. No production evolution change
is authorized by these results. The interval-analysis Lean draft is separately
marked unverified after an import-cache failure.
