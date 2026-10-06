# Independent projected-acceleration review

**Verdict: accepted for the declared common-timelike-clock domain, stationary NR source branch, coincident tensor block, and eliminated-envelope regularity. No blocking mathematical error found. Full scalar health and coefficient selection remain open.**

Frozen input hashes independently verified:

- REPORT.md: `6c385dfd264e9721d56acc53a825f210a4a329daa508209782a5d42ac53d26b6`.
- checks.py: `3cdb2ecd7df140af248dab0473ff2df92858a9e0a4604fc92f50a3ff08c7e119`.

## Covariant domain and ADM reconstruction

For each metric the normalized clock normal is u_mu=−theta_mu/sqrt(X), with X=−g^-1(dtheta,dtheta)>0. In its local orthonormal rest frame P=g^-1+u u has eigenvalues (0,1,...,1) on covectors. Thus each projector is positive semidefinite. Its kernel is the span of u_mu, equivalently dtheta. Both kernels coincide because the clock scalar is shared, regardless of differing normalizations. The averaged projector therefore remains positive on the spatial quotient, and the proposed I is nonnegative throughout the admitted domain. This domain excludes pairs/clock gradients with no common timelike foliation; the result is not uniform as either X approaches zero.

Exchange reverses A=a_g−a_hat and interchanges projectors, so I is exactly exchange invariant. For relabelings with f'>0 the normals are invariant. A decreasing relabeling flips both normals, but acceleration, projector and I remain invariant. This is a nonblocking orientation qualification to the report's phrase “monotone relabeling leaves u invariant”; restricting to future-oriented clock relabelings gives f'>0. It does not change the action or calculations.

Independent normalization of a shifted ADM metric yields u^mu=(1/N,−S^i/N), P00=P0i=0, Pij=gamma^ij. Orthogonality of acceleration gives a0=S^i ai and ai=partial_i ln N. Retaining this time component before contraction gives exactly

`I = H^ij partial_i ln(N/L) partial_j ln(N/L)/a0²`,

where H=(gamma^-1+hatgamma^-1)/2. Shift independence follows from projection, not from setting shifts to zero. The interaction has no lapse, shift or spatial-metric velocities in this unitary chart. That observation does not determine secondary constraint preservation or physical scalar degrees.

## Actual first variations and source dictionary

I independently varied the unitary interaction at fixed spatial metrics. Writing v=sqrt(NL)D, r=ln(N/L), and S^j=v M_I H^ij partial_i r, integration by parts gives

`EL_N=Kchi/N [a0²vM−4partial_j S^j]`,

`EL_L=Kchi/L [a0²vM+4partial_j S^j]`.

The terms from differentiating 1/N or 1/L cancel against the explicit dependence of partial r. These equations retain the volume terms. Spatial variation must separately retain variation of H and v, as the report says. They cannot be replaced with a lapse-independent Poisson constraint beyond the declared leading limit.

For the clock check I independently expanded the covariant normal and acceleration in a static zero-shift metric. With theta=t+pi one has delta u_i=−N partial_i pi, delta u^0=0. Computing the connection terms gives

`delta a_i=−partial_i pi_dot`,

independently of N and the static spatial metric; the time variation is generally nonzero. For example diag(−N(x)²,1) gives delta a0=N N' pi_x, while delta ax=−pi_tx. Thus the two spatial acceleration variations cancel exactly. Baseline A0=0 and delta Pij=0 then give delta I=0 pointwise. Minimal matter has no explicit clock coupling, so this proves the stationary clock first-variation admission rather than merely evaluating I on an imposed clock.

At leading stationary weak field, I=|grad(phi−hatphi)|²/a0². The general-dimensional Poisson normalization is Omega G_N=8pi(n−2)G_EH/(n−1), giving 2Kchi=1/(2Omega G_N). Direct variation of the displayed NR action therefore gives the three equations in the report. For an aligned spherical source, its selected flux gives y=(1−2m)x and g/a0=(1−m)x. With m=1/2−x/8+... this yields y=x²/4+... and g/a0=x/2+...=sqrt(y)+.... This preserves the radial constitutive normalization. It neither proves a full sourced relativistic solution nor imports nonspherical QUMOND multipoles or likelihood scores.

