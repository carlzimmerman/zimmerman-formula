# FGF044 independent root audit — recovery pass

## Normalized claim and verdict

**Primary verdict: proved as written.** The verdict concerns the stated single
prescribed-velocity residual family, conditional on its explicitly fixed static
Q background. It is not a verdict about exact coupled evolution or physical
closure. No mathematical error requiring correction was found.

For each sufficiently large dimensionless integer N, fix ell=L/N^3,
v_N=v0 N f((x-x*)/ell), f(y)=(1-y^2)^2 on (-1,1) and zero elsewhere.
The point x* is on the positive-gradient regular side of the fixed background;
rho_x<0 throughout the supports. On each fixed finite slab [0,T], transport
rho exactly by this stationary velocity and keep both fields static. The claim
is positivity and exact mass conservation; uniformly vanishing density L1,
kinetic energy, relative entropy and full-energy-density differences; the
specified vanishing field/momentum/energy residuals; vanishing full spacetime
energy flux despite the nonzero initial spatial cubic-flux measure; failure of
the exact global energy inequality at small positive times for each N; and a
uniform O(N^-3 log N) approximate global energy budget.

The coefficient domain is real, all physical coefficients named positive remain
fixed, rho is positive and smooth on the perturbation neighborhood, and all
limits concern this one family. The inherited central crossing is untouched.
Spatial integrals use the inherited planar convention (per unit transverse
area when rho is a physical volume density). Tests and constants are measured
in fixed reference units. No N-independent pointwise density bound is needed.

## Recovery role, independence and source pins

Auditor: `/root/fgf044_root_review_recovery`, freshly dispatched after the
original root-only auditor reportedly stopped at a usage limit without a
durable audit. That reported operational fact was not used as evidence for
any mathematical conclusion. The dispatch named obligations but supplied no
assumed verdict. This auditor reconstructed the flow, energy and residual
identities from the frozen root proof and older definitions.

No new stage31 author/reviewer proof, preview, conclusion or audit was read.
Only the two authorized audit outputs were written; the root proof was not
edited. Independence here means isolation from those new proofs, not a claim
that model agreement itself establishes correctness.

Substantively read inputs (SHA256):

| Input | SHA256 |
| --- | --- |
| stage31 `exact_continuity/ROOT_DERIVATION.md` | `4e426c18438987afdfdf87ea06bfee428a195584b22b514fa1a9bf2c047ad337` |
| stage31 `exact_continuity/PROOF_RECORD.json` | `0ffce17e6bb5f35eb432544f0f4a6baa8e14ba5b8d4471d57d9db893cf0b91ab` |
| followups `tasks/FGF-044.md` | `4f17b753567fb4f98dafa241195dac0bf24fd0107ab1b06b4c1486db4fcde023` |
| stage30 `local_energy/ROOT_DERIVATION.md` | `45236fe01ee93bdcedbe785bcb2948d408b4ea05869aa81235095e2cfec2ca27` |
| stage30 `local_energy/CORRECTION.md` | `cfa5cc3117ba7b42b3fafee936fec35f1353042c5d429986277a24e51fdafa74` |
| followups `results/FGF-043/fgf043_run_001/DERIVATION.md` | `dd56899478c637f5d8e1c51fddde2b4754d24795234037e3cee9526336f6e414` |
| followups `results/FGF-023/fgf023_run_001/DERIVATION.md` | `0b9babab32edd602cf5aea8db63126a52f09c379b858e5c5967d46835bbf1f4a` |

Here stage31/stage30 are under `campaign_fresh_gravity_astra/`, and followups
is `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/`. All ten ancestry
hashes in the proof record were checked and matched; hash-only access to an
ancestry artifact is not represented as a substantive audit of that artifact.
The proof-audit skill and its obligation checklist were read. No applicable
AGENTS.md or `.mathbox` directory was found in the inspected ancestry/paths.

## Dependency graph

1. Fixed background equations and full H,Q,P,Pi definitions: inherited
   hypotheses/conventions, read in pinned FGF043 and FGF023 sources.
