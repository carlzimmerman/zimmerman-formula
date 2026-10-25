"""Read-only CCT015 shell-inventory audit; run from repository root.

Prints NDJSON: frozen trapezoid versus mapped nodal-density SEM, then
operator-consistent weak SEM with element-local derivatives. Partial balls
integrate the cubic interpolant of J*radial_density on the containing element;
complete-element integration equals four-point LGL quadrature. This partial
construction is an approximation and still needs radial refinement.

For chi=r*A, physical radial kinetic inventory equals weak chi kinetic
minus eta^2/(2*R)*integral_Omega |chi(R)|^2. Gravity surface Phi*d_rPhi/(8*pi)
is retained unchanged to isolate inventory errors. No evolution or old edits.
"""
import pathlib,hashlib,resource,datetime
ROOT=pathlib.Path(__file__).resolve().parents[2]
import os
os.chdir(ROOT)
OLD=ROOT/'sol61_push/cold_fourth_flux_2026_10_25'
PINS=[pathlib.Path(__file__),OLD/'sphere_v2.py',OLD/'budget.py',OLD/'flux.py',ROOT/'sol61_push/cold_envelope_formation_2026_10_24/runs/draco_escape_long_fields.npz']
for tag in ['draco_v2_128','draco_v2_256']:
 for ext in ['json','npz']:PINS.append(OLD/'runs'/(tag+'.'+ext))
