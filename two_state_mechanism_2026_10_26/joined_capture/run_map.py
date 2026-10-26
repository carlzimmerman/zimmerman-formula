import sys,json,argparse
from pathlib import Path
import numpy as np
from qmap import load,hamiltonian,transform
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'nuclear_flux'))
from electronic import states
p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args();b=Path(__file__).resolve().parent;rows=[];arrays={}
for R in [2,3,4]:
 q=load(b/'inputs'/('R%d_fort.70'%R),b/'inputs'/('R%d_h2+.molden'%R))
 k=np.load(b.parent/'nuclear_flux'/('run_kernel' if R==2 else 'run_kernel_R%d'%R)/'kernel.npz')
 err=float(np.max(abs(hamiltonian(q)-k['H_QQ'])));assert err<1e-8
 for basis in ['aug-cc-pvdz','rydberg2','rydberg3']:
  s=states(R,basis);T=transform(s,q);iso=float(np.linalg.norm(T.T@T-np.eye(42)));assert iso<1e-9
  herr=float(np.max(abs(T.T@(s[3][:,None]*T)-k['H_QQ'])));assert herr<1e-8
  for E in ['0.001','0.05','0.199']:
   A=T@k['entrance_'+E];Sigma=T@k['Sigma_'+E]@T.T;Gamma=1j*(Sigma-Sigma.conj().T)
   optical=float(np.linalg.norm(Gamma-A@A.conj().T)/np.linalg.norm(Gamma));assert optical<1e-10
   rows.append(dict(R=R,basis=basis,energy=float(E),H_max_error=err,embedded_H_max_error=herr,isometry_error=iso,optical_error=optical,entrance_norm=float(np.linalg.norm(A)),capture_weight_first4=float(np.linalg.norm(A[:4])**2/np.linalg.norm(A)**2),capture_weight_first16=float(np.linalg.norm(A[:16])**2/np.linalg.norm(A)**2)))
   arrays['R%d_%s_A_%s'%(R,basis,E)]=A;arrays['R%d_%s_Sigma_%s'%(R,basis,E)]=Sigma
  arrays['R%d_%s_T'%(R,basis)]=T
  print(R,basis,'isometry',iso,'H',herr,flush=True)
np.savez_compressed(Path(a.output).parent/'mapped.npz',**arrays)
Path(a.output).write_text(json.dumps(dict(rows=rows,physical_DR_rates_derived=False,scope='Exact signed finite-Q embedding and electronic optical identity only; larger basis does not add missing continuum physics.'),indent=2)+'\n')
