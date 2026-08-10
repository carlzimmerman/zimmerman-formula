#!/usr/bin/env python3
"""
SVT SCALAR SECTOR ON FRW -- second-order perturbation theory for THE_COMPLETION v7 action.
(See header docstring of task; conventions:)

Action (units c=1, signature -+++):
  S = int d^4x sqrt(-g) { [R - 2 Lam - (KB/2) F^{mn}F_{mn} + lam (A^m A_m + 1)]/(16 pi G)
        + (Acal(Q)/(8 pi G)) F_Y(Y/Acal(Q))  +  K(Q)  +  Ab * B(Y/Acal(Q)) * (Q-Q0)^2 } + S_matter
  Q = A^m d_m phi ; Y = (g^{mn} + A^m A^n) d_m phi d_n phi ; B(y)=y/(1+y)^2
  F_Y'(y) = 1 - exp(-sqrt(y))  =>  F_Y(y) = y + 2(sqrt(y)+1)exp(-sqrt(y)) - 2   (F_Y(0)=0)
  K(Q) generic: K0 + K1 dQ + K2 dQ^2/2 at the background point (DBI values substitutable).
  Acal(Q) = kappa^2 G (-K(Q)) > 0 : generic A0c + A1c dQ + A2c dQ^2/2.

GAUGE: Newtonian (longitudinal). For k != 0 the scalar gauge transformation reaching E=B=0 is
unique => COMPLETE gauge fixing => imposing it in the action is legitimate (Motohashi-Suyama-
Takahashi 2016); the momentum constraint lost with delta g_{0i} must reappear as a kinetic
degeneracy of the reduced action -- verified explicitly below.

Perturbations, single Fourier direction z:
  Phi = eps P(t) cos kz, Psi = eps S(t) cos kz, chi = eps X(t) cos kz,
  A^i = d^i alpha/a^2, alpha = eps s(t) cos kz  =>  A^z = -eps k s sin(kz)/a^2,
  A^0 solved EXACTLY from the unit-norm constraint (so the lam-multiplier term is identically
  zero to all orders: the constraint eliminates delta A^0).
"""

import sympy as sp
from sympy import Rational as R
import time, sys, functools
print = functools.partial(print, flush=True)

t_start = time.time()
def banner(s):
    print("\n" + "="*100); print(s); print("="*100, flush=True)
def tick(lbl):
    print("    [t=%6.1fs] %s" % (time.time()-t_start, lbl), flush=True)
def check(cond, label):
    print(("  [PASS] " if cond else "  [FAIL] ") + label, flush=True)
    if not cond:
        print("  *** HARD FAIL ***"); sys.exit(1)

# ---------------------------------------------------------------- symbols
t, z, x, y_ = sp.symbols('t z x y', real=True)
eps = sp.Symbol('eps', positive=True)
k   = sp.Symbol('k', positive=True)
G   = sp.Symbol('G', positive=True)
Lam = sp.Symbol('Lam', real=True)
KB  = sp.Symbol('K_B', real=True)
Ab  = sp.Symbol('A_b', real=True)
ub  = sp.Symbol('u_b', real=True)
K0, K1, K2 = sp.symbols('K0 K1 K2', real=True)
A1c, A2c   = sp.symbols('A1c A2c', real=True)
A0cp       = sp.Symbol('A0cp', positive=True)   # Acal(Qb) > 0 always (v7: -K = M^4/sqrt(1+nu^2))

a    = sp.Function('a', positive=True)(t)
P    = sp.Function('P')(t)
S    = sp.Function('S')(t)
X    = sp.Function('X')(t)
al   = sp.Function('s')(t)
phib = sp.Function('phib')(t)
Qb   = sp.Derivative(phib, t)

C  = sp.cos(k*z)
Sn = sp.sin(k*z)

Phi = eps*P*C
Psi = eps*S*C
chi = eps*X*C
alpha = eps*al*C
Az  = sp.diff(alpha, z)/a**2

def taylor(e, n):
    """coefficients [c0, c1, ..., cn] of e in eps via derivatives (fast)."""
    out = []
    cur = e
    fact = 1
    for i in range(n+1):
        out.append(sp.expand(cur.subs(eps, 0)/fact))
        if i < n:
            cur = sp.diff(cur, eps)
            fact *= (i+1)
    return out

def zavg(e):
    """average over a z-period. Valid for expressions bilinear in cos(kz), sin(kz)."""
    e = sp.expand(e)
    e = e.subs([(C**2, sp.Rational(1,2)), (Sn**2, sp.Rational(1,2)), (C*Sn, 0)])
    e = sp.expand(e)
    assert not e.has(C) and not e.has(Sn), "zavg: leftover single trig factor (odd term?)"
    return e

