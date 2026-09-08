"""Invariant-curvature endpoint gate for Q=-beta*q^2*Z, beta>0.

The canonical matter quadratic action is varied before eliminating lapse,
spatial curvature and shift. Four-dimensional background and linearized
connections then produce Ricci and Weyl curvature; their coefficients are
not assigned from an expected growth formula. The scalar observables R_com
and Ricci_UU_com subtract their background time derivative times u/q.

The original beta=1/4 branch and the coefficient obtained by cancelling its
derived growing curvature term are reported separately. Neither a positive
matter kinetic coefficient nor cancellation of this endpoint growth is a
full stability, causality, or nonlinear degree-of-freedom certificate.
"""

import argparse
from functools import lru_cache
import json

import sympy as s


def _connection(metric, inverse, coordinates):
    return [[[
        s.simplify(sum(inverse[i, ell]*(s.diff(metric[ell, j], coordinates[k])
                       + s.diff(metric[ell, k], coordinates[j])
                       - s.diff(metric[j, k], coordinates[ell]))
                        for ell in range(4))/2)
        for k in range(4)] for j in range(4)] for i in range(4)]


def _ricci(connection, coordinates):
    return s.Matrix(4, 4, lambda i, j: s.simplify(sum(
        s.diff(connection[ell][i][j], coordinates[ell])
        - s.diff(connection[ell][i][ell], coordinates[j])
        + sum(connection[ell][i][j]*connection[b][ell][b]
              - connection[b][i][ell]*connection[ell][j][b]
              for b in range(4)) for ell in range(4))))


