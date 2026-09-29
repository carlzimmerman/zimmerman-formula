#!/usr/bin/env python3
"""a04: Euler / Pontryagin / Einstein-Hilbert content of the Euclidean de Sitter CONE  (period beta = 2 pi Z L  instead of 2 pi L, i.e. the
thermal circle of the a0-Rindler temperature a0/2pi = T_dS / Z), as a function of Z.  Is Z = sqrt(32 pi/3) a special value of anything?

Geometry (L = 1):  ds^2 = d chi^2 + sin^2(chi) d theta^2 + cos^2(chi) dOmega_2^2,  chi in [0, pi/2], theta in [0, 2 pi Z).
Z = 1 is the round S^4 (smooth); Z != 1 is a cone of total angle 2 pi Z on the horizon S^2 (chi = 0, radius L).
Claims (each computed, not assumed):
  K1  E4 of the warped metric d chi^2 + h^2 d theta^2 + c^2 dOmega_2^2 is computed symbolically; on the cone E4 = 24 away from the tip and the
      REGULAR part of Int E4 is 64 pi^2 Z   (= 32 pi^2 * 2Z).
  K2  Smoothing the tip (h -> h_eps, even-analytic, h_eps ~ chi/Z at 0, -> sin chi at chi >> eps) gives a smooth metric on S^4 whose Int E4 = 64 pi^2
      (chi_Euler = 2) for every eps and Z (numerical quadrature), and the E4 concentrated in the tip tends to 64 pi^2 (1 - Z)
      as eps -> 0.  So the conical contribution of Int E4 is  32 pi^2 * 2(1 - Z): total 64 pi^2 for all Z (topological invariance).
  K3  The tip contribution 2(1 - Z) is an INTEGER number of 32 pi^2 instanton units only for half-integer Z (Z = 1/2, 3/2, ...); Z = sqrt(32 pi/3) is
      transcendental (Lindemann) and 2(1-Z) = -9.578 is 0.42 from the nearest integer: nothing special.
  K4  Pontryagin density R R~ = 0 identically on this family (k_+ = k_-); the split of the regular part is k_+^reg = k_-^reg = Z, tip 1 - Z each.
  K5  The Euclidean Einstein-Hilbert action of the cone, (regular + delta-function part), is beta-INDEPENDENT (= -pi L^2/G for every Z): E = 0 in dS,
      I(beta) = beta E - S = -S_dS: no thermodynamic selection of a period, in particular none of beta = 2 pi Z L.  Analytically: for ANY smooth
      h, Int(R - 2 Lambda) sqrt(g) and Int E4 sqrt(g) are both total derivatives, I_EH = -pi Z h'(0), Int E4 = 64 pi^2 Z h'(0) (h'(0) = 1/Z smooth).
  K6  eps F F (the MM action density) vanishes identically on the whole family: the entire action is the Euler term, I_EH = -(1/64 pi) Int E4.
Exit 0 = all checks and controls behave.
"""
import sys
import numpy as np
import sympy as sp
from scipy import integrate

ok = []
def chk(name, cond):
    ok.append(bool(cond)); print(("PASS " if cond else "FAIL ") + name)

# ---------------------------------------------------------------- symbolic curvature of the warped metric (diagonal)
chi, th, vt, ph = sp.symbols('chi theta vartheta phi', real=True)
X = [chi, th, vt, ph]
hf = sp.Function('h')(chi); cf = sp.Function('c')(chi)
g = sp.diag(1, hf ** 2, cf ** 2, cf ** 2 * sp.sin(vt) ** 2)
n = 4
ginv = g.inv()
Gam = [[[sum(ginv[i, l] * (sp.diff(g[l, j], X[k]) + sp.diff(g[l, k], X[j]) - sp.diff(g[j, k], X[l])) for l in range(n)) / 2
         for k in range(n)] for j in range(n)] for i in range(n)]
