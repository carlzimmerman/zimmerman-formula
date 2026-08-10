#!/usr/bin/env python3
"""
ADVERSARIAL VERIFIER (independent code, written from scratch).

Part 1: independent re-derivation of Sections A-B (A^0, h^00, dQ, dY) and Section C
        (promotion dropout) -- claims 1-5.
Part 2: THE OMITTED AeST TERMS. The action THE_COMPLETION says it is (SZ2021 Eq. 5, as
        transcribed in real_research/bridge1_aest_equations.md) contains
            + 2(2-K_B) J^mu grad_mu phi      J^mu = A^al nabla_al A^mu
            -   (2-K_B) Y
        inside the 1/(16 pi G) bracket. svt_scalar_master.py's action has NEITHER.
        Compute their exact O(eps^2) scalar-sector contribution DeltaL2.
Part 3: reduction redone with my own code on (a) their L2s (checkpoint, verified by
        re-run) and (b) L2s + DeltaL2s. Compare: det factorization, kinetic matrix,
        c_s^2, k^4 coefficient, K_B window.
"""
import sympy as sp
from sympy import Rational as R
import functools, sys, time
print = functools.partial(print, flush=True)
T0 = time.time()
def chk(c, lbl):
    print(("  [OK ] " if c else "  [BAD] ") + lbl)
    return bool(c)

t, z = sp.symbols('t z', real=True)
eps = sp.Symbol('eps', positive=True)
k   = sp.Symbol('k', positive=True)
G   = sp.Symbol('G', positive=True)
Lam = sp.Symbol('Lam', real=True)
KB  = sp.Symbol('K_B', real=True)
Ab  = sp.Symbol('A_b', real=True)
ub  = sp.Symbol('u_b', real=True)
K0, K1, K2 = sp.symbols('K0 K1 K2', real=True)
A0cp = sp.Symbol('A0cp', positive=True)

a    = sp.Function('a', positive=True)(t)
P    = sp.Function('P')(t)     # Phi amp
S    = sp.Function('S')(t)     # Psi amp
X    = sp.Function('X')(t)     # chi amp
al   = sp.Function('s')(t)     # alpha amp
phib = sp.Function('phib')(t)
Qb   = sp.Derivative(phib, t)

C, Sn = sp.cos(k*z), sp.sin(k*z)
Phi, Psi, chi, alpha = eps*P*C, eps*S*C, eps*X*C, eps*al*C

def tay(e, n):
    out, cur, fact = [], e, 1
    for i in range(n+1):
        out.append(sp.expand(cur.subs(eps, 0)/fact))
        if i < n:
            cur = sp.diff(cur, eps); fact *= (i+1)
    return out

def zavg(e):
    e = sp.expand(e).subs([(C**2, R(1,2)), (Sn**2, R(1,2)), (C*Sn, 0)])
    e = sp.expand(e)
    assert not e.has(C) and not e.has(Sn), "leftover trig"
    return e

# metric (Newtonian gauge, -+++)
gdn = sp.diag(-(1+2*Phi), a**2*(1-2*Psi), a**2*(1-2*Psi), a**2*(1-2*Psi))
gup = sp.diag(-1/(1+2*Phi), 1/(a**2*(1-2*Psi)), 1/(a**2*(1-2*Psi)), 1/(a**2*(1-2*Psi)))
sqrtg = sp.sqrt(1+2*Phi)*a**3*(1-2*Psi)**R(3,2)

Az  = sp.diff(alpha, z)/a**2                       # A^z (pure O(eps))
A0  = sp.sqrt((1 + gdn[3,3]*Az**2)/(1+2*Phi))      # exact unit-norm solve

print("="*100); print("PART 1 -- independent claims 1-5"); print("="*100)
ok = True
A0c = tay(A0, 2)
ok &= chk(sp.simplify(A0c[1] + P*C) == 0, "claim1: dA^0(1) = -Phi")
ok &= chk(sp.simplify(A0c[2] - (R(3,2)*P**2*C**2 + k**2*al**2*Sn**2/(2*a**2))) == 0,
          "claim1: dA^0(2) = (3/2)Phi^2 + (d alpha)^2/(2a^2)")
h00 = sp.simplify(gup[0,0] + A0**2)
ok &= chk(sp.simplify(h00.subs(al, 0)) == 0, "claim2: h^00 == 0 exactly at alpha=0")
ok &= chk(sp.simplify(tay(h00, 1)[1]) == 0, "claim2: no O(eps) piece of h^00")
ok &= chk(sp.simplify(tay(h00, 2)[2] - k**2*al**2*Sn**2/a**2) == 0,
          "claim2: h^00(2) = (d alpha)^2/a^2")

phf = phib + chi
Qex = A0*sp.diff(phf, t) + Az*sp.diff(phf, z)
qc = tay(Qex, 2)
ok &= chk(sp.simplify(qc[0] - Qb) == 0, "claim4: Qbar = phibdot")
ok &= chk(sp.simplify(qc[1] - (sp.Derivative(X, t) - P*Qb)*C) == 0,
          "claim4: dQ(1) = (chidot - Qb Phi)")
Yex = (h00*sp.diff(phf, t)**2 + 2*A0*Az*sp.diff(phf, t)*sp.diff(phf, z)
       + (gup[3,3] + Az**2)*sp.diff(phf, z)**2)
