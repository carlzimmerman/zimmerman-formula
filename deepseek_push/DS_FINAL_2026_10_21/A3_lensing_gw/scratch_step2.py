#!/usr/bin/env python3
"""Step 2: exact static-spherical EL equations from the ADM action; validate
against Schwarzschild and against the round-1 leading-order system."""
import sympy as s

r = s.symbols('r', positive=True)
K, beta, eta, gamma, a0, Lam = s.symbols('K beta eta gamma a0 Lambda', positive=True)
Nv, Np, Npp, fv, fp, fpp, Pv, Pp, Ppp = s.symbols(
    'Nv Np Npp fv fp fpp Pv Pp Ppp', positive=True)
rho = s.Function('rho')(r)
rho1 = s.symbols('rho1', positive=True)

sq = s.sqrt(fv)
R3 = -2*fpp/fv**2 + s.Rational(3, 2)*fp**2/fv**3 - 4*fp/(r*fv**2)
u = K*Pv/sq
W = a0**2/K*(-u/a0 - s.log(1 - u/a0))
d = Pp/fv + 2*Pv/(r*fv) + fp*Pv/(2*fv**2)
Lag = 4*s.pi*r**2*Nv*fv**s.Rational(3, 2)*((R3 - 2*Lam)/(4*K) + Pv*Np/Nv - W
                                          - (gamma/2)*d**2 - rho)


def Dt(e):
    return (s.diff(e, r) + s.diff(e, Nv)*Np + s.diff(e, Np)*Npp
            + s.diff(e, fv)*fp + s.diff(e, fp)*fpp
            + s.diff(e, Pv)*Pp + s.diff(e, Pp)*Ppp)


EN = s.simplify(s.cancel((Dt(s.diff(Lag, Np)) - s.diff(Lag, Nv))/(4*s.pi*r**2)))
Ef = s.simplify(s.cancel((s.diff(Lag, fv) - Dt(s.diff(Lag, fp))
                          + Dt(Dt(s.diff(Lag, fpp))))/(4*s.pi*r**2)))
EP = s.simplify(s.cancel((s.diff(Lag, Pv) - Dt(s.diff(Lag, Pp)))/(4*s.pi*r**2)))
for nm, e in [('EN', EN), ('Ef', Ef), ('EP', EP)]:
    print(nm, 'has Npp', e.has(Npp), 'Ppp', e.has(Ppp), 'len', len(str(e)))

# ---------- check A: Schwarzschild isotropic (P=0, Lam=0, rho=0) ----------
m = s.symbols('m', positive=True)
Nr = (1 - m/r)/(1 + m/r)
fr = (1 + m/r)**4
sub0 = {Pv: 0, Pp: 0, Ppp: 0, Lam: 0, rho: 0, Nv: Nr, Np: s.diff(Nr, r),
        Npp: s.diff(Nr, r, 2), fv: fr, fp: s.diff(fr, r), fpp: s.diff(fr, r, 2)}
print('EN(Schw) =', s.simplify(EN.subs(sub0)))
print('Ef(Schw) =', s.simplify(Ef.subs(sub0)))
print('EP(Schw) =', s.simplify(EP.subs(sub0)))

# ---------- check B: round-1 leading order ----------
eps = s.symbols('eps', positive=True)
n1 = s.Function('n1')(r); h1 = s.Function('h1')(r); p1 = s.Function('p1')(r)


def lin(e, order=1):
    e = s.expand(e.subs({Nv: 1 + eps*n1, Np: eps*s.diff(n1, r), Npp: eps*s.diff(n1, r, 2),
                         fv: 1 + eps*h1, fp: eps*s.diff(h1, r), fpp: eps*s.diff(h1, r, 2),
                         Pv: eps*p1, Pp: eps*s.diff(p1, r), Ppp: eps*s.diff(p1, r, 2),
                         rho: eps*rho1}))
    return s.expand(s.series(e, eps, 0, order + 1).removeO()).coeff(eps, order)
for nm, e in [('lapse', EN), ('metric', Ef), ('P', EP)]:
    print('\nO(eps)', nm, ':', s.factor(s.simplify(lin(e)*K)))
