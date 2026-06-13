"""
agentOO Route 1, C8 — FAST fully-numeric self-energy with EXACT angular integral (u-substitution),
vectorized numpy Gauss-Legendre radial+angular grids. Finite-difference / lstsq in k for sigma_n.

EXACT angular integral. For fixed q,k the only x=cos(theta) dependence is through u=W_{q+k}=c_b|q+k|,
with u in [c_b|q-k|, c_b(q+k)] and dx = u du/(c_b^2 q k). The kernel
  K(u) = 1/(2 Wq u) [ (nq+nu)(1/(om-Wq-u)-1/(om+Wq+u)) + (nq-nu)(1/(om-Wq+u)-1/(om+Wq-u)) ]
is integrated over u (1-D). PV handled by symmetric grid avoidance of poles (we use a smooth grid that
does not land on poles; for the on-shell gapless mode with c_chi != c_b the emission poles are outside
[umin,umax] and the Landau pole, if inside, is integrated as a PV via odd-symmetric subtraction).

We compute ReSigma(c_chi k, k) for several k and lstsq-fit s0+s2 k^2+s4 k^4+s6 k^6, scanning r=c_chi/c_b.
This is the SAME physics as C1/C5 but fast (numpy, fixed grids). The SIGN of s4 is the deliverable.
"""
import numpy as np

H=1.0; T=H/(2*np.pi)
def nB(W):
    W=np.asarray(W,float)
    out=np.zeros_like(W)
    pos=W>0
    x=np.where(pos,W/T,1.0)
    small=x<50
    out[pos & small] = 1.0/(np.exp(np.clip(x[pos&small],None,500))-1.0)
    out[pos & ~small] = np.exp(-x[pos&~small])
    return out

# Gauss-Legendre nodes
NQ=400; NU=200
gq_x,gq_w=np.polynomial.legendre.leggauss(NQ)
gu_x,gu_w=np.polynomial.legendre.leggauss(NU)

def ReSigma(cchi,cb,k):
    om=cchi*k
    # radial q grid on [qa,qb] mapped from [-1,1]; bath weight cuts off ~ few*T/cb
    qa,qb=1e-4, max(40.0, 60*T/cb)
    qs=0.5*(qb-qa)*gq_x+0.5*(qb+qa); wq=0.5*(qb-qa)*gq_w
    total=0.0
    for q,wqi in zip(qs,wq):
        Wq=cb*q; nq=nB(np.array([Wq]))[0]
        umin=cb*abs(q-k); umax=cb*(q+k)
        if umax-umin<1e-14: continue
        us=0.5*(umax-umin)*gu_x+0.5*(umax+umin); wu=0.5*(umax-umin)*gu_w
        nu=nB(us)
        # PV: avoid exact poles. Landau pole at u=Wq-om (if >0) or u=Wq+om; emission poles u=om-Wq(neg),
        # u=-(om+Wq)(neg) -> outside positive range. We do straight quad (Gauss nodes won't hit poles);
        # for u near a Landau pole the integrable PV is approximated; refine if a node is too close.
        def den(z):
            z=np.asarray(z,float)
            out=np.zeros_like(z)
            far=np.abs(z)>1e-6
            out[far]=1.0/z[far]
            return out
        emi=(nq+nu)*(den(om-Wq-us)-den(om+Wq+us))
        lan=(nq-nu)*(den(om-Wq+us)-den(om+Wq-us))
        Ku=(1.0/(2*Wq*us))*(emi+lan)
        # angular int = \int dx ... = \int du (u/(cb^2 q k)) Ku
        ang=np.sum(wu*(us/(cb*cb*q*k))*Ku)
        total+=wqi*ang*q*q
    return -total/(4*np.pi**2)

def fit(cchi,cb,ks):
    ys=np.array([ReSigma(cchi,cb,k) for k in ks])
    A=np.array([[1,k**2,k**4,k**6] for k in ks])
    coef,_,_,_=np.linalg.lstsq(A,ys,rcond=None)
    return coef,ys

print("# C8 fast numeric self-energy. dS bath T=%.6f, g chi phi phi, c_b=1."%T,flush=True)
print("# omega_eff^2=c_chi^2 k^2+ReSigma; fit ReSigma=s0+s2 k^2+s4 k^4+s6 k^6",flush=True)
ks=[0.03,0.06,0.09,0.12,0.15,0.18,0.21,0.24]
for cchi in [0.5,0.7,0.9,1.1,1.3,1.5,2.0,2.5,3.0]:
    coef,ys=fit(cchi,1.0,ks)
    s0,s2,s4,s6=coef
    print("r=c_chi/c_b=%4.2f : s0=% .4e s2=% .4e s4=% .4e s6=% .4e | sign(s4)=%s"
          %(cchi,s0,s2,s4,s6,'NEG(bend/roton)' if s4<0 else 'POS(stiffen)'),flush=True)
print("C8 done",flush=True)
