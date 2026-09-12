#!/usr/bin/env python3
"""Exact necessary gates for identifying C003 kicks with one dust clock.

No MOND/PPN/DOF PASS is inferred. Newtonian velocity moments are a local,
nonrelativistic limit; clock integrability and dust variation are covariant.
The exponential MOND kernel and a0 are untouched, and are not used to fit gates.
"""
import argparse
import json
from pathlib import Path

import sympy as s


def moments(weights, velocities):
    total = sum(weights)
    mean = sum((w*v for w, v in zip(weights, velocities)), s.zeros(3, 1))/total
    covariance = sum((w*(v-mean)*(v-mean).T for w, v in zip(weights, velocities)), s.zeros(3))/total
    return mean.applyfunc(s.simplify), covariance.applyfunc(s.simplify)


def wedge_derivative(one_form, coordinates):
    """Coefficient of dx0 wedge dx1 wedge dx2 in n wedge dn."""
    n, x = one_form, coordinates
    return s.simplify(sum(n[i]*(s.diff(n[k], x[j])-s.diff(n[j], x[k]))
                          for i, j, k in ((0, 1, 2), (1, 2, 0), (2, 0, 1))))


def isotropic_kick_moments(velocity, kick):
    mu = s.Symbol("mu", real=True)
    phi = s.Symbol("phi", real=True)
    direction = s.Matrix([s.sqrt(1-mu**2)*s.cos(phi),
                          s.sqrt(1-mu**2)*s.sin(phi), mu])
    final = velocity + kick*direction

    def average(expr):
        return s.simplify(s.integrate(s.integrate(s.expand(expr), (phi, 0, 2*s.pi)),
                                      (mu, -1, 1))/(4*s.pi))

    return final.applyfunc(average), (final*final.T).applyfunc(average)


def dust_variation():
    """Vary sqrt(-g) rho[-g^ab tau_a tau_b - 1]/2.

    Metric variation is computed in ten symmetric basis directions about a
    local inertial metric. This determines the covariant tensor algebraically;
    the covariant Euler equation follows by integrating the scalar variation.
    """
    rho = s.Symbol("rho", positive=True)
    tau = s.Matrix(s.symbols("tau0:4", real=True))
    eta = s.diag(-1, 1, 1, 1)
    eps = s.Symbol("eps", real=True)
    scalar_l = rho*(-(tau.T*eta*tau)[0]-1)/2
    stress = s.zeros(4)
    for i in range(4):
        for j in range(i, 4):
            perturb = s.zeros(4)
            perturb[i, j] = 1
            perturb[j, i] = 1
            inverse_metric = eta + eps*perturb
            density = s.sqrt(-1/inverse_metric.det())
            lagrangian = density*rho*(-(tau.T*inverse_metric*tau)[0]-1)/2
            variation = s.diff(lagrangian, eps).subs(eps, 0)
            # Off-diagonal symmetric variations contain two identical entries.
            stress[i, j] = stress[j, i] = s.simplify(-2*variation/(1 if i == j else 2))
    residual = (stress - rho*tau*tau.T - eta*scalar_l).applyfunc(s.simplify)
    return {"multiplier_EL": str(s.diff(scalar_l, rho)),
            "scalar_momentum": list(map(str, [s.diff(scalar_l, p) for p in tau])),
            "stress": [[str(stress[i, j]) for j in range(4)] for i in range(4)],
            "stress_identity_residual": [[str(residual[i, j]) for j in range(4)] for i in range(4)]}


def calculate():
    t, x, y, omega = s.symbols("t x y omega", real=True)
    raw = s.Matrix([-1, -omega*y, omega*x])
    # Timelike for omega^2 (x^2+y^2)<1. Frobenius zero/nonzero is unchanged
    # by multiplying a nonvanishing one-form by any smooth scalar.
    normal = raw/s.sqrt(1-omega**2*(x*x+y*y))
    rotating_wedge = wedge_derivative(normal, (t, x, y))
    exact = t+x*y
    gradient = s.Matrix([s.diff(exact, c) for c in (t, x, y)])
    clock_wedge = wedge_derivative((1+x*x)*gradient, (t, x, y))
    velocity = s.Matrix(s.symbols("vx vy vz", real=True))
    kick, rate, rho = s.symbols("kick Gamma rho", positive=True)
    first, second = isotropic_kick_moments(velocity, kick)
    stress_source = (rho*rate*(second-velocity*velocity.T)).applyfunc(s.simplify)
    bulk, cov_bulk = moments([s.Integer(1)], [s.Matrix([s.Rational(1, 10), 0, 0])])
    counter, cov_counter = moments([s.Rational(1, 2)]*2,
                                   [s.Matrix([s.Rational(1, 10), 0, 0]),
                                    s.Matrix([-s.Rational(1, 10), 0, 0])])
    OM, OL, a, theta, H0 = s.symbols("Omega_m Omega_L a theta H0", positive=True)
    # This is a background identity in flat dust+Lambda GR, not a C003 action.
    E2 = OM/a**3+OL
    normalized_de_fraction = s.simplify((OL/E2)/OL)
    local_theta_replacement = 9*H0**2/theta**2
    return {
        "status": "necessary-action-gates-only; C003 not certified",
        "dust_variation": dust_variation(),
        "clock_integrability": {"gradient_n_wedge_dn": str(clock_wedge),
                                "rotating_n_wedge_dn": str(rotating_wedge),
                                "rotating_value_at_origin": str(rotating_wedge.subs({x: 0, y: 0}))},
        "moments": {"single_stream_bulk_velocity": list(map(str, bulk)),
                    "single_stream_covariance_trace": str(s.trace(cov_bulk)),
                    "counterstream_bulk_velocity": list(map(str, counter)),
                    "counterstream_covariance_trace": str(s.trace(cov_counter)),
                    "kick_mean_increment": list(map(str, first-velocity)),
                    "kick_stress_source": [[str(stress_source[i, j]) for j in range(3)] for i in range(3)],
                    "kinetic_energy_source": str(s.trace(stress_source)/2)},
        "epoch_trigger": {"flat_dust_lambda_GR_only": str(normalized_de_fraction),
                          "replacement_using_local_expansion": str(local_theta_replacement),
                          "limit_as_local_expansion_goes_to_zero": str(s.limit(local_theta_replacement, theta, 0, dir="+"))},
        "non_claims": ["No theorem excludes all covariant MOND actions or general clock stresses",
                       "Dust multiplier action is an explicit subcase, not the full cuscuton/P(X,tau) action",
                       "Frobenius counterexample excludes identifying one scalar clock with every possible single stream",
                       "The rotating example is a kinematic counterexample, not a claimed solution of the candidate",
                       "No observational likelihood, CMB/PPN, rank/DOF count, or first-principles kick coupling is calculated"]}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--result-file", required=True, type=Path)
    args = parser.parse_args()
    result = calculate()
    args.result_file.parent.mkdir(parents=True, exist_ok=True)
    args.result_file.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps(result, indent=2))
