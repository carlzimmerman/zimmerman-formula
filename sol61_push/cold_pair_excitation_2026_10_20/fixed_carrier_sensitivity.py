"""Existing pair snapshots in one frozen shared-carrier phase frame.

No field, eigenvalue, stationary, or outgoing solve. A conditional modal
coordinate and a finite complex fit are not accepted energy/eigenfrequency.
"""
from pathlib import Path
import json
import math
import resource
import sys
import time

import numpy as np
from numpy.polynomial.legendre import leggauss
from pair_projection import (analyze_snapshot, load_reference, read_snapshot,
                             _sample_spheres)

out = Path(sys.argv[1])
here = Path(__file__).resolve().parent
prior = json.loads((here/'analysis_run_001/results.json').read_text())
checks, rows, comparisons = [], [], []
started = time.monotonic()
CASES = ['pair_inphase', 'pair_dt_half', 'pair_dx_fine']
TIMES = list(range(120, 241, 20))


def ck(name, condition, value=None):
    row = {'name': name, 'pass': bool(condition)}
    if value is not None:
        row['value'] = float(value)
    checks.append(row)


def old_row(case, Q, ti):
    return next(x for x in prior['conditional_projections']
                if x['case'] == case and x['Q_reference'] == Q
                and x['frame'] == 'reference_omega' and x['time'] == ti)


def fit_coordinate(data):
    """Exactly the declared old finite basis/search, with condition number."""
    tt = np.array([x['time'] for x in data])
    cc = np.array([complex(x['coordinate_real'], x['coordinate_imag']) for x in data])
    best, curve = None, []
    for freq in np.linspace(.04, .075, 701):
        basis = np.array([np.ones_like(tt), np.exp(1j*freq*tt),
                          np.exp(2j*freq*tt)]).T
        coef = np.linalg.lstsq(basis, cc, rcond=None)[0]
        res = np.linalg.norm(basis@coef-cc)/max(np.linalg.norm(cc), 1e-300)
        curve.append([float(freq), float(res)])
        if best is None or res < best['relative_complex_residual']:
            best = {'Omega_fit': float(freq),
                    'relative_complex_residual': float(res),
                    'constant_complex': [float(coef[0].real), float(coef[0].imag)],
                    'fundamental_complex': [float(coef[1].real), float(coef[1].imag)],
                    'fundamental_abs_squared': float(abs(coef[1])**2),
                    'second_harmonic_abs_squared': float(abs(coef[2])**2),
                    'basis_condition_number': float(np.linalg.cond(basis))}
    best.update(window=[120, 240], n_samples=len(data),
                exploratory_scope='Finite coordinate fit only; no nonlinear eigenfrequency or mode-energy acceptance.',
                search_curve=curve)
    return best


def channel_kinematics(omega, Omega, scope):
    """Reference or explicitly hypothetical sideband kinematics, never a rate."""
    nu = omega+2*Omega
    open_channel = nu > 1
    return {'scope': scope, 'omega': omega, 'Omega': Omega, 'nu': nu,
            'Omega_positive_Psi_cutoff': (1-omega)/2,
            'Omega_minus_cutoff': Omega-(1-omega)/2,
            'positive_Psi_channel_open_if_frequency_physical': open_channel,
            'group_speed_over_c_if_open': math.sqrt(1-1/nu**2) if open_channel else None,
            'charge_per_K_if_open': 1/(2*Omega) if open_channel else None,
            'free_Psi_kinetic_per_K_if_open': (nu-1)/(2*Omega) if open_channel else None,
            'charge_unbinding_per_K_if_open': (1-omega)/(2*Omega) if open_channel else None,
            'no_loss_rate_or_galactic_wind_coupling_inferred': True}


