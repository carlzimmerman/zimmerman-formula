#!/usr/bin/env python3
"""ROOT note, addendum A1: (1) the symmetry behind alpha = 2, (2) the deep-MOND term in the invariant variables,
(3) the locality bound for any sector gapped by the clock's acceleration.

(1) In D space dimensions, with a_i = d_i ln N and ghat_ij = N^(2/(D-2)) g_ij,
        N sqrt(g) ( R[g] + eta a.a )  =  sqrt(ghat) R[ghat]  +  d_i( c_D sqrt(ghat) ghat^ij d_j ln N )
    exactly when eta = (D-1)/(D-2), with c_D = 2(D-1)/(D-2).  D = 3: eta = 2, ghat = N^2 g, c_3 = 4.
    So at alpha = 2 the static sector of khronometric gravity is 3-d Einstein gravity of ghat alone: ln N drops out
    (a local Weyl symmetry g -> e^(2w) g, N -> e^(-w) N).
(2) N sqrt(g) |a|_g^3 = 27 sqrt(ghat) |d psi|_ghat^3 with psi = N^(1/3).
(3) Numbers: Rindler length c^2/a0, time c/a0, and c^2/v_f^2 for the 6e10 Msun point mass, both footings.

Exact rational arithmetic at rational points (the functions are polynomials / exponentials of polynomials).
`--mutate` shifts eta by 1/10: (1) must fail.  A note, not a graded lane.
Adopts nothing. kappa = 1/2 FITTED; not theory closed.
"""
import sys

import sympy as sp

MUT = "--mutate" in sys.argv
out = []


def say(s=""):
    out.append(s)
    print(s, flush=True)


def ricci_scalar(g, X):
    n = len(X)
    gi = g.inv()
    Gam = [[[sum(gi[a, d] * (sp.diff(g[d, b], X[c]) + sp.diff(g[d, c], X[b]) - sp.diff(g[b, c], X[d]))
                 for d in range(n)) / 2 for c in range(n)] for b in range(n)] for a in range(n)]
    R = 0
    for b in range(n):
        for c in range(n):
            ric = 0
            for a in range(n):
                ric += sp.diff(Gam[a][b][c], X[a]) - sp.diff(Gam[a][b][a], X[c])
                for d in range(n):
                    ric += Gam[a][a][d] * Gam[d][b][c] - Gam[a][c][d] * Gam[d][b][a]
            R += gi[b, c] * ric
    return R


def check(D, g, lnN, X, pts, eta):
    N = sp.exp(lnN)
    a = [sp.diff(lnN, x) for x in X]
    gi = g.inv()
    aa = sum(gi[i, j] * a[i] * a[j] for i in range(D) for j in range(D))
    L1 = N * sp.sqrt(g.det()) * (ricci_scalar(g, X) + eta * aa)
    gh = N ** sp.Rational(2, D - 2) * g
    ghi = gh.inv()
    sq = sp.sqrt(gh.det())
    cD = sp.Rational(2 * (D - 1), D - 2)
    td = sum(sp.diff(cD * sq * ghi[i, j] * a[j], X[i]) for i in range(D) for j in range(D))
    resid = L1 - sq * ricci_scalar(gh, X) - td
    vals = []
    for p in pts:
        v = sp.nsimplify(sp.simplify(resid.subs(dict(zip(X, p)))))
        vals.append(v)
    return vals, L1


x, y, z, w = sp.symbols("x y z w", real=True)
R = sp.Rational

# D = 3, non-diagonal polynomial metric (positive definite near the points), generic ln N
X3 = [x, y, z]
g3 = sp.Matrix([[2 + x * y + z**2, R(1, 5) * x * z, R(1, 7) * y],
                [R(1, 5) * x * z, 3 + y**2 + R(1, 3) * x, R(1, 6) * z * y],
                [R(1, 7) * y, R(1, 6) * z * y, 2 + x**2 * z + y]])
