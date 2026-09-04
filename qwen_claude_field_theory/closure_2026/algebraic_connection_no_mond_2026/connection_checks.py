#!/usr/bin/env python3
"""Exact component audit of algebraic metric-affine MOND proposals.

General theorem and limitations are in REPORT.md. This code constructs the
torsion-free distortion C^a_bc, not a vector ansatz. The 4D frozen-metric
canonical calculation is ONLY the regular auxiliary L=B block (unit nonzero
prefactor); it is not the full metric/connection Dirac analysis, and is NOT
transferred to the irregular exponential potential. No expected ranks,
determinants, PPN coefficients or gravitational DOF counts are input.

Signature (-+++), c=1; exact rational/symbolic SymPy arithmetic. General g^ij
uses one variable per symmetric pair. Off-diagonal derivatives count that
variable once. Boundary terms in Palatini R are treated in the written proof.
"""

import argparse
from functools import lru_cache
import json
from pathlib import Path
import platform
import time

import sympy as sp


@lru_cache(maxsize=None)
def distortion(n):
    if not isinstance(n, int) or n < 1:
        raise ValueError("dimension must be a positive integer")
    pairs = [(i, j) for i in range(n) for j in range(i, n)]
    gvars = sp.symbols(" ".join(f"g{i}{j}" for i, j in pairs), seq=True)
    gdict = dict(zip(pairs, gvars))
    gi = sp.Matrix(n, n, lambda i, j: gdict[min(i, j), max(i, j)])
    indices = [(a, b, c) for a in range(n) for b, c in pairs]
    q = sp.symbols(" ".join(f"C{a}{b}{c}" for a, b, c in indices), seq=True)
    components = dict(zip(indices, q))

    def C(a, b, c):
        return components[a, min(b, c), max(b, c)]

    trace = [sum(C(a, a, b) for a in range(n)) for b in range(n)]
    B = sp.expand(sum(gi[m, nu] * (
        trace[b] * C(b, m, nu) - sum(C(a, nu, b) * C(b, m, a) for a in range(n))
    ) for m in range(n) for nu in range(n) for b in range(n)))
    J = sp.expand(sum(gi[m, nu] * trace[m] * trace[nu]
                      for m in range(n) for nu in range(n)))
    eta = sp.diag(-1, *([1] * (n - 1)))
    flat = {gi[i, j]: eta[i, j] for i, j in pairs}
    return {"n": n, "pairs": pairs, "gvars": gvars, "ginv": gi,
            "indices": indices, "q": q, "C": C, "B": B,
            "trace_square": J, "flat_metric": flat, "eta": eta}


@lru_cache(maxsize=None)
def hessian_audit(n):
    data = distortion(n)
    B, q = data["B"].subs(data["flat_metric"]), data["q"]
    grad = sp.Matrix([sp.diff(B, v) for v in q])
    hessian = grad.jacobian(q)
    euler = sp.expand(sum(v * dv for v, dv in zip(q, grad)) - 2 * B)
    if euler != 0:
        raise AssertionError("quadratic Euler identity failed")
    return {"dimension": n, "components": len(q), "B": B,
            "gradient": grad, "hessian": hessian,
            "rank": hessian.rank(), "determinant": hessian.det(),
            "euler_residual": euler}


@lru_cache(maxsize=None)
def frame_audit(n):
    """Differentiate both independent metric and C under every GL generator."""
    data = distortion(n)
    gi, C, q = data["ginv"], data["C"], data["q"]
    all_residuals, c_only = [], []
    metric_columns = []
    derivatives = [(tuple(sp.diff(U, g) for g in data["gvars"]),
                    tuple(sp.diff(U, v) for v in q))
                   for U in (data["B"], data["trace_square"])]
    for row in range(n):
        for column in range(n):
            H = sp.zeros(n)
            H[row, column] = 1
            delta_g = H * gi + gi * H.T
            dg = [delta_g[i, j] for i, j in data["pairs"]]
            metric_columns.append(sp.Matrix(dg).subs(data["flat_metric"]))
            dc = [sum(H[a, d] * C(d, b, c) - H[d, b] * C(a, d, c)
                      - H[d, c] * C(a, b, d) for d in range(n))
                  for a, b, c in data["indices"]]
            residuals = []
            for g_derivative, c_derivative in derivatives:
                metric_part = sum(d * v for d, v in zip(g_derivative, dg))
                tensor_part = sum(d * v for d, v in zip(c_derivative, dc))
                residuals.append(sp.expand(metric_part + tensor_part))
            all_residuals.append(residuals)
            c_only.append(sp.expand(sum(d * v for d, v in zip(derivatives[0][1], dc))))
    if any(v != 0 for pair in all_residuals for v in pair):
        raise AssertionError("scalar frame covariance failed")
    metric_map = sp.Matrix.hstack(*metric_columns)
    return {"B_residuals": [p[0] for p in all_residuals],
            "trace_residuals": [p[1] for p in all_residuals],
            "C_only_B_variations": c_only,
            "metric_map": metric_map, "metric_map_rank": metric_map.rank()}


