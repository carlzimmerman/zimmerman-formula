# Independent upstream review: galaxy T identifiability and joint kappa design

12 November 2026. Analytic audit of route_redshift.md; no observations or data-agreement fits. The redshift route's 54-case computation was not independently rerun here. This review independently reconstructs the equations and gives an exact illustrative three-bin joint witness rather than claiming fresh numerical evidence.

## Status

The two-radius identities, global-light-normalization cancellation, response derivatives, Fisher determinant and positive-density gradient counterexample are CORRECT under the specified one-template, fixed-geometry, pointwise acceleration law. The AQUAL angular covariance is also correct. Their transfer to an observationally robust T measurement is CONDITIONAL and UNDEMONSTRATED. In particular an unknown common inclination leaves an exact amplitude degeneracy in the idealized fixed-light-geometry model, while arbitrary radial M/L defeats T identification constructively. This is a measurement-design result, not a completed empirical gate or theory.

## Independent reconstruction

Let w=v_c^2/theta, D=DA, gb=U b(theta), A=D U, T=D a0. Dimensions: w,T are velocity squared; b acceleration; A length. For simple-mu,

    gb=g^2/(g+a0),  g=w/D
    implies w^2=A b(w+T).

Thus p=w^2/b=A w+B with B=A T. At two radii with w2!=w1, A=(p2-p1)/(w2-w1), B=(w2 p1-w1 p2)/(w2-w1), T=B/A. Positive A and B are required. Vanishing A or denominator is a boundary failure, not an allowed normalization measurement.

For the quadratic law g^2=gb^2+a0 gb,

    w^2=A^2 b^2+A T b,
    p=C b+E, C=A^2, E=A T.

For b2!=b1, C=(p2-p1)/(b2-b1), E=(b2 p1-b1 p2)/(b2-b1), T=E/sqrt(C). C,E must be positive. A global b->k b sends (A,B)->(A/k,B/k) for simple-mu and (C,E)->(C/k^2,E/k) for quadratic; T is invariant. No assumption of common U between galaxies or redshifts is needed for this restricted cancellation.

Simple-mu implicit differentiation gives

    dlnw/dlnT = T/(w+2T) = t,
    dlnw/dlnA = (w+T)/(w+2T) = 1-t.

Quadratic gives t=1/[2(1+gb/a0)] and the same complementary A response. For independent log-w weights omega, the Jacobian rows are (1-t_i,t_i). The Cauchy-Binet expansion of det(J^T W J) is

    det F = sum_(i<j) omega_i omega_j (t_j-t_i)^2.

This confirms the stated determinant. For correlated positive-definite errors use J^T Cov^-1 J; the simple pairwise weight expression no longer applies unchanged. Rank still requires nonidentical response directions. Deep t=1/2 gives only A T; Newtonian t=0 eliminates T. The use of different accelerations is therefore load-bearing. Two radii determine two parameters but leave no shape residual; at least three usable independent radial modes are needed for an internal model check, with more needed for added nuisance parameters. PSF-smoothed radial pixels are not automatically independent modes.

The distance-independent b construction is conditional on distance duality, correctly transformed rest-frame surface brightness and fixed angular deprojection/thickness. Surface luminosity density scales as (DL/DA)^2=(1+z)^4. Arbitrary overall photometric calibration is absorbed in U; radial colour/dust/SED/geometry distortions are not. For general AQUAL, x=D theta and rho=U j_tilde/D yield angular source 4piG A j_tilde and interpolation argument |grad_theta Phi|/T. That proves covariance, not unique inversion or observational identifiability. The pointwise linear estimators and their Fisher numbers must not be imported into a disc AQUAL solver.

## Exact nuisance obstructions

Velocity amplitude: with b held fixed, w->lambda w sends A->lambda A and T->lambda T for either law. For simple-mu B->lambda^2 B; for quadratic C,E->lambda^2(C,E). If observed v_los=v_c sin(i), an unconstrained inclination allows T sin^2(i) to remain fixed while T changes. An independent angular light-shape constraint can restrict i only given intrinsic shape/thickness and alignment assumptions. Resolved 2D kinematics may add inclination information, but that is a new data constraint, not algebraic cancellation. Real light deprojection also changes with i and must be fitted jointly.

Radial M/L: for any a>0, a spherical flat circular-speed curve V has

    Mb^(a)(<r)=V^4 r/[G(V^2+a r)],
    dMb/dr=V^6/[G(V^2+a r)^2]>0.

