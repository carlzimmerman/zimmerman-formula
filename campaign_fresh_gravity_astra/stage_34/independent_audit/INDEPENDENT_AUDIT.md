# FGF047 independent proof audit

Normalized claim: for every fixed finite N with L/N^3<R/2, positive fixed
diagnostic coefficients and a smooth inherited hydrostatic background on a
regular g>0 patch, the exact compact C1,1 velocity and specified compatible
field/density data admit a positive-time local solution of the actual Q/scale/
isothermal-fluid equations. Matter and first field derivatives are C1 in
spacetime with uniformly spatial Lipschitz first derivatives; potentials are
C2. The positive g, density and scale box, exact initial traces, compatibility,
local uniqueness and extension independence on common backward domains, full
energy balance and hydrostatic control hold.

Primary verdict: **proved as written** for precisely this local claim.

Author DERIVATION.md SHA256:
`1f11fd635d50a36b6cc747187595b26ebd1f4d2c4e19b9ee58c024cc5b47cf7a`.
Author result.json SHA256:
`bbc88bd9ea34282728fd620b7973a1a329b80ffceccd8d611242a1a5adbb43ad`.
The result does not prove a uniform N^-4 lower time, persistence of fixed-force
breakdown, crossing/wall well-posedness, a global solution, endpoint
classification, observational adequacy or physical theory closure.

## 1. Independence and authoritative target

The target is the author's complete frozen DERIVATION.md, particularly its
claim in Section 1 and constants (14)-(18),(28), together with result.json's
exact_claim. The report and self-verdict were not substituted for that proof.

I wrote and froze FROZEN_DERIVATION.md at 2026-10-06T03:42:49.276631+00:00,
SHA256 `28643f530341805d86a316025e5388f3b40b5c05db01b937dd3e47324b608cd6`,
after reading task, common contract and pinned OLD ancestry only. Before
new-author exposure I found one incorrect off-constraint intermediate in my
own derivation and recorded PRE_EXPOSURE_CORRECTION.md at
2026-10-06T03:43:17.766133+00:00, SHA256
`8c2f6846fb42b84b8a6030a8da1fd41d5acb64bbfdce33c6c2d622fec67fc083`.
The original remains unchanged. The correct identity is g_t=p_x independently
of chi_x=k; only the p_t equation acquires the defect b h_chi(chi_x-k).
My mistaken intermediate agreed after compatibility was proved, so it did not
alter the constructed compatible solution, but it must not be cited off shell.
The author contains the correct off-constraint identity and needs no correction.

AUTHOR_EXPOSURE.json records the final author's bytes before their first text
read, at 2026-10-06T03:46:00.962288+00:00. The coordinator supplied paths and
hashes only, with no verdict cues. No new root or compatibility proof was read.
A generic completed-agent status was visible through list_agents after my
freeze; it supplied no proof text. The old task ancestry text was initially
read before pin checking; all nine pins matched before my derivation. This
provenance limitation is retained. Same-route convergence and agent agreement
are not the evidence; the reconstructed algebra and estimates below are.

## 2. Dependency graph and leaves

1. Hypotheses: fixed positive coefficients, smooth inherited background on a
   compact regular patch, exact C1,1 velocity, compatible initial field traces.
   The inherited background is a task premise, not a new existence claim here.
2. Exact Q constitutive differentiation on g>0 -> b=sqrt(B_g/tau)>0 and
   smooth h(g,chi)=integral b dg -> invertible seven-coordinate map.
3. Chain rule -> all characteristic sources in author (10) -> a smooth diagonal
   transport system on the coordinate image. This is an internal algebra leaf.
4. Compatible auxiliary data and compact state neighborhood -> smooth bounded
   coefficient extensions -> finite actual coefficient and initial-data norms.
5. Direct characteristic ODE contraction -> linear transport formula (20) ->
   uniform first-gradient and Lipschitz-gradient envelopes (21)-(24).
6. Difference transport (25) -> C0 contraction -> interpolation (27) and the
   time-integrated PDE limit -> actual spacetime C1 solution.
7. Scale compatibility, scalar difference/sum identities and time integration
   -> C2 potentials and every original equation (5), with the dynamic source.
8. Strict characteristic cone and difference inequality (29) -> physical
   localization, local C1 uniqueness and extension-independent local germ.
9. Original equations and chain/product rules -> matter/Q/scale exchanges ->
   complete energy law and moving-boundary terms; background equations -> exact
   stationary zero-velocity control, identified by local uniqueness.

There is no external PDE existence theorem, empirical or numerical leaf, and
no circular use of the desired nonlinear solution. Compatibility is recovered
from the limit and is never assumed for nonlinear iterates. The old fixed-force
breakdown result is not a dependency of the current local theorem.

## 3. Obligation matrix

