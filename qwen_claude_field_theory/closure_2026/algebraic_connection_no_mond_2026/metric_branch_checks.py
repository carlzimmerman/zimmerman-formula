#!/usr/bin/env python3
"""Independent physical-metric checks for an Einstein branch (SymPy exact).

Contract: derive curvature in four dimensions from the displayed metrics,
not from supplied field-equation components. Signature (-+++), c=1, and
R_mn = d_a Gamma^a_mn - d_n Gamma^a_ma
       + Gamma^a_ab Gamma^b_mn - Gamma^a_nb Gamma^b_ma.
The static calculation retains O(epsilon) in independent Phi(r), Psi(r),
in isotropic spherical coordinates. Its exterior is spherical, static,
weak, source-free, and locally Lambda-negligible. Matter obeys
G_mn + Lambda g_mn = kappa T_mn; kappa=1/M_Pl^2 for the stated action.
Spatial FLRW curvature k and a(t) are arbitrary; that calculation is exact.

The MOND calculation uses mu(y)=1-exp(-y), y=g/a0>0, a0>0, r>0.
It does NOT substitute the different explicit exponential RAR nu function.
All algebra is symbolic over exact rationals, functions, and exponentials.
No sampling, numerical rank, full PPN result, connection constraint count,
or general action-level theorem is established by this bounded calculation.
Run this file for equations; run its sibling unittest file for independent
benchmarks and rejection of non-vacuum metric potentials.
"""

from functools import lru_cache
import platform
import time

import sympy as sp


def assert_zero(expression, label):
    residual = sp.simplify(expression)
    if residual != 0:
        raise AssertionError(f"{label}: nonzero residual {residual}")


def metric_curvature(metric, coordinates, linear_parameter=None):
    """Return Ricci, scalar, Einstein computed via Levi-Civita coefficients.

    With a linear parameter all intermediate operations occur modulo eps^2,
    retaining background spherical-coordinate coefficients exactly.
    """
    n = len(coordinates)

    def reduce(expression):
        if linear_parameter is None:
            return sp.simplify(expression)
        eps = linear_parameter
        return sp.simplify(expression.subs(eps, 0)) + eps * sp.simplify(
            sp.diff(expression, eps).subs(eps, 0)
        )

    inverse = metric.inv().applyfunc(reduce)
    connection = {}
    for a in range(n):
        for b in range(n):
            for c in range(b, n):
                value = reduce(sum(
                    inverse[a, d] * (
                        sp.diff(metric[d, c], coordinates[b])
                        + sp.diff(metric[d, b], coordinates[c])
                        - sp.diff(metric[b, c], coordinates[d])
                    ) / 2 for d in range(n)
                ))
                if value != 0:
                    connection[a, b, c] = value
                    connection[a, c, b] = value

    def gamma(a, b, c):
        return connection.get((a, b, c), sp.S.Zero)

    ricci = sp.zeros(n)
    for m in range(n):
        for nu in range(n):
            ricci[m, nu] = reduce(sum(
                sp.diff(gamma(a, m, nu), coordinates[a])
                - sp.diff(gamma(a, m, a), coordinates[nu])
                + sum(
                    gamma(a, a, b) * gamma(b, m, nu)
                    - gamma(a, nu, b) * gamma(b, m, a)
                    for b in range(n)
                ) for a in range(n)
            ))
    scalar = reduce(sum(inverse[m, nu] * ricci[m, nu]
                        for m in range(n) for nu in range(n)))
    einstein = (ricci - metric * scalar / 2).applyfunc(reduce)
    return ricci, scalar, einstein


