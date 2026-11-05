# Joint phase energy and MOND response: exact conditional calculation

This new continuation computes both quantities from the explicitly specified
spectral-parent potential in CONTRACT.md. It does not derive the coefficient,
fix the absolute vacuum energy, or supply a healthy covariant completion.
Kappa=1/2 remains fitted. All review is self-review.

For positive A,B,t,h, the nonzero-amplitude stationary branch is

    sigma^2=(t/A)^2-h^2 p^2, 0<=p<p_c=t/(Ah).

Its amplitude curvature is t[1-(p/p_c)^2]>0. Eliminating sigma gives exactly

    U_eff=U0-t^3/(6A^2)+delta p^2/2+B h^3 p^3/3.

Thus the same calculation produces the condensed vacuum energy and the
nonlinear response coefficient:

    epsilon_cond=U0-t^3/(6A^2), C3=B h^3.

The energy difference from the uncondensed origin is Delta epsilon=t^3/(6A^2).
It is independent of the additive offset. However the origin has amplitude
curvature -t and is unstable, not a metastable dark-energy state. Equating
this positive energy difference with gravitating dark energy is unjustified.
Positive epsilon_cond requires U0>t^3/(6A^2); the model has not fixed U0.

For the specified leading static coupling, variation gives

    g_N=g-p=K(delta p+C3 p^2), K=4pi G.

On the conditional delta=0 slice,

    g=g_N+sqrt(a_MOND g_N), a_MOND=1/(K B h^3).

This force relation differs from the adopted simple-mu interpolation even
though their deep limits have the same exponent. For delta>0, the strict
infrared response is instead linear:

    g/g_N -> (1+K delta)/(K delta), g^2/g_N -> 0.

The second gapless sector distinguishes p from sigma, so the radial symmetry
of the first sector does not protect delta=0 in the combined construction.
The potential is stipulated after renormalization; no full loop protection
or beta-function calculation was performed.

At p=p_c the amplitude curvature vanishes. The sigma=0 branch above this
point has

    U_above=U0+(delta-t h^2)p^2/2+(A+B)h^3 p^3/3.

Both energy and first derivative join continuously. The closing amplitude
gap invalidates an adiabatic elimination arbitrarily close to the endpoint.
This is a concrete extra prediction of the conditional construction, not
a measured feature or a completed physical model.

If epsilon_cond were justified as dark energy, the resulting ratio would be

    kappa^2=1/[K^2 B^2 h^6 G (U0-t^3/(6A^2))].

Its derivative with respect to U0 is nonzero. Even the unjustified
phase-gap identification would leave

    a_MOND^2/(G Delta epsilon)=24pi(B/A)/lambda_phase^3,
    lambda_phase=p_c/a_MOND=K B t h^2/A.

No coefficient has been selected; no target number was supplied upstream.
The calculation advances the explicit joint construction but exposes two
remaining requirements: protected criticality and absolute vacuum matching.
An isotropic gravitational embedding and full dynamical health are also
absent. The previous nodal-medium calculation, CFG900, did not include this
dynamical condensed branch; its free-vacuum warning still applies.

Evidence: calculate.py, main and mutation manifests/results. Main passes17
exact checks. Deliberately omitting delta fails exactly the full-force and
noncritical-infrared checks. No numerical scan, empirical fit, or coefficient
campaign hit is claimed.

## Source boundary

[Jose and Uchoa, arXiv1912.12504v2](https://arxiv.org/html/1912.12504v2),
sectionII equations(1)-(6), supplies a primary example of nodal-loop Yukawa
models with order parameters and anticommuting gap terms. Its enlarged
Hilbert-space discussion permits additional mass structures in principle.
It does not supply this combined potential, its gravitational coupling,
its absolute vacuum energy, or a MOND prediction. Those are hypotheses of
this feasibility calculation. The subtracted cone integral used here was
derived directly and checked symbolically. The source was read in HTML;
no downloaded source or archived-source hash is claimed.
