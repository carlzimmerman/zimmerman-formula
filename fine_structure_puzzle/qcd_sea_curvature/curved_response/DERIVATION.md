# A calculated unconditioned scalar curvature response of light-quark QCD

FSP-007; parent FSP-006. Calculation and primary-source checks: 2026-10-19.
This lane computes the low-energy two-pion discontinuity of the vacuum
metric functional and a finite, subtracted dispersive kernel. It does not
compute the sphere one-point coefficient A_rho or R(alpha).

## 1. Definition, contacts, and the physical component being calculated

Work first in the ordinary theta=0, unconditioned vacuum of two-flavor QCD,
at positive degenerate quark masses. Match its low-energy theory at fixed
renormalized strong inputs. No fixed topology, prescribed sea determinant,
or normalized theta partition function is used. The pion loop is a
low-energy contribution of dynamical light-quark QCD; it is not a separate
identification of an individual quark-line sea contribution.

Couple a compactly supported, weak conformal metric source on Euclidean R4:
g_mn=exp(2 sigma) delta_mn, W=-log Z, and let Theta=S_sigma at sigma=0.
All source derivatives below are derivatives of the SAME regulated action,
including its measure and matching terms. Exactly,

    W_sigma_sigma = <S_sigma_sigma> - <S_sigma S_sigma>_c.       (1)

The first term is the metric seagull, not a disposable vacuum constant.
With P=Q_E^2 and Delta=-partial^2, write the positive separated-insertion
spectral function as

    Pi_E(P) = integral_0^infinity ds rho_Theta(s)/(s+P)
              + subtraction polynomial,
    rho_Theta(s) = Im Pi_M(s+i0)/pi >= 0.                     (2)

The required renormalizable curved-QCD source counterterms through
dimension four give polynomials through P^2 in this channel. These include
the cosmological, Einstein, curvature-squared and source contact pieces.
The nonlocal piece of W^(2) is -sigma Pi_E sigma/2, with the MINUS sign
fixed by (1). Keeping the seagull is consistent with isolating a cut: a
local source counterterm has no two-particle discontinuity. This is not
the claim that the full one-point stress is a separated trace correlator.

The primary induced-gravity paper Donoghue--Menezes [S5], equations
(7),(8),(10), explicitly retains the two-graviton vertex. Its Appendix,
equation (A2), shows why omitting it changes the cosmological sum rule by
a factor of two. Equations (12)--(17) concern the Einstein term, not a
linear-H coefficient. Their numerical evaluation is gluonic and uses
matched lattice/UV inputs; it is not imported into full light-quark QCD.

## 2. Actual trace vertex and its two-pion cut

The LO chiral action coupled to gravity is fixed by minimal covariantization:

    S_pi = (1/2) sum_a integral sqrt(g)
              [g^mn partial_m pi_a partial_n pi_a + M_a^2 pi_a^2]
           + higher chiral vertices + vacuum local terms.              (3)

There is no freely chosen LO conformal scalar improvement for QCD's
Goldstone pions. This follows directly from the chiral action in [S2],
equation (1); [S1], Section 4, footnote 5, states the same LO restriction.
The NLO curvature operators are treated below, rather than set to zero.

In Minkowski notation the leading trace is
Theta=-(partial pi_a)^2+2 M_a^2 pi_a^2. With relativistically normalized
one-pion states its crossed two-pion matrix element is

    <pi_a(p1) pi_b(p2)|Theta|0>
       = delta_ab [s+2 M_a^2] + O(p^4/F^2),
    s=(p1+p2)^2.                                                (4)

The derivative term and the mass term BOTH enter (4). The source [S1],
equations (5.12),(5.13), explicitly starts with 2 M_pi^2+s at nonzero
mass. [S4], arXiv:2102.00110v2, equations (39),(40), independently fixes
the chiral-limit normalization and multiplicity of the cut.

