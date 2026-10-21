# One interacting quantum functional: induced gravity and a frame-current portal

2026-10-20. Base `431f22bd6`; criteria-only `89bf113b0`.
Analytic investigation only. No script, scan, source download, build,
Lean run or numerical target input. Primary versions and extraction
limits are recorded in `SOURCES_INDUCED.md`.

**Result.** An interacting gauge theory supplies a genuine common
functional for an Einstein term and vacuum contribution. It does not
yet supply a positive MOND cubic. A specific covariant conserved-current
portal to frame acceleration is exactly removable on the static rest
branch. Its non-pure-gauge timelike-current replacement changes both
the physical Newton coefficient and total vacuum stress; the simplest
retained phase/frame realization is unstable in flat space. None of
these results excludes all interacting induced-gravity theories or all
curved critical frame completions. No physical value of R is selected.

## 1. The actual common microscopic object

Start with pure SU(N) Yang--Mills, minimally coupled to an external
Lorentzian metric, and then promote the metric only after deriving its
effective action. In signature -+++ write

    S_YM[g,A]=-(1/4) integral sqrt(-g) F^a_mu nu F^{a mu nu},
    exp(i Gamma[g])=integral DA exp(i S_YM[g,A]).

Gauge fixing, ghosts, the measure, state and renormalization conditions
belong to this definition. This is an interacting quantum functional,
not a fitted list of free masses or a heat-kernel spectrum. The source
Donoghue--Menezes1712.04468v3 derives its metric response, including the
quadratic metric contact coupling. Its equations 5--17,48--60 are the
primary normalization authority used here.

For the following three formulas only, retain that source's +--- trace
and curvature conventions. Set Theta_s=T^mu_mu in those conventions,
Theta_bar=Theta_s-<Theta_s>, and

    Pi_AZ(q^2)=-i integral d4x exp(iqx)<T{Theta_bar(x)Theta_bar(0)}>,
    Q=1/(16pi G_ind)=Pi_AZ'(0)/12,
    epsilon_ind=<Theta_s>/4=Pi_AZ(0)/16.

The last equality is the Yang--Mills low-energy sum rule with its
specified contact prescription, rather than a generic identity for
every matter theory. In the lane's -+++ convention the physical vacuum
stress is `T_mu nu=-epsilon_ind g_mu nu`; its trace is
`-4epsilon_ind`. No opposite-sign trace convention is silently inserted
into the source formulas. The physical energy epsilon_ind and positive
Einstein coefficient have the same interpretations after translation.

The factor in the vacuum sum rule matters. The expansion contains both
`h T` and a local two-graviton coupling `h h tau`. Leaving out the latter
produces the incorrect factor-two vacuum relation discussed in the
source. Coincident OPE/contact contributions can affect the zero moment
without supplying the same contribution to the x^2-weighted moment.
Consequently an unsubtracted positive spectral integral cannot simply
be substituted for these renormalized quantities. In the source's
conventions even its infrared positive glueball contribution gives a
negative shift in Q; its full positive estimate includes the short-
distance calculation and subtractions.

The source's interacting determination of Q is approximate and positive,
not an exact positivity theorem for every Yang--Mills theory. Its usual
condensate estimate for epsilon_ind is negative; the text also discusses
the possibility of a vanishing condensate. We use neither its numerical
inputs nor a scale-rescaled version as a normalization prediction.
There is no established positive same-state vacuum in that calculation.

Even granting a UV prescription that uniquely fixes all local matching
terms, the subsequent operator/source failures below remain. Conversely,
allowing unspecified finite gravitational matching terms would require
fixing those terms before claiming an absolute prediction. A common
functional is meaningful but is not by itself one selecting invariant.

## 2. Actual metric source and Newton response

Assume a stable gapped phase admits the long-wavelength expansion

    Gamma[g]=integral sqrt(-g)[-epsilon+M^2 R/2
                    +a R^2+b R_mu nu R^{mu nu}+...],  M^2=2Q>0.

Here M is the reduced Planck coefficient. Additional visible bodies
couple minimally to this same physical metric. In a local weak-field
region take

    ds^2=-(1+2Phi)dt^2+(1-2Psi)delta_ij dx^i dx^j.

