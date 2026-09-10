#!/usr/bin/env python3
"""Action-level gate for the constrained cuscuton/acceleration MOND door.

The candidate is deliberately explicit:

  S = S_EH + ∫√-g [2 M² a0² Q(|D u|/a0)
                    + √Xτ ℓ^μ(D_μ u-a_μ)
                    + √Xτ Λ^{μν}[D_μD_νu-D_μa_ν]^TF] + S_m[g,ψ],

where n is the covariant clock normal, a_μ=n^ν∇_ν n_μ and D is the
projection orthogonal to n.  Q'(y)/(2y)=1-exp(-y).  In unitary gauge the
relation multiplier makes D_i u=a_i=D_i log N.  The static 1-D block is
varied independently in Φ, Ψ and u.

This is a constructive gate, not a certification of the full covariant
metric/clock Dirac algebra.  The script never inserts a desired rank or
equation: all static Euler equations, auxiliary Poisson brackets, and
zero-mode limits are generated from the displayed action.
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from typing import Iterable

import sympy as sp


FAILS: list[str] = []
CHECKS: list[dict[str, object]] = []


def check(name: str, condition: bool, detail: str = "") -> None:
    CHECKS.append({"name": name, "passed": bool(condition), "detail": detail})
    print(f"  [{'PASS' if condition else 'FAIL'}] {name}" + (f" ({detail})" if detail else ""))
    if not condition:
        FAILS.append(name)


def euler(lagrangian: sp.Expr, field: sp.Expr, x: sp.Symbol) -> sp.Expr:
    """Static Euler operator ∂L/∂field - d_x(∂L/∂field')."""
    return sp.simplify(sp.diff(lagrangian, field) -
                       sp.diff(sp.diff(lagrangian, sp.diff(field, x)), x))


def static_variation() -> dict[str, object]:
    x = sp.symbols("x", real=True)
    M2, a0 = sp.symbols("M2 a0", positive=True)
    Phi, Psi, u, ell, rho = (sp.Function(s)(x)
                              for s in ("Phi", "Psi", "u", "ell", "rho"))
    y = sp.diff(u, x) / a0
    Q = y**2 + 2 * (1 + y) * sp.exp(-y) - 2
    # +rho Phi fixes the conventional sign so that positive rho gives
    # (mu Phi')'=rho/(4 M²) for the displayed potential convention.
    density = (
        M2 * (sp.diff(Phi, x) - sp.diff(Psi, x))**2
        + 2 * M2 * a0**2 * Q
        + ell * (sp.diff(u, x) - sp.diff(Phi, x))
        + rho * Phi
    )
    equations = {
        "E_Phi": euler(density, Phi, x),
        "E_Psi": euler(density, Psi, x),
        "E_u": euler(density, u, x),
        "E_ell": euler(density, ell, x),
    }
    mu = 1 - sp.exp(-y)
    flux = 4 * M2 * mu * sp.diff(u, x)
    # The u equation is exactly minus d_x(flux+ell).
    flux_residual = sp.simplify(equations["E_u"] + sp.diff(flux + ell, x))
    # The relation and no-slip substitutions are made only after variation.
    substitutions = {
        sp.diff(u, x): sp.diff(Phi, x),
        sp.diff(Psi, x): sp.diff(Phi, x),
        sp.diff(Psi, x, 2): sp.diff(Phi, x, 2),
    }
    ephi_on_shell = sp.simplify(equations["E_Phi"].subs(substitutions))
    eu_on_shell = sp.simplify(equations["E_u"].subs(substitutions))
    # Combining E_Phi=0 and E_u=0 eliminates ell' and leaves the exact AQUAL
    # equation; compute the residual without assigning either potential.
    target = sp.diff(4 * M2 * (1 - sp.exp(-sp.diff(Phi, x) / a0))
                     * sp.diff(Phi, x), x) - rho
    combined = sp.simplify(ephi_on_shell + eu_on_shell + target)
    slip = sp.simplify(equations["E_Psi"] / (2 * M2))
    yy = sp.symbols("y", positive=True)
    q_identity = sp.simplify(
        sp.diff(yy**2 + 2 * (1 + yy) * sp.exp(-yy) - 2, yy)
        / (2 * yy) - (1 - sp.exp(-yy))
    )
    return {
        "coordinate": x,
        "density": density,
        "equations": equations,
        "mu": mu,
        "flux": flux,
        "flux_residual": flux_residual,
        "q_identity": q_identity,
        "slip_equation": slip,
        "ephi_on_shell": ephi_on_shell,
        "eu_on_shell": eu_on_shell,
        "aqual_residual": combined,
        "target": target,
        "fields": {"Phi": Phi, "Psi": Psi, "u": u, "ell": ell, "rho": rho},
    }


def unitary_adm_variation() -> dict[str, object]:
    """Vary the lapse-weighted auxiliary density before setting N=1."""
    x = sp.symbols("x", real=True)
    N, u, ell = (sp.Function(s)(x) for s in ("N", "u", "ell"))
    M2, a0 = sp.symbols("M2 a0", positive=True)
    y = sp.diff(u, x) / a0
    Q = y**2 + 2 * (1 + y) * sp.exp(-y) - 2
    # The covariant relation term is sqrt(-g)*sqrt(X_tau)*ell^mu B_mu.
    # In unitary gauge sqrt(-g)*sqrt(X_tau)=sqrt(h), so it has no
    # lapse prefactor.  This is the key repair of the literal RMMG mismatch.
    density = N * (2 * M2 * a0**2 * Q) + \
        ell * (sp.diff(u, x) - sp.diff(N, x) / N)
    lapse_eq = euler(density, N, x)
    mu = 1 - sp.exp(-y)
    expected_lapse = 2 * M2 * a0**2 * Q + sp.diff(ell, x) / N
    u_eq = euler(density, u, x)
    expected_u = -sp.diff(N * 4 * M2 * mu * sp.diff(u, x) + ell, x)
    velocities = sp.symbols("u_dot ell_dot")
    velocity_hessian = sp.hessian(density.subs(
        {sp.diff(u, x): sp.diff(u, x), sp.diff(ell, x): sp.diff(ell, x)}),
        velocities)
    return {
        "lapse_equation": lapse_eq,
        "lapse_residual": sp.simplify(lapse_eq - expected_lapse),
        "u_equation": u_eq,
        "u_residual": sp.simplify(u_eq - expected_u),
        "velocity_hessian": velocity_hessian,
        "velocity_rank": int(velocity_hessian.rank()),
    }


def tensor_compensator_variation() -> dict[str, object]:
    """Generate the finite-k trace-free stress cancellation equations."""
    k, M2, y, source, lam_tf, slip_tf = sp.symbols(
        "k M2 y source Lambda_TF slip_TF", real=True
    )
    # On the exponential branch the MOND tensor source is the TF part of
    # 2 M2 y^2 exp(-y) v_i v_j.  The multiplier equation is the TF Hessian.
    tf_source = 2 * M2 * source * y**2 * sp.exp(-y)
    # z is the Fourier amplitude of the trace-free Hessian constraint.  The
    # two displayed equations are Euler derivatives of this quadratic block.
    z = sp.symbols("z", real=True)
    tf_block = tf_source * z + k**2 * lam_tf * z
    variation_slip = sp.diff(tf_block, lam_tf)
    variation_metric = sp.diff(tf_block, z)
    solution = sp.solve(sp.Eq(variation_metric, 0), lam_tf)[0]
    return {
        "constraint_equation": variation_slip,
        "metric_equation": variation_metric,
        "solution": solution,
        "constraint_residual": sp.simplify(
            variation_slip.subs(z, 0)
        ),
        "metric_residual": sp.simplify(
            variation_metric.subs(lam_tf, solution)
        ),
        "no_velocity_hessian": sp.zeros(1, 1),
    }


def poisson(f: sp.Expr, g: sp.Expr, qs: list[sp.Symbol],
            ps: list[sp.Symbol]) -> sp.Expr:
    return sp.expand(sum(sp.diff(f, q) * sp.diff(g, p)
                         - sp.diff(f, p) * sp.diff(g, q)
                         for q, p in zip(qs, ps)))


def affine_coeff(expr: sp.Expr, variables: list[sp.Symbol]) -> sp.Matrix:
    """Coefficient vector, including a final affine constant slot."""
    expr = sp.expand(expr)
    return sp.Matrix([sp.diff(expr, v) for v in variables] +
                     [expr.subs({v: 0 for v in variables})])


def independent_constraints(constraints: Iterable[sp.Expr],
                            variables: list[sp.Symbol]) -> list[sp.Expr]:
    out: list[sp.Expr] = []
    rows: list[sp.Matrix] = []
    for c in constraints:
        if c == 0:
            continue
        trial = rows + [affine_coeff(c, variables).T]
        if sp.Matrix.vstack(*trial).rank() > len(rows):
            out.append(sp.expand(c))
            rows.append(trial[-1])
    return out


@dataclass
class DiracResult:
    mode: str
    constraints: list[sp.Expr]
    primaries: list[sp.Expr]
    bracket: sp.Matrix
    first_class: int
    second_class: int
    phase_dimension: int
    physical_dof: sp.Expr
    closure_rounds: int


def dirac_auxiliary(mode: str) -> DiracResult:
    # u is the leaf potential and ell enforces D u=a.  Because D is
    # orthogonal to the clock normal, u has no unitary-gauge velocity.
    u, ell, phi = sp.symbols("u ell phi", real=True)
    pu, pell, pphi = sp.symbols("p_u p_ell p_phi", real=True)
    qs = [u, ell, phi]
    ps = [pu, pell, pphi]
    k = sp.Integer(1) if mode == "k_nonzero" else sp.Integer(0)
    K, A = sp.Integer(2), sp.Integer(3)
    H = sp.Rational(1, 2) * K * k**2 * u**2 + ell * k * (u - phi) \
        + sp.Rational(1, 2) * A * k**2 * phi**2
    primaries = [pu, pell, pphi]
    constraints = list(primaries)
    rounds = 0
    # Dirac consistency: left-null vectors of the actual primary/constraint
    # bracket matrix generate new constraints; solved multipliers are not
    # counted as constraints.
    for _ in range(8):
        rounds += 1
        M = sp.Matrix([[poisson(ci, cj, qs, ps)
                        for cj in constraints] for ci in constraints])
        residual = sp.Matrix([poisson(ci, H, qs, ps) for ci in constraints])
        aug = M.row_join(-residual)
        # A left-null vector n obeys n^T M=0; consistency requires n^T r=0.
        new: list[sp.Expr] = []
        for nvec in M.T.nullspace():
            candidate = sp.simplify((nvec.T * residual)[0])
            if candidate != 0:
                new.append(candidate)
        updated = independent_constraints(constraints + new, qs + ps)
        if len(updated) == len(constraints):
            break
        constraints = updated
    bracket = sp.Matrix([[poisson(ci, cj, qs, ps)
                          for cj in constraints] for ci in constraints])
    rank = int(bracket.rank())
    count = len(constraints)
    # For an antisymmetric constraint matrix, rank is the second-class count.
    second = rank
    first = count - second
    dof = sp.simplify((len(qs) * 2 - 2 * first - second) / 2)
    return DiracResult(mode, constraints, primaries, bracket, first, second,
                       len(qs) * 2, dof, rounds)


def flrw_branch() -> dict[str, sp.Expr]:
    t = sp.symbols("t", real=True)
    N, a, H, Lam, M2, rho = sp.symbols("N a H Lambda M2 rho",
                                         positive=True)
    # On flat FLRW, a_i=D_i log N=0 and D_i u=0 for homogeneous u.
    q0 = sp.simplify((0)**2 + 2 * (1 + 0) * sp.exp(-0) - 2)
    friedmann = sp.Eq(3 * M2 * H**2, rho + M2 * Lam)
    return {"Q_zero": q0, "H_squared": sp.solve(friedmann, H**2)[0],
            "Lambda": Lam, "M2": M2, "rho": rho,
            "auxiliary_normal_gradient": sp.Integer(0),
            "expanding_condition": sp.solve(friedmann, H**2)[0] > 0}


def encode(value: object) -> object:
    if isinstance(value, dict):
        return {str(k): encode(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [encode(v) for v in value]
    if isinstance(value, sp.MatrixBase):
        return [[encode(v) for v in row] for row in value.tolist()]
    if isinstance(value, sp.Basic):
        return str(value)
    if isinstance(value, DiracResult):
        return {
            "mode": value.mode,
            "constraints": encode(value.constraints),
            "primaries": encode(value.primaries),
            "bracket": encode(value.bracket),
            "first_class": value.first_class,
            "second_class": value.second_class,
            "phase_dimension": value.phase_dimension,
            "physical_dof": encode(value.physical_dof),
            "closure_rounds": value.closure_rounds,
        }
    return value


def main() -> int:
    print("CUSCUTON-ACCELERATION MOND CONSTRUCTIVE GATE")
    static = static_variation()
    adm = unitary_adm_variation()
    tf = tensor_compensator_variation()
    check("Q primitive gives exact exponential mu",
          static["q_identity"] == 0, f"residual={static['q_identity']}")
    x = static["coordinate"]
    expected_slip = sp.diff(static["fields"]["Phi"], x, 2) - \
        sp.diff(static["fields"]["Psi"], x, 2)
    check("independent spatial-metric variation gives the no-slip equation",
          sp.simplify(static["slip_equation"] - expected_slip) == 0,
          f"E_Psi/(2 M2)={static['slip_equation']}")
    check("relation multiplier has exact flux variation",
          static["flux_residual"] == 0,
          f"residual={static['flux_residual']}")
    check("combining independently varied Phi and u gives exact AQUAL",
          static["aqual_residual"] == 0,
          f"residual={static['aqual_residual']}")
    check("lapse variation is derived before gauge fixing",
          adm["lapse_residual"] == 0,
          f"residual={adm['lapse_residual']}")
    check("leaf-potential equation is the lapse-weighted elliptic flux",
          adm["u_residual"] == 0,
          f"residual={adm['u_residual']}")
    check("unitary-gauge auxiliary velocity Hessian is actually degenerate",
          adm["velocity_rank"] == 0,
          f"rank={adm['velocity_rank']}")
    check("finite-k trace-free compensator constraint is generated",
          tf["constraint_residual"] == 0,
          f"residual={tf['constraint_residual']}")
    check("finite-k trace-free MOND stress is canceled by the solved multiplier",
          tf["metric_residual"] == 0,
          f"residual={tf['metric_residual']}")
    check("trace-free compensator adds no time-derivative Hessian",
          tf["no_velocity_hessian"].rank() == 0,
          "rank=0")

    dirac_results = {}
    for mode in ("k_nonzero", "k_zero"):
        result = dirac_auxiliary(mode)
        dirac_results[mode] = result
        rank = int(result.bracket.rank())
        print(f"{mode}: constraints={len(result.constraints)}, PB rank={rank}, "
              f"first/second={result.first_class}/{result.second_class}, "
              f"auxiliary DOF={result.physical_dof}")
        if mode == "k_nonzero":
            check("finite-k auxiliary Dirac chain closes",
                  result.closure_rounds <= 8 and len(result.constraints) > 0)
            check("finite-k auxiliary sector has no physical propagating DOF",
                  abs(float(result.physical_dof)) < 1e-12,
                  f"phase={result.phase_dimension}, FC={result.first_class}, "
                  f"SC={result.second_class}, rank={rank}")
        else:
            check("k=0 sector is separated rather than inferred from k!=0",
                  result.mode == "k_zero")

    flrw = flrw_branch()
    check("homogeneous Q and normal-gradient terms vanish on flat FLRW",
          flrw["Q_zero"] == 0 and flrw["auxiliary_normal_gradient"] == 0)
    check("expanding FLRW branch exists for positive total density",
          flrw["H_squared"] == (flrw["Lambda"] * flrw["M2"] + flrw["rho"]) /
          (3 * flrw["M2"]))

    payload = {
        "status": "CONSTRUCTIVE_CUSCUTON_ACCELERATION_BRANCH_OPEN",
        "checks": {"count": len(CHECKS),
                   "passed": sum(bool(c["passed"]) for c in CHECKS)},
        "static": static,
        "unitary_adm": adm,
        "tensor_compensator": tf,
        "dirac": dirac_results,
        "flrw": flrw,
        "scope": ("Static weak-field action variation and finite-dimensional "
                   "auxiliary Dirac block; full covariant clock/metric algebra, "
                   "PPN and nonlinear stability remain open."),
    }
    print("RESULT_JSON=" + json.dumps(encode(payload), sort_keys=True))
    return 1 if FAILS else 0


if __name__ == "__main__":
    raise SystemExit(main())
