# Density-cap removal by exact constrained entropy

2026-09-30 20:31 UTC pass. Root proof frozen before new author/reviewer proof
or previews. Task039 proposes exact density elimination; no new numerical run
or imported mechanism. Inherit the reviewed Q crossing and energy from FGF038.
C=4piG, cs²,J,S0,a_ref are fixed positive physical coefficients. On one fixed
short restriction I of length ell, rho>0, M=integral rho, g=phi', a=a_ref exp chi,
B'=C rho, e'(rho)+phi=mu, -J chi''+U'-T=0. The actual static Q source is used.
Here e(n)=cs² n(log(n/rho_ref)-1), e(0)=0, U=S0(cosh(2chi)-1)/4,
B=sgn(g)(sqrt(a²+4g²)-a)/2, W_s=b, A=2|g|/sqrt(a²+4g²).

Allow any measurable n>=0 with integral n=M and finite relative entropy to
rho, and psi,eta in H1_0(I) with |eta|<=d=1/4. No density cap is imposed.
All static energy terms are finite: n log n is integrable on this finite
interval relative to bounded positive rho, psi is bounded, a exp eta is
bounded positive and potential gradients are L2. This comparison includes
vacuum sets but asserts no classical fluid dynamics on such sets.

## Exact density minimizer, including zero-density competitors

Let p=rho/M be a probability density, angle brackets its integral, and
Z=<exp(-psi/cs²)>, m_psi=rho exp(-psi/cs²)/Z. Since psi is bounded, Z is
finite strictly positive and m_psi is bounded strictly positive, with mass M.
Exact algebra, using mass equality and 0 log 0=0, gives

