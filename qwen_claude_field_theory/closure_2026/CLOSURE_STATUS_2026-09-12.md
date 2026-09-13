# Crispy closure status — 2026-09-12

## Verdict

No single explicit action currently in this repository is certified to satisfy
all ten requested gates.  The defensible global status is **OPEN**, with the
main AeST host branch **closed negatively under a strict two-tensor gravitational
sector**.

This is not a failure of a numerical search.  The latest action-level audit
derives a finite-k scalar from the same covariant host action that the prior
board treated as a nonpropagating ghost-band constraint.

## Decisive derivation

From `fried_chicken_final/fc_aest_finitek/fc_fk_routeB_covariant.py`, after the
unit-norm condition and spatially-flat gauge, the exact source-matched quadratic
Lagrangian has canonical constraints

```text
p_Phi = 0,
C1    = Q0*p_chi - p_v = 0.
```

Their computed Poisson-bracket matrix is identically zero.  For finite `k`, the
gauge-invariant scalar `X = delta phi + Q0 v` has

```text
D       = 2 K2 Q0^2 + K_B k^2
K_X     = 2 K2 K_B k^2 / D
Omega_X = 2 k^2 (2-K_B)(K2 Q0^2+k^2) / D
omega^2 = (2-K_B)(K2 Q0^2+k^2)/(K2 K_B).
```

For `K2>0`, `K_B>0`, `0<K_B<2`, this is a genuine positive-kinetic finite-k
scalar.  The computed Dirac count is one scalar configuration DOF at finite
k and zero homogeneous scalar DOF at `k=0`; the zero-mode degeneracy does
not remove the finite-k mode.  The exact exponential MOND term is cubic on
the `Ybar=0` background, so it cannot change this quadratic conclusion.

Therefore the earlier `Omega_red=0` finite-k rescue is an external input,
not a consequence of the displayed action.  Strictly counting every field in
the gravitational action gives `N_grav != 2`.  If `X` is reclassified as the
permitted clock scalar, it must be explicitly retained in PPN, FLRW, causal,
and strong-coupling calculations; that branch remains open rather than closed.

## Independent coefficient result

The newest committed lane, L230 (`504bd5ad4`), strips the `a0-Lambda` idea to a
single shape-slope statement.  Parameter-free standard kernels, including
`1-exp(-y)`, give `kappa=1`; the desired `kappa=1/2` requires a no-free-parameter
shape with deep-MOND slope `2`.  L230 explicitly does not derive such a shape.

## Reproduction commands and statuses

```bash
cd qwen_claude_field_theory/closure_2026/fried_chicken_final/fc_aest_finitek
python3 verify_aest_source_lagrangian.py          # exit 0, residual 0
python3 aest_metric_scalar_dirac_audit.py        # exit 0
python3 -m unittest discover -s . -p 'test_*.py' # 3 tests, exit 0
python3 run_aest_metric_scalar_lean.py           # exit 0, warnings only
python3 A_kernel_blindness_finitek.py            # exit 0
python3 B_decoupling_dispersion.py               # exit 0
python3 C_effective_kinetic_and_decider.py       # exit 1, unresolved sign-dependent limit
```

The tensor-compensated suite remains `14` tests, exit `0`, but its strict
anti-hardcoding audit finds literal expected ranks/DOF values.  L223's board
still exits `0` while reporting `CONSOLIDATION_NOT_ACTION_CERTIFICATION`.

## Exact files

