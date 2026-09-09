# IC46 closeout: numerical obstruction, full theory OPEN

## Verdict

This is a reproducible failed convergence checkpoint, not a completed relativistic MOND theory and not a universal no-go. The user requested a closeout with 7% credits remaining; no further research sweep is being launched. Mathbox computation/proof-audit discipline requires separating a completed integrator, a valid evidence manifest, and a mathematical closure proof.

The strongest preceding analytical checkpoint remains IC44's action-derived, noncharacteristic two-phase transmission solution, with computed determinant -64 K^2 V^2 u^2/9 (a transmission matrix, NOT a Poisson-bracket matrix), and IC45's independently varied angular equation and compatible second-time auxiliary acceleration. These are local necessary/finite-order results. They do not establish full Dirac closure, a global solution, or all physical gates from one action.

## What IC46 actually tests

The same fixed IC39 coefficients and IC41 initial data are used. IC30/45's unpinned radial/angular equations and exact timelike fluid Legendre inversion advance independent canonical fields in two phases with RK4. Three auxiliary fields are solved at every stage on a moving Chebyshev mesh. The active level set determines interface speed.

Six imposed auxiliary boundary conditions are: inner S and w values, outer S value, continuity of S and S_r at the interface, and inactive w=w_c at the interface. Endpoint values are prescribed using IC45's second-time Taylor data. The remaining w_r joining condition, canonical trace equality, physical metric gradient jumps, and momentum constraint are measured, not projected. Thus junction_projected=false does NOT mean all interface conditions are unconstrained. Canonical endpoint evolution uses one-sided collocation, not a derived characteristic boundary prescription.

## Results preserved without retuning

All three absolute-field probes reached t=2e-7 with width 3e-5. Values below are final, unscaled all-node constraint maxima and signed active reaction.

| Run | Nodes | dt | Steps | max abs C | max abs W inactive | active reaction |
|---|---:|---:|---:|---:|---:|---:|
| coarse | 7 | 1e-8 | 20 | 2.2254e-6 | 1.9585e-6 | 7.0935e-6 |
| time_half | 7 | 5e-9 | 40 | 1.7019e-6 | 4.5949e-6 | 1.9001e-5 |
| space | 9 | 5e-9 | 40 | 1.6619e-5 | 2.2925e-5 | -5.7834e-5 |

There is no demonstrated convergence. The initial collar already has reaction errors around 1e-5 despite its zero-reaction construction. Differentiation of absolute fields on this thin domain is a suspected roundoff contributor, not a proved sole cause. Scaled interior solve residuals near 1e-15 do not control the unscaled physical residuals or omitted endpoint equations.

A separate centered-coordinate implementation preserves the frozen equations and original runs. Its proposed regression FAILED: the auxiliary root solve stalled at scaled residual 1.96569e-11, above the unchanged 2e-12 acceptance threshold. We did not loosen the threshold or turn the failure into an expected pass. The failed test is intentionally retained.

Earlier development attempt width .001 left the fixed coefficient cell (0.10247152233147314, 0.10255550152117493): active-side initial S reached 0.10240247621043982. The width was reduced before freezing the raw evidence; no coefficient extrapolation or action change was made. The contract's planned 100-step case was NOT run.

## Verification and scope

Raw three scientific commands deliberately exit 2 under --strict because full_theory remains OPEN; their evidence runners exit 1. The centered regression genuinely fails (child exit 1). The combined four-test run and manifest validations are recorded in run_index.json. Original development tests: absent-module red exit 1, invalid-domain exit 1, corrected original three-test suite exit 0; centered development red and implementation tests exit 1.

No empirical comparison, novelty certification, full PPN derivation, nonlinear Dirac preservation, homogeneous-sector count, causal/global stability theorem, or complete cosmological construction was established by IC46. No claim from concurrent Fable work is imported as a result for this action.

## Next unavoidable work, if funding resumes

First establish a numerically conditioned auxiliary boundary problem with independent time, space, and arithmetic-precision convergence and constraint/junction error control. Then prove finite-time existence and constraint preservation for the actual moving-interface problem, including characteristic/zero-speed and zero-field limits. Even success there leaves the same-action full Dirac, homogeneous, PPN, causal stability, and empirical gates. Do not resume by declaring the finite-order Taylor construction a full theory.
