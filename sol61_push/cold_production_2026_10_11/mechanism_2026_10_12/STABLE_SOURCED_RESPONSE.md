# Stable sourced response in the separate polarization extension

12 October 2026. This closes the finite-spatial-stiffness static-profile gap identified in ../POSITIVE_POLARIZATION.md, in a bounded numerical family, and supplies a fixed-source stability argument. It does not close the microscopic cold-carrier or vacuum-normalization gaps. This is a different action from the unstable dipolar fluid discussed in POLARIZATION_REPAIR_GATE.md.

## One action for the response and its stability

Use the existing nonrelativistic extension with scalar phi and vector P:

    L = Z phi_dot^2/2 + I |P_dot|^2/2 - E - alpha rho_b phi,
    E = a/2 |grad phi-P/a|^2 + beta/3 |P|^3
        + gamma/2 |grad P|^2.

All a, beta, gamma, Z, I and alpha are positive. The baryon density is fixed externally. Neither the fields nor these interaction coefficients have been derived from the protected two-scalar carrier. In particular, choosing the critical square and cubic norm is a phenomenological assumption.

Static variation gives, with D=a grad phi-P,

    div D = alpha rho_b,
    grad phi = P/a + beta |P|P - gamma laplacian P.

For spherical sources, take P=p(r) r_hat, with p nonnegative. Gauss's law fixes D=alpha M_b(<r)/(4 pi r^2). Eliminating phi yields

    -gamma [p''+2p'/r-2p/r^2] + beta p^2 = D/a.

The 2p/r^2 term is essential: this is the vector Laplacian of a radial vector, not the scalar Laplacian of its magnitude. The attractive scalar acceleration has magnitude

    g_s = alpha (D+p)/a.

Thus the stabilizing gradient term changes p and the force together. No unmodified force profile is imposed on the interior.

## Stability about a sourced equilibrium

For a fixed source and fixed outer field boundary values, the source term is linear and has zero second variation. At a stationary solution, writing perturbations as delta phi and delta P gives

    delta^2 H = integral {
      Z delta(phi_dot)^2 + I |delta(P_dot)|^2
      + a |grad(delta phi)-delta P/a|^2
      + beta [|P| |delta P|^2 + (P dot delta P)^2/|P|]
      + gamma |grad(delta P)|^2 } d^3x >= 0.

The cubic Hessian is defined as zero at P=0 by continuity. On a finite domain with perturbations vanishing at the boundary, gamma>0 controls the polarization gradients and the square controls scalar gradients. Poincare's inequality removes constant perturbations; the kinetic terms are positive. Consequently the fixed-source field problem has no exponentially growing linear mode. This argument includes nonspherical field perturbations; it is not just a radial eigenvalue sample.

More generally, convexity makes any stationary solution with the specified boundary data an energy minimum. The conserved relative energy is the sum of positive kinetic energy and the convex energy remainder after its linear tangent is subtracted. This gives stability in the resulting energy norm, assuming sufficiently regular solutions exist. It is not a global PDE existence theorem, pointwise stability guarantee, or a proof of convergence from arbitrary initial conditions. A conservative minimum supports oscillations; attraction to it requires a derived energy-loss or radiation mechanism.

Allowing baryons to move changes the problem. Their density perturbations couple to delta phi, and this fixed-source positivity argument cannot be transferred to the full gravitating matter system.

## Computed profiles with finite stiffness

Choose a Plummer baryon source with total mass M and scale b. Define

    x=r/b,
    B=sqrt(alpha M/(4 pi a beta)),
    p=(B/b) u(x),
    epsilon=gamma/(beta B b).

Then

    -epsilon [u''+2u'/x-2u/x^2] + u|u|
        = x/(1+x^2)^(3/2).

The zero-stiffness profile is u_0=sqrt[x/(1+x^2)^(3/2)]. It has a nonregular central slope. Finite stiffness instead permits a regular u proportional to x at the origin. The numerical boundary-value problem uses inner regularity u'=u/x at a small positive cutoff, and the two-term outer asymptote u(R)=1/R-epsilon/R^2. This outer condition is approximate, not an exact infinite-domain boundary condition.

Five epsilon values were solved on both [1e-4,200] and [1e-5,400]. The following ratios use the latter domain:

| epsilon | u/u_0 at x=1 | at x=10 | at x=30 | at x=100 |
|---:|---:|---:|---:|---:|
| 0.001 | 0.99753 | 0.99990 | 0.99997 | 0.99999 |
| 0.01 | 0.97528 | 0.99897 | 0.99967 | 0.99990 |
| 0.1 | 0.78453 | 0.98964 | 0.99665 | 0.99900 |
| 1 | 0.28477 | 0.88860 | 0.96590 | 0.98995 |
| 10 | 0.04197 | 0.35069 | 0.66123 | 0.89362 |

These are polarization ratios, not ratios of the full force, which also includes D and any ordinary gravity. Spatial stiffness smooths and suppresses the central response. It does not remove the inverse-radius tail in this family. Across x=0.1 to 30 the maximum relative profile change under the joint inner-cutoff and outer-domain check is below 6.1e-7. This is a finite-domain sensitivity diagnostic, not a certified global error bound.

An integrated identity independently checks the radial solve:

    integral [epsilon (x^2 u'^2+2u^2)+x^2 |u|^3] dx
      = integral x^2 f u dx + epsilon [x^2 u u']_inner^outer.

The final ten solves pass the 2e-6 relative identity tolerance as well as positivity and solver convergence checks. All 35 declared checks pass.

## What is predicted, and what is still inserted

For a localized spherical source, asymptotic matching of the differential equation gives

    p(r)=B/r - gamma/(beta r^2) + O(r^-3),
    g_s=G_s M/r^2 + alpha B/(a r)
        - alpha gamma/(a beta r^2) + O(r^-3),
    G_s=alpha^2/(4 pi a).

The inverse-radius term implies

    V_infinity^4 = alpha^3 M/(4 pi a^3 beta) = G_s a_s M,
    a_s=alpha/(beta a^2).

Ordinary Newtonian gravity adds another inverse-square term and does not change this asymptotic coefficient. Matching the observed baryonic relation requires G_s a_s=G_N a0. This relation fixes a free combination of parameters; the calculation does not predict its value. It also does not derive the repo's full interpolation kernel.

The stiffness crossover length is ell_gamma=gamma/(beta B), proportional to M^-1/2 at fixed coefficients. The fractional tail correction is approximately ell_gamma/r. Therefore a common action predicts a mass-dependent onset of the asymptotic response, which could be tested rather than fitted separately for every galaxy. The numerical source scale b adds another finite-size correction.

An indefinitely extended inverse-radius force has logarithmic potential growth and this static field energy has a logarithmic large-radius contribution. An isolated infinite-space configuration is not a finite-total-energy completion. A finite environment or cosmological matching remains necessary; our finite boundaries do not derive it.

Finally, adding a constant vacuum energy to this nongravitating field action leaves both static equations unchanged. Nothing here ties that independent constant to alpha, a or beta. The requested a0=(c/2)sqrt(G rho_DE) therefore remains an extra assumption, not an output.

## Decision and provenance

The constructive result is that the existing phenomenological extension can keep its large-radius mass–velocity scaling with a finite spatial regulator and stable fixed-source field dynamics. The instability of the different dipolar model is not a general obstruction to this construction. The outstanding bridge is to derive this action, its coefficients and its cosmological boundary conditions from actual degrees of freedom, and then test coupled live matter and formation. No new empirical evidence for the carrier is claimed.

Final evidence: sourced_polarization_v3.py, sourced_polarization_contract_v3.json, and sourced_polarization_run_v3/. The initial run failed the integrated identity tolerance for the coarsest epsilon=10 solve. Tightening the BVP tolerance repaired that residual. Version 2 additionally requested 2e-10 tolerance in the extended domain and failed solver convergence for four stiff cases. Both attempts are preserved. Version 3 uses the convergent 2e-8 tolerance on both domains and retains the original physical equations and check thresholds. No result from a failed run is presented as passing. The final manifest validates file provenance; the analytic stability and asymptotic arguments above are separately self-reviewed and are not proved by the numerical pass count.
