import argparse,json
from pathlib import Path
import numpy as np,torch
from scipy.linalg import null_space
from latent_stiff import LatentStiff
from fast_complete import finish
from surface_checked import transfer_species
from joint_recovery import moved
from joint import T

def model(h,domain=12):
 m=LatentStiff(domain=domain,beta=4,K=30,charge=0,L=0,eta=0,sigma=0,eps=.3,h=h,volume_cost=.001,material_length=.25);m.ell2=(3*np.sqrt(.5)/m.rm)**2;return m

def hessian(m,r):
 n=m.n;v=np.r_[r['mass'],r['v'][n:]];z=T(v).requires_grad_(True);H=torch.autograd.functional.hessian(lambda a:m.energy(torch.log(a[:n]),a[n:]),z).detach().numpy();im=np.where(v[:n]>1e-8)[0];ix=np.where((v[n:]>1e-7)&(v[n:]<1-1e-7))[0]+n;P0=null_space(np.ones((1,len(im))));P=np.zeros((2*n,len(im)-1));P[im]=P0;X=np.eye(2*n)[:,ix];Z=np.c_[P,X];HH=Z.T@H@Z;ev=np.linalg.eigvalsh(HH);end=np.where((v[n:]<=1e-7)|(v[n:]>=1-1e-7))[0];neg=end[np.diag(H)[n:][end]<-1e-8];rad=np.array(r['r']);q=np.array(r['q']);i=np.where((q[:-1]-.5)*(q[1:]-.5)<0)[0][-1];dr=rad[i+1]-rad[i];hp=np.pi/2*np.sin(np.pi*v[n:]);C=np.zeros(2*n);C[n+i]=dr*(.5-q[i+1])/(q[i+1]-q[i])**2*hp[i];C[n+i+1]=-dr*(.5-q[i])/(q[i+1]-q[i])**2*hp[i+1];cc=C@Z;kk=float(1/(cc@np.linalg.solve(HH,cc))) if ev[0]>0 else None
 return dict(minimum_active_tangent_H=float(ev[0]),minimum_active_material_H=float(np.linalg.eigvalsh(P.T@H@P)[0]),negative_endpoint_radii_kpc=rad[neg].tolist(),relaxed_boundary_stiffness_Eunit_per_kpc2=kk,active_mass_cutoff=1e-8,phase_endpoint_cutoff=1e-7,qualification='Finite-grid radial active Hessian; finite displaced recovery and mesh/domain convergence are independent tests.')
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();dest=Path(a.output);old=json.loads(Path('boundary_resolution_2026_10_25/run_latent_thin/base_4.json').read_text());out={'runs':[]}
 for h in [.25,.125]:
  m=model(h);v,info=transfer_species(m,old);r=finish(m,v,dest.with_name(f'base_{h}.json'),initial_iterations=0,newton_iterations=45);r.update(stage='base',transfer=info,hessian=hessian(m,r));out['runs'].append(r);dest.write_text(json.dumps(out,indent=2)+'\n');print('BASE',h,{k:r[k] for k in ['law_endpoint_error_dex','density_KKT_max','gradient_max','density_rebound_full','mass_outside50','explicit_exterior_mass','explicit_exterior_T_fraction','interpolated_crossings_kpc','optimizer','hessian']},flush=True)
  assert r['optimizer']['success'],'base must converge before recovery';old=r
  for d in [-1.,1.]:
   v=moved(m,r,d);assert v is not None and min(m.cap(v))>0
   rr=finish(m,v,dest.with_name(f'recover_{h}_{d}.json'),initial_iterations=0,newton_iterations=55);rr.update(stage='recovery',displacement_kpc=d,energy_difference=rr['energy']-r['energy'],front_change_kpc=rr['interpolated_crossings_kpc'][-1]-r['interpolated_crossings_kpc'][-1]);out['runs'].append(rr);dest.write_text(json.dumps(out,indent=2)+'\n');print('RECOVERY',h,d,{k:rr[k] for k in ['front_change_kpc','energy_difference','law_endpoint_error_dex','density_KKT_max','gradient_max','density_rebound_full','optimizer']},flush=True)