2. The explicit C1,1 profile and F-coordinate: internal construction of a
   global finite-time increasing flow and its Jacobian.
3. Pushforward mass identity: exact continuity, positivity, invariant support,
   participating mass, and the elementary current/kinetic bounds.
4. Derivative of z=(1-y^2)^-1: polynomial Jacobian bounds, logarithmic density
   bound, relative entropy and full-energy-density convergence.
5. Hydrostatic first variation plus continuity: initial positive energy
   derivative; even decreasing F-coordinate profile plus layer sets: the
   sharper approximate global budget.
6. Monotone finite trajectory length plus pushforward: integrated current and
   cubic-flux estimates; the logarithmic bound: complete flux convergence.
7. Direct source substitution and weak integration by parts: all remaining
   residual and trace claims.

No conclusion is fed back as a premise. The global flow is explicitly given,
so no unchecked literature theorem supplies its existence. The elementary
change-of-variable, integration-by-parts and bounded-convergence steps are
justified below on their actual domains. No external-source leaf or numerical
computation is needed for the family being audited.

## Obligation matrix

| Obligation | Status | Decisive reason |
| --- | --- | --- |
| Profile and finite-time flow regularity | passed | C1,1 vector field; divergent F at endpoints; finite-time positive Jacobian joining 1 |
| Exact continuity, positivity, mass, support | passed | n(t,X) X_x=rho; invariant support; no endpoint flux/jump |
| Polynomial Jacobian estimates | passed | z'=2Y and z>=1 in both time directions |
| Entropy and full energy | passed | equal participating masses; bounded log ratio; exact hydrostatic first variation |
| Claimed failure of exact energy inequality | passed | E'(0)=-(1/3) integral rho_x v_N^3>0 |
| Sharper approximate energy budget | passed | centered layer-set overlap maximized at zero translation |
| Full spacetime flux and finite supply | passed | actual trajectory travel at most 2ell; enthalpy/potential explicitly included |
| Initial and fixed-positive-time limits | passed | initial cubic measure; labelwise decay at fixed t>0; total time weight vanishes |
| Field and scale residuals/source signs | passed | Rphi=C(n-rho), Rchi=0, actual signed MOND source |
| Primitive/conservative/combined momentum | passed | exact Rc=0 and field-source force correction retained |
| Local energy residual topology | passed | direct L1 estimates for H-H0 and Q in spacetime |
| Initial/wall traces | passed | actual initial density/energy/momentum; identity flow near walls |
| Zero-velocity control and units | passed | identity flow and static solution; s dimensionless and all physical factors retained |
| Exact coupled solutions/physical closure | out of scope | explicitly unclaimed and not established |

## Independent derivation of the critical steps

### Flow and entropy