Its Newtonian acceleration is V^4/[r(V^2+a r)], exactly g^2/(g+a) for g=V^2/r. All a give the same circular curve with positive baryonic density. A fixed light profile can therefore accommodate different a through a positive radial M/L proportional to (V^2+a_old r)^2/(V^2+a_new r)^2. This counterexample is mathematically valid; formation plausibility and spectroscopic limits on gradients are empirical questions. It refutes an unrestricted claim that light plus velocities independently measures T. An unmeasured radial gas component has the same inverse-problem freedom.

The phrase 'global M/L eliminated' remains true but does not imply 'stellar-population systematic eliminated'. A one-template analysis must publish its nuisance-template scope and demonstrate stability under physically measured gradient uncertainty.

## Exact three-redshift joint witness, not a forecast

Let u=(2,3,4), q^2=s(1,2,1), s>0, A=1 and C=32pi/3. Define synthetic h_i^2=A u_i^3+C q_i^2. No observations enter. The first two bins have determinant

    D=u1^3 q2^2-u2^3 q1^2=8(2s)-27s=-11s !=0.

The coefficient formula returns

    C=(8 h2^2-27 h1^2)/(-11s)=32pi/3,
    kappa=sqrt[8pi/(3C)]=1/2.

The third independent synthetic bin is exactly h3^2=64+C s. Perturb only that bin by epsilon: the first-two solution predicts a third-bin residual epsilon. This is an elementary overdetermination witness; it proves neither robustness nor power at actual redshifts/covariances. Conversely q_i^2=s u_i^3 collapses the determinant at all bins, so even infinite precision cannot separate A from C. This is an exact adversarial mutation for any future joint implementation.

With Tobs=b Ttrue, qobs=b qtrue and Cfit=Ctrue/b^2: kappafit=b kappatrue. A redshift-independent T calibration does not cancel when measuring the absolute dimensionless joint coefficient, although it cancels in the redshift ratio Q alone. This is the central distinction between the redshift-route ratio and the joint-kappa route.

## First unproved implication and smallest useful next check

First unproved implication: after nuisance freedoms consistent with the proposed actual galaxy data are included, the T likelihood has finite, informative width rather than inheriting an inclination/gradient/template prior. Present Foundation catalogues do not establish this.

Smallest useful next check is synthetic and model-specific, not an observational agreement fit: one resolved bulgeless development template, its actual angular radial sampling/PSF, and a chosen physical law. Compute the full observable Jacobian for [ln A,ln T,inclination,one radial M/L-gradient coefficient,gas amplitude] with the independently available geometry/colour/gas constraints. Examine the singular vector containing ln T after nuisance projection, then inject a permitted gradient and inclination perturbation. Hold out one resolved radial mode. Stop if the nuisance-projected T direction is rank deficient or its bias exceeds the target separation. This directly tests the link on which the BAO joint design rests. A successful single-template witness would justify a broader design study, not immediate population/theory claims.

The prior-art caveats and CFG712/713 shape gate remain mandatory for any lensing extension: do not let a mean lensing/dynamics normalization pass hide failed radial shape or excess scatter.

## Provenance

Reviewed route_redshift.md SHA256: 27e30ecd7c14481240fdfc2f61bcd8549801a86cee3f895522bd531683b36300
The independent derivation above uses its definitions but does not import its checking script. No numerical fit, new survey measurement, broad novelty search or independent rerun of its 54 cases is claimed.


## Fix-forward: earlier inverse-cosmology prior art and two Newton constants

A further explicit predecessor was located after the initial scoped search: `real_research/dark_energy_inverse_2026_09_26/scales/REPORT.md` lines 24–46 distinguishes gG=G_cosm/G_N. Its lines 34–38 already state that background-rate/acceleration comparison identifies kappa/sqrt(gG), not kappa alone. Therefore the general joint coefficient is

    C = 8 pi gG/(3 kappa^2),
    kappa_cosm = kappa/sqrt(gG) = sqrt[8 pi/(3C)].

The C=32pi/3 null is the joint hypothesis kappa=1/2 AND gG=1; equivalently it is kappa_cosm=1/2. The earlier single-G derivation is valid only under that explicitly stronger assumption. With unknown constant gG the design does not isolate local-normalized kappa. With running gG(z) the single-coefficient column model generally fails and must be extended.

`real_research/dark_energy_inverse_2026_09_26/reconstruction/RESULT.md` lines 112–150 already provides an inverse pressure-ratio test, cancellation of H0/kappa/constant gG in a theoretical redshift ratio, and an integral Friedmann family whose constant-a0 limit is vacuum-plus-dust. Thus the general acceleration–background inverse connection and constant-a0 Friedmann relation are prior work in this repo. The proposed angular T measurement plus uncalibrated BAO observables is a narrower measurement-design synthesis; do not present the background relation itself as new. Pressure tracking and density tracking coincide for constant vacuum but differ for evolving w, so that predecessor is overlap rather than universal algebraic identity with the present density test.
