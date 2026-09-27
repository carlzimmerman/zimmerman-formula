#!/usr/bin/env python3
"""Exact homogeneous-sector separation check; no cosmological fit or particle input.

Conventions: c=1, signature (-,+,+,+), ds²=-N²dt²+a²dx²,
Q=phi_dot/N, L=N*a³*K(Q), K=-V+A*(Q-Q0)²/2, A,N,a>0.
rho=-a^-3 dL/dN; p=(3*N*a²)^-1 dL/da; I=dL/dphi_dot.
This is a bounded symbolic audit of this specified first-derivative scalar
sector, not the full C-H/K action, the scalar's perturbative health, or data.
"""
import argparse
import json
from pathlib import Path
import sympy as s


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    N, a, A = s.symbols("N a A", positive=True)
    V, Q0, velocity, I, C, Q = s.symbols("V Q0 phi_dot I C Q", real=True)
    checks, expressions = {}, {}

    def exact(name, expression):
        value = s.simplify(expression)
        checks[name] = {"residual": str(value), "passed": value == 0}
        assert value == 0, (name, value)

    K = -V + A * (Q - Q0)**2 / 2
    L = N * a**3 * K.subs(Q, velocity / N)
    rho_variation = -s.diff(L, N) / a**3
    pressure_variation = s.diff(L, a) / (3 * N * a**2)
    charge_variation = s.diff(L, velocity)
    exact("lapse_stress", rho_variation - (Q * s.diff(K, Q) - K).subs(Q, velocity / N))
    exact("scale_factor_pressure", pressure_variation - K.subs(Q, velocity / N))
    exact("Noether_charge", charge_variation - a**3 * s.diff(K, Q).subs(Q, velocity / N))

    Q_solution = Q0 + I / (A * a**3)
    rho = s.expand((Q * s.diff(K, Q) - K).subs(Q, Q_solution))
    pressure = s.expand(K.subs(Q, Q_solution))
    exact("charge_solution", (a**3 * s.diff(K, Q)).subs(Q, Q_solution) - I)
    exact("vacuum_dust_stiff_separation", rho - (V + Q0*I/a**3 + I**2/(2*A*a**6)))
    exact("pressure_separation", pressure - (-V + I**2/(2*A*a**6)))
    exact("continuity_independent_invariant", a*s.diff(rho, a) + 3*(rho + pressure))
    exact("zero_charge_vacuum", rho.subs(I, 0) - V)
    exact("zero_charge_vacuum_pressure", pressure.subs(I, 0) + V)
    exact("zero_Q0_excitation_stiff", (rho - V).subs(Q0, 0) - (pressure + V))

    # Orthogonal metric check: a homogeneous phi has Y=0, but X=Q²/2.
    g_inv = s.diag(-1/N**2, 1/a**2, 1/a**2, 1/a**2)
    unit_u = s.Matrix([1/N, 0, 0, 0])
    gradient = s.Matrix([velocity, 0, 0, 0])
    projector = g_inv + unit_u * unit_u.T
    Y = (gradient.T * projector * gradient)[0]
    X = -(gradient.T * g_inv * gradient)[0] / 2
    exact("FRW_projected_gradient_vanishes", Y)
    exact("FRW_timelike_gradient_need_not_vanish", X - velocity**2/(2*N**2))

    # Shift the additive vacuum constant before doing the variation.
    shifted_L = L + N*a**3*C
    shifted_rho = -s.diff(shifted_L, N)/a**3
    exact("constant_shift_charge_unchanged", s.diff(shifted_L, velocity) - charge_variation)
    exact("constant_shift_vacuum_moves", shifted_rho - rho_variation + C)
    exact("constant_shift_kernel_unchanged", s.diff(K + C, Q) - s.diff(K, Q))

    expressions.update({"L": str(L), "K": str(K), "Q_charge_solution": str(Q_solution),
                        "rho": str(rho), "pressure": str(pressure),
                        "active_gravity_rho_plus_3p": str(s.expand(rho + 3*pressure)),
                        "FRW_spatial_Y": str(Y), "FRW_timelike_X": str(X)})
    # An exact counterexample to 'homogeneity forces vacuum' at the same V,A,Q0.
    parameters = {a: 1, A: 1, Q0: 1, V: 1}
    counterexample = []
    for charge in (0, 1):
        substitutions = parameters.copy()
        substitutions[I] = charge
        r, p = rho.subs(substitutions), pressure.subs(substitutions)
        counterexample.append({"I": charge, "Q": str(Q_solution.subs(substitutions)),
                               "rho": str(r), "p": str(p), "w": str(p/r)})
    output = {"result": "exact identities verified for the declared homogeneous quadratic sector",
              "checks": checks, "expressions": expressions,
              "same_action_homogeneous_states": counterexample,
              "non_claims": ["No proof of full C-H/K cosmology or nonlinear health",
                             "No new species or particle hypothesis assumed",
                             "No CMB, growth, lensing, or expansion data fitted",
                             "No claim that every khronon action reduces to K(Q)"]}
    target = Path(args.output)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
