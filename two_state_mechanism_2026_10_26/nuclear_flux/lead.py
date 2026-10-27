"""Exact modes of a stationary block lattice; no phenomenological absorber."""
import numpy as np
from scipy.linalg import eig

def modes(H,W,E):
    n=len(H);I=np.eye(n);Z=np.zeros((n,n))
    A=np.block([[E*I-H,-W.T],[I,Z]]);B=np.block([[W,Z],[Z,I]])
    lam,z=eig(A,B);u=z[n:,:];u/=np.linalg.norm(u,axis=0)
    current=-2*np.imag(np.einsum('ij,ij->j',u.conj(),W@u)*lam)
    propagating=abs(abs(lam)-1)<1e-7
    choose=np.flatnonzero((~propagating & (abs(lam)<1)) | (propagating & (current>1e-8)))
    assert len(choose)==n,(len(choose),n)
    chosen=sorted(choose,key=lambda i:(not propagating[i],int(np.argmax(abs(u[:,i])**2))))
    lam=lam[chosen];u=u[:,chosen];cur=current[chosen];op=np.flatnonzero(propagating[chosen])
    u[:,op]/=np.sqrt(cur[op])
    F=(u*lam)@np.linalg.inv(u);sigma=W@F
    residual=max(np.linalg.norm((W*lam[j]+H-E*I+W.T/lam[j])@u[:,j])/max(1,np.linalg.norm(u[:,j])) for j in range(n))
    assert residual<1e-7,residual
    return dict(lambda_=lam,**{'lambda':lam},U=u,open=op,F=F,sigma=sigma,residual=float(residual))

def scattering_lead(potentials,overlaps,E,h,lead_overlap,mu=50.):
    n=len(potentials[0]);I=np.eye(n);t=1/(2*mu*h*h);W=-t*lead_overlap
    m=modes(np.diag(potentials[-1])+2*t*I,W,E)
    G=None
    for i,V in enumerate(potentials):
        A=(E-2*t)*I-np.diag(V)
        if i:
            link=-t*overlaps[i-1];A=A-link.T@G@link
        if i==len(potentials)-1:A=A.astype(complex)-m['sigma']
        G=np.linalg.inv(A)
    op=m['open'];Uin=m['U'][:,op].conj();lin=m['lambda'][op].conj()
    forcing=W@(Uin*lin-m['F']@Uin)
    psi=G@forcing;coeff=np.linalg.solve(m['U'],psi-Uin);S=coeff[op,:]
    return dict(S=S,unitarity=float(np.linalg.norm(S.conj().T@S-np.eye(len(op)))),reciprocity=float(np.linalg.norm(S-S.T)),mode_weights=(abs(m['U'][:,op])**2/np.sum(abs(m['U'][:,op])**2,axis=0)).tolist(),mode_angles=np.angle(m['lambda'][op]).tolist(),mode_residual=m['residual'])
