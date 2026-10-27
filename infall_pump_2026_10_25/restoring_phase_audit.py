import argparse,json,sys
from pathlib import Path
import numpy as np
sys.path.insert(0,'compression_current_2026_10_25')
from compression import Compression
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args();m=Compression(eta=.01,wave_R_kpc=10000.);s=np.load('nonlinear_transfer_2026_10_25/run_exact_equilibrium/state.npz');a=s['a'];x=s['alpha'];c=np.zeros(len(m.wr));v=c.copy();p=np.zeros(m.n);E0=m.full_energy(a,x,p,c,v);rho=abs(a[0])**2/m.vol;ph=np.array([.1*np.sin(m.r),.07*np.cos(m.r)]);dc=1e-6*np.exp(-(m.wr/20)**2);dp=1e-4*np.sqrt(m.Z(a))*np.exp(-(m.r/20)**2);cm=m.chi_m(dc);b=m.g2/m.sigma*(2*rho[1:]*cm[1:]-2*rho[:-1]*cm[:-1]-.5*(rho[1:]+rho[:-1])*np.diff(cm));beta=(m.g+2*m.g2*rho)*cm/m.sigma;psi=a.real/np.sqrt(m.vol);align=m.J*np.cos(x)*np.sin(x)*a[0].real*a[1].real
Q=float(.5*m.k*np.sum(m.w*(psi[0,:-1]*psi[0,1:]*(np.diff(ph[0])+b)**2+psi[1,:-1]*psi[1,1:]*np.diff(ph[1])**2))+np.sum(align*(ph[0]-ph[1]+beta)**2)+.5*np.sum(dp*dp/m.Z(a))+.5*m.c**2*np.sum(m.ww*np.diff(dc)**2));checks=[]
for eps in [.01,.003,.001]:
 ep=m.full_energy(a*np.exp(1j*eps*ph),x,eps*dp,eps*dc,v);em=m.full_energy(a*np.exp(-1j*eps*ph),x,-eps*dp,-eps*dc,v);fd=(ep+em-2*E0)/(2*eps*eps);checks.append({'epsilon':eps,'energy_quadratic_coefficient':fd,'relative_error':abs(fd-Q)/Q})
constant=1e-6;gphase=np.zeros_like(ph);gphase[0]=-(m.g+2*m.g2*rho)*constant/m.sigma;Eg=m.full_energy(a*np.exp(1j*gphase),x,p,c+constant,v);old=json.loads(Path('nonlinear_transfer_2026_10_25/run_restoring/results.json').read_text());out={'quadratic_phase_energy':Q,'minimum_alignment_coefficient':float(np.min(align)),'checks':checks,'exact_shift_gauge_energy_error':Eg-E0,'inherited_active_density_min_eigenvalue':old['minimum_scaled_constrained_H_eigenvalue'],'inherited_relaxed_boundary_stiffness_Eunit_per_kpc2':old['relaxed_boundary_stiffness_Eunit_per_kpc2'],'scope':'Coherent active finite-grid equilibrium only. Full infall boundary restoration is not established by this block argument.'};Path(args.output).write_text(json.dumps(out,indent=2)+'\n');print(out)
assert np.min(align)>-1e-15 and Q>0
assert min(z['relative_error'] for z in checks)<1e-5 and abs(Eg-E0)<1e-11
assert old['minimum_scaled_constrained_H_eigenvalue']>0
