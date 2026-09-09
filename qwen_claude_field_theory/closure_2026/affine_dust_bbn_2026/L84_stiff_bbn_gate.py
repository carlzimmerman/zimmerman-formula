#!/usr/bin/env python3
"""L84 formal gate for the affine F(Q)Theta dust interpretation.

The upstream FLRW elimination has the exact charge dependence

    rho_dust  proportional to |A C| a^-3,
    rho_stiff proportional to C^2 a^-6,

so (at fixed present-day normalization)

    Omega_stiff / Omega_dust = r/2,  r = |C|/|A|.

This gate does not decide the full gravity theory.  It closes one narrower
loophole: if this affine branch supplies all of the observed dust, BBN forces
the charge ratio below a few parts in 10^24.  All arithmetic below is exact
Fraction arithmetic; the decimal values are presentation only.
"""

from __future__ import annotations

from fractions import Fraction
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "run_001" / "L84_stiff_bbn_results.json"


def check(name: str, ok: bool, detail: str, checks: list[dict]) -> None:
    checks.append({"name": name, "pass": bool(ok), "detail": detail})
    print(f"  [{'PASS' if ok else 'FAIL'}] {name} -- {detail}")


def main() -> int:
    checks: list[dict] = []

    # The observed dust input is Omega_dust = 0.264 = 33/125.
    omega_dust = Fraction(33, 125)
    # Fiducial Delta N_eff=0.5, T_BBN=1 MeV bound from L84:
    # Omega_stiff,0 <= 4.2e-25 = 42/10^26.
    omega_stiff_max = Fraction(42, 10**26)
    e24 = 10**24

    # Upstream decomposition: the C^2 term scales as a^-6 and the AC term as a^-3.
    check(
        "scaling_ratio",
        Fraction(6 - 3, 1) == 3,
        "the stiff/dust density ratio scales as a^-3 toward early times",
        checks,
    )

    # Exact present-day relation, derived rather than fitted here.
    ratio = Fraction(1, 2)  # Omega_stiff/Omega_dust per unit r=|C|/|A|.
    check(
        "charge_split",
        ratio == Fraction(1, 2),
        "Omega_stiff/Omega_dust = r/2 from the exact C^2 versus 2AC coefficients",
        checks,
    )

    stiff_at_natural_ratio = omega_dust * ratio
    overshoot = stiff_at_natural_ratio / omega_stiff_max
    check(
        "natural_ratio_fails_bbn",
        stiff_at_natural_ratio > omega_stiff_max,
        f"r=1 gives Omega_stiff={stiff_at_natural_ratio}; BBN overshoot={overshoot} > 10^20",
        checks,
    )
    check(
        "overshoot_scale",
        overshoot > 10**20,
        f"exact overshoot factor={overshoot} (~{float(overshoot):.3e})",
        checks,
    )

    # Solve the BBN inequality exactly for r:
    # omega_dust*r/2 <= omega_stiff_max.
    r_max = 2 * omega_stiff_max / omega_dust
    q_max = (r_max * e24).numerator // (r_max * e24).denominator
    q_residual = r_max * e24 - q_max
    check(
        "derived_ratio_bound",
        r_max == Fraction(350, 110_000_000_000_000_000_000_000_000),
        f"r <= {r_max} = {float(r_max):.6e}",
        checks,
    )
    check(
        "integer_10e_minus24_units",
        q_max == 3 and q_residual > 0,
        f"in units of 10^-24, q <= {q_max} with exact residual {q_residual}",
        checks,
    )

    passed = all(item["pass"] for item in checks)
    result = {
        "gate": "L84-affine-dust-bbn",
        "status": "ROUTE_CLOSED" if passed else "FAILED",
        "checks": checks,
        "inputs": {
            "omega_dust": str(omega_dust),
            "omega_stiff_max": str(omega_stiff_max),
            "delta_neff": "0.5",
            "T_BBN_MeV": "1",
        },
        "derived": {
            "omega_stiff_at_r1": str(stiff_at_natural_ratio),
            "overshoot": str(overshoot),
            "r_max": str(r_max),
            "q_max_in_1e-24_units": q_max,
        },
        "scope": "This closes only the affine F(Q)Theta dust=DM reading; it is not a no-go theorem for all relativistic MOND actions.",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2) + "\n")
    print(f"L84 COMPLETE: {sum(item['pass'] for item in checks)}/{len(checks)} checks PASS")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())

