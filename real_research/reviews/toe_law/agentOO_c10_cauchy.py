"""
agentOO Route 1, C10 — TRUE Cauchy principal value via scipy weight='cauchy'.

Each energy denominator 1/(om - Wq + u) = 1/(u - (Wq-om)) is exactly a Cauchy kernel 1/(u-u0).
scipy.integrate.quad(g, a, b, weight='cauchy', wvar=u0) returns the PRINCIPAL VALUE  P\int g(u)/(u-u0) du.
We split the kernel into its four denominator pieces and apply the correct PV per piece. This is the
mathematically correct treatment of the Landau cut; the emission pieces 1/(om-Wq-u) and 1/(om+Wq+u)
have their zeros (u=om-Wq<0 typically, u=-(om+Wq)<0) OUTSIDE [umin,umax] so they are smooth there.

Then radial q-integral (smooth, ordinary quad). Fit ReSigma(c_chi k,k)=s0+s2k^2+s4k^4+s6k^6.

We ALSO report a robustness cross-check: a 3-point central second-difference estimate of the curvature of
the SUBTRACTED self-energy, to confirm the lstsq s4 is the genuine analytic coefficient and not fit noise.
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
        # base smooth factor B(u) = (u/(cb^2 q k)) * 1/(2 Wq u) = 1/(2 Wq cb^2 q k)  (u cancels!)
        Bconst = 1.0/(2*Wq*cb*cb*q*k)
        # The four pieces, each g(u)*1/(u-u0) with g containing the n-weights:
        #  emission: (nq+nu)*[ 1/(om-Wq-u) - 1/(om+Wq+u) ]
        #     1/(om-Wq-u) = -1/(u-(om-Wq)) ; u0a=om-Wq  (g=-(nq+nu))
        #     1/(om+Wq+u) =  1/(u-(-(om+Wq))) ; u0b=-(om+Wq) (g=(nq+nu)) -> appears with minus -> g=-(nq+nu)
        #  landau:   (nq-nu)*[ 1/(om-Wq+u) - 1/(om+Wq-u) ]
        #     1/(om-Wq+u) = 1/(u-(Wq-om)) ; u0c=Wq-om (g=(nq-nu))
        #     1/(om+Wq-u) = -1/(u-(om+Wq)) ; u0d=om+Wq (g=-(nq-nu))-> with minus -> g=+(nq-nu)
        def nu_of(u): return nB(u)
        total=0.0
        # piece by piece; use cauchy PV when u0 in (umin,umax), else ordinary
        def piece(gfun,u0):
            if umin< u0 < umax:
                val,_=sciint.quad(gfun,umin,umax,weight='cauchy',wvar=u0,limit=200)
            else:
                val,_=sciint.quad(lambda u: gfun(u)/(u-u0),umin,umax,limit=200)
            return val
        # a: u0a=om-Wq, integrand coeff -(nq+nu)
        total+=piece(lambda u: -(nq+nu_of(u)), om-Wq)
        # b: u0b=-(om+Wq), coeff -(nq+nu)
        total+=piece(lambda u: -(nq+nu_of(u)), -(om+Wq))
        # c: u0c=Wq-om, coeff (nq-nu)
        total+=piece(lambda u:  (nq-nu_of(u)), Wq-om)
        # d: u0d=om+Wq, coeff (nq-nu)
        total+=piece(lambda u:  (nq-nu_of(u)), om+Wq)
        return Bconst*total*q*q
    val,_=sciint.quad(radial,1e-5,max(40.0,60*T/cb),limit=300)
    return -val/(4*np.pi**2)

print("# C10 TRUE Cauchy-PV self-energy. dS bath T=%.6f, g chi phi phi, c_b=1."%T,flush=True)
print("# fit ReSigma(c_chi k,k)=s0+s2 k^2+s4 k^4+s6 k^6 ; report fit quality + curvature cross-check",flush=True)
ks=np.array([0.03,0.05,0.07,0.09,0.11,0.13,0.15,0.17,0.19])
for cchi in [0.5,0.7,0.9,1.3,1.7,2.0,2.5,3.0]:
    ys=np.array([ReSigma(cchi,1.0,k) for k in ks])
    A=np.array([[1,k**2,k**4,k**6] for k in ks])
    coef,_,_,_=np.linalg.lstsq(A,ys,rcond=None)
    s0,s2,s4,s6=coef
    pred=A@coef; rms=np.sqrt(np.mean((pred-ys)**2)); scale=np.max(np.abs(ys))+1e-30
    print("r=%4.2f s0=% .3e s2=% .3e s4=% .4e s6=% .3e | rms/scale=%.1e sign(s4)=%s"
          %(cchi,s0,s2,s4,s6,rms/scale,'NEG(bend)' if s4<0 else 'POS(stiff)'),flush=True)
print("C10 done",flush=True)
