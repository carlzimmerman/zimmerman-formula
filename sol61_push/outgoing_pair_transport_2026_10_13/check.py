import math,json,sys
from pathlib import Path
import numpy as np
from scipy.optimize import brentq
from scipy.sparse import diags,bmat,eye
from scipy.sparse.linalg import eigs
from scipy.integrate import solve_ivp

def exact_growth(g):
 if abs(g-1)<1e-12:return -1.
 if g<1:
  p=brentq(lambda p:p/math.sinh(p)-g,1e-8,30)
  return -p/math.tanh(p)
 q=brentq(lambda q:q/math.sin(q)-g,1e-8,math.pi-1e-8)
 return -q/math.tan(q)
rows=[]
for g in [.5,1.1,1.4,math.pi/2,1.8,2,3]:
 exact=exact_growth(g);errs=[]
 for N in [80,160,320]:
  # First-order upwind transport, incoming values zero, L=v=1.
  left=diags([-N*np.ones(N),N*np.ones(N-1)],[0,-1],format='csr')
  right=left.T;L=bmat([[left,g*eye(N)],[g*eye(N),right]],format='csr')
  vals,vecs=eigs(L,k=1,sigma=exact+.05,which='LM',tol=1e-10,maxiter=2000,v0=np.ones(2*N))
  vec=vecs[:,0].real
  if sum(vec)<0:vec=-vec
  assert min(vec)>0 and np.linalg.norm(L@vec-vals[0]*vec)<1e-7
  numerical=float(vals[0].real);assert abs(vals[0].imag)<1e-7
  errs.append(abs(numerical-exact));rows.append(dict(g=g,N=N,exact=exact,numerical=numerical,error=errs[-1]))
 assert errs[-1]<errs[0] and errs[-1]<.02
# Independent boundary transfer calculation: normalized starting w(0)=1,u(0)=0.
boundary=[]
for g in [1.1,1.4,1.8,2,3]:
 lam=exact_growth(g)
 sol=solve_ivp(lambda x,y:[-lam*y[0]+g*y[1],-g*y[0]+lam*y[1]],[0,1],[0,1],rtol=1e-11,atol=1e-12)
 assert abs(sol.y[1,-1])<1e-10
 boundary.append(dict(g=g,outgoing_boundary_residual=float(abs(sol.y[1,-1]))))
# Zero-frequency input/output Bogoliubov scattering preserves commutators.
scattering=[]
for g in [.1,.5,1.,1.4]:
 transmission=1/math.cos(g);pair=math.tan(g)
 assert abs(transmission**2-pair**2-1)<1e-12
 scattering.append(dict(g=g,vacuum_output_occupation_per_frequency_channel=pair*pair,amplitude_transmission=transmission))
old=json.loads((Path(__file__).parent/'INPUT_PAIR_GAIN.json').read_text());v=old['phonon_group_velocity_m_s'];physical=[]
for r in old['matter_pair_physical']:
 mu=r['pair_gain_s_inv'];physical.append(dict(eta=r['eta'],critical_open_chord_m=math.pi*v/(2*mu),
  g_for_one_cm=mu*.01/v,one_cm_normal_chord_below_threshold=bool(mu*.01/v<math.pi/2)))
out=dict(growth_checks=rows,boundary_checks=boundary,scattering=scattering,physical=physical,
 scope='Uniform one-dimensional counterpropagating envelopes with nonreflecting incoming boundaries. Ray/chord application is conditional, not full three-dimensional sample stability.')
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(physical,indent=2));print('maximum finest-grid error',max(r['error'] for r in rows if r['N']==320))
