#!/usr/bin/env python3
"""L194's frozen mean-field ODE, signed balance and added-mode invasion.

Only selected original function definitions are executed through AST extraction;
the source's top-level checks and JSON writes are never executed.
"""
import argparse
import ast
from functools import lru_cache
import json
from pathlib import Path
import sys

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
import sympy as sy

HERE=Path(__file__).resolve().parent
REPAIR=HERE.parents[1]
ROOT=next(p for p in HERE.parents if (p/'.git').exists())
SOURCE=ROOT/'fable_independent_2026/L194_tracking_dynamics.py'
sys.path.insert(0,str(REPAIR/'cosmological_bridge_2026'))
from radiation_probe import ProbeBackground


@lru_cache(maxsize=1)
def original():
    source_ast=ast.parse(SOURCE.read_text())
    allowed={'coeffs','cs2','epoch','track','fixed_point','multi'}
    body=[node for node in source_ast.body if isinstance(node,ast.FunctionDef) and node.name in allowed]
    if {node.name for node in body} != allowed:
        raise ValueError('expected original pure-function definitions not found')
    history=json.loads((REPAIR/'cosmological_bridge_2026/radiation_002/result.json').read_text())
    namespace=dict(np=np,solve_ivp=solve_ivp,brentq=brentq,S=history['samples'],
                   bg=ProbeBackground(history['parameters']['coefficient_efolds']))
    exec(compile(ast.Module(body=body,type_ignores=[]),str(SOURCE),'exec'),namespace)
    old=json.loads((ROOT/'fable_independent_2026/L192_results.json').read_text())
    row=next(r for r in old if abs(r['a']-.5627)<1e-3)
    return namespace,row


def exact():
    k,kn=sy.symbols('k kn',positive=True)
    nu=sy.symbols('nu',real=True)
    u=1/k
    balance=sy.simplify(-2+2*k*u)
    invasion=sy.simplify(-2+2*kn*u)
    # sigma_NN+nu*sigma_N-kappa^2*u^2*sigma=0; sigma~exp(N).
    required_k2u2=1+nu
    checks=dict(balance_zero=balance==0,
                signed_sound_speed=sy.simplify(-u*u+1/k**2)==0,
                higher_mode_rate=sy.simplify(invasion-2*(kn/k-1))==0,
                double_mode_rate=sy.simplify(invasion.subs(kn,2*k)-2)==0,
                drag_balance=sy.expand(1+nu-required_k2u2)==0,
                drag_three_control=required_k2u2.subs(nu,3)==4)
    if not all(checks.values()):raise AssertionError(checks)
    return dict(checks=checks,signed_balance='c_squared=-1/kappa_max^2',
                added_mode_log_variance_rate=str(invasion),
                drag_control='For sigma_NN+nu sigma_N-kappa²u² sigma=0, sigma=exp(N) requires kappa²u²=1+nu',
                scope='Exact identities within the stated ODE and a separate explicit drag sensitivity control, not an action-derived closure')


def invasion(kappa=1000.,ratio=2.,seed_fraction=1e-6,Nmax=12.):
    namespace,row=original()
    equilibrium,signed=namespace['fixed_point'](row,kappa)
    if not np.isfinite(equilibrium):raise ValueError('original finite-kappa balance absent')
    coeff=namespace['coeffs'](namespace['epoch'](row)['tau'])
    modes=np.array([kappa,ratio*kappa])
    def rhs(N,logs):
        c=namespace['cs2'](*coeff,row['s0'],float(np.sum(np.exp(logs))))
        if not np.isfinite(c):raise ValueError('nonfinite source proxy; not relabeled as dilution')
        return -2+2*modes*np.sqrt(max(0.,-c))
    initial=np.log([equilibrium,equilibrium*seed_fraction])
    sol=solve_ivp(rhs,(0.,Nmax),initial,method='LSODA',rtol=1e-10,atol=1e-12)
    if not sol.success:raise RuntimeError(sol.message)
    variances=np.exp(sol.y[:,-1]);total=float(sum(variances))
    endpoint=namespace['cs2'](*coeff,row['s0'],total)
    return dict(kappas=modes.tolist(),Nmax=Nmax,seed_fraction=seed_fraction,
                original_Y_equilibrium=float(equilibrium),original_signed_c_squared=float(signed),
                initial_log_variance_rates=rhs(0.,initial).tolist(),
                infinitesimal_invader_rate=float(-2+2*ratio*kappa*np.sqrt(-signed)),
                final_fractions=(variances/total).tolist(),final_total_Y=total,
                final_signed_c_squared=float(endpoint),new_balance_ratio=float(-endpoint*modes[-1]**2),
                nfev=sol.nfev,solver_success=bool(sol.success))


def run():
    namespace,row=original();co=namespace['coeffs'](namespace['epoch'](row)['tau'])
    balances=[]
    for kappa in (100.,1000.,10000.):
        Y,c=namespace['fixed_point'](row,kappa)
        balances.append(dict(kappa=kappa,Y=float(Y),signed_c_squared=float(c),
                             negative_balance_ratio=float(-c*kappa*kappa)))
    Yeq,c=namespace['fixed_point'](row,1000.)
    track=namespace['track'](row,1000.,np.log(.01*row['Yt']),Nmax=8.)
    if not track.success:raise RuntimeError(track.message)
    Yend=float(np.exp(track.y[0,-1]))
    return dict(exact=exact(),epoch_a=row['a'],source_reference_coefficients=list(co),
                proxy_critical_Y=row['Yt'],balances=balances,
                original_single_mode_probe=dict(Nmax=8.,initial_fraction_of_Yt=.01,
                    final_Y_over_equilibrium=Yend/Yeq,
                    final_signed_c_squared=float(namespace['cs2'](*co,row['s0'],Yend)),
                    nfev=track.nfev,solver_success=bool(track.success)),
                added_double_kappa_mode=invasion(),
                result='Source ODE balance is negative-c² and is invadable when a larger-kappa mode is added',
                non_claims=['No covariant action derivation of the mean-field growth/dilution closure',
                            'No physical UV cutoff, forest/CMB pass, or actual statistical background construction',
                            'No replacement of the frozen action by the separate drag sensitivity equation',
                            'The statistical-variance proposal is not excluded by the earlier localized-tail theorem'])


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--result-file',type=Path,required=True)
    args=parser.parse_args();result=run();args.result_file.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
