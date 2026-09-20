# Independent auxiliary-action audit

Date: 2026-09-20. Repository HEAD observed during review:
`89f5ef2e7d8079de87fd86d2f1ada0c6c5992905` (the assignment named the earlier
base `928c61c79`). Target: the action specified below, independently derived
from its formulas; this report does not certify the evolving Lean file.

**Normalized claim.** For fixed `s>0`, `G>0`, `lambda>0`, `y=|grad Phi|/s>=0`
and nondynamical fields restricted to `0<q_i<=1`, eliminate

```
U(q) = q^2/2 - 2q + log q + 3/2,
W = y^2(1-q1 q2) + [U(q1)+U(q2)]/lambda^2,
S = - integral [s^2 W/(8 pi G) + rho_b Phi] d^3x.
```

**Primary verdict: conditional on a named input.** The elimination and unit
response are mathematically correct **conditional on choosing this action,
this auxiliary domain, and the relative coefficient `lambda=1`**. They do not
derive that coefficient from first principles. The arbitrary positive-lambda
family survives all structural checks below. This qualification is substantive,
not merely a choice of units when `s` is independently fixed.

## Independent derivation

`U'(q)=(1-q)^2/q`; consequently
`W_qi=-y^2 qj+(1-qi)^2/(lambda^2 qi)`.
Multiplication by the positive `lambda^2 qi` gives exactly

`(1-qi)^2=lambda^2 y^2 q1 q2`.

Both `1-qi` are nonnegative. Equality of their squares therefore implies
`q1=q2=q`; positivity permits taking the nonnegative square root to obtain
`1-q=lambda*y*q`, hence the unique solution
`q=1/(1+lambda*y)`. It lies in the stated domain for every finite `y>=0`.
At `y=0`, it gives the upper endpoint `q=1`, with zero first derivative.

Writing `t=lambda*y`, direct substitution gives

`W_red=y^2-2/lambda^2 [log(1+t)+(1+t)^(-1)-1]`.

The envelope derivative is `W_red'=2y(1-q^2)`. Varying `Phi` with compactly
supported variations, integrating by parts, and retaining the sign of the
source term gives

`div(mu(|grad Phi|/s) grad Phi)=4 pi G rho_b`,
`mu(y)=1-(1+lambda*y)^(-2)`.

At zero gradient this expression extends continuously with zero flux; no
division by `|grad Phi|` is needed in the final equation. With `p=1-q`,
`p=lambda*y/(1+lambda*y)` and `p'(0)=lambda`. Thus the two-channel polynomial
`mu=1-(1-p)^2` is exact, but a stochastic interpretation or statistical
independence of two channels does not follow from the action.

Since `mu(y)=2 lambda*y+O(y^2)`, matching the convention `mu~g/a0` yields
`a0/s=1/(2 lambda)`. For this chosen action, `lambda=1` gives unit response
and `kappa=1/2` without inserting either derivative or kappa separately.
Nevertheless, selecting that relative action coefficient remains precisely
the missing numerical input.

## Domain, extrema, and endpoint checks

The bound `q<=1` is essential. Positivity alone admits additional stationary
branches: `q1=q2=1/(1-t)` for `0<t<1`, and the asymmetric pair
`q1=1+t/sqrt(1+t^2)`, `q2=1-t/sqrt(1+t^2)` (or exchanged) for every `t>0`.
The logarithm alone therefore does not select the proposed physical branch.

On the stated branch the auxiliary Hessian has diagonal entries
`[1-(1+t)^2]/lambda^2` and off-diagonal entries `-y^2`. Its symmetric and
antisymmetric eigenvalues are respectively

`-2y(1+lambda*y)/lambda`, `-2y/lambda`.

They are strictly negative for `y>0` and both vanish at `y=0`. Thus `W` is
maximized, not minimized, over the auxiliary variables. In fact this is the
unique global maximum: `W` tends to minus infinity as either `q_i` tends to
zero, while at a face `qi=1` for `y>0` its derivative is `-y^2 qj<0`, so an
inward displacement increases `W`. The unique interior stationary point
must then be the maximum. At `y=0`, `U'(q)>0` for `q<1` proves the unique
maximum at `(1,1)` directly. The full action's auxiliary Hessian has the
opposite sign. These are static auxiliary statements, not a proof of
relativistic or dynamical stability.

The reduced density begins as
`W_red=(4/3)lambda*y^3-(3/2)lambda^2*y^4+O(y^5)`.
For `t>0`, both static flux eigenvalues are positive:
`mu>0` and `mu+y mu'=t(t^2+3t+4)/(1+t)^3>0`.
They vanish at the origin, so ellipticity is degenerate there. Also `mu->1`
at large `y`. All these properties hold for every `lambda>0`; none singles
out one. The zero-field degeneracy does not create extra stationary solutions
within the stated domain, but excludes a nondegenerate-Hessian argument there.

## Dependency and obligation record

`chosen U, relative weight, and domain` -> `auxiliary stationarity` ->
`unique reduced constitutive law` -> `deep-limit matching convention` ->
`kappa=1/(2 lambda)` -> **additional coefficient selection** -> `kappa=1/2`.

| Obligation | Result |
| --- | --- |
| Stationarity, existence, uniqueness in the stated domain | Passed analytically |
| Exact elimination, flux sign, source normalization | Passed analytically |
| Zero-field endpoint and auxiliary Hessian | Passed with degeneracy recorded |
| Uniqueness assuming positivity alone | Failed; explicit branches above |
| Unit slope for the specifically selected lambda=1 action | Passed |
| Exchange symmetry/channel count fixes lambda | Failed; the full family is symmetric |
| Particle interpretation, covariant completion, dynamical viability | Not established |
| Historical novelty or observational acceptability | Not addressed |

Hand-checks independent of a symbolic simplifier: at `(lambda,y)=(1,1)`,
`q=1/2`, `mu=3/4`, `W_red=2-2 log 2`, and the Hessian eigenvalues are
`-4,-2`; at `(2,1)`, `q=1/3`, `mu=8/9`, and the eigenvalues are `-3,-1`.
These corroborate signs and factors; the universal conclusions use the
explicit derivations above, not sampling. No numerical run, external theorem,
or literature claim is needed for this audit. Repository inspection used
`git rev-parse HEAD`, `rg --files`, and reads of `ACTION_ROUTE.md` and the
developing `UnitResponse.lean`; no Lean compilation was performed by this reviewer.

The auxiliary representation is an exact variational realization of a selected
interpolating function. Because eliminating the fields leaves precisely
`mu=1-(1+lambda*y)^(-2)`, it supplies no additional reduced static predictions
beyond that chosen law. Its useful contribution is an explicit local action
with algebraic auxiliaries, not an independent physical explanation of the
law's shape or normalization. No propagation equation for these auxiliaries
or additional particle species has been introduced.

The exact remaining gap is an independently motivated restriction selecting
both the proposed action structure and `lambda=1` at the fixed vacuum scale.
The cheapest discriminating next check is to exhibit a concrete symmetry or
physical constraint whose equation changes when `lambda` changes and whose
derivation does not use the desired unit slope or half. Reimposing the half
as an auxiliary constraint would merely transfer the original assumption.