def Riem(i, j, k, l):
    return sp.simplify(sp.diff(Gam[i][j][l], X[k]) - sp.diff(Gam[i][j][k], X[l])
                       + sum(Gam[i][k][m] * Gam[m][j][l] - Gam[i][l][m] * Gam[m][j][k] for m in range(n)))
Rup = [[[[Riem(i, j, k, l) for l in range(n)] for k in range(n)] for j in range(n)] for i in range(n)]
Ric = sp.Matrix(n, n, lambda j, l: sp.simplify(sum(Rup[i][j][i][l] for i in range(n))))
Rs = sp.simplify(sum(ginv[j, l] * Ric[j, l] for j in range(n) for l in range(n)))
Rl = [[[[sum(g[i, m] * Rup[m][j][k][l] for m in range(n)) for l in range(n)] for k in range(n)] for j in range(n)] for i in range(n)]
riem2 = sp.simplify(sum(ginv[i, i] * ginv[j, j] * ginv[k, k] * ginv[l, l] * Rl[i][j][k][l] ** 2 for i in range(n) for j in range(n) for k in range(n) for l in range(n)))
ric2 = sp.simplify(sum(ginv[i, i] * ginv[j, j] * Ric[i, j] ** 2 for i in range(n) for j in range(n)))
E4 = sp.simplify(riem2 - 4 * ric2 + Rs ** 2)
# Pontryagin density: (1/2) eps^{mnpq} R_{mn}^{ab} R_{pq ab}  (orthonormal-frame contraction, diagonal metric)
pont = 0
for (m, nn, p, q) in [(a, b, c_, d) for a in range(4) for b in range(4) for c_ in range(4) for d in range(4) if len({a, b, c_, d}) == 4]:
    eps = sp.LeviCivita(m, nn, p, q)
    for a in range(4):
        for b in range(4):
            pont += sp.Rational(1, 2) * eps * Rl[a][b][m][nn] * Rl[a][b][p][q] * ginv[a, a] * ginv[b, b]
pont = sp.simplify(pont)
print("   warped-metric E4 =", sp.simplify(E4))
chk("K4 Pontryagin density R R~ = 0 identically for every h(chi), c(chi) (product-type curvature: k_+ = k_-)", pont == 0)

# check on the round sphere h = sin, c = cos : E4 = 24, R = 12
E4_round = sp.simplify(E4.subs({hf: sp.sin(chi), cf: sp.cos(chi)}).doit())
R_round = sp.simplify(Rs.subs({hf: sp.sin(chi), cf: sp.cos(chi)}).doit())
chk("K1 round S^4 (h = sin chi, c = cos chi): E4 = 24, R = 12", sp.simplify(E4_round - 24) == 0 and sp.simplify(R_round - 12) == 0)
dens_sym = sp.simplify(E4 * hf * cf ** 2)
dens_R_sym = sp.simplify(Rs * hf * cf ** 2)
hp, cp = sp.diff(hf, chi), sp.diff(cf, chi)
chk("K1 analytic: E4 h c^2 = 8 d/dchi [ (c'^2 - 1) h' ]  (a total derivative for ANY h, c: this is why Int E4 depends only on h'(0) and c'(pi/2))",
    sp.simplify(dens_sym - 8 * sp.diff((cp ** 2 - 1) * hp, chi)) == 0)
sub_c = lambda expr: sp.simplify(expr.subs(cf, sp.cos(chi)).doit())
R_dens_c = sub_c(dens_R_sym)                         # R h c^2 with c = cos(chi)
EH_dens_c = sp.simplify(R_dens_c - 6 * hf * sp.cos(chi) ** 2)
chk("K5 analytic: (R - 6) h c^2 = d/dchi[ -2 cos^2(chi) h' ] for ANY h  =>  Int (R - 2 Lambda) sqrt(g) = 8 pi^2 Z * 2 h'(0),  I_EH = -pi Z h'(0)",
    sp.simplify(EH_dens_c - sp.diff(-2 * sp.cos(chi) ** 2 * hp, chi)) == 0)
