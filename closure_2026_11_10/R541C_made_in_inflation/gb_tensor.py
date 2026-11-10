"""R541C KA5 (sympy): tensor-mode speed with xi(t) * G_GB on FRW. Metric diag(-1, a^2 e^{eps h}, a^2 e^{-eps h}, a^2),
h = h(t, z). Second-order action from sqrt(-g)[R/(4K) + xi G_GB]; the linear h equation's coefficients of h_tt and h_zz
give c_T^2. Target (Kobayashi 2019, PROVISIONAL): c_T^2 = (M^2 + 8 xi_ddot)/(M^2 + 8 H xi_dot), M^2 = 1/(2K).
Prints to gb_tensor.out."""
import sympy as sp
from sympy.calculus.euler import euler_equations

t, x, y, z, eps = sp.symbols('t x y z epsilon')
K = sp.symbols('K', positive=True)
a = sp.Function('a')(t); xi = sp.Function('xi')(t); h = sp.Function('h')(t, z)
X = [t, x, y, z]
g = sp.diag(-1, a ** 2 * sp.exp(eps * h), a ** 2 * sp.exp(-eps * h), a ** 2)
n = 4; gi = sp.diag(*[1 / g[i, i] for i in range(n)])


def ser(e, order=2):
    out = 0; d = e
    for k in range(order + 1):
        out += sp.expand(d.subs(eps, 0)) * eps ** k / sp.factorial(k)
        d = sp.diff(d, eps)
    return sp.expand(out)


Gam = [[[sum(gi[a_, d] * (sp.diff(g[d, b], X[c]) + sp.diff(g[d, c], X[b]) - sp.diff(g[b, c], X[d])) for d in range(n)) / 2
         for c in range(n)] for b in range(n)] for a_ in range(n)]
Gam = [[[sp.expand(ser(Gam[i][j][k])) for k in range(n)] for j in range(n)] for i in range(n)]
Riem = {}
for A in range(n):
    for B in range(n):
        for C in range(n):
            for D in range(C + 1, n):
                e = sp.diff(Gam[A][B][D], X[C]) - sp.diff(Gam[A][B][C], X[D])
                e += sum(Gam[A][C][k] * Gam[k][B][D] - Gam[A][D][k] * Gam[k][B][C] for k in range(n))
                e = sp.expand(ser(sp.expand(e)))
                if e != 0:
                    Riem[(A, B, C, D)] = e
                    Riem[(A, B, D, C)] = -e
Ric = sp.zeros(n, n)
for (A, B, C, D), v in Riem.items():
    if A == C:
        Ric[B, D] += v
Ric = Ric.applyfunc(lambda e: sp.expand(ser(e)))
dg = [sp.expand(ser(gi[i, i])) for i in range(n)]
gd = [g[i, i] for i in range(n)]
Rs = sp.expand(ser(sum(dg[i] * Ric[i, i] for i in range(n))))
RicSq = sp.expand(ser(sum(Ric[i, j] ** 2 * dg[i] * dg[j] for i in range(n) for j in range(n))))
Kr = 0
for (A, B, C, D), v in Riem.items():
    # R_{ABCD} R^{ABCD} = sum (g_AA R^A_BCD)^2 g^AA g^BB g^CC g^DD = (R^A_BCD)^2 g_AA g^BB g^CC g^DD
    Kr += v ** 2 * ser(gd[A] * dg[B] * dg[C] * dg[D])
Kr = sp.expand(ser(sp.expand(Kr)))
GB = sp.expand(ser(Rs ** 2 - 4 * RicSq + Kr))
sqg = a ** 3  # det is exactly -a^6
L = sp.expand(ser(sqg * (Rs / (4 * K) + xi * GB)))
L2 = L.coeff(eps, 2)
eq = euler_equations(L2, [h], [t, z])[0].lhs
eq = sp.expand(eq)
ctt = sp.simplify(eq.coeff(sp.Derivative(h, (t, 2))))
czz = sp.simplify(eq.coeff(sp.Derivative(h, (z, 2))))
print("coefficient of h_tt:", sp.factor(ctt))
print("coefficient of h_zz:", sp.factor(czz))
cT2 = sp.simplify(-czz * a ** 2 / ctt)
print("c_T^2 = -a^2 c_zz / c_tt =", sp.factor(cT2))
H = sp.diff(a, t) / a
M2 = 1 / (2 * K)
target = (M2 + 8 * sp.diff(xi, t, 2)) / (M2 + 8 * H * sp.diff(xi, t))
print("c_T^2 - Kobayashi target =", sp.simplify(cT2 - target))
print("KA5 at xi = const (GR + topological term): c_T^2 =", sp.simplify(cT2.subs(xi, sp.Symbol('c0')).doit()))
print("check: no fourth derivatives in h equation:",
      all(sp.Derivative(h, (v, 3)) not in eq.atoms(sp.Derivative) for v in (t, z)))
