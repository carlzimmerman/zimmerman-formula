"""Eliminate an explicit Hermitian P Hamiltonian with outgoing boundary channels."""
import numpy as np

def eliminate(E,Hp,V,B,L):
    """V is Q by P; B is boundary by P; outgoing Im L is nonnegative.

    Nuclear motion, when present, belongs in Hp and in the channel boundary L.
    The caller must provide a common orthonormal basis and physical boundaries.
    No dissociation rate is inferred by this function.
    """
    assert np.max(abs(Hp-Hp.conj().T))<1e-9
    assert np.min(L.imag)>-1e-12
    G=np.linalg.solve(E*np.eye(len(Hp))-Hp+B.conj().T@(L[:,None]*B),V.conj().T)
    Sigma=V@G
    # Compute the independent source using the same retarded resolvent.
    op=np.flatnonzero(L.imag>1e-12)
    source=np.linalg.solve(E*np.eye(len(Hp))-Hp+B.conj().T@(L[:,None]*B),B[op].conj().T*np.sqrt(2*L[op].imag))
    A=V@source;Gamma=1j*(Sigma-Sigma.conj().T)
    err=float(np.linalg.norm(Gamma-A@A.conj().T)/max(np.linalg.norm(Gamma),1e-25))
    if len(op):assert err<1e-8,err
    else:
        assert np.linalg.norm(Gamma)<1e-8
        err=float(np.linalg.norm(Gamma)) # absolute error: closed width is zero
    return Sigma,A,err
