# FGF048 independent pre-exposure derivation

Reviewer /root/fgf048_reviewer. Only the task/common contract and pinned OLD
ancestry were read. No FGF048 author, root, preview or other stage35 proof was
read before this file was frozen. Proof only; no mathematical executable runs.
Applicable skills: mathbox proof-audit and proofread-math. Old ancestry hashes
all match. The large combined ancestry read was output-truncated; the complete
FGF047 derivation, task and common documents were read separately in full.

## Claim and independent conclusion

For all admissible integers N>=1, the prescribed exact C1,1 bump has a
classical actual coupled solution through kappa ell/V, for one positive kappa
independent of N (dependent on fixed backgrounds/coefficients and a fixed
auxiliary extension). A sufficiently small kappa retains positive n,a,g in a
fixed box and physical containment. No pressureless limit is taken. A simple
uniform estimate proves |g-g0|<=C kappa/V; a refined field-gradient estimate
below improves this to C kappa ell/V. These are deliberately conservative.
They do not prove the FGF046 upper lifespan or a shock endpoint theorem.

Fix dimensionless measuring units once for all N before taking norms or
adding constants below. All powers refer to restoration with those fixed
units. Constants C may depend on those units and the positive fixed physical
coefficients, never on N. Set c=cs, d=sqrt(J/sigma), delta=ell/V,
epsilon=c/V, eta=1/V, alpha=ell/V^2. None changes a physical coefficient.

Take the FGF047 smooth positive-g auxiliary background extensions once,
independent of N. Let q0=log(rho_e/nref), with p0=w0=0,
k0=chi_e', g0=g_e. Smooth extensions have bounded derivatives. They need
not be hydrostatic outside the physical initial interval K0. The exact velocity
is u0(y)=f(y), y=(x-x*)/ell; s=t/delta, u=v/V. The C1,1 joins remain exact.

## Exact scaled diagonal equations

Define b=sqrt(B_g/tau), h_g=b on g>0, and use
r+=u+epsilon q, r-=u-epsilon q;
H+=p+h(g,chi), H-=p-h(g,chi);
Z+=w+d k, Z-=w-d k, and chi.
Write Y for these seven coordinates and Fld for its last five coordinates.
Then q=(r+-r-)/(2epsilon), u=(r++r-)/2, and

 (partial_s+(u+epsilon)partial_y)r+=-alpha g,
 (partial_s+(u-epsilon)partial_y)r-=-alpha g,
 (partial_s-eta b partial_y)H+=delta[A+h_chi(w-bk)],
 (partial_s+eta b partial_y)H-=delta[A-h_chi(w+bk)],
 (partial_s-eta d partial_y)Z+=delta D,
 (partial_s+eta d partial_y)Z-=delta D,
 chi_s=delta w,

