"""Complete finite-basis singlet Ag Coulomb Hamiltonian, no fitted potentials."""
import numpy as np
from pyscf import gto,ao2mo,lib
from scipy.linalg import eigh
lib.num_threads(1)
def basis_spec(basis):
    if basis.startswith('rydberg'):
        count=int(basis[-1]);return {'H':gto.basis.load('aug-cc-pvdz','H')+[[l,[start/3**j,1.]] for l,start in [(0,.02),(1,.04)] for j in range(count)]}
    return basis

def states(R,basis='aug-cc-pvdz'):
    m=gto.M(atom=[('H',(0,0,-R/2)),('H',(0,0,R/2))],unit='Bohr',basis=basis_spec(basis),symmetry='D2h',verbose=0)
    S=m.intor('int1e_ovlp');parts=[];labels=[]
    for ir,Q in zip(m.irrep_id,m.symm_orb):
        val,U=eigh(Q.T@S@Q)
        assert val.min()>1e-10
        parts.append(Q@(U/np.sqrt(val))@U.T);labels.extend([ir]*Q.shape[1])
    C=np.column_stack(parts);n=C.shape[1];h=C.T@(m.intor('int1e_kin')+m.intor('int1e_nuc'))@C
    eri=ao2mo.restore(1,ao2mo.kernel(m,C),n)
    pairs=[(i,j) for i in range(n) for j in range(i,n) if labels[i]==labels[j]]
    B=np.zeros((n*n,len(pairs)))
    for k,(i,j) in enumerate(pairs):
        if i==j:B[i*n+j,k]=1
        else:B[i*n+j,k]=B[j*n+i,k]=1/np.sqrt(2)
    H=np.kron(h,np.eye(n))+np.kron(np.eye(n),h)+eri.transpose(0,2,1,3).reshape(n*n,n*n)
    E,U=eigh(B.T@H@B)
    ci=(B@U).T.reshape(len(E),n,n)
    return m,C,ci,E+m.energy_nuc()
def overlap(a,b):
    O=a[1].T@gto.intor_cross('int1e_ovlp',a[0],b[0])@b[1]
    return np.einsum('iab,ac,jcd,bd->ij',a[2],O,b[2],O,optimize=True)
