"""Analytic t=0 unseeded source derivative, checked by centered directional FD."""
import argparse,json
from pathlib import Path
import numpy as np
from sparse_absolute import SparseMidpoint
from fine_initial import fine_initial

ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args()
m=SparseMidpoint(eta=.01,material_h_kpc=.125,wave_R_kpc=10000.)
rows=[]
for case in ['formed','dilated']:
 a,x,chi,pi,meta=fine_initial(m,case,'nonlinear_transfer_2026_10_25/run_exact_equilibrium/state.npz')
 m.chi_override=None;m.rho_coupling=None
 mu=m.pot(a,x,True)[1];extra,S,bulk,conv,U,rate=m.transfer(a,x,chi);mu[0]+=extra
 Ha=(m.kd+mu)*a+m.J*m.alignment(a,x,chi)
 Ha[0,:-1]+=m.ko*U*a[0,1:];Ha[0,1:]+=m.ko*np.conj(U)*a[0,:-1]
 Ha[1,:-1]+=m.ko*a[1,1:];Ha[1,1:]+=m.ko*a[1,:-1]
 ad=-1j*Ha/m.sigma;psi=a[0]/np.sqrt(m.vol);pd=ad[0]/np.sqrt(m.vol)
 Dd=m.k*m.w*np.imag(np.conj(pd[:-1])*psi[1:]+np.conj(psi[:-1])*pd[1:])
 Bd=np.zeros(m.n);rho=abs(a[0])**2/m.vol
 Bd[:-1]+=Dd*m.g2/m.sigma*(-1.5*rho[:-1]+.5*rho[1:]);Bd[1:]+=Dd*m.g2/m.sigma*(1.5*rho[1:]-.5*rho[:-1])
 Gd=2*m.J/m.sigma*np.imag(np.conj(ad[0])*m.alignment(a,x,chi)[0]+np.conj(a[0])*m.alignment(ad,x,chi)[0])
 Cd=(m.g+2*m.g2*rho)*Gd;Sd=Bd+Cd
 fd=[]
 for eps in [1e-6,1e-7,1e-8]:
  s1=m.transfer(a+eps*ad,x,chi)[1];s0=m.transfer(a-eps*ad,x,chi)[1];fd.append({'epsilon_dimensionless_time':eps,'relative_error':float(np.linalg.norm((s1-s0)/(2*eps)-Sd)/np.linalg.norm(Sd))})
 def norm(v):return float(np.sqrt(np.sum(v*v/m.vol)))
 def poisson(v):
  prev=np.cumsum(v)-v
  return float(np.sum((v*v+2*v*prev)/m.r))
 rows.append({'case':case,'initial_diagnostics':m.diagnostics(a,x,chi,pi),'initial_meta':meta,'initial_source_norm':norm(S),'analytic_Sdot_norm':norm(Sd),'bulk_Sdot_norm':norm(Bd),'conversion_Sdot_norm':norm(Cd),'poisson_norm_squared_Sdot':poisson(Sd),'poisson_norm_squared_bulk':poisson(Bd),'poisson_norm_squared_conversion':poisson(Cd),'finite_difference_checks':fd,'outer_T_fraction_above70kpc':float(np.sum(abs(a[0,m.r*m.rm>70])**2)/np.sum(abs(a[:,m.r*m.rm>70])**2))})
Path(args.output).write_text(json.dumps({'domain':'actual radial model, t=0 acceleration, not a sustained emission calculation','cases':rows},indent=2)+'\n');print(json.dumps(rows,indent=2))
