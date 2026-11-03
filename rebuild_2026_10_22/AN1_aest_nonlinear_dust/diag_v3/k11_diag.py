"""Post-hoc, after K11's miss; rescues nothing. Is the P1 deviation from r_1 k / r_k = 1 true differential focus or a runaway?
Compares each of the first shells on the P1 floor row with its own exact dust-shell ODE, independent of Run, until the central cell reaches 1e-3."""
import sys,os,json,numpy as np
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
import an1_v3 as v, an1
from scipy.integrate import solve_ivp
G=an1.G
for key in ('1e12','1e15'):
  for N in (300,1200):
    R=v.build(key,1.24e8,'canonical',N=N); bg=R.bg; L=bg.OL*bg.H0**2; ai=1/21.; t0=R.t
    qe=R.dq*np.arange(N+1); sol={}
    for k in (1,2,3,5):
        M=4*np.pi/3*bg.rm0*qe[k]**3
        sol[k]=solve_ivp(lambda t,y:[y[1],-G*M/y[0]**2+L*y[0]],(t0,3*R.t0),[R.r[k],R.v[k]],rtol=1e-11,atol=1e-14*R.r[k],method='DOP853',dense_output=True,events=(lambda t,y:y[0]-1e-5*R.r[k]))
    R.forces(); mx={k:0. for k in sol}; dev=0.; 
    while True:
        R.step(3*R.t0)
        if getattr(R,'crossed',False): break
        for k in sol:
            te=sol[k].t[-1]
            if R.t<te: mx[k]=max(mx[k],abs(R.r[k]/sol[k].sol(R.t)[0]-1))
        for k in (2,3,5): dev=max(dev,abs(R.r[1]*k/R.r[k]-1))
        if R.r[1]/(R.aval()*R.dq)<1e-3: break
    ex={k:float(sol[k].sol(R.t)[0]) if R.t<sol[k].t[-1] else None for k in sol}
    pred=max([abs(ex[1]*k/ex[k]-1) for k in (2,3,5) if ex[1] and ex[k]] or [float("nan")])
    print(json.dumps(dict(key=key,N=N,K11_dev_run=dev,K11_dev_exact_dust_at_end=pred,max_rel_to_own_shell=mx,steps=R.nstep)),flush=True)
