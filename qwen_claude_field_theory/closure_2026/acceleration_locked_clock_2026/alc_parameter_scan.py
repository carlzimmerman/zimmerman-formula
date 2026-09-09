#!/usr/bin/env python3
"""Parameter scan for the acceleration-locked-clock constitutive coefficient."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np


def scan(etas=None):
    # eta multiplies -2 M2 a0^2 [G(Z)-Z^2].  The derived weak-field law is
    # mu_eta(y)=1-eta*exp(-y); exact mu(0)=0 and the whole exponential curve
    # force eta=1.  Values are calculated over a finite test grid, not assumed.
    if etas is None:
        etas = np.linspace(-1.0, 3.0, 401)
    y = np.geomspace(1e-6, 30.0, 400)
    target = 1.0 - np.exp(-y)
    rows = []
    for eta in np.asarray(etas, dtype=float):
        mu = 1.0 - eta * np.exp(-y)
        err = mu - target
        rows.append({
            "eta": float(eta),
            "max_abs_mu_error": float(np.max(np.abs(err))),
            "mu_at_zero_limit": float(1.0 - eta),
            "high_y_limit": 1.0,
            "passes_exact_grid": bool(np.max(np.abs(err)) < 1e-12),
        })
    best = min(rows, key=lambda row: row["max_abs_mu_error"])
    return {
        "grid": {"y_min": float(y.min()), "y_max": float(y.max()), "points": len(y)},
        "best": best,
        "rows": rows,
        "analytic_identification": "mu_eta(y)-mu_target(y)=(1-eta)exp(-y), so eta=1 is uniquely selected",
        "status": "OPEN",
        "non_claims": ["this coefficient scan does not establish covariant khronon health or PPN"],
    }


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path,
                        default=Path(__file__).resolve().parent / "run_001" / "parameter_scan.json")
    args = parser.parse_args(argv)
    result = scan()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"best": result["best"], "status": result["status"]}, indent=2))


if __name__ == "__main__":
    main()
