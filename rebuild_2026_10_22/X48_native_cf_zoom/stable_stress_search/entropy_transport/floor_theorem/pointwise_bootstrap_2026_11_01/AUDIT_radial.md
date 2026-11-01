# Independent audit of radial heat histories and delayed release

Primary verdict: **proved as written**, for the conditional actual-history
claims (R9)--(R12) and the stated coefficient-class counterexample to
(R15). The original common compression interval and actual pointwise stress
estimate remain open; this audit does not validate an unclaimed implication
to either.

Audited artifact: [radial_route.md](radial_route.md), SHA-256
`70a7b577c14a898042d6a70a23044bc4ffbab930526c2e59274bb994c69100ea`.
Base checkpoint: **X48-DEN-2026-11-01-A**; observed source HEAD
`8a293ba8b8411e84c9e37bb9770d1a6f993f606e`. This independent reviewer
reconstructed the critical steps from the exact four law files, without
editing the proof note. Write scope: this audit file only.

## Claim cards and dependency graph

**Actual-history claim.** For every finite N and actual prefix satisfying
the explicit state box (R6) on the whole interval from cold activation to
`s<=10^-3`, the outgoing face luminosity obeys
`integral_0^s L_j <=2517*j*dm*s^3`. At the origin,
`Var K_1 <=(10000/3)*s^3` and the time integral of the absolute local
stress heat source is at most `(6.5e8/3)*s^5`. These conclusions are
conditional on the state box and on prefix coverage. They do not give a
common interval on which that box holds.

**Coefficient-class claim.** Fix `c>0`, `0<epsilon<=1/2`, and `t_*>0`.
For the fixed homogeneous radial mechanical graph, scalar conservative
time-dependent heat with only its first face open can satisfy
`0<=B_N(t)<=epsilon A_N` as forms, positive outward heat and a scalar
maximum principle, while the solution of (R13) violates every uniform
estimate (R15) using only the initial weighted L2 norms. The initial heat
state may have fixed pointwise amplitude. These clocks are prescribed
coefficients; they are not the actual constitutive gates or the cold IVP.

The dependency graph has two separate branches:

1. Exact heater and shared luminosity -> moving-weight prefix balance ->
   nonnegative thermal content -> (R9), then (R10). First-cell no inflow
   -> direct variation bound (R11) -> constitutive derivative -> (R12).
2. Exact first radial rate -> finite substochastic mechanical semigroup ->
   smooth first-face heat clock and explicit two-cell solution -> signed
   first-cell Duhamel lower bound -> contradiction to (R15).

Every leaf in these two branches is an internal identity, an explicit
finite-dimensional construction, or an elementary inequality. No external
regularity theorem, continuum limit or numerical trajectory is a proof leaf.

## Independent reconstruction of the actual-history estimates

The exact normalized source is

\[
 Q=h\{\tfrac12x(x-2)_++\tfrac12g x^2\}.
\]

On the active box `2<x<=8` this is (R3). Since `g<=100K`,
`Q<=200s^2*(24+3200K)<5000s^2`. Also the exact material identity
`W_rho=h` gives `W_t=rho*h*x<=1616s^2`. Thus the bounds (R7) do not
omit the memory heater or a moving-weight term.

The exact heat contribution to `dm*(WK)'` is `L_(i-1)-L_i`.
Summation over cells `1,...,j` cancels all internal luminosities and
retains exactly `-L_j`, because `L_0=0`. The remaining source satisfies

\[
 WQ+K W_t\le7550s^2+2585600s^5<7551s^2
 \quad(s\le10^{-3}).
\]

With zero initial thermal content and nonnegative final thermal content,
integration gives `7551*j*dm*s^3/3=2517*j*dm*s^3`, exactly (R9).
This argument uses positivity of outward luminosity and does not assume
the prefix is insulated or its last face is closed.

Dividing the two adjacent flux integrals by `dm W>=3dm/2` gives
`integral |H_j|<=1678*(2j-1)*s^3`. Adding the heater integral gives
`Var K_j <=[3356j-34/3]*s^3<=3356j*s^3`, so the slightly generous
constant in (R10) is valid, including j=1. This estimate is not uniform
in a cell index growing with N, and the proof note correctly preserves
that distinction.

At cell 1 one can instead integrate its own equation:

\[
 \int_0^s\frac{L_1}{dm W_1}
       =\int_0^sQ_1-K_1(s)\le\int_0^sQ_1.
\]

This does not integrate a time-dependent coefficient by parts; it simply
integrates the exact equation for K. Therefore
`Var K_1<=2 integral Q_1<=(10000/3)*s^3`. The separate moving W term is
already included in the prefix-energy argument, where it belongs.

