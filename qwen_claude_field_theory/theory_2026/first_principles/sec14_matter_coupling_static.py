#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SECTION 14 -- Matter coupling, local (static weak-field) G, and the
perturbations pointer, for the FROZEN ACTION (sympy-verified; c = 1).

Static sector conventions:
  N = e^{k phi},  h_ij = e^{-2 k psi} delta_ij   (k = field-amplitude bookkeeping)
  a_i = D_i ln N = k d_i phi   (verified below on a general static metric)
  X = a_i a^i / a0^2  ->  (grad phi)^2 / a0^2 at leading order in psi
  weak-field double expansion: FIRST order in the potentials phi, psi,
  ALL orders in |grad phi|/a0 (standard AQUAL bookkeeping; dropped terms are
  relatively O(phi, psi)).

WHAT THIS SCRIPT DERIVES AND VERIFIES:

  [14.0] Convention sanity: the direct 3D Ricci computation reproduces R = 6
         for the unit round S^3 in stereographic (conformally flat) form; and
         a_mu = (0, d_i ln N) on a general static metric.               [DERIVED]
  [14.1] Quadratic static action (no F): N sqrt(h)[(3)R + eta_K a_i a^i] gives,
         up to total derivatives, L2 = 2(grad psi)^2 - 4 grad phi.grad psi
         + eta_K (grad phi)^2; the linear term is a pure divergence.    [DERIVED]
  [14.2] With dust coupled ONLY through N (S_m = -int rho N, rho = conserved
         coordinate mass density): the psi-equation forces psi = phi
         (Delta(psi - phi) = 0 with decaying b.c.)  =>  gamma_PPN = 1 at this
         order, INDEPENDENT of eta_K and of the F-term (which carries no psi
         at this order).  The eps Y-term is quartic here (A(X)Y ~ phi^4 psi^2
         gradients) and DORMANT for linear response; it is the ONLY source of
         phi - psi differences, entering at nonlinear order in the
         intermediate-X regime.                                          [DERIVED]
  [14.3] The full static field equation:
             div[ (1 + F_X - eta_K/2) grad phi ] = 4 pi G rho
         with 1 + F_X = mu(x) = x/(1+x), x = |grad phi|/a0.  So the operative
         kernel is  mu(x) - eta_K/2.                                     [DERIVED]
  [14.4] Newtonian limit (X -> oo): G_local = G/(1 - eta_K/2); GR at eta_K=0.
         Combined with sec13:  G_cosmo/G_local = (2 - eta_K)/(3 lam_K - 1).
                                                                         [DERIVED]
  [14.5] Deep-MOND limit: kernel -> x - eta_K/2 + O(x^2).  MOND phenomenology
         therefore REQUIRES eta_K/2 << x at the lowest probed accelerations
         (x ~ 1e-2): eta_K << ~2e-2 from this alone; PPN preferred-frame
         bounds are far stronger and subsume it.                         [DERIVED]
  [14.6] Matter coupling statements (proof in comments, instance verified):
         S_m[g, psi_m] contains NO khronon T  =>  delta S_m/delta T == 0:
         NO direct khronon-matter vertex, hence NO tree-level fifth force;
         diffeomorphism invariance of S_m ALONE (independent of the gravity
         equations) gives nabla_mu T^{mu nu} = 0 on the matter shell; dust
         then moves on geodesics of g; WEP holds for test bodies.
         Verified instance: FLRW continuity (sec13 [13.6]).              [DERIVED]
  [14.7] Perturbations POINTER: around X = 0 (cosmology), the quadratic
         acceleration term of  eta_K a.a - 2 a0^2 F(a.a/a0^2)  is
         (eta_K + 2) a.a: the theory sits at effective khronometric
         alpha_eff = 2 + eta_K, i.e. AT the alpha = 2 boundary (up to eta_K).
         2 - alpha_eff = -eta_K exactly.  The same F_X(0) = -1 that makes
         mu(0) = 0 (the MOND limit) produces this: the khronon scalar's
         gradient/pressure term is O(eta_K, lam_K - 1) instead of O(1) --
         the natural DUST-LIKE growth carrier.  Amplitude, initial conditions
         and the SIGN of c_s^2 (stability!) are NOT derived here.
                                                       [DERIVED coefficient;
                                                        rest UNRESOLVED]
