import sympy as sp
b, K = sp.symbols('beta K', real=True, positive=True)
idx = [(i, j) for i in range(3) for j in range(i, 3)]
Ks = {k: sp.Symbol(f'K{k[0]}{k[1]}', real=True) for k in idx}
Hs = {k: sp.Symbol(f'hd{k[0]}{k[1]}', real=True) for k in idx}
def build(d):
    M = sp.zeros(3, 3)
    for (i, j), s in d.items():
        M[i, j] = s; M[j, i] = s
    return M
Kij = build(Ks)
Khd = build({k: v/2 for k, v in Hs.items()})
def Lg(M):
    t = sp.trace(M)
    return (sum(M[i, j]**2 for i in range(3) for j in range(3)) - (1+b)*t**2)/(4*K)
th = sp.trace(Kij)
PIm = sp.Matrix(3, 3, lambda i, j: (Kij[i, j] - (1+b)*th*(1 if i == j else 0))/(4*K))
res = 0
for (i, j) in idx:
    e = sp.simplify(sp.diff(Lg(Khd), Hs[(i, j)]).subs({Hs[(a, c)]: 2*Ks[(a, c)] for (a, c) in idx}) - PIm[i, j])
    res = max(res, abs(float(e)))
print("L1 pi^ij = dL/dhdot residual:", res)
tr_pi = sp.simplify(sum(PIm[i, i] for i in range(3)))
print("L2  theta(pi)-theta:", sp.simplify(-4*K*tr_pi/(2+3*b) - th))
Kback = sp.Matrix(3, 3, lambda i, j: sp.simplify(4*K*(PIm[i, j] + (1+b)*(-4*K*tr_pi/(2+3*b))*(1 if i == j else 0))))
print("L2  K^ij(pi)-K^ij:", [sp.simplify(Kback[a] - Kij[a]) for a in (0, 4, 1)])
print("L1  Euler pi.K-L:", sp.simplify(sum(PIm[i, j]*Kij[i, j] for i in range(3) for j in range(3)) - Lg(Kij)))
cb = (1+b)/(2+3*b)
Hgrav = 4*K*(sum(PIm[i, j]**2 for i in range(3) for j in range(3)) - cb*tr_pi**2)
print("L3  H_grav-L_grav:", sp.simplify(Hgrav - Lg(Kij)))
print("L8  c_beta:", cb, " 4c-2:", sp.factor(sp.simplify(4*cb - 2)), " at beta=0:", (4*cb-2).subs(b, 0))
print("    H(beta=0) - 4K(pi.pi-pi^2/2):", sp.simplify((Hgrav - 4*K*(sum(PIm[i, j]**2 for i in range(3) for j in range(3)) - tr_pi**2/2)).subs(b, 0)))
print("    beta->inf limit of c_beta:", sp.limit(cb, b, sp.oo))