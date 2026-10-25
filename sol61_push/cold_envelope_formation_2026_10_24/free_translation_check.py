"""Analytic moving/spreading free Gaussian benchmark of weighted radial/angular representation."""
import pathlib,json,hashlib,numpy as np
from scipy.linalg.lapack import zgttrf,zgttrs
from angular_half import Angular
P=pathlib.Path(__file__).resolve().parent;files=[pathlib.Path(__file__),P/'angular_half.py'];before={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in files};rows=[]
for nr in [512,1024]:
 L=12;eta=.05;vel=.1;sig=1.;dt=.02;T=10.;rmax=28.;inner=nr//3;r=np.r_[np.geomspace(1e-4,1,inner,endpoint=False),np.linspace(1,rmax,nr-inner+1)[:-1]];hl=np.diff(np.r_[0,r]);hr=np.diff(np.r_[r,rmax]);w=(hl+hr)/2;ang=Angular(L,4,r,w)
 g=(np.sqrt(w)*r*np.exp(-r*r/(2*sig*sig)))[:,None,None]*np.exp(1j*vel/eta*r[:,None,None]*ang.field.mu[None,:,None])*np.ones((1,1,ang.field.nphi));v=ang.field.back(g);v/=np.linalg.norm(v)
 diagonal=.5*eta*eta*(1/hl+1/hr)/w;off=-.5*eta*eta/(hr[:-1]*np.sqrt(w[:-1]*w[1:]));groups=[]
 for l in range(L+1):
  ix=np.array([j for j,(ll,m) in enumerate(ang.field.lm) if ll==l]);d=diagonal+.5*eta*eta*l*(l+1)/r**2;c=1j*dt/(4*eta);f=zgttrf(c*off,1+c*d,c*off);assert f[-1]==0;groups.append((ix,d,f[:-1]))
 def kinetic(z):
  out=np.empty_like(z);c=1j*dt/(4*eta)
  for ix,d,f in groups:
   u=z[:,ix];rhs=(1-c*d[:,None])*u;rhs[:-1]-=c*off[:,None]*u[1:];rhs[1:]-=c*off[:,None]*u[:-1];out[:,ix],info=zgttrs(*f,np.asfortranarray(rhs));assert info==0
  return out
 for k in range(round(T/dt)):v=kinetic(kinetic(v))
 va=ang.field.forward(v);mass=float(np.sum(abs(v)**2));zmean=float(np.sum(r*ang.field.integral(abs(va)**2*ang.field.mu[None,:,None]))/mass);r2=float(np.sum(r*r*np.sum(abs(v)**2,axis=1))/mass);width=r2-zmean*zmean;exactwidth=1.5*sig*sig*(1+(eta*T/sig**2)**2)
 row={'nr':nr,'mass_error':abs(mass-1),'COM_z':zmean,'analytic_COM_z':vel*T,'COM_error':abs(zmean-vel*T),'centred_r2':width,'analytic_centred_r2':exactwidth,'relative_centred_r2_error':abs(width/exactwidth-1)};rows.append(row);assert row['mass_error']<1e-10 and row['COM_error']<.01 and row['relative_centred_r2_error']<.01
assert rows[1]['COM_error']<rows[0]['COM_error'] and rows[1]['relative_centred_r2_error']<rows[0]['relative_centred_r2_error']
after={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in files};assert before==after
(P/'free_translation_check.json').write_text(json.dumps({'scope':'free-Gaussian Galilean translation/spreading only; does not certify nonlinear fragment momentum/recoil or moving stellar DF','inputs_before':before,'inputs_after':after,'results':rows},indent=2)+'\n');print(rows)