Two-body phase space, including the identical-real-pion factor, gives

    rho_Theta^pi_pi(s)
       = sum_a [s+2 M_a^2]^2 sqrt(1-4 M_a^2/s)
                   /(32 pi^2) * 1_(s>=4 M_a^2) + higher chiral orders. (5)

There are three real pions. A pi+pi- channel is equivalent to TWO real
species in (5), and the neutral channel to one. For M_a=0, (5) reduces to
3 s^2/(32 pi^2), agreeing with [S4]. The coefficient is not guessed from
the scalar gluon condensate or a susceptibility.

For a generalized improvement c=1-6 xi, replace the amplitude by
c s+2 M^2. This is useful ONLY for keeping the explicitly matched NLO
curvature insertion below; xi=0 at LO QCD. The associated two-pion
spectral cut is

    rho_c(s)=(c s+2 M^2)^2 sqrt(1-4 M^2/s)/(32 pi^2).             (6)

## 3. Finite dispersion calculation, with a bounded EFT option

Subtract the three local Taylor coefficients of Pi at P=0:

    Pi_hat(P)=Pi_E(P)-Pi_E(0)-P Pi_E'(0)-(P^2/2)Pi_E''(0)
             =-P^3 integral ds rho_Theta(s)/[s^3(s+P)].           (7)

For full QCD the last integral is UV convergent under the usual
dimension-four trace asymptotic behavior; its value is not supplied by
ChPT. For a rigorously delimited low-energy CONTRIBUTION, restrict its
two-pion integral to 4 M^2 <= s <= Lambda^2, with Lambda below the chiral
breakdown scale, and retain higher-state/high-energy data as unknown.
Equation (5) on that segment is the LO chiral approximation, not an exact
physical spectral function. No fit of Lambda is made.

Let z=P/M^2 and t=sqrt(1-4 M^2/s). Direct change of variables yields

    integral_(4M^2)^infinity ds rho_c(s)/[s^3(s+P)]
       = J(z,c)/(32 pi^2 M^2),
    J(z,c)=(1/2) integral_0^1 dt
          t^2(2c+1-t^2)^2/[4+z(1-t^2)].                        (8)

For the bounded contribution the upper endpoint is instead
t_Lambda=sqrt(1-4 M^2/Lambda^2). The displayed infinity in (8) defines
the evaluated LO pion loop, not an extrapolation theorem for QCD.

Its third spectral moment is especially simple:

    M3_pi = integral ds rho_c(s)/s^4
          = I(c)/(32 pi^2 M^2),
    I(c)=c^2/6+c/15+1/105,
    I(1)=17/70.                                                (9)

At finite cutoff,

    I_Lambda(c)=(1/8)[(2c+1)^2 t_Lambda^3/3
                      -2(2c+1)t_Lambda^5/5+t_Lambda^7/7].       (10)

This is an evaluated physical low-energy cut contribution. In particular,

    M3_pi,LO = 17/(2240 pi^2) sum_a 1/M_a^2.                   (11)

The coefficient of the leading inverse pion-mass singularity is universal
in the chiral expansion: at FIXED small Lambda, the difference between
(9) and (10) is O(1/Lambda^2), whereas (9) grows as 1/M^2. NLO chiral
amplitude corrections generate at worst the usual less-singular
1/F^2 log(M^2) terms in this power counting. Thus using (11) as a leading
chiral singularity does not assert that the LO amplitude is valid at
arbitrarily large s. At physical quark masses, (10) is the honest
bounded contribution and the full moment still needs higher-order and
high-energy input.

## 4. The nonlocal scalar gravitational response and its sign check

At first order in sigma, R=6 Delta sigma. After the local subtractions in
(7), equations (1),(7) give the scalar quadratic metric functional

    W_hat^(2) = integral R F_hat(Delta) R,
    F_hat(P)=P/(72) integral ds rho_Theta(s)/[s^3(s+P)].          (12)

