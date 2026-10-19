"""Independent FSP-U2 check in inverse gauge squares and squared Yukawas.

Does not import or execute inverse_bvp.py. Solves the gauge ODEs as states,
rather than evaluating that implementation's analytic gauge helper.
"""
import argparse
import json
import math
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import root

p = argparse.ArgumentParser()
p.add_argument('--output', required=True)
args = p.parse_args()
base = Path('fine_structure_puzzle/uv_selection')
d = json.loads((base / 'inverse_inputs.json').read_text())
reference = json.loads((base / 'inverse-002/result.json').read_text())
L = 16 * math.pi ** 2
bY = 41 / 6
b = np.array([-19 / 6, -7.])
target2 = np.array([d['y_t_mt'] ** 2, d['y_b_mt'] ** 2])
k_mt = np.array([d['alpha_2_inverse_mz'], d['alpha_3_inverse_mz']]) / (4 * math.pi)
k_mt -= 2 * b / L * math.log(d['mt_GeV'] / d['mz_GeV'])


def trajectory(logparameters, crossover, span=4000., tolerance=2e-11):
    fg, vstar = np.exp(logparameters)
    hstar = L * fg / bY
    ustar = vstar + hstar / 3
    fy = (6 * vstar + hstar / 12) / L
    T = math.log(crossover / d['mt_GeV'])
    k_T = k_mt - 2 * b * T / L
    k_UV = b / (L * fg) + (k_T - b / (L * fg)) * math.exp(2 * fg * span)

    # State: k2=1/g2^2, k3=1/g3^2, u=yt^2, v=yb^2,
    # integrated log(u/v) derivative. The ratio equation cancels fy and
    # the common non-Abelian gauge contributions exactly.
    def rhs(gravity):
        def evaluate(t, state):
            k = state[:2]
            u, v = state[2:4]
            h = hstar if gravity else state[5]
            common = 9 / (4 * k[0]) + 8 / k[1]
            duk = 2 * fg * k - 2 * b / L if gravity else -2 * b / L
            du = 2 * u * ((4.5 * u + 1.5 * v - 17 * h / 12 - common) / L - (fy if gravity else 0))
            dv = 2 * v * ((4.5 * v + 1.5 * u - 5 * h / 12 - common) / L - (fy if gravity else 0))
            ratio = (6 * (u - v) - 2 * h) / L
            values = [*duk, du, dv, ratio]
            if not gravity:
                values.append(2 * bY * h * h / L)
            return values
        return evaluate

    uv = solve_ivp(rhs(True), (T + span, T), [*k_UV, ustar, vstar, 0.],
                   method='DOP853', rtol=tolerance,
                   atol=[1e-12, 1e-12, 1e-14, 1e-17, 1e-13], max_step=10.)
    assert uv.success, uv.message
    ir = solve_ivp(rhs(False), (T, 0), [*uv.y[:, -1], hstar],
                   method='DOP853', rtol=tolerance,
                   atol=[1e-12, 1e-12, 1e-14, 1e-17, 1e-13, 1e-14], max_step=.5)
    assert ir.success, ir.message
    final = ir.y[:, -1]
    assert min(final[:4]) > 0
    ratio_error = math.log(final[2] / final[3]) - math.log(ustar / vstar) - final[4]
    analytic_h_mt = 1 / (1 / hstar + 2 * bY * T / L)
    return {
        'fg': float(fg), 'fy': float(fy), 'yb_UV_squared': float(vstar),
        'yt_yb': np.sqrt(final[2:4]).tolist(), 'gY_mt': math.sqrt(final[5]),
        'log_ratio_integral_error': ratio_error,
        'k_T_max_relative_error': float(np.max(abs(uv.y[:2, -1] / k_T - 1))),
        'k_mt_max_relative_error': float(np.max(abs(final[:2] / k_mt - 1))),
        'gY_squared_analytic_relative_error': float(final[5] / analytic_h_mt - 1),
        'UV_nfev': uv.nfev, 'IR_nfev': ir.nfev,
    }


def residual(parameters):
    pred = trajectory(parameters, d['planck_GeV'])
    return np.log(np.array(pred['yt_yb']) / np.sqrt(target2))


# One local solve, no parameter search or scan. Guess specifies no gY or alpha.
fit = root(residual, np.log([.0062, 5.3e-6]), method='hybr', options={'xtol': 1e-9})
assert fit.success, fit.message
central = trajectory(fit.x, d['planck_GeV'])
assert max(abs(residual(fit.x))) < 1e-7
central['residual_log'] = residual(fit.x).tolist()
central['root_evaluations'] = int(fit.nfev)
central['gY_difference_from_reference'] = central['gY_mt'] - reference['central']['gY_mt']
short = trajectory(fit.x, d['planck_GeV'], span=2000., tolerance=2e-12)
central['shorter_cutoff_tighter_tolerance_max_y_relative_change'] = float(np.max(abs(np.array(short['yt_yb']) / central['yt_yb'] - 1)))

# The second crossover is a forward check of its recorded calibrated parameters,
# not a second independent inverse fit.
rr = reference['crossover_sensitivity_only']
sensitivity = trajectory(np.log([rr['fg'], rr['yb_UV_squared']]), d['other_crossover_GeV_for_sensitivity_only'])
sensitivity['gY_difference_from_reference'] = sensitivity['gY_mt'] - rr['gY_mt']
sensitivity['target_max_y_relative_error'] = float(np.max(abs(np.array(sensitivity['yt_yb']) / np.sqrt(target2) - 1)))

out = {
    'formulation': 'ODE states k2,k3,yt^2,yb^2, integrated log-ratio; gY^2 is an ODE state below the gravity step',
    'central_independent_local_fit': central,
    'second_crossover_forward_check_only': sensitivity,
    'nonclaims': ['No global uniqueness certificate', 'No physical input matching audit', 'No alpha derivation', 'No rigorous interval error bound'],
}
Path(args.output).parent.mkdir(parents=True, exist_ok=True)
Path(args.output).write_text(json.dumps(out, indent=2, sort_keys=True) + '\n')
print(json.dumps(out, indent=2, sort_keys=True))
