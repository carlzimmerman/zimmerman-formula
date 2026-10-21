#!/usr/bin/env python3
"""Step 7 (single process): exact EL equations, O(eps), O(eps^2); validate the
second-order slip equation on pure-GR Schwarzschild."""
import sympy as s, time

r = s.symbols('r', positive=True)
K, beta, eta, gamma, a0, Lam = s.symbols('K beta eta gamma a0 Lambda', positive=True)
Nv, Np, Npp, fv, fp, fpp, Pv, Pp, Ppp = s.symbols(
    'Nv Np Npp fv fp fpp Pv Pp Ppp', positive=True)
rho = s.Function('rho')(r)
rho1 = s.symbols('rho1', positive=True)
sq = s.sqrt(fv)
R3 = -2*fpp/fv**2 + s.Rational(3, 2)*fp**2/fv**3 - 4*fp/(r*fv**2)
uS = K*Pv/sq
W = a0**2/K*(-uS/a0 - s.log(1 - uS/a0))
dS = Pp/fv + 2*Pv/(r*fv) + fp*Pv/(2*fv**2)
Lag = 4*s.pi*r**2*(Nv*fv**s.Rational(3, 2)*((R3 - 2*Lam)/(4*K) - W - (gamma/2)*dS**2)
                   + sq*Pv*Np - rho*Nv)


def Dt(e):
    return (s.diff(e, r) + s.diff(e, Nv)*Np + s.diff(e, Np)*Npp
            + s.diff(e, fv)*fp + s.diff(e, fp)*fpp
            + s.diff(e, Pv)*Pp + s.diff(e, Pp)*Ppp)


EN = s.expand(Dt(s.diff(Lag, Np)) - s.diff(Lag, Nv))
Ef = s.expand(s.diff(Lag, fv) - Dt(s.diff(Lag, fp)) + Dt(Dt(s.diff(Lag, fpp))))
EP = s.expand(s.diff(Lag, Pv) - Dt(s.diff(Lag, Pp)))

n1 = s.Function('n1')(r); h1 = s.Function('h1')(r); p1 = s.Function('p1')(r)
n2 = s.Function('n2')(r); h2 = s.Function('h2')(r); p2 = s.Function('p2')(r)
eps = s.symbols('eps', positive=True)
sub = {Nv: 1 + eps*n1 + eps**2*n2, Np: eps*s.diff(n1, r) + eps**2*s.diff(n2, r),
       Npp: eps*s.diff(n1, r, 2) + eps**2*s.diff(n2, r, 2),
       fv: 1 + eps*h1 + eps**2*h2, fp: eps*s.diff(h1, r) + eps**2*s.diff(h2, r),
       fpp: eps*s.diff(h1, r, 2) + eps**2*s.diff(h2, r, 2),
       Pv: eps*p1 + eps**2*p2, Pp: eps*s.diff(p1, r) + eps**2*s.diff(p2, r),
       Ppp: eps*s.diff(p1, r, 2) + eps**2*s.diff(p2, r, 2), rho: eps*rho1, Lam: 0}
E1, E2 = {}, {}
for nm, E in [('EN', EN), ('Ef', Ef), ('EP', EP)]:
    e = s.expand(E.subs(sub))/(4*s.pi*r**2)
    ser = s.series(s.expand(e), eps, 0, 3).removeO()
    E1[nm] = s.expand(s.expand(ser).coeff(eps, 1))
    E2[nm] = s.expand(s.expand(ser).coeff(eps, 2))
print('built ok')
print('\nE1 lapse :', s.factor(s.simplify(E1['EN']*K)))
print('E1 metric:', s.factor(s.simplify(E1['Ef']*K)))
print('E1 P     :', s.factor(s.simplify(E1['EP']*K)))
Ef2 = s.expand(4*K*E2['Ef'])
S2 = n2 + h2/2
linpart = s.expand(Ef2.subs({n1: 0, h1: 0}))
print('\nlinear part of 4K*Ef2 :', s.factor(linpart))
print('Q (quadratic part)     :', s.factor(s.expand(Ef2 - linpart)))