- `fried_chicken_final/fc_aest_finitek/aest_metric_scalar_dirac_audit.py`
- `fried_chicken_final/fc_aest_finitek/verify_aest_source_lagrangian.py`
- `fried_chicken_final/fc_aest_finitek/AestMetricScalarFormal.lean`
- `fried_chicken_final/fc_aest_finitek/AEST_METRIC_SCALAR_DIRAC_REPORT.md`
- `fried_chicken_final/fc_aest_finitek/test_aest_metric_scalar_dirac_audit.py`
- `fried_chicken_final/fc_aest_finitek/run_aest_metric_scalar_lean.py`
- `INDEPENDENT_AEST_SCALAR_CHECKPOINT_2026-09-12.md`
- `exponential_kernel_trilemma_2026/exponential_kernel_trilemma.py`
- `exponential_kernel_trilemma_2026/ExponentialKernelTrilemmaFormal.lean`
- `exponential_kernel_trilemma_2026/EXPONENTIAL_KERNEL_TRILEMMA_REPORT.md`
- `fable_independent_2026/L232_robustness_audit.py`
- `fable_independent_2026/test_L232_robustness_audit.py`
- `fable_independent_2026/L232_ROBUSTNESS_REPORT.md`
- `fried_chicken_final/fc_aest_finitek/verify_aest_source_lagrangian.py` (CWD-independent path fix)
- `exact_exponential_york_slip_gate_2026.py`
- `ExactExponentialYorkSlipFormal.lean`
- `run_exact_exponential_york_lean.py`
- `general_york_no_slip_no_go_2026.py`
- `test_general_york_no_slip_no_go_2026.py`
- `GeneralYorkNoSlipNoGoFormal.lean`
- `run_general_york_lean.py`
- `GENERAL_YORK_NO_SLIP_NO_GO_REPORT.md`
- `kepler_precession_prediction_2026.py`
- `test_kepler_precession_prediction_2026.py`
- `KEPLER_PRECESSION_REPORT.md`
- `KeplerTransitionFormal.lean`
- `run_kepler_transition_lean.py`

These files are presently in the working tree but not committed because the
host rejected index writes after the usage-limit review.  No workaround or
unrelated file staging was performed.

## Remaining mathematical obligation

The only honest rescue route is a full lapse/shift-retained FLRW ADM reduction
of a modified action in which the extra scalar is either demonstrably a healthy
separate clock field or is removed by genuinely new constraints.  Its PPN
parameters, matter Ward identity, tensor cone, cosmological perturbations,
and nonlinear MOND branch must then be derived from that same action.  No
parameter-board pass or Lean algebraic identity substitutes for this missing
common-action calculation.

## New structural result: exponential-kernel trilemma

`exponential_kernel_trilemma_2026/` derives a broader conditional obstruction:
because

```text
G(y) = 2 y^3/3 + O(y^4),   Ybar_FLRW=0,
```

the exact exponential MOND sector has no quadratic Hessian and no linear MOND
principal symbol around a regular isotropic homogeneous background.  The three
local repairs each spend a required gate:

```text
quadratic cY repair       -> mu_eff(0)=c, violating exact mu(0)=0;
nonzero spatial gradient  -> anisotropic background, violating isotropic FLRW;
P(0)=0 auxiliary repair   -> inverse-Laplacian IR pole, while finite regulator -> slip.
```

The SymPy gate and its Lean certificate both exit `0`.  This is conditional on
locality, one metric, regular isotropic FLRW, and the exact exponential law; it
is not a universal no-go against arbitrary nonlocal or multi-metric actions.

## Exact-exponential coefficient lock

`exact_exponential_scale_lock_2026/` closes the remaining normalization escape
under the one-scale assumption.  Since `1-exp(-u)` has unit slope at the
origin, matching the same law written as `mu(g/a0)` to a scale-free law written
as `mu(g/a_Lambda)` forces `a0=a_Lambda`, hence `kappa=1`.  The desired
`kappa=1/2` requires `1-exp(-2u)` (or an equivalent inserted factor of two),
which is a different kernel/normalization.  Python, unittest, and Lean all exit
`0`.  L231's `1-(1+u)^(-2)` is therefore an interesting alternative curve, not
closure of the fixed exponential target.

## L232 aggregation robustness

`fable_independent_2026/L232_robustness_audit.py` reruns the discrete integer
test with one RMS residual per galaxy (equal galaxy weighting), rather than
allowing long curves to dominate the pooled-point score.  It then resamples
galaxies 1000 times with a fixed recorded seed.  The computed winner is

```text
                 equal-galaxy winner     bootstrap winner fraction
rho_Lambda              n = 2                    1.000
rho_crit                n = 2                    1.000
```

The median winning margin is `0.02498 dex` for the Lambda convention and
`0.01723 dex` for the critical-density convention.  This makes L232's
`n=2` preference robust to the most immediate pooling objection.  It remains
only a curve-level prediction: the audit fixes the mass-to-light ratios and
does not marginalise the SPARC covariance, and no action-level calculation
selects the integer.  It therefore strengthens the empirical clue without
changing the global status from **OPEN**.

