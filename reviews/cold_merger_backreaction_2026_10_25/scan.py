import argparse,json,math
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args();out=Path(a.output);out.mkdir(parents=True,exist_ok=True)
base=json.load(open('reviews/cold_merger_backreaction_2026_10_25/run/result.json'));P=base['summary']['uncoupled_period_over_T'];turn=math.sqrt(24);B=1e-4
orbit=solve_ivp(lambda s,z:[z[1],-z[0]/(1+z[0]*z[0])**1.5],[0,P/2],[turn,0],rtol=2e-12,atol=1e-14,method='DOP853',dense_output=True)
assert abs(orbit.y[0,-1]+turn)<1e-8 and abs(orbit.y[1,-1])<1e-8
rows=[]
for T in np.geomspace(.01,2,161):
 def fun(s,z):
  x=orbit.sol(s)[0];w2=8+4*(1+x*x)**(-2.5)
  return (np.array([[0,T],[-T*w2,0]])@z.reshape(2,2)).ravel()
 sol=solve_ivp(fun,[0,P/2],np.eye(2).ravel(),rtol=2e-10,atol=1e-12,method='DOP853');assert sol.success
 M=sol.y[:,-1].reshape(2,2);assert abs(np.linalg.det(M)-1)<1e-7
 rows.append(dict(T=float(T),multiplier=float(max(abs(np.linalg.eigvals(M)))),det=float(np.linalg.det(M))))
best=max(rows,key=lambda r:r['multiplier']);T=best['T'];mass=B*T*T

def run(tol):
 def fun(t,z):
  q,p,x,v=z;s=math.sin(q/2)**2;f=1-s;xx=1/math.sqrt(f);am1=s/(math.sqrt(f)*(1+math.sqrt(f)));d=40+16*(1+x*x)**(-2.5);dp=-80*x*(1+x*x)**(-3.5)
  fq=(40*xx**3-48*xx+d)*.5*xx*math.tan(q/2)
  return [p,-fq,v,(-B*x/(1+x*x)**1.5-dp*am1)/mass]
 ts=np.linspace(0,100*P*T,40001);sol=solve_ivp(fun,[0,ts[-1]],[1e-6,0,turn,0],t_eval=ts,rtol=tol,atol=tol*1e-3,method='DOP853');assert sol.success
 q,p,x,v=sol.y;s=np.sin(q/2)**2;f=1-s;d=40+16*(1+x*x)**(-2.5)
 ef=.5*p*p+(-4*s+14*s*s)/f**2+d*s/(np.sqrt(f)*(1+np.sqrt(f)));eo=.5*mass*v*v-B/np.sqrt(1+x*x);h=ef+eo;err=float(max(abs(h-h[0])))
 assert err<2e-10 and max(ef)<h[0]+B+2e-10
 return dict(final_energy=float(ef[-1]),peak_energy=float(max(ef)),initial_energy=float(ef[0]),orbital_loss=float(eo[0]-eo[-1]),energy_error=err,budget=float(h[0]+B))
r1=run(2e-10);r2=run(2e-12)
# Chaotic phase divergence is possible; do not assert pointwise late-time convergence.
result=dict(scan=rows,selected=best,base=r1,tight=r2,scope='Optimized finite resonance control, not a derived cluster encounter')
(out/'result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='scan'},indent=2))
