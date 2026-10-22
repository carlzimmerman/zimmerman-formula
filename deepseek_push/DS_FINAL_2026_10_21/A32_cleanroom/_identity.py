import sympy as sp

t, x, y, z, kk, eps = sp.symbols('t x y z k epsilon', real=True)
a = sp.Function('a')(t)
sig = sp.Function('sigma')(t)
Lam = sp.symbols('Lambda', real=True)
cs4 = [t, x, y, z]
cs3 = [x, y, z]

def christoffel(g, inv, cs):
    n = len(cs)
    G = [[[sp.S.Zero]*n for _ in range(n)] for _ in range(n)]
    for u in range(n):
        for i in range(n):
            for j in range(n):
                s = sp.S.Zero
                for l in range(n):
                    s += inv[u, l]*(sp.diff(g[i, l], cs[j]) + sp.diff(g[j, l], cs[i]) - sp.diff(g[i, j], cs[l]))
                G[u][i][j] = sp.expand(s/2)
    return G

def ricci(g, cs):
    inv = g.inv()
    G = christoffel(g, inv, cs)
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
    R = sum(inv[i, j]*Ric[i, j] for i in range(n) for j in range(n))
    return R

f = eps*sig*sp.cos(kk*z)
h3 = sp.diag(a**2*(1+f), a**2*(1-f), a**2)
g4 = sp.diag(-1, a**2*(1+f), a**2*(1-f), a**2)

R4 = sp.simplify(ricci(g4, cs4))
R3 = sp.simplify(ricci(h3, cs3))
Kij = sp.Matrix(3, 3, lambda i, j: sp.diff(h3[i, j], t)/2)
h3inv = h3.inv()
K = sp.simplify(sum(h3inv[i, j]*Kij[i, j] for i in range(3) for j in range(3)))
Ksq = sp.simplify(sum(h3inv[i, k]*h3inv[j, l]*Kij[i, j]*Kij[k, l]
                      for i in range(3) for j in range(3) for k in range(3) for l in range(3)))
sqh = sp.simplify(sp.sqrt(sp.det(h3)))
sqg = sp.simplify(sp.sqrt(-sp.det(g4)))

lhs = sp.simplify(sqg*R4)
rhs = sp.simplify(sqh*(R3 + Ksq - K**2) + 2*sp.diff(sqh*K, t))
print("identity residual (should be 0):", sp.simplify(lhs - rhs))
print("\nK =", K)
print("\nKsq - K^2 =", sp.simplify(Ksq - K**2))
print("\nR3 =", sp.simplify(R3))