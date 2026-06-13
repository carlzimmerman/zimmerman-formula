"""
agentOO Route 1, C13 — DERIVATIVE coupling vertices: does sigma4 flip negative?

Same Cauchy-PV bubble machinery (C10), but with a momentum-dependent VERTEX FACTOR V(q,u,k) inside the
loop, modelling the admissible derivative operators:

 'scalar'      : V=1                                         (g chi phi phi)            [C10 baseline]
 'deriv2'      : V = (Wq*u - cb^2 q.(q+k))^2                  (chi (d phi)^2 : two bath derivatives)
                 with q.(q+k) recovered from u: cb^2 q.(q+k) = (u^2 - cb^2 q^2 - cb^2 k^2)/2 ... wait,
                 u=cb|q+k| so u^2=cb^2(q^2+k^2+2 q.k); cb^2 q.(q+k)=cb^2 q^2 + cb^2 q.k
                 = cb^2 q^2 + (u^2-cb^2 q^2-cb^2 k^2)/2 = (u^2+cb^2 q^2-cb^2 k^2)/2.
                 So q.(q+k)*cb^2 = (u^2 + cb^2 q^2 - cb^2 k^2)/2. Good, expressible in u.
 'deriv_ext'   : V = (om*Wq + ... )  external-derivative weighting ~ (om^2 + cb^2 q.(q+k))  (one external
                 derivative on chi, one on a bath line) — models (d chi).(phi d phi)-type.
 'timelike'    : V = (Wq*u + cb^2 q.(q+k))^2  (the OTHER sign contraction — relevant since the khronon
                 has a PREFERRED FRAME, the natural contraction is the TIME component (d_t chi)(d_t phi)^2
                 giving Wq*u with a + sign, not the Lorentz d_mu d^mu).

The khronon's foliation means the natural derivative is d_t along the preferred frame, i.e. ENERGY
factors Wq, u, om (not the Lorentz-invariant contraction). We test both the spatial-gradient and the
time-derivative weightings, since that choice is exactly the 'free coupling' the forced-vs-free axis asks
about.
"""
import numpy as np
from scipy import integrate as sciint
H=1.0; T=H/(2*np.pi)
def nB(W):
    W=float(W)
    if W<=0: return 1e30
    x=W/T
    return np.exp(-x) if x>50 else 1.0/(np.exp(x)-1.0)

def Vfac(kind,om,Wq,u,cb,q,k):
    qdotcb2 = (u*u + cb*cb*q*q - cb*cb*k*k)/2.0   # = cb^2 q.(q+k)
    if kind=='scalar':   return 1.0
    if kind=='deriv2':   return (Wq*u - qdotcb2)**2          # Lorentz (d phi)^2, both internal
    if kind=='timelike': return (Wq*u + qdotcb2)**2          # time-derivative weighting (preferred frame)
    if kind=='deriv_ext':return (om*Wq + qdotcb2)            # one external chi derivative * internal
    if kind=='grad2':    return (qdotcb2)**2                 # pure spatial gradient (d_i phi)^2
    return 1.0

def ReSigma(cchi,cb,k,kind):
    om=cchi*k
    def radial(q):
        Wq=cb*q; nq=nB(Wq); umin=cb*abs(q-k); umax=cb*(q+k)
        if umax-umin<1e-13: return 0.0
        Bconst=1.0/(2*Wq*cb*cb*q*k)
        def piece(sign,nfun,u0):
            # integrand g(u)/(u-u0) with g(u)=sign*nfun(u)*Vfac(u)
            def g(u): return sign*nfun(u)*Vfac(kind,om,Wq,u,cb,q,k)
            if umin<u0<umax:
                v,_=sciint.quad(g,umin,umax,weight='cauchy',wvar=u0,limit=200)
            else:
                v,_=sciint.quad(lambda u: g(u)/(u-u0),umin,umax,limit=200)
            return v
        tot =piece(-1.0,lambda u:(nq+nB(u)), om-Wq)
        tot+=piece(-1.0,lambda u:(nq+nB(u)), -(om+Wq))
        tot+=piece(+1.0,lambda u:(nq-nB(u)), Wq-om)
        tot+=piece(+1.0,lambda u:(nq-nB(u)), om+Wq)
        return Bconst*tot*q*q
    val,_=sciint.quad(radial,1e-5,max(40.0,60*T/cb),limit=300)
    return -val/(4*np.pi**2)

def beyond_quad_sign(cchi,kind):
    ks=np.array([0.03,0.05,0.07,0.10,0.13,0.16,0.20])
    ys=np.array([ReSigma(cchi,1.0,k,kind) for k in ks])
    A=np.array([[1,k**2] for k in ks[:2]]); c,_,_,_=np.linalg.lstsq(A,ys[:2],rcond=None)
    R=ys-(c[0]+c[1]*ks**2)
    # sign of the convexity beyond k^2: use the largest-k residuals (cleanest)
    med=np.median(R[-4:])
    return med, ys

print("# C13 derivative-vertex self-energy. dS bath T=%.6f, c_b=1."%T,flush=True)
print("# beyond-quadratic convexity sign: + = stiffen/convex, - = bend/roton-tendency",flush=True)
for kind in ['scalar','deriv2','timelike','grad2','deriv_ext']:
    row="%-10s | "%kind
    for cchi in [0.7,1.3,2.0]:
        med,ys=beyond_quad_sign(cchi,kind)
        row+="r=%.1f:%s(%.2e) "%(cchi,'STIFF' if med>0 else 'BEND',med)
    print(row,flush=True)
print("C13 done",flush=True)