def hashes():return {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in PINS}
BEFORE=hashes()
import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='1'
import pathlib,sys,json,numpy as np
from scipy.interpolate import CubicSpline
from scipy.integrate import cumulative_trapezoid
sys.path.insert(0,str(pathlib.Path('sol61_push/cold_fourth_flux_2026_10_25').resolve()))
from sphere_v2 import Sphere
from budget import initial,derivative,shells
P=pathlib.Path('sol61_push/cold_fourth_flux_2026_10_25');old=np.load('sol61_push/cold_envelope_formation_2026_10_24/runs/draco_escape_long_fields.npz');rr,v,lm=[old[k] for k in ['r','initial','lm']]
radii=np.array([1.,2.,4.,8.,12.,16.])
for ne in [128,256]:
 tag='draco_v2_'+str(ne);meta=json.loads((P/'runs'/(tag+'.json')).read_text());eta=meta['physical']['eta_code'];j=next(j for j,x in enumerate(lm) if tuple(x)==(0,0));valid=(rr<21.8)&(abs(v[:,j])>1e-20);rv=rr[valid];sp=CubicSpline(rv,eta*np.unwrap(np.angle(v[valid,j])))
 def phase(x,der=0):
  if der:return np.where(x<=rv[-1],sp(x,1),sp(rv[-1],1))
  return np.where(x<=rv[-1],sp(x),sp(rv[-1])+sp(rv[-1],1)*(x-rv[-1]))
 s=Sphere(ne,24,32,eta=eta,phase=phase);sf=np.load(P/'runs'/(tag+'.npz'));u0=initial(s,old)
 z=s.z;polys=[]
 for i in range(4):
  p=np.poly1d([1.])
  for j in range(4):
   if i!=j:p*=np.poly1d([1.,-z[j]])/(z[i]-z[j])
  polys.append(np.polyint(p))
 def integrate(F):
  # F is the physical radial density at interior global nodes.
  full=np.r_[0.,F,0.];vals=[]
  for R in np.r_[radii,s.R]:
   xi=np.arcsinh(R*np.sinh(s.alpha)/s.R)/s.alpha;ee=min(int(xi*ne),ne-1);total=0.
   for e in range(ee+1):
    ix=np.arange(3*e,3*e+4);xx=(e+(z+1)/2)/ne;J=s.R*s.alpha*np.cosh(s.alpha*xx)/np.sinh(s.alpha);zend=1. if e<ee else 2*(xi*ne-e)-1
    weights=np.array([p(zend)-p(-1.) for p in polys])/(2*ne);total+=weights@(full[ix]*J)
   vals.append(total)
  return np.array(vals)
 states=[]
 for state,u,pot in [('initial',u0,s.poisson(u0)),('final',sf['u'],sf['phi'])]:
  A=u/s.sr[:,None,None]/s.sa[None,:,:];Dr=derivative(s,A)+1j*s.p[:,None,None]/eta*A;x=s.mu;bw=np.array([1/np.prod(x[i]-np.delete(x,i)) for i in range(len(x))]);D=np.zeros((len(x),len(x)))
  for i in range(len(x)):
   for j in range(len(x)):
    if i!=j:D[i,j]=bw[j]/bw[i]/(x[i]-x[j])
   D[i,i]=-D[i].sum()
  dm=np.einsum('ij,rjk->rik',D,A);dp=np.fft.ifft(np.fft.fft(A,axis=2)*(1j*s.m)[None,None,:],axis=2)
  kin=.5*eta**2*(abs(Dr)**2+((1-x*x)[None,:,None]*abs(dm)**2+abs(dp)**2/(1-x*x)[None,:,None])/s.r[:,None,None]**2)
  Fk=s.r*s.r*np.sum(s.aw[None,:,:]*kin,axis=(1,2));Fw=s.r*s.r*np.sum(s.aw[None,:,:]*(.5*abs(A)**2*pot),axis=(1,2));qk=integrate(Fk);qw=integrate(Fw);trap=shells(s,u,pot,radii);surf=np.interp(radii,s.r,s.r*s.r*np.sum(s.aw[None,:,:]*pot*derivative(s,pot,True),axis=(1,2))/(8*np.pi));canon=qk[:-1]+qw[:-1]+surf
  states.append((np.array(trap['E_canonical']),canon))
  mom=s.moments(u,pot)
  assert abs(qw[-1]-mom['W'])<1e-12
  print(json.dumps(dict(ne=ne,state=state,K_operator=mom['K'],K_SEM_same_point_gradient=qk[-1],K_trap_global=np.trapz(np.r_[0,Fk,0],np.r_[0,s.r,s.R]),W_operator=mom['W'],W_SEM=qw[-1],W_trap_global=np.trapz(np.r_[0,Fw,0],np.r_[0,s.r,s.R]),shell_SEM_minus_trap=(canon-np.array(trap['E_canonical'])).tolist())))
 hist=meta['history'];inte=np.trapz([h['flux']['energy'] for h in hist],[h['t'] for h in hist],axis=0);res_trap=states[1][0]-states[0][0]+inte;res_sem=states[1][1]-states[0][1]+inte
 print(json.dumps(dict(ne=ne,r=radii.tolist(),flux=inte.tolist(),res_trap=res_trap.tolist(),res_SEM_same_point_gradient=res_sem.tolist(),ratio_trap=(abs(res_trap)/abs(inte)).tolist(),ratio_sem=(abs(res_sem)/abs(inte)).tolist())))

