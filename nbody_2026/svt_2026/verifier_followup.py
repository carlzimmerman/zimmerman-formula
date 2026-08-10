#!/usr/bin/env python3
"""Follow-ups: (i) J-term recomputed via lower-index route (cross-check of DeltaL2);
(ii) claim 6 B-term independent check; (iii) claim 15 bump branch in FULL theory."""
import sympy as sp
from sympy import Rational as R
import numpy as np
import functools
print = functools.partial(print, flush=True)
def chk(c, l): print(("  [OK ] " if c else "  [BAD] ") + l); return bool(c)

t, z = sp.symbols('t z', real=True)
eps = sp.Symbol('eps', positive=True); k = sp.Symbol('k', positive=True)
G = sp.Symbol('G', positive=True); KB = sp.Symbol('K_B', real=True)
a = sp.Function('a', positive=True)(t)
P = sp.Function('P')(t); S = sp.Function('S')(t); X = sp.Function('X')(t)
al = sp.Function('s')(t); phib = sp.Function('phib')(t)
Qb = sp.Derivative(phib, t)
C, Sn = sp.cos(k*z), sp.sin(k*z)
Phi, Psi, chi, alpha = eps*P*C, eps*S*C, eps*X*C, eps*al*C
gdn = sp.diag(-(1+2*Phi), a**2*(1-2*Psi), a**2*(1-2*Psi), a**2*(1-2*Psi))
gup = sp.diag(-1/(1+2*Phi), 1/(a**2*(1-2*Psi)), 1/(a**2*(1-2*Psi)), 1/(a**2*(1-2*Psi)))
sqrtg = sp.sqrt(1+2*Phi)*a**3*(1-2*Psi)**R(3,2)
Az = sp.diff(alpha, z)/a**2
A0 = sp.sqrt((1 + gdn[3,3]*Az**2)/(1+2*Phi))
co = [t, sp.Symbol('x1'), sp.Symbol('x2'), z]
phf = phib + chi

def tay(e, n):
    out, cur, fact = [], e, 1
    for i in range(n+1):
        out.append(sp.expand(cur.subs(eps, 0)/fact))
        if i < n: cur = sp.diff(cur, eps); fact *= (i+1)
    return out

# (i) lower-index route: J_mu = A^nu (d_nu A_mu - Gamma^lam_{nu mu} A_lam); Jphi = g^{mu rho} J_rho d_mu phi
Aup = {0: A0, 3: Az}
Adn = {0: gdn[0,0]*A0, 3: gdn[3,3]*Az}
def Gam(lam, nu, mu):   # Gamma^lam_{nu mu}, diagonal metric
    return sp.expand(gup[lam,lam]*(sp.diff(gdn[lam,mu], co[nu]) + sp.diff(gdn[lam,nu], co[mu])
                                   - sp.diff(gdn[nu,mu], co[lam]))/2)
Jdn = {}
for mu in (0, 3):
    s_ = 0
    for nu in (0, 3):
        s_ += Aup[nu]*sp.diff(Adn[mu], co[nu])
        for lam in (0, 3):
            s_ -= Aup[nu]*Gam(lam, nu, mu)*Adn[lam]
    Jdn[mu] = s_
Jphi_low = gup[0,0]*Jdn[0]*sp.diff(phf, t) + gup[3,3]*Jdn[3]*sp.diff(phf, z)
# upper-index route (as in main verifier)
Jup = {}
for mu in (0, 3):
    s_ = 0
    for nu in (0, 3):
        s_ += Aup[nu]*sp.diff(Aup[mu], co[nu])
        for lam in (0, 3):
            s_ += Aup[nu]*Gam(mu, nu, lam)*Aup[lam]
    Jup[mu] = s_
Jphi_up = Jup[0]*sp.diff(phf, t) + Jup[3]*sp.diff(phf, z)
d = sp.simplify(tay(Jphi_low - Jphi_up, 2)[2])
chk(d == 0 and sp.simplify(tay(Jphi_low - Jphi_up, 1)[1]) == 0,
    "(i) J.grad phi identical via lower-index and upper-index routes through O(eps^2)")

# (ii) claim 6: B-term quadratic piece
Ab = sp.Symbol('A_b', real=True); ub = sp.Symbol('u_b', real=True)
A0cp = sp.Symbol('A0cp', positive=True); A1c, A2c = sp.symbols('A1c A2c', real=True)
h00 = gup[0,0] + A0**2
Yex = (h00*sp.diff(phf, t)**2 + 2*A0*Az*sp.diff(phf, t)*sp.diff(phf, z)
       + (gup[3,3] + Az**2)*sp.diff(phf, z)**2)
