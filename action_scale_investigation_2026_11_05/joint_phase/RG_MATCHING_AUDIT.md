# What the nodal critical point can select

Base: b3268c9114af471b41e313961f92d85e3150b93f. The preceding commit-check
turn added no physics result. This route tests a previously unexecuted
selector for the joint model: interacting criticality. Self-review only.

## Verified source and translation boundary

Geo Jose and Bruno Uchoa, *Quantum critical scaling of gapped phases in
nodal-line semimetals*, [1912.12504v2](https://arxiv.org/html/1912.12504v2),
dated 6 January 2020; checked 5 November 2026. Equations 21, 27, 33, 35,
and 40 give, in the stated one-loop, large-flavor approximation,

    g_tilde^2 = N_f g^2 k_F/(v_r v_z c_0^2 Lambda),
    g_tilde_infinity^2 = 3pi/2,
    d M^2/d ell = (2-eta_phi) M^2,
    delta = 2 + 0.1487 (N_b-2)/N_f + O(1/N_f^2).

The mass eigenvalue is near one and positive in the controlled regime.
The models have N_b=1,2,3 order-parameter components. This is an interacting
fixed point for specified condensed-matter theories, not our curved-space
two-sector model. In particular g_tilde is not our bare h; its normalization
contains velocities, the running cutoff and the nodal radius. No gravity,
baryonic source or vacuum-energy identity is supplied. Source authentication
and equation extraction are verified; transfer of its fixed-point values to
our model is unverified. This is an adjacent result, not a novelty claim.

## Relevant detuning does not follow from an attractive interaction

At a fixed eigenvalue y=2-eta_phi>0, the mass equation integrates to
M^2(ell)=M^2(0) exp(y ell). Setting the interaction to its fixed point does
not set this integration constant. This alone is not a theorem against
universal amplitude ratios: relevant-parameter dependence could cancel in
a correctly matched observable. We therefore check that cancellation in
the specific existing mean-field model, separately from the source RG.

In INDUCED_RESULT.md let u=t/A^2>0. Grant, more strongly than established,
that h, xi, r_B=B/A and x are fixed. Its identities give

    sigma0 = x t/(A h^3),
    F0 = xi x^2 t^2/(A^2 h^6),
    theta = t/F0 = h^6/(xi x^2 u),
    kappa^2 = 128pi xi^3 x^4 u^3/[r_B^2 h^18 (x-1)].

Thus the remaining dimensionless detuning has not cancelled. Fixing F0
does not fix it: for any u>0 the algebraic family

    A = sqrt(F0) h^3/(sqrt(xi) x u),
    t = F0 h^6/(xi x^2 u)

preserves that calibration. The requisite U0 still follows from the
previous stationarity formula; this family is not a microscopic RG flow.
At fixed A and couplings, t approaching zero instead sends F0 to zero.
These are conditional statements about that action, not a no-go for a
genuinely RG-improved action with different scaling of F, U and response.

## The force exponent also needs matching

Suppose a critical equation of state transfers to the polarization with

    W(p)=C p_ref^(2-delta) p^(delta+1)/(delta+1),

where C,p_ref>0 and delta>1. Here delta is an exponent, not the quadratic
coefficient denoted delta in RESULT.md. In the same local, aligned,
unscreened force construction used there,

    g_N=g-p=K W'(p)=K C p_ref^(2-delta) p^delta.

Consequently p dominates g_N as p tends to zero, and

    g ~ [g_N/(K C p_ref^(2-delta))]^(1/delta),
    g^2/g_N ~ (1/(K C)) (p/p_ref)^(2-delta).

An asymptotically constant nonzero MOND acceleration requires delta=2.
Outside a spherical source, g_N=GM/r^2 then implies
v_c^2=r g proportional to r^(1-2/delta). A flat asymptotic rotation curve
again requires delta=2. At delta=2+e its exponent is e/2+O(e^2).
These follow directly by differentiation and spherical flux conservation;
they are not claims that the source's order parameter is gravity.

The three physical polarization components cannot simply be identified
with the source's three spin-order components. Even a matched one-loop
zero correction would not prove an all-orders protected exponent. A
coupled-sector calculation must establish both the exponent and amplitude.

## Decision and continuation

Substituting 3pi/2 for h^2 is invalid. The specific published fixed point
does not provide the missing selector. A new coupled RG calculation is
deferred until a microscopic curved-space embedding and its fields are
specified; there is no such beta-function system to run in the current model.

The algebra suggests a concrete changed construction instead. With a
condensate scale s, let F scale as s^f, cubic coefficient C as s^c and
vacuum U as s^v. The held-background tensor ratio is

    kappa_tensor^2=32pi F^3/(C^2 U),

so scale cancellation requires 3f-2c-v=0. The existing fixed-A model has
(f,c,v)=(2,0,3) and fails this condition. The alternative (1,0,3) passes.
LINEAR_INDUCED_CONTRACT.md tests that changed gravitational coupling,
including scalar exchange; no microscopic origin is assumed for it.
The original coefficient goal remains unresolved.
