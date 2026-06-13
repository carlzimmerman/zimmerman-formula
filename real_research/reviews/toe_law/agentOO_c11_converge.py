"""
agentOO Route 1, C11 — convergence-controlled sigma4 + channel decomposition.

Two improvements over C10:
  (A) SMALLER k window + Richardson-style check: fit s0+s2k^2+s4k^4 on a small-k window where s6 is
      negligible, and verify s4 is STABLE as the window shrinks (true Taylor coefficient, not fit noise).
  (B) Channel decomposition: report sigma4 from the EMISSION channel and the LANDAU channel SEPARATELY,
      so we see which one carries the sign and whether either can be negative.

Cauchy PV from C10 (correct). g chi phi phi, c_b=1, dS bath.
"""
import numpy as np
from scipy import integrate as sciint
H=1.0; T=H/(2*np.pi)
def nB(W):
    W=float(W)
    if W<=0: return 1e30
    x=W/T
    return np.exp(-x) if x>50 else 1.0/(np.exp(x)-1.0)

def ReSigma(cchi,cb,k,channels=('emi','lan')):
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
        tot=0.0
        if 'emi' in channels:
            tot+=piece(lambda u:-(nq+nB(u)), om-Wq)
            tot+=piece(lambda u:-(nq+nB(u)), -(om+Wq))
        if 'lan' in channels:
            tot+=piece(lambda u:(nq-nB(u)), Wq-om)
            tot+=piece(lambda u:(nq-nB(u)), om+Wq)
        return Bconst*tot*q*q
    val,_=sciint.quad(radial,1e-5,max(40.0,60*T/cb),limit=300)
    return -val/(4*np.pi**2)

def s4_window(cchi,kmax,channels):
    ks=np.linspace(0.2*kmax,kmax,7)
    ys=np.array([ReSigma(cchi,1.0,k,channels) for k in ks])
    A=np.array([[1,k**2,k**4] for k in ks])  # 3-term: small window, drop k^6
    coef,_,_,_=np.linalg.lstsq(A,ys,rcond=None)
    pred=A@coef; rms=np.sqrt(np.mean((pred-ys)**2)); scale=np.max(np.abs(ys))+1e-30
    return coef[2], rms/scale

print("# C11 convergence + channel decomposition. dS bath T=%.6f."%T,flush=True)
print("# s4 from shrinking k-windows (kmax=0.20,0.12,0.07); STABLE sign = real Taylor coeff",flush=True)
for cchi in [0.5,0.7,1.3,2.0,3.0]:
    row="r=%4.2f | "%cchi
    for ch,lab in [(('emi','lan'),'FULL'),(('emi',),'emi'),(('lan',),'lan')]:
        vals=[]
        for kmax in [0.20,0.12,0.07]:
            s4,q=s4_window(cchi,kmax,ch)
            vals.append(s4)
        sgn='NEG' if vals[-1]<0 else 'POS'
        row+="%s s4@[.20,.12,.07]=[% .2e,% .2e,% .2e]->%s ; "%(lab,vals[0],vals[1],vals[2],sgn)
    print(row,flush=True)
print("C11 done",flush=True)
