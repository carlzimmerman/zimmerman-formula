#!/usr/bin/env python3
"""Independent finite canonical deformations of frozen kinetic witnesses."""
import importlib.util
import json
import math
import resource
import sys
from pathlib import Path

import numpy as np
from numpy.polynomial.legendre import legder, leggauss, legval
from scipy.integrate import solve_bvp

HERE = Path(__file__).resolve().parent


def load_radial():
    spec = importlib.util.spec_from_file_location("fr01_frozen_radial", HERE / "radial_stability_v2.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def gauss(lo, hi, count):
    z, w = leggauss(count)
    return lo + (z + 1) * (hi - lo) / 2, w * (hi - lo) / 2


def background(sol, r):
    psi, dp, s, ds = sol.sol(r)
    p = np.maximum(psi, 0)
    n = p ** 1.5 * np.exp(3 * s)
    dn = np.exp(3 * s) * (1.5 * np.sqrt(p) * dp + 3 * p ** 1.5 * ds)
    return p, dp, s, ds, n, dn


def displacement(vector, r, radius):
    z = 2 * (r / radius) ** 2 - 1
    p = legval(z, vector)
    dp = legval(z, legder(vector))
    return r * p, p + 4 * (r / radius) ** 2 * dp, p


def density_variation(vector, sol, r, radius):
    p, dp, s, ds, n, dn = background(sol, r)
    xi, dx, xir = displacement(vector, r, radius)
    return np.where(r < radius, -dn * xi - n * (dx + 2 * xir), 0)


def scalar_forcing(vector, sol, radius, epsilon):
    outer = sol.x[-1]
    tail = math.sqrt(3 / epsilon) + 1 / outer
    mesh = np.unique(np.r_[sol.x, np.linspace(0.9 * radius, min(1.02 * radius, outer), 150)])

    def rhs(r, y):
        p, dp, s, ds, n, dn = background(sol, r)
        q = density_variation(vector, sol, r, radius)
        c = 6 * n * p + 9 * np.exp(3 * s)
        return np.array([y[1], (c * y[0] - 5 * p * q) / (3 * epsilon)])

    def jac(r, y):
        p, dp, s, ds, n, dn = background(sol, r)
        c = 6 * n * p + 9 * np.exp(3 * s)
        j = np.zeros((2, 2, r.size))
        j[0, 1] = 1
        j[1, 0] = c / (3 * epsilon)
        return j

    def bc(left, right):
        return np.array([left[1], right[1] + tail * right[0]])

    answer = solve_bvp(rhs, bc, mesh, np.zeros((2, mesh.size)),
                       S=np.diag([0.0, -2.0]), fun_jac=jac,
                       tol=3e-8, max_nodes=30000)
    if not answer.success:
        raise RuntimeError("independent scalar BVP failed: " + answer.message)
    return answer


def step_scale(vector, sol, scalar, radius):
    outer = sol.x[-1]
    r = np.linspace(0, radius, 4097)
    xi, dx, xir = displacement(vector, r, radius)
    sig = scalar.sol(np.linspace(0, outer, 4097))[0]
    return float(max(1, np.max(np.abs(dx)), np.max(np.abs(xir)),
                     np.max(np.abs(sig)), np.max(np.abs(xi)) / min(radius, outer - radius)))


def one_quadrature(vector, sol, scalar, radius, epsilon, scale, count):
    r, w = gauss(0, radius, count)
    re, we = gauss(radius, sol.x[-1], count)
    rr = np.r_[r, re]
    ww = np.r_[w * r * r, we * re * re]
    p, dp, s, ds, n, dn = background(sol, rr)
    sig, dsg = scalar.sol(rr)
    xi, dx, xir = displacement(vector, r, radius)
    q = -dn[:count] * xi - n[:count] * (dx + 2 * xir)
    er = 1.5 * n[:count] * p[:count]
    m = -r * r * dp[:count]
    a = (5 / 3) * p[:count] / n[:count]
    b = -5 * p[:count]
    c = 6 * n * p + 9 * np.exp(3 * s)
    terms = {
        "density": float(np.dot(w * r * r, a * q * q)),
        "mixed": float(np.dot(w * r * r, 2 * b * q * sig[:count])),
        "scalar": float(np.dot(ww, c * sig * sig)),
        "gradient": float(np.dot(ww, 3 * epsilon * dsg * dsg)),
        "gravity": float(np.dot(w * r * r, -2.5 * n[:count] ** 2 * xi * xi)),
        "kinetic_shear": float(np.dot(w * r * r, (4 / 3) * n[:count] * p[:count] * (dx - xir) ** 2)),
    }
    outer = sol.x[-1]
    tail_k = math.sqrt(3 / epsilon) + 1 / outer
    tail_pref = 1.5 * epsilon * outer * outer * tail_k
    sl = float(sol.sol(outer)[2])
    gl = float(scalar.sol(outer)[0])
    terms["tail"] = 2 * tail_pref * gl * gl
    quadratic = math.fsum(terms.values())

    # First derivative of the exact configuration energy, independently of Q.
    first_matter = np.dot(w * r * r, er * (-2 * (ds[:count] * xi + sig[:count]) - (2 / 3) * (dx + 2 * xir)))
    first_potential = np.dot(ww, 3 * np.expm1(3 * s) * sig)
    first_gradient = np.dot(ww, 3 * epsilon * ds * dsg)
    first_gravity = np.dot(w * r * r, 2.5 * m * n[:count] * xi / (r * r))
    first_tail = 2 * tail_pref * sl * gl
    first_variation = math.fsum(map(float, [first_matter, first_potential, first_gradient, first_gravity, first_tail]))

    baseline = math.fsum([
        float(np.dot(w * r * r, er)),
        float(np.dot(ww, np.expm1(3 * s) - 3 * s)),
        float(np.dot(ww, 1.5 * epsilon * ds * ds)),
        float(np.dot(w * r * r, -2.5 * m * n[:count] / r)),
        tail_pref * sl * sl,
    ])

    def increment(t):
        rt = r + t * xi
        stretch_r, stretch_t = 1 + t * dx, 1 + t * xir
        if np.min(stretch_r) <= 0 or np.min(stretch_t) <= 0:
            raise RuntimeError("nonpositive canonical stretch")
        edge = radius + t * displacement(vector, np.array([radius]), radius)[0][0]
        if np.min(rt) <= 0 or edge >= outer:
            raise RuntimeError("finite deformation leaves scalar domain")
        moved_s = sol.sol(rt)[2] + t * scalar.sol(rt)[0]
        delta_s = moved_s - s[:count]
        trace_minus_one = (-t * dx * (2 + t * dx) / stretch_r ** 2
                           -2 * t * xir * (2 + t * xir) / stretch_t ** 2) / 3
        factor_minus_one = trace_minus_one + np.expm1(-2 * delta_s) * (1 + trace_minus_one)
        kin = np.dot(w * r * r, er * factor_minus_one)
        du = np.exp(3 * s) * np.expm1(3 * t * sig) - 3 * t * sig
        pot = np.dot(ww, du)
        grad = np.dot(ww, 1.5 * epsilon * (2 * t * ds * dsg + t * t * dsg * dsg))
        grav = np.dot(w * r * r, 2.5 * m * n[:count] * t * xi / (r * rt))
        tail = tail_pref * (2 * t * sl * gl + t * t * gl * gl)
        return math.fsum(map(float, [kin, pot, grad, grav, tail])), {
            "kinetic": float(kin), "potential": float(pot), "gradient": float(grad),
            "gravity": float(grav), "tail": float(tail),
            "minimum_radial_stretch": float(np.min(stretch_r)),
            "minimum_tangential_stretch": float(np.min(stretch_t)),
            "deformed_matter_radius": float(edge),
        }

    steps = []
    for normalized in [0.02, 0.01, 0.005, 0.0025]:
        h = normalized / scale
        plus, cp = increment(h)
        minus, cm = increment(-h)
        curvature = (plus + minus) / (h * h)
        steps.append({"normalized_step": normalized, "h": h,
                      "delta_energy_plus": plus, "delta_energy_minus": minus,
                      "finite_second_derivative": curvature,
                      "relative_curvature_error": abs(curvature - quadratic) / abs(quadratic),
                      "odd_first_derivative": (plus - minus) / (2 * h),
                      "plus_components": cp, "minus_components": cm})
    checks = {
        "negative_independent_quadratic": quadratic < -1e-7,
        "finite_derivative_matches_quadratic": all(x["relative_curvature_error"] <= 0.001 for x in steps[-2:]),
        "both_signs_lower_energy": all(x["delta_energy_plus"] < 0 and x["delta_energy_minus"] < 0 for x in steps[-2:]),
        "first_variation_controlled": abs(first_variation) <= 0.1 * abs(quadratic) * steps[-1]["h"],
    }
    return {"quadrature": count, "baseline_energy": baseline, "quadratic_terms": terms,
            "independent_quadratic": quadratic, "first_variation": first_variation,
            "steps": steps, "checks": checks}


def run_case(module, record):
    pc, epsilon = record["psi_c"], record["epsilon"]
    witness = record["evaluations"][-1]["nested"][-1]
    vector = np.asarray(witness["vector"], dtype=float)
    if len(vector) != 12:
        raise ValueError("expected the frozen 12-basis witness")
    src = module.source_module()
    loc, guess = src.local_solution(pc)
    base, sol = src.solve_case(pc, epsilon, loc, guess, refine=True)
    if not base["passed"]:
        raise RuntimeError("frozen background control failed")
    radius = base["radius"]
    scalar = scalar_forcing(vector, sol, radius, epsilon)
    scale = step_scale(vector, sol, scalar, radius)
    evaluations = [one_quadrature(vector, sol, scalar, radius, epsilon, scale, nq)
                   for nq in [512, 1024]]
    qlo, qhi = [row["independent_quadratic"] for row in evaluations]
    original = witness["minimum_rayleigh"]
    checks = {
        "quadrature_refinement": abs(qlo - qhi) / max(1, abs(qhi)) < 3e-5,
        "frozen_witness_curvature": abs(qhi - original) / max(1, abs(qhi)) < 3e-5,
        "all_energy_controls": all(all(row["checks"].values()) for row in evaluations),
    }
    return {"psi_c": pc, "epsilon": epsilon, "radius": radius, "outer": float(sol.x[-1]),
            "vector": vector.tolist(), "step_scale": scale, "scalar_nodes": len(scalar.x),
            "original_quadratic": original, "evaluations": evaluations,
            "checks": checks, "passed": all(checks.values())}


def main():
    target = Path(sys.argv[1])
    target.parent.mkdir(parents=True, exist_ok=True)
    result = {"assertion_tested": "Direct finite canonical energy decreases for six frozen kinetic witnesses.",
              "cases": [], "all_controls_pass": False,
              "non_claim": "Accessible energy saddles, not a kinetic exponential-mode proof."}
    try:
        records = json.loads((HERE / "kinetic_run_002/result.json").read_text())
        if not records["all_controls_pass"]:
            raise RuntimeError("frozen kinetic source did not pass its controls")
        module = load_radial()
        for record in records["cases"]:
            row = run_case(module, record)
            result["cases"].append(row)
            print(row["psi_c"], row["epsilon"], row["passed"], row["evaluations"][-1]["independent_quadratic"], flush=True)
        if len(result["cases"]) != 6:
            raise RuntimeError("expected all six fixed cases")
        result["all_controls_pass"] = all(row["passed"] for row in result["cases"])
    except Exception as exc:
        import traceback
        result["exception"] = repr(exc)
        result["traceback"] = traceback.format_exc()
    result["peak_rss_bytes"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    target.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")
    if not result["all_controls_pass"]:
        print(result.get("traceback", "numerical control failure"), file=sys.stderr)
    return 0 if result["all_controls_pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
