#!/usr/bin/env python3
"""Bounded alternate-branch continuation of the frozen action.

High-k mode values come from the actual six-state transfer operator at two
wavenumbers. Positive values do not establish a positive reduced kinetic
action, full stability, radiation-era viability, or a complete theory.
"""
import argparse
import json
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
from background_evolve import Model, system_functions
from radiation_probe import ProbeBackground
from transfer_evolve import Background, mode_system


class BranchBackground(Background):
    def __init__(self, direction):
        self.model = ProbeBackground(5.).model if direction < 0 else Model(2., gamma=1e-6)
        self.names, self.fun = system_functions()
        self.tau_min = self.model.tau_min if direction < 0 else 0.
        self.tau_max = 0. if direction < 0 else 2.

    def evaluate(self, state, extended=False):
        if not self.tau_min <= state[3] <= self.tau_max:
            raise ValueError('outside integrated coefficient history; no extrapolation')
        return super().evaluate(state, extended)


def high_k_modes(v):
    """Frozen local operator eigenvalues, not an action-Hessian health test."""
    results = []
    for k in (3000., 30000.):
        operator, matrix, *_ = mode_system(v, k)
        frequency = k/v['a']
        # Similarity scaling improves numerical balance without changing modes.
        scales = np.array([1., frequency, 1., frequency, 1., max(v['rho'], 1.)*frequency])
        balanced = operator*scales[None, :]/scales[:, None]/frequency
        eigenvalues = np.linalg.eigvals(balanced)
        values = -eigenvalues**2
        radiation = sorted(range(6), key=lambda i: abs(values[i]-1/3))[:2]
        remaining = [i for i in range(6) if i not in radiation]
        dust = sorted(remaining, key=lambda i: abs(values[i]))[:2]
        clock = [i for i in remaining if i not in dust]
        results.append(dict(k=k, clock_cs2=float(np.mean(values[clock]).real),
                            radiation_cs2=float(np.mean(values[radiation]).real),
                            dust_cs2=[float(values[i].real) for i in dust],
                            scaled_eigenvalue_real=eigenvalues.real.tolist(),
                            scaled_eigenvalue_imag=eigenvalues.imag.tolist(),
                            transfer_matrix_condition=float(np.linalg.cond(matrix))))
    return results


