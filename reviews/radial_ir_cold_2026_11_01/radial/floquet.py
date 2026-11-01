import os,sys
sys.dont_write_bytecode=True
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[k]='1'
import json,math,time,resource
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp,quad
from scipy.optimize import brentq

def monodromy(eta,kappa,rtol=2e-13,atol=2e-14):
    def rhs(t,y):
        w=kappa*kappa+eta*math.cos(t)/(1+eta*math.cos(t));return [y[1],-w*y[0],y[3],-w*y[2]]
    sol=solve_ivp(rhs,(0,2*math.pi),[1,0,0,1],method='DOP853',rtol=rtol,atol=atol)
    assert sol.success
    y=sol.y[:,-1];M=np.array([[y[0],y[2]],[y[1],y[3]]]);vals=np.linalg.eigvals(M);mu=math.log(max(abs(vals)))/(2*math.pi)
    return max(0,float(mu)),float(np.linalg.det(M)),M

def expanding(eta0,chi,phase):
    h=eta0*eta0/chi;T=8*eta0/h
    def w2(t,eta=eta0):
        base=math.exp(1.5*h*t);cs=math.cos(t+phase);Q=base+eta*cs;Qdd=2.25*h*h*base-eta*cs
        return .25*math.exp(-2*h*t)-Qdd/Q
    wi=math.sqrt(w2(-T));dt=1e-3;wip=(math.sqrt(w2(-T+dt))-math.sqrt(w2(-T-dt)))/(2*dt);y0=1/math.sqrt(2*wi);v0=(-1j*wi-wip/(2*wi))*y0
    def rhs(t,y):return [y[1],-w2(t)*y[0]]
    sol=solve_ivp(rhs,(-T,T),np.array([complex(y0),v0]),method='DOP853',rtol=2e-10,atol=2e-12,max_step=.8)
    assert sol.success
    y,v=sol.y[:,-1];wo=math.sqrt(w2(T));N=float((abs(v)**2+wo*wo*abs(y)**2)/(2*wo)-.5);Wr=float((y*np.conj(v)-np.conj(y)*v).imag)
    # Baseline expansion-only mode uses the identical canonical convention.
    def rhs0(t,y):return [y[1],-w2(t,0)*y[0]]
    w0=math.sqrt(w2(-T,0));wp0=(math.sqrt(w2(-T+dt,0))-math.sqrt(w2(-T-dt,0)))/(2*dt);u0=1/math.sqrt(2*w0);v00=(-1j*w0-wp0/(2*w0))*u0
    ss=solve_ivp(rhs0,(-T,T),np.array([complex(u0),v00]),method='DOP853',rtol=2e-10,atol=2e-12,max_step=.8);assert ss.success
    yy,vv=ss.y[:,-1];ww=math.sqrt(w2(T,0));N0=float((abs(vv)**2+ww*ww*abs(yy)**2)/(2*ww)-.5)
    eta=lambda t:eta0*math.exp(-1.5*h*t);det=lambda t:math.exp(-2*h*t)-1
    left=brentq(lambda t:det(t)-2*eta(t),-T,0);right=brentq(lambda t:det(t)+2*eta(t),0,T)
    grow=lambda t:.25*math.sqrt(max(0,4*eta(t)**2-det(t)**2));I=quad(grow,left,right,epsabs=1e-11)[0];pred=math.pi*chi/4
    return dict(eta0=eta0,chi=chi,H_over_m=h,pump_phase=phase,in_out_tau=[-T,T],occupation=N,expansion_only_occupation=N0,Wronskian=Wr,I_band=I,I_narrow=pred,I_relative_difference=abs(I/pred-1),weak_crossing_N=2*pred,strong_exponent_diagnostic=math.expm1(2*pred),steps=len(sol.t))

def main(path):
    start=time.monotonic();rows=[];controls={};interior=[];outside=[];dets=[]
    for eta in (1e-5,1e-4,1e-3,1e-2):
        for x in (-1.5,-.75,0,.75,1.5):
            k=.5*(1+eta*x);mu,det,M=monodromy(eta,k);pred=eta*math.sqrt(max(0,1-x*x))/2;rows.append(dict(eta=eta,detuning=x,k_over_m=k,Floquet_over_m=mu,narrow_prediction=pred,det=det));dets.append(abs(det-1))
            if abs(x)<1:interior.append(abs(mu/pred-1))
            else:outside.append(mu)
        mu,det,M=monodromy(eta,0);phase=np.array([1+eta,0.]);controls[f'zero_k_phase_solution_eta{eta}']=float(np.max(abs(M@phase-phase)))
    a=monodromy(.001,.5)[0];b=monodromy(.001,.5,5e-14,5e-15)[0];controls['Floquet_tolerance_relative_repeat']=abs(a/b-1)
    exp=[expanding(.005,c,p) for c in (.1,1.,3.) for p in (0.,math.pi/2)]
    controls.update(monodromy_det_error=max(dets),narrow_interior_relative_error=max(interior),outside_growth=max(outside),expansion_Wronskian_error=max(abs(r['Wronskian']-1) for r in exp),crossing_I_relative_error=max(r['I_relative_difference'] for r in exp),expansion_only_occupation=max(abs(r['expansion_only_occupation']) for r in exp))
    checks={k:(v<1e-9 if k.startswith('zero_k') or k=='monodromy_det_error' else v<1e-5 if k=='Floquet_tolerance_relative_repeat' else v<.05 if k in ('narrow_interior_relative_error','crossing_I_relative_error') else v<1e-8 if k=='outside_growth' else v<2e-5 if k in ('expansion_Wronskian_error','expansion_only_occupation') else False) for k,v in controls.items()}
    out=dict(claim_id='TP04_PHASE_FLOQUET',checks=checks,controls=controls,stationary=rows,expanding=exp,runtime_seconds=time.monotonic()-start,peak_rss_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,non_claims=['Harmonic smallamplitude pump; finite native anharmonic background not fully evolved','Finite inout adiabatic occupation is not a selected cosmology or irreversible halo depletion rate','No model mu,density,velocitydispersion or halo size selected'])
    Path(path).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2));assert all(checks.values()),checks
if __name__=='__main__':main(sys.argv[1])
