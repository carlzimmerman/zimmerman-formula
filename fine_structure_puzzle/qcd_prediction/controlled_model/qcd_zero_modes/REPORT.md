# Two-flavor QCD topology and its leading charge response

This new packet preserves the earlier Maxwell work. It computes actual
two-flavor QCD chiral/topological zero-mode functions, and then their leading
electromagnetic Dashen-operator response. There is no dark-energy or alpha fit.
The group integrals are exact for the retained leading chiral action; their
identification with QCD has the explicit finite-volume regime below.

The calculated results are an all-scaling-mass susceptibility/condensate
identity, a fixed-topology suppression mechanism, an exact cancellation of
an apparent 3/(2V) metric stress on matching the canonical pion measure,
and an explicit unfitted electromagnetic response function. None determines
the complete QCD gravitational coefficient c_H or a physical alpha root.

## 1. QCD action and domain

Assume Nc>=3, two fundamental quarks with the same positive renormalized
mass m, spontaneous chiral breaking in the infinite-volume theory, and no
electromagnetism initially. The covariant leading Euclidean chiral action is

    S = integral sqrt(g) [F^2/4 Tr(partial U partial Udagger)
        - Sigma/2 Tr(m e^(i theta/2) Udagger + m e^(-i theta/2) U)],
    U in SU(2), Sigma>0, M_pi^2=2m Sigma/F^2.

The epsilon/Leutwyler--Smilga regime requires a characteristic size L with
Lambda_chi L>>1, F L>>1 and M_pi L<<1. Nonconstant pion modes are
perturbative; the constant group mode is integrated rather than expanded.
The singlet anomalous mode and other hadrons are heavy. Higher mass,
derivative, curvature and electromagnetic operators are not retained here.

