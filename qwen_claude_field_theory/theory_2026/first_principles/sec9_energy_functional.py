#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sec9_energy_functional.py -- program section 9, energy functional + part (b)
============================================================================
The static variational/energy structure of the FROZEN ACTION, derived from
scratch (two-potential; the single-potential schematic is NOT imported).

Setup (ASSUMED, standard static weak field):
    T = t,  N = 1 + e Phi/c^2,  N^i = 0,  h_ij = (1 - 2 e Psi/c^2) delta_ij,
    all fields static; e = amplitude bookkeeping;
    MOND double expansion: first order in the potentials, all orders in
    x = |grad Phi|/a0 and in the curvature ratio entering Y.

DERIVED AND CHECKED (PASS/FAIL), see also printed commentary:
  [A0] khronon kinematics exact; X is built from Phi ONLY, Y from Psi ONLY.
  [A1]-[A2] quadratic GR block coefficients SOLVED FOR (alpha,beta,gamma).
  [A3] eta_K block; Rbar_ij -> S_ij[Psi]/c^2; lam_K drops out (K_ij = 0).
  [A4] THE STATIC ENERGY FUNCTIONAL

       E[Phi,Psi] = INT d^3x { (1/8 pi G)[ -(grad Psi)^2
                     + 2 grad Phi . grad Psi - (eta_K/2)(grad Phi)^2
                     + a0^2 F(X,Y) ] + rho Phi },

       F(X,Y) = -2 sqrt(X) + 2 log(1+sqrt(X)) + eps A(X) Y,
       X = |grad Phi|^2/a0^2,  Y = (c^4/a0^4) S_ij[Psi] S_ij[Psi],
       S_ij[f] = d_i d_j f - (1/3) delta_ij lap f.

       delta E = 0  <=>  the static weak-field equations (both verified):
         (Phi):  lap Psi + div[ (F_X - eta_K/2 + eps A'(X) Y) grad Phi ]
                 = 4 pi G rho
         (Psi):  lap(Psi - Phi) + (eps c^4/a0^2) d_i d_j [A(X) S_ij[Psi]] = 0
       E = -L_static = canonical Hamiltonian for static fields (up to the
       matter rest-mass constant): a genuine variational energy principle.
       NOTE the structural point: the eps-term's double-divergence
       d_i d_j [A S_ij] acts on PSI and lands in the PSI-equation; the
       single-potential schematic (which put d_i d_j [A S_ij[Phi]] in the
       Phi-equation) is only the effective equation after eliminating Psi
       at O(eps) -- it is NOT the fundamental variational structure.
  [A5] Newtonian anchor: reduced kernel G(X) = X + F(X), G' = mu = x/(1+x);
       G convex, >= 0.
  [A6] boundedness/convexity (part b): E is a SADDLE -- unbounded below
       (long-wavelength Psi family; the eps-term CANNOT rescue it),
       unbounded above, not convex, not coercive.  Deep-MOND term alone:
       concave.  eps A Y term alone: bounded below iff eps > 0 but never
       jointly convex (A'' < 0 window).
  [A7] reduced eps = 0 functional: convex, bounded below, coercive along
       rays => Bekenstein-Milgrom-type uniqueness, DERIVED for this action.

Exit code 1 on any FAIL.
"""
import sys, random, time
import numpy as np
import sympy as sp
from sympy.calculus.euler import euler_equations

T0 = time.time()
x, y, z, e = sp.symbols('x y z e', real=True)
c, a0, G, etaK = sp.symbols('c a_0 G eta_K', positive=True)
epsl = sp.symbols('epsilon', real=True)
V = (x, y, z)
Phi = sp.Function('Phi')(x, y, z)
Psi = sp.Function('Psi')(x, y, z)
rho = sp.Function('rho')(x, y, z)
delta = sp.eye(3)

def grad(f):  return [sp.diff(f, v) for v in V]
def lap(f):   return sum(sp.diff(f, v, 2) for v in V)
def div(vec): return sum(sp.diff(vec[i], V[i]) for i in range(3))
def S_ij(f, i, j): return sp.diff(f, V[i], V[j]) - delta[i, j] * lap(f) / 3

results = []
def check(name, cond):
    results.append((name, bool(cond)))
    print(('PASS' if cond else 'FAIL'), '--', name, '   [t=%.1fs]' % (time.time() - T0))

def is_zero(expr):
    ee = sp.expand(expr)
    if ee == 0: return True
    ee = sp.simplify(ee)
    return ee == 0 or (hasattr(ee, 'equals') and ee.equals(0) is True)

random.seed(20260821)
_fP = sp.Rational(1, 10) * (2 * x + 3 * y - z) + sp.Rational(1, 20) * (x**2 - y * z) \
      + sp.Rational(1, 50) * x**2 * y
_fS = sp.Rational(1, 10) * (x - 2 * y + 2 * z) + sp.Rational(1, 25) * (y**2 + x * z) \
      + sp.Rational(1, 40) * z**3
_fR = sp.Rational(1, 10) * (1 + x * y)
def num_zero(expr, scale_ref=None, tol=1e-10):
    """Random-point numeric identity check on generic polynomial field probes.
    Rigor: the expressions are analytic in all arguments; vanishing at several
    generic points of a generic probe family to 1e-10 relative accuracy."""
    ee = expr.subs([(rho, _fR), (Phi, _fP), (Psi, _fS)]).doit()
    args = (x, y, z, c, a0, G, etaK, epsl, e)
    f = sp.lambdify(args, ee, 'numpy')
    fr = sp.lambdify(args, scale_ref.subs([(rho, _fR), (Phi, _fP), (Psi, _fS)]).doit(),
                     'numpy') if scale_ref is not None else None
    for _ in range(8):
        pt = [random.uniform(0.3, 1.2) for _ in range(3)]
        pars = (1.3, 0.7, 0.11, 0.23, 0.07, 0.31)
        v = f(*pt, *pars)
        ref = abs(fr(*pt, *pars)) + 1.0 if fr is not None else 1.0
        if not abs(v) < tol * ref:
            return False
    return True

def christoffel(g, coords):
    n = len(coords); ginv = g.inv()
    Gam = [[[sp.S(0)] * n for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for d in range(b, n):
                ex = sum(ginv[a, s] * (sp.diff(g[s, b], coords[d])
                                       + sp.diff(g[s, d], coords[b])
                                       - sp.diff(g[b, d], coords[s]))
                         for s in range(n)) / 2
                ex = sp.cancel(sp.expand(ex))
                Gam[a][b][d] = ex; Gam[a][d][b] = ex
    return Gam

def ricci(g, coords):
    n = len(coords); Gam = christoffel(g, coords)
    Ric = sp.zeros(n)
    for b in range(n):
        for d in range(b, n):
            expr = sp.S(0)
            for a in range(n):
                expr += sp.diff(Gam[a][b][d], coords[a]) - sp.diff(Gam[a][a][b], coords[d])
                for l in range(n):
                    expr += Gam[a][a][l] * Gam[l][b][d] - Gam[a][d][l] * Gam[l][a][b]
            Ric[b, d] = sp.cancel(sp.expand(expr)); Ric[d, b] = Ric[b, d]
    return Ric

print('=' * 100)
print('[A0] khronon 4-velocity and acceleration on the static conformal metric (exact)')
print('=' * 100)
t4 = sp.symbols('t')
Nlapse = 1 + e * Phi / c**2
Wc = 1 - 2 * e * Psi / c**2
g4 = sp.diag(-Nlapse**2 * c**2, Wc, Wc, Wc)
coords4 = (t4, x, y, z)
g4inv = g4.inv()
norm2 = -g4inv[0, 0]                                # -g^{tt} = 1/(N^2 c^2)
u_dn = sp.Matrix([-1 / sp.sqrt(norm2), 0, 0, 0])    # u_mu = -N c delta^t_mu
u_up = g4inv * u_dn
check('[A0.1] u_mu u^mu = -1 exactly (T = t, unit, hypersurface-orthogonal)',
      is_zero(sp.cancel(sp.expand((u_dn.T * u_up)[0, 0] + 1))))
Gam4 = christoffel(g4, coords4)
a_dn = [sp.cancel(sp.expand(sum(u_up[n4] * (sp.diff(u_dn[m4], coords4[n4])
        - sum(Gam4[l4][n4][m4] * u_dn[l4] for l4 in range(4)))
        for n4 in range(4)))) for m4 in range(4)]
ok = is_zero(a_dn[0]) and all(num_zero(a_dn[i + 1] - sp.diff(sp.log(Nlapse), V[i]))
                              for i in range(3))
check('[A0.2] a_0 = 0 and a_i = d_i ln N  (EXACT, all orders in e)', ok)
Xexact = c**4 * (1 / Wc) * sum(a_dn[i + 1]**2 for i in range(3)) / a0**2
Xtarget = (e**2 * sum(sp.diff(Phi, v)**2 for v in V)
           / (a0**2 * (1 + e * Phi / c**2)**2 * (1 - 2 * e * Psi / c**2)))
check('[A0.3] X exact = e^2|grad Phi|^2/(a0^2 N^2 (1-2e Psi/c^2)): leading order'
      ' X = |grad Phi|^2/a0^2 -- the LAPSE potential Phi ONLY',
      num_zero(Xexact - Xtarget))

print('=' * 100)
print('[A1]-[A2] quadratic GR block of N sqrt(h) (3)R: coefficients SOLVED FOR')
print('=' * 100)
h3 = sp.diag(Wc, Wc, Wc)
Ric3 = ricci(h3, V)
R3 = sp.cancel(sp.expand(sum(Ric3[i, i] for i in range(3)) / Wc))
EHdensity = Nlapse * Wc**sp.Rational(3, 2) * R3

def coeff_e(expr, k):
    return sp.expand(sp.diff(expr, e, k).subs(e, 0) / sp.factorial(k))

E0 = coeff_e(EHdensity, 0)
E1 = coeff_e(EHdensity, 1)
E2 = coeff_e(EHdensity, 2)
check('[A1.0] O(e^0) of N sqrt(h)(3)R vanishes (flat background)', is_zero(E0))
check('[A1.1] O(e^1) = (4/c^2) lap Psi exactly: a pure divergence, no tadpole',
      is_zero(sp.expand(E1 - 4 * lap(Psi) / c**2)))

al, be, ga = sp.symbols('alpha beta gamma')
gP = grad(Phi); gS = grad(Psi)
gradPhi2 = sum(gi**2 for gi in gP)
gradPsi2 = sum(gi**2 for gi in gS)
dotPS = sum(gP[i] * gS[i] for i in range(3))
cand = (al * gradPsi2 + be * dotPS + ga * gradPhi2) / c**4
eldiff = euler_equations(sp.expand(E2 - cand), [Phi, Psi], V)
probes = [(x**2 + x * y, y**2 + z**2 + x * z), (x * y * z + x**3, x**2 * y + z**3)]
lin_eqs = []
for fP, fS in probes:
    for eq in eldiff:
        expr = sp.expand((eq.lhs - eq.rhs).subs([(Phi, fP), (Psi, fS)]).doit())
        lin_eqs.extend(sp.Poly(expr, x, y, z).coeffs())
sol = sp.solve(list(set(lin_eqs)), [al, be, ga], dict=True)
assert len(sol) == 1, 'quadratic block not uniquely determined: %s' % sol
alv, bev, gav = sol[0][al], sol[0][be], sol[0][ga]
ok2 = all(is_zero(sp.expand((eq.lhs - eq.rhs).subs(sol[0]))) for eq in eldiff)
check('[A2] N sqrt(h)(3)R|_{e^2} = (1/c^4)[%s (grad Psi)^2 + (%s) gradPhi.gradPsi + '
      '(%s)(grad Phi)^2] + tot.div. (two-potential GR block: SOLVED, generic fields)'
      % (alv, bev, gav), ok2 and (alv, bev, gav) == (2, -4, 0))

print('=' * 100)
print('[A3] eta_K block, Rbar linearisation, staticity')
print('=' * 100)
eta_block = sp.expand(sp.diff(Nlapse * Wc**sp.Rational(3, 2)
                              * etaK * (1 / Wc) * sum(a_dn[i + 1]**2 for i in range(3)),
                              e, 2).subs(e, 0) / 2)
check('[A3.1] eta_K N sqrt(h) a_i a^i |_{e^2} = eta_K (grad Phi)^2/c^4',
      num_zero(eta_block - etaK * gradPhi2 / c**4))
okR = all(is_zero(sp.expand(sp.diff(Ric3[i, j] - h3[i, j] * R3 / 3, e).subs(e, 0)
                            - S_ij(Psi, i, j) / c**2))
          for i in range(3) for j in range(3))
check('[A3.2] linearised Rbar_ij = (1/c^2) S_ij[Psi]: TRACE-FREE Hessian of the'
      ' SPATIAL potential Psi ONLY  =>  Y = (c^4/a0^4) S_ij[Psi] S_ij[Psi]', okR)
print('   [A3.3] staticity: h_ij time-independent, N^i = 0  =>  K_ij = 0 exactly =>')
print('          the lam_K K^2 and K_ij K^ij terms VANISH; lam_K is ABSENT from the')
print('          entire static sector.                                    [DERIVED]')

print('=' * 100)
print('[A4] THE STATIC ENERGY FUNCTIONAL and its Euler-Lagrange equations')
print('=' * 100)
X = gradPhi2 / a0**2
xs = sp.sqrt(X)
Fmond = -2 * xs + 2 * sp.log(1 + xs)
Afun = X**2 / (1 + X)**4
Yq = c**4 / a0**4 * sum(S_ij(Psi, i, j)**2 for i in range(3) for j in range(3))
Ffull = Fmond + epsl * Afun * Yq
# E = -L_static; prefactor anchor IMPORTED (repo): M_Pl^2 c^3/2 = c^4/(16 pi G),
# so the F-term is -(a0^2/8 pi G) F per dt d^3x; matter couples through N only
# with conserved coordinate mass density (IMPORTED: sec14 script) => +rho Phi in E.
Edens = (sp.S(1) / (8 * sp.pi * G)) * (
    -gradPsi2 + 2 * dotPS - (etaK / 2) * gradPhi2 + a0**2 * Ffull) + rho * Phi
print('  E[Phi,Psi] = INT d^3x { (1/8piG)[ -(grad Psi)^2 + 2 grad Phi.grad Psi')
print('               - (eta_K/2)(grad Phi)^2 + a0^2 F(X,Y) ] + rho Phi }')
print('  (assembled from [A2] with the IMPORTED anchor prefactor; E = -L_static =')
print('   canonical Hamiltonian density for static fields, up to matter rest mass)')
eqs = euler_equations(Edens, [Phi, Psi], V)
elphi = eqs[0].lhs - eqs[0].rhs
elpsi = eqs[1].lhs - eqs[1].rhs
FX = -1 / (1 + xs)
Ap = 2 * X * (1 - X) / (1 + X)**5
coefPhi = FX - etaK / 2 + epsl * Ap * Yq
target_phi = (lap(Psi) + div([coefPhi * gP[i] for i in range(3)])) / (4 * sp.pi * G) - rho
tidal = sum(sp.diff(Afun * S_ij(Psi, i, j), V[i], V[j]) for i in range(3) for j in range(3))
target_psi = (lap(Psi) - lap(Phi) + (epsl * c**4 / a0**2) * tidal) / (4 * sp.pi * G)
check('[A4.1] delta E/delta Phi = 0  <=>  lap Psi + div[(F_X - eta_K/2 + eps A\'(X) Y)'
      ' grad Phi] = 4 pi G rho', num_zero(elphi + target_phi, scale_ref=target_phi))
check('[A4.2] delta E/delta Psi = 0  <=>  lap(Psi - Phi) + (eps c^4/a0^2)'
      ' d_i d_j[A(X) S_ij[Psi]] = 0', num_zero(elpsi - target_psi, scale_ref=target_psi))
print('   STRUCTURAL: the double-divergence tidal operator acts on S_ij[PSI] and sits')
print('   in the PSI-equation; the Phi-equation feels the eps-term only through the')
print('   scalar kernel shift eps A\'(X) Y.  The single-potential schematic (S_ij[Phi]')
print('   in the Phi-equation) is the O(eps) EFFECTIVE equation after eliminating Psi,')
print('   NOT the variational structure of the frozen action.')

print('=' * 100)
print('[A5] Newtonian anchor and the reduced kernel G(X) = X + F(X)')
print('=' * 100)
Xs = sp.symbols('X_s', positive=True)
xv = sp.sqrt(Xs)
fM = -2 * xv + 2 * sp.log(1 + xv)
GX = Xs + fM
mu = sp.simplify(sp.diff(GX, Xs))
check('[A5.1] G\'(X) = mu = x/(1+x): the 2 gradPhi.gradPsi cross term supplies the'
      ' "+1" in mu = 1 + F_X after Psi-elimination',
      is_zero(sp.simplify(mu - xv / (1 + xv))))
radial = sp.simplify(2 * sp.diff(GX, Xs) + 4 * Xs * sp.diff(GX, Xs, 2))
check('[A5.2] Hessian of a0^2 G(|g|^2/a0^2) in g: transverse eigenvalue 2mu > 0 (x2),'
      ' radial = 2x(2+x)/(1+x)^2 > 0 for x > 0',
      is_zero(sp.simplify(radial - 2 * xv * (2 + xv) / (1 + xv)**2)))
check('[A5.3] G >= 0, G(0) = 0; G ~ X (Newtonian) at large X, ~ (2/3)X^{3/2} deep-MOND',
      sp.limit(GX / Xs, Xs, sp.oo) == 1 and
      is_zero(sp.limit(GX / Xs**sp.Rational(3, 2), Xs, 0) - sp.Rational(2, 3)))
Ered_check = sp.expand((-gradPsi2 + 2 * dotPS).subs(Psi, Phi).doit() - gradPhi2)
check('[A5.4] at Psi = Phi: -(grad Psi)^2 + 2 gradPhi.gradPsi == +(grad Phi)^2, so'
      ' E(eps=etaK=0)|_{Psi=Phi} = INT[a0^2 G(X)/(8piG) + rho Phi]', is_zero(Ered_check))

print('=' * 100)
print('[A6] boundedness / convexity / coercivity of E  (part b)')
print('=' * 100)
xr = sp.symbols('x_r', positive=True)
fmx = -2 * xr + 2 * sp.log(1 + xr)
check('[A6.1] deep-MOND term alone: f\' = -2x/(1+x) < 0, f\'\' = -2/(1+x)^2 < 0'
      ' => CONCAVE, unbounded below (~ -2x); convexity of the reduced theory comes'
      ' ENTIRELY from the GR cross term (the +X in G = X + F)',
      is_zero(sp.simplify(sp.diff(fmx, xr) + 2 * xr / (1 + xr))) and
      is_zero(sp.simplify(sp.diff(fmx, xr, 2) + 2 / (1 + xr)**2)))
Xq = sp.symbols('X_q', positive=True)
App = sp.simplify(sp.diff(Xq**2 / (1 + Xq)**4, Xq, 2))
rootsA = sorted([r for r in sp.solve(sp.Eq(3 * Xq**2 - 6 * Xq + 1, 0), Xq)])
check('[A6.2] A\'\'(X) = 2(3X^2-6X+1)/(1+X)^6, NEGATIVE exactly on X in'
      ' (1-sqrt(2/3), 1+sqrt(2/3)) ~ (0.1835, 1.8165) => eps A(X) Y is NOT jointly'
      ' convex (X-concave there at fixed Y > 0), either sign of eps',
      is_zero(sp.simplify(App - 2 * (3 * Xq**2 - 6 * Xq + 1) / (1 + Xq)**6)) and
      abs(float(rootsA[0]) - (1 - np.sqrt(2. / 3))) < 1e-12 and
      abs(float(rootsA[1]) - (1 + np.sqrt(2. / 3))) < 1e-12)
check('[A6.3] A(0) = 0, A\'(0) = 0: the eps-term switches OFF where grad Phi = 0'
      ' (degeneracy of the 4th-order sector at critical points; used in the symbol'
      ' script)', sp.simplify((Xq**2 / (1 + Xq)**4).subs(Xq, 0)) == 0 and
      sp.simplify(sp.diff(Xq**2 / (1 + Xq)**4, Xq).subs(Xq, 0)) == 0)

def numeric_psi_scaling():
    Ls = [4.0, 8.0, 16.0, 32.0]
    out = []
    n = 64
    for kY in (0.0, 1.0, 100.0):
        vals = []
        for L in Ls:
            h = 6.0 * L / n
            ax = (np.arange(n) - n / 2 + .5) * h
            XX, YY, ZZ = np.meshgrid(ax, ax, ax, indexing='ij')
            R2 = XX**2 + YY**2 + ZZ**2
            psi = L * np.exp(-R2 / (2 * L**2))
            gx, gy, gz = np.gradient(psi, h, edge_order=2)
            grad2 = gx**2 + gy**2 + gz**2
            hxx = np.gradient(gx, h, axis=0, edge_order=2)
            hyy = np.gradient(gy, h, axis=1, edge_order=2)
            hzz = np.gradient(gz, h, axis=2, edge_order=2)
            hxy = np.gradient(gx, h, axis=1, edge_order=2)
            hxz = np.gradient(gx, h, axis=2, edge_order=2)
            hyz = np.gradient(gy, h, axis=2, edge_order=2)
            lapp = hxx + hyy + hzz
            S2 = ((hxx - lapp / 3)**2 + (hyy - lapp / 3)**2 + (hzz - lapp / 3)**2
                  + 2 * hxy**2 + 2 * hxz**2 + 2 * hyz**2)
            vals.append(np.sum(-grad2 + kY * S2) * h**3)
        out.append((kY, vals))
    return Ls, out

Ls, scal = numeric_psi_scaling()
print('  Psi-direction counterexample: psi_L = L exp(-r^2/2L^2) around a background')
print('  with the eps-term ON (coefficient kY := eps A(X0) c^4/a0^2 held fixed):')
print('  dE = (1/8piG) INT[ -(grad psi_L)^2 + kY S[psi_L]:S[psi_L] ]  (units 8piG=1)')
okB = True
for kY, vals in scal:
    print('    kY=%6.1f : ' % kY + '  '.join('%10.4g' % v for v in vals)
          + '   for L = ' + str(Ls))
    # asymptotic claim: dE < 0 and falling ~ L^3 at large L (at strong kY the
    # subleading +kY L term delays the turnover, it cannot prevent it)
    okB = okB and vals[-1] < vals[-2] < 0 and vals[-1] / vals[-2] > 4.0
check('[A6.4] E UNBOUNDED BELOW on every background: INT(grad psi_L)^2 = L^3 INT(grad f)^2'
      ' but INT S[psi_L]^2 = L INT S[f]^2 -- the quartic-derivative eps-term scales one'
      ' power of L, the negative GR term three: dE ~ -C L^3 for ANY eps', okB)

def numeric_up():
    n = 48; h = 20.0 / n
    ax = (np.arange(n) - n / 2 + .5) * h
    XX, YY, ZZ = np.meshgrid(ax, ax, ax, indexing='ij')
    R2 = XX**2 + YY**2 + ZZ**2
    P = -1.0 / np.sqrt(1.0 + R2)
    gx, gy, gz = np.gradient(P, h, edge_order=2)
    g2 = gx**2 + gy**2 + gz**2
    lams = [1., 4., 16., 64.]
    va = []
    for lam in lams:
        Xf = lam**2 * g2
        Ff = -2 * np.sqrt(Xf) + 2 * np.log(1 + np.sqrt(Xf))
        dens = lam**2 * g2 + Ff        # (-(gPsi)^2 + 2 gPhi.gPsi)|_{Psi=Phi} + F, a0=1
        va.append(np.sum(dens) * h**3)
    return lams, va

lams, va = numeric_up()
print('  E[lambda P, lambda P] (vacuum, units 8piG = a0 = 1): '
      + '  '.join('%.4g' % v for v in va))
check('[A6.5] E UNBOUNDED ABOVE along lambda (P,P): grows ~ lambda^2 (Newtonian'
      ' quadratic dominance)', all(v2 > v1 for v1, v2 in zip(va, va[1:]))
      and va[-1] > 100 * abs(va[0]))
print('  => E is a SADDLE functional: NOT convex, NOT bounded either way, NOT coercive.')
print('     This is the GR conformal-mode saddle, DERIVED here for the frozen action;')
print('     it is a property of the (Phi,Psi) pair, not a pathology of the F-term.')
print('     The meaningful positivity lives on the reduced slice ([A7]) and in the')
print('     second-variation/ellipticity analysis (sec9_second_variation_symbol.py).')

print('=' * 100)
print('[A7] reduced functional (eps = 0): convex, bounded below, coercive along rays')
print('=' * 100)
def numeric_red():
    n = 48; h = 20.0 / n
    ax = (np.arange(n) - n / 2 + .5) * h
    XX, YY, ZZ = np.meshgrid(ax, ax, ax, indexing='ij')
    R2 = XX**2 + YY**2 + ZZ**2
    P = -1.0 / np.sqrt(1.0 + R2)
    rhoP = 3.0 / (4 * np.pi) * (1.0 + R2)**-2.5
    gx, gy, gz = np.gradient(P, h, edge_order=2)
    g2 = gx**2 + gy**2 + gz**2
    lams = [-64., -8., -1., 1., 8., 64.]
    va = []
    for lam in lams:
        Xf = lam**2 * g2
        sx = np.sqrt(Xf)
        GG = Xf - 2 * sx + 2 * np.log(1 + sx)
        va.append(np.sum(GG / 2.0 + rhoP * lam * P) * h**3)   # 8piG = 2*(4piG=1)
    return lams, va

lams, va = numeric_red()
print('  E_red[lambda Phi_plummer], lambda = ' + str(lams) + ':')
print('     ' + '  '.join('%9.4g' % v for v in va))
check('[A7.1] E_red = INT[a0^2 G(X)/8piG + rho Phi] coercive along scaling rays'
      ' (-> +inf both directions, minimum at lambda ~ O(1))',
      va[0] > va[2] and va[-1] > va[-3] and min(va) in (va[2], va[3]))
print('    G convex pointwise [A5.2] => E_red CONVEX (strict where grad Phi != 0)')
print('    => at most ONE critical point: Bekenstein-Milgrom-type uniqueness for the')
print('       frozen action at eps = 0.   (Full coercivity on the natural Orlicz')
print('       class ~ min(|g|^2, |g|^3): standard, ASSUMED functional-analytic detail.)')
print('    For eps != 0 no local reduction exists (4th-order Psi solve, nonlocal):')
print('    the honest stability object is the COUPLED second variation -> next script.')

print('=' * 100)
nfail = sum(1 for _, okc in results if not okc)
print('SUMMARY: %d checks, %d FAIL   [total %.1fs]' % (len(results), nfail, time.time() - T0))
sys.exit(1 if nfail else 0)