Inside the support f>0 and F'=1/f. Near either endpoint 1/f has a
nonintegrable quadratic singularity, hence F maps (-1,1) onto the real line.
Its inverse produces Y_s for every finite real s. The endpoints and exterior
are fixed. Differentiating gives J_s=f(Y_s)/f(a), equivalently
J_s=exp(integral_0^s f'(Y_r) dr). The exponential is positive and tends to 1
as a approaches either endpoint at fixed finite s, since f' vanishes there.
The Lipschitz bound for f' and finite-time Lipschitz bounds for Y make J
locally Lipschitz in its label. Thus the joined flow is C1 with Lipschitz
spatial derivative, and its positive Jacobian has a positive lower bound on
each fixed finite-N finite-time compact slab. The transported density is
continuous and W1,infinity on the perturbation neighborhood, with permitted
N-dependent constants. Second-derivative endpoint jumps do not create a
continuity delta source: n and nv join continuously, with v=0 at endpoints.

The physical time rescaling is s=(v0 N/ell)t, which is dimensionless; indeed
dX/dt=v0 N f(Y_s). The change of variables n dx=rho dx0 proves exact mass
transport, and the support carries only m_N=O(ell). Consequently
||n-rho||_1<=2m_N, ||j||_1<=v0 N m_N and K<=v0^2 N^2 m_N/2,
uniformly in t. Outside density remains rho.

Set z=1/(1-y^2). The exact derivative is dz(Y_s)/ds=2Y_s, of magnitude at
most 2. Thus z(Y_s)<=z(a)+2s<=(1+2s)z(a); applying the reverse comparison
gives z(a)<=(1+2s)z(Y_s). Since J=[z(a)/z(Y_s)]^2, root equation (2)
follows for s>=0. This argument does not use an exponential-in-N bound.

The density ratio is rho(x0)/(J rho(X)), and |X-x0|<=2ell. Therefore its
logarithm has absolute value at most Lambda=2 log(1+2s)+2ell Lrho.
Equal mass on the invariant interval gives D=integral n log(n/rho), while
the pointwise convex integrand h is nonnegative. It follows that
0<=D<=m_N Lambda and sup D=O(N^-3 log N). All logarithms have dimensionless
arguments. Positivity and finiteness are established separately at each N.

### Energy and its two distinct inequalities

For e(n)=cs^2 n(log(n/rho_ref)-1), the exact Bregman identity is
e(n)-e(rho)=cs^2 h(n,rho)+e'(rho)(n-rho).
Keeping n phi0 and using e'(rho)+phi0=mu gives
H-H0=nv^2/2+cs^2 h+mu(n-rho). Its integral is K+cs^2 D since the mass
difference integrates to zero. The pointwise signed linear term is retained
when taking an L1 norm. This verifies root (5) and its finite internal-energy
claim, without omitting interaction energy.

At t=0, differentiating K through exact continuity gives
K'=integral rho v^2 v_x=-(1/3) integral rho_x v^3. The support is on the
strictly decreasing-density side; f is positive inside and v0>0. This is
strictly positive. D'(0)=0 follows by differentiating its convex integrand at
n=rho. Hence E(t)>E(0) on some sufficiently small positive time interval for
each N. This interval need not be uniform in N; no uniform assertion is made.

For the upper budget, F is odd, so g(u)=f(F^-1(u)) is even and decreases
with |u|. At constant label density rho*, the kinetic integral is proportional
to integral g(u+s)^2 g(u) du. Nonnegative layer-set representations apply by
Tonelli; each positive-level set is a finite centered interval. Its overlap
with the translated interval is at most its overlap at zero displacement.
Also integral g du=2, so these integrals are finite. Thus the constant-density
kinetic integral never exceeds its initial one. Replacing rho* by rho(x0)
introduces at most a constant times v0^2 N^2 ell^2 at each comparison time,
because |rho(x0)-rho*|<=ell sup|rho_x| and integral f(Y_s(a))^2 da<=2.
This proves K(t)<=K(0)+O(N^-4), and adding cs^2 D proves (6) uniformly on
the fixed slab. The positive initial derivative and this vanishing-error
bound are compatible.

### Finite supply, fast time, and the complete flux

For each actual label, dt=dX/v wherever v>0, hence
integral_0^T v(X(t))^3 dt=integral_x0^X(T) v(x)^2 dx.
Stationary endpoint labels cause no difficulty. Nonnegative velocity and
invariant support give travel at most 2ell. Integrating labels against rho
proves integral integral nv^3/2 <=v0^2 N^2 ell m_N=O(N^-4).
Similarly integral integral nv<=2ell m_N=O(N^-6). These are integrated
travel bounds, not the weaker T times instantaneous bounds.

The inherited full energy flux reduces exactly to
Q=nv^3/2+cs^2 nv log(n/rho)+mu nv.
Both field fluxes vanish. Multiplying the integrated current estimate by the
uniform logarithmic bound proves ||Q||_L1(tx)<=O(N^-4)+O(N^-6 log N).
The estimate concerns the absolute flux as well as its signed integral.

At t=0 the cubic spatial measure tends to
[rho(x*) v0^3 L integral f^3/2] delta_x*, a positive finite measure.
At every fixed t>0, s_N tends to infinity; F(Y_s)=F(a)+s implies Y_s tends
to 1 for every interior label. The label integral for the cubic flux is
v0^3 L integral rho(x*+ell a) f(Y_s(a))^3 da. A fixed bounded integrable
majorant on (-1,1) gives convergence to zero. For completeness the other
full-flux terms at fixed time are bounded by
(cs^2 Lambda+|mu|)||j||_1=O(N^-2 log N), so also vanish there.
The time-boundary layer has vanishing total variation by the spacetime
estimate and cannot leave a temporal delta. The root's phrase “initial
nonzero current” in this paragraph denotes energy/cubic current; the mass
current j itself tends to zero even at t=0, as explicitly proved earlier.

### Residuals, signs and traces

Direct substitution into tau phi_tt-B_x+C n gives C(n-rho), with positive
sign; the scale equation and field kinematics remain exact. Thus Rphi is
O(N^-3) in L-infinity_t L1_x. No field equation is falsely declared exact.

Writing r=n-rho and using cs^2 rho_x+rho g0=0 gives
Rj=j_t+(nv^2+cs^2 r)_x+r g0.
For a compact spacetime C1 test zeta, its pairing is bounded by
T[sup||j||_1 ||zeta_t||_infinity
 +sup||nv^2+cs^2 r||_1 ||zeta_x||_infinity
 +sup||r g0||_1 ||zeta||_infinity].
The three rates are respectively O(N^-2), O(N^-1)+O(N^-3), O(N^-3).
No spatial norm for j_t at individual times follows from this argument or
is claimed. The inherited primitive convention is density-weighted:
Rv=n(v_t+vv_x)+cs^2 n_x+n g0, and Rj-Rv=v Rc=0. It is not the residual
obtained after dividing by n with an N-uniform reciprocal-density bound.

The inherited combined momentum has P=j and
Pi=Pi0+nv^2+cs^2 r. Consequently Rcomb=Rj-r g0. Equivalently the field
off-shell contribution is -g0 Rphi/C, confirming the sign of the essential
source correction. Its residual has the same spacetime dual convergence;
P and Pi-Pi0 converge L1 uniformly in time.

Direct integration by parts gives
|<RE,zeta>|<=T sup||H-H0||_1 ||zeta_t||_infinity
 +||Q||_L1(tx) ||zeta_x||_infinity ->0.
This argument never multiplies a weak residual by the unbounded velocity.
For tests reaching t=0, the density difference there is exactly zero,
the momentum difference is O(N^-2), and the energy difference O(N^-1).
The temporal weak energy law has an H trace, not a Q trace; the nonzero
initial cubic flux is therefore not a missing initial boundary term. Uniform
estimates also control terminal density/energy/momentum traces if needed.
All perturbations vanish near walls, giving zero perturbation mass/energy
flux and momentum traction. Zero prescribed velocity returns the identity
flow, n=rho, all residuals zero, and zero relative energy and flux.

## Errors, remaining gap, and strongest safe statement

Error log before any correction: **empty**. No correction was made or is
required for this root claim. The clarifications about weighted primitive
momentum and the referent of “current” above use the explicitly pinned
conventions; they neither change a hypothesis nor strengthen a conclusion.

There is no remaining implication missing from the stated finite-family
claim. Exact coupled evolution, propagation of admissibility, general
existence/uniqueness or stability, and physical closure remain unproved and
out of scope. In particular this family fails the strict global inequality;
it cannot be reported as a family satisfying that stronger admissibility
condition. Both positive a_ref normalizations are separate fixed backgrounds;
constant vacuum and frozen H cases are distinct from a genuinely evolving
reference, whose work/reservoir sector has not been supplied.

The strongest safe statement is exactly the bounded transport result: exact
continuity with finite initial participating mass removes this family's
persistent spacetime energy-flux defect, while retaining only a quantified
vanishing-error global energy budget. No further mathematical check is needed
for the audited root claim. Any next research task must specify an additional
actual dynamical or admissibility constraint rather than repeat this estimate.

Verification used file reads, SHA256 checks, and subsequent JSON/output checks.
Mathematical executable computations: zero. No literature/network/service
access, scans, commits, or outside-scope proof edits were used.
