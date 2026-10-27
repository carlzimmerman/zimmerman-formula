import argparse,json
from pathlib import Path
import numpy as np
from full import Full
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);arg=ap.parse_args();m=Full();s=np.load('nonlinear_transfer_2026_10_25/run_equilibrium/state.npz');a=s['a'].copy()*np.exp(.1j*np.sin(np.arange(m.n)))[None,:];x=s['alpha'];chi=s['chi'];Z=m.Z(a);p=np.sqrt(Z)*1e-3*np.cos(np.arange(m.n));d=.1*a*np.sin(np.arange(m.n))[None,:];h=1e-5
def Tk(a):return .5*sum(p*p/m.Z(a))
fd=(Tk(a+h*d)-Tk(a-h*d))/(2*h);u=m.enclosed(abs(a[0])**2);mu=-(2/np.pi)**2*m.ell2/m.c**2*m.transpose(.5*m.vol*(p/Z)**2*m.f(u)[3]);exact=2*np.real(sum(mu*np.conj(a[0])*d[0]));err=abs(fd-exact)/max(abs(fd),1e-25);assert err<1e-6
# Relative material phase makes the nonzero scalar source sign test meaningful.
a[0]*=np.exp(.3j);chidir=np.cos(m.wr*.1)*1e-3
def HA(ch):return m.J*np.real(np.sum(np.conj(a)*m.alignment(a,x,ch)))
fdc=(HA(chi+h*chidir)-HA(chi-h*chidir))/(2*h);rate=2*m.J/m.sigma*np.imag(np.conj(a[0])*m.alignment(a,x,chi)[0]);ex=m.g*sum(rate*m.chi_m(chidir));ec=abs(fdc-ex)/max(abs(fdc),1e-20);assert ec<1e-6
out={'carrier_inertia_density_force_relative_error':float(err),'scalar_source_sign_relative_error':float(ec),'short_steps':[]}
for dt_Myr in [.005,.0025,.00125]:
 a=s['a'].copy();x=s['alpha'].copy();chi=s['chi'].copy();pi=s['pi'].copy();p=np.zeros(m.n);E0=m.full_energy(a,x,p,chi,pi);Q0=m.wvol@pi+m.g*sum(abs(a[0])**2);sink=0;qs=0;maxe=0;maxq=0;maxfp=0;maxr=0
 for j in range(int(round(1/dt_Myr))):
  a,x,p,chi,pi,ds,dq,info=m.full_step(a,x,p,chi,pi,dt_Myr/m.tdyn);sink+=ds;qs+=dq;maxfp=max(maxfp,info['fixed_point_error']);maxr=max(maxr,info['carrier_root_residual']);maxe=max(maxe,abs(m.full_energy(a,x,p,chi,pi)+sink-E0));maxq=max(maxq,abs(m.wvol@pi+m.g*sum(abs(a[0])**2)+qs-Q0))
 ans={'dt_Myr':dt_Myr,'duration_Myr':1.,'max_energy_error':maxe,'max_charge_error':float(maxq),'max_fixed_point_error':maxfp,'max_carrier_root_error':maxr,'final':m.diagnostics(a,x,chi,pi)};out['short_steps'].append(ans);Path(arg.output).write_text(json.dumps(out,indent=2)+'\n');print(ans,flush=True)