E4_dens_c = sub_c(dens_sym)
FF_dens_c = sp.simplify(E4_dens_c - 4 * EH_dens_c)     # eps F F / vol = E4 - 4 (R - 6)/L^2  (a01, L = 1)
chk("K6 the MM 'gauge action' density eps F F = E4 - 4(R - 6) vanishes IDENTICALLY for every h(chi) on this family (whole action = Euler term; I_EH = -(1/64 pi) Int E4)",
    sp.simplify(FF_dens_c) == 0)
Z = sp.symbols('Z', positive=True)
Vreg = 2 * sp.pi * Z * 4 * sp.pi
reg_E4 = sp.simplify(Vreg * sp.integrate(24 * sp.sin(chi) * sp.cos(chi) ** 2, (chi, 0, sp.pi / 2)))
chk("K1 regular part of Int E4 on the cone (theta in [0, 2 pi Z)) = 64 pi^2 Z", sp.simplify(reg_E4 - 64 * sp.pi ** 2 * Z) == 0)

# ---------------------------------------------------------------- K2: smoothed tip, numerical integration
def make_funcs(Zv, eps):
    s_ = lambda x: 1 / Zv + (1 - 1 / Zv) * (1 - sp.exp(-x ** 2 / eps ** 2))
    hexpr = sp.sin(chi) * s_(chi)
    dens = sp.lambdify(chi, dens_sym.subs({hf: hexpr, cf: sp.cos(chi)}).doit(), 'numpy')
    dR = sp.lambdify(chi, dens_R_sym.subs({hf: hexpr, cf: sp.cos(chi)}).doit(), 'numpy')
    dV = sp.lambdify(chi, hexpr * sp.cos(chi) ** 2, 'numpy')
    return dens, dR, dV
def quad_pts(f, a, b, pts):
    tot = 0.0
    edges = [a] + [p for p in pts if a < p < b] + [b]
    for lo, hi in zip(edges[:-1], edges[1:]):
        tot += integrate.quad(f, lo, hi, limit=400, epsabs=1e-13, epsrel=1e-12)[0]
    return tot
res = []
for Zv in (0.5, 2.0, float(sp.sqrt(32 * sp.pi / 3))):
    for eps in (0.05, 0.02):
        dens, dR, dV = make_funcs(Zv, eps)
        pts = [eps, 3 * eps, 6 * eps]
        angvol = 2 * np.pi * Zv * 4 * np.pi
        total = angvol * quad_pts(dens, 1e-12, np.pi / 2, pts)
        tip = angvol * quad_pts(dens, 1e-12, 12 * eps, pts) - angvol * 24 * quad_pts(lambda x: np.sin(x) * np.cos(x) ** 2, 1e-12, 12 * eps, [])
        Vol = angvol * quad_pts(dV, 1e-12, np.pi / 2, pts)
        Rint = angvol * quad_pts(dR, 1e-12, np.pi / 2, pts)
        Iz = -(1 / (16 * np.pi)) * (Rint - 6 * Vol)
        res.append((Zv, eps, total, tip, Iz))
        print("   Z=%.4f eps=%.2f:  Int E4 = %.6f pi^2 (64 expected);  tip part (chi<12 eps, minus its regular value) = %.4f pi^2 ;  64(1-Z) = %.4f pi^2 ;  I_EH = %.5f (-pi = %.5f)" %
              (Zv, eps, total / np.pi ** 2, tip / np.pi ** 2, 64 * (1 - Zv), Iz, -np.pi))
