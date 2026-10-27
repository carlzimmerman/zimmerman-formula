"""Exact separable frozen-electronic nuclear benchmark, NOT molecular DR.

H_P = H_P(R=2) + h_ion - V_ion(2), projected onto four bound ionic modes.
This is a specified approximation; its spectral evaluation is exact for that
finite Hamiltonian. No R-dependent electron transport or dissociation products.
"""
import sys,json,argparse
from pathlib import Path
import numpy as np
from feshbach_v2 import eliminate
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'nuclear_flux'))
from extract_inner import read_ci,read_boundary
from coulomb_kernel_grid import references,channels
p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args();b=Path(__file__).resolve().parent;n=b.parent/'nuclear_flux'
E,U,phase=read_ci(n/'inputs/inner_R2_N25_L2_M20.ci');c=b.parent/'continuum/run_physical_radial25';e,W,r=read_boundary(c/'fort.21');assert np.max(abs(e-E))<1e-10
H=(U*E)@U.T;B=W@U.T;Hp=H[:-42,:-42];V=H[-42:,:-42];Bp=B[:,:-42];target,ell=channels(c/'fort.10')
ion=np.load(b/'run_ion/ion.npz');ev=ion['aug-cc-pvdz_energies'][:4];chi=ion['aug-cc-pvdz_vectors'][:,:4];assert np.linalg.norm(chi.T@chi-np.eye(4))<1e-10
shift=ev-target.min();rows=[];arrays={}
for incident in [.001,.05]:
 total=ev[0]+incident;sigmas=[];gammas=[];ranks=[];errs=[]
 for v in range(4):
  ee=total-shift[v];L=references(ee,target,ell,r)[:,0];S,A,err=eliminate(ee,Hp,V,Bp,L)
  sigmas.append(S);gammas.append(A@A.conj().T);ranks.append(int(np.linalg.matrix_rank(A,tol=1e-9)));errs.append(err)
  arrays['E%s_v%d_Sigma'%(incident,v)]=S;arrays['E%s_v%d_A'%(incident,v)]=A
 norm=np.sqrt(sum(np.linalg.norm(g)**2 for g in gammas));local_error=float(np.sqrt(sum(np.linalg.norm(g-gammas[0])**2 for g in gammas))/norm)
 # Coordinate-space off-diagonal block, with quadrature-normalized eigenvectors.
 i=int(np.argmin(abs(ion['aug-cc-pvdz_R']-2)));j=int(np.argmin(abs(ion['aug-cc-pvdz_R']-3)))
 cross=sum(chi[i,v]*chi[j,v]*gammas[v] for v in range(4));diag=sum(chi[i,v]**2*gammas[v] for v in range(4))
 rows.append(dict(incident=incident,open_vibrational_modes=int(sum(ev<total)),ranks=ranks,maximum_open_relative_error=max(err for err,rank in zip(errs,ranks) if rank),maximum_closed_absolute_error=max([err for err,rank in zip(errs,ranks) if not rank] or [0.]),local_width_replacement_relative_error=local_error,coordinate_cross_block_norm=float(np.linalg.norm(cross)),coordinate_diagonal_norm=float(np.linalg.norm(diag))))
 print(rows[-1],flush=True)
np.savez_compressed(Path(a.output).parent/'nonlocal.npz',**arrays)
Path(a.output).write_text(json.dumps(dict(rows=rows,ionic_energies=ev.tolist(),physical_DR_rates_derived=False,scope='Separable frozen-electronic R2 benchmark with four BO bound ionic modes. Exact spectral elimination of this approximate Hamiltonian, not physical varying-R capture or DR. Higher energy omitted because ionic dissociation continuum opens.'),indent=2)+'\n')
