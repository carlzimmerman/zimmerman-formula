"""Hermitian fourth-order projected kinetic; two radial sites per block."""
import numpy as np

def diagonal(Va,Vb,Oab,t):
 n=len(Va);I=np.eye(n)
 return np.block([[np.diag(Va)+2.5*t*I,-4*t/3*Oab],[-4*t/3*Oab.T,np.diag(Vb)+2.5*t*I]])

def link(Oac,Obc,Obd,t):
 return np.block([[t/12*Oac,np.zeros_like(Oac)],[-4*t/3*Obc,t/12*Obd]])

def response(A,H,W,E,modes):
 m=modes(H,W,E);op=m['open'];G=np.linalg.inv(A.astype(complex)-m['sigma'])
 Uin=m['U'][:,op].conj();forcing=W@(Uin*m['lambda'][op].conj()-m['F']@Uin)
 psi=G@forcing;S=np.linalg.solve(m['U'],psi-Uin)[op,:]
 err=float(np.linalg.norm(S.conj().T@S-np.eye(len(op))));rec=float(np.linalg.norm(S-S.T))
 assert err<1e-7 and rec<1e-7,(err,rec)
 weights=abs(m['U'][:,op])**2;n=len(H)//2;weights=weights[:n]+weights[n:];weights/=weights.sum(axis=0)
 ground=int(np.argmax(weights[0]));loss=float(np.sum(abs(S[:,ground])**2)-abs(S[ground,ground])**2)
 return dict(probabilities=(abs(S)**2).tolist(),unitarity_error=err,reciprocity_error=rec,mode_weights=weights.tolist(),ground_mode=ground,ground_to_other=loss,mode_residual=m['residual'])
