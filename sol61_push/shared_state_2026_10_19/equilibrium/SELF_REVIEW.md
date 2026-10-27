# Focused author proof, computation and prose review

Date: 2026-10-19. Scope: EQUILIBRIUM.md §§1–7, the executable finite contract,
parameters and run_002 outputs. This is author self-review, not an independent
agent audit. The parent and mode lane may attach separate focused reviews.

Claim card: positive tau,K,Kb,G and two finite strictly positive masses;
nonnegative scalar density with finite L1/L2/Fisher terms, baryons with finite
L1/L5/3 terms; shared Newtonian energy (3), two separate mass constraints.
Conclusion is existence of a full constrained energetic minimum, including a
centered spherical representative. It is not uniqueness, orbital/asymptotic
flow stability, formation or an assertion outside the NR/dilute EFT regime.

Dependency and obligation checks:

| Step | Result |
|---|---|
| Daughter contact and density normalization | Passed against the inherited matched coefficient; scalar T and K have mass-density normalization, not particle-density normalization. |
| Degenerate baryon pressure and energy | Recomputed phase-space integrals; B=(3/2)int P and h=(5/2)Kb rho^(2/3). EOS is declared environmental input. |
| Lower bound | Passed: near-kernel exponent 1/5, optimized D bound exponent M^(7/6), scalar interpolation A^(2/3), gravitational coercivity powers A^(1/3),Cb^(1/2). |
| Rearrangement arrows | Source-checked exact nonnegative-function and H1 hypotheses; mutual term included. |
| Radial weak-limit Coulomb continuity | Passed: exterior bound 2M²/R, singular-kernel contribution O(epsilon^(1/5)), smooth compact kernel product approximation; no false inference of strong local L5/3 convergence from weak convergence. |
| Quantum lower semicontinuity | Passed: Fisher convex dual formula has correct minus divergence and square coefficients; equivalently H1/local compactness. |
| No mass loss | Passed: smooth square annular profile; Fisher subadditivity permits overlap with scalar tail; baryon O(R^-2), contact O(R^-3); negative self-shell R^-1 works even zero surviving core. |
| Euler equations | Recomputed factor 2K in scalar equation, baryon exponent3/2, one Poisson source, separate multipliers. |
| Stability | Restricted to exact constrained energy minimum, nonnegative tangent Hessian, and explicitly conditional Hamiltonian spectral implication; no positive internal gap or full nonlinear orbit theorem inferred. |
| Common cutoff | Correctly requires equal multipliers only in TF; arbitrary ODE branch member not claimed to be minimum. |
| TF minimum-set limit | Recovery by smooth mass-preserving approximations and no-loss compactness; subsequence limits are minima and internal-norm convergence follows; no boundary/mode convergence claimed. |
| Numerical finite assertion | Four TF and six GP/BVP cases, deterministic; small exact n1 control, Poisson flux, independent mass and virial quadratures, two boxes/tolerances. No global optimality or Hessian spectrum claimed. |
| Full physical source | Shared COM zero retained; trial relative curvature not promoted to mode or independent spring. |

Computation outcome: **implementation and finite assertion verified in the
stated range, conditional on floating tolerances**. Current bounded runner
record run_002 completed in 0.566710 seconds, with wall45s, CPU30s per process,
one requested library thread, 65536 log bytes, no hard memory/affinity cap.
Manifest current-input hash validation passed. Python3.9.6, NumPy1.26.2,
SciPy1.11.4 on macOS arm64 were observed.

An earlier run_001 passed the same numerical cases. Self-review found that its
n1 errors were reported but not explicit assertions, and that the TF eta-family
EOS convention needed clarification. The code now asserts those error limits,
the contract distinguishes eta-family controls from the fixed-Kb GP controls,
and run_002 pins the corrected inputs. Historical run_001 remains preserved;
its old script hash is stale relative to the current script, so it is not
the current regenerable evidence record.

Mathematical verdict: **proved as written** for the reduced-model constrained
minimum proposition, subject to the two checked standard rearrangement inputs
and the explicitly specified admissible domain. The physical original-action
application is **conditional on the named EOS/state/EFT inputs**. The broader
dipole/population/saturation/normalization objective remains open.

Proofread in self-review mode: changed files in this lane only. Corrected a
potentially ambiguous TF eta/EOS sentence and made n1 test bounds explicit.
No unrelated source, manuscript, navigation, ledger or global history was
modified. Remaining restrictions are mathematical scope statements, not hidden
permission or unfinished code checks. No novelty claim is made.