@lru_cache(None)
def derive_connection():
    t, x, y, w = s.symbols("t x y w", real=True)
    k = s.symbols("k", positive=True)
    coordinates = (t, x, y, w)
    a, n, z, v = (s.Function(name)(t) for name in ("a", "n", "z", "v"))
    cosine, sine = s.cos(k*x), s.sin(k*x)
    metric = s.diag(-1, a*a, a*a, a*a)
    inverse = metric.inv()
    perturbation = s.Matrix([
        [-2*n*cosine, a*a*v*sine, 0, 0],
        [a*a*v*sine, 2*a*a*z*cosine, 0, 0],
        [0, 0, 2*a*a*z*cosine, 0],
        [0, 0, 0, 2*a*a*z*cosine],
    ])
    inverse_variation = -inverse*perturbation*inverse
    connection = _connection(metric, inverse, coordinates)
    delta_connection = [[[
        s.simplify(sum(
            inverse_variation[i, ell]*(s.diff(metric[ell, j], coordinates[b])
                + s.diff(metric[ell, b], coordinates[j])
                - s.diff(metric[j, b], coordinates[ell]))
            + inverse[i, ell]*(s.diff(perturbation[ell, j], coordinates[b])
                + s.diff(perturbation[ell, b], coordinates[j])
                - s.diff(perturbation[j, b], coordinates[ell]))
            for ell in range(4))/2)
        for b in range(4)] for j in range(4)] for i in range(4)]
    ricci = _ricci(connection, coordinates)
    delta_ricci = s.Matrix(4, 4, lambda i, j: s.simplify(sum(
        s.diff(delta_connection[ell][i][j], coordinates[ell])
        - s.diff(delta_connection[ell][i][ell], coordinates[j])
        + sum(delta_connection[ell][i][j]*connection[b][ell][b]
              + connection[ell][i][j]*delta_connection[b][ell][b]
              - delta_connection[b][i][ell]*connection[ell][j][b]
              - connection[b][i][ell]*delta_connection[ell][j][b]
              for b in range(4)) for ell in range(4))))
    background_R = s.simplify(s.trace(inverse*ricci))
    delta_R = s.simplify(s.trace(inverse*delta_ricci)+s.trace(inverse_variation*ricci))

    def riemann(rho, sigma, mu, nu, varied=False):
        if not varied:
            return s.simplify(s.diff(connection[rho][nu][sigma], coordinates[mu])
                - s.diff(connection[rho][mu][sigma], coordinates[nu])
                + sum(connection[rho][mu][ell]*connection[ell][nu][sigma]
                      - connection[rho][nu][ell]*connection[ell][mu][sigma]
                      for ell in range(4)))
        return s.simplify(s.diff(delta_connection[rho][nu][sigma], coordinates[mu])
            - s.diff(delta_connection[rho][mu][sigma], coordinates[nu])
            + sum(delta_connection[rho][mu][ell]*connection[ell][nu][sigma]
                  + connection[rho][mu][ell]*delta_connection[ell][nu][sigma]
                  - delta_connection[rho][nu][ell]*connection[ell][mu][sigma]
                  - connection[rho][nu][ell]*delta_connection[ell][mu][sigma]
                  for ell in range(4)))

    weyl = {}
    background_weyl = {}
    for i in (1, 2):
        R0i0i = sum(metric[0, rho]*riemann(rho, i, 0, i) for rho in range(4))
        delta_R0i0i = sum(perturbation[0, rho]*riemann(rho, i, 0, i)
                          + metric[0, rho]*riemann(rho, i, 0, i, True)
                          for rho in range(4))
        background_weyl[i] = s.simplify(R0i0i
            -(metric[0, 0]*ricci[i, i]+metric[i, i]*ricci[0, 0])/2
            + background_R*metric[0, 0]*metric[i, i]/6)
        electric = (delta_R0i0i
            -(perturbation[0, 0]*ricci[i, i]+metric[0, 0]*delta_ricci[i, i]
              + perturbation[i, i]*ricci[0, 0]+metric[i, i]*delta_ricci[0, 0])/2
            + delta_R*metric[0, 0]*metric[i, i]/6
            + background_R*(perturbation[0, 0]*metric[i, i]
                            + metric[0, 0]*perturbation[i, i])/6)
        # Background Weyl=0: projection onto the physical orthonormal frame
        # needs only the background a^-2 factor at linear order.
        weyl[i] = s.simplify(electric/(a*a*cosine))

    H = s.diff(a, t)/a
    delta_K = 3*s.diff(z, t)-3*H*n-k*v
    # Independent ADM scalar identity, used only to check the connection result.
    adm_delta_R = 2*k*k*(n+2*z)/a**2+8*H*delta_K+2*s.diff(delta_K, t)-6*n*s.diff(H, t)
    # An explicit four-dimensional pure time diffeomorphism, not merely an
    # assigned scalar transformation rule: insert -Lie_xi(g) into the same
    # connection-derived curvature. Spatial gauge remains E=0 for this xi.
    chi = s.Function("chi")(t)
    xi_vector = (chi*cosine, 0, 0, 0)
    pure_gauge_metric = s.Matrix(4, 4, lambda i, j: -sum(
        xi_vector[ell]*s.diff(metric[i, j], coordinates[ell])
        +metric[ell, j]*s.diff(xi_vector[ell], coordinates[i])
        +metric[i, ell]*s.diff(xi_vector[ell], coordinates[j])
        for ell in range(4)))
    gauge_amplitudes = {n: -pure_gauge_metric[0, 0]/(2*cosine),
                        z: pure_gauge_metric[1, 1]/(2*a*a*cosine),
                        v: pure_gauge_metric[0, 1]/(a*a*sine)}
    gauge_R = (delta_R/cosine).subs(gauge_amplitudes, simultaneous=True).doit()
    residuals = {
        "connection_Ricci_ADM_identity": s.simplify(delta_R/cosine-adm_delta_R),
        "connection_pure_time_gauge_Ricci": s.simplify(gauge_R+s.diff(background_R, t)*chi),
        "background_Weyl_parallel": background_weyl[1],
        "background_Weyl_transverse": background_weyl[2],
        "linear_Weyl_trace": s.simplify(weyl[1]+2*weyl[2]),
    }
    return dict(t=t, k=k, a=a, n=n, z=z, v=v, cosine=cosine, sine=sine,
                metric=metric, perturbation=perturbation,
                background_R=background_R, background_Ricci=ricci,
                delta_R=s.simplify(delta_R/cosine), delta_Ricci=delta_ricci,
                Weyl_parallel=weyl[1], Weyl_transverse=weyl[2], residuals=residuals)


