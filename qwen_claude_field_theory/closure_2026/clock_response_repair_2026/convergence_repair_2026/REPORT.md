# Fixed-action evolution convergence repair

User's order is binding: repair numerical convergence; then derive the
cosmological constitutive argument; then calculate galactic dust retention.
No reconstruction of coefficient functions is permitted. The memory study
was stopped, not promoted to a result.

## Reproduced failure and isolated defects

The original unchanged test command was

`python3 -B -m unittest test_evolve.EvolutionTests.test_constraint_residuals_decrease_under_spatial_refinement -v`

run from `../nonlinear_evolution_2026/`. It returned 1 with Hamiltonian/momentum
errors (2.62280e-6,4.88899e-6) at 129 points and (9.11447e-6,8.88044e-6) at
257 points. Source amplitude .02, width .3, outer radius 3, gamma=1e-6,
time .02 and dt=.00025 were retained throughout. The test's .6 reduction
factor and original constraint monitors were not relaxed or removed.

At fixed evolved data, smaller radial ODE steps and tighter tolerances barely
changed the momentum error (~8.88e-6). The largest errors occurred near the
origin. Further probes isolated several discretization inconsistencies:

1. Cubic interpolation in r, with only the first derivative fixed at zero,
   does not preserve smooth even parity at higher orders. A manufactured
   polynomial gave third derivative 1.125 at r=0 (the exact answer is zero)
   and second-derivative error -0.00585899. Representing even profiles as
   F(r²) and odd profiles as r G(r²) removes this defect. The density
   interpolant remains shape-preserving to protect positivity.
2. Projection and the origin lapse equation used different center jets.
   Both now use the same regular Taylor data derived from the constraints.
3. The second-order lapse solve was combined with fourth-order derivatives
   in evolution. The solve now uses the same fourth-order interior first/second
   derivative operators, even reflection and unchanged outer N=1 condition,
   with the existing one-sided penultimate stencil (third-order local second
   derivative). The source docstring's fourth-order wording is interior shorthand.
   Exact-polynomial and non-polynomial fourth-order refinement tests pass.
4. The adaptive radial solve estimated relative errors against order-one
   A and H, rather than their small perturbations. It now evolves A-a_c
   and h-h_c and adds the reference values back. This affine variable change
   preserves the radial ODE, its initial Taylor approximation and tolerances.

Intermediate partial repairs were **not** called successful. With parity
alone the 129/257 momentum errors were 7.07803e-6/7.05134e-6. Shared center
jets gave 5.32125e-6/4.01499e-6. Compatible lapse derivatives reduced them to
1.05805e-6/1.68934e-7, but Hamiltonian errors still failed refinement.
Only after the radial variable change did the unchanged combined test pass.

## Verification already executed

`python3 -B -m unittest test_projection test_lapse test_evolve -v` returned 0:
eight tests passed in 211.203 s. This includes the unchanged source/background,
mass-conservation, negative-density rejection and 129->257 refinement tests.

`python3 -B -m unittest test_equations test_constitutive test_center test_derivatives -v`
returned 0: five tests passed in 28.755 s.

After adding the non-polynomial lapse control,
`python3 -B -m unittest test_lapse -v` returned 0: both lapse tests passed.

The source files containing constitutive functions, background construction,
and the varied action/equations have no differences from base aafe58d20.
This is a numerical repair, not a new gravity theory or parameter fit.

## Stronger convergence check

`refinement.py` compares 65,129,257 grids, halves dt at 257, and measures
centered projection tangency. It deliberately does not report evolved force
claims. The completed `run_002/` returned **0**, with the following measured
constraint errors at t=.02 (dt=.00025 unless noted):

| Grid | Hamiltonian | Momentum | Clock |
|---|---:|---:|---:|
| 65 | 7.92547e-6 | 6.20799e-6 | 5.95604e-9 |
| 129 | 1.08498e-6 | 1.06160e-6 | 5.38774e-10 |
| 257 | 1.57608e-7 | 1.81625e-7 | 3.34368e-11 |
| 257, half dt | 1.59111e-7 | 1.78166e-7 | 3.40274e-11 |

