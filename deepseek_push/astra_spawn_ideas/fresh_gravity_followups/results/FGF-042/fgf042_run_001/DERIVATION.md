# FGF042: zero full excess energy gives unweighted compactness

Proof-only derivation fixed before new root/reviewer proof or previews. The
conclusion is at zero excess about one fixed static reference. It is neither
finite-energy weak compactness nor a nonlinear existence theorem.

## 1. Full class, physical action and exact cancellation

Use the SAME reviewed Q central crossing on I=(-d,d), ell=2d. After choosing
d, keep its mass M, induced field walls and all physical coefficients fixed.
Write C=4piG, g=phi', a=a_ref exp chi, A=2|g|/sqrt(a²+4g²), and

 B=sgn(g)(sqrt(a²+4g²)-a)/2, W_s=b,
 T=-a W_a, U=S0[cosh(2chi)-1]/4.

The background obeys B'=C rho, e'(rho)+phi=constant, J chi''=U'-T,
with e(n)=cs² n[log(n/rho_ref)-1], e(0)=0. The positive constants
cs²,J,S0,tau,sigma are inherited diagnostic inputs. The signed dynamic source
is B_x=C n+tau phi_tt, not the static source condition on all comparisons.

Allow n>=0, integral n=M, finite relative entropy, psi,eta in H1_0(I),
||eta||infinity<=1/4, actual fields Phi=phi+psi, X=chi+eta. Allow momentum j
with finite kinetic energy, using j²/n=0 when n=j=0 and +infinity when n=0
but j!=0. Thus finite energy forces j=0 almost everywhere on vacuum. Field
velocities Phi_t and X_t are L2. Put

 K=integral[j²/(2n)+(tau Phi_t²+sigma X_t²)/(2C)].

Define D(n|q)=integral[n log(n/q)-n+q], with0 log0=0, and

 Z=M^-1 integral rho exp(-psi/cs²), q_psi=rho exp(-psi/cs²)/Z.

