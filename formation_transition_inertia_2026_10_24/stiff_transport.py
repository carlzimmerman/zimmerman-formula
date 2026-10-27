"""Implicit continuation with accepted-segment evidence."""
import argparse,json,time
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
from transport import Transport,checks

ap=argparse.ArgumentParser();ap.add_argument('--output',required=True)
ap.add_argument('--n',type=int,default=6);ap.add_argument('--nq',type=int,default=256)
ap.add_argument('--duration',type=float,default=12);ap.add_argument('--rtol',type=float,default=2e-7)
ap.add_argument('--alpha',type=float,default=1);ap.add_argument('--iota',type=float,default=.1)
args=ap.parse_args();path=Path(args.output)
m=Transport(1e8,1,n=args.n,nq=args.nq,f=.95,alpha=args.alpha,iota=args.iota,scale=30,nu0=1)
y=m.initial();t=0.;hist=[m.observe(0,y)];start=time.monotonic()
def boundary(t,y):return min(min(y[:len(m.m)])/m.rmin-2,m.rmax/(2*max(y[:len(m.m)]))-1)
boundary.terminal=True;boundary.direction=-1
out=dict(parameters=vars(args),checks=checks(),status='running',history=hist)
path.write_text(json.dumps(out,indent=2)+'\n')
for stop in np.arange(.5,args.duration+.01,.5)*m.tdyn:
    sol=solve_ivp(m.rhs,(t,stop),y,method='Radau',rtol=args.rtol,atol=args.rtol*.01,
                  max_step=.1*m.tdyn,events=boundary,dense_output=True)
    for tt in np.linspace(t,sol.t[-1],11)[1:]:hist.append(m.observe(tt,sol.sol(tt)))
    t=float(sol.t[-1]);y=sol.y[:,-1]
    out.update(status='completed' if stop>=args.duration*m.tdyn-1e-9 else 'partial',
               last_t=t/m.tdyn,history=hist,elapsed=time.monotonic()-start)
    if sol.status==1:out['status']='radial domain reached'
    if not sol.success:out['status']='failed';out['reason']=sol.message
    norm=max(abs(hist[0]['energy']),abs(hist[0]['gravity']))
    out['max_energy_error']=max(abs(h['energy']-hist[0]['energy']) for h in hist)/norm
    out['max_J_error']=max(abs(h['J']-m.J) for h in hist)/abs(m.J)
    out['peak_q']=max(h['q'] for h in hist);out['final']=hist[-1]
    path.write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(out['status'],out['last_t'],hist[-1]['q'],hist[-1]['minimum_baryon_radius'],flush=True)
    if sol.status!=0:break
