"""
mc_selftest.py -- validation of the symbolic tensor core.

Every check is a hard assert.  If this file does not exit 0, nothing downstream is
trustworthy.

  T1  Ricci of Schwarzschild vanishes            (curvature engine)
  T2  R of FRW matches the textbook value        (sign convention)
  T3  Palatini vector-distortion identity
        C^a_mn = d^a_m A_n + d^a_n A_m  =>  R(Gamma) = R(g) - 3 div A + 3 A^2
      by DIRECT component computation on a curved metric with a generic A(x).
      (this is the archetype the search is meant to generalise)
  T4  the same machinery on the OTHER natural distortion C^a_mn = g_mn A^a gives
        R(Gamma) = R(g) + 3 div A + 3 A^2
  T5  covariant derivative of the metric vanishes (Christoffel correctness)
"""
import sys
import sympy as sp
from mc_core import christoffel, ricci, cov_d_vector, cov_d_tensor2

PASS = 0
FAIL = 0


def check(name, cond):
    global PASS, FAIL
    if cond:
        PASS += 1
        print(f"  PASS  {name}")
    else:
        FAIL += 1
        print(f"  FAIL  {name}")


# ---------------------------------------------------------------- T1 Schwarzschild
t, r, th, ph = sp.symbols('t r theta phi', positive=True)
M = sp.Symbol('M', positive=True)
f = 1 - 2 * M / r
gS = sp.diag(-f, 1 / f, r**2, r**2 * sp.sin(th)**2)
coordsS = [t, r, th, ph]
GamS = christoffel(gS, gS.inv(), coordsS)
RicS = ricci(GamS, coordsS)
check("T1 Ricci[Schwarzschild] == 0", sp.simplify(RicS) == sp.zeros(4, 4))

# ---------------------------------------------------------------- T2 FRW
tt, xx, yy, zz = sp.symbols('t x y z')
a = sp.Function('a')(tt)
gF = sp.diag(-1, a**2, a**2, a**2)
coordsF = [tt, xx, yy, zz]
GamF = christoffel(gF, gF.inv(), coordsF)
RicF = ricci(GamF, coordsF)
ginvF = gF.inv()
RF = sp.simplify(sum(ginvF[i, j] * RicF[i, j] for i in range(4) for j in range(4)))
# textbook (flat FRW, signature -+++, R = 6(add/a + (ad/a)^2))
RF_ref = 6 * (sp.diff(a, tt, 2) / a + (sp.diff(a, tt) / a)**2)
check("T2 R[FRW] == 6(a''/a + (a'/a)^2)", sp.simplify(RF - RF_ref) == 0)

# ---------------------------------------------------------------- T5 metric compatibility
Sm = sp.Matrix(4, 4, lambda i, j: sp.Function(f'S{min(i,j)}{max(i,j)}')(*coordsF))
DgF = cov_d_tensor2(gF, GamF, coordsF)
ok = all(sp.simplify(DgF[m][i][j]) == 0 for m in range(4) for i in range(4) for j in range(4))
check("T5 nabla_m g_np == 0", ok)


# ------------------------------------------------- T3/T4 Palatini distortion identities
def ricci_from_connection(Gam, coords):
    return ricci(Gam, coords)


def distortion_test(Cfun, expected_div_coeff, expected_A2_coeff, label):
    """Gamma = LeviCivita(g) + C ; compare R(Gamma) with R(g) + a*divA + b*A^2."""
    # a generic (but tractable) curved metric and a generic A_mu(x)
    u, v = sp.symbols('u v')
    F1 = sp.Function('F1')(u)
    F2 = sp.Function('F2')(v)
    g = sp.diag(-sp.exp(2 * F1), sp.exp(2 * F2), 1, 1)
    coords = [u, v, sp.Symbol('p'), sp.Symbol('q')]
    A = [sp.Function('A0')(u, v), sp.Function('A1')(u, v), sp.S.Zero, sp.S.Zero]
    ginv = g.inv()
    Gam0 = christoffel(g, ginv, coords)
    Au = [sum(ginv[i, j] * A[j] for j in range(4)) for i in range(4)]

    C = Cfun(A, Au, g, coords)
    Gam = [[[sp.expand(Gam0[a_][m][n] + C[a_][m][n]) for n in range(4)]
            for m in range(4)] for a_ in range(4)]
    RicG = ricci_from_connection(Gam, coords)
    RG = sum(ginv[i, j] * RicG[i, j] for i in range(4) for j in range(4))

    Ric0 = ricci(Gam0, coords)
    R0 = sum(ginv[i, j] * Ric0[i, j] for i in range(4) for j in range(4))
    DA = cov_d_vector(A, Gam0, coords)
    divA = sum(ginv[i, j] * DA[i][j] for i in range(4) for j in range(4))
    A2 = sum(Au[i] * A[i] for i in range(4))

    diff = sp.simplify(sp.expand(RG - R0 - expected_div_coeff * divA
                                 - expected_A2_coeff * A2))
    check(label, diff == 0)


def C_vector(A, Au, g, coords):
    C = [[[sp.S.Zero] * 4 for _ in range(4)] for _ in range(4)]
    for a_ in range(4):
        for m in range(4):
            for n in range(4):
                C[a_][m][n] = (1 if a_ == m else 0) * A[n] + (1 if a_ == n else 0) * A[m]
    return C


def C_metric(A, Au, g, coords):
    C = [[[sp.S.Zero] * 4 for _ in range(4)] for _ in range(4)]
    for a_ in range(4):
        for m in range(4):
            for n in range(4):
                C[a_][m][n] = g[m, n] * Au[a_]
    return C


distortion_test(C_vector, -3, 3,
                "T3 C^a_mn = d^a_m A_n + d^a_n A_m  =>  R(Gamma) = R(g) - 3 divA + 3 A^2")
distortion_test(C_metric, +3, 3,
                "T4 C^a_mn = g_mn A^a          =>  R(Gamma) = R(g) + 3 divA + 3 A^2")

print(f"\nSELFTEST  {PASS} passed / {FAIL} failed")
sys.exit(0 if FAIL == 0 else 1)
