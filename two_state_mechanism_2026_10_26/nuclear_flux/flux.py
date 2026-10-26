"""Unit-flux scattering for a projected radial Hamiltonian and ideal lattice lead.

This solves neutral-sector propagation, NOT electron capture or DR. The ideal
lead is an explicit approximation whose matching-domain stability must be tested.
"""
import numpy as np

def scattering(potentials,overlaps,energy,spacing,mu=50.):
    n=len(potentials[0]);I=np.eye(n);t=1/(2*mu*spacing**2)
    G=None
    for i,V in enumerate(potentials):
        A=(energy-2*t)*I-np.diag(V)
        if i:
            W=-t*overlaps[i-1];A=A-W.T@G@W
        if i==len(potentials)-1:
            # Retarded semi-infinite discrete lead, one diagonal channel each.
            z=(energy-potentials[-1]-2*t)/(-2*t)
            lam=np.empty(n,dtype=complex);opened=abs(z)<1
            lam[opened]=z[opened]+1j*np.sqrt(1-z[opened]**2)
            lam[~opened]=z[~opened]-np.sign(z[~opened])*np.sqrt(z[~opened]**2-1)
            sigma=-t*lam;gamma=-2*sigma.imag
            A=A.astype(complex)-np.diag(sigma)
        G=np.linalg.inv(A)
    idx=np.flatnonzero(opened);root=np.sqrt(gamma[idx]);S=np.eye(len(idx))-1j*root[:,None]*G[np.ix_(idx,idx)]*root[None,:]
    return dict(S=S,open_indices=idx,unitarity=float(np.linalg.norm(S.conj().T@S-np.eye(len(idx)))),reciprocity=float(np.linalg.norm(S-S.T)))
