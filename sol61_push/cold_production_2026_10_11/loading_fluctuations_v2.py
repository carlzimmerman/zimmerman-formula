"""Conservative moving-minimum loading followed by charged-source preparation."""
import json
from pathlib import Path
import math
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import minimize_scalar
J=10.;d=.01;release=.0001

def ramp(z):return z**3*(10+z*(-15+6*z)),30*z*z*(1-z)**2

def drive(s,R):
 if s<=-R-release or s>=0:return 0.,0.
 if s<-release:
  z=(s+R+release)/R;v,dv=ramp(z);return v,dv/R
 v,dv=ramp((s+release)/release);return 1-v,-dv/release

def window(s,D):
 if s<=0 or s>=D+d:return 0.,0.
 if s<d:v,dv=ramp(s/d);return v,dv/d
 if s<=D:return 1.,0.
 v,dv=ramp((s-D)/d);return 1-v,-dv/d

def integrate(z,edges,R,D,tol=1e-11):
 hist=[];t=0.
 def rhs(t,z):
  x,y,vx,vy,s,v=z;f,df=drive(s,R);w,dw=window(s,D)
  return [vx,vy,-x+f,-y+f-3*w*y,v,((x+y-2*f)*df-1.5*dw*y*y)/J]
 for edge,step in edges:
  def event(t,z):return z[4]-edge
  event.terminal=True;event.direction=1
  sol=solve_ivp(rhs,(0.,500.),z,events=event,dense_output=True,method='DOP853',rtol=tol,atol=tol*.05,max_step=step)
  if len(sol.t_events[0])!=1:raise RuntimeError('no crossing')
  z=sol.y[:,-1];t+=sol.t[-1];z[4]=edge;hist.append(sol)
 return z,t,hist

def prep(R,tol=1e-11):
 z=np.array([0.,0.,0.,0.,-R-release,math.sqrt(12/J)])
 return integrate(z,[(-release,.1),(0.,release/12)],R,1.31,tol)

def pulse(z,R,D,tol=1e-11):return integrate(z,[(d,d/12),(D,.025),(D+d,d/12)],R,D,tol)


p=Path(__file__).parent
source=json.loads((p/'clock_loading_run/results.json').read_text())['rows'][1]
R=source['rise_width'];D=source['pulse_width']
z,pretime,h1=prep(R,2e-13);q,pulsetime,h2=pulse(z,R,D,2e-13)
hist=h1+h2
checks=[]
def check(name,b):checks.append(dict(name=name,passed=bool(b)))
def ramp2(z):return 60*z*(1-z)*(1-2*z)
def derivatives(s):
 f,fp=drive(s,R);w,wp=window(s,D);fpp=wpp=0.
 if -R-release<s<-release:fpp=ramp2((s+R+release)/R)/R**2
 if -release<s<0:fpp=-ramp2((s+release)/release)/release**2
 if 0<s<d:wpp=ramp2(s/d)/d**2
 if D<s<D+d:wpp=-ramp2((s-D)/d)/d**2
 return f,fp,fpp,w,wp,wpp

def hessian(z):
 x,y,vx,vy,s,v=z;f,fp,fpp,w,wp,wpp=derivatives(s)
 return np.array([[1.,0.,-fp/math.sqrt(J)],[0.,1+3*w,(-fp+3*y*wp)/math.sqrt(J)],[-fp/math.sqrt(J),(-fp+3*y*wp)/math.sqrt(J),(2*fp*fp-(x+y-2*f)*fpp+1.5*y*y*wpp)/J]])
# The antisymmetric source direction stays an eigenvector of mass one while W=0.
for h in h1:
 for t in np.linspace(h.t[0],h.t[-1],11):
  H=hessian(h.sol(t));e=np.array([1.,-1.,0.])/math.sqrt(2)
  check('loading antisymmetric eigenmode',np.max(abs(H@e-e))<1e-9)
