#!/usr/bin/env python3
"""Free-clock memory and fixed-source response; no fabricated assembly history."""
import json
import math
from pathlib import Path
import sys
import numpy as np
from scipy.integrate import solve_ivp
from scipy.special import expit
import sympy as s

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'spherical_baryon_bridge'))
from source import derive, load


def run():
    print('memory: deriving sourced action',file=sys.stderr,flush=True)
    facts,c=derive()
    order=('a','H','q','M','gamma','k','A','U','B0','qd')
    C,z,u,ud=[c[x] for x in ('C','z','u','ud')]
    parts=[c['pre_zeta_kinetic'],c['velocity_mixing'],c['field_mixing'],c['constraint'],
           c['raw_mixed'],c['raw_potential'],c['fz']/C,-c['Qmix']/2,-c['nu']/2,
           *[s.diff(c['T'],x) for x in (z,u,ud,C)],c['Qmix'],c['phi_z'],c['phi_u']]
    fn=s.lambdify([c[x] for x in order],parts,'numpy',cse=True)
    print('memory: deriving background profile',file=sys.stderr,flush=True)
    _,flow=load('memory_profile',HERE.parent/'nonlinear_transport/stationary.py').symbolic()
    def bg_rhs(x,y):return flow(math.exp(y[0]),expit(y[1]),1/(1+7*math.exp(3*x)))
    profiles=[]
    for method,tol in [('DOP853',2e-13),('Radau',2e-12)]:
        sol=solve_ivp(bg_rhs,(0,-1.01),[math.log(.1),0.],method=method,rtol=tol,atol=tol/10,dense_output=True)
        if not sol.success:raise AssertionError(sol.message)
        profiles.append(sol)
    kval=np.array([.1,1.,10.,100.]);nm=len(kval);gamma=1e-6
    def algebra(x,lm,lv):
        a=np.exp(x);m=np.exp(lm);v=1/(1+np.exp(-lv))
        q=1/(1+m);A=.1/a**3;U=m*q*A;H=np.sqrt((.7+A)/3)
        B0=A/q*(1+2/m);qd=-3*A*H*v/B0-q*U/(2*H)
        raw=[np.broadcast_to(np.asarray(z),kval.shape) for z in fn(a,H,q,1.,gamma,kval,A,U,B0,qd)]
        A0,J,E,D,Br,Cr,fz,fv0,fu0,Tz,Tu,Tv,TC,Qmix,pz,pu=raw
        return dict(H=H,Af=A0-J*J/D,Bf=Br-J*E/D,Cf=Cr-E*E/D,J=J,E=E,D=D,
                    fv=fv0-J*fz/D,fu=fu0-E*fz/D,fz=fz,Tz=Tz,Tu=Tu,Tv=Tv,TC=TC,Qmix=Qmix,pz=pz,pu=pu)
    def coeff(x,back):return algebra(x,*back.sol(x))
    pi=coeff(-1,profiles[0]);scale=pi['Af']*pi['H']
    initial=np.zeros((nm,2,3));initial[:,:,:2]=np.eye(2)
    initial[:,1,2]=pi['fv']/scale # C=1, physical u=udot=0, not p=0
    def generator(p):
        F=np.empty((nm,2,2),dtype=np.result_type(p['Af']))
        F[:,0,0]=-p['Bf']/(p['Af']*p['H']);F[:,0,1]=scale/(p['Af']*p['H'])
        F[:,1,0]=(p['Cf']-p['Bf']**2/p['Af'])/(scale*p['H']);F[:,1,1]=-F[:,0,0]
        force=np.stack([-p['fv']/(p['Af']*p['H']),
                        (p['fu']-p['Bf']*p['fv']/p['Af'])/(scale*p['H'])],axis=1)
        return F,force
    def rhs(x,flat,back):
        p=coeff(x,back)
        if np.any(p['Af']<=0) or np.any(p['D']>=0):raise ValueError('outside regular reduced branch')
        F,b=generator(p);rate=np.einsum('nij,njk->nik',F,flat.reshape(nm,2,3));rate[:,:,2]+=b
        return rate.ravel()
    def metric(primitives,state,C):
        p=algebra(*primitives);u=state[:,0];ps=state[:,1]
        vel=(scale*ps-p['Bf']*u-C*p['fv'])/p['Af']
        z=-(p['J']*vel+p['E']*u+C*p['fz'])/p['D']
        T=p['Tz']*z+p['Tu']*u+p['Tv']*vel+C*p['TC']
        return p,u,z,T
    runs=[]
    for method,tol,back in zip(('DOP853','Radau'),(1e-11,2e-11),profiles):
        print('memory: integrating '+method,file=sys.stderr,flush=True)
        sol=solve_ivp(lambda x,y:rhs(x,y,back),(-1.,0.),initial.ravel(),method=method,
                      rtol=tol,atol=tol*1e-3,dense_output=True)
        if not sol.success:raise AssertionError(sol.message)
        det_errors=[];samples=[]
        for x in np.linspace(-1.,0.,51):
            mat=sol.sol(x).reshape(nm,2,3)[:,:,:2]
            det_errors.append(float(np.max(abs(np.linalg.det(mat)-np.linalg.det(initial[:,:,:2])))))
        for x in (-.7,-.35,0.):
            primitives=np.r_[x,back.sol(x)];allstate=sol.sol(x).reshape(nm,2,3)
            rates=rhs(x,allstate.ravel(),back).reshape(nm,2,3)
            values=[]
            for col,source in ((0,0.),(1,0.),(2,1.)):
                state=allstate[:,:,col];p,u,z,T=metric(primitives,state,source)
                direction=p['H']*np.r_[1.,bg_rhs(x,back.sol(x))]
                phis=[]
                for step in (1e-18,1e-23):
                    Td=np.imag(metric(primitives+1j*step*direction,
                                      state+1j*step*rates[:,:,col]*p['H'],source)[3])/step
                    phis.append(p['pz']*z+p['pu']*u+Td)
                psi=p['H']*(p['Qmix']*u-T)
                values.append(dict(Phi=phis[-1].tolist(),Psi=psi.tolist(),
                    derivative_step_error=float(np.max(abs(phis[0]-phis[1]))),
                    slip_abs=float(np.max(abs(phis[-1]-psi)))))
            samples.append(dict(ln_a=float(x),columns=values))
        runs.append(dict(method=method,nfev=sol.nfev,max_determinant_error=max(det_errors),
                         final_transfer=sol.sol(0).reshape(nm,2,3).tolist(),samples=samples))
    a=np.array(runs[0]['final_transfer']);b=np.array(runs[1]['final_transfer'])
    comparison=float(np.max(abs(a-b)/np.maximum(1.,abs(b))))
    metrics_a=np.array([[v['Phi'] for v in row['columns']] for row in runs[0]['samples']])
    metrics_b=np.array([[v['Phi'] for v in row['columns']] for row in runs[1]['samples']])
    metric_error=float(np.max(abs(metrics_a-metrics_b)/np.maximum(1.,abs(metrics_b))))
    observable=[]
    for i,k in enumerate(kval):
        O=metrics_a[-2:,:2,i];norms=np.linalg.norm(O,axis=1)
        normalized=O/np.maximum(norms[:,None],1e-30)
        sv=np.linalg.svd(normalized,compute_uv=False)
        observable.append(dict(k=float(k),two_time_metric_map=O.tolist(),row_normalized_singular_values=sv.tolist(),
            computed_numerical_rank=int(np.linalg.matrix_rank(normalized)),
            final_memory_Phi=metrics_a[-1,:2,i].tolist(),final_fixed_source_Phi=float(metrics_a[-1,2,i])))
    checks=dict(independent_state_solvers=comparison<1e-7,independent_metric_solvers=metric_error<1e-7,
        determinant_preservation=max(r['max_determinant_error'] for r in runs)<1e-7,
        independent_no_slip=max(v['slip_abs'] for r in runs for row in r['samples'] for v in row['columns'])<1e-7,
        derivative_refinement=max(v['derivative_step_error'] for r in runs for row in r['samples'] for v in row['columns'])<1e-8)
    if not all(checks.values()):raise AssertionError(checks)
    return dict(checks=checks,source_variation_checks=facts['checks'],state_comparison=comparison,
                metric_comparison=metric_error,modes=kval.tolist(),runs=runs,observability=observable,
                clock_initial_basis='unit u and unit p/(Af_initial H_initial); response derivatives, not finite perturbations',
                source='C=1 conserved-response kernel; physical initial u=udot=0',
                full_theory='OPEN',memory_prediction='initial amplitudes and assembly transfer not fixed',
                non_claims=['no arbitrary time-dependent baryon source','no nonlinear galaxies or primordial prescription',
                            'k=0 excluded','no empirical result or measured Newton constant'])


if __name__=='__main__':print(json.dumps(run(),indent=2))
