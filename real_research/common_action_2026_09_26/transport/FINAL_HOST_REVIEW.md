# Independent final host and perspective review

Reviewed 2026-09-26 from the transport lane. This is a read-only mathematical
review of the named files, not a new computation or a full gravitational
constraint analysis. The shared checkout HEAD was
`ecffd2af3623ff3e32318234fd51e1fac50b9126`; the reviewed work was uncommitted.

## Review result

No unresolved concrete contradiction remains in the current
[FINAL_ACTION.md](../action/FINAL_ACTION.md),
[CP_AND_CARRIER.md](../evolution/CP_AND_CARRIER.md),
[PERSPECTIVE_VARIANT.md](../action/PERSPECTIVE_VARIANT.md) and
[PERSPECTIVE_REPAIR.md](../assembly/PERSPECTIVE_REPAIR.md) within their
explicitly stated scopes. Historical weighted-gate and exponential-carrier
failures remain failures; the later variants change the action.

The following findings were raised during this independent review and are
resolved in the current files:

- The compensated inactive branch changes the all-scale static response.
  `Gbare/cN` is the high-momentum/local Newton normalization. Reciprocal
  cross forces do not imply that all entries equal the old response.
- A globally fully active geometric gate is impossible on a compact closed
  leaf: at a maximum of its potential, the gradient vanishes and its
  Laplacian is nonpositive. A local active patch also does not recover a
  globally ungated nonlocal filtered law. The final action now states the
  changed exact target.
- The no-slip calculation applies to the inactive/formal constant-gate
  leading weak-field ordering, not arbitrary transition derivatives.
- The provisional content includes the host clock scalar in addition to
  two tensors and five real carrier fields. It is not a full Dirac count.
- The affine compensator changes the auxiliary energy lower bound even
  though it leaves its Hessian unchanged. The current evolution report
  uses `E_CP >= r^2/2 - (2 + ell^2 kappa_N/2) A_N^2`.
- With a positive perspective floor `V0`, separating its homogeneous
  energy does not remove its linear susceptibility. At zero excitations,
  `rho=V0/t`, `sigma=V0/t^2`, hence
  `delta(rho-sigma)=V0 z`. Projection also contributes
  `+V0 delta ln N` to the nonzero-mode source about the homogeneous
  unit-lapse state. The old response matrix therefore needs `V0=0` or a
  stated regime in which these terms are negligible, together with a
  consistent background. Reciprocity alone does not preserve its entries.

## Perspective positive-lapse proof

The fixed-data continuum argument is valid on a smooth compact connected
closed leaf, with smooth `N>0`, `m>0`, smooth `b`, and smooth
`epsilon >= epsilon_min>0`. The constraint is the unweighted spatial mean
`<t>_h=1`. These hypotheses are essential to this review.

For the regularization written in the assembly report, its two branches
join with two continuous derivatives, it is convex and nonnegative, and
`f_delta + t f_delta' >= 0`. Poincare coercivity on the mean-one affine
space and weak lower semicontinuity give a unique minimizer. The
regularized equation has sufficient classical regularity for the minimum
argument; full smoothness is needed only after positive separation from
the regularization threshold.

Testing the Euler equation by `t-1`, comparing with `t=1`, and retaining
the volume factor give

```
lambda <= [integral N epsilon + (3m/2)||b||_N^2] / Vol_h,
C = lambda_max + 2m ||div_h(N b)||_infinity > 0.
```

At a minimum with `t_min <= delta`, the Euler equation implies
`N_min epsilon_min / delta^2 <= C`. Taking
`0<delta<min(1,sqrt(N_min epsilon_min/C))` excludes this possibility.
The true equation then gives
`t_min >= sqrt(N_min epsilon_min/C) > 0`.

The additional domination identity is necessary to connect this Euler
solution to global minimization of the original singular functional:

```
1/t - f_delta(t) = (1-t/delta)^3/t >= 0  for 0<t<delta.
```

Above the threshold the two integrands agree. Thus the regularized
minimizer attains the original global minimum against all positive
competitors. Strict convexity gives uniqueness, and elliptic regularity
after the positive lower bound gives a finite smooth solution for each
fixed smooth data set. The current assembly report includes all these
steps. This is not a uniform estimate over unconstrained data families,
nor a proof of time-dependent gravitational continuation.

The perspective momentum/auxiliary Hessian is jointly nonnegative with
the positive-floor term. This repairs the specific exponential reduced
kinetic counterexample under the stated frozen-data conditions; the
remaining metric/clock kinetic and constraint analysis is explicitly open.

## Transport interface

The static inhomogeneous extension in [CONVERSION.md](CONVERSION.md)
checks out: for fixed smooth `h`, `N>0`, finite smooth projected exponent
`z`, and zero shift, `A=e^z/N` and `B=N e^-z` are bounded above and away
from zero. The operator `-A^-1 div_h(B D)` is nonnegative and self-adjoint
on `L2(A dvol_h)` through its closed quadratic form. The polynomial
degree-at-most-four nonnegative potential has an energy-space locally
Lipschitz force in three dimensions. Conserved weighted energy and the
finite-time `L2` growth bound prevent a finite-time energy-space blowup
on this fixed geometry. No field phase is assumed to be a global clock.

This analytic continuation argument does not control the evolving host
metric, lapse, projected gate, foliation, or their constraints. It is not
among the Lean-certified algebra statements or a claim of global health
of the coupled common action.

## Exact file versions reviewed

SHA-256 values at review completion:

| File | SHA-256 |
| --- | --- |
| `action/FINAL_ACTION.md` | `b8c04d4e365f1c8e1c2ec3bf8d14629618d1ac162e97e3fdf809382fb147546e` |
| `action/PERSPECTIVE_VARIANT.md` | `36efa45459468d22c1f2553cbcd5d2a2349bef56c6df1e03a5b9fefb9806d78b` |
| `assembly/PERSPECTIVE_REPAIR.md` | `12e3418abb361d53d1941f6f0ae09bb3ec292f6dfb57132816cf4c6bf65f62a6` |
| `evolution/CP_AND_CARRIER.md` | `34643194d4450a54e4bdadf52916053a5bb90f79d0eb059b4d851027f090ba8f` |

Subsequent edits need a version-aware review. No new numerical run or
compiler acceptance is claimed by this record.
