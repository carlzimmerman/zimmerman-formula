"""Autonomous smooth clock pulse: finite homogeneous classical experiment."""
import json
from pathlib import Path
import math
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import root

def window(s,D,d):
 def ramp(z): return z**3*(10+z*(-15+6*z)),30*z*z*(1-z)**2
 if s<=0 or s>=D+d:return 0.,0.
 if s<d:
  w,dw=ramp(s/d);return w,dw/d
 if s<=D:return 1.,0.
 w,dw=ramp((s-D)/d);return 1-w,-dw/d

def run(theta,D,J,d=.01,tol=1e-10):
 z=np.array([math.sqrt(2)*math.cos(theta),math.sqrt(2)*math.sin(theta),0.,0.,0.,1.])
 def rhs(t,z):
  x,y,vx,vy,s,v=z;w,dw=window(s,D,d)
  return [vx,vy,-x,-(1+3*w)*y,v,-1.5*dw*y*y/J]
 hist=[]; t=0
 for edge,step in [(d,d/12),(D,.025),(D+d,d/12)]:
  def stop(t,z):return z[4]-edge
  stop.terminal=True;stop.direction=1
  sol=solve_ivp(rhs,(t,t+20),z,events=stop,dense_output=True,rtol=tol,atol=tol*.1,max_step=step)
  if len(sol.t_events[0])==0:raise ValueError('clock did not cross')
  t=sol.t[-1];z=sol.y[:,-1];hist.append(sol)
 return z,t,hist


p=Path(__file__).parent
source=json.loads((p/'autonomous_clock_run/results.json').read_text())['rows'][0]['tight']
J=source['inertia'];D=source['width'];theta=source['theta'];d=.01
_,end,hist=run(theta,D,J,tol=2e-13)
def second(s):
 if 0<s<d:
  z=s/d;return 60*z*(1-z)*(1-2*z)/d**2
 if D<s<D+d:
  z=(s-D)/d;return -60*z*(1-z)*(1-2*z)/d**2
 return 0.
def hessian(z):
 y=z[1];s=z[4];w,dw=window(s,D,d)
 return np.array([[1+3*w,3*y*dw/math.sqrt(J)],[3*y*dw/math.sqrt(J),1.5*y*y*second(s)/J]])

from scipy.integrate import simpson
checks=[]
def check(name,b):checks.append(dict(name=name,passed=bool(b)))
def normalize(w): return np.diag(np.r_[np.sqrt(w),1/np.sqrt(w)])
def beta(R): return .5*(R[:2,:2]-R[2:,2:]+1j*(R[2:,:2]+R[:2,2:]))
def rotation(w,t):
 c=np.diag(np.cos(w*t));s=np.diag(np.sin(w*t))
 return np.block([[c,s],[-s,c]])
def modes(k,tol=1e-10):
 outside=np.array([math.sqrt(1+k*k),k]);inside=np.array([math.sqrt(4+k*k),k])
 Tout=normalize(outside);Tin=normalize(inside);Rs=[]
 for h,left,right in [(hist[0],Tout,Tin),(hist[2],Tin,Tout)]:
  # Integrate in the fixed outside normalization, controlling large k units.
  def rhs(t,f):
   H=hessian(h.sol(t))+k*k*np.eye(2)
   A=np.zeros((4,4));A[:2,2:]=np.eye(2);A[2:,:2]=-H
   B=Tout@A@np.linalg.inv(Tout)
   return (B@f.reshape(4,4)).reshape(-1)
  sol=solve_ivp(rhs,[h.t[0],h.t[-1]],np.eye(4).reshape(-1),method='DOP853',rtol=tol,atol=tol*.02,max_step=min(d/10,.4/max(1,k)))
  if not sol.success:raise RuntimeError(sol.message)
  S=np.linalg.inv(Tout)@sol.y[:,-1].reshape(4,4)@Tout
  Rs.append(right@S@np.linalg.inv(left))
 R=Rs[1]@rotation(inside,hist[1].t[-1]-hist[1].t[0])@Rs[0]
 n=np.sum(abs(beta(R))**2,axis=1)
 N1=float(np.sum(abs(beta(Rs[0]))**2));N2=float(np.sum(abs(beta(Rs[1]))**2))
 upper=(math.sqrt((1+N2)*N1)+math.sqrt((1+N1)*N2))**2
 # N upper follows from alpha alpha^dagger-beta beta^dagger=I and matrix norm inequalities.
 return dict(k=k,occupations=n.tolist(),total_occupation_upper=upper,edge_occupations=[N1,N2],energy_integrand_upper=k*k*outside[0]*upper/(2*math.pi**2))
prior=json.loads((p/'clock_fluctuations_run/results.json').read_text())
comparisons=[]
for row in prior['rows']:
 k=row['momentum_over_M']
 if k==0:continue
 z=modes(k);old=np.array(row['runs'][-1]['vacuum_occupations'])
 error=float(max(abs(np.array(z['occupations'])-old)))
 check('analytic plateau reproduces full evolution',error<3e-7)
 check('occupation envelope bounds composed value',sum(z['occupations'])<=z['total_occupation_upper']*(1+1e-8)+1e-12)
 comparisons.append(dict(k=k,max_occupation_difference=error))
ks=np.geomspace(.001,10000,257)
rows=[modes(float(k)) for k in ks]
y=np.array([r['energy_integrand_upper'] for r in rows])
# Integrate in log k with its Jacobian, reporting coarse/fine and cumulative cutoffs.
logk=np.log(ks)
fine=float(simpson(y*ks,x=logk));coarse=float(simpson((y*ks)[::2],x=logk[::2]))
check('cutoff quadrature refinement',abs(fine-coarse)/fine<.05)
cutoffs=[]
for i in [128,192,224,240,256]:
 cutoffs.append(dict(kmax=float(ks[i]),integral_upper_estimate=float(simpson((y*ks)[:i+1],x=logk[:i+1]))))
checks_tight=[]
for k in [300.,1000.,3000.,10000.]:
 a=modes(k);b=modes(k,2e-12)
 err=abs(a['total_occupation_upper']-b['total_occupation_upper'])/max(b['total_occupation_upper'],1e-100)
 check('high momentum tolerance convergence',err<.005)
 checks_tight.append(dict(k=k,relative_envelope_difference=err,occupation_upper=b['total_occupation_upper']))
M=2e-12*math.sqrt(1+.001**2);rho=9.71510619e6
out=dict(all_pass=all(c['passed'] for c in checks),checks=checks,rows=rows,comparisons=comparisons,
         quadrature=dict(fine=fine,coarse=coarse,relative_difference=abs(fine-coarse)/fine,cutoffs=cutoffs),tight_checks=checks_tight,
         physical=dict(M_eV=M,source_density_eV4=rho,finite_band_energy_upper_estimate_eV4=fine*M**4,fraction_of_source=fine*M**4/rho),
         non_claims=['Envelope is pointwise bound; numerical integral is an estimate, not interval-certified',
                     'Only .001<=p/M<=10000; no uncomputed UV/IR tail bound',
                     'Linear vacuum fluctuations only; no primordial classical spectrum'])
(p/'clock_energy_run'/'results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ['rows','checks','comparisons']},indent=2));print('Checks:',len(checks));assert out['all_pass']
