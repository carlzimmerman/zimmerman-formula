#!/usr/bin/env python3
"""x1_05_noether_euler_static_patch.py -- lane X1 task (3): the MacDowell-Mansouri / Euler / Iyer-Wald link.
Question: is the puzzle's Rindler-horizon condition  A Lambda = 32 pi^2  (a0-surface at r = 1/(2 a0) = Z L/2, Z^2 = 32 pi/3)  equivalent to
  (a) 'Euler coefficient x A'   or   (b) 'Noether charge of the de Sitter static-patch Killing vector through the a0-surface = one natural unit'
without inserting a0?  Variable held fixed throughout: L (i.e. Lambda = 3/L^2);  a0 enters only through the evaluation radius r = Z L/2.

Parts
  P1  Euclidean dS action = c_E x 32 pi^2 x chi with c_E = L^2/(64 pi G), chi = 2  (= S_dS = pi L^2/G)                      [verified]
  P2  Iyer-Wald charge Q(r) of xi = d_t through the sphere r in dS, r < L and r > L:  Q = -r^3/(2 G L^2);  S(r) = 2 pi Q/kappa_xi = -pi r^3/(G L)
      compare: area law S_A(r) = pi r^2/G ;  Euclidean EH action of the ball ; Euler charge inside r:   ALL Noether/volume-type quantities scale as r^3, the area as r^2
  P3  general r-law and the pi-content at r = Z L/2:  a quantity ~ r^n has pi-content pi^(n/2): an integer power of pi only for even n  (exact statement)
  P4  'one unit' solutions: r_u/L = (2u)^(1/3);  the unit needed at r = Z L/2 is Z^3/16 (not rational x pi^k)
  P5  the Euler-term (alpha E4) deformation: E_GB^{abcd} = 2R^{abcd} - 2(...) + R(...) verified by finite differences; on dS E_GB = 2k(gg-gg);
      Q_alpha(r) = (1 + 4 alpha/L^2) Q_EH(r) ;  Wald/JM entropy at the dS horizon S = A/4G + 4 pi alpha/G ;  MM (alpha = -L^2/4)  => Q_MM = 0 for every r
      and the GB tensor vanishes identically in D = 4, so alpha changes NO equation of motion (control: D = 5 it does)
  P6  the ratio  S_{a0}/(Euler unit) = 16 pi/3 = Z^2/2  (irrational: not an integer number of Euler units) and area-law vs Noether-law at the a0-surface
Exit 0 iff all checks and controls behave as declared.
"""
import sys, json, itertools, time
import numpy as np
import sympy as sp

ok = []
def chk(name, cond):
    ok.append(bool(cond)); print(("PASS " if cond else "FAIL ") + name, flush=True)
def ctl(name, cond_rejected):
    ok.append(bool(cond_rejected)); print(("PASS CONTROL " if cond_rejected else "FAIL CONTROL ") + name, flush=True)
T0 = time.time()
pi = sp.pi
G, L, r, alpha = sp.symbols('G L r alpha', positive=True)
alpha_s = sp.Symbol('alpha_s', real=True)
Z = sp.sqrt(32 * pi / 3)

# ---------------------------------------------------------------- P1 Euclidean action = Euler term
cE = L ** 2 / (64 * pi * G)
S4 = 8 * pi ** 2 / 3
E4_S4 = 24 / L ** 4
Euler_int = E4_S4 * S4 * L ** 4                                              # int E4 over S^4(L) = 64 pi^2
chk("P1 int_{S^4} E4 = 32 pi^2 chi with chi = 2 (=64 pi^2); c_E = L^2/(64 pi G):  c_E x 32 pi^2 x 2 = pi L^2/G = S_dS = A_dS/(4G)",
    sp.simplify(Euler_int - 64 * pi ** 2) == 0 and sp.simplify(cE * 32 * pi ** 2 * 2 - pi * L ** 2 / G) == 0 and sp.simplify(4 * pi * L ** 2 / (4 * G) - pi * L ** 2 / G) == 0)
