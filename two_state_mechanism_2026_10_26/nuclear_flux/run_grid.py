import argparse,json,time
from pathlib import Path
import numpy as np
from electronic import states,overlap,basis_spec
from flux import scattering
from pyscf import gto
from scipy.linalg import eigh
p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--basis',default='aug-cc-pvdz');p.add_argument('--h',type=float,default=.1);p.add_argument('--end',type=float,default=30);p.add_argument('--retain',default='4,16,42');a=p.parse_args()
ret=[int(x) for x in a.retain.split(',')];R=np.arange(round((a.end-.5)/a.h)+1)*a.h+.5
Vs=[];Os=[];prev=None;start=time.monotonic()
for i,r in enumerate(R):
    s=states(r,a.basis);n=len(s[3]);assert max(ret)<=n
    if prev is not None:Os.append(overlap(prev,s)[:max(ret),:max(ret)])
    Vs.append(s[3][:max(ret)]);prev=s
    if i%100==0:print('grid',i,len(R),'R',r,'seconds',time.monotonic()-start,flush=True)
Vs=np.array(Vs);Os=np.array(Os)
out=Path(a.output);out.parent.mkdir(parents=True,exist_ok=True)
np.savez_compressed(out.parent/'grid.npz',R=R,V=Vs,O=Os)
# Atomic thresholds independently indicate whether the product basis is adequate.
m=gto.M(atom='H 0 0 0',basis=basis_spec(a.basis),spin=1,verbose=0)
atom=eigh(m.intor('int1e_kin')+m.intor('int1e_nuc'),m.intor('int1e_ovlp'))[0]
rows=[]
for keep in ret:
 for E in [-.62,-.60,-.58]:
    result=scattering(Vs[:,:keep],Os[:,:keep,:keep],E,a.h)
    assert result['unitarity']<1e-8 and result['reciprocity']<1e-8
    row=dict(retain=keep,energy=E,open_indices=result['open_indices'].tolist(),probabilities=(abs(result['S'])**2).tolist(),S_real=result['S'].real.tolist(),S_imag=result['S'].imag.tolist(),unitarity_error=result['unitarity'],reciprocity_error=result['reciprocity'])
    rows.append(row);print('flux',keep,E,row['probabilities'],flush=True)
result=dict(settings=dict(basis=a.basis,h=a.h,end=float(R[-1]),Rmin=float(R[0]),electronic_states=n,nuclear_reduced_mass=50,J=0),atomic_eigenvalues=atom.tolist(),asymptotic_energies=Vs[-1].tolist(),rows=rows,seconds=time.monotonic()-start,scope='Neutral finite-basis radial scattering with ideal diagonal lead; no incident electron, no DR rate or DR product branching',physical_DR_rates_derived=False)
out.write_text(json.dumps(result,indent=2)+'\n')