The authenticated primary calculation of the flat-torus group integral is
Lenaghan and Wilke, [hep-th/0108166v2](https://arxiv.org/abs/hep-th/0108166),
Section II and equations (5)--(11), with the two-flavor sum in (19)--(24).
Its source conventions and exact hashes are recorded in `source_records.json`.
The original Leutwyler--Smilga publisher metadata was authenticated; its
PDF returned HTTP401, so exact extraction relies on the accessible primary
Lenaghan--Wilke paper. The curved constant-field action below is derived
from the leading covariant EFT, not attributed as a full curved-QCD theorem
to the flat-torus source.

## 2. Exact group integral and an unfitted QCD response

Write U=a0+i a.sigma with a0^2+|a|^2=1. Normalize Haar measure by
integral_SU2 dU=1 and put

    mu=m Sigma V, c=cos(theta/2), z=2mu c.

The exact normalized zero-mode integral is

    Ztilde(mu,theta) = (2/pi) integral_0^pi sin(phi)^2 exp(z cos(phi)) dphi
                    = 2 I1(z)/z,                                   (1)
    Z_chi,LO = N(V) Ztilde.

At z=0 its value is one. It is even in z and 2pi-periodic in theta.
The source uses an overall factor 1/2 in its displayed two-flavor expression;
this constant has no effect on its derivatives. It does not determine the
volume-dependent normalization N(V).

Let r(z)=I2(z)/I1(z), with r(0)=0 and r'(0)=1/4. Then

    d_z logZtilde = r(z),  r'=1-r^2-3r/z.

Define the positive condensate magnitude per flavor by the common-mass
derivative C=(1/(2V))d_m logZ. Keeping the leading mass-independent
normalization separate gives

    C/Sigma = c r(z),
    chi V = -d_theta^2 logZtilde
          = (mu c/2) r(z)-mu^2 sin(theta/2)^2 r'(z).                  (2)

At theta=0 the exact leading-action relation is

    chi = (m/2) C,    chi V=(mu/2)r(2mu).                            (3)

This predicts a full dimensionless finite-volume response, without fitting
Sigma to a desired result:

    chi V = mu^2/4 - mu^4/24 + O(mu^6),
    C/Sigma = mu/2 - mu^3/12 + O(mu^5)                 (mu small),
    chi -> m Sigma/2, C -> Sigma                     (mu large).    (4)

The latter is a mathematical saddle of the group function, physically usable
only in an overlap where the epsilon inequalities continue to hold.
The scalar mass susceptibility is also fixed:

    d_m C = 2 Sigma^2 V c^2 r'(z).

The identity at theta=pi, Ztilde=1 and C=0, is a property of this
leading degenerate action. Higher mass operators can become particularly
important there; it is not claimed as an exact all-order QCD phase statement.

## 3. Summing actual QCD topology

With the same normalization the fixed-topology Fourier coefficients are

    Z_nu(mu)=I_nu(mu)^2-I_(nu-1)(mu) I_(nu+1)(mu),
    Ztilde(theta)=sum_(nu in Z) exp(i nu theta) Z_nu(mu).              (5)

For n=|nu| and small mu,

    Z_nu = (mu/2)^(2n)/[n!(n+1)!] [1+O(mu^2)].

In particular Z_0=1+O(mu^2), Z_(+/-1)=mu^2/8+O(mu^4).
At theta=0, P_nu=Z_nu/sum Z_nu and
<nu^2>=chi V. Thus the leading chi V=mu^2/4 follows from the
two first winding sectors. It is not a continuum Gaussian assumption.

At fixed nonzero nu the condensate behaves as
C_nu=|nu|/(mV)+O(m): the Dirac zero-mode pole is present in that
conditioned sector. Its posterior probability vanishes as m^(2|nu|),
and summing all sectors produces the finite C~m Sigma^2 V/2 in (4).
The experiment verifies the weighted sum of independently differentiated
fixed-nu partition functions against (2). This is a physical topological
suppression/cancellation, not an arbitrary toy function.

## 4. The measure cancellation in metric response

For the area/volume-only leading constant-field action, define W=-logZ
and the isotropic Euclidean metric response epsilon=d_V W at fixed
mass and couplings. Using Ztilde alone would give

    epsilon_tilde=-2m Sigma c r(z).

At theta=0 the large-mu expansion is

    Ztilde ~ exp(2mu)/(2sqrt(pi) mu^(3/2)) [1-3/(16mu)+...],
    epsilon_tilde=-2m Sigma+3/(2V)-3/(16m Sigma V^2)+... .              (6)

The apparent 3/(2V) term counts three collective Gaussian coordinates
with a volume-independent normalized Haar measure. It cannot be inserted
as a physical finite-size gravitational energy without matching the field
measure.

Near U=1 set U=exp(i sigma.pi/F). The orthonormal constant-pion coefficient
is q0=sqrt(V) pi=F sqrt(V) phi_vector. A canonical Gaussian measure
product (mu_R/sqrt(2pi))dq0 differs from the normalized local Haar
measure d^3phi/(2pi^2) by

    N0(V)=sqrt(pi/2)(mu_R F sqrt(V))^3.

Therefore

    N0 Ztilde_saddle = exp(2m Sigma V)(mu_R^2/M_pi^2)^(3/2),
    -d_V logN0 = -3/(2V).                                          (7)

This cancels the +3/(2V) in (6). The constant mode has positive
eigenvalue M_pi^2 at positive mass; that eigenvalue is independent
of radius. The cancellation is exact at the Gaussian level and was
independently checked by the coordinator from this packet's raw derivation.
It fixes this local measure Jacobian; it does not fix the complete N(V).
The remaining O(1/(m Sigma V^2)) of the exact group integral after
this Jacobian is a constant-mode interaction correction, not the full
QCD curvature expansion.

If a full S4 pion determinant includes its constant mode, (7) is already
present in that determinant convention. Do not add another copy.
An algebraic replacement factor, if a consistent epsilon expansion is
being assembled, is the exact group integral divided by its same-normalization
Gaussian saddle. Mixed constant/nonconstant-mode interactions must still
be treated in the same counting.

## 5. Sphere geometry and what the zero-mode normalization cannot fix

For a round S4,

    V=kappa H^-4, kappa=8pi^2/3, R=12H^2.

Even the uncorrected 1/V in (6) would be H^4 rather than H.
More fundamentally, with fixed positive m and fixed F,Sigma,
M_pi/H grows without bound as H->0. The epsilon condition fails.
Holding mu fixed instead requires m~H^4, so that M_pi/H~H;
this is a different mass-changing path. Neither operation gives the
contracted fixed-positive-mass definition of c_H.

The normalized group integral determines ratios and mass/theta derivatives.
Its construction factors out heavy modes, nonconstant pion determinants
and gravitational matching terms in N(V), including a cosmological
constant convention. Curvature-dependent mass operators enter beyond this
leading action as well. Setting N(V)=1 would assume the unknown stress.
Knowing the canonical factor (7) fixes only one component of this matching.

For clarity, a hypothetical mass/theta-independent normalization

    delta W=(4/3)c Lambda^3 kappa^(1/4) V^(3/4)

would be invisible to (2)--(5), but would give
delta epsilon=d_V delta W=c Lambda^3 H. This is a diagnostic of
what the normalized observables cannot see, not an assigned coefficient
or a declaration that such a nonanalytic gravitational term occurs in
QCD. Its coefficient must be computed, or excluded, by actual state/metric
matching outside this zero-mode reduction. In particular W/V would differ
from this stress by a factor 4/3.

## 6. Leading electromagnetic operator: an explicit alpha response

Now include just the leading local Dashen operator. Take
Q=diag(2/3,-1/3), e4^2=4pi alpha and an explicitly unknown, independently
matched coefficient C_EM>0 (called C in the scripts/raw note). The operator
and mass normalization are authenticated in Urech,
[hep-ph/9405341v2](https://arxiv.org/abs/hep-ph/9405341), equations
(1),(5),(8). Its SU3 source uses charges including e; here e4^2 is
written explicitly, and the two-flavor coefficient is not numerically
identified with a three-flavor phenomenological fit.

Direct Pauli algebra gives

    Tr(Q U Q Udagger)=5/9-s, s=a1^2+a2^2.

Use the explicit aligned-vacuum-subtracted Euclidean action
S_EM=e4^2 C_EM V s=t s. The conventional unsubtracted action instead
adds exp(5t/9) to Z; its constant vacuum shift remains in the subtraction
and matching convention, rather than being hidden in a predicted energy.

The Haar marginal of s on the unit three-sphere is uniform on [0,1].
Conditioned on s, (a0,a3) is a circle of radius sqrt(1-s). The retained
leading-action integral is consequently

    Zhat(z,t)=integral_0^1 ds exp(-t s) I0(z sqrt(1-s)).               (8)

At t=0 it is (1); at z=0 it is (1-exp(-t))/t. It is finite and
provides an exact two-parameter response function for the retained action.
The full QCD+QED partition still includes N(V,alpha), other operators,
dynamical photons and electromagnetic/anomalous sectors.

To first order in t,

    logZhat = logZtilde-t K(z)+O(t^2),
    K(z)=<s>_0=2r(z)/z, K(0)=1/2.                                 (9)

This follows because SU2 rotational symmetry gives
<s>=(2/3)(1-<a0^2>) and <a0^2>=r'+r^2=1-3r/z.
Holding m,V,Sigma,F,C_EM fixed in this leading insertion, the calculated
charge responses are

    d_logalpha logZhat = -t K(z)+O(t^2),
    d_logalpha(C/Sigma) = -c t K'(z)+O(t^2),
    d_logalpha(chi V) = -(mu t/2)K'(2mu)+O(t^2) at theta=0.          (10)

The relation chi=(m/2)C survives to this order and indeed to all t
within the single retained operator: m and theta enter only through z,
whereas t is independent of both. This is not an all-order QCD+QED Ward
theorem. Independent alpha dependence of the LECs, unequal running quark
masses and the constrained physical mass path are additional problems.

There is a simple nonperturbative small-mass limit of this charge response.
At z=0 the charged-coordinate mean is

    <s>_t=1/t-1/(exp(t)-1),
    C/Sigma = mu [1-1/t+1/(exp(t)-1)] + O(mu^3),
    chi V = (mu^2/2)[1-1/t+1/(exp(t)-1)] + O(mu^4).                  (10a)

The bracket tends to 1/2 at t=0 and to one as t grows: penalizing the
charged coordinates leaves a neutral circle rather than breaking the
finite-volume restoration at m=0. Its expansion is 1/2+t/12+O(t^3),
so the fractional leading susceptibility response is +t/6 at small t.
This coefficient is fixed by the group measure; converting t to a physical
alpha derivative still requires C_EM and a specified mass path.

## 7. The charged-pair metric cancellation

For a metric derivative at fixed m,e4^2,C_EM, both mu and t vary
with V. Differentiating (9), rather than dividing it by volume, yields

    delta epsilon_EM = e4^2 C_EM [K(z)+z K'(z)]
                     = 2e4^2 C_EM r'(z) + O(e4^4).                  (11)

At theta=0, K(2mu)=1/mu-3/(4mu^2)+..., so the leading
t/mu=e4^2 C_EM/(m Sigma) effective-action correction is volume-independent
and cancels from the metric stress. Its first group-model remainder is
3e4^2 C_EM/(4mu^2). This is an explicitly calculated cancellation,
not an undetermined assigned power-law coefficient.

The all-t Gaussian saddle makes the same point without a nonuniform
small-t expansion:

    Zhat(mu,0,t) ~ exp(2mu)/(2sqrt(pi) sqrt(mu)(mu+t)),
    Zhat(mu,0,t)/Zhat(mu,0,0) -> 1/(1+t/mu).                        (12)

The charged-pion pair has
M_charged^2=M_pi^2+2e4^2 C_EM/F^2. Its canonical Gaussian partition
ratio is M_pi^2/M_charged^2=1/(1+e4^2 C_EM/(m Sigma)), exactly
(12). It is radius-independent at fixed masses/couplings, so it gives
no separate leading metric stress. Its first charge derivative is
-C_EM/(m Sigma), agreeing with (9).

The epsilon regime with electromagnetism also requires M_charged L<<1.
At fixed t and mu while V grows, e4^2 as well as m scales as H^4.
This controlled scaling is not the fixed physical alpha and mass limit.
The asymptotic tests below are tests of the group function; they are not
certificates that each dimensionless point has specified physical F,L.

## 8. Computation and provenance

The pure-QCD experiment is frozen in `run_001`: 30 (mu,theta) points,
five topology sums with |nu|<=80, three selected fixed sectors and four
saddle values, run at 100 and 130 decimal digits. It passed 325 controls
per precision; the repeated-precision error is at most 3.020e-100 on
the declared scales. Its v2 manifest validates with current input hashes.
Controls use independent Haar quadrature, Bessel/hypergeometric expressions,
fixed-topology sums, mass/theta finite differences, posterior derivatives
and direct canonical measure/volume derivatives.

An analytic bound controls the winding cutoff: for n>=0,
I_n(mu)<=(mu/2)^n/n! exp[mu^2/(4(n+1))] and
0<=Z_nu<=I_nu^2. Geometric tails, including the nu^2 moment, are
recorded. Arbitrary-precision rounding is checked by the second precision;
it is not interval-certified. The analytic group/measure derivations, not
the finite grid alone, support the all-parameter identities.

The QED extension has separate immutable raw derivation, inputs, source
record, contract and runner, avoiding changes to the executed pure-QCD inputs.
It compares the disk/Bessel integral with a direct SU2 axis-angle integral
whose polar-axis integration uses an independent hypergeometric expression.
Mass, charge and theta finite differences check the displayed responses.
The first insertion and its metric cancellation are compared independently,
and the charged-pair saddle is tested at fixed t/mu. See its manifest and
`REPRODUCE.md` for the observed execution result.

The completed QED record is `qed_run_002`: 18 finite (mu,theta,t)
points at each of 80 and 110 decimal digits, three first-insertion cases,
and six saddle comparisons. It passed 105 controls per precision, with
repeated-precision error at most 1.280e-80. Its manifest validates with
current input hashes. Runtime was 98.29 seconds; the earlier otherwise
identical `qed_run_001` reached its 80-second CPU cap and is preserved
as `resource-limit`, not accepted mathematical evidence.

For example, at mu=1 and theta=0, K=0.433127426722312 and
-K'=0.0538542212237151. At mu=400, t/mu=1, the exact charge-to-pure
partition ratio is 0.500312793335563, approaching its calculated Gaussian
value 1/2; its metric energy difference in units m Sigma is 1.56445649e-6,
approaching zero rather than a volume-independent density.

## 9. What is established and the next executable step

These are unfitted low-energy response functions of actual QCD chiral and
topological sectors, with an explicit leading electromagnetic insertion.
They show why finite normalized chiral/topological information can be right
while an inferred finite-size stress is wrong: the canonical mode measure
removes the apparent 3/(2V), and the charged Gaussian response is a
volume-independent effective-action shift. Neither leaves a linear-H
coefficient to determine from this sector.

The next consistent assembly is to match the group's constant-mode
normalization to the coordinator's canonical S4 determinant. If that
determinant already contains all constant pion modes, replace its Gaussian
constant-mode factor by the exact group factor, multiplying by

    Q(mu,t) = Zhat(mu,0,t)
              /[exp(2mu)/(2sqrt(pi) sqrt(mu)(mu+t))],

and calculate constant/nonconstant-mode interactions at the same epsilon
order. An independent determination of the complete metric-dependent
normalization, its QCD+QED matching, and the fixed-state fixed-mass curvature
limit is still required to compute c_H/C_p^3 or select alpha(0).
