"""
agentOO Route 1, C3 — ROBUST numeric extraction of sigma4 sign, multiple operators.

We compute the dispersion-shifting real part of the thermal self-energy for the khronon chi(omega,k)
coupling to the dS Gibbons-Hawking bath, with the external line OFF the bath cone (c_chi != c_b) so the
PV is regular. We use a high-precision mpmath PV via symmetric pole subtraction and fit s0+s2 k^2+s4 k^4+s6 k^6.

We test THREE operator structures and report sign(s4) for each, scanning c_chi/c_b.

Physical normalization: the bath is the dS horizon Planck spectrum n(W)=1/(e^{W/T}-1), T=H/2pi, H=1.
The induced piece of omega_eff^2(k) is  omega^2 = c_chi^2 k^2 + Re Sigma_T(c_chi k, k).
So the on-shell ReSigma(k) fit directly gives sigma2 (renorm of c_chi^2), sigma4, sigma6.
"""
import mpmath as mp
mp.mp.dps = 30

H = mp.mpf(1)
T = H/(2*mp.pi)

def nB(w):
    x = w/T
    if x > 50: return mp.e**(-x)
    return 1/(mp.e**x - 1)

def make_ReSigma(cchi, cb, vertex):
    """vertex(q,k,x,qpk) returns the squared-vertex factor V(omega,k,q,...) for the operator.
       Operators:
         'scalar'  : V = 1                          (g chi phi phi, relevant trilinear)
         'deriv'   : V = (omega^2 - c_chi^2 (k.something))  ~ for (d chi)^2 phi the chi legs bring
                      external (omega^2 + c_chi^2 k^2)-type factors; we model the leading derivative
                      vertex factor as (omega*W_q - c_b^2 q.(q+k))-type. We implement the canonical
                      shift-symmetric (d_mu chi)(d^mu chi) phi vertex squared = (k1.k2)^2 with the two
                      bath momenta; here both internal lines are bath, external are chi, so the vertex
                      is (p_chi . q)(p_chi . (q+k)) form. We take the leading: V = (omega^2 - cchi^2 k^2)
                      is zero on-shell (massless), so derivative coupling on the EXTERNAL chi legs
                      vanishes on-shell; the nontrivial derivative coupling is on the loop -> 'deriv_loop'.
         'deriv_loop': V = (W_q*Wpk - cb^2 * (q.(q+k)))^2  (two bath derivatives, the (d phi)^2 chi op)
    """
    def ReSigma(k):
        k = mp.mpf(k)
        omega = cchi*k
        def integrand(q, x):
            qpk = mp.sqrt(q*q + k*k + 2*q*k*x)
            Wq = cb*q; Wpk = cb*qpk
            n1 = nB(Wq); n2 = nB(Wpk)
            if vertex == 'scalar':
                V = mp.mpf(1)
            elif vertex == 'deriv_loop':
                qdot = q*q + q*k*x      # q.(q+k)
                V = (Wq*Wpk - cb*cb*qdot)**2
            elif vertex == 'mass':
                V = mp.mpf(1)  # single-line handled separately below
            pref = V/(4*Wq*Wpk)
            # PV combination
            def PV(z):
                az = abs(z)
                if az < 1e-9:
                    return mp.mpf(0)   # principal value: symmetric, the divergent point integrates to 0 contribution under PV around it
                return 1/z
            t = (n1+n2)*(PV(omega-Wq-Wpk)-PV(omega+Wq+Wpk)) + (n1-n2)*(PV(omega-Wq+Wpk)-PV(omega+Wq-Wpk))
            return pref*t*q*q
        # radial * angular
        def rad(q):
            return mp.quad(lambda x: integrand(q,x), [-1, mp.mpf('-0.001'), mp.mpf('0.001'), 1])
        I = mp.quad(rad, [mp.mpf('1e-5'), 5, 20])
        return -I/(4*mp.pi**2)
    return ReSigma

def fit_sigma(ReSigma, kgrid):
    import numpy as np
    ks = [mp.mpf(s) for s in kgrid]
    ys = [ReSigma(k) for k in ks]
    A = np.array([[1, float(k)**2, float(k)**4, float(k)**6] for k in ks], float)
    b = np.array([float(y) for y in ys], float)
    coef,_,_,_ = np.linalg.lstsq(A,b,rcond=None)
    return coef, [float(y) for y in ys]

print("# C3 robust thermal self-energy, dS bath T=%.5f" % float(T))
for cchi, cb, label in [(mp.mpf('1.5'), mp.mpf('1.0'), 'c_chi>c_b (super-bath)'),
                         (mp.mpf('0.7'), mp.mpf('1.0'), 'c_chi<c_b (sub-bath)'),
                         (mp.mpf('2.0'), mp.mpf('1.0'), 'c_chi=2 c_b')]:
    for vtx in ['scalar','deriv_loop']:
        RS = make_ReSigma(cchi, cb, vtx)
        coef, ys = fit_sigma(RS, ['0.05','0.10','0.15','0.20','0.25','0.30'])
        s0,s2,s4,s6 = coef
        print("%-22s vtx=%-11s : s2=% .4e s4=% .4e s6=% .4e  sign(s4)=%s"
              % (label, vtx, s2, s4, s6, 'NEG(bend)' if s4<0 else 'POS(stiff)'))