Omega=np.zeros((6,6));Omega[:3,3:]=np.eye(3);Omega[3:,:3]=-np.eye(3)
rows=[]
for k in [0.,.001,.01,.1,1.,10.,30.]:
 runs=[]
 for tol in [2e-11,5e-13]:
  freqs=np.array([math.sqrt(1+k*k)]*2+[k if k else 1.])
  scale=np.sqrt(freqs[:,None]*freqs[None,:]);S=np.eye(6)
  for index,h in enumerate(hist):
   def rhs(t,flat):
    H=hessian(h.sol(t))+k*k*np.eye(3);a=flat.reshape(6,6);out=np.empty_like(a)
    out[:3]=freqs[:,None]*a[3:];out[3:]=-(H/scale)@a[:3]
    return out.reshape(-1)
   step=release/12 if index==1 else (d/12 if index in [2,4] else .1)
   sol=solve_ivp(rhs,[h.t[0],h.t[-1]],S.reshape(-1),method='DOP853',rtol=tol,atol=tol*.02,max_step=min(step,.4/max(1,k)))
   check('mode integration',sol.success)
   if not sol.success:raise RuntimeError(sol.message)
   S=sol.y[:,-1].reshape(6,6)
  error=float(np.max(abs(S.T@Omega@S-Omega)))
  check('symplectic transfer',error<3e-6)
  beta=.5*(S[:3,:3]-S[3:,3:]+1j*(S[3:,:3]+S[:3,3:]))
  runs.append(dict(rtol=tol,matrix=S.tolist(),symplectic_error=error,quadrature_gain=float(np.linalg.svd(S,compute_uv=False)[0]),occupations=np.sum(abs(beta)**2,axis=1).tolist() if k else None))
 diff=float(np.max(abs(np.array(runs[0]['matrix'])-np.array(runs[1]['matrix']))))
 check('tolerance convergence',diff<3e-5)
 rows.append(dict(k=k,runs=runs,tolerance_difference=diff))
# k=0 canonical transfer predicts the response to a fractional initial clock speed change.
S=np.array(rows[0]['runs'][-1]['matrix']);B=np.array([[0,-1,0,1,0,0],[1,0,0,0,1,0]])
response=B@S[:,5]*math.sqrt(12)
E=.5*np.dot(q[:4],q[:4]);ratio=math.sqrt(1+1e-6)
coefficient=float(np.dot(response,response)/(2*E*ratio))
eta0=1-1/ratio
sensitivity=[]
for delta in [-.001,-.0001,.0001,.001]:
 zi=np.array([0.,0.,0.,0.,-R-release,math.sqrt(12/J)*(1+delta)])
 z,t,h=integrate(zi,[(-release,.1),(0.,release/12)],R,D,2e-13)
 qq,tt,hh=pulse(z,R,D,2e-13);EE=.5*np.dot(qq[:4],qq[:4]);Q=2*(qq[1]*qq[2]-qq[0]*qq[3])
 eta=1-Q/(2*EE*ratio);pred=eta0+coefficient*delta*delta
 if abs(delta)==.0001:check('nonlinear small-perturbation comparison',abs((eta-eta0)/(pred-eta0)-1)<.01)
 sensitivity.append(dict(relative_clock_speed_error=delta,eta=eta,linear_prediction=pred))
out=dict(all_pass=all(c['passed'] for c in checks),checks=checks,rows=rows,clock_speed_sensitivity=dict(quadratic_eta_coefficient=coefficient,estimated_relative_tolerance_for_eta_1e5=math.sqrt((1e-5-eta0)/coefficient),nonlinear_cases=sensitivity),non_claims=['Seven sampled linear modes; no momentum-integrated energy or UV bound','Only R100 chosen loading path','Zero-mode transfer is classical, not massless oscillator vacuum','No arbitrary primordial perturbation spectrum or nonlinear spatial stability'])
(p/'loading_fluctuations_run_v2'/'results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(dict(all_pass=out['all_pass'],checks=len(checks),rows=[dict(k=r['k'],gain=r['runs'][-1]['quadrature_gain'],n=r['runs'][-1]['occupations'],symplectic_error=r['runs'][-1]['symplectic_error'],difference=r['tolerance_difference']) for r in rows],sensitivity=out['clock_speed_sensitivity']),indent=2));assert out['all_pass']