lnN3 = R(1, 3) * x - R(1, 4) * y * z + R(1, 5) * x**2 + R(1, 7) * z**3
pts3 = [(R(1, 3), R(1, 5), R(2, 7)), (R(-1, 4), R(1, 2), R(1, 9)), (R(2, 5), R(-1, 3), R(1, 4))]
eta3 = sp.Integer(2) + (R(1, 10) if MUT else 0)
v3, _ = check(3, g3, lnN3, X3, pts3, eta3)
ok3 = all(v == 0 for v in v3)
say(f"(1) D = 3, eta = {eta3}, non-diagonal metric, 3 rational points: residuals {[str(v)[:24] for v in v3]} -> "
    f"{'IDENTITY HOLDS' if ok3 else 'FAILS'}")

# D = 4, diagonal polynomial metric, eta = 3/2
X4 = [x, y, z, w]
g4 = sp.diag(2 + x * y, 3 + z**2 + w, 2 + y * w + x**2, 4 + x * z)
lnN4 = R(1, 3) * x * w - R(1, 4) * y + R(1, 6) * z**2 + R(1, 5) * w**2 * y
pts4 = [(R(1, 3), R(1, 5), R(2, 7), R(1, 4)), (R(-1, 4), R(1, 2), R(1, 9), R(1, 3))]
eta4 = R(3, 2) + (R(1, 10) if MUT else 0)
v4, _ = check(4, g4, lnN4, X4, pts4, eta4)
ok4 = all(v == 0 for v in v4)
say(f"(1) D = 4, eta = {eta4}, diagonal metric, 2 rational points: residuals {[str(v)[:24] for v in v4]} -> "
    f"{'IDENTITY HOLDS' if ok4 else 'FAILS'}")
say("    general D (by hand, checked above at D = 3, 4): eta = (D-1)/(D-2), ghat = N^(2/(D-2)) g, "
    "N -> e^((2-D) w) N under g -> e^(2w) g")

# (2) the cubic in invariant variables, D = 3
N = sp.exp(lnN3)
gi = g3.inv()
a = [sp.diff(lnN3, v) for v in X3]
lhs = N * sp.sqrt(g3.det()) * sp.sqrt(sum(gi[i, j] * a[i] * a[j] for i in range(3) for j in range(3))) ** 3
gh = N**2 * g3
ghi = gh.inv()
psi = N ** R(1, 3)
dps = [sp.diff(psi, v) for v in X3]
rhs = 27 * sp.sqrt(gh.det()) * sp.sqrt(sum(ghi[i, j] * dps[i] * dps[j] for i in range(3) for j in range(3))) ** 3
r2 = [sp.nsimplify(sp.simplify((lhs - rhs).subs(dict(zip(X3, p))))) for p in pts3]
say(f"(2) N sqrt(g) |a|^3 = 27 sqrt(ghat) |d psi|^3, psi = N^(1/3): residuals {[str(v)[:12] for v in r2]} -> "
    f"{'HOLDS' if all(v == 0 for v in r2) else 'FAILS'}")

# (3) numbers
c = 2.99792458e8
G = 6.6743e-11
Msun = 1.98841e30
Gpc = 3.0856775814913673e25
Gyr = 3.15576e16
say("(3) the scale of a0 as a length and a time, and the locality ratio on the 6e10 Msun point mass:")
for name, a0 in (("canonical", 9.3603e-11), ("alt", 1.1312e-10)):
    vf = (G * 6e10 * Msun * a0) ** 0.25
    say(f"    {name}: c^2/a0 = {c*c/a0/Gpc:.2f} Gpc, c/a0 = {c/a0/Gyr:.1f} Gyr, v_f = {vf/1e3:.1f} km/s, "
        f"c^2/v_f^2 = {c*c/vf/vf:.3e} (log10 {sp.log(c*c/vf/vf, 10).evalf(4)}); against 4 pi: "
        f"{c*c/vf/vf/(4*3.141592653589793):.2e}")

open(__file__.replace("root_a1.py", "root_a1_MUTATE.out" if MUT else "root_a1.out"), "w").write("\n".join(out) + "\n")
sys.exit(0 if (ok3 and ok4) != MUT else 1)
