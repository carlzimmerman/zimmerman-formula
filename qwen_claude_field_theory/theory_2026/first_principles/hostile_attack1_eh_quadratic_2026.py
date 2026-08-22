#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
hostile_attack1_eh_quadratic_2026.py -- HOSTILE REFEREE, ATTACK 1
==================================================================
Independent re-derivation (no code shared with s2/s4/s7) of:

  (A) linearised spatial Ricci of h_ij = (1 - 2 Psi) delta_ij
      [claim: R3_ij = d_i d_j Psi + delta_ij lap Psi, R3 = 4 lap Psi,
       Rbar_ij = S_ij[Psi]]  (c = 1 units);
  (B) quadratic static reduction of N sqrt(h) (3)R
      [claim: == 2 (grad Psi)^2 - 4 grad Phi . grad Psi mod total derivatives,
       i.e. alpha = 2, beta = -4], for BOTH lapse conventions
       N = 1 + Phi and N = sqrt(1 + 2 Phi);
  (C) the full two-potential Euler-Lagrange system with the FROZEN F and A:
        (I)  lap Psi + div[(F_X - eta/2 + eps A'(X) Y) grad Phi] = 4 pi G rho
        (II) lap(Psi - Phi) = -(eps/a0^2) d_i d_j [A(X) S_ij[Psi]]
      verified against my own EL operator; radical-heavy identities checked
      on random polynomial probes at 40-digit precision (tol 1e-25).

Total-derivative ambiguity handled by comparing EULER-LAGRANGE operators only.
"""
import sympy as sp
import random, sys

t, x, y, z = sp.symbols('t x y z', real=True)
V = (x, y, z)
e = sp.symbols('e', positive=True)
eta, epsY, a0, G, rho = sp.symbols('eta epsilon a_0 G rho', real=True)
Phi = sp.Function('Phi')(x, y, z)
Psi = sp.Function('Psi')(x, y, z)

def grad(f): return [sp.diff(f, v) for v in V]
def lap(f):  return sum(sp.diff(f, v, 2) for v in V)
def dot(u, w): return sum(a*b for a, b in zip(u, w))

npass = nfail = 0
def check(name, cond):
    global npass, nfail
    if cond: npass += 1
    else: nfail += 1
    print(('PASS' if cond else 'FAIL'), '--', name); sys.stdout.flush()

def christoffel(g, coords):
    n = len(coords); gi = g.inv()
    Gam = [[[0]*n for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for c_ in range(b, n):
                s = sum(gi[a, m]*(sp.diff(g[m, b], coords[c_])
                                  + sp.diff(g[m, c_], coords[b])
                                  - sp.diff(g[b, c_], coords[m])) for m in range(n))/2
                Gam[a][b][c_] = Gam[a][c_][b] = sp.together(s)
    return Gam

def ricci_tensor(g, coords):
    n = len(coords); Gam = christoffel(g, coords)
    R = sp.zeros(n, n)
    for b in range(n):
        for d in range(b, n):
            expr = 0
            for a in range(n):
                expr += sp.diff(Gam[a][b][d], coords[a]) - sp.diff(Gam[a][a][b], coords[d])
                for l in range(n):
                    expr += Gam[a][a][l]*Gam[l][b][d] - Gam[a][d][l]*Gam[l][a][b]
            R[b, d] = R[d, b] = sp.together(expr)
    return R

# ---- [0] sign convention: unit 3-sphere R = +6
th, ph, ps_ = sp.symbols('theta phi_c psi_c', real=True)
gS = sp.diag(1, sp.sin(ps_)**2, sp.sin(ps_)**2*sp.sin(th)**2)
RS = ricci_tensor(gS, (ps_, th, ph)); gSi = gS.inv()
Rscal_S = sp.simplify(sum(gSi[i, i]*RS[i, i] for i in range(3)))
check('[0] sign convention: unit 3-sphere R = +6', sp.simplify(Rscal_S - 6) == 0)

# ---- (A) conformal 3-metric, exact then linearised
h3 = sp.diag(1-2*e*Psi, 1-2*e*Psi, 1-2*e*Psi)
R3 = ricci_tensor(h3, V); h3i = h3.inv()
R3scal = sp.cancel(sp.together(sum(h3i[i, i]*R3[i, i] for i in range(3))))

def lin_coeff(expr):
    return sp.expand(sp.series(sp.together(expr), e, 0, 2).removeO()).coeff(e, 1)

R3_lin = sp.Matrix(3, 3, lambda i, j: lin_coeff(R3[i, j]))
target = sp.Matrix(3, 3, lambda i, j: sp.diff(Psi, V[i], V[j]) + (lap(Psi) if i == j else 0))
check('[A1] linear (3)R_ij = d_i d_j Psi + delta_ij lap Psi',
      all(sp.simplify(R3_lin[i, j]-target[i, j]) == 0 for i in range(3) for j in range(3)))

R3scal_lin = lin_coeff(R3scal)
check('[A2] linear (3)R = 4 lap Psi', sp.simplify(R3scal_lin - 4*lap(Psi)) == 0)

def S_ij(f):
    return sp.Matrix(3, 3, lambda i, j: sp.diff(f, V[i], V[j]) - (lap(f)/3 if i == j else 0))

Rbar_lin = sp.Matrix(3, 3, lambda i, j:
                     R3_lin[i, j] - sp.Rational(1, 3)*sp.eye(3)[i, j]*R3scal_lin)
check('[A3] linear Rbar_ij = S_ij[Psi]  (Y is built from the SPATIAL potential)',
      all(sp.simplify(Rbar_lin[i, j]-S_ij(Psi)[i, j]) == 0 for i in range(3) for j in range(3)))
print('  ... geometry block done')

# ---- (B) quadratic reduction, both lapse conventions
def quadratic_density(Nexpr):
    dens = Nexpr*sp.sqrt(h3.det())*R3scal
    ser = sp.series(sp.together(dens), e, 0, 3).removeO()
    return sp.expand(ser).coeff(e, 2)

def EL(L, f):
    res = sp.diff(L, f)
    for D in L.atoms(sp.Derivative):
        if D.expr == f:
            vs = []
            for v, n in D.variable_count:
                vs += [v]*int(n)
            res = res + sp.Integer(-1)**len(vs)*sp.diff(sp.diff(L, D), *vs)
    return res

L2_claim = 2*dot(grad(Psi), grad(Psi)) - 4*dot(grad(Phi), grad(Psi))

for name, Nexpr in [('N = 1 + e Phi', 1 + e*Phi),
                    ('N = sqrt(1+2 e Phi)', sp.sqrt(1 + 2*e*Phi))]:
    L2 = quadratic_density(Nexpr)
    dP = sp.simplify(sp.expand(EL(L2, Phi) - EL(L2_claim, Phi)))
    dS = sp.simplify(sp.expand(EL(L2, Psi) - EL(L2_claim, Psi)))
    check('[B] %s: quad(N sqrt(h) R3) == 2(gPsi)^2 - 4 gPhi.gPsi mod tot.derivs' % name,
          dP == 0 and dS == 0)
print('  ... EH quadratic block done')

# uniqueness of (alpha, beta)
al, be = sp.symbols('alpha beta')
L2_gen = al*dot(grad(Psi), grad(Psi)) + be*dot(grad(Phi), grad(Psi))
L2a = quadratic_density(1 + e*Phi)
dP = sp.expand(EL(L2a, Phi) - EL(L2_gen, Phi))
dS = sp.expand(EL(L2a, Psi) - EL(L2_gen, Psi))
sol = sp.solve([dP.coeff(sp.Derivative(Psi, (x, 2))),
                dS.coeff(sp.Derivative(Psi, (x, 2))),
                dS.coeff(sp.Derivative(Phi, (x, 2)))], [al, be], dict=True)
ok = (len(sol) == 1 and sol[0][al] == 2 and sol[0][be] == -4
      and sp.simplify(dP.subs(sol[0])) == 0 and sp.simplify(dS.subs(sol[0])) == 0)
check('[B2] (alpha, beta) = (2, -4) unique (mod null Lagrangians)', ok)

# ---- (C) full static EL system, frozen F and A, numeric-probe verification
Xs = sp.symbols('Xs', positive=True)
check('[C0] F_X = -1/(1+sqrt X)',
      sp.simplify(sp.diff(-2*sp.sqrt(Xs)+2*sp.log(1+sp.sqrt(Xs)), Xs) + 1/(1+sp.sqrt(Xs))) == 0)
check("[C0b] A'(X) = 2X(1-X)/(1+X)^5",
      sp.simplify(sp.diff(Xs**2/(1+Xs)**4, Xs) - 2*Xs*(1-Xs)/(1+Xs)**5) == 0)

X = dot(grad(Phi), grad(Phi))/a0**2
Ymat = S_ij(Psi)
Y = sum(Ymat[i, j]**2 for i in range(3) for j in range(3))/a0**4
Ffro = -2*sp.sqrt(X) + 2*sp.log(1 + sp.sqrt(X))
Afun = lambda XX: XX**2/(1 + XX)**4
Apr  = lambda XX: 2*XX*(1-XX)/(1+XX)**5
FXfun = lambda XX: -1/(1 + sp.sqrt(XX))

Lfull = (L2_claim + eta*dot(grad(Phi), grad(Phi))
         - 2*a0**2*(Ffro + epsY*Afun(X)*Y) - 16*sp.pi*G*rho*Phi)

divterm = sum(sp.diff((FXfun(X) - eta/2 + epsY*Apr(X)*Y)*sp.diff(Phi, v), v) for v in V)
CI = lap(Psi) + divterm - 4*sp.pi*G*rho
ddterm = sum(sp.diff(Afun(X)*Ymat[i, j], V[i], V[j]) for i in range(3) for j in range(3))
CII = lap(Phi) - lap(Psi) - (epsY/a0**2)*ddterm

resI  = EL(Lfull, Phi) - 4*CI
resII = EL(Lfull, Psi) - 4*CII
print('  ... EL system built')

def probe_zero(expr, tag, ntrial=2):
    random.seed(20260822 + abs(hash(tag)) % 10000)
    for trial in range(ntrial):
        def rpoly():
            terms = []
            for _ in range(8):
                i, j, k = random.randint(0, 2), random.randint(0, 2), random.randint(0, 2)
                terms.append(sp.Rational(random.randint(-9, 9), random.randint(1, 5))
                             * x**i * y**j * z**k)
            return sp.Add(*terms)
        pm = {a0: sp.Rational(random.randint(1, 4), random.randint(1, 3)),
              eta: sp.Rational(random.randint(-3, 3), 2),
              epsY: sp.Rational(random.randint(-3, 3), 2),
              G: sp.Rational(1, 2), rho: sp.Integer(0)}
        eD = expr.subs(pm)
        eD = eD.subs({Phi: rpoly(), Psi: rpoly()}, simultaneous=True).doit()
        pt = {x: sp.Rational(random.randint(2, 7), 5),
              y: sp.Rational(random.randint(2, 7), 6),
              z: sp.Rational(random.randint(2, 7), 7)}
        val = eD.subs(pt).evalf(40)
        if not (abs(sp.im(val)) < sp.Float(10)**(-25) and abs(sp.re(val)) < sp.Float(10)**(-25)):
            print('   probe fail', trial, tag, '->', val)
            return False
    return True

check('[C1] EL_Phi(L) == 4 x eq (I)  [kernel F_X - eta/2 + eps A\'(X) Y; matter '
      'sources ONLY the lapse eq]', probe_zero(resI, 'I'))
print('  ... C1 done')
check('[C2] EL_Psi(L) == 4 x eq (II) [tidal operator acts on S_ij[PSI]; slip eq]',
      probe_zero(resII, 'II'))
print('  ... C2 done')

# ---- deep-MOND kernel limit
xk = sp.symbols('x_k', positive=True)
kernel = 1 - 1/(1 + xk) - eta/2
ser = sp.series(kernel, xk, 0, 3).removeO()
check('[C3] small-x kernel = -eta/2 + x - x^2: any eta != 0 kills deep MOND',
      sp.expand(ser - (-eta/2 + xk - xk**2)) == 0)

# ---- O(eps) elimination -> single-potential schematic (structural identity)
# (I) with lap Psi eliminated via exact (II):
#   lap Phi - (eps/a0^2) dd[A S[Psi]] + div[(F_X - eta/2 + eps A'(X) Y(Psi)) grad Phi]
# every eps-multiplied factor evaluated at Psi = Phi + O(eps) => replace Psi -> Phi
# there with O(eps^2) error; result:
#   div[(1 - eta/2 + F_X + eps A' Y(Phi)) grad Phi] - (eps/a0^2) dd[A S[Phi]]
# The residual is exactly eps * [terms each containing (S[Psi]-S[Phi]) or
# (Y(Psi)-Y(Phi))], each O(eps) on-shell. Verify the residual FORM:
YPhi = sum(S_ij(Phi)[i, j]**2 for i in range(3) for j in range(3))/a0**4
ddPhi = sum(sp.diff(Afun(X)*S_ij(Phi)[i, j], V[i], V[j]) for i in range(3) for j in range(3))
lhs_elim = (lap(Phi) - (epsY/a0**2)*ddterm
            + sum(sp.diff((FXfun(X) - eta/2 + epsY*Apr(X)*Y)*sp.diff(Phi, v), v) for v in V))
schematic = (sum(sp.diff((1 - eta/2 + FXfun(X) + epsY*Apr(X)*YPhi)*sp.diff(Phi, v), v)
                 for v in V) - (epsY/a0**2)*ddPhi)
residual = sp.expand(lhs_elim - schematic)
# residual must (i) carry an overall factor epsY, (ii) vanish identically at Psi=Phi
res_at_eq = residual.subs(Psi, Phi).doit()
check('[C4a] elimination residual vanishes identically at Psi == Phi',
      probe_zero(res_at_eq, 'C4a'))
check('[C4b] elimination residual is O(eps) (vanishes at eps = 0)',
      sp.expand(residual.subs(epsY, 0)) == 0)
print('  ... C4 done')

# ---- derivative orders of eq (II)
ordPsi = max(sum(int(n) for _, n in D.variable_count)
             for D in CII.atoms(sp.Derivative) if D.expr == Psi)
ordPhi = max(sum(int(n) for _, n in D.variable_count)
             for D in CII.atoms(sp.Derivative) if D.expr == Phi)
check('[C5] eq (II): 4th order in Psi, 3rd order in Phi', ordPsi == 4 and ordPhi == 3)

# ---- d_i d_j S_ij = (2/3) lap^2
f = sp.Function('f')(x, y, z)
dd = sum(sp.diff(S_ij(f)[i, j], V[i], V[j]) for i in range(3) for j in range(3))
check('[C6] d_i d_j S_ij[f] = (2/3) lap^2 f',
      sp.simplify(dd - sp.Rational(2, 3)*lap(lap(f))) == 0)

print()
print('TOTAL: %d PASS, %d FAIL' % (npass, nfail))
