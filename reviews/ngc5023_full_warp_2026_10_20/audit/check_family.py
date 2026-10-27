#!/usr/bin/env python3
"""Independent reconstruction of saved finite-family calibration diagnostics.

No production-code imports, renderer calls, new shape fitting, or scan claims.
"""
import argparse
import collections
import hashlib
import itertools
import json
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
PACKET = HERE.parent


def bounded(A, y, lower, upper):
    best = None
    for state in itertools.product((-1, 0, 1), repeat=A.shape[1]):
        state = np.asarray(state)
        fixed = state != 0
        free = ~fixed
        x = np.zeros(len(state))
        x[state == -1] = lower[state == -1]
        x[state == 1] = upper[state == 1]
        rhs = y - A[:, fixed] @ x[fixed]
        if free.any():
            x[free] = np.linalg.lstsq(A[:, free], rhs, rcond=None)[0]
        if np.any(x < lower - 1e-9) or np.any(x > upper + 1e-9):
            continue
        objective = float(np.sum((A @ x - y) ** 2))
        if best is None or objective < best[0]:
            best = objective, x.copy()
    assert best is not None
    return best


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    out = Path(args.output)
    out.mkdir(exist_ok=True)
    obs = np.load(PACKET / 'nominal_run001/arrays.npz')
    data = obs['data_binned'].astype(float)
    blanks = obs['blanks_binned'].astype(float)
    U, Z, X = np.meshgrid(obs['U'], obs['Z'], obs['X'], indexing='ij')
    safe = np.ones(X.shape, bool)
    for x, z, u, width in ((-72, 80, -24.8, 56), (112, 92, 39.2, 40), (120, -76, 39.2, 52)):
        for sign in (-1, 1):
            safe &= ~((abs(X - sign * x) <= 70) & (abs(Z - sign * z) <= 70) &
                      (abs(U - sign * u) <= width / 2 + 6.18 + 8.24))
    masks = {
        'train': (abs(Z) <= 10) & (abs(X) <= 230) & (abs(U) <= 105) & safe,
        'validation': (abs(Z) >= 50) & (abs(X) <= 230) & (abs(U) <= 105) & safe,
        'guarded_validation': (abs(Z) >= 70) & (abs(X) <= 230) & (abs(U) <= 105) & safe,
    }
    train = masks['train']
    scatter = blanks.std(0, ddof=1)
    floor = np.median(scatter[train]) * .5
    scale = np.maximum(scatter[train], floor)
    expected = np.array([4.8e8, 4.9e7, 4.3e7]) / (2.356e5 * 6.6 ** 2)
    fraction = np.array([.26 / 4.8, .7 / 4.9, .3 / 4.3])
    checks = []
    maxima = collections.defaultdict(float)
    rows = []
    scenarios = []

    def check(name, error, tolerance):
        checks.append({'name': name, 'error': float(error), 'tolerance': tolerance,
                       'passed': bool(error <= tolerance)})

    sources = [('family_run001', 'uncertainty_scenarios.json'),
               ('trace_run001', 'trace_scenarios.json'), ('controls_run001', None)]
    controls = {}
    for run, scenario_file in sources:
        records = json.loads((PACKET / run / 'results.json').read_text())['cases']
        arrays = np.load(PACKET / run / 'arrays.npz')
        if scenario_file:
            source = json.loads((PACKET / scenario_file).read_text())['cases']
            check(run + ' scenario identifiers and order',
                  int([c['id'] for c in source] != [r['id'] for r in records]), 0)
            scenarios.extend(source)
        for i, record in enumerate(records):
            model = arrays['components'][i].astype(float)
            saved = record['bounded_fit']
            intrinsic = np.array([c['intrinsic_integrated_flux_Jy_km_s']
                                  for c in record['render_metadata']['components']])
            assert np.all(intrinsic > 1e-10), 'This finite audit expects all three components alive.'
            lower = np.maximum(.001, expected * (1 - fraction) / intrinsic)
            upper = expected * (1 + fraction) / intrinsic
            A = model[:, train].T / scale[:, None]
            y = data[train] / scale
            _, coefficient = bounded(A, y, lower, upper)
            prediction = np.einsum('i,ijkl->jkl', coefficient, model)
            residual = data - prediction
            sv = np.linalg.svd(A, compute_uv=False)
            errors = {
                'coefficient': np.max(abs(coefficient - saved['coefficients'])),
                'source_bounds': np.max(abs(np.array([lower, upper]) - saved['coefficient_bounds'])),
                'prediction': np.max(abs(prediction - arrays['predictions'][i])),
                'raw_peak_fixed': np.max(abs(model.sum(0) - arrays['peak_fixed_unfitted'][i])),
                'sv_relative': np.max(abs(sv - saved['weighted_design_singular_values']) / sv),
                'condition_relative': abs(sv[0] / sv[-1] - saved['weighted_design_condition_number']) / (sv[0] / sv[-1]),
            }
            bound_hits = np.where((abs(coefficient-lower) < 1e-5) | (abs(coefficient-upper) < 1e-5))[0].tolist()
            errors['bound_hits'] = int(bound_hits != saved['bound_hits'])
            errors['success'] = int(not saved['success'])
            metric_errors = []
            actual_metrics = {}
            for name, mask in masks.items():
                rms = float(np.sqrt(np.mean((residual[mask] / np.maximum(scatter[mask], floor)) ** 2)))
                actual_metrics[name] = rms
                metric_errors.append(abs(rms - saved['metrics'][name]['RMS_in_empirical_blank_scatter']))
                metric_errors.append(abs(float(residual[mask].sum()) - saved['metrics'][name]['signed_flux_residual_Jy_km_s']))
                metric_errors.append(abs(float(np.sqrt(np.mean(residual[mask]**2))) - saved['metrics'][name]['RMS_flux_Jy_km_s']))
                metric_errors.append(abs(float(np.sqrt(np.mean((data[mask]-model.sum(0)[mask])**2))) - record['peak_fixed_unfitted_RMS_Jy_km_s'][name]))
            errors['metric_absolute'] = max(metric_errors)
            _, broad = bounded(A, y, np.zeros(3), np.full(3, 3.))
            errors['broad_0_to_3_coefficient'] = np.max(abs(broad - record['broad_0_to_3_amplitude_diagnostic']['coefficients']))
            for name, value in errors.items():
                maxima[name] = max(maxima[name], float(value))
            row = {'id': record['id'], 'run': run, 'coefficients': coefficient.tolist(),
                   'lower': lower.tolist(), 'upper': upper.tolist(), 'bound_hits': bound_hits,
                   'upper_hits': np.where(abs(coefficient-upper) < 1e-5)[0].tolist(),
                   'condition': float(sv[0]/sv[-1]), 'singular_values': sv.tolist(),
                   'metrics': actual_metrics}
            rows.append(row)
            if run == 'controls_run001':
                controls[record['id']] = prediction
                native = arrays[record['id']+'_native_components'].astype(float)
                rebinned = native.reshape(3,20,3,12,5,30,5).sum((2,4,6))*16*4.12
                maxima['native_to_saved_binned'] = max(maxima['native_to_saved_binned'], float(abs(rebinned-model).max()))

    tolerances = {'coefficient': 1e-6, 'source_bounds': 1e-12, 'prediction': 1e-7,
                  'raw_peak_fixed': 1e-7, 'sv_relative': 1e-6,
                  'condition_relative': 1e-6, 'bound_hits': 0, 'success': 0,
                  'metric_absolute': 1e-5, 'broad_0_to_3_coefficient': 1e-6,
                  'native_to_saved_binned': 1e-7}
    for name, tolerance in tolerances.items():
        check('all saved cases: ' + name, maxima[name], tolerance)
    check('labeled non-control scenario count', abs(len(scenarios)-118), 0)
    distinct = collections.defaultdict(list)
    for case in scenarios:
        encoded = json.dumps(case['parameters'], sort_keys=True, separators=(',', ':')).encode()
        distinct[hashlib.sha256(encoded).hexdigest()].append(case['id'])
    check('distinct parameter set count', abs(len(distinct)-117), 0)
    family_rows = [r for r in rows if r['run'] != 'controls_run001']
    nominal = next(r for r in family_rows if r['id'] == 'nominal')
    gates = {str(g): [r['id'] for r in family_rows if r['metrics']['train'] <= g*nominal['metrics']['train']]
             for g in (1.10,1.25,1.50)}
    numerics = {}
    for name, pred in controls.items():
        if name == 'nominal_v2':
            continue
        difference = pred-controls['nominal_v2']
        numerics[name] = {region: float(np.sqrt(np.mean((difference[mask]/np.maximum(scatter[mask],floor))**2)))
                          for region,mask in masks.items()}
    result = {
        'all_passed': all(c['passed'] for c in checks), 'checks': checks,
        'production_code_imported': False, 'new_renderer_run': False,
        'scope': 'Independent saved-array reconstruction of 122 calibrations (118 labeled scenarios, four controls); no 206-parameter inference, scan significance, or uniform numerical bound.',
        'mask_counts': {k:int(v.sum()) for k,v in masks.items()},
        'scenario_count': len(scenarios), 'distinct_parameter_set_count': len(distinct),
        'duplicate_parameter_sets': [v for v in distinct.values() if len(v)>1],
        'all_scenarios_hit_some_bound': all(r['bound_hits'] for r in family_rows),
        'both_arms_upper_bound_count': sum(1 in r['upper_hits'] and 2 in r['upper_hits'] for r in family_rows),
        'condition_min_max': [min(r['condition'] for r in family_rows), max(r['condition'] for r in family_rows)],
        'relative_training_gate_members': gates,
        'numerical_prediction_difference_RMS_in_blank_scatter': numerics,
        'cases': rows,
    }
    (out/'checks.json').write_text(json.dumps(result, indent=2, allow_nan=False)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('cases','relative_training_gate_members')},indent=2))
    return 0 if result['all_passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
