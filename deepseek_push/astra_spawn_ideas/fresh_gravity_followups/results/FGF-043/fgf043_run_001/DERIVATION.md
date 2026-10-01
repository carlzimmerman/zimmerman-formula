# FGF043: weak equation residuals do not enforce local energy balance

Proof-only derivation frozen before new root/reviewer proofs or previews. The
static cubic-flux concentration is explicitly inherited from the independently
frozen FGF042 proof; it is NOT a new result here. The new target is its complete
time-independent equation-residual and initial/wall/local-energy audit.

## 1. Same action, fixed support and inherited family

Keep the fixed-reference Q static crossing on I=(-d,d), fixed physical
coefficients and field walls, background rho>0, phi0,chi0 and g0=phi0'. Write
C=4piG, a=a_ref exp chi0, signed Q flux B, T=-a W_a and
U=S0[cosh(2chi)-1]/4. The background obeys

 B0'=C rho, cs²rho'=-rho g0, J chi0''=U'-T0,
 e'(rho)+phi0=mu (a spatial constant),
 e(n)=cs² n[log(n/rho_ref)-1], e(0)=0.

Choose x* on a regular side strictly away from the center and walls; fix a
compact interior neighborhood there. Let L>0 be a reference length, v0>0 a
velocity, and one nonnegative nonzero f in C_c^infinity((-1,1)). For all
sufficiently large dimensionless integers N, use the inherited states

 v_N(x)=v0 N f(N³(x-x*)/L), j_N=rho v_N,
 n_N=rho, Phi_N=phi0, X_N=chi0,
 Phi_N,t=X_N,t=0.                                            (1)

Make ALL these states time independent on one fixed interval [0,T]. The
support remains inside the chosen regular neighborhood. No coefficient,
reference, mass, field wall or scale is changed with N. Perturbations vanish
near the crossing as well as near the outer walls. These states are smooth
where nontrivial; the inherited static weak background is unchanged elsewhere.
They are approximate states, never claimed exact solutions.

Direct change of variable y=N³(x-x*)/L gives, uniformly in time,

 ||j_N||_1=O(N^-2), integral rho v_N²=O(N^-1),
 integral rho v_N³/2 -> F_* =rho(x*) v0³ L integral f³/2>0.     (2)

The last moment is the already-known control. The spatially integrated flux
F_* has units of energy flux times length; delta_(x*) has inverse-length
units. The rate estimates use fixed bounded rho and its derivatives on the
chosen compact neighborhood, not a changed density ansatz.

## 2. Every actual equation residual in declared spaces

Define conservative residuals

 Rc=n_t+j_x,
 Rphi=tau Phi_tt-B(Phi_x,a)_x+C n,
 Rchi=sigma X_tt-J X_xx+U'(X)-T,
 Rm=j_t+(j²/n+cs² n)_x+n Phi_x.

Use the spatial weak norm Lip*: the supremum against compact tests zeta with
||zeta||infinity+||zeta'||infinity<=1. In particular
||partial_x h||_(Lip*)<=||h||_1. All estimates below hold in L-infinity_t
of that spatial norm, and therefore against smooth compact spacetime tests.
No stronger residual norm is implied.

Since density and both fields are exactly their static reference,

 Rphi=0, Rchi=0,
 Rc=partial_x(rho v_N),
 Rm=partial_x(rho v_N²).                                   (3)

Thus ||Rc||_(Lip*)=O(N^-2) and ||Rm||_(Lip*)=O(N^-1), both tending to0.
The source relation used is the actual signed MOND equation
B_x=C n+tau Phi_tt. It happens to reduce exactly to the background static
source on this ansatz, not to a Newtonian equation.

For completeness the primitive matter residual is
Rv=rho(v_t+v v_x)+cs²rho_x+rho Phi_x=rho v_N v_N'. It obeys

 Rv=(1/2)partial_x(rho v_N²)-(1/2)rho' v_N²,
 Rm=Rv+v_N Rc.

It too tends to0 in Lip* at O(N^-1). This is a weak statement; neither the
large derivative residuals nor their products with v_N are claimed small in
strong norms. Separate force rho g0 is bounded and cancels hydrostatics exactly.

The FULL combined momentum and stress are

 P=j-(tau Phi_t Phi_x+sigma X_t X_x)/C,
 Pi=j²/n+cs²n+[tau Phi_t²/2+sigma X_t²/2
                          +B Phi_x-W+J X_x²/2-U]/C.

