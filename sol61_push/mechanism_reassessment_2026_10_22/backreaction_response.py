# Extracted accepted forced solver with susceptibility output; original unchanged.
import numpy as np
from scipy.integrate import solve_bvp,simpson
import json,sys
G=.01; eta=G/((2+3*.02798)/.02798)
mutate='--mutate' in sys.argv

def background(end):
 r=np.geomspace(1e-5,end,1000); n=r/(1+r*r)**1.5; q=(np.sqrt(n*n+4*n)-n)/2
 def fun(r,y):
  q,d=y;return np.array([d,(q*q/(1-q)-r/(1+r*r)**1.5)/G-2*d/r+2*q/r**2])
 return solve_bvp(fun,lambda a,b:np.array([a[1]-a[0]/1e-5,b[1]+b[0]/end]),r,np.array([q,np.gradient(q,r)]),tol=2e-8,max_nodes=10000)

def run(w,end,vacuum=False,tol=2e-7):
 bg=background(end)
 def hh(r):
  if vacuum:return np.zeros_like(r),np.zeros_like(r)
  q,d=bg.sol(r);return (1-q)**-2-1,2*d/(1-q)**3
 def source(r):return -r*(r*r-3)*np.exp(-r*r/2)/(2*np.pi)**1.5
 z=(eta*w*w+np.sqrt(eta*eta*w**4+4*G*w*w))/(2*G); k=np.sqrt(z); kap=np.sqrt(w*w/(G*z)); H=0 if vacuum else 2
 alpha=-H*k/(2*(2*G*k*k-eta*w*w)); ad=-H*kap/(2*(2*G*kap*kap+eta*w*w))
 def column(lam,p):
  # nth derivative divided by value for exp(lam*r) r^p.
  return np.array([1,lam+p/end,lam*lam+2*lam*p/end+p*(p-1)/end**2,lam**3+3*lam*lam*p/end+3*lam*p*(p-1)/end**2+p*(p-1)*(p-2)/end**3],complex)
 out=column(1j*k,1j*alpha); incoming=np.conj(out); decay=column(-kap,ad); growing=column(kap,-ad)
 if mutate and not vacuum:out,incoming=incoming,out
 inv=np.linalg.inv(np.column_stack([out,decay,incoming,growing]))
 def fun(r,y):
  h,dh=hh(r)
  return np.array([y[1],y[2],y[3],(source(r)-(eta*w*w-h)*y[2]+dh*y[1]-(dh/r-w*w)*y[0])/G])
 def bc(a,b):return np.array([a[0]-1e-5*a[1],a[2]-1e-5*a[3],(inv@b)[2],(inv@b)[3]])
 r=np.unique(np.r_[np.geomspace(1e-5,10,250),np.linspace(1e-5,end,int(end*k*5)+300)])
 def real_fun(r,y):
  z=fun(r,y[:4]+1j*y[4:]); return np.vstack([z.real,z.imag])
 def real_bc(a,b):
  z=bc(a[:4]+1j*a[4:],b[:4]+1j*b[4:]);return np.r_[z.real,z.imag]
 sol=solve_bvp(real_fun,real_bc,r,np.zeros((8,r.size)),tol=tol,max_nodes=120000)
 def field(r):
  y=sol.sol(r);return y[:4]+1j*y[4:]
 def flux(r):
  u,d,dd,ddd=field(r);h,_=hh(r)
  return w/2*np.imag((h-eta*w*w)*np.conj(u)*d+G*(np.conj(d)*dd-np.conj(u)*ddd))
 radii=np.linspace(10,end,200);fl=flux(radii);p=float(fl[-1]);x=np.linspace(1e-5,12,5000)
 chi=simpson(source(x)*field(x)[0],x=x)
 work=float(w/2*chi.imag)
 # All powers here are angular-normalized (physical spatial integral has 4pi).
 rhoFT=-k*k*np.exp(-k*k/2)
 analytic=w*k*rhoFT**2/(32*np.pi**2*G*(k*k+kap*kap))
 return dict(chi_real=float(chi.real),chi_imag=float(chi.imag),omega=w,outer=end,vacuum=vacuum,status=sol.status,background_status=bg.status,nodes=sol.x.size,power=p,work=work,work_residual=abs(work-p)/max(abs(p),1e-30),flux_variation=float(np.ptp(fl)/max(abs(p),1e-30)),vacuum_analytic=analytic,vacuum_error=abs(p/analytic-1) if vacuum else None,central_response=[float(field(.1)[0].real),float(field(.1)[0].imag)])
