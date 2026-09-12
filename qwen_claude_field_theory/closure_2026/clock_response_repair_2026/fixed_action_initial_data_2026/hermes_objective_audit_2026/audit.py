#!/usr/bin/env python3
"""A deterministic counterexample to a slope-only dust gate, not a candidate action.

Import the original Hermes objective without running its optimizer or changing
any coefficient/action files. A synthetic input audits the implementation only.
"""
import argparse
import importlib.util
import json
from pathlib import Path

import numpy as np


def calculate():
    root = Path(__file__).resolve().parents[5]
    source = root / "hermes_push/search/objective.py"
    spec = importlib.util.spec_from_file_location("hermes_objective", source)
    objective = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(objective)
    a = objective.AGRID.copy()
    q, ratio, s0 = .5, .45, 1.001
    # With q constant and d/U=ratio*a^2, the objective's density simplifies to
    # rho=U0*a^p/(1-2*ratio*q^2*a^2). Choose p to cancel the regression slope
    # of the non-power-law denominator. Its curvature remains nonzero.
    curvature = -np.log(1-2*ratio*q*q*a*a)
    power = -3-np.polyfit(np.log(a), curvature, 1)[0]
    u0 = (3*objective.OMEGA_C)*(1-2*ratio*q*q)
    theta = np.array([np.log10(u0), power, np.log10(ratio*u0), power+2,
                      -1., 0., q, 0., s0, 0.])
    assert all(lo <= value <= hi for value, (lo, hi) in zip(theta, objective.BOUNDS))
    loss, gates = objective.gates(theta)
    density = u0*a**power/(1-2*ratio*q*q*a*a)
    original_density = []
    for scale in a:
        U, d, _, Q, _ = objective.history(theta, scale)
        original_density.append(2*Q*Q*U*d/(U-2*d*Q*Q)+U)
    np.testing.assert_allclose(density, original_density, rtol=1e-14, atol=0.)
    charge = a**3*density
    ratio_span = float(charge.max()/charge.min()-1)
    max_relative_nonconservation = float(np.max(np.abs(charge/charge[-1]-1)))
    # Execution succeeds when the explicit failure of the scientific gate is
    # reproduced. This does not mark dust evolution or field dynamics as passed.
    assert np.isfinite(loss) and loss < 1e-12
    assert all(np.isfinite(value) and value < 1e-12 for value in gates.values())
    assert ratio_span > .14
    assert max_relative_nonconservation > .12
    return {
        "scope": "Synthetic implementation counterexample; no optimizer, action construction, coefficient-file modification, or physical candidate",
        "source": str(source.relative_to(root)),
        "synthetic_parameter_names": objective.PARAM_NAMES,
        "synthetic_theta": theta.tolist(),
        "within_declared_parameter_bounds": True,
        "objective_loss": float(loss),
        "objective_gates": {key: float(value) for key, value in gates.items()},
        "objective_accepts_its_1e_minus_9_threshold": bool(loss < 1e-9),
        "density_formula": "rho=U0*a^p/(1-2*ratio*q^2*a^2), ratio=.45, q=.5; independently agrees with original objective density",
        "constant_charge_check": {
            "quantity": "a^3 rho, necessary for independently conserved pressureless matter",
            "maximum_to_minimum_fractional_span": ratio_span,
            "maximum_relative_deviation_from_a1": max_relative_nonconservation,
            "constant_to_1e_minus_9": bool(max_relative_nonconservation <= 1e-9),
        },
        "samples": [dict(a=float(x), rho=float(r), a3rho=float(c))
                    for x, r, c in zip(a, density, charge)],
        "scientific_outcome": "REFUTED: small total objective loss does not imply its density redshifts as a^-3",
        "execution_outcome": "Implementation counterexample reproduced",
        "non_claims": [
            "No actual solution of the clock/background field equations is constructed or excluded",
            "No physical scalar charge or field evolution is computed; a^3 rho here tests the objective's claimed dust-density law",
            "No change to any existing coefficient history or action; theta is solely an adversarial input to the gate",
            "No complete stability, kinetic-signature, gradient attractor, CMB, PPN, or MOND conclusion",
        ],
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--result", required=True, type=Path)
    args = parser.parse_args()
    result = calculate()
    text = json.dumps(result, indent=2)+"\n"
    args.result.write_text(text)
    print(text, end="")