The background Pi0 is distributionally constant, P0=0, so on (1)

 P_N=j_N, Pi_N=Pi0+rho v_N²,
 Rcomb=partial_t P_N+partial_x Pi_N=partial_x(rho v_N²).       (4)

This actual combined residual vanishes with the same O(N^-1) Lip* bound.
P_N and Pi_N-Pi0 even converge strongly in L1. No field momentum, scale stress
or kinetic stress is dropped in deriving (4).

## 3. Full initial energy and exact global scalar inequality

The inherited FULL energy density and current are

 E=j²/(2n)+e(n)+n Phi
       +[tau Phi_t²/2+W(|Phi_x|,a)+sigma X_t²/2
                                   +J X_x²/2+U(X)]/C,
 S=v[j²/(2n)+e(n)+cs²n+n Phi]
                        -[Phi_t B+J X_t X_x]/C.             (5)

For (1), every interaction and scale term remains at its background value,
so E_N-E0=rho v_N²/2. The total excess is O(N^-1)->0 at t=0 and every t,
and is EXACTLY constant in time for each N. Hence these approximate states
satisfy the global scalar statement Erel_N(t)<=Erel_N(0), indeed equality.
This is a verified property of this time-independent ansatz, not an assertion
that its nonzero equation residuals produce an exact solution energy law.

The initial data are strongly prepared in FULL energy: the relative energy
density tends to0 in L1, field and scale differences vanish, entropy vanishes,
and integral rho v_N² tends to0. There is no hidden initial energy-density
concentration. Initial mass equals the background, and j_N tends strongly to0
in L1 (also L2 here since background rho is bounded). The initial energy FLUX,
which is not controlled by the energy norm, has a different limit below.

All current perturbations vanish near both outer walls. Mass flux j_N, matter
energy flux and field energy flux vanish there exactly. Background momentum
traction can be nonzero, but its perturbation is zero. Fixed wall values and
mass are genuine, not compensating external work assumptions.

## 4. The actual LOCAL energy residual survives

Hydrostatic balance gives e'(rho)+phi0=mu, and e(rho)+cs²rho=rho e'(rho).
Therefore the full current (5) specializes EXACTLY to

 S_N=rho v_N³/2+mu rho v_N.                                 (6)

The enthalpy and potential terms are included together, not omitted as small
without checking them. Their combined L1 norm is O(N^-2). The cubic current
converges as a finite spatial measure to F_* delta_(x*); for a continuous
test this follows by the same y change of variable and dominated convergence.
Consequently the actual local residual is the smooth-on-support distribution

 RE_N=partial_t E_N+partial_x S_N=partial_x S_N
        -> F_* partial_x delta_(x*)                         (7)

at each time and as a spacetime distribution with the extra dt factor. For
any compact smooth test zeta(t,x),

 <RE_N,zeta> -> -F_* integral_0^T partial_x zeta(t,x*)dt.      (8)

Choosing a product test with nonzero spatial derivative at x* makes this
limit nonzero. Every member's local energy residual is well defined; its
failure is nonvanishing, not undefined multiplication.

There is no conflict with the global constant energy: the residual integrates
to zero in x, since the full flux vanishes at both walls. The spatial derivative
of a delta is sign indefinite. It also fails a distributional local dissipative
inequality with a vanishing error, because nonnegative tests can have either
sign of derivative at x*. This is local balance failure in approximate states,
not creation of net energy or an exact-solution pathology.

The precise initial trace cannot cancel (8). With tests vanishing at T, the
relative time-density term integral(E_N-E0) zeta_t and its initial trace
integral(E_N(0)-E0)zeta(0) cancel exactly because E_N-E0 is time independent.
Both separately tend to0, while the flux term has the nonzero limit (8).
No initial defect measure or outer-wall flux is suppressed.

One can check why equation-residual convergence is insufficient without
repeating a general off-shell theorem. Directly on this ansatz,

 RE_N=v_N Rm+(mu-v_N²/2)Rc
     =v_N Rv+(mu+v_N²/2)Rc.                                (9)

Expanding both derivatives gives exactly (6)'s derivative. The factors v_N
and v_N² are unbounded, so convergence of Rc,Rm or Rv in Lip* does not imply
that the right side tends to0. Equations (7)-(9) identify the missing local
acceptance test: an approximation claiming local energy balance must also
have RE_N->0 against compact spacetime tests, or a justified local dissipative
inequality with vanishing admissibility error. Global energy and the listed
weak equation residuals alone do not supply this test.

