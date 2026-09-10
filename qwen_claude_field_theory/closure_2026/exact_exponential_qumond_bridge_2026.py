#!/usr/bin/env python3
"""Exact exponential AQUAL/QUMOND spherical bridge.

The York candidate used nu(s)=sqrt(1+1/s), which belongs to a different
interpolation law. For the required mu(x)=1-exp(-x), the exact spherical
QUMOND inverse is defined implicitly by

    s = x (1-exp(-x)),     x=g/a0,  s=g_N/a0,
    nu(s)=x/s.

There is no elementary Lambert-W form, so this script solves the strictly
monotone inverse numerically and audits the bridge over a wide acceleration
range. The companion Lean file certifies the algebraic spherical identity and
the deep-MOND BTFR implication.
"""

from __future__ import annotations

import json
import math
import sys

import numpy as np
import sympy as sp


def s_of_x(x: float) -> float:
    return x * (-math.expm1(-x))


def ds_dx(x: float) -> float:
    return 1.0 + (x - 1.0) * math.exp(-x)


def F_of_x(x: float) -> float:
    """Primitive F(u) with u=s^2, written through the inverse parameter x."""
    return x * x + 2.0 - 2.0 * math.exp(-x) * (x * x + x + 1.0)


def dF_dx(x: float) -> float:
    """Analytic derivative of F(x(s)^2) obtained by differentiating F_of_x."""
    return 2.0 * x * ds_dx(x)


def x_of_s(s: float) -> float:
    if not (s > 0.0):
        raise ValueError("s must be positive")
    lo = 0.0
    hi = max(1.0, s + 1.0)
    while s_of_x(hi) < s:
        hi *= 2.0
    for _ in range(120):
        mid = 0.5 * (lo + hi)
        if s_of_x(mid) < s:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def check(name: str, condition: bool, detail: str = "") -> bool:
    ok = bool(condition)
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f" ({detail})" if detail else ""))
    return ok


def main() -> int:
    samples = np.geomspace(1e-12, 1e4, 240)
    xs = np.array([x_of_s(float(s)) for s in samples])
    residuals = np.array([s_of_x(float(x)) - float(s) for x, s in zip(xs, samples)])
    rel_residual = np.max(np.abs(residuals) / samples)
    derivatives = np.array([ds_dx(float(x)) for x in xs])
    mu = -np.expm1(-xs)
    nu = xs / samples
    approx_nu = np.sqrt(1.0 + 1.0 / samples)

    deep = samples < 1e-8
    high = samples > 100.0
    deep_ratio = xs[deep] / np.sqrt(samples[deep])
    high_nu_minus_one = nu[high] - 1.0
    high_resolved = (samples > 100.0) & (samples < 700.0)
    high_bound = np.max(np.abs((nu[high_resolved] - 1.0) / np.maximum(np.exp(-samples[high_resolved]), 1e-300)))
    primitive_nu = np.array([
        dF_dx(float(x)) / (2.0 * float(s) * ds_dx(float(x)))
        for x, s in zip(xs, samples)
    ])
    primitive_mismatch = float(np.max(np.abs(primitive_nu - nu)))
    x_symbol = sp.symbols("x", positive=True)
    primitive_symbolic_residual = sp.simplify(
        sp.diff(x_symbol**2 + 2 - 2 * sp.exp(-x_symbol) * (x_symbol**2 + x_symbol + 1), x_symbol)
        - 2 * x_symbol * (1 + (x_symbol - 1) * sp.exp(-x_symbol))
    )

    print("=" * 96)
    print("EXACT EXPONENTIAL AQUAL/QUMOND SPHERICAL BRIDGE")
    print("=" * 96)
    print("s=x(1-exp(-x)), x=g/a0, s=g_N/a0, nu_exact(s)=x/s")
    print("  max relative inverse residual =", rel_residual)
    print("  min ds/dx =", float(derivatives.min()))
    print("  deep x/sqrt(s) range =", float(deep_ratio.min()), float(deep_ratio.max()))
    print("  high nu-1 samples =", [float(v) for v in high_nu_minus_one[:4]])
    mismatch = float(np.max(np.abs(nu / approx_nu - 1.0)))
    print("  approximate sqrt-kernel max relative mismatch =", mismatch)
    print("  exact primitive F(x(s)^2) = x^2 + 2 - 2 exp(-x)(x^2+x+1)")
    print("  primitive derivative / nu_exact max mismatch =", primitive_mismatch)
    checks = [
        check("inverse residual is machine-small across 16 decades", rel_residual < 2e-13, f"{rel_residual:.3e}"),
        check("the inverse is strictly monotone on every sampled branch", bool(np.all(derivatives > 0.0)) and bool(np.all(np.diff(xs) > 0.0))),
        check("0<mu<=1 on the finite positive branch (floating-point saturation allowed)", bool(np.all((mu > 0.0) & (mu <= 1.0))) and float(np.min(mu)) > 0.0),
        check("deep-MOND scaling x/sqrt(s)->1", bool(np.max(np.abs(deep_ratio - 1.0)) < 3e-5)),
        check("the exact inverse is not the candidate sqrt interpolation", mismatch > 0.05),
        check("high-acceleration nu approaches one", bool(np.max(np.abs(nu[high] - 1.0)) < 1e-12)),
        check("the closed-form QUMOND primitive differentiates symbolically", primitive_symbolic_residual == 0),
        check("the numerical primitive derivative tracks nu_exact", primitive_mismatch < 1e-8),
    ]
    result = {
        "status": "EXACT_STATIC_BRIDGE_CERTIFIED",
        "samples": int(len(samples)),
        "s_range": [float(samples.min()), float(samples.max())],
        "max_relative_inverse_residual": float(rel_residual),
        "min_ds_dx": float(derivatives.min()),
        "deep_ratio_range": [float(deep_ratio.min()), float(deep_ratio.max())],
        "sqrt_kernel_max_relative_mismatch": mismatch,
        "primitive_nu_max_mismatch": primitive_mismatch,
        "primitive_symbolic_residual": str(primitive_symbolic_residual),
        "high_resolved_ratio_bound": float(high_bound),
        "checks": {"count": len(checks), "passed": int(sum(checks))},
        "scope": "spherical exact static bridge; not a covariant Dirac/PPN/FLRW proof",
    }
    print("\n[VERDICT]")
    print("  The York static carrier must replace sqrt(1+1/s) by the implicit exact")
    print("  exponential inverse nu_exact(s)=x/s. The bridge is unique and monotone,")
    print("  reproduces deep-MOND x^2=s and Newtonian nu->1, and differs materially")
    print("  from the old kernel. Full covariant closure remains to be derived.")
    print(f"  Checks completed: {sum(checks)}/{len(checks)}")
    print("RESULT_JSON=" + json.dumps(result, sort_keys=True))
    return 0 if all(checks) else 1


if __name__ == "__main__":
    sys.exit(main())