To quadratic static order, after boundaries and the appropriate vacuum
background terms are separated, the Einstein term plus nonrelativistic
source is

    S_stat=integral dt d3x {
       M^2[(grad Psi)^2-2 grad Phi.grad Psi]-rho Phi}.

Independent lapse and spatial-metric variation gives

    2M^2 Delta Psi=rho,
    Delta(Phi-Psi)=0.

With the decaying boundary branch Psi=Phi, the reduced action is

    S_stat=-integral dt d3x [M^2 |grad Phi|^2+rho Phi],
    G_Newton=1/(8pi M^2),
    Phi=-m/(8pi M^2 r),    a_test=-grad Phi.

Thus this conditional Einstein regime has the force coefficient
`C2,Newton=M^2=2Q`. A conformal trace probe used to extract Q is not an
additional independently sourced scalar. Its unreduced kinetic term
must not be assigned a separate attractive force or ghost.

The expansion is a low-*momentum*/low-curvature result. It is not an
evaluation of the gravitational functional at arbitrary high momentum,
and its quadratic coefficient is not automatically the high-gradient
side of a demonstrated MOND crossover. This model currently has only
the Newton regime within that controlled expansion. A constructed
MOND branch would still have to show that its actual high-gradient
force returns to this coefficient, with all extra modes retained.

For a genuinely positive constant vacuum, promoting the truncated
action would require `H^2=epsilon/(3M^2)` and also `H<<m_gap` before a
flat-vacuum derivative expansion could be trusted on that state. At
large N a conditional single-scale form

    Gamma ~ N^2 integral sqrt(-g)[-c0 Lambda^4+c1 Lambda^2 R+...]

would give `H^2/Lambda^2=c0/(6c1)`. Increasing N cancels out of this
condition. This does not prove a failure for every interacting theory;
it states the actual small-curvature requirement. A curved stationary
state and its stress are not calculated by merely naming flat-space
induction coefficients.

## 3. Why pure metric induction has not supplied the cubic

In the gapped local metric expansion, there is no invariant made solely
from a first metric derivative which measures a local acceleration.
An explicit check is the flat Rindler patch

    ds^2=-(1+kx)^2 dt^2+dx^2+dy^2+dz^2.

Its curvature vanishes, while the acceleration of its static congruence
is `|a|=|k|/(1+kx)`. The same Minkowski vacuum cannot acquire a new local
`|a|^3` gravitational density because of that coordinate choice. Selecting
a different observer ensemble, a boundary or a preferred physical frame
adds information beyond the metric-only vacuum functional.

This is not a theorem excluding every nonanalytic metric theory.
Critical nonlocal functionals and nonanalytic curvature operators need
their own metric constraints and mass/source scaling. They cannot be
identified with `|grad Phi|^3` by replacing a curvature with a first
derivative. The regular gapped derivative expansion above supplies no
leading positive MOND cubic. No free determinant or thermal zero-mode
calculation is repeated here.

## 4. A concrete covariant current portal and an exact Ward test

Pure Yang--Mills has no Dirac U(1) current. For this distinct candidate,
extend the microscopic theory by vectorlike Dirac matter charged under
the confining gauge group and an anomaly-free global U(1), with a
background connection B_mu:

    S_micro[g,A,psi,B]=S_YM+
       integral sqrt(-g) sum_i psibar_i(i gamma^mu D_mu-m_i)psi_i,
    D_mu=nabla_mu-i g A_mu^a T^a-i q_i B_mu,
    exp(i Gamma[g,B])=integral DA Dpsi Dpsibar exp(i S_micro).

Choose the Hermitian Dirac convention appropriate to the declared
signature. All charges and current normalization are specified by this
action; no U(1) charge is identified with inertial mass. Visible matter
continues to couple minimally to g, providing its universal metric
source. Pure-Yang--Mills numerical values or positivity estimates for Q
are not transferred to this different matter theory.

The exact anomaly-free background vector identity is

    Gamma[g,B+d alpha]=Gamma[g,B],
    nabla_mu[(1/sqrt(-g))delta Gamma/delta B_mu]=0,

