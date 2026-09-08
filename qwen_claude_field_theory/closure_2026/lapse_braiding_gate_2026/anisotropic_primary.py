#!/usr/bin/env python3
"""Exact primary-consistency audit for gradient-dependent lapse braiding.

Candidate (m = M^2):
  L_kin = m N sqrt(h)/2 [Q_ij Q^ij - Q^2],
  Q_ij = K_ij + A_ij F, F = (dot(N)-N^i partial_i N)/N,
  A_ij = eta partial_i N partial_j N/(a0^2 N^2) + omega(N) h_ij.

The potential R+2f(s) and minimally coupled matter have no lapse/metric
velocities and do not change this primary calculation. The optional
omega = w_N control is included in the actual metric and lapse variations.

Canonical convention: {h_ij(x), pi^kl(y)} = delta_(i^k delta_j)^l delta(x-y),
{N(x), p_N(y)} = delta(x-y). pi is a weight-one density. Independent
off-diagonal metric coordinates have conjugate momentum 2*pi^ij.

Velocity differentiation gives Psi = p_N - 2 A_ij pi^ij. Its smeared bracket
is NOT inferred from the Hessian. It is computed by Euler derivatives:
  {Psi[u],Psi[v]} = 4 eta/a0^2 integral pi^ij partial_i N/N^2
                                      (v partial_j u-u partial_j v).
All local metric/N terms cancel; the gradient-N Euler term survives.

Counterexample on the flat three-torus, coordinates of period 2*pi:
  N = n + e sin(x), n>e>0,
  F0(N) = (n^2-e^2)/N - N + 2 n log(N),
  pi^xx = P = P0 exp(eta F0(N)/a0^2), other pi^ij = 0,
  p_N = 2 eta P (N'/N)^2/a0^2, omega=0.
Then P' = eta P (N')^3/(a0^2 N^2), so Psi=0 and the FULL spatial momentum
constraint H_i=-2 h_ik D_j pi^jk+p_N partial_i N is zero. N>0, h is positive
definite, and all fields are smooth and periodic. The nondegenerate six-
metric-velocity block ensures these momenta lie in the Legendre image.

Take a nonzero C-infinity bump u inside |x|,|y|,|z|<1/2 and v=x*u,
extended by zero on the torus. The bracket is
  -4 eta/a0^2 integral P N' u^2/N^2,
strictly nonzero for eta!=0. Thus it cannot be a regular combination of
Psi and H_i. For a smooth omega=w_N control, multiplying P by exp(w(N))
and adding 2 w_N P to p_N gives the same counterexample.

This refutes weak self-commutation modulo those constraints. It assigns no
degree-of-freedom count: the first-order symbol vanishes for transverse
wavevectors and at zero wavevector, and the full Dirac algorithm, lower-
order transport terms and boundary conditions remain separate obligations.

No files are written. Default exit 0 means the audit ran and its algebra
checks passed; --require-primary-consistency exits 2 for this counterexample.
"""

import argparse
from functools import lru_cache
import json
import math

import sympy as s
from scipy.integrate import quad


PAIRS = ((0, 0), (1, 1), (2, 2), (0, 1), (0, 2), (1, 2))


def _symmetric(values, momentum=False):
    matrix = s.zeros(3)
    for value, (i, j) in zip(values, PAIRS):
        entry = value/2 if momentum and i != j else value
        matrix[i, j] = matrix[j, i] = entry
    return matrix