For the metric/clock state variables the fine-grid differences are .066-.095
of the preceding differences (about fourth order); the coordinate dust density
D gives .262 (about second order). Every measured time-refinement difference
is below .2 of its fine spatial difference plus 1e-10. Relative baryon mass
balance errors are below 4.4e-16. These are bounded observations, not a proof
of global order or long-time existence. In particular, fourth-order interior
stencils do not imply fourth-order local truncation at the one-sided boundary.

The first longer execution computed all four evolution cases but exited 1
while serializing a NumPy boolean in the final summary. Its logged 129/257
Hamiltonian errors are 1.08498e-6/1.57608e-7; momentum errors are
1.06160e-6/1.81625e-7. Halving dt at 257 gives 1.59111e-7/1.78166e-7.
This reporting bug is distinct from a physical or numerical evolution failure.
The native-bool fix was rerun in `run_002`, with intermediate states saved so
a reporting error cannot discard an expensive calculation again.

The final complete command (from the repository root) was

`python3 -B -m unittest discover -s qwen_claude_field_theory/closure_2026/clock_response_repair_2026/nonlinear_evolution_2026 -p 'test_*.py' -v`

It returned **0**, all **14 tests passed**, in 222.011 s; see
`tests_run_002/stderr.txt`. The earlier `tests_run_001` was intentionally
interrupted (130) to add the imported background file to the evidence inputs.
The first refinement run's input hashes describe a historical revision, not
the corrected script. The refinement manifests do not pin background.py;
the final test-suite manifest does, so the former alone is not a complete
dependency record. No historical manifest was silently rewritten.

### Additional metric-evolution check: still OPEN

`projection_tangency.py` reuses the saved states and checks
`(P(t+e,x+eF)-P(t-e,x-eF))/(2e)-F`, where P is the radial constraint projection
and F the same-action evolution right-hand side. A smooth continuum projection
must be tangent to solutions; decreasing constraint residuals alone is not
sufficient. The script measures discrepancies rather than hard-coding a pass.

Tightening the diagnostic radial tolerance from (2e-10,2e-12) to
(2e-12,2e-14) reduces the noisy A discrepancy to about 2e-8--4e-8 for steps
5e-4--1e-4. However, the center h discrepancy remains about 2.57e-6 at 129
points and 1.78e-6 at 257. The near-center k discrepancy is about 8.38e-6
and 2.31e-6 respectively. Removing the center from a norm would conceal this
issue; the full-domain values are retained alongside fixed-radius diagnostics.

Thus the original 129->257 constraint regression is repaired, **but the full
metric-evolution consistency check is not certified**. The next numerical
calculation is the tangent-linear radial constraint solve, including the
regular-center Taylor conditions, to distinguish interpolation/startup error
from incompatible evolution. No late-time or galaxy-retention claim should
be based on this checkpoint. The exact invariant calculation below is
independent of that numerical issue.

## Gate 2: what the fixed action actually puts in its argument

After the unchanged refinement test passed, `cosmology_argument.py` derived
the ADM projector and clock acceleration, retaining lapse and shift. It also
imports the unrestricted spherical action and differentiates its W sector;
it does not infer the argument from a phenomenological force recipe.
Thirteen new exact checks and 36 imported action checks pass.

With tau=t and spatial metric h_ij,

\[
Y=(g^{\mu\nu}+n^\mu n^\nu)\partial_\mu\chi\partial_\nu\chi
  =h^{ij}\partial_i\chi\partial_j\chi.
\]

Thus on homogeneous FLRW, Y=0 even when H!=0. In the zero-shift clock
coordinates, the connection calculation gives a_i=partial_i ln(N), a_0=0.
The homogeneous clock congruence has zero four-acceleration, not zero curvature.
For chi=chi_bg(t)+epsilon sigma and h_ij=a² exp(-2 epsilon Psi) delta_ij,

\[
Y=\epsilon^2 a^{-2}|\nabla\sigma|^2+O(\epsilon^3),\qquad
K_{FLRW}=3H,\qquad\Box\chi_{bg}=-\dot q-3Hq.
\]

The same action has the fixed functions

