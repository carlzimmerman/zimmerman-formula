# FGF043: a global energy budget does not impose local balance

Root proof frozen before new FGF043 author/reviewer proofs or previews. The
static cubic-flux moment family is already in FGF042 ancestry. What is new here
is its full equation-residual and local-balance test on a fixed time slab.
Proof-only; no mathematical executable, scan, imported mechanism or novelty.

## Fixed background and actual residuals

Use the inherited fixed-reference Q diagnostic action on a fixed interval I.
Background rho>0,phi0,chi0 satisfies B0_x=C rho, cs²rho_x=-rho g0,
-J chi0_xx+U'-T0=0, g0=phi0_x, C=4piG. Signed
B(g,a)=sgn(g)(sqrt(a²+4g²)-a)/2, a=a_ref exp chi0, W_g=B,T=-W_chi.
The hydrostatic chemical-plus-potential value
mu=cs²log(rho/rho_ref)+phi0 is spatially constant. It has potential units.
Coefficients tau,sigma,J,cs²,S0 remain fixed positive; same mass and walls.
Select x* on one regular side of the crossing, fixed physical length L,
velocity v0>0, nonnegative nonzero f in C_c^infinity(-1,1), and N->infinity.
For all sufficiently large N the support below lies away from center and walls.
On a FIXED time slab[0,T] set the time-independent states

n_N=rho, phi_N=phi0, chi_N=chi0, u_N=w_N=0,
v_N=v0 N f(N³(x-x*)/L), j_N=rho v_N.

They are smooth on the perturbation support and equal background elsewhere.
No claim of exact nonlinear evolution: their continuity equation is not exact.
The actual residuals, with conservative matter momentum convention, are

Rc=n_t+j_x=(rho v_N)_x,
Rphi=tau phi_tt-B_x+C n=0,
Rchi=sigma chi_tt-J chi_xx+U'-T=0,
Rj=j_t+(j²/n+cs² n)_x+n phi_x=(rho v_N²)_x.

Both field kinematic identities are exact. The material-velocity convention
Rv=n(v_t+v v_x)+cs²n_x+n phi_x equals rho v_N v_N,x here, and
Rj=Rv+v_N Rc exactly. Distinguish these conventions in energy identities.
The background Q source, not a Newtonian substitute, was used for Rphi=0.

A fixed spatial test norm with bounded value and first derivative (after
fixed reference units if needed) gives ||partial_x F||dual<=||F||1.
By changing variable y=N³(x-x*)/L, uniformly in t,
||j_N||1=O(N^-2), integral rho v_N²=O(N^-1), ||j_N||2=O(N^-1/2).
Thus Rc is O(N^-2) in the spatial Lipschitz-test dual and O(N^-1/2) in H^-1.
Rj is O(N^-1) in the Lipschitz-test dual. No H^-1 smallness of Rj is claimed.
Also Rv=partial_x(rho v_N²)/2-rho_x v_N²/2 is O(N^-1) in that same dual.
All statements hold uniformly in time, hence for compact spacetime tests.
There is no small pointwise or strong L1 residual assertion.

Full combined momentum has P_N=j_N and Pi_N=Pi0+rho v_N²; the field/scale
parts are unchanged. The background Pi0 is constant distributionally, including
the unchanged central crossing. Its residual is the same Rj, small in the stated
weak norm. P and Pi converge strongly in L1 to their background values.

## Initial/global energy versus local energy residual

Let H and Q denote full energy density and flux. All field/internal/interaction
terms remain background except fluid kinetic energy, so

H_N=H0+rho v_N²/2,
Q_N=rho v_N[v_N²/2+cs²log(rho/rho_ref)+phi0]
   =rho v_N³/2+mu rho v_N.

Both field fluxes vanish since u=w=0. The full relative TOTAL energy is
E_N=integral rho v_N²/2=O(N^-1)->0. It is exactly constant in time as a
functional of these static comparison states, so E_N(t)<=E_N(0) holds with
equality. This global inequality does not make the states solutions. Initial
energy is also O(N^-1), weighted fluid velocity tends strongly to zero and all
other initial fields are exactly background. Unlike FGF041, no nonzero initial
energy defect is hidden. The kinetic energy DENSITY tends to zero in L1 uniformly
in time. The fixed supports imply zero perturbation mass/energy flux at both
walls and identical field traces; integrating the energy residual over I gives
zero at every finite N.

For each continuous spatial or spacetime test, the SAME change of variable gives

(rho v_N³/2) dx -> Kdelta delta_x*,
Kdelta=rho(x*) v0³ L integral f³/2>0,
mu j_N->0 strongly in L1.

Here Kdelta has the units of spatially integrated energy flux. Therefore the
actual local total-energy residual is

RE_N=partial_t H_N+partial_x Q_N=partial_x Q_N
 -> Kdelta partial_x delta_x*                            (1)

as a spacetime distribution constant in time. More explicitly its pairing with
compact smooth zeta(t,x) tends to -Kdelta integral_0^T zeta_x(t,x*)dt.
Choose a test with nonzero derivative there to see that it DOES NOT vanish.
No strong-residual inference was used. The distribution in(1) takes both signs
even on nonnegative tests: a positive spatial bump can have either sign of
slope at x*, multiplied by a nonnegative temporal bump. Hence it is neither
nonpositive nor nonnegative distribution. A local energy inequality RE<=0 with
an error tending to zero on each nonnegative compact test excludes this family,
as does a local equality with vanishing residual. The global integrated budget
cannot see this spatial derivative because its boundary integral is zero.
This is not net energy creation and not a pathology of an exact solution.

