#!/usr/bin/env python3
"""Bounded initial-data search for the unmodified clock action.

The field tau and conserved physical matter charges vary; coefficient ODE
initial data and all action functions remain frozen. This searches sign-changing
constraint roots, not all roots, and screens only local high-k/partial kinetic
conditions, not full stability or observational viability.
"""
import argparse
from collections import Counter
import json
from pathlib import Path
import sys

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

BASE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE / 'cosmological_bridge_2026'))
from background_evolve import Model, system_functions
from radiation_probe import BackwardHistory
from transfer_evolve import Background, mode_system
from branch_continuation import high_k_modes
from branch_kinetic import kinetic
from dark_energy_branches import stress


class FrozenHistory(Model):
    """Join two integrations of the SAME coefficient IVP, without extrapolation."""
    def __init__(self):
        super().__init__(2., gamma=1e-6)
        self.backward = BackwardHistory(5.)
        self.tau_min = self.backward.tau_min
        self.tau_max = 2.

    def background(self, tau):
        if tau < 0:
            return self.backward.background(float(tau))
        return super().background(float(tau))


class FrozenBackground(Background):
    def __init__(self):
        self.model = FrozenHistory()
        self.names, self.fun = system_functions()


def curve(model, q, tau, baryon, radiation):
    jets = model.jets(float(tau), np.asarray(q)**2, 0.)
    H = (jets['P_t']-jets['V_t'])/(3*jets['W'])
    rho = 2*np.asarray(q)**2*jets['P_X']-jets['P']+jets['V']-6*model.gamma*H*np.asarray(q)**3
    return 3*H*H-.7-rho-baryon-radiation, H


def roots(model, tau, baryon, radiation, grid=1601):
    coeff = model.background(float(tau))
    qmax = np.sqrt(coeff['U']/(2*coeff['d']))
    x = np.unique(np.r_[np.linspace(-.999999, .999999, grid),
                        -1+np.geomspace(1e-10, .01, 100),
                        1-np.geomspace(1e-10, .01, 100)])
    errors = curve(model, x*qmax, tau, baryon, radiation)[0]
    found = []
    for i in range(len(x)-1):
        if not np.isfinite(errors[i:i+2]).all() or errors[i]*errors[i+1] >= 0:
            continue
        q = brentq(lambda q: curve(model, q, tau, baryon, radiation)[0],
                   x[i]*qmax, x[i+1]*qmax, xtol=1e-14)
        error, H = curve(model, q, tau, baryon, radiation)
        found.append(dict(a=1., H=float(H), q=float(q), tau=float(tau),
                          baryon=float(baryon), radiation=float(radiation),
                          root_residual=float(error), qmax=float(qmax),
                          bracket=[float(x[i]*qmax), float(x[i+1]*qmax)]))
    return found


def state(initial, loga, y):
    H, q, tau, time = y
    return [np.exp(loga), H, q, tau,
            initial['baryon']*np.exp(-3*loga), initial['radiation']*np.exp(-4*loga)]


def extended_modes(v):
    """Preserve old operator probes and add a third wavenumber for convergence."""
    result = high_k_modes(v)
    k = 300000.
    operator,matrix,*_ = mode_system(v,k)
    frequency = k/v['a']
    scales = np.array([1.,frequency,1.,frequency,1.,max(v['rho'],1.)*frequency])
    eigenvalues = np.linalg.eigvals(operator*scales[None,:]/scales[:,None]/frequency)
    values = -eigenvalues**2
    radiation = sorted(range(6),key=lambda i:abs(values[i]-1/3))[:2]
    remaining = [i for i in range(6) if i not in radiation]
    dust = sorted(remaining,key=lambda i:abs(values[i]))[:2]
    clock = [i for i in remaining if i not in dust]
    result.append(dict(k=k,clock_cs2=float(np.mean(values[clock]).real),
                       radiation_cs2=float(np.mean(values[radiation]).real),
                       dust_cs2=[float(values[i].real) for i in dust],
                       scaled_eigenvalue_real=eigenvalues.real.tolist(),
                       scaled_eigenvalue_imag=eigenvalues.imag.tolist(),
                       transfer_matrix_condition=float(np.linalg.cond(matrix))))
    return result


