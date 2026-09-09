"""Asymptotic, testable rotation-curve prediction of the exact exponential law."""

import json
from pathlib import Path

import sympy as sp


def derive_series():
    eps = sp.symbols("eps", positive=True)
    a, b = sp.symbols("a b")
    y = eps + a * eps**2 + b * eps**3
    lhs = sp.series(y * (1 - sp.exp(-y)), eps, 0, 5).removeO()
    coeff3 = sp.expand(lhs - eps**2).coeff(eps, 3)
    coeff4 = sp.expand(lhs - eps**2).coeff(eps, 4)
    solved = sp.solve([coeff3, coeff4], [a, b], dict=True)[0]
    y_series = sp.expand(y.subs(solved))
    return {
        "implicit_dimensionless_law": "y*(1-exp(-y)) = eps**2",
        "y_series": str(y_series),
        "coefficients": {str(k): str(v) for k, v in solved.items()},
        "rotation_prediction": "v^2 = sqrt(G*M*a0) + G*M/(4*r) + 7*(G*M)^(3/2)/(96*r^2*sqrt(a0)) + O(r^-3)",
        "leading_BTFR": "v^4 = G*M*a0",
    }


if __name__ == "__main__":
    result = derive_series()
    out = Path(__file__).with_name("run_001")
    out.mkdir(exist_ok=True)
    (out / "spherical_prediction.json").write_text(json.dumps(result, indent=2) + "\n")
    print("EXPONENTIAL_SPHERICAL_PREDICTION")
    print(result["y_series"])
    print(result["rotation_prediction"])
