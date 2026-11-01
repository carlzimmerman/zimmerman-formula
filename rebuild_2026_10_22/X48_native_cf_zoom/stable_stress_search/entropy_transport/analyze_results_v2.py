"""Separate accepted-step energy diagnostics from dense-output sample errors.

The immutable v1 analyzer and result remain historical evidence. This wrapper
retains their window/plot definitions and adds the independent sample audit.
Neither metric is a rigorous error bound at all intervening times.
"""
import argparse
import json
from pathlib import Path

import analyze_results as original


def sampled_energy_error(runs):
    reference = runs[0]['initial']['total']
    errors = []
    for run in runs:
        for row in run['time_history']:
            if row.get('sample_status') == 'invalid_dense_interpolation':
                continue
            errors.append(abs(row['total'] - reference)/abs(reference))
    if not errors:
        raise ValueError('no valid energy samples')
    return max(errors)


def analyze():
    report = original.analyze()
    report['schema'] = 'X48-entropy-transport-analysis-v2'
    for row in report['resolution']:
        n = row['N']
        names = [f'conv_n{n}_t8'] if n < 128 else []
        names.append(f'floor_n{n}_t32')
        runs = [original.load(name) for name in names]
        row['original_accepted_state_energy_error_bound'] = row.pop('original_energy_error_bound')
        row['original_maximum_sampled_energy_error'] = sampled_energy_error(runs)
    for row in report['stability']:
        runs = [original.load(name) for name in row['lineage']]
        row['accepted_state_energy_error_bound_from_prepared_state'] = row.pop(
            'energy_error_bound_from_prepared_state')
        row['maximum_sampled_energy_error_from_prepared_state'] = sampled_energy_error(runs)
    tight = [original.load(name) for name in ('tight_n256_t32','tight_n256_finish')]
    report['tighter_time_check_energy'] = dict(
        original_accepted_state_energy_error_bound=original.energy_bound(tight),
        original_maximum_sampled_energy_error=sampled_energy_error(tight))
    checks = report['finite_checks']
    checks['original_accepted_state_energy_bounds_below_1e_6'] = checks.pop(
        'original_energy_bounds_below_1e_6')
    checks['original_sampled_energy_errors_below_1e_6'] = all(
        row['original_maximum_sampled_energy_error'] < 1e-6 for row in report['resolution'])
    checks['stability_accepted_and_sampled_energy_errors_below_1e_6'] = all(
        row['accepted_state_energy_error_bound_from_prepared_state'] < 1e-6 and
        row['maximum_sampled_energy_error_from_prepared_state'] < 1e-6
        for row in report['stability'])
    report['energy_scope'] = (
        'Ancestry-aware accepted-state bounds sum recorded segment diagnostics. '
        'Sample maxima separately inspect all valid recorded diagnostic times, '
        'including dense interpolation. Neither certifies intervening times.')
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--figure',type=Path)
    args = parser.parse_args()
    report = analyze()
    args.output.write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
    if args.figure:
        original.figure(args.figure)
    print(json.dumps(report['finite_checks']))
    return 0 if all(report['finite_checks'].values()) else 1


if __name__ == '__main__':
    raise SystemExit(main())