for ne in [128,256]:
 tag='draco_v2_'+str(ne);meta=json.loads((P/'runs'/(tag+'.json')).read_text());eta=meta['physical']['eta_code'];j=next(j for j,x in enumerate(lm) if tuple(x)==(0,0));valid=(rr<21.8)&(abs(v[:,j])>1e-20);rv=rr[valid];sp=CubicSpline(rv,eta*np.unwrap(np.angle(v[valid,j])))
 def phase(x,der=0):
  if der:return np.where(x<=rv[-1],sp(x,1),sp(rv[-1],1))
  return np.where(x<=rv[-1],sp(x),sp(rv[-1])+sp(rv[-1],1)*(x-rv[-1]))
 s=Sphere(ne,24,32,eta=eta,phase=phase);sf=np.load(P/'runs'/(tag+'.npz'));u0=initial(s,old);z=s.z;lp=[];ip=[]
 for i in range(4):
  q=np.poly1d([1.])
  for j in range(4):
   if i!=j:q*=np.poly1d([1.,-z[j]])/(z[i]-z[j])
  lp.append(q);ip.append(np.polyint(q))
 states=[]
 for state,u,pot in [('initial',u0,s.poisson(u0)),('final',sf['u'],sf['phi'])]:
  chi=u/np.sqrt(s.w[:,None,None])/s.sa[None,:,:];full=np.concatenate([np.zeros_like(chi[:1]),chi,np.zeros_like(chi[:1])]);ang=np.sum(abs(s.transform(u))**2*s.lam[None,:,:],axis=(1,2))*eta**2/(2*s.r*s.r*s.w);ang=np.r_[0.,ang,0.];fw=np.r_[0.,.5*np.sum(abs(u)**2*pot,axis=(1,2))/s.w,0.];segments=[];radK=0;angK=0
  for e in range(ne):
   ix=np.arange(3*e,3*e+4);xx=(e+(z+1)/2)/ne;r=s.R*np.sinh(s.alpha*xx)/np.sinh(s.alpha);J=s.R*s.alpha*np.cosh(s.alpha*xx)/np.sinh(s.alpha);dc=(s.Dr@full[ix].reshape(4,-1)).reshape(full[ix].shape)*(2*ne/J)[:,None,None]+1j*phase(r,1)[:,None,None]/eta*full[ix];kr=.5*eta**2*np.sum(s.aw[None,:,:]*abs(dc)**2,axis=(1,2));segments.append((J*(kr+ang[ix]+fw[ix]),full[ix]));radK+=np.array([1,5,5,1])@(J*kr)/(12*ne);angK+=np.array([1,5,5,1])@(J*ang[ix])/(12*ne)
  vals=[]
  for R in radii:
   xi=np.arcsinh(R*np.sinh(s.alpha)/s.R)/s.alpha;ee=min(int(xi*ne),ne-1);value=0
   for e in range(ee+1):
    ze=1. if e<ee else 2*(xi*ne-e)-1;weights=np.array([p(ze)-p(-1) for p in ip])/(2*ne);value+=weights@segments[e][0]
   cr=np.einsum('i,ijk->jk',np.array([p(ze) for p in lp]),segments[ee][1]);value-=.5*eta**2*np.sum(s.aw*abs(cr)**2)/R;vals.append(value)
  surf=np.interp(radii,s.r,s.r*s.r*np.sum(s.aw[None,:,:]*pot*derivative(s,pot,True),axis=(1,2))/(8*np.pi));vals=np.array(vals)+surf;states.append(vals);mom=s.moments(u,pot);assert abs(radK+angK-mom['K'])<1e-11;print(json.dumps(dict(ne=ne,state=state,K_operator=mom['K'],K_weak_sem=radK+angK,K_difference=radK+angK-mom['K'])))
 inte=np.trapz([h['flux']['energy'] for h in meta['history']],[h['t'] for h in meta['history']],axis=0);res=states[1]-states[0]+inte;print(json.dumps(dict(ne=ne,res_weak_sem=res.tolist(),ratio_weak_sem=(abs(res)/abs(inte)).tolist())))

from scipy.integrate import quad
Iamp,erramp=quad(lambda x:x**4/(1+x*x)**4.5,0,np.inf,epsabs=1e-13)
Igrav,errgrav=quad(lambda x:x*x/(1+x*x)**3,0,np.inf,epsabs=1e-13)
assert abs(Iamp-2/35)<1e-12 and abs(Igrav-np.pi/16)<1e-12
print(json.dumps(dict(plummer=dict(amplitude_integral=Iamp,gravity_integral=Igrav,K_amplitude_coefficient=75*Iamp/8,W_self_magnitude_coefficient=1.5*Igrav,virial_amplitude_fraction_coefficient=(75*Iamp/8)/(.75*Igrav),scope='self-gravitating stationary scalar virial necessary support screen; no baryon or lifetime claim'))))
AFTER=hashes();assert BEFORE==AFTER
rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
assert rss<1_000_000_000
print(json.dumps(dict(audit_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),inputs_before=BEFORE,inputs_after=AFTER,peak_RSS_bytes=rss,interpreter=sys.executable)))