@lru_cache(maxsize=1)
def derive_velocity_primary():
    """Differentiate the kinetic action before constructing its primary.

An orthonormal spatial frame is used at the point. This loses no rank
information for positive-definite h; the metric variation is retained
without this specialization in derive_smeared_bracket(). Shift terms only
translate velocities, so they are set to zero for this local Legendre map.
"""
    N, m = s.symbols("N m", positive=True)
    metric_velocities = s.symbols("hd00 hd11 hd22 hd01 hd02 hd12")
    Nd = s.Symbol("Nd")
    A_values = s.symbols("A00 A11 A22 A01 A02 A12")
    A = _symmetric(A_values)
    Q = _symmetric(metric_velocities)/(2*N) + A*Nd/N
    L = m*N*((Q*Q).trace()-s.trace(Q)**2)/2
    momenta = tuple(s.diff(L, velocity) for velocity in metric_velocities)
    p_N = s.diff(L, Nd)
    primary_residual = s.expand(p_N-2*sum(a*p for a, p in zip(A_values, momenta)))
    velocities = (*metric_velocities, Nd)
    hessian = s.hessian(L, velocities)
    kinetic_hessian_rank = hessian.rank()
    candidate_null = s.Matrix([*(-2*a for a in A_values), 1])
    null_residual = (hessian*candidate_null).applyfunc(s.expand)
    return {
        "N": N, "m": m, "L": L, "Q": Q, "A": A,
        "metric_momenta": momenta, "p_N": p_N,
        "primary_residual": primary_residual,
        "metric_hessian_determinant": s.factor(hessian[:6, :6].det()),
        "hessian_null_residual": null_residual,
        "hessian": hessian,
        "kinetic_hessian_rank": kinetic_hessian_rank,
        "velocity_count": len(velocities),
    }


@lru_cache(maxsize=1)
def derive_smeared_bracket():
    """Actual first-jet Euler derivatives of both smeared constraints.

Spatial derivatives of N, momenta, metric and smearings are independent
jets. Second derivatives of N are symmetric. This retains the full
gradient dependence rather than differentiating a homogeneous surrogate.
"""
    N, a0 = s.symbols("N a0", positive=True)
    eta = s.Symbol("eta", real=True)
    omega = s.Function("omega")(N)
    dN = s.symbols("Nx Ny Nz")
    d2N = _symmetric(s.symbols("Nxx Nyy Nzz Nxy Nxz Nyz"))
    h_values = s.symbols("h00 h11 h22 h01 h02 h12")
    momenta = s.symbols("p00 p11 p22 p01 p02 p12")
    h, pi = _symmetric(h_values), _symmetric(momenta, momentum=True)
    A = eta*s.Matrix(dN)*s.Matrix(dN).T/(a0**2*N**2) + omega*h
    p_N, u, v = s.symbols("p_N u v")
    du, dv = s.symbols("ux uy uz"), s.symbols("vx vy vz")
    constraint = p_N-2*sum(A[i, j]*momenta[k] for k, (i, j) in enumerate(PAIRS))
    Cu, Cv = u*constraint, v*constraint
    fields = (*h_values, *momenta)
    field_jets = {field: s.symbols(f"{field}_x {field}_y {field}_z") for field in fields}

    def spatial_derivative(expression, j):
        answer = s.diff(expression, N)*dN[j]
        answer += sum(s.diff(expression, dN[i])*d2N[i, j] for i in range(3))
        answer += sum(s.diff(expression, field)*field_jets[field][j] for field in fields)
        answer += s.diff(expression, u)*du[j] + s.diff(expression, v)*dv[j]
        return answer

    def lapse_euler(expression):
        return s.diff(expression, N)-sum(
            spatial_derivative(s.diff(expression, dN[j]), j) for j in range(3))

    ELu, ELv = lapse_euler(Cu), lapse_euler(Cv)
    metric_part = s.expand(sum(
        s.diff(Cu, q)*s.diff(Cv, p)-s.diff(Cu, p)*s.diff(Cv, q)
        for q, p in zip(h_values, momenta)))
    bracket = s.expand(ELu*s.diff(Cv, p_N)-s.diff(Cu, p_N)*ELv+metric_part)
    V = 4*eta*pi*s.Matrix(dN)/(a0**2*N**2)
    k = s.symbols("kx ky kz", real=True)
    # integral V^i(v du_i-u dv_i) = integral u[-2 V^i d_i-div(V)]v.
    principal_symbol = s.expand(-2*s.I*V.dot(s.Matrix(k)))
    expected = sum(V[j]*(v*du[j]-u*dv[j]) for j in range(3))
    return {
        "N": N, "eta": eta, "a0": a0, "omega": omega,
        "h": h, "pi": pi, "momenta": momenta, "A": A,
        "u": u, "v": v, "du": du, "dv": dv, "dN": dN,
        "lapse_euler_u": ELu, "lapse_euler_v": ELv,
        "metric_part": metric_part, "bracket_density": bracket,
        "bracket_residual": s.expand(bracket-expected),
        "V": V, "k": k, "principal_symbol": principal_symbol,
    }


