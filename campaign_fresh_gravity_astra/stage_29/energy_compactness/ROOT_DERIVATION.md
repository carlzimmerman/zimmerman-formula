# FGF042: exact small-energy control in unweighted norms

Root analytic derivation frozen before new FGF042 author/reviewer proof or
formula previews. Common task suggested retaining exact convexity; the
calculations below are independently reconstructed. No mathematical executable,
external mechanism or parameter scan. Inherited FGF039 equality correction
applies: ZERO excess energy, not saturation of a lower bound, selects background.

## Fixed domain and complete energy

Fix one reviewed Q crossing restricted to I=(-d,d), length ell, with all
physical coefficients fixed: C=4piG, tau,sigma,J,S0,cs²>0. Write rho>0,
phi0,chi0 for the static solution, g=phi0', a=a_ref exp chi0, B'=C rho,
e'(rho)+phi0=constant, -J chi0''+U'-T=0. Here
B(g,a)=sgn(g)(sqrt(a²+4g²)-a)/2, W_g=B,
A(g,a)=2|g|/sqrt(a²+4g²), T=-W_chi,
e(n)=cs² n[log(n/rho_ref)-1], e(0)=0,
U(chi)=S0[cosh(2chi)-1]/4.
The only A zero is the crossing and R=integral 1/A is finite. Backgrounds
are bounded, rho and a bounded positive, and A~constant sqrt(|x|) at the
crossing. Shrinking I restricts the same solution, not its physical couplings.

Comparison states: n>=0 of fixed mass M=integral rho and finite entropy,
psi=phi-phi0, eta=chi-chi0 in H1_0(I), ||eta||infinity<=delta=1/4;
field velocities u=phi_t,w=chi_t in L2 and matter current j with j²/n integrable.
At vacuum require j=0, define j²/n=0; otherwise nonzero j on vacuum gives
infinite energy and is excluded. No density pointwise cap. These are comparison
states, not necessarily solutions. Put h=psi', a'=a exp eta.

Define D_a(g,h)=W(g+h,a)-W(g,a)-B(g,a)h. Signed-gradient W is understood.
The full relative total energy is kinetic plus the exact static remainder:

mathcalE=K+G[n,psi]+(1/C) integral[Frel+J eta'^2/2+Urel],
K=integral j²/(2n)+(1/(2C))integral(tau u²+sigma w²),
G=cs²D(n||rho)+integral(n-rho)psi,
Frel=W(g+h,a')-W(g,a)-B(g,a)h+T(g,a)eta,
Urel=U(chi0+eta)-U(chi0)-U'(chi0)eta.

D(n||q)=integral[n log(n/q)-n+q]. All linear cancellations use static
B'=C rho, hydrostatic constant times zero mass variation and the scale equation
with both zero field traces. The n phi interaction has not been dropped; its
finite remainder is in G. Actual evolving source is B_x=Cn+tau u_t, and
comparison states are not required to satisfy a false static source constraint.

## Retain exact field convexity after all couplings

Let k=exp(-delta)/64. The inherited global signed Q inequality and scale
comparison give D_a'(g,h)>=k A(g,a)h² for every finite h and |eta|<=delta.
Define at background g,a
qcap(x)=sup_|theta|<=delta |B_chi(g,a exp theta)|,
Kcap=sup_(x,theta) |W_chichi(g,a exp theta)|,
Lcap=sup_x qcap²/A, with its continuous zero value at the center.

Decompose exactly
Frel=D_a'(g,h)+[B(g,a')-B(g,a)]h
              +W(g,a')-W(g,a)+T(g,a)eta.
The last two terms are >=-qcap|h eta|-Kcap eta²/2. Split the first term
into two halves, bounding only one. Young's elementary square gives
qcap|h eta| <=(k/4)A h²+qcap² eta²/(k A).
At A=0, qcap=0 and this extends continuously. Hence

Frel >= D_a'(g,h)/2+(k/4)A h²-(Lcap/k+Kcap/2)eta².

Since U''>=S0, impose the sufficient scale gate

Lcap/k+Kcap/2 <= S0/4.                                      (G1)

For the matter minimizer mpsi=rho exp(-psi/cs²)/Z,
Z=(1/M)integral rho exp(-psi/cs²), the exact FGF039 identity is
G=cs²D(n||mpsi)-M cs² log Z-integral rho psi.
Its last two terms are >=-M(osc psi)²/(8cs²); this follows by integrating
the bounded tilted variance, not by truncating the exponential. Weighted
Cauchy gives (osc psi)²<=R integral A h². Impose

alpha=C M R/(8cs²) <= k/8.                                 (G2)

Combining ALL terms proves

mathcalE >= K+cs²D(n||mpsi)+(1/(2C))integral D_a'(g,h)
             +(k/(8C))integral A h²
             +(J/(2C))integral eta'^2+(S0/(4C))integral eta². (1)

This is a full finite-increment inequality with no h-amplitude restriction.
G1 and G2 are stronger sufficient hypotheses, not consequences assumed from
older constants. They are nonempty on short restrictions of the SAME crossing:
qcap=O(|g|²), W_chichi=O(|g|³), A~constant |g|,
so Lcap,Kcap=O(d^(3/2)); M=O(d), R=O(sqrt(d)), alpha=O(d^(3/2)).
Coefficients and central data are not retuned. Mass/walls are induced once for
the selected interval and then fixed in all comparisons. No physical radius
or common observational size for the two a0 backgrounds is asserted.

## An increment-sensitive bound, including a zero background gradient

For every signed g,h and a'>0 the integral Taylor identity is
D_a'(g,h)=h² integral_0^1 (1-t) A(g+t h,a') dt.
If |g|>=|h|/2, then for t in[0,1/4], |g+t h|>=|h|/4.
If |g|<|h|/2, then for t in[3/4,1], |g+t h|>=|h|/4.
Monotonicity of A in absolute gradient and the respective integrals7/32 and
1/32 prove the UNIFORM bound

