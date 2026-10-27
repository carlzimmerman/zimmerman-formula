import argparse,json
from pathlib import Path
import numpy as np
from hydro import Hydro
p=argparse.ArgumentParser();p.add_argument('--output');a=p.parse_args();checks=[]
def ck(n,v,t):checks.append(dict(name=n,value=float(v),tolerance=t,passed=bool(v<t)))
m=Hydro(128,0,xe=0);U=np.array([np.ones(m.n),np.zeros(m.n),np.ones(m.n)/(m.gamma-1)]);rhs,h=m.gas_rhs(U,1,0,np.zeros(m.n-1));ck('homogeneous_pressure_balance',np.max(abs(rhs)),1e-10)
U[2]=np.where(m.r<m.R/2,1,.1)/(m.gamma-1);initial=U.copy();mass0=np.sum(m.vol*U[0]);en0=np.sum(m.vol*U[2]);entropy=lambda U:np.sum(m.vol*U[0]*np.log(m.primitive(U)[2]/U[0]**m.gamma));s0=entropy(U);t=0;end=.1*m.R
steps=0
while t<end:
 rho,v,pres,cs=m.primitive(U);dt=min(.2*m.dx/max(abs(v)+cs),end-t);f,_=m.gas_rhs(U,1,0,np.zeros(m.n-1));trial=U+dt*f;fn,_=m.gas_rhs(trial,1,0,np.zeros(m.n-1));U=.5*(U+trial+dt*fn);m.primitive(U);t+=dt;steps+=1
ck('shock_mass',abs(np.sum(m.vol*U[0])/mass0-1),1e-12);ck('shock_energy',abs(np.sum(m.vol*U[2])/en0-1),1e-12);ck('entropy_not_decreased',max(0,s0-entropy(U)),1e-12)
# Adjoint gas-flux gravitational power: finite difference potential energy under a mass-only update.
m=Hydro(64,.03,xe=0);U=m.initial_gas();xc=m.x0;A=2.;rc,ic,dc,dr,g,phi=m.gravity(xc,U,A);du,_=m.gas_rhs(U,A,0,g);eps=1e-8
potential=lambda U:.5*A**3*np.sum(m.vol*m.gravity(xc,U,A)[3]*m.gravity(xc,U,A)[5])
up=U.copy();um=U.copy();up[0]+=eps*du[0];um[0]-=eps*du[0];fd=(potential(up)-potential(um))/(2*eps);du0,_=m.gas_rhs(U,A,0,np.zeros(m.n-1));power=np.sum(m.vol*(du[2]-du0[2]));ck('gas_gravity_work',abs(fd+power)/max(abs(fd),1e-30),1e-5)
Path(a.output).write_text(json.dumps(dict(checks=checks,shock_steps=steps,entropy_change=float(entropy(U)-s0) if False else None),indent=2)+'\n')
