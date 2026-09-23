# Small-delay remainder: an explicit bound on all collision orders

Codex derivation, 22 September 2026. Status: proved under the definitions below
in a separate self-review pass; not independently refereed, not an established
novelty claim, and not a confirmation of the JWST scattering interpretation.

## Model and statement

A photon starts at the centre of a unit sphere at time zero, travels at speed
one, and scatters at a uniform rate tau > 0. After each collision its direction
has the scalar, unpolarized Thomson law

    K(u,dv) = (3/4)(1+(u dot v)^2) dnu(v),   dnu = dOmega/(4 pi).

There is no absorption. Let N be the number of collisions before first exit,
T the exit time, x the exit position, u_N the outgoing direction, and
D = T - x dot u_N. Count all emitted photons. Define

    B_tau(e) = (3 tau e/4) [1 + log(4/e)],                 0 < e <= 1.

For each integer n >= 1,

    P(0 < D <= e, N=n) <= B_tau(e)^n.                    (1)

Consequently, whenever B_tau(e) < 1,

    R_tau(e) := P(0 < D <= e, N>=2)
             <= B_tau(e)^2 / [1-B_tau(e)].               (2)

In particular, at every fixed tau,
R_tau(e) = O_tau(e^2 log^2(1/e)) = o(e log(1/e)).

## Proof

Write l_0,...,l_(n-1) for the complete flights ending at collisions, with
directions u_0,...,u_(n-1), and L for the final flight in direction u_n.
Each collision flight has length at most two; the first is actually at most
one. First-exit geometry gives

    x = sum_(j=0)^(n-1) l_j u_j + L u_n,
    T = sum_(j=0)^(n-1) l_j + L,
    D = sum_(j=0)^(n-1) l_j (1-u_j dot u_n).             (3)

Every summand is nonnegative. Thus D <= e implies each summand <= e.
This statement includes arbitrarily short flights; no positive lower bound on
collision separation is imposed.

On the admissible first-exit domain the path probability measure for exactly
n collisions, conditional on u_0, is

    tau^n exp[-tau(sum l_j+L)] product_j dl_j
       product_(j=1)^n K(u_(j-1),du_j).                 (4)

The last exponential factor includes survival without another collision to the
boundary. Remove the attenuation factor using exp(-tau T) <= 1. Bound each
Thomson density relative to nu by 3/2. Enlarge the collision-flight domain to
[0,2]^n and replace the delay event by the n separate inequalities from (3).
All these changes increase the nonnegative integral. No sphere-exit length is
evaluated outside the original admissible domain: attenuation has already
been removed before that enlargement.

For a fixed unit vector v and l>0, the normalized area of the cap
{u: l(1-u dot v)<=e} is

    b_e(l) = min(1,e/(2l)).                             (5)

Set b_e(0)=1, which does not affect any length integral. In the enlarged
integral the intermediate directions u_1,...,u_(n-1) can be integrated
independently conditional on u_n; they give the factors b_e(l_1),...,b_e(l_(n-1)).
The remaining u_n integral constrained relative to fixed u_0 gives b_e(l_0).
This is a factorization of an UPPER-BOUND PRODUCT MEASURE after removing the
kernel dependence; it is not an assertion that physical scattering directions
are independent. Averaging the initial direction leaves the same bound.

Therefore the enlarged integral equals

    (3 tau/2)^n [integral_0^2 b_e(l) dl]^n.

Splitting the integral at e/2 evaluates it as

    integral_0^2 b_e(l) dl = (e/2)[1+log(4/e)].          (6)

This proves (1). Summing the disjoint events over n>=2 and using the geometric
series for B_tau(e)<1 proves (2). It gives an explicit summable majorant for
all orders at once; no unproved exchange of asymptotic expansions is used.
Since B_tau(e)=O_tau(e log(1/e)) tends to zero, the stated remainder follows.

For completeness, exit occurs after finitely many collisions almost surely.
At any collision the next boundary distance is at most two, so the conditional
chance of exiting before the next collision is at least exp(-2 tau). Induction
bounds the tail of N by a geometric sequence. The scattering rate is finite,
so there is no finite-time accumulation of collisions. Also, (1) applied to
{D=0,N=n} via {D<=e,N=n} and then e decreasing to zero shows that scattered
zero-delay trajectories have probability zero. Thus the sole zero-delay atom
is P(N=0)=exp(-tau).

## Full positive-delay asymptotic

The previously derived one-scatter leaf ONE_SCATTER.md gives

    F1(e) ~ (3 tau/4) exp(-tau) e log(1/e).

Combining that leaf with (2), rather than assuming a remainder, gives

    P(0<D<=e) ~ (3 tau/4) exp(-tau) e log(1/e).          (7)

The rate tau is fixed in this limit. Neither the coefficient nor a relative
error statement is asserted uniformly as tau tends to infinity.
The earlier one-scatter attenuation sandwich and (2) also give a finite bound:
if A(e)=tau exp(-tau)[(3/4)e log(2/e)+3e^2/8-e^3/16], then

    exp(-tau e) A(e) <= P(0<D<=e)
                    <= A(e) + B_tau(e)^2/[1-B_tau(e)].

## Refutation of the cubic two-scatter claim ee65d549

For 0<e<=1 restrict both collision flights r,l to [1/8,1/4], and restrict
u_1,u_2 to the same cap around u_0 with 1-u_i dot u_0 <= e/4.
Both collision positions lie inside radius 1/2. If the cap half-angle is delta,
then 1-u_1 dot u_2 <= 1-cos(2 delta) <= 4(1-cos delta) <= e.
Equation (3) gives D <= 5e/16. It is positive except on a zero-measure set.
The total path length T is at most r+l+(1+|r u_0+l u_1|)<=2.
Each Thomson density relative to nu is at least 3/4, and each cap has
nu-area e/8. Integrating (4) over this admissible subfamily proves

    P(0<D<=e,N=2) >= (9 tau^2 exp(-2 tau)/65536) e^2.   (8)

For fixed tau the constant is strictly positive. Hence this probability is
not O(e^3), contradicting ee65d549's claimed exact cubic asymptotic. This does
not identify the sharp two-scatter asymptotic; an e^2 log^2(1/e) term remains
compatible with (1) and (8).

## Adversarial self-review and dependencies

Checked separately: kernel normalization and 3/4,3/2 bounds; the distinction
between solid-angle and cosine densities; exactly n collision flights plus
one escape flight; the nonnegative path identity; admissibility and enlargement
direction; conditional factorization only AFTER kernel domination; the l=0
endpoint and short flights; the geometric sum and fixed-tau limit; finite exit;
the unscattered atom; and the admissible lower-bound subfamily. No gap was found
in these steps. This is self-review by the deriving agent, not peer review.

Dependency graph: model law -> path measure/identity -> cap measure -> (1)
-> (2); (2) + pinned one-scatter leaf -> (7). Simulations and literature are
not premises of this proof. The six-million-photon calculation is a finite
consistency check using a shared transport implementation, not proof of (1).

Small-delay separation of scattering orders overlaps established inverse
transport methods. See SOURCES.md; novelty and a useful measured JWST
consequence remain unresolved. Absorption-conditioned moments, polarization,
noncentral sources, singular angular kernels and moving media are outside
this statement.
