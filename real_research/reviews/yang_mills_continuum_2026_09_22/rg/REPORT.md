# YM-C1 RG bridge: exact budgets and the metric obstruction

Owner: `ym_rg_bridge`. Checkpoint: `YM-C1-RG-1`, 2026-09-22.
Delegated base: `b73311096299e2f1816be00036ccdb2922bc44d4`.
Observed working-tree HEAD during this run:
`a0dc7c516f7a5c33ae9db03a9af6340ffdc74d2c`; this discrepancy was reported to
the coordinator. The argument pins actual input content rather than assuming
that HEAD and the delegated base coincide.

Inputs (SHA-256):

- `../CONTRACT.md`:
  `563555c68bafae04e62b69fef58ffb5f8f8aac8db93afafc9d4e72a98052f114`.
- `../../spectral_spine_closure_2026_09_22/i15/PROOF.md`:
  `223d5d0f7ba6bd6fc7cfeffc8cfa18ac32c906e7172af2f4acd2708b5e149b72`.

## Outcome and first unsupported estimate

No continuum Yang--Mills construction or mass-gap proof was obtained.
There is a precise viable *conditional interface*: use exact vacuum-subtracted
Schur forms together with their induced Hilbert metrics. If eliminated modes
have physical gaps of order `x_j/a_j`, their inverse-gap cost is summable
along an asymptotically-free scale profile. This is much more favorable than
an additive operator-norm error at each scale.

The first unsupported Yang--Mills estimate is the construction of a gauge-
compatible coarse projection for which the eliminated block of the *true
vacuum-subtracted Hamiltonian* obeys

    D_j >= c x_j/a_j

uniformly in volume, cutoff, and admissible coarse configurations. Next one
must control the exact Schur form AND its induced metric all the way to a
terminal coarse Hamiltonian satisfying a uniform gap estimate. The fact that
a Wilson coupling runs into the strong-coupling region supplies neither
estimate. The inherited I15 theorem applies to its specified Wilson
Hamiltonian in the standard product Haar metric, not automatically to the
Schur complement and nonlocal metric produced by eliminating modes.

The source check of Chatterjee's confinement criterion is complete at the
theorem-statement and application level. Balaban's 1989 paper is
bibliographically authenticated, but its exact theorem text was unavailable
through the tested primary endpoints. No Balaban theorem is used as a proved
leaf in the mathematics below. See `SOURCES.md` for the exact status.

## 1. Units and the starting endpoint

The initial Hamiltonian has dimensionless gap `Delta(x)` at spacing one:

    H(x)=(x/2) sum C_l + (b_N/x) sum_p(1-Re Tr(U_p)/N).

At physical spacing `a`, physical gap is `m=Delta/a`. The inherited theorem
gives `Delta>=3x/16` for `x>=X_d`, where no numerical `X_d` was established.
Consequently a terminal *actual Wilson Hamiltonian* at spacing `A` and
coupling `x_*>=X_d` would have `m_*>=3x_*/(16A)`.

Let `L>1` be a blocking factor, `a_j=a L^j`, `0<=j<=K`, and `A=a_K`.
The ultraviolet limit at fixed endpoint scale is `K->infinity`,
`a=A L^{-K}`. Each Hamiltonian in a spectral comparison must have its own
actual vacuum energy subtracted. Subtracting a trial-state expectation is
insufficient, as already established by the inherited I15 proof.

## 2. Exact error accounting for approximate gap transport

**Lemma 1.** Suppose that at each scale an established comparison gives

    Delta_j >= (1-epsilon_j) Delta_{j+1}/L - delta_j,
    0<=epsilon_j<1, delta_j>=0.

Write `P_0=1`, `P_j=product_{i=0}^{j-1}(1-epsilon_i)`. Then

    m_0 >= P_K Delta_K/A - sum_{j=0}^{K-1} P_j delta_j/a_j.       (1)

Proof: divide the one-step inequality by `a_j` and use
`L a_j=a_{j+1}`. Successive substitution gives (1), including the empty
product in its first error term. There is no hidden volume normalization.

In particular, a usable lower bound requires a positive limiting product
and an additive budget smaller than the retained endpoint gap. Uniformly
small errors are not sufficient. If `epsilon_j=epsilon>0`, the product is
`(1-epsilon)^K->0` even when every `delta_j=0`.

For a transparent exact model of ultraviolet running, define

    n=K-j, x_j=1/(s+q n), s>0, q>0.                            (2)

This is an abstract scale profile, NOT a theorem about the exact
Yang--Mills flow and NOT an extension of perturbation theory into strong
coupling. The subsequent claims are exact implications of (2).

For `epsilon_j=C x_j^p`, `C>0`, `p>0`, with all factors bounded away from zero,
`P_K` has a positive limit if and only if `p>1`. Indeed,
`log(1-u)` is comparable to `-u` when `u` is bounded below one, and the
corresponding series is `sum_{n>=1}(s+qn)^{-p}`. Thus relative losses of
order `x^2=g^4` are summable; losses of order `x=g^2` are not, absent an
additional cancellation or a different normalization of the comparison.

