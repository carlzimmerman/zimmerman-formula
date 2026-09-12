#!/usr/bin/env python3
"""All ten inverse-metric variations of the frozen gamma0 action.

The fixed reference qbar in P is never changed to physical Q. Recorded roots
and background values are inputs, not claimed on-shell gamma0 solutions.
"""
import argparse
from functools import lru_cache
import importlib.util
import json
from pathlib import Path
import numpy as np
import sympy as sy
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

HERE=Path(__file__).resolve().parent
REPAIR=HERE.parent
ROOT=REPAIR.parents[2]
CONSTITUTIVE=REPAIR/'nonlinear_evolution_2026/constitutive.py'
SAMPLES=REPAIR/'cosmological_bridge_2026/radiation_002/result.json'
L192=ROOT/'fable_independent_2026/L192_results.json'


@lru_cache(maxsize=1)
def derive():
    e=sy.symbols('epsilon',real=True)
    Q,b=sy.symbols('Q b',real=True)
    s0=sy.symbols('s0',positive=True)
    P,PX,V,W,WY=sy.symbols('P PX V W WY',real=True)
    eta=sy.diag(-1,1,1,1)
    tau=sy.Matrix([s0,0,0,0]);chi=sy.Matrix([Q,b,0,0])
    lag=P-V+s0*W
    expected=sy.diag(2*PX*Q**2-P+V,
                    lag+2*(PX-s0*WY)*b**2,lag,lag)
    expected[0,1]=expected[1,0]=2*PX*Q*b
    variations=[];calculated=sy.zeros(4)
    for i in range(4):
        for j in range(i,4):
            direction=sy.zeros(4)
            direction[i,j]=1;direction[j,i]=1
            inverse=eta+e*direction
            s=sy.sqrt(-(tau.T*inverse*tau)[0])
            X=-(chi.T*inverse*chi)[0]
            cross=(tau.T*inverse*chi)[0]
            Y=-X+cross**2/s**2
            # First jets exactly determine a first metric variation.
            L=P+PX*(X-(Q**2-b**2))-V+s*(W+WY*(Y-b**2))
            density=L/sy.sqrt(-inverse.det())
            mult=1 if i==j else 2
            component=sy.simplify(-sy.Rational(2,mult)*sy.diff(density,e).subs(e,0))
            calculated[i,j]=calculated[j,i]=component
            residual=sy.simplify(component-expected[i,j])
            variations.append(dict(component=f'{i}{j}',inverse_metric_multiplicity=mult,
                                   stress=str(component),residual=str(residual),passed=residual==0))
    mixed=eta*calculated
    lam=sy.symbols('lambda',real=True)
    characteristic=sy.factor((mixed-lam*sy.eye(4)).det())
    transverse_check=all(sy.simplify(mixed[i,j]-(lag if i==j else 0))==0
                         for i in [2,3] for j in range(4))
    N=2*PX*(1-2*Q**2*WY/W)-2*s0*WY
    shifted_tx=(mixed[:2,:2]-lag*sy.eye(2)).det()
    proxy_identity=sy.factor(shifted_tx+s0*b**2*W*N)
    checks=dict(all_ten_metric_variations=all(v['passed'] for v in variations),
                two_transverse_mixed_eigenvalues_L=transverse_check,
                transverse_proxy_zero_adds_third_L_eigenvalue=proxy_identity==0)
    if not all(checks.values()):raise AssertionError(checks)
    return dict(checks=checks,variations=variations,covariant_stress=str(calculated),
                mixed_characteristic=str(characteristic),
                proxy_identity='det(Tmixed_tx-L I) = -s0*b^2*W*[2 PX*(1-2 Q^2 WY/W)-2 s0 WY]')


