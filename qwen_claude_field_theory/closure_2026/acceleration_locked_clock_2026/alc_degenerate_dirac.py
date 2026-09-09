#!/usr/bin/env python3
"""ADM/Dirac gate for the exact-luminal PPN corner.

The standard Einstein--aether kinetic density is evaluated in a local
orthonormal 3+1 frame, then restricted to a hypersurface-orthogonal aether.
The calculation is deliberately algebraic: no rank or determinant is supplied
as an expected answer.

For a hypersurface-orthogonal normal, write

    B_{mu nu}=nabla_mu n_nu,  B_{0i}=a_i,
    B_{ij}=K_{ij}+omega_{ij},  B_{i0}=0.

With the usual Einstein--aether signs the density is

    c1 B_mu nu B^mu nu + c2 (B_mu^mu)^2
      + c3 B_mu nu B^nu mu - c4 a_i a^i.

The script derives the ADM decomposition.  On the exact tensor-luminal,
alpha_1=0 branch, c13=0 and c14=0.  The remaining scalar combination is
c123=c2.  A finite c123 gives a purely spatial (instantaneous) khronon
constraint; c123=0 removes the whole quadratic hypersurface-orthogonal
kinetic form and leaves a rank-degenerate/strong-coupling branch.

This is a bounded nonlinear-ADM obstruction for the constant-aether
regularisation of ALC.  It is not a universal no-go for every nonlocal action;
the exact exponential MOND sector and metric mixing still require their own
full covariant analysis.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent


def _pb(A, B, q, p):
    return sp.simplify(sum(sp.diff(A, qi) * sp.diff(B, pi)
                          - sp.diff(A, pi) * sp.diff(B, qi)
                          for qi, pi in zip(q, p)))


def _adm_decomposition():
    c1, c2, c3, c4 = sp.symbols("c1 c2 c3 c4", real=True)
    k11, k22, k33, k12, k13, k23 = sp.symbols(
        "K11 K22 K33 K12 K13 K23", real=True
    )
    w12, w13, w23 = sp.symbols("w12 w13 w23", real=True)
    a1, a2, a3 = sp.symbols("a1 a2 a3", real=True)
    K = sp.Matrix([[k11, k12, k13], [k12, k22, k23], [k13, k23, k33]])
    W = sp.Matrix([[0, w12, w13], [-w12, 0, w23],
                   [-w13, -w23, 0]])
    B = sp.zeros(4)
    for i, ai in enumerate((a1, a2, a3), start=1):
        B[0, i] = ai
    spatial = K + W
    for i in range(3):
        for j in range(3):
            B[i + 1, j + 1] = spatial[i, j]
    eta = sp.diag(-1, 1, 1, 1)
    B_up = eta * B * eta
    I1 = sp.expand(sum(B[i, j] * B_up[i, j]
                       for i in range(4) for j in range(4)))
    I3 = sp.expand(sum(B[i, j] * B_up[j, i]
                       for i in range(4) for j in range(4)))
    theta = sp.trace(K)
    a_sq = a1**2 + a2**2 + a3**2
    K_sq = sum(K[i, j]**2 for i in range(3) for j in range(3))
    W_sq = sum(W[i, j]**2 for i in range(3) for j in range(3))
    density = sp.expand(c1 * I1 + c2 * theta**2 + c3 * I3 - c4 * a_sq)
    target = sp.expand((c1 + c3) * K_sq + c2 * theta**2
                       - (c1 + c4) * a_sq + (c1 - c3) * W_sq)
    hypersurface_orthogonal = {w12: 0, w13: 0, w23: 0}
    density_ho = sp.factor(density.subs(hypersurface_orthogonal))
    branch_luminal = {c3: -c1, c4: -c1}
    density_luminal = sp.factor(density.subs(branch_luminal))
    density_degenerate = sp.factor(density_luminal.subs(c2, 0))
    density_ho_luminal = sp.factor(density_ho.subs(branch_luminal))
    density_ho_degenerate = sp.factor(density_ho_luminal.subs(c2, 0))
    velocity_variables = (k11, k22, k33, k12, k13, k23, a1, a2, a3)
    hessian = sp.hessian(density, velocity_variables)
    hessian_luminal = hessian.subs(branch_luminal)
    hessian_samples = {
        "c123_nonzero": hessian_luminal.subs({c1: 1, c2: 1}),
        "c123_zero": hessian_luminal.subs({c1: 1, c2: 0}),
    }
    return {
        "symbols": (c1, c2, c3, c4),
        "density": density,
        "I1": I1,
        "I3": I3,
        "target": target,
        "decomposition_residual": sp.factor(density - target),
        "density_hypersurface_orthogonal": density_ho,
        "density_exact_luminal": density_luminal,
        "density_exact_luminal_and_c123_zero": density_degenerate,
        "density_ho_exact_luminal": density_ho_luminal,
        "density_ho_exact_luminal_and_c123_zero": density_ho_degenerate,
        "hessian_exact_luminal": hessian_luminal,
        "hessian_rank_c123_nonzero": hessian_samples["c123_nonzero"].rank(),
        "hessian_rank_c123_zero": hessian_samples["c123_zero"].rank(),
        "hessian_shape": hessian.shape,
        "K_symbols": (k11, k22, k33, k12, k13, k23),
        "W_symbols": (w12, w13, w23),
        "a_symbols": (a1, a2, a3),
    }


def _scalar_dirac(adm):
    c1, c2, c3, c4 = adm["symbols"]
    tau, p_tau, tau_dot, k = sp.symbols("tau p_tau tau_dot k", real=True)
    # A single real Fourier direction.  K_ij = d_i d_j tau and
    # a_i = d_i dot(tau), so the exact coefficients are c123 and c14.
    k11 = adm["K_symbols"][0]
    a1 = adm["a_symbols"][0]
    substitutions = {k11: k**2 * tau, a1: k * tau_dot}
    for item in adm["K_symbols"][1:]:
        substitutions[item] = 0
    for item in adm["W_symbols"]:
        substitutions[item] = 0
    for item in adm["a_symbols"][1:]:
        substitutions[item] = 0
    L_mode = sp.factor(adm["density"].subs(substitutions))
    c13 = c1 + c3
    c14 = c1 + c4
    c123 = c1 + c2 + c3
    coefficient_residual = sp.factor(L_mode - (c123 * k**4 * tau**2
                                               - c14 * k**2 * tau_dot**2))
    p_mode = sp.factor(sp.diff(L_mode, tau_dot))
    velocity_hessian = sp.factor(sp.diff(L_mode, tau_dot, 2))
    luminal = {c3: -c1, c4: -c1}
    L_luminal = sp.factor(L_mode.subs(luminal))
    p_luminal = sp.factor(p_mode.subs(luminal))
    H_luminal = sp.factor(-L_luminal)  # p_tau=0, hence H=p dot(tau)-L.
    secondary_luminal = sp.factor(-sp.diff(H_luminal, tau))
    constraints_nonzero = [p_tau, secondary_luminal]
    q = (tau,)
    p = (p_tau,)
    pb_nonzero = sp.Matrix([[_pb(A, B, q, p) for B in constraints_nonzero]
                            for A in constraints_nonzero])
    u = sp.symbols("u_tau", real=True)
    tertiary_nonzero = sp.factor(_pb(secondary_luminal, H_luminal + u * p_tau, q, p))
    closure_nonzero = sp.solve(sp.Eq(tertiary_nonzero, 0), u, dict=True)
    # c123=0 removes the secondary, so the quadratic PB block is generated
    # from the constraints that actually survive the derived equation.
    deg_sub = {c1: 1, c2: 0, c3: -1, c4: -1}
    secondary_degenerate = sp.factor(secondary_luminal.subs(deg_sub))
    surviving_deg = [p_tau] + ([secondary_degenerate]
                                if secondary_degenerate != 0 else [])
    pb_degenerate = sp.Matrix([[_pb(A, B, q, p) for B in surviving_deg]
                               for A in surviving_deg])
    # k=0 must not be inferred from the k!=0 matrix.
    zero_sub = {k: 0}
    L_zero = sp.factor(L_luminal.subs(zero_sub))
    p_zero = sp.factor(p_luminal.subs(zero_sub))
    return {
        "L_mode": L_mode,
        "coefficient_residual": coefficient_residual,
        "p_mode": p_mode,
        "velocity_hessian": velocity_hessian,
        "L_exact_luminal": L_luminal,
        "p_exact_luminal": p_luminal,
        "H_exact_luminal": H_luminal,
        "secondary_exact_luminal": secondary_luminal,
        "pb_exact_luminal": pb_nonzero,
        "pb_rank_exact_luminal_c123_nonzero": pb_nonzero.subs({c1: 1, c2: 1, k: 1}).rank(),
        "pb_det_exact_luminal": sp.factor(pb_nonzero.det()),
        "tertiary_exact_luminal": tertiary_nonzero,
        "closure_multiplier_exact_luminal": closure_nonzero,
        "secondary_degenerate": secondary_degenerate,
        "surviving_degenerate_constraints": surviving_deg,
        "pb_degenerate": pb_degenerate,
        "pb_rank_degenerate": pb_degenerate.rank(),
        "L_zero_mode": L_zero,
        "p_zero_mode": p_zero,
        "zero_mode_primary_constraint": "p_tau=0 (the derived momentum is identically zero at k=0)",
        "zero_mode_constraint_count": 1,
    }


def _exponential_constitutive():
    y = sp.symbols("y", positive=True)
    F = sp.Rational(1, 2) * y**2 + (1 + y) * sp.exp(-y) - 1
    H_correction = sp.simplify(2 * F - y**2)
    mu = sp.factor(sp.diff(F, y) / y)
    transverse = sp.factor(sp.diff(F, y) / y)
    longitudinal = sp.factor(sp.diff(F, y, 2))
    return {
        "F": F,
        "ALC_H_correction": H_correction,
        "mu": mu,
        "flux_residual": sp.simplify(sp.diff(F, y) / y - (1 - sp.exp(-y))),
        "transverse_hessian": transverse,
        "longitudinal_hessian": longitudinal,
        "longitudinal_positive_transform": sp.factor(sp.exp(y) * longitudinal),
        "transverse_positive_transform": sp.factor(sp.exp(y) * transverse),
        "finite_y_hessian_nonzero": sp.simplify(longitudinal.subs(y, 1)),
        "ALC_H_longitudinal_hessian": sp.factor(sp.diff(H_correction, y, 2)),
        "ALC_H_hessian_at_y_half": sp.simplify(sp.diff(H_correction, y, 2).subs(y, sp.Rational(1, 2))),
        "ALC_H_hessian_at_y_two": sp.simplify(sp.diff(H_correction, y, 2).subs(y, 2)),
    }


def derive_gate():
    adm = _adm_decomposition()
    scalar = _scalar_dirac(adm)
    exponential = _exponential_constitutive()
    c1, c2, c3, c4 = adm["symbols"]
    return {
        "adm": {key: value for key, value in adm.items() if key not in ("symbols", "K_symbols", "W_symbols", "a_symbols")},
        "scalar_dirac": scalar,
        "exponential": exponential,
        "exact_branch": {
            "c13": sp.simplify((c1 + c3).subs({c3: -c1})),
            "c14": sp.simplify((c1 + c4).subs({c4: -c1})),
            "c123_equals": sp.simplify((c1 + c2 + c3).subs({c3: -c1})),
        },
        "status": "OPEN",
        "scope": "constant-aether ADM regularisation of the ALC corner; not a universal theorem about nonlocal or non-minimally coupled actions",
    }


def _jsonable(value):
    """Convert SymPy expressions/matrices and symbolic dictionary keys."""
    if isinstance(value, dict):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [_jsonable(item) for item in value]
    if isinstance(value, sp.MatrixBase):
        return [[_jsonable(item) for item in row] for row in value.tolist()]
    if isinstance(value, sp.Basic):
        return str(value)
    return value


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path,
                        default=HERE / "run_001" / "degenerate_dirac.json")
    args = parser.parse_args(argv)
    result = derive_gate()
    serializable = _jsonable(result)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(serializable, indent=2) + "\n")
    print(json.dumps(serializable, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
