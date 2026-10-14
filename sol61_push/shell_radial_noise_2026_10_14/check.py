"""Bounded radial elastic mode sum and diagonal trapped-pair thermal dephasing."""
import json,math,sys
from pathlib import Path
import numpy as np
from scipy.special import spherical_jn as j,spherical_yn as y
from scipy.optimize import brentq
from numpy.polynomial.legendre import leggauss
prior=json.loads(Path('sol61_push/stable_window_retention_2026_10_14/run/retention.json').read_text())
hc=1.973269804e-7;hb=6.582119569e-16;kb=1.380649e-23;rho=2201.;cl=6000.;ct=3750.;T=300.;Q=100.
shear=rho*ct*ct;lame=rho*(cl*cl-2*ct*ct);alpha=lame/(rho*cl*cl);checks=[]
def ck(name,e,t):
 assert e<t,(name,e,t)
 checks.append(dict(name=name,error=float(e),tolerance=t))
def stress(fun,z):return fun(1,z,derivative=True)+2*alpha*fun(1,z)/z
cases=[]
for label in ['near_resonant_large','detuned_small']:
 old=[x for x in prior['rows'] if x['candidate']==label][-1];a=old['radius_m'];b=a+old['thickness_m'];U=old['barrier_eV'];eta=a/b
 def determinant(q):return stress(j,q*eta)*stress(y,q)-stress(y,q*eta)*stress(j,q)
 def roots(step):
  grid=np.arange(.0001,160,step);roots=[];last=determinant(grid[0])
  for left,right in zip(grid[:-1],grid[1:]):
   val=determinant(right)
   if last*val<0:roots.append(brentq(determinant,left,right,xtol=1e-13))
   last=val
  assert len(roots)>=40
  return np.array(roots[:40])
 qs=roots(.02);qfine=roots(.01);ck(label+'_root_grid_refinement',max(abs(qs/qfine-1)),1e-11)
 z0=a/hc*math.sqrt(2*U);z=brentq(lambda z:z/math.tan(z)+math.sqrt(z0*z0-z*z),math.pi/2+1e-12,min(z0,math.pi)-1e-12)
 beta=math.sqrt(z0*z0-z*z);norm=.5-math.sin(2*z)/(4*z)+math.sin(z)**2/(2*beta);decay=beta/a
 def weight(r):return math.sin(z)**2/(a*norm)*np.exp(-2*decay*(r-a))
 def mode(q,r,deriv=False):
  A=stress(y,q*eta);B=-stress(j,q*eta);scale=math.hypot(A,B);A/=scale;B/=scale
  return (A*j(1,q*r/b,derivative=deriv)+B*y(1,q*r/b,derivative=deriv))*(q/b if deriv else 1)
 def calc(q,N):
  x,w=leggauss(N);r=a+(x+1)*(b-a)/2;w=w*(b-a)/2;f=mode(q,r);fp=mode(q,r,True);div=fp+2*f/r
  mass=4*math.pi*rho*np.dot(w,r*r*f*f)
  elastic=4*math.pi*np.dot(w,r*r*(lame*div*div+2*shear*(fp*fp+2*f*f/(r*r))))
  # Full density and both moving surfaces, and its integrated-by-parts form.
  direct=-2*U*(np.dot(w,weight(r)*div)+weight(a)*mode(q,a)-weight(b)*mode(q,b))
  coupled=-4*U*np.dot(w,(decay+1/r)*weight(r)*f)
  omega=cl*q/b
  gamma=(coupled/hb)**2*kb*T/(mass*omega**3*Q)
  return dict(q=q,frequency_Hz=omega/(2*math.pi),effective_mass_kg=mass,pair_energy_derivative_eV_per_m=coupled,phase_decay_per_s=gamma),elastic/(mass*omega*omega),direct,coupled
 modes=[]
 for i,q in enumerate(qs):
  record,ray,direct,coupled=calc(q,384);fine,_,_,_=calc(q,768)
  ck(label+'_Rayleigh_'+str(i),abs(ray-1),1e-9)
  ck(label+'_coupling_refinement_'+str(i),abs(record['phase_decay_per_s']/fine['phase_decay_per_s']-1),1e-7)
  ck(label+'_surface_bulk_identity_'+str(i),abs(direct-coupled)/max(abs(direct),abs(coupled),1e-30),1e-8)
  # Relative stress residual at the free outer boundary; inner is built in.
  stressb=mode(q,b,True)+2*alpha*mode(q,b)/b
  ck(label+'_outer_free_stress_'+str(i),abs(stressb)/(q/b),1e-10)
  modes.append(record)
 x,w=leggauss(768);r=a+(x+1)*(b-a)/2;w=w*(b-a)/2
 for i in range(4):
  fi=mode(qs[i],r);fj=mode(qs[i+1],r)
  overlap=np.dot(w,r*r*fi*fj)/math.sqrt(np.dot(w,r*r*fi*fi)*np.dot(w,r*r*fj*fj))
  ck(label+'_orthogonality_'+str(i),abs(overlap),1e-9)
 cases.append(dict(candidate=label,radius_m=a,outer_radius_m=b,modes=modes,partial_dephasing_sums_per_s={str(N):sum(x['phase_decay_per_s'] for x in modes[:N]) for N in [10,20,40]}))
result=dict(scope='First 40 l=0 elastic modes of ideal homogeneous isotropic free spherical shells; classical thermal viscous damping, Q=100 and T=300 K assigned; diagonal dephasing only',assumptions=dict(density_kg_per_m3=rho,longitudinal_speed_m_s=cl,transverse_speed_m_s=ct,temperature_K=T,quality_factor=Q),cases=cases,checks=checks,passed=len(checks))
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(dict(passed=len(checks),cases=[dict(candidate=x['candidate'],first_frequency_Hz=x['modes'][0]['frequency_Hz'],partial_sums=x['partial_dephasing_sums_per_s']) for x in cases]),indent=2))