def core_field_mismatches(snapshot, ref, phases):
    """Positive field-only L2 mismatch in declared spherical core apertures."""
    snap = read_snapshot(snapshot)
    r = ref['r'][ref['r'] < 15.]
    mu, weights = leggauss(48)
    sampled = _sample_spheres(snap, r, mu, 0., 3)
    f, b, h = ref['background'](r)
    psi_lab = sampled[0]+1j*sampled[1]
    x_lab = sampled[2]+1j*sampled[3]
    result = {}
    for label, phase in phases.items():
        psi = psi_lab*np.exp(-1j*phase)
        xx = x_lab*np.exp(-2j*phase)
        can = np.array([math.sqrt(2)*(psi.real-f[:, None]),
                        math.sqrt(2)*(xx.real-b[:, None]),
                        sampled[4]-h[:, None],
                        math.sqrt(2)*psi.imag, math.sqrt(2)*xx.imag])
        rec = []
        for radius in [12., 15.]:
            keep = r < radius
            numerator = 2*math.pi*ref['dr']*np.sum(
                r[keep, None]**2*weights[None, :]*np.sum(can[:, keep, :]**2, axis=0))
            denominator = 4*math.pi*ref['dr']*np.sum(
                r[keep]**2*(2*f[keep]**2+2*b[keep]**2+h[keep]**2))
            rec.append({'radius': radius, 'field_mismatch_numerator': float(numerator),
                        'reference_field_norm_squared': float(denominator),
                        'relative_field_L2_mismatch': float(math.sqrt(numerator/denominator)),
                        'scope': 'Field norm only, not an energy or bound-charge diagnostic.'})
        result[label] = rec
    return result


