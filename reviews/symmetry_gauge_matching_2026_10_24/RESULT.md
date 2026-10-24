# Symmetry and gauge matching: result

No parameter-free quantum-gravity mechanism has been established. This continuation isolates why two unusually close proposals do not yet supply one. Kappa=1/2 remains FITTED; CFG493 kappa_Lambda=0.417 +/- 0.095 and kappa_crit=0.345 +/- 0.078 are separate and unused. Dark-energy footing throughout.

## Authenticated source boundaries

[A Relativistic MOND, arXiv:2601.04290v1](https://arxiv.org/html/2601.04290v1), equations 3,5,9-15 and sections 4-7: a proposed gauge-gravity origin, de Sitter vacuum and conformal static limit. The displayed action imposes the AQUAL deformation; neither the vacuum-selection dynamics nor numerical matching factor xi is calculated. Covariant completion is explicitly open. This is not an established quantum-gravity matching calculation.

[Non-Abelian graviphoton EFT, arXiv:2502.14686v1](https://arxiv.org/html/2502.14686v1), equations 12-13,50-61,74-77: a classical polarization mechanism with cubic gauge interaction and minimal baryonic gravity. Linear-response cancellation is imposed through a particle-ratio sum rule. The displayed one-dimensional stationary approximation retains oscillation amplitudes and phase in a0; their universality is conjectured. Vacuum and EFT scales are related by order of magnitude, not a fixed coefficient. Version identification follows the URL/header, despite a later date rendered in the page body.

These short source cards are applicability audits, not independent verification of the papers' entire dynamics or health claims.

## Own symmetry diagnostic

Let h_ij -> Omega^2 h_ij on an n-dimensional spatial slice, theta have weight zero, and J=|grad theta|. Then sqrt(h) J^n is locally Weyl invariant as a background-metric functional. For n=3 this is precisely the cubic static operator. A quadratic term has weight n-2, so the bare three-dimensional construction excludes it. Multiplying the invariant by any C preserves that symmetry. An external source density transforming as rho -> Omega^(-n) rho permits q sqrt(h) rho theta for any q. This statement does not establish conformal invariance of dynamical massive baryons.

An invariant vacuum scale requires additional structure. In the compensator test, chi -> Omega^(-1) chi and N -> Omega^z N, so each of

    N sqrt(h) lambda chi^(n+z)
    N sqrt(h) Z chi^(n+z-2) J^2

is invariant. In the static n=3,z=0 case these are lambda chi^3 and Z chi J^2 under the measure. A nonzero compensator background therefore permits a quadratic response with an independent coefficient. The symmetry does not require it to be generated, but cannot by itself forbid it. For general z the bare J^n operator is not invariant under the full ADM measure; this is explicitly a static-sector test, not a constructed relativistic theory.

Thus the simple conformal route has a precise gap: its protection in the scale-free static sector does not automatically survive the structure used to introduce the vacuum and baryonic scales. A different symmetry, extra constraint or interacting dynamics could evade this conditional diagnostic. Anomalies, composite-operator dimensions, and a full matter/vacuum matching calculation are not computed here. The earlier integrable-Weyl model audit is a separate result, not claimed as newly discovered.

## Own matching diagnostic for the cited gauge coefficients

Write u_a=eta_a^(-2)>0, t=-sin(theta23)>0 on the positive-force branch, and lambda_v=Lambda alpha^2>0. The source formula becomes

    a0 = 8 c^2 / [3 alpha k2 k3 t sqrt(u1 u2 u3)].
    rho_DE = Lambda c^2/(8 pi G).

Consequently

    kappa = a0/[c sqrt(G rho_DE)]
          = 8 sqrt(8 pi)/[3 k2 k3 t sqrt(lambda_v u1 u2 u3)].

The common length alpha cancels, but a dimensionless amplitude remains. Even granting exact cancellation u1+u2+u3=1, neither lambda_v nor the initial amplitudes are fixed by that equation. In particular

    d ln kappa/d ln lambda_v = -1/2,
    d ln kappa/d ln k2 = -1,
    d ln kappa/d ln t = -1.

On the particle cancellation surface u3=1-u1-u2,

    partial_(u1) ln(kappa^2) = -1/u1 + 1/(1-u1-u2).

This is generically nonzero. Cancellation alone does not select even the particle contribution to the amplitude. This does not prove all such deformations have UV completions; it identifies freedoms not removed by the published EFT and its stated conditions. Changing lambda_v preserves its order-of-magnitude relation without supplying a radiatively protected vacuum prescription.

## Residual-response discriminator

For the separate, explicitly isotropic constitutive hypothesis

    D = delta g + g^2/a0,  delta>=0,

spherical flux gives D=g_N and

    g = [sqrt(a0^2 delta^2 + 4 a0 g_N) - a0 delta]/2.

For delta>0, the lowest-gradient force is g~g_N/delta; for delta=0 it is sqrt(a0 g_N). The relative unwanted linear response is delta a0/g. A finite observed MOND interval therefore requires delta << g/a0 throughout that interval, not merely a qualitative near-cancellation. Here delta corresponds to 1-sum(u_a) in the published linear coefficient, but isotropy and a spherical gauge solution have not been derived from that paper. Negative delta branches and their stability are outside this calculation.

## Verification and next evidential threshold

All 15 frozen symbolic checks pass. The separate mutation changes the bare conformal exponent and doubles the vacuum density: exactly two baseline assertions fail, exit status 1 as required. These are algebraic diagnostics, not simulations, an RG integration, a stability proof, or an independent reproduction of the full source models.

What would constitute progress beyond this result is a microscopic equation or Ward identity tying the vacuum coefficient, the cubic response and the physical baryonic normalization together while making the residual linear response vanish or remain sufficiently suppressed under quantum corrections. An attractor for the gauge model would also have to erase the displayed initial-amplitude dependence. Imposing those conditions as a boundary value or choosing a special stationary state is not their derivation. No such joint identity or attractor has been obtained here.