def poisson(left, right, q, p):
    return sp.expand(sum(sp.diff(left, qi) * sp.diff(right, pi)
                         - sp.diff(left, pi) * sp.diff(right, qi)
                         for qi, pi in zip(q, p)))


@lru_cache(maxsize=1)
def canonical_audit():
    """Actual primary/secondary functions and their PB; frozen regular L=B."""
    data, hess = distortion(4), hessian_audit(4)
    q = data["q"]
    p = sp.symbols(f"p0:{len(q)}", real=True)
    velocities = sp.symbols(f"v0:{len(q)}", real=True)
    multipliers = sp.Matrix(sp.symbols(f"u0:{len(q)}", real=True))
    L = hess["B"]
    momentum_functions = [sp.diff(L, v) for v in velocities]
    primary = [pi - value for pi, value in zip(p, momentum_functions)]
    H = sp.expand(sum(pi * v for pi, v in zip(momentum_functions, velocities)) - L)
    secondary = [poisson(constraint, H, q, p) for constraint in primary]
    constraints = sp.Matrix(primary + secondary)
    jac = constraints.jacobian((*q, *p))
    identity, zero = sp.eye(len(q)), sp.zeros(len(q))
    symplectic = zero.row_join(identity).col_join((-identity).row_join(zero))
    pb = jac * symplectic * jac.T
    # Preservation including every multiplier; not an assumed closure verdict.
    total_H = H + sum(u * constraint for u, constraint in zip(multipliers, primary))
    preservation = sp.Matrix([poisson(constraint, total_H, q, p) for constraint in secondary])
    coefficient = preservation.jacobian(multipliers)
    rhs = -preservation.subs(dict.fromkeys(multipliers, sp.S.Zero))
    solved = coefficient.inv() * rhs
    residual = preservation.subs(dict(zip(multipliers, solved)))
    if residual != sp.zeros(len(q), 1):
        raise AssertionError("secondary preservation did not close")
    constraint_rank, pb_rank = jac.rank(), pb.rank()
    first_class = constraint_rank - pb_rank
    reduced_phase = 2 * len(q) - 2 * first_class - pb_rank
    return {"q": q, "p": p, "k": sp.Symbol("k", real=True), "H": H,
            "momentum_functions": momentum_functions,
            "primary": primary, "secondary": secondary,
            "constraint_jacobian": jac, "constraint_jacobian_rank": constraint_rank,
            "poisson_matrix": pb, "poisson_rank": pb_rank, "poisson_determinant": pb.det(),
            "first_class": first_class, "second_class": pb_rank,
            "multipliers": solved, "preservation_residual": residual,
            "auxiliary_phase_dimension_after_reduction": reduced_phase}


