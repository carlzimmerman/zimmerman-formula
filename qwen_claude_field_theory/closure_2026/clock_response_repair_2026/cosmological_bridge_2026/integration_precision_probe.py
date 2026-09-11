#!/usr/bin/env python3
"""Step refinement of all three stored float64 histories, with mp diagnostics.

A non-monotone residual is recorded, not hidden or relabeled as convergence.
This does not modify any coefficient function or fit an expansion history.
"""
import argparse
import json
from pathlib import Path
import mpmath as mp
import numpy as np
from scipy.integrate import solve_ivp
from transfer_evolve import Background, mode_system
from transfer_precision import PrecisionEvaluator


def trajectory(max_step):
    bg = Background(.02)
    model = bg.model
    model.solution = solve_ivp(lambda t, y: model.flowfunc(*y), [0, .2], [1, .1, .5],
                              method='DOP853', rtol=2e-13, atol=2e-15,
                              dense_output=True, max_step=max_step)
    model.background.cache_clear()
    initial = bg.solution.y[:, 0].copy()
    bg.solution = solve_ivp(bg.rhs, [0, .02], initial, method='DOP853',
                            rtol=2e-12, atol=2e-14, dense_output=True, max_step=max_step)
    bg.at.cache_clear()
    k = .3
    sol = solve_ivp(lambda t, u: (mode_system(bg.at(float(t))[0], k)[0]
                                  @ u.reshape(6, 6)).ravel(), [0, .02], np.eye(6).ravel(),
                   method='DOP853', rtol=2e-10, atol=2e-12,
                   dense_output=True, max_step=max_step)
    for solution in (model.solution, bg.solution, sol):
        if not solution.success:
            raise RuntimeError(solution.message)
    return bg, sol


def run(steps=(.01, .005, .0025)):
    rows = []
    previous = None
    for step in steps:
        bg, sol = trajectory(step)
        with mp.workdps(40):
            diagnostic = PrecisionEvaluator(bg, sol, .3).diagnose(.000125, .02)
        endpoint = sol.y[:, -1]
        rows.append(dict(max_integration_step=step, diagnostic=diagnostic,
            max_background_constraint=max(float(max(abs(bg.at(float(t))[2][:2])))
                                          for t in np.linspace(0, .02, 17)),
            nfev=[bg.model.solution.nfev, bg.solution.nfev, sol.nfev],
            max_endpoint_transfer_change=0. if previous is None else float(max(abs(endpoint-previous))),
            endpoint_comparison='first row has no previous endpoint' if previous is None else 'previous row',
            transfer_end=endpoint.reshape(6, 6).tolist()))
        previous = endpoint
    residuals = [row['diagnostic']['max_scaled_euler'] for row in rows]
    return dict(rows=rows, sampled_residuals_monotonically_decrease=all(
                    b < a for a, b in zip(residuals, residuals[1:])),
                diagnostic_digits=40, diagnostic_step=.000125, k=.3,
                scope='Three short same-action integration step caps; not a convergence theorem',
                full_theory_status='OPEN')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--result-file', type=Path, required=True)
    args = parser.parse_args()
    result = run()
    args.result_file.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))
