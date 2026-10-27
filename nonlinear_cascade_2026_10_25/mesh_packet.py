"""Unitary packet propagation distinguishes mesh trapping from physical loss."""
import argparse,json
from pathlib import Path
import numpy as np
from scipy.linalg import solve_banded
from fine_material import FineMaterial
from physical_branch import PhysicalFull
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args();rows=[]
for h in [None,.125,.0625]:
 m=PhysicalFull() if h is None else FineMaterial(material_h_kpc=h);j=np.argmin(abs(m.r*m.rm-60));spacing=(m.r[j+1]-m.r[j])*m.rm;d=spacing/m.rm;lam=1.;k=2/d*np.arcsin(np.sqrt(lam*d*d/(2*m.k)));a=np.sqrt(m.vol)*np.exp(-.5*((m.r*m.rm-60)/3)**2)*np.exp(1j*k*m.r);a/=np.linalg.norm(a);E0=np.real(np.vdot(a,m.kd*a))+2*np.real(np.sum(m.ko*np.conj(a[:-1])*a[1:]));dt=.02/m.tdyn;fac=1j*dt/(2*m.sigma);ab=np.zeros((3,m.n),complex);ab[0,1:]=fac*m.ko;ab[1]=1+fac*m.kd;ab[2,:-1]=fac*m.ko
 for step in range(12500):
  rhs=(1-fac*m.kd)*a;rhs[:-1]-=fac*m.ko*a[1:];rhs[1:]-=fac*m.ko*a[:-1];a=solve_banded((1,1),ab,rhs,check_finite=False)
 E1=np.real(np.vdot(a,m.kd*a))+2*np.real(np.sum(m.ko*np.conj(a[:-1])*a[1:]));rows.append({'h_kpc':h,'n':m.n,'time_Myr':250.,'outward_mass_beyond90kpc':float(sum(abs(a[m.r*m.rm>90])**2)),'outward_mass_beyond120kpc':float(sum(abs(a[m.r*m.rm>120])**2)),'mean_radius_kpc':float(np.sum(abs(a)**2*m.r*m.rm)),'mass_error':float(abs(sum(abs(a)**2)-1)),'energy_error':float(abs(E1-E0)),'initial_packet_energy':float(E0)})
out={'rows':rows,'scope':'Free positive radial material-gradient operator only. Local packet energy matched, global mass and energy conserved. Demonstrates numerical propagation capability, not galaxy formation or full Bogoliubov transmission.'};Path(args.output).write_text(json.dumps(out,indent=2)+'\n');print(out)
