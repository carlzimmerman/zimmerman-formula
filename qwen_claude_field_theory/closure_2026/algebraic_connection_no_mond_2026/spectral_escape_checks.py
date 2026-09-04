#!/usr/bin/env python3
"""Scoped obstructions for a local Ricci spectral / curvature-source escape.

Contract: exact SymPy algebra over real local metric jets, signature (-+++),
R^a_bcd = d_c Gamma^a_db - d_d Gamma^a_cb + Gamma^a_ce Gamma^e_db
          - Gamma^a_de Gamma^e_cb. No randomness, numerical tolerance, files,
or external sources. The normalized spectral formulas use d > |b| and d > 0;
the scalar-curvature endpoint is R=lambda_0 I for arbitrary lambda_0.

The weighted regularity calculation samples ONLY the transverse boundary
path d=1, b=1-epsilon and its zero extension. It is not a global smoothness
theorem for a four-dimensional spectral prescription. Curvature matching is
an off-shell local-jet obstruction to a pointwise curvature-algebraic source
that vanishes on all the matched dust FLRW jets yet is nonzero on every
static Poisson-source jet. Derivative/nonlocal sources are outside that claim.

The action Hessian is a single highest-derivative trigger, not a complete
lapse/shift/auxiliary Dirac calculation or a physical degree-of-freedom count.
These results do not construct the exact exponential MOND action, derive a0,
or prove that every metric-only nonlocal completion is impossible.
"""

from functools import lru_cache
from itertools import product
import platform
import sys

import sympy as sp


INDICES = tuple(product(range(4), repeat=4))
ETA = sp.diag(-1, 1, 1, 1)


def _riemann_from_metric_jet(first, second):
    """Construct all covariant components at a point where g=eta.

    first(a,b,c)=g_ab,c and second(a,b,c,d)=g_ab,cd. The connection
    products are essential on the FLRW jet and are generated from first.
    """
    gamma = sp.MutableDenseNDimArray.zeros(4, 4, 4)
    for a, b, c in product(range(4), repeat=3):
        gamma[a, b, c] = sum(
            ETA[a, e] * (first(e, b, c) + first(e, c, b) - first(b, c, e))
            for e in range(4)
        ) / 2
    result = sp.MutableDenseNDimArray.zeros(4, 4, 4, 4)
    for a, b, c, d in INDICES:
        derivative_terms = (
            second(a, d, b, c) + second(b, c, a, d)
            - second(a, c, b, d) - second(b, d, a, c)
        ) / 2
        connection_terms = sum(
            ETA[e, e] * (gamma[e, b, c] * gamma[e, a, d]
                         - gamma[e, b, d] * gamma[e, a, c])
            for e in range(4)
        )
        result[a, b, c, d] = sp.expand(derivative_terms + connection_terms)
    return sp.ImmutableDenseNDimArray(result)


def _static_riemann(potential_hessian):
    """Jet of h00=-2Phi, hij=-2Phi deltaij, with zero first metric jet."""
    def second(a, b, c, d):
        if a != b or c == 0 or d == 0:
            return sp.S.Zero
        return -2 * potential_hessian[c - 1, d - 1]

    return _riemann_from_metric_jet(lambda a, b, c: sp.S.Zero, second)


def _ricci(riemann):
    return sp.Matrix(4, 4, lambda b, d: sp.expand(sum(
        ETA[a, a] * riemann[a, b, a, d] for a in range(4)
    )))


def _weyl_components(riemann):
    ricci = _ricci(riemann)
    scalar = sp.trace(ETA * ricci)
    return tuple(sp.expand(
        riemann[a, b, c, d]
        - (ETA[a, c] * ricci[d, b] - ETA[a, d] * ricci[c, b]
           - ETA[b, c] * ricci[d, a] + ETA[b, d] * ricci[c, a]) / 2
        + scalar * (ETA[a, c] * ETA[d, b] - ETA[a, d] * ETA[c, b]) / 6
    ) for a, b, c, d in INDICES)