@lru_cache(maxsize=1)
def static_geometry():
    t, r, theta, azimuth = sp.symbols("t r theta azimuth", positive=True)
    eps = sp.symbols("epsilon", real=True)
    phi, psi = sp.Function("Phi")(r), sp.Function("Psi")(r)
    metric = sp.diag(-(1 + 2 * eps * phi), 1 - 2 * eps * psi,
                     r**2 * (1 - 2 * eps * psi),
                     r**2 * sp.sin(theta)**2 * (1 - 2 * eps * psi))
    ricci, scalar, einstein = metric_curvature(
        metric, (t, r, theta, azimuth), linear_parameter=eps
    )
    for component in (*ricci, *einstein, scalar):
        assert_zero(component.subs(eps, 0), "static flat background")
    coefficient = lambda expression: sp.simplify(sp.diff(expression, eps))
    return {"r": r, "Phi": phi, "Psi": psi,
            "G00": coefficient(einstein[0, 0]),
            "Grr": coefficient(einstein[1, 1]),
            "Gtheta_over_r2": coefficient(einstein[2, 2] / r**2),
            "R00": coefficient(ricci[0, 0]), "R": coefficient(scalar)}


def assert_vacuum_potentials(phi, psi, radius):
    """Reject potentials unless every independent generated vacuum eq holds."""
    data = static_geometry()
    r = data["r"]
    substitutions = {data["Phi"]: phi.subs(radius, r),
                     data["Psi"]: psi.subs(radius, r)}
    for name in ("G00", "Grr", "Gtheta_over_r2", "R00"):
        assert_zero(data[name].subs(substitutions).doit(), name)


@lru_cache(maxsize=1)
def static_exterior():
    """Integrate generated vacuum equations, then match a baryonic source."""
    data = static_geometry()
    r, phi, psi = data["r"], data["Phi"], data["Psi"]
    c_phi, c_psi, b = sp.symbols("C_phi C_psi B", real=True)
    kappa, mass = sp.symbols("kappa M_b", positive=True)
    # The ODE solver sees the actual generated density equation.
    psi_general = sp.dsolve(sp.Eq(data["G00"], 0), psi).rhs
    psi_general = psi_general.subs({sp.Symbol("C1"): c_psi,
                                   sp.Symbol("C2"): b})
    phi_prime = sp.solve(data["Grr"], sp.diff(phi, r))[0]
    phi_general = sp.integrate(phi_prime.subs(psi, psi_general).doit(), r) + c_phi
    # Density normalization is derived from the generated derivative coefficient:
    # A Laplacian(Psi)=kappa rho, so 4*pi A r^2 Psi'=kappa M_b.
    laplacian_coefficient = sp.expand(data["G00"]).coeff(sp.diff(psi, r, 2))
    flux = 4 * sp.pi * laplacian_coefficient * r**2 * sp.diff(psi_general, r)
    matched_b = sp.solve(sp.Eq(flux, kappa * mass), b)[0]
    phi_solution, psi_solution = (sp.simplify(value.subs(b, matched_b))
                                  for value in (phi_general, psi_general))
    g_newton = sp.simplify(-matched_b / mass)
    gamma = sp.simplify((psi_solution - c_psi) / (phi_solution - c_phi))
    substitutions = {phi: phi_solution, psi: psi_solution}
    residuals = [sp.simplify(data[name].subs(substitutions).doit())
                 for name in ("G00", "Grr", "Gtheta_over_r2", "R00")]
    for residual in residuals:
        assert_zero(residual, "integrated static exterior")
    return {"r": r, "Phi": phi_solution, "Psi": psi_solution,
            "C_phi": c_phi, "C_psi": c_psi, "kappa": kappa,
            "mass": mass, "G_N": g_newton, "gamma": gamma,
            "vacuum_residuals": residuals}