def sample(bg, initial, loga, y, *, with_kinetic=True):
    physical = state(initial, loga, y)
    v, matrix, checks, margin = bg.evaluate(physical, extended=True)
    coeff = bg.model.background(float(physical[3]))
    modes = extended_modes(v)
    s = stress(v)
    mrel = float(margin/coeff['U'])
    result = dict(loga=float(loga), a=float(physical[0]), H=float(physical[1]),
                  q=float(physical[2]), tau=float(physical[3]), time=float(y[3]),
                  baryon=float(physical[4]), radiation=float(physical[5]),
                  coefficient_a=float(coeff['a']), coefficient_q=float(coeff['q']),
                  clock_rate=float(v['sbar']), relative_logarithm_margin=mrel,
                  gamma0_formula=float((1-v['sbar'])*mrel/(2-mrel)),
                  high_k=modes, clock_cs2=modes[-1]['clock_cs2'],
                  sign_resolution_scale=max(1e-10,10*abs(modes[-2]['clock_cs2']-modes[-1]['clock_cs2'])),
                  radiation_fraction=float(physical[5]/(3*v['H']**2)),
                  clock_fraction=float(s['rho_clock']/(3*v['H']**2)),
                  background_condition=float(np.linalg.cond(matrix)),
                  scalar_charge=float(physical[0]**3*checks[2]),
                  scaled_friedmann_residual=float(abs(checks[0])/(1+3*v['H']**2+.7+abs(s['rho_clock'])+sum(physical[4:]))),
                  scaled_clock_residual=float(abs(checks[1])/(1+abs(v['Pt'])+abs(v['Vt'])+3*abs(v['H']*v['W']))),
                  stress=s)
    if with_kinetic:
        kresult = kinetic(v, 3000.)
        result['kinetic'] = dict(eigenvalues=kresult['eigenvalues'].tolist(),
                                 negative_tolerance=float(kresult['null_tolerance']),
                                 matrix=kresult['matrix'].tolist())
    return result


def gate(point):
    if point['H'] <= 0:
        return 'not_expanding'
    if max(point['scaled_friedmann_residual'],point['scaled_clock_residual']) > 1e-8:
        return 'constraint_residual_stop'
    if point['background_condition'] > 1e12 or point['relative_logarithm_margin'] < 1e-7:
        return 'conditioning_or_domain_stop'
    if any(abs(m['radiation_cs2']-1/3) > 1e-4 for m in point['high_k']):
        return 'mode_assignment_unresolved'
    if 'kinetic' in point and min(point['kinetic']['eigenvalues']) < -point['kinetic']['negative_tolerance']:
        return 'partial_kinetic_negative'
    if point['clock_cs2'] < -point['sign_resolution_scale']:
        return 'clock_gradient_negative'
    if point['clock_cs2'] <= point['sign_resolution_scale']:
        return 'clock_gradient_unresolved'
    return None


def continue_initial(bg, initial, direction=-1, efolds=2.3, step=.025, rtol=2e-11):
    if direction not in (-1,1) or not 0 < efolds <= 3 or not 0 < step <= .05:
        raise ValueError('out-of-contract continuation')
    def rhs(loga, y):
        v = bg.evaluate(state(initial, loga, y))[0]
        if v['H'] <= 0:
            raise ValueError('expanding branch lost')
        return np.array([v['Hd'],v['qd'],v['sbar'],1.])/v['H']
    y = np.array([initial['H'], initial['q'], initial['tau'], 0.])
    loga = 0.
    points = []
    outcome = 'requested_loga_bound'
    reason = ''
    attempted = None
    try:
        points.append(sample(bg, initial, loga, y))
        outcome = gate(points[-1]) or outcome
        while outcome == 'requested_loga_bound' and abs(loga) < efolds-1e-13:
            next_loga = direction*min(efolds,abs(loga)+step)
            attempted = [loga,next_loga]
            sol = solve_ivp(rhs,(loga,next_loga),y,method='DOP853',rtol=rtol,
                            atol=rtol*.01,max_step=step/4)
            if not sol.success:
                raise RuntimeError(sol.message)
            y, loga = sol.y[:,-1], next_loga
            points.append(sample(bg,initial,loga,y))
            outcome = gate(points[-1]) or outcome
            drift = abs(points[-1]['scalar_charge']/points[0]['scalar_charge']-1)
            if drift > 1e-8:
                outcome = 'scalar_charge_drift_stop'
    except (ValueError,RuntimeError,FloatingPointError,np.linalg.LinAlgError) as exc:
        outcome,reason = 'branch_or_numerical_stop',str(exc)
    return dict(initial=initial,direction=direction,requested_loga=direction*efolds,
                step=step,rtol=rtol,outcome=outcome,reason=reason,
                attempted_interval=attempted,samples=points,
                max_charge_drift=max((abs(p['scalar_charge']/points[0]['scalar_charge']-1) for p in points),default=None))


