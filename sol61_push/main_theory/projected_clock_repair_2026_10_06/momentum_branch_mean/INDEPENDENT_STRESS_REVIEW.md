# Independent action-stress review of momentum–decay interference

Primary verdict: **proved as written for the declared formal quadratic, aligned Fourier preparation and fixed Einstein/source split**. This accepts the action-derived normal density and pressure trace, and their exact averaged Hamiltonian identity. It does not establish a complete second-order classical solution, a fluid equation of state, or cold abundance.

Reviewed bytes: REPORT.md SHA256 `46b68b4129ecb070bb022ccb6181830b6c1a339afee80a2b631d77a119b67f81`; checks.py SHA256 `cd54cdf99f72a93e1ecb5898fcab3a21b9ad6521c07c4339b7117fda9008fcc5`. Author inputs were read only; no author functions were imported to derive the stress. This review reconstructs the variation and constraint rather than using the assertion count as proof.

## Claim and dependency scope

The action is the projected-acceleration interaction plus individual shear repair on two metrics, with individual Einstein coefficient M=2K, shared timelike clock, n=3, 0<eta<1 and coincident on-shell de Sitter H²=A a0²/6. The admitted linear relative solution has b=3(1−eta)/eta, P=k²/a², k>0, d=D0/a, u=CP/(bH²), and lapse difference nu=(d+u)cos(kx). The quadratic calculation fixes the homogeneous relative correction to zero and uses D1=D2=0 for the relative logarithmic four-volume. It is a formal order-two stress/mean constraint calculation on this specified preparation.

Dependency leaves are: the explicit covariant projected/shear action and ADM convention; the constrained linear solution; variational definitions of normal stress; proper spatial averaging and periodic integration by parts; and the sourced common mean lapse row. No external fluid/tracking theorem is needed. The nonsmooth norm-cube force at nonflat gradient zeros remains an admission issue, explicitly not proved by these identities.

## Independent lapse and spatial variations

For ONE metric, hold its spatial metric and contravariant shift, the other metric and clock fixed. With r=ln(N/L), v=sqrt(Vg Vh) and Havg=(gamma_g^-1+gamma_h^-1)/2, the quadratic projected density is K v Havg^{ij} r_i r_j. Its log-lapse Euler row is

EL_logN = K v Havg^{ij}r_i r_j/2 − 2K partial_i(v Havg^{ij}r_j).

The full interaction additionally has its vacuum-volume term, equivalent to K a0² v M_eff. Normal density is −EL_logN/Vg. At the seed Vg=Vh=a³, Havg=a^-2 identity to the relevant order. Thus rho_grad,1=2K nu_xx/a² and rho_grad,2_direct=−K nu_x²/(2a²). These signs follow from the functional derivative, not a positive-energy analogy.

Each proper SPATIAL measure is sqrt(gamma_g)=a³ exp(−nu/2), with the opposite first sign for the other metric. The linear-density times linear-measure term is −K<nu nu_xx>/a²=K<nu_x²>/a². Normalization by the same measure introduces no further order-two contribution because the vacuum-subtracted background density is zero and the order-one mean vanishes. Consequently

rho_grad = K<nu_x²>/(2a²) = KP(d+u)²/4.

Holding the other metric fixed, a conformal variation gamma_g -> exp(2Z)gamma_g gives delta v=(3/2)v delta Z and delta Havg=−gamma_g^-1 delta Z. Dividing its Euler row by 3Vg gives p_grad=K<nu_x²>/(6a²)=KP(d+u)²/12. This verifies the inverse-projector variation rather than treating the projector as fixed.

For −eta K N sqrt(gamma) sigma², sigma has one inverse lapse. The actual normal density is −eta K sigma². Under the same conformal spatial variation, mixed extrinsic curvature acquires only an isotropic additive term; its tracefree part is unchanged, including the shift transport term. Therefore p_shear=rho_shear. The first scalar shear tensor is −3Hu cos(kx)/(2eta) times (khat_i khat_j−delta_ij/3); the latter norm is 2/3. Averaging gives <sigma_1²>=3H²u²/(4eta²).

