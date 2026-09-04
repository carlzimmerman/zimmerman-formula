#!/usr/bin/env python3
"""Finite-interval consequences of specified algebraic MOND acceleration laws.

The two exponential force inversions reuse the existing vectorized orbit module.
These are algebraic response laws, not non-spherical AQUAL/QUMOND field solves.
The analytic proof is in DERIVATION.md. Run this file to print computed JSON.
"""

from functools import lru_cache
import importlib.util
import json
from pathlib import Path

import numpy as np
import sympy as sp


KERNELS = ("mu_exp", "nu_rar", "simple", "deep", "newton")


@lru_cache(maxsize=1)
def _orbit_module():
    source = Path(__file__).resolve().parents[1] / "two_kernel_orbit_shape_2026" / "orbit_shape.py"
    spec = importlib.util.spec_from_file_location("finite_interval_existing_orbit", source)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _positive_finite(value, name):
    try:
        values = np.asarray(value, dtype=float)
    except (TypeError, ValueError, OverflowError) as error:
        raise ValueError(f"{name} must contain positive finite numbers") from error
    if values.size == 0 or np.any(~np.isfinite(values)) or np.any(values <= 0):
        raise ValueError(f"{name} must contain positive finite numbers")
    return values


def _result(value):
    value = np.asarray(value)
    return float(value) if value.ndim == 0 else value


def acceleration(b, a0, kernel):
    """Return g(b); b>0, scalar a0>0, with scalar or array shape preserved.

    mu_exp solves b=g*(1-exp(-g/a0)); nu_rar is the DISTINCT law
    g=b/(1-exp(-sqrt(b/a0))). The numerical tests cover b/a0=1e-16..1e12.
    """
    b = _positive_finite(b, "b")
    scale = _positive_finite(a0, "a0")
    if scale.ndim != 0:
        raise ValueError("a0 must be a scalar")
    a0 = float(scale)
    if kernel not in KERNELS:
        raise ValueError(f"kernel must be one of {KERNELS}")
    with np.errstate(over="ignore", under="ignore", invalid="ignore"):
        s = b / a0
    _positive_finite(s, "b/a0")
    if kernel in ("mu_exp", "nu_rar"):
        value = _orbit_module().acceleration(b, a0, kernel)
    elif kernel == "simple":
        # Solve g^2/(g+a0)=b without squaring the largest dimensional number.
        value = a0 * (s/2 + np.sqrt(s)*np.sqrt(s/4 + 1))
    elif kernel == "deep":
        value = a0 * np.sqrt(s)
    else:
        value = b.copy()
    _positive_finite(value, "predicted acceleration")
    return _result(value)


def finite_transfer(blo, bhi, a0, kernel):
    """Exact log10[g(bhi)/g(blo)] for broadcastable ordered endpoints."""
    lo = _positive_finite(blo, "blo")
    hi = _positive_finite(bhi, "bhi")
    try:
        lo, hi = np.broadcast_arrays(lo, hi)
    except ValueError as error:
        raise ValueError("endpoints must be broadcastable") from error
    if np.any(hi <= lo):
        raise ValueError("every upper baryonic acceleration must exceed the lower one")
    return _result(np.log10(acceleration(hi, a0, kernel))
                   - np.log10(acceleration(lo, a0, kernel)))


def chord_defect(b, g):
    """Log10 middle response minus the endpoint chord, for exactly three radii.

    b must be strictly ascending. g is not sorted or required to be monotone:
    observed violations must remain measurable. Uniform rescalings of either
    input leave the statistic invariant.
    """
    b = _positive_finite(b, "b")
    g = _positive_finite(g, "g")
    if b.shape != (3,) or g.shape != (3,):
        raise ValueError("b and g must each be one-dimensional triples")
    if np.any(np.diff(b) <= 0):
        raise ValueError("b must be strictly ascending")
    logb, logg = np.log10(b), np.log10(g)
    t = (logb[1]-logb[0]) / (logb[2]-logb[0])
    return float(logg[1] - (1-t)*logg[0] - t*logg[2])


@lru_cache(maxsize=1)
def derive():
    """Differentiate both laws with their correct acceleration coordinates.

    All derivatives use natural logarithms. Convexity has the same sign in
    base 10; base-10 curvature is ln(10) times the returned curvature.
    """
    x = sp.Symbol("x", positive=True)
    mu = 1-sp.exp(-x)
    L = x/(sp.exp(x)-1)
    b = {"mu_exp": x*mu, "nu_rar": x**2}
    g = {"mu_exp": x, "nu_rar": x**2/mu}
    slope = {k: sp.simplify(sp.diff(sp.log(g[k]), x)/sp.diff(sp.log(b[k]), x))
             for k in b}
    curvature = {k: sp.simplify(sp.diff(slope[k], x)/sp.diff(sp.log(b[k]), x))
                 for k in b}
    Lprime = sp.diff(L, x)
    numerator = sp.exp(x)*(1-x)-1
    residuals = {
        "exp_slope": sp.simplify(slope["mu_exp"]-1/(1+L)),
        "rar_slope": sp.simplify(slope["nu_rar"]-1+L/2),
        "exp_curvature": sp.simplify(curvature["mu_exp"]+x*Lprime/(1+L)**3),
        "rar_curvature": sp.simplify(curvature["nu_rar"]+x*Lprime/4),
        "Lprime_numerator": sp.simplify(Lprime-numerator/(sp.exp(x)-1)**2),
        "numerator_derivative": sp.simplify(sp.diff(numerator, x)+x*sp.exp(x)),
    }
    return {"x": x, "L": L, "Lprime": Lprime, "Lprime_numerator": numerator,
            "Lprime_numerator_at_zero": numerator.subs(x, 0),
            "Lprime_numerator_derivative": sp.diff(numerator, x),
            "b_over_a0": b, "g_over_a0": g, "slope": slope,
            "curvature": curvature, "residuals": residuals,
            "domains": {"mu_exp": "x=g/a0>0; b=a0*x*(1-exp(-x))",
                        "nu_rar": "x=sqrt(b/a0)>0; g=a0*x^2/(1-exp(-x))"},
            "slope_limits": {k: {"deep": sp.limit(slope[k], x, 0, dir="+"),
                                  "newton": sp.limit(slope[k], x, sp.oo)} for k in b}}


def main():
    derived = derive()
    b = np.array([.003, .3, 30.])
    examples = {}
    for kernel in KERNELS:
        predicted = acceleration(b, 1., kernel)
        examples[kernel] = {"b_over_a0": b.tolist(), "g_over_a0": predicted.tolist(),
                            "log10_transfer": finite_transfer(b[0], b[-1], 1., kernel),
                            "chord_defect_dex": chord_defect(b, predicted)}
    output = {"domains": derived["domains"],
              "logarithm_convention": "slope and curvature use ln; finite statistics use log10",
              "slope": {k: str(v) for k, v in derived["slope"].items()},
              "curvature": {k: str(v) for k, v in derived["curvature"].items()},
              "residuals": {k: str(v) for k, v in derived["residuals"].items()},
              "slope_limits": {k: {a: str(v) for a, v in limits.items()}
                               for k, limits in derived["slope_limits"].items()},
              "Lprime_numerator_at_zero": str(derived["Lprime_numerator_at_zero"]),
              "Lprime_numerator_derivative": str(derived["Lprime_numerator_derivative"]),
              "examples": examples,
              "scope": "Formal corollaries of algebraic laws; no disk-field or empirical certificate."}
    print(json.dumps(output, indent=2))
    return 0 if all(v == 0 for v in derived["residuals"].values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
