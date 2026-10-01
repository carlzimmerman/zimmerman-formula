# FGF039: exact entropy elimination without a pointwise density cap

Proof-only worker derivation frozen before any new root/auditor proof. Keep the
same local Q crossing, physical coefficients and fixed-reference action. This
changes the density domain and its distance; it does not repeat or repair the
failed weighted upper/Taylor argument.

## 1. Fixed comparison class and exact full energy identity

Fix an induced interval I=(-d,d), ell=2d, background rho>0, phi, chi,
g=phi', a=a_ref exp chi, mass M=integral rho, and C=4piG. The background
obeys signed Q flux B'=C rho, hydrostatic e'(rho)+phi=constant and
J chi''=U'−T, with e(n)=cs²n[log(n/rho_ref)−1] and e(0)=0.

Allow every measurable n>=0 with integral n=M and finite relative entropy
integral[n log(n/rho)−n+rho], with0 log0 interpreted as0. No pointwise density
cap is imposed. Let psi,eta in H1_0, ||eta||infinity<=1/4, and the new actual
scale be a exp eta. These ordinary H1 fields have bounded potentials/scale
and finite Q field action. The background rho,a are bounded positive on I.

With r=n−rho the exact identity inherited and derived in FGF038 is

 Delta E=F(n,psi)+(1/C)integral[F_rel+J eta'²/2+U_rel],
 F(n,psi)=cs² integral[n log(n/rho)−n+rho]+integral(n−rho)psi,
 F_rel=W(|g+psi'|,a exp eta)−W(|g|,a)−B psi'+T eta,
 U_rel=U(chi+eta)−U(chi)−U'(chi)eta.                  (1)

This remains valid without a density cap: r is L1, e'(rho)+phi is a bounded
constant, psi is bounded, and mass is fixed. The linear terms cancel exactly
by mass, integral B psi'=−C integral rho psi, and the scale equation with
zero traces. It is not an expansion in r. Density is Eulerian; no finite
material-displacement identity is inserted.

## 2. Exact mass-constrained density minimizer

At fixed bounded psi define

 Z=(1/M)integral rho exp(−psi/cs²),
 rho_psi=rho exp(−psi/cs²)/Z.                         (2)

Z is finite and strictly positive, rho_psi>0, and its integral is M. It has
finite relative entropy because rho_psi/rho is bounded above and below.
For any admissible n, direct substitution of
log(rho_psi/rho)=−psi/cs²−log Z gives

 F(n,psi)=cs² D(n|rho_psi)+F_min(psi),
 D(n|q)=integral[n log(n/q)−n+q],
 F_min(psi)=−M cs² log Z−integral rho psi.             (3)

The nonnegative scalar function H(t)=t log t−t+1 has minimum0 uniquely at1
(by H'=log t,H''=1/t and its continuous value H(0)=1). Thus D>=0, with
equality only n=q almost everywhere. Equation (3) proves existence and
uniqueness of the minimizer rho_psi, its normalization and its exact remainder;
no unverified statistical inequality or extra matter species is used. It also
shows why freezing the mass multiplier would give the wrong minimization.

## 3. A global bound on the minimized negative functional

Let psi_min,psi_max be its extrema, Rpsi=psi_max−psi_min, and use the
probability measure rho dx/M. Define

 L(t)=log[(1/M)integral rho exp(−t psi/cs²)], 0<=t<=1.

Boundedness of psi justifies differentiation under the integral. Then
L(0)=0, L'(0)=−<psi>rho/cs², and L''(t)=Var_t(psi)/cs^4, where the tilted
probability is proportional to rho exp(−t psi/cs²). For any probability
supported in [u,v], the pointwise nonnegative product(Y−u)(v−Y) gives
Var(Y)<=(v−mean)(mean−u)<=(v−u)²/4. Hence

 0<=L(1)−L'(0)=integral_0^1(1−t)L''(t)dt
                                       <=Rpsi²/(8cs^4),
 −M Rpsi²/(8cs²)<=F_min(psi)<=0.                     (4)

This global bound holds for arbitrarily large bounded psi. It is not a
small-amplitude exponential truncation. The weighted endpoint inequality
on the fixed crossing gives

 Rpsi²<=I_A integral A psi'², I_A=integral 1/A<infinity,
 E_p=(1/C)integral A psi'².

Take the two points attaining the extrema and apply weighted Cauchy-Schwarz
on the interval between them; its reciprocal-A integral is no greater than
I_A. Combining (3),(4),

 F(n,psi)>=cs² D(n|rho_psi)−alpha E_p,
 alpha=C M I_A/(8cs²).                              (5)

## 4. Combine the exact finite scale response

Retain the reviewed FGF038 constants and coefficient functions, restated here
to specify the exact gate. Put k=exp(−1/4)/64 and, at background |g|,a,

 qhat=sup_(|theta|<=1/4) q(|g|,a exp theta),
 Dhat=sup_(|theta|<=1/4) |T_chi(|g|,a exp theta)|,
 R(x)=qhat²/(2k A)+Dhat/2,

extended by0 at the single crossing. The accepted global signed Q inequality
and finite-scale decomposition give

 F_rel>=(k/2)A psi'²−R(x)eta²,
 U_rel>=S0 eta²/2.                                  (6)

These bounds require only the scale cap and finite-action psi, not a density
cap or a pointwise gradient cap. In the same central solution Rmax=O(d^(3/2)).
Set E_eta=(J/C)integral eta'² and beta=ell²Rmax/J. The endpoint estimate
||eta||_2²<=ell²||eta'||_2² gives the exact full lower bound

 Delta E>=cs²D(n|rho_psi)+(k/2−alpha)E_p
                       +(1/2−beta)E_eta+(S0/(2C))integral eta².

The sufficient gates are

 alpha<=k/4, beta<=1/4.                              (7)

Under them,

 Delta E>=cs²D(n|rho_psi)+(k/4)E_p+E_eta/4
                                  +(S0/(2C))integral eta². (8)

They hold on all sufficiently short restrictions of the SAME central
solution: M=O(d), I_A=O(sqrt(d)), so alpha=O(d^(3/2)); beta=O(d^(7/2)).
All physical coefficients stay fixed. The wall values and mass are induced
for each d and held fixed during that interval's comparisons. No numerical
radius or a shared measured size for the different reference choices is asserted.
Equality in (8) forces psi=eta=0 and n=rho. Thus restricted static energetic
minimality now holds for the whole nonnegative fixed-mass finite-entropy
density class, with the scale cap retained.

## 5. Which density distance is actually controlled

The entropy in (8) is relative to rho_psi, not directly to rho. A useful L1
bound follows elementarily. For t>=0 the integral Taylor formula or its limit
at0 gives

 H(t)>=(t−1)²/[2 max(1,t)]>=(t−1)²/[2(t+1)].

Multiplying by q and integrating, for positive q of mass M and n>=0 of the
same mass,

 D(n|q)>= (1/2)integral (n−q)²/(n+q)
                 >=||n−q||_1²/(4M).                (9)

The second step is Cauchy-Schwarz with integral(n+q)=2M. This does not presume
a positive lower bound for n. The exact energy therefore controls
cs²||n−rho_psi||_1²/(4M).

Conversion to the original background must also account for the potential.
For rho_t=rho exp(−t psi/cs²)/Z(t),
partial_t rho_t=−rho_t(psi−<psi>t)/cs². Integrating its L1 norm yields

 ||rho_psi−rho||_1<=M Rpsi/cs²
                        <=(M/cs²)sqrt(C I_A E_p).   (10)

The first bound is global (it may exceed the trivial bound2M). Triangle and
square inequalities combined with (9),(10) imply

 ||n−rho||_1²<=8M D(n|rho_psi)+2M² C I_A E_p/cs^4
                  <=K_rho Delta E,
 K_rho=max{8M/cs², 8M² C I_A/(k cs^4)}.             (11)

Thus an original-background L1 distance is controlled as well, with its stated
constant and potential contribution. No pointwise density bound or fixed
quadratic integral(n−rho)²/rho is inferred from entropy/L1 alone.

## 6. No positive barrier for the old pointwise density cap

Choose shrinking subintervals J_epsilon inside I and put
m_epsilon=integral_J_epsilon rho, with0<m_epsilon<M and m_epsilon->0.
Define one explicit fixed-mass family

 n_epsilon=0 on J_epsilon,
 n_epsilon=[M/(M−m_epsilon)]rho outside J_epsilon,
 psi=eta=0.                                         (12)

It is nonnegative, has mass M, finite entropy and finite exact action. It
violates the old lower pointwise half-cap throughout J_epsilon, and has a
small compensating density increase elsewhere. No density gradient energy
exists in this inherited isothermal action, so these measurable comparison
profiles are admissible. They are not claimed equilibrium profiles or solutions.
Its exact energy is

 Delta E=cs²D(n_epsilon|rho)
       =cs² M log[M/(M−m_epsilon)] ->0.              (13)

The source-potential interaction is correctly included: the hydrostatic
first variation is a constant times the zero total mass change. The unchanged
potential need not statically solve the source equation for n_epsilon. In the
inherited dynamic potential theory the actual source relation is
P_x=C n+tau phi_tt; no static constraint is silently imposed on arbitrary
finite-energy initial configurations. No existence theorem for their evolution
is implied. The family proves that exact energy conservation alone cannot
bootstrap the old density pointwise cap or a no-vacuum condition.

## 7. A separate conditional scale barrier

For eta in H1_0 on length ell, integrate its derivative from both ends. At a
point with left/right distances l and ell−l,

 integral eta'² >= |eta(x)|²(1/l+1/(ell−l))
                       >=4|eta(x)|²/ell.

Hence ||eta||infinity²<=ell integral eta'²/4. Equation (8) gives

 Delta E>=J||eta||infinity²/(C ell).

Reaching ||eta||infinity=1/4 therefore costs at least

 B_scale=J/(16 C ell)>0.                            (14)

No pointwise density cap is required for this bound. Now suppose, additionally,
an already existing nonlinear trajectory has fixed-reference energy conservation,
fixed physical field walls, impermeable matter walls, fixed mass, nonnegative
finite-entropy density, finite-action fields, and is continuous in H1 for eta.
Its kinetic terms are the inherited nonnegative ones:
integral[n v²/2+(tau phi_t²+sigma chi_t²)/(2C)]. The full energy relative to
the static reference is kinetic plus Delta E. Boundary/source work is assumed
accounted for by the actual equations and those walls, not by prescribing an
external static source in place of matter.

If it starts with ||eta||infinity<1/4 and conserved relative TOTAL energy
strictly below B_scale, it cannot reach the quarter-cap while these hypotheses
hold. Indeed H1 continuity implies continuous supremum norm; at a first
hitting time the state still satisfies the closed cap used in (8). Nonnegative
kinetic energy and (14) contradict the conserved energy value. This is a
conditional continuation of the scale cap during the trajectory's existing
lifetime. It proves neither that a trajectory exists nor that it extends past
a singularity, is unique, preserves other regularity or satisfies weak energy
equality. It gives no density half-cap or no-vacuum theorem, as (12) demonstrates.

## 8. Scope and physical bookkeeping

F_min and cs²D have energy-per-area units; D has mass-per-area units. The
field and scale distances share energy-per-area units. alpha,beta are
dimensionless, and J/(C ell) has energy-per-area units. All reference units
and coefficients are fixed during comparisons; no hidden rescaling or fitted
physical V is used.

Both a_ref=9.3619e-11 and1.1279e-10 m/s² are separate positive reference
hypotheses. Constant-vacuum, frozen a(0)E(z) and genuinely evolving-H histories
remain distinct. The last needs its own reservoir/exchange accounting; it
cannot inherit the conditional fixed-reference energy barrier automatically.
Locally responsive scale remains an added diagnostic premise, not proof of a
literal pointwise vacuum relation. Signed MOND Q source and the time-dependent
source correction are explicit; RAR transfer and registered M action remain open.

FGF037 upper/Taylor discontinuity and infinite-energy directions remain valid.
The exact new result is a stronger density DOMAIN for a lower energetic bound,
plus a density-cap counterexample and a conditional scale barrier. No nonlinear
solution construction, physical-theory stability, imported mechanism, historical
novelty, filtered-MONO/metric/photon/DOF or instrument-calibrated closure follows.
