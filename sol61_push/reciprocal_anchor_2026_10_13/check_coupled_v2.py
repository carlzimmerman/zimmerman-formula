import json,sys
from pathlib import Path
import numpy as np
import sympy as sy
from scipy.integrate import solve_bvp,simpson
from scipy.special import gammainc

checks=[]
def check(name,c,detail=''):
    checks.append(dict(name=name,passed=bool(c),detail=str(detail)))
    if not c:raise AssertionError(name+': '+str(detail))
r,m,q,M,B,S=sy.symbols('r m q Mb B S',positive=True)
u=(m-q)/r**2
w=-u-sy.log(1-u)
energy=-(M*m+m*m/2)/r**2+r*r*w
du=sy.simplify(sy.diff(energy,m))
check('physical carrier force variation',sy.simplify(du+(M+m)/r**2-u/(1-u))==0,du)
check('reference force variation',sy.simplify(sy.diff(energy,q)+u/(1-u))==0,sy.diff(energy,q))
check('carrier convex at fixed reference',sy.simplify(sy.diff(energy,m,2)-(1/(1-u)**2-1)/r**2)==0,'positive for0<u<1')
A,L=sy.symbols('A L',positive=True)
d=A*(r+L)*sy.exp(-r/L)
check('exterior decaying linear deficit',sy.simplify(sy.diff(d,r,2)-2*sy.diff(d,r)/r-d/L**2)==0,d)
nt=-sy.diff(d,r)/r**2
check('exterior density tail',sy.simplify(nt-A*sy.exp(-r/L)/(L*r))==0,nt)
check('exterior mass tail',sy.simplify(sy.integrate(nt*r*r,(r,r,sy.oo))-d)==0,d)

Sval=5.364;rmin=1e-5
def baryon(x):return np.minimum(x**3,1.)
def profiles(x,qr):
    # Smooth-enough extension for nonlinear solver trials; final domains checked separately.
    qq=np.clip(qr,0.,Sval);Q=baryon(x)+qq
    root=2*Q*x*x/(np.sqrt(Q*Q+4*Q*x*x)+Q)
    mm=np.minimum(qq+root,Sval)
    uv=(mm-qq)/(x*x)
    return mm,uv,uv/(1-uv)

rows=[]
previous=None
for beta in [100.,10.,1.,.1,.05,.02,.01]:
  ell=np.sqrt(beta);Rout=max(50.,15*ell)
  x=np.unique(np.r_[np.geomspace(rmin,Rout,500),1.])
  scale=max(ell,.05)
  initialq=Sval*gammainc(3,x/scale)
  initialn=Sval*np.exp(-x/scale)/(2*scale**3)
  if previous is not None:
    ratio=previous_ell/ell
    yy=previous.sol(np.minimum(x*ratio,previous.x[-1]))
    initialq=yy[0];initialn=yy[1]*ratio**3
  def fun(x,y):
    _,_,force=profiles(x,y[0]);return np.array([x*x*y[1],-force/beta])
  def bc(a,z):
    return np.array([a[0]-a[1]*rmin**3/3,z[1]-(Sval-z[0])/(ell*Rout*(Rout+ell))])
  sol=solve_bvp(fun,bc,x,np.array([initialq,initialn]),tol=2e-6,max_nodes=20000)
  check('coupled BVP '+str(beta),sol.success,sol.message)
  grid=np.unique(np.r_[np.geomspace(rmin,Rout,4000),1.])
  qr,den=sol.sol(grid);mm,uv,force=profiles(grid,qr)
  check('reference physical domain '+str(beta),min(qr)>-1e-7 and max(qr)<=Sval+1e-7 and min(den)>-1e-8,(min(qr),max(qr),min(den)))
  check('actual physical domain '+str(beta),np.all(mm>=qr-1e-7) and np.all(mm<=Sval+1e-7) and min(uv)>=-1e-8 and max(uv)<1,(min(uv),max(uv)))
  check('physical mass monotonic '+str(beta),min(np.diff(mm))>=-1e-7,min(np.diff(mm)))
  g=(baryon(grid)+mm)/(grid*grid)
  interior=mm<Sval-1e-6
  residual=force-g
  check('carrier interior force '+str(beta),max(abs(residual[interior])/(1+g[interior]))<1e-9,max(abs(residual[interior])))
  check('carrier cap variational inequality '+str(beta),max(residual[~interior])<1e-6,max(residual[~interior]))
  eq=sol.sol(grid,1)-fun(grid,sol.sol(grid))
  eqnorm=max(np.max(abs(eq[0])/(1+abs(grid*grid*den))),np.max(abs(eq[1])/(1+abs(force/beta))))
  check('reference residual '+str(beta),eqnorm<2e-5,eqnorm)
  integral=float(simpson(grid*grid*den,x=grid))
  deficit=float(Sval-qr[-1]);ledger=integral+float(qr[0])+deficit
  check('reference mass quadrature '+str(beta),abs(ledger-Sval)<2e-4,(ledger,deficit))
  # Vacuum starts when unconstrained carrier optimum reaches supply.
  inds=np.flatnonzero(mm>=Sval-1e-8)
  edge=float(grid[inds[0]]) if len(inds) else None
  controls=[]
  for radius in [1.,2.,5.,10.,20.]:
    qq=float(sol.sol(radius)[0]);actual=float(profiles(np.array([radius]),np.array([qq]))[0][0])
    gg=(float(baryon(radius))+actual)/radius**2
    gb=float(baryon(radius))/radius**2
    goal=(gb+np.sqrt(gb*gb+4*gb))/2
    controls.append(dict(r=radius,reference_mass=qq,carrier_mass=actual,physical_g_over_baryon_law=gg/goal,below_carrier_cap=actual<Sval-1e-8))
  previous=sol;previous_ell=ell
  rows.append(dict(B=beta,outer_radius=Rout,nodes=len(sol.x),equation_residual=eqnorm,reference_mass_ledger=ledger,outer_mass_deficit=deficit,carrier_edge_sample=edge,central_reference_density=float(den[0]),controls=controls))
out=dict(checks=checks,cases=rows,scope='Conditional NR constrained equilibrium; trial extension clipped q, all accepted domains checked. No covariant vacuum boundary, coupled stability, physical EOS selection or observational score.')
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(dict(checks=len(checks),cases=rows),indent=2))