# ---------------------------------------------------------------- metric
g4 = sp.diag(-(1+2*Phi), a**2*(1-2*Psi), a**2*(1-2*Psi), a**2*(1-2*Psi))
g4inv = sp.diag(-1/(1+2*Phi), 1/(a**2*(1-2*Psi)), 1/(a**2*(1-2*Psi)), 1/(a**2*(1-2*Psi)))
sqrtg = sp.sqrt(1+2*Phi) * a**3 * (1-2*Psi)**R(3,2)

banner("SECTION A -- A^0 from unit norm, to SECOND order (exact solve; lam-term identically zero)")
A0ex = sp.sqrt((1 + g4[3,3]*Az**2)/(1+2*Phi))
A0c0, A0c1, A0c2 = taylor(A0ex, 2)
print("  A^0 = 1 + eps*(%s) + eps^2*(%s)" % (A0c1, sp.simplify(A0c2)))
check(sp.simplify(A0c1 + P*C) == 0, "delta A^0(1) = -Phi (matches row 17: dA0 = -Phi A0 at O(1))")
check(sp.simplify(A0c2 - (R(3,2)*P**2*C**2 + k**2*al**2*Sn**2/(2*a**2))) == 0,
      "delta A^0(2) = (3/2)Phi^2 + (d alpha)^2/(2a^2)   [the O(2) piece]")
h00_exact = sp.simplify(g4inv[0,0] + A0ex**2)
print("  h^00 exact =", h00_exact)
check(sp.simplify(h00_exact.subs(al, 0)) == 0, "h^00 == 0 EXACTLY when alpha = 0 (banked statement)")
check(sp.simplify(taylor(h00_exact, 1)[1]) == 0, "h^00 has NO first-order piece even with alpha != 0")
print("  NOTE: with alpha != 0, h^00 = (d alpha)^2/a^2 + O(3): second order -- it is exactly the piece")
print("  that completes delta Y^(2)'s perfect square below (sharpens row 19's 'to all orders' wording).")

banner("SECTION B -- Q and Y to second order; PROOF delta Y^(1) = 0; delta Y^(2) exact")
phi_full = phib + chi
Qex = A0ex*sp.diff(phi_full, t) + Az*sp.diff(phi_full, z)
Q0c, q1, q2 = taylor(Qex, 2)
check(sp.simplify(Q0c - Qb) == 0, "Qbar = phibdot")
print("  delta Q^(1) =", sp.simplify(q1))
check(sp.simplify(q1 - (sp.Derivative(X, t) - P*Qb)*C) == 0,
      "delta Q^(1) = (Xdot - Qbar P) cos kz   [row 17's delta Q = chidot - Qbar Phi]")
print("  delta Q^(2) =", sp.simplify(q2))

Yex = (h00_exact*sp.diff(phi_full, t)**2
       + 2*(A0ex*Az)*sp.diff(phi_full, t)*sp.diff(phi_full, z)
       + (g4inv[3,3] + Az**2)*sp.diff(phi_full, z)**2)
y0, y1v, y2v = taylor(Yex, 2)
check(sp.simplify(y0) == 0,  "Ybar = 0 on FRW")
check(sp.simplify(y1v) == 0, "delta Y^(1) = 0 -- PROVED by explicit expansion")
Y2target = k**2*Sn**2*(X + Qb*al)**2/a**2
check(sp.simplify(y2v - Y2target) == 0,
      "delta Y^(2) = (k^2 sin^2 kz/a^2)(X + Qbar s)^2  ==  |d(chi + Qbar alpha)|^2 / a^2  (perfect square)")
print("  delta Y^(2) =", Y2target)

banner("SECTION C -- the v7 promotion: every generated coupling drops out of the FRW quadratic action")
yv   = sp.Symbol('y_v', positive=True)
Qsym = sp.Symbol('Q_s', real=True)
Ysym = sp.Symbol('Y_s', positive=True)
Fex  = yv + 2*(sp.sqrt(yv)+1)*sp.exp(-sp.sqrt(yv)) - 2
check(sp.simplify(sp.diff(Fex, yv) - (1 - sp.exp(-sp.sqrt(yv)))) == 0,
      "F_Y' = 1 - e^{-sqrt y}  integrates to  F_Y = y + 2(sqrt y + 1)e^{-sqrt y} - 2,  F_Y(0) = 0")
check(sp.limit(Fex/yv**R(3,2), yv, 0, '+') == R(2,3), "deep-MOND: F_Y -> (2/3) y^{3/2} (c = 1)")

