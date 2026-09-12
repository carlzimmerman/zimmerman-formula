#!/usr/bin/env python3
"""Resolve the early-clock survivors with larger actual operator wavenumbers.

Imports archived initial_data.py unchanged. This changes only diagnostic k
and requested physical continuation range; coefficients and equations are fixed.
"""
import argparse
import json
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp
from initial_data import FrozenBackground, sample as base_sample, state, gate, roots
from transfer_evolve import mode_system


def spectrum(v,k):
    op,matrix,*_ = mode_system(v,k)
    freq = k/v['a']
    scales = np.array([1.,freq,1.,freq,1.,max(v['rho'],1.)*freq])
    eigenvalues = np.linalg.eigvals(op*scales[None,:]/scales[:,None]/freq)
    values = -eigenvalues**2
    rad = sorted(range(6),key=lambda i:abs(values[i]-1/3))[:2]
    other = [i for i in range(6) if i not in rad]
    dust = sorted(other,key=lambda i:abs(values[i]))[:2]
    clock = [i for i in other if i not in dust]
    return dict(k=k,clock_cs2=float(np.mean(values[clock]).real),
                radiation_cs2=float(np.mean(values[rad]).real),
                dust_cs2=[float(values[i].real) for i in dust],
                scaled_eigenvalue_real=eigenvalues.real.tolist(),
                scaled_eigenvalue_imag=eigenvalues.imag.tolist(),
                transfer_matrix_condition=float(np.linalg.cond(matrix)))


def sample(bg,initial,loga,y):
    result = base_sample(bg,initial,loga,y)
    v = bg.evaluate(state(initial,loga,y),extended=True)[0]
    result['high_k'] += [spectrum(v,k) for k in (3e6,3e7)]
    result['clock_cs2'] = result['high_k'][-1]['clock_cs2']
    result['sign_resolution_scale'] = max(1e-10,10*abs(
        result['high_k'][-2]['clock_cs2']-result['high_k'][-1]['clock_cs2']))
    return result


def continuation(bg,initial,direction,step):
    def rhs(loga,y):
        v=bg.evaluate(state(initial,loga,y))[0]
        if v['H'] <= 0:
            raise ValueError('expanding branch lost')
        return np.array([v['Hd'],v['qd'],v['sbar'],1.])/v['H']
    loga=0.
    y=np.array([initial['H'],initial['q'],initial['tau'],0.])
    points=[]
    outcome='requested_loga_bound'
    reason=''
    attempted=None
    rtol=5e-12
    try:
        points.append(sample(bg,initial,loga,y))
        outcome=gate(points[-1]) or outcome
        while outcome=='requested_loga_bound' and abs(loga)<2.3-1e-13:
            next_loga=direction*min(2.3,abs(loga)+step)
            attempted=[loga,next_loga]
            sol=solve_ivp(rhs,(loga,next_loga),y,method='DOP853',rtol=rtol,
                          atol=rtol*.01,max_step=step/4)
            if not sol.success:
                raise RuntimeError(sol.message)
            loga,y=next_loga,sol.y[:,-1]
            points.append(sample(bg,initial,loga,y))
            outcome=gate(points[-1]) or outcome
            if abs(points[-1]['scalar_charge']/points[0]['scalar_charge']-1)>1e-8:
                outcome='scalar_charge_drift_stop'
    except (ValueError,RuntimeError,FloatingPointError,np.linalg.LinAlgError) as exc:
        outcome,reason='branch_or_numerical_stop',str(exc)
    return dict(initial=initial,direction=direction,step=step,rtol=rtol,
                requested_loga=direction*2.3,outcome=outcome,reason=reason,
                attempted_interval=attempted,samples=points,
                max_charge_drift=max((abs(p['scalar_charge']/points[0]['scalar_charge']-1) for p in points),default=None))


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--source',type=Path,required=True)
    parser.add_argument('--result-file',type=Path,required=True)
    parser.add_argument('--step',type=float,default=.025)
    args=parser.parse_args()
    if not .005<=args.step<=.025:
        raise ValueError('step outside contract')
    previous=json.loads(args.source.read_text())
    selected=[r['initial'] for r in previous['continuations']
              if r['outcome']=='clock_gradient_unresolved']
    bg=FrozenBackground()
    representative=[i for i in selected if i['baryon']==.001][0]
    counterparts=roots(bg.model,representative['tau'],representative['baryon'],representative['radiation'],3201)
    selected += [min(counterparts,key=lambda r:abs(r['q']+representative['q']))]
    result=dict(source=str(args.source),continuations=[continuation(bg,i,d,args.step)
                for i in selected for d in (-1,1)],full_theory_status='OPEN',
                finite_k=[3000,30000,300000,3000000,30000000],
                non_claims=['No all-initial-data theorem','No rigorous k-to-infinity error certificate',
                            'No complete kinetic/DOF reduction','No CMB/recombination map or calibrated today'])
    args.result_file.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps([dict(initial=r['initial'],direction=r['direction'],outcome=r['outcome'],reason=r['reason'],
                           count=len(r['samples']),last={k:r['samples'][-1][k] for k in
                           ('loga','H','tau','clock_cs2','clock_rate','radiation_fraction')})
                          for r in result['continuations']],indent=2))