class Coefficients:
    """Independently rebuild only the same frozen coefficient IVP."""
    def __init__(self,efolds):
        spec=importlib.util.spec_from_file_location('frozen_constitutive_for_stress',CONSTITUTIVE)
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        self.bg,self.flow,self.names,self.jets=module.functions()
        def rhs(loga,state):
            m,v,tau=state;a=np.exp(loga)
            if m<=0:raise ValueError('coefficient m domain lost')
            f=np.asarray(self.flow(a,m,v),dtype=float);H=f[0]/a
            return [f[1]/H,f[2]/H,1/H]
        self.history=solve_ivp(rhs,(0.,-efolds),[.1,.5,0.],method='DOP853',
                               rtol=2e-13,atol=2e-15,dense_output=True,max_step=.05)
        if not self.history.success:raise RuntimeError(self.history.message)

    def at(self,tau):
        tmin=float(self.history.y[2,-1])
        if not tmin<=tau<=0:raise ValueError('outside frozen coefficient history')
        loga=0. if tau==0 else brentq(lambda x:self.history.sol(x)[2]-tau,
                                    self.history.t[-1],0.,xtol=2e-13,rtol=2e-14)
        m,v,_=self.history.sol(loga)
        raw=np.asarray(self.bg(np.exp(loga),m,v),dtype=float)
        return dict(qbar=raw[0],U=raw[1],d=raw[2],Hbar=raw[3],ell=raw[4],raw=raw)


def action_jets(U,d,ell,qbar,Q,Y):
    reference=U-2*d*qbar*qbar
    margin=U-2*d*(Q*Q-Y)
    if min(U,d,ell,reference,margin)<=0 or Y<0:raise ValueError('constitutive domain')
    P=-U/2*np.log(margin/reference)
    PX=U*d/margin
    W=U+2*d*ell*(np.sqrt(1+Y/ell)-1)
    WY=d/np.sqrt(1+Y/ell)
    return dict(P=P,PX=PX,PXX=2*U*d*d/margin**2,V=U,W=W,WY=WY,
                WYY=-d/(2*ell)*(1+Y/ell)**-1.5,
                reference_margin=reference,physical_margin=margin)


def stress(j,Q,Y,s0):
    L=j['P']-j['V']+s0*j['W']
    T=np.diag([2*j['PX']*Q*Q-j['P']+j['V'],
               L+2*(j['PX']-s0*j['WY'])*Y,L,L])
    T[0,1]=T[1,0]=2*j['PX']*Q*np.sqrt(Y)
    return T,L


def explicit_metric_density(inverse,U,d,ell,qbar,Q,Y,s0):
    tau=np.array([s0,0,0,0]);chi=np.array([Q,np.sqrt(Y),0,0])
    ss=np.sqrt(-(tau@inverse@tau))
    X=-(chi@inverse@chi)
    YY=-X+(tau@inverse@chi)**2/ss**2
    P=-U/2*np.log((U-2*d*X)/(U-2*d*qbar*qbar))
    W=U+2*d*ell*(np.sqrt(1+YY/ell)-1)
    return (P-U+ss*W)/np.sqrt(-np.linalg.det(inverse))


def finite_difference_stress(U,d,ell,qbar,Q,Y,s0,step):
    eta=np.diag([-1.,1.,1.,1.]);out=np.zeros((4,4))
    for i in range(4):
        for j in range(i,4):
            h=np.zeros((4,4));h[i,j]=h[j,i]=step
            delta=(explicit_metric_density(eta+h,U,d,ell,qbar,Q,Y,s0)-
                   explicit_metric_density(eta-h,U,d,ell,qbar,Q,Y,s0))/(2*step)
            out[i,j]=out[j,i]=-2*delta/(1 if i==j else 2)
    return out


