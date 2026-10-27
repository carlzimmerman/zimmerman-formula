import argparse,json
from pathlib import Path
import numpy as np,torch
from scipy.linalg import null_space
from latent_verify import model
from joint import T
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();r=json.loads(Path('boundary_resolution_2026_10_25/run_latent_verify/base_0.125.json').read_text());m=model(.125);n=m.n;v=np.r_[r['mass'],r['v'][n:]];zz=T(v).requires_grad_(True);H=torch.autograd.functional.hessian(lambda b:m.energy(torch.log(b[:n]),b[n:]),zz).detach().numpy();im=np.where(v[:n]>1e-8)[0];P0=null_space(np.ones((1,len(im))));P=np.zeros((2*n,len(im)-1));P[im]=P0;Z=np.c_[P,np.eye(2*n)[:,n:]];ev=np.linalg.eigvalsh(Z.T@H@Z)
# Independent finite differences of full mass/phase force in a physical tangent.
d=np.r_[np.array(r['mass'])*np.cos(np.arange(n)),.1*np.sin(np.arange(n))];d[:n]-=np.array(r['mass'])*sum(d[:n])/sum(r['mass']);err=[]
for dt in [1e-6,3e-7,1e-7]:
 fd=(m.direct(v+dt*d)[1]-m.direct(v-dt*d)[1])/(2*dt);err.append(float(max(abs(fd-H@d))/max(1,max(abs(H@d)))))
# Independent species finite differences of local phase-volume and binding term.
B=m.volume_cost;eps=m.eps;species=[]
def e(t,f):return t/(t+f)*(B-eps*(t+f))
for rho,q in [(.04,.9),(.003,.5),(.0001,.01)]:
 t=rho*q;f=rho*(1-q);dt=rho*1e-6;fdT=(e(t+dt,f)-e(t-dt,f))/(2*dt);fdF=(e(t,f+dt)-e(t,f-dt))/(2*dt);species.append(max(abs(fdT-(-eps+B*(1-q)/rho)),abs(fdF+B*q/rho)))
# Pure F conversion-seed Hessian is independent of the prepared converted branch.
x=T(np.zeros(n)).requires_grad_(True);z=T(np.log(r['mass']));HF=torch.autograd.functional.hessian(lambda xx:m.energy(z,xx),x).detach().numpy();rho=np.array(r['mass'])/m.vol.numpy();expected=np.pi**2/2*m.vol.numpy()*(B-rho*(eps+2.5*m.K*rho**(2/3)));phaseerr=float(max(abs(np.diag(HF)-expected))/max(1,max(abs(expected))));offdiag=float(max(abs(HF-np.diag(np.diag(HF)))).max());outer=np.array(r['r'])>1.2*r['interpolated_crossings_kpc'][-1]
out=dict(full_phase_active_mass_tangent_minimum_eigenvalue=float(ev[0]),full_phase_variables=n,active_mass_variables=len(im),mass_cutoff=1e-8,hessian_directional_errors=err,local_species_chemical_potential_errors=species,all_F_seed_hessian_relative_error=phaseerr,all_F_seed_hessian_offdiagonal_max=offdiag,all_F_outer_seed_minimum_coefficient=float(min(expected[outer])),all_F_negative_seed_radii_kpc=np.array(r['r'])[expected<0].tolist(),qualification='All-F seed diagnostic uses candidate density, not independent all-F hydrostatic equilibrium or time evolution. Full phase radial Hessian positivity is local only; microscopic floor mass directions are excluded.')
assert min(ev)>0 and max(err)<1e-6 and max(species)<1e-7 and phaseerr<1e-10 and offdiag<1e-10 and min(expected[outer])>0
Path(a.output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='all_F_negative_seed_radii_kpc'},indent=2))