# EH on-shell Euclidean action of the full S^4:  -(1/16 pi G) int (R - 2 Lambda) = -(1/16 pi G)(12/L^2 - 6/L^2)(8 pi^2 L^4/3) = - pi L^2/G
chk("P1 on-shell Euclidean EH action  -(1/16 pi G)(6/L^2) Vol(S^4(L)) = -pi L^2/G = -S_dS", sp.simplify(-(6 / L ** 2) / (16 * pi * G) * S4 * L ** 4 + pi * L ** 2 / G) == 0)

# ---------------------------------------------------------------- P2 Iyer-Wald charge in the dS static patch (metric-computed, r < L and r > L)
tc, thc, phc = sp.symbols('t theta phi', real=True)
def christoffel(g, ginv, X):
    n = len(X)
    return [[[sum(ginv[a, d] * (sp.diff(g[d, b], X[c]) + sp.diff(g[d, c], X[b]) - sp.diff(g[b, c], X[d])) for d in range(n)) / 2
              for c in range(n)] for b in range(n)] for a in range(n)]
fds = 1 - r ** 2 / L ** 2
Xc = (tc, r, thc, phc)
gds = sp.diag(-fds, 1 / fds, r ** 2, r ** 2 * sp.sin(thc) ** 2); gdsi = gds.inv()
Gam = christoffel(gds, gdsi, Xc)
xi_low = [gds[i, 0] for i in range(4)]
nab = sp.Matrix(4, 4, lambda m, n: sp.diff(xi_low[n], Xc[m]) - sum(Gam[l][m][n] * xi_low[l] for l in range(4)))     # nabla_m xi_n
up = sp.simplify(gdsi * nab * gdsi)                                                                                  # nabla^m xi^n
sqrtg = r ** 2 * sp.sin(thc)                                                   # |sqrt(g)|, valid for r < L and r > L (f changes sign, g_tt g_rr = -1 throughout)
Qthph = -(1 / (16 * pi * G)) * sqrtg * (up[0, 1] - up[1, 0])
Qr = sp.simplify(sp.integrate(sp.integrate(Qthph, (thc, 0, sp.pi)), (phc, 0, 2 * pi)))
chk("P2 Iyer-Wald charge of xi = d_t through S^2(r) in de Sitter: Q(r) = %s  (same analytic formula inside the static patch r < L and in the region r > L where xi is spacelike)" % Qr,
    sp.simplify(Qr + r ** 3 / (2 * G * L ** 2)) == 0)
kap_xi = sp.Rational(1, 1) / L                                                 # surface gravity of xi at the cosmological horizon r = L: |f'(L)|/2 = 1/L
chk("P2 at the horizon r = L: |Q(L)| = kappa A/(8 pi G) = L/(2G) (kappa = 1/L, A = 4 pi L^2), i.e. Q_H = T S;  S = 2 pi |Q|/kappa = pi L^2/G = S_dS = A/4G",
    sp.simplify(sp.Abs(Qr.subs(r, L)) - kap_xi * 4 * pi * L ** 2 / (8 * pi * G)) == 0 and sp.simplify(2 * pi * L * (L / (2 * G)) - pi * L ** 2 / G) == 0)
S_noether = sp.simplify(2 * pi * Qr / kap_xi)                                  # (2 pi/kappa) Q
S_area = pi * r ** 2 / G                                                       # A/4G = 4 pi r^2/(4G)
chk("P2 Noether entropy S_N(r) = 2 pi Q/kappa_xi = -pi r^3/(G L) versus area law S_A(r) = pi r^2/G: ratio |S_N|/S_A = r/L  (equal only at r = L)",
    sp.simplify(S_noether + pi * r ** 3 / (G * L)) == 0 and sp.simplify(sp.Abs(S_noether) / S_area - r / L) == 0)
