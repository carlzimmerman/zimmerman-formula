import argparse,json
from pathlib import Path
import numpy as np,torch
from scipy.linalg import null_space
from coupled_model import Coupled
from joint import T
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();dest=Path(a.output);data=json.loads(Path('gradient_coupling_2026_10_24/run_continue/results.json').read_text());out={'force_audit':[],'virial_check':[]}
for n in [96,144]:
 r=[r for r in data['runs'] if r['n']==n and r['stage']=='recovery'][-1];m=Coupled(n=n,domain=12,beta=2,K=30,charge=0,L=r['density_stiffness_length_kpc'],eta=r['eta']);m.ell2=(10/m.rm)**2;v=np.r_[r['mass'],r['v'][n:]];aa=T(v).requires_grad_(True);H=torch.autograd.functional.hessian(lambda z:m.energy(torch.log(z[:n]),z[n:]),aa).detach().numpy();mass=v[:n];x=v[n:];im=np.where(mass>1e-7)[0];ix=np.where((x>1e-6)&(x<1-1e-6))[0]+n;P0=null_space(np.ones((1,len(im))));P=np.zeros((2*n,len(im)-1));P[im]=P0;X=np.eye(2*n)[:,ix];Z=np.c_[P,X];ev=np.linalg.eigvalsh(Z.T@H@Z);q=np.array(r['q']);rad=np.array(r['r']);i=np.where((q[:-1]-.5)*(q[1:]-.5)<0)[0][-1];dr=rad[i+1]-rad[i];hp=np.pi/2*np.sin(np.pi*x);C=np.zeros(2*n);C[n+i]=dr*(.5-q[i+1])/(q[i+1]-q[i])**2*hp[i];C[n+i+1]=-dr*(.5-q[i])/(q[i+1]-q[i])**2*hp[i+1];cc=C@Z
 K=float(1/(cc@np.linalg.solve(Z.T@H@Z,cc))) if ev[0]>0 else None;end=np.where((x<=1e-6)|(x>=1-1e-6))[0];neg=end[np.diag(H)[n:][end]<-1e-8]
 out['force_audit'].append(dict(n=n,R=r['interpolated_crossings_kpc'],minimum_tangent_H=float(ev[0]),minimum_material_H=float(np.linalg.eigvalsh(P.T@H@P)[0]),relaxed_boundary_stiffness_Eunit_per_kpc2=K,negative_endpoint_diagonal_radii=rad[neg].tolist(),density_KKT=r['density_KKT_max'],law_error_dex=r['law_endpoint_error_dex'],support=r['support'],qualification='Finite-active-set Hessian at numerically approximate stationary point; not a resolution-independent boundary certificate.'))
 # Independent homology check on the discrete coupling alone.
 a0=np.sqrt(mass/m.vol.numpy());dq=np.diff(q);w=np.diff(a0)-m.eta*(a0[1:]+a0[:-1])/2*dq;k=(m.L/m.rm)**3;E0=.5*k*np.sum(m.rf.numpy()**2/m.dr.numpy()*w*w)
 for scale in [.8,1.2]:
  aa=a0/scale**1.5;ww=np.diff(aa)-m.eta*(aa[1:]+aa[:-1])/2*dq;EE=.5*k*np.sum((scale*m.rf.numpy())**2/(scale*m.dr.numpy())*ww*ww);err=abs(EE/E0-scale**-2);assert err<1e-12;out['virial_check'].append(dict(n=n,scale=scale,measured_energy_ratio=EE/E0,expected_ratio=scale**-2,error=err))
dest.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
