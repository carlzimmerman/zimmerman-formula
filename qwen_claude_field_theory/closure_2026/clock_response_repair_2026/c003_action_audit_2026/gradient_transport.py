#!/usr/bin/env python3
"""Exact kinematic tracking condition, not an integrated attractor proof."""
import argparse
import json
from pathlib import Path
import sympy as s


def derive():
    # Local jets of ds²=-N(t,x)²dt²+a(t)²dx², zero shift.
    # H denotes proper expansion a_dot/(a*N) at the evaluation point.
    a, N = s.symbols("a N", positive=True)
    H, chidot = s.symbols("H chidot", real=True)
    b = s.Matrix(s.symbols("b1:4", real=True))
    bdot = s.Matrix(s.symbols("bdot1:4", real=True))
    dN = s.Matrix(s.symbols("N1:4", real=True))
    Q = chidot/N
    Y = b.dot(b)/a**2
    dQ = bdot/N - chidot*dN/N**2
    acceleration = dN/N
    raw = 2*b.dot(bdot)/(N*a**2)-2*H*Y
    projected = 2*b.dot(dQ+Q*acceleration)/a**2-2*H*Y
    uniform = projected.subs(dict(zip(dN, [0]*3))).subs(dict(zip(bdot, [0]*3)))
    target, target_rate, source = s.symbols("Ystar Ystar_dot source", real=True)
    error_rate = source-2*H*target-target_rate
    required_source = s.solve(error_rate, source)[0]
    return {"transport_residual": s.simplify(raw-projected),
            "uniform_gradient_residual": s.simplify(uniform+2*H*Y),
            "required_source": required_source,
            "tracking_symbols": (H, target, target_rate),
            "raw_derivative": raw, "projected_derivative": projected}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--result", type=Path, required=True)
    args = parser.parse_args()
    result = derive()
    assert result["transport_residual"] == 0
    assert result["uniform_gradient_residual"] == 0
    out = {key: str(value) for key, value in result.items()}
    out["scope"] = "Exact local lapse/FLRW-spatial-metric jet identity; general covariant derivation is in GRADIENT_TRACKING.md."
    out["non_claims"] = ["No field-equation solution or attracting trajectory computed.",
                         "No sound-speed expression assumed or certified.",
                         "No new law of nature or global impossibility theorem."]
    args.result.write_text(json.dumps(out, indent=2)+"\n")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