for case in CASES:
    for Q in [136000, 140000]:
        mode = here/f'matched_refs_run_004/Q{Q}_L60_N1199.npz'
        profile = here/f'matched_refs_run_004/profile_Q{Q}_L60_N1199.npz'
        ref = load_reference(mode, profile, Q)
        omega = ref['omega']
        theta_anchor = old_row(case, Q, 120)['carrier_phase_used']
        group = []
        for ti in TIMES:
            old = old_row(case, Q, ti)
            theta = theta_anchor+omega*(ti-120)
            snap = here/(case+'_run_001')/'evolution'/f'snap_t{ti*1000:09d}.bin'
            fixed = analyze_snapshot(snap, mode, profile, Qref=Q,
                                     carrier_frequency=omega, carrier_phase=theta)
            fixed.update(case=case, frame='fixed_phase_reference_omega',
                         carrier_anchor_time=120, carrier_anchor_phase=theta_anchor)
            ck(f'{case}Q{Q}t{ti} finite fixed-frame coordinate',
               np.isfinite(fixed['conditional_K_coordinate']))
            ck(f'{case}Q{Q}t{ti} declared fixed carrier frequency',
               fixed['carrier_frequency_used'] == omega)
            if ti == 120:
                z = complex(fixed['coordinate_real'], fixed['coordinate_imag'])
                expected = complex(old['coordinate_real'], old['coordinate_imag'])
                error = abs(z-expected)/max(abs(expected), 1e-300)
                ck(f'{case}Q{Q} anchor matches old coordinate', error < 1e-10, error)
            cores = core_field_mismatches(snap, ref,
                      {'fixed_phase': theta, 'snapshot_fitted_phase': old['carrier_phase_used']})
            ck(f'{case}Q{Q}t{ti} finite core field norms',
               all(np.isfinite(x['relative_field_L2_mismatch']) for v in cores.values() for x in v))
            wrapped = float(np.angle(np.exp(1j*(old['carrier_phase_used']-theta))))
            row = {'case': case, 'Q_reference': Q, 'time': ti,
                   'fixed_frame_analysis': fixed,
                   'snapshot_fitted_phase_coordinate': {
                       k: old[k] for k in ['coordinate_real', 'coordinate_imag',
                                          'conditional_K_coordinate', 'carrier_phase_used',
                                          'ell2_reconstruction_state_residual_fraction',
                                          'full_canonical_field_mismatch_relative_L2']},
                   'snapshot_phase_minus_fixed_wrapped': wrapped,
                   'core_field_mismatches': cores}
            rows.append(row)
            group.append(row)
        fixed_fit = fit_coordinate([x['fixed_frame_analysis'] for x in group])
        snapshot_fit = fit_coordinate([old_row(case, Q, ti) for ti in TIMES])
        prior_fit = next(x for x in prior['exploratory_fits']
                         if x['case'] == case and x['Q_reference'] == Q)
        ck(f'{case}Q{Q} cached old fit reproduced',
           abs(snapshot_fit['Omega_fit']-prior_fit['Omega_fit']) < 1e-14
           and abs(snapshot_fit['relative_complex_residual']-prior_fit['relative_complex_residual']) < 1e-12)
        phase_unwrapped = np.unwrap([x['snapshot_phase_minus_fixed_wrapped'] for x in group])
        ck(f'{case}Q{Q} fixed phase sequence derivative equals omega',
           np.max(abs(np.diff([x['fixed_frame_analysis']['carrier_phase_used'] for x in group])/20-omega)) < 1e-13)
        reference_channel = channel_kinematics(omega, ref['Omega'],
                              'Kinematics of the accepted finite-reference linear mode second harmonic, not a measured collision flux.')
        ck(f'{case}Q{Q} reference sideband kinetic/unbinding partition',
           abs(reference_channel['free_Psi_kinetic_per_K_if_open']
               + reference_channel['charge_unbinding_per_K_if_open']-1) < 1e-13)
        comparisons.append({'case': case, 'Q_reference': Q,
                            'Omega_reference': ref['Omega'], 'omega_reference': omega,
                            'fixed_frame_fit': fixed_fit,
                            'snapshot_phase_fit': snapshot_fit,
                            'reference_positive_Psi_channel': reference_channel,
                            'hypothetical_coordinate_fit_thresholds': {
                                'fixed_phase_fit': channel_kinematics(omega, fixed_fit['Omega_fit'],
                                    'Hypothetical threshold proximity only: this fitted coordinate rate is not an accepted physical eigenfrequency.'),
                                'snapshot_phase_fit': channel_kinematics(omega, snapshot_fit['Omega_fit'],
                                    'Hypothetical threshold proximity only: this fitted coordinate rate is not an accepted physical eigenfrequency.')},
                            'unwrapped_snapshot_minus_fixed_phase': [float(x) for x in phase_unwrapped],
                            'max_relative_K_phase_frame_change': float(max(
                                abs(x['fixed_frame_analysis']['conditional_K_coordinate']
                                    /x['snapshot_fitted_phase_coordinate']['conditional_K_coordinate']-1)
                                for x in group)),
                            'mode_energy_accepted': False,
                            'nonlinear_eigenfrequency_accepted': False})
        print(json.dumps({'case': case, 'Q': Q,
                          'fixed_fit': fixed_fit['Omega_fit'],
                          'snapshot_fit': snapshot_fit['Omega_fit'],
                          'fixed_residual': fixed_fit['relative_complex_residual'],
                          'phase_drift_final': float(phase_unwrapped[-1])}), flush=True)

rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
ck('measured RSS below1GB', rss < 1_000_000_000, rss)
size = sum(x.stat().st_size for x in out.iterdir() if x.is_file())
ck('retained result output below1GB', size < 1_000_000_000, size)
result = {'scope': 'Consistent carrier-phase sensitivity of existing finite collision coordinates; core field norms only. No eigenfrequency/mode-energy acceptance.',
          'rows': rows, 'comparisons': comparisons, 'checks': checks,
          'n_checks': len(checks), 'all_checks_pass': all(x['pass'] for x in checks),
          'peak_RSS_bytes_macos': rss, 'runtime_seconds': time.monotonic()-started,
          'non_claims': ['No field/eigen/BVP/outgoing solve',
                        'Finite complex-coordinate fits are not nonlinear eigenfrequencies',
                        'Core field norm is not excitation energy or bound charge',
                        'No measured damping, branching efficiency or four-dwarf closure']}
(out/'results.json').write_text(json.dumps(result, indent=2)+'\n')
raise SystemExit(0 if result['all_checks_pass'] else 1)