For tests including t=0, H_N-H0 initial traces are L1-small, as are initial P_N.
Integrating H_N zeta_t plus the initial term cancels its static time boundary
contribution exactly. The surviving local term is still the flux derivative.
There is no omitted initial or wall energy supplying this distribution.
The weak limiting background itself solves all its equations; this is failure
of a proposed APPROXIMATION admissibility criterion, not of that background.

## Why weak equation residuals cannot be multiplied by this velocity

The inherited smooth off-shell identity at fixed reference is
RE=v Rv+(v²/2+e'(n)+phi)Rc+u Rphi/C+w Rchi/C.
Substituting Rv=Rj-v Rc gives the conservative form

RE=v Rj+(e'(n)+phi-v²/2)Rc+u Rphi/C+w Rchi/C.

For the selected states this is exactly
v_N(rho v_N²)_x+(mu-v_N²/2)(rho v_N)_x
  =partial_x(rho v_N³/2+mu rho v_N).
The terms involving rho_x and v_x give the correct cubic derivative, with no
remaining background hydrostatic term. Small Rc and Rj in fixed-test dual
norms do not control their products by the growing N-dependent velocity and
squared velocity. This explicitly identifies the failed passage from the
individual residuals to the energy residual. No distribution is multiplied
by a rough limiting velocity; the identity is applied to each regular member
before taking its limit.

## One amplitude control

Use v_N^small=v0 f(N³(x-x*)/L), dividing the old amplitude by N, with all
other states unchanged. Then ||j||1, integral rho v² and ||rho v³||1 are
O(N^-3). All previous residuals vanish, E_N is constant and tends to zero,
and the full energy-flux norm is O(N^-3). Thus the local energy residual now
vanishes even in the spatial Lipschitz-test dual uniformly in time. The
control has exactly the same shrinking support and fixed walls/mass/action.
It is a single explicit control, not an exponent or physical-parameter scan.

## A sufficient full matter-flux condition without density bounds

Consider the GENERAL FGF042 zero-full-excess class on the fixed gated interval,
not just the selected family. That result already gives n->rho in L1,
D(n||rho)->0, integral n v²->0, phi->phi0 uniformly, and strong L2 field
velocities/gradients/scale derivatives. Add the explicit independent hypothesis
|v|<=V on n>0, with one fixed finite physical velocity V for the whole sequence;
define j=nv=0 on vacuum. This is not proved by energy and not a physical cutoff.

At n>=0 let h(n,rho)=n log(n/rho)-n+rho>=0. With 0log0=0,

n |log(n/rho)|=|h(n,rho)+n-rho|<=h(n,rho)+|n-rho|.

The full fluid flux can be decomposed using the actual background constant mu:

Qmatter=n v³/2+cs² n v log(n/rho)+(mu+psi)j, psi=phi-phi0.

Consequently, writing Kfluid=integral n v²/2,

||Qmatter||1 <= V Kfluid+V cs²[D(n||rho)+||n-rho||1]
                    +(abs(mu)+||psi||infinity)sqrt(2M Kfluid) ->0. (2)

At vacuum all products extend by zero and the inequality remains valid. No
uniform density upper or lower bound and no extra log-squared moment is used.
The dimensionless logarithm and the bounded positive background are essential.
The earlier kinetic/entropy convergence supplies every right-hand term in(2).
Field flux -[uB+Jw chi_x]/C also converges in L1 from FGF042's strong L2
products. Thus the COMPLETE energy flux converges strongly in L1 under this
extra velocity hypothesis. Full energy density already converges in L1, so
compact spacetime local energy residuals converge to the background residual0.
This last kinematic consequence does not supply any exact equations for finite
members, a velocity bound propagated by the PDE, or initial/wall traces beyond
those independently specified. Uniform-in-time versions require corresponding
uniform hypotheses as in FGF042.

## Scope, physical bookkeeping, and next gap

This refutes the precise implication: strong initial full-energy preparation,
a global full-energy inequality and all stated weak mass/momentum/field residuals
force local total-energy balance. The counterexample's residual norms and its
unbounded velocity are part of the premises. Adding a local energy admissibility
condition rules it out; a uniform velocity cap suffices for strong full flux in
the vanishing-energy class, but is an additional hypothesis. Local balance alone
is not hereby proved to ensure all strong compactness or nonlinear existence.

Both a_ref=9.3619e-11 and1.1279e-10 m/s² remain separate. Constant-vacuum and
frozen a(0)E(z), E²=.315(1+z)^3+.685, are fixed-reference comparisons; an
actually evolving reference requires its unprovided work/reservoir sector.
The signed Q MOND source and positive inertias are preserved. This diagnostic
fluid model imposes no relativistic velocity ceiling; the unbounded-velocity
family makes no physical superluminal claim or prediction. A physical metric
completion would need its own admissible matter class. No RAR/M/filtered-MONO,
metric/photon/DOF, calibrated observation, novelty or theory closure follows.
A specified energy-consistent approximation/evolution and justified local flux
regularity remain missing; the static budget alone cannot stand in for them.