If the only available additive estimate is `delta_j<=C x_j^p`, its
worst-case physical budget is

    (C/A) sum_{n=1}^K L^n/(s+qn)^p,                           (3)

which diverges for every fixed finite `p`. This does not assert that the
true errors are that large: it says that the polynomial upper estimate
alone cannot certify a positive continuum gap by (1).

For `delta_j<=C exp(-c/x_j)`, the analogous unweighted budget is

    (C exp(-cs)/A) sum_{n=1}^K exp[n(log L-cq)].                (4)

It is uniformly finite exactly when `cq>log L`; at equality it grows
linearly in `K`, and below equality exponentially. A finite budget must
still be smaller than the retained endpoint mass. If the products `P_j`
are uniformly bounded below, the same convergence/divergence thresholds
hold for the weighted budget. These thresholds are specific to the
comparison (1), not universal requirements on every possible proof.

**Decisive counterexample to polynomial-error sufficiency.** Let `L=2`,
`s=q=1`, `p=2`, `A=1`, and for `K>=6` set

    Delta_j=2^{j-K} for j>=1,  Delta_0=2^{-2K},
    epsilon_j=0, delta_0=(K+1)^{-2}, delta_j=0 for j>=1.

Since `(K+1)^2<=2^K` for `K>=6` (check `K=6`, then use
`((K+2)/(K+1))^2<2`), the comparison of Lemma 1 holds at every scale.
Each gap can be realized by the positive two-state Hamiltonian
`diag(0,Delta_j)`. The endpoint physical gap equals one, while
`m_0=Delta_0/a=2^{-K}->0`. Thus the comparison hypotheses plus an
`O(x^2)` additive error really permit collapse; this is not just a loose
sign estimate in (3). The two-state family is a counterexample to that
abstract inference, not to Yang--Mills.

## 3. Exact block elimination and a favorable inverse-gap sum

The coordinator supplied the following exact block mechanism during this
run. Here is a finite-dimensional independent derivation, adequate to
identify the scale budget without asserting unproved operator domains.
The coordinator's route owns the closed-form-domain extension.

Let a nonnegative self-adjoint matrix be split as

    H = [[A,B*],[B,D]],  D>=d I>0,
    C=D^{-1}B, S=A-B*D^{-1}B, Jp=(p,-Cp), G=J*J=I+C*C.

The Schur form `S` is nonnegative. Suppose it has a one-dimensional
kernel and the generalized gap in the `G` metric is `gamma>0`, meaning

    <p,Sp> >= gamma inf_{z in ker S} ||J(p-z)||^2.             (5)

Then `ker H=J ker S` and

    gap(H) >= (gamma^{-1}+d^{-1})^{-1}.                       (6)

Proof: write `v=(p,q)=Jp+(0,r)`, where `r=q+Cp`. Completion of squares
gives `h[v]=<p,Sp>+<r,Dr>`. If `z` minimizes the distance in (5),

    dist(v,ker H) <= ||J(p-z)||+||r||
                     <= sqrt(<p,Sp>/gamma)+sqrt(<r,Dr>/d).

Weighted Cauchy--Schwarz bounds its square by
`(gamma^{-1}+d^{-1})h[v]`. This proves (6).

For a sequence of exact eliminations in the successive induced Hilbert
metrics, let `m_j` denote physical gaps and let `d_j` be eliminated-sector
physical gap lower bounds. If the next coarse operator is exactly the
generalized Schur operator, (6) implies

    1/m_0 <= 1/m_K + sum_{j=0}^{K-1}1/d_j.                   (7)

This is conditional on the stated exact operator construction at every
step. One cannot substitute a convenient Wilson operator for the exact
coarse operator without an additional comparison.

**Lemma 2 (summable ultraviolet elimination cost).** Under (2), suppose

    d_j >= c x_j/a_j, c>0,
    m_K >= M/A, M>0.

Then (7) yields for every `K`

    m_0 >= A^{-1} / [ M^{-1}
               + c^{-1}{s/(L-1)+qL/(L-1)^2} ].              (8)

Proof: with `n=K-j`,

    sum 1/d_j <= (A/c) sum_{n=1}^K (s+qn)L^{-n}
               <= (A/c){s/(L-1)+qL/(L-1)^2}.

The last identity follows from the geometric series and its derivative.
It is independent of the number of ultraviolet scales. If a valid
terminal comparison supplies `M=3x_*/16`, insert that value in (8).

More generally, a lower bound `x_j>=c_0/(1+K-j)^r` for any fixed finite
`r>=0` suffices for finiteness, since
`sum_{n>=1}(1+n)^r L^{-n}<infinity`. Exact beta coefficients and an exact
one-loop flow are therefore unnecessary for the *summability* step.
They do not establish the eliminated-mode coercivity or terminal gap.

## 4. A coarse metric cannot be discarded