def numerical():
    archive=json.loads(SAMPLES.read_text());old=json.loads(L192.read_text())
    samples=archive['samples'][::23]+[archive['samples'][-1]]
    if len(samples)!=len(old):raise ValueError('source sample alignment')
    coeffs=Coefficients(archive['parameters']['coefficient_efolds'])
    rows=[];checks=[];fd=[]
    for sample,record in zip(samples,old):
        if abs(sample['a']-record['a'])>1e-12:raise ValueError('source epoch mismatch')
        if record['Yt']<=0:continue
        c=coeffs.at(float(sample['tau']));U,d,ell,qbar=(c[k] for k in ('U','d','ell','qbar'))
        actual_margin=(U-2*d*sample['q']**2)/U
        checks.append(abs(actual_margin-sample['relative_logarithm_margin'])<1e-10)
        for rootlabel,Y,pol in [('Yt',record['Yt'],'T'),('Yl',record['Yl'],'L')]:
            for which,Q in [('L192_qbar',qbar),('physical_q_unchanged_root',sample['q'])]:
                j=action_jets(U,d,ell,qbar,Q,Y)
                authoritative=dict(zip(coeffs.names,coeffs.jets(*c['raw'],Q*Q-Y,Y,0.)))
                errors={k:float(abs(j[k]-authoritative[a])/(1+abs(j[k])))
                        for k,a in [('P','P'),('PX','P_X'),('PXX','P_XX'),('V','V'),('W','W'),('WY','W_Y')]}
                checks.append(max(errors.values())<1e-12)
                s0=sample['clock_rate'];T,L=stress(j,Q,Y,s0)
                wc=j['WY'] if pol=='T' else j['WY']+2*Y*j['WYY']
                D=2*Q*Q*wc/j['W'];B=2*j['PX']+4*(Q*Q-Y)*j['PXX']
                proxy=(2*j['PX']*(1-D)-2*s0*wc)/(B*(1-D))
                if which=='L192_qbar':checks.append(abs(proxy)<1e-10)
                mixed=np.diag([-1,1,1,1])@T
                eig=np.linalg.eigvals(mixed)
                if np.max(np.abs(eig.imag))>1e-10:raise ValueError('unexpected complex stress eigenvalues')
                rows.append(dict(a=sample['a'],tau=sample['tau'],root=rootlabel,Y=Y,Q_source=which,
                    qbar=float(qbar),Q=float(Q),s0=float(s0),U=float(U),d=float(d),ell=float(ell),
                    reference_relative_margin=float(j['reference_margin']/U),
                    evaluated_relative_margin=float(j['physical_margin']/U),
                    P_over_U=float(j['P']/U),transverse_pressure=float(L),
                    transverse_pressure_over_U=float(L/U),transverse_pressure_over_clock_energy=float(L/T[0,0]),
                    covariant_T=T.tolist(),mixed_eigenvalues=eig.real.tolist(),
                    L192_proxy_cs2_at_this_unchanged_root=float(proxy),
                    authoritative_jet_relative_errors=errors,
                    nonzero_transverse_pressure=bool(abs(L/U)>1e-9)))
                if sample['a']==1. and rootlabel=='Yt':
                    for step in [1e-5,1e-6]:
                        numeric=finite_difference_stress(U,d,ell,qbar,Q,Y,s0,step)
                        error=float(np.max(np.abs(numeric-T))/(1+np.max(np.abs(T))))
                        checks.append(error<1e-7)
                        fd.append(dict(Q_source=which,metric_step=step,max_scaled_stress_error=error))
    if not all(checks):raise AssertionError('source/finite-difference consistency check failed')
    return dict(rows=rows,numerical_consistency_checks=len(checks),finite_difference_checks=fd,
                every_recorded_case_has_nonzero_transverse_pressure=all(r['nonzero_transverse_pressure'] for r in rows),
                background_archive_gamma=archive['parameters']['gamma'],action_evaluation_gamma=0.)


def run():
    exact=derive();numbers=numerical()
    verdict=('The frozen gamma0 stress has nonzero invariant transverse pressure at every tested L192 root, for both Q choices; cs2=0 does not imply exact dust.'
             if numbers['every_recorded_case_has_nonzero_transverse_pressure'] else
             'At least one tested case has unresolved or zero transverse pressure; the stress-only exact-dust exclusion is not established for every recorded case.')
    return dict(exact=exact,numerical=numbers,verdict=verdict,
                scope='Metric variation of P(X,tau)-V(tau)+s W(Y,tau), local constant gradients; gamma0; fixed inherited coefficients and recorded root values.',
                non_claims=['Not a full cubic/Einstein solution or an on-shell gamma0 cosmological branch',
                            'Not a principal-symbol or nonlinear-attractor proof',
                            'No coefficient, reference-state, root, or clock-rate refit',
                            'A nonzero transverse eigenvalue obstructs exact dust; clock-frame anisotropy alone is not frame invariant'])


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--result-file',required=True,type=Path);args=p.parse_args()
    result=run();args.result_file.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(exact_checks=result['exact']['checks'],numerical_checks=result['numerical']['numerical_consistency_checks'],
                          verdict=result['verdict'],first_two_rows=result['numerical']['rows'][:2]),indent=2))
