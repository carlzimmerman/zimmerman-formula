#!/usr/bin/env python3
"""High-precision audit of the exponential-MOND center Puiseux root.

This script deliberately does not import the symbolic derivation module.  It
solves y(1-exp(-y))=x directly, compares the exact positive root with the
three-term Puiseux approximation, and measures the convergence exponent.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import mpmath as mp


def least_squares_slope(xs: list[float], ys: list[float]) -> float:
    mean_x = sum(xs) / len(xs)
    mean_y = sum(ys) / len(ys)
    return sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys)) / sum(
        (x - mean_x) ** 2 for x in xs
    )


def run_audit() -> dict:
    mp.mp.dps = 80
    dimensionless_sources = [mp.mpf(10) ** (-power) for power in range(3, 13)]
    relative_errors: list[mp.mpf] = []
    residuals: list[mp.mpf] = []
    rows = []

    for source in dimensionless_sources:
        exact_root = mp.findroot(
            lambda y: y * (1 - mp.exp(-y)) - source,
            mp.sqrt(source),
        )
        approximation = (
            mp.sqrt(source)
            + source / 4
            + mp.mpf(7) * source ** mp.mpf("1.5") / 96
        )
        relative_error = abs((approximation - exact_root) / exact_root)
        equation_residual = abs(
            exact_root * (1 - mp.exp(-exact_root)) - source
        )
        relative_errors.append(relative_error)
        residuals.append(equation_residual)
        rows.append(
            {
                "x": float(source),
                "exact_y": float(exact_root),
                "relative_series_error": float(relative_error),
                "error_over_x_3_2": float(relative_error / source ** mp.mpf("1.5")),
            }
        )

    slope = least_squares_slope(
        [math.log(float(value)) for value in dimensionless_sources],
        [math.log(float(value)) for value in relative_errors],
    )
    asymptotic_scaled_error = relative_errors[-1] / (
        dimensionless_sources[-1] ** mp.mpf("1.5")
    )
    expected_scaled_error = mp.mpf(1) / 48
    return {
        "arithmetic": "mpmath 80 decimal digits",
        "equation": "y*(1-exp(-y))=x, positive root",
        "sample_count": len(rows),
        "x_range": [float(dimensionless_sources[-1]), float(dimensionless_sources[0])],
        "relative_error_log_slope": slope,
        "expected_relative_error_log_slope": 1.5,
        "asymptotic_error_over_x_3_2": float(asymptotic_scaled_error),
        "expected_asymptotic_error_over_x_3_2": float(expected_scaled_error),
        "scaled_error_limit_deviation": float(
            abs(asymptotic_scaled_error - expected_scaled_error)
        ),
        "max_equation_residual": float(max(residuals)),
        "rows": rows,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run_audit()
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output is not None:
        args.output.write_text(rendered, encoding="utf-8")
    if args.json:
        print(rendered, end="")
    else:
        print("Independent exponential-MOND center-root audit")
        print(rendered, end="")

    passed = (
        1.49 < result["relative_error_log_slope"] < 1.51
        and result["max_equation_residual"] < 1e-60
        and result["scaled_error_limit_deviation"] < 5e-6
    )
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
