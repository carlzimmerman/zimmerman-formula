"""
agentOO Route 1, C12 — what is the TRUE small-k analytic structure of Re Sigma(c_chi k, k)?

C11 showed the lstsq 's4' GROWS as the fit window shrinks -> Re Sigma is NOT a clean even Taylor series;
there is a non-analytic / lower term contaminating. We must identify the genuine leading structure before
any 'sigma4' claim. We:
 (1) tabulate Re Sigma(k) on a fine small-k grid (Cauchy PV, the correct C10 kernel);
 (2) subtract the analytic s0+s2 k^2 (fit on the SMALLEST k's) and look at the residual scaling:
     log|R(k)| vs log k -> slope tells the leading non-(s0,s2) power p. p=4 => clean k^4; p=3 => odd
     thermal non-analyticity; p=4 with log => marginal.
 (3) Report the SIGN of the residual R(k) (does the dispersion bend down or stiffen up beyond k^2?),
     which is the physically meaningful 'does it fold' question regardless of integer-power labeling.

If the leading correction beyond c_chi^2 k^2 is NEGATIVE (R(k)<0, concave) -> bending/roton tendency.
If POSITIVE -> stiffening/convex. This is operator-independent-of-labeling honesty.
"""
import numpy as np
from scipy import integrate as sciint
H=1.0; T=H/(2*np.pi)
def nB(W):
    W=float(W)
    if W<=0: return 1e30
    x=W/T
    return np.exp(-x) if x>50 else 1.0/(np.exp(x)-1.0)
def ReSigma(cchi,cb,k):
    om=cchi*k
    def radial(q):
        Wq=cb*q; nq=nB(Wq); umin=cb*abs(q-k); umax=cb*(q+k)
        if umax-umin<1e-13: return 0.0
        Bconst=1.0/(2*Wq*cb*cb*q*k)
        def piece(gfun,u0):
            if umin<u0<umax:
                v,_=sciint.quad(gfun,umin,umax,weight='cauchy',wvar=u0,limit=200)
            else:
                v,_=sciint.quad(lambda u: gfun(u)/(u-u0),umin,umax,limit=200)
            return v
        tot =piece(lambda u:-(nq+nB(u)), om-Wq)
        tot+=piece(lambda u:-(nq+nB(u)), -(om+Wq))
        tot+=piece(lambda u:(nq-nB(u)), Wq-om)
        tot+=piece(lambda u:(nq-nB(u)), om+Wq)
        return Bconst*tot*q*q
    val,_=sciint.quad(radial,1e-5,max(40.0,60*T/cb),limit=300)
    return -val/(4*np.pi**2)

print("# C12 leading small-k structure of Re Sigma(c_chi k,k). T=%.6f, c_b=1."%T,flush=True)
for cchi in [0.7,1.3,2.0]:
    ks=np.array([0.02,0.03,0.04,0.05,0.06,0.08,0.10,0.13,0.16,0.20])
    ys=np.array([ReSigma(cchi,1.0,k) for k in ks])
    # fit s0+s2 k^2 on the 3 smallest k
    sm=ks[:3]; A=np.array([[1,k**2] for k in sm]); c,_,_,_=np.linalg.lstsq(A,ys[:3],rcond=None)
    s0,s2=c
    R=ys-(s0+s2*ks**2)            # residual beyond quadratic
    print("\n r=c_chi/c_b=%.2f : s0=% .4e s2=% .4e (from 3 smallest k)"%(cchi,s0,s2),flush=True)
    print("   k      ReSigma        R=resid(beyond k^2)   sign(R)",flush=True)
    for k,y,r in zip(ks,ys,R):
        print("   %.3f  % .6e   % .6e    %s"%(k,y,r,'+' if r>0 else '-'),flush=True)
    # slope of log|R| vs log k on the larger k where R is resolved
    mask=np.abs(R)>1e-9
    if mask.sum()>=3:
        p=np.polyfit(np.log(ks[mask][-5:]),np.log(np.abs(R[mask][-5:])),1)[0]
        print("   -> leading residual power p ~ %.2f  (4=clean k^4, 3=odd thermal, 2=just renorm)"%p,flush=True)
        print("   -> SIGN of beyond-quadratic correction: %s"%('POSITIVE=stiffen/convex' if np.median(R[mask])>0 else 'NEGATIVE=bend/concave'),flush=True)
print("C12 done",flush=True)
