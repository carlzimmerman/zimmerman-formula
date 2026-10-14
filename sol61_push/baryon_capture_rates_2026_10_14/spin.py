"""Small explicit Dirac representation, metric+--- and ubar u=2m."""
import numpy as np
pauli=[np.array([[0,1],[1,0]],complex),np.array([[0,-1j],[1j,0]],complex),np.diag([1,-1]).astype(complex)]
zero=np.zeros((2,2),complex);eye=np.eye(4,dtype=complex)
g0=np.diag([1,1,-1,-1]).astype(complex)
gamma=[g0]+[np.block([[zero,s],[-s,zero]]) for s in pauli]
g5=1j*gamma[0]@gamma[1]@gamma[2]@gamma[3]
PR=(eye+g5)/2
def slash(p):return p[0]*g0-sum((p[i]*gamma[i] for i in [1,2,3]),np.zeros((4,4),complex))
def adjoint(a):return g0@a.conj().T@g0
def dot(a,b):return a[0]*b[0]-np.dot(a[1:],b[1:])
def spinor(p,m,j):
    s=np.eye(2,dtype=complex)[:,j]
    pp=sum((p[i+1]*pauli[i] for i in range(3)),zero.copy())
    return np.sqrt(p[0]+m)*np.concatenate([s,pp@s/(p[0]+m)])
