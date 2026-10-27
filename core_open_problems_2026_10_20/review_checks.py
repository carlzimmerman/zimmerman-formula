#!/usr/bin/env python3
"""Independent coordinator checks of shared conventions; Python stdlib only.

Run: python3 core_open_problems_2026_10_20/review_checks.py
These finite checks supplement the algebra in REVIEW.md. They do not validate
a microscopic origin, relativistic completion, or observational likelihood.
"""
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path
import hashlib
import json
import math
import argparse


def main():
    root = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=root / 'review_results.json')
    args = parser.parse_args()
    exact_count = 0
    # Parametrize by polarization rather than solving the same root as a lane.
    # p = u/a0, y = gbar/a0, x = g/a0.
    for n in (1, 2):
        for j in range(1, 100):
            p = Fraction(j, 100 * n)
            y = p * p / (1 - n * p)
            x = y + p
            assert (x * x == y * (x + 1)) if n == 1 else (x * x == y * y + y)
            exact_count += 1

    max_residual = Decimal(0)
    sampled_ratio_max = Decimal(0)
    with localcontext() as ctx:
        ctx.prec = 70
        ys = [Decimal(10) ** (Decimal(i) / 10) for i in range(-200, 201)]
        ys += [Decimal('0.5')]
        for y in ys:
            xs = []
            for n in (1, 2):
                nn = Decimal(n)
                # Stable root of the capacity equation, then total acceleration.
                u = 2 * y / ((nn * nn * y * y + 4 * y).sqrt() + nn * y)
                x = y + u
                control = ((y + (y * y + 4 * y).sqrt()) / 2 if n == 1
                           else (y * y + y).sqrt())
                residual = abs(x / control - 1)
                max_residual = max(max_residual, residual)
                assert residual < Decimal('1e-48')
                assert 0 < u < 1 / nn
                xs.append(x)
            ratio = xs[0] / xs[1]
            assert ratio > 1
            assert ratio <= (Decimal(4) / 3).sqrt() + Decimal('1e-60')
            sampled_ratio_max = max(sampled_ratio_max, ratio)

        # At y=1/2, g1/a0=1 and g2/a0=sqrt(3)/2 exactly.
        acceleration_ratio = 2 / Decimal(3).sqrt()
        speed_ratio = acceleration_ratio.sqrt()
        assert abs(sampled_ratio_max - acceleration_ratio) < Decimal('1e-60')

    manifest = json.loads((root / 'BASELINE_INPUTS.json').read_text())
    snapshots_ok = []
    for item in manifest['inputs']:
        snapshot = root / item['snapshot_path']
        assert hashlib.sha256(snapshot.read_bytes()).hexdigest() == item['sha256']
        snapshots_ok.append(item['snapshot_path'])

    z = math.sqrt(32 * math.pi / 3)
    result = {
        'scope': 'shared action algebra, finite precision cross-check, input integrity',
        'exact_rational_examples': exact_count,
        'decimal_y_domain': ['1e-20', '1e20'],
        'decimal_y_samples': len(ys),
        'max_relative_law_residual': str(max_residual),
        'max_acceleration_ratio': str(acceleration_ratio),
        'max_circular_speed_ratio': str(speed_ratio),
        'ratio_maximizer_gbar_over_a0': '1/2',
        'horizon_conventions': {
            'Z': z,
            'a0_over_cH_Lambda_given_kappa_half': 1 / z,
            'half_a0_over_cH_Lambda': 1 / (2 * z),
            'note': 'half_a0 is not the physical de Sitter horizon surface gravity'
        },
        'baseline_snapshots_verified': snapshots_ok,
        'nonclaims': ['microscopic derivation', 'full relativistic stability',
                      'new empirical constraint', 'kappa or Lstar selection'],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
