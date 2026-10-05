"""EXT04 check: independent re-derivation of the external 'two-potential flat-rotation trace solution' note (2026-10-05; zip sha256 0493dfc3..., not vendored).
Metric ds^2 = -(r/r0)^(2p) dt^2 + dr^2/F + r^2 dOmega^2 (constant F). Own sympy Riemann tensor (not the package's code).
Run: python3 ext04_check.py  |  MUTATE=1: q = (2/3)(1 - p) instead of (2/3)(1 - p^2) (check T must fail)
"""
import os, sys
import sympy as sp
MUTATE = os.environ.get("MUTATE") == "1"
res = []
def check(n, ok): res.append(bool(ok)); print(("PASS  " if ok else "FAIL  ") + n)
t, r, th, ph = sp.symbols("t r theta phi", positive=True); p, F, r0 = sp.symbols("p F r0", positive=True)
X = [t, r, th, ph]
g = sp.diag(-(r / r0)**(2 * p), 1 / F, r**2, r**2 * sp.sin(th)**2); gi = g.inv()
Gam = [[[sp.simplify(sum(gi[a, d] * (sp.diff(g[d, b], X[c]) + sp.diff(g[d, c], X[b]) - sp.diff(g[b, c], X[d])) for d in range(4)) / 2)
         for c in range(4)] for b in range(4)] for a in range(4)]
def Rie(a, b, c, d):  # R^a_{bcd}
    return sp.simplify(sp.diff(Gam[a][b][d], X[c]) - sp.diff(Gam[a][b][c], X[d]) + sum(Gam[a][c][e] * Gam[e][b][d] - Gam[a][d][e] * Gam[e][b][c] for e in range(4)))
R4 = [[[[Rie(a, b, c, d) for d in range(4)] for c in range(4)] for b in range(4)] for a in range(4)]
Rl = [[[[sp.simplify(sum(g[a, e] * R4[e][b][c][d] for e in range(4))) for d in range(4)] for c in range(4)] for b in range(4)] for a in range(4)]
Ric = sp.Matrix(4, 4, lambda b, d: sp.simplify(sum(R4[a][b][a][d] for a in range(4))))
Rs = sp.simplify(sum(gi[i, j] * Ric[i, j] for i in range(4) for j in range(4)))
# invariants (diagonal metric: raise with gi diag)
Riem2 = sp.simplify(sum(Rl[a][b][c][d]**2 * gi[a, a] * gi[b, b] * gi[c, c] * gi[d, d] for a in range(4) for b in range(4) for c in range(4) for d in range(4)))
Ric2 = sp.simplify(sum(Ric[a, b]**2 * gi[a, a] * gi[b, b] for a in range(4) for b in range(4)))
E4 = sp.simplify(Riem2 - 4 * Ric2 + Rs**2); C2 = sp.simplify(Riem2 - 2 * Ric2 + Rs**2 / 3)
check("R  = 2[1 - F(1+p+p^2)]/r^2", sp.simplify(Rs - 2 * (1 - F * (1 + p + p**2)) / r**2) == 0)
check("E4 = 8Fp(1-p)(1-F)/r^4", sp.simplify(E4 - 8 * F * p * (1 - p) * (1 - F) / r**4) == 0)
check("C^2 = (4/3)[F(p-1)^2 - 1]^2/r^4", sp.simplify(C2 - sp.Rational(4, 3) * (F * (p - 1)**2 - 1)**2 / r**4) == 0)
F0 = 1 / (1 + p + p**2)
q = sp.Rational(2, 3) * ((1 - p) if MUTATE else (1 - p**2))
check("T scalar-flat F0 = 1/(1+p+p^2) satisfies the trace equation iff c_E/a_E = (2/3)(1 - p^2)", sp.simplify((E4 - q * C2).subs(F, F0)) == 0 and sp.simplify(Rs.subs(F, F0)) == 0)
vc2 = sp.simplify(r * sp.diff(-g[0, 0], r) / (2 * (-g[0, 0])))
check("flat circular speed v_c^2 = p (independent of r)", sp.simplify(vc2 - p) == 0)
# Einstein tensor -> stress (8 pi G T) at F0
Gmn = sp.simplify(Ric - Rs * g / 2)
rho = sp.simplify((-Gmn[0, 0] * gi[0, 0]).subs(F, F0)); pr = sp.simplify((Gmn[1, 1] * gi[1, 1]).subs(F, F0)); pt = sp.simplify((Gmn[2, 2] * gi[2, 2]).subs(F, F0))
D = 1 + p + p**2
check("8 pi G (rho, p_r, p_t) = (p(1+p), p(1-p), p^2)/(D r^2), traceless", sp.simplify(rho - p * (1 + p) / (D * r**2)) == 0 and sp.simplify(pr - p * (1 - p) / (D * r**2)) == 0
      and sp.simplify(pt - p**2 / (D * r**2)) == 0 and sp.simplify(-rho + pr + 2 * pt) == 0)
# the decisive physics point: v_c^4 = p^2 = 1 - (3/2) q is fixed by the QFT ratio, independent of baryonic mass -> no BTFR (v^4 = G M a0)
qs = sp.symbols("q", positive=True)
check("v_c^4 = 1 - (3/2) q: one fixed speed per quantum theory, no baryonic-mass dependence (no v^4 = G M a0)", sp.simplify(sp.solve(sp.Eq(q.subs(p, sp.sqrt(sp.Symbol('P', positive=True))), qs), sp.Symbol('P', positive=True))[0] - (1 - sp.Rational(3, 2) * qs)) == 0 if not MUTATE else False)
# Hofman et al. bound 18/31 <= q <= 3 -> p <= 2/sqrt(31)
pmax = sp.solve(sp.Eq(sp.Rational(2, 3) * (1 - p**2), sp.Rational(18, 31)), p)
check(f"with 18/31 <= q the branch needs p <= {pmax} = 2/sqrt(31) = {float(2/sp.sqrt(31)):.3f}, i.e. v_c <= {float(sp.sqrt(2/sp.sqrt(31))):.3f} c (galaxies have v ~ 1e-3 c)", pmax == [2 / sp.sqrt(31)])
print(f"\n{sum(res)}/{len(res)} pass" + ("  (MUTATE)" if MUTATE else ""))
sys.exit(0 if all(res) else 1)