@lru_cache(maxsize=1)
def mond_obstruction():
    """Implicitly differentiate the exact mu-law; substitute into metric R00."""
    data = static_geometry()
    r, phi = data["r"], data["Phi"]
    a0, y, q = sp.symbols("a0 y q", positive=True)
    y_r = sp.Function("y")(r)
    constitutive = a0 * y_r * (1 - sp.exp(-y_r)) - q / r**2
    y_prime = sp.solve(sp.diff(constitutive, r), sp.diff(y_r, r))[0]
    q_on_branch = sp.solve(constitutive, q)[0]
    y_prime = sp.simplify(y_prime.subs(q, q_on_branch).subs(y_r, y))
    acceleration = a0 * y
    curvature = sp.simplify(data["R00"].subs({
        sp.diff(phi, r, 2): a0 * y_prime,
        sp.diff(phi, r): acceleration,
    }))
    log_slope = sp.simplify(r * y_prime / y)
    curvature_derivative = sp.factor(sp.diff(curvature, r)
                                     + sp.diff(curvature, y) * y_prime)
    # For y>0, exp(y)-1+y>0 and the numerator below is positive.
    expected_positive_form = 2 * a0 * y**2 / (r * (sp.exp(y) - 1 + y))
    assert_zero(curvature - expected_positive_form, "MOND Ricci obstruction")
    return {"r": r, "y": y, "a0": a0,
            "s": sp.simplify((constitutive + q / r**2).subs(y_r, y) / a0),
            "y_prime": y_prime, "log_slope": log_slope,
            "R00": curvature,
            "R00_derivative_along_branch": curvature_derivative}


@lru_cache(maxsize=1)
def flrw_geometry():
    t, r, theta, azimuth = sp.symbols("t r theta azimuth", real=True)
    k, cosmological = sp.symbols("k Lambda", real=True)
    a = sp.Function("a")(t)
    metric = sp.diag(-1, a**2 / (1 - k * r**2),
                     a**2 * r**2, a**2 * r**2 * sp.sin(theta)**2)
    _, _, einstein = metric_curvature(metric, (t, r, theta, azimuth))
    spatial = sp.simplify(einstein[1, 1] / metric[1, 1])
    for i in (2, 3):
        assert_zero(einstein[i, i] / metric[i, i] - spatial, "FLRW isotropy")
    return {"t": t, "a": a, "k": k, "Lambda": cosmological,
            "G00": einstein[0, 0], "Gii_over_gii": spatial,
            "rho_equation_lhs": einstein[0, 0] - cosmological,
            "p_equation_lhs": spatial + cosmological}


def main():
    started = time.perf_counter()
    print(f"Python {platform.python_version()}; SymPy {sp.__version__}; exact arithmetic")
    print("Static isotropic metric, O(epsilon), independent Phi and Psi; c=1:")
    data = static_geometry()
    for name in ("G00", "Grr", "Gtheta_over_r2", "R00"):
        print(f"  {name} = {data[name]}")
    exterior = static_exterior()
    print("Vacuum exterior, Lambda negligible; rho matching G00=kappa*rho:")
    for name in ("Phi", "Psi", "G_N", "gamma"):
        print(f"  {name} = {exterior[name]}")
    print("  C_phi and C_psi are coordinate normalization constants; the ratio")
    print("  of their subtracted 1/r potentials gives the local linear gamma.")
    print("  For the stated action kappa=1/M_Pl^2, G_N=1/(8*pi*M_Pl^2).")
    mond = mond_obstruction()
    print("Implicit mu_exp MOND: s=g_N/a0=y*(1-exp(-y)), y=g/a0>0:")
    for name in ("y_prime", "log_slope", "R00", "R00_derivative_along_branch"):
        print(f"  {name} = {mond[name]}")
    print("  R_mn*u^m*u^n = epsilon*R00 + O(epsilon^2) for the normalized")
    print("  static observer. R00>0 for all finite r,a0,y>0, independent of Psi;")
    print("  source-free Einstein with negligible Lambda requires this to vanish.")
    print("  This rejects that MOND law on this local branch; no full PPN or")
    print("  connection degree-of-freedom assertion is made by this script.")
    flrw = flrw_geometry()
    print("Exact FLRW metric with arbitrary a(t), spatial curvature k:")
    print(f"  kappa*rho = {flrw['rho_equation_lhs']}")
    print(f"  kappa*p = {flrw['p_equation_lhs']}")
    print(f"Elapsed seconds: {time.perf_counter() - started:.3f}")


if __name__ == "__main__":
    main()