Qex = A0*sp.diff(phf, t) + Az*sp.diff(phf, z)
dQ = sp.expand(eps*tay(Qex, 2)[1] + eps**2*tay(Qex, 2)[2])
Acal_ser = A0cp + A1c*dQ + A2c*dQ**2/2
Yser = sp.expand(eps**2*tay(Yex, 2)[2])
yarg = Yser/Acal_ser
LB = sqrtg*Ab*(yarg/(1+yarg)**2)*(ub + dQ)**2
LB2 = tay(LB, 2)[2]
tgt = a**3*Ab*ub**2*k**2*Sn**2*(X + Qb*al)**2/(a**2*A0cp)
chk(sp.simplify(LB2 - tgt) == 0, "(ii) claim6: B-term O(eps^2) = a^3 Ab ub^2 dY^(2)/Abar exactly")

# (iii) claim 15 in the FULL theory: is the bump gradient instability still there?
Lam = sp.Symbol('Lam', real=True)
K0, K1, K2 = sp.symbols('K0 K1 K2', real=True)
p0, s0, x0, a0v = sp.symbols('p0 s0 x0 a0v', real=True)
s1, x1, a1v, p1 = sp.symbols('s1 x1 a1v p1', real=True)
Hh = sp.Symbol('H', real=True); av = sp.Symbol('a_v', positive=True); Qbs = sp.Symbol('Qb', real=True)
FRIED = [(Lam, 3*Hh**2 - 8*sp.pi*G*(Qbs*K1 - K0))]
vels = [s1, x1, a1v]; flds = [s0, x0, a0v]
L2s = sp.sympify(open('L2s_checkpoint.txt').read())
dL2s = sp.sympify(open('DeltaL2s_checkpoint.txt').read())
for tag, L2 in [("TRUNCATED", L2s), ("FULL", sp.expand(L2s + dL2s))]:
    cP = sp.expand(sp.diff(L2, p0)); AP = sp.expand(sp.diff(cP, p0)/2)
    cP0 = sp.expand(cP.subs(p0, 0))
    Lf = sp.expand((4*AP*L2.subs(p0, 0) - cP0**2).subs(FRIED))
    acc = sp.symbols('s2 x2 a2v', real=True)
    def ddt(e):
        return (sum(sp.diff(e, f)*v for f, v in zip(flds, vels))
                + sum(sp.diff(e, v)*aa for v, aa in zip(vels, acc)))
    EL = [sp.expand(ddt(sp.diff(Lf, vels[i])) - sp.diff(Lf, flds[i])) for i in range(3)]
    w = sp.Symbol('omega'); hat = sp.symbols('hS hX hA', real=True)
    sub = (list(zip(acc, [-w**2*h for h in hat])) + list(zip(vels, [sp.I*w*h for h in hat]))
           + list(zip(flds, hat)))
    M = sp.Matrix(3, 3, lambda i, j: sp.diff(sp.expand(EL[i].subs(sub, simultaneous=True)), hat[j]))
    Dp = sp.Poly(sp.expand(M.det()), w)
    dd = {n: sp.expand(Dp.coeff_monomial(w**n)) for n in (0, 2, 4)}
    rho_cr = 3*0.05**2/(8*np.pi)
    subs_num = [(G, 1.0), (av, 1.0), (Hh, 0.05), (Qbs, 1.0), (K0, -rho_cr), (K1, 1e-6*rho_cr),
                (K2, 0.4), (Ab, 1e-4), (ub, 1e-3), (A0cp, 1.0)]
    fns = {n: sp.lambdify((KB, k), dd[n].subs(subs_num), 'numpy') for n in (0, 2, 4)}
    print("  --- %s, bump ON (Ab ub^2 = 1e-10), K_B = 0.5 ---" % tag)
    for kv in [1e3, 1e5]:
        kk = kv*0.05
        a_, b_, c_ = fns[4](0.5, kk), fns[2](0.5, kk), fns[0](0.5, kk)
        disc = b_*b_ - 4*a_*c_
        r1 = (-b_ + np.sqrt(complex(disc)))/(2*a_); r2 = (-b_ - np.sqrt(complex(disc)))/(2*a_)
        soft, hard = sorted([r1, r2], key=abs)
        print("    k/aH=%8g : w2_soft=%s  w2_hard=%s" % (kv, soft, hard))
print("DONE")
