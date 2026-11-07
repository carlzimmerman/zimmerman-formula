# Native constraint bounds do not supply a uniform Osgood modulus

This tests an implication from the already controlled slice quantities. It is
not a postbreak solution, a counterexample to dynamical regularization, or a
nonexistence theorem.

Take a fixed periodic proper slice, theta=0, constant alpha=beta=0 and E_beta=0.
Choose r0=1, gamma=1/10 and the homogeneous auxiliary value A0=11/10, P0=0.
Take B nonzero and constant. For small fixed delta>0 prescribe

    r_epsilon(x)=1+delta chi(x)
                    [(x^2+epsilon^2)^(a/2)-epsilon^a], 0<a<1,

where chi is a smooth nonnegative periodic cutoff equal to one near x=0 and
supported in a fixed coordinate interval. Each epsilon>0 gives a smooth
clock profile with uniform small amplitude and total variation. As epsilon
vanishes it converges uniformly to the continuous BV cusp
1+delta chi(x)|x|^a.

The PF14 local periodic auxiliary reconstruction gives A_epsilon,P_epsilon
with uniform spatial Lipschitz and compact-domain bounds, independent of the
clock slope. Set the longitudinal expansion by the Hamiltonian constraint

    K_epsilon=(energy_density_epsilon/M-B^2)/(2B).

The momentum constraint is satisfied because eB=0 and E_beta=0. The initial
conformal metric derivatives realize this K and B, exactly as in PF09's
constraint-compatible initial-family construction. Each positive-epsilon
member is legitimate finite-regularity native initial data. This makes no
assertion that its lifespan, stronger moduli, or the limit's spacetime metric
regularity remain uniform. The native hold-law cusp is not called C-infinity.

At this slice the speed in the C1 clock chart of CONDITIONAL_TRANSPORT.md is

    lambda_sigma= sigma c(r_epsilon,A_epsilon)/r_epsilon.

There is a nonzero dependence on r that cannot be hidden in the auxiliary
response. At the stated homogeneous point,

    c^2=10/91,
    partial_r(c^2)=7911/8281,
    partial_r(c^2/r^2)=6091/8281>0.

These are exact differentiations of c^2=h/(rR), holding A fixed, with h=1,
R=91/10 and R_r=-27/5. Thus partial_r(c/r)>0 in a small common neighborhood.
Because A_epsilon is uniformly Lipschitz, the mean-value formula gives, for
small s>0 near zero,

    |lambda_sigma(s)-lambda_sigma(0)|
      >= k delta[(s^2+epsilon^2)^(a/2)-epsilon^a]-C s,

with k>0 and uniform constants. If a common modulus rho and finite constant L
controlled all these speeds, passing epsilon to zero would imply

    L rho(s)>=k delta s^a-C s>= (k delta/2)s^a

for sufficiently small s. This forces integral_0 ds/rho(s)<infinity near
zero, contradicting the Osgood condition. A modulus used here is positive
away from zero, so no divergence can be hidden elsewhere in its domain.

Therefore the native initial constraints plus the compact, amplitude and
variation bounds do not yield a uniform Osgood modulus estimate. Every
positive-epsilon speed is individually Lipschitz, with constants allowed to
deteriorate. The limiting cusp is only a slice-level test, not a constructed
native weak evolution. The time-integrable modulus required by the conditional
transport theorem might still follow from an additional dynamical mechanism;
no such mechanism is established by this test.