Finally, `S_K=kappa*g'*x+rho^2*h` is positive on the active box, with

\[
 S_K\le[\tfrac12(1.01)(1.51)(200)(100)(8)
                 +(1.01)^2(200)]s^2
       <1.3\,10^5s^2.
\]

There is no incoming luminosity at the origin, so `H_1<=0`.
Bounding the coefficient on `[0,s]` by `1.3e5*s^2` and using the last
flux integral proves (R12), including its sign and `s^5` power. This
controls the origin's own heat term only. It does not control a heat
source born elsewhere and subsequently propagated mechanically to cell 1.

## Independent reconstruction of the coefficient-class counterexample

At homogeneous density, the first mechanical row has only one exit and
its rate is exactly

\[
 \lambda_N=\frac{(4\pi r_1^2)^2}{dm V_1}
       =144b^4\rho_*N^{2/3}.
\]

The mechanical exterior Dirichlet face and the exterior half mass do not
change this first-row computation. The full operator nevertheless retains
both. The finite mechanical semigroup is positive and substochastic.
Its first row satisfies

\[
 P_{11}(u)\ge e^{-\lambda_Nu},\qquad
 P_{12}(u)\le1-e^{-\lambda_Nu}.
\]

The first inequality follows by the no-exit event; the second follows
because reaching cell 2 requires an exit. This uses no uniform estimate
on the distant exterior jump rates.

Opening only the first heat face with conductance `epsilon*b_N*a_1`
gives the positive form
`epsilon*b_N*a_1*(q_1-q_2)^2`, bounded by epsilon times the mechanical
form. Capacities at the first two cells are equal, so the exact nonconstant
heat mode is `q_*(e_1-e_2)/2` decaying at rate
`2epsilon*lambda_N*b_N`. This independently recovers (R19), positivity,
the fixed amplitude bound and outward flux.

The derivative of that solution is

\[
 q_t=-\epsilon\lambda_Nq_*b_N(t)
        e^{-2\epsilon\lambda_N\int b_N}(e_1-e_2).
\]

Substitution in variation of constants yields (R20) with the displayed
negative sign. On the final interval of length
`h_N=1/(4lambda_N)`, the difference `P_11-P_12` is at least `1/2`,
the heat exponential is larger than `1/2`, and a smooth clock bounded by
one can have integral at least `h_N/2`. Thus

\[
 |y_1(t_*)|\ge c\epsilon\lambda_Nq_*\frac{h_N}{8}
                 =c\epsilon q_*/32.
\]

For every fixed positive `t_*`, the final interval fits inside `(0,t_*)`
for sufficiently large N. With fixed `q_*>0`, the initial weighted L2
norm is `q_*sqrt(dm/rho_*) ->0`. Therefore (R15), with a constant
independent of N and the heat clocks, fails. No assertion about the
specified cold IVP is involved.

The scaling discussion in Section 5 is also correctly limited: inserting
`epsilon=O(s^2)` and `q_*=O(s^3)` into this release mechanism gives an
`O(s^5)` scale, compatible with a favorable startup power. The example
does not refute a hybrid estimate that retains the small pointwise memory
amplitude or uses the actual constitutive heat history.

## Obligation matrix and remaining implication

| Obligation | Audit result |
| --- | --- |
| Exact moving-W prefix balance | Passed |
| Both heaters and active state-box bounds | Passed |
| Prefix outgoing flux retained | Passed |
| First-cell no-inflow variation bound | Passed |
| Origin local heat sign and `O(s^5)` | Passed |
| Exact first radial rate and origin boundary | Passed |
| Smooth clocks and form domination | Passed |
| Duhamel sign and uniform lower bound | Passed |
| Separation of coefficient-class example from cold IVP | Passed |
| Actual propagated-heat estimate | Not addressed by a complete proof |
| Common prefix/collar interval | Not addressed by a complete proof |

No correction to the audited proof is required. The strongest safe actual
conclusion is (R9)--(R12), conditional on (R6). The next actual implication
needs to estimate the mechanically propagated contribution of heat sources
from other cells, using more than frozen triangular smoothing and initial
L2 data. Nothing in this audit supplies that estimate or propagates the
prefix hypotheses.

## Checks and provenance

The four law-source hashes, and the hashes for the referenced continuation,
entropy and primitive notes, were recomputed with `shasum -a 256`; all
match the table in the audited artifact. The target artifact's hash was
recomputed and matches the pinned value above. The proof was checked by
exact algebra and inequalities; no finite trajectory computation was used.
The audit file was self-proofread for notation, displayed signs and scope.

This is a fresh-agent independent audit of the radial note, not an
independent proof of the original uniform compression assertion. No proof
source, original note, physical law or numerical record was edited.
