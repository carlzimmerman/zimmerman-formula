"""t05: the Weyl action on the de Sitter instanton S^4(L): where 32 pi^2 appears and why it is scale-free.

Pure Weyl gravity has S_W = alpha_g * Integral C^2.  On S^4(L) (conformally flat) C^2 = 0, so S_W = 0 for every L.  The identity
     C^2 = E4 + 2 (Ric^2 - R^2/3)          (E4 = Riem^2 - 4 Ric^2 + R^2 the Euler density)
splits this zero into  0 = 64 pi^2 (Euler, chi = 2)  +  2 (-32 pi^2).  So the puzzle's number 32 pi^2 does occur, as  Integral (R^2/3 - Ric^2) dV = 32 pi^2  on S^4,
but it is L-independent (dimensionless action density in a scale-free theory): it cannot relate the acceleration scale to the curvature scale.
Controls: the same integrals on S^2 x S^2 (Nariai) give E4-integral 128 pi^2 and a NONZERO Weyl^2 integral (so the vanishing on S^4 is not automatic).
"""
import sys
import sympy as sp
sys.path.insert(0, '.')
from wg_tools import Geo

ok = []


def chk(name, cond):
    ok.append(bool(cond))
    print(("PASS " if cond else "FAIL ") + name)


L = sp.symbols('L', positive=True)
chi, th, ps, ph = sp.symbols('chi theta psi phi', positive=True)
gd = [L**2, L**2 * sp.sin(chi)**2, L**2 * sp.sin(chi)**2 * sp.sin(th)**2, L**2 * sp.sin(chi)**2 * sp.sin(th)**2 * sp.sin(ps)**2]
S4 = Geo((chi, th, ps, ph), gd)
sqrtg = L**4 * sp.sin(chi)**3 * sp.sin(th)**2 * sp.sin(ps)


def scalars(geo):
    n, gi = 4, geo.gi
    Riem2 = 0
    for a, b, c, d in [(a, b, c, d) for a in range(n) for b in range(n) for c in range(n) for d in range(n)]:
        v = geo.Rl[(a, b, c, d)]
        if v != 0:
            Riem2 += gi[a, a] * gi[b, b] * gi[c, c] * gi[d, d] * v**2
    Ric2 = sum(gi[a, a] * gi[b, b] * geo.Ric[a, b]**2 for a in range(n) for b in range(n))
    R = geo.R
    W2 = geo.weyl_squared()
    return sp.simplify(Riem2), sp.simplify(Ric2), sp.simplify(R), sp.simplify(W2)


Riem2, Ric2, R, W2 = scalars(S4)
E4 = sp.simplify(Riem2 - 4 * Ric2 + R**2)
print("   S^4(L): Riem^2 = %s, Ric^2 = %s, R = %s, Weyl^2 = %s, E4 = %s" % (Riem2, Ric2, R, W2, E4))
vol = sp.integrate(sp.integrate(sp.integrate(sp.integrate(sqrtg, (ph, 0, 2 * sp.pi)), (ps, 0, sp.pi)), (th, 0, sp.pi)), (chi, 0, sp.pi))
chk("A1 Vol(S^4(L)) = 8 pi^2 L^4/3", sp.simplify(vol - 8 * sp.pi**2 * L**4 / 3) == 0)
chk("A2 Weyl^2 = 0 on S^4(L): the pure-Weyl action vanishes for every L", W2 == 0)
intE4 = sp.simplify(E4 * vol)
chk("A3 Integral E4 dV = 64 pi^2 (chi = 2), independent of L", sp.simplify(intE4 - 64 * sp.pi**2) == 0)
intX = sp.simplify((R**2 / 3 - Ric2) * vol)
chk("A4 Integral (R^2/3 - Ric^2) dV = 32 pi^2, independent of L  (the puzzle's number, as a scale-free density integral)", sp.simplify(intX - 32 * sp.pi**2) == 0)
chk("A5 identity C^2 = E4 + 2(Ric^2 - R^2/3) holds pointwise on S^4: 0 = 64 pi^2 - 2 (32 pi^2)", sp.simplify(W2 - (E4 + 2 * (Ric2 - R**2 / 3))) == 0)
chk("A6 CONTROL: a scale-dependent alternative, Integral R dV = 32 pi^2 L^2, DOES depend on L",
    sp.simplify(sp.simplify(R * vol) - 32 * sp.pi**2 * L**2) == 0 and sp.simplify(sp.diff(sp.simplify(R * vol), L)) != 0)
# control: Nariai S^2 x S^2 (radii^2 = 1/Lam each; here both radius a): E4 integral 128 pi^2, Weyl^2 integral non-zero
a = sp.symbols('a', positive=True)
t1, t2, p1, p2 = sp.symbols('t1 t2 p1 p2', positive=True)
N = Geo((t1, p1, t2, p2), [a**2, a**2 * sp.sin(t1)**2, a**2, a**2 * sp.sin(t2)**2])
Riem2n, Ric2n, Rn, W2n = scalars(N)
E4n = sp.simplify(Riem2n - 4 * Ric2n + Rn**2)
voln = (4 * sp.pi * a**2)**2
chk("B1 CONTROL Nariai S^2 x S^2: Integral E4 = 128 pi^2 (chi = 4), independent of a", sp.simplify(E4n * voln - 128 * sp.pi**2) == 0)
chk("B2 CONTROL Nariai: Weyl^2 != 0 (so the vanishing on S^4 is a property of S^4, not a bug)", W2n != 0)
intWn = sp.simplify(W2n * voln)
chk("B3 CONTROL Nariai: Integral Weyl^2 is also a pure number (scale-free): %s" % intWn, sp.simplify(sp.diff(intWn, a)) == 0)
print("\nPASS %d / %d" % (sum(ok), len(ok)))
sys.exit(0 if all(ok) else 1)
