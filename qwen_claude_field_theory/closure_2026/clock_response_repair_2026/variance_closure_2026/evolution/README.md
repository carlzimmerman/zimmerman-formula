# Same-action quadratic gradient variance

This bounded computation evaluates the existing constrained six-state
time-dependent action, with its existing sourced background and coefficient
history. It supplies a counterexample to treating the quadratic gradient
variance as a universally sufficient state variable for a first-order scalar
growth law. It also finds that three admissible initial states with zero
variance derivative have nonzero variance acceleration. These conclusions do
not exclude nonlinear or restricted-family attractors.

The frozen source is
`cosmological_bridge_2026/transfer_evolve.py`, importing its action,
background, derivative jets, and the existing constitutive model. None of
those files was changed. The parent repository commit recorded by the runner
is `48ab93de353de3a8a8b680587b604136f50284c8`; the working tree was dirty.
The v2 manifest pins the source dependency files before and after execution.

## Observable and exact linear covariance law

Use the existing unitary-clock and scalar spatial gauges, with state

\[
 u=(\sigma,\delta Q,r_1,\delta Q_r,\theta_1,\delta\rho_b)^T,
 \qquad \dot u=A(t,k)u,
 \qquad \delta Q=\dot\sigma-q\alpha.
\]

The independent geometry audit identifies the gauge-invariant scalar
\(S=\sigma-(q/\dot\tau)\delta\tau\), which equals \(\sigma\) in this gauge.
At quadratic order the projected gradient is
\(Y_2=a^{-2}|\nabla S|^2\). Here each mode uses an RMS-normalized real Fourier
basis, for example \(\sqrt2\cos(kx)\). With \(C=\langle uu^T\rangle\),

\[
 p=k^2/a^2,\quad \dot p=-2Hp,\qquad
 \mathcal Y_2=pC_{00},\qquad
 \dot C=AC+CA^T.
\]

If instead \(\sigma_{\rm amp}\) is the source action's unnormalized cosine
amplitude, its spatially averaged gradient is
\(p\langle\sigma_{\rm amp}^2\rangle/2\). The two conventions agree after
\(\sigma_{\rm amp}=\sqrt2\sigma_{\rm RMS}\). No factor of two is absorbed
into the action or the transfer operator.

Retaining the physical expansion and full coefficient rates gives

\[
\dot{\mathcal Y}_2=p[\dot C_{00}-2HC_{00}],
\]
\[
\ddot{\mathcal Y}_2=p[\ddot C_{00}-4H\dot C_{00}
 +(4H^2-2\dot H)C_{00}],
\quad
\ddot C=\dot A C+C\dot A^T+A\dot C+\dot C A^T.
\]

Equivalently, write \(S_2=\langle\sigma^2\rangle\),
\(B=\langle\sigma\dot\sigma\rangle\),
\(V=\langle\dot\sigma^2\rangle\), and
\(D=\langle\sigma\ddot\sigma\rangle\). Then

\[
\dot{\mathcal Y}_2=2p(B-HS_2),\qquad
\ddot{\mathcal Y}_2=2p[V+D-4HB+(2H^2-\dot H)S_2].
\]

The first derivative contains correlations with the six-state velocity and
the constrained lapse: \(\dot\sigma=\delta Q+q\alpha\). The second derivative
contains velocity variance and acceleration correlations in addition.
On a stationary-variance slice \(B=HS_2\),

\[
\ddot{\mathcal Y}_2=2p[V+D-(2H^2+\dot H)S_2].
\]

For a rank-one ensemble with \(\dot\sigma=H\sigma\), this becomes
\(2p\sigma[\ddot\sigma-(H^2+\dot H)\sigma]\).
The acceleration is evaluated from
\(\ddot u=(\dot A+A^2)u\), using one-sided numerical derivatives of the actual
operator. It is independently checked by differentiating the evolved
\(\mathcal Y_2(t)\). The source background is solved on the positive-time
interval only; these stencils never extrapolate it backwards.

## Initial ensembles and finite result

For each \(k\in\{0.3,3,30\}\), put \(\epsilon=10^{-6}/k\) and choose

\[
 u_d=\epsilon\left(1,
 \frac{H+d-A_{00}}{A_{01}},0,0,0,0\right)^T,
 \qquad d\in\{-1,0,+1\}.
\]

Each ensemble assigns equal probability to \(+u_d\) and \(-u_d\), so its
mean is zero and \(C_d=u_du_d^T\) is positive semidefinite. These are initial
conditions of the same unchanged linear action. The nonsingular constraint
reduction reconstructs the lapse, curvature, and shift for every state; the
original eight Euler equations are checked both on the full fundamental
basis and on these selected state columns. All reconstructed physical
initial amplitudes are small; the largest curvature amplitude is
\(2.54\times10^{-5}\).

At the initial time all nine ensembles have
\(\mathcal Y_2=10^{-12}\), while
\(\dot{\mathcal Y}_2/\mathcal Y_2=2d\), up to floating-point rounding.
Consequently, even allowing an explicitly time-dependent scalar law
\(\dot{\mathcal Y}_2=f(t,k,\mathcal Y_2)\) cannot describe all these states.

