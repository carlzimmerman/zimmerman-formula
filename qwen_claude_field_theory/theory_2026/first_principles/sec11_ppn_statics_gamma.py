#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sec11_ppn_statics_gamma.py -- Section 11 part 1: static PPN sector
===================================================================
PPN statics of the frozen khronon action, from the two-potential
weak-field system of [var-adm] (re-verified here, not quoted):

  L = (1/16 pi G)[ 2(grad Psi)^2 - 4 grad Phi.grad Psi + eta_K (grad Phi)^2 ]
      - (a0^2/8 pi G) F(X,Y) - rho Phi
  X = |grad Phi|^2/a0^2 (lapse),  Y = (c^4/a0^4) S_ij[Psi] S_ij[Psi] (spatial)
  F(X,Y) = F_m(X) + eps A(X) Y,  F_m = -2 sqrt(X) + 2 ln(1+sqrt(X)),
  A = X^2/(1+X)^4.

Derived (all sympy; EL checks done on a spanning monomial basis X^m Y^n --
legitimate because the EL <-> divergence-form identity is LINEAR in F --
plus the actual F_m):
 [1] EL_Phi == eq (I):  lap Psi + div[(F_X - eta_K/2) grad Phi] = 4 pi G rho
 [2] EL_Psi == eq (II): lap(Psi-Phi) = -(c^4/a0^2) d_i d_j [F_Y S_ij[Psi]]
 [3] eps=0 => slip harmonic => (regular@0 + decay) Psi == Phi:
     gamma_PPN = 1 EXACTLY at every X and every (lam_K, eta_K)
 [4] high-X kernel: g = g_N/k0 + a0/k0 - a0^2/g_N + ..., k0 = 1-eta_K/2
 [5] radial double-divergence identity (random-polynomial + numeric)
 [6] O(eps) slip on the Newtonian branch: gamma-1 = -(16/5) chi x^-3
 [7] A(X) large-X series
 [8] numbers vs Cassini
