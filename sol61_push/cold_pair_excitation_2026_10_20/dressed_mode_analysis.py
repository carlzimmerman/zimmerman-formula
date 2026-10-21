"""Conditional analysis of four completed dressed Cauchy evolutions.

Prepared before field results. Execution requires explicit parent confirmation
and all four frozen run records. This script evolves and solves no fields.
"""
from pathlib import Path
import argparse
import json
import math
import resource
import time

import numpy as np
from pair_projection import analyze_snapshot, load_reference

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
KS = [0, 1, 50, 500]
TIMES = np.arange(0., 241., 10.)
ORDERS = np.array([0, 1, -1, 2, -2])
TRAIN = (TIMES >= 20) & (TIMES <= 180)
HOLDOUT = (TIMES >= 190) & (TIMES <= 240)


def read_jsonlines(path):
    return [json.loads(x) for x in path.read_text().splitlines()]


def complex_pair(value):
    return [float(value.real), float(value.imag)]


def coordinate(record):
    return complex(record['coordinate_real'], record['coordinate_imag'])


def model_at_frequency(freq):
    basis = np.exp(1j*float(freq)*TIMES[:, None]*ORDERS[None, :])
    train = basis[TRAIN]
    singular = np.linalg.svd(train, compute_uv=False)
    return {'frequency': float(freq), 'basis': basis,
            'train_pinv': np.linalg.pinv(train),
            'train_design_condition': float(singular[0]/singular[-1]),
            'train_design_singular_values': singular}