D_a'(g,h) >= h² A(|h|/4,a')/32.                            (2)

For h=0 this is trivial. Set amax=exp(delta) sup_I a. Because A decreases
with a, fix any threshold r>0 with acceleration units. Splitting |h|<=r
and |h|>r, (1),(2) yield

||h||_2² <= ell r² + 32 integral D_a'(g,h)/A(r/4,amax)
          <= ell r² + 64 C mathcalE/A(r/4,amax).            (3)

For a sequence mathcalE_m->0, first fix r, take the limsup, then let r->0.
Thus h_m->0 strongly in UNWEIGHTED L2. No positive constant quadratic
Hessian at the center was presumed. Indeed D_a(0,h)=W(h,a)~|h|³/(3a),
so D_a(0,h)/h²->0; a global positive pointwise quadratic constant is false.
The split estimate provides a nonlinear modulus without making that assertion.
All terms in (3) have acceleration-squared times length units; r is not a
hidden dimensionless physical cutoff. A numerical optimization is unnecessary.

## Other strong limits, including entropy and vacuum

Inequality(1) also gives ||u||²<=2C mathcalE/tau,
||w||²<=2C mathcalE/sigma, ||eta'||²<=2C mathcalE/J,
and ||eta||²<=4C mathcalE/S0. With fixed zero traces,
||eta||infinity²<=ell ||eta'||²/4, so a'->a uniformly.
Weighted control gives ||psi||infinity<=osc psi<=sqrt(8 C R mathcalE/k).
The unweighted derivative limit also gives the ordinary H1 convergence.

Exact entropy satisfies D(n||mpsi)<=mathcalE/cs² and the already derived
bound ||n-mpsi||1²<=4M D(n||mpsi), valid for n>=0 including vacuum.
Furthermore |log(mpsi/rho)|<=osc psi/cs², giving
||mpsi-rho||1<=M[exp(osc psi/cs²)-1]. Thus n->rho strongly in L1.
Returning the entropy reference uses the EXACT identity, by equal masses,

D(n||rho)=D(n||mpsi)+integral n log(mpsi/rho).

It follows 0<=D(n||rho)<=D(n||mpsi)+M osc psi/cs²->0. This is additional
information beyond mere density L1 convergence. Pointwise convexity gives

||e(n)-e(rho)||1 <= cs²D(n||rho)
                       +||e'(rho)||infinity ||n-rho||1 ->0.

Let r_n=sqrt(n), z_n=j/sqrt(n), with z_n=0 on vacuum. Then
||r_n-sqrt(rho)||²<=||n-rho||1->0 and ||z_n||²<=2mathcalE->0.
Thus the limiting velocity-weighted current is zero; it cannot retain a
nonzero hidden kinetic contribution on limiting vacuum. Also
||j||1<=sqrt(M)||z_n||2->0 and ||j²/n||1=||z_n||²->0.
No pointwise density positivity is concluded. The FGF039 vacuum-hole example
still has arbitrarily small energy and is consistent with all these norms.

