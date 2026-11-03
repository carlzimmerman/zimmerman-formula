# Self-audit at the phase boundary

κ = ½ FITTED; not theory closed

Evidence checkpoint: 38835782664077d53810b4e162b9d896b3377a4a. Review provenance: self-review by the implementing agent, not independent review. Scope: the eleven AZ assertions, their raw scripts/results, and their implications for this goal. External literature theorems are not load-bearing; internal prior-record claims are attributed rather than re-proved. Numerical assertions remain finite unless an explicit analytic argument is given.

Primary verdict for the goal-level claim of a new complete survivor: **incomplete, with the smallest missing implication** being a single action-derived, regular local rule that survives all affected observational gates. No result is a proof of closure. Individual obligations:

| Claim | Dependency chain and audit outcome |
|---|---|
| AZ1 isolated estimator | Newtonian Hessian -> tau derivative -> exact point-mass mass -> fixed Gaussian filter -> old integral. Identity passed; physical solar interpretation conditional on external field. Uniform-core extension absent. |
| AZ2 conservative operator | Symmetric flux matrix / positive bilinear form -> mass/constants/reciprocity. Passed on stated periodic/prescribed-D class; full gravity action not addressed. A resolvent is not a Gaussian. |
| AZ3 peak/centroid | Fubini and change of variables with finite moments -> centroid identity; complete-square Gaussian -> peak zero. Passed for stated single clump. NOT extended to arbitrary multi-clump peaks. |
| AZ4 quartic shear | Trace-free projection -> quartic energy -> cubic stress. Passed; isotropic contraction counterexample refutes only a universal LOCAL shear cure. Boundary propagation not addressed. |
| AZ5 snapshot | Direct Vlasov differentiation -> moment integral. Passed; distinct positive harmonic forces admit same initial snapshot. Real tracer history unmeasured, so no empirical rescue. |
| AZ6 compensation | Projected mass definition -> annular cancellation. Passed. Native redshift weights and outer inventory remain dependencies; processed ESD not silently accepted as raw. |
| AZ7 compression | Declared mechanical Lagrangian -> Legendre energy -> positive-root speed -> finite integral. Passed in reduced model. General power asymptotic requires p>4/3 for nonlinear dominance, with separate kinetic-dominated 1<p<4/3 case; final derivation states this explicitly. No full covariant inference. |
| AZ8 variation | Periodic integration by parts -> extra D' term -> manufactured field comparison. Passed; shortcut refuted. Separate-field D(Phi) is different and not excluded. |
| AZ9 cusp | Green ODE/normalization -> enclosed fraction -> constant-magnitude central field. Frozen absolute convergence fails; NO VERDICT retained. Inner samples suggest cutoff divergence but are not a converged exclusion. |
| AZ10 regular kernel | Squared resolvent -> exponential Green function -> finite central density -> reduced quadrupole. Finite numerical PASS under both external conventions, 18 controls pass. Full action / local D / MW absent. |
| AZ11 radial monopole | Divergence-source Gauss law -> angular average -> small-h response oracle -> diagnostic bounds. Controls passed. Published acceleration conversion assumes constant force: pre-result A1 prevents treating point-radius Z as a full ephemeris likelihood. |

Known-answer and MUTATE checks test actual equations/invariants. Algebra-only identical footing entries are explicitly invariant under the change of a0; they are not two independent datasets. Synthetic controls are not empirical evidence. AZ9 has failed controls and cannot be promoted by the size of its raw number. Current manifest validation is provenance validation, not proof validation.

Two provenance defects were found and disclosed: AZ1 initially omitted declared_results; AZ3 omitted tested bounds in the manifest. Original invalid manifests are preserved, repeat records now validate, and no physical threshold was changed. AZ1 repeat result was byte-identical. No first-run success is retroactively fabricated.

Coverage audit found a third record issue: RQ3's prose says 96, but row_marks.json expands to 99 after A23/A26 splits. `coverage.json` preserves all 99 and separately aggregates 96 groups. The zero credited coverage is unchanged. The prose and other sessions' data remain untouched.

Proofreading self-review: all newly written derivation/status/summary files checked for defined signs, footing conventions, units and restricted scope. No mathematical-token correction was hidden as copyediting. The p-range distinction above was supplied during derivation and is stated openly. No claim that a numerical grid proves the full field equations. Remaining reviews: independent mathematical review, full solar orbit response and a regular covariant completion are absent.

See VERIFICATION.json for fresh script reproduction, input/output-hash validation, criteria-before-script Git ancestry, six status files, coverage shape, and privacy/write-scope checks. Passing those checks certifies the requested artifacts and finite runs, not the physics.
