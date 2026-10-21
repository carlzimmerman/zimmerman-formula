#!/usr/bin/env python3
"""Step 10b: two-function spatially-spherical reduction h_ij = f(r) delta_ij + g(r) n_i n_j.
g-variation = shear (anisotropic stress) equation."""
import sympy as s

r = s.symbols('r', positive=True)
th, ph = s.symbols('theta phi', real=True)
K, beta, eta, gamma, a0 = s.symbols('K beta eta gamma a0', positive=True)
FV, FP, FPP = s.symbols('FV FP FPP', positive=True)
GV, GP = s.symbols('GV GP', positive=True)
PV, PP, PPP = s.symbols('PV PP PPP', positive=True)
NV, NP, NPP = s.symbols('NV NP NPP', positive=True)
rho = s.Function('rho')(r)
rho1 = s.symbols('rho1', positive=True)


def cr3(h, coords):
    n = len(coords); ginv = h.inv()
    G = [[[s.S.Zero]*n for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for c in range(n):
                G[a][b][c] = s.together(s.Rational(1, 2)*sum(
                    ginv[a, d]*(s.diff(h[d, b], coords[c]) + s.diff(h[d, c], coords[b])
                                - s.diff(h[b, c], coords[d])) for d in range(n)))
    Ric = s.zeros(n, n)
    for b in range(n):
        for d in range(n):
            tot = 0
            for a in range(n):
                tot += (s.diff(G[a][b][d], coords[a]) - s.diff(G[a][b][a], coords[d])
                        + sum(G[a][a][e]*G[e][b][d] - G[a][d][e]*G[e][b][a] for e in range(n)))
            Ric[b, d] = s.together(tot)
    Rs = s.together(sum(ginv[b, d]*Ric[b, d] for b in range(n) for d in range(n)))
    return Rs


fF = s.Function('f')(r); gF = s.Function('g')(r)
h3 = s.diag(fF + gF, fF*r**2, fF*r**2*s.sin(th)**2)
R3F = cr3(h3, [r, th, ph])


def tojet(e):
    e = e.subs({s.Derivative(fF, (r, 2)): FPP, s.Derivative(fF, r): FP, fF: FV,
                s.Derivative(gF, r): GP, gF: GV})
    return s.expand(e)


R3 = tojet(R3F)
print('R3 =', R3)
print('check g=0:', s.simplify(R3.subs({GV: 0, GP: 0}) -
      (-2*FPP/FV**2 + s.Rational(3, 2)*FP**2/FV**3 - 4*FP/(r*FV**2))))

H = FV*s.sqrt(FV + GV)
uS = K*PV/s.sqrt(FV + GV)
W = a0**2/K*(-uS/a0 - s.log(1 - uS/a0))
dS = (1/H)*(1/r**2)*s.diff(r**2*FV*PV/s.sqrt(FV + GV), r)   # r-diff only via explicit P(r)
# rebuild dS in jet form by hand:
dS = s.expand((1/(FV*s.sqrt(FV + GV)))*s.diff(r**2*FV*PV/s.sqrt(FV + GV), r))
Lag = 4*s.pi*r**2*(NV*H*((R3)/(4*K) - W - (gamma/2)*dS**2)
                   + FV*PV*NP/s.sqrt(FV + GV) - rho*NV)


def Dt(e):
    out = s.diff(e, r)
    for v, dv, ddv in ((NV, NP, NPP), (FV, FP, FPP), (GV, GP, s.S.Zero),
                       (PV, PP, PPP)):
        out += s.diff(e, v)*dv + (s.diff(e, ddv)*ddv if ddv != s.S.Zero else 0)
    return out


Eg = s.expand(s.diff(Lag, GV) - Dt(s.diff(Lag, GP)))
EN = s.expand(Dt(s.diff(Lag, NP)) - s.diff(Lag, NV))
print('Eg len', len(str(Eg)), ' EN len', len(str(EN)))

n1 = s.Function('n1')(r); h1 = s.Function('h1')(r); G1 = s.Function('G1')(r)
p1 = s.Function('p1')(r)
n2 = s.Function('n2')(r); h2 = s.Function('h2')(r); G2 = s.Function('G2')(r)
p2 = s.Function('p2')(r)
eps = s.symbols('eps', positive=True)


def build(first, second, background):
    return {0: background, 1: first, 2: second}


sub = {}
for (v, dv, ddv), (a, b, bg) in (((NV, NP, NPP), (n1, n2, 1)),
                                 ((FV, FP, FPP), (h1, h2, 1)),
                                 ((GV, GP, 0), (G1, G2, 0)),
                                 ((PV, PP, PPP), (p1, p2, 0))):
    sub[v] = bg + eps*a + eps**2*b
    sub[dv] = eps*s.diff(a, r) + eps**2*s.diff(b, r)
    if ddv != 0:
        sub[ddv] = eps*s.diff(a, r, 2) + eps**2*s.diff(b, r, 2)
sub[rho] = eps*rho1

out = {}
for nm, E in [('Eg', Eg), ('EN', EN)]:
    e = s.expand(E.subs(sub))/(4*s.pi*r**2)
    ser = s.series(s.expand(e), eps, 0, 3).removeO()
    out[nm+'1'] = s.expand(s.expand(ser).coeff(eps, 1))
    out[nm+'2'] = s.expand(s.expand(ser).coeff(eps, 2))
print('\nO(eps) Eg :', s.factor(s.simplify(4*K*out['Eg1'])))
print('\nO(eps^2) Eg:', s.factor(s.expand(8*K*out['Eg2'])))
print('\nO(eps) EN :', s.factor(s.simplify(4*K*out['EN1'])))