# Euclidean EH action of the ball r' < r  (tau period 2 pi L)   and Euler action inside r
vol_ball = 2 * pi * L * (4 * pi / 3) * r ** 3
I_EH_ball = -(6 / L ** 2) / (16 * pi * G) * vol_ball
I_Euler_ball = cE * E4_S4 * vol_ball
chk("P2 Euclidean EH action of the ball of radius r: -pi r^3/(G L) = -S_N(r) magnitude; Euler-term action inside r: c_E E4 Vol = pi r^3/(G L): the volume-type quantities agree with the Noether entropy",
    sp.simplify(I_EH_ball + pi * r ** 3 / (G * L)) == 0 and sp.simplify(I_Euler_ball - pi * r ** 3 / (G * L)) == 0)
chk("P2 Euler number inside r: chi(r) = (1/32 pi^2) int_{ball x tau} E4 = 2 (r/L)^3 (= 2 at r = L)", sp.simplify(E4_S4 * vol_ball / (32 * pi ** 2) - 2 * (r / L) ** 3) == 0)
ctl("P2 CONTROL: the Noether entropy is NOT the area law: |S_N|/S_A = r/L != 1 at r = Z L/2", sp.simplify((Z / 2) - 1) != 0)

# ---------------------------------------------------------------- P3 pi-content at r = Z L/2:  r^n  ->  pi^(n/2)
rZ = Z * L / 2
print("\n  pi-content of a quantity  q_n = (r/L)^n  at the a0 radius r = Z L/2  (Z^2 = 32 pi/3):")
rows = []
for n in range(0, 6):
    v = sp.simplify((Z / 2) ** n)
    _, b = sp.sympify(v).as_coeff_exponent(pi)
    rows.append((n, v, b))
    print("     n = %d : (Z/2)^n = %-22s = %.4f   pi-power %s" % (n, v, float(v), b))
chk("P3 pi-power of (Z/2)^n is n/2: an integer power of pi (so possibly 'rational x pi^k') iff n is even", all(b == sp.Rational(n, 2) for n, v, b in rows) and all((b.q == 1) == (n % 2 == 0) for n, v, b in rows))
ctl("P3 CONTROL: (Z/2)^3 is not rational x pi^k for any integer k (its pi-power is 3/2)", rows[3][2] == sp.Rational(3, 2))
print("      => the area (n = 2), the horizon curvature (n = -2) and A Lambda (n = 2) can be rational x pi^k at r = Z L/2; every Noether/Komar/volume/Euler-inside-r quantity (n = 3) has pi^(3/2) or pi^(5/2): never a rational multiple of a power of pi.")

# ---------------------------------------------------------------- P4 'one unit' solutions
print("\n  P4  r/L at which each normalisation equals a candidate 'unit' u, versus the a0 radius Z/2 = %.4f:" % float(Z / 2))
G1 = sp.Symbol('G1', positive=True)
q_of = lambda x: x ** 3 / 2                                                    # G|Q|/L  as a function of x = r/L
s_of = lambda x: pi * x ** 3                                                   # G|S_N|/L^2
chi_of = lambda x: 2 * x ** 3                                                  # Euler number inside r
units = {'1': sp.Integer(1), '2 pi': 2 * pi, '4 pi': 4 * pi, '32 pi^2': 32 * pi ** 2, '2': sp.Integer(2)}
tab = []
for uname, u in units.items():
    xq = sp.simplify((2 * u) ** sp.Rational(1, 3)); xs = sp.simplify((u / pi) ** sp.Rational(1, 3)); xc = sp.simplify((u / 2) ** sp.Rational(1, 3))
    tab.append((uname, float(xq), float(xs), float(xc)))
    print("     unit %-8s : G|Q|/L = u at r/L = %.4f ;  G|S_N|/L^2 = u at r/L = %.4f ;  chi(r) = u at r/L = %.4f" % (uname, float(xq), float(xs), float(xc)))
