"""
agentOO Route 1, C5 — FORCED vs FREE: what controls sign(sigma4)?

We compute the k^4 coefficient of Re Sigma on-shell as a functional of a GENERIC bath occupation n(W)
(left abstract) and a GENERIC vertex factor, to see whether the SIGN is fixed by:
  (i) the dS Gibbons-Hawking Planck spectrum specifically (FORCED by the bath), or
  (ii) the coupling/operator choice (FREE).

Two clean sub-questions, each fast:

C5a — STIFFENING THEOREM for the emission channel.  The emission/absorption (pair) channel denominators
are  1/(omega - W_q - W_{q+k}) - 1/(omega + W_q + W_{q+k}). On-shell omega=c_chi k, for a GAPLESS external
mode and a bath, the sum (W_q + W_{q+k}) >> omega at the relevant q~T, so this is ~ -2/(W_q+W_{q+k}) which
is a SMOOTH, monotonic, positive-definite (after the -g^2) kernel. We test the SIGN of its k^4 curvature.

C5b — the FULL on-shell sigma4 sign as a function of c_chi/c_b (does it ever flip negative?). We integrate
numerically with the EXACT angular integral done analytically per q (no sqrt series in the radial var),
which is fast and exact.
"""
import sympy as sp
import mpmath as mp
mp.mp.dps = 30

# ---------- C5b: exact-angular, fast radial. ----------
# For fixed q and k, the angular integral over x=cos theta of the FULL kernel can be done in closed form
# because the only x-dependence is through W_{q+k}=c_b*sqrt(q^2+k^2+2qkx). Substitute u=W_{q+k}:
#   u in [c_b|q-k|, c_b(q+k)],  x = (u^2/c_b^2 - q^2 - k^2)/(2qk),  dx = u du/(c_b^2 q k).
# Then \int_{-1}^1 dx f(u) = \int_{c_b|q-k|}^{c_b(q+k)} (u/(c_b^2 q k)) f(u) du.
# The kernel f(u) = (1/(2 Wq u)) * [ (nq+nu)(1/(om-Wq-u)-1/(om+Wq+u)) + (nq-nu)(1/(om-Wq+u)-1/(om+Wq-u)) ]
# Each 1/(om±Wq±u) integrates to a log in u. So the angular integral is ELEMENTARY (logs). We do it
# numerically per q (1-D u integral) and then radial q integral. Fast and exact (PV handled by symmetric
# limits, the gapless om=c_chi k keeps poles off the integration range for c_chi<c_b on the emission side;
# Landau poles handled by mpmath PV via splitting).

H=mp.mpf(1); T=H/(2*mp.pi)
def nB(W):
    Wv=mp.mpf(W)
    if Wv<=0: return mp.mpf('1e30')
    x=Wv/T
    if x>50: return mp.e**(-x)
    return 1/(mp.e**x-1)

def ReSigma_exact(cchi, cb, k):
    cchi=mp.mpf(cchi); cb=mp.mpf(cb); k=mp.mpf(k)
    om=cchi*k
    def radial(q):
        q=mp.mpf(q)
        Wq=cb*q; nq=nB(Wq)
        umin=cb*abs(q-k); umax=cb*(q+k)
        def fu(u):
            u=mp.mpf(u); nu=nB(u)
            pref=u/(cb*cb*q*k) * 1/(2*Wq*u)   # u/(cb^2 q k) Jacobian * 1/(2 Wq u) vertex
            def PV(z):
                az=abs(z)
                if az<mp.mpf('1e-10'): return mp.mpf(0)
                return 1/z
            emi=(nq+nu)*(PV(om-Wq-u)-PV(om+Wq+u))
            lan=(nq-nu)*(PV(om-Wq+u)-PV(om+Wq-u))
            return pref*(emi+lan)*q*q
        # integrate u; split around any Landau pole u0 where om - Wq + u =0 => u=Wq-om, or om+Wq-u=0 => u=om+Wq
        pts=[umin]
        for u0 in [Wq-om, Wq+om]:
            if umin<u0<umax: pts.append(u0)
        pts.append(umax)
        pts=sorted(set([mp.mpf(p) for p in pts]))
        val=mp.mpf(0)
        for i in range(len(pts)-1):
            a,b=pts[i],pts[i+1]
            if b-a>mp.mpf('1e-12'):
                val+=mp.quad(fu,[a,b])
        return val
    I=mp.quad(radial,[mp.mpf('1e-5'),k+mp.mpf('1e-3'),5,30,100])
    return -I/(4*mp.pi**2)

def fit(cchi,cb):
    import numpy as np
    ks=[mp.mpf(s) for s in ['0.04','0.08','0.12','0.16','0.20','0.24','0.28']]
    ys=[ReSigma_exact(cchi,cb,k) for k in ks]
    A=np.array([[1,float(k)**2,float(k)**4,float(k)**6] for k in ks],float)
    b=np.array([float(y) for y in ys],float)
    coef,_,_,_=np.linalg.lstsq(A,b,rcond=None)
    return coef,[float(y) for y in ys]

print("# C5b EXACT-angular self-energy, dS bath, g chi phi phi trilinear. T=%.5f"%float(T))
print("# omega_eff^2 = c_chi^2 k^2 + ReSigma ; fit ReSigma = s0+s2 k^2+s4 k^4+s6 k^6")
for cchi in ['0.5','0.7','0.9','1.1','1.5','2.0','3.0']:
    try:
        coef,ys=fit(cchi,'1.0')
        s0,s2,s4,s6=coef
        print("c_chi=%-4s s0=% .4e s2=% .4e s4=% .4e s6=% .4e | sign(s4)=%s"
              %(cchi,s0,s2,s4,s6,'NEG(bend/roton)' if s4<0 else 'POS(stiffen)'))
    except Exception as e:
        print("c_chi=%-4s ERROR %s"%(cchi,e))
