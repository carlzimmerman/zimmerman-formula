import sympy as sp

t, x, y, z, kk, eps = sp.symbols('t x y z k epsilon', real=True)
a = sp.Function('a')(t)
sig = sp.Function('sigma')(t)
Lam = sp.symbols('Lambda', real=True)
Kc = sp.Symbol('K', positive=True)
cs3 = [x, y, z]
E = sp.Symbol('E', positive=True)

def avg(expr):
    e = expr.subs(sp.cos(kk*z), (E + 1/E)/2).subs(sp.sin(kk*z), (E - 1/E)/(2*sp.I))
    return sp.simplify(sp.expand(sp.expand(sp.simplify(e))).coeff(E, 0))

# --- 3D pieces, exact ---
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

def ricci_scalar(g, cs):
    inv = g.inv(); G = christoffel(g, inv, cs); n = len(cs)
    Ric = sp.zeros(n, n)
    for i in range(n):
        for j in range(n):
            s = sp.S.Zero
            for k in range(n):
                s += sp.diff(G[k][i][j], cs[k]) - sp.diff(G[k][i][k], cs[j])
                for l in range(n):
                    s += G[k][k][l]*G[l][i][j] - G[k][j][l]*G[l][i][k]
            Ric[i, j] = s
    return sum(inv[i, j]*Ric[i, j] for i in range(n) for j in range(n))

f = eps*sig*sp.cos(kk*z)
h = sp.diag(a**2*(1+f), a**2*(1-f), a**2)
minv = h.inv()
Kij = sp.Matrix(3, 3, lambda i, j: sp.diff(h[i, j], t)/2)
K = sum(minv[i, j]*Kij[i, j] for i in range(3) for j in range(3))
Ksq = sum(minv[i, k]*minv[j, l]*Kij[i, j]*Kij[k, l]
          for i in range(3) for j in range(3) for k in range(3) for l in range(3))
R3 = ricci_scalar(h, cs3)
sqh = sp.sqrt(sp.det(h))

L = sp.simplify(sqh*(R3 + Ksq - K**2 - 2*Lam)/(4*Kc))
L2 = sp.expand(sp.series(L, eps, 0, 3).removeO()).coeff(eps, 2)
L2a = avg(L2)
print("L2 (averaged, per mode) =", sp.simplify(L2a))

# Euler-Lagrange for sigma(t), spatial density integrated: S = int dt L2a
s, sd, sdd = sp.symbols('s sd sdd')
Lsub = L2a.subs({sp.diff(sig, t, 2): sdd, sp.diff(sig, t): sd, sig: s})
EL = sp.simplify(sp.diff(Lsub, s) - sp.diff(sp.diff(Lsub, sd), t) - sp.diff(sp.diff(Lsub, sdd), t))
EL = sp.simplify(EL.subs({sdd: sp.diff(sig, t, 2), sd: sp.diff(sig, t), s: sig}))
print("\nEL residual =", EL)
print("EL / (common factor) =", sp.simplify(sp.expand(EL*Kc*16)))