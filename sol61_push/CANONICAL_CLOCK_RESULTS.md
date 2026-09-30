# A persistent scalar vacuum and the preferred-clock cost

Base 5e0250fdc2e4fe15c35eec2b6c81d66dc23b2854. This replaces the failed conserved-density implementation of RELAXING_DENSITY_RESULTS.md with a canonical positive scalar order parameter q. It is an explicit phenomenological action probe. Its operators, critical matching and free parameters are assumed; no microscopic network or exact 32pi selection is derived.

## Action and homogeneous solution

Use c=hbar=1 and M^2=1/(8pi G). In the preferred-time gauge, let N,h_ij,N_i be lapse, spatial metric and shift, K_ij their extrinsic curvature, R3 their intrinsic scalar curvature, and a_i=partial_i ln N. Introduce an auxiliary spatial vector p_i with positive spatial norm P. The proposed action density, including N sqrt(h), is

(M^2/2)[K_ij K^ij-lambda K^2+R3-kappa R3^2/Mstar^2]

 +2M^2[p dot a-P^2/2]-Kcoupling q P^3

 -(Z/2)g^{mu nu}partial_mu q partial_nu q-U(q),

U(q)=A/q^2+Bq^2, A,B,Z,kappa>0, lambda>1.

The spacetime signature is (-,+,+,+). A foliation scalar T defines a unit timelike normal u_mu=-partial_mu T/sqrt(-partial T dot partial T); the induced spatial metric, projected curvature and u-acceleration supply the covariant dictionary. Impose p dot u=0. The displayed gauge action has two time derivatives and a fourth-order spatial curvature operator. This does not constitute a UV completion or a full constraint/interaction analysis in general backgrounds.

Here q is an independent scalar, not a conserved material-coordinate determinant. Identifying it with surface area density and setting Kcoupling=nu y^3/(6pi v^2) requires an additional microscopic matching calculation. A local |p|^3 term is a phenomenological input: the previous uniform planar determinant does not prove that the full massless fermion effective action is local at nonzero frequency or momentum.

On flat-slicing homogeneous expansion, a_i=0,p_i=0,R3=0. A constant q=q0=(A/B)^(1/4) solves its field equation, has positive energy U0=2sqrt(AB), and scalar mass m_q^2=8B/Z. Unlike conserved labels, this q is not kinematically diluted as 1/a. Its homogeneous perturbation obeys delta q double-dot+3H delta q dot+m_q^2 delta q=0 on the fixed background, with no linear mixing from U'(q0).

The gravitational background lapse constraint and scale-factor equation give

H^2=2U0/[3M^2(3lambda-1)],

Lambda_geom=3H^2=16pi G U0/(3lambda-1).

The density minimum now supplies persistent vacuum stress in this specified homogeneous solution. The preferred-time kinetic sector nevertheless changes its curvature relative to the Einstein proxy 8pi G U0. Ignoring that sector would carry the previous coefficient into the wrong physical theory.

## Critical matching and the scalar mode

Auxiliary polarization stationarity gives a=P+12pi G Kcoupling q P^2. At quadratic order integrating it out adds M^2 a^2, or eta=2 in the convention (M^2/2)eta a_i a^i. This coefficient implements the assumed cancellation necessary for the static cubic response; no symmetry protecting it against renormalization has been established.

For local scalar perturbations h_ij=e^(2zeta)delta_ij,N=1+n,N_i=partial_i psi, the derivative quadratic expressions inside the gravitational bracket are

3(1-3lambda)zeta_dot^2+2(3lambda-1)zeta_dot Delta psi+(1-lambda)(Delta psi)^2,

k^2(2zeta^2+4n zeta+eta n^2)-16kappa k^4 zeta^2/Mstar^2.

Eliminating shift and lapse gives kinetic coefficient 2(3lambda-1)/(lambda-1)>0 and spatial coefficient (2-4/eta)k^2-16kappa k^4/Mstar^2. At the critical eta=2, the ordinary k^2 gradient vanishes. With kappa>0,

omega^2=8kappa(lambda-1)k^4/[(3lambda-1)Mstar^2]>0.

The canonical q mode has its independent positive time kinetic and mass; the cubic coupling gives no quadratic mixing at p=0. The R3^2 operator does not affect transverse traceless modes at this order because their linear R3 is zero. The calculation thus repairs the local principal scalar gradient degeneracy without reverting to the conserved medium's wrong-sign kinetic term.

Crucial scope: positive U0 means the actual background is de Sitter, not Minkowski. These are local derivative/principal-part expressions, valid only in a window where H is small relative to k and to the mode frequency, while k remains below the spatial EFT cutoff. In particular omega is proportional to k^2/Mstar, so k>>H alone is insufficient. Full de Sitter scalar mixing, large-scale stability, nonlinear strong coupling and high-frequency causality remain untested. Positivity of this dispersion cannot certify them.

