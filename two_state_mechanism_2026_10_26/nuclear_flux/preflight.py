"""Independent Coulomb atomic thresholds, E1 emission and nuclear completeness."""
import argparse,json
from pathlib import Path
import numpy as np
from scipy.linalg import eigh
from pyscf import gto
from electronic import states,overlap,basis_spec
p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args();rows=[]
for basis in ['aug-cc-pvdz','rydberg2','rydberg3']:
    m=gto.M(atom='H 0 0 0',basis=basis_spec(basis),spin=1,verbose=0);S=m.intor('int1e_ovlp');en,C=eigh(m.intor('int1e_kin')+m.intor('int1e_nuc'),S);dip=m.intor('int1e_r',comp=3)
    d=np.einsum('p,xpq,qj->xj',C[:,0],dip,C,optimize=True);strength=(d*d).sum(axis=0)
    # Identify first dipole-allowed triplet by matrix elements, not index/name.
    ids=np.flatnonzero((strength>1e-5)&(np.arange(len(en))>0))[:3]
    freq=en[ids]-en[0];A=(4/3)*freq**3*strength[ids]
    mid=states(2,basis);steps=[]
    for h in [.005,.0025]:
        minus=states(2-h,basis);plus=states(2+h,basis)
        sm=np.sign(overlap(mid,minus)[0,0]);sp=np.sign(overlap(mid,plus)[0,0])
        derivative=(overlap(mid,plus)[:,0]*sp-overlap(mid,minus)[:,0]*sm)/(2*h)
        metric=(2-2*overlap(minus,plus)[0,0]*sm*sp)/(4*h*h)
        steps.append(dict(h=h,metric=float(metric),retained_fractions={str(n):float(np.sum(derivative[:n]**2)/metric) for n in [4,16,len(mid[3])]}))
    rows.append(dict(basis=basis,atomic_energies=en.tolist(),first_E1_states=ids.tolist(),line_frequencies=freq.tolist(),dipole_strength=strength[ids].tolist(),E1_rate_divided_by_alpha_cubed=A.tolist(),electronic_singlet_Ag_states=len(mid[3]),ground_energy_R2=float(mid[3][0]),nuclear_derivatives=steps))
    print(basis,rows[-1],flush=True)
exact_d=256/(243*np.sqrt(2));exact_A=(4/3)*(.375)**3*exact_d**2
# The known analytic hydrogen 2p ->1s coefficient checks the numerical dipole scale.
assert max(abs(np.array(rows[-1]['E1_rate_divided_by_alpha_cubed'])/exact_A-1))<.02
Path(a.output).write_text(json.dumps(dict(rows=rows,exact_Coulomb_2p_E1_rate_divided_by_alpha_cubed=exact_A,exact_line_energy=.375,scope='Clamped-nucleus atomic Coulomb and radial finite-basis metrics; E1 atomic decay is physical within this approximation, not a DR rate. Finite mass corrections and 2s two-photon decay not included.'),indent=2)+'\n')
