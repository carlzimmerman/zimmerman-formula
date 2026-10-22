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
Kij = build(Ks); Khd = build({k: v/2 for k, v in Hs.items()})
def Lg(M):
    t = sp.trace(M)
    return (sum(M[i, j]**2 for i in range(3) for j in range(3)) - (1+b)*t**2)/(4*K)
th = sp.trace(Kij)
PIm = sp.Matrix(3, 3, lambda i, j: (Kij[i, j] - (1+b)*th*(1 if i == j else 0))/(4*K))
tr_pi = sp.simplify(sum(PIm[i, i] for i in range(3)))
# L1: symmetric functional derivative: delta L / delta hdot_ij = 2 pi^ij (i!=j), pi^ii (i==j)
res = 0.0
for (i, j) in idx:
    d = sp.diff(Lg(Khd), Hs[(i, j)]).subs({Hs[(a, c)]: 2*Ks[(a, c)] for (a, c) in idx})
    want = (1 if i == j else 2)*PIm[i, j]
    res = max(res, abs(float(sp.simplify(d - want))))
print("L1 sym functional derivative residual:", res)
print("L1 Euler (full-sum pi.hdot=2L):", sp.simplify(2*sum(PIm[i, j]*Kij[i, j] for i in range(3) for j in range(3)) - 2*Lg(Kij)))
print("L2 theta(pi)-theta:", sp.simplify(-4*K*tr_pi/(2+3*b) - th))
Kback = sp.Matrix(3, 3, lambda i, j: sp.simplify(4*K*(PIm[i, j] + (1+b)*(-4*K*tr_pi/(2+3*b))*(1 if i == j else 0))))
print("L2 Kback-K:", [sp.simplify(Kback[a] - Kij[a]) for a in (0, 4, 1)])
cb = (1+b)/(2+3*b)
Hgrav = 4*K*(sum(PIm[i, j]**2 for i in range(3) for j in range(3)) - cb*tr_pi**2)
print("L3 H_grav-L_grav:", sp.simplify(Hgrav - Lg(Kij)))
print("L8 c_beta:", cb, " 4c-2:", sp.factor(sp.simplify(4*cb-2)), " at 0:", (4*cb-2).subs(b, 0), " lim:", sp.limit(cb, b, sp.oo))
print("   beta=0 H == 4K(pi.pi-pi^2/2)?", sp.simplify((Hgrav - 4*K*(sum(PIm[i, j]**2 for i in range(3) for j in range(3)) - tr_pi**2/2)).subs(b, 0)))