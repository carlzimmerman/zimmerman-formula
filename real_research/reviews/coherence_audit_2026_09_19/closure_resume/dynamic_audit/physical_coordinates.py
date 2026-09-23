from pathlib import Path
import json, math
import sympy as s
import numpy as np
from scipy.integrate import solve_ivp
from scipy.linalg import eigh
here=Path(__file__).resolve().parent
d=json.loads((here/'symbolic_observables.json').read_text())
a,h,q,j,ep,xi,k,al,ald,b=[s.sympify(x) for x in d['variables']]
K,D,U,acc=[s.sympify(d[z]) for z in ('K','D','U','acceleration')]
gc=1+s.Rational(3,2)*b;hd=q*j/(4*gc)
def dt(z):return a*h*s.diff(z,a)+hd*s.diff(z,h)-3*ep*h*s.diff(z,q)-3*h*j*s.diff(z,j)+ald*s.diff(z,al)
S=s.Matrix([[1,-1],[0,q/h]])
St=S.applyfunc(dt);Stt=St.applyfunc(dt)
Kn=(h*S.T*K*S).applyfunc(s.factor)
Dn=(S.T*(2*K*St+D*S)+hd/h*S.T*K*S).applyfunc(s.factor)
Un=(S.T*(K*Stt+D*St+U*S)/h).applyfunc(s.factor)
Bn=(Dn-Dn.T)/2
Vn=((Un+Un.T)/2).applyfunc(s.factor)
Anew=(-Kn.inv()*s.Matrix.hstack(Un[:,0],Dn[:,0],Un[:,1],Dn[:,1])).applyfunc(s.factor)
fn=s.lambdify([a,h,q,j,ep,xi,k,al,ald,b],[Kn,Dn,Vn,Anew], 'numpy',cse=True)
for c in json.loads((here/'audit_results.json').read_text())['cases'][:2]:
 label=c['case'];bn=1/39998 if label=='constant' else .03;eps=1e-9;j0=-1.86/(1-eps);Gc=1+1.5*bn;lam=3*Gc-(eps-1)*j0/2;hub=299792458/67400;n0=math.log(c['a0']);n1=n0+c['delta_N']
 def evaluate(n,y=None):
  aa=np.exp(n);qq=1-3*eps*n;jj=j0/aa**3;hh=np.sqrt(((eps-qq)*jj/2+lam)/(3*Gc));hdot=qq*jj/(4*Gc)
  if label=='constant':alpha=1/40000;ad=0.
  else:v=1e-7*aa**-4;alpha=.5*v/(.5+v);ad=-4*hh*alpha*(1-2*alpha)
  kval,dval,vval,av=fn(aa,hh,qq,jj,eps,4e-6/hub,c['k_Mpc']*hub,alpha,ad,bn)
  mat=np.array([[0,1,0,0],av[0],[0,0,0,1],av[1]])
  if y is None:return mat
  ratio=hh/qq;rp=ratio*(hdot/hh**2+3*eps/qq)
  z=np.array([y[0]+ratio*y[2],y[1]+ratio*y[3]+rp*y[2],ratio*y[2],ratio*y[3]+rp*y[2]])
  # Failed comparison-energy candidate: +4K does NOT make this transformed potential positive.
  veigs=eigh(vval,kval,eigvals_only=True)
  qv=z[[0,2]];vel=z[[1,3]]
  ene=float((vel@kval@vel+qv@(vval+4*kval)@qv)/2)
  return {'state':z.tolist(),'spectrum':[[float(v.real),float(v.imag)] for v in np.linalg.eigvals(mat)],'V_generalized':veigs.tolist(),'E_plus4K':ene}
 i=evaluate(n0,np.array(c['y0']));f=evaluate(n1,np.array(c['y1']));i0=np.array(i['state'])
 sol=solve_ivp(lambda n,z:evaluate(n)@z,(n0,n1),i0,rtol=1e-11,atol=1e-15,max_step=c['delta_N']/100)
 result={'case':label,'initial':i,'final':f,'energy_amplification':f['E_plus4K']/i['E_plus4K'],'physical_coordinate_integration_end':sol.y[:,-1].tolist(),'relative_match':float(np.linalg.norm(sol.y[:,-1]-f['state'])/np.linalg.norm(f['state']))}
 print(json.dumps(result),flush=True)
