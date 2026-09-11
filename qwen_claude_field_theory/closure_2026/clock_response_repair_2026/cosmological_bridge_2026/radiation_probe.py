#!/usr/bin/env python3
"""Bounded backward radiation probe; no recombination calibration or refitting.

The original coefficient ODE is integrated in log(coefficient scale factor),
then its strictly bounded dense output is inverted to evaluate at tau. The
sourced equations use log(physical scale factor). Matter densities use their
exact conserved charges; these charge relations are imposed, not diagnostics.
"""
import argparse
from functools import lru_cache
import json
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq, root
from background_evolve import Model, system_functions
from constitutive import functions
from transfer_evolve import Background


class BackwardHistory(Model):
    """Same coefficient initial-value problem, extended only by integration."""
    def __init__(self, efolds=5.):
        if not 0 < efolds <= 6:
            raise ValueError('coefficient probe requires 0 < efolds <= 6')
        self.gamma = 1e-6
        self.bgfunc, self.flowfunc, self.names, self.jetfunc = functions()
        def rhs(loga, state):
            m, v, tau = state
            a = np.exp(loga)
            if m <= 0:
                raise ValueError('coefficient m domain lost')
            flow = np.asarray(self.flowfunc(a, m, v), dtype=float)
            H = flow[0]/a
            return [flow[1]/H, flow[2]/H, 1/H]
        self.history = solve_ivp(rhs, (0., -efolds), [.1, .5, 0.],
                                 method='DOP853', rtol=2e-13, atol=2e-15,
                                 dense_output=True, max_step=.05)
        if not self.history.success:
            raise RuntimeError(self.history.message)
        self.loga_min = float(self.history.t[-1])
        self.tau_min = float(self.history.y[2, -1])

    @lru_cache(maxsize=128)
    def background(self, tau):
        if not np.isfinite(tau) or not self.tau_min <= tau <= 0:
            raise ValueError('outside the integrated backward coefficient interval')
        loga = 0. if tau == 0 else brentq(
            lambda x: self.history.sol(x)[2]-tau, self.loga_min, 0.,
            xtol=2e-13, rtol=2e-14)
        m, v, _ = self.history.sol(loga)
        a = np.exp(loga)
        raw = np.asarray(self.bgfunc(a, m, v), dtype=float)
        return dict(a=a, m=m, v=v, q=raw[0], U=raw[1], d=raw[2], H=raw[3],
                    ell=raw[4], qdot=raw[5], Hdot=raw[8], raw=raw)


class ProbeBackground(Background):
    def __init__(self, coefficient_efolds):
        self.model = BackwardHistory(coefficient_efolds)
        self.names, self.fun = system_functions()


