# FGF044: exact continuity exhausts the localized transport supply

Proof-only derivation frozen before new root/reviewer proofs or previews.
Only continuity is solved exactly. Prescribed velocity and frozen fields are
an explicit residual ansatz, not a solution of the whole coupled system.

## 1. Physical units, profile and finite flow

Use the same fixed-reference Q crossing with C=4piG and background rho,phi0,
chi0 on a fixed finite interval. Write g0=phi0', a=a_ref exp chi0,
B0'=C rho, cs²rho'=-rho g0, J chi0''=U'-T0. Choose x* strictly on the POSITIVE
regular side, so g0>0 and rho'<0 in a fixed compact neighborhood. Fix physical
v0,L>0 and a finite time slab [0,T]. For sufficiently large dimensionless N,
put l_N=L/N³, V_N=v0 N, omega_N=V_N/l_N=v0 N4/L, and

 v_N(x)=V_N f((x-x*)/l_N),
 f(y)=(1-y²)² for |y|<1, and0 outside.                       (1)

The profile is C1 and globally C1,1, piecewise smooth, NOT C-infinity: its
second derivative jumps at +/-1. This declared regularity suffices below.
The support interval J_N=(x*-l_N,x*+l_N) stays away from crossing and walls.
Keep Phi=phi0, X=chi0 and field velocities zero.

For |y|<1 define the increasing coordinate

 H(y)=y/[2(1-y²)]+(1/4)log[(1+y)/(1-y)], H'=1/f.

It maps (-1,1) onto the real line. The exact dimensionless flow is

 Y_s(y)=H^-1(H(y)+s), s=omega_N t.                           (2)

Thus Y_s'=f(Y_s) in s, and no interior particle reaches +/-1 at finite time.
Outside J_N particles remain stationary. In physical coordinates define
X_t(b)=x*+l_N Y_(omega_N t)((b-x*)/l_N) on J_N, and X_t(b)=b outside.
For every finite N,t this is a strictly increasing bijection of the interval,
fixing both endpoints of J_N and the physical walls. Its Jacobian is

 J_t(b)=partial_b X_t=f(Y_s(y))/f(y)>0                       (3)

