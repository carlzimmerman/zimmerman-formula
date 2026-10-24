# Source spectral constraints and the origin of the cubic response

## Result

There is a genuine restriction on admissible protection mechanisms, and a conditional amplitude bound, but no universal numerical bound on R = u^3/(v sqrt(e)). For a linear Hermitian scalar portal into a unitary Lorentz-invariant matter vacuum, a finite positive-mass spectral band contributes a nonnegative quadratic kinetic term. Additional physical intermediate states cannot cancel this spectral weight by negative probabilities. Cancellation of the full local quadratic coefficient still requires control of contact terms, nonlinear portals or other sectors. Separately, an effective energy analytic in the gradient cannot generate the required cubic absolute-gradient term. Thus an ordinary regular gapped analytic sector alone cannot provide both the desired cubic and its protection.

These are restrictions on microscopic constructions, not a reduction from four continuous parameters to three. The original joint-selection goal remains open.

Frozen criteria: 13dd783e9e. Base: 2ce8f3c2b8. Kappa = 1/2 remains FITTED. CFG493 kappa_Lambda = 0.417 +/- 0.095 and kappa_crit = 0.345 +/- 0.078 are distinct and unused. No target value, fit or scan enters this analytic audit. Units c = hbar = 1; the vacuum footing is dark energy. No independent second observational prediction or microscopic hbar cancellation is claimed.

## 1. Positive spectral response of the source sector

This argument concerns a matter vacuum in fixed flat spacetime, not the complete preferred-frame gravitational theory. Let O_a be Hermitian Lorentz-scalar local operators and let the Euclidean interaction be integral chi h_a O_a with real h_a. Define O_h = sum h_a O_a and connected correlators. In n spatial dimensions, insertion of a complete set of positive-norm states gives a positive semidefinite spectral matrix rho_ab(sigma): for every real vector h,

    h_a rho_ab(sigma) h_b >= 0.

It is a sum/integral of absolute squares of vacuum-to-state matrix elements of O_h, with positive phase-space measure. This does not depend on whether the intermediate state contains fermions or bosons. Signs in individual loop diagrams are not signs of inclusive physical spectral probabilities.

Restrict to a finite band B = [sigma_1,sigma_2] with sigma_1 > 0 and finite spectral moments. Its Euclidean dispersive contribution is

    Pi_B(p_E^2) = integral_B d sigma rho_h(sigma)/(sigma+p_E^2).

Full composite correlators can require subtractions. Accordingly Pi_B is a specified finite-band dispersive piece; local polynomials P(p_E^2) and the rest of the spectrum are not silently set to zero.

Expanding the connected generating functional for the linear portal gives

    Delta S_eff^(2) = -(1/2) integral_p chi(-p) Pi_B(p_E^2) chi(p).

The minus sign follows directly from minus log of the matter partition function. For |p_E^2| < sigma_1,

    Pi_B(p_E^2) = I_0 - p_E^2 I_1 + O(p_E^4),
    I_1 = integral_B d sigma rho_h(sigma)/sigma^2 >= 0.

Therefore Delta S_eff includes +(I_1/2) integral (partial_E chi)^2. In the static scalar notation it contributes Delta beta_B = I_1. The associated zero-derivative term also exists and must be controlled in a complete long-range-force model; this argument does not solve that additional problem.

For a single portal g chi O, keep g outside the spectral measure and define

    I_B = integral_B d sigma rho_O(sigma)/sigma^2,
    Delta beta_B = g^2 I_B.

In four spacetime dimensions, an operator O of engineering dimension four with g of dimension minus one gives I_B dimension two, so Delta beta_B is dimensionless. The derivation assumes the renormalized operator and portal are defined consistently; it does not identify an arbitrary O with baryonic mass density without matching. Applying it to the previous EFT requires a relativistic source whose nonrelativistic limit has that coupling.

### What extra fields can and cannot cancel

For independent source sectors the spectral responses add. For interacting sectors, interference may create null combinations, but the complete matrix remains positive semidefinite. The finite-band term vanishes precisely when

    sum_a h_a <N|O_a|0> = 0

for almost every physical state N with invariant mass in the band. Thus cancelling the spectral term means removing the portal's vacuum-transition matrix elements in that band. It does not follow from arranging equal numbers of bosons and fermions. This statement does not prove that every static charge vanishes, nor does a band null imply a null in the entire spectrum.

This is different from the previous supertrace cancellation of a vacuum determinant. A positive two-point function of a fixed Hermitian source operator is not a boson-minus-fermion supertrace. Supersymmetric or gauge-completed portals may contain additional interactions and contact contributions. They must be checked as complete portals, not excluded by this restricted calculation.

### Contact-term loophole is real

A local coefficient beta_local contributes independently. In a fixed matching convention,

    beta_eff = beta_local + g^2 I_B + beta_other.

Choosing beta_local = -g^2 I_B - beta_other sets beta_eff = 0, while the spectral discontinuity remains nonzero. Thus spectral positivity alone does NOT prove beta_eff > 0 and gives no universal lower bound on the full renormalized beta. It instead identifies the matching relation a genuine symmetry would have to enforce and maintain. Finite-band dispersive attribution is a useful diagnostic, not a scheme-independent naturalness theorem. Nonlinear derivative portals can add further local terms outside this linear-portal argument.

## 2. A conditional inequality for the physical amplitude

