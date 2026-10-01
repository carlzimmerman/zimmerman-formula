# FGF041: a traveling concentration with weakly vanishing actual residuals

Proof-only worker derivation fixed before new root/reviewer proof or previews.
One analytic packet family, not exact solutions or a parameter scan. Its initial
energy defect is explicit. The action remains the fixed-reference Q diagnostic
model, with C=4piG and positive constant tau,sigma,J,cs²,S0.

## 1. Actual background, units, support and speed

Fix the reviewed static crossing (rho,phi0,chi0) on I=(-d,d), with signed
B0'=C rho, cs²rho'=−rho g0, g0=phi0', and J chi0''=U'−T0. Choose a compact
interval J strictly within the positive regular side (0,d). Choose x0 and a
finite time slab [0,T] so that X(t)=x0+c_tau t stays strictly inside J,
where

 c_tau=1/sqrt(tau).

This speed comes from the actual potential inertia and the exact Q
high-gradient slope1; it is not inserted as a metric light speed. If
tau=K/c², it equals c/sqrt(K) in that convention, with K still an added input.
Fix reference length L>0 and potential unit Psi>0. Choose one fixed smooth
nonzero f compactly supported in (−1,1), with I_f=integral f'²>0. For all
sufficiently small dimensionless epsilon, define

 psi_e=Psi sqrt(epsilon) f((x−X(t))/(L epsilon)),
 p_e=partial_x psi_e=(Psi/L)epsilon^(−1/2) f',
 partial_t psi_e=−c_tau p_e.                         (1)

The support lies inside J and away from the crossing/walls for the whole slab.
Set n_e=rho, j_e=0, chi_e=chi0, phi_e=phi0+psi_e. Mass, scale cap and fixed
field walls are exactly unchanged. The background is not globally H2 at the
crossing, but it is unchanged there; all packet calculations occur on the
smooth regular side, and background weak identities apply elsewhere.

Potential amplitude tends to zero uniformly. The exact identities

 tau psi_e,tt=psi_e,xx,
 integral p_e² dx=(Psi²/L)I_f=:S_*,
 ||p_e||_L1=O(sqrt(epsilon)), ||psi_e||_L2=O(epsilon)

hold uniformly in t. Both p_e and psi_e,t converge weakly to0 in L2, at each
time and in spacetime: their supports shrink, so testing against L2 functions
uses absolute continuity of the test's squared integral. They do not converge
strongly in L2. In particular the initial kinetic/gradient data are not strongly
convergent to the background.

## 2. Exact Q high-gradient bounds and residual conventions

For signed G and the unchanged bounded positive scale a(x), write

 B(G,a)=G+R_B(G,a), |R_B|<=a/2,
 W(|G|,a)=G²/2+R_W(G,a), |R_W|<=a|G|/2,
 S(G,a)=B(G,a)G−W(|G|,a)=G²/2+R_S(G,a),
 |R_S|<=a|G|.

These are global exact inequalities obtained directly from Q, not a deep-field
expansion. The differences Delta R_B,R_W,R_S below compare G=g0+p_e to g0
at the same x. They vanish outside packet support. Consequently

 ||Delta R_B||_L1=O(epsilon), ||Delta R_B||_L2=O(sqrt(epsilon)),
 ||Delta R_W||_L1+||Delta R_S||_L1=O(sqrt(epsilon)).    (2)

Also T_s=q<=a/2 gives ||T_e−T0||_L1=O(sqrt(epsilon)).
All estimates are uniform in t. Background coefficients and derivatives
appearing with the packet are bounded on J.

Residual signs are defined as the left sides of

 R_mass=n_t+j_x,
 R_phi=tau phi_tt−B_x+C n,
 R_chi=sigma chi_tt−J chi_xx+U'−T,
 R_m=j_t+(j²/n+cs² n)_x+n phi_x,
 R_comb=P_t+Pi_x.

Let ||R||_(Lip*) mean the supremum of its distributional pairing against
compactly supported spatial tests with ||zeta||infinity+||zeta'||infinity<=1.
This is a declared weak norm, not an L1 norm for a derivative distribution.
An expression f+partial_x F with f,F in L1 has Lip* norm at most
||f||_1+||F||_1. Spacetime distributional statements use compact tests with
bounded first time/space derivatives on the fixed slab.

## 3. Every actual equation residual

Mass residual is exactly zero. The dynamic Q source residual is exactly

 R_phi=−partial_x Delta R_B,