For each LO real pion,

    F_hat(P) = z J(z,1)/(2304 pi^2),
    F_hat(P) = 17 P/(161280 pi^2 M^2)+O(P^2/M^4).               (13)

The threshold/discontinuity of this form factor is invariant under local
gravity subtractions. The moment and low-P expansion specify a chosen
dispersive matter contribution. An independent local gravitational EFT
term d6 integral R Delta R can shift the total local six-derivative
coefficient. Therefore (13) is NOT the total curvature-six coefficient of
an unspecified gravitational EFT. In particular a cut cannot determine
a local R^3 coefficient.

There is an independent Feynman calculation of the normalization and
Euclidean sign in (12),(13). Set pi=exp(-sigma) chi in the minimal scalar
action. The quadratic operator is

    -partial^2+M^2+V,
    V=(partial^2 sigma)+(partial sigma)^2+M^2(exp(2 sigma)-1),
    V1=(2 M^2-P)sigma.

The one-loop determinant has bubble term -Tr(G V1 G V1)/4. The scalar
bubble difference is -L(z)/(16 pi^2), where

    L(z)=integral_0^1 dx log[1+z x(1-x)].

Removing the local terms through P^2 leaves

    W_hat^(2)=M^4/(64 pi^2) sigma K(z,1) sigma,
    K(z,c)=(2-cz)^2 L(z)-(2/3)z+(1/15+2c/3)z^2,
    K(z,c)=z^3 J(z,c).                                         (14)

For c=1 the z^3 coefficient is 4/420+4/60+1/6=17/70,
independently reproducing (9),(13) including the sign. Local measure
Jacobians and the V2 seagull do not have this two-particle discontinuity;
they remain in the full source functional. The bounded executable
checks compare (8) and (14) at 20 distinct (z,c) points, using exact
rationals for the moment and independent quadratures for the kernels.

## 5. Matched charge-mass effect: a calculated component, not full QED

Use canonical lambda=e^2=4 pi alpha and dimensionless
Qhat=diag(2/3,-1/3), placing e explicitly outside the charge matrix.
At the chosen LO matching point hold M^2=B(mu+md), F and C fixed:

    M0^2=M^2,
    Mplus^2=M^2+2 lambda C/F^2.                                 (15)

This is [S3], equations (5),(8),(40). The sentence immediately following
its equation (40) explicitly notes the convention dependence of the
strong/EM mass decomposition. We use no measured pion mass split to fix
C. Holding a measured charged or neutral pion mass fixed by retuning
quark masses changes the path and must be converted separately.

The mass-shift piece of the LO loop moment at FINITE lambda is

    M3_mass(lambda)=17/(2240 pi^2)
       [1/M^2+2/(M^2+2 lambda C/F^2)].                          (16)

Writing y=2 lambda C/(F^2 M^2), its ratio to lambda=0 is
[1+2/(1+y)]/3. This is a calculated dimensionless function with unfitted
conditional QCD inputs. Its derivative, solely as a derivative of this
selected component, is

    dM3_mass/dlambda|0 = -17 C/(560 pi^2 F^2 M^4).               (17)

Differentiating only phase space and keeping s+2 M^2 fixed would be
wrong even for this component: the trace vertex in (4) changes as well.
Equation (16) includes both changes. It is a mass-resummed LO chiral
expression, not an all-orders finite-charge QCD+QED result.

The electromagnetic trace audit identifies exact independent missing
terms rather than silently assigning them to the mass split. In [S1],
Section 4, equations (4.1),(4.7),(4.8), the NLO curved chiral action has

    l11 R <D U D Udagger> + l12 R_mn <D^m U D^n Udagger>
      + l13 R <chi Udagger+U chi_dagger>,
    lambda F^2 k15^r R <Qhat U Qhat Udagger>,                  (18)
    beta15=1/2+2 Z/3,  Z=C/F^4.