G[n,psi]=integral{e(n)-e(rho)-e'(rho)(n-rho)+(n-rho)psi}
 =cs² D(n||m_psi) - M cs² log Z - integral rho psi,           (1)
D(n||m)=integral[n log(n/m)-n+m].

The function f(z)=z log z-z+1 satisfies f>=0 for z>=0, with equality only
at z=1, by f'=log z, f''=1/z>0 and the limit f(0)=1. Thus D>=0, with
D=0 only for n=m a.e. Equation (1) proves existence and uniqueness of the
constrained minimizer m_psi without a compactness or differentiability
assumption on the set of densities. Its logarithm differs from log rho by
bounded terms, so finite relative entropy is preserved. This is the inherited
isothermal matter law, not an added matter species.

Put X=(psi-<psi>)/cs². The minimum equals -M cs² log<exp(-X)>.
For F(t)=log<exp(-t X)>, bounded X justifies differentiation:
F(0)=F'(0)=0 and F''(t)=Var_t(X), where the tilted positive probability is
proportional to exp(-t X)p. If X lies between L and U, then
Var_t(X)<=E_t[(X-(L+U)/2)²]<=(U-L)²/4. Integration from 0 to1 yields

0<=log<exp(-X)><=(osc psi)²/(8cs^4).                         (2)

The lower inequality also follows by exp y>=1+y and <X>=0. This is a direct
bounded-variable proof, not an invocation of an external statistical theorem.
Together (1),(2) give G>=cs²D(n||m_psi)-M(osc psi)²/(8cs²).
The negative functional bound is global in psi amplitude.

## Complete field/scale coupling and shortness

All first variations of the full energy cancel exactly as in FGF038: the
hydrostatic multiplier times n-rho integrates to zero, B psi'/C cancels
rho psi, and the scale gradient first variation cancels (U'-T)eta/C.
The retained matter remainder is precisely (1). There is no uncanceled
n-phi interaction: it is inside G, not omitted by minimization.

Use the root FGF038 exact field/scale bound with k=exp(-d)/64. With
qcap(x)=sup_|theta|<=d |B_chi(g,a exp theta)|,
K=sup_(x,theta)|W_chichi(|g|,a exp theta)|,
Lcap=sup_x qcap²/A (continuous zero value at the crossing), impose

K+Lcap/k <= S0/2.                                          (3)

Then the exact tangent-subtracted field, scale gradient and U contributions
are at least
(k/2) A psi'^2 + (J/2)eta'^2+(S0/4)eta², divided by C.
This is global in psi', retains finite scale coupling, and uses Taylor
integration only in bounded eta at the BACKGROUND gradient. Its signed Q
scalar bound is D_a(g,h)>=A(g,a)h²/64. FGF037's failed upper/Taylor
implication is not used. The old density cap played no role in this field bound.

Let R=integral_I 1/A, E_A=integral A psi'^2. For any x,y, weighted
Cauchy-Schwarz gives |psi(x)-psi(y)|²<=R E_A, hence (osc psi)²<=R E_A.
Choose the second sufficient gate

C M R/(8cs²) <= k/4.                                      (4)

Equations (1)-(4) prove, for EVERY density and field in the enlarged class,

DeltaE >= cs²D(n||m_psi) + k E_A/(4C)
                   + J integral eta'^2/(2C)
                   + S0 integral eta²/(4C).                (5)

This is an exact static inequality. On shortening the SAME central solution,
M=O(ell), R=O(sqrt(ell)), K->0, Lcap->0, so both gates hold without any
retuning. Coefficients/central data are fixed; interval restriction changes
induced walls and mass. No numerical or astrophysical interval size is given.
Each term has energy per transverse area units; CMR/cs² is dimensionless.
Equality forces eta=0, psi=0 from traces/A>0 a.e., and n=m_0=rho. Thus a
strict energetic minimum persists without either upper or lower density cap,
including finite-entropy nonnegative densities. The scale cap is still used.

## A proved density distance and its reference

The entropy in (5) is relative to m_psi, not directly rho. A conservative
L1 estimate can be derived without quoting a named inequality. Taylor's
integral formula for f(z) gives f(z)>=(z-1)²/(2 max(1,z)) for z>0; its
limit at0 preserves the bound. Consequently

D(n||m)>= (1/2)integral (n-m)²/(n+m)
        >= ||n-m||_1²/(4M).                               (6)

The last step is Cauchy-Schwarz and integral(n+m)=2M. All denominators are
positive since m=m_psi>0. The constant is sufficient, not sharp. Equations
(5),(6) control ||n-m_psi||_1; they do not supply a pointwise density bound.

For conversion to the original density, exp(-osc psi/cs²)<=m_psi/rho
<=exp(osc psi/cs²), giving ||m_psi-rho||_1<=M[exp(osc psi/cs²)-1].
If DeltaE<=E while the class/gates hold, then

||n-rho||_1 <= sqrt(4M E/cs²)
 +M[exp(sqrt(4 C R E/k)/cs²)-1].                            (7)

This tends to zero with E for the fixed background interval. It is neither
an L-infinity estimate nor a no-vacuum theorem. Replacing E by the conserved
TOTAL excess energy is valid only when kinetic energy is nonnegative and
an appropriate conservative trajectory already exists.

## Explicit failure of a density pointwise energy barrier

Choose an interior point away from the cusp and a disjoint compact interior
region. Let f_epsilon be a smooth nonnegative bump, equal to1 on a smaller
interval, at most1, supported in width O(epsilon) about the point. Let j be
a fixed smooth nonnegative unit-integral bump in the disjoint region.
For alpha=3/4 define

m_epsilon=alpha integral rho f_epsilon=O(epsilon),
n_epsilon=rho(1-alpha f_epsilon)+m_epsilon j,
psi=eta=0.

This density is positive, finite entropy and exactly mass M. On the plateau
n_epsilon=rho/4, violating the old half-density cap. Since all fields are
unchanged and the hydrostatic first variation is zero at fixed mass,
DeltaE=cs² integral rho f(n_epsilon/rho). On the depletion support f is
uniformly bounded, so its contribution is O(epsilon). On the compensating
support n_epsilon/rho=1+O(epsilon), with rho bounded away from zero, hence
f=O(epsilon²) by bounded local curvature. Everywhere else f=0. Therefore
DeltaE=O(epsilon)->0 despite a fixed pointwise cap violation.

Taking alpha=1 instead gives an actual vacuum plateau and the same finite
O(epsilon) energy, using f(0)=1. This is an admissible energy-comparison
family, not a claim that a positive classical solution creates vacuum or
reaches it dynamically. It disproves a positive energy threshold that alone
would enforce the old density cap or strictly positive density.

## A scale barrier, only conditional on evolution

For eta in H1_0 and x at distances a_x,b_x from the two walls,
integral eta'^2 >= eta(x)²(1/a_x+1/b_x)>=4eta(x)²/ell,
by Cauchy-Schwarz separately on the two subintervals. Taking the supremum,
(5) yields at scale-cap equality ||eta||infinity=d the barrier

DeltaE >= E_bar=2J d²/(C ell)=J/(8 C ell), d=1/4.           (8)

Consider an ALREADY EXISTING trajectory with fixed reference/impermeable walls,
fixed mass, nonnegative finite-entropy density, finite-action fields, eta
continuous in H1 in time, and conserved total excess energy mathcalE, with
nonnegative kinetic energy integral[n v²+(tau phi_t²+sigma chi_t²)/C]/2.
If initially ||eta||infinity<d and mathcalE<E_bar, a first time at cap equality
would satisfy (5),(8), contradicting conservation and kinetic positivity.
This precludes scale-cap exit for as long as these independent trajectory
hypotheses hold. It cannot bootstrap missing existence, uniqueness, retention
of H1/entropy, weak energy equality, density smoothness or no-vacuum.

Only the BACKGROUND obeys static B'=C rho in the energy cancellation. For
an actual dynamical state, the inherited equation is
partial_x B= C n+tau phi_tt; arbitrary comparison n and psi are not required
to solve the static source law. Static energy alone is not assumed conserved.
Fixed field walls remove field energy flux and impermeability removes matter
flux if the equations and traces justify the conservation calculation; such
regularity for nonlinear crossing evolution is not constructed here.

Both a0=9.3619e-11 and1.1279e-10 m/s² apply separately to their own backgrounds.
Constant-vacuum reference, frozen a0 E(z) with E²=.315(1+z)^3+.685, and actually
evolving-H cases stay distinct. Evolving reference work requires a physical
reservoir. Locally responsive scale remains an added diagnostic assumption.
No RAR/M/filtered-MONO, metric/photon/DOF, instrument-calibrated evidence,
historical novelty, full nonlinear stability or theory closure follows.
