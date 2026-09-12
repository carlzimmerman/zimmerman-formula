#!/usr/bin/env python3
"""Exact anisotropic scalar-clock principal audit of L192.

Scope: fixed Minkowski metric, gamma=0, locally constant scalar gradients,
frozen coefficient jets. Both chi and tau are varied. This is not the full
Einstein/cubic principal reduction on a solved anisotropic background.
"""
import argparse
import ast
from functools import lru_cache
import json
from pathlib import Path
import sys

import numpy as np
import sympy as sy
from scipy.optimize import brentq

HERE=Path(__file__).resolve().parent
REPAIR=HERE.parent
ROOT=HERE.parents[3]
CLAUDE=ROOT/'fable_independent_2026'
BRIDGE=REPAIR/'cosmological_bridge_2026'
sys.path.insert(0,str(BRIDGE))
from radiation_probe import ProbeBackground


@lru_cache(maxsize=1)
def derive():
    Q,s,W,WY,PX,PXX=sy.symbols('Q s W WY PX PXX',positive=True)
    Y=sy.symbols('Y',nonnegative=True)
    w,WYY,c=sy.symbols('w WYY c',real=True)
    ct,cg,tt,tg=sy.symbols('ct cg tt tg',real=True)
    # Gradient perturbations are along a unit direction n; w=v dot n and
    # Y=v dot v, hence 0 <= w^2 <= Y. T=sqrt(Xtau) > 0 near the background.
    T=sy.sqrt((s+tt)**2-tg**2)
    spatial_chi=Y+2*w*cg+cg**2
    X=(Q+ct)**2-spatial_chi
    projected_Y=spatial_chi-(Q+ct)**2+((s+tt)*(Q+ct)-tg*(w+cg))**2/T**2
    # Taylor jets of the explicit invariant functions suffice for the Hessian.
    # Constants in P and the potential do not affect its derivative principal.
    dx=X-(Q**2-Y)
    dy=projected_Y-Y
    lagrangian=PX*dx+PXX*dx**2/2+T*(W+WY*dy+WYY*dy**2/2)
    derivatives=[ct,cg,tt,tg]
    hessian=sy.hessian(lagrangian,derivatives).subs({x:0 for x in derivatives})
    hessian=hessian.applyfunc(sy.simplify)
    C=WY+2*w**2*WYY
    F=W-2*Q**2*C-2*w**2*WY
    K=2*PX+4*Q**2*PXX
    expected=sy.Matrix([
        [K,-4*Q*w*PXX,0,-2*w*WY],
        [-4*Q*w*PXX,-2*PX+4*w**2*PXX+2*s*C,2*w*WY,-2*Q*C],
        [0,2*w*WY,0,0],
        [-2*w*WY,-2*Q*C,0,-F/s]])
    # Real derivative replacement (dt,dx)=(-c,1), before field variation:
    # congruence returns the symmetric Fourier characteristic matrix.
    substitution=sy.Matrix([[-c,0],[1,0],[0,-c],[0,1]])
    symbol=(substitution.T*hessian*substitution).applyfunc(sy.simplify)
    schur=sy.factor(symbol[0,0]-symbol[0,1]**2/symbol[1,1])
    G=2*PX-4*PXX*w**2-2*s*C*(W-2*w**2*WY)/F
    expected_schur=K*c**2+8*Q*PXX*w*c-G
    quarter_discriminant=16*Q**2*PXX**2*w**2+K*G
    proxy_s=PX*(W-2*Q**2*C)/(W*C)
    marginal_discriminant=sy.factor(quarter_discriminant.subs(s,proxy_s))
    negative_form=-8*PX*w**2*(PXX+K*Q**2*C*WY/(W*F))
    U,d,m=sy.symbols('U d m',positive=True)
    baseline=sy.factor((G/K).subs(w,0).subs({W:U,WY:d,PX:U*d/m,PXX:2*U*d**2/m**2}))
    closure=(1-s)*(m/U)/(2-m/U)
    closure_difference=sy.factor((baseline-closure).subs(m,U-2*d*Q**2))
    checks=dict(
        hessian_matches_chain_rule=all(sy.simplify(x)==0 for x in hessian-expected),
        mixed_clock_time_terms_cancel=sy.simplify(symbol[0,1]+2*Q*C)==0,
        schur_identity=sy.factor(schur-expected_schur)==0,
        proxy_zero_has_negative_discriminant=sy.factor(marginal_discriminant-negative_form)==0,
        zero_gradient_recovers_L186=closure_difference==0)
    if not all(checks.values()):
        raise AssertionError(checks)
    return dict(symbols=locals(),hessian=hessian,symbol=symbol,schur=schur,
                K=K,C=C,F=F,G=G,quarter_discriminant=quarter_discriminant,
                negative_form=negative_form,checks=checks)


def jets(U,d,ell,Q,Y):
    X=Q*Q-Y
    margin=U-2*d*X
    if U<=0 or d<=0 or ell<=0 or margin<=0 or Y<0:
        raise ValueError('outside stated constitutive domain')
    return dict(PX=U*d/margin,PXX=2*U*d*d/margin**2,
                W=U+2*d*ell*(np.sqrt(1+Y/ell)-1),
                WY=d/np.sqrt(1+Y/ell),WYY=-d/(2*ell)*(1+Y/ell)**-1.5,
                X=X,margin=margin)