because tau psi_tt=p_e,x. It tends to0 in L-infinity-in-time H^-1(I) with
norm O(sqrt(epsilon)), and in the stated spatial Lip* norm with O(epsilon).
The unchanged background signed MOND flux, not a Newtonian source equation,
is canceled here. We do not impose the false static condition B_e,x=C rho.

The scale residual is R_chi=T0−T_e, tending to0 in L-infinity-in-time L1(I)
with O(sqrt(epsilon)). No scale adjustment is needed for this particular weak
residual statement. It is generally nonzero at finite epsilon.

Separate matter momentum is well-defined for every member, since density is
the bounded background. Its residual is

 R_m=rho p_e,

which tends to0 in L-infinity-in-time L1(I) as O(sqrt(epsilon)). Its L2 norm
need not tend to zero. Thus these are approximate states only in the declared
weak norms, not a claim of accurate strong-force balance.

The FULL combined momentum from FGF040 is

 P=j−(tau phi_t phi_x+sigma chi_t chi_x)/C,
 Pi=j²/n+cs²n+[tau phi_t²/2+sigma chi_t²/2
                          +B phi_x−W+J chi_x²/2−U]/C.

The background has P0=0 and distributionally constant Pi0. Direct substitution
of (1), using tau c_tau²=1, gives exactly

 P_e=(tau c_tau/C)(p_e²+g0 p_e),
 Pi_e−Pi0=(1/C)(p_e²+g0 p_e+Delta R_S).             (3)

The leading packet pair is conserved because p_e² travels at c_tau. The
remaining terms give the exact identity

 C R_comb=g0' p_e+partial_x Delta R_S.               (4)

Indeed partial_t(g0 p_e)=−c_tau partial_x(g0 p_e)+c_tau g0' p_e,
so the two derivative cross terms cancel. Equation (4) tends to0 in
L-infinity-in-time Lip* as O(sqrt(epsilon)), and hence in spacetime
distributions. We do not infer this merely by multiplying R_phi by the large
packet gradient: such a product is not controlled by the H^-1 residual norm.
The direct stress calculation is essential. No strong combined-residual norm
beyond the displayed one is claimed.

## 4. Fields, momentum and energy limits

The current fields converge to the background: n,j,chi are unchanged,
phi_e converges uniformly, phi_e,x and phi_e,t converge weakly in L2.
B_e−B0=p_e+Delta R_B tends strongly to0 in L1 and weakly in L2.
T_e−T0 tends to0 in L1. These limits satisfy the background equations.
But the quadratic packet has, at each time and as a spacetime measure,

 (p_e²/C) dx -> E_* delta_(X(t)),
 E_*=Psi² I_f/(C L)>0.                              (5)

For a continuous test this follows by x=X(t)+L epsilon y and ordinary
dominated convergence over fixed compact y support. The bounds (2) remove
all the lower-order stress terms in (3). Therefore

 P_e dx -> (tau c_tau E_*)delta_X=(E_*/c_tau)delta_X,
 (Pi_e−Pi0)dx -> E_* delta_X.                        (6)

These are nonzero moving concentration measures, not the momentum/stress of
the limiting background fields. They obey their own conservation identity
because (E_*/c_tau)c_tau=E_*. Thus weak vanishing of R_comb does not eliminate
the defect.