need_q = sp.simplify(q_of(Z / 2)); need_s = sp.simplify(s_of(Z / 2)); need_c = sp.simplify(chi_of(Z / 2))
print("     at r = Z L/2 the needed 'unit' is:  G|Q|/L = Z^3/16 = %.4f ;  G|S_N|/L^2 = pi Z^3/8 = %.4f ;  chi = Z^3/4 = %.4f" % (float(need_q), float(need_s), float(need_c)))
cand_units = [sp.Integer(1), 2 * pi, 4 * pi, 32 * pi ** 2, sp.Integer(2), pi, 8 * pi, 16 * pi, 2 * pi ** 2, 8 * pi ** 2, 3 * pi]
chk("P4 none of the units {1, 2, pi, 2 pi, 4 pi, 8 pi, 16 pi, 3 pi, 2 pi^2, 8 pi^2, 32 pi^2} equals the needed Noether (%.4f), Noether-entropy (%.4f) or Euler (%.4f) value at r = Z L/2"
    % (float(need_q), float(need_s), float(need_c)),
    all(sp.simplify(need_q - u) != 0 and sp.simplify(need_s - u) != 0 and sp.simplify(need_c - u) != 0 for u in cand_units))
chk("P4 exact reason: need = rational x pi^(3/2 or 5/2), a unit rational x pi^k has integer k: (need)/(unit) = rational x sqrt(pi) is transcendental (Lindemann), never 1",
    all(sp.sympify(v).as_coeff_exponent(pi)[1].q == 2 for v in (need_q, need_s, need_c)))
ctl("P4 CONTROL: for the AREA law the a0 value 8 pi/3 IS rational x pi (n = 2): the puzzle is an even-power statement", sp.sympify(sp.simplify((Z / 2) ** 2)).as_coeff_exponent(pi)[1] == 1)

# ---------------------------------------------------------------- P5 the Euler deformation: E_GB tensor, Noether charge, entropy, EOM invariance
rng = np.random.default_rng(99)
def KN(h, k):
    return (np.einsum('ac,bd->abcd', h, k) + np.einsum('bd,ac->abcd', h, k) - np.einsum('ad,bc->abcd', h, k) - np.einsum('bc,ad->abcd', h, k))
def rand_curv(n):
    Rm = np.zeros((n,) * 4)
    for _ in range(5):
        h = rng.normal(size=(n, n)); h = h + h.T; k = rng.normal(size=(n, n)); k = k + k.T
        Rm += KN(h, k)
    return Rm
def E4t(Rm):
    Ric = np.einsum('acbc->ab', Rm); Rs = np.trace(Ric)
    return np.sum(Rm * Rm) - 4 * np.sum(Ric * Ric) + Rs ** 2
def EGB_tensor(Rm):
    n = Rm.shape[0]; d = np.eye(n)
    Ric = np.einsum('acbc->ab', Rm); Rs = np.trace(Ric)
    P = (np.einsum('ac,bd->abcd', d, Ric) - np.einsum('ad,bc->abcd', d, Ric) - np.einsum('bc,ad->abcd', d, Ric) + np.einsum('bd,ac->abcd', d, Ric))
    return 2 * Rm - 2 * P + Rs * (np.einsum('ac,bd->abcd', d, d) - np.einsum('ad,bc->abcd', d, d))
maxerr = 0.0
for n in (4, 5):
    for _ in range(30):
        Rm = rand_curv(n); dR = rand_curv(n); h = 1e-6
        num = (E4t(Rm + h * dR) - E4t(Rm - h * dR)) / (2 * h)
        ana = np.sum(EGB_tensor(Rm) * dR)
        maxerr = max(maxerr, abs(num - ana) / (1 + abs(ana)))
