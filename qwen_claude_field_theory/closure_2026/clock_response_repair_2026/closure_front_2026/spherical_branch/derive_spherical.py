#!/usr/bin/env python3
"""Bounded exact spherical current and small-source discriminants.

Frozen coefficients, signature -+++, no fitted parameters. This computes
necessary local identities, not a global metric/clock/matter solution.
"""
import json
import platform
import sympy as S


def derive():
    checks = {}

    def zero(name, expr):
        residue = S.simplify(expr)
        checks[name] = residue == 0
        if residue != 0:
            raise AssertionError((name, residue))

    r = S.symbols("r", positive=True)
    q, gamma = S.symbols("q gamma", real=True)
    N, A, pi = [S.Function(k)(r) for k in ("N", "A", "pi")]
    p = S.diff(pi, r)
    X = q**2/N**2-p**2/A**2
    Y = p**2/A**2
    box = S.diff(N*r**2*p/A, r)/(N*A*r**2)
    L3raw = gamma*N*A*r**2*X*box
    L3 = (2*gamma*q**2*r**2*S.diff(N, r)*p/(A*N**2)
          -2*gamma*r**2*S.diff(N, r)*p**3/(3*A**3)
          -4*gamma*N*r*p**3/(3*A**3))
    boundary = gamma*X*N*r**2*p/A+2*gamma*N*r**2*p**3/(3*A**3)
    zero("cubic_radial_IBP_boundary", L3raw-L3-S.diff(boundary, r))
    P, W = S.Function("P"), S.Function("W")
    V = S.symbols("V", real=True)
    lag = N*A*r**2*(P(X)-V)+A*r**2*W(Y)+L3
    PX = S.Subs(S.Derivative(P(S.Symbol("x")), S.Symbol("x")), S.Symbol("x"), X)
    WY = S.Subs(S.Derivative(W(S.Symbol("y")), S.Symbol("y")), S.Symbol("y"), Y)
    flux = ((N*PX-WY)*p/A-gamma*q**2*S.diff(N, r)/(A*N**2)
            +gamma*S.diff(N, r)*p**2/A**3+2*gamma*N*p**2/(r*A**3))
    zero("first_order_variation_current", S.diff(lag, p)+2*r**2*flux)
    covariant_Jr = (-2*(PX+gamma*box)*p/A**2
                    -gamma*S.diff(X, r)/A**2+2*WY*p/(N*A**2))
    zero("independent_covariant_current", N*A*r**2*covariant_Jr+2*r**2*flux)

    # Independently vary a clock radial slope before setting it to zero.
    n, a, u, z = S.symbols("N0 A0 p z", real=True, positive=True)
    sr = S.sqrt(1/n**2-z**2/a**2)
    Xs = q**2/n**2-u**2/a**2
    inner = -q/n**2+u*z/a**2
    Ys = -Xs+inner**2/sr**2
    clock_lag = n*a*r**2*sr*W(Ys)
    clock_j = S.diff(clock_lag, z).subs(z, 0)
    WYu = S.Subs(S.Derivative(W(S.Symbol("y")), S.Symbol("y")), S.Symbol("y"), u**2/a**2)
    zero("clock_current_from_projector", clock_j+2*q*r**2*WYu*u/a)
    zero("clock_projector_background", Ys.subs(z, 0)-u**2/a**2)
    flat_replacements = {N: 1, A: 1, S.diff(N, r): 0}
    zero("flat_cubic_reduction", L3.subs(flat_replacements)+4*gamma*r*p**3/3)
    flat_flux = flux.subs(flat_replacements)
    zero("flat_cubic_flux", S.diff(L3, p).subs(flat_replacements)+4*gamma*r*p**2)

    # Weak metric/field amplitude is expanded at fixed r, fixed coefficients.
    eps, phi, psi, gp, pp, PX0, WY0 = S.symbols("eps Phi Psi g p PX0 WY0", real=True)
    flux_jet = ((1+eps*phi)*PX0-WY0)*(eps*pp)/(1+eps*psi)
    flux_jet += (-gamma*q**2*eps*gp/((1+eps*psi)*(1+eps*phi)**2)
                 +gamma*eps*gp*(eps*pp)**2/(1+eps*psi)**3
                 +2*gamma*(1+eps*phi)*(eps*pp)**2/(r*(1+eps*psi)**3))
    zero("weak_linear_current", S.diff(flux_jet, eps).subs(eps, 0)
         -((PX0-WY0)*pp-gamma*q**2*gp))

    # Positive p is the one-sided local branch for |p|^3. Delta is positive
    # logarithm denominator at p=0; no q=0 restriction is needed for parity.
    U, d, ell, Delta, beta, a0, norm = S.symbols("U d ell Delta beta a0 norm", positive=True)
    v = S.symbols("p_positive", nonnegative=True)
    sign = S.symbols("sign", real=True)
    xs, ys, m0 = S.symbols("X Y m0", positive=True)
    original_P = -U*S.log((U-2*d*xs)/m0)/2
    original_W = U+2*d*ell*(S.sqrt(1+ys/ell)-1)
    original_PX = S.diff(original_P, xs)
    original_WY = S.diff(original_W, ys)
    constitutive = U*d/(Delta+2*d*v**2)-d/S.sqrt(1+v**2/ell)
    zero("constitutive_from_original_functions", constitutive.subs(Delta, U-2*d*q**2)
         -(original_PX.subs(xs, q**2-v**2)-original_WY.subs(ys, v**2)))
    kernel = constitutive*v-sign*S.Rational(3, 2)*beta*v**2+2*gamma*v**2/r
    target = norm*(1-S.exp(-v/a0))*v
    series = S.series(kernel, v, 0, 6).removeO().expand()
    lambda_X, lambda_W, qbar = S.symbols("lambda_X lambda_W qbar", real=True)
    completed_P = original_P+lambda_X*(xs-qbar**2)
    completed_W = original_W+lambda_W
    completed_kernel = (S.diff(completed_P, xs).subs(xs, q**2-v**2)
                        -S.diff(completed_W, ys).subs(ys, v**2))*v
    zero("canonical_completion_changes_only_linear_scalar_flux",
         completed_kernel-(constitutive.subs(Delta, U-2*d*q**2)+lambda_X)*v)
    zero("canonical_completion_no_fourth_power",
         S.diff(completed_kernel, v, 4).subs(v, 0))
    zero("scalar_flux_no_fourth_power", series.coeff(v, 4))
    zero("target_nonzero_fourth_power", S.diff(target, v, 4).subs(v, 0)-4*norm/a0**3)
    zero("q0_no_linear_flux", series.coeff(v, 1).subs(Delta, U))
    zero("q0_analytic_cubic_coefficient", series.coeff(v, 3).subs(Delta, U)
         -(d/(2*ell)-2*d**2/U))
    zero("q0_tuned_next_coefficient", series.coeff(v, 5).subs(Delta, U).subs(U, 4*d*ell)
         +d/(8*ell**2))
    zero("beta_plus_transverse_bad_near_zero", S.diff(-S.Rational(3, 2)*beta*v**2, v, 2)+3*beta)
    zero("beta_minus_transverse_leading", (2*constitutive+3*beta*v).diff(v).subs(v, 0)-3*beta)

    # Cubic-only scalar forcing is explicitly hypothetical; minimal matter
    # does not put baryonic mass into the scalar integration constant.
    charge = S.symbols("charge", positive=True)
    gamma_pos = S.symbols("gamma_positive", positive=True)
    cubic_p = S.sqrt(charge/(2*gamma_pos*r))
    zero("hypothetical_cubic_sourced_flux", 2*gamma_pos*cubic_p**2/r-charge/r**2)
    zero("hypothetical_cubic_radius_exponent", r*S.diff(cubic_p, r)/cubic_p+S.Rational(1, 2))

    # Independently invert the *conditional* static principal equations
    # derived by the sibling metric response calculation. No pi=Phi occurs.
    G0, M2, b, gn = S.symbols("G0 M2 b gN", nonzero=True, real=True)
    G = G0-2*b**2/M2
    sol = S.solve([G0*pp-2*b*gp, gp-gn-b*pp/M2], (pp, gp))
    zero("principal_scalar_source", sol[pp]-2*b*gn/G)
    zero("principal_metric_finite_gain", sol[gp]-G0*gn/G)
    schur = (2*original_PX.subs(xs, q**2)
             -2*original_WY.subs(ys, 0)*original_W.subs(ys, 0)
             /(original_W.subs(ys, 0)-2*q**2*original_WY.subs(ys, 0)))
    zero("analytic_clock_schur_zero", schur)
    completed_schur = (2*S.diff(completed_P, xs).subs(xs, q**2)
                      -2*S.diff(completed_W, ys).subs(ys, 0)*completed_W.subs(ys, 0)
                      /(completed_W.subs(ys, 0)-2*q**2*S.diff(completed_W, ys).subs(ys, 0)))
    completed_expected = (2*lambda_X+4*d**2*q**2*lambda_W
                          /((U-2*d*q**2)*(U-2*d*q**2+lambda_W)))
    zero("canonical_completion_clock_schur_shift", completed_schur-completed_expected)
    C = S.symbols("gain", positive=True)
    kappa = S.symbols("newtonian_shape", positive=True)
    mismatch = (1-S.exp(-C*eps*kappa/a0))*C*eps*kappa/(eps*kappa)
    zero("regular_linear_metric_MONDratio_limit", S.limit(mismatch, eps, 0, dir="+"))
    zero("target_leading_source_power", S.limit(target/v**2, v, 0, dir="+")-norm/a0)

    # Exact rational display fixtures, never candidate coefficients or fits.
    sample = []
    for ee in [S.Rational(1, 10)**k for k in (2, 4, 6, 8)]:
        sample.append({"epsilon": str(ee), "g_regular_gain_2": str(2*ee),
                       "MOND_necessary_lower_g_at_a0_n_1": str(S.sqrt(ee)),
                       "gain2_below_necessary_g": bool(2*ee < S.sqrt(ee))})
    return {
        "scope": "Exact frozen static scalar/clock identities and conditional local source scaling; no global solution or full health certificate",
        "base_revision_supplied": "f59fad6c7",
        "software": {"python": platform.python_version(), "sympy": S.__version__},
        "conventions": {"signature": "-+++", "metric": "-N(r)^2 dt^2+A(r)^2 dr^2+r^2 dOmega^2", "tau": "t for restricted current; clock varied before restriction", "chi": "q t+pi(r)", "source": "minimal matter; no direct chi source"},
        "cubic_reduced_density": str(L3),
        "cubic_boundary": str(boundary),
        "scalar_flux_F": str(flux),
        "clock_density_current": str(S.simplify(clock_j)),
        "analytic_plus_beta_scalar_flux_series": str(series),
        "canonical_completion": {"lambda_X": "3 gamma qbar Hbar", "lambda_W": "-2 gamma qbar^2 qbar_dot", "flat_scalar_flux_correction": str(lambda_X*v), "aligned_schur_G0": str(completed_expected), "constraint": "lambda_X and lambda_W are fixed reconstructed histories, not new free parameters"},
        "exponential_target_series": str(S.series(target, v, 0, 6)),
        "regular_principal_metric_gain": str(S.factor(sol[gp]/gn)),
        "finite_gain_fixture": sample,
        "checks": checks,
        "checks_passed": len(checks),
        "non_claims": ["Frozen coefficients need not solve background equations", "Diagonal metric plus tau=t can overrestrict a static branch", "Uniform global susceptibility is not implied by nonzero local principal coefficient alone", "No scalar force is identified with the physical metric", "Fourth-order mismatch only concerns displayed restricted scalar constitutive flux", "No direct scalar matter coupling added", "No arbitrary scalar charge assigned to baryon mass", "No beta coefficient is introduced into the original action"]
    }


if __name__ == "__main__":
    print(json.dumps(derive(), indent=2))