@lru_cache(maxsize=1)
def torus_witness():
    """Exact smooth constraint solution; quadrature only illustrates its sign."""
    x = s.Symbol("x", real=True)
    n, e, a0, P0 = s.symbols("n e a0 P0", positive=True)
    eta = s.Symbol("eta", real=True)
    N = n+e*s.sin(x)
    F0 = (n*n-e*e)/N-N+2*n*s.log(N)
    P = P0*s.exp(eta*F0/a0**2)
    p_N = 2*eta*P*(s.diff(N, x)/N)**2/a0**2
    primary = s.simplify(p_N-2*eta*P*(s.diff(N, x)/N)**2/a0**2)
    Hx = -2*s.diff(P, x)+p_N*s.diff(N, x)
    Hx_over_P = s.trigsimp(s.simplify(Hx/P))
    momentum_residuals = [s.simplify(P*Hx_over_P), s.S.Zero, s.S.Zero]

    # Substitute the exact constrained fields and v=x*u into the ACTUAL
    # Euler-derived bracket. No expected bracket value is inserted here.
    bracket = derive_smeared_bracket()
    U, Ux, Uy, Uz = s.symbols("U Ux Uy Uz", real=True)
    substitutions = {
        bracket["N"]: N, bracket["eta"]: eta, bracket["a0"]: a0,
        bracket["u"]: U, bracket["v"]: x*U,
    }
    substitutions.update(zip(bracket["dN"], (s.diff(N, x), 0, 0)))
    substitutions.update(zip(bracket["momenta"], (P, 0, 0, 0, 0, 0)))
    substitutions.update(zip(bracket["du"], (Ux, Uy, Uz)))
    substitutions.update(zip(bracket["dv"], (U+x*Ux, x*Uy, x*Uz)))
    weak_bracket_density = s.factor(bracket["bracket_density"].xreplace(substitutions))
    positive_weight = P*s.diff(N, x)/(a0**2*N**2)
    signed_coefficient = s.simplify(weak_bracket_density/(eta*U**2*positive_weight))
    # On this support cos(x)>0 exactly, not from floating quadrature.
    # With n>e>0, N>=n-e>0; P0 exp(real)>0, e>0 and a0^2>0.
    support_radius = s.Rational(1, 2)
    positive_weight_on_support = bool(0 < support_radius < s.pi/2)
    exact_nonzero = bool(
        primary == 0 and momentum_residuals == [0, 0, 0]
        and positive_weight_on_support and signed_coefficient.is_negative is True)

    def bump(t):
        return math.exp(1-1/(1-4*t*t)) if abs(t) < 0.5 else 0.0

    def weighted(t):
        lapse = 2+math.sin(t)
        momentum = math.exp(3/lapse-lapse+4*math.log(lapse))
        return momentum*math.cos(t)*bump(t)**2/lapse**2

    integral_x, error_x = quad(weighted, -0.5, 0.5, epsabs=1e-12, epsrel=1e-12)
    integral_y, error_y = quad(lambda t: bump(t)**2, -0.5, 0.5,
                             epsabs=1e-12, epsrel=1e-12)
    return {
        "N": N, "P": P, "p_N": p_N, "F0": F0,
        "primary_residual": primary,
        "momentum_residuals": momentum_residuals,
        "N_min": 1,
        "positive_bracket_weight_on_support": positive_weight_on_support,
        "weak_bracket_density": weak_bracket_density,
        "signed_integrand_coefficient": signed_coefficient,
        "exact_nonzero_witness": exact_nonzero,
        "compact_smear_bracket": -4*integral_x*integral_y**2,
        "quadrature_error_estimates": [error_x, error_y],
    }