\[
P=-\frac U2\log\frac{U-2dX}{U-2dq^2}+3\gamma qH(X-q^2),
\quad W=U+2d\ell(\sqrt{1+Y/\ell}-1)-2\gamma q^2\dot q,
\quad V=U.
\]

Consequently H enters the background coefficients, curvature and cubic
coupling, but **not as an additive cH in Y**. The homogeneous cubic density
gamma q² Box(chi) is -2 gamma H q³ plus the verified time boundary term
-a^-3 partial_t(a³ gamma q³/3). Expansion has not been dropped from the action.
Varying the actual spherical W density gives radial scalar flux
2 R² W_Y chi_r/A, with W_Y=d/sqrt(1+Y/ell), and no chi_t contribution.

This establishes the constitutive invariant, not a complete cosmological MOND
reduction. Y is a scalar-field gradient, not automatically the baryonic or
physical metric acceleration. The action has not been shown to reduce to the
preferred exponential MOND kernel after all metric/clock constraints and time
terms are retained. Adding cH to Y by hand changes the action; replacing the
whole coupled dynamics with a peculiar-field nu recipe is also unproved.

Therefore the reported phenomenological PM outcomes for the two prescriptions
cannot simply be imported as this fixed action's spectrum or as a proof that
it passes/fails cosmology. The **kernel-identification and resulting structure
evolution gate remains OPEN**. No coefficient reconstruction repairs this gap.

## Gate 3 status

The mass-dependent dust-retention calculation has **not** been completed.
No claim that clock dust avoids spiral potentials, remains at the stated
cluster fraction, or satisfies the M^0.16 trend follows from this work.
It must use the action's effective stress tensor and current on a validated
cosmological/galactic solution, not insert a depletion function or equate
conserved scalar charge with gravitating mass without derivation.

## Reproduction and checkpoint scope

From the repository root, the completed claim-supporting commands are:

```sh
python3 -B -m unittest discover -s qwen_claude_field_theory/closure_2026/clock_response_repair_2026/nonlinear_evolution_2026 -p 'test_*.py' -v
python3 -B qwen_claude_field_theory/closure_2026/clock_response_repair_2026/convergence_repair_2026/refinement.py --state-cache qwen_claude_field_theory/closure_2026/clock_response_repair_2026/convergence_repair_2026/run_002/states.npz
python3 -B qwen_claude_field_theory/closure_2026/clock_response_repair_2026/convergence_repair_2026/cosmology_argument.py
python3 -B qwen_claude_field_theory/closure_2026/clock_response_repair_2026/convergence_repair_2026/projection_tangency.py
```

All four final executions returned 0. The tangency command is a diagnostic,
**not** a passing closure test. Its measured remaining discrepancy is described
above. Re-running the refinement command replaces its state-cache file;
choose a fresh path when preserving the archived evidence.
`tests_run_002`, `run_002`, `cosmology_run_001`, and `tangency_run_001` contain
the exact argument arrays, input hashes, software versions, timings and logs.
Their manifest validation commands also returned 0. Mathbox's computation-audit
workflow records reproducibility, not truth of an interpretation.

Files modified: `../nonlinear_evolution_2026/evolve.py` and `project.py`.
Files added: the adjacent `test_lapse.py`, `test_projection.py`, and this
`convergence_repair_2026/` directory (plans, six diagnostic/verification Python
scripts, four contracts, and execution records). The interrupted
`../memory_transfer_2026/` draft is excluded, as are unrelated concurrent files.
No new Lean theorem is claimed in this checkpoint: the new exact identities
were checked in SymPy, and bounded numerical convergence is not a Lean proof
of a law of nature.

**Status: OPEN.** Pieces may be reusable, but same-action compatibility remains
unproved. The immediate next calculation is metric/projection tangency at the
regular origin; the physical MOND-kernel reduction and dust-retention mechanism
are not replaced by this numerical progress.

Independent read-only review found no blocking regression in the scoped
numerical changes. It independently reran both lapse tests (0), checked band
indexing/reflection, the affine projection variable change, shared center data,
and the W-flux/projector/cubic-boundary signs. Its boundary-order qualification
is recorded above. No action or evolution source was changed after the final
hashed test suite.
