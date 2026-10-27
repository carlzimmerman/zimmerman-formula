"""Signed two-electron singlet CSFs from CONGEN, not eigenvalue matching."""
import numpy as np
from scipy.io import FortranFile
from pyscf.tools import molden
from pyscf import ao2mo,gto

def configurations(path):
    f=FortranFile(path);a=f.read_record('u1').tobytes()
    norb,nsrb,ncsf,nelt,lcd,idiag,nsym,symtyp,lnd=np.frombuffer(a[160:232],'<i8')
    nctarg,ntgcon=np.frombuffer(a[288:304],'<i8')
    assert nelt==2 and nctarg>0 and ntgcon>0
    f.read_record('u1');meta=f.read_ints('<i8')
    nob=meta[:nsym];ref=list(meta[nsym:nsym+nelt]);nob0=meta[nsym+nelt+ncsf+1:nsym+nelt+ncsf+1+nsym]
    indices=f.read_ints('<i8');ic=indices[:ncsf+1];ind=indices[ncsf+1:]
    packed=f.read_ints('<i8');coeff=f.read_reals('<f8')
    orbital_map={};start=0;target=0
    for n,k in zip(nob,nob0):
        for j in range(k):orbital_map[start+j]=target+j
        start+=n;target+=k
    csfs=[]
    for c in range(ncsf):
        pos=ind[c]-1;matrix=np.zeros((target,target));pure=True
        for d in range(ic[c]-1,ic[c+1]-1):
            nr=packed[pos];src=packed[pos+1:pos+1+nr];dst=packed[pos+1+nr:pos+1+2*nr];pos+=2*nr+1
            occ=ref.copy();sign=1
            for s in src:
                i=occ.index(s);sign*=(-1)**i;occ.pop(i)
            for s in dst[::-1]:
                i=sum(t<s for t in occ);sign*=(-1)**i;occ.insert(i,s)
            assert len(occ)==2 and occ[0]%2!=occ[1]%2
            if not all((s-1)//2 in orbital_map for s in occ):pure=False;continue
            alpha=next(s for s in occ if s%2);beta=next(s for s in occ if s%2==0)
            if occ[0]!=alpha:sign*=-1
            matrix[orbital_map[(alpha-1)//2],orbital_map[(beta-1)//2]]+=sign*coeff[d]
        if pure:csfs.append(matrix)
    ci=np.array(csfs);assert np.max(abs(ci-ci.transpose(0,2,1)))<1e-12
    assert np.max(abs(ci.reshape(len(ci),-1)@ci.reshape(len(ci),-1).T-np.eye(len(ci))))<1e-12
    return ci,nob0

def load(congen,molden_path):
    ci,nob0=configurations(congen)
    mol,e,C,occ,labels,spin=molden.load(str(molden_path))
    order=sorted(range(len(e)),key=lambda i:tuple(map(int,labels[i].split('.')[::-1])))
    for j,k in enumerate(nob0):assert sum(int(x.split('.')[1])==j+1 for x in labels)==k
    C=C[:,order];assert len(ci)==42 and C.shape[1]==18
    S=mol.intor('int1e_ovlp');assert np.max(abs(C.T@S@C-np.eye(18)))<1e-10
    return mol,C,ci

def hamiltonian(q):
    m,C,ci=q;n=C.shape[1];B=ci.reshape(len(ci),-1).T
    h=C.T@(m.intor('int1e_kin')+m.intor('int1e_nuc'))@C
    v=ao2mo.restore(1,ao2mo.kernel(m,C),n)
    H=np.kron(h,np.eye(n))+np.kron(np.eye(n),h)+v.transpose(0,2,1,3).reshape(n*n,n*n)
    return B.T@H@B+np.eye(len(ci))*m.energy_nuc()

def transform(nuclear,q):
    """T[a,q]=<nuclear eigenstate a | original signed Q CSF q>."""
    O=nuclear[1].T@gto.intor_cross('int1e_ovlp',nuclear[0],q[0])@q[1]
    return np.einsum('iab,ac,jcd,bd->ij',nuclear[2],O,q[2],O,optimize=True)