with the charged fields transformed, fixed compatible state/domain,
and no boundary or holonomy obstruction. Now let u_mu be a dynamical
unit timelike covector, `u^2=-1`, and `a_mu=u^nu nabla_nu u_mu`.
Test the actual Lorentzian portal `B_mu=lambda a_mu`, lambda constant.
For every static zero-shift rest-frame configuration

    ds^2=-N(x)^2dt^2+gamma_ij(x)dx^i dx^j,
    u_mu=(-N,0),
    a_0=0,    a_i=partial_i ln N,
    B=d(lambda ln N).

Hence on a neutral static branch where that gauge transformation is
admissible,

    Gamma[g,lambda a]=Gamma[g,0].

This cancellation is exact in the hidden interactions and does not
require a gap. It kills the proposed current-induced static cubic,
not the metric's Einstein response. Nontrivial holonomies, boundary
charges, time-dependent configurations or a nonconserved/anomalous
current change the test. No general current/frame no-go is inferred.

## 5. The non-pure-gauge replacement B_mu=mu u_mu

Take mu>0 with mass dimension one, not determined from the target. Then
on the same static rest frame

    B_0=-mu N,   B_i=0,
    F(B)_0i=mu partial_i N,
    e=|F_hat0 hati|=mu |a|.

This connection is physical and avoids the previous Ward cancellation.
It is an actual way for the same quantum sector to respond to static
acceleration. A homogeneous chemical potential still requires a charge
ensemble/temporal boundary condition: a constant B is locally pure
gauge. A vacuum functional without that datum does not acquire a
chemical potential from notation alone.

### Neutral gapped branch

For `H_mu=H-mu Q`, assume a neutral vacuum and a positive threshold
`mu_c=inf_(Q!=0)(E_Q-E_0)/|Q|`. With a common admissible domain,
`|mu|<mu_c` leaves the homogeneous zero-temperature ground state and
density unchanged. This elementary spectral statement is the contract
used here, not an assumed threshold for all confining theories.

A slowly varying weak static source additionally requires a retained
gap, momenta small compared with it and field strengths small compared
with the charged threshold scales. Its real local power expansion may
contain

    Gamma[g,B] contains -Z_B F(B)^2/4+O(F^4,grad F terms),

with a specified matched Z_B. It has no leading algebraic electric cubic
in that regular expansion. A real uniform electric vacuum at infinite
extent is a separate assumption: pair production can give an imaginary
part, so an in-out response is not automatically a stable static state.
The homogeneous threshold argument does not certify arbitrary varying
electric backgrounds or the full vector/frame Hamiltonian.

### The force coefficient changes

On the conditional weak-field static rest branch, the Maxwell term
contributes `+Z_B mu^2 |grad Phi|^2/2` to the action. Eliminating Psi as
in section 2 gives

    C2,rest=M^2-Z_B mu^2/2,
    G_rest=1/[8pi(M^2-Z_B mu^2/2)]

if the denominator is positive and this is the selected sourced branch.
The Einstein coefficient alone is not then measured Newton G.
The minimal Maxwell-frame theory has additional constraint/initial-data
modes, so this linear rest-branch coefficient is not a certificate of a
unique nonlinear Newton regime. Its full frame equation and boundary
data must be solved.

More generally, if a critical current response were actually to give a
real static electric Lagrangian

    L_current(e)=Z_IR e^2/2+ell3 |e|^3+...,

then the reduced metric energy would start as

    E_rest(h)=(M^2-Z_IR mu^2/2)h^2-ell3 mu^3 h^3+... .

A leading positive MOND cubic would require both an independently
derived cancellation of the quadratic and `ell3<0`. A positive electric
cubic has the wrong sign for this particular metric map. Negative ell3
is not by itself a photon ghost: a positive quadratic electric Hessian
can survive sufficiently near zero. The actual critical quantum
functional and retained mode analysis are missing, rather than replaced
by a universal sign assertion. No high-gradient interpolation is derived.

### Total homogeneous stress, including the source/frame

A finite-density pressure must be represented with its state variables.
For a simple gauge-complete superfluid realization retain a phase theta,

    X=-g^{mu nu}(partial_mu theta-B_mu)(partial_nu theta-B_nu),
    L_medium=P(X),
    L_constraint=lambda_u(u^2+1),   B_mu=mu u_mu.