Reproduction:

```bash
python3 fable_independent_2026/L232_robustness_audit.py       # exit 0
python3 -m unittest -v fable_independent_2026/test_L232_robustness_audit.py  # 2 tests, exit 0
```

The finite-k AeST source-match suite now also passes when invoked from the
repository root (`3` tests, exit `0`); the verifier resolves its generated
covariant source relative to its own file.

## Elliptic phantom-density action gate

The explicit candidate in
`elliptic_phantom_action_gate_2026/elliptic_phantom_action_gate_2026.py` was
also rerun from its displayed action, not from a phenomenological equation.
Its Euler--Lagrange variations reproduce the exact exponential MOND flux and
the desired elliptic pair.  The same calculation then gives, for every
sampled nonzero Fourier vector, a full auxiliary Poisson block of rank `8`
(the rank and determinant are computed from the displayed Hessian), with
three physical scalar/auxiliary configuration DOF after the stated spatial
diffeomorphism subtraction.  At `k=0`, the equation
`D^2 chi = 4 pi G rho_0` reduces to `-4 pi G rho_0 = 0`, so positive-density
homogeneous FLRW is not an allowed solution.

Metric variation of the actual multiplier term gives a strictly nonzero
trace-free stress for every finite `y>0`; setting it to zero forces the
multiplier gradient to vanish, which collapses the metric branch to ordinary
Einstein/Poisson rather than MOND.  The same action’s Ward calculation gives
a nonzero divergence of the baryonic stress from `S_m` alone.  Thus this
candidate simultaneously fails the no-slip, ordinary-matter conservation,
homogeneous-FLRW, and strict two-tensor gates.  Its standalone script and two
regression tests both exit `0` because they computationally certify the
falsification conditions, not because the candidate passes them.

## Exact exponential York/QUMOND carrier

`exact_exponential_york_slip_gate_2026.py` independently varies the static
cross-gradient action that carries the exact exponential QUMOND flux.  It
derives both Euler--Lagrange potentials, then varies the spatial metric on the
putative no-slip branch.  The trace-free source is

```text
T_ij^TF  proportional to  (nu_exp(x) - 2) (q_i q_j)^TF,
nu_exp(x) = x / [x(1-exp(-x))] = 1/(1-exp(-x)).
```

The exact equation `nu_exp(x)=2` has the single finite solution `x=log(2)`;
the stress therefore cannot vanish throughout a finite-range galactic field.
The script's eight symbolic checks exit `0`, including the primitive and the
nonzero finite-field slip witness.  This closes the exact York/QUMOND
single-metric no-slip carrier, while remaining explicitly scoped (it is not a
universal theorem against every nonlocal action).

The accompanying `ExactExponentialYorkSlipFormal.lean` certificate compiles
through `run_exact_exponential_york_lean.py` (exit `0`); it certifies the
trace-free factorization and the contradiction that the exponential response
cannot equal a constant two on all positive fields.

## General first-gradient York/QUMOND theorem

The new `general_york_no_slip_no_go_2026.py` calculation removes the special
choice `A=1` from the previous gate.  For the full isotropic class

```text
L = -2 A(u) h^{ij} Phi_i Psi_j + a0^2 F(u),
```

exact Poisson response fixes `A(u)=1` pointwise.  The independently varied
Hilbert trace-free coefficient then reduces to `F'(u)-2`, so no-slip for
arbitrary anisotropic gradients requires `F'(u)=2` identically.  The exact
exponential carrier instead needs
`F'(u)=1/(1-exp(-sqrt(u)))`, which is nonconstant and differs from `2` away
from the isolated value `sqrt(u)=log(2)`.  The five symbolic gates, its
regression test, and `run_general_york_lean.py` all exit `0`.  This is a
scoped theorem for one metric, local first gradients, and two static
potentials; it is not a universal no-go for arbitrary nonlocal or multi-metric
actions.

## Kepler-like orbital prediction

`kepler_precession_prediction_2026.py` derives a new static observable directly
from the exact spherical law, with no fitted curve parameters.  Writing
`x=g/a0` and `r_M=sqrt(GM/a0)`,

