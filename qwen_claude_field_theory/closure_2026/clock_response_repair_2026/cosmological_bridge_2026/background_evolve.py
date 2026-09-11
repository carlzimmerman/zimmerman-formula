#!/usr/bin/env python3
"""Short sourced trajectory of the frozen action; not a recombination history."""
import argparse
from functools import lru_cache
import json
from pathlib import Path
import sys
import numpy as np
import sympy as s
from scipy.integrate import solve_ivp
from scipy.optimize import root
from derive import construct

BASE=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(BASE/'nonlinear_evolution_2026'))
from constitutive import Model


@lru_cache(maxsize=1)
def system_functions():
    d=construct();b=d['background']
    expressions=list(b['matrix'])+list(b['rhs'])+[b['friedmann'],b['clock_constraint'],d['j0']]
    inputs=sorted(set.union(*(x.free_symbols for x in expressions)),key=str)
    return [str(x) for x in inputs],s.lambdify(inputs,expressions,'numpy',cse=True)


def evolve(tend=.02):
    # The original coefficient history is evaluated at tau, never refitted
    # using the new physical H, q, radiation or baryon density.
    model=Model(.2,gamma=1e-6);names,fun=system_functions()
    aliases=dict(P='P',PX='P_X',PXX='P_XX',PXt='P_Xt',Pt='P_t',Ptt='P_tt',
                 V='V',Vt='V_t',Vtt='V_tt',W='W',Wt='W_t')
    def evaluate(state):
        a,H,q,tau,rhod,rhor=state
        jets=model.jets(tau,q*q,0.)
        values={key:float(jets[value]) for key,value in aliases.items()}
        values.update(a=a,H=H,q=q,M2=1.,Lambda=.7,gamma=model.gamma,
                      rho=rhod,Cr=1.,qr=(rhor/3.)**.25)
        out=np.asarray(fun(*[values[key] for key in names]),dtype=float)
        matrix=out[:9].reshape(3,3);rhs=out[9:12]
        return matrix,rhs,out[12:],float(jets['domain_denominator'])
    bg=model.background(0.)
    def residual(x):return evaluate([1.,x[0],x[1],0.,.001,.01])[2][:2]
    initial=root(residual,[bg['H'],bg['q']],tol=1e-11)
    if not initial.success or max(abs(residual(initial.x)))>1e-11:
        raise RuntimeError('sourced initial constraints not solved: '+initial.message)
    state0=np.array([1.,*initial.x,0.,.001,.01])
    def rhs(t,state):
        matrix,forcing,_,_=evaluate(state)
        Hd,qd,sbar=np.linalg.solve(matrix,forcing)
        a,H,q,tau,rd,rr=state
        if sbar<=0 or rd<=0 or rr<=0:raise ValueError('physical branch lost')
        return [a*H,Hd,qd,sbar,-3*H*rd,-4*H*rr]
    sol=solve_ivp(rhs,[0.,tend],state0,rtol=2e-11,atol=2e-13,
                  method='DOP853',t_eval=np.linspace(0,tend,17))
    if not sol.success:raise RuntimeError(sol.message)
    samples=[]
    for t,state in zip(sol.t,sol.y.T):
        matrix,forcing,checks,margin=evaluate(state)
        velocity=np.linalg.solve(matrix,forcing)
        samples.append(dict(t=float(t),a=float(state[0]),H=float(state[1]),q=float(state[2]),
                            tau=float(state[3]),rho_dust=float(state[4]),rho_rad=float(state[5]),
                            clock_rate=float(velocity[2]),matrix_determinant=float(np.linalg.det(matrix)),
                            matrix_condition=float(np.linalg.cond(matrix)),domain_margin=margin,
                            friedmann_residual=float(checks[0]),clock_residual=float(checks[1]),
                            scalar_charge=float(state[0]**3*checks[2])))
    dust=sol.y[0]**3*sol.y[4];rad=sol.y[0]**4*sol.y[5]
    charge=np.array([x['scalar_charge'] for x in samples])
    result=dict(samples=samples,
                max_friedmann_residual=max(abs(x['friedmann_residual']) for x in samples),
                max_clock_residual=max(abs(x['clock_residual']) for x in samples),
                max_relative_dust_charge_drift=float(max(abs(dust/dust[0]-1))),
                max_relative_radiation_charge_drift=float(max(abs(rad/rad[0]-1))),
                max_relative_scalar_charge_drift=float(max(abs(charge/charge[0]-1))),
                min_clock_rate=min(x['clock_rate'] for x in samples),min_H=min(x['H'] for x in samples),
                scope='Short late-epoch homogeneous sourced trajectory, no new reconstruction; not primordial/CMB or perturbation-stability validation',
                full_theory_status='OPEN')
    if max(result['max_friedmann_residual'],result['max_clock_residual'])>1e-9:
        raise AssertionError('homogeneous constraints drifted')
    if max(result[x] for x in ('max_relative_dust_charge_drift',
           'max_relative_radiation_charge_drift','max_relative_scalar_charge_drift'))>1e-8:
        raise AssertionError('conserved homogeneous charges drifted')
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--result-file',type=Path,required=True)
    parser.add_argument('--tend',type=float,default=.02)
    args=parser.parse_args();result=evolve(args.tend)
    args.result_file.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