def probe(efolds=3., coefficient_efolds=5., step=.025, rtol=2e-11):
    if not (0 < efolds <= 4 and 0 < step <= .05 and 0 < rtol < 1e-5):
        raise ValueError('probe bounds: efolds in (0,4], step in (0,.05]')
    bg = ProbeBackground(coefficient_efolds)
    def state(loga, y):
        H, q, tau, proper_time = y
        return [np.exp(loga), H, q, tau, .001*np.exp(-3*loga), .01*np.exp(-4*loga)]
    def initial_constraints(x):
        return bg.evaluate(state(0., [*x, 0., 0.]))[2][:2]
    old = bg.model.background(0.)
    initial = root(initial_constraints, [old['H'], old['q']], tol=1e-11)
    if not initial.success or max(abs(initial_constraints(initial.x))) > 1e-11:
        raise RuntimeError('initial sourced constraints failed')
    y = np.array([*initial.x, 0., 0.])
    def rhs(loga, y):
        v = bg.evaluate(state(loga, y))[0]
        if v['H'] <= 0:
            raise ValueError('expanding physical branch lost')
        return np.array([v['Hd'], v['qd'], v['sbar'], 1.])/v['H']
    def sample(loga, y):
        physical = state(loga, y)
        v, matrix, checks, margin = bg.evaluate(physical)
        a, H, q, tau, rho, rad = physical
        coeff = bg.model.background(float(tau))
        clock_rho = 2*q*q*v['PX']-v['P']+v['V']-6*v['gamma']*H*q**3
        return dict(loga=float(loga), physical_time=float(y[3]), a=float(a),
                    H=float(H), q=float(q), tau=float(tau), coefficient_a=float(coeff['a']),
                    radiation_fraction=float(rad/(3*H*H)), rho_clock=float(clock_rho),
                    rho_baryon=float(rho), rho_radiation=float(rad), clock_rate=float(v['sbar']),
                    logarithm_margin=float(margin), relative_logarithm_margin=float(margin/coeff['U']),
                    determinant=float(np.linalg.det(matrix)), condition=float(np.linalg.cond(matrix)),
                    scaled_friedmann_residual=float(abs(checks[0])/(1+3*H*H+.7+abs(clock_rho)+rho+rad)),
                    scaled_clock_residual=float(abs(checks[1])/(1+abs(v['Pt'])+abs(v['Vt'])+3*abs(H*v['W']))),
                    scalar_charge=float(a**3*checks[2]))
    loga = 0.
    samples = [sample(loga, y)]
    outcome, reason, attempted = 'physical_efold_bound', '', None
    while loga > -efolds+1e-13:
        next_loga = max(-efolds, loga-step)
        attempted = [float(loga), float(next_loga)]
        try:
            sol = solve_ivp(rhs, (loga, next_loga), y, method='DOP853',
                            rtol=rtol, atol=rtol*.01, max_step=step/4)
            if not sol.success:
                raise RuntimeError(sol.message)
            point = sample(next_loga, sol.y[:, -1])
        except (ValueError, RuntimeError, FloatingPointError, np.linalg.LinAlgError) as error:
            outcome, reason = 'branch_or_numerical_stop', str(error)
            break
        samples.append(point)
        loga, y = next_loga, sol.y[:, -1]
        if max(point['scaled_friedmann_residual'], point['scaled_clock_residual']) > 1e-8:
            outcome, reason = 'numerical_constraint_gate', 'scaled residual exceeds 1e-8'
            break
        if point['condition'] > 1e12 or point['relative_logarithm_margin'] < 1e-7:
            outcome, reason = 'conditioning_or_domain_guard', 'condition > 1e12 or relative logarithm margin < 1e-7'
            break
        if point['radiation_fraction'] >= .5:
            outcome = 'radiation_fraction_reached'
            break
    charge0 = samples[0]['scalar_charge']
    return dict(outcome=outcome, stop_reason=reason, last_attempted_loga_interval=attempted,
                parameters=dict(physical_efolds=efolds, coefficient_efolds=coefficient_efolds,
                                step=step, rtol=rtol, atol=rtol*.01, gamma=1e-6,
                                initial_rho_baryon=.001, initial_rho_radiation=.01),
                coefficient_tau_interval=[bg.model.tau_min, 0.], samples=samples,
                max_scaled_friedmann_residual=max(x['scaled_friedmann_residual'] for x in samples),
                max_scaled_clock_residual=max(x['scaled_clock_residual'] for x in samples),
                max_relative_scalar_charge_drift=max(abs(x['scalar_charge']/charge0-1) for x in samples),
                scope='Backward continuation of the same coefficient ODE and sourced homogeneous branch; dimensionless, not recombination-calibrated, not stability or a physical no-go',
                matter_charge_note='a^3 rho_b and a^4 rho_r imposed as exact first integrals; scalar charge and both constraints monitored independently',
                full_theory_status='OPEN')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--efolds', type=float, default=3.)
    parser.add_argument('--coefficient-efolds', type=float, default=5.)
    parser.add_argument('--step', type=float, default=.025)
    parser.add_argument('--rtol', type=float, default=2e-11)
    parser.add_argument('--result-file', type=Path)
    args = parser.parse_args()
    result = probe(args.efolds, args.coefficient_efolds, args.step, args.rtol)
    output = result
    if args.result_file:
        args.result_file.write_text(json.dumps(result, indent=2)+'\n')
        output = {key: value for key, value in result.items() if key != 'samples'}
        output.update(sample_count=len(result['samples']), last=result['samples'][-1])
    print(json.dumps(output, indent=2))
