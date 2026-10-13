"""Frozen-metric linear chi transport on the published actual exterior."""
import argparse,json
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp,simpson

parser=argparse.ArgumentParser();parser.add_argument('--output-dir',required=True)
OUT=Path(parser.parse_args().output_dir)
source=json.loads((Path(__file__).parent/'source_snapshot/self_gravity_results.json').read_text())
case=next(c for c in source['cases'] if c['b']==1000)
Y=case['Y'];C=Y**2/2000;BR=1-C
labels=np.linspace(1.001,1.005,257)
chi0=np.sin(np.pi*(labels-1.001)/.004)**2
times=np.array([0,.5,1,2,3])
def B(x):return 1-C*(2/(3*x)+x*x/3)
def fields(x,sign):
    H=np.sqrt((x+2)/(3*x));Hp=-1/(3*x*x*H)
    bx=B(x);bp=C*(2/(3*x*x)-2*x/3)
    V=sign*bx/BR*(x-1)*H
    Vp=sign*(bp/BR*(x-1)*H+bx/BR*(H+(x-1)*Hp))
    reaction=sign*bx/BR*(2*(x-1)*H/x+H+(x-1)*Hp)
    return V,Vp,reaction
weight0=labels**2/B(labels)
charge0=float(simpson(weight0*chi0,x=labels))
records=[];arrays={}
for sign in [-1,1]:
    def rhs(t,z):
        x,j,n=z.reshape(3,-1)
        V,Vp,reaction=fields(x,sign)
        return np.concatenate([V,Vp,-reaction])
    initial=np.concatenate([labels,np.zeros_like(labels),np.zeros_like(labels)])
    stages=[]
    for tight in [False,True]:
        sol=solve_ivp(rhs,(0,3),initial,t_eval=times,method='DOP853',rtol=2e-13 if tight else 2e-11,atol=2e-15 if tight else 2e-13)
        assert sol.success,sol.message
        stages.append(sol.y.reshape(3,len(labels),len(times)))
    refined=stages[-1];difference=float(np.max(np.abs(stages[0]-refined)))
    assert difference<1e-7
    x,logj,logn=refined
    assert x.min()>1 and x.max()<1.11 and B(x).min()>.9
    J=np.exp(logj);chi=chi0[:,None]*np.exp(logn)
    weight=x*x/B(x)
    expected=chi0[:,None]*weight0[:,None]/weight/J
    identity_error=float(np.max(abs(chi-expected))/(1+np.max(abs(chi))))
    assert identity_error<1e-8
    entries=[]
    for i,time in enumerate(times):
        charge=float(simpson(weight[:,i]*chi[:,i]*J[:,i],x=labels))
        mutation_charge=float(simpson(weight[:,i]*chi0*J[:,i],x=labels))
        err=abs(charge-charge0)/charge0
        assert err<1e-8
        peak=float(chi[:,i].max()/chi0.max())
        leading=float(np.exp(-sign*time))
        entries.append({'tau':float(time),'peak_amplification':peak,'near_edge_prediction':leading,'relative_peak_deviation':abs(peak/leading-1),'charge':charge,'relative_charge_error':err,'omit_expansion_charge':mutation_charge,'omit_expansion_relative_error':abs(mutation_charge-charge0)/charge0})
    assert entries[-1]['relative_peak_deviation']<.15
    assert entries[-1]['omit_expansion_relative_error']>.001
    arrays['s'+str(sign)]=np.stack([x,chi,J,weight],axis=0)
    records.append({'sign':sign,'meaning':'inward' if sign<0 else 'outward','max_refinement_difference':difference,'identity_relative_scale_error':identity_error,'min_x':float(x.min()),'max_x':float(x.max()),'min_B':float(B(x).min()),'samples':entries})
np.savez_compressed(OUT/'profiles.npz',labels=labels,times=times,**arrays)
payload={'all_passed':True,'b':1000,'Y':Y,'C':C,'BR':BR,'charge0':charge0,'cases':records,'coordinates':'x=r/R,tau=t sqrt(8piG rho0)','array_order':['x','chi_normalized_shape','Jacobian','x_squared_over_B'],'scope':'fixed-metric linear test packets; arbitrary overall infinitesimal amplitude; not constraint-satisfying Einstein perturbations','nonclaims':['No full coupled or nonlinear instability certificate','No UV or horizon theorem']}
(OUT/'results.json').write_text(json.dumps(payload,indent=2)+'\n')
print(json.dumps({'all_passed':True,'cases':[{'sign':c['sign'],'tau3':c['samples'][-1],'max_refinement_difference':c['max_refinement_difference']} for c in records]}))
