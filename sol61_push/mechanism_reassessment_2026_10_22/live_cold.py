import numpy as np,json,sys,time
from pathlib import Path
from scipy.integrate import solve_ivp
from scipy.stats import qmc

def initial(n,ng):
 from scipy.integrate import cumulative_trapezoid
 data=json.load(open(Path(__file__).parent/('cold_discrete_'+str(ng)+'_10000.json')))
 rg=np.array(data['rg']);z=np.array(data['z'])
 rr=np.linspace(0,rg[-1],80000)
 psi=np.maximum(np.interp(rr,rg,z)+1/np.sqrt(1+rr*rr),0)
 rho=10000*psi**2.5/(1+rr*rr)
 mass=cumulative_trapezoid(rr*rr*rho,rr,initial=0);mass/=mass[-1]
 samples=qmc.Sobol(3,scramble=False).random_base2(int(np.log2(n//2)))
 samples=(samples*(n//2-1)+.5)/(n//2)
 radii=np.interp(samples[:,0],mass,rr)
 pp=np.maximum(np.interp(radii,rg,z)+1/np.sqrt(1+radii*radii),0)
 ss=np.linspace(0,1,20000);cdf=(5*ss**3-3*ss**5)/2
 speed=np.sqrt(2*pp)*np.interp(samples[:,1],cdf,ss);mu=samples[:,2]
 vr=speed*mu;vt=speed*np.sqrt(1-mu*mu)/np.sqrt(1+radii*radii)
 return np.column_stack([np.r_[radii,radii],np.zeros(n)]),np.column_stack([np.r_[vr,-vr],np.r_[vt,vt]])

def evolve(n=32768,dt=.01,duration=40,dilation=1.05,ng=256,target_energy=None):
 x,v=initial(n,ng);x*=dilation;v/=dilation
 Rmax=10.;dr=Rmax/ng;rg=(np.arange(ng)+.5)*dr;gamma=.01;mp=1/n
 def field(x,energy=False):
  r=np.linalg.norm(x,axis=1)
  if r.max()>=rg[-1]:raise RuntimeError('outer excursion')
  t=np.clip((r-rg[0])/dr,0,ng-1-1e-10);idx=t.astype(int);frac=t-idx
  m=(np.bincount(idx,weights=1-frac,minlength=ng)+np.bincount(idx+1,weights=frac,minlength=ng))*mp
  q=np.cumsum(m)/rg**2
  if q.max()>=.98:raise RuntimeError('polarization cap q='+str(float(q.max()))+' at grid radius '+str(float(rg[np.argmax(q)])))
  rest=q*q/(1-q);mu=np.cumsum(rest[::-1])[::-1]*dr+gamma*m/(rg*rg*dr)
  acc=-(mu[idx+1]-mu[idx])/dr;acc[r<rg[0]]=0
  acc-=r/(1+r*r)**1.5
  force=acc[:,None]*x/np.maximum(r[:,None],1e-30)
  U=np.sum(rg*rg*(-q-np.log1p(-q)-q*q/2))*dr+gamma/2*np.sum(m*m/(rg*rg*dr))-np.mean(1/np.sqrt(1+r*r)) if energy else 0
  return force,U,float(q.max()),r
 if target_energy is not None:
  from scipy.optimize import brentq
  xx=x/dilation;vv=v*dilation
  baseE=.5*np.mean(np.sum(vv*vv,axis=1))+field(xx,True)[1]
  def excess(lam):return .5*np.mean(np.sum((vv/lam)**2,axis=1))+field(xx*lam,True)[1]-baseE-target_energy
  dilation=brentq(excess,1.,1.15,xtol=1e-13);x=xx*dilation;v=vv/dilation
 a,U,q,r=field(x,True)
 # Finite difference the identical discrete energy, selecting off-node particles.
 errs=[]
 for i in [123,1001,2345]:
  xx=x.copy();direction=x[i]/r[i];eps=1e-5
  xx[i]+=eps*direction;up=field(xx,True)[1];xx[i]-=2*eps*direction;um=field(xx,True)[1]
  inferred=-(up-um)/(2*eps*mp);exact=np.dot(a[i],direction)
  errs.append(abs(inferred-exact)/max(abs(exact),1e-8))
 L=x[:,0]*v[:,1]-x[:,1]*v[:,0];E0=.5*np.mean(np.sum(v*v,axis=1))+U;rows=[];start=time.monotonic()
 failure=None
 for step in range(int(round(duration/dt))+1):
  if step%20==0:
   a,U,q,r=field(x,True);E=.5*np.mean(np.sum(v*v,axis=1))+U
   rows.append(dict(t=step*dt,energy=E,relative_energy_drift=(E-E0)/abs(E0),rms_radius=float(np.sqrt(np.mean(r*r))),half_mass_radius=float(np.median(r)),mass_inside_one=float(np.mean(r<1)),max_q=q,max_radius=float(r.max())))
  if step==int(round(duration/dt)):break
  v+=.5*dt*a;x+=dt*v
  try:a,_,_,_=field(x)
  except RuntimeError as e:
   failure=dict(message=str(e),time=(step+1)*dt,max_radius=float(np.linalg.norm(x,axis=1).max()));break
  v+=.5*dt*a
 out=dict(failure=failure,target_energy=target_energy,n=n,dt=dt,ng=ng,duration=duration,dilation=dilation,force_relative_errors=errs,max_energy_drift=max(abs(r['relative_energy_drift']) for r in rows),max_L_error=float(np.max(np.abs(x[:,0]*v[:,1]-x[:,1]*v[:,0]-L))),rows=rows,wall_seconds=time.monotonic()-start,scope='exploratory spherical particle-mesh Hamiltonian; no relaxation claim without convergence')
 return out
if __name__=='__main__':
 cfg=json.loads(sys.argv[2]) if len(sys.argv)>2 else {}
 try:
  result=evolve(**cfg)
 except RuntimeError as e:
  Path(sys.argv[1]).write_text(json.dumps(dict(config=cfg,error=str(e)),indent=2))
  raise
 Path(sys.argv[1]).write_text(json.dumps(result,indent=2))
 print(json.dumps({k:v for k,v in result.items() if k!='rows'},indent=2))