def scan(grid=1601):
    bg = FrozenBackground()
    tau_values = [float(bg.model.backward.history.sol(n)[2]) for n in (-2.,-1.,-.5,0.)]+[.5,1.]
    baryons = [.0001,.001,.01]
    radiations = [.0001,.01,1.]
    inventory = []
    for tau in tau_values:
        for baryon in baryons:
            for radiation in radiations:
                found = roots(bg.model,tau,baryon,radiation,grid)
                for row in found:
                    try:
                        row['point'] = sample(bg,row,0.,[row['H'],row['q'],tau,0.])
                        row['gate'] = gate(row['point']) or 'local_screen_pass'
                    except (ValueError,RuntimeError,np.linalg.LinAlgError) as exc:
                        row['gate'], row['reason'] = 'initial_evaluation_rejected',str(exc)
                inventory.append(dict(tau=tau,baryon=baryon,radiation=radiation,roots=found))
    # All locally surviving positive-orientation roots: same finite search,
    # avoid spending continuation time on the nearly orientation-degenerate copy.
    selected = [r for entry in inventory for r in entry['roots']
                if r['gate']=='local_screen_pass' and r['q']>0]
    continuations=[]
    for row in selected:
        initial = {k:v for k,v in row.items() if k not in ('point','gate')}
        continuations.append(continue_initial(bg,initial))
    statuses = Counter(r['gate'] for entry in inventory for r in entry['roots'])
    return dict(grid=grid,tau_values=tau_values,baryon_values=baryons,radiation_values=radiations,
                coefficient_tau_interval=[bg.model.tau_min,bg.model.tau_max],
                inventory=inventory,initial_status_counts=dict(statuses),continuations=continuations,
                continuation_status_counts=dict(Counter(r['outcome'] for r in continuations)),
                full_theory_status='OPEN',
                non_claims=['Not exhaustive initial-data or root enumeration',
                            'No exact high-k asymptotic error bound',
                            'Partial kinetic elimination is not a complete no-ghost or DOF theorem',
                            'No CMB/recombination mapping, no observationally calibrated today',
                            'No coefficient reconstruction or extra particle dark matter'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--result-file',required=True,type=Path)
    parser.add_argument('--grid',type=int,default=1601)
    parser.add_argument('--refine-input',type=Path)
    args = parser.parse_args()
    if args.refine_input:
        previous = json.loads(args.refine_input.read_text())
        candidates = sorted(previous['continuations'],key=lambda r:len(r['samples']),reverse=True)[:3]
        candidates += [r for r in previous['continuations'] if r['outcome'] != 'clock_gradient_negative' and r not in candidates]
        bg = FrozenBackground()
        runs = [continue_initial(bg,r['initial'],direction=d,efolds=(2.3 if d<0 else .2),
                                 step=.0125,rtol=5e-12) for r in candidates for d in (-1,1)]
        result = dict(continuations=runs,full_theory_status='OPEN')
    else:
        result = scan(args.grid)
    args.result_file.write_text(json.dumps(result,indent=2)+'\n')
    summary = {k:v for k,v in result.items() if k not in ('inventory','continuations')}
    summary['continuations'] = [dict(initial=r['initial'],outcome=r['outcome'],reason=r['reason'],
                                      count=len(r['samples']),last={k:r['samples'][-1][k] for k in
                                      ('loga','tau','clock_cs2','clock_rate','radiation_fraction')}
                                      if r['samples'] else None) for r in result['continuations']]
    print(json.dumps(summary,indent=2))