## Tensor and regularity leaves

Pure TT spatial perturbations with spatially homogeneous lapses leave ai and I zero exactly. Consequently there is no interaction TT derivative contribution, even though the static source envelope has m(0)=1/2. This is a changed operator, not a two-sided continuation of the former indefinite connection invariant.

For traceless perturbations at coincidence, the geometric-mean volume's second variation equals half the sum of the two individual volume second variations. Its constant term is therefore an ordinary cosmological-constant contribution at quadratic TT order; on the common vacuum background the usual EH curvature terms cancel it. The remaining kinetic coefficients are K/2 for the mean TT and K/8 for the relative TT in the displayed normalization. Both cones are luminal on the common metric. This does not decide scalar/vector dynamics away from coincidence.

A smooth positive Cholesky factor on compact common-clock patches writes I=||B||² in smooth field-jet coordinates. Direct differentiation of Q^(3/2), Q=v^TPv, gives

`Hess = 3sqrt(Q)P + 3(Pv)(Pv)^T/sqrt(Q)`.

Its norm is O(|v|), so it extends continuously by zero. Smooth composition proves C² regularity of the eliminated norm-cube even at zeros. There is no nonzero indefinite-null direction with nonzero dQ that produces the earlier divergent Hessian. This does not imply C³ or uniform coercivity: the cubic Hessian vanishes at zero. The report correctly distinguishes the eliminated interaction from the joint auxiliary action; T_min~||B||^(7/4) is C¹ but not C² at zero and does not remove that joint-action issue.

At g=hatg the accelerations agree for arbitrary clock. Linearizing at double Minkowski gives delta a_g,i=partial_i(nu−pi_dot) and its hatted counterpart, so delta A_i=partial_i(nu−hatnu). The common clock cancels from the complete quadratic interaction. The same cancellation follows on any coincidence background from equality of the two functionals. No positive quadratic clock kinetic is supplied. Absence of that coefficient is not itself a proof of a propagating ghost or strong coupling: the full constraint and sourced-foliation analysis is needed.

The coincident first variation yields Lambda/a0²=chi A/2 and H²=chi a0²A/[n(n−1)]. The clock equation adds no offset selector. A conditional inherited endpoint relation A=2C_resp(lambda) is preserved only as a separate input dictionary.

## Primary sources and computation evidence

I authenticated the [2011 journal primary](https://www2.iap.fr/users/blanchet/images/PhysRevD.84.044056.pdf), the related [1205.0400v1 primary](https://arxiv.org/pdf/1205.0400v1), and [Flanagan's exact v3](https://arxiv.org/pdf/2302.14846v3). They establish prior single-metric foliation acceleration MOND and its adapted-coordinate identity. The latter's stability result is restricted to its slow-motion single-metric theory and stated stationary backgrounds; it is not a stability theorem for this shared-clock relative action. No novelty or transferred cosmological/observational claim follows.

All four frozen manifests independently validate against current inputs with validate_manifest.py and the repository root:

| Run | Result | Intended interpretation |
|---|---:|---|
| main_a | 21/21 | Declared checks pass |
| control_naive_a | 21/22 | Rejects positivity of the naive indefinite connection contraction |
| control_tensor_a | 21/22 | Rejects inherited critical TT kinetic cancellation |
| control_scalar_a | 21/22 | Rejects positive common-clock quadratic kinetic |

Each control has exactly its declared failure. The analytic positivity, covariant static variation, lapse variation and regularity reasoning above supplies the substantive verdict; the bounded records do not replace that proof. REPORT was pinned as an execution input and was not changed. This peer note is outside the runner inputs.

The next exact implication is full scalar constraint/principal-symbol health and sourced foliation existence for this action, followed by cosmology and the independent coefficient selector. This construction closes the specific tensor-cancellation and indefinite-null regularity leaves, while leaving those larger obligations open.