chk("P5 E_GB^{abcd} = dE4/dR_{abcd} = 2R^{abcd} - 2(g^{ac}R^{bd} - g^{ad}R^{bc} - g^{bc}R^{ad} + g^{bd}R^{ac}) + R (g^{ac}g^{bd} - g^{ad}g^{bc}) (finite differences, D = 4, 5, 60 tensors; max rel. error %.1e)" % maxerr, maxerr < 1e-6)
# dS: Riemann of the static patch = k (g g - g g), and E_GB on it
def riemann_lower(g, ginv, X, Gam):
    n = len(X)
    Rup = [[[[sp.diff(Gam[a][b][d], X[c]) - sp.diff(Gam[a][b][c], X[d]) + sum(Gam[a][c][e] * Gam[e][b][d] - Gam[a][d][e] * Gam[e][b][c] for e in range(n)) for d in range(n)] for c in range(n)] for b in range(n)] for a in range(n)]
    return [[[[sp.simplify(sum(g[a, e] * Rup[e][b][c][d] for e in range(n))) for d in range(n)] for c in range(n)] for b in range(n)] for a in range(n)]
Rlow = riemann_lower(gds, gdsi, Xc, Gam)
k = 1 / L ** 2
maxsym = all(sp.simplify(Rlow[a][b][c][d] - k * (gds[a, c] * gds[b, d] - gds[a, d] * gds[b, c])) == 0 for a in range(4) for b in range(4) for c in range(4) for d in range(4))
chk("P5 Riemann of the dS static patch is R_abcd = (1/L^2)(g_ac g_bd - g_ad g_bc) (all 256 components, symbolic)", maxsym)
# E_GB on dS: (D-2)(D-3) k (g g - g g) = 2k (g g - g g)  -- numeric check in an orthonormal frame with the closed-form tensor
RmDS = 1.0 * (np.einsum('ac,bd->abcd', np.eye(4), np.eye(4)) - np.einsum('ad,bc->abcd', np.eye(4), np.eye(4)))       # k = 1 (L = 1)
EGB_ds = EGB_tensor(RmDS)
gg_ds = np.einsum('ac,bd->abcd', np.eye(4), np.eye(4)) - np.einsum('ad,bc->abcd', np.eye(4), np.eye(4))
chk("P5 on a maximally symmetric D = 4 space E_GB^{abcd} = 2 k (g^{ac}g^{bd} - g^{ad}g^{bc}) = (D-2)(D-3) k G^{abcd}", np.allclose(EGB_ds, 2 * gg_ds))
# Noether charge with L = (1/16 pi G)(R - 2 Lambda + alpha E4):  E^{abcd} = (1/16 pi G)[ (1/2) + 2 alpha k ] G^{abcd};  Q ~ E^{abcd} nabla_c xi_d  => Q_alpha/Q_EH = 1 + 4 alpha k
fac = sp.simplify((sp.Rational(1, 2) + 2 * alpha_s * k) / sp.Rational(1, 2))
chk("P5 Iyer-Wald charge of the Killing vector with an Euler term: Q_alpha(r) = (1 + 4 alpha/L^2) Q_EH(r) = %s  (the factor is r-independent; the GB term adds no nabla E contribution since nabla E = 0)" % sp.simplify(fac * Qr),
    sp.simplify(fac - (1 + 4 * alpha_s / L ** 2)) == 0)
Qalpha = sp.simplify(fac * Qr)
MMalpha = -L ** 2 / 4
chk("P5 MacDowell-Mansouri / Kounterterm value alpha = -L^2/4 (from I_EH + c_E int E4 = c_E int eps F F, c_E = L^2/(64 pi G) = -alpha/(16 pi G)): Q_MM(r) = 0 for EVERY r",
    sp.simplify(Qalpha.subs(alpha_s, MMalpha)) == 0 and sp.simplify(-MMalpha / (16 * pi * G) - cE) == 0)
