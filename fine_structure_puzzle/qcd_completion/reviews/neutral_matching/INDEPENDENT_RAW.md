# Independent raw derivation, before target reports

Date: 2026-10-18/19. Reviewer: independent subagent `neutral_matching_review`.
At creation I have read the task and audit skill instructions, but none of the
target derivations, reports, run code, or source records. These are derivations
from the mathematical objects specified in the task, not source rederivations.
No runnable experiment is used for these analytic conclusions.

## A. Closed S3 Gaussian sine-Gordon theory

Let the physical sphere have radius R and volume V=2 pi^2 R^3, with
S3 action integral [kappa (grad sigma)^2/2 + f + u(1-cos sigma)].
Keep L, kappa, u>0, and f fixed in a volume derivative. Define m^2=u/kappa.
The specified observable is s=(1/L) partial_V W, W=-log Z; this sign is
the opposite of the thermodynamic pressure if F=W/L. An action written
as -u cos sigma instead has f shifted by -u.

For the full canonically normalized Gaussian determinant, after a local
covariant subtraction, W_G=1/2 log det(-Delta+m^2). Constant kappa factors
are local measure terms; zeta_A(0)=0 for a positive massive scalar on a
closed odd-dimensional manifold. Scalar eigenvalues and degeneracies are
lambda_n=(n^2-1)/R^2 and d_n=n^2, n=1,2,...; n=1 is the spatial constant mode.
Set a^2=m^2 R^2-1. For mR>1,

    dW_G/da = a sum[n^2/(n^2+a^2)]_ren
             = -(pi/2) a^2 coth(pi a),
    W_G = -pi a^3/6 + pi integral_a^infinity t^2/(exp(2 pi t)-1) dt.

An R-independent additive constant has no stress. Consequently

    s_G(R) = -m^2 a coth(pi a)/(12 pi L R),
    s_G(flat) = -m^3/(12 pi L),
    s_G(R)-s_G(flat)
      = m/(24 pi L R^2) + O(1/(Lm R^4)) + exponentially small terms.

There is no 1/R response at fixed microscopic coefficients. The R^-2
coefficient is subject to the local curvature counterterm convention;
the displayed value is the minimally coupled zeta/heat-kernel convention.
For 0<mR<1 put b=sqrt(1-m^2 R^2) and replace a coth(pi a) by b cot(pi b).
The formula is smooth through mR=1. The m->0 limit of the full massive
Gaussian stress is 1/(6 pi^2 L R^3), from the massless nonzero determinant's
scale dependence. This limit is not a uniform compact-scalar saddle limit.

Compactness and the massless reference must be specified separately.
The compact zero angle integrated as d sigma_bar/(2 pi), with uV>>1,
contributes Z_zero approximately (2 pi uV)^(-1/2), and hence
W_zero=1/2 log(2 pi uV). A normalized Coulomb-gas Hubbard-Stratonovich
representation also divides by its massless nonzero Gaussian partition
function. Its saddle therefore reads

    W_CG = f V + 1/2 log(2 pi uV)
           + 1/2 sum_{n>=2} n^2 log(1+m^2/lambda_n),

with a common regulator for all terms and the appropriate classical
potential minimum included in f. Equivalently it is the full massive
determinant minus the compact massless partition function. The compact
canonical massless reference has

    W_0 = 1/2 log det'(-Delta) - 1/2 log V + constant,
    partial_R W_0 = -1/(2R).

Thus the normalized Coulomb-gas convention adds 1/(6LV)=
1/(12 pi^2 L R^3) to the massive full-determinant stress. This correction
matters if an exact finite-radius answer is asserted, though it supplies
no 1/R. Mixing a normalized zero angle with an unnormalized determinant
without stating the reference can instead generate another R^-3 term.
The local microscopic compact measure, canonical determinant, and
normalized massless reference must not be silently interchanged.