Specialize to three spatial dimensions, the source/force identification of the parent audit, and a cubic-dominated regime. Let a_min denote the scalar acceleration at the lowest-gradient point in a specified test interval, s_min = a_min/g. Let epsilon > 0 be the allowed ratio of the quadratic contribution to the cubic contribution in the radial flux. This is a flux tolerance, not exactly the fractional change of the solved acceleration.

Impose the additional no-cancellation criterion: the displayed positive band contribution individually satisfies the tolerance. Then

    Delta beta_B/(lambda s_min) <= epsilon
    implies (g^3/lambda) I_B <= epsilon a_min.

For I_B > 0, the parent matching identities give

    a0 = g^3/(4 pi G lambda),
    R = u^3/(v sqrt(e)),
    g^3/lambda = R sqrt(e)/M_Pl.

Consequently

    R <= epsilon a_min M_Pl / (I_B sqrt(e)),
    equivalently 4 pi G I_B (a0/a_min) <= epsilon.

This is a conditional physical constraint, not a renamed R and not a numerical prediction: it relates amplitude, allowed force-law distortion and a separately calculable source spectral moment. It becomes useful only when the microscopic portal fixes I_B and the test interval fixes a_min and epsilon. No observed acceleration or arbitrary spectral cutoff has been inserted to claim a number. Bands with I_B = 0 yield no such bound. A freely adjustable contact cancellation invalidates the no-cancellation premise, not the positivity proof.

For an exact asymptotic MOND law extending to arbitrarily small scalar acceleration within the idealized static model, nonzero I_B violates this criterion at any nonzero g. Protection then requires an actual matching identity, a portal with the appropriate spectral null, or physics outside this direct-portal setup. Choosing a smaller nonzero coupling merely delays the departure from the asymptote. This limit is not an observational statement about arbitrarily large cosmological radii.

## 3. Analyticity cannot selectively protect the unwanted cusp

Let z_i = partial_i chi and assume the local energy E(z) is real analytic near z = 0 and rotationally invariant. In any n >= 2 spatial dimensions its Taylor series consists of invariant polynomials in z_i z_i:

    E(z) = c_0 + c_1 |z|^2 + c_2 |z|^4 + ... .

One way to see the restriction is to rotate any vector onto a fixed axis and rotate that axis to its negative: the analytic restriction E(t,0,...) is even. Rotational invariance then extends its even series to powers of |z|^2. In n = 1 the same argument requires reflection invariance.

It follows that both |z| and |z|^3 are absent. On a signed axis |t| is not differentiable at zero, and |t|^3 has a discontinuous third derivative. Analyticity therefore cannot protect the missing linear-gradient term while producing a nonzero cubic absolute-gradient response. It also does not forbid the quadratic term.

A uniformly gapped sector with analytic microscopic interactions, a regular solution branch and an effective expansion analytic in gradient amplitudes belongs to this restricted class. A mass gap alone is NOT asserted to prove all these assumptions. If a cubic term is already present nonanalytically in the bare action, this is no longer an explanation of its microscopic origin. Gapless or critical modes, a singular branch/phase transition, nonuniform limits, or a different nonanalytic microscopic structure remain possible routes.

The previous finite-shell scalar loop generating a linear-gradient term is not contradicted: its starting cubic action is itself nonanalytic at zero gradient. An analytic additional heavy sector cannot simply generate an equal opposite cusp within its analytic expansion. Protection must act on the nonanalytic response sector itself, or constrain the complete matching beyond the assumptions above.

## 4. What this does to the remaining search

Exclude the following proposed explanations within their stated assumptions:

- independent healthy source-coupled partners cancel the physical spectral response through a negative spectral weight;
- ordinary analytic heavy-field matching creates the cubic term while analyticity forbids only the linear term;
- positivity of the source correlator alone fixes the vacuum energy or a numerical R.

Keep open but require explicit calculations for: nonanalytic/critical response sectors with a complete baryon portal; symmetry-fixed contact matching; constrained metric/vector mixing such as the previously audited AeST source mechanism; and supersymmetric completions with all nonlinear portal terms included. These are not constructed solutions.

The source spectral data do not by themselves fix e. In the fixed-background calculation an additive vacuum constant changes V while leaving connected source correlators unchanged. Extending the calculation to dynamical gravity is necessary before claiming a stable positive-vacuum identity; simply adding that constant would reintroduce the freedom we are trying to remove.

## Evidence and review status

The work is analytic, not a new executable experiment. Controls: g = 0 removes the induced response; a compensating local quadratic coefficient cancels beta_eff but leaves the spectral response; a pre-existing nonanalytic cubic invalidates the analytic-origin restriction. A single-pole spectral example and a two-operator null example are checked in REVIEW.md. All source matching, contact-term and analyticity assumptions are explicit. Review is self-review, not independent verification. No all-orders protection or microscopic prediction of a0 has been obtained.

Source for the spectral-representation foundation: Eric D'Hoker, Quantum Field Theory 230A, section 6.2, equations (6.37)-(6.46), official UCLA compilation headed October 3, 2004, inspected 2026-10-24. It establishes the scalar positive-weight representation; the finite-band matrix extension, portal expansion and conditional MOND inequality above are derived here. [Official lecture notes](https://www.pa.ucla.edu/faculty-websites/dhoker-lecture-notes/graduate-courses/qft-2016.pdf). No full source was downloaded into the repository.