@lru_cache(maxsize=1)
def derive_spectral_escape_checks():
    d, b = sp.symbols("d b", positive=True)
    epsilon = sp.Symbol("epsilon", positive=True)
    lambda_0 = sp.Symbol("lambda_0", real=True)
    eta2 = sp.diag(-1, 1)
    M = sp.Matrix([[d, b], [-b, -d]])
    curvature_block = lambda_0 * sp.eye(2) + M
    delta = d**2 - b**2
    Q2 = (sp.eye(2) + M / sp.sqrt(delta)) / 2
    Q4 = sp.diag(Q2, sp.zeros(2))
    spatial = sp.simplify((sp.eye(4) - Q4) * ETA)
    rest_path = {d: epsilon, b: 0}
    boosted_path = {d: 5 * epsilon / 3, b: 4 * epsilon / 3}

    def path_limit(matrix, substitution):
        return matrix.subs(substitution).applyfunc(
            lambda entry: sp.limit(entry, epsilon, 0, dir="+")
        )

    rest_limit = path_limit(spatial, rest_path)
    boosted_limit = path_limit(spatial, boosted_path)
    jordan = M.subs({d: 1, b: 1})
    spectral = {
        "symbols": {"d": d, "b": b, "epsilon": epsilon, "lambda_0": lambda_0},
        "curvature_block": curvature_block,
        "delta": delta,
        "timelike_projector": Q4,
        "spatial_tensor": spatial,
        "self_adjoint_residual": eta2 * M - (eta2 * M).T,
        "minimal_polynomial_residual": sp.simplify(M**2 - delta * sp.eye(2)),
        "idempotence_residual": sp.simplify(Q4**2 - Q4),
        "projector_trace": sp.simplify(sp.trace(Q4)),
        "spatial_determinant": sp.simplify(spatial.det()),
        "rest_spatial_tensor": sp.simplify(spatial.subs(b, 0)),
        "rest_path_limit": rest_limit,
        "boosted_path_limit": boosted_limit,
        "path_difference": boosted_limit - rest_limit,
        "curvature_path_endpoint_residual": (
            path_limit(curvature_block, rest_path)
            - path_limit(curvature_block, boosted_path)
        ),
        "jordan_block": jordan,
        "jordan_square": jordan**2,
        "null_boundary_h11_limit": sp.limit(
            spatial[1, 1].subs({d: 1, b: 1 - epsilon}), epsilon, 0, dir="+"
        ),
        "complex_branch_eigenvalues": tuple(M.subs({d: 1, b: 2}).eigenvals()),
    }

    weighted = {}
    for n in (1, 2, 3):
        right = sp.simplify((delta**n * spatial[1, 1]).subs(
            {d: 1, b: 1 - epsilon}
        ))
        weighted[n] = {
            "right_expression": right,
            "right_derivative_limits": tuple(
                sp.limit(sp.diff(right, epsilon, order), epsilon, 0, dir="+")
                for order in range(n + 1)
            ),
            "left_derivative_limits": tuple(
                sp.limit(sp.diff(sp.S.Zero, epsilon, order), epsilon, 0, dir="-")
                for order in range(n + 1)
            ),
        }

    p = sp.Symbol("p", positive=True)
    A, H, tidal = sp.symbols("A H epsilon_tidal", real=True)
    static = _static_riemann(sp.eye(3) * p / 3)

    # FLRW ds^2=-dt^2+a(t)^2 dx^2 at a=1, adot=H, addot=A+H^2.
    def flrw_first(a, b, c):
        return 2 * H if a == b and a > 0 and c == 0 else sp.S.Zero

    def flrw_second(a, b, c, d):
        if a == b and a > 0 and c == 0 and d == 0:
            return 2 * (A + 2 * H**2)
        return sp.S.Zero

    flrw = _riemann_from_metric_jet(flrw_first, flrw_second)
    static_ricci = sp.simplify(ETA * _ricci(static))
    flrw_ricci = sp.simplify(ETA * _ricci(flrw))
    match = {A: -p, H**2: 2 * p / 3}
    matched_residuals = tuple(sp.simplify(
        flrw[index].subs(match) - static[index]
    ) for index in INDICES)
    # Antisymmetries, pair exchange and first Bianchi, for both actual tensors.
    symmetries = tuple(sp.expand(residual)
        for tensor in (static, flrw)
        for a, b_, c, d_ in INDICES
        for residual in (
            tensor[a, b_, c, d_] + tensor[b_, a, c, d_],
            tensor[a, b_, c, d_] + tensor[a, b_, d_, c],
            tensor[a, b_, c, d_] - tensor[c, d_, a, b_],
            tensor[a, b_, c, d_] + tensor[a, c, d_, b_]
            + tensor[a, d_, b_, c],
        )
    )
    c1, c2 = sp.symbols("c1 c2", real=True)
    source_flrw = sp.expand(-c1 * flrw_ricci[0, 0] + c2 * sp.trace(flrw_ricci))
    coefficient_equations = [source_flrw.coeff(A), source_flrw.coeff(H, 2)]
    coefficient_matrix, _ = sp.linear_eq_to_matrix(coefficient_equations, (c1, c2))
    static_scalar = sp.trace(static_ricci)
    static_traceless = static_ricci - static_scalar * sp.eye(4) / 4
    spectral_subtraction = sp.simplify(
        -static_ricci[0, 0] + static_scalar / 4
        - sp.sqrt(3 * sp.trace(static_traceless**2)) / 2
    )
    source = {
        "symbols": {"p": p, "A": A, "H": H, "c1": c1, "c2": c2},
        "static_riemann": static,
        "flrw_riemann": flrw,
        "static_ricci_mixed": static_ricci,
        "flrw_ricci_mixed": flrw_ricci,
        "matched_riemann_residuals": matched_residuals,
        "static_weyl_components": _weyl_components(static),
        "riemann_symmetry_residuals": symmetries,
        "linear_source_flrw_coefficients": coefficient_matrix,
        "linear_source_solution": sp.solve(coefficient_equations, (c1, c2)),
        "spectral_subtraction_static": spectral_subtraction,
    }

    euclidean = sp.Matrix([[d, b], [b, -d]])
    euclidean_Q = (sp.eye(2) + euclidean / sp.sqrt(delta)) / 2
    tidal_riemann = _static_riemann(sp.diag(p / 3 + tidal, p / 3 - tidal, p / 3))
    controls = {
        "euclidean_self_adjoint_residual": eta2 * euclidean - (eta2 * euclidean).T,
        "euclidean_idempotence_residual": sp.simplify(euclidean_Q**2 - euclidean_Q),
        "tidal_ricci_difference": sp.simplify(ETA * _ricci(tidal_riemann) - static_ricci),
        "tidal_weyl_components": _weyl_components(tidal_riemann),
        "tidal_riemann_difference": tuple(sp.expand(
            tidal_riemann[index] - static[index]
        ) for index in INDICES),
    }

    lam, C = sp.symbols("lambda C", nonzero=True, real=True)
    # Relate d to a genuine acceleration direction, not an independent matter
    # variable: at a local N=1 point, R^0_0 has principal sum_i dot(H_i),
    # R^1_1 has dot(H_1), and R^0_1 has mixed space/time derivatives.
    # The trace-free variation delta dot(H_i)=(-2,1,1) delta s shifts
    # d=(R^0_0-R^1_1)/2 by delta s while b stays fixed. The block mean and
    # spectator eigenvalues also shift, but do not change its simple time
    # eigenprojector before an eigenvalue collision. Full constraints could
    # still change the physical interpretation of this nonzero subblock.
    action_term = lam * C * spatial[1, 1]
    acceleration_hessian = sp.simplify(sp.diff(action_term, d, 2))
    derivative_trigger = {
        "symbols": {"d": d, "b": b, "lambda": lam, "C": C},
        "action_term": action_term,
        "acceleration_hessian": acceleration_hessian,
        "diagonal_ricci_control": sp.simplify(acceleration_hessian.subs(b, 0)),
        "off_diagonal_numeric_control": sp.simplify(
            acceleration_hessian.subs({d: 2, b: 1, lam: 1, C: 1})
        ),
    }
    return {
        "spectral": spectral,
        "weighted_boundary": weighted,
        "curvature_source": source,
        "negative_controls": controls,
        "derivative_trigger": derivative_trigger,
    }


