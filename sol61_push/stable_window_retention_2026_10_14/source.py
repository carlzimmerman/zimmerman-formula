"""Reference bound-orbital source, retaining spatial mediator resolvent."""
import json,math,sys
from pathlib import Path
import numpy as np
from scipy.integrate import solve_bvp,quad
from scipy.optimize import brentq
from scipy.special import dawsn
from numpy.polynomial.legendre import leggauss
prior=json.loads(Path('sol61_push/neutral_stable_window_2026_10_14/run/results.json').read_text())
hc=1.973269804e-7;hb=6.582119569e-16;c=299792458.;ej=1.602176634e-19;g=1e-20;lam=1e-6;checks=[]
def ck(name,e,t):
 assert e<t,(name,e,t)
 checks.append(dict(name=name,error=float(e),tolerance=t))
rows=[]
for label,index,asi in [('near_resonant_large',0,.2),('detuned_small',2,.02)]:
 row=prior['rows'][index];U=row['scaled_barrier_eV'];mu=row['selected_mu_eV'];delta=row['detuning_eV'];M=2+delta;a=asi/hc;Lt=.001/hc
 h=mu/(2*math.sqrt(2*M));F0=g*(1e12/c)/(ej/hc**3)/math.sqrt(2*M)
 z0=a*math.sqrt(2*U)
 z=brentq(lambda z:z/math.tan(z)+math.sqrt(z0*z0-z*z),math.pi/2+1e-12,min(z0,math.pi)-1e-12,xtol=1e-14)
 beta=math.sqrt(z0*z0-z*z);norm=.5-math.sin(2*z)/(4*z)+math.sin(z)**2/(2*beta);E0=z*z/(2*a*a);end=1+25/beta
 def v(x):
  x=np.asarray(x);return np.where(x<=1,np.sin(z*x),math.sin(z)*np.exp(-beta*np.maximum(x-1,0)))/math.sqrt(norm)
 def src(x):
  t=np.asarray(x)*a/(math.sqrt(2)*Lt);out=np.ones_like(t);np.divide(dawsn(t),t,out=out,where=t!=0);return out
 C=a*math.sqrt(2*M*(delta-2*E0))
 def solve(kind,tol):
  stop=1 if kind=='source' else end
  mesh=np.unique(np.r_[np.linspace(0,1,601),np.linspace(1,stop,201)])
  def rhs(x,y):
   if kind=='source':f=x*src(x)
   else:f=np.divide(v(x)**2,x,out=np.zeros_like(x),where=x!=0)
   # Scale unknown by C^2 to keep O(1) quantities for the stiff detuned case.
   return np.vstack((y[1],C*C*(y[0]-f)))
  sol=solve_bvp(rhs,lambda l,r:np.array([l[0],r[1]+C*r[0]]),mesh,np.zeros((2,len(mesh))),tol=tol,max_nodes=30000)
  assert sol.success,sol.message
  def value(x):
   x=np.asarray(x);return np.where(x<=stop,sol.sol(np.minimum(x,stop))[0],sol.sol(stop)[0]*np.exp(-C*np.maximum(x-stop,0)))/(C*C)
  return value
 def integrals(tol,N):
  ss=solve('source',tol);pp=solve('pair',tol);q,w=leggauss(N);js=0.;jp=0.
  for left,right in [(0,1),(1,end)]:
   x=left+(q+1)*(right-left)/2;weights=w*(right-left)/2;density=v(x)**2/x
   js+=float(np.dot(weights,density*ss(x)));jp+=float(np.dot(weights,density*pp(x)))
  return js,jp,ss
 js,jp,ss=integrals(1e-8,256);fs,fp,_=integrals(2e-10,384)
 ck(label+'_source_refinement',abs(js/fs-1),2e-6);ck(label+'_self_refinement',abs(jp/fp-1),2e-6)
 # Independent direct source Green integral, with cusp isolated by interval split.
 for X in [.01,.2,.8,1.]:
  def f(y):return (math.exp(-C*abs(X-y))-math.exp(-C*(X+y)))/(2*C)*y*float(src(y))
  val=quad(f,0,X,epsabs=1e-20,epsrel=1e-9)[0]+quad(f,X,1,epsabs=1e-20,epsrel=1e-9)[0]
  ck(label+'_green_'+str(X),abs(float(ss(X))/val-1),3e-6)
 ck(label+'_normalization',abs(quad(lambda x:float(v(x))**2,0,1)[0]+math.sin(z)**2/(2*beta*norm)-1),1e-12)
 contact=(lam-mu*mu/(4*M*M))/(4*math.pi*a**3)*quad(lambda x:float(v(x))**4/x**2 if x else 0,0,end,points=[1],epsabs=1e-11)[0]
 shift=-M*h*h/(2*math.pi*a)*fp;omega=-2*M*a*a*h*F0*fs
 assert abs(contact+shift)/(delta-2*E0)<1e-8
 rows.append(dict(candidate=label,radius_m=asi,reference_energy_eV=E0,orbital_probability_inside_cavity=(.5-math.sin(2*z)/(4*z))/norm,contact_shift_eV=contact,virtual_shift_eV=shift,net_pair_interaction_eV=contact+shift,pair_drive_per_s=abs(omega)/hb,weak_no_loss_time_for_probability_001_s=.1*hb/abs(omega),mediator_C=C,pair_shift_over_mediator_gap=abs(contact+shift)/(delta-2*E0)))
result=dict(scope='Prescribed I=1e12 W/m^2 per wave, waist=2mm, spherical-average source truncated at cavity boundary; infinite-exterior reference orbitals and leading pair projection; no actual optics or many-pair probability',rows=rows,checks=checks,passed=len(checks))
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='checks'},indent=2))
