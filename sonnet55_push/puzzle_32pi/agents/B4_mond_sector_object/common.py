import numpy as np, mpmath as mp, random
TARGET = 1/np.sqrt(32*np.pi)
MASSES = {"1/sqrtL":1.0, "Nariai 1/(3sqrtL)":1/3, "Hubble L/2":np.sqrt(3)/2}   # Lambda = 1
def radii(a0,M):
    return {"r_M":np.sqrt(M/a0), "1/a0":1/a0, "1/(2a0)=r_H":1/(2*a0), "L=sqrt3":np.sqrt(3.0), "1/sqrtLam":1.0, "2GM":2*M}
def roots_log(F, lo=1e-5, hi=1e3, n=4000):
    xs=np.exp(np.linspace(np.log(lo),np.log(hi),n)); v=[F(x) for x in xs]; out=[]
    for i in range(n-1):
        if np.sign(v[i])!=np.sign(v[i+1]) and np.isfinite(v[i]) and np.isfinite(v[i+1]):
            out.append(float(mp.findroot(lambda t: F(float(t)), (xs[i],xs[i+1]), solver='bisect',tol=1e-14,maxsteps=200)))
    return out
def scan(cond):
    """cond(a0,M,rt_name)-> residual; returns list of (mass,radius,a0 roots)"""
    res=[]
    for mn,M in MASSES.items():
        for rn in radii(1.0,M):
            rts=roots_log(lambda a: cond(a,M,rn))
            res.append((mn,rn,rts))
    return res
def hits(res, target, tol=0.01):
    return sum(1 for _,_,rt in res for r in rt if abs(r/target-1)<tol), sum(len(rt) for _,_,rt in res)
def decoy_rate(res, n=2000, tol=0.01, seed=1):
    rng=random.Random(seed); roots=[r for _,_,rt in res for r in rt]
    if not roots: return 0.0
    h=0
    for _ in range(n):
        t=float(np.exp(rng.uniform(np.log(0.03),np.log(0.3))))
        h+= any(abs(r/t-1)<tol for r in roots)
    return h/n
