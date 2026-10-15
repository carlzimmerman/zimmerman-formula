#!/usr/bin/env python3
"""Exact identities and finite witnesses for the equilibrium RTM local gate."""
import argparse
import json
from pathlib import Path
import sympy as s


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    identities, witnesses = [], []

    def zero(name, expression):
        residual = s.factor(expression)
        assert residual == 0, (name, residual)
        identities.append(name)

    def positive(name, expression):
        value = s.factor(expression)
        assert value.is_positive is True, (name, value)
        return str(value)

    r, G, a0, light, x, alpha = s.symbols("r G a0 c x alpha", positive=True)
    # Differentiate the two defining enclosed-mass/force relations independently.
    X = s.Function("X")(r)
    MB = s.Function("MB")(r)
    MC = a0 * r**2 * X / G
    logarithmic_force_equation = s.Eq(
        s.diff(s.log(G * MB / r**2), r),
        s.diff(s.log(a0 * X**2 / (1 - X)), r),
    )
    derivative = s.solve(logarithmic_force_equation, s.diff(X, r))[0]
    derivative = derivative.subs(s.diff(MB, r), alpha * MB / r).subs(X, x)
    zero("implicit_x_radial_derivative", derivative - x * (alpha - 2) * (1 - x) / (r * (2 - x)))
    rho_from_mass = s.diff(MC, r).subs(s.diff(X, r), derivative).subs(X, x) / (4 * s.pi * r**2)
    rho_formula = a0 * x * (2 + alpha * (1 - x)) / (4 * s.pi * G * r * (2 - x))
    zero("density_from_actual_enclosed_chi_mass", rho_from_mass - rho_formula)
    rho_critical = a0**2 * x**3 / (4 * s.pi * G * light**2 * (1 - x)**2)
    gb = a0 * x**2 / (1 - x)
    H = light**2 * (1 - x) * (2 + alpha * (1 - x)) / (gb * r * (2 - x))
    zero("actual_density_to_critical_density", rho_formula / rho_critical - H)
    # Relation to q=gb/a0, using d=1-x to avoid opaque radical simplification.
    d = s.symbols("d", positive=True)
    q = (1 - d)**2 / d
    f0 = 2 * d / (1 + d)
    zero("source_bound_factor_identity_squared", (1 - f0)**2 - q / (q + 4))
    # For 0<d<1 both sides of 1-f0=sqrt(q/(q+4)) are positive.

    M, b = s.symbols("M b", positive=True)
    enclosed = M * r**2 / (r + b)**2
    acceleration = G * enclosed / r**2
    al = s.factor(r * s.diff(enclosed, r) / enclosed)
    zero("Hernquist_alpha", al - 2 * b / (r + b))
    zero("Hernquist_force", acceleration - G * M / (r + b)**2)
    zero("Hernquist_velocity_bound_gap", G * M / (4 * b) - acceleration * r - G * M * (r - b)**2 / (4 * b * (r + b)**2))
    zero("Hernquist_acceleration_bound_gap", G * M / b**2 - acceleration - G * M * r * (r + 2 * b) / (b**2 * (r + b)**2))

    B, eps = s.symbols("B epsilon", positive=True)
    L = 4 * B * (1 - 1 / s.sqrt(1 + 4 * B**2)) / eps
    cubic_bound = 8 * B**3 / (eps * (1 + 4 * B**2))
    # Rationalize the positive difference: L - cubic_bound > 0 for B>0.
    z = s.symbols("z", positive=True)
    zero("elementary_bound_difference_identity", (L - cubic_bound).subs(B, s.sqrt(z**2 - 1) / 2) - s.sqrt(z**2 - 1) * (z - 1)**2 / (eps * z**2))
    healthy_B, healthy_eps = s.Rational(1, 100), s.Rational(1, 1000000)
    healthy_lower = cubic_bound.subs({B: healthy_B, eps: healthy_eps})
    witnesses.append({
        "name": "whole_interval_sufficient_Hernquist_member",
        "B": str(healthy_B), "epsilon": str(healthy_eps),
        "GM_over_b_c_squared": str(healthy_eps / healthy_B),
        "rational_uniform_lower_bound_H": str(healthy_lower),
        "lower_bound_minus_one": positive("healthy_bound_above_one", healthy_lower - 1),
        "scope": "All finite r>0 by the separate analytic inequalities; origin and vacuum matching excluded",
    })

    # Finite exact checks use x=1-d^2 and r/b=1, making all values rational.
    dd = s.Rational(1, 1000)
    xx = 1 - dd**2
    compact_B = dd / (2 * xx)
    failed_H = (4 * compact_B / healthy_eps) * dd**2 * (2 + dd**2) / (1 + dd**2)
    witnesses.append({
        "name": "compact_Hernquist_local_failure_at_r_equals_b",
        "B": str(compact_B), "epsilon": str(healthy_eps),
        "x": str(xx), "alpha": "1", "r_over_b": "1",
        "GM_over_b_c_squared": str(healthy_eps / compact_B),
        "H": str(failed_H), "one_minus_H": positive("compact_member_fails_gate", 1 - failed_H),
        "scope": "One equilibrium radius only; no relativistic or global instability verdict",
    })
    # Directly reconstruct the density from the Hernquist force, not the formula.
    rM = s.sqrt(G * M / a0)
    x_hern = 2 / (1 + s.sqrt(1 + 4 * (r + b)**2 / rM**2))
    rho_hern_direct = s.diff(a0 * r**2 * x_hern / G, r) / (4 * s.pi * r**2)
    rho_hern_formula = rho_formula.subs({x: x_hern, alpha: al})
    zero("Hernquist_direct_density_control", rho_hern_direct - rho_hern_formula)

    # Dimensionless exact radius samples: rM=G=a0=c=1 except epsilon separately.
    sample_rows = []
    for BB, EE in [(healthy_B, healthy_eps), (s.Integer(1), s.Rational(1, 100))]:
        for rr in [s.Rational(1, 100), s.Rational(1, 10), s.Integer(1), s.Integer(10), s.Integer(100)]:
            # rr=r/b, hence q=1/(B^2(1+rr)^2), gb*r/c^2=epsilon*rr/[B(1+rr)^2].
            xxr = 2 / (1 + s.sqrt(1 + 4 * BB**2 * (1 + rr)**2))
            alphar = 2 / (1 + rr)
            HH = BB * (1 + rr)**2 * (1 - xxr) * (2 + alphar * (1 - xxr)) / (EE * rr * (2 - xxr))
            bound = cubic_bound.subs({B: BB, eps: EE})
            sample_rows.append({"B": str(BB), "epsilon": str(EE), "r_over_b": str(rr), "H_minus_uniform_bound": positive("finite_Hernquist_bound_check", HH - bound)})

    # Point-source inner scaling: y=sqrt(1-x)/x, with x=1-d^2.
    ep = s.symbols("ep", positive=True)
    point_H = 2 * d**3 / (ep * (1 - d**2) * (1 + d**2))
    point_y = d / (1 - d**2)
    zero("point_inner_asymptotic_coefficient", s.limit(point_H / (2 * point_y**3 / ep), d, 0) - 1)
    exact_point = point_H.subs({d: dd, ep: healthy_eps})
    witnesses.append({"name": "point_source_inner_local_failure", "epsilon": str(healthy_eps), "x": str(xx), "r_over_rM": str(point_y.subs(d, dd)), "H": str(exact_point), "one_minus_H": positive("point_source_small_r_fails", 1 - exact_point)})

    result = {
        "status": "all declared exact identities, analytic-bound witnesses and finite samples passed",
        "coefficient_domain": "Q and symbolic algebraic expressions with positive square-root branches, exact SymPy arithmetic",
        "symbolic_identity_count": len(identities), "symbolic_identities": identities,
        "witnesses": witnesses, "finite_radial_sample_count": len(sample_rows), "finite_radial_samples": sample_rows,
        "non_claims": [
            "The all-r sufficient condition is an analytic inequality, not an inference from the finite samples.",
            "Only the assigned pure-chi pressureless spherical equilibrium and local B=0 principal gate are tested.",
            "No origin regularity, finite halo edge or vacuum matching, field-stress backreaction, stiffness/pressure, conversion, settling, metric solution or global stability is established.",
        ],
    }
    Path(args.output).write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"status": result["status"], "symbolic_identity_count": len(identities), "finite_radial_sample_count": len(sample_rows), "witness_count": len(witnesses)}, indent=2))


if __name__ == "__main__":
    main()
