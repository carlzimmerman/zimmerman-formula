#!/usr/bin/env python3
"""Orthogonal analytic-kernel benchmark of the l=1 Ritz susceptibility."""

import argparse
import json
from pathlib import Path

import mpmath as mp


mp.mp.dps = 80


def jl(ell, z):
    return mp.sqrt(mp.pi / (2 * z)) * mp.besselj(ell + mp.mpf("0.5"), z)


def static(q):
    j0, j1, j2 = [jl(ell, q) for ell in range(3)]
    aa = (j1**2 - j0 * j2) / 2
    bb = q * j0 / (mp.pi * (mp.pi**2 - q**2))
    jj = j2 / q
    pp = q**2 / (q**2 - mp.pi**2)
    return 9 * mp.pi**2 / q**2 * pp * (aa - jj / (3 / mp.pi**3) * bb)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--result", required=True)
    args = parser.parse_args()
    previous = json.loads(Path(args.input).read_text())
    rows = []
    for data in previous["total"][-1]["source_rows"]:
        q = mp.mpf(str(data["kR"]))
        exact = static(q)
        ritz = mp.mpf(str(data["4piG_chiP_over_object_volume"]))
        relerr = abs(ritz / exact - 1)
        assert relerr < mp.mpf("1e-6")
        rows.append({"kR": str(q), "analytic_80_digit_kernel": str(exact), "Ritz_relative_error": float(relerr)})
    # Independent direct integration of the regular static solution; this
    # checks Bessel overlap factors and the projected-COM inverse in formula.
    for qstr in ["0.1", "1", "3"]:
        q = mp.mpf(qstr)
        p = q**2 / (q**2 - mp.pi**2)
        h = lambda x: p * (jl(1, q * x) - (jl(2, q) / q) / (3 / mp.pi**3) * jl(1, mp.pi * x))
        com = mp.quad(lambda x: x**3 * h(x), [0, 1])
        direct = 9 * mp.pi**2 / q**2 * mp.quad(lambda x: x**2 * jl(1, q * x) * h(x), [0, 1])
        assert abs(com) < mp.mpf("1e-60")
        assert abs(direct / static(q) - 1) < mp.mpf("1e-60")
    c4 = 1 / (5 * mp.pi**2) - mp.mpf(2) / 105
    q = mp.mpf("0.0001")
    assert abs(static(q) / q**4 / c4 - 1) < mp.mpf("1e-8")
    result = {
        "assertion_tested": "The COM-projected closed static l=1 kernel agrees with the finite Ritz response at six prescribed kR and with direct 80-digit Bessel quadrature at three kR; infrared coefficient matches to the expected finite-q order.",
        "rows": rows,
        "infrared_q4_coefficient": str(c4),
        "mpmath_version": mp.__version__,
        "precision_decimal_digits": mp.mp.dps,
        "direct_quadrature_kR": ["0.1", "1", "3"],
        "status": "all finite assertions passed",
        "non_claims": ["No interval certification", "Only the l=1 internal sector; higher and lower angular channels are separate", "No occupancy or nonlinear constitutive law"],
    }
    Path(args.result).write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"status": result["status"], "max_Ritz_relative_error": max(r["Ritz_relative_error"] for r in rows), "infrared_q4_coefficient": str(c4)}, indent=2))


if __name__ == "__main__":
    main()
