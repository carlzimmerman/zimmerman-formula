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
pathlib.Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
