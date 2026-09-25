import numpy as np, itertools
from setalg import *
n=5; pc=popcount_table(n); rng=np.random.default_rng(1)
f=rng.normal(size=1<<n)+1j*rng.normal(size=1<<n); g=rng.normal(size=1<<n)+1j*rng.normal(size=1<<n)
h=np.zeros(1<<n,dtype=complex)
for M in range(1<<n):
    K=M
    while True:
        h[M]+=f[K]*g[M^K]
        if K==0: break
        K=(K-1)&M
print('conv err',abs(conv(f,g,n,pc)-h).max())
c=f.copy(); c[0]=0
E=np.zeros(1<<n,dtype=complex); E[0]=1; term=E.copy()
for k in range(1,n+1):
    term=conv(term,c,n,pc)/k; E+=term
print('exp err',abs(sexp(c,n,pc)-E).max())
# operator check: exp(C) as matrix acting on Omega
dim=1<<n; C=np.zeros((dim,dim),dtype=complex)
for M in range(1,dim):
    for S in range(dim):
        if S&M==0: C[S|M,S]+=c[M]
import scipy.linalg as sl
print('op err',abs(sl.expm(C)[:,0]-E).max(), abs(sl.expm(C)@g - conv(E,g,n,pc)).max())
