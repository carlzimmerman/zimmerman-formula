"""CE-FM-002: full saturating discrete force, energy and short local evolution.
G=a0=M_b=1. Fixed core .2, reflecting inner radius .5: u_core=.8<1.
No formation-attractor or long-term convergence claim.
"""
import json
import sys
from pathlib import Path
import numpy as np

N, CORE, RMIN, RMAX = 256, .2, .5, 50.
DM = ((np.sqrt(1+4*RMAX**2)-1)/2-CORE)/N
MIN = CORE+DM*np.arange(N)
MAX = MIN+DM
checks=[]
def check(name, cond, detail):
    checks.append(dict(name=name,passed=bool(cond),detail=detail))
    if not cond: raise AssertionError(name)

def w(x):
    x=np.asarray(x)
    if np.any(x>=1): raise ValueError('outside full saturation domain')
    val=np.empty_like(x)
    small=x<.05
    val[small]=sum(x[small]**n/n for n in range(3,25))
    val[~small]=-x[~small]**2/2-x[~small]-np.log1p(-x[~small])
    return val

def accel(r):
    o=np.argsort(r); rs=r[o]
    ui,uo=MIN/rs**2,MAX/rs**2
    # Exact derivative of piecewise enclosed-mass field energy.
    av=(w(uo)-w(ui))/(uo-ui)
    a=np.empty_like(r); a[o]=-1/rs**2+av
    return a

def energy(r,v,nq=128):
    rs=np.sort(r)
    # q=1/r: field energy int r^2 w(m/r^2)dr becomes int w(m q^2)/q^4 dq.
    nodes,weights=np.polynomial.legendre.leggauss(nq)
    bounds=np.concatenate(([0.],1/rs[::-1],[1/RMIN]))
    mass=np.concatenate((MAX[::-1],[CORE]))
    lo,hi=bounds[:-1],bounds[1:]
    q=(hi+lo)[:,None]/2+(hi-lo)[:,None]*nodes[None,:]/2
    integrals=(hi-lo)/2*np.sum(weights[None,:]*w(mass[:,None]*q*q)/q**4,axis=1)
    return float(.5*DM*np.sum(v*v)-DM*np.sum(1/r)+np.sum(integrals))

# Discrete equilibrium: solve exact averaged finite-shell force, without using r=m.
lo=np.sqrt(MAX)*(1+1e-12); hi=np.maximum(MAX+2,2*lo)
for unused in range(120):
    mid=(lo+hi)/2
    # Here ranks are known; no sort during root finding.
    ui,uo=MIN/mid**2,MAX/mid**2
    f=-1/mid**2+(w(uo)-w(ui))/(uo-ui)
    lo=np.where(f>0,mid,lo); hi=np.where(f>0,hi,mid)
r=(lo+hi)/2; v=np.zeros(N)
check('equilibrium domain',np.all(r>RMIN) and np.all(MAX/r**2<1),float(np.max(MAX/r**2)))
check('equilibrium positive shell ordering',np.all(np.diff(r)>0),float(np.min(np.diff(r))))
check('equilibrium force balance',np.max(np.abs(accel(r))*r*r)<1e-10,float(np.max(np.abs(accel(r))*r*r)))

r_test=r*(1+.01*np.exp(-r/10))
e128=energy(r_test,v,128);e256=energy(r_test,v,256)
check('quadrature agreement',abs(e128-e256)<1e-10,abs(e128-e256))
fdrows=[]
for i in (0,12,100,255):
    h=1e-4*r_test[i]
    plus=r_test.copy();minus=r_test.copy();plus[i]+=h;minus[i]-=h
    fd=-(energy(plus,v)-energy(minus,v))/(2*h*DM)
    analytic=accel(r_test)[i]
    err=abs(fd-analytic)/max(1/r_test[i]**2,abs(analytic))
    check(f'force from energy shell {i}',err<2e-6,err)
    fdrows.append(dict(shell=i,force=analytic,finite_difference=fd,normalized_error=err))

# Short equilibrium and tiny displacement tests at two resolutions. No reflecting collision is allowed.
def evolve(start,dt,tend=20.):
    rr=start.copy();vv=np.zeros(N);e0=energy(rr,vv);a=accel(rr);minmargin=1.
    for unused in range(round(tend/dt)):
        vv+=.5*dt*a;rr+=dt*vv
        if np.any(rr<=RMIN):raise ValueError('boundary impulse invalidates local test')
        a=accel(rr);vv+=.5*dt*a
        minmargin=min(minmargin,float(np.min(1-MAX/np.sort(rr)**2)))
    return rr,vv,dict(dt=dt,time=tend,energy_absolute_error=abs(energy(rr,vv)-e0),
                     maximum_relative_displacement=float(np.max(np.abs(rr/start-1))),minimum_wall_margin=minmargin)

req,veq,eq=evolve(r,.004)
check('equilibrium maintained',eq['maximum_relative_displacement']<1e-9,eq)
perturbed=r*(1+.0005*np.exp(-r/10))
r1,v1,coarse=evolve(perturbed,.004)
r2,v2,fine=evolve(perturbed,.002)
check('perturbed energy conservation',fine['energy_absolute_error']<1e-8,fine)
check('trajectory resolution agreement',np.max(np.abs(r1-r2)/r)<1e-6,float(np.max(np.abs(r1-r2)/r)))
check('resolution improves energy error',fine['energy_absolute_error']<.4*coarse['energy_absolute_error'],{'coarse':coarse,'fine':fine})

result=dict(checks=checks,N=N,core=CORE,inner_boundary=RMIN,initial_core_u=CORE/RMIN**2,
            finite_difference_controls=fdrows,equilibrium=eq,coarse=coarse,fine=fine,
            scope='Local full-force discretization and short admissible trajectories only; not formation or global stability.')
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
