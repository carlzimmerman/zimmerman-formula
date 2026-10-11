"""Conditional spherical projection bounds; no observational verdict."""
import hashlib
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
SOURCE = ROOT / 'campaign_fresh_gravity/CFG625_merger_baryon_inputs/cfg625_static_results.json'


def fraction(R, r):
    if r <= R:
        return 1.0
    x = (R / r) ** 2
    return x / (1 + math.sqrt(1 - x))


def largest_radius(R, needed, available):
    if available < 0:
        return None
    if needed <= 0:
        return 'unbounded'
    if needed > available or available == 0:
        return None
    q = needed / available
    return R / math.sqrt(q * (2 - q))


def main():
    checks = []

    def check(name, ok, diagnostic=None):
        checks.append(dict(name=name, passed=bool(ok), diagnostic=diagnostic))

    check('inside_endpoint', fraction(1, .5) == fraction(1, 1) == 1)
    check('far_limit', abs(fraction(1, 1e6) * 2e12 - 1) < 1e-11)
    n = 200000
    for r in (1, 1.01, 2, 4, 10):
        # Uniform cos(theta) integrates solid angle; no use of analytic cap boundary.
        count = sum(r * r * (1 - (-1 + (i + .5) * 2 / n) ** 2) <= 1
                    for i in range(n))
        err = abs(count / n - fraction(1, r))
        check('angular_count_' + str(r), err <= 2e-5, err)
    for r0 in (1, 2, 4):
        for k in (1, 3, 10):
            radii = [r0 * (1 + i / 10) for i in range(k)]
            weights = [i + 1 for i in range(k)]
            actual = sum(w * fraction(1, r) for w, r in zip(weights, radii))
            bound = sum(weights) * fraction(1, r0)
            check('positive_mixture_%s_%s' % (r0, k), actual <= bound + 1e-14)
    for q in (.01, .1, .5, .99, 1):
        rr = largest_radius(1, q, 1)
        check('inverse_' + str(q), abs(fraction(1, rr) - q) < 1e-12)
    reference = 1 - math.sqrt(3) / 2
    check('benchmark_r2', abs(fraction(1, 2) - reference) < 1e-15)
    check('MUTATE_one_cap_rejected', abs(reference / 2 - reference) > .05)
    check('MUTATE_full_shell_rejected', abs(1 - reference) > .5)
    check('infeasible_supply', largest_radius(1, 2, 1) is None)
    check('negative_supply', largest_radius(1, .1, -.1) is None)

    raw = SOURCE.read_bytes()
    source = json.loads(raw)['masses_t0']
    rows = []
    for name, s in sorted(source.items()):
        host = name.rsplit('_', 1)[-1]
        for f in (1, .90, .86):
            total_budget = 5.364 * s['Mb'] / f
            available = total_budget - s['Mcold']
            wrong_available = total_budget - s['Mcold_proj250']
            check('MUTATE_aperture_subtraction_%s_%s' % (name, f),
                  wrong_available > available and
                  math.isclose(wrong_available - available,
                               s['Mcold'] - s['Mcold_proj250'], rel_tol=1e-12))
            for target_name, target in (('recorded_central', s['P16']),
                                       ('recorded_lower_2sigma', 2.3e14 if host == 'main' else 1.6e14)):
                needed = max(0.0, target - s['tot_proj250'])
                rows.append(dict(case=name, retained_baryon_fraction=f,
                                 target=target_name, target_mass=target,
                                 model_aperture_mass=s['tot_proj250'],
                                 deficit=needed, conditional_total_cold_budget=total_budget,
                                 already_committed_total_cold=s['Mcold'], available=available,
                                 budget_consistent=available >= 0,
                                 maximum_exterior_inner_radius_kpc=largest_radius(250, needed, available),
                                 exterior_capacity={str(r): max(available, 0) * fraction(250, r)
                                                    for r in (250, 500, 1000)}))
    output = dict(status='conditional_geometry_only',
                  source_sha256=hashlib.sha256(raw).hexdigest(),
                  angular_samples=n, checks=checks,
                  checks_passed=sum(c['passed'] for c in checks), checks_total=len(checks),
                  rows=rows)
    (HERE / 'run' / 'results.json').write_text(json.dumps(output, indent=2) + '\n')
    print('%s/%s checks; %s conditional rows' % (output['checks_passed'], len(checks), len(rows)))
    for row in rows:
        if row['case'].startswith('B3_') and row['retained_baryon_fraction'] == .86:
            print(row['case'], row['target'], 'remaining=', row['available'],
                  'deficit=', row['deficit'], 'rmax=', row['maximum_exterior_inner_radius_kpc'])
    assert all(c['passed'] for c in checks)


if __name__ == '__main__':
    main()