def principal(U,d,ell,Q,s,Y,mu):
    if not -1<=mu<=1:
        raise ValueError('direction cosine outside [-1,1]')
    j=jets(U,d,ell,Q,Y)
    PX,PXX,W,WY,WYY=(j[x] for x in ('PX','PXX','W','WY','WYY'))
    w=np.sqrt(Y)*mu
    z=w*w
    C=WY+2*z*WYY
    F=W-2*Q*Q*C-2*z*WY
    K=2*PX+4*Q*Q*PXX
    if F==0:
        raise ValueError('clock elliptic Schur denominator vanishes')
    G=2*PX-4*PXX*z-2*s*C*(W-2*z*WY)/F
    quarter=16*Q*Q*PXX*PXX*z+K*G
    drift=4*Q*PXX*w
    speeds=[(-drift+sign*np.lib.scimath.sqrt(quarter))/K for sign in (-1,1)]
    return dict(jets=j,direction_cosine=mu,C=C,F=F,K=K,G=G,
                quarter_discriminant=float(quarter),
                phase_speeds_real=[float(x.real) for x in speeds],
                phase_speeds_imag=[float(x.imag) for x in speeds])


@lru_cache(maxsize=1)
def proxy_function():
    # Extract only the inspected pure function: importing L192 would execute
    # its top-level write to Claude's results. Preserve that file untouched.
    tree=ast.parse((CLAUDE/'L192_gradient_criticality.py').read_text())
    selected=[node for node in tree.body if isinstance(node,ast.FunctionDef) and node.name=='cs2']
    if len(selected)!=1:
        raise ValueError('L192 cs2 function locator changed')
    module=ast.Module(body=selected,type_ignores=[])
    namespace={'np':np}
    exec(compile(module,str(CLAUDE/'L192_gradient_criticality.py'),'exec'),namespace)
    return namespace['cs2']


def numerical():
    archive=json.loads((BRIDGE/'radiation_002/result.json').read_text())
    claude=json.loads((CLAUDE/'L192_results.json').read_text())
    samples=archive['samples'][::23]+[archive['samples'][-1]]
    if len(samples)!=len(claude):
        raise ValueError('sample alignment changed')
    bg=ProbeBackground(archive['parameters']['coefficient_efolds'])
    proxy=proxy_function()
    rows=[]
    for sample,old in zip(samples,claude):
        if abs(sample['a']-old['a'])>1e-12:
            raise ValueError('source epochs do not match')
        coeff=bg.model.background(float(sample['tau']))
        U,d,ell,qbar=(coeff[k] for k in ('U','d','ell','q'))
        s=sample['clock_rate']
        baseline=principal(U,d,ell,sample['q'],s,0.,0.)
        mrel=(U-2*d*sample['q']**2)/U
        baseline['closure_formula']=(1-s)*mrel/(2-mrel)
        baseline['computed_G_over_K']=baseline['G']/baseline['K']
        row=dict(a=sample['a'],tau=sample['tau'],s=s,U=U,d=d,ell=ell,
                 coefficient_q=qbar,physical_q=sample['q'],zero_Y_actual_q=baseline)
        if old['Yt']>0:
            row['coefficient_q_cases']=[]
            for label,Y in (('L192_longitudinal_zero',old['Yl']),('L192_transverse_zero',old['Yt'])):
                row['coefficient_q_cases'].append(dict(label=label,Y=Y,
                    proxy_T=float(proxy(U,d,ell,qbar,s,Y,'T')),
                    proxy_L=float(proxy(U,d,ell,qbar,s,Y,'L')),
                    transverse=principal(U,d,ell,qbar,s,Y,0.),
                    longitudinal=principal(U,d,ell,qbar,s,Y,1.)))
            # Correcting qbar to the actual physical Q does not remove the
            # algebraic defect. Recompute its proxy roots for that same jet.
            Q=sample['q']
            physical_cases=[]
            for pol in ('L','T'):
                hi=old['Yt']*8
                root=brentq(lambda Y:proxy(U,d,ell,Q,s,Y,pol),0.,hi,xtol=1e-16)
                physical_cases.append(dict(proxy_polarization=pol,Y=root,
                    proxy_value=float(proxy(U,d,ell,Q,s,root,pol)),
                    transverse=principal(U,d,ell,Q,s,root,0.),
                    longitudinal=principal(U,d,ell,Q,s,root,1.)))
            row['physical_q_recomputed_proxy_roots']=physical_cases
            lo=old['Yl'];hi=old['Yt']
            root=brentq(lambda Y:principal(U,d,ell,qbar,s,Y,1.)['quarter_discriminant'],lo,hi,xtol=1e-16)
            row['longitudinal_hyperbolicity_boundary_in_restricted_symbol']=dict(Y=root,
                **principal(U,d,ell,qbar,s,root,1.))
        rows.append(row)
    return rows


def run():
    exact=derive()
    return dict(exact_checks=exact['checks'],
                exact_expressions={key:str(exact[key]) for key in
                                   ('hessian','symbol','schur','K','C','F','G','quarter_discriminant','negative_form')},
                rows=numerical(),
                primary_verdict='L192 substitution is not the anisotropic principal symbol even in the restricted fixed-metric gamma0 two-field problem.',
                scope='Both tau and chi varied; frozen constant gradients and jets; gamma=0; metric held fixed.',
                non_claims=['Not full Einstein/cubic constrained principal reduction',
                            'Not a solved anisotropic or inhomogeneous cosmological background',
                            'Not proof of a nonlinear attractor or of exact dust stress',
                            'No coefficient reconstruction, extra particle dark matter, or CMB mapping'])


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--result-file',required=True,type=Path)
    args=parser.parse_args()
    result=run()
    args.result_file.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(exact_checks=result['exact_checks'],primary_verdict=result['primary_verdict'],
                         first_counterexample=result['rows'][0]),indent=2))