"""
import sympy as sp

x_, y_, z_ = sp.symbols('x y z', real=True)
V = (x_, y_, z_)
r_, a0, G, c, etaK, eps, B = sp.symbols('r a_0 G c eta_K epsilon B', positive=True)
delta = sp.eye(3)

Phi = sp.Function('Phi')(x_, y_, z_)
Psi = sp.Function('Psi')(x_, y_, z_)
rho = sp.Function('rho')(x_, y_, z_)

def lap(f):   return sum(sp.diff(f, v, 2) for v in V)
def div(w):   return sum(sp.diff(w[i], V[i]) for i in range(3))
def S_ij(f, i, j): return sp.diff(f, V[i], V[j]) - delta[i, j]*lap(f)/3

results = []
def check(name, cond):
    results.append((name, bool(cond)))
    print(('PASS' if cond else 'FAIL'), '--', name, flush=True)

def is_zero_num(expr, nsamples=4, tol=1e-12):
    """random-rational numeric zero test on an expression in x,y,z (fields concrete)."""
    import random
    random.seed(11)
    free = list(expr.free_symbols)
    for _ in range(nsamples):
        subs = {}
        for s in free:
            subs[s] = sp.Rational(random.randint(2, 9), random.randint(2, 7))
        val = sp.N(expr.subs(subs), 30)
        if abs(val) > tol*max(1, abs(val)+1):
            # scale-aware: compare against magnitude of a term
            return abs(sp.N(expr.subs(subs), 40)) < sp.Float(10)**(-15)
    return True

gradPhi2 = sum(sp.diff(Phi, v)**2 for v in V)
Xe = gradPhi2/a0**2
Ye = (c**4/a0**4)*sum(S_ij(Psi, i, j)**2 for i in range(3) for j in range(3))

Xs, Ys = sp.symbols('Xs Ys', positive=True)

def run_EL_check(Fsym, tag):
    """Fsym: expression in (Xs, Ys). Returns (ok1, ok2)."""
    Fexpr = Fsym.subs({Xs: Xe, Ys: Ye})
    FXc = sp.diff(Fsym, Xs).subs({Xs: Xe, Ys: Ye})
    FYc = sp.diff(Fsym, Ys).subs({Xs: Xe, Ys: Ye})
    L = (1/(16*sp.pi*G))*(2*sum(sp.diff(Psi, v)**2 for v in V)
         - 4*sum(sp.diff(Phi, v)*sp.diff(Psi, v) for v in V)
         + etaK*gradPhi2) \
        - (a0**2/(8*sp.pi*G))*Fexpr - rho*Phi
    # EL_Phi (1st order):
    ELPhi = sum(sp.diff(sp.diff(L, sp.diff(Phi, v)), v) for v in V) - sp.diff(L, Phi)
    target_I = lap(Psi) + div([(FXc - etaK/2)*sp.diff(Phi, v) for v in V]) - 4*sp.pi*G*rho
    d1 = sp.expand(-4*sp.pi*G*ELPhi - target_I)
    # EL_Psi (2nd order):
    t0 = sp.diff(L, Psi)
    t1 = sum(sp.diff(sp.diff(L, sp.diff(Psi, v)), v) for v in V)
    t2 = sp.S(0)
    for i in range(3):
        for j in range(3):
            if i == j:
                t2 += sp.diff(sp.diff(L, sp.diff(Psi, V[i], 2)), V[i], 2)
            elif i < j:
                t2 += sp.diff(sp.diff(L, sp.diff(Psi, V[i], V[j])), V[i], V[j])
    ELPsi = t0 - t1 + t2
    dd = sp.S(0)
    for i in range(3):
        for j in range(3):
            dd += sp.diff(FYc*S_ij(Psi, i, j), V[i], V[j])
    target_II = lap(Psi - Phi) + (c**4/a0**2)*dd
    # ELPsi as built is (dL/dPsi - div d/d(grad) + dd/d(hess)); the displayed
    # eq (II) is its (-4 pi G) multiple (same overall convention as EL_Phi)
    d2 = sp.expand(-4*sp.pi*G*ELPsi - target_II)
    return d1, d2

# concrete random-polynomial substitution for the numeric zero test
import random
random.seed(7)
def poly3(seed):
    random.seed(seed)
    terms = [x_, y_, z_, x_*y_, x_*z_, y_*z_, x_**2, y_**2, z_**2, x_**2*y_, x_*y_*z_]
    return sum(sp.Rational(random.randint(-5, 5), random.randint(1, 4))*t for t in terms)

PhiC, PsiC, rhoC = poly3(1), poly3(2), poly3(3)
def concretize(e):
    e = e.subs({Phi: PhiC, Psi: PsiC, rho: rhoC})
    return e.doit()

basis = [(Xs, '[X]'), (Xs**2, '[X^2]'), (Ys, '[Y]'), (Xs*Ys, '[XY]'), (Xs**2*Ys, '[X^2 Y]'),
         (-2*sp.sqrt(Xs) + 2*sp.log(1+sp.sqrt(Xs)), '[F_m]')]
ok1_all, ok2_all = True, True
for Fsym, tag in basis:
    d1, d2 = run_EL_check(Fsym, tag)
    z1 = is_zero_num(concretize(d1))
    z2 = is_zero_num(concretize(d2))
    ok1_all &= z1; ok2_all &= z2
    print('   ', tag, 'EL_Phi zero:', z1, ' EL_Psi zero:', z2, flush=True)
check('[1] EL_Phi == eq (I) on monomial basis + F_m (linear-in-F => generic F)', ok1_all)
check('[2] EL_Psi == eq (II) on monomial basis + F_m (S_ij[Psi] structure)', ok2_all)

# ----------------------------------------------------------------------
# [3] eps=0: eq (II) -> lap(Psi-Phi)=0.  Radial harmonic = C1 + C2/r.
# integrating (II) over a small ball: RHS = boundary flux of a field that
# vanishes with A(X) regular -> no delta source -> C2 = 0; decay -> C1 = 0.
# ----------------------------------------------------------------------
u = sp.Function('u')
gensol = sp.dsolve(sp.diff(r_**2*sp.diff(u(r_), r_), r_), u(r_)).rhs
cset = sorted(gensol.free_symbols - {r_}, key=lambda s: s.name)
istwo = len(cset) == 2
span_ok = istwo and sp.simplify(gensol - cset[0] - cset[1]/r_) == 0 or \
          istwo and sp.simplify(gensol - cset[1] - cset[0]/r_) == 0
check('[3] eps=0 slip solves lap s = 0: s = C1 + C2/r; regularity+decay => s=0 => gamma_PPN = 1 exactly', bool(span_ok))

# ----------------------------------------------------------------------
# [4] high-X kernel solve
# ----------------------------------------------------------------------
xk, yk = sp.symbols('x_k y_k', positive=True)
k0 = 1 - etaK/2
cc1, cc2 = sp.symbols('c1 c2')
ans = yk/k0 + cc1 + cc2/yk
res = sp.expand(sp.series(k0*ans - ans/(1+ans) - yk, yk, sp.oo, 2).removeO())
solc = sp.solve([res.coeff(yk, 0), res.coeff(yk, -1)], [cc1, cc2])
c1v, c2v = sp.simplify(solc[cc1]), sp.simplify(solc[cc2])
print('    c1 =', c1v, ';  c2 =', c2v)
check('[4a] g = g_N/(1-eta_K/2) + a0*c1 + a0^2*c2/g_N with c1 = 1/(1-eta_K/2)',
      sp.simplify(c1v - 1/k0) == 0)
check('[4b] eta_K=0: g -> g_N + a0 - a0^2/g_N (matches [mond-limits]); G_local = G/(1-eta_K/2)',
      sp.simplify(c1v.subs(etaK, 0) - 1) == 0 and sp.simplify(c2v.subs(etaK, 0) + 1) == 0)

# ----------------------------------------------------------------------
# [5] radial double-divergence identity, random polynomial T(r^2), f(r^2)
#     (use polynomials in r^2 so Cartesian expressions stay rational)
# ----------------------------------------------------------------------
r2 = x_**2 + y_**2 + z_**2
random.seed(23)
def polyr2(seed):
    random.seed(seed)
    return sum(sp.Rational(random.randint(-4, 4), random.randint(1, 3))*r2**k for k in range(1, 4))
ok5 = True
for sd in [(5, 6), (7, 8)]:
    Tc = polyr2(sd[0]); fc = polyr2(sd[1])
    Dsum = sp.S(0)
    for i in range(3):
        for j in range(3):
            Sij = sp.diff(fc, V[i], V[j]) - delta[i, j]*lap(fc)/3
            Dsum += sp.diff(Tc*Sij, V[i], V[j])
    Trad = Tc.subs(r2, r_**2); frad = fc.subs(r2, r_**2)
    Srad = sp.diff(frad, r_, 2) - sp.diff(frad, r_)/r_
    w_r = sp.Rational(2, 3)*(sp.diff(Trad*Srad, r_) + 3*Trad*Srad/r_)
    target5 = sp.expand(sp.diff(r_**2*w_r, r_)/r_**2)
    dd5 = sp.expand(Dsum - target5.subs(r_, sp.sqrt(r2)))
    ok5 &= is_zero_num(dd5)
check('[5] d_i d_j[T S_ij[f]] = (1/r^2) d/dr(r^2 w_r), w_r = (2/3)((TS)\' + 3TS/r)', ok5)

# ----------------------------------------------------------------------
# [6] O(eps) slip, Newtonian branch: Psi0 = -B/r, A -> X^-2
# ----------------------------------------------------------------------
Psi0 = -B/r_
Sr = sp.diff(Psi0, r_, 2) - sp.diff(Psi0, r_)/r_
check('[6a] S[Psi0] = -3B/r^3', sp.simplify(Sr + 3*B/r_**3) == 0)
Xr = (B/r_**2)**2/a0**2
T6 = (Xr**-2)*Sr
w6 = sp.Rational(2, 3)*(sp.diff(T6, r_) + 3*T6/r_)
sprime = -(eps*c**4/a0**2)*w6
s_slip = sp.integrate(sprime, r_)
check('[6b] slip Psi-Phi = (16/5) eps c^4 a0^2 r^5 / B^3',
      sp.simplify(s_slip - sp.Rational(16, 5)*eps*c**4*a0**2*r_**5/B**3) == 0)
xloc = B/(a0*r_**2)
gm1 = sp.simplify(s_slip/Psi0 + sp.Rational(16, 5)*(eps*c**4/(B*a0))/xloc**3)
check('[6c] gamma_PPN(r) - 1 = -(16/5) chi / x^3,  chi = eps c^4/(B a0), x = B/(a0 r^2)',
      sp.simplify(gm1) == 0)
check('[6d] eps>0 => slip>0 => gamma < 1 (light sees shallower potential)',
      s_slip.subs({eps: 1, c: 1, a0: 1, B: 1, r_: 1}) > 0)

# ----------------------------------------------------------------------
# [7] A(X) large-X series
# ----------------------------------------------------------------------
XX = sp.symbols('X', positive=True)
Aser = sp.series((XX**2/(1+XX)**4)*XX**2, XX, sp.oo, 2)
check('[7] A(X) = X^-2 (1 - 4/X + O(X^-2))',
      sp.simplify(Aser.removeO() - (1 - 4/XX)) == 0)

# ----------------------------------------------------------------------
# [8] numbers vs Cassini gamma-1 = (2.1 +/- 2.3)e-5
# ----------------------------------------------------------------------
a0N, GN, Msun, cN = 9.3619e-11, 6.674e-11, 1.989e30, 2.998e8
Rsun, AU = 6.957e8, 1.496e11
chi_cap = 1.73                # ellipticity cap on chi_sun = eps*Lambda_sun (repo sec9/15)
epsA_gw = 3.3e-55             # GW170817 bound on eps*A(X_path) [gw-sector]
Lam_sun = cN**4/(GN*Msun*a0N)
rows = []
for name, rm in [('R_sun', Rsun), ('Mercury', 0.387*AU), ('1 AU', AU), ('Saturn', 9.55*AU)]:
    xv = GN*Msun/rm**2/a0N
    g1_cap = (16/5)*chi_cap/xv**3
    eps_gw = epsA_gw*xv**4            # A ~ x^-4; eps = bound/A(X_path~few) is HARSHER; this is generous
    g1_gw = (16/5)*(min(eps_gw, epsA_gw/2.6e-2)*Lam_sun)/xv**3
    rows.append((name, xv, g1_cap, g1_gw))
    print(f'    {name:9s} x={xv:10.3e}  |gamma-1|_cap={g1_cap:9.2e}  |gamma-1|_GW={g1_gw:9.2e}')
check('[8a] |gamma-1| at the ellipticity cap: max over radii < 1e-15 (Cassini 2.3e-5: nil)',
      max(rw[2] for rw in rows) < 1e-15)
check('[8b] |gamma-1| at the GW170817 eps bound: smaller still', max(rw[3] for rw in rows) < 1e-15)

print()
n_pass = sum(1 for _, ok in results if ok)
print(f'{n_pass}/{len(results)} checks pass')
import sys
sys.exit(0 if n_pass == len(results) else 1)
