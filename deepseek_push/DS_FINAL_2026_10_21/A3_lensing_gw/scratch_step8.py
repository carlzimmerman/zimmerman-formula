#!/usr/bin/env python3
"""Step 8: clean second-order slip equation + Schwarzschild second-order check."""
import sympy as s

r = s.symbols('r', positive=True)
K, beta, eta, gamma, a0 = s.symbols('K beta eta gamma a0', positive=True)
Nv, Np, Npp, fv, fp, fpp, Pv, Pp, Ppp = s.symbols(
    'Nv Np Npp fv fp fpp Pv Pp Ppp', positive=True)
rho = s.Function('rho')(r)
rho1 = s.symbols('rho1', positive=True)
sq = s.sqrt(fv)
R3 = -2*fpp/fv**2 + s.Rational(3, 2)*fp**2/fv**3 - 4*fp/(r*fv**2)
uS = K*Pv/sq
W = a0**2/K*(-uS/a0 - s.log(1 - uS/a0))
dS = Pp/fv + 2*Pv/(r*fv) + fp*Pv/(2*fv**2)
Lag = 4*s.pi*r**2*(Nv*fv**s.Rational(3, 2)*((R3)/(4*K) - W - (gamma/2)*dS**2)
                   + sq*Pv*Np - rho*Nv)


def Dt(e):
    return (s.diff(e, r) + s.diff(e, Nv)*Np + s.diff(e, Np)*Npp
            + s.diff(e, fv)*fp + s.diff(e, fp)*fpp
            + s.diff(e, Pv)*Pp + s.diff(e, Pp)*Ppp)


Ef = s.expand(s.diff(Lag, fv) - Dt(s.diff(Lag, fp)) + Dt(Dt(s.diff(Lag, fpp))))
EN = s.expand(Dt(s.diff(Lag, Np)) - s.diff(Lag, Nv))
EP = s.expand(s.diff(Lag, Pv) - Dt(s.diff(Lag, Pp)))

n1 = s.Function('n1')(r); h1 = s.Function('h1')(r); p1 = s.Function('p1')(r)
n2 = s.Function('n2')(r); h2 = s.Function('h2')(r); p2 = s.Function('p2')(r)
eps = s.symbols('eps', positive=True)
sub = {Nv: 1 + eps*n1 + eps**2*n2, Np: eps*s.diff(n1, r) + eps**2*s.diff(n2, r),
       Npp: eps*s.diff(n1, r, 2) + eps**2*s.diff(n2, r, 2),
       fv: 1 + eps*h1 + eps**2*h2, fp: eps*s.diff(h1, r) + eps**2*s.diff(h2, r),
       fpp: eps*s.diff(h1, r, 2) + eps**2*s.diff(h2, r, 2),
       Pv: eps*p1 + eps**2*p2, Pp: eps*s.diff(p1, r) + eps**2*s.diff(p2, r),
       Ppp: eps*s.diff(p1, r, 2) + eps**2*s.diff(p2, r, 2), rho: eps*rho1}
E1, E2 = {}, {}
for nm, E in [('EN', EN), ('Ef', Ef), ('EP', EP)]:
    e = s.expand(E.subs(sub))/(4*s.pi*r**2)
    ser = s.series(s.expand(e), eps, 0, 3).removeO()
    E1[nm] = s.expand(s.expand(ser).coeff(eps, 1))
    E2[nm] = s.expand(s.expand(ser).coeff(eps, 2))

Ef2 = s.expand(4*K*E2['Ef'])
zero1 = {n1: s.S.Zero, h1: s.S.Zero, p1: s.S.Zero}
linpart = s.expand(s.expand(Ef2.subs(zero1)).doit())
quad = s.expand(s.expand(Ef2 - linpart).doit())
print('linear part :', s.factor(linpart))
print()
print('Q           :', s.factor(quad))
print()
# ---- Schwarzschild second order check (gamma-free, p=0) ----
m = s.symbols('m', positive=True)
# exact isotropic Schwarzschild: g_tt=-((1-m/r)/(1+m/r))^2 , f=(1+m/r)^4
Nex = (1 - m/r)/(1 + m/r)
fex = (1 + m/r)**4
print('is Ef2 satisfied by the exact Schwarzschild expansion?')
# expand exact metric in eps: N = 1+eps n1+eps^2 n2 with eps~m/r
# Phi=-U+U^2 ..., U=m*2/r?  do it exactly instead: substitute exact functions
subex = {Nv: Nex, Np: s.diff(Nex, r), Npp: s.diff(Nex, r, 2),
         fv: fex, fp: s.diff(fex, r), fpp: s.diff(fex, r, 2),
         Pv: 0, Pp: 0, Ppp: 0, rho: 0, gamma: s.Symbol('gamma')}
print('Ef(exact Schwarzschild) =', s.simplify(Ef.subs({k: v for k, v in subex.items() if k != 'gamma'})))
# second-order check: n1=-U, h1=2U with U=GM/r ; n2=U^2, h2=3/2 U^2
U = s.symbols('U', positive=True)
GM = s.symbols('GM', positive=True)
Uexpr = GM/r
n1e = -Uexpr; h1e = 2*Uexpr; n2e = Uexpr**2; h2e = s.Rational(3, 2)*Uexpr**2
rep = {n1: n1e, s.diff(n1, r): s.diff(n1e, r), s.diff(n1, r, 2): s.diff(n1e, r, 2),
       h1: h1e, s.diff(h1, r): s.diff(h1e, r), s.diff(h1, r, 2): s.diff(h1e, r, 2),
       n2: n2e, s.diff(n2, r): s.diff(n2e, r), s.diff(n2, r, 2): s.diff(n2e, r, 2),
       h2: h2e, s.diff(h2, r): s.diff(h2e, r), s.diff(h2, r, 2): s.diff(h2e, r, 2),
       p1: 0, s.diff(p1, r): 0, s.diff(p1, r, 2): 0, p2: 0,
       s.diff(p2, r): 0, s.diff(p2, r, 2): 0, rho1: 0}
res = s.simplify(Ef2.subs(rep))
print('4K*Ef2 on (n1=-U,h1=2U,n2=U^2,h2=1.5U^2):', res)
