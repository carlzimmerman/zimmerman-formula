#!/usr/bin/env python3
"""Step 5: second-order equations. Extract the O(eps^2) coefficients of EN,Ef,EP
and print them factored, to identify the slip equation."""
import sympy as s
import pickle, time

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
Lag = 4*s.pi*r**2*(Nv*fv**s.Rational(3, 2)*((R3 - 2*Lam)/(4*K) - W - (gamma/2)*d**2)
                   + sq*Pv*Np - rho*Nv)


def Dt(e):
    return (s.diff(e, r) + s.diff(e, Nv)*Np + s.diff(e, Np)*Npp
            + s.diff(e, fv)*fp + s.diff(e, fp)*fpp
            + s.diff(e, Pv)*Pp + s.diff(e, Pp)*Ppp)


t0 = time.time()
EN = s.expand(Dt(s.diff(Lag, Np)) - s.diff(Lag, Nv))
Ef = s.expand(s.diff(Lag, fv) - Dt(s.diff(Lag, fp)) + Dt(Dt(s.diff(Lag, fpp))))
EP = s.expand(s.diff(Lag, Pv) - Dt(s.diff(Lag, Pp)))
print('built', time.time()-t0, [len(str(e)) for e in (EN, Ef, EP)])

n1 = s.Function('n1')(r); h1 = s.Function('h1')(r); p1 = s.Function('p1')(r)
n2 = s.Function('n2')(r); h2 = s.Function('h2')(r); p2 = s.Function('p2')(r)
eps = s.symbols('eps', positive=True)
sub = {Nv: 1 + eps*n1 + eps**2*n2, Np: eps*s.diff(n1, r) + eps**2*s.diff(n2, r),
       Npp: eps*s.diff(n1, r, 2) + eps**2*s.diff(n2, r, 2),
       fv: 1 + eps*h1 + eps**2*h2, fp: eps*s.diff(h1, r) + eps**2*s.diff(h2, r),
       fpp: eps*s.diff(h1, r, 2) + eps**2*s.diff(h2, r, 2),
       Pv: eps*p1 + eps**2*p2, Pp: eps*s.diff(p1, r) + eps**2*s.diff(p2, r),
       Ppp: eps*s.diff(p1, r, 2) + eps**2*s.diff(p2, r, 2), rho: eps*rho1, Lam: 0}

res = {}
for nm, E in [('EN', EN), ('Ef', Ef), ('EP', EP)]:
    t0 = time.time()
    e = s.expand(E.subs(sub))
    for k in (1, 2):
        ck = s.expand(s.series(s.expand(e/(4*s.pi*r**2)), eps, 0, 3).removeO()).coeff(eps, k)
        res[(nm, k)] = s.expand(ck)
    print(nm, 'done', time.time()-t0, len(str(res[(nm, 2)])))
with open('scratch_step5.pkl', 'wb') as fh:
    pickle.dump({k: str(v) for k, v in res.items()}, fh)
print('\n--- O(eps) checks (Lam=0) ---')
print('EN1 :', s.factor(s.simplify(res[('EN', 1)]*K)))
print('Ef1 :', s.factor(s.simplify(res[('Ef', 1)]*K)))
print('\n--- O(eps^2) Ef, grouped ---')
Ef2 = s.expand(res[('Ef', 2)]*K)
print('n2 coeff :', s.factor(Ef2.coeff(s.diff(n2, r, 2))))
print('h2 coeff :', s.factor(Ef2.coeff(s.diff(h2, r, 2))))
print('p2 coeff :', s.factor(Ef2.coeff(s.diff(p2, r, 2))))
print('has p2  :', Ef2.has(p2), ' has n2 :', Ef2.has(n2))
