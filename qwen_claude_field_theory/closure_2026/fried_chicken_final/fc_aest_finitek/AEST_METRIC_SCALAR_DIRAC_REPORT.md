# Independent finite-k metric-coupled AeST Dirac audit

This audit addresses the one residual that the earlier finite-k scripts did
not derive: whether the host action itself has a nonpropagating scalar, or
whether the aether/clock sector leaves a finite-k scalar mode.

## Contract

The input is the quadratic Minkowski expansion of the explicit host action in
`fc_fk_routeB_covariant.py`, with the unit-norm condition imposed on the
aether.  The spatial shift term is an exact total derivative on this branch and
is dropped.  The calculation is restricted to `k != 0`, then repeats the
constraint analysis at `k=0`; it is not a nonlinear cosmological certificate.

Pass for the claimed ghost-band rescue would require the finite-k scalar
direction to be a genuine constraint (`no` propagating scalar DOF).  Finding a
finite-k scalar closes this host gate as a failure of the requested
`N_grav=2`/no-hidden-auxiliary condition, unless the theory explicitly accepts
that scalar as an additional healthy matter/clock field.

## Derived result

The canonical momenta are obtained from the exact quadratic Lagrangian.  For
finite `k`, `p_Phi=0` is primary.  Its preservation gives

```text
C1 = Q0 p_chi - p_v = 0,
```

and `C1` is preserved without a tertiary constraint.  The computed Poisson
matrix of `[p_Phi,C1]` is the zero matrix, so the pair is first class.

The gauge-invariant combination is

```text
X = delta phi + Q0 v,
D = 2 K2 Q0^2 + K_B k^2.
```

Eliminating the algebraic lapse perturbation yields, up to the constant-
background total derivative `X Xdot`,

```text
L_phys = 1/2 K_X Xdot^2 - 1/2 Omega_X X^2,
K_X = 2 K2 K_B k^2 / D,
Omega_X = 2 k^2 (2-K_B) (K2 Q0^2+k^2) / D.
```

Consequently the actual finite-k mode has

```text
omega^2 = (2-K_B) (K2 Q0^2+k^2)/(K2 K_B).
```

For `K2>0`, `K_B>0`, `0<K_B<2`, this kinetic coefficient and `omega^2` are
strictly positive for every finite `k>0`.  The phase space has dimension six,
two first-class constraints and no second-class constraints, hence one
physical scalar configuration DOF.  The count is computed from the generated
Poisson matrix, not inserted as an expected rank.

At `k=0`, `p_Phi=0`, `p_v=0`, and `Q0 p_chi=0` are first class; the homogeneous
scalar count is zero.  This discontinuity is a strong-coupling/degenerate
zero-mode feature, not evidence that finite-k modes are absent.

## Reproducibility

From this directory:

```bash
python3 aest_metric_scalar_dirac_audit.py
python3 verify_aest_source_lagrangian.py
python3 -m unittest discover -s . -p 'test_*.py'
python3 run_aest_metric_scalar_lean.py
```

The source-matching script first checks the compact polynomial against the
covariant route-B expansion (`SOURCE_MATCH_RESIDUAL=0`).  The main Python script
then exits zero when the symbolic derivation is internally consistent; its
final status line distinguishes the strict two-tensor and separately-counted
clock readings.
The unittest and Lean runner likewise exit zero on a successful derivation.  The
Lean file certifies the exact rational formulae and positivity implications
only.

## Decision

**HOST SCALAR GATE: the claimed nonpropagating-constraint rescue is refuted.**
Under the strict reading that every field in the AeST gravitational action is
part of the gravitational sector, this is **DEAD** for `N_grav=2`.  Under the
user's more permissive allowance for a separately counted clock scalar, the
gate is instead **OPEN**, but the scalar must be carried into every PPN,
cosmological, and strong-coupling calculation; it cannot be hidden in a
constraint count.  In the displayed parameter regime its quadratic kinetic and
gradient coefficients are positive, so this audit alone does not call it a
ghost.

This result does not establish a no-go theorem for every imaginable
single-metric MOND action.  It does establish that the particular AeST host
action used by the finite-k “winner” cannot be certified by treating its
negative `K_eff` band as a nonpropagating constraint: the direct covariant
quadratic reduction contains a finite-k scalar with the dispersion above.
