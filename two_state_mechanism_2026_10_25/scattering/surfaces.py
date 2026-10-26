"""Correlated two-electron BO channel energies; NOT scattering amplitudes."""
import argparse,json
from pathlib import Path
import numpy as np
from scipy.linalg import eigh, eigh_tridiagonal
from scipy.interpolate import PchipInterpolator
from pyscf import gto,scf,fci,lib,__version__
lib.num_threads(1)

def atom(basis,charge):
    mol=gto.M(atom='H 0 0 0',basis=basis,charge=charge,
              spin=1 if charge==0 else 0,verbose=0)
    if charge==0:
        return float(eigh(mol.intor('int1e_kin')+mol.intor('int1e_nuc'),mol.intor('int1e_ovlp'),subset_by_index=(0,0))[0][0])
    mf=scf.RHF(mol).run(conv_tol=1e-12)
    solver=fci.direct_spin0.FCI(mol);solver.conv_tol=1e-11
    h=mf.mo_coeff.T@mf.get_hcore()@mf.mo_coeff
    from pyscf import ao2mo
    eri=ao2mo.kernel(mol,mf.mo_coeff)
    energy,_=solver.kernel(h,eri,mf.mo_coeff.shape[1],(1,1))
    assert solver.converged
    return float(energy)

def molecule(R,basis):
    mol=gto.M(atom=[('H',(0,0,-R/2)),('H',(0,0,R/2))],unit='Bohr',basis=basis,verbose=0)
    mf=scf.RHF(mol).run(conv_tol=1e-11,max_cycle=200)
    # Orbital choice does not truncate FCI. Core orbitals also work if SCF stalls.
    coeff=mf.mo_coeff; h=coeff.T@mf.get_hcore()@coeff
    from pyscf import ao2mo
    eri=ao2mo.kernel(mol,coeff);n=coeff.shape[1];out={}
    for name,solver,nel in [('singlet',fci.direct_spin0.FCI(mol),(1,1)),('triplet',fci.direct_spin1.FCI(mol),(2,0))]:
        solver.conv_tol=1e-10;solver.max_cycle=200
        e,ci=solver.kernel(h,eri,n,nel)
        assert solver.converged,(R,basis,name)
        out[name]=float(e+mol.energy_nuc())
        out[name+'_spin2']=float(fci.spin_op.spin_square(ci,n,nel)[0])
    out['ion']=float(eigh(h,subset_by_index=(0,0))[0][0]+mol.energy_nuc())
    return dict(R=R,basis=basis,orbitals=n,**out)

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args()
    basis='aug-cc-pvdz'
    grid=np.unique(np.r_[np.arange(.4,3.01,.1),np.arange(3.2,6.01,.2),8.,10.,15.,20.])
    rows=[]
    for R in grid:
        r=molecule(float(R),basis);rows.append(r);print('R',R,r['singlet'],r['triplet'],flush=True)
    checks=[]
    for b in ['aug-cc-pvdz','aug-cc-pvtz']:
        checks.append(dict(basis=b,atom=atom(b,0),anion=atom(b,-1),molecules=[molecule(R,b) for R in [1.4,2.,4.,10.]]))
        print('basis',b,checks[-1]['atom'],checks[-1]['anion'],flush=True)
    # Finite-box Dirichlet nuclear spectrum on computed interval. No invented tail.
    asym=2*checks[0]['atom'];potential=PchipInterpolator(grid,[r['singlet']-asym for r in rows])
    nuclear=[]
    for step in [.02,.01,.005]:
        r=np.arange(.4+step,20.-step/2,step);v=potential(r);mu=50.
        e=eigh_tridiagonal(1/(mu*step**2)+v,np.full(len(r)-1,-1/(2*mu*step**2)),select='v',select_range=(-1.,0.))[0]
        nuclear.append(dict(h=step,energies=e.tolist(),ground_binding=float(-e[0]),box=[.4,20.],J=0))
    result=dict(pyscf=__version__,rows=rows,checks=checks,nuclear=nuclear,
                non_claim='Fixed-nuclei bound-state Galerkin calculation, no continuum S matrix or finite reaction rate')
    assert all(abs(r['singlet_spin2'])<1e-7 and abs(r['triplet_spin2']-2)<1e-7 for r in rows)
    Path(a.output).write_text(json.dumps(result,indent=2)+'\n')
if __name__=='__main__':main()
