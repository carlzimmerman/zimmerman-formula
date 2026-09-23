"""Independent 50-digit fixed-step checks of two phase-space witnesses."""
from pathlib import Path
import json
import sympy as s
import mpmath as mp
import numpy as np
from scipy.integrate import solve_ivp

here=Path(__file__).resolve().parent
mp.mp.dps=50
rows=[]
for filename,mode,a_text,k_text,dn_text in (
    ('canonical.json','response_n4','.1','.001','.5'),
    ('lorentz_canonical.json','constant','.1','.1','.1'),
):
    d=json.loads((here/filename).read_text())
    variables=[s.sympify(z) for z in d['variables']]
    mf=s.lambdify(variables,s.sympify(d['matrix_N']),'mpmath',cse=True)
    of=s.lambdify(variables,s.sympify(d['observables']),'mpmath',cse=True)
    ep=mp.mpf('1e-9');b=mp.mpf(1)/39998 if mode=='constant' else mp.mpf('.03')
    gc=1+3*b/2;j0=-mp.mpf('1.86')/(1-ep);lam=3*gc-(ep-1)*j0/2
    hub=mp.mpf(299792458)/67400;k=mp.mpf(k_text)*hub
    def matrices(n):
        a=mp.exp(n);q=1-3*ep*n;j=j0/a**3
        h=mp.sqrt(((ep-q)*j/2+lam)/(3*gc));hd=q*j/(4*gc)
        if mode=='constant':alpha=mp.mpf(1)/40000;ad=0
        else:
            v=mp.mpf('1e-7')*a**-4;alpha=mp.mpf('.5')*v/(mp.mpf('.5')+v)
            ad=-4*h*alpha*(1-2*alpha)
        args=(a,h,q,j,ep,mp.mpf('4e-6')/hub,k,alpha,ad,b)
        sc=mp.diag([1,1,q/h,1]);iv=mp.diag([1,1,h/q,1])
        B=iv*mp.matrix(mf(*args))*sc;B[2,2]+=hd/h**2+3*ep/q
        O=mp.matrix(of(*args))*sc
        return B,O
    n0=mp.log(mp.mpf(a_text));dn=mp.mpf(dn_text);n1=n0+dn
    initial=mp.matrix([1,0,0,0])
    endpoints=[]
    for count in (2000,4000):
        step=dn/count;n=n0;y=initial.copy()
        for unused in range(count):
            A0,_=matrices(n);Ah,_=matrices(n+step/2);A1,_=matrices(n+step)
            k1=A0*y;k2=Ah*(y+step*k1/2);k3=Ah*(y+step*k2/2);k4=A1*(y+step*k3)
            y+=step*(k1+2*k2+2*k3+k4)/6;n+=step
        endpoints.append(y)
    reference=endpoints[-1]
    step_error=float(mp.norm(endpoints[0]-reference)/mp.norm(reference))
    assert step_error<2e-6,step_error
    # Adaptive solver uses independently chosen steps, with coefficients evaluated
    # at high precision and then rounded to float64 before integration.
    sol=solve_ivp(lambda n,y:np.asarray(matrices(mp.mpf(n))[0].tolist(),float)@y,
                  (float(n0),float(n1)),np.array([1.,0.,0.,0.]),method='DOP853',
                  rtol=1e-11,atol=1e-14,max_step=float(dn)/100)
    assert sol.success
    ref=np.array([float(z) for z in reference]);adaptive_error=float(np.linalg.norm(sol.y[:,-1]-ref)/np.linalg.norm(ref))
    assert adaptive_error<2e-6,adaptive_error
    initial_obs=matrices(n0)[1]*initial;final_obs=matrices(n1)[1]*reference
    row={'action':filename,'response':mode,'a_start':a_text,'k_Mpc_inv':k_text,'delta_N':dn_text,
         'state':['Phi','Phi_N','H*P/Q','canonical_charge_contrast'],'initial':[1,0,0,0],
         'final':[float(z) for z in reference],'initial_observables':[float(z) for z in initial_obs],
         'final_observables':[float(z) for z in final_obs],
         'Bardeen_gain':float(final_obs[4]/initial_obs[4]),
         'step_doubling_relative_error':step_error,'adaptive_relative_error':adaptive_error,
         'decimal_precision':50,'steps':[2000,4000]}
    rows.append(row);print(json.dumps(row),flush=True)
(here/'phase_precision_results.json').write_text(json.dumps(rows,indent=2)+'\n')