def run():
    """Return JSON-safe evidence; a successful audit reports failed consistency."""
    velocity = derive_velocity_primary()
    bracket = derive_smeared_bracket()
    witness = torus_witness()
    checks = {
        "primary_from_momenta": velocity["primary_residual"] == 0,
        "six_velocity_block_invertible": velocity["metric_hessian_determinant"] != 0,
        "seven_velocity_null_direction": velocity["hessian_null_residual"] == s.zeros(7, 1),
        "actual_euler_bracket": bracket["bracket_residual"] == 0,
        "metric_variation_cancels": bracket["metric_part"] == 0,
        "witness_primary": witness["primary_residual"] == 0,
        "witness_full_spatial_momentum": witness["momentum_residuals"] == [0, 0, 0],
        "exact_compact_smear_nonzero": witness["exact_nonzero_witness"],
    }
    exact_counterexample = all(checks.values()) and witness["exact_nonzero_witness"]
    strongly_zero = bracket["bracket_density"] == 0
    # Failure of this witness would not by itself establish consistency.
    primary_consistency = not exact_counterexample if exact_counterexample or strongly_zero else None
    verdict = ("refuted, with an exact smooth torus counterexample for eta != 0"
               if exact_counterexample else
               "strong self-commutation verified" if strongly_zero else
               "inconclusive: neither strong vanishing nor a valid weak counterexample established")
    return {
        "candidate": "A_ij=eta partial_i N partial_j N/(a0^2 N^2)+w_N(N) h_ij",
        "claim": "{Psi[u],Psi[v]} vanishes weakly modulo Psi and full H_i",
        "verdict": verdict,
        "algebra_checks_passed": all(checks.values()),
        "checks": checks,
        "primary_consistency": primary_consistency,
        "velocity_primary": {
            "constraint": "Psi=p_N-2 A_ij pi^ij",
            "metric_hessian_determinant": str(velocity["metric_hessian_determinant"]),
            "kinetic_hessian_rank": velocity["kinetic_hessian_rank"],
            "velocity_count": velocity["velocity_count"],
            "normalization": "m=M^2; orthonormal spatial frame; off-diagonal momentum=2 pi^ij",
        },
        "smeared_bracket": {
            "density": str(bracket["bracket_density"]),
            "formula": "4 eta/a0^2 integral pi^ij partial_i N/N^2 (v partial_j u-u partial_j v)",
            "w_N_control": "All local w_N and metric Euler terms cancel; the same obstruction remains.",
        },
        "torus_witness": {
            "domain": "flat T^3, period 2*pi; n>e>0, a0>0, P0>0, eta!=0",
            "N": str(witness["N"]), "F0": str(witness["F0"]),
            "pi_xx": str(witness["P"]), "other_pi": 0,
            "p_N": str(witness["p_N"]),
            "primary_residual": str(witness["primary_residual"]),
            "full_momentum_residuals": [str(item) for item in witness["momentum_residuals"]],
            "smearings": "u=chi(x)chi(y)chi(z), v=x*u; chi(t)=exp(1-1/(1-4t^2)) for |t|<1/2, else 0",
            "exact_sign": "bracket=-4 eta/a0^2 integral P N' u^2/N^2 != 0, since N'>0 on support",
            "actual_weak_bracket_density": str(witness["weak_bracket_density"]),
            "signed_integrand_coefficient": str(witness["signed_integrand_coefficient"]),
            "exact_nonzero_witness": witness["exact_nonzero_witness"],
            "illustration_parameters": {"n": 2, "e": 1, "eta": 1, "a0": 1, "P0": 1},
            "compact_smear_bracket": witness["compact_smear_bracket"],
            "quadrature_error_estimates": witness["quadrature_error_estimates"],
            "proof_role": "Nonzero sign is exact; floating quadrature only illustrates it.",
        },
        "fourier_kernel": {
            "V": "V^i=4 eta pi^ij partial_j N/(a0^2 N^2)",
            "operator": "D=-2 V^i partial_i-partial_i V^i",
            "principal_symbol": str(bracket["principal_symbol"]),
            "longitudinal": "nonzero when V dot k != 0",
            "transverse_and_zero": "frozen principal symbol vanishes for V dot k=0, including k=0",
            "limit": "This does not establish the full variable-coefficient kernel or invertibility; lower-order terms and boundaries matter.",
        },
        "dof_count": None,
        "not_established": ["complete Dirac algorithm", "degree-of-freedom count",
                            "Hamiltonian stability", "secondary consistency on all branches"],
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--require-primary-consistency", action="store_true")
    arguments = parser.parse_args(argv)
    result = run()
    print(json.dumps(result, indent=2, sort_keys=True, allow_nan=False))
    if not result["algebra_checks_passed"]:
        return 1
    return 2 if arguments.require_primary_consistency and not result["primary_consistency"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