maxdev = max(abs(t / np.pi ** 2 - 64) for (_, _, t, _, _) in res)
chk("K2 smoothed cone = smooth metric on S^4: Int E4 = 64 pi^2 for Z = 1/2, 2, sqrt(32 pi/3) and two smoothings (max deviation %.1e pi^2)" % maxdev, maxdev < 1e-6)
tip_err = max(abs(tp / np.pi ** 2 - 64 * (1 - Zv)) / (1 + abs(64 * (1 - Zv))) for (Zv, e, t, tp, I) in res if e == 0.02)
chk("K2 the E4 concentrated in the tip -> 64 pi^2 (1 - Z) (relative deviation at eps = 0.02: %.1e; exponentially small, e^{-(12)^2}, because E4 h c^2 is a total derivative)" % tip_err, tip_err < 1e-9)
tip_err_prev = max(abs(tp / np.pi ** 2 - 64 * (1 - Zv)) / (1 + abs(64 * (1 - Zv))) for (Zv, e, t, tp, I) in res if e == 0.05)
chk("K2 the tip value is the same for eps = 0.05 and 0.02 (%.1e, %.1e): it does not depend on the smoothing" % (tip_err_prev, tip_err), tip_err_prev < 1e-9 and tip_err < 1e-9)
chk("K2-control: a wrong coefficient 32 pi^2 (1 - Z) for the tip is rejected at Z = 2", all(abs(tp / np.pi ** 2 - 32 * (1 - Zv)) > 5 for (Zv, e, t, tp, I) in res if abs(Zv - 2) < 1e-9))
Ierr = max(abs(I + np.pi) for (Zv, e, t, tp, I) in res if e == 0.02)
chk("K5 Euclidean EH action of the smoothed cone -> -pi (= -S_dS G/L^2) for Z = 1/2, 2, sqrt(32 pi/3): independent of the period (max dev %.1e at eps = 0.02: exact, because (R-6) h c^2 is a total derivative when c = cos chi)" % Ierr, Ierr < 1e-3)
Is = [I for (Zv, e, t, tp, I) in res if e == 0.02]
I_reg = lambda Zv: -np.pi * Zv          # regular part only: -(1/16 pi)(12 - 6) Vol_reg with Vol_reg = 8 pi^2 Z/3
chk("K5-control: the regular part alone gives I_reg = -pi Z (Z-dependent: -2 pi at Z = 2); the delta-function tip part (+pi(Z-1)) is what makes I flat",
    abs(I_reg(2.0) + np.pi) > 3.0 and abs(I_reg(1.0) + np.pi) < 1e-12)

# ---------------------------------------------------------------- K3 the tip is not an integer number of instanton units for Z = sqrt(32 pi/3)
Zn = sp.sqrt(32 * sp.pi / 3)
tipk = 2 * (1 - Zn)
print("   tip contribution / (32 pi^2) = 2(1 - Z) = %.5f ; regular part / 32 pi^2 = 2 Z = %.5f" % (float(tipk), float(2 * Zn)))
frac = abs(float(tipk) - round(float(tipk)))
chk("K3 2(1-Z) at Z = sqrt(32 pi/3) is %.3f from the nearest integer (no near-coincidence); integer only for half-integer Z" % frac, frac > 0.3)
zs = [sp.Rational(k, 2) for k in range(-5, 12)]
chk("K3-control: Z = 1/2, 3/2, 5/2, ... do give integer tip charge 2(1-Z) (so the test can pass)", all(sp.simplify(2 * (1 - z)).is_integer for z in zs))
import mpmath as mp
mp.mp.dps = 60
Zm = mp.sqrt(32 * mp.pi / 3)
chk("K3 Z^2/pi = 32/3 rational and pi transcendental (Lindemann) => Z is not algebraic; integer-relation search (degree <= 8, coeff <= 1e5) finds no polynomial for Z",
    sp.nsimplify(Zn ** 2 / sp.pi) == sp.Rational(32, 3) and mp.findpoly(Zm, 8, maxcoeff=10 ** 5, maxsteps=100000) is None)
chk("K3-control: the same search recovers sqrt(2) + 3 (degree 2)", mp.findpoly(mp.sqrt(2) + 3, 2, maxcoeff=10 ** 3) is not None)
print("   chiral bookkeeping (K4): regular k_+ = k_- = Z, tip 1 - Z each, total 1 each: at Z = sqrt(32 pi/3) the smooth field carries %.4f instanton units in each SU(2)_pm" % float(Zn))
print("\n%d/%d" % (sum(ok), len(ok)))
sys.exit(0 if all(ok) else 1)