We display the explicit lambda in our charge convention. The raw
spurion notation in [S1] suppresses it in (4.7) while its charge matrix
is displayed dimensionlessly. The normalization in our (18) is pinned
by the explicit-e mass equation (2.7) and charged trace equation (5.12),
not by adding an extra factor of e to their already explicit-e formulas.

The operator k15 in (18) is an INDEPENDENT QCD+QED matching constant;
its running does not fix its finite part. It is not a pure gravitational
identity counterterm. Expanding its flavor trace gives

    <Qhat U Qhat Udagger>
        = <Qhat^2> - (pi1^2+pi2^2)/F^2+O(pi^4),
    xi_charged=-2 lambda k15^r,
    c_charged=1+12 lambda k15^r.                                (19)

This matches the k15 part of [S1], (5.12): using their (2.5),(4.8),

    12 lambda k15^r(mu) s
       = lambda/(16 pi^2)(3+4Z)s
             [kbar15+log(M0^2/mu^2)].                          (20)

The source combines this with loop logarithms so that its final term is
lambda/(16 pi^2)(3+4Z)s[kbar15+2 log(Mplus/M0)].
Thus the independently matched curvature vertex affects the two-pion
cut, not just a removable vacuum normalization. With our loop moment,
its isolated insertion gives

    dM3/dlambda|0, k15 = 3 k15^r/(10 pi^2 M^2),                 (21)

in addition to (17). Equations (17),(21) are checked exact coefficients;
(21) alone is scale dependent and only becomes part of a physical
prediction together with the accompanying photon/chiral loops. Its
chiral order is higher than the mass-resummed LO pion loop.

Equation (5.12) also has photon functions Kplus,G, infrared logarithms,
and strong curvature constants l11,l12,l13. Sections 6.2, equations
(6.4)--(6.7), require the corresponding real-photon states for an
infrared finite inclusive spectral density. An exclusive charged-pion
matrix element squared is insufficient beyond LO. Full QCD+QED also
has photon intermediate states; the pion threshold in (5) is not a gap
theorem for that full theory. Charge renormalization is represented
explicitly by [S1], equations (2.9)--(2.11), and has not been used here
to identify a Thomson alpha. These restrictions prevent (16) from
being promoted to a complete alpha response.

## 6. Mixed metric/current contacts in one common regulator

For any action parameter lambda, the exact mixed metric response is

    W_sigma1_sigma2_lambda
      = <S_sigma1_sigma2_lambda>
        - Cov(S_sigma1_sigma2,S_lambda)
        - Cov(S_sigma1_lambda,S_sigma2)
        - Cov(S_sigma1,S_sigma2_lambda)
        + kappa3(S_sigma1,S_sigma2,S_lambda).                  (22)

This follows by differentiating (1) once, before removing the
regulator. At zero charge, S_lambda is the full integrated-current
insertion I=(1/2)J D_g J+I_ct in the frozen parent convention. Its
metric derivatives include photon-kernel, measure, current, mass-path
and UV-contact derivatives. At finite charge one must use the full
matched action and all orders, not extrapolate the zero-charge
insertion by assumption. Equations (18)--(21) show explicitly where a
real curvature matching coefficient enters this common source
functional. Neither connected flat trace covariance nor the pion mass
split determines every term in (22).

## 7. What follows for H, and what does not

The calculated quantity is a weak, inhomogeneous scalar metric response
around flat R4 at specified momenta. It is not a sphere vacuum energy.
For fixed positive pion masses its calculated kernel (8) is regular at
P=0. The leading dispersive term is R Delta R/M^2. On the ROUND S4,
R=12 H^2 is constant, so Delta R=0 and this derivative term vanishes.
No substitution P=H^2 in (12) is a valid way to manufacture a sphere
one-point energy. Pure curvature-cubic terms, the global/state sector,
and the homogeneous mode are independent of this flat quadratic
calculation.