inside, with continuous extension1 at either endpoint. This also follows
from J_t=exp(integral_0^t v_N'(X_u)du). Continuous v_N' gives the C1 flow;
its Lipschitz derivative gives finite bounds on difference quotients of J_t
on every finite time interval by this integral formula. Thus X_t is C1 with
locally Lipschitz first derivative, as is its inverse for each finite N,T.
The bounds may depend on N; no uniform smoothness is claimed.

Set n_N(t,X_t(b))=rho(b)/J_t(b), j_N=n_N v_N.                 (4)

This is positive and finite for every finite N,t, initially rho, continuous
and piecewise regular, with weak first derivatives locally integrable (indeed
bounded on the moving compact patch for fixed N,T). Outside J_N it equals
rho. Change of variables proves, for any smooth compact test h,

 integral n_N(t,x)h(x)dx=integral rho(b)h(X_t(b))db.

Differentiating gives integral n_N v_N h', proving n_t+(n v_N)_x=0 exactly,
including its initial trace. All ensuing derivative equations are interpreted
in distributions, with ordinary a.e. identities where available. The C1,1
profile introduces no sheet mass, jump delta or hidden smoothing.

## 2. Participating mass and exact displacement accounting

Only the initial mass

 m_N=integral_(J_N) rho dx=O(N^-3)

participates. No outside stationary particle can cross a fixed support edge,
by the explicit flow and uniqueness at its zero-velocity endpoints. The
transported mass in J_N remains m_N, so at every t

 ||n_N-rho||_1<=2m_N, ||j_N||_1<=V_N m_N=O(N^-2).

Because v_N>=0, all displacements are nonnegative and at most2l_N. The exact
flow identity and its useful consequence are

 integral_0^T integral j_N dx dt
 =integral_(J_N) rho(b)[X_T(b)-b]db <=2l_N m_N=O(N^-6),       (5)
 integral_0^T integral n_N v_N³/2 dx dt
 <=(V_N²/2) integral_0^T integral j_N
 <=V_N² l_N m_N=O(N^-4).                                   (6)

This is finite baryonic supply, not a pointwise velocity cutoff. Formula(5)
independently checks the mass/flux accounting. It directly precludes the
persistent nonzero cubic SPACETIME flux of the static-density ansatz.

## 3. Uniform finite entropy without an exponential-in-N estimate

A crude exp(||v_N'|| T) Jacobian bound would not settle the energy question.
Use instead the special quadratic vanishing of the actual profile. Along
Y_s, write delta_+=1-Y_s and delta_-=1+Y_s. Then

 d(1/delta_+)/ds=(1+Y_s)²<=4,
 -d(1/delta_-)/ds=(1-Y_s)²<=4.

The right distance decreases, the left distance increases; both are at most2.
Consequently, for every initial y and s>=0,

 (1+8s)^-1 <=delta_+(s)/delta_+(0)<=1,
 1<=delta_-(s)/delta_-(0)<=1+8s.

Using f=delta_+² delta_-² in (3) gives the uniform polynomial bounds

 (1+8s)^-2<=J_t<=(1+8s)².                                  (7)

Let K_rho=max |(log rho)'| on the fixed regular neighborhood. Since
|X_t(b)-b|<=2l_N, the exact transported density has

 |log[n_N(t,X_t(b))/rho(X_t(b))]|
 <=h_N(t):=2log(1+8omega_N t)+2K_rho l_N.                    (8)

Relative entropy D(n|rho)=integral[n log(n/rho)-n+rho] is nonnegative. Total
mass agrees, and n-rho vanishes outside J_N, so (8) implies

 0<=D(n_N(t)|rho)<=m_N h_N(t),
 sup_(0<=t<=T) D=O(N^-3 log N).                             (9)

For each finite N,t the density is bounded above/below, but no N-independent
pointwise density cap or physical incompressibility is assumed. The entropy
bound is obtained from the actual flow, not from assuming such a cap.

## 4. FULL energy, the failed exact global inequality, and its error

All field and scale energy components stay exactly at their background values.
The internal energy is e(n)=cs²n[log(n/rho_ref)-1], and hydrostatic balance
makes e'(rho)+phi0=mu constant. With fixed total mass, the FULL integrated
relative total energy therefore is exactly

 Erel_N(t)=K_N(t)+cs²D(n_N(t)|rho),
 K_N=(1/2)integral n_N v_N².                                (10)

The matter-potential interaction is included: its first variation cancels
the internal-energy linear part through mu integral(n-rho)=0. It is not
permissible to omit that interaction term separately.

K_N<=V_N²m_N/2=O(N^-1). Hence, uniformly on the fixed slab,

 0<=Erel_N(t)<=epsilon_N:=V_N²m_N/2+cs²m_N h_N(T)->0.         (11)

In particular initial full excess tends to0, with D(0)=0 and
K_N(0)=(1/2)integral rho v_N². The sequence obeys the quantified approximate
budget Erel_N(t)<=Erel_N(0)+epsilon_N, but we do NOT call this an exact
energy inequality.

In fact the exact inequality Erel_N(t)<=Erel_N(0) FAILS for every sufficiently
large N with our declared positive-side support. Differentiate the flow
kinetic identity and entropy at t=0:

 K_N'(0)=integral rho v_N² v_N'
        =-(1/3)integral rho' v_N³ >0,
 D'(0)=integral n_t(0)log[n(0)/rho]=0.                       (12)

The integration by parts has no support-edge term, and rho'<0 throughout the
nonzero profile. Thus Erel_N'(0)>0 and the energy exceeds its initial value
for a sufficiently short positive time for each N. Indeed K_N'(0) tends to
the positive constant -rho'(x*)v0³L integral f³/3. This does not contradict
(11): the initial change occurs on an increasingly short scale and the total
uniform excess tends to0. No finite-amplitude energy injection or exact coupled
solution is inferred from a prescribed-velocity residual ansatz.

The full relative energy DENSITY has the exact form

 E_N-E0=n_N v_N²/2+cs² h(n_N,rho)+mu(n_N-rho),
 h=n log(n/rho)-n+rho>=0.

Its uniform-in-time L1 norm is at most epsilon_N+2|mu|m_N, hence tends to0.
The small signed linear density term cannot conceal an energy concentration.

## 5. Full current, fixed times and the initial fast transient

The full inherited energy current, with field velocities zero, is

 S_N=n_N v_N³/2+j_N[cs²log(n_N/rho_ref)+phi0].                (13)

For fixed N it is finite and integrable, including all cubic, enthalpy and
potential transport. On the transported support, (8) gives
|log(n_N/rho_ref)|<=K_ref+h_N(T), with K_ref a fixed bound for
|log(rho/rho_ref)|. Therefore (5),(6) imply

 ||S_N||_(L1([0,T]xI))
 <=V_N² l_N m_N
  +[cs²(K_ref+h_N(T))+||phi0||infinity]2l_N m_N
 =O(N^-4)+O(N^-6 log N) ->0.                               (14)

At t=0 the cubic current still converges as a spatial measure to
F_*delta_(x*), F_*=rho(x*)v0³L integral f³/2>0, as in the inherited control.
At EVERY fixed t>0 its limit is instead zero. To see this without freely
exchanging limits, use the flow change of variables:

 integral n_N(t,x)v_N(x)³/2 dx
 =(v0³L/2) integral_(-1)^1 rho(x*+l_N y)
                                      f(Y_(omega_N t)(y))³ dy.

For each interior y, Y_s(y)->1 as s->infinity, by (2), and f(Y_s)->0. The
integrand is dominated by the fixed local bound for rho, because0<=f<=1.
Thus dominated convergence proves the zero limit for each fixed t>0. The
same reasoning works uniformly on [t0,T] for t0>0: for each y the flow has
eventually reached the decreasing part of f. Lower-order current has the
uniform spatial L1 bound O(N^-2 log N) and also vanishes.

At scaled times t_N=s/omega_N with fixed finite s>=0, the cubic flux instead
has the finite coefficient (rho(x*)v0³L/2)integral f(Y_s(y))³dy, concentrated
at x*. This is an initial fast transient, not uniform-in-time flux convergence.
It carries vanishing spacetime L1 mass by (14), so no time-delta flux survives.
The full initial ENERGY density still converges strongly; an initial flux
trace of order1 is a different object.

## 6. Actual coupled residuals and test topologies

Define Rc=n_t+j_x, Rphi=tau Phi_tt-B_x+C n,
Rchi=sigma X_tt-J X_xx+U'-T, and
Rm=j_t+(n v²+cs²n)_x+n g0. The exact identities are

 Rc=0, Rphi=C(n_N-rho), Rchi=0,
 Rm=j_t+partial_x[n_N v_N²+cs²(n_N-rho)]+(n_N-rho)g0.        (15)

Thus the actual Q source residual is small but NONZERO, with uniform-time
L1 bound2C m_N=O(N^-3). No changed-density static solution is asserted.
Continuity being exact, conservative and primitive momentum forms agree
where their products are defined; equivalently Rm=n_N v_N v_N'+cs²n_x+n g0.

The full combined momentum has P_N=j_N and
Pi_N=Pi0+n_N v_N²+cs²(n_N-rho), with Pi0 the unchanged constant background
stress. Hence

 Rcomb=partial_t j_N+partial_x[n_N v_N²+cs²(n_N-rho)]
      =Rm-(n_N-rho)g0.                                    (16)

To declare a sufficient topology, test (15),(16) against compact spacetime
C1 functions with supremum of value and first derivatives bounded. Use

 ||j_N||_(L1_tx)<=2l_N m_N=O(N^-6),
 ||n_N v_N²||_(L1_tx)<=2V_N l_N m_N=O(N^-5),
 ||n_N-rho||_(L1_tx)<=2T m_N=O(N^-3).

Both momentum residuals tend to0 in that spacetime first-derivative-test norm,
with O(N^-3) bound for interior-time tests. No uniform-in-time spatial momentum
residual norm is claimed: temporal concentration must not be erased by such
an assertion. For weak tests that include t=0, the additional actual initial
momentum trace has L1 norm O(N^-2), so it also vanishes. Fixed fields have
zero perturbative initial traces. Mass has its exact initial rho trace.

## 7. Actual local energy residual and wall/initial terms

Use the FULL current(13) and density in Section4. The exact local residual
of this prescribed ansatz is RE_N=partial_t E_N+partial_x S_N; it is generally
nonzero for finite N. Since E0 is static and its energy current is zero,
for compact spacetime C1 tests

 |<RE_N,zeta>|
 <=||E_N-E0||_(L1_tx)||zeta_t||infinity
    +||S_N||_(L1_tx)||zeta_x||infinity ->0.                  (17)

The rate is bounded by T[epsilon_N+2|mu|m_N] plus the right side of(14).
Thus the persistent FGF043 local defect disappears after this exact continuity
repair. This result includes a vanishing FULL local-energy residual, not only
a vanishing scalar global budget.

For tests meeting t=0, include the actual relative initial energy term, whose
L1 norm is K_N(0)=O(N^-1). It tends to zero and supplies no time-delta energy
source. The order1 initial spatial flux trace is not an energy-density trace;
it cannot be inserted as a boundary source in(17). All states equal background
near the physical walls, j_N=0 and S_N=0 there exactly, with no incoming mass
or unmodeled work. No support-edge delta occurs because the finite-time flow
and fields have the stated continuous traces. The nonzero residual at finite
N means neither local nor global exact solution energy balance is claimed.

## 8. Zero-velocity control, scope and branch bookkeeping

With velocity identically zero, the flow is the identity, n=rho for all time,
all residuals vanish, and full relative energy/current are exactly zero. This
is the one requested control. Formula(5) then has both sides zero and verifies
that no mass transport is produced by the coordinate representation itself.

Outcome: finite initial participating mass removes the persistent cubic
SPACETIME current; polynomial compression preserves uniformly vanishing
entropy and full excess energy. The exact global energy inequality nevertheless
fails by(12), while a quantified vanishing error and all declared weak local
residual limits hold. These distinctions are simultaneous, not alternatives
that may be silently substituted for one another. This is an exact continuity
solution only; the coupled Q source/momentum equations are residual equations.
It does not construct a nonlinear coupled solution or settle finite nonzero-
energy compactness, uniqueness, physical stability or the evolution problem.

L,l_N are lengths; v0,V_N velocities; omega_N an inverse time; H,s,N are
dimensionless; participating mass is per transverse area. D has mass-per-area
units, Erel energy per area, and integrated spacetime energy current has energy
per area times length. Coefficients and all MOND source laws are unchanged.
The two a0 footings9.3619e-11 and1.1279e-10 m/s² remain separate background
hypotheses. Constant-vacuum, frozen-H and genuinely evolving-H histories are
distinct; the last requires its own work/reservoir accounting. Responsive scale
and inertias remain added diagnostic assumptions. No RAR/M/filtered-MONO,
metric/photon/DOF, physical reservoir, observations, historical novelty or
physical-theory closure follows.

The remaining implication is whether a narrowly specified same-action
approximation can satisfy the actual momentum/field dynamics AND a justified
energy admissibility rule, rather than merely this prescribed-velocity weak
residual limit. The exact inequality failure(12) must remain visible in any
such next target. No new approximation is executed in this pass.
