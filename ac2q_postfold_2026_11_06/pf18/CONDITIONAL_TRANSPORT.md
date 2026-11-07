# A valid absolute-variation estimate under an additional Osgood condition

This derives a conditional estimate for the actual native gradient equation.
The Osgood hypothesis below is NOT derived from AC2q's evolution. It is not
adopted as a new admissibility rule, and the result is not weak existence.

## Exact native flux in a clock chart

Use tau=phi and a periodic spatial coordinate x, with

    n=r partial_tau+nu partial_x,   e=l^-1 partial_x,
    dVol_2=(l/r) d tau d x,        l>0.

A C1 clock chart exists in PF17's continuous timelike-gradient class. Write
W_sigma for the covariant Riemann-gradient slice measure. Its normal flux
measure is mu_sigma=W_sigma d ell, where d ell=l dx; more explicitly,

    mu_sigma=D_x z_sigma+l omega(e) dx,
    lambda_sigma=nu/r+sigma c/(r l).

The notation W_sigma d ell means this measure, not multiplying two measures.
The conservative native identity from PF16 becomes

    partial_tau mu_sigma+partial_x(lambda_sigma mu_sigma)=q_sigma,
    q_sigma=D_x(F_sigma/r)+(l R_base/(2r)) dx.           (1)

Indeed the volume-weighted source is
r^-1 D_x F_sigma-F_sigma r^-2 D_x r+(l R_base/(2r))dx.
The first two terms combine by the slice continuous-BV product rule. No
characteristic-flow regularity is used for this conversion. PF17 gives

    ||q_sigma(tau)|| <= C(1+Z(tau))^2,
    Z(tau)=sum_sigma ||mu_sigma(tau)||.                 (2)

## Additional transport hypothesis and exact external theorem

Assume the actual continuous acoustic speeds satisfy, on the interval,

    |lambda_sigma(tau,x)-lambda_sigma(tau,y)|
        <= C_sigma(tau) rho(|x-y|),
    C_sigma in L1(time),  integral_(0)^1 ds/rho(s)=infinity,

with rho continuous, increasing and zero at zero. Also assume bounded speeds,
mu_sigma in L-infinity(time; finite signed measures), and q_sigma integrable
in time in measure norm. These are separate hypotheses on an existing solution.

Ambrosio--Bernard, arXiv:0807.1592v1 (10 July 2008), Theorem 1, PDF page 3,
proves signed-measure uniqueness and the pushforward formula under its
quantitative two-sided Osgood condition (O), boundedness (B), and an L-infinity
bound on measure mass. In one spatial dimension (O) is precisely the displayed
modulus estimate. For continuous velocities its flow gives existence for the
linear homogeneous continuity equation. The source theorem is on Euclidean
space; a circle version follows by a smooth circle embedding and a bounded
tangent extension on an annulus, retaining the modulus up to a Lipschitz term.

Primary source inspected: https://arxiv.org/pdf/0807.1592
No full-text local cache or source hash is claimed. A Holder modulus s^alpha,
0<alpha<1, does not satisfy this condition; log-Lipschitz is allowed.

## Forced representation and variation estimate

Let X_sigma(s,t) denote that flow. Define the finite signed measure

    nu_sigma(t)=X_sigma(0,t)#mu_sigma(0)
                 +integral_0^t X_sigma(s,t)#q_sigma(s) ds.

Testing against a smooth function and differentiating its value along each
flow path verifies (1) for nu_sigma, with its stated initial trace. Integrable
source mass and bounded speed justify the integrations. The difference
mu_sigma-nu_sigma solves the homogeneous equation with zero initial measure
and bounded mass. The verified uniqueness theorem makes it zero. Therefore

    ||mu_sigma(t)|| <= ||mu_sigma(0)||
                           +integral_0^t ||q_sigma(s)|| ds,
    Z(t) <= Z(0)+C integral_0^t (1+Z(s))^2 ds.           (3)

Pushforward cannot increase total variation; no multiplication by the sign
of a singular measure is used. On intervals where the denominator is positive,
comparison yields

    1+Z(t) <= (1+Z(0))/(1-C(1+Z(0))t).

This is a genuine conditional native TV estimate, with the source supplied
by the full coupling and transport supplied by the additional modulus bound.
It gives a quantitative bound within the stipulated bounded-mass class;
it does not establish membership of an arbitrary spacetime BV continuation
in that class or produce an approximation lasting beyond breakdown.

## Limits of the implication

The Osgood bound has not been proved dynamically or uniformly through the
breaking packet. Neither compact fields, BV variation, nor mere continuity
supplies it. The state-only density obstruction and (1) in NATIVE_WEIGHT.md
remain consistent with this theorem, which uses a different extra hypothesis.

Uniqueness here is for the linear gradient equation with fixed lambda,q.
Two native solutions generally have different speeds and sources. The theorem
does not compare their self-consistent fields, construct a full Einstein
solution, or prove absence of Cantor derivatives: controlling total mass does
not identify its absolutely continuous and singular components.
