"""Independent small exact-solution and Hamiltonian-gradient controls."""
import json,sys,subprocess
from pathlib import Path
import numpy as np
from scipy.special import ellipj,hankel1

here=Path(__file__).parent; out=Path(sys.argv[1]);out.mkdir(exist_ok=True)
def run(name,q,v,dt,end,b,mp,mx,c,quartic=1.):
 n=q.shape[1]; path=out/(name+'.bin')
 with path.open('wb') as f:
  np.array([n,n,dt,end,b,mp,mx,c,quartic],dtype='<f8').tofile(f)
  q.tofile(f);v.tofile(f)
 subprocess.run([str(here/'coupled_field_lattice'),str(path),str(out/(name+'.csv')),str(out/(name+'_final.bin'))],check=True)
 return np.fromfile(out/(name+'_final.bin')).reshape(2,*q.shape)
errors=[]
for dt in [.01,.005]:
 q=np.zeros((4,4,4,4));v=q.copy();q[0]=1;q[2]=.5;v[2]=.1
 result=run('exact_'+str(dt),q,v,dt,10,0,0,0,0)
 sn,cn,dn,_=ellipj(10,.5)
 expectedq=np.array([cn,0,1.5,0]);expectedv=np.array([-sn*dn,0,.1,0])
 err=max(np.max(np.abs(result[0,:,0,0,0]-expectedq)),np.max(np.abs(result[1,:,0,0,0]-expectedv)))
 errors.append(float(err))

rng=np.random.default_rng(2026102203);q=.2*rng.standard_normal((4,4,4,4));v=np.zeros_like(q)
dt=1e-4;mp=.2;mx=.4;c=.1
result=run('gradient',q,v,dt,dt,.2,mp,mx,c)
force=2*(result[0]-q)/dt**2
def potential(q):
 f,h,x,y=q;r=f*f+h*h
 return np.sum(.5*mp**2*r+.5*mx**2*(x*x+y*y)+.25*r*r+c*(x*(f*f-h*h)+2*y*f*h))+sum(.5*np.sum((np.roll(q,-1,axis=ax)-q)**2) for ax in [1,2,3])
diff=[]
for idx in [(s,1,2,3) for s in range(4)]:
 qp=q.copy();qm=q.copy();qp[idx]+=1e-6;qm[idx]-=1e-6
 numerical=-(potential(qp)-potential(qm))/(2e-6)
 diff.append(float(abs(numerical-force[idx])))
k=np.geomspace(.01,1,40)
cov=np.pi/4*np.abs(hankel1(1.5,k))**2
expected=(1+1/k**2)/(2*k)
cov_error=float(np.max(np.abs(cov/expected-1)))
checks=dict(exact_solution=errors[1]<1e-5,
 second_order=3.8<errors[0]/errors[1]<4.2,
 Hamiltonian_gradient=max(diff)<1e-6,
 massless_deSitter_covariance=cov_error<1e-12)
data=dict(checks=checks,all_pass=all(checks.values()),exact_solution_errors=errors,
 gradient_errors=diff,covariance_relative_error=cov_error,
 scope='Code-level controls only; no proof of correct full quantum initial state or late relic kinetics.')
(out/'results.json').write_text(json.dumps(data,indent=2));print(json.dumps(data,indent=2))
sys.exit(0 if data['all_pass'] else 1)
