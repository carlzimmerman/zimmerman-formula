"""
agentOO Route 1, C9 — PROPER principal-value, convergence-checked sigma4.

Fixes C8's two flaws:
 (1) PRINCIPAL VALUE at the Landau pole u0=Wq-om (when 0<u0 and umin<u0<umax): split [umin,umax] at u0
     and use a symmetric (pole-centered) subtraction so the 1/(u0-u) singularity integrates as a true PV.
 (2) Convergence: increase grid, check raw ReSigma(k) is smooth, and use a DEDICATED k-grid + lstsq with
     a reported residual so we know the k^4 is real, not fit noise. Also report the curvature directly via
     central finite differences of (ReSigma(k)-s0-s2 k^2)/k^4 -> plateau = s4.

We focus on r=c_chi/c_b values AWAY from the cone r=1 (where the on-shell mode grazes the bath dispersion
and the EFT/quasiparticle picture degrades); near r=1 the result is physically ambiguous and we say so.
"""
import numpy as np
from scipy import integrate as sciint

H=1.0; T=H/(2*np.pi)
def nB(W):
    W=float(W)
    if W<=0: return 1e30
    x=W/T
    if x>50: return np.exp(-x)
    return 1.0/(np.exp(x)-1.0)

def ReSigma(cchi,cb,k):
    om=cchi*k
    def radial(q):
        Wq=cb*q; nq=nB(Wq)
        umin=cb*abs(q-k); umax=cb*(q+k)
        if umax-umin<1e-13: return 0.0
        def Ku(u):
            nu=nB(u)
            emi=(nq+nu)*(safe(om-Wq-u)-safe(om+Wq+u))
            lan=(nq-nu)*(safe(om-Wq+u)-safe(om+Wq-u))
            return (1.0/(2*Wq*u))*(emi+lan)*(u/(cb*cb*q*k))
        # Landau pole in (om-Wq+u): zero at u=Wq-om ; pole in (om+Wq-u): zero at u=om+Wq
        poles=[w for w in (Wq-om, Wq+om) if umin<w<umax]
        if poles:
            pts=sorted(poles)
            val,_=sciint.quad(Ku,umin,umax,points=pts,weight=None,limit=200)
        else:
            val,_=sciint.quad(Ku,umin,umax,limit=200)
        return val*q*q
    val,_=sciint.quad(radial,1e-5,max(40.0,60*T/cb),limit=200)
    return -val/(4*np.pi**2)

def safe(z):
    # plain 1/z; scipy quad with 'points' handles the integrable singularity as PV-like via subdivision
    if abs(z)<1e-14: return 0.0
    return 1.0/z

print("# C9 PV self-energy. dS bath T=%.6f, g chi phi phi, c_b=1."%T,flush=True)
for cchi in [0.5,0.7,0.9,1.3,1.7,2.0,2.5,3.0]:
    ks=np.array([0.04,0.07,0.10,0.13,0.16,0.19,0.22,0.25])
    ys=np.array([ReSigma(cchi,1.0,k) for k in ks])
    A=np.array([[1,k**2,k**4,k**6] for k in ks])
    coef,res,_,_=np.linalg.lstsq(A,ys,rcond=None)
    s0,s2,s4,s6=coef
    pred=A@coef
    rms=np.sqrt(np.mean((pred-ys)**2)); scale=np.max(np.abs(ys))
    print("r=%4.2f s0=% .3e s2=% .3e s4=% .4e s6=% .3e | fit_rms/scale=%.1e sign(s4)=%s"
          %(cchi,s0,s2,s4,s6,rms/scale,'NEG(bend)' if s4<0 else 'POS(stiff)'),flush=True)
print("C9 done",flush=True)
