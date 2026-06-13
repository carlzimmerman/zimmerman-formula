"""
agentOO Route 1, C6 — the HTL / leading-thermal self-energy structure function, exact k-expansion.

The leading thermal (Hard Thermal Loop) self-energy of a scalar chi(omega,k) coupled g chi phi phi to a
bath of relativistic phi (dispersion W=c_b q, occupation n_B) has the universal angular structure

   Pi(omega,k) = m_th^2 * < f(omega, c_b k, x) >_angle

where m_th^2 = (g^2/ (2pi^2 c_b)) \int_0^inf q n_B(c_b q) dq  (positive thermal mass^2), and the structure
function from the forward/Landau region is the standard

   Pi(omega,k) = m_th^2 [ 1 - (omega/(2 c_b k)) ln( (omega + c_b k)/(omega - c_b k) ) ]

(this is the scalar analog of the gluon/photon HTL; the angular average of 1/(omega - c_b k x) gives the
log). Put it ON-SHELL omega = c_chi k. Then the argument is a fixed ratio r = c_chi/c_b and the WHOLE
structure function becomes k-INDEPENDENT(!) in the strict HTL (the leading m_th^2 term carries no extra k),
so the HTL gives sigma2 only, sigma4=0. The k^4 comes from the SUBLEADING (non-HTL) terms where the loop
momentum q ~ k matters. So we must go beyond strict HTL.

THEREFORE: the honest sigma4 comes from the full kernel (C5b). But C6 still gives the decisive structural
fact: ON-SHELL the HTL structure function is evaluated at FIXED r=c_chi/c_b, and its SIGN / curvature as we
perturb away from pure HTL is governed by whether omega < c_b k (r<1, INSIDE bath cone, Landau cut, log is
complex -> damping, real part from PV) or omega > c_b k (r>1, OUTSIDE, real log).

We compute here, EXACTLY and symbolically:
  (1) the on-shell HTL real part as function of r (to confirm sigma2 sign and the r<1 vs r>1 dichotomy);
  (2) the NEXT order in the gradient expansion (the q~k correction) that produces the first nonzero k^4,
      by expanding the full kernel's structure function keeping the q-recoil c_b k^2(1-x^2)/(2q) term.
"""
import sympy as sp

r = sp.symbols('r', positive=True)   # r = c_chi/c_b = omega/(c_b k) on-shell
# HTL structure function S(r) = 1 - (r/2) ln((r+1)/(r-1)) for r>1 (outside cone, real)
S_out = 1 - (r/2)*sp.log((r+1)/(r-1))
# r<1 (inside cone): PV real part = 1 - (r/2) ln((1+r)/(1-r))
S_in  = 1 - (r/2)*sp.log((1+r)/(1-r))

print("HTL on-shell structure function (multiplies +m_th^2, m_th^2>0):")
for lbl,S,dom in [('outside cone r>1',S_out,[sp.Rational(11,10),sp.Rational(3,2),sp.Integer(2),sp.Integer(3)]),
                  ('inside cone r<1', S_in,[sp.Rational(1,2),sp.Rational(7,10),sp.Rational(9,10)])]:
    print("  %s : S(r)="%lbl, sp.simplify(S))
    for rv in dom:
        print("     r=%s  S=% .5f"%(rv, float(S.subs(r,rv))))

# m_th^2 sign: positive (thermal mass). So sigma2 = m_th^2 * S(r):
#   sigma2 = m_th^2 S(r).  This RENORMALIZES c_chi^2 (a k^2 term). Its sign is S(r)'s sign.
# The dispersion CURVATURE (sigma4) requires the q-recoil correction. Build it:
print("\n# q-recoil correction -> first nonzero k^4 coefficient (sign test)")
q,k,x,cchi,cb,T,W = sp.symbols('q k x c_chi c_b T W', positive=True)
# energy denominator for the dominant emission pair, with q-recoil in W_{q+k}:
Wpk = cb*q + cb*k*x + cb*k**2*(1-x**2)/(2*q)   # to O(k^2)
Wq = cb*q
om = cchi*k
# emission pair real part kernel  R = 1/(om - Wq - Wpk) - 1/(om + Wq + Wpk), times (n(Wq)+n(Wpk))/(2WqWpk)
nq = 1/(sp.exp(Wq/T)-1)
npk = 1/(sp.exp(Wpk/T)-1)
Rk = (1/(om - Wq - Wpk) - 1/(om + Wq + Wpk))
ker = (nq+npk)/(2*Wq*Wpk)*Rk
ser = sp.series(sp.expand(ker), k, 0, 5).removeO()
ser_q2 = sp.expand(ser*q**2)
ang = sp.integrate(ser_q2,(x,-1,1))
poly = sp.Poly(sp.expand(ang),k)
print("emission-channel k^n coefficients (q-integrand):")
import mpmath as mp
mp.mp.dps=30
Tn = mp.mpf(1)/(2*mp.pi)
for cv in [mp.mpf('0.7'), mp.mpf('1.5'), mp.mpf('2.5')]:
    print(" c_chi=%s:"%cv)
    for nn in [0,2,4]:
        c = poly.coeff_monomial(k**nn)
        if c==0:
            print("   sigma%d=0"%nn); continue
        cc = c.subs({cb:1,cchi:cv,T:sp.nsimplify(float(Tn))})
        f = sp.lambdify(q, cc, 'mpmath')
        val = mp.quad(lambda Q:f(mp.mpf(Q)),[mp.mpf('1e-6'),5,30,100])
        val = -val/(4*mp.pi**2)
        print("   sigma%d=% .6e %s"%(nn,float(val),'<--SIGMA4' if nn==4 else ''))