where A=B_chi k/tau-C nref exp(q)/tau and
D=(T-U_s')/sigma. In particular all chi-dependent characteristic sources
remain. The two acoustic speeds are distinct for each N but no speed gap
enters the differentiated transport estimates below.

The coordinate inverse on a fixed compact positive-g field box has bounded
first and second derivatives independent of N. The ONLY potentially singular
fluid inverse derivative is 1/(2epsilon). A fixed box in q is part of the
bootstrap, not inferred from independent rectangular ranges for r+ and r-.
This distinction prevents the false exp(O(N)) density bound.

## Uniform estimates on the physical state box

Bootstrap |u|<=U, qlo-1<=q<=qhi+1 and a fixed field box containing its initial
range at a strictly positive distance m from its boundary. The g sub-box
is separated from zero. The speed vector lambda and source vector F above
have, on this box, uniformly bounded derivatives through order two:

 |D lambda|+|D^2 lambda| <= C,
 |F| <= C(alpha+delta),
 |D F| <= C[alpha+delta(1+epsilon^-1)],
 |D^2 F| <= C[alpha+delta(1+epsilon^-2)].

These statements concern derivatives of the explicit unrestricted formula at
points in the box; no N-dependent cutoff derivative is included or hidden.
The right sides are uniformly bounded since
 delta/epsilon=ell/c=O(N^-3),
 delta/epsilon^2=ell V/c^2=O(N^-2).
For fluid speeds D^2 lambda=0. For field speeds both derivatives are O(eta).
Coefficients need not have such bounds outside the bootstrap box.

Initially P0=||Y_y|| and H0=Lip_y(Y_y) are uniformly bounded: the fluid
coordinates have f' and f'' plus epsilon times smooth background derivatives
scaled by ell and ell^2, while the field coordinates have O(ell) and
O(ell^2) derivatives. In particular H0 exists at the exact joins although
classical second derivatives need not exist there.

For any already constructed fixed-N solution while inside the box, let
P(s)=||Y_y(s)|| and H(s)=Lip_y(Y_y(s)). Differentiating the characteristic
formula once gives D_i Y_i,y=-(D lambda_i Y_y)Y_i,y+D F_i Y_y. Hence

 P(s)<=P0+int_0^s C[P(z)^2+P(z)] dz.

Comparing this derivative equation on two same-family characteristics and
dividing by their separation gives, by the scalar integrating factor,

 H(s)<=H0+int_0^s C[(1+P)H+P^3+P^2] dz.

The factor 3 in the quadratic transport contribution can be absorbed in C:
two factors arise from differentiating lambda_y Y_y, and one from comparing
transport positions. This is the same pair-flow argument as FGF047; it uses
only spatially Lipschitz first derivatives. It never evaluates f'' at a join.
Choose a fixed M>2(sup_N P0+1). Choose kappa small enough that
kappa C(M^2+M)<M/2. Then a first-exit argument gives P<M on [0,kappa]
while in the state box. With this bound the second inequality implies
H<=[sup_N H0+kappa C(M^3+M^2)] exp(C(1+M)kappa)=:Hbar.
Hbar is finite independently of N; it need not be small.

Density is bounded by the exact continuity equation
 (partial_s+u partial_y)q=-u_y.
Since |u_y|<=P, q stays within [qlo-kappa M,qhi+kappa M]. Choose
kappa M<1/2. This propagates density uniformly without applying the singular
inverse to separate amplitude bounds. The fluid characteristic formulas give
|r+|,|r-| <= initial maximum +kappa alpha sup|g|, hence a uniform u bound;
choose U larger than that initial maximum by a fixed margin and shrink kappa.

For a field coordinate Y_j its PDE yields
 |Y_j(s,y)-Y_j(0,y)|<=kappa[C eta M+C delta].
Both eta and delta are bounded above over N>=1, so choose kappa to make this
less than m/2. The inverse field chart is uniformly Lipschitz, hence actual
g,chi,p,w,k remain in their field box. In particular g>=gmin/2>0 and
nref exp(qlo-1)<n<nref exp(qhi+1); a=a_ref exp chi has a fixed positive
lower bound. All box exits are excluded by strict inequalities.

## Why this proves existence through the uniform time

Start with the already proved FGF047 positive-time solution for each fixed N.
On its rescaled interval it obeys the preceding a priori bounds. This use of
a priori estimates does not claim that all FGF047 Picard cutoffs have uniform
constants. Fix N. On a finite maximal interval with s<kappa, the state range
is bounded and separated from the original chart boundary; P and H are bounded.
The PDE gives a bounded Y_s. Its first differentiated equation, interpreted
almost everywhere or by pair difference quotients, gives bounded (Y_y)_s,
because |Y_yy|<=H almost everywhere, speeds are bounded, and the differentiated
source/speed coefficients are bounded. Thus Y and Y_y have uniform time limits
at the endpoint. The trace is C1 with Lip(Y_y)<=Hbar and is compatible.
Compatibility passes by integrating g_t=p_x, chi_t=w, k_t=w_x and the initial
constraints. Apply the finite-N FGF047 construction to this trace, which is
allowed to have nonzero field velocities and arbitrary compatible C1,1 data.
Its construction used only those properties, not hydrostatic stationarity.
Uniqueness glues the restart to the earlier solution. This contradicts an
endpoint before kappa. Strict box margins also allow a restart at kappa.
No uniform lower bound on a restart step is required. Potential reconstruction
uses the trace's compatible spatial gradients and its known potential values.
Thus the original matter/field equations hold classically and the potentials
remain C2. This proves the uniform gate, including endpoint regularity.

## Force feedback, and a conservative derivative estimate

Already g_s=eta p_y yields
 sup|g(s,y)-g0(x*+ell y)| <= C kappa eta M = O(N^-1).
This actual time-integral estimate alone suffices to retain the positive g
margin for large N, and the box gate handles every admissible finite N.
It is not a Taylor estimate at the initial slice.

For a sharper bound put P_F=||Fld_y||. Its initial value is <=C ell.
The field derivative transport equations give, with P<=M,

 P_F(s)<=C ell+int_0^s C[(eta P_F+delta)P_F
                              +delta epsilon^-1 P] dz.

The initial/source field bounds and the bootstrap bound P_F<=M imply
P_F(s)<=C_kappa[ell+kappa delta/epsilon]<=C_kappa ell,
using delta/epsilon=ell/c. Therefore, without a hydrostatic cancellation,

 sup |g-g0| <= C_kappa kappa eta ell = C_kappa kappa delta
                         =O(N^-4).

This is weaker than an optimized feedback expansion but uniformly valid.
For derivative feedback the pair-flow inequality for H_F=Lip(Fld_y), using
bounded P,H and the explicit field-source derivatives, gives

 H_F(s)<=C_kappa[ell^2+kappa delta(1+epsilon^-2)],

with constants also absorbing terms quadratic in P_F and linear in H_F.
Integrating (g_y)_s=eta p_yy in the a.e. sense, then using continuous g_y,
proves on a smaller common spatial interval

 sup |g_x-g0_x| <= C_kappa kappa eta/ell
                       [ell^2+kappa delta(1+epsilon^-2)]
 <= C_kappa[kappa delta+kappa^2(1/V^2+1/c^2)].

This only supplies an O(1) upper bound as N grows; it does not claim that
g_x-g0_x tends to zero. The required positive-gradient margin is g=phi_x>0,
not a sign of g_x. The latter was not assumed positive in the inherited task.

## Physical cones, constraints, energy and controls

On the box, physical speeds obey |v|+c<=VU+c; field speeds are bounded by
fixed bmax,d. Choose S_N=VU+c+bmax+d+1 in fixed speed units. Restrict to
K_t=[x*-R+S_N t,x*+R-S_N t]. Backward characteristics and vertical segments
remain within this cone because S_N bounds every speed strictly. Since
S_N kappa ell/V<=kappa ell[U+(c+bmax+d+1)/v0], choose kappa once so the
right side is <R/4 for all admissible ell<R/2. Thus all original support
and a fixed interior interval remain inside the hydrostatic patch. Comparing
two extensions on their common contained cones gives equality by the FGF047
characteristic difference inequality. The proof uses one fixed extension for
constants but the physical restriction does not depend on arbitrary exterior
values once the domains of dependence fit.

The exact H equations subtract to b(g_t-p_x)=0 after chi_t=w; adding gives
p_t=b^2 g_x+A+b h_chi(chi_x-k). The Z equations and chi_t=w propagate
chi_x=k, eliminating precisely that last term. Reconstruct phi by its time
integral to propagate phi_x=g. There is no static source inversion.

The full local energy is
 E=nv^2/2+c^2 n(log(n/nref)-1)+n phi
  +[tau p^2/2+W+sigma w^2/2+Jk^2/2+U_s]/C,
 F=nv[v^2/2+c^2 log(n/nref)+phi]-(pB+Jwk)/C.
Matter plus interaction contributes +np; Q contributes -np-Tw/C; scale
contributes +Tw/C. Thus E_t+F_x=0 in the proved classical class. Moving
endpoints retain F(alpha)-F(beta)+beta'E(beta)-alpha'E(alpha). Nothing here
asserts conservation of the shrinking-cone integral. The zero-velocity control
is the exact hydrostatic tuple on the physical patch; uniqueness gives it.
Small initial energy plays no role in the regularity argument.

## Failed routes and exact scope

Rejected estimate 1: a separate rectangular amplitude box for the unscaled
Riemann invariants gives q=O(V/c), hence an exponential-in-N density bound.
Rejected estimate 2: using the unchanged finite-N coefficient-cutoff constants
without their N dependence does not establish a uniform time.
Rejected estimate 3: uniform first derivatives alone do not justify C1 restart
unless derivative-Lipschitz control and the time trace are supplied.
Rejected estimate 4: a formal force time jet cannot bound feedback on a full
interval; the integral estimates above refer to actual constructed fields.
These are failures of estimates, not counterexamples to existence.

No new external theorem, mechanism, computation or empirical source was used.
Both a0=9.3619e-11 and 1.1279e-10 are separate positive fixed backgrounds.
Constant vacuum and each frozen a0 E(z), E^2=.315(1+z)^3+.685, are distinct.
One can take the minimum of kappa for the two specified backgrounds; no
uniformity over unbounded frozen redshift is claimed. Evolving reference/H
would have protocol work and is excluded. Q, RAR, registered M and filtered
MONO remain distinct. This diagnostic scale dynamics proves no metric/photon
completion, two-DOF result, criterion B, cluster evidence, novelty or closure.

Pre-exposure verdict: the uniform early-time gate is derivable by this route.
The forthcoming audit must verify the author's actual inequalities and restart
argument, not accept them merely because a related route is available. No
remaining gap in this independent route is presently identified; all constants
are conservative analytic sup bounds, not numerical values or optimized rates.
Proofread self-review: exact profile and mathematical tokens retained; no
external manuscript edited; no computation/LaTeX compilation needed.
