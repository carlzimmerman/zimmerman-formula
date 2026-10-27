"""Exploratory dissipative reference formation, not galaxy data or microphysics."""
import json
from pathlib import Path
import numpy as np

checks=[];rows=[];endpoints={}
def ck(name,p,value=None): checks.append(dict(name=name,passed=bool(p),value=value))
def evolve(Q,R,ext,N,dt,duration,baseline=None,freeze=False):
    x=np.arange(N)*2*np.pi/N
    src=np.sin(x)+.2*np.sin(2*x)
    k=np.fft.fftfreq(N)*N
    Aq=.01*k*k;Aq[0]=1.
    Ar=10*k*k
    def energy(q,r):
        qx=np.fft.ifft(1j*k*np.fft.fft(q)).real
        rx=np.fft.ifft(1j*k*np.fft.fft(r)).real
        return .5*q.mean()**2+np.mean(abs(q-r)**3/3+.005*qx*qx+5*rx*rx-src*q)-ext*q.mean()
    previous=energy(Q,R);max_up=0.
    sample_times=[0,.1,.5,1,2,5,10,20,40,80]
    sample_steps={round(t/dt):t for t in sample_times if t<=duration}
    history=[]
    for j in range(round(duration/dt)+1):
        if j in sample_steps:
            shape=0 if baseline is None else float(np.linalg.norm(Q-Q.mean()-baseline)/np.linalg.norm(baseline))
            history.append(dict(t=sample_steps[j],Q_mean=float(Q.mean()),R_mean=float(R.mean()),relative_internal_error=shape))
        if j==round(duration/dt): break
        nl=(Q-R)*abs(Q-R)
        Q=np.fft.ifft(np.fft.fft(Q+dt*(src+ext-nl))/(1+dt*Aq)).real
        if not freeze: R=np.fft.ifft(np.fft.fft(R+dt*nl)/(1+dt*Ar)).real
        current=energy(Q,R)
        max_up=max(max_up,current-previous);previous=current
    return Q,R,history,max_up

for N,dt in [(64,.002),(128,.001)]:
    Q,R,_,inc=evolve(np.zeros(N),np.zeros(N),0,N,dt,80)
    ck('baseline energy '+str(N),inc<1e-10,inc)
    base=Q-Q.mean()
    for ext in [0.,1.,3.]:
        q,r,h,up=evolve(Q.copy(),R.copy(),ext,N,dt,80,base)
        err=h[-1]['relative_internal_error'];meanerr=max(abs(q.mean()-ext),abs(r.mean()-ext))
        ck('adapted shape '+str((N,ext)),err<1e-5,err)
        ck('adapted means '+str((N,ext)),meanerr<1e-5,float(meanerr))
        ck('energy descent '+str((N,ext)),up<1e-10,up)
        rows.append(dict(N=N,dt=dt,external_step=ext,frozen_reference=False,history=h))
        endpoints[N,ext]=q-q.mean()
    q,r,h,up=evolve(Q.copy(),R.copy(),3.,N,dt,80,base,freeze=True)
    ck('frozen reference retains EFE '+str(N),h[-1]['relative_internal_error']>.05,h[-1]['relative_internal_error'])
    rows.append(dict(N=N,dt=dt,external_step=3.,frozen_reference=True,history=h))
for ext in [0.,1.,3.]:
    low=endpoints[64,ext];high=endpoints[128,ext][::2]
    err=float(np.linalg.norm(low-high)/np.linalg.norm(high))
    ck('grid and time refinement '+str(ext),err<1e-4,err)
result=dict(all_pass=all(c['passed'] for c in checks),checks=checks,runs=rows,
 scope='Overdamped periodic 1D experiment; adaptation is demonstrated only for the specified source, parameters and duration.')
out=Path(__file__).parent/'adaptation_run';out.mkdir(exist_ok=True)
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
raise SystemExit(0 if result['all_pass'] else 1)
