"""Physical dr-integral of the existing cubic reference interpolant; no evolution."""
import numpy as np

def cell_mass(ne,alpha,R,amplitude_full,nq):
 amp=np.asarray(amplitude_full);assert amp.shape==(3*ne+1,)
 nodes=np.array([-1.,-1/np.sqrt(5),1/np.sqrt(5),1.]);z,w=np.polynomial.legendre.leggauss(nq);basis=np.ones((nq,4))
 for i in range(4):
  for j in range(4):
   if i!=j:basis[:,i]*=(z-nodes[j])/(nodes[i]-nodes[j])
 values=amp[3*np.arange(ne)[:,None]+np.arange(4)[None,:]]@basis.T;xi=(np.arange(ne)[:,None]+(z+1)/2)/ne
 J=np.full_like(xi,R) if alpha==0 else R*alpha*np.cosh(alpha*xi)/np.sinh(alpha)
 return np.sum(abs(values)**2*(w[None,:]*J/(2*ne)),axis=1)
