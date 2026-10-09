import numpy as np
from scipy.optimize import brentq, minimize_scalar
def I4(s):
    s=abs(s); return 1.0 if s<1e-100 else 1-s*s*np.log1p(1/(s*s))
def I3(s):
    s=abs(s); return 1.0 if s<1e-100 else np.sqrt(1+s*s)-s*s*np.arcsinh(1/s)
R=206.768283
def fam(g,I):
    psi=lambda s: s-g*s*I(s)
    sp=minimize_scalar(psi,bounds=(1e-9,20),method='bounded').x; Cm=-psi(sp)
    def roots(C):
        return np.array([brentq(lambda s:psi(s)-C,-1e4,-sp),brentq(lambda s:psi(s)-C,-sp,sp),brentq(lambda s:psi(s)-C,sp,1e4)])
    return roots,Cm
def obs(r):
    a=np.sort(np.abs(r)); return (a[1]/a[0])**2,(a**2).sum()/a.sum()**2
for name,I in [("I4",I4),("I3",I3)]:
    print(name)
    rows=[]
    for g in np.geomspace(10,2000,40):
        roots,Cm=fam(g,I)
        # find C in (0,Cm) with m_mu/m_e = R (scan then refine)
        Cs=np.linspace(1e-6*Cm,Cm*(1-1e-9),400); f=[np.log(obs(roots(C))[0]/R) for C in Cs]
        for i in range(len(Cs)-1):
            if f[i]*f[i+1]<0:
                C=brentq(lambda c:np.log(obs(roots(c))[0]/R),Cs[i],Cs[i+1],xtol=1e-15); r=roots(C)
                Q=obs(r)[1]; rho=C/(r.sum()/3-C); rows.append((g,C,Q,rho))
    for g,C,Q,rho in rows[::8]: print(f"  g={g:.3f} C={C:.5f}  Q={Q:.6f}  h/g needed={rho:+.4f}")
    Qs=np.array([r[2] for r in rows]); print("  Q range along the m_mu/m_e-fitted family:",Qs.min(),Qs.max())
    # does Q cross Koide?
    for a,b in zip(rows,rows[1:]):
        if (a[2]-0.666661)*(b[2]-0.666661)<0: print("  KOIDE crossing between g",a[0],b[0]," h/g needed ~",a[3],b[3])
