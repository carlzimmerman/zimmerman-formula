#!/usr/bin/env python3
"""Finite homogeneous regularity scan, not a cosmological-data or stability fit."""
import argparse
import importlib.util
import json
import math
from pathlib import Path
import mpmath as mp
import numpy as np
import sympy as s
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
from scipy.special import expit

HERE=Path(__file__).resolve().parent

def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module

def run():
    derivation=load('cubic_background_derive',HERE/'derive.py')
    symbolic,ctx=derivation.derive()
    principal=load('cubic_principal',HERE.parent/'cubic_principal_audit/derive.py')
    principal_facts,pc=principal.derive()
    assert principal_facts['passed']
    principal_arguments=[pc[k] for k in ('gamma','q','H','qdot','M2','S0','d','B0')]
    # This profile obeys the original dust relation exactly. Use its factored
    # action-derived expression so the gamma=0 control is not cancellation noise.
    pfun=s.lambdify(principal_arguments,[pc['kinetic'],pc['dust_restoring'],pc['tau_stiffness'],
        s.factor(pc['dust_restoring']*pc['tau_stiffness'])],'mpmath',cse=True)
    old=load('stationary_profile',HERE.parent/'nonlinear_transport/stationary.py')
    _,rhs=old.symbolic()
    grid=np.linspace(-6*math.log(10),3*math.log(10),361)
    def ode(x,y):
        return rhs(math.exp(y[0]),expit(y[1]),1/(1+7*math.exp(3*x)))
    def integrate(method,rtol,atol):
        runs=[]
        for end in (grid[0],grid[-1]):
            sol=solve_ivp(ode,(0,end),[math.log(.1),0.],method=method,
                rtol=rtol,atol=atol,dense_output=True)
            if not sol.success:raise RuntimeError(sol.message)
            runs.append(sol)
        return runs
    primary=integrate('DOP853',1e-11,1e-12)
    control=integrate('Radau',2e-12,2e-13)
    mismatch=max(float(np.max(np.abs(primary[int(x>=0)].sol(x)-
                                  control[int(x>=0)].sol(x)))) for x in grid)
    assert mismatch<1e-7, 'independent profile integrators disagree'
    mp.mp.dps=70
    def point(x,gamma,runs=primary):
        lm,lv=runs[int(x>=0)].sol(float(x))
        a=mp.exp(float(x));m=mp.exp(float(lm));v=1/(1+mp.exp(-float(lv)))
        q=1/(1+m);A=mp.mpf('.1')/a**3;U=m*q*A
        H=mp.sqrt((mp.mpf('.7')+A)/3);B0=A/q*(1+2/m)
        R=B0*q*q/(H*H);z=gamma*q**3/H
        D=R-6*z+6*z*z
        # Polynomial evaluation avoids catastrophic cancellation when v->1.
        numerator=R*(1-v)+(2*R+6*v)*z+(R-6*v)*z*z
        schur=D*H*H/(q*q)
        gap=9*A*A*(H*H/B0)*(numerator/D) if D else mp.nan
        qdot=-3*A*H*v/B0-q*U/(2*H)
        W=U-2*gamma*q*q*qdot
        d=A*U/(2*q*(q*A+U));S0=U*U/(q*A+U)
        pk,pn,ps,pns=pfun(gamma,q,H,qdot,1,S0,d,B0)
        assert abs(pk-schur)<mp.mpf('1e-60')*max(1,abs(pk))
        speed=pn/pk if pk else mp.nan
        return dict(a=a,m=m,v=v,R=R,z=z,D=D,numerator=numerator,
            schur=schur,gap=gap,W=W,B0=B0,H=H,q=q,A=A,U=U,qdot=qdot,
            tau_principal=ps,restoring_times_tau=pns,restoring=pn,speed_squared=speed)
    # Cross-check compact numeric quantities against uncompressed action output.
    sample=point(0,mp.mpf('.01'))
    substitutions={ctx[k]:sample[k] for k in ('A','q','U','H','B0')}
    substitutions.update({ctx['M']:1,ctx['gamma']:mp.mpf('.01'),ctx['qd']:sample['qdot']})
    actual_delta=mp.mpf(str(ctx['delta'].subs(substitutions).evalf(60)))
    assert abs(actual_delta+sample['gap'])<mp.mpf('1e-45')
    scans=[]
    for raw in ('-3','-1','-.1','-.01','-.001','-.000001','0',
                '.000001','.001','.01','.1','1','3'):
        gamma=mp.mpf(raw);rows=[point(x,gamma) for x in grid]
        roots=[]
        for field in ('D','numerator','tau_principal','restoring_times_tau'):
            for xl,xr,pl,pr in zip(grid[:-1],grid[1:],rows[:-1],rows[1:]):
                if pl[field]*pr[field]<0:
                    root=brentq(lambda x:float(point(x,gamma)[field]),xl,xr,xtol=1e-12)
                    p=point(root,gamma);pc=point(root,gamma,control)
                    roots.append(dict(equation=field,a=str(p['a']),schur=str(p['schur']),
                        other_numerator=str(p['numerator']),other_D=str(p['D']),
                        independent_integrator_field_residual=str(pc[field]),
                        bracket_a=[str(pl['a']),str(pr['a'])]))
        scans.append(dict(gamma=raw,
            positive_schur_on_grid=all(p['schur']>0 for p in rows),
            positive_lapse_gap_on_grid=all(p['gap']>0 for p in rows),
            positive_W_on_grid=all(p['W']>0 for p in rows),
            positive_tau_principal_on_grid=all(p['tau_principal']>0 for p in rows),
            nonnegative_restoring_on_grid=all(p['restoring']>=0 for p in rows),
            speed_squared_range=[str(min(p['speed_squared'] for p in rows)),
                                 str(max(p['speed_squared'] for p in rows))],
            principal_at_present={key:str(point(0,gamma)[key]) for key in
                ('schur','tau_principal','restoring','speed_squared')},
            minimum_schur_over_B0=str(min(p['schur']/p['B0'] for p in rows)),
            minimum_gap_normalized=str(min(p['numerator']/p['D'] for p in rows)),
            resolved_sign_crossings=roots,
            first_epoch={key:str(rows[0][key]) for key in ('a','schur','gap')},
            present_epoch={key:str(point(0,gamma)[key]) for key in ('a','schur','gap')}))
    return dict(symbolic=symbolic,principal_derivation=principal_facts,parameters=dict(M_squared=1,Qc=1,I='.1',Lambda='.7',
        m_at_a1='.1',v_at_a1='.5'),epochs=len(grid),a_range=['1e-6','1e3'],
        arithmetic_digits=mp.mp.dps,integrator_log_coordinate_mismatch=mismatch,
        scans=scans,action_expression_crosscheck=True,
        caveats=['Prescribed background reconstruction, not a first-principles origin or a fit to data.',
        'No radiation/baryons in this chosen FLRW history: this is NOT a recombination/CMB calculation.',
        '70-digit algebra on float64 ODE output, not interval-certified evolution.',
        'A finite grid cannot certify all epochs or all parameter values.',
        'A zero homogeneous lapse bracket requires a renewed Dirac chain; its sign is not a physical ghost test.',
        'Principal high-frequency coefficients are not finite-k health, CMB, MOND, PPN, or a particle-free depletion mechanism.'],
        full_theory_status='OPEN')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--result-file',type=Path);a=p.parse_args()
    result=run()
    if a.result_file:a.result_file.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(epochs=result['epochs'],integrator_mismatch=result['integrator_log_coordinate_mismatch'],
        scans=[{k:r[k] for k in ('gamma','positive_schur_on_grid','positive_lapse_gap_on_grid',
            'positive_tau_principal_on_grid','nonnegative_restoring_on_grid',
            'speed_squared_range')} for r in result['scans']],full_theory_status='OPEN'),indent=2))
