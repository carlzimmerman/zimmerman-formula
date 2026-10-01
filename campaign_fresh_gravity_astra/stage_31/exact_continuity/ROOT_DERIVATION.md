# FGF044: exact continuity removes the sustained local flux in this family

Root proof frozen before new FGF044 author/reviewer proofs or previews. One
specified profile and one exact transport flow; no computation or scan. The
coupled fields remain a residual ansatz, not exact solutions. The profile is
changed as declared by the task, from a smooth bump to a C1 compact polynomial.

## Flow, support, density and regularity

Fix the same Q static crossing on I, with C=4piG, positive coefficients,
rho>0, phi0,chi0, signed B0_x=C rho, cs²rho_x=-rho g0, g0=phi0_x,
-Jchi0_xx+U'-T0=0. Choose x* on the POSITIVE-gradient regular side, so
rho_x<0 on a compact neighborhood. Fixed L,v0,T>0 have length, velocity and
time units. Define ell_N=L/N³, s=v0 N t/ell_N=v0 N4 t/L, and
f(y)=(1-y²)² for |y|<1, zero otherwise. Put v_N(x)=v0 N f((x-x*)/ell_N).
Support S_N=(x*-ell_N,x*+ell_N) lies strictly away from center and walls.

f is globally C1,1 (C1 with Lipschitz first derivative), piecewise polynomial;
its second derivative has endpoint jumps. This is sufficient for the following
classical continuity flow and weak residual tests, not a claim of C-infinity
solutions. Let Y_s(a) solve Y_s'=f(Y_s), Y_0=a. Outside [-1,1] it is stationary.
Inside, the increasing coordinate
F(y)=integral_0^y (1-z²)^-2 dz
has range all real numbers; define Y_s(a)=F^-1(F(a)+s). This proves existence
for every finite s, no arrival at an endpoint in finite time, and an increasing
invertible flow. Its Jacobian J_s=partial_a Y_s=f(Y_s)/f(a)>0 inside, with
endpoint limit1 and outside value1. Equivalently J_s=exp(integral_0^s f'(Y_r)dr).
These formulas and f in C1,1 give a C1 flow with locally Lipschitz spatial
Jacobian at each finite time. Transported density is continuous and piecewise
W1,infinity on this regular neighborhood for each N and finite time; no uniform
N regularity bound is claimed. Endpoint density joins the background because
J_s->1 there. There is no jump source in continuity. Elsewhere the old static
crossing regularity is unchanged.

Physical flow X_N(t,x0)=x*+ell_N Y_s((x0-x*)/ell_N) on S_N, identity outside.
Define n_N(t,X_N)=rho(x0)/J_s and j_N=n_N v_N. Then the Jacobian identity
n_N dx=rho(x0)dx0 proves EXACT n_t+(n v_N)_x=0, positivity and fixed total mass.
The interval S_N is invariant; outside particles cannot feed it. Its conserved
participating mass m_N=integral_S_N rho is O(N^-3). Thus

||n_N-rho||1<=2m_N, ||j_N||1<=v0 N m_N=O(N^-2),
K_N=integral n_N v_N²/2<=v0² N² m_N/2=O(N^-1),              (1)

uniformly on [0,T]. Keep phi=phi0,chi=chi0 and field velocities zero. Field
walls and total mass remain fixed. This repairs only continuity exactly.

## Polynomial Jacobian bounds and entropy

Along an interior flow set z(y)=1/(1-y²)=1/sqrt(f(y)). Direct differentiation
gives dz(Y_s)/ds=2Y_s, whose magnitude is at most2. Since z>=1, forward and
backward comparison yield

(1+2s)^-1<=z(Y_s)/z(a)<=1+2s,
(1+2s)^-2<=J_s<=(1+2s)².                                  (2)

There is no exponential-in-N entropy estimate hidden here. Let Lrho be the
fixed supremum of |partial_x log rho| on the support neighborhood. Along a
trajectory |X_N-x0|<=2ell_N. The density formula and (2) imply on S_N

|log(n_N/rho)|<=2log(1+2s)+2ell_N Lrho=:Lambda_N(t).          (3)

The restriction of n_N and rho to S_N has the same mass m_N. Therefore the
relative entropy D(n_N||rho)=integral[n_N log(n_N/rho)-n_N+rho] satisfies

0<=D<=m_N Lambda_N(t), sup_[0,T] D=O(N^-3 log N).            (4)

The background is bounded positive; at every finite N,T so is the flow density,
with bounds allowed to depend on N,T. No uniform density cap is used. All
entropy and energy terms are finite. In particular e(n)=cs²n(log(n/rho_ref)-1)
obeys ||e(n_N)-e(rho)||1<=cs²D+||e'(rho)||infinity||n_N-rho||1.

## Full energy: small uniformly, but exact global inequality fails here

Hydrostatics gives mu=e'(rho)+phi0 constant. All field/scale energies remain
background. Pointwise the full energy-density difference is exactly

H_N-H0=n_N v_N²/2+cs² h(n_N,rho)+mu(n_N-rho),
h=n_N log(n_N/rho)-n_N+rho>=0.

Hence the TOTAL relative energy is
E_N(t)=K_N(t)+cs²D(n_N||rho),
and sup_t ||H_N-H0||1=O(N^-1)+O(N^-3 log N)->0.              (5)
The n phi interaction and the hydrostatic first variation were retained; they
are not neglected because the fields were frozen. At t=0, D=0 and E_N(0)=K_N(0).

The exact inequality E_N(t)<=E_N(0) is NOT true for this positive-side choice.
At t=0 continuity gives
K_N'(0)=integral rho v_N² v_N,x=-(1/3)integral rho_x v_N³>0.
The relative entropy derivative is zero at n=rho, so E_N'(0)=K_N'(0)>0.
All finite-N differentiations are legitimate with compact C1,1 velocity and
positive finite-time density; integration by parts has no boundary term.
Thus for each N, some sufficiently small positive times violate that exact
inequality. No global energy law of an exact coupled solution is contradicted.

A sharper approximate inequality is available without assuming conservation.
For constant initial density rho*=rho(x*), define g(u)=f(F^-1(u)); g is even
and decreases with |u|. Changing a=F^-1(u), da=g(u)du, gives
integral_-1^1 f(Y_s(a))² da=integral_R g(u+s)² g(u)du.
This is maximal at s=0: represent each nonnegative factor as an integral of
indicators of its level sets. Those level sets are centered intervals; their
intersection length after translation cannot exceed the length when centers
coincide. Integration proves the inequality directly. Integrals are finite
since integral g du=2 and 0<=g<=1. Therefore constant-density kinetic energy
never exceeds its initial value. For the actual rho, |rho(x0)-rho*|<=ell_N
sup|rho_x|; comparing both times to that constant-density integral yields

K_N(t)<=K_N(0)+O(N² ell_N²)=K_N(0)+O(N^-4),
E_N(t)<=E_N(0)+O(N^-4)+cs²m_N Lambda_N(T).                  (6)

The error is O(N^-3 log N), uniform on the fixed slab. It is an explicit
vanishing-error global budget, NOT the exact inequality disproved above.
Constants depend on fixed physical inputs, not N; no claimed sharp constant.

## Finite travel budget for cubic and complete energy flux

Every particle initially inside S_N moves only rightward and by at most2ell_N.
For nonnegative stationary v_N, integration along each actual trajectory gives

integral_0^T integral n_N v_N³/2 dxdt
 = (1/2)integral_S_N rho(x0) integral_(x0)^(X_N(T,x0)) v_N(x)² dx dx0
 <= v0² N² ell_N m_N=O(N^-4).                             (7)

This exact mass/flow identity, independently checked using dX/dt=v_N, is the
finite-supply bound. Also integral_0^T ||j_N||1 dt<=2ell_N m_N=O(N^-6).
The complete energy flux, both field fluxes being zero, is

Q_N=n_N v_N³/2+cs² n_N v_N log(n_N/rho)+mu j_N.

Using (3) and the integrated current bound,

||Q_N||L1((0,T)xI)<=O(N^-4)+[cs²Lambda_N(T)+|mu|]O(N^-6)->0. (8)

Thus the previous persistent cubic SPACETIME concentration disappears. This
is not a uniform-in-time flux estimate. At t=0, the old cubic flux measure is
still rho(x*)v0³L integral f³/2 times delta_x*. At every FIXED t>0, s_N->infinity
and for each interior label a, Y_s(a)->1, so f(Y_s(a))->0. The pushforward
formula
integral n_N v_N³ dx=v0³L integral_-1^1 rho(x*+ell_N a) f(Y_s(a))³ da
and bounded convergence prove the cubic flux L1 norm tends to0 at that time.
The initial nonzero current is only a fast transient with vanishing integrated
weight by (7); no nonzero temporal delta remains. The two limits t->0 and N->
infinity are not interchangeable for the current. Equation(8) includes the
enthalpy/potential terms and requires no assertion about a long-time physical
trajectory. It is a fixed-T statement with an N-dependent dimensionless time.

## Actual remaining equation residuals and traces

Mass residual Rc=0 EXACTLY. Since original fields are fixed,
Rphi=tau phi_tt-B_x+C n_N=C(n_N-rho),
Rchi=sigma chi_tt-Jchi_xx+U'-T=0.
Thus Rphi is O(N^-3) in L-infinity_t L1_x; source is not falsely declared exact.
The signed MOND dynamic source B_x=Cn+tau phi_tt is used. Both field kinematic
identities are exact.

Conservative matter momentum residual can be written with no large products:

Rj=partial_t j_N+partial_x[n_N v_N²+cs²(n_N-rho)]
                                      +(n_N-rho)g0.         (9)

Bounds(1) and bounded g0 show this tends to0 against compact spacetime C1 tests:
the terms are controlled by O(N^-2), O(N^-1)+O(N^-3), and O(N^-3) respectively,
times the fixed slab length and the corresponding test derivative suprema.
No uniform-in-time spatial residual norm is asserted for partial_t j_N. Because
continuity is exact, primitive and conservative momentum residuals coincide
where computed. Density is regular enough at each finite N for the force and
pressure to be meaningful; the form(9) is the accepted weak estimate.

Full combined momentum is P_N=j_N, Pi_N=Pi0+n_N v_N²+cs²(n_N-rho).
Its residual is (9) minus (n_N-rho)g0 and also tends to0 in that spacetime dual.
This difference is essential because the field source residual is no longer0.
Combined density and stress converge L1 uniformly in time by(1).

The full local energy residual RE=partial_t H_N+partial_x Q_N tends to0
against compact spacetime C1 tests by the actual L1 estimates(5),(8). This is
not inferred by multiplying the small momentum residual by an unbounded v_N.
Initial density equals rho, initial energy excess is O(N^-1) and initial current
L1 is O(N^-2). Tests reaching t=0 use those actual traces; their difference
from background is small. The initial flux itself need not converge strongly,
but there is no initial flux term in the first-order weak energy-density law,
and its integrated transient vanishes. Near both walls the flow is identity,
n=rho and v_N=0, so mass/energy boundary currents vanish and perturbation
momentum traction is zero. No hidden external mass or energy is introduced.

Zero-velocity control: set the prescribed v to0, obtaining identity flow,
n=rho, every residual exactly0, Erel=0 and Q=0. This checks source signs,
initial/wall terms and absence of artificial density evolution.

## Exact scope and branches

For this ONE task-specified C1,1 profile and exact continuity flow, entropy and
full energy remain uniformly small, all remaining equations have vanishing
residuals in the stated norms, and full spacetime energy flux/local residual
vanish. Finite participating mass removes the persistent FGF043 flux. However
the strict global energy inequality fails for the selected positive side; only
the quantified vanishing-error budget(6) is proved. Density transport does not
make field or momentum equations exact. This is no general existence, uniqueness,
local admissibility sufficiency, physical stability or arbitrary-energy theorem.

Both a_ref=9.3619e-11 and1.1279e-10 m/s² are separate backgrounds. Constant-vacuum
and frozen a(0)E(z), E²=.315(1+z)^3+.685, are fixed-reference cases; evolving-H
requires its still-missing work/reservoir sector. Signed Q MOND source and all
inertias remain intact. The prescribed unbounded velocity is a diagnostic
transport input, not a physical photon-speed prediction. No RAR/M/filtered-MONO,
metric/photon/DOF, conserving physical reservoir, calibrated evidence, historical
novelty or theory closure. The next implication must change another actual
constraint or admissibility mechanism, not repeat this one finite-supply estimate.