"""
import sys
import sympy as sp
from sympy.calculus.euler import euler_equations

x, y, z = sp.symbols('x y z', real=True)
X3 = [x, y, z]
eta = sp.Symbol('eta_K', real=True)
G = sp.Symbol('G', positive=True)
a0 = sp.Symbol('a0', positive=True)
pi = sp.pi
pref = 1/(16*pi*G)

results = []
def check(name, cond):
    ok = bool(cond)
    results.append(ok)
    print(("PASS: " if ok else "FAIL: ") + name)

def lap(f):
    return sum(sp.diff(f, c, 2) for c in X3)

# ----------------------------------------------------------------------------
# [14.0a] direct 3D Ricci scalar for a conformally flat metric h = e^{2w} delta
# ----------------------------------------------------------------------------
def ricci3_conformal(omega, simplify_out=True):
    h = sp.eye(3)*sp.exp(2*omega)
    hinv = sp.eye(3)*sp.exp(-2*omega)
    Gam = [[[sp.S(0)]*3 for _ in range(3)] for _ in range(3)]
    for l in range(3):
        for m in range(3):
            for n_ in range(3):
                Gam[l][m][n_] = sp.expand(sum(
                    hinv[l, s_]*(sp.diff(h[s_, m], X3[n_])
                                 + sp.diff(h[s_, n_], X3[m])
                                 - sp.diff(h[m, n_], X3[s_])) for s_ in range(3))/2)
    Ric = sp.zeros(3, 3)
    for i in range(3):
        for j in range(3):
            Ric[i, j] = (sum(sp.diff(Gam[kk][i][j], X3[kk]) for kk in range(3))
                         - sum(sp.diff(Gam[kk][i][kk], X3[j]) for kk in range(3))
                         + sum(Gam[kk][kk][l_]*Gam[l_][i][j]
                               for kk in range(3) for l_ in range(3))
                         - sum(Gam[kk][j][l_]*Gam[l_][i][kk]
                               for kk in range(3) for l_ in range(3)))
    R = sum(hinv[i, j]*Ric[i, j] for i in range(3) for j in range(3))
    return sp.simplify(R) if simplify_out else sp.expand(R)

# sanity: unit round S^3 stereographic, h = [2/(1+r^2)]^2 delta  =>  R = 6
R_sphere = ricci3_conformal(sp.log(2/(1 + x**2 + y**2 + z**2)))
check("[14.0a] direct Ricci computation gives R = 6 on the unit S^3", sp.simplify(R_sphere - 6) == 0)

# ----------------------------------------------------------------------------
# [14.0b] a_i = D_i ln N on a general static metric (khronon T = t)
# ----------------------------------------------------------------------------
t = sp.Symbol('t', real=True)
coords4 = [t, x, y, z]
LamF = sp.Function('LambdaN', real=True)(x, y, z)   # N = e^Lambda
wF = sp.Function('w', real=True)(x, y, z)           # h_ij = e^{2w} delta_ij
g4 = sp.diag(-sp.exp(2*LamF), sp.exp(2*wF), sp.exp(2*wF), sp.exp(2*wF))
g4inv = g4.inv()
Gam4 = [[[sp.simplify(sum(g4inv[l, s_]*(sp.diff(g4[s_, m], coords4[n_])
                                        + sp.diff(g4[s_, n_], coords4[m])
                                        - sp.diff(g4[m, n_], coords4[s_]))
                          for s_ in range(4))/2)
          for n_ in range(4)] for m in range(4)] for l in range(4)]
u4_lo = [-sp.exp(LamF), 0, 0, 0]
u4_up = [sp.simplify(sum(g4inv[m, n_]*u4_lo[n_] for n_ in range(4))) for m in range(4)]
acc4 = [sp.simplify(sum(u4_up[n_]*(sp.diff(u4_lo[m], coords4[n_])
                                   - sum(Gam4[l][n_][m]*u4_lo[l] for l in range(4)))
                        for n_ in range(4))) for m in range(4)]
check("[14.0b] static metric: a_mu = (0, d_i Lambda) = (0, D_i ln N) exactly",
      sp.simplify(acc4[0]) == 0 and
      all(sp.simplify(acc4[i] - sp.diff(LamF, X3[i - 1])) == 0 for i in (1, 2, 3)))

# ----------------------------------------------------------------------------
# [14.1]-[14.2] quadratic static action and psi = phi
# ----------------------------------------------------------------------------
k = sp.Symbol('k')                                   # bookkeeping parameter
phi = sp.Function('phi', real=True)(x, y, z)
psi = sp.Function('psi', real=True)(x, y, z)
rho = sp.Function('rho', real=True)(x, y, z)

R3 = ricci3_conformal(-k*psi, simplify_out=False)
gradphi2 = sum(sp.diff(phi, c)**2 for c in X3)
NsH = sp.exp(k*phi - 3*k*psi)                        # N sqrt(h)
# a_i a^i = h^{ij} a_i a_j = e^{2 k psi} k^2 (grad phi)^2
Lg_noF = NsH*(R3 + eta*sp.exp(2*k*psi)*k**2*gradphi2)
ser = sp.expand(Lg_noF.series(k, 0, 3).removeO())
L0 = ser.coeff(k, 0)
L1 = sp.expand(ser.coeff(k, 1))
L2 = sp.expand(ser.coeff(k, 2))
check("[14.1] O(k^0) vanishes (flat space is a solution)", sp.simplify(L0) == 0)
eqs_L1 = euler_equations(L1, [phi, psi], X3)
check("[14.1] O(k^1) term is a pure divergence (EL-trivial)",
      all(sp.simplify(e.lhs - e.rhs) == 0 for e in eqs_L1))

Ltot = pref*L2 - rho*phi     # dust couples through N only: S_m = -int rho e^{k phi}
eqs = euler_equations(Ltot, [phi, psi], X3)
exprs = [sp.expand(e.lhs - e.rhs) for e in eqs]
exprPhi = next(e for e in exprs if e.has(rho))
exprPsi = next(e for e in exprs if not e.has(rho))

ok_psi = any(sp.simplify(exprPsi - sgn*4*pref*(lap(psi) - lap(phi))) == 0
             for sgn in (1, -1))
check("[14.2] psi-equation is Delta(psi - phi) = 0  =>  psi = phi (decaying b.c.)"
      "  =>  gamma_PPN = 1 at linear response, independent of eta_K", ok_psi)

exprPhi_sub = exprPhi.subs(psi, phi)
check("[14.2] phi-equation on psi=phi:  (4 - 2 eta_K)/(16 pi G) Delta phi = rho",
      sp.simplify(exprPhi_sub - (-rho + pref*(4 - 2*eta)*lap(phi))) == 0)
check("[14.4] => G_local = G/(1 - eta_K/2)   (GR: eta_K = 0 gives Delta phi = 4 pi G rho)",
      sp.simplify(16*pi*G/(4 - 2*eta) - 4*pi*G/(1 - eta/2)) == 0)

# ----------------------------------------------------------------------------
# [14.3] add the F-term (depends on grad phi only at this order; the eps Y-term
#         is quartic in fields and dormant for linear response)
# ----------------------------------------------------------------------------
XF = gradphi2/a0**2
Ffrozen = -2*sp.sqrt(XF) + 2*sp.log(1 + sp.sqrt(XF))
LF = -2*a0**2*pref*Ffrozen
eqF = euler_equations(LF, [phi], X3)[0]
exprF = sp.expand(eqF.lhs - eqF.rhs)
FXfun = -1/(1 + sp.sqrt(XF))
targetF = 4*pref*sum(sp.diff(FXfun*sp.diff(phi, c), c) for c in X3)
check("[14.3] F-term EL contribution = (4/16 pi G) div[F_X grad phi]",
      sp.simplify(exprF - targetF) == 0)

combined_target = 4*pref*sum(sp.diff((1 + FXfun - eta/2)*sp.diff(phi, c), c)
                             for c in X3) - rho
check("[14.3] FULL static equation: div[(1 + F_X - eta_K/2) grad phi] = 4 pi G rho",
      sp.simplify((exprPhi_sub + exprF) - combined_target) == 0)

Xs = sp.Symbol('X', positive=True)
s = sp.Symbol('s', positive=True)  # s = sqrt(X) = x = g/a0
Ffull = -2*sp.sqrt(Xs) + 2*sp.log(1 + sp.sqrt(Xs))
FX = sp.simplify(sp.diff(Ffull, Xs))
check("[14.3] F_X = -1/(1+sqrt(X))  (repo fact re-derived)",
      sp.simplify(FX + 1/(1 + sp.sqrt(Xs))) == 0)
mu = 1 + FX
check("[14.3] mu = 1 + F_X = x/(1+x)", sp.simplify(mu - sp.sqrt(Xs)/(1 + sp.sqrt(Xs))) == 0)
check("[14.4] Newtonian limit: mu -> 1, kernel -> 1 - eta_K/2",
      sp.limit(mu, Xs, sp.oo) == 1)
mu_ser = sp.series(mu.subs(Xs, s**2), s, 0, 3).removeO().expand()
check("[14.5] deep-MOND: mu = x - x^2 + ..., kernel -> x - eta_K/2",
      mu_ser.coeff(s, 1) == 1 and mu_ser.coeff(s, 2) == -1)
print("NOTE [14.5]: the deep-MOND kernel is (x - eta_K/2): MOND phenomenology at")
print("  the lowest probed accelerations (x ~ 1e-2) REQUIRES eta_K << ~2e-2 from")
print("  this alone; PPN preferred-frame bounds on the a_i a^i coupling are far")
print("  stronger and subsume it.  [DERIVED here; PPN numerics not re-derived]")

# eps Y-term dormancy bookkeeping: A(X) = X^2/(1+X)^4 asymptotics (repo facts)
Aa = Xs**2/(1 + Xs)**4
check("[14.2] A(1) = 1/16, A'(1) = 0 (peak at the MOND scale)",
      sp.simplify(Aa.subs(Xs, 1) - sp.Rational(1, 16)) == 0
      and sp.simplify(sp.diff(Aa, Xs).subs(Xs, 1)) == 0)
check("[14.2] A ~ X^2 (X<<1) and A ~ X^-2 (X>>1): eps-term dead in BOTH the deep-"
      "MOND and Newtonian limits => it cannot shift G_local",
      sp.limit(Aa/Xs**2, Xs, 0) == 1 and sp.limit(Aa*Xs**2, Xs, sp.oo) == 1)
print("NOTE [14.2] (the two-potential point the earlier schematic guessed at):")
print("  X is built from the LAPSE (phi), Y from the SPATIAL curvature (psi).")
print("  At linear response the eps A(X) Y term is quartic in fields, so it is")
print("  DORMANT: psi = phi and the phi-equation above are exact at this order.")
print("  At nonlinear order in the intermediate regime (X ~ 1, where A peaks at")
print("  1/16) the eps-term enters the PSI equation (it is the only Y-carrier),")
print("  sourcing phi - psi differences there -- NOT the single-potential")
print("  d_i d_j [eps A S_ij(phi)] guess of the earlier schematic.")

# ----------------------------------------------------------------------------
# [14.6] matter coupling (structural; instance = FLRW continuity in sec13)
# ----------------------------------------------------------------------------
print("STATEMENT [14.6]: S_m = S_m[g_munu, psi_m] contains NO khronon T, so")
print("  delta S_m/delta T == 0 IDENTICALLY: there is no direct khronon-matter")
print("  vertex and hence NO tree-level fifth force. Diffeomorphism invariance of")
print("  S_m ALONE (delta g = 2 nabla_(mu xi_nu), matter on shell) gives")
print("  nabla_mu T^{mu nu} = 0 WITHOUT using the gravity equations; for dust,")
print("  nabla.(rho u u) = 0 => u^mu nabla_mu u^nu = 0: geodesics; universal")
print("  coupling to the single metric g => WEP for test bodies.  [DERIVED]")
print("  The foliation affects matter ONLY through the g it helps shape:")
print("  preferred-frame effects for SELF-GRAVITATING bodies (SEP violation,")
print("  PPN alpha_1/alpha_2 type) and any loop-induced matter-sector Lorentz")
print("  violation are separate, NOT tree-level fifth forces.  [pointer]")

# ----------------------------------------------------------------------------
# [14.7] perturbations pointer: alpha_eff = 2 + eta_K around X = 0
# ----------------------------------------------------------------------------
xi = sp.Symbol('xi', positive=True)                 # xi = |a_i| (accel. norm)
quad = eta*xi**2 - 2*a0**2*Ffull.subs(Xs, xi**2/a0**2)
qser = sp.series(quad, xi, 0, 4).removeO().expand()
check("[14.7] quadratic a.a coefficient around X=0 is (eta_K + 2): alpha_eff = 2 + eta_K,"
      "  i.e. 2 - alpha_eff = -eta_K exactly",
      sp.simplify(qser.coeff(xi, 2) - (eta + 2)) == 0)
check("[14.7] next term is the non-analytic -(4/3)|a|^3/a0 (the MOND cubic)",
      sp.simplify(qser.coeff(xi, 3) + sp.Rational(4, 3)/a0) == 0)
print("NOTE [14.7]: in khronometric language the X=0 (cosmological) branch sits")
print("  AT the alpha = 2 boundary up to eta_K. The khronometric scalar's sound")
print("  speed is proportional to (2 - alpha) x (lam - 1)-type factors")
print("  [IMPORTED structure: Blas-Pujolas-Sibiryakov 2010], so here")
print("  c_s^2 = O(eta_K, lam_K - 1) ~ 0: the khronon scalar is the natural")
print("  dust-like growth carrier (cf. Blanchet-Skordis khronon-dust). This is")
print("  the SAME F_X(0) = -1 that makes mu(0) = 0: the MOND limit and the")
print("  DM-like cosmological scalar are one property of F.  NOT derived here:")
print("  the amplitude (why Omega_dm?), adiabatic initial conditions, and the")
print("  SIGN of c_s^2 (eta_K < 0 vs > 0: growth vs gradient instability).")
print("  Those belong to the full perturbation section.  [UNRESOLVED]")

n_fail = results.count(False)
print(f"\n{results.count(True)}/{len(results)} checks passed, {n_fail} failed.")
sys.exit(1 if n_fail else 0)