yc = tay(Yex, 2)
ok &= chk(sp.simplify(yc[0]) == 0 and sp.simplify(yc[1]) == 0, "claim3: Ybar = dY(1) = 0")
ok &= chk(sp.simplify(yc[2] - k**2*Sn**2*(X + Qb*al)**2/a**2) == 0,
          "claim3: dY(2) = k^2 sin^2(kz)(chi + Qb alpha)^2/a^2 (perfect square)")

# claim 5: promotion dropout. F_Y(y) with F_Y' = 1 - e^{-sqrt y}; exact composite.
yv = sp.Symbol('y_v', positive=True)
Fex = yv + 2*(sp.sqrt(yv)+1)*sp.exp(-sp.sqrt(yv)) - 2
ok &= chk(sp.simplify(sp.diff(Fex, yv) - (1 - sp.exp(-sp.sqrt(yv)))) == 0, "claim5: F_Y antiderivative")
Qs = sp.Symbol('Q_s', real=True); Ys = sp.Symbol('Y_s', positive=True)
Acal = sp.Function('Acal', positive=True)(Qs)
LF = Acal/(8*sp.pi*G)*Fex.subs(yv, Ys/Acal)
for lbl, d in [("dY coeff", sp.diff(LF, Ys)), ("dQ coeff", sp.diff(LF, Qs)),
               ("dQ^2 coeff", sp.diff(LF, Qs, 2)), ("dYdQ coeff", sp.diff(LF, Ys, Qs))]:
    ok &= chk(sp.limit(sp.simplify(d), Ys, 0, '+') == 0, "claim5: %s -> 0 at Ybar=0" % lbl)
V = sp.Symbol('V', positive=True)
ok &= chk(sp.limit(LF.subs(Ys, eps**2*V**2).subs(Acal, A0cp)/eps**2, eps, 0, '+') == 0,
          "claim5: entire F-term O(eps^3)")

print("\n" + "="*100)
print("PART 2 -- the OMITTED AeST terms: 2(2-K_B) J.grad(phi) - (2-K_B) Y, inside 1/(16 pi G)")
print("="*100)
co = [t, sp.Symbol('x1'), sp.Symbol('x2'), z]
# needed Christoffels: upper in {0,3}, lower pairs in {0,3} (diagonal metric)
def Gamma(mu, nu, la):
    return sp.expand(gup[mu,mu]*(sp.diff(gdn[mu,la], co[nu]) + sp.diff(gdn[mu,nu], co[la])
                                 - sp.diff(gdn[nu,la], co[mu]))/2)
Aup = {0: A0, 3: Az}
Jup = {}
for mu in (0, 3):
    s_ = 0
    for nu in (0, 3):
        s_ += Aup[nu]*sp.diff(Aup[mu], co[nu])
        for la in (0, 3):
            s_ += Aup[nu]*Gamma(mu, nu, la)*Aup[la]
    Jup[mu] = s_
Jphi = Jup[0]*sp.diff(phf, t) + Jup[3]*sp.diff(phf, z)
dL_om = sqrtg*(2*(2-KB)*Jphi - (2-KB)*Yex)/(16*sp.pi*G)
c0, c1, c2 = tay(dL_om, 2)
chk(sp.simplify(c0) == 0, "omitted terms: BACKGROUND contribution = 0 (Friedmann unchanged)")
c1s = sp.simplify(c1)
print("  O(eps^1) =", c1s)
# if O(eps^1) is a pure z-derivative / vanishes on z-average it does not disturb the background EOM
chk(sp.simplify(sp.integrate(c1, (z, 0, 2*sp.pi/k))) == 0,
    "omitted terms: O(eps^1) z-integrates to 0 (no background EOM shift)")
dL2 = zavg(c2)
print("\n  z-averaged O(eps^2) contribution of the omitted terms:")
dL2 = sp.expand(dL2)
print("  DeltaL2 =", sp.simplify(dL2))
nonzero = sp.simplify(dL2) != 0
chk(not nonzero, "DeltaL2 == 0 (if [BAD]: the master action is missing O(eps^2) scalar terms)")

# convert to the checkpoint's plain symbols (identical substitution as master)
p0, s0, x0, a0v = sp.symbols('p0 s0 x0 a0v', real=True)
s1, x1, a1v, p1 = sp.symbols('s1 x1 a1v p1', real=True)
Hh = sp.Symbol('H', real=True); av = sp.Symbol('a_v', positive=True); Qbs = sp.Symbol('Qb', real=True)
rep = [(sp.Derivative(P, t), p1), (sp.Derivative(S, t), s1), (sp.Derivative(X, t), x1),
       (sp.Derivative(al, t), a1v), (sp.Derivative(a, t), Hh*a), (sp.Derivative(phib, t, 2), sp.Symbol('Qbdot', real=True)),
       (sp.Derivative(phib, t), Qbs), (P, p0), (S, s0), (X, x0), (al, a0v)]
dL2s = sp.expand(dL2.subs(rep, simultaneous=True).subs(a, av))
print("\n  DeltaL2 (plain symbols) =", sp.collect(dL2s, [p0, s0, x0, a0v, s1, x1, a1v, p1]))
open('DeltaL2s_checkpoint.txt', 'w').write(sp.srepr(dL2s))
print("  [t=%.1fs] Part 2 done" % (time.time()-T0))