Primary framework checks: [Blas, Pujolas and Sibiryakov, arXiv:0909.3525v1](https://arxiv.org/html/0909.3525), equations 11-16 and 23-24, supplies the preferred-time scalar reduction and differing cosmological/Newton couplings. Its usual healthy two-derivative interval 0<alpha<2 does not establish health at our boundary eta=2; the fourth-gradient reduction here is explicit. [Blanchet and Marsat, arXiv:1107.5264v1](https://arxiv.org/html/1107.5264), Section IV equations 36-41, identifies the same critical acceleration-squared cancellation for foliation MOND. Their illustrative thermal function is explicitly an unsupported example; it does not derive our coefficient or 32pi. SciSpace discovery is not used as theorem evidence.

## Static limit and corrected coefficient

In the slowly varying weak-static limit, lambda does not enter K_ij=0. If q can relax adiabatically and the fourth-gradient terms are negligible, the previous full-field static law survives:

b(P)=12pi G Kcoupling q(P)P^2,

D=12pi G(2A Kcoupling^2)^(1/3),

G_N=G(1+D)/D, a0_N=[D/(1+D)]/[12pi G Kcoupling q0].

Adiabatic relaxation requires density gradients small compared with the local canonical scalar mass scale. It is not automatic in a galaxy, and no lensing/source profile is solved here. With zero additive vacuum constant, the actual homogeneous geometric ratio becomes

Lambda_geom/a0_N^2 = 4D(1+D)^2/[3(3lambda-1)].

The old (2/3)D(1+D)^2 proxy is recovered formally at lambda=1, outside the chosen scalar-mode regime. Achieving 32pi now requires D(1+D)^2=24pi(3lambda-1). This is a condition on free parameters, not a selection law. An additive vacuum constant changes H while leaving the vacuum q minimum and the static coefficients unchanged; it remains permitted.

There is a useful testable consequence of imposing the target relation in this particular branch. The gravitational coupling in the homogeneous Friedmann equation is G_cosm=2G/(3lambda-1). Therefore

G_cosm/G_N=2D/[(1+D)(3lambda-1)].

If the target 32pi is imposed, this simplifies to 48pi/(1+D)^3. Lambda-branch lambda>1 requires D>D_min, where D_min(1+D_min)^2=48pi and D_min approximately 4.67775639. Hence G_cosm/G_N is strictly less than D_min/(1+D_min), about 0.824. The target cannot approach equal cosmological and Newton couplings within this branch. This is a conditional mathematical prediction, not an observational exclusion: current primordial-abundance and cosmological bounds must be checked with the model's full expansion history before drawing that conclusion.

The stabilizer also perturbs the static law. Solving the weak-static spatial metric perturbation to leading k^2/Mstar^2 gives the low-momentum effective term -8M^2 kappa(Delta Phi)^2/Mstar^2. Combined with the deep cubic, the leading field equation is

div[(|grad Phi|/a0_bare)grad Phi]-(8kappa/Mstar^2)Delta^2 Phi=4pi G rho.

For the formal exterior tail grad Phi=A_tail/r, the radial current is r^2[g_field^2/a0_bare-(8kappa/Mstar^2)(Delta Phi)']. Keeping its constant value gives

g_field=A_tail/r-8kappa a0_bare/(Mstar^2 r^2)+higher orders.

The relative correction decreases as 1/r. This is a leading weak-static derivative expansion, with small fractional correction and k below the cutoff, not a complete global solution. Near vanishing source amplitude the expansion fails. Density gradients, the full spatial constraint and fermionic nonlocal response have not been included in this tail estimate.

## Evidence and next decision

Twenty checks pass: exact shift/lapse reduction, critical polarization matching, canonical vacuum mass, two background equations, geometric-curvature bridge, leading radial current, and six positive principal-dispersion parameter samples. The symbolic sign analysis supplies the universal positive-parameter statement; samples do not establish background health. Self-review finds the displayed background and local reductions consistent, conditional on the explicitly assumed action. All-background stability, strong-coupling control, microscopic matching, parameter/counterterm selection and observations remain open.

This is a constructive improvement over a static energy minimum with no viable vacuum dynamics. The next high-value test is the full retarded gapless-mode polarization: the prior massless planar loop has a nonlocal momentum response and may alter the clock's quadratic dispersion before the added k^4 term dominates. A dressed collective mode could have a different dispersion from a fundamental fractional kinetic field; its causal frequency kernel must be checked rather than inferred from a static |k| term. Separately, check the conditional G_cosm/G_N prediction against current cosmological evidence and audit de Sitter perturbations. None of these gaps is resolved by declaring 32pi a fitted input.
