# Independently frozen FGF039 mass-constrained entropy and barrier proof

Derived before reading any new author/root proof or preview. Proof-only, no numerical computation or scan. Use one fixed Q crossing on I of length ell, inherited positive coefficients and fixed field walls. Let u=cs²>0 (not a velocity variable), M=int rho>0, and mu= rho dx/M. Density n is any nonnegative measurable function with int n=M and finite relative isothermal entropy; zero density is allowed, with 0 log0=0. psi,eta are H1_0, initially ||eta||infinity<=kappa=1/4. Actual a becomes a exp eta; background source remains signed MOND B'=C rho. No density pointwise cap is imposed.

## Exact density minimization, including vacuum

The density part of the complete relative energy is

 G(n,psi)=u int[n log(n/rho)-n+rho]+int(n-rho)psi.

Define Z=int exp(-psi/u)dmu and m_psi=rho exp(-psi/u)/Z. H1 psi is bounded; hence Z is finite positive, m_psi positive, normalized to mass M, and has finite entropy. Exact substitution gives

 G(n,psi)=H_psi(n)-J(psi),
 H_psi(n)=u int[n log(n/m_psi)-n+m_psi],
 J(psi)=u M log Z+int rho psi.

This identity is valid with n=0 on sets, and the entropy is finite because log(m_psi/rho) is bounded. For t>=0, f(t)=t log t-t+1 is nonnegative, vanishing only at t=1: f'=log t on t>0 and f(0)=1. Thus H_psi>=0, equality iff n=m_psi a.e. This proves existence and uniqueness of the minimizer and its exact nonnegative remainder. The minimum is -J(psi), not -u M log Z alone. The mass multiplier produces the normalization Z. A constant potential shift changes neither m_psi nor J.

## Global negative functional bound without a named inequality

Put K(t)=log int exp(-t psi/u)dmu, t in [0,1], and let expectation_t refer to the normalized tilted measure. Direct differentiation, justified by bounded psi, gives K''=Var_t(psi)/u². If a random bounded value lies between a and b, (X-a)(b-X)>=0 implies Var(X)<=(mean-a)(b-mean)<=(b-a)²/4. Therefore

 0<=J=u M integral_0^1(1-t)K''(t)dt
                  <=M osc(psi)²/(8u).

This is global in the potential amplitude. Weighted Cauchy between maximum and minimum yields osc(psi)²<=I_A int A psi'², I_A=int 1/A. Consequently J<=alpha E_p, where E_p=int A psi'²/C and alpha=C M I_A/(8u).

## Full lower bound after exact entropy elimination

