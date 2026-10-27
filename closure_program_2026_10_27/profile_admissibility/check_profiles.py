#!/usr/bin/env python3
"""Bounded supporting checks; never import executable historical lane scripts."""
import argparse
import ast
import json
import math
from pathlib import Path

import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
from scipy.special import beta

ROOT = Path(__file__).resolve().parents[2]
REB = ROOT / "rebuild_2026_10_22"
X38 = REB / "X38_a0_surface_density_halos"
SC1 = REB / "SC1_self_coupled_core_law"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    source = (X38 / "x38_sd_halos.py").read_text()
    selected = [node for node in ast.parse(source).body
                if isinstance(node, ast.FunctionDef) and node.name in ("B", "solve_r0")]
    assert len(selected) == 2
    namespace = {"np": np, "math": math, "MUTATE": False, "SAT": {"n": 0}, "brentq": brentq}
    exec(compile(ast.Module(body=selected, type_ignores=[]), "<actual-X38-B-and-root-only>", "exec"), namespace)
    B, solve = namespace["B"], namespace["solve_r0"]
    saved = json.loads((X38 / "x38_sd_halos_results.json").read_text())
    sc1 = json.loads((SC1 / "sc1_core_law_results.json").read_text())
    roots = {foot: row["clusters"]["r0_Mpc"] for foot, row in saved["footings"].items()}
    values = [value for row in roots.values() for bg in row.values() for value in bg.values()]
    assert len(values) == 12 and all(np.isfinite(values)) and min(values) > 0
    factors = {foot: row["tercile_Sigma"] for foot, row in sc1["footings"].items()}
    assert all(value > 0 and np.isfinite(value) for row in factors.values() for value in row.values())
    # Re-evaluate the original K1 fixture, not the catalog. Units are the
    # original EM1 constants and original X38 Sigma conversion (source-pinned).
    msun, pc = 1.98847e30, 3.0857e16
    sigma = saved["Sigma_Msun_pc2"]["canonical"] * msun / pc ** 2
    mass, rt = 1e11 * msun, 3.0e21
    r0 = solve(mass, rt, sigma)
    rho = lambda r: sigma * r0 ** 2 / ((r + r0) * (r * r + r0 * r0))
    enclosed = lambda r: math.pi * sigma * r0 ** 2 * float(B(min(r, rt) / r0))
    mass_error = enclosed(rt) / mass - 1
    quadrature_mass = quad(lambda r: 4 * math.pi * r * r * rho(r), 0, rt,
                           epsabs=0, epsrel=1e-11)[0]
    quadrature_error = quadrature_mass / enclosed(rt) - 1
    assert abs(mass_error) < 1e-10 and abs(quadrature_error) < 1e-10
    assert namespace["SAT"]["n"] == 0 and np.isfinite(rho(rt)) and rho(rt) > 0
    h, r = rt * 1e-5, rt * .9
    derivative_density = (enclosed(r + h) - enclosed(r - h)) / (2 * h * 4 * math.pi * r * r)
    assert abs(derivative_density / rho(r) - 1) < 1e-8
    assert enclosed(1.01 * rt) == enclosed(2 * rt) == enclosed(rt)
    # Independent velocity-space quadrature checks the coefficient and powers
    # in the proof. p=-1/2 is integrably singular; p=0 is bounded; p=1 lowered.
    checks = []
    for p in (-.5, 0., 1.):
        for psi in (1., 1e-2, 1e-4, 1e-6):
            # v=sqrt(2psi)*u: integrate actual 4pi*v^2*f(psi-v^2/2) dv.
            value = 4 * math.pi * (2 * psi) ** 1.5 * psi ** p * quad(
                lambda u: u * u * (1 - u * u) ** p, 0, 1, epsabs=1e-12, epsrel=1e-12)[0]
            expected = 4 * math.pi * math.sqrt(2) * beta(p + 1, 1.5) * psi ** (p + 1.5)
            error = value / expected - 1
            assert abs(error) < 1e-10
            checks.append({"p": p, "psi": psi, "rho_velocity_quad": value,
                           "rho_beta_formula": expected, "relative_error": error})
    result = {
        "pass": True,
        "saved_root_medians_Mpc": roots,
        "saved_root_summary": {"count": len(values), "min": min(values), "max": max(values),
                               "paired_per_object_truncation_radii_available": False},
        "saved_surface_density_Msun_pc2": saved["Sigma_Msun_pc2"],
        "saved_SC1_tercile_Sigma_multipliers": factors,
        "K1_fixture_re_evaluation": {"M_kg": mass, "rt_m": rt, "Sigma_kg_m2": sigma,
                                   "r0_m": r0, "rt_over_r0": rt / r0,
                                   "edge_density_kg_m3": rho(rt),
                                   "edge_over_central_density": rho(rt) / (sigma / r0),
                                   "root_relative_mass_error": mass_error,
                                   "density_quadrature_relative_mass_error": quadrature_error,
                                   "mass_derivative_relative_density_error": derivative_density / rho(r) - 1,
                                   "mass_constant_outside": True, "saturated": False},
        "velocity_integral_checks": checks,
        "non_claims": ["Numerics do not prove the analytic boundary theorem",
                       "No per-object cluster edge density reconstructed from medians",
                       "No refit, global DF inversion, dynamical evolution or observational exclusion"]}
    with args.output.open("x") as output:
        json.dump(result, output, indent=2)
        output.write("\n")
    print(json.dumps({"pass": True, "root_median_range_Mpc": [min(values), max(values)],
                      "fixture": result["K1_fixture_re_evaluation"],
                      "velocity_quadratures": len(checks),
                      "max_velocity_quadrature_relative_error": max(abs(v["relative_error"]) for v in checks)}, indent=2))


if __name__ == "__main__":
    main()
