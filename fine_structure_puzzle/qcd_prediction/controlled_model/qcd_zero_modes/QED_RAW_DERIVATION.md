# Independent QED insertion before coordinator comparison

Keep the previous leading two-flavor chiral action and its separate matching
normalization. Let Q=diag(2/3,-1/3), e4^2=4pi alpha, C>0 the independently
matched electromagnetic chiral low-energy constant, and
U=a0+i a.sigma with a0^2+a1^2+a2^2+a3^2=1. Direct Pauli algebra gives

    Tr(Q U Q U^dagger)=5/9-(a1^2+a2^2).

Use the explicit aligned-vacuum-subtracted Dashen action

    S_EM = e4^2 C V [Tr Q^2-Tr(Q U Q U^dagger)] = t s,
    s=a1^2+a2^2, t=e4^2 C V.

The usual unsubtracted Euclidean operator -e4^2 C Tr(Q U Q Udagger)
adds the volume factor exp[(5/9)e4^2 C V] to Z, which must be accounted
for by the same chosen vacuum/matching convention, not hidden as a
prediction. This derivation concerns the subtracted operator. Dynamical
photons, electromagnetic topology and independent source changes of
Sigma,F,C are not included at this order.

The exact finite-dimensional zero-mode integral is

    Z_tilde(mu,theta,t)=integral_SU2 dU exp[z a0-t s],
    z=2mu cos(theta/2).

On the uniform unit three-sphere, s has the uniform Beta(1,1) density.
Conditioned on s, (a0,a3)=sqrt(1-s)(cos psi,sin psi). Hence

    Z_tilde(z,t)=integral_0^1 ds exp(-t s) I0(z sqrt(1-s)).

This exact disk/Bessel representation is finite for every real z,t.
At t=0 it reduces to 2I1(z)/z. At z=0 it is (1-exp(-t))/t.

To first order in t,

    log Z_tilde(z,t)=log Z_tilde(z,0)-t K(z)+O(t^2),
    K(z)=<s>_0=(2/3)[1-<a0^2>_0]=2r(z)/z,
    r=I2(z)/I1(z), K(0)=1/2.

The identity uses r'=1-r^2-3r/z. With theta=0 and fixed V,C,

    C_perflavor/Sigma = r(2mu)-t K'(2mu)+O(t^2),
    chi V = (mu/2)[r(2mu)-t K'(2mu)]+O(t^2).

Thus chi=(m/2)C_perflavor survives the insertion. Indeed it holds to
all orders in this single Dashen operator because m and theta enter
only through z and t is independent of both at this order.

With Sigma,F,C held fixed in this leading-operator calculation,

    d_logalpha logZ_tilde=-t K(z)+O(t^2),
    d_logalpha(C_perflavor/Sigma)=-t K'(z)+O(t^2),
    d_logalpha(chi V)=-(mu t/2)K'(2mu)+O(t^2) at theta=0.

These are unfitted response functions with an explicit unknown matching
coefficient C. They are not a physical alpha selection rule.

For the metric response at fixed m,e4^2,C, both mu and t grow with V.
The first insertion W_EM=t K(z) gives

    delta epsilon_EM = e4^2 C [K(z)+z K'(z)]
                     = 2 e4^2 C r'(z).

At theta=0, large mu, K=1/mu-3/(4mu^2)+..., so the leading t/mu
effective-action correction is volume-independent and drops out of
the metric stress. Its first remainder is
3e4^2 C/(4mu^2). This is a constant-mode-model remainder, not a full
fixed-mass small-H QCD prediction.

The all-t saddle at theta=0 is

    Z_tilde(mu,0,t) ~ exp(2mu)/(2sqrt(pi) sqrt(mu)(mu+t)),
    Z_tilde(mu,0,t)/Z_tilde(mu,0,0) ~ 1/(1+t/mu).

It matches the canonical charged-pair Gaussian: M_charged^2=M_pi^2+
2e4^2C/F^2, so its partition ratio is M_pi^2/M_charged^2=
1/(1+e4^2 C/(m Sigma)), independent of V. The canonical Haar
Jacobian from RAW_DERIVATION is the same, and must not be added again
if the constant pion mode is already in the full determinant.

No coordinator QED derivation has been read before saving this file.