## Identified currents and the remaining energy-flux gap

Strong L2 of g+h,u,chi0'+eta',w and uniform scale convergence identify
quadratic field terms in L1. B has |B_g|<=1, |B_a|<=1/2, so B(g+h,a')->B(g,a)
strongly in L2. W differences obey the integrated gradient-growth estimate
|W(g1,a)-W(g2,a)|<=(|g1|+|g2|)|g1-g2| and |W_a|=T/a<=|g|/2;
therefore W converges in L1. U converges uniformly. The n phi interaction
converges in L1 since phi converges uniformly and n in L1 with fixed mass.

Consequently the FULL combined momentum and stress
P=j-(tau u(g+h)+sigma w(chi0'+eta'))/C,
Pi=j²/n+cs²n+[B(g+h)-W+tau u²/2+sigma w²/2
                         +J(chi0'+eta')²/2-U]/C
converge strongly in L1 to their background expressions. Here B(g+h)
in Pi means B(g+h,a') multiplied by g+h. The full energy DENSITY also
converges strongly in L1, since every kinetic, internal, interaction and
field term has just been controlled. Hence the FGF041 nonzero momentum,
stress and energy-density concentrations are excluded in this changed class.

The field part of energy flux -[uB+Jw(chi0'+eta')]/C converges strongly in L1.
The general fluid flux j[(j/n)²/2+e'(n)+phi] contains cubic velocity and
velocity-times-entropy factors not controlled by these estimates. No convergence
of that FULL energy flux is claimed, nor passage to a local energy equation.
Energy density and its transported flux are distinct obligations. Likewise
no assertion is made that n(g+h) is locally integrable for every comparison;
FGF040's force-domain obstruction at arbitrarily small energy remains valid.

## Conditional time conclusion, controls, exact limits

Suppose trajectories ALREADY EXIST on[0,T] with the above finite-action/mass/
wall/vacuum/entropy hypotheses, eta continuous in H1 in time, and the assumed
global full relative energy inequality mathcalE(t)<=mathcalE(0). Start strictly
inside the scale cap. Inequality(1) gives, while ||eta||infinity<=delta,
mathcalE>=2J ||eta||infinity²/(C ell), hence the exit cost
Ebar=2J delta²/(C ell)=J/(8 C ell). If initial excess<Ebar, a first cap
hitting time contradicts the inequality. These statements require the energy
inequality at that hitting time (or sufficient limiting lower continuity);
we assume it for all represented times. An a.e.-time bound with no trace
information is not silently upgraded to that assumption.

For such a sequence with mathcalE_m(0)->0 and initially inside the cap, all
estimates hold uniformly in t throughout the already-existing common interval.
Equation(3) then gives uniform-in-time strong L2 convergence; the other bounds
similarly give the listed uniform spatial norms and their spacetime versions.
This supplies neither those trajectories nor their energy inequality, traces,
regularity persistence or continuation beyond their known lifetime. It concerns
vanishing excess about this STATIC reference, not arbitrary two solutions or
bounded nonzero perturbation energies.

Fixed density/scale control: the exact energy reduces to K+integral D_a(g,h)/C,
by signed background source cancellation. Formula(2) directly implies the same
unweighted convergence; matter minimization has not weakened that conclusion.
FGF041's main packet has excess tending to E*>0, so fails the new premise;
its vanishing-amplitude control has excess->0 and strong derivatives as required.
No packet or exponent scan is repeated. FGF037 weighted upper/Taylor failure
survives: this is a one-way exact energy-to-norm bound, not norm-to-energy
continuity or uniform quadratic comparability.

Both a_ref=9.3619e-11 and1.1279e-10 m/s² apply separately to their backgrounds.
Constant-vacuum and frozen a(0)E(z), E²=.315(1+z)^3+.685, are fixed-reference
comparisons; evolving-H work still needs its reservoir and does not inherit
this inequality without that accounting. Responsive scale and positive inertias
are diagnostic assumptions. Signed MOND Q source is retained; no RAR/M/filtered-
MONO, physical metric/photon/DOF, instrument-calibrated evidence or theory closure.
The next missing implication is a defensible approximation/evolution mechanism
with the required energy inequality and flux regularity, not another coefficient
sweep within this static estimate.