For the \(d=0\) states:

| \(k\) | \(\ddot{\mathcal Y}_2(0)/\mathcal Y_2(0)\) | \(\mathcal Y_2(0.02)/\mathcal Y_2(0)\) |
|---:|---:|---:|
| 0.3 | -0.84352413 | 0.9998327920 |
| 3 | -1.05325329 | 0.9997923561 |
| 30 | 1.54430648 | 1.0003006835 |

Thus a zero initial variance derivative does not make these states fixed.
It only sets one instantaneous correlation relation. The coefficient rates,
inertia, and expansion determine the subsequent departure.

One further instantaneous check adds independent \(\delta Q\) variance to
the normalized stationary covariance:
\(\widetilde C=C+0.01e_1e_1^T\). This remains positive semidefinite, preserves
\(\mathcal Y_2\) and \(\dot{\mathcal Y}_2\), and increases
\(\ddot{\mathcal Y}_2/\mathcal Y_2\) by \(0.02A_{01}^2\). The increases are
2.12781070, 2.22137048, and 2.28989039, respectively. A scalar second-order
equation depending only on \(t,k,\mathcal Y_2,\dot{\mathcal Y}_2\) therefore
also needs restrictions on the allowed covariances. This enlarged covariance
was checked instantaneously; it was not a fourth integrated ensemble.

## Verification and provenance

`run_001/result.json` stores nine sample times per wavenumber, compact
residual summaries, both curvature checks, and initial reconstructed states.
It does not dump fundamental matrices at every time. `run_001/manifest.json`
records the complete reproducible argument vector, software versions, source
hashes, output hashes, and actual caps. The bounded run completed in
3.3365 seconds with exit status 0. Manifest validation with `--root` passed.

The fundamental matrix was integrated with DOP853 at relative tolerances
\(2\times10^{-10}\) and \(2\times10^{-12}\). The covariance differential
equation was integrated independently with RK45 at relative tolerance
\(2\times10^{-11}\); its initial covariance is unit-scaled to prevent the
absolute tolerance from erasing the physical \(10^{-12}\) variance.

- Maximum scaled independent covariance/transport discrepancy:
  \(3.10\times10^{-12}\).
- Maximum scaled fundamental-matrix tolerance-refinement discrepancy:
  \(3.90\times10^{-12}\).
- Most negative scaled covariance eigenvalue:
  \(-6.94\times10^{-14}\), consistent with solver roundoff near rank one;
  no positive-definiteness projection was applied.
- Maximum scaled original Euler residual: \(1.93\times10^{-7}\), below the
  existing \(3\times10^{-6}\) source diagnostic threshold. Both finite
  difference steps and both basis/selected-state checks passed.
- Largest operator-rate curvature refinement change:
  \(6.54\times10^{-8}\); largest difference from directly differentiated
  solution curvature: \(8.11\times10^{-8}\).
- Maximum finite-k reduction condition number: 123.01. The dust-lapse minor
  identity from the independent algebra audit held within
  \(2.23\times10^{-16}\).

The rate differences at the finest steps are not monotonically convergent
in every mode because subtraction roundoff is visible. They are tiny relative
to the observed nonzero curvature; they are not interval error certificates.
Both numerical evolution methods share the same original background and
operator implementation. The original uneliminated Euler residual supplies
an orthogonal action check, but the finite run does not independently prove
the physical correctness of every source equation.

Four cheap independent tests passed: a constant operator against a matrix
exponential, an elementary inertial mode in an expanding background,
same-variance/opposite-derivative initialization, and finite-difference
polynomials plus the zero-gradient \(k=0\) observable. An initially overly
strict single-step curvature comparison was replaced by a two-step
refinement test consistent with the third-order stencil truncation error.

From the repository root, reproduce the tests with:

```bash
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 -m unittest discover -s qwen_claude_field_theory/closure_2026/clock_response_repair_2026/variance_closure_2026/evolution -p 'test_variance_evolve.py' -v
```

For a quick rerun, choose a new result path and run:

```bash
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 qwen_claude_field_theory/closure_2026/clock_response_repair_2026/variance_closure_2026/evolution/variance_evolve.py --result-file /private/tmp/variance-reproduction.json
```

To reproduce the provenance record, use the argument vector in the manifest
with a fresh run output directory and result path. Validate the existing
record with:

```bash
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.0.0/skills/computation-audit/scripts/validate_manifest.py qwen_claude_field_theory/closure_2026/clock_response_repair_2026/variance_closure_2026/evolution/run_001/manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

The assertions concern the leading quadratic observable formed from linear
perturbations, on this short solved background. They do not demonstrate a
measured cosmological variance, absence of all attractors, a primordial
spectrum, nonlinear backreaction closure, or the fate of a prescribed finite
nonlinear variance. At \(k=0\) the projected-gradient observable is zero; the
finite-k constraint reduction is singular there and is explicitly excluded.
The full theory remains open.