@lru_cache(None)
def derive():
    m, k, a, q, H, beta = s.symbols("m k a q H beta", positive=True)
    u, ud, n, z, v = s.symbols("u ud n z v", real=True)
    Q = s.symbols("Q", real=True, nonzero=True)
    # Full canonical-P(X) scalar quadratic density from the trace/VCDM
    # action, with its action-defined slip-channel coefficient Q retained.
    L = (ud**2/2-q*n*ud+3*q*z*ud+q*q*n*n/2+Q*(z+n)**2
         - k*k*u*u/(2*a*a)+q*k*v*u+m*k*k*v*v/3)
    auxiliary_equations = [s.diff(L, variable) for variable in (n, z, v)]
    auxiliary = s.solve(auxiliary_equations, (n, z, v), dict=True)[0]
    reduced = s.factor(L.subs(auxiliary))
    adaptive_Q = -beta*q*q
    kinetic = s.factor(s.diff(reduced, ud, 2).subs(Q, adaptive_Q))
    gradient = s.factor(-s.diff(reduced, u, 2))
    adaptive_auxiliary = {variable: s.factor(expression.subs(Q, adaptive_Q))
                          for variable, expression in auxiliary.items()}

    def dt(expression):
        rules = {a: a*H, H: -q*q/(2*m), q: -3*H*q, u: ud,
                 ud: -3*H*ud-gradient*u/kinetic}
        return s.factor(sum(s.diff(expression, variable)*value
                            for variable, value in rules.items()))

    geometry = derive_connection()
    time = geometry["t"]
    jets = {geometry["a"]: a,
            s.diff(geometry["a"], time): a*H,
            s.diff(geometry["a"], time, 2): a*(H*H-q*q/(2*m))}
    for key, variable in (("n", n), ("z", z), ("v", v)):
        expression = adaptive_auxiliary[variable]
        jets[geometry[key]] = expression
        jets[s.diff(geometry[key], time)] = dt(expression)
        jets[s.diff(geometry[key], time, 2)] = dt(dt(expression))

    def jet(expression):
        return s.factor(expression.subs(jets, simultaneous=True))

    Rbar = jet(geometry["background_R"])
    R00bar = jet(geometry["background_Ricci"][0, 0])
    R11bar = jet(geometry["background_Ricci"][1, 1])
    Rbar_dot, R00bar_dot = dt(Rbar), dt(R00bar)
    delta_R = jet(geometry["delta_R"])
    delta_R00 = jet(geometry["delta_Ricci"][0, 0]/geometry["cosine"])
    delta_R0x = jet(geometry["delta_Ricci"][0, 1]/geometry["sine"])
    # U^mu is the canonical scalar's normalized four-velocity. At first
    # order delta U^0=-n and background R_0i=0, hence delta(R_UU) below.
    delta_RUU = s.factor(delta_R00-2*adaptive_auxiliary[n]*R00bar)
    observables = {
        "R_com": s.factor(delta_R-Rbar_dot*u/q),
        "Ricci_UU_com": s.factor(delta_RUU-R00bar_dot*u/q),
        "Weyl_parallel": jet(geometry["Weyl_parallel"]),
        "Weyl_transverse": jet(geometry["Weyl_transverse"]),
        "Ricci_spatial_anisotropy": jet((geometry["delta_Ricci"][1, 1]
                                       -geometry["delta_Ricci"][2, 2])
                                      /(geometry["a"]**2*geometry["cosine"])),
        # R_{mu nu} U^mu e_x^nu has zero background. The boost term follows
        # from U_i=-partial_i u/q and orthogonality of the physical frame.
        "Ricci_flux": s.factor(delta_R0x/a-R11bar*adaptive_auxiliary[v]/a
                               +(R00bar+R11bar/a**2)*k*u/(a*q)),
    }

    # Four-dimensional scalar gauge check. Under a time displacement xi,
    # delta R -> delta R - Rbar_dot xi and u -> u - q xi.
    xi, delta_scalar = s.symbols("xi delta_scalar", real=True)
    gauge_residual = s.expand((delta_scalar-Rbar_dot*xi)
                              - Rbar_dot*(u-q*xi)/q
                              - (delta_scalar-Rbar_dot*u/q))
    gauge_UU_residual = s.expand((delta_scalar-R00bar_dot*xi)
                                 -R00bar_dot*(u-q*xi)/q
                                 -(delta_scalar-R00bar_dot*u/q))

    Hd, q0, u_infinity = s.symbols("H_d q0 u_infinity", positive=True)
    U3, c2, c4 = s.symbols("U3 c2 c4", real=True)
    x = s.symbols("inverse_a", positive=True)
    frobenius_u = u_infinity+c2*x*x+U3*x**3+c4*x**4
    # The exact background has H-Hd=O(a^-6), q=q0*a^-3. Thus the
    # de Sitter equation fixes c2,c4 and all potentially growing/nondecaying
    # curvature terms; those omitted background terms contribute O(a^-5)
    # or smaller to the largest curvature amplitude (which scales as a).
    frobenius_equation = s.expand(x*x*s.diff(frobenius_u, x, 2)
                                  -2*x*s.diff(frobenius_u, x)
                                  +k*k*x*x*frobenius_u/(kinetic*Hd*Hd))
    coefficients = s.solve([frobenius_equation.coeff(x, 2),
                            frobenius_equation.coeff(x, 4)], (c2, c4), dict=True)[0]
    asymptotic_u = s.factor(frobenius_u.subs(coefficients).subs(x, 1/a))
    asymptotic_ud = s.factor(Hd*a*s.diff(asymptotic_u, a))
    asymptotic = {name: s.factor(expression.subs(
        {H: Hd, q: q0/a**3, u: asymptotic_u, ud: asymptotic_ud}, simultaneous=True))
        for name, expression in observables.items()}
    growth_coefficients = {name: s.factor(s.limit(expression/a, a, s.oo))
                           for name, expression in asymptotic.items()}
    roots = s.solve(growth_coefficients["R_com"], beta)
    healthy_roots = [root for root in roots if root.is_positive is True
                     and s.simplify(kinetic.subs(beta, root)).is_positive is True]
    candidate = healthy_roots[0] if len(healthy_roots) == 1 else None
    if candidate is None:
        raise ValueError("The derived curvature cancellation did not select a unique healthy beta")

    def positive_powers(expression):
        return s.factor(sum(term for term in s.Add.make_args(s.expand(expression))
                            if term.as_powers_dict().get(a, 0) > 0))

    candidate_positive = {name: positive_powers(expression.subs(beta, candidate))
                          for name, expression in asymptotic.items()}
    candidate_limits = {name: s.factor(s.limit(expression.subs(beta, candidate), a, s.oo))
                        for name, expression in asymptotic.items()}
    candidate_curvature = {name: s.factor(expression.subs(beta, candidate))
                           for name, expression in observables.items()}

    # Exact expanding background with canonical physical scalar and optional
    # seed Lambda=3 Hd^2. It approaches de Sitter while q remains nonzero at
    # every finite time t>0.
    t = s.symbols("proper_time", positive=True)
    a_background = s.sinh(3*Hd*t)**s.Rational(1, 3)
    H_background = Hd*s.coth(3*Hd*t)
    q_background = s.sqrt(6*m)*Hd/s.sinh(3*Hd*t)
    tau_background = -3*m*H_background
    background_residuals = {
        "scale_Hubble": s.simplify(s.diff(a_background, t)/a_background-H_background),
        "Friedmann": s.simplify(3*m*H_background**2-q_background**2/2-3*m*Hd**2),
        "matter_conservation": s.simplify(s.diff(a_background**3*q_background, t)),
        "Hubble_evolution": s.simplify(s.diff(H_background, t)+q_background**2/(2*m)),
        "trace_clock_evolution": s.simplify(s.diff(tau_background, t)-3*q_background**2/2),
    }
    residuals = dict(geometry["residuals"])
    residuals.update({"action_auxiliary_"+str(i): s.simplify(equation.subs(auxiliary))
                      for i, equation in enumerate(auxiliary_equations)})
    residuals.update(scalar_gauge_invariance=gauge_residual,
                     Ricci_UU_gauge_invariance=gauge_UU_residual,
                     frobenius_order_two=s.simplify(frobenius_equation.coeff(x, 2).subs(coefficients)),
                     frobenius_order_four=s.simplify(frobenius_equation.coeff(x, 4).subs(coefficients)))
    return dict(m=m, k=k, a=a, q=q, Q=Q, H=H, beta=beta, u=u, ud=ud, n=n, z=z, v=v,
                L=L, auxiliary=adaptive_auxiliary, kinetic=kinetic, gradient=gradient,
                reduced_equation_acceleration=s.factor(-3*H*ud-gradient*u/kinetic),
                background_R=Rbar, background_R_dot=Rbar_dot, delta_R=delta_R,
                observables=observables, Hd=Hd, q0=q0, u_infinity=u_infinity, U3=U3,
                frobenius_coefficients=coefficients, asymptotic_u=asymptotic_u,
                asymptotic_observables=asymptotic, growth_coefficients=growth_coefficients,
                cancellation_roots=roots, candidate_beta=candidate,
                candidate_positive_power_terms=candidate_positive,
                candidate_limits=candidate_limits, candidate_curvature=candidate_curvature,
                background=dict(time=t, a=a_background, H=H_background,
                                q=q_background, tau=tau_background, Lambda=3*Hd**2),
                background_residuals=background_residuals, residuals=residuals,
                analytic_scope="Regular-singular asymptotic expansion on the exact stiff-plus-Lambda background, for each fixed nonzero k and q0>0; u_infinity and U3 label the two matter solutions",
                invariant_scope="R_com and Ricci_UU_com are scalar comoving gauge invariants. Weyl, physical Ricci flux and spatial anisotropy have zero FLRW backgrounds. Their linear values are evaluated at finite q!=0.",
                non_claim="No full nonlinear constraint count, zero-q uniformity, external retarded causality, or complete stability claim follows from this endpoint screen")


