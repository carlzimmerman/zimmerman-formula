import sympy as sp

t, x, y, z, kk, eps = sp.symbols('t x y z k epsilon', real=True)
a = sp.Function('a')(t)
sig = sp.Function('sigma')(t)
Lam = sp.symbols('Lambda', real=True)
Kc = sp.Symbol('K', positive=True)
cs = [t, x, y, z]
E = sp.Symbol('E', positive=True)

def avg(expr):
    e = expr.subs(sp.cos(kk*z), (E + 1/E)/2).subs(sp.sin(kk*z), (E - 1/E)/(2*sp.I))
    return sp.simplify(sp.expand(sp.expand(sp.simplify(e))).coeff(E, 0))

f = eps*sig*sp.cos(kk*z)
g = sp.diag(-1, a**2*(1+f), a**2*(1-f), a**2)

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
    return sp.simplify(sp.expand(R))

R4 = ricci(g, cs)
print("R4 exact:", sp.simplify(R4))
Rs = sp.series(R4, eps, 0, 3).removeO()
Rs = sp.expand(Rs)
detg = sp.simplify(sp.det(g))
sq = sp.sqrt(-detg)
print("sqrt(-g):", sp.simplify(sq))
Lcov = sp.simplify((Rs - 2*Lam)*sq/(16*sp.pi*sp.Symbol('G', positive=True)))
L2 = sp.expand(sp.series(Lcov, eps, 0, 3).removeO()).coeff(eps, 2)
print("\nL2_cov =", sp.simplify(L2))
L2a = avg(L2)
print("\n<L2_cov> =", sp.simplify(sp.expand(L2a)))
sd = sp.Symbol('sd')
L2s = sp.expand(L2a.subs(sp.diff(sig, t), sd))
print("\ncoeff sd^2:", sp.simplify(sp.diff(L2s, sd, 2)/2))
print("coeff k^2:", sp.simplify(sp.diff(L2s, kk, 2)/2))
print("coeff sigma^2 (sd=0):", sp.simplify(L2s.subs(sd, 0)))