@lru_cache(maxsize=1)
def exponential_audit():
    """First variation of U=a0^2 G(sqrt(|B|)/a0), including the null cone."""
    y, b, a0, t, direction_norm = sp.symbols("y b a0 t D", positive=True)
    primitive = y**2 + 2 * (1 + y) * sp.exp(-y) - 2
    primitive_residual = sp.simplify(sp.diff(primitive, y) / (2 * y) - (1 - sp.exp(-y)))
    positive_U = a0**2 * primitive.subs(y, sp.sqrt(b) / a0)
    positive_derivative = sp.simplify(sp.diff(positive_U, b))
    # For B=-b<0, d/dB = -d/db. Positive b is the magnitude, not B.
    negative_derivative = -positive_derivative
    hb, data = hessian_audit(4), distortion(4)
    null_point = dict.fromkeys(data["q"], sp.S.Zero)
    null_point[data["C"](0, 0, 0)] = sp.S.One
    null_B = hb["B"].subs(null_point)
    null_gradient = hb["gradient"].subs(null_point)
    # Along C=t*Dvec, |B(C)|=t^2*|B(Dvec)|. This verifies the vanishing
    # second directional derivative at the origin; the report supplies the
    # uniform norm bound needed to distinguish it from nonzero null points.
    origin_U = positive_U.subs(b, t**2 * direction_norm)
    return {"y": y, "b": b, "a0": a0, "primitive": primitive,
            "primitive_residual": primitive_residual,
            "U_B_positive": positive_derivative,
            "U_B_negative_magnitude": negative_derivative,
            "derivative_limit_at_zero": sp.limit(positive_derivative, b, 0, dir="+"),
            "U_BB_limit_at_zero": sp.limit(sp.diff(positive_derivative, b), b, 0, dir="+"),
            "null_B": null_B, "null_gradient_B": null_gradient,
            "null_point_nonzero_components": {str(k): str(v) for k, v in null_point.items() if v != 0},
            "origin_directional_second_derivative": sp.limit(sp.diff(origin_U, t, 2), t, 0, dir="+"),
            "small_y_series": sp.series(primitive, y, 0, 6)}


def sparse_entries(matrix):
    return [[i, j, str(matrix[i, j])] for i in range(matrix.rows)
            for j in range(matrix.cols) if matrix[i, j] != 0]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="write exact results and computed sparse PB matrix")
    args = parser.parse_args()
    started = time.perf_counter()
    result = {"environment": {"python": platform.python_version(), "sympy": sp.__version__},
              "scope": "exact component checks; frozen regular auxiliary canonical block only"}
    results = []
    for n in range(1, 5):
        data = hessian_audit(n)
        item = {name: str(data[name]) for name in ("dimension", "components", "rank", "determinant", "euler_residual")}
        results.append(item)
        print("Palatini B Hessian:", item, flush=True)
    result["hessians"] = results
    frame = frame_audit(4)
    result["frame"] = {"generators": len(frame["B_residuals"]),
                       "B_residuals": [str(v) for v in frame["B_residuals"]],
                       "trace_residuals": [str(v) for v in frame["trace_residuals"]],
                       "metric_variation_map_rank": frame["metric_map_rank"],
                       "omitted_metric_variation_nonzero_count": sum(v != 0 for v in frame["C_only_B_variations"])}
    print("Frame audit:", result["frame"], flush=True)
    canonical = canonical_audit()
    result["regular_auxiliary_canonical"] = {
        name: str(canonical[name]) for name in ("constraint_jacobian_rank", "poisson_rank",
                                              "poisson_determinant", "first_class", "second_class",
                                              "auxiliary_phase_dimension_after_reduction")}
    result["regular_auxiliary_canonical"].update({
        "basis": [str(v) for v in (*canonical["q"], *canonical["p"])],
        "primary": [str(v) for v in canonical["primary"]],
        "secondary": [str(v) for v in canonical["secondary"]],
        "poisson_sparse_entries": sparse_entries(canonical["poisson_matrix"]),
        "multipliers": [str(v) for v in canonical["multipliers"]],
        "sectors": "No spatial C derivatives: identical auxiliary block for k=0 and k!=0; not the metric sectors."})
    print("Regular auxiliary PB:", {key: value for key, value in result["regular_auxiliary_canonical"].items()
                                     if key not in ("basis", "primary", "secondary", "poisson_sparse_entries", "multipliers")}, flush=True)
    exp_data = exponential_audit()
    result["exponential"] = {key: str(value) for key, value in exp_data.items()}
    print("Exponential branch:", {key: value for key, value in result["exponential"].items()
                                  if key not in ("null_gradient_B",)}, flush=True)
    result["runtime_seconds"] = time.perf_counter() - started
    result["non_claims"] = ["Full gravitational Dirac algebra not computed.",
                            "No regular Dirac rank assigned to nonzero null exponential branch.",
                            "No full PPN, tensor perturbation or stability certificate.",
                            "Finite invariant tests are not a proof for all algebraic potentials; see analytic GL proof."]
    if args.output:
        args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(f"Elapsed {result['runtime_seconds']:.3f}s; component computation complete, not a theory PASS.")


if __name__ == "__main__":
    main()
