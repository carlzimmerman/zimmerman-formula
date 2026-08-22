#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
hostile_attack2_weyl_slip_2026.py -- HOSTILE REFEREE, ATTACK 2
===============================================================
Independent 4D re-derivation (own Riemann/Weyl code, c = 1) of the
[ricci-vs-weyl] and [var-adm] structural claims:

  ds^2 = -(1 + 2 e Phi) dt^2 + (1 - 2 e Psi) delta_ij dx^i dx^j, khronon T = t.

  [W1] exact a_mu = u^nu nabla_nu u_mu has a_0 = 0, a_i = d_i ln N (EXACT);
  [W2] exact X = h^{ij} a_i a_j = |grad Phi|^2 / ((1+2 Phi)^2 (1-2 Psi))
       -- X is LAPSE-built; ALSO adjudicate the s2 convention discrepancy:
       s2 quotes (1+Phi)^2 in the denominator because s2 uses N = 1 + Phi
       (i.e. g_00 = -(1+Phi)^2); under the g_00 = -(1+2 Phi) convention of
       sec3 the exact denominator is (1+2 Phi)^2.  Same linear order; the
       two "exact" formulas differ at O(Phi^2) -- flag as a convention
       inconsistency between committed scripts, not an error at claimed order;
  [W3] linear electric Weyl E_ij = C_{i0j0} (u^0)^2 = (1/2) S_ij[Phi + Psi];
  [W4] linear Rbar_ij = S_ij[Psi]  (4D-independent recomputation);
  [W5] difference law Rbar_ij - E_ij = (1/2) S_ij[Psi - Phi];
  [W6] at Phi = Psi: Rbar_ij = E_ij with constant exactly 1;
  [W7] the action's invariant Y matches the Weyl invariant ONLY at zero slip:
       Y - (E:E)*(1/a0^4-normalisation) has leading term proportional to
       S[Psi]:S[Psi] - (1/4)S[Phi+Psi]:S[Phi+Psi]  which is NOT identically
       zero for Phi != Psi (exhibited on an explicit witness).