S_JM = sp.simplify(2 * pi * L * Qalpha.subs(r, L) * (-1))                    # S = (2 pi/kappa)|Q_alpha(L)|
chk("P5 dS horizon entropy with the Euler term: S = (2 pi/kappa) Q_alpha(L) = A/(4G) + 4 pi alpha/G  (= Jacobson-Myers A/4G + (alpha/2G) oint R_Sigma with oint R_Sigma = 8 pi); alpha = -L^2/4 gives S_MM = 0",
    sp.simplify(S_JM - (pi * L ** 2 / G + 4 * pi * alpha_s / G)) == 0 and sp.simplify(S_JM.subs(alpha_s, MMalpha)) == 0)
# EOM invariance: Lanczos/GB tensor H_ab = 2(R R_ab - 2 R_ac R^c_b - 2 R_acbd R^cd + R_acde R_b^cde) - (1/2) g_ab E4  vanishes identically for D = 4
def H_GB(Rm):
    n = Rm.shape[0]
    Ric = np.einsum('acbc->ab', Rm); Rs = np.trace(Ric)
    H = 2 * (Rs * Ric - 2 * Ric @ Ric - 2 * np.einsum('acbd,cd->ab', Rm, Ric) + np.einsum('acde,bcde->ab', Rm, Rm)) - 0.5 * np.eye(n) * E4t(Rm)
    return H
h4 = max(np.abs(H_GB(rand_curv(4))).max() for _ in range(30))
h5 = min(np.abs(H_GB(rand_curv(5))).max() for _ in range(30))
chk("P5 the Gauss-Bonnet field-equation tensor vanishes identically in D = 4 (max |H| over 30 random curvature tensors = %.1e) so alpha changes NO classical equation" % h4, h4 < 1e-9)
ctl("P5 CONTROL: in D = 5 the same tensor does not vanish (min over 30 tensors of max |H| = %.2f): the test can fail" % h5, h5 > 1e-3)
print("      => an absolute Noether-charge (or entropy) condition 'Q(r_a0) = unit' is alpha-dependent, but a0 = (1/2) sqrt(G rho) is an equation-of-motion statement and cannot depend on alpha: such a condition cannot be the origin of the relation.")

# ---------------------------------------------------------------- P6 the a0 surface in Euler units; the 'natural' Noether units
S_a0 = sp.simplify(pi * (Z * L / 2) ** 2 / G)                                  # A/4G = pi r^2/G at r = Z L/2
euler_unit = cE * 32 * pi ** 2                                                  # c_E x 32 pi^2 (one instanton unit) = S_dS/2
chk("P6 S_{a0}/S_dS = 8 pi/3 and S_{a0}/(Euler unit c_E 32 pi^2) = 16 pi/3 = Z^2/2: irrational, not an integer number of Euler/instanton units",
    sp.simplify(S_a0 / (pi * L ** 2 / G) - 8 * pi / 3) == 0 and sp.simplify(S_a0 / euler_unit - 16 * pi / 3) == 0 and sp.simplify(S_a0 / euler_unit - Z ** 2 / 2) == 0)
chk("P6 the equivalence 'A Lambda = 32 pi^2  <=>  S_{a0} = (16 pi/3) x (Euler unit)' is an exact rewriting (G- and L-free), it carries no information beyond A Lambda = 32 pi^2",
    sp.simplify((S_a0 / euler_unit) * 3 / (16 * pi) - 1) == 0)
Sn_a0 = sp.simplify(sp.Abs(S_noether).subs(r, Z * L / 2))
chk("P6 Noether entropy at the a0 radius = (Z/2)^3 S_dS = %.3f S_dS (versus area law 8 pi/3 = %.3f S_dS): three normalisations of S_dS agree at r = L and disagree at r = Z L/2"
    % (float(sp.simplify(Sn_a0 / (pi * L ** 2 / G))), float(8 * pi / 3)), sp.simplify(Sn_a0 / (pi * L ** 2 / G) - (Z / 2) ** 3) == 0 and abs(float((Z / 2) ** 3) - float(8 * pi / 3)) > 1)

print("\n%d/%d checks and controls behave as declared  (%.1f s)" % (sum(ok), len(ok), time.time() - T0))
sys.exit(0 if all(ok) else 1)
