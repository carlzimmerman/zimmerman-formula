# Independent review: covariant response and four-form residual

Verdict: the report's normalized leading P2 response, classical form
constraints, residual ratio and exact affine-band cancellation are correct
under its explicit branch and boundary assumptions. No concrete algebraic
error remains in the reviewed version. The correction -K<L_K>/2 is necessary.
This is a counterfamily at action/background/leading-static level, not a
healthy completed galaxy/cosmology theory.

Reviewed source hashes (SHA256):

- `vacuum_constraint/REPORT.md`: `71b1a3abbbd1892cfb97d000fe943e32fe081b8da8dcc0f76630214a01d58c10`
- `vacuum_constraint/checks.py`: `72e7638c743d3c43b947a4967f432c8cbed10691302a78173b3834bc16141e87`

Paths are relative to `sol61_push/puzzle_32pi/selection_2026_10_06/`.
I read the actual source and reconstructed the variations, rather than using
the assertion count. No peer files were executed or changed.

## Source normalization and the covariant term

The term -2 M^2[W(s)-s^2/2] is covariant for the explicitly declared unit
foliation vector; it is not a Lorentz-invariant scalar with no preferred
background. In the weak static branch s=|grad Phi|, eliminating the ordinary
second metric potential from Einstein gravity produces -K|grad Phi|^2.
At the declared branch K=M^2, the sum is exactly -2K W(s). Hence varying Phi
in -2K W-rho_b Phi gives

    2K div[W_s grad Phi/s]=rho_b.

With G=1/(8piK), this is div[W_s grad Phi/s]=4piG rho_b. Differentiation of
the stated W gives W_s=sqrt(s^2+a0^2/4)-a0/2=b; therefore its spherical Gauss
match b=GM_b(<r)/r^2 yields s^2=b^2+a0 b. Both the Newton normalization and
the deep coefficient are correct. The factor 2 in L_resp matters: removing
it would leave an uncanceled quadratic term and would not give this law.
Independent Sympy differentiation checks the W derivative, the cancellation
of static quadratic terms and a0 W_a0=2W-sW_s.

For geodesic comoving FRW foliation, acceleration vanishes. W=s^3/(3a0)+
higher terms near zero, so W-s^2/2 starts as -s^2/2. Its value and first
variation vanish at zero acceleration even though its quadratic variation
does not. Thus no background stress or foliation source is left on that
FRW vacuum branch. This supplies a background consistency check, not the
missing kinetic/constraint health theorem. The report correctly states that
critical static quadratic cancellation needs that separate audit. G's tensor
normalization follows from K; identifying all high-frequency gravitational
or matter observables still requires the preferred-sector analysis.

## Form variations and residual curvature

Using the report's plus L_m convention with vacuum L_m=-V, scalar variations
for a response independent of Lambda,K yield

    (sigma'/mu^4)F=vol_g,
    (sigmahat'/M^2)Fhat=-R vol_g/2.

Three-form variations require constant Lambda,K only where both derivatives
are nonzero. The metric equation is K G=T-Lambda g on that branch; its trace
is -K R=T-4Lambda. With a common regulated average,

    Lambda=<T>/4+Delta,
    Delta=K<R>/4
         =-mu^4 K sigmahat' Qhat/(2M^2 sigma' Q).

For T=-4V+tau, the explicit -V cancels in the projected metric equation. In
pure vacuum the actual geometric curvature coefficient is Delta/K, not the
bare Lambda. Dividing by the action-declared a0^2=zeta^2 mu^4/M^2 gives

    C=-(sigmahat'/sigma')(Qhat/Q)/(2zeta^2).

This confirms the missing selector (sigmahat'/sigma')(Qhat/Q)=-64pi zeta^2.
The form equations determine how a chosen curvature and flux ratio match;
they do not prescribe that particular dimensionless ratio.

I also checked the publisher's primary text, Kaloper et al.,
[PRL 116, 051302](https://harvest.aps.org/v2/journals/articles/10.1103/PhysRevLett.116.051302/fulltext).
Its local construction and arbitrary residual integration data agree with the
scope claimed. It does not furnish the proposed MOND scale relation or a
32pi selector.

## Exact shift band and changed-scale derivative

The displayed sigma is smooth, globally nonlinear and has sigma'=1 exactly
on the open band; sigmahat'=K/M^2 is nonzero at K=M^2. Inside that band,
V increases by deltaV while Lambda decreases by deltaV. The bulk combination
-Lambda-V, all local field equations and both form strengths remain unchanged
at fixed metric,K and response fields. The topological action changes by a
constant times the fixed form flux; with fixed-flux boundary variations this
does not change the equations. A global change crossing the band boundary
would not have this property. The report correctly distinguishes this exact
mapping from generic nonlinear radiative stability and from fixed independent
fluxes determining every integration parameter.

For FRW de Sitter the form fields are constant multiples of vol_g. The ratio
Qhat/Q is therefore a pointwise fixed ratio under any *common* finite
regulator. Extending both integrals to infinity does not require taking an
undefined ratio of independently regulated infinities. A new gravitational
boundary action or flux quantization would be additional premises.

If a0^2=epsilon Lambda/K is put into the action instead, variations give

    (sigma'/mu^4)F=(1-L_Lambda)vol_g,
    (sigmahat'/M^2)Fhat=-(R/2+L_K)vol_g.

Averaging and solving yields

    Delta=-K<L_K>/2
          -mu^4 K sigmahat' (Qhat/Q)(1-<L_Lambda>)/(2M^2 sigma').

The first term has factor 1/2, not 1/4. Homogeneity of W gives precisely
L_Lambda=-(M^2/Lambda)(2W-sW_s) and
L_K=(M^2/K)(2W-sW_s), since the reference M^2 is held fixed. On a vacuum
branch these vanish, but a0 then depends on bare Lambda=Delta-V; at fixed
geometry/fluxes its squared scale shifts by -epsilon deltaV/K. This repair
therefore loses vacuum-independent force normalization rather than selecting
the desired coefficient. Substituting the on-shell invariant Delta into an
off-shell local action would require a new implementing constraint.

The missing implication remains a derived boundary-state/flux selector plus
full response perturbative health. Exact cancellation of matter vacuum shifts
is insufficient to supply either. This review supports the report's scoped
negative result and does not promote its unaudited preferred-foliation action
to a physical completion.