Acal = sp.Function('Acal', positive=True)(Qsym)
LF = Acal/(8*sp.pi*G) * Fex.subs(yv, Ysym/Acal)
A0_, A1_, A2_ = sp.symbols('Abar Abar1 Abar2', positive=True)
def at_bg(e):
    return e.subs(sp.Derivative(Acal, Qsym, 2), A2_).subs(sp.Derivative(Acal, Qsym), A1_).subs(Acal, A0_)
cands = [
  ("dL/dY|bg      (x delta Y^(2))          ", at_bg(sp.diff(LF, Ysym))),
  ("F_Q^new  dL/dQ|bg  (x dQ^(2), x mix)   ", at_bg(sp.diff(LF, Qsym))),
  ("F_QQ^new d2L/dQ2|bg  (x (dQ^(1))^2)    ", at_bg(sp.diff(LF, Qsym, 2))),
  ("F_YQ  d2L/dYdQ|bg  (x dY^(1) dQ^(1)=0) ", at_bg(sp.diff(LF, Ysym, Qsym))),
]
for lab, e in cands:
    lim = sp.limit(sp.simplify(e), Ysym, 0, '+')
    check(lim == 0, "coefficient -> 0 at Ybar = 0:  " + lab)
V = sp.Symbol('V', positive=True)
LF_sub = LF.subs(Ysym, eps**2*V**2).subs(Acal, A0_)
check(sp.limit(LF_sub/eps**2, eps, 0, '+') == 0,
      "DIRECT DEGREE PROOF: whole F-term = O(eps^3): zero in the quadratic action")
print("  leading:  L_F = eps^3 *", sp.simplify(sp.limit(LF_sub/eps**3, eps, 0, '+')),
      "  (F_YY ~ y^{-1/2} diverges but multiplies (dY)^2 = O(eps^4))")
print("  CONCLUSION: the promotion Acal(Q) leaves the FRW scalar quadratic action of AeST UNCHANGED.")

banner("SECTION D -- assemble the FULL quadratic action: ADM gravity + aether F^2 + K(Q) + B-term")
N     = sp.sqrt(1+2*Phi)
h3    = sp.diag(a**2*(1-2*Psi), a**2*(1-2*Psi), a**2*(1-2*Psi))
h3inv = h3.inv()
sqrth = a**3*(1-2*Psi)**R(3,2)
Kij   = sp.Matrix(3,3, lambda i,j: sp.diff(h3[i,j], t)/(2*N))
Kmix  = h3inv*Kij
trK   = sp.trace(Kmix)
KKt   = sp.trace(Kmix*Kmix)

coords3 = [x, y_, z]
def ricci3(h, hinv, co):
    n = 3
    Gam = [[[sum(hinv[i,l]*(sp.diff(h[l,j],co[kk]) + sp.diff(h[l,kk],co[j]) - sp.diff(h[j,kk],co[l]))
                 for l in range(n))/2 for kk in range(n)] for j in range(n)] for i in range(n)]
    Rc = 0
    for j in range(n):
        for kk in range(n):
            e = 0
            for i in range(n):
                e += sp.diff(Gam[i][j][kk], co[i]) - sp.diff(Gam[i][j][i], co[kk])
                for p in range(n):
                    e += Gam[i][i][p]*Gam[p][j][kk] - Gam[i][kk][p]*Gam[p][j][i]
            Rc += hinv[j,kk]*e
    return Rc
R3 = ricci3(h3, h3inv, coords3)
tick("R3 done")
R3lin = sp.simplify(taylor(R3, 1)[1])
print("  R3^(1) =", R3lin)
Ladm = N*sqrth*(R3 + KKt - trK**2 - 2*Lam)/(16*sp.pi*G)

# 4d equivalence check (conventions PROVED): sqrt(-g)(R-2Lam) - Ladm = total derivative
def ricci_scalar_4(g, ginv, co):
    n = 4
    Gam = [[[sum(ginv[i,l]*(sp.diff(g[l,j],co[kk]) + sp.diff(g[l,kk],co[j]) - sp.diff(g[j,kk],co[l]))
                 for l in range(n))/2 for kk in range(n)] for j in range(n)] for i in range(n)]
    Rs = 0
    for j in range(n):
        for kk in range(n):
            e = 0
            for i in range(n):
                e += sp.diff(Gam[i][j][kk], co[i]) - sp.diff(Gam[i][j][i], co[kk])
                for p in range(n):
                    e += Gam[i][i][p]*Gam[p][j][kk] - Gam[i][kk][p]*Gam[p][j][i]
            Rs += ginv[j,kk]*e
    return Rs
