import sympy as sp

t, x, y, z, kk, eps = sp.symbols('t x y z k epsilon', real=True)
a = sp.Function('a')(t)
sig = sp.Function('sigma')(t)
Lam = sp.symbols('Lambda', real=True)
cs = [t, x, y, z]


def christoffel(g, inv, cs):
    n = len(cs)
    G = [[[sp.S.Zero] * n for _ in range(n)] for _ in range(n)]
    for u in range(n):
        for i in range(n):
            for j in range(n):
                s = sp.S.Zero
                for l in range(n):
                    s += inv[u, l] * (sp.diff(g[i, l], cs[j]) + sp.diff(g[j, l], cs[i])
                                      - sp.diff(g[i, j], cs[l]))
                G[u][i][j] = sp.expand(s / 2)
    return G


def ricci_tensor(g, cs):
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
                    s += G[k][k][l] * G[l][i][j] - G[k][j][l] * G[l][i][k]
            Ric[i, j] = s
    return Ric


f = eps * sig * sp.cos(kk * z)
g = sp.diag(-1, a**2 * (1 + f), a**2 * (1 - f), a**2)
Ric = ricci_tensor(g, cs)
Rsc = sum(g.inv()[i, j] * Ric[i, j] for i in range(4) for j in range(4))
E = sp.zeros(4, 4)
for i in range(4):
    for j in range(4):
        E[i, j] = sum(g.inv()[i, k] * Ric[k, j] for k in range(4)) - Rsc * sp.KroneckerDelta(i, j) / 2

# transverse-traceless component: E^x_x - E^y_y  ~ 2 * (linearised TT operator)
comb = sp.simplify(E[1, 1] - E[2, 2])
lin = sp.simplify(sp.diff(comb, eps).subs(eps, 0))
print("d/de E^x_x - E^y_y |_0 =")
print(sp.simplify(lin))
H = sp.diff(a, t) / a
target = (sp.Derivative(sig, (t, 2)) + 3 * H * sp.Derivative(sig, t) + kk**2 * sig / a**2) * sp.cos(kk * z)
print("\nratio (lin / massless TT operator) =", sp.simplify(lin / target))