def continue_branch(initialH, q, direction, *, efolds=None, step=.025, rtol=2e-11):
    if direction not in (-1, 1):
        raise ValueError('direction must be -1 or +1')
    bound = 2.3 if direction < 0 else .2
    efolds = bound if efolds is None else float(efolds)
    if not (0 < efolds <= bound and 0 < step <= .05 and 0 < rtol < 1e-5):
        raise ValueError('requested continuation exceeds declared bounds')
    bg = BranchBackground(direction)
    def physical(loga, y):
        H, fieldq, tau, time = y
        return [np.exp(loga), H, fieldq, tau, .001*np.exp(-3*loga), .01*np.exp(-4*loga)]
    def rhs(loga, y):
        v = bg.evaluate(physical(loga, y))[0]
        if v['H'] <= 0:
            raise ValueError('expanding background branch lost')
        return np.array([v['Hd'], v['qd'], v['sbar'], 1.])/v['H']
    def sample(loga, y):
        v, matrix, residuals, margin = bg.evaluate(physical(loga, y), extended=True)
        a, H, fieldq, tau, rho, rad = physical(loga, y)
        coeff = bg.model.background(float(tau))
        rho_clock = 2*fieldq**2*v['PX']-v['P']+v['V']-6*v['gamma']*H*fieldq**3
        modes = high_k_modes(v)
        uncertainty = max(1e-10, 10*abs(modes[0]['clock_cs2']-modes[1]['clock_cs2']))
        return dict(loga=float(loga), a=float(a), H=float(H), q=float(fieldq), tau=float(tau),
                    physical_time=float(y[3]), coefficient_a=float(coeff['a']),
                    coefficient_q=float(coeff['q']), clock_rate=float(v['sbar']),
                    radiation_fraction=float(rad/(3*H*H)), rho_clock=float(rho_clock),
                    relative_logarithm_margin=float(margin/coeff['U']),
                    background_condition=float(np.linalg.cond(matrix)),
                    background_determinant=float(np.linalg.det(matrix)),
                    scaled_friedmann_residual=float(abs(residuals[0])/(1+3*H*H+.7+abs(rho_clock)+rho+rad)),
                    scaled_clock_residual=float(abs(residuals[1])/(1+abs(v['Pt'])+abs(v['Vt'])+3*abs(H*v['W']))),
                    scalar_charge=float(a**3*residuals[2]), high_k=modes,
                    clock_cs2=modes[1]['clock_cs2'], sign_resolution_scale=uncertainty)
    def gate(point):
        if max(point['scaled_friedmann_residual'], point['scaled_clock_residual']) > 1e-8:
            return 'constraint_residual_stop'
        if point['background_condition'] > 1e12 or point['relative_logarithm_margin'] < 1e-7:
            return 'conditioning_or_domain_stop'
        if any(abs(x['radiation_cs2']-1/3) > 1e-4 for x in point['high_k']):
            return 'high_k_mode_assignment_unresolved'
        if point['clock_cs2'] < -point['sign_resolution_scale']:
            return 'high_k_negative_clock'
        if point['clock_cs2'] <= point['sign_resolution_scale']:
            return 'high_k_clock_sign_unresolved'
        return None
    loga, y = 0., np.array([initialH, q, 0., 0.], dtype=float)
    samples, reason, attempted = [], '', None
    outcome = 'requested_loga_bound'
    try:
        samples.append(sample(loga, y))
        outcome = gate(samples[-1]) or outcome
        while outcome == 'requested_loga_bound' and abs(loga) < efolds-1e-13:
            next_loga = direction*min(efolds, abs(loga)+step)
            attempted = [float(loga), float(next_loga)]
            sol = solve_ivp(rhs, (loga, next_loga), y, method='DOP853',
                            rtol=rtol, atol=rtol*.01, max_step=step/4)
            if not sol.success:
                raise RuntimeError(sol.message)
            point = sample(next_loga, sol.y[:, -1])
            samples.append(point)
            loga, y = next_loga, sol.y[:, -1]
            outcome = gate(point) or 'requested_loga_bound'
            if abs(point['scalar_charge']/samples[0]['scalar_charge']-1) > 1e-8:
                outcome = 'scalar_charge_drift_stop'
            if outcome == 'requested_loga_bound' and direction < 0 and point['radiation_fraction'] >= .5:
                outcome = 'radiation_fraction_reached'
    except (ValueError, RuntimeError, FloatingPointError, np.linalg.LinAlgError) as error:
        outcome, reason = 'branch_or_numerical_stop', str(error)
    return dict(outcome=outcome, stop_reason=reason, direction=direction,
                requested_loga=direction*efolds, last_attempted_loga_interval=attempted,
                initial=dict(H=initialH, q=q, a=1., tau=0., rho_b=.001, rho_r=.01,
                             Lambda=.7, gamma=1e-6),
                coefficient_tau_interval=[bg.tau_min, bg.tau_max],
                tolerances=dict(rtol=rtol, atol=rtol*.01, step=step), samples=samples,
                max_scaled_constraint=max((max(x['scaled_friedmann_residual'], x['scaled_clock_residual']) for x in samples), default=None),
                max_scalar_charge_drift=max((abs(x['scalar_charge']/samples[0]['scalar_charge']-1) for x in samples), default=None),
                health_gate_note='Clock sign uses two finite large-k frozen-operator evaluations; sign_resolution_scale is a diagnostic tolerance, not a rigorous asymptotic error bound.',
                full_health_established=False,
                scope='Fixed-action bounded homogeneous continuation with local high-k sign screening. No reduced kinetic-action positivity, complete stability, CMB viability, or global no-go claim.',
                full_theory_status='OPEN')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--step', type=float, default=.025)
    parser.add_argument('--result-file', type=Path)
    args = parser.parse_args()
    branches = ((.6967532055475008, .9477017173736229),
                (.6967560366493584, -.9477017537279459))
    results = [continue_branch(H, q, direction, step=args.step)
               for H, q in branches for direction in (-1, 1)]
    if args.result_file:
        args.result_file.write_text(json.dumps(results, indent=2)+'\n')
    print(json.dumps([dict(initial=x['initial'], direction=x['direction'], outcome=x['outcome'],
                           stop_reason=x['stop_reason'], samples=len(x['samples']),
                           max_scaled_constraint=x['max_scaled_constraint'],
                           last=x['samples'][-1] if x['samples'] else None)
                      for x in results], indent=2))