It follows directly that

rho_normal = KP(d+u)²/4 − 3KH²u²/(4eta),
p_normal = KP(d+u)²/12 − 3KH²u²/(4eta).

These are the specified Einstein-RHS interaction split and spatial trace. The negative shear contribution is not a contradiction of the positive constrained scalar kinetic coefficient, and is not by itself a ghost diagnosis. Pressure trace alone does not erase flux, directional stress or metric-exchange terms in the conservation equations.

The geometric-mean constant potential is varied before setting the metrics' volumes equal. On D1=D2=0, v/Vg=v/Vh=1 through this order, so its matched vacuum subtraction has no omitted relative-volume correction. The norm-cube spatial/volume stress starts at third order; its order-two lapse force is a periodic zero-mean divergence. With the stated absence of extra homogeneous relative data, it cannot add the claimed missing average.

## Independent geometric constraint check

Use Gnn=R3/2+Theta²/3−sigma²/2. The exact diagonal curvature, weighted by sqrt(gamma), integrates at quadratic order to <Y_x²>/(2a²), hence Rbar=P(C−d−u)²/4. The nonzero first expansion trace requires its linear-volume covariance: Theta_g,1=−bHu cos(kx)/2. Thus variance(Theta_1)=b²H²u²/8.

The sourced common mean row and the correctly weighted trace give

delta H_normal=−PC²/(48H)+bHu²/16+bHdu/24.

The full averaged vacuum-subtracted equation is

Rbar/2+6H delta H_normal+variance(Theta_1)/3−<sigma_1²>/2=rho_normal/(2K).

Independent substitution of PC=bH²u verifies the identity: curvature plus mean-expansion terms reduce to P(d+u)²/8+bH²u²/8. The remaining shear/variance coefficient is

b/8+b²/24−3/(8eta²)=−3/(8eta),

which is exactly the density coefficient divided by 2K. In particular +PCd/4 from 6H delta H cancels −PCd/4 from Rbar/2. This is cancellation of the a^-3 interference, not cancellation of every cross term. The physical density cross is KPdu/2, proportional to a^-5; the pressure cross is one third of that. The residual density powers are a^-4, a^-5 and a^-6. The signed a^-3 expansion term is real in this specified average, but does not supply a homogeneous dust source.

## Computation and provenance checks

I read the actual raw ADM expansion in checks.py, its variation order, branch substitutions and proper-weight formulas. The implementation distinguishes coordinate mean Euler sources from local interaction stress; its controls remove the weighting covariance, remove intrinsic curvature, or misidentify expansion interference as density. The preserved failed preflight made an overstrong all-cross cancellation assertion; the current test properly retains the faster cross.

Independently ran the standard validate_manifest.py command against the repository root for all current records: main_a, control_covariance_a, control_curvature_a, control_dust_a. Each returned exit 0 and `valid evidence record; mathematical interpretation requires review`. Current main has 32/32; each control has 31/32 with precisely its declared failing assertion. These records validate executable provenance, not a continuum or whole-theory existence theorem.

## Remaining implication and strongest safe statement

Passed: normal-stress signs and proper measure; conformal pressure variation; shear normalization; matched-volume subtraction under the stated D1/D2 conditions; the exact averaged Einstein identity and interference cancellation. Conditional: action/linear branch as declared, regular timelike clock domain, formal order-two expansion, periodic aligned preparation and zero extra homogeneous relative correction. Not addressed: full second-order inhomogeneous classical admission, nonperturbative dynamics, matter-era growth, optical averaging, positive fluid abundance and coefficient selection.

The smallest missing implication for a real new sourced family remains admission of the complete second-order relative equations across the cosine's gradient zeros (and the other unsolved inhomogeneous rows), rather than another mean expansion identity. The strongest safe result is that this prepared momentum–decay interference cannot be interpreted as a dust-scaling normal source at the audited order, despite its dust-scaling preferred-normal mean expansion. A, eta and both integration data remain free.