| Obligation | Status | Evidence |
|---|---|---|
| Exact quantified finite-N problem and C1,1 profile | passed | (3)-(5), unchanged polynomial, derivative norms |
| Exact Q, B_g, B_chi, dynamic source | passed | (1),(2),(6),(7),(12) |
| Smooth invertible characteristic chart | passed | h_g=b>0, explicit inverse in Section 2 |
| Every induced h_chi source and sign | passed | independent chain-rule expansion, (10) |
| Coincident principal speeds retain basis | passed | Jacobian depends only on nonzero c,d,b |
| Off-constraint feedback and both gradient constraints | passed | (11)-(13), correct scalar difference |
| Auxiliary data preserve physical initial values | passed | Section 4 cutoff and phi antiderivative |
| State cutoff legitimate and all norms dimensional | passed | (14)-(18), explicit normalization |
| Linear characteristic construction | passed | integral ODE, Jacobian, source formula (20) |
| Uniform first-gradient estimate | passed | (21), quantitative 5M/6 margin |
| Uniform Lipschitz-gradient estimate for non-C2 joins | passed | pair-characteristic quotient (22),(23) |
| Same-point box persistence | passed | (24), positive delta and bounded time drift |
| C0 contraction and full C1 limit | passed | (25)-(27), integrated time derivative limit |
| Exact original PDE and initial trace | passed | converse Section 3 applied to Section 6 |
| Explicit positive physical time | passed | (18),(28), actual finite norms for fixed N |
| Backward containment in physical patch | passed | strict speed S and shrinking K_t |
| Local uniqueness and auxiliary independence | passed | factorial estimate (29), common cones |
| Evolving energy, interaction and both field fluxes | passed | (30)-(34) |
| Zero-velocity control solves all equations | passed | background balances (3), local uniqueness |
| Construction ensures third field time derivative | not addressed | initial p_tt diagnostic is conditional and unused |
| N^-4 lower time or fixed-force breakdown transfer | out of scope | explicitly excluded |
| Crossing/walls/global evolution and physical closure | out of scope | explicit regular-patch diagnostic scope |

## 4. Decisive reconstructions and adversarial checks

### Characteristic algebra and compatibility

Write the author's field velocity as w, gradient as k, scalar wave speed as b,
and coordinate integral as h. Direct differentiation gives

 (p+h)_t-b(p+h)_x
 =p_t-b^2g_x+b(g_t-p_x)+h_chi(chi_t-b chi_x).

Substitution of the original compatible system produces exactly
A+h_chi(w-bk). The other sign gives A-h_chi(w+bk). Thus B_chi k/tau,
h_chi w and both -b h_chi k contributions all remain. A formal diagonal
principal symbol with these sources omitted would not establish the claim.

For the converse, subtracting the scalar rows yields
b(g_t-p_x)+h_chi chi_t=h_chi w. Since chi_t=w, this gives g_t=p_x
without already assuming chi_x=k. Adding gives
p_t=b^2g_x+A+b h_chi(chi_x-k). The scale rows separately imply k_t=w_x,
and the time-integrated chi row gives chi_x=k using the exact initial trace.
The defect therefore vanishes. The potential reconstruction proves phi_x=g,
with its initial additive constant fixed. No mixed derivative beyond continuous
first derivatives of the state is invoked. The source is then exactly
B_x=Cn+tau phi_tt; no static inversion has entered.

The coordinate map is triangular after pairing the two variables in each
wave block: its relevant nonzero derivative factors are c,b,d. Equality of
speeds across blocks, including zero coincidence with a fluid speed, changes
none of them. The zero-speed chi equation and the independent k coordinate
are compatible through evolution, rather than requiring a constant global
eigenbasis. The lower integration point g_*>0 may be any fixed value: the
integration interval stays in g>0, and inversion is monotone for each chi.

### Iteration constants and exact regularity

In the author's normalized variables, a=lambda_i(u^j), f=F_i(u^j) satisfy
|a_x|<=LM, |f_x|<=PM,
Lip(a_x)<=LH+KM^2, Lip(f_x)<=PH+QM^2.
For p=(u_i^{j+1})_x, its characteristic ODE is Dp=-a_x p+f_x.
This gives (21). Its numerical slack is valid because
M0<=M/2, TP<=1/8, TLM<=1/8, exp(1/8)<4/3,
so the bound is at most 5M/6.

For two trajectories X,Y in one row let e=|p(X)-p(Y)|/|X-Y|.
Their separation never vanishes for distinct labels and has logarithmic
rate bounded by LM. The upper derivative inequality for the quotient is

e' <= 2LM e+(LH+KM^2)M+PH+QM^2.

It follows using the initial derivative seminorm H0 that the first line of
(23) holds. Because T<=1 and
H=4(H0+KM^3+QM^2+1), the combination
H0+T(KM^3+QM^2) is at most H/4. The remaining term is at most H/8,
and exp(2LMT)<=exp(1/4)<4/3; hence H/2 is a valid bound. This tests the
potentially dangerous source-curvature terms, not merely the principal speeds.
The quotient argument uses only Lipschitz gradients and absolutely continuous
ODEs along trajectories; no continuous second derivative at a polynomial
support endpoint is required. Zero coefficient derivatives L=0 or P=0 cause
no singularity because all time denominators include a positive floor.