co4 = [t, x, y_, z]
R4  = ricci_scalar_4(g4, g4inv, co4)
Leh = sqrtg*(R4 - 2*Lam)/(16*sp.pi*G)
tick("R4 done")
Del = Leh - Ladm
Del0 = sp.simplify(taylor(Del, 0)[0] - sp.diff(6*a**2*sp.Derivative(a, t), t)/(16*sp.pi*G))
check(Del0 == 0, "background: sqrt(-g)R - ADM = d/dt(6 a^2 adot)/(16 pi G) EXACTLY (sign conventions anchored)")
Del2 = zavg(taylor(Del, 2)[2])
ok_td = True
for f in [P, S]:
    ELd = (sp.diff(Del2, f)
           - sp.diff(sp.diff(Del2, sp.Derivative(f, t)), t)
           + sp.diff(sp.diff(Del2, sp.Derivative(f, (t, 2))), t, 2))
    ok_td = ok_td and (sp.simplify(ELd) == 0)
check(ok_td, "quadratic order: z-avg(EH - ADM) has vanishing EL derivatives == pure total derivative")
tick("ADM equivalence proven")

# aether F^2
A0dn = g4[0,0]*A0ex
Azdn = g4[3,3]*Az
Ftz  = sp.diff(Azdn, t) - sp.diff(A0dn, z)
F2   = 2*g4inv[0,0]*g4inv[3,3]*Ftz**2
Laeth = sqrtg*(-KB/2)*F2/(16*sp.pi*G)
Ftz1 = sp.simplify(taylor(Ftz, 1)[1])
check(sp.simplify(Ftz1 + k*Sn*(sp.Derivative(al, t) + P)) == 0,
      "F_tz^(1) = -k sin(kz)(sdot + P): the aether scalar's field strength is  d_z(alphadot + Phi)")

# K(Q) sector, generic K
dQ = sp.expand(eps*q1 + eps**2*q2)
LK = sqrtg*(K0 + K1*dQ + K2*dQ**2/2)

# bump B-term with generic Acal expansion
Acal_ser = A0cp + A1c*dQ + A2c*dQ**2/2
Yser = sp.expand(eps**2*y2v)     # exact through eps^2 (y0=y1=0 proven)
yarg = Yser/Acal_ser
Bfun = yarg/(1+yarg)**2
LB   = sqrtg*Ab*Bfun*(ub + dQ)**2
LB2  = taylor(LB, 2)[2]
check(sp.simplify(LB2 - a**3*Ab*ub**2*Y2target/A0cp) == 0,
      "B-term quadratic piece = a^3 Ab ubar^2 deltaY^(2)/Abar  (B'(0)=1; delta-Acal enters only at O(eps^3))")
tick("dark sector expanded")

Ltot = Ladm + Laeth + LK + LB
L2 = zavg(taylor(Ltot, 2)[2])
print("  quadratic z-averaged Lagrangian assembled:", len(sp.Add.make_args(L2)), "terms")
tick("L2 assembled")

# plain symbols
p0, s0, x0, a0v = sp.symbols('p0 s0 x0 a0v', real=True)
s1, x1, a1v, p1 = sp.symbols('s1 x1 a1v p1', real=True)
Hh  = sp.Symbol('H', real=True)
av  = sp.Symbol('a_v', positive=True)
Qbs = sp.Symbol('Qb', real=True)
rep = [
    (sp.Derivative(P, t), p1), (sp.Derivative(S, t), s1), (sp.Derivative(X, t), x1), (sp.Derivative(al, t), a1v),
    (sp.Derivative(a, t), Hh*a), (sp.Derivative(phib, t), Qbs),
    (P, p0), (S, s0), (X, x0), (al, a0v),
]
L2s = sp.expand(L2.subs(rep, simultaneous=True).subs(a, av))
open('L2s_checkpoint.txt','w').write(sp.srepr(L2s))
tick("L2s checkpointed")
check(sp.diff(L2s, p1) == 0, "Pdot ABSENT: the lapse Phi is a Lagrange multiplier (Hamiltonian constraint)")
print("\n  L2 =", sp.collect(L2s, [p0, s0, x0, a0v, s1, x1, a1v]))

print("\n  Sections E (constraint elimination, kinetic matrix, no-ghost) and F (dispersion) run from the")
print("  checkpoint in svt_scalar_reduce.py and svt_scalar_physical.py -- see svt_scalar_all.py runner.")
print("\nSECTIONS A-D COMPLETE (%.1f s)" % (time.time()-t_start))
