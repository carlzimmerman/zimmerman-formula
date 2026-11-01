import os,sys
sys.dont_write_bytecode=True
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[k]='1'
import json,math,time,resource
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp

def crossing(eta,chi,K,phase):
    h=eta*eta/chi;T=K/math.sqrt(h)
    def w2(t):
        B=math.exp(1.5*h*t);C=math.cos(t+phase);Q=B+eta*C
        return .25*math.exp(-2*h*t)-(2.25*h*h*B-eta*C)/Q
    def wprime(t):
        dt=.001
        return (math.sqrt(w2(t+dt))-math.sqrt(w2(t-dt)))/(2*dt)
    wi=math.sqrt(w2(-T));y0=1/math.sqrt(2*wi);v0=(-1j*wi-wprime(-T)/(2*wi))*y0
    def rhs(t,y):return [y[1],-w2(t)*y[0]]
    sol=solve_ivp(rhs,(-T,T),np.array([complex(y0),v0]),method='DOP853',rtol=2e-10,atol=2e-12,max_step=.8)
    assert sol.success
    y,v=sol.y[:,-1];wo=math.sqrt(w2(T));N=(abs(v)**2+wo*wo*abs(y)**2)/(2*wo)-.5
    pred=math.expm1(math.pi*chi/2)
    return dict(eta=eta,chi=chi,K=K,phase=phase,H_over_m=h,endpoints=[-T,T],occupation=float(N),asymptotic_narrow_N=pred,weak_N=math.pi*chi/2,relative_difference=float(N/pred-1),Wronskian=float((y*np.conj(v)-np.conj(y)*v).imag),steps=len(sol.t))

def main(path):
    start=time.monotonic();rows=[crossing(.001,c,K,0.) for c in (.02,.1) for K in (8,16,32,64)]
    rows += [crossing(.001,c,64,math.pi/2) for c in (.02,.1)]
    err=max(abs(r['Wronskian']-1) for r in rows);last=[r for r in rows if r['K']==64]
    phase_spreads=[abs(next(r['occupation'] for r in last if r['chi']==c and r['phase']==0)/next(r['occupation'] for r in last if r['chi']==c and r['phase']>0)-1) for c in (.02,.1)]
    checks=dict(Wronskian=err<2e-5,asymptotic_diagnostic=max(abs(r['relative_difference']) for r in last)<.15,phase_endpoint_control=max(phase_spreads)<.15)
    out=dict(claim_id='TP04_FLOQUET_ENDPOINT',checks=checks,Wronskian_error=err,phase_spreads=phase_spreads,cases=rows,runtime_seconds=time.monotonic()-start,peak_rss_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,non_claims=['No full native finite-amplitude background or backreaction','Finite harmonic mode crossing not irreversible cosmological depletion'])
    Path(path).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2));assert all(checks.values()),checks
if __name__=='__main__':main(sys.argv[1])
