"""DM1 exact rational moment witnesses plus labeled synthetic Q/R conversion."""
import argparse
import json
import math
from fractions import Fraction as F
from pathlib import Path


def witness(mu, nu, target):
    variance = nu - mu * mu
    eps = min(F(1, 1000), variance / (10 * (variance + (target - mu) ** 2)), mu / (10 * target))
    mean = (mu - eps * target) / (1 - eps)
    var = (variance - eps * (variance + (target - mu) ** 2)) / (1 - eps) ** 2
    assert eps > 0 and var > 0 and mean > 0 and mean * mean > var
    mass = (1 - eps) * mean + eps * target
    emission = (1 - eps) * (mean * mean + var) + eps * target * target
    assert mass == mu and emission == nu
    return {
        'target': str(target), 'epsilon': str(eps),
        'bulk_mean': str(mean), 'bulk_variance': str(var),
        'bulk_densities_display': [float(mean) - math.sqrt(float(var)), float(mean) + math.sqrt(float(var))],
        'mass_exact': str(mass), 'emission_exact': str(emission),
        'epsilon_ceiling': str(variance / (variance + (target - mu) ** 2)),
    }


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--out', required=True); args = ap.parse_args()
    mu, nu = F(3, 2), F(5, 2)
    exact = [witness(mu, nu, x) for x in [F(1, 10), F(1, 2), F(1), F(3, 2), F(3), F(10), F(100)]]
    # Deliberately exceed the exact finite-volume ceiling.
    target = F(10); v = nu - mu * mu; ceiling = v / (v + (target - mu) ** 2)
    eps_bad = (1 + ceiling) / 2
    var_bad = (v - eps_bad * (v + (target - mu) ** 2)) / (1 - eps_bad) ** 2
    assert var_bad < 0
    zero_var_bad = -F(1, 1000) * (target - mu) ** 2 / (1 - F(1, 1000)) ** 2
    assert zero_var_bad < 0
    eps = F(1, 1000)
    frozen_bulk_mass = (1 - eps) * mu + eps * target
    assert frozen_bulk_mass != mu
    # A small finite-width witness at a fixed force-derived density, not a data fit.
    rho_ref, pressure_gradient, B = 1e-25, 1e-35, 1e-12
    E3 = math.sqrt(.315 * 4 ** 3 + .685)
    examples = []
    for a0 in [9.3619e-11, 1.1279e-10]:
        for history, ratio in [('vacuum', 1.0), ('frozen_H_z3', E3)]:
            a = a0 * ratio
            for kernel in ['Q', 'R']:
                force = math.sqrt(B * B + a * B) if kernel == 'Q' else B / (-math.expm1(-math.sqrt(B / a)))
                L = pressure_gradient / (rho_ref * force)
                # Treat the represented binary64 target as a rational number for
                # the exact toy moment identity; it is not an exact force value.
                w = witness(mu, nu, F.from_float(L))
                restored = pressure_gradient / (rho_ref * L)
                assert abs(restored / force - 1) < 5e-15
                examples.append({'a0_si': a0, 'history': history, 'kernel': kernel,
                                 'a_si': a, 'B_si': B, 'force_si': force, 'L': L,
                                 'epsilon': w['epsilon'], 'force_recovery_rel': abs(restored / force - 1),
                                 'mass_exact': w['mass_exact'], 'emission_exact': w['emission_exact']})
    result = {'claim_id': 'DM1', 'exact_witnesses': exact, 'synthetic_gravity_examples': examples,
              'controls': {'above_volume_ceiling_variance': str(var_bad),
                           'zero_global_variance_nonuniform_shell_variance': str(zero_var_bad),
                           'frozen_bulk_mass_mismatch': str(frozen_bulk_mass - mu)},
              'all_checks_passed': True,
              'non_claims': ['No cluster fit, variable emissivity response, global hydrostatic solution, smoothness proof, or theory closure.']}
    out = Path(args.out); out.mkdir(parents=True, exist_ok=True)
    (out / 'results.json').write_text(json.dumps(result, indent=2) + '\n')
    print('Seven exact rational witnesses and eight synthetic Q/R gravity conversions passed, including three negative controls.')


if __name__ == '__main__':
    main()
