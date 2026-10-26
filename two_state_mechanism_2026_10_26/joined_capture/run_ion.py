"""Leading Born-Oppenheimer ionic vibrational thresholds, fixed axis."""
import sys,json,argparse
from pathlib import Path
import numpy as np
from scipy.linalg import eigh,eigh_tridiagonal
from pyscf import gto,lib
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'nuclear_flux'))
from electronic import basis_spec
lib.num_threads(1)
p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args();rows=[];arrays={}
for basis in ['aug-cc-pvdz','rydberg3']:
 h=.025;R=.2+np.arange(1,792)*h;V=[]
 for i,r in enumerate(R):
  m=gto.M(atom=[('H',(0,0,-r/2)),('H',(0,0,r/2))],unit='Bohr',basis=basis_spec(basis),charge=1,spin=1,verbose=0)
  V.append(eigh(m.intor('int1e_kin')+m.intor('int1e_nuc'),m.intor('int1e_ovlp'),subset_by_index=[0,0])[0][0]+1/r)
 V=np.array(V)
 atom=gto.M(atom='H 0 0 0',basis=basis_spec(basis),spin=1,verbose=0)
 threshold=float(eigh(atom.intor('int1e_kin')+atom.intor('int1e_nuc'),atom.intor('int1e_ovlp'),subset_by_index=[0,0])[0][0])
 for stride in [4,2,1]:
  hh=h*stride;vv=V[stride-1::stride];t=1/(100*hh*hh);E,U=eigh_tridiagonal(vv+2*t,-t*np.ones(len(vv)-1),select='i',select_range=[0,11]);bound=E[E<threshold];opens=[int(sum(bound<bound[0]+x)) for x in [.001,.05,.199]]
  rows.append(dict(basis=basis,h=hh,bound_energies=bound.tolist(),atomic_threshold=threshold,bound_open_counts=opens,ion_dissociation_open=[bool(bound[0]+x>threshold) for x in [.001,.05,.199]]))
  print(rows[-1],flush=True)
  if stride==1:arrays[basis+'_R']=R;arrays[basis+'_V']=V;arrays[basis+'_energies']=E;arrays[basis+'_vectors']=U
np.savez_compressed(Path(a.output).parent/'ion.npz',**arrays)
Path(a.output).write_text(json.dumps(dict(rows=rows,mu=50,inner_wall=.2,outer_wall=20,physical_DR_rates_derived=False,scope='Single-surface scalar BO ionic thresholds; no DBOC, rotation or mass polarization. Above dissociation, bound-level counts exclude continuum channels.'),indent=2)+'\n')