This is a conditional retained-medium EFT, not a derived phase of the
preceding vectorlike gauge theory. The phase transforms with the
background U(1); its equation is current conservation. Only on the
selected homogeneous resting state with both `partial theta=0` and
`B=mu u` may one replace X by `Y=-mu^2u^2`. This is a state restriction,
not an arbitrary gauge choice preserving both relations. Vary u and the
metric before imposing its normalization. At this state

    lambda_u=mu^2 P_Y,
    T_total,mu nu=2(mu^2 P_Y-lambda_u)u_mu u_nu+P g_mu nu
                 =P(mu^2)g_mu nu,
    epsilon_total=-P(mu^2).

The independently fixed-B matter density would instead be
`epsilon_matter=mu n-P`, `n=2mu P_Y`. That density is not the gravitating
vacuum after the constrained source reservoir is included. For a stable
grand ground state with the neutral vacuum as an admissible trial,
`P(mu^2)-P(0)>=0`: its energy density is the infimum of `H-mu Q`.
Relative to a convention with `P(0)=0`, the total homogeneous vacuum
shift above is therefore nonpositive. An already positive baseline
vacuum is separate input to this comparison, not fixed by this pressure
inequality. Fixed charge, normal-fluid variables, different temporal
boundary conditions and additional frame operators require their own
total variation. No replacement of every medium by this P(X) is made.

Vacuum-form instantaneous stress does not establish an expanding
stationary state. On homogeneous FRW with theta constant, constant mu
and the unit rest frame, the retained phase equation is

    partial_t[a(t)^3 2mu P_X(mu^2)]=0.

For de Sitter H>0 this ansatz requires P_X(mu^2)=0. The nonzero-density
pressure calculation is therefore a local homogeneous-rest/flat
diagnostic, not an exhibited finite-charge de Sitter solution. Letting
the density, phase or mu evolve changes the state and requires solving
its complete stress and field equations.

### Retained minimal phase/frame health test

In flat space add only the Maxwell frame kinetic term
`-K(du)^2/4`, K>0, to this phase/constraint model. Put
`theta=pi`, `u_i=v_i`, `u_0=-sqrt(1+v^2)`, and evaluate derivatives of
P at X=mu^2. Direct expansion gives

    X=mu^2+2mu pi_dot+pi_dot^2-(grad pi)^2
                  +2mu v.grad pi+O(3),
    A=P_X+2mu^2 P_XX,    B=P_X,
    L2=A pi_dot^2-B(grad pi)^2+2mu B v.grad pi
                  +K v_dot^2/2-K(du)_ij^2/4.

The v^2 terms cancel, rather than supplying a stabilizing frame mass.
For a nonzero longitudinal wave number k, the equations have determinant

    A K omega^4-B K k^2 omega^2-2mu^2 B^2 k^2=0.

If the phase by itself has A>0,B>0 and K>0, its two roots in omega^2
have negative product. One is negative: this particular flat minimal
retained completion is unstable. At B=0 the argument becomes degenerate,
not a proof of a healthy nonanalytic response. Curvature, gravitational
constraints, higher derivative terms or different frame dynamics can
change the spectrum and have not been classified by this test. The
separate P3 packet performs its actual de Sitter constraints.

## 6. The first still-missing implication

The common functional genuinely computes multiple gravitational
observables. Formally a single-scale large-N theory could have

    epsilon=N^2 c0 Lambda^4,
    C2=N^2 c2 Lambda^2,
    C3=N^2 c3 Lambda,
    R=c0 c3^2/c2^3.

Both the species factor and transmutation scale cancel. This is why a
quantum origin cannot be dismissed merely by calling its coefficients
loop effects. But in the concrete controlled metric induction no
positive C3 exists, and the tested current/frame maps do not supply it.
The expression above is conditional, not a numerical prediction.

A viable reopening needs a specified interacting Lorentzian critical
functional whose non-pure-gauge frame response actually has the required
sign, whose quadratic cancellation and ultraviolet force coefficient
follow dynamically, and whose full stationary state has positive total
vacuum stress and healthy retained modes. Its microscopic relation must
connect the trace response, current/frame response and source matching,
including their contact terms and ensemble. Neither the Adler--Zee
sum rule nor the vector Ward identity supplies that relation. No value
R=128pi/9, target-dependent scale or complete physical/Lean bridge has
been obtained. More elaborate interacting or nonlocal induced-gravity
models remain open.
