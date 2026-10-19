# Raw QCD zero-mode derivation, before coordinator comparison

Derived independently of `coordinator/curved_pion/` work. Pure two-flavor
QCD in its chirally broken phase, no QED, equal real positive quark masses
m. The leading chiral action is

    S_chi = integral sqrt(g) [F^2/4 Tr(partial U partial U^dagger)
          - Sigma/2 Tr(m e^(i theta/2) U^dagger + m e^(-i theta/2) U)],
    U in SU(2), Sigma>0, M_pi^2=2m Sigma/F^2.

Retain only constant U, write U=cos(phi)+i n.sigma sin(phi), and normalize
Haar measure so integral dU=1. Put mu=m Sigma V, c=cos(theta/2), z=2mu c.
Then

    Z_tilde = (2/pi) integral_0^pi sin(phi)^2 exp[z cos(phi)] dphi
            = 2 I_1(z)/z,
    Z_chi,LO = N(V) Z_tilde.

N includes matching and the omitted modes, and is not set to one for a
gravitational-energy claim. At this order its undetermined part can be
mass- and theta-independent. Z_tilde is continuous with value one at z=0,
even in z, and 2pi-periodic in theta. Let r(z)=I2(z)/I1(z), interpreted by
continuity at zero. Since d_z log Z_tilde=r(z),

    (1/(2V)) d_m log Z_tilde = Sigma c r(z),
    chi = -(1/V) d_theta^2 log Z_tilde
        = [mu c r(z)/2 - mu^2 sin(theta/2)^2 r'(z)]/V.

In particular at theta=0,

    chi = m Sigma r(2mu)/2
        = (m/2) [per-flavor condensate],
    chi V = mu r(2mu)/2,
    chi V = mu^2/4 + O(mu^4) as mu->0.

The fixed-topology Fourier coefficients are

    Z_nu = I_nu(mu)^2-I_(nu-1)(mu) I_(nu+1)(mu),
    Z_tilde(theta)=sum_nu exp(i nu theta) Z_nu.

The Fourier identity and mass/theta derivatives must be verified by an
independent Haar integral and bounded numerical controls before use.

The normalized Haar integral alone would have metric response

    epsilon_tilde = -d_V log Z_tilde = -2m Sigma c r(z).

Its formal large-mu, theta=0 saddle gives

    Z_tilde ~ exp(2mu)/(2 sqrt(pi) mu^(3/2)),
    epsilon_tilde = -2m Sigma + 3/(2V) + O(1/(m Sigma V^2)).

That 3/(2V) is not an independently physical zero-mode vacuum stress.
Near the saddle use U=exp(i sigma.pi/F). The orthonormal constant-pion
coefficient is q0=sqrt(V) pi=F sqrt(V) phi_vector. A canonical Gaussian
measure product (mu_R/sqrt(2pi)) dq0 gives, relative to normalized Haar
d^3 phi/(2pi^2),

    N0(V) = sqrt(pi/2) (mu_R F sqrt(V))^3.

Multiplying the Haar saddle by N0 gives

    N0 Z_tilde ~ exp(2m Sigma V) (mu_R^2/M_pi^2)^(3/2).

Thus the measure contributes -3/(2V) to the metric response and cancels
the Haar-saddle +3/(2V). The massive constant eigenvalue M_pi^2 itself
is independent of sphere radius. This component is already included if
a full canonical S4 pion determinant includes its n=0 eigenvalue; do not
add it a second time. This local Gaussian comparison fixes a measure
Jacobian, not the entire matching function N(V).

On S4, V=8pi^2/(3H^4). For fixed-positive-mass H->0, M_pi/H diverges:
the epsilon-regime M_pi/H<<1 is lost, so the zero-mode-only formula
cannot determine that limit. A controlled epsilon scaling holds mu=O(1)
while m~V^-1~H^4; this changes the physical quark mass as H changes.
The exact susceptibility/condensate response along that regime is a real
QCD low-energy result, but is not the requested fixed-mass c_H.
