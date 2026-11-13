#!/usr/bin/env python3
"""Original failing witnesses plus an analytic collision benchmark."""
import argparse
import json
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
import cold_shells as C


def main(output):
    checks = {}
    a = np.array([C.AI, .2, .5, 1.])
    required = -.5 * (C.OC + C.OB) / a**3 + C.OL
    old_force = -.5 * C.OC / a**3
    checks['old_force_fails_background_at_every_probe'] = bool(np.all(np.abs(old_force - required) > .1))
    corrected = old_force - .5 * C.OB / a**3 + C.OL
    checks['corrected_force_matches_friedmann'] = bool(np.allclose(corrected, required, atol=5e-14, rtol=5e-15))
    for n in (130, 260):
        f = np.geomspace(1, 2000, n + 1)
        r = .75 * (f[1:]**4 - f[:-1]**4) / (f[1:]**3 - f[:-1]**3)
        old_inner_v = C.HI * r[0]
        true_inner_v = C.HI * f[0]
        checks[f'old_inner_face_fails_homology_N{n}'] = bool(abs(old_inner_v / true_inner_v - 1) > .01)
        old_interior = np.cumsum(np.diff(f**3)) - .5 * np.diff(f**3)
        checks[f'old_mass_missing_inner_ball_N{n}'] = bool(old_interior[0] / r[0]**3 < .1)
        checks[f'half_cell_fails_even_with_inner_ball_N{n}'] = bool(np.max(np.abs((old_interior + f[0]**3) / r**3 - 1)) > 2e-4)
        exact_at_r = f[0]**3 + np.concatenate(([0.], np.cumsum(np.diff(f**3))[:-1])) + r**3 - f[:-1]**3
        checks[f'exact_enclosed_volume_N{n}'] = bool(np.allclose(exact_at_r, r**3, atol=1e-12, rtol=1e-14))
    # Orthogonal analytic event: radial free fall from rest, F=0.  This exercises
    # the candidate regularized RHS itself, with no finite-shell singularity.
    saved_background = C.background
    C.background = lambda t: 0.
    def hit(tau, y):
        return y[0]
    hit.terminal = True
    hit.direction = -1
    try:
        sol = solve_ivp(lambda t, y: C.regularized_rhs(t, y, np.array([]), False),
                        (0, 10), [1., 0., -C.A, 0.], method='DOP853',
                        rtol=2e-13, atol=1e-15, events=hit, max_step=.02)
    finally:
        C.background = saved_background
    exact_time = np.pi / (2 * np.sqrt(2 * C.A))
    error = float(abs(sol.y[3, -1] / exact_time - 1))
    checks['regularized_central_focus_matches_exact_kepler_freefall'] = bool(sol.success and len(sol.t_events[0]) and error < 2e-11)
    lane = Path(__file__).parent
    hom = json.loads((lane/'homogeneous/results.json').read_text())
    lo = json.loads((lane/'central_130_strict/results.json').read_text())
    hi = json.loads((lane/'central_260_strict/results.json').read_text())
    checks['homogeneous_outward_despite_inward_acceleration'] = bool(hom['checks']['all_shell_velocities_outward'] and hom['checks']['initial_acceleration_is_inward'])
    checks['strict_focus_times_agree_within_1e_minus_10_Gyr'] = abs(lo['elapsed_Gyr'] - hi['elapsed_Gyr']) < 1e-10
    checks['finite_shell_turnaround_precedes_focusing'] = hi['first_turnarounds'][1]['elapsed_Gyr'] < hi['elapsed_Gyr']
    checks['sampled_finite_cell_density_stays_above_216'] = hi['checks']['sampled_min_finite_cell_density_over_present_cold'] > 216
    checks['no_finite_shell_crossing_precedes_center_focus'] = hi['event'] == 'central_limit_focusing' and hi['checks']['sampled_min_normalized_finite_spacing'] > 0
    data = np.load(lane/'central_260_strict/trajectory.npz')
    center_q_min = float(np.min(C.AI**-3 / data['center_s']**6))
    result = {'checks': checks, 'all_pass': all(checks.values()), 'count': len(checks),
              'analytic_kepler_time_Gyr': exact_time, 'computed_kepler_time_Gyr': float(sol.y[3, -1]),
              'kepler_relative_error': error,
              'strict_focus_time_difference_Gyr': abs(lo['elapsed_Gyr'] - hi['elapsed_Gyr']),
              'minimum_sampled_center_density_over_present_cold': center_q_min,
              'scope': 'Finite regression witnesses and numerical benchmarks; model equivalence not established'}
    Path(output).write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))
    assert result['all_pass']


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--output', required=True)
    main(p.parse_args().output)
