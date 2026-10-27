# An explicit window error for a conditioned harmonic cloud

19 October 2026. Bounded analytic supplement to `CANONICAL_RESPONSE.md`.
This calculation conditions a Maxwell-Boltzmann distribution on particle
positions inside a fixed ball. It introduces no reflecting force and does
not assert that the original scalar action maintains that condition.

**Result.** For positive compression, the conditioned induced width lies
below the rational curve normalized to its own reference width. Its
absolute error divided by that reference width obeys

\[
 0\le {Q_{0c}E/(a+E)-p_c(E)\over Q_{0c}}
 \le {\epsilon(x_0)\over s[1-\epsilon(x_0)]},
 \qquad s=1+E/a\ge1.                                      \tag{1}
\]

Here `x0=m kappa0 R_c^2/(2T)`, and the explicit exponentially small
function `epsilon` is derived below. The bound is for the declared
conditioned state, rather than a dynamical finite-core equilibrium.

## State and exact conditioned partition function

Keep the parent's `N,m,T,L,kappa0>0`, `a=kappa0 L`,
`kappa=kappa0+E/L=kappa0 s`, and actual source

\[
 Q={m\over2L}\sum_{i=1}^N r_i^2,\qquad H(E)=H(0)+EQ.
\]

At each source value condition the independent classical canonical state
on `r_i<R_c` for every particle, with `R_c` fixed as `E` changes. Momenta
remain unrestricted Gaussian variables. This is a statistical conditional
distribution on a fixed domain. Its position density is proportional to
`exp[-m kappa sum_i r_i^2/(2T)]` on the product of balls. All assumptions
about dilution, the tracer limit and the original matched contact remain
those of the parent note; in particular the peak density, not only a
reference average, must remain dilute throughout the selected window.

Define the regularized lower incomplete gamma function

\[
 P(\alpha,x)={\gamma(\alpha,x)\over\Gamma(\alpha)},\qquad
 \gamma(\alpha,x)=\int_0^x t^{\alpha-1}e^{-t}\,dt,\qquad
 x={m\kappa R_c^2\over2T}=x_0s .                           \tag{2}
\]

The substitution `t=m kappa r^2/(2T)` in the radial integral gives the
single-particle spatial partition function as its unconditioned harmonic
value times `P(3/2,x)`. Therefore, with momentum factors and `1/N!`
canceling in the ratio,

\[
 {Z_c(E)\over Z_c(0)}
 =s^{-3N/2}\left[{P(3/2,x_0s)\over P(3/2,x_0)}\right]^N.
                                                               \tag{3}
\]

The same radial substitution in the second moment yields

\[
 \boxed{\langle Q\rangle_c(E)
 ={3NT\over2L\kappa}\,{P(5/2,x)\over P(3/2,x)}}.          \tag{4}
\]

It also equals `-T partial_E log Z_c`, since the conditioning domain is
independent of `E`. This identity is a statistical derivative; using it
as a physical quasistatic work formula would additionally require a
mechanism that realizes the family of conditional states.

## Recurrence and monotonicity

Integration by parts gives
`gamma(alpha+1,x)=alpha gamma(alpha,x)-x^alpha exp(-x)`.
For `alpha=3/2`, put

\[
 R(x)={P(5/2,x)\over P(3/2,x)}=1-\epsilon(x),\qquad
 \boxed{\epsilon(x)={x^{3/2}e^{-x}\over
                       \Gamma(5/2)P(3/2,x)}}.             \tag{5}
\]

Both `R` and `epsilon` are strictly between zero and one for `x>0`.
To establish the direction needed in (1), let

\[
 \mu(x)={\gamma(\alpha+1,x)\over\gamma(\alpha,x)}
       =\alpha R(x).
\]

This is the mean of `t` under its positive Gamma density conditioned on
`0<t<x`. Hence `0<mu(x)<x`. Direct differentiation gives

\[
 \mu'(x)={x^{\alpha-1}e^{-x}\over\gamma(\alpha,x)}
                [x-\mu(x)]>0.                            \tag{6}
\]

Thus `R(x)` strictly increases and `epsilon(x)` strictly decreases. An
equivalent direct check is
`d log epsilon/dx=alpha R(x)/x-1<0`. Moreover `R(x)->1` as `x->infinity`.
This proves monotonicity analytically; illustrative values below are not
used to establish it.

## Curve normalized to the actual truncated reference width

Write `Q0=3NT/(2a)`, `epsilon0=epsilon(x0)` and `R0=1-epsilon0`.
The correct reference value and induced response are