"""
import sympy as sp
import sys

t, x, y, z = sp.symbols('t x y z', real=True)
C4 = (t, x, y, z)
V = (x, y, z)
e = sp.symbols('e', positive=True)
Phi = sp.Function('Phi')(x, y, z)
Psi = sp.Function('Psi')(x, y, z)

npass = nfail = 0
def check(name, cond):
    global npass, nfail
    if cond: npass += 1
    else: nfail += 1
    print(('PASS' if cond else 'FAIL'), '--', name); sys.stdout.flush()

def lap(f): return sum(sp.diff(f, v, 2) for v in V)
def S_ij(f):
    return sp.Matrix(3, 3, lambda i, j: sp.diff(f, V[i], V[j]) - (lap(f)/3 if i == j else 0))

# ---------------- exact 4-metric (sec3 convention g_00 = -(1+2 e Phi))
g = sp.diag(-(1 + 2*e*Phi), 1 - 2*e*Psi, 1 - 2*e*Psi, 1 - 2*e*Psi)
gi = g.inv()
n4 = 4

def christoffel4(g, gi):
    Gam = [[[0]*n4 for _ in range(n4)] for _ in range(n4)]
    for a in range(n4):
        for b in range(n4):
            for c_ in range(b, n4):
                s = sum(gi[a, m]*(sp.diff(g[m, b], C4[c_]) + sp.diff(g[m, c_], C4[b])
                                  - sp.diff(g[b, c_], C4[m])) for m in range(n4))/2
                Gam[a][b][c_] = Gam[a][c_][b] = sp.together(s)
    return Gam

Gam = christoffel4(g, gi)

# ---------------- [W1] exact acceleration of the khronon congruence
N = sp.sqrt(1 + 2*e*Phi)
u_lo = [-N, 0, 0, 0]                       # u_mu = -d_mu T/|dT|, T=t
u_up = [sp.together(sum(gi[a, b]*u_lo[b] for b in range(n4))) for a in range(n4)]
a_lo = []
for mu in range(n4):
    expr = sum(u_up[nu]*(sp.diff(u_lo[mu], C4[nu])
               - sum(Gam[l][nu][mu]*u_lo[l] for l in range(n4))) for nu in range(n4))
    a_lo.append(sp.simplify(expr))
lnN = sp.log(N)
okW1 = sp.simplify(a_lo[0]) == 0 and all(
    sp.simplify(a_lo[i+1] - sp.diff(lnN, V[i])) == 0 for i in range(3))
check('[W1] exact: a_0 = 0, a_i = d_i ln N', okW1)

# ---------------- [W2] exact X (a0 = 1 units): h^{ij} a_i a_j
Xexact = sp.simplify(sum(a_lo[i+1]**2 for i in range(3))/(1 - 2*e*Psi))
gp2 = sum(sp.diff(Phi, v)**2 for v in V)
Xclaim_thisconv = e**2*gp2/((1 + 2*e*Phi)**2*(1 - 2*e*Psi))
Xclaim_s2 = e**2*gp2/((1 + e*Phi)**2*(1 - 2*e*Psi))
check('[W2a] exact X = |grad Phi|^2/((1+2Phi)^2 (1-2Psi)) under g00 = -(1+2Phi)',
      sp.simplify(Xexact - Xclaim_thisconv) == 0)
check('[W2b] s2 formula (1+Phi)^2 denominator is NOT exact in this convention '
      '(differs at O(Phi^2)) -- convention mismatch flagged',
      sp.simplify(Xexact - Xclaim_s2) != 0)
# leading order agreement:
diff_lead = sp.expand(sp.series(Xexact - Xclaim_s2, e, 0, 4).removeO())
check('[W2c] the two conventions agree through O(e^2) x O(e^0) relative '
      '(difference starts at e^3)', diff_lead.coeff(e, 2) == 0 and diff_lead.coeff(e, 3) != 0)

# ---------------- Riemann, Ricci, Weyl at linear order
def riemann_lo(g, gi, Gam):
    """R^a_{bcd} then lower: R_{abcd}"""
    Rup = [[[[0]*n4 for _ in range(n4)] for _ in range(n4)] for _ in range(n4)]
    for a in range(n4):
        for b in range(n4):
            for c_ in range(n4):
                for d in range(n4):
                    expr = (sp.diff(Gam[a][b][d], C4[c_]) - sp.diff(Gam[a][b][c_], C4[d])
                            + sum(Gam[a][c_][l]*Gam[l][b][d]
                                  - Gam[a][d][l]*Gam[l][b][c_] for l in range(n4)))
                    Rup[a][b][c_][d] = expr
    Rlo = [[[[0]*n4 for _ in range(n4)] for _ in range(n4)] for _ in range(n4)]
    for a in range(n4):
        for b in range(n4):
            for c_ in range(n4):
                for d in range(n4):
                    Rlo[a][b][c_][d] = sp.together(
                        sum(g[a, m]*Rup[m][b][c_][d] for m in range(n4)))
    return Rlo

Rlo = riemann_lo(g, gi, Gam)
Ric = sp.Matrix(n4, n4, lambda b, d: sp.together(
    sum(gi[a, c_]*Rlo[a][b][c_][d] for a in range(n4) for c_ in range(n4))))
Rs = sp.together(sum(gi[b, d]*Ric[b, d] for b in range(n4) for d in range(n4)))

def lin(expr):
    return sp.expand(sp.series(sp.together(expr), e, 0, 2).removeO()).coeff(e, 1)

# Weyl (4D):
def weyl_lo(a, b, c_, d):
    return (Rlo[a][b][c_][d]
            - sp.Rational(1, 2)*(g[a, c_]*Ric[d, b] - g[a, d]*Ric[c_, b]
                                 - g[b, c_]*Ric[d, a] + g[b, d]*Ric[c_, a])
            + sp.Rational(1, 6)*Rs*(g[a, c_]*g[d, b] - g[a, d]*g[c_, b]))

# E_ij = C_{i mu j nu} u^mu u^nu = C_{i0j0} (u^0)^2 ; linear order
E = sp.zeros(3, 3)
u0sq = sp.together(u_up[0]**2)
for i in range(3):
    for j in range(i, 3):
        E[i, j] = E[j, i] = lin(weyl_lo(i+1, 0, j+1, 0)*u0sq)

SW = S_ij((Phi + Psi)/2)
check('[W3] linear E_ij = S_ij[(Phi+Psi)/2]  (WEYL potential Hessian)',
      all(sp.simplify(E[i, j] - SW[i, j]) == 0 for i in range(3) for j in range(3)))

# ---------------- [W4] Rbar from the induced 3-metric (independent of attack1)
h3 = sp.diag(1-2*e*Psi, 1-2*e*Psi, 1-2*e*Psi)
h3i = h3.inv()
def christoffel3(g3, g3i):
    Gam3 = [[[0]*3 for _ in range(3)] for _ in range(3)]
    for a in range(3):
        for b in range(3):
            for c_ in range(b, 3):
                s = sum(g3i[a, m]*(sp.diff(g3[m, b], V[c_]) + sp.diff(g3[m, c_], V[b])
                                   - sp.diff(g3[b, c_], V[m])) for m in range(3))/2
                Gam3[a][b][c_] = Gam3[a][c_][b] = sp.together(s)
    return Gam3
G3 = christoffel3(h3, h3i)
Ric3 = sp.zeros(3, 3)
for b in range(3):
    for d in range(b, 3):
        expr = 0
        for a in range(3):
            expr += sp.diff(G3[a][b][d], V[a]) - sp.diff(G3[a][a][b], V[d])
            for l in range(3):
                expr += G3[a][a][l]*G3[l][b][d] - G3[a][d][l]*G3[l][a][b]
        Ric3[b, d] = Ric3[d, b] = sp.together(expr)
R3s = sp.together(sum(h3i[i, i]*Ric3[i, i] for i in range(3)))
Rbar = sp.Matrix(3, 3, lambda i, j: lin(Ric3[i, j] - h3[i, j]*R3s/3))
SP = S_ij(Psi)
check('[W4] linear Rbar_ij = S_ij[Psi]', all(
    sp.simplify(Rbar[i, j] - SP[i, j]) == 0 for i in range(3) for j in range(3)))

# ---------------- [W5]-[W6] difference law and unit constant
D = S_ij((Psi - Phi)/2)
check('[W5] Rbar_ij - E_ij = (1/2) S_ij[Psi - Phi]', all(
    sp.simplify(Rbar[i, j] - E[i, j] - D[i, j]) == 0 for i in range(3) for j in range(3)))
sub_eq = {Psi: Phi}
check('[W6] at Phi = Psi: Rbar_ij = E_ij exactly (constant 1, not 2 or 1/2)', all(
    sp.simplify((Rbar[i, j] - E[i, j]).subs(Psi, Phi).doit()) == 0
    for i in range(3) for j in range(3)))

# ---------------- [W7] the action's invariant is S[Psi]:S[Psi], not the Weyl one
# witness with slip: Phi = x^2, Psi = 0  =>  S[Psi]:S[Psi] = 0 but E:E != 0
wit = {Phi: x**2, Psi: sp.Integer(0)}
Ew = sp.Matrix(3, 3, lambda i, j: E[i, j].subs(wit).doit())
Rw = sp.Matrix(3, 3, lambda i, j: Rbar[i, j].subs(wit).doit())
EE = sum(Ew[i, j]**2 for i in range(3) for j in range(3))
RR = sum(Rw[i, j]**2 for i in range(3) for j in range(3))
check('[W7] with slip (Phi = x^2, Psi = 0): Rbar:Rbar = 0 but E:E != 0 '
      '-- Y is the SPATIAL-curvature invariant, not the Weyl invariant',
      sp.simplify(RR) == 0 and sp.simplify(EE) != 0)

print()
print('TOTAL: %d PASS, %d FAIL' % (npass, nfail))