def _transfer(beta_value, rtol):
    import numpy as np
    from scipy.integrate import solve_ivp

    d = derive()
    kinetic = float(d["kinetic"].subs(d["beta"], beta_value))
    m_value, Hd_value, k_value = 1.0, 1.0, 1.0

    def background(t):
        argument = 3*Hd_value*t
        return (np.sinh(argument)**(1/3), Hd_value/np.tanh(argument),
                np.sqrt(6*m_value)*Hd_value/np.sinh(argument))

    def rhs(t, state):
        scale, hubble, matter_q = background(t)
        frequency = (k_value*k_value/(scale*scale)+3*matter_q*matter_q/(2*m_value))/kinetic
        # Integrate p=a^3*ud, not the exponentially tiny ud itself. This is
        # exactly equivalent to ud_dot+3H*ud+frequency*u=0 and avoids an
        # absolute-error floor amplified by 1/q in the curvature observables.
        return [state[1]/scale**3, -scale**3*frequency*state[0]]

    times = np.linspace(1.0, 8.0, 701)
    solution = solve_ivp(rhs, (1.0, 8.0), [1.0, 0.0], method="DOP853",
                         rtol=rtol, atol=rtol*1e-3, t_eval=times)
    if not solution.success:
        raise RuntimeError(solution.message)
    scale, hubble, matter_q = background(solution.t)
    expressions = dict(d["observables"])
    expressions["n"] = d["auxiliary"][d["n"]]
    expressions["z"] = d["auxiliary"][d["z"]]
    curves = {"u": solution.y[0], "ud": solution.y[1]/scale**3}
    for name, expression in expressions.items():
        function = s.lambdify((d["a"], d["H"], d["q"], d["u"], d["ud"]),
            s.factor(expression.subs({d["beta"]: beta_value, d["m"]: m_value, d["k"]: k_value})), "numpy")
        values = np.asarray(function(scale, hubble, matter_q, curves["u"], curves["ud"]), dtype=float)
        curves[name] = np.broadcast_to(values, solution.t.shape).copy()
    if not all(np.all(np.isfinite(values)) for values in curves.values()):
        raise RuntimeError("Nonfinite transfer output")
    summary = dict(success=bool(solution.success), method="DOP853", rtol=rtol,
        atol=rtol*1e-3, integrated_state=["u", "a^3*ud"], nfev=int(solution.nfev),
        parameters=dict(m=m_value, H_d=Hd_value, k=k_value, beta=str(beta_value)),
        time_interval=[1.0, 8.0], initial_state=[1.0, 0.0], samples=len(times),
        final={name: float(values[-1]) for name, values in curves.items()},
        maximum_abs={name: float(np.max(np.abs(values))) for name, values in curves.items()},
        selected_samples=[dict(time=float(solution.t[index]), a=float(scale[index]),
            **{name: float(values[index]) for name, values in curves.items()})
            for index in (0, 100, 300, 500, 700)],
        illustrative_amplitude=1e-12,
        maximum_scaled_metric_amplitude=float(1e-12*max(np.max(np.abs(curves["n"])),
                                                       np.max(np.abs(curves["z"])))),
        scope="Normalized linear transfer, not finite-amplitude nonlinear evolution. Multiplying all initial perturbations and outputs by 1e-12 keeps this finite interval small; no uniform all-time claim is made.")
    return summary, curves


