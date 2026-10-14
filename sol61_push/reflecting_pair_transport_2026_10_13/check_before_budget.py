import json,math,sys
from pathlib import Path
import numpy as np
from scipy.sparse import diags,bmat,eye
from scipy.sparse.linalg import eigs
from scipy.integrate import solve_ivp
from wall_solver import scatter
p=Path(__file__).parent;old=json.loads((p/'INPUT_GAIN.json').read_text());v=old['phonon_group_velocity_m_s'];mu=old['matter_pair_physical'][0]['pair_gain_s_inv']
angular=[]
for angle in list(range(0,90,5))+[88,89,89.9]:
 vals=[]
 for h in [.02,.01,.005,.0025]:
  r=scatter(1.,math.radians(angle),h);rho=math.sqrt(r['reflection'])
  assert 0<rho<1
  threshold=math.pi/2-2*math.atan(rho)
  diameter=v*threshold/(mu*math.cos(math.radians(angle)))
  vals.append(dict(h=h,amplitude_reflection=rho,gain_threshold=threshold,critical_diameter_m=diameter,flux_error=r['flux_error']))
  if len(vals)>1 and abs(vals[-2]['critical_diameter_m']-vals[-1]['critical_diameter_m'])/vals[-1]['critical_diameter_m']<.005:break
 assert abs(vals[-2]['critical_diameter_m']-vals[-1]['critical_diameter_m'])/vals[-1]['critical_diameter_m']<.005, (angle,vals)
 angular.append(dict(angle_degrees=angle,refinements=vals))
# Positive comparison generator: boundary inflow u(0)=rho*w(0), w(1)=rho*u(1).
checks=[]
for rho in [.1,.3,.7]:
 crit=math.pi/2-2*math.atan(rho)
 for factor in [.8,1.2]:
  g=crit*factor
  for N in [160,320]:
   adv=diags([-N*np.ones(N),N*np.ones(N-1)],[0,-1],format='csr')
   L=bmat([[adv,g*eye(N)],[g*eye(N),adv.T]],format='lil')
   L[0,N]+=N*rho;L[2*N-1,N-1]+=N*rho;L=L.tocsr()
   ev,vec=eigs(L,k=1,sigma=0,which='LM',tol=1e-10,maxiter=2000,v0=np.ones(2*N))
   a=vec[:,0].real
   if sum(a)<0:a=-a
   assert min(a)>0 and np.linalg.norm(L@a-ev[0]*a)<1e-7
   growth=float(ev[0].real);assert (growth>0)==(factor>1)
   checks.append(dict(rho=rho,factor=factor,N=N,growth=growth))
 # Critical positive eigenfunction independently satisfies both boundary relations.
 a=math.atan(rho)
 assert abs(math.sin(a)-rho*math.cos(a))<1e-12
 assert abs(math.cos(crit+a)-rho*math.sin(crit+a))<1e-12
 # Below threshold, an explicit positive supersolution yields weighted-norm decay.
 xs=np.linspace(0,1,501);U=np.sin(crit*xs+a);W=np.cos(crit*xs+a);delta=.2*crit
 assert min(delta*W/U)>=delta*rho-1e-12 and min(delta*U/W)>=delta*rho-1e-12
out=dict(angular_scan=angular,comparison_eigenchecks=checks,
 minimum_sampled_critical_diameter_m=min(r['refinements'][-1]['critical_diameter_m'] for r in angular),
 scope='Phase-independent positive-envelope comparison, equal passive reflectivities, uniform pair gain; finite angular scan of an imposed one-field wall. Not global three-dimensional stability or a physical trap.')
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n');print('angles',len(angular),'minimum sampled diameter',out['minimum_sampled_critical_diameter_m'])