If a matched local coefficient f(R)=f_0+f_1/R is postulated, its direct
stress contribution is (f_0+2f_1/(3R))/L, not (f_0+f_1/R)/L. If
kappa(R)=kappa_0+kappa_1/R with fixed u, then m changes. The flat one-loop
term -m^3/(12 pi) has density coefficient
f_1,loop=m_0^3 kappa_1/(8 pi kappa_0), and its stress coefficient is
(2/3)f_1,loop/L. These are conditional chain-rule facts, not evidence
that such nonlocal 1/R matching coefficients exist. A simultaneous u(R)
also contributes through m^2=u/kappa and the classical minimum.

## B. Mean-zero Coulomb Green function and neutral clusters

The inverse of -Delta on mean-zero functions satisfies
-Delta G=delta-1/V and integral G=0. At geodesic separation r=R chi,

    G_R(chi)=[(pi-chi) cot chi - 1/2]/(4 pi^2 R).

The -1/2 is fixed by the mean-zero condition: the weighted mean of
(pi-chi) cot chi against sin^2 chi dchi is 1/2. At fixed r<<R,

    G_R(r)=1/(4 pi r)-3/(8 pi^2 R)-r/(12 pi R^2)
           +r^2/(12 pi^2 R^3)+O(r^3/R^4).

For energy (C/2) sum_ij q_i q_j G_R(x_i,x_j), including the renormalized
diagonal using the same local subtraction, the constant contribution is

    delta E_(1/R)=-3 C (sum_i q_i)^2/(16 pi^2 R).

It cancels exactly for every neutral finite cluster. If only i!=j
pair terms are retained while diagonal fugacity matching is omitted, a
spurious remainder proportional to sum q_i^2 survives. A consistent
neutral grand ensemble must transform both pair interactions and
self/fugacity terms under a constant shift of G. The next generic
fixed-cluster term is R^-2. No conclusion follows for clusters spanning
the sphere, R-dependent separations, long-range correlations, or a
singular thermodynamic limit without separate control.

## C. Screened Abelian monopole exterior

For the functional specified in the task, a radial three-dimensional
exterior has

    E=2 pi kappa integral_rc^R [r^2 psi'^2+1/r^2+m^2 r^2 psi^2] dr,
    psi(rc)=psi_c, psi(R)=0, m>0.

Writing y=r psi gives y''=m^2 y and

    psi(r)=rc psi_c sinh[m(R-r)]/[r sinh[m(R-rc)]].

Integration by parts gives the exact on-shell result

    E(R)=2 pi kappa [1/rc-1/R+rc psi_c^2
                    +m rc^2 psi_c^2 coth(m(R-rc))],
    E(R)-E(infinity)=-2 pi kappa/R
                    +2 pi kappa m rc^2 psi_c^2[coth(m(R-rc))-1].

For fixed m>0 and m(R-rc)>>1 the electric/scalar boundary response is
exponential and the unscreened magnetic exterior leaves -2 pi kappa/R.
This is a charged insertion with an outer boundary. It is not a closed
neutral ensemble or its physical vacuum stress.

If m->0 at fixed R, m coth(mD)->1/D. For the BPS matching value
psi_c=1/rc, the scalar term contributes +2 pi kappa/(R-rc), cancelling
the magnetic -2 pi kappa/R at order R^-1. Thus m->0 and R->infinity do
not commute for the coefficient of 1/R. A positive screening mass must
not be taken small while still using mR>>1 unless both scales are stated.

At R=infinity and fixed core data,

    E_m(infinity)-E_0(infinity)=2 pi kappa m rc^2 psi_c^2.

For psi_c=1/rc this is +2 pi kappa m. It is the elementary possible
small-m core-cloud correction. It is not an independently derived full
non-Abelian monopole determinant/action: core response, the definition
of the background, matching subtraction and parameter normalization
must be supplied. A stationary matched core can fix the leading term,
but that stationarity and the same microscopic theory must be proved.

## Raw verdict

The leading massive closed Gaussian response is curvature order R^-2,
with convention-dependent algebraic R^-3 reference terms. The charged
screened exterior can have a 1/R action tail. A mean-zero closed
neutral finite cluster cannot inherit the constant Green-function
1/R term when self and pair matching use the same prescription.
None of these objects alone is a derivation of full-QCD de Sitter stress
or of a physical electromagnetic fine-structure constant.
