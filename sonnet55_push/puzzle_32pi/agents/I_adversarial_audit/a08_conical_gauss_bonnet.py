#!/usr/bin/env python3
"""a08_conical_gauss_bonnet.py -- scope test of README section 2 ('Gauss-Bonnet cannot fix a scale').

p01 shows Int E4 = 32 pi^2 chi for SMOOTH Euclidean dS, Schwarzschild and Nariai.  The README generalises to 'a topological invariant is scale-free, so no GB reason can exist'.
The two-horizon Euclidean Schwarzschild-de Sitter geometry is smooth at BOTH horizons only in the Nariai limit; for M < M_N one horizon has a conical deficit, and the
smooth-part Gauss-Bonnet integral then depends on the RATIO kappa_c/kappa_b (a scale ratio).  That is the one place where a curvature integral does relate the two surface gravities.
Whether this can produce 32 pi/3 is a separate question; here we only test the README's scope statement.

Checks (L = 1):
 C1  E4 of SdS = 24/L^4 + 48 M^2/r^6 (Einstein space: Riem^2 = 24/L^4 + 48M^2/r^6, Ric^2 = 36/L^4, R = 12/L^2)  -- verified by direct sympy curvature computation
 C2  Int E4 (smooth part) over the Euclidean section r_b < r < r_c with period beta = 2 pi/kappa_b (regular at r_b): NOT constant in M/L (varies between limits)
 C3  the conical formula  Int E4 = 32 pi^2 chi - 16 pi delta chi(S^2) = 64 pi^2 (1 + kappa_c/kappa_b)   (deficit 2 pi - beta kappa_c at the S^2 horizon with chi = 2) reproduces C2: the GB integral of the smooth part measures kappa_c/kappa_b
 C4  in the Nariai limit kappa_c = kappa_b and the constant 128 pi^2 (= 32 pi^2 * 4, S^2 x S^2) is recovered (controls p01 G3)
Exit 0 = all checks held (they show the topological-invariance argument is scoped to smooth geometries).
"""
import sys
import mpmath as mp
import sympy as sp

mp.mp.dps = 30
ok = []
def chk(name, cond):
    ok.append(bool(cond)); print(("PASS " if cond else "FAIL ") + name)

# ---------------------------------------------------------------- C1 curvature of SdS (independent, direct)
t, r, th, ph = sp.symbols('t r theta phi', real=True)
M, L = sp.symbols('M L', positive=True)
f = 1 - 2 * M / r - r**2 / L**2
g = sp.diag(f, 1 / f, r**2, r**2 * sp.sin(th)**2)
x = [t, r, th, ph]
ginv = g.inv()
Gam = [[[sum(ginv[i, l] * (sp.diff(g[l, j], x[k]) + sp.diff(g[l, k], x[j]) - sp.diff(g[j, k], x[l])) for l in range(4)) / 2 for k in range(4)] for j in range(4)] for i in range(4)]
def Riem(i, j, k, l):
    return sp.simplify(sp.diff(Gam[i][j][l], x[k]) - sp.diff(Gam[i][j][k], x[l]) + sum(Gam[i][k][m] * Gam[m][j][l] - Gam[i][l][m] * Gam[m][j][k] for m in range(4)))
R4 = [[[[Riem(i, j, k, l) for l in range(4)] for k in range(4)] for j in range(4)] for i in range(4)]
Ric = sp.Matrix(4, 4, lambda j, l: sp.simplify(sum(R4[i][j][i][l] for i in range(4))))
Rs = sp.simplify(sum(ginv[j, l] * Ric[j, l] for j in range(4) for l in range(4)))
Rl = [[[[sum(g[i, m] * R4[m][j][k][l] for m in range(4)) for l in range(4)] for k in range(4)] for j in range(4)] for i in range(4)]
riem2 = sp.simplify(sum(ginv[i, i] * ginv[j, j] * ginv[k, k] * ginv[l, l] * Rl[i][j][k][l]**2 for i in range(4) for j in range(4) for k in range(4) for l in range(4)))
ric2 = sp.simplify(sum(ginv[i, i] * ginv[j, j] * Ric[i, j]**2 for i in range(4) for j in range(4)))
E4 = sp.simplify(riem2 - 4 * ric2 + Rs**2)
chk("C1 E4(SdS) = 24/L^4 + 48 M^2/r^6 (direct Riemann computation)", sp.simplify(E4 - (24 / L**4 + 48 * M**2 / r**6)) == 0)

# ---------------------------------------------------------------- C2/C3 numerics (L = 1)
def horizons(Mv):
    rts = sorted([mp.re(z) for z in mp.polyroots([1, 0, -1, 2 * Mv], maxsteps=300, extraprec=100) if mp.re(z) > 0])
    return rts[0], rts[1]
def kap(rr, Mv):
    return abs(2 * Mv / rr**2 - 2 * rr) / 2
MN = 1 / (3 * mp.sqrt(3))
def gb_smooth(Mv, beta):
    rb, rc = horizons(Mv)
    return 4 * mp.pi * beta * (8 * (rc**3 - rb**3) + 16 * Mv**2 * (1 / rb**3 - 1 / rc**3))
vals = []
maxdev = 0
print("   M/M_N   kappa_c/kappa_b   Int E4 (beta = 2pi/kappa_b) / pi^2   conical formula / pi^2")
for fr in ['0.02', '0.2', '0.5', '0.8', '0.95', '0.999']:
    Mv = MN * mp.mpf(fr)
    rb, rc = horizons(Mv)
    kb, kc = kap(rb, Mv), kap(rc, Mv)
    beta = 2 * mp.pi / kb
    I = gb_smooth(Mv, beta)
    conical4 = 32 * mp.pi**2 * 4 - 16 * mp.pi * (2 * mp.pi - beta * kc) * 2      # 32 pi^2 chi(M) - 16 pi delta chi(S^2), chi(M) = 4 (S^2 x S^2 topology), delta = 2 pi - beta kappa_c
    vals.append(I)
    print("   %.3f   %.6f         %.6f                            %.6f" % (float(fr), float(kc / kb), float(I / mp.pi**2), float(conical4 / mp.pi**2)))
    maxdev = max(maxdev, abs(I - conical4))
chk("C2 Int E4 over the smooth part depends on M/L: it ranges over [%.1f, %.1f] pi^2 (not the constant 128 pi^2 of the smooth Nariai case)" % (float(min(vals) / mp.pi**2), float(max(vals) / mp.pi**2)),
    max(vals) - min(vals) > 10 * mp.pi**2)
chk("C3 the conical Gauss-Bonnet formula Int E4 = 32 pi^2 chi(M) - 16 pi (2 pi - beta kappa_c) chi(S^2) = 64 pi^2 (1 + kappa_c/kappa_b) with chi(M) = 4 reproduces the numbers (max |diff| = %.2e): the smooth-part GB integral measures kappa_c/kappa_b" % float(maxdev),
    maxdev < mp.mpf('1e-15'))
# C4 Nariai limit
Mn = MN * (1 - mp.mpf('1e-8'))
rb, rc = horizons(Mn)
kb, kc = kap(rb, Mn), kap(rc, Mn)
chk("C4 Nariai limit M -> M_N: kappa_c/kappa_b -> 1 and Int E4 -> 128 pi^2 (p01 G3 recovered: the topological value is the ratio-1 point of a ratio-dependent function)",
    abs(kc / kb - 1) < 1e-3 and abs(gb_smooth(Mn, 2 * mp.pi / kb) / mp.pi**2 - 128) < 0.05)
print("\n%d/%d" % (sum(ok), len(ok)))
sys.exit(0 if all(ok) else 1)