def evaluate_model(cc, model):
    coef = model['train_pinv']@cc[TRAIN]
    predicted = model['basis']@coef
    errors = predicted-cc
    ntrain = float(np.linalg.norm(cc[TRAIN]))
    ntest = float(np.linalg.norm(cc[HOLDOUT]))
    nonconstant = abs(coef[1:])**2
    dominant = int(ORDERS[1+int(np.argmax(nonconstant))]) if np.max(nonconstant) else None
    normal = np.linalg.norm(model['basis'][TRAIN].conj().T@errors[TRAIN])
    return {'frequency': model['frequency'],
            'coefficients_by_signed_harmonic': {str(k): complex_pair(v) for k, v in zip(ORDERS, coef)},
            'train_relative_complex_residual': float(np.linalg.norm(errors[TRAIN])/max(ntrain, 1e-300)),
            'holdout_relative_complex_residual': float(np.linalg.norm(errors[HOLDOUT])/max(ntest, 1e-300)),
            'train_absolute_complex_RMS_error': float(np.linalg.norm(errors[TRAIN])/math.sqrt(np.sum(TRAIN))),
            'holdout_absolute_complex_RMS_error': float(np.linalg.norm(errors[HOLDOUT])/math.sqrt(np.sum(HOLDOUT))),
            'train_coordinate_norm': ntrain, 'holdout_coordinate_norm': ntest,
            'train_normal_equation_relative_residual': float(normal/max(ntrain, 1e-300)),
            'train_design_condition': model['train_design_condition'],
            'train_design_singular_values': [float(x) for x in model['train_design_singular_values']],
            'constant_coordinate_power': float(abs(coef[0])**2),
            'positive_fundamental_coordinate_power': float(abs(coef[1])**2),
            'negative_fundamental_coordinate_power': float(abs(coef[2])**2),
            'positive_second_harmonic_coordinate_power': float(abs(coef[3])**2),
            'negative_second_harmonic_coordinate_power': float(abs(coef[4])**2),
            'dominant_nonconstant_signed_harmonic': dominant,
            'dominant_observed_coordinate_rate': abs(dominant)*model['frequency'] if dominant else None,
            'first_harmonic_coordinate_power_sum': float(abs(coef[1])**2+abs(coef[2])**2),
            'second_harmonic_coordinate_power_sum': float(abs(coef[3])**2+abs(coef[4])**2),
            'predicted_coordinates_all_times': [complex_pair(x) for x in predicted],
            'fit_scope': 'Finite coordinate model trained only on20..180; holdout190..240 never refitted. Powers are coefficient magnitudes, not accepted mode energies.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output')
    parser.add_argument('--root-confirmed-four-complete', action='store_true')
    args = parser.parse_args()
    if not args.root_confirmed_four_complete:
        raise RuntimeError('Preparation only: wait for explicit parent confirmation that all four dressed runs are complete.')
    out = Path(args.output)
    started = time.monotonic()
    checks, evolutions, projections, fits = [], [], [], []

    def ck(name, condition, value=None):
        rec = {'name': name, 'pass': bool(condition)}
        if value is not None:
            rec['value'] = float(value)
        checks.append(rec)

    mode = HERE/'matched_refs_run_004/Q136000_L60_N1199.npz'
    profile = HERE/'matched_refs_run_004/profile_Q136000_L60_N1199.npz'
    ref = load_reference(mode, profile, 136000)
    omega, Omega = ref['omega'], ref['Omega']
    records = {}
    for K in KS:
        run = HERE/f'dressed_K{K}_run_001'
        result = json.loads((run/'results.json').read_text())
        manifest = json.loads((run/'manifest.json').read_text())
        if manifest['run']['status'] != 'completed' or not result['all_checks_pass']:
            raise RuntimeError(f'dressed K{K} is not a completed passing recorded evolution')
        case = result['case']
        ck(f'K{K} recorded nominal label matches', case['nominal_K'] == K)
        ck(f'K{K} reference carrier matches initializer', abs(case['omega']-omega) < 1e-12)
        logs = read_jsonlines(run/'evolution/log.jsonl')
        energy = read_jsonlines(run/'evolution/enclosed_energy.jsonl')
        by_time = {float(x['t']): x for x in logs}
        en_time = {float(x['t']): x for x in energy}
        if set(by_time) != set(en_time):
            raise ValueError('charge/energy diagnostic times differ')
        seed_audit = ROOT/case['seed_audit']
        audit = json.loads(seed_audit.read_text())
        seed_row = next(x for x in audit['rows'] if x['nominal_K'] == K)
        initial = by_time[0.]
        ck(f'K{K} initial Q matches independent seed audit',
           abs(initial['Q']-seed_row['Q_actual'])/max(abs(initial['Q']), 1.) < 1e-10)
        ck(f'K{K} initial E matches independent seed audit',
           abs(initial['E']-seed_row['E_laplacian'])/max(abs(initial['E']), 1.) < 1e-10)
        records[K] = {'logs': logs, 'energy': energy, 'by_time': by_time,
                      'en_time': en_time, 'case': case, 'seed_audit': str(seed_audit),
                      'manifest': manifest}
        for ti in TIMES:
            path = run/'evolution'/f'snap_t{round(ti*1000):09d}.bin'
            for frame in ['fixed_phase', 'snapshot_fitted_phase']:
                result = analyze_snapshot(path, mode, profile, Qref=136000,
                                          carrier_frequency=omega,
                                          carrier_phase=omega*ti if frame == 'fixed_phase' else None)
                result.update(nominal_K=K, frame=frame)
                ck(f'K{K}t{int(ti)}{frame} finite coordinate', np.isfinite(result['conditional_K_coordinate']))
                ck(f'K{K}t{int(ti)}{frame} finite field/state norms',
                   np.isfinite(result['full_canonical_field_mismatch_relative_L2'])
                   and np.isfinite(result['ell2_reconstruction_state_residual']))
                if frame == 'fixed_phase':
                    ck(f'K{K}t{int(ti)} fixed carrier phase', result['carrier_phase_used'] == omega*ti)
                projections.append(result)

    # Compare actual global diagnostics before making any coordinate-energy claim.
    baseline = records[0]
    base_initial = baseline['by_time'][0.]
    for K in KS:
        record = records[K]
        initial = record['by_time'][0.]
        dE0 = initial['E']-base_initial['E']
        dQ0 = initial['Q']-base_initial['Q']
        actual_initial_excess = dE0-omega*dQ0
        trace = []
        max_e = max_q = max_grand = max_diff_grand = 0.
        for point in record['logs']:
            ti = float(point['t'])
            base = baseline['by_time'][ti]
            energy = record['en_time'][ti]
            Eerror = point['E']-initial['E']
            Qerror = point['Q']-initial['Q']
            grand_error = Eerror-omega*Qerror
            diff_grand = (point['E']-base['E'])-omega*(point['Q']-base['Q'])
            max_e = max(max_e, abs(Eerror))
            max_q = max(max_q, abs(Qerror))
            max_grand = max(max_grand, abs(grand_error))
            max_diff_grand = max(max_diff_grand, abs(diff_grand-actual_initial_excess))
            apertures = []
            for radius in [10, 15, 20]:
                charge = point[f'Q{radius}']
                apertures.append({'radius': radius, 'Q': charge,
                                  'Q_fraction_of_current_box': charge/point['Q'],
                                  'Q_relative_to_initial_aperture': charge/initial[f'Q{radius}'],
                                  'positive_face_energy': energy[f'E{radius}'],
                                  'E_aperture_over_Q_aperture': energy[f'E{radius}']/charge if charge else None,
                                  'scope': 'Fixed-origin inventory, not automatically bound mass or escaped flux.'})
            trace.append({'time': ti, 'E': point['E'], 'Q': point['Q'],
                          'grand_E_minus_omega_Q': point['E']-omega*point['Q'],
                          'global_E_error': Eerror, 'global_Q_error': Qerror,
                          'global_grand_error': grand_error,
                          'baseline_difference_grand': diff_grand,
                          'apertures': apertures})
        all_finite = all(np.isfinite(x['E']) and np.isfinite(x['Q'])
                         and np.isfinite(x['baseline_difference_grand']) for x in trace)
        ck(f'K{K} finite global/aperture inventory trace', all_finite)
        evolutions.append({'nominal_K': K, 'actual_initial_E': initial['E'],
                           'actual_initial_Q': initial['Q'],
                           'actual_initial_Q_minus_reference': initial['Q']-136000,
                           'initial_Delta_E_relative_K0': dE0,
                           'initial_Delta_Q_relative_K0': dQ0,
                           'initial_actual_Delta_E_minus_omega_Delta_Q': actual_initial_excess,
                           'max_absolute_global_E_error': max_e,
                           'max_absolute_global_Q_error': max_q,
                           'max_relative_global_E_error': max_e/max(abs(initial['E']), 1.),
                           'max_relative_global_Q_error': max_q/max(abs(initial['Q']), 1.),
                           'max_absolute_global_grand_error': max_grand,
                           'max_absolute_baseline_difference_grand_drift': max_diff_grand,
                           'global_grand_error_over_actual_initial_excess': max_grand/abs(actual_initial_excess) if actual_initial_excess else None,
                           'difference_grand_drift_over_actual_initial_excess': max_diff_grand/abs(actual_initial_excess) if actual_initial_excess else None,
                           'seed_audit': record['seed_audit'], 'trace': trace,
                           'scope': 'Actual fixed-omega endpoint grand difference; not E-E_stat(Qactual), not nominal K, not a physical mode-energy measurement.'})

    known = model_at_frequency(Omega)
    known_half = model_at_frequency(Omega/2)
    grid = [model_at_frequency(freq) for freq in np.linspace(.03, .09, 1201)]
    coordinate_series = []
    for frame in ['fixed_phase', 'snapshot_fitted_phase']:
        zero = np.array([coordinate(next(x for x in projections
                         if x['nominal_K'] == 0 and x['frame'] == frame and x['time'] == ti))
                         for ti in TIMES])
        for K in KS:
            raw = np.array([coordinate(next(x for x in projections
                           if x['nominal_K'] == K and x['frame'] == frame and x['time'] == ti))
                           for ti in TIMES])
            corrected = raw-zero
            coordinate_series.append({'nominal_K': K, 'frame': frame,
                                      'times': [float(x) for x in TIMES],
                                      'raw_coordinates': [complex_pair(x) for x in raw],
                                      'K0_coordinates': [complex_pair(x) for x in zero],
                                      'baseline_subtracted_coordinates': [complex_pair(x) for x in corrected],
                                      'raw_coordinate_squared': [float(abs(x)**2) for x in raw],
                                      'baseline_subtracted_coordinate_squared': [float(abs(x)**2) for x in corrected],
                                      'scope': 'Subtract complex coordinates before squaring. This is an artifact control, not an exact nonlinear energy decomposition.'})
            for name, cc in [('raw', raw), ('K0_coordinate_subtracted', corrected)]:
                if K == 0 and name == 'K0_coordinate_subtracted':
                    fits.append({'nominal_K': K, 'frame': frame, 'signal': name,
                                 'status': 'exactly_zero_control_no_frequency_assigned'})
                    ck(f'{frame} corrected K0 is identicallyzero', np.max(abs(cc)) == 0)
                    continue
                fixed_fit = evaluate_model(cc, known)
                known_alias_fit = evaluate_model(cc, known_half)
                # Frequency chosen on training residual only. Test scores are never used here.
                best = None
                curve = []
                for model in grid:
                    coef = model['train_pinv']@cc[TRAIN]
                    error = model['basis'][TRAIN]@coef-cc[TRAIN]
                    res = float(np.linalg.norm(error)/max(np.linalg.norm(cc[TRAIN]), 1e-300))
                    curve.append([model['frequency'], res])
                    if best is None or res < best[0]:
                        best = (res, model)
                scanned = evaluate_model(cc, best[1])
                ck(f'K{K}{frame}{name} finite train/holdout scores',
                   all(np.isfinite(x[k]) for x in [fixed_fit, scanned]
                       for k in ['train_relative_complex_residual', 'holdout_relative_complex_residual',
                                 'train_absolute_complex_RMS_error', 'holdout_absolute_complex_RMS_error']))
                ck(f'K{K}{frame}{name} least-squares normal equations',
                   max(x['train_normal_equation_relative_residual']
                       for x in [fixed_fit, known_alias_fit, scanned]) < 1e-10)
                values = np.array([x[1] for x in curve])
                minima = [j for j in range(len(grid))
                          if (j == 0 or values[j] <= values[j-1])
                          and (j == len(grid)-1 or values[j] <= values[j+1])]
                minima = sorted(minima, key=lambda j: values[j])[:8]
                alternatives = [evaluate_model(cc, grid[j]) for j in minima]
                fits.append({'nominal_K': K, 'frame': frame, 'signal': name,
                             'known_linear_Omega': Omega, 'known_frequency_fit': fixed_fit,
                             'known_linear_mode_as_second_harmonic_alias_fit': known_alias_fit,
                             'train_selected_frequency_fit': scanned,
                             'up_to8_local_training_minima': alternatives,
                             'train_frequency_scan': curve,
                             'mode_energy_accepted': False,
                             'nonlinear_eigenfrequency_accepted': False,
                             'charge_caveat': 'Actual seed Q varies with amplitude; a fitted shift is not a pure fixed-Q amplitude shift.'})
            if frame == 'fixed_phase':
                evolution = next(x for x in evolutions if x['nominal_K'] == K)
                print(json.dumps({'nominal_K': K,
                                  'actual_initial_Q': evolution['actual_initial_Q'],
                                  'actual_initial_DeltaGrand': evolution['initial_actual_Delta_E_minus_omega_Delta_Q'],
                                  'corrected_coordinate_squared_initial': float(abs(corrected[0])**2),
                                  'corrected_coordinate_squared_final': float(abs(corrected[-1])**2)}), flush=True)
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    ck('measured RSS below1GB', rss < 1_000_000_000, rss)
    retained = sum(x.stat().st_size for x in out.iterdir() if x.is_file())
    ck('retained outputs below1GB', retained < 1_000_000_000, retained)
    result = {'scope': 'Conditional finite dressed-Cauchy coordinate identification and conservative inventories; no fixed-Q nonlinear-mode/damping claim.',
              'Q_reference': 136000, 'omega_reference': omega, 'linear_Omega_reference': Omega,
              'frame_definition': 'Primary theta=omega_reference*t, frequency=omega_reference, common charge-one/two U1; optional instantaneous fitted phase retains reference frequency.',
              'fit_design': {'basis_orders': [int(x) for x in ORDERS],
                             'train_times': [float(x) for x in TIMES[TRAIN]],
                             'holdout_times': [float(x) for x in TIMES[HOLDOUT]],
                             'frequency_range': [.03, .09], 'frequency_step': .00005,
                             'alias_control': 'Known Omega/2 model includes known Omega as second harmonic. Report dominant signed harmonic and up to8 local training minima; base rate alone is not a mode frequency.',
                             'selection': 'Training residual only; holdout predicted without refit.'},
              'evolutions': evolutions, 'conditional_projections': projections,
              'coordinate_series': coordinate_series, 'fits': fits,
              'checks': checks, 'n_checks': len(checks),
              'all_checks_pass': all(x['pass'] for x in checks),
              'peak_RSS_bytes_macos': rss, 'runtime_seconds': time.monotonic()-started,
              'non_claims': ['Nominal K and baseline-subtracted coordinate powers are not accepted nonlinear mode energies',
                            'Actual Q varies; no pure fixed-Q amplitude-frequency relation is inferred',
                            'Quasistatic chi dressing is initial preparation, not radiation',
                            'A short harmonic train/holdout fit is not an eigenfrequency or damping measurement',
                            'No outgoing solve, physical units, population kernel, orbitalJ or four-dwarf closure']}
    (out/'results.json').write_text(json.dumps(result, indent=2)+'\n')
    raise SystemExit(0 if result['all_checks_pass'] else 1)


if __name__ == '__main__':
    main()