@lru_cache(None)
def numerical_transfer(beta_value):
    import numpy as np
    coarse, low_curves = _transfer(beta_value, 1e-9)
    refined, high_curves = _transfer(beta_value, 1e-11)
    differences = {name: float(np.max(np.abs(high_curves[name]-low_curves[name]))
                               /max(1.0, float(np.max(np.abs(high_curves[name])))))
                   for name in high_curves}
    return dict(coarse=coarse, refined=refined, scaled_tolerance_differences=differences,
                maximum_scaled_tolerance_difference=max(differences.values()),
                evidence_scope="Finite numerical agreement between two tolerances; the analytic asymptotic calculation supplies the unbounded-time statement")


def encode(value):
    if isinstance(value, dict):
        return {str(key): encode(item) for key, item in value.items()}
    if isinstance(value, s.MatrixBase):
        return encode(value.tolist())
    if isinstance(value, (list, tuple)):
        return [encode(item) for item in value]
    if isinstance(value, s.Integer):
        return int(value)
    if isinstance(value, s.Basic):
        return str(value)
    return value


@lru_cache(None)
def run():
    d = derive()
    checks = {name: s.simplify(value) == 0 for name, value in
              dict(d["residuals"], **d["background_residuals"]).items()}
    if not all(checks.values()):
        raise AssertionError({name: value for name, value in checks.items() if not value})
    original_growth = s.simplify(d["growth_coefficients"]["R_com"].subs(d["beta"], s.Rational(1, 4))) != 0
    cancellation = all(s.simplify(value) == 0 for value in d["candidate_positive_power_terms"].values())
    numerical = dict(original_beta_one_quarter=numerical_transfer(s.Rational(1, 4)),
                     derived_cancellation=numerical_transfer(d["candidate_beta"]))
    return encode(dict(algebra_checks_passed=all(checks.values()), checks=checks,
        original_endpoint_growing=bool(original_growth),
        candidate_beta=d["candidate_beta"], candidate_curvature_growth_cancelled=bool(cancellation),
        numerical=numerical, derivation=d,
        status="ORIGINAL_ADAPTIVE_ENDPOINT_FAILS_DERIVED_CANCELLATION_REMAINS_OPEN",
        scope="The original beta=1/4 has growing gauge-invariant curvature. The derived coefficient cancels growth in the displayed linear curvature observables; it is not a full stability or causality certificate."))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--require-stable-endpoint", action="store_true")
    parser.add_argument("--use-derived-cancellation", action="store_true")
    args = parser.parse_args(argv)
    result = run()
    print(result["status"])
    print("Original beta=1/4 growing curvature:", result["original_endpoint_growing"])
    print("Derived cancellation beta:", result["candidate_beta"])
    print("Derived candidate curvature growth cancelled:", result["candidate_curvature_growth_cancelled"])
    for name, transfer in result["numerical"].items():
        print(name, "final R_com:", transfer["refined"]["final"]["R_com"],
              "tolerance difference:", transfer["maximum_scaled_tolerance_difference"])
    passed = (result["candidate_curvature_growth_cancelled"] if args.use_derived_cancellation
              else not result["original_endpoint_growing"])
    return 2 if args.require_stable_endpoint and not passed else 0


if __name__ == "__main__":
    raise SystemExit(main())
