import numpy as np
G=6.674e-11; c=2.998e8; M=1.0e11*1.989e30; a=10.0*3.086e19; a0=1.2e-10
K=8*np.pi*G/c**4; K1=K*c**2
r=np.geomspace(1e2,3e6*3.086e19,400000)
def gN(r): return G*M/(r+a)**2
def nu(y): return np.sqrt(1+1/y)
def gg(r): return nu(gN(r)/a0)*gN(r)
u=gg(r)-gN(r)          # <0 deep MOND
Pi=u*gg(r)/K1          # kg/m^3, negative
f_=(Pi/r)
seg=0.5*(f_[1:]+f_[:-1])*np.diff(r)
I=np.concatenate([np.cumsum(seg[::-1])[::-1],[0.0]])  # int_r^inf Pi/r' dr'
for rk in (10.0,100.0):
    rm=rk*3.086e19; j=np.argmin(abs(r-rm))
    dphi=-2*K1*rm*I[j]
    obs=dphi/(2*gg(r)[j]/c**2)
    print(f"r={rk:5.0f}kpc  g={gg(r)[j]:.3e}  Psi={gg(r)[j]*rm/c**2:.3e}  1-Phi/Psi={2*obs:+.3e}   (coef2K)")
    # what 3K would give
    print(f"          with coef 3K instead: {2*obs*1.5:+.3e}")
print("\nmax |1-Phi/Psi| over r in [1,3e4]kpc, coef 2K:", end=" ")
mx=0
for rk in np.geomspace(1,3e4,40):
    rm=rk*3.086e19; j=np.argmin(abs(r-rm)); dphi=-2*K1*rm*I[j]; o=dphi/(2*gg(r)[j]/c**2); mx=max(mx,2*abs(o))
print(f"{mx:.3e}")
