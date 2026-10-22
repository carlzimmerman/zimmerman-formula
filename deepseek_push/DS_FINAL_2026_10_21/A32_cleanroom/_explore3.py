import sympy as sp
from sympy import Rational as R

t, x, y, z, kk, eps = sp.symbols('t x y z k epsilon', real=True)
a = sp.Function('a')(t)
sig = sp.Function('sigma')(t)
beta = sp.symbols('beta', real=True)
Lam = sp.symbols('Lambda', positive=True)

f = eps*sig*sp.cos(kk*z)          # the TT amplitude

# 3-metric h_ij = a^2 * m_ij , m = diag(1+f, 1-f, 1)  (TT: tr=0, d_i g_iz = 0)
m = sp.diag(1+f, 1-f, 1)
coords = [x, y, z]

def christoffel(g, inv, cs):
    n = len(cs)
    G = [[[sp.S.Zero]*n for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for l in range(n):
                s = sp.S.Zero
                for k in range(n):
                    s += inv[k, l]*(sp.diff(g[i, k], cs[j]) + sp.diff(g[j, k], cs[i]) - sp.diff(g[i, j], cs[k]))
                G[i][j][l] = sp.simplify(s/2)
    return G

minv = sp.diag(1/(1+f), 1/(1-f), 1)
Gm = christoffel(m, minv, coords)

def ricci_scalar(g, inv, G, cs):
    n = len(cs)
    Ric = sp.zeros(n, n)
    for i in range(n):
        for j in range(n):
            s = sp.S.Zero
            for k in range(n):
                s += sp.diff(G[k][i][j], cs[k]) - sp.diff(G[k][i][k], cs[j])
                for l in range(n):
                    s += G[k][k][l]*G[l][i][j] - G[k][j][l]*G[l][i][k]
            Ric[i, j] = s
    Rsc = sum(inv[i, j]*Ric[i, j] for i in range(n) for j in range(n))
    return sp.simplify(Rsc), Ric

R3m, Ricm = ricci_scalar(m, minv, Gm, coords)
R3m = sp.simplify(sp.expand(R3m))
print("R3(m) exact:", R3m)
R3m_ser = sp.series(R3m, eps, 0, 3).removeO()
R3m_ser = sp.expand(R3m_ser)
print("\nR3(m) to eps^2:", sp.simplify(R3m_ser))
print("  coeff eps^1:", sp.simplify(sp.expand(R3m_ser).coeff(eps,1)))
print("  coeff eps^2:", sp.simplify(sp.expand(R3m_ser).coeff(eps,2)))
print("  check R3(m) eps^2 == (1/2)(d f)^2 ? ",
      sp.simplify(sp.expand(R3m_ser).coeff(eps,2) - sp.Rational(1,2)*sp.diff(f,z)**2/sp.expand(1)))
