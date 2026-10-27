"""Moving-basis electronic derivative couplings; finite bound/pseudostate basis."""
import argparse,json
from pathlib import Path
import numpy as np
from pyscf import gto,scf,fci,ao2mo,lib,symm
lib.num_threads(1)

def states(R):
    m=gto.M(atom=[('H',(0,0,-R/2)),('H',(0,0,R/2))],unit='Bohr',basis='aug-cc-pvdz',symmetry='D2h',verbose=0)
    mf=scf.RHF(m).run(conv_tol=1e-12)
    C=mf.mo_coeff;h=C.T@mf.get_hcore()@C;eri=ao2mo.kernel(m,C)
    solver=fci.direct_spin0_symm.FCI(m);solver.wfnsym='Ag';solver.orbsym=symm.label_orb_symm(m,m.irrep_id,m.symm_orb,C)
    solver.nroots=4;solver.conv_tol=1e-11;solver.max_cycle=200
    energies,ci=solver.kernel(h,eri,C.shape[1],(1,1));assert all(solver.converged)
    return m,C,np.array(ci),np.array(energies)+m.energy_nuc()

def overlap(a,b):
    # One alpha and one beta electron: product of the two one-electron overlaps.
    O=a[1].T@gto.intor_cross('int1e_ovlp',a[0],b[0])@b[1]
    return np.einsum('iab,ac,jcd,bd->ij',a[2],O,b[2],O,optimize=True)

def align(ref,b):
    signs=np.sign(np.diag(overlap(ref,b)));assert np.all(signs!=0)
    return b[0],b[1],b[2]*signs[:,None,None],b[3]

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args();rows=[]
    for R in [1.8,2.,2.2]:
        mid=states(R);assert np.max(abs(overlap(mid,mid)-np.eye(4)))<1e-9
        steps=[]
        for h in [.01,.005]:
            minus=align(mid,states(R-h));plus=align(mid,states(R+h))
            op=overlap(mid,plus);om=overlap(mid,minus)
            d=(op-om)/(2*h)
            metric=(2-2*np.diag(overlap(minus,plus)))/(4*h*h)
            remainder=metric-np.sum(d*d,axis=0)
            steps.append(dict(h=h,d=d.tolist(),metric=metric.tolist(),omitted_derivative_norm=remainder.tolist(),antisymmetry_error=float(np.max(abs(d+d.T))),ground_DBOC=float(metric[0]/100)))
        assert steps[1]['antisymmetry_error'] < steps[0]['antisymmetry_error']/3
        assert min(steps[1]['omitted_derivative_norm']) > 0
        assert abs(steps[1]['metric'][0]-steps[0]['metric'][0]) < 5e-6
        rows.append(dict(R=R,energies=mid[3].tolist(),steps=steps));print(R,rows[-1],flush=True)
    Path(a.output).write_text(json.dumps(dict(rows=rows,scope='4 Ag singlet states, aug-cc-pVDZ; no continuum normalization or DR widths'),indent=2)+'\n')
if __name__=='__main__':main()