The bounded-speed terminal flow formula also gives its time derivative without
assuming the linear PDE in advance: compare the formula at t and t+h along
the short terminal characteristic. The source integral divided by h tends
to f(t,x), and the transported starting value differs by
-a(t,x)u_x(t,x)h+o(h), yielding u_t=f-a u_x. This validates the C1 induction.

The nonlinear difference equation has no differentiated source iterate;
its sup norm coefficient is LM+P. Thus the contraction factor T(LM+P)<=1/8
is correct. The bound Lip((u^j-u^l)_x)<=2H gives (27), which tends to zero
uniformly in time and space as the states converge. Integration in x identifies
the derivative. Uniform convergence of the linear PDE right sides identifies
u_t by integration in t. This closes both derivatives of the classical limit;
C0 convergence alone has not been treated as sufficient.

The same-point estimate ||u(t)-u0||<=T(Lambda M+F0)<delta/2 stays strictly
inside the closed 2delta neighborhood where the cutoff equals one. Hence the
actual evolving state has g>=g_-/2, positive density and positive a as claimed.
It is not enough to appeal to initial hydrostatics, and the author does not do
so. Different coordinate rows originating at different spatial points do not
break box persistence because the argument uses this same-point time drift.
All norms are taken after explicit physical-unit normalization; positive
physical time is Theta T0 further restricted by geometry.

### Domain, uniqueness and energy

At a point of K_t, a backward trajectory of speed magnitude <S cannot cross
either inward-moving boundary when followed backward. The zero-speed integrals
for chi and phi also stay in earlier slices. This makes the physical solution
a local solution with data on K0, despite arbitrary exterior auxiliary data.
For two admissible solutions, the difference transported along the first one's
row has source bounded by a compact coefficient Lipschitz constant times the
state difference, with the other solution's finite C1 gradient as multiplier.
The factorial iteration of (29) is valid without a contraction-small comparison
time. The common cone condition is essential and is explicitly imposed.

I recomputed the three energy exchanges: matter plus n phi contributes n p;
the Q sector contributes -n p-Tw/C; the scale sector contributes Tw/C. Their
fluxes are the fluid enthalpy/interaction flux, -pB/C and -Jwk/C. Signs and
C factors cancel as in (30)-(33). Both p and w are evolved fields, so this is
not the old frozen-force identity. Reynolds endpoint terms are retained in
(34); the shrinking cone need not conserve its integrated energy. A stationary
hydrostatic solution has p=w=v=0 and satisfies every equation by (3), giving
the required negative control on the physical domain.

The author's initial tau p_tt=C(rho v_in)_x statement is explicitly qualified
by existence of its derivatives and excluded from the proof. The constructed
C2 potentials alone do not supply a general third-time-derivative theorem;
no such theorem was needed or promoted in this audit.

## 5. Sources, computation and integrity checks

All nine task ancestry pins match. All twelve author input hashes, four output
hashes and the standalone input map match. Every required RESULT_CONTRACT field
is present. The author freeze agrees with the final derivation and report,
and the coordinator's two supplied hashes agree. My immutable independent
freeze and separately preserved pre-exposure correction agree with their
receipts. These are administrative integrity checks, not mathematical tests.

No external source leaf required a literature check. No mathematical executable
computation, numerical sample, random seed, installation, service, network
request or commit was used. Mathematical command lists are empty. Only source
reads, scoped artifact writes and standard-library SHA256/JSON validation were
performed. No candidate author/root file was changed. The only failed
mathematical intermediate found was in my own frozen off-constraint derivation,
recorded before author exposure and unrelated to any author defect.

## 6. Remaining gap and strongest safe statement

No remaining implication is missing from the exact local theorem stated in
Section 1. The construction supplies a positive actual coupled branch for each
fixed admissible finite N with explicit conservative norm/box/geometric time
gates, and all stated compatibility, regularity, uniqueness and energy results.

Whether the former fixed-force compression survives evolving Q/scale feedback
is a distinct unproved question. No upper lifespan, N^-4 lower time, shock or
endpoint classification follows from this audit. The cheapest next check for
promoting this package is a final byte-integrity comparison at reconciliation;
a feedback estimate would be new mathematical work, not an omitted repair.
Both acceleration normalizations remain separate fixed backgrounds, and a
frozen-H family remains distinct from evolving H. Dynamic diagnostic chi does
not establish pointwise physical vacuum scaling, two gravitational degrees
of freedom, metric/photon completion, RAR/M/filtered-MONO transfer, criterion B,
real cluster calibration, cosmology, historical novelty or theory closure.

Mathematical proofreading (mathbox:proofread-math, self-review) covered this
new audit and its JSON companion. Routine edits: none. Mathematical-token
changes to the author or immutable freeze: none. The reviewer correction is
separate and explicitly recorded. No unresolved proofreading issue remains;
there is no typesetting build for these Markdown artifacts.