The full total energy density on this ansatz is

 e_e=e(rho)+rho(phi0+psi_e)
       +[tau phi_e,t²/2+W(|g0+p_e|,a)+J chi0'²/2+U]/C.

All matter and scale contributions are retained. Its exact difference is

 e_e−e0=(1/C)[p_e²+g0 p_e+Delta R_W]+rho psi_e.

The error terms tend to0 in L1 uniformly in time, so

 (e_e−e0)dx -> E_* delta_X.                          (7)

The inherited full energy flux on this state has zero fluid and scale-velocity
parts and is S_e=−phi_e,t B_e/C. Thus

 S_e=(c_tau/C)p_e²+L1 error of order sqrt(epsilon),
 S_e dx -> c_tau E_* delta_X.                       (8)

The total energy residual partial_t e_e+partial_x S_e also tends to0 in
spacetime distributions, by (7)-(8) with the leading pair canceled exactly
at finite epsilon and the remainder derivatives tested against bounded
first derivatives. This is weak approximate energy balance, not exact
conservation of each member's total energy.

## 5. Initial energy is not well-prepared

The initial relative energy already tends to E_*>0, concentrated at x0.
At every t the exact integrated difference is

 E_e(t)−E0=(1/C)integral[p_e²/2
                    +W(|g0+p_e|,a)−W(|g0|,a)−B0 p_e].

Here the interaction rho psi_e cancels integral B0 p_e/C by the background
source and zero traces. Since the Q gradient Hessian is between0 and1,

 S_*/(2C)<=E_e(t)−E0<=S_*/C,
 E_e(t)−E0 -> E_* uniformly on the selected time slab.

The nonzero defect is present in the initial energy and momentum measures;
it has not been created from zero energetic data. Uniform convergence of
potentials and weak derivative convergence are not strong initial energy
convergence. This is not a counterexample to exact-solution uniqueness, strong
initial-data convergence or a scheme imposing an appropriate no-defect initial
condition. The boundary fields and mass are fixed exactly, but no exact
nonlinear solution sequence is supplied.

## 6. Explicit vanishing-energy control

Multiply the one packet (1) by sqrt(epsilon):

 psi_e^small=Psi epsilon f((x−X(t))/(L epsilon)).

Its gradient has squared L2 norm epsilon S_* and its time derivative retains
the same traveling relation. The exact integrated energy identity and
0<=Q Hessian<=1 imply

 0<=E_e^small−E0<=epsilon E_* ->0.

The original residual estimates still vanish, and every concentration measure
in (5)-(8) now has zero mass. This is a single amplitude control, not an
exponent scan or a replacement physical coupling. Both derivative and kinetic
initial data converge strongly in L2, unlike the main family.

## 7. What stronger compactness would suffice

In this exact fixed-density, fixed-scale packet class, strong L2 convergence
of phi_x and phi_t on the time slab would identify ALL the displayed nonlinear
momentum and energy densities/fluxes in L1. The Q bound |partial_g B|<=1
gives strong L2 convergence of B. Products such as phi_t phi_x, phi_t B,
B phi_x and phi_t² then converge in L1 by Cauchy-Schwarz. The growth bound
|W(|G1|,a)−W(|G2|,a)|<=(|G1|+|G2|)|G1−G2| gives the same conclusion for W.
Potential interaction converges by uniform potential convergence and fixed rho;
all other matter/scale terms are unchanged. This states a sufficient condition,
not a condition furnished by the weak residual equations.

Convergence in measure of the derivatives together with uniform integrability
of their squares is another sufficient condition for that strong L2 convergence:
split squared differences into the set where the difference is at most a
small threshold and its complement; the former integral is small by its bound,
the latter by convergence in measure and uniform integrability. The current
family converges in measure but fails uniform integrability: each shrinking
packet tube retains a fixed nonzero squared-gradient and kinetic integral.
An L2 bound alone does not exclude this mechanism.

For general varying matter or scale states, the preceding packet-specific
criterion cannot simply be asserted for every flux. One additionally needs
appropriate strong convergence/uniform integrability of matter pressure and
kinetic flux j²/n, internal energy and interaction, the scale derivatives and
potential, and any fluid energy advection flux. In particular kinetic energy
alone does not bound a cubic-velocity advective energy flux. This pass makes
no such general compactness theorem. Passing the coupled nonlinear equations
and their traces simultaneously remains a separate approximation obligation.

## 8. Exact scope and branch bookkeeping

The result refutes one precise implication: uniform finite energy and the
listed vanishing weak residuals, with only weak initial derivative convergence,
do not by themselves identify nonlinear energy/momentum fluxes with those of
the limiting fields. The nonzero initial defect and the chosen weak residual
norms are part of the counterexample. Nothing here refutes a more restrictive
well-designed approximation, exact solutions, a nonlinear energy theorem or
physical gravity. The earlier FGF039 scale barrier is not being invoked to
construct these approximate states or prove a trajectory; eta is simply zero.

Psi is a potential unit, L a length unit and epsilon dimensionless. c_tau has
velocity units, E_* energy per transverse area, and E_*/c_tau momentum per
transverse area. Actual Q high-gradient bounds govern the concentrating core;
the MOND background source is retained. Both a_ref values9.3619e-11 and
1.1279e-10 m/s² are separate hypotheses. Constant-vacuum and frozen-H references
are distinct from an evolving-H prescription and its reservoir/exchange issue.
Responsive scale and tau remain added diagnostic assumptions. No RAR/M transfer,
filtered-MONO/metric/photon/DOF, physical scale reservoir, calibrated empirical
result, imported mechanism, historical novelty or theory closure is established.