def main():
    r = derive_spectral_escape_checks()
    spectral, source = r["spectral"], r["curvature_source"]
    controls, trigger = r["negative_controls"], r["derivative_trigger"]
    checks = [
        ("Lorentz self-adjoint and idempotent timelike projector",
         spectral["self_adjoint_residual"] == sp.zeros(2)
         and spectral["idempotence_residual"] == sp.zeros(4)
         and spectral["projector_trace"] == 1),
        ("same scalar-curvature endpoint, distinct normalized-projector limits",
         spectral["curvature_path_endpoint_residual"] == sp.zeros(2)
         and spectral["path_difference"] != sp.zeros(4)),
        ("null/Jordan boundary diverges; continuation has complex eigenvalues",
         spectral["jordan_block"] != sp.zeros(2)
         and spectral["jordan_square"] == sp.zeros(2)
         and spectral["null_boundary_h11_limit"] == sp.oo
         and all(value.is_real is False for value in spectral["complex_branch_eigenvalues"])),
        ("weights soften the sampled boundary jets without global regularity claim",
         all(r["weighted_boundary"][n]["right_derivative_limits"] == (0,) * n + (sp.oo,)
             for n in (1, 2, 3))),
        ("all 256 static and dust-FLRW Riemann components agree",
         all(item == 0 for item in source["matched_riemann_residuals"])
         and all(item == 0 for item in source["riemann_symmetry_residuals"])),
        ("curvature subtraction removes the static Poisson source too",
         source["linear_source_flrw_coefficients"].det() != 0
         and source["spectral_subtraction_static"] == 0),
        ("Euclidean-sign and tidal-anisotropy mutations are detected",
         controls["euclidean_self_adjoint_residual"] != sp.zeros(2)
         and controls["euclidean_idempotence_residual"] != sp.zeros(2)
         and controls["tidal_ricci_difference"] == sp.zeros(4)
         and any(item != 0 for item in controls["tidal_weyl_components"])),
        ("off-diagonal Ricci activates the action acceleration Hessian",
         trigger["off_diagonal_numeric_control"] != 0
         and trigger["diagonal_ricci_control"] == 0),
    ]
    print("LOCAL SPECTRAL ESCAPE: EXACT SCOPED CHECKS")
    print("Python", platform.python_version(), "SymPy", sp.__version__)
    print("Normalized H =", spectral["spatial_tensor"])
    print("Endpoint path difference =", spectral["path_difference"])
    print("Static mixed Ricci =", source["static_ricci_mixed"])
    print("FLRW mixed Ricci =", source["flrw_ricci_mixed"])
    for n in (1, 2, 3):
        print("Delta^%s H11 right derivatives through order %s =" % (n, n),
              r["weighted_boundary"][n]["right_derivative_limits"])
    print("Action acceleration Hessian =", trigger["acceleration_hessian"])
    for label, condition in checks:
        print("[%s] %s" % ("PASS" if condition else "FAIL", label))
    print("Checks: %s/%s" % (sum(bool(condition) for _, condition in checks), len(checks)))
    print("Scope: local tensors and sampled boundary jets; no global weighted-projector theorem.")
    print("Full metric/auxiliary Dirac, static MOND/slip and PPN: UNCOMPUTED.")
    print("Next: vary a specified weighted spectral action and source on an inhomogeneous")
    print("off-diagonal-Ricci background, retaining lapse, shift and all auxiliary fields.")
    return 0 if all(condition for _, condition in checks) else 1


if __name__ == "__main__":
    sys.exit(main())
