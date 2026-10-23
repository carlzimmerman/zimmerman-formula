# A finite-stiffness spherical background and central regularization

The reduced weak-field, fixed-baryon energy now has numerical spherical stationary backgrounds, rather than an arbitrarily imposed polarization profile. Finite stiffness changes the central behavior qualitatively: regular polarization is proportional to radius and its effective gravitational density is finite. This supplies a background for a later perturbation calculation; it is not yet a full A33 metric/clock/cold-sector solution or a mechanism of formation.

## Equation and boundaries

Using the energy and conventions in NONLINEAR_WEAK_RESULT.md, let s=r/R, q=K P/a0, epsilon²=gamma/(K R²), and prescribe a Plummer baryonic source

    gN/a0 = A s/(1+s²)^(3/2), A=GM/(a0 R²).

Radial vector stationarity gives

    epsilon² (q''+2q'/s-2q/s²) = q²/(1-q)-A s/(1+s²)^(3/2).

The -2q/s² term is essential: this is a radial vector, not a scalar amplitude obeying a scalar Laplacian. The gravitational field follows from the same reduced Poisson equation, g=gN+a0 q. The calculation used A=1, inner radius 1e-5, regular leading boundary q'=q/s, and outer q'=-q/s at 100 or 200. The latter is a leading asymptotic condition, not an exact cosmological boundary.

## Numerical evidence

All three runs converged with q between zero and one on the tested interval. Tightening tolerance from 1e-6 to 2e-8 changed the profile by at most 2.01e-9 on 1e-4<=s<=50. Doubling the outer radius changed it by at most 1.58e-9 there. An original-equation residual evaluated using derivatives of the collocation interpolant is below 2.95e-9. This residual is an equation check, not an independent numerical method. Inner-cutoff convergence and a rigorous error bound remain untested.

| epsilon | central q/s estimate | q at s=0.01 | q at s=1 |
|---|---:|---:|---:|
| 0.03 | 2.94213 | 0.0293156 | 0.443065 |
| 0.1 | 1.64619 | 0.0164521 | 0.438122 |
| 0.3 | 0.832837 | 0.00832726 | 0.392240 |

The algebraic zero-stiffness solution has q=0.0951181 at s=0.01 and 0.443549 at s=1. Thus stiffness is a small correction outside the central transition for the smallest epsilon, but cannot be omitted uniformly at the centre.

## Central insight

For smooth nonzero central baryonic density, gN/a0~A s. The algebraic relation yields q~sqrt(A s), so its radial vector is not differentiable at the origin and its effective polarization density diverges as s^(-1/2). Finite stiffness permits a regular branch

    q(s)=c s - A s³/(10 epsilon²) + c² s⁴/(18 epsilon²)+... .

The coefficient c is determined by the global boundary problem, not by the local expansion. In the reduced Poisson equation,

    rho_pol = (a0/(K R)) (q'+2q/s),

so rho_pol(0)=3c a0/(K R) is finite on this branch. The s⁴ term means this expansion should not be described as an analytic radial vector at all orders; the underlying |P|³ potential limits smoothness. It is sufficient for a finite density and the displayed differential equation.

Balancing the gradient term of q~sqrt(A s) with the source suggests

    s_core ~ epsilon^(4/5) A^(-1/5),
    r_core ~ (gamma/K)^(2/5) (a0 R³/(GM))^(1/5).

These are transition scaling estimates, not measured core radii or fitted observational relations. The numerical run did not test the scaling exponent across A or define a core threshold. In the inherited gamma=K Lstar²/2 convention, the length depends on both Lstar and the central source density; it is not a universal fixed core size. No new length parameter was inserted into this equation.

## Verification and limits

spherical_run/manifest.json validates; five checks pass. The mutation deleting radial vector curvature fails the original-equation residual while solving its altered equation, establishing that the residual test distinguishes these operators. Source: spherical_background.py. The pre-computation scope and tolerances are in SPHERICAL_CONTRACT.md. Review is self-review.

This is a candidate structural benefit of the existing gradient term, not evidence of novelty. The baryonic profile is prescribed, the cold component is absent, and the finite-polarization kinetic/constraint reduction remains approximate. Positive energy at a fixed-source minimum does not establish settling. The next calculation must use the radial Hessian around these backgrounds, retain the spherical geometry and kinetic operator, and impose an outgoing exterior. It must distinguish radiative loss from instability and eventually include matter backreaction. Existing Solar-System and cold-sourcing obstacles remain unresolved.
