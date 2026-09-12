#!/usr/bin/env python3
"""Same-action density bookkeeping and bounded alternative-root search.

Constant Lambda, evolving clock density, evolving coefficient V(tau), and
the combined dark sector are distinct objects. None is fitted here.
Sign-change root isolation is not a proof of exhaustive branch enumeration.
"""
import argparse
import json
from pathlib import Path
import numpy as np
from scipy.optimize import brentq
from transfer_evolve import Background, mode_system
from radiation_probe import ProbeBackground


def stress(v):
    q, H, g, s0 = (v[k] for k in ('q', 'H', 'gamma', 'sbar'))
    rho = 2*q*q*v['PX']-v['P']+v['V']-6*g*H*q**3
    pressure = v['P']-v['V']+s0*v['W']+2*g*q*q*v['qd']
    px_dot = s0*v['PXt']+2*q*v['qd']*v['PXX']
    p_dot = s0*v['Pt']+2*q*v['qd']*v['PX']
    rho_dot = (4*q*v['qd']*v['PX']+2*q*q*px_dot-p_dot+s0*v['Vt']
               -6*g*(v['Hd']*q**3+3*H*q*q*v['qd']))
    vacuum = v['M2']*v['Lambda']
    rho_x, p_x = rho+vacuum, pressure-vacuum
    return dict(rho_Lambda=vacuum, V_tau=v['V'], rho_clock=rho, p_clock=pressure,
                rho_X=rho_x, p_X=p_x, w_clock=pressure/rho, w_X=p_x/rho_x,
                dlnrho_X_dlna=rho_dot/(H*rho_x),
                continuity_prediction=-3*(1+p_x/rho_x),
                ward_residual=rho_dot+3*H*(rho+pressure),
                Omega_Lambda=vacuum/(3*v['M2']*H*H),
                scope='X=Lambda+clock, not an independently identified observational dark-energy component')


def constraint_curve(model, q):
    """Eliminate H with the actual clock equation before solving Friedmann."""
    j = model.jets(0., q*q, 0.)
    H = (j['P_t']-j['V_t'])/(3*j['W'])
    rho = 2*q*q*j['P_X']-j['P']+j['V']-6*model.gamma*H*q**3
    return 3*H*H-.7-rho-.001-.01, H


def find_roots(model, grid=1601):
    raw = model.background(0.)
    qmax = np.sqrt(raw['U']/(2*raw['d']))
    # Cover both orientations; add logarithmic boundary sampling without
    # evaluating the singular endpoints. Even-multiplicity roots can be missed.
    x = np.unique(np.r_[np.linspace(-.999999, .999999, grid),
                        -1+np.geomspace(1e-10, .01, 100),
                        1-np.geomspace(1e-10, .01, 100)])
    values = [constraint_curve(model, y*qmax)[0] for y in x]
    roots = []
    for i, (left, right) in enumerate(zip(x, x[1:])):
        if values[i]*values[i+1] >= 0:
            continue
        q = brentq(lambda q: constraint_curve(model, q)[0],
                   left*qmax, right*qmax, xtol=1e-14)
        error, H = constraint_curve(model, q)
        roots.append(dict(q=float(q), H=float(H), residual=float(error),
                          bracket=[float(left*qmax), float(right*qmax)], q_domain_max=float(qmax)))
    return roots


def clock_speed(v, k):
    """Full operator spectrum; radiation/dust identification checked, not preset."""
    eigenvalues = np.linalg.eigvals(mode_system(v, k)[0])
    squared = -(eigenvalues*v['a']/k)**2
    used = set()
    pairs = []
    for i in np.argsort(-abs(squared)):
        if i in used:
            continue
        j = min((j for j in range(6) if j != i and j not in used),
                key=lambda j: abs(squared[j]-squared[i]))
        used.update((i, j))
        pairs.append(float(((squared[i]+squared[j])/2).real))
    radiation = min(pairs, key=lambda x: abs(x-1/3))
    if abs(radiation-1/3)>1e-3:
        raise ValueError('radiation mode failed control')
    rest = list(pairs)
    rest.remove(radiation)
    dust, clock = sorted(rest, key=abs)
    return clock, radiation, dust


def inventory(grid=1601):
    bg = Background(.02)
    roots = find_roots(bg.model, grid)
    for row in roots:
        try:
            v, matrix, checks, _ = bg.evaluate([1., row['H'], row['q'], 0., .001, .01], extended=True)
            row.update(stress(v), clock_rate=v['sbar'], determinant=float(np.linalg.det(matrix)),
                       condition=float(np.linalg.cond(matrix)), constraint_residuals=checks[:2].tolist(),
                       clock_cs2=[clock_speed(v, k)[0] for k in (3000., 30000.)],
                       expanding=row['H']>0, kinetic_health='not established by positive sound speed')
        except (ValueError, np.linalg.LinAlgError) as exc:
            row['rejected'] = str(exc)
    archive = json.loads((Path(__file__).parent/'radiation_002/result.json').read_text())
    back = ProbeBackground(archive['parameters']['coefficient_efolds'])
    samples = archive['samples']
    history = []
    for target in (1., .5, .3, .1):
        smp = min(samples, key=lambda s: abs(s['a']-target))
        v = back.evaluate([smp['a'], smp['H'], smp['q'], smp['tau'],
                           smp['rho_baryon'], smp['rho_radiation']], extended=True)[0]
        history.append(dict(a=smp['a'], **stress(v)))
    return dict(roots=roots, existing_branch_density_history=history,
                grid=grid, searched_q_over_qmax=[-1+1e-10, 1-1e-10],
                root_search_limit='sign-changing roots only; not exhaustive or all initial epochs',
                initial_data='tau=0,a=1,rho_b=.001,rho_r=.01, M2=1,Lambda=.7,gamma=1e-6 unchanged',
                full_theory_status='OPEN')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--result-file', type=Path, required=True)
    parser.add_argument('--grid', type=int, default=1601)
    args = parser.parse_args()
    result = inventory(args.grid)
    args.result_file.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))
