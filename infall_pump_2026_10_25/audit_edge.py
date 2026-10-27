import argparse,json
from pathlib import Path
import numpy as np
from split_engine import Split
from volume_initial import fine_initial
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args();m=Split(eta=.01,material_h_kpc=.125,wave_R_kpc=10000.)
a,x,c,v,meta=fine_initial(m,'dilated','nonlinear_transfer_2026_10_25/run_exact_equilibrium/state.npz');a*=np.exp(1j*np.array([.03*np.sin(m.r),.02*np.cos(m.r)]));c=1e-5*np.exp(-(m.wr/6)**2);v=1e-3*np.exp(-(m.wr/6)**2)
def edge_energy(a):
 i=m.edge_sets[0];j=i+1;rho=abs(a[0])**2/m.vol;cm=m.true_chi_m(c);h=m.g+m.g2*(rho[i]+rho[j])/2;U=np.exp(-1j*h*(cm[j]-cm[i])/m.sigma);psi=a/np.sqrt(m.vol)
 return float(m.k/2*np.sum(m.w[i]*(abs(U*psi[0,j]-psi[0,i])**2+abs(psi[1,j]-psi[1,i])**2)))
E0=edge_energy(a);M0=np.sum(abs(a)**2);Q0=m.charge(a,v);an,vn,w,fw=m.edge_flow(a,c,v,.02/m.tdyn,0)
i=m.edge_sets[0];j=i+1;cm=m.true_chi_m(c);rho=abs(a[0])**2/m.vol;h=m.g+m.g2*(rho[i]+rho[j])/2;U=np.exp(-1j*h*(cm[j]-cm[i])/m.sigma);psi=a/np.sqrt(m.vol);D=m.k*m.w[i]*np.imag(np.conj(psi[0,i])*U*psi[0,j]);md=-m.g2*D*(cm[j]-cm[i])/(2*m.sigma)
H=np.zeros_like(a);H[:,i]=m.k*m.w[i]/(2*m.vol[i])*a[:,i];H[:,j]=m.k*m.w[i]/(2*m.vol[j])*a[:,j];ko=-m.k*m.w[i]/(2*np.sqrt(m.vol[i]*m.vol[j]));H[0,i]+=ko*U*a[0,j]+md/m.vol[i]*a[0,i];H[0,j]+=ko*np.conj(U)*a[0,i]+md/m.vol[j]*a[0,j];H[1,i]+=ko*a[1,j];H[1,j]+=ko*a[1,i];ad=-1j*H/m.sigma;massdot=2*np.real(np.conj(a[0])*ad[0]);Pdot=np.zeros(m.n);Pdot[i]=-h*D/m.sigma;Pdot[j]=h*D/m.sigma;vd=m.deposit(Pdot-(m.g+2*m.g2*rho)*massdot)/m.wvol
checks=[]
for eps in [1e-6,1e-7,1e-8]:
 ap1,vp,_,_=m.edge_flow(a,c,v,eps,0);am1,vm,_,_=m.edge_flow(a,c,v,-eps,0)
 checks.append({'epsilon':eps,'material_derivative_relative_error':float(np.linalg.norm((ap1-am1)/(2*eps)-ad)/np.linalg.norm(ad)),'scalar_derivative_relative_error':float(np.linalg.norm((vp-vm)/(2*eps)-vd)/np.linalg.norm(vd))})
out={'edge_energy_defect':edge_energy(an)-E0,'mass_defect':float(np.sum(abs(an)**2)-M0),'charge_defect':m.charge(an,vn)-Q0,'derivative_checks':checks}
g2=m.g2;m.g2=0.;az,vz,_,_=m.edge_flow(a,c,v,.02/m.tdyn,0);out['g2_zero_max_bulk_pi_kick']=float(np.max(abs(vz-v)));m.g2=g2
Path(args.output).write_text(json.dumps(out,indent=2)+'\n');print(out)
assert abs(out['edge_energy_defect'])<1e-12
assert abs(out['mass_defect'])<1e-12 and abs(out['charge_defect'])<1e-9
assert min(z['material_derivative_relative_error'] for z in checks)<1e-6
assert min(z['scalar_derivative_relative_error'] for z in checks)<1e-4
