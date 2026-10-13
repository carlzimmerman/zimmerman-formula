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
checks=[]
def check(name,b): checks.append(dict(name=name,passed=bool(b)))
# Algebraic Hessian versus finite differences of the actual potential.
def potential(y,sigma):return .5*y*y+1.5*y*y*window(sigma/math.sqrt(J),D,d)[0]
for ss in [d*.3,d*.7,D*.5,D+d*.3,D+d*.7]:
 y=.83;sigma=math.sqrt(J)*ss;eps=1e-6
 zz=[0,y,0,0,ss,1];H=hessian(zz)
 numyy=(potential(y+eps,sigma)-2*potential(y,sigma)+potential(y-eps,sigma))/eps**2
 nums=(potential(y,sigma+eps)-2*potential(y,sigma)+potential(y,sigma-eps))/eps**2
 cross=(potential(y+eps,sigma+eps)-potential(y+eps,sigma-eps)-potential(y-eps,sigma+eps)+potential(y-eps,sigma-eps))/(4*eps**2)
 check('potential Hessian finite difference',np.max(abs(H-np.array([[numyy,cross],[cross,nums]])))/(1+np.max(abs(H)))<2e-4)
Omega=np.block([[np.zeros((2,2)),np.eye(2)],[-np.eye(2),np.zeros((2,2))]])
rows=[]
for k in [0.,.01,.1,.3,1.,3.,10.,30.,100.,300.]:
 entries=[]
 for tol in [1e-9,2e-11]:
  S=np.eye(4)
  for h in hist:
   def rhs(t,flat):
    H=hessian(h.sol(t))+k*k*np.eye(2)
    A=np.block([[np.zeros((2,2)),np.eye(2)],[-H,np.zeros((2,2))]])
    return (A@flat.reshape(4,4)).reshape(-1)
   sol=solve_ivp(rhs,[h.t[0],h.t[-1]],S.reshape(-1),method='DOP853',rtol=tol,atol=tol*.05,max_step=min(.02,.25/max(1,k),d/8 if h is not hist[1] else .02))
   check('mode integration completed',sol.success)
   S=sol.y[:,-1].reshape(4,4)
  freqs=np.array([math.sqrt(1+k*k),k if k>0 else 1.])
  T=np.diag(np.r_[np.sqrt(freqs),1/np.sqrt(freqs)])
  R=T@S@np.linalg.inv(T)
  numbers=[float((np.sum(R[i]**2)+np.sum(R[i+2]**2))/4-.5) for i in range(2)] if k>0 else None
  err=float(np.max(abs(R.T@Omega@R-Omega)))
  entries.append(dict(rtol=tol,symplectic_error=err,largest_quadrature_gain=float(np.linalg.svd(R,compute_uv=False)[0]),vacuum_occupations=numbers,matrix=R.tolist()))
  check('symplectic mode transfer',err<2e-6)
  if numbers is not None:check('nonnegative vacuum occupations',min(numbers)>-2e-7)
 delta=float(np.max(abs(np.array(entries[0]['matrix'])-np.array(entries[1]['matrix']))))
 check('tolerance convergence',delta<2e-5)
 rows.append(dict(momentum_over_M=k,runs=entries,matrix_tolerance_difference=delta))
mins=[]
for h in hist:
 for t in np.linspace(h.t[0],h.t[-1],1001):mins.append(float(np.linalg.eigvalsh(hessian(h.sol(t)))[0]))
out=dict(all_pass=all(c['passed'] for c in checks),checks=checks,rows=rows,
         sampled_minimum_hessian_eigenvalue=min(mins),background=source,
         non_claims=['Finite linear fluctuation sample, not nonlinear stability',
                     'Vacuum occupations assume free incoming oscillator vacuum; zero mode excluded',
                     'No momentum-integrated energy or UV convergence claim',
                     'No primordial perturbation spectrum or daughter fluctuations included'])
(p/'clock_fluctuations_run'/'results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(dict(all_pass=out['all_pass'],checks=len(checks),min_hessian=min(mins),rows=[dict(k=r['momentum_over_M'],gain=r['runs'][-1]['largest_quadrature_gain'],n=r['runs'][-1]['vacuum_occupations'],symplectic_error=r['runs'][-1]['symplectic_error'],tolerance_difference=r['matrix_tolerance_difference']) for r in rows]),indent=2))
assert out['all_pass']