For `t>=0`, consider the exact matrix

    H_t = [[0,0,0], [0,1+t^2,t], [0,t,1]],

with the first two coordinates retained. Then

    D=1, S=diag(0,1), G=diag(1,1+t^2), gamma=1/(1+t^2).

The ordinary Schur gap is always one, but the full gap is

    lambda_-(t)=(t^2+2-sqrt(t^4+4t^2))/2 -> 0.

At `t=2`, the false estimate obtained by ignoring `G` would give `1/2`,
while the true gap is `3-2 sqrt(2)<1/2`. The corrected (6) gives `1/6`,
and `1/6<=3-2 sqrt(2)`. Positivity and the kernel can be checked without
diagonalization from

    <(p0,p1,q),H_t(p0,p1,q)> = |p1|^2 + |t p1+q|^2.

Thus positivity, a good eliminated-sector gap, and a positive ordinary
Schur gap are insufficient if the induced metric is uncontrolled.
An eventual Yang--Mills terminal comparison has to bound generalized
Rayleigh quotients, or obtain a uniform comparison of the induced metric
to the standard metric.

**Lemma 3 (an energy-relative terminal metric bound suffices).** Suppose
`S>=0` has kernel spanned by a standard-normalized vector `Omega`, and
an ordinary gap `Delta>0`. Set `Q=I-|Omega><Omega|`. It is enough to prove
the form estimate

    Q G Q <= M Q + eta S,  M>0, eta>=0,                       (9)

on the common form domain. Then its generalized gap satisfies

    gamma >= (M/Delta+eta)^{-1}.                             (10)

In physical energy units, `Delta,gamma,S` have energy units, `G,Q,M`
are dimensionless, and `eta` has inverse-energy units. Thus both terms
in the denominator of (10) have inverse-energy units. The same argument
can instead be applied entirely in dimensionless lattice units, followed
by one division by the terminal spacing `A`.

Indeed, in the infimum defining `dist_G(p,ker S)`, take the particular
representative `Qp`. Since `s[Qp]=s[p]` and
`||Qp||^2<=s[p]/Delta`, (9) gives

    dist_G(p,ker S)^2 <= <Qp,GQp>
                       <= (M/Delta+eta)s[p].

The statement is immediate for matrices. For nonnegative closed forms,
assume `Omega` is in the metric form domain, the `S` form domain is
contained in the `G` form domain, and (9) holds there. Then `Q` preserves
the relevant domains and the same argument applies. An inequality on an
unrelated core without its form closure would not justify this extension.

This criterion avoids a global bound on `G`: large vacuum dressing is
irrelevant to the upper bound on the quotient distance, and growth of
the metric in high-energy directions can be paid for by `eta S`. For
the preceding `H_t` example, `M=1`, `eta=t^2`, `Delta=1` gives the exact
generalized gap. If a terminal comparison proves
`S>=alpha K` with the SAME kernel as a gapped reference Hamiltonian
`K` of gap `Delta_ref`, one may use
`Delta=alpha Delta_ref` in (10). Vacuum alignment and this form
comparison are extra hypotheses, not consequences of coupling matching.

## 5. Why partition stability cannot supply the missing arrow alone

Take `H_eta=diag(0,eta)` with `eta>0`. Its vacuum-subtracted partition
function satisfies `1<=Tr exp(-t H_eta)<=2` for all `t>=0`, uniformly
as `eta->0`. Yet its gap is `eta->0`. A product of `V` copies gives
`1<=Z<=2^V` with exactly the same collapsing gap. Consequently
upper/lower exponential-volume partition bounds, even uniform in the
cutoff and valid at all nonnegative times, do not by themselves imply a
uniform gap. Decay estimates that distinguish the vacuum contribution
from the first excitation are a different input.

This is a direct algebraic non-implication, not a claim about what every
estimate in Balaban's full program can or cannot prove. It prevents using
the phrase “ultraviolet stability” as a substitute for (5), (7), or a
uniform connected-correlation estimate.

## 6. Executed checks, interpretation, and next action

`check_rg.py` uses exact rational arithmetic to check the telescoping
identity against direct recursion, the finite geometric sum against its
closed form, and the gap-collapse and metric counterexamples at declared
finite values. The universal conclusions above are supplied by the
displayed proofs, not by extrapolating the script. Run provenance and
input/output hashes are in `run/manifest.json`.

The computation does not construct a Yang--Mills block projection,
compute a Yang--Mills vacuum, or verify a nonperturbative RG flow.

The next discriminating task is to choose one concrete gauge-compatible
block map and determine whether its exact *vacuum-subtracted* eliminated
block satisfies `D_j>=c x_j/a_j`. A proof only for the bare electric
Hamiltonian or an unshifted positive Hamiltonian does not meet that
contract. If this first condition survives, measure/control the induced
metric and compare the terminal generalized form to the I15 endpoint.
The inverse-gap budget is already adequate under a very weak polynomial
lower bound on the running coupling; sharpening the beta-function
coefficients does not resolve the present bottleneck.
