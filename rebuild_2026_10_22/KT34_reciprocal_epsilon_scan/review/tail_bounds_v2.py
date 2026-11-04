#!/usr/bin/env python3
"""Arithmetic application of REVIEW.md's independently audited continuum bound.

This does not run a Gaussian solver or certify the archived Newtonian speeds.
The analytic lemma is separate from this finite check of all 2,750 cells.
"""
import argparse
from fractions import Fraction as F
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / 'rebuild_2026_10_22/KT33_reciprocal_filter/mw/grid_refined_run/results.json'
A0 = {'canonical': 9.3603e-11, 'alt': 1.1312e-10}
G = 4.30091e-6
M_GAS = 11910967635.394314
R0 = 8.122
VC_MIN = 219.9
EPS_TAIL = 2.5
G_SI = 6.67430e-11
M_SUN = 1.98847e30
KPC_SOLVER = 3.0856775814913673e19
G_K_SOLVER = G_SI*M_SUN/(KPC_SOLVER*1e6)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    source = json.loads(SOURCE.read_text())
    # pi > 25/8 implies c=sqrt(2/pi)<4/5. The familiar weaker pi>3.14
    # already suffices. All remaining safe-constant slack is exact rational.
    c_upper, root33_upper, cube_upper = F(4, 5), F(23, 4), F(13, 20)
    K_upper = F(2, 3) * c_upper * root33_upper * cube_upper
    checks = {
        'pi_lower_3_14_exceeds_25_8': F(314, 100) > F(25, 8),
        'root33_upper': root33_upper**2 > 33,
        'cube_root_upper': cube_upper**3 > c_upper/3,
        'safe_K_below_two': K_upper < 2,
    }
    out = {
        'assertion_tested': 'The safe continuum bound with K=2 excludes L1 for every archived baryon cell at every epsilon>=2.5, conditional on the archived Newtonian speeds and source masses; explicit baseline slack is also checked.',
        'analytic_bound_reference': '../REVIEW.md, New continuum Milky Way tail bound',
        'bound': 'v_c(R0)^2 <= v_N(R0)^2 + 2*sqrt(Gk_solver*M*a0k_solver)*R0^2*exp(.005)/(epsilon^2*RM_width^2)',
        'normalization_correction_to_v1': math.sqrt(G_SI*M_SUN/(G*3.0857e19*1e6)),
        'physical_constants': {'G_SI':G_SI,'M_SUN':M_SUN,'KPC_SOLVER':KPC_SOLVER,'G_K_SOLVER':G_K_SOLVER},
        'supersedes': 'tail_001/results.json: omitted small solver-G versus width-G correction; first result is not the accepted physical bound',
        'K_safe': 2,
        'K_rational_upper': str(K_upper),
        'K_sharp_angular_decimal': (2*math.sqrt(33)/3)*math.sqrt(2/math.pi)*(math.sqrt(2/math.pi)/3)**(1/3),
        'epsilon_tail_lower': EPS_TAIL,
        'local_velocity_lower_cut_km_s': VC_MIN,
        'baseline_slack': {'add_to_newton_velocity_km_s': 1., 'physical_mass_multiplier': 1.01, 'width_mass_unchanged': True},
        'footings': {},
        'checks': checks,
    }
    for foot, a0 in A0.items():
        archived = source['footings'][foot]['rows']
        a0k = a0*3.0857e19/1e6
        rows = []
        for index, row in enumerate(archived):
            mass = row['Mstar'] + M_GAS
            rm = math.sqrt(G*mass/a0k)
            vn = row['newton']['vc']
            a0k_solver = a0*KPC_SOLVER/1e6
            boost = 2*math.sqrt(G_K_SOLVER*mass*a0k_solver)*R0**2*math.exp(.005)/(rm**2)
            upper = math.sqrt(vn**2 + boost/EPS_TAIL**2)
            slack_upper = math.sqrt((vn+1)**2 + math.sqrt(1.01)*boost/EPS_TAIL**2)
            rows.append({'index': index, 'cell': row['cell'], 'nominal_mass_Msun': mass,
                         'RM_width_kpc': rm, 'newton_vc_km_s': vn,
                         'upper_vc_at_epsilon_2_5': upper,
                         'upper_vc_with_baseline_slack': slack_upper,
                         'threshold_without_slack': math.sqrt(boost/(VC_MIN**2-vn**2)),
                         'discrete_source_mass_relative_to_nominal': row['mass']['full_source']/mass-1})
        checks[foot+'|population_count'] = len(rows) == 1375
        checks[foot+'|newton_below_L1'] = all(r['newton_vc_km_s'] < VC_MIN for r in rows)
        checks[foot+'|uniform_tail_excluded'] = all(r['upper_vc_at_epsilon_2_5'] < VC_MIN for r in rows)
        checks[foot+'|tail_excluded_with_baseline_slack'] = all(r['upper_vc_with_baseline_slack'] < VC_MIN for r in rows)
        out['footings'][foot] = {'n_cells': len(rows),
            'max_newton_vc_km_s': max(r['newton_vc_km_s'] for r in rows),
            'max_upper_vc_at_epsilon_2_5': max(r['upper_vc_at_epsilon_2_5'] for r in rows),
            'max_upper_vc_with_baseline_slack': max(r['upper_vc_with_baseline_slack'] for r in rows),
            'max_threshold_without_slack': max(r['threshold_without_slack'] for r in rows),
            'worst_cell_index': max(rows, key=lambda r:r['upper_vc_at_epsilon_2_5'])['index'],
            'rows': rows}
    out['all_checks_pass'] = all(checks.values())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(out, indent=2, allow_nan=False)+'\n')
    print(json.dumps({foot:{k:v for k,v in value.items() if k != 'rows'} for foot,value in out['footings'].items()}, indent=2))
    print('all_checks_pass', out['all_checks_pass'])
    if not out['all_checks_pass']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
