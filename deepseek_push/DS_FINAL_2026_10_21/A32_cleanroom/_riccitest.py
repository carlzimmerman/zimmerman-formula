import sympy as sp

x, y, z = sp.symbols('x y z', real=True)
cs = [x, y, z]

def christoffel(g, inv):
    n = 3
    G = [[[sp.S.Zero]*n for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for l in range(n):
                s = sp.S.Zero
                for k in range(n):
                    s += inv[k, l]*(sp.diff(g[i, k], cs[j]) + sp.diff(g[j, k], cs[i]) - sp.diff(g[i, j], cs[k]))
                G[i][j][l] = sp.expand(s/2)
    return G

def ricci_scalar(g):
    inv = g.inv()
    G = christoffel(g, inv)
    n = 3
    Ric = sp.zeros(n, n)
    for i in range(n):
        for j in range(n):
            s = sp.S.Zero
            for k in range(n):
                s += sp.diff(G[k][i][j], cs[k]) - sp.diff(G[k][i][k], cs[j])
                for l in range(n):
                    s += G[k][k][l]*G[l][i][j] - G[k][j][l]*G[l][i][k]
            Ric[i, j] = sp.simplify(sp.expand(s))
    Rsc = sp.simplify(sum(inv[i, j]*Ric[i, j] for i in range(n) for j in range(n)))
    return Rsc, Ric

# ---- test 1: unit S3 in stereographic coords: g = (1/(1+r^2/4))^2 I , R3 = 6
r2 = x**2 + y**2 + z**2
Om = 1/(1 + r2/4)
g = sp.diag(Om**2, Om**2, Om**2)
R3, _ = ricci_scalar(g)
print("S3 (unit) R3 =", sp.simplify(R3), " expected 6")

# ---- test 2: flat space in weird z-coordinate: g = diag(1,1,f(z)) -> R3 = 0
f = sp.Function('f')(z)
g2 = sp.diag(sp.Integer(1), sp.Integer(1), f**2)
R32, _ = ricci_scalar(g2)
print("flat reparam R3 =", sp.simplify(R32), " expected 0")

# ---- test 3: g = diag(A(z),1,1), compare to hand formula -A''/A + 3/4 (A'/A)^2
A = sp.Function('A')(z)
g3 = sp.diag(A, sp.Integer(1), sp.Integer(1))
R33, _ = ricci_scalar(g3)
hand = -sp.diff(A, z, 2)/A + sp.Rational(3,4)*(sp.diff(A, z)/A)**2
print("diag(A,1,1) R3 =", sp.simplify(R33), " hand:", sp.simplify(hand), " diff:", sp.simplify(R33-hand))