\[
 Q_{0c}=Q_0R_0,\qquad
 p_c(E)=Q_{0c}-\langle Q\rangle_c(E)
       =Q_0\left[R_0-{R(x_0s)\over s}\right].             \tag{7}
\]

Compare this with the rational curve having the same reference width,
`p_rat,c(E)=Q0c E/(a+E)=Q0 R0(1-1/s)`. Subtraction gives the exact error

\[
 \boxed{{p_{\rm rat,c}(E)-p_c(E)\over Q_{0c}}
 ={\epsilon_0-\epsilon(x_0s)\over s(1-\epsilon_0)}}.
                                                               \tag{8}
\]

For `s>=1`, monotonicity gives (1). The error vanishes at `s=1` and tends
to zero as `s->infinity`; the upper bound is deliberately conservative
near the reference point. In particular the uniform absolute normalized
error on every chosen positive-compression window is at most
`epsilon0/(1-epsilon0)`. These are absolute errors in `p/Q0c`, not relative
errors divided by the induced response, which vanishes at the reference.

The response remains nonnegative: for this fixed conditional domain,
`d<Q>/dE=-Var_c(Q)/T<0`. Hence
`0<=p_c(E)<=p_rat,c(E)<=Q0c` for `E>=0`. The reference-width correction
itself is exactly `(Q0-Q0c)/Q0=epsilon0`. Neither (1) nor its sign is
asserted for negative source increments, which reduce `x` below `x0`.

## Illustrative size of the analytic bound

The following numbers are rounded direct evaluations of (2), (5) and (8),
using Python 3.9.6 / mpmath 1.3.0 with 50 decimal working digits. The call
was a short interactive evaluation, not a new runner-backed scientific
experiment or a certified interval calculation. The proof of (1) is the
analytic argument above. The recurrence expression and direct ratio of
the two incomplete gamma functions agreed at the displayed precision.

| `x0` | `1-P(3/2,x0)` | `epsilon0` | Uniform bound `epsilon0/(1-epsilon0)` | Exact absolute normalized error at `s=2` |
|---:|---:|---:|---:|---:|
| 5 | `0.0185661` | `0.0577411` | `0.0612795` | `0.0300666` |
| 10 | `0.000169742` | `0.00108017` | `0.00108134` | `0.000540600` |
| 20 | `1.06551e-8` | `1.38682e-7` | `1.38682e-7` | `6.93409e-8` |

At `s=2`, the bound in (1) is one half the uniform bound in the fourth
column. Thus, for example, `x0=10` bounds the absolute normalized curve
error by `0.00108134` throughout any positive-compression window where
the other model approximations hold. No claim is made that the tracer,
classical or dilute regime persists to arbitrarily large `s`.

The second column is the unconditioned single-particle probability of
lying outside the declared ball. The unconditioned probability that all
N independent particles lie inside is `P(3/2,x0)^N`, which need not be
close to one at large N. A small one-particle tail therefore does not by
itself justify conditioning every member of a macroscopic cloud or prove
negligible evaporation. The weighted second-moment error is controlled
here by its explicit incomplete-gamma calculation, rather than by an
assumption that an unweighted tail probability bounds an unbounded moment.

## What this window does not establish

This supplement supplies an explicit, preparation-dependent correction
to the rational *curvature-moment* response under a declared statistical
condition. A finite Newtonian host still has a nonconfining outer tail.
No reflecting wall, dynamical trapping mechanism, escape lifetime,
replenishment/selection process, heat receiver or equilibration rate has
been derived. Maintaining a fixed conditioned inventory as E changes
requires such additional physical information. The heat and entropy cost
of any real selection/replenishment mechanism is absent from this trace.

The source remains the even second moment `Q`, conjugate to an isotropic
curvature increment. Conditioning supplies neither an internal mass
dipole conjugate to uniform acceleration nor a source-preserving map to
the desired polarization. The inventory, T, core, R_c, L and receiver
remain state/protocol inputs; no universal G normalization follows.

## Exact parent and write scope

Parent file SHA256:
`CANONICAL_RESPONSE.md` =
`e97cb72d71a31a31226414184ff8bf1f5a5280596a7d01f8028ed3690727c622`.
This includes its explicit finite-core conditioning/escape caveat and
N=1 / independent-MB quantum qualification. The separate TF comparison
was not used to derive this result.

Only this new `FINITE_CORE_WINDOW.md` was written for the refinement.
Existing notes, scientific code, contracts, run outputs, manifests and
evidence were not modified. The primary result is analytic; the displayed
numbers are illustrative evaluations of its exact formula.
