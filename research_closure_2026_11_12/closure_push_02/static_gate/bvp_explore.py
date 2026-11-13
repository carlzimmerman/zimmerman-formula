import numpy as np
from scipy.integrate import solve_bvp,cumulative_trapezoid


def svals(u):
    v=np.clip(u,-2.,15.)
    S=np.exp(-v**3)
    return S,-3*v*v*S,(9*v**4-6*v)*S


def solve(m,ell=.2,d=.01,previous=None):
    r=np.geomspace(.001,60.,250)
    bsoft=.5
    b=3*bsoft*bsoft/(r*r+bsoft*bsoft)**2.5
    gn=r/(r*r+bsoft*bsoft)**1.5
    y=(gn+np.sqrt(gn*gn+4*gn))/2
    p=y/(1+y)
    f=-r[-1]*y[-1]-np.flip(cumulative_trapezoid(np.flip(y),-np.flip(r),initial=0))
    Z=np.gradient(p,r)+2*p/r
    z0=np.vstack((f,y,p,Z)) if previous is None else previous.sol(r)
    def fun(x,z):
        f,y,p,Z=z
        S,Sp,Spp=svals(Z/d)
        D=ell*ell/2-m*m*f*f/(2*d*d)*Spp
        b=3*bsoft*bsoft/(x*x+bsoft*bsoft)**2.5
        denom=1-p
        return np.vstack((y,b+Z-m*m*f*S-2*y/x,Z-2*p/x,(p/denom-y+m*m*f*y*Sp/d)/D))
    def bc(a,b):return np.array([a[1],a[2],b[0]+r[-1]*y[-1],b[2]-p[-1]])
    sol=solve_bvp(fun,bc,r,z0,tol=1e-5,max_nodes=12000)
    z=sol.sol(np.geomspace(.001,60.,2000));ff,yy,pp,ZZ=z
    D=ell*ell/2-m*m*ff*ff/(2*d*d)*svals(ZZ/d)[2]
    return sol,dict(m=m,status=int(sol.status),message=sol.message,nodes=len(sol.x),residual=float(np.max(sol.rms_residuals)),Dmin=float(np.min(D)),pmin=float(pp.min()),pmax=float(pp.max()),fmin=float(ff.min()),fmax=float(ff.max()))

if __name__=='__main__':
 import json
 old=None
 for m in [0,1e-5,1e-4,3e-4,1e-3]:
  sol,d=solve(m,previous=old)
  print(json.dumps(d),flush=True)
  if sol.status==0:old=sol