## 5. One amplitude control

Use the SAME width/profile/units but remove the factor N:

 v_N^small=v0 f(N³(x-x*)/L).

This is one amplitude control, not a scan. It has a fixed velocity cap,
||j_N^small||_1=O(N^-3), integral rho(v_N^small)²=O(N^-3), and the entire
energy current has L1 norm O(N^-3). Its mass and both momentum residuals are
O(N^-3) in Lip*, field residuals remain exactly0, and RE_N^small->0 in
spacetime distributions. Initial excess and wall terms behave as before,
now with no nonzero flux measure. Thus the nonzero local defect in (7) is
sensitive to the amplitude, not to a wall or background artifact.

## 6. Sufficient extra bounded-velocity gate, without a density cap

Consider the GENERAL FGF042 zero-excess class, not only n=rho. In addition to
its proved conclusions, impose ONE extra uniform physical velocity bound

 |j_m|<=V n_m almost everywhere, V<infinity fixed.             (10)

At n=0 this forces j=0; define v=0 there and v=j/n when n>0. Terms involving
n log n use their continuous0 value at vacuum. No positive lower bound or
upper pointwise density bound is assumed. The condition (10) is an extra
approximation hypothesis, not a physical cutoff or modified action.

FGF042 gives integral j_m²/n_m->0, ||j_m||_1->0,
D(n_m|rho)->0, ||n_m-rho||_1->0 and Phi_m->phi0 uniformly. The full cubic
kinetic energy current satisfies

 integral |j_m³/(2n_m²)| <= (V/2)integral j_m²/n_m ->0.        (11)

For enthalpy, write log(n/rho_ref)=log(n/rho)+log(rho/rho_ref).
The bounded positive background has bounded logarithm, and pointwise for
n>=0, with the continuous vacuum convention,

 |n log(n/rho)|<=h(n,rho)+|n-rho|,
 h=n log(n/rho)-n+rho>=0.

Thus, with Klog=||log(rho/rho_ref)||infinity,

 integral |j log(n/rho_ref)|
 <=V[D(n|rho)+||n-rho||_1]+Klog||j||_1 ->0.                 (12)

This justifies integrability AND convergence of logarithmic enthalpy transport
without assuming bounded density or excluding vacuum. Also
integral |j Phi|<=||Phi||infinity ||j||_1->0. Multiplying (12) by cs² and
combining with (11) identifies the entire matter energy current strongly in
L1. The already-controlled field energy current converges strongly too.

If the FGF042 conclusions and cap V hold uniformly in time on a fixed finite
slab, these estimates are uniform in time, hence also spacetime L1. With the
strong energy-density convergence, the full local energy residual then tends
to the zero background residual in spacetime distributions. This is a
sufficient compactness/acceptance gate, not a derivation of (10), exact local
balance for each member, PDE existence or equivalence of separate weak force
products. The main family violates (10); the one amplitude control meets it.

## 7. Scope, units and next bounded obligation

The established counterexample has vanishing full initial excess, an exact
global scalar energy inequality, all declared weak mass/field/momentum
residuals tending to0, correct initial/wall accounting, and a NONZERO LOCAL
energy residual. It refutes that precise approximate-admissibility implication.
It does not meet a local energy acceptance criterion and therefore is not a
counterexample to exact equations or approximations already satisfying one.

L is length, v0 and V velocity, N dimensionless. E is energy density, S energy
flux, F_* energy flux times length, and RE energy density per time. No field
inertia or scale coupling has been adjusted. Both a0 footings9.3619e-11 and
1.1279e-10 m/s² remain separate; each uses its own actual signed Q background.
Constant-vacuum, frozen-H references and evolving-H histories are distinct;
the last requires external work/reservoir accounting absent from this fixed-
reference construction. No RAR/M/filtered-MONO, physical metric/photon/DOF,
conserved physical reservoir, empirical calibration, historical novelty or
theory closure is inferred.

The next obligation should construct or test one actual same-action bounded
approximation with an independently justified local energy residual estimate
and its initial/wall traces. Merely adding a global budget or redoing a static
moment mismatch is exhausted. The present extra velocity gate identifies what
would suffice for zero-excess local energy compactness; it does not show the
coupled dynamics preserve that gate or control finite nonzero-energy limits.