All first variations cancel by the same actual hydrostatic multiplier, fixed mass, B'=C rho and scale equation as in FGF038. Those arguments require only n-rho in L1 here: background multipliers and psi are bounded, so every linear integral exists. The exact energy identity is

 DeltaE=H_psi-J +(1/C)int[F_rel+Jscale eta'²/2+U_rel].

In this display Jscale is the physical gradient coefficient denoted J in prior files; J(psi) above denotes only the minimized functional. To avoid ambiguity below, denote the latter by N(psi)=J(psi), and return the physical coefficient to J.

Use the pinned FGF038 finite-scale bound F_rel>=(k/2)A psi'²-R eta², k=exp(-1/4)/64, R=qhat²/(2kA)+Dhat/2, with the continuous zero extension, and U_rel>=S0 eta²/2. Let E_eta=J int eta'²/C and beta=ell² Rmax/J. Then

 DeltaE>=H_psi+(k/2-alpha)E_p+(1/2-beta)E_eta
                                    +S0 int eta²/(2C).

Sufficient gates alpha<=k/4, beta<=1/4 give

 DeltaE>=H_psi+(k/4)E_p+E_eta/4+S0 int eta²/(2C).

These gates hold after enough restriction of the same solution: M=O(ell), I_A=O(sqrt(ell)), Rmax=O(ell^(3/2)), so alpha=O(ell^(3/2)) and beta=O(ell^(7/2)). No density cap has reentered the proof. The field/scale estimates remain uniform over all admissible n and all H1 potential gradients. Reference units and physical coefficients are fixed; alpha,beta are dimensionless.

## Density distance and conversion of reference

The entropy reference in the lower bound is m_psi, not rho. An elementary pointwise bound gives a controlled L1 distance, including vacuum. For t>0,

 f(t)=(t-1)² integral_0^1(1-s)/(1+s(t-1))ds
      >=(t-1)²/[2max(1,t)] >=(t-1)²/[2(1+t)].

The last bound also holds at t=0 by continuity. It follows that

 H_psi >=(u/2)int (n-m_psi)²/(n+m_psi)
         >=u ||n-m_psi||_1²/(4M),

where the final step is Cauchy-Schwarz and int(n+m_psi)=2M. Thus this distance is controlled directly by DeltaE.

To compare with the original background, let m_t=rho exp(-t psi/u)/Z_t. Its derivative is -m_t(psi-mean_t psi)/u. Cauchy-Schwarz and the variance bound above give ||partial_t m_t||_1<=M osc(psi)/(2u). Integrating yields ||m_psi-rho||_1<=M osc(psi)/(2u). Therefore

 ||n-rho||_1² <= (8M/u)H_psi+[M² C I_A/(2u²)]E_p
               <=C_rho DeltaE,
 C_rho=max{8M/u, 2M² C I_A/(k u²)}.

The first inequality uses the elementary square of the triangle bound; the second uses the retained H_psi+(k/4)E_p. This is an L1 distance result, not a pointwise density bound or L2 estimate. Constants carry physical units appropriately.

## Small energy can violate the density cap and create vacuum

Let E_epsilon be intervals of shrinking positive background mass m_epsilon=int_E rho, with 0<m_epsilon<M and m_epsilon->0. Set

 n_epsilon=0 on E_epsilon,
 n_epsilon=[M/(M-m_epsilon)]rho outside E_epsilon,
 psi=eta=0, velocities zero.

This is nonnegative, fixed-mass, finite-entropy data. It violates the old half-cap on E_epsilon and has actual vacuum there. Its exact full relative energy is

 DeltaE=u M log[M/(M-m_epsilon)] ->0.

The hydrostatic multiplier cancels the density-linear background term, so this is the complete energy comparison, not an omitted potential interaction. The family is allowed by the stated measurable density class; it is not claimed to be a nonlinear solution. The scalar potential is a dynamical field in the inherited action and is not re-solved as an instantaneous constraint for each comparison. Thus no positive energy barrier can enforce the old pointwise density half-cap or absence of vacuum on this class. L1 control is fully compatible with a shrinking vacuum set.

## Conditional scale barrier and exact dynamical limitation

For eta in H1_0, integrating its derivative to each wall gives int eta'²>=4||eta||infinity²/ell: if a maximum is at distances l1,l2 from the walls, Cauchy gives a²/l1+a²/l2>=4a²/ell. This remains valid by continuity at endpoints or for negative extrema. Hence at ||eta||infinity=kappa, the static lower bound gives

 DeltaE >=(1/4)E_eta >=J kappa²/(C ell)=J/(16 C ell).

Call this positive threshold B_scale. The full perturbation energy is kinetic plus DeltaE. The inherited kinetic terms are nonnegative: fluid n v²/2 (or finite momentum energy at vacuum) and positive tau phi_t²/(2C), sigma chi_t²/(2C). Do not remove potential dynamics by entropy minimization; n=m_psi is an energy minimizer, not an imposed evolution closure.

Assume an ALREADY EXISTING trajectory on its given time interval keeps n>=0, mass M, finite entropy/action and fixed walls, is continuous in eta's H1 topology, starts strictly inside the quarter-cap, and conserves full fixed-reference energy with impermeable fluid walls and time-independent field walls. If its initial relative total energy is strictly below B_scale, a first hit of ||eta||infinity=kappa would have energy at least B_scale, a contradiction. The lower bound is needed only up to and at that first hit, where the cap still holds. Thus the scale cap bootstraps along such a trajectory. The same energy then controls the displayed weighted, scale and L1 distances while the trajectory exists.

This proves neither existence, uniqueness, continuation, nonlinear conservation or weak energy equality, nor preservation of positive density or no-vacuum. It does not establish physical-theory stability. Boundary work, prescribed evolving reference work or loss of the finite-action solution class would invalidate the stated conservation premise. Constant reference, fixed field walls and impermeability are necessary premises of this conditional argument.

Both a0 choices and distinct constant-vacuum/frozen-H/evolving-H interpretations remain. Q signed source throughout; no RAR/M action, physical metric/photon/DOF, scale reservoir, empirical calibration or theory closure. FGF037's upper/Taylor obstruction is unchanged. The result is an enlarged-density static energetic theorem plus a strictly conditional scale barrier.
