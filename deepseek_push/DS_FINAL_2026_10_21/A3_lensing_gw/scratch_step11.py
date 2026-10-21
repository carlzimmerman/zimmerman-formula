#!/usr/bin/env python3
"""Step 11: two-function spherical reduction, hard-coded R3 (verified), shear eq."""
import sympy as s, time

r = s.symbols('r', positive=True)
K, beta, eta, gamma, a0 = s.symbols('K beta eta gamma a0', positive=True)
FV, FP, FPP = s.symbols('FV FP FPP', positive=True)
GV, GP = s.symbols('GV GP', positive=True)
PV, PP, PPP = s.symbols('PV PP PPP', positive=True)
NV, NP, NPP = s.symbols('NV NP NPP', positive=True)
rho = s.Function('rho')(r)
rho1 = s.symbols('rho1', positive=True)

A = FV + GV
B = FV*r**2
Ap = FP + GP
Bp = FP*r**2 + 2*FV*r
Bpp = FPP*r**2 + 4*FP*r + 2*FV
R3 = (4*A**2*B - 4*A*B*Bpp + A*Bp**2 + 2*B*Ap*Bp)/(2*A**2*B**2)
# sanity: g=0 -> old formula
old = -2*FPP/FV**2 + s.Rational(3, 2)*FP**2/FV**3 - 4*FP/(r*FV**2)
print('R3(g=0) ok:', s.simplify(R3.subs({GV: 0, GP: 0}) - old))

H = s.sqrt(A*B)                 # sqrt(det h) = sqrt(A B) = f r^2 sqrt(1+g/f)
uS = K*PV/s.sqrt(FV + GV)
W = a0**2/K*(-uS/a0 - s.log(1 - uS/a0))
# d = D_i P^i = (1/(r^2 sqrt(AB))) d/dr( r^2 sqrt(AB) P^r ), P^r = P/(f+g)
fsq = FV*PV/s.sqrt(FV + GV)     # sqrt(h) P^r  = f r^2 sqrt(1+g/f)*P/(f+g) = r^2 f P/sqrt(f+g)
# careful: sqrt(h)P^r = (f r^2 sqrt((f+g)/f)) * P/(f+g) = r^2 f P/sqrt(f+g)
num = s.diff(r**2*FV*PV/s.sqrt(FV + GV), r)
dS = num/(r**2*s.sqrt(A*B))
Lag = 4*s.pi*r**2*(NV*s.sqrt(A*B)*(R3/(4*K) - W - (gamma/2)*dS**2)
                   + FV*PV*NP/s.sqrt(FV + GV) - rho*NV)


def Dt(e):
    out = s.diff(e, r)
    for v, dv, ddv in ((NV, NP, NPP), (FV, FP, FPP), (GV, GP, None), (PV, PP, PPP)):
        out += s.diff(e, v)*dv
        if ddv is not None:
            out += s.diff(e, ddv)*ddv
    return out


t0 = time.time()
Eg = s.expand(s.diff(Lag, GV) - Dt(s.diff(Lag, GP)))
EN = s.expand(Dt(s.diff(Lag, NP)) - s.diff(Lag, NV))
print('built', time.time()-t0, len(str(Eg)), len(str(EN)))

n1 = s.Function('n1')(r); h1 = s.Function('h1')(r); G1 = s.Function('G1')(r)
p1 = s.Function('p1')(r)
n2 = s.Function('n2')(r); h2 = s.Function('h2')(r); G2 = s.Function('G2')(r)
p2 = s.Function('p2')(r)
eps = s.symbols('eps', positive=True)
sub = {}
for (v, dv, ddv), (a, b, bg) in (((NV, NP, NPP), (n1, n2, 1)),
                                 ((FV, FP, FPP), (h1, h2, 1)),
                                 ((GV, GP, None), (G1, G2, 0)),
                                 ((PV, PP, PPP), (p1, p2, 0))):
    sub[v] = bg + eps*a + eps**2*b
    sub[dv] = eps*s.diff(a, r) + eps**2*s.diff(b, r)
    if ddv is not None:
        sub[ddv] = eps*s.diff(a, r, 2) + eps**2*s.diff(b, r, 2)
sub[rho] = eps*rho1

out = {}
for nm, E in [('Eg', Eg), ('EN', EN)]:
    t0 = time.time()
    e = s.expand(E.subs(sub))/(4*s.pi*r**2)
    ser = s.series(s.expand(e), eps, 0, 3).removeO()
    out[nm+'1'] = s.expand(s.expand(ser).coeff(eps, 1))
    out[nm+'2'] = s.expand(s.expand(ser).coeff(eps, 2))
    print(nm, time.time()-t0)
print('\nO(eps) Eg :', s.factor(s.simplify(4*K*out['Eg1'])))
print('\nO(eps) EN :', s.factor(s.simplify(4*K*out['EN1'])))
print('\nO(eps^2) Eg:', s.factor(s.expand(8*K*out['Eg2'])))