The new k15 operator is also not a freedom to tune A_rho. At one pion
loop, its leading homogeneous insertion has the form

    delta W = (1/2) sum_charged delta xi integral sqrt(g) R G_M(x,x),
    G_M,flat^ren = M^2/(16 pi^2)[log(M^2/mu^2)-1].              (23)

It starts with R M^2, followed by R^2 and higher integer curvature
powers in the local positive-mass expansion. On the sphere these are
H^2,H^4,H^6,... . Local subtraction dependence and the full matching
must be retained; their coefficients are not presented as universal.
None of these terms has a linear-H projection. The dispersive
nonlocal kernel remains an independently observable finite response,
but its missing k15 input does not by itself obstruct or freely shift
A_rho. A proposed nonanalytic/global linear-H effect needs its OWN
microscopic calculation; it is not established or excluded by (23).

For reference, [S6], arXiv:1812.00460v2, equations (4),(7)--(13),
separates the free massive-field determinant, required local terms,
and quadratic curvature form factors. Its Introduction explicitly
explains the limitation of trying to infer a cosmological-constant
running from these form factors. We use that source for scope,
not to transfer a free-field theorem to global QCD.

We take no M->0, lambda->0 and H->0 interchange. The chiral singularity
test in Section 3 is a statement about the flat spectral observable;
it is not used to determine an H limit at finite charge.

## 8. Exact remaining inputs and a falsifiable next calculation

To extend the present finite response, the independently required data
are the timelike pion TRACE form factors and their inclusive radiative
completion, or equivalently matched l11,l12,l13,k15 and the relevant
photon counterterms, plus the nonpionic spectral tail. The k15 term
can be fixed from the charged-pion gravitational/trace slope after
the other terms in [S1], (5.12), are matched. It cannot be fixed from
the charged-neutral mass difference alone.

A cheap discriminating lattice/continuum check is the unconditioned
flat trace correlator at positive quark masses in a common regulator,
with metric seagulls matched as in (1). Measure its third momentum
derivative (or the spectral segment below a fixed cutoff), and compare
the mass dependence with (9)--(11). At e=0 the leading chiral prediction is

    lim_(M^2->0) M^2[-Pi_E'''(0)/6] = 51/(2240 pi^2),           (24)

for two degenerate light flavors, in the stated matter-subtraction
convention. Higher local gravitational EFT operators must be specified
or removed when extracting a dispersive moment from a full source
response. A successful (24) validates a real QCD curvature-response
component and its operator normalization. It does not validate A_rho.

For the target A_rho itself the still-independent datum is the
unconditioned, renormalized integrated ONE-POINT stress of the actual
globally curved ensemble, at fixed nonzero full charge and one common
matching path, across a radius sequence with the specified regular
state. No spectral datum acquired here supplies that global functional
or a uniform reconstruction of it. The parent's direct sphere
prescription remains the appropriate target test. A bounded primary
search found no new unquenched curved-QCD stress dataset that supplies
this datum. That is a stated search limit, not a nonexistence theorem.

## 9. Reproduction and calibration audit

Run the bounded, dependency-free script from the repository root:

    python3 fine_structure_puzzle/qcd_sea_curvature/curved_response/checks/check_trace_cut.py

The script checks exact rational phase-space/Feynman coefficients,
20 kernel comparisons, five cutoff integrals, and six finite-charge
dimensionless mass scenarios. It contains no empirical alpha, Hubble
scale, proton mass, pion mass, condensate, or fitted LEC. C,F,M,k15
remain declared matching inputs. The cutoff ratios are quadrature
scenarios, not physically calibrated data. No result supplies the
numerator or denominator of R=A_rho/m_p^3.

Input snapshots and hashes are in INPUTS.json; primary-source versions,
locators, interpretation and PDF/text receipts are in SOURCES.json.
Full source material is retained only in /private/tmp, not copied into
the project. The check manifest records the actual argv, version,
input/output hashes and run status; Git metadata is explicitly
unobserved under the task's no-Git instruction.
