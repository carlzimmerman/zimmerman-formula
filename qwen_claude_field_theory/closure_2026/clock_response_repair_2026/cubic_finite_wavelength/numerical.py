#!/usr/bin/env python3
"""Finite-wave constraint signs and canonical transfer from the derived action."""
import argparse
import importlib.util
import json
import math
from pathlib import Path
import mpmath as mp
import numpy as np
from scipy.integrate import solve_ivp
from scipy.special import expit
import sympy as s

HERE=Path(__file__).resolve().parent

def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module

def run():
    facts,c=load('finite_action',HERE/'derive.py').derive()
    _,rhs=load('stationary_profile',HERE.parent/'nonlinear_transport/stationary.py').symbolic()
    order=['a','H','q','M','gamma','k','A','U','B0','qd']
    args=[c[v] for v in order]
    parts=[c['pre_zeta_kinetic'],c['velocity_mixing'],c['field_mixing'],
           c['constraint'].subs(c['k'],0),c['constraint_k2'],c['raw_mixed'],c['raw_potential']]
    function=s.lambdify(args,parts,'mpmath',cse=True)
    grid=np.linspace(-6*math.log(10),3*math.log(10),37)
    def ode(x,y):return rhs(math.exp(y[0]),expit(y[1]),1/(1+7*math.exp(3*x)))
    def profile(method,rtol,atol):
        result=[]
        for end in (grid[0],grid[-1]):
            sol=solve_ivp(ode,(0,end),[math.log(.1),0.],method=method,
                rtol=rtol,atol=atol,dense_output=True)
            assert sol.success,sol.message
            result.append(sol)
        return result
    primary=profile('DOP853',1e-11,1e-12);control=profile('Radau',2e-12,2e-13)
    disagreement=max(float(np.max(np.abs(primary[int(x>=0)].sol(x)-
                                 control[int(x>=0)].sol(x)))) for x in grid)
    assert disagreement<1e-7
    mp.mp.dps=80
    def coefficients(x,gamma,kval,source=primary):
        lm,lv=source[int(x>=0)].sol(float(x));a=mp.exp(float(x))
        m=mp.exp(float(lm));v=1/(1+mp.exp(-float(lv)))
        q=1/(1+m);A=mp.mpf('.1')/a**3;U=m*q*A
        H=mp.sqrt((mp.mpf('.7')+A)/3);B0=A/q*(1+2/m)
        qd=-3*A*H*v/B0-q*U/(2*H)
        A0,J,E,D0,D2,Braw,Craw=function(a,H,q,1,gamma,kval,A,U,B0,qd)
        D=D0+D2*kval*kval
        if D==0:raise ZeroDivisionError('unreduced zeta constraint required at pole')
        Af=A0-J*J/D;Bf=Braw-J*E/D;Cf=Craw-E*E/D
        return dict(a=a,H=H,A0=A0,J=J,E=E,D0=D0,D2=D2,D=D,
                    kinetic=Af,cross=Bf,potential=Cf)
    rows=[];cases=[]
    for gs in ('0','.000001'):
        g=mp.mpf(gs)
        for x in grid:
            p=coefficients(x,g,mp.mpf(1))
            ratios=[]
            for wavelength_ratio in np.logspace(-4,4,17):
                point=coefficients(x,g,mp.mpf(float(wavelength_ratio))*p['a']*p['H'])
                ratios.append(point['kinetic']/point['A0'])
            criterion=bool(p['D0']<0 and p['D2']<0 and p['A0']>0)
            rows.append(dict(gamma=gs,a=str(p['a']),D0=str(p['D0']),D2=str(p['D2']),
                A0=str(p['A0']),all_nonzero_wavenumbers_sufficient_signs=criterion,
                kinetic_over_bare_min=str(min(ratios)),kinetic_over_bare_max=str(max(ratios)),
                possible_positive_k_squared_pole=str(-p['D0']/p['D2']) if p['D0']*p['D2']<0 else None))
        # Integrate actual Hamilton equations without numerically differentiating
        # time-dependent action coefficients. This preserves the u*udot term.
        for kval in (mp.mpf(1),mp.mpf(10),mp.mpf(100)):
            initial=coefficients(-2.,g,kval);scale=float(initial['kinetic']*initial['H'])
            def field_ode(x,y,source=primary):
                p=coefficients(x,g,kval,source)
                Af,Bf,Cf,H=[float(p[key]) for key in ('kinetic','cross','potential','H')]
                generator=np.array([[-Bf/Af,scale/Af],
                    [(Cf-Bf*Bf/Af)/scale,Bf/Af]])/H
                assert abs(np.trace(generator))<1e-12
                return (generator@y.reshape(2,2)).ravel()
            results=[]
            for method,tolerance in (('DOP853',1e-9),('Radau',2e-10)):
                sol=solve_ivp(field_ode,(-2.,0.),np.eye(2).ravel(),method=method,
                    rtol=tolerance,atol=tolerance*1e-2)
                assert sol.success,sol.message
                transfer=sol.y[:,-1].reshape(2,2)
                results.append(dict(method=method,matrix=transfer.tolist(),nfev=sol.nfev,
                    determinant=float(np.linalg.det(transfer))))
            first=np.array(results[0]['matrix']);second=np.array(results[1]['matrix'])
            error=float(np.linalg.norm(first-second)/max(1,np.linalg.norm(second)))
            determinant_error=max(abs(r['determinant']-1) for r in results)
            assert error<1e-6, 'independent perturbation integrators disagree'
            assert determinant_error<1e-6,'canonical transfer not symplectic within tolerance'
            cases.append(dict(gamma=gs,comoving_k=str(kval),a_range=[str(mp.exp(-2)),'1'],
                state='(u, canonical_p / constant_initial_AH)',momentum_scale=scale,
                results=results,relative_integrator_difference=error,
                determinant_error=determinant_error))
    return dict(derivation_checks=facts['checks'],profile_log_disagreement=disagreement,
        profile_slices=rows,transfer_cases=cases,arithmetic_digits=mp.mp.dps,
        caveats=['Fixed reconstructed radiation-free history; no CMB or empirical inference.',
        'Slice sign checks use floating profiles, not interval ODE enclosures.',
        'Conditional algebra extends each sign condition to all k!=0, not to untested epochs.',
        'No nonlinear DOF, strong-coupling, caustic or full stability certificate.',
        'Transfer maps are arbitrary canonical-state evolution, not observed cosmological transfer functions.'],
        full_theory_status='OPEN')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--result-file',type=Path);args=p.parse_args()
    result=run()
    if args.result_file:args.result_file.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(slices=len(result['profile_slices']),
        sufficient_sign_slices=sum(r['all_nonzero_wavenumbers_sufficient_signs'] for r in result['profile_slices']),
        transfers=len(result['transfer_cases']),max_transfer_determinant_error=max(r['determinant_error'] for r in result['transfer_cases']),
        max_transfer_integrator_error=max(r['relative_integrator_difference'] for r in result['transfer_cases']),
        full_theory_status='OPEN'),indent=2))