The FULL relative total energy is exactly

 Erel=K+cs²D(n|q_psi)+Fmin(psi)
        +(1/C)integral[Frel+J eta'²/2+Urel],                    (1)
 Fmin=-M cs² log Z-integral rho psi,
 Frel=W(|g+psi'|,a exp eta)-W(|g|,a)-B psi'+T eta,
 Urel=U(chi+eta)-U(chi)-U'(chi)eta.

This retains every matter, interaction, field, scale and kinetic term. The
mass constraint cancels the constant e'(rho)+phi first variation; signed
MOND source and zero traces cancel integral(B psi'/C+rho psi); the scale
ODE and zero traces cancel integral[J chi'eta'+(U'-T)eta]. No center term
is introduced. Density need not be bounded away from zero or pointwise above.
FGF039's exact entropy minimization applies to this entire class, giving

 Fmin>=-alpha E_p, alpha=C M I_A/(8cs²),
 E_p=C^-1 integral A psi'², I_A=integral 1/A<infinity.           (2)

## 2. Retain exact convex energy while absorbing the cross terms

Let e0=1/4, k=exp(-e0)/64. At each point and z=psi', define the exact
NEW-scale Bregman remainder

 H(x,z,eta)=W(|g+z|,a exp eta)-W(|g|,a exp eta)
                 -B(g,a exp eta)z >=0.

The reviewed global signed Q inequality gives H>=k A z² for all z. Define
qhat=sup_(|theta|<=e0) q(|g|,a exp theta), with q=s A-b, and
Dhat=sup_(|theta|<=e0)|T_chi(|g|,a exp theta)|. The exact finite-scale
split, with its Taylor remainder only at the BACKGROUND gradient, yields

 Frel>=H-qhat|eta z|-Dhat eta²/2
     >=H/2+(k/4)A z²-R2 eta²,
 R2=qhat²/(k A)+Dhat/2.                                      (3)

Indeed retain H/2, bound the other half by k A z²/2, and apply
qhat|eta z|<=k A z²/4+qhat² eta²/(k A). The quotient is set to0 at the
single crossing, where qhat=Dhat=0 and the unsplit convex inequality holds.
The exact potential satisfies Urel>=S0 eta²/2. Define

 E_eta=(J/C)integral eta'², beta2=ell² sup R2/J.

The explicit STRENGTHENED sufficient gates are

 alpha<=k/8, beta2<=1/4.                                    (4)

Combining (1)-(4), with ||eta||_2²<=ell²||eta'||_2², proves

 Erel>=K+cs²D(n|q_psi)+(1/(2C))integral H
        +(k/8)E_p+E_eta/4+(S0/(2C))integral eta².             (5)

This is a uniform finite-state inequality, not a Hessian expansion. It retains
half the exact convex increment. All terms are nonnegative. Zero Erel implies
the reference state and zero kinetic variables; equality in (5) alone is not
claimed to characterize the reference.

The gates are nonempty on restrictions of the SAME central solution:
M=O(d), I_A=O(sqrt(d)), qhat=O(g²), Dhat=O(|g|³), A comparable to sqrt(|x|),
so alpha=O(d^(3/2)), sup R2=O(d^(3/2)), beta2=O(d^(7/2)). The coefficients
are fixed as d shrinks. The induced mass/walls vary across these restrictions,
then are held fixed for every comparison on the selected interval. This is
not a common fixed-mass family across d and no numerical radius is asserted.

## 3. A finite-increment bound that sees the increment itself

For ANY signed background g, signed increment z and positive scale b, the
Q Bregman remainder has the exact integral representation

 H_b(g,z)=z² integral_0^1(1-t) A(|g+t z|,b)dt.

For z!=0, inside t in [0,1/2] the excluded set |g+t z|<|z|/8 has length at
most1/4. Its complement therefore has length at least1/4. On that complement
1-t>=1/2 and A(|g+t z|,b)>=A(|z|/8,b)>=A(|z|,b)/8. Consequently

 H_b(g,z)>=z² A(|z|,b)/64.                                   (6)

For z=0 the same statement is exact. This elementary argument covers sign
changes and arbitrary g and does not assume a positive Hessian at zero.
Let a_* = exp(1/4) max_I a, a fixed physical acceleration. Since a exp eta
<=a_*, (6) gives, uniformly over all admissible eta,

 H(x,z,eta)>=z² [2|z|/sqrt(a_*²+4z²)]/64.                    (7)

Choose any explicit physical threshold h=a_* r, r>0 dimensionless, and split
where |z|<=h and where |z|>h. Equations (5),(7) imply

 ||psi'||_2²<=ell a_*² r²
              +128 C Erel / A_r,
 A_r=2r/sqrt(1+4r²)>0.                                      (8)

Hence Erel_m->0 forces ||psi_m'||_2->0: first hold any r fixed, take limsup,
then let r decrease to0. This is strong UNWEIGHTED convergence. No positive
constant times ||psi'||_2² lower bound for all small increments was needed.
Fixed endpoint values also give ||psi||infinity<=sqrt(ell)||psi'||_2.
Equation (5) directly gives eta'->0, eta->0 uniformly, and Phi_t,X_t->0 in
L2, for fixed positive J,tau,sigma. The background gradient may vanish at the
center throughout; the proof does not remove that degeneracy by assumption.

## 4. Entropy, density, vacuum and kinetic convergence

As psi->0 uniformly, log(q_psi/rho)=-psi/cs²-log Z tends uniformly to0.
Thus q_psi->rho uniformly and in L1. The elementary FGF039 entropy bound

 ||n-q_psi||_1²<=4M D(n|q_psi)

and (5) yield n->rho strongly in L1 without any positive lower bound on n.
Moreover the exact equal-mass identity is

 D(n|rho)=D(n|q_psi)+integral n log(q_psi/rho).

The last integral is bounded in absolute value by M||log(q_psi/rho)||infinity.
Thus D(n|rho)->0 as well. This is an entropy convergence statement, stronger
than merely n->rho in L1. Put h(n,rho)=n log(n/rho)-n+rho>=0. Then

 e(n)-e(rho)=cs² h(n,rho)+e'(rho)(n-rho).

The first term has L1 norm cs²D(n|rho)->0 and e'(rho) is bounded, proving
strong L1 convergence of the internal-energy density itself. Also sqrt(n)
converges strongly in L2 since (sqrt(n)-sqrt(rho))²<=|n-rho|.

K->0 gives ||j/sqrt(n)||_2->0 under the declared zero-on-vacuum convention,
||j||_1<=sqrt(M integral j²/n)->0, and j²/n->0 in L1. This is weighted kinetic
velocity convergence. It is NOT unweighted velocity convergence: velocities
on vacuum are unspecified, and arbitrarily low density supplies no such bound.
The comparison class still admits small vacuum regions; no density cap follows.

## 5. Products controlled and products not controlled

All convergence in this section is relative to the SAME fixed background.
The signed Q B is1-Lipschitz in gradient; its scale derivative at fixed gradient
has magnitude q<=a/2. Thus strong L2 convergence of Phi_x plus eta->0 uniformly
implies B(Phi_x,a exp eta)->B0 strongly in L2. The bound

 |W(|u|,a)-W(|v|,a)|<=(|u|+|v|)|u-v|,
 |partial_chi W(|u|,a)|=T<=a|u|/2

then gives strong L1 convergence of field energy. Products Phi_t Phi_x,
Phi_t B, B Phi_x, Phi_t², X_t X_x, X_t² and X_x² converge in L1 by
Cauchy-Schwarz and the established strong L2 bounds. U(X)->U(chi) uniformly.
Interaction n Phi->rho phi in L1 since n has mass M and Phi->phi uniformly.
Together with Section4, every component of the FULL total-energy DENSITY
converges strongly in L1. Every component of combined momentum density and
stress does too:

 P=j-(tau Phi_t Phi_x+sigma X_t X_x)/C,
 Pi=j²/n+cs² n+[tau Phi_t²/2+sigma X_t²/2
                         +B Phi_x-W+J X_x²/2-U]/C.

In particular no nonzero energy-density/momentum-stress concentration of the
FGF041 type can survive. The field part of the energy flux also converges in
L1, because it consists of Phi_t B and J X_t X_x products divided by C.

The GENERAL MATTER energy flux is different. It contains
j cs² log(n/rho_ref), j Phi, and j³/(2n²), with suitable vacuum definitions.
Neither small integral j²/n nor small entropy controls the cubic kinetic or
enthalpy transport moment. Their integrability/convergence is NOT established.
Similarly strong L1 density and strong L2 gradient do not by themselves control
the separate force product n Phi_x. Combined momentum convergence is not a
new proof of equivalence to separately forced matter momentum. No broad
nonlinear energy-flux or PDE passage-to-the-limit theorem is being asserted.

## 6. Conditional uniform-in-time consequence

Only now suppose already-existing admissible trajectories on a fixed [0,T]
have the fixed mass/physical coefficients/walls, the fixed reference, and an
ASSUMED full relative total-energy inequality Erel(t)<=Erel(0). Suppose their
scale perturbation is continuous in H1 in time, their initial scale norm is
strictly below1/4, and every other finite-energy/entropy/kinetic requirement
above holds during their existing lifetime. Actual wall/source work must be
accounted for in that assumed inequality; it is not derived here.

From the endpoint estimate ||eta||infinity²<=ell integral eta'²/4 and (5),

 Erel>=J||eta||infinity²/(C ell)

inside the cap. The first arrival at ||eta||infinity=1/4 would cost at least
B_scale=J/(16 C ell)>0. If Erel(0)<B_scale, H1 continuity and the closed-cap
estimate rule out such a first arrival on the existing interval. No density
cap is used, and this argument does not extend a solution past its lifetime.

For a sequence strongly prepared in FULL initial energy Erel_m(0)->0,
all sufficiently large m meet this barrier. Then 0<=Erel_m(t)<=Erel_m(0)
uniformly on [0,T]. Every estimate above holds uniformly in t; in particular
(8), followed by its two-limit argument, gives uniform-in-time strong L2
potential-gradient convergence. Scale derivatives/field velocities, entropy,
density and combined momentum/energy DENSITIES have the corresponding uniform
convergence. The assumed trajectories and energy inequality are hypotheses,
not conclusions. Initial/wall traces, existence, uniqueness and general matter
energy-flux regularity remain separate.

## 7. Controls and the surviving failure

At fixed scale and density and with zero velocities, the exact relative energy
is C^-1 integral H_a(g,psi'), so (6)-(8) specialize without any coupling loss.
The FGF041 main packet fails Erel->0 because its explicitly initial defect is
positive. Its vanishing-amplitude control satisfies the new hypothesis; the
present implication agrees with its strong derivative convergence. No packet
calculation or old spike scan is rerun.

Uniform quadratic coercivity at zero gradient remains FALSE. At g=0,
H_a(0,z)=W(|z|,a)=|z|³/(3a)+O(|z|5), so H_a(0,z)/z²->0. The failure can
also be realized after integration on the central crossing: choose a fixed
smooth compact f, a reference length L and acceleration a_*, and
psi_r=a_* L r³ f(x/(L r²)), eta=0,n=rho, all velocities zero. Then z=psi_r'
is O(r), the support has width O(r²), and the background g is O(r) there.
Since A along its gradient segment is O(r), integral H<=O(r) integral z².
Thus no uniform strictly positive quadratic lower coefficient is available
on all arbitrarily small central perturbations. Each has finite action and
fixed outer walls. This does not contradict strong compactness from the
nonquadratic finite-increment bound (7).

## 8. Units, branches and unresolved implication

H,W have acceleration-squared units, H/C is energy density, integrated Erel
is energy per transverse area. D has mass-per-area units; alpha,beta2,k are
dimensionless; r is dimensionless, h=a_*r an acceleration. All kinetic terms
and units are restored, with tau Phi_t² matching gradient-squared units.

The two a_ref footings9.3619e-11 and1.1279e-10 m/s² are separate hypotheses,
each with its own same-solution short-interval gate. Constant-vacuum and frozen
H references a(0)E(z) remain distinct; a genuinely evolving-H prescription
requires its own work/reservoir accounting and does not inherit this fixed-
reference inequality automatically. Responsive scale and its inertias remain
added diagnostic hypotheses, not an established pointwise vacuum relation.
No RAR or M-action transfer, filtered-MONO, physical metric/photon/DOF,
calibrated empirical result, external mechanism, novelty or theory closure.

A specific next obligation is to isolate the smallest additional matter
transport moment that controls the cubic/enthalpy energy flux on an admissible
approximation class, or give one exact small-energy counterexample to that
flux implication. That is distinct from the zero-excess density/stress result
proved here, and from the still-open construction of actual trajectories.
