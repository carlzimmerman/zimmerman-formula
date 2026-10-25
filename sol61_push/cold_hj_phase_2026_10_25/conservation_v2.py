"""Independent unitary-gauge and shared-wave energy-partition audit."""
import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='1'
import json,pathlib,sys,numpy as np,sympy as sp
from adaptive_v2 import Grid,DynamicAxis
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent.parent/'cold_conservative_phase_2026_10_24'))
from solver import Evolve
# Symbolic Fisher-information partition identity, arbitrary positive rho and0<f<1.
r,f,rp,fp=sp.symbols('rho f rho_prime f_prime',real=True,nonzero=True)
expr=(f*rp+r*fp)**2/(r*f)+((1-f)*rp-r*fp)**2/(r*(1-f))-rp**2/r-r*fp**2/(f*(1-f))
symbolic=sp.factor(expr);assert symbolic==0
# Finite-box one-source gravitational cross energy, and analytic-gradient wave partition.
g=Grid(16,6,1.5);eta=.2;x,y,z=g.xyz;rho=np.exp(-x*x-2*y*y-.5*z*z);rho/=np.sum(rho*g.vol);frac=1/(1+np.exp(-2*x));grad=[-2*x*rho,-4*y*rho,-z*rho];df=2*frac*(1-frac)
quant=lambda rr,gg:eta**2/8*sum(v*v for v in gg)/rr
full=quant(rho,grad);qc=rho*frac;qe=rho*(1-frac);gc=[frac*v for v in grad];ge=[(1-frac)*v for v in grad];gc[0]+=rho*df;ge[0]-=rho*df
split=quant(qc,gc)+quant(qe,ge);interface=eta**2/8*rho*df*df/(frac*(1-frac));interface_integral=float(np.sum(interface*g.vol))
mc=qc*g.vol;me=qe*g.vol;m=mc+me;pc=g.poisson(mc);pe=g.poisson(me);pt=g.poisson(m)
W=float(.5*np.sum(m*pt));Wparts=float(.5*np.sum(mc*pc)+.5*np.sum(me*pe)+np.sum(mc*pe));wrongW=float(.5*np.sum(mc*pc)+.5*np.sum(me*pe)+2*np.sum(mc*pe))
# Exact discrete gauge covariance: transformed hopping coefficients and local phases.
g=Grid(12,6,1.5);x,y,z=g.xyz;eta=.2;dt=.02;zeros=[np.zeros_like(g.r) for _ in range(3)];base=Evolve(g,eta,zeros,dt);u=np.exp(-g.r*g.r/2+1j*.2*x*y)*g.sv;u/=np.linalg.norm(u);q=abs(u)**2*(x>0);phi=g.poisson(abs(u)**2)
ref,qr,pr,_=base.step(u.copy(),q.copy(),phi.copy());theta0=np.zeros_like(x);thetaM=.5*dt*25*(x**3/4+y*y+.3*np.sin(z));thetaN=2*thetaM;ug=u*np.exp(-1j*thetaM);ug*=np.exp(-1j*dt/(2*eta)*phi);qg=q.copy()
for k in (0,1,2,1,0):
 op=DynamicAxis(g,eta,zeros[k],k,dt*(1 if k==2 else .5));th=np.moveaxis(thetaM,k,0);op.h*=np.exp(-1j*th[:-1]+1j*th[1:]);op.set_tau(op.tau);ug,qg,e=op.apply(ug,qg)
pnew=g.poisson(abs(ug)**2);ug*=np.exp(-1j*dt/(2*eta)*pnew);ug*=np.exp(1j*(thetaM-thetaN));physical=ug*np.exp(1j*thetaN)
out=dict(symbolic_partition_residual=str(symbolic),partition_gradient_error=float(np.max(abs(split-full-interface))),interface_energy=interface_integral,gravity_cross_energy_error=abs(Wparts-W),double_counted_cross_energy_error=abs(wrongW-W),gauge_wave_error=float(np.linalg.norm(physical-ref)),gauge_tag_error=float(np.max(abs(qg-qr))),gauge_energy_error=float(abs(base.energy(physical,pnew)-base.energy(ref,pr))))
# Interface integral was computed on the first grid; retain its exact weights separately.
assert out['partition_gradient_error']<1e-12 and out['gravity_cross_energy_error']<1e-12
assert out['double_counted_cross_energy_error']>1e-4
assert out['gauge_wave_error']<1e-12 and out['gauge_tag_error']<1e-12 and out['gauge_energy_error']<1e-12
# Exact instantaneous self-consistent polynomial Schrödinger/Poisson jet.
xx,yy,zz=sp.symbols('x y z',real=True);cs=[xx,yy,zz];ee=sp.Rational(1,5)
lap=lambda a:sum(sp.diff(a,c,2) for c in cs)
def inverse_lap(source):
 result=0;term=sp.expand(source)
 for _ in range(12):
  if term==0:return sp.expand(result)
  part=sp.integrate(sp.integrate(term,xx),xx);result+=part;term=sp.expand(-sp.diff(part,yy,2)-sp.diff(part,zz,2))
 raise AssertionError('polynomial Poisson inversion failed')
u0=1+xx+xx*yy+zz**2;v0=xx**2/3-yy*zz;rho0=u0*u0+v0*v0;phi0=inverse_lap(4*sp.pi*rho0)
ut=-ee*lap(v0)/2+phi0*v0/ee;vt=ee*lap(u0)/2-phi0*u0/ee;rhot=sp.expand(2*(u0*ut+v0*vt));phit=inverse_lap(4*sp.pi*rhot)
K_t=ee**2*sum(sp.diff(u0,c)*sp.diff(ut,c)+sp.diff(v0,c)*sp.diff(vt,c) for c in cs)
e_t=K_t+rhot*phi0+rho0*phit+sum(sp.diff(phi0,c)*sp.diff(phit,c) for c in cs)/(4*sp.pi)
flux_div=sum(sp.diff(ee**2*(ut*sp.diff(u0,c)+vt*sp.diff(v0,c))+phit*sp.diff(phi0,c)/(4*sp.pi),c) for c in cs)
energy_res=sp.expand(e_t-flux_div)
T=[[ee**2*(sp.diff(u0,ci)*sp.diff(u0,cj)+sp.diff(v0,ci)*sp.diff(v0,cj))-ee**2/4*(lap(rho0) if i==j else 0)+(sp.diff(phi0,ci)*sp.diff(phi0,cj)-(sum(sp.diff(phi0,c)**2 for c in cs)/2 if i==j else 0))/(4*sp.pi) for j,cj in enumerate(cs)] for i,ci in enumerate(cs)]
momentum=[]
for i,c in enumerate(cs):
 jt=ee*(ut*sp.diff(v0,c)+u0*sp.diff(vt,c)-vt*sp.diff(u0,c)-v0*sp.diff(ut,c));momentum.append(sp.expand(jt+sum(sp.diff(T[i][j],cs[j]) for j in range(3))))
out['local_polynomial_energy_residual']=str(energy_res);out['local_polynomial_momentum_residuals']=[str(v) for v in momentum];out['symmetric_stress']=all(sp.expand(T[i][j]-T[j][i])==0 for i in range(3) for j in range(3))
assert energy_res==0 and all(v==0 for v in momentum) and out['symmetric_stress']
pathlib.Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