```text
x(1-exp(-x)) = (r_M/r)^2,
A(x) = 1 + x/(exp(x)-1),
kappa^2/Omega^2 = 3 - 2/A(x),
Delta-varpi = 2 pi [1/sqrt(3-2/A(x)) - 1].
```

The computed curve is retrograde: `Delta-varpi -> 0` in the Newtonian regime,
`-79.035 deg` at `r=r_M`, and
`2 pi(1/sqrt(2)-1) = -105.44 deg` per radial cycle in deep MOND.  The period
ratio at fixed `M,r` is independently `P/P_Newton=sqrt(mu(x))`.  The script,
its regression test, and `KEPLER_PRECESSION_REPORT.md` are a prediction lane,
not a relativistic closure; a valid covariant action must reproduce this
static limit and then supply its own slip/clock corrections.

## PAPER27 source notation audit

The published PAPER27 TeX source contains an overloaded `c` in the scale
output display (`a_0=s/c`, `kappa=1/c`) immediately after defining
`s=c_light sqrt(G rho_Lambda)`.  The first-principles deep-branch calculation
requires the constitutive slope to be named separately:

```text
mu_n(g/s)=n g/s+O(g^2)  =>  a_0=s/n,
kappa=a_0/[c_light sqrt(G rho)] = 1/n.
```

`PAPER27_scale_erratum_audit.py` detects the source token and verifies the
corrected algebra (exit `0`), with the full note in `PAPER27_SCALE_ERRATUM.md`.
The numerical tables' `n=2` values are consistent with the corrected formula;
the audit does not rewrite the already published PDF.

## Conditional closure theorem (2026-09-13)

`CLOSURE_THEOREM_2026-09-13.md` consolidates the general first-gradient
York/QUMOND obstruction with the independently varied elliptic phantom and
AeST Dirac failures.  It records the exact scope: the explored local
single-metric classes are closed negatively, while the full ten-gate problem
remains OPEN because arbitrary nonlocal/multimetric actions were not excluded.

## No-slip/Ward phantom trilemma (2026-09-13)

`phantom_noslip_ward_trilemma_2026.py` tests the most direct remaining
architecture: rewrite exact exponential MOND as an auxiliary phantom density
on the right-hand side of ordinary Einstein curvature.  In the stated local
weak-field scope, no trace-free spatial stress plus `Phi=Psi` gives

```text
0 = 8 pi G (3 p_aux)  =>  p_aux = 0.
```

The separately conserved isotropic Ward identity
`grad p_aux + (rho_aux+p_aux) grad Phi = 0` then gives
`rho_aux=0` wherever `grad Phi != 0` (for static pressure).  Exact MOND
instead requires
`rho_aux=(4 pi G)^(-1) div[(1-mu) grad Phi]`, which is generically nonzero;
the explicit witness `Phi'=x`, `a0=1`, `x=2` is
`-exp(-2)/(4 pi G)`.  Thus this architecture cannot keep all three of exact
MOND, no slip, and a separately conserved isotropic auxiliary stress while
retaining ordinary Einstein curvature.  The scope is conditional, not a
universal no-go against nonlocal, multimetric, or explicitly anisotropic
actions.

The Python gate, its regression test, and `PhantomNoSlipWardFormal.lean`
compile/run with exit `0`; the zero status certifies the falsification
calculation, not a passing theory.

## Closest constructive architecture remains causally open (2026-09-13)

The `elliptic_curvature_clock_2026` action is still the nearest constructive
candidate: its varied static sector reproduces the exponential MOND flux and
`Phi=Psi`; its finite-`k` Dirac blocks close with one explicit scalar pair,
positive scalar/tensor kinetic terms, and an expanding homogeneous branch.
However, its compact-support vacuum test derives
`R_00^(4)(0) = 4 D^2 q^3/[9(q+D)] f`. For anisotropic exponential response
`D` this contains a non-polynomial inverse elliptic operator and produces a
nonzero exterior fourth time derivative. The strict suite therefore returns
the expected refusal status `2`: positive wave speed is not finite-domain
causality. Replacing that inverse by a hyperbolic operator would either alter
the exact static MOND kernel or introduce a propagating scalar; this tradeoff
is the next unavoidable calculation, not a coefficient-fit problem.
