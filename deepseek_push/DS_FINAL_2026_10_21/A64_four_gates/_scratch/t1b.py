import sympy as sp
b, K = sp.symbols('beta K', real=True, positive=True)
hd = {}
for i in range(3):
    for j in range(i, 3):
        hd[(i, j)] = sp.Symbol(f'hd{i}{j}', real=True)
def M_of_hd():
    M = sp.zeros(3, 3)
    for (i, j), s in hd.items():
        M[i, j] = s/2; M[j, i] = s/2
    return M
def L_of_hd():
    M = M_of_hd(); t = sp.trace(M)
    return (sum(M[i, j]*M[i, j] for i in range(3) for j in range(3)) - (1+b)*t**2)/(4*K)
pi_hd = {k: sp.simplify(sp.diff(L_of_hd(), s)) for k, s in hd.items()}
Kij = M_of_hd(); th = sp.trace(Kij)
PIm = sp.zeros(3, 3)
for i in range(3):
    for j in range(3):
        PIm[i, j] = (Kij[i, j] - (1+b)*th*(1 if i == j else 0))/(4*K)
res = 0
for (i, j) in hd:
    e = sp.simplify(pi_hd[(i, j)].subs({hd[(a, c)]: 2*Kij[a, c] for (a, c) in hd}) - PIm[i, j])
    res = max(res, abs(e))
print("L1 pi^ij = dL/dhdot residual:", res)
tr_pi = sp.simplify(sum(PIm[i, i] for i in range(3)))
print("L2 pi =", tr_pi, ";  theta(pi) - theta =", sp.simplify(-4*K*tr_pi/(2+3*b) - th))
Kback = sp.zeros(3, 3)
for i in range(3):
    for j in range(3):
        Kback[i, j] = sp.simplify(4*K*(PIm[i, j] + (1+b)*(-4*K*tr_pi/(2+3*b))*(1 if i == j else 0)))
print("L2 K^ij(pi) - K^ij:", sp.simplify(Kback[0, 0] - Kij[0, 0]), sp.simplify(Kback[0, 1] - Kij[0, 1]))
Lg = (sum(Kij[i, j]**2 for i in range(3) for j in range(3)) - (1+b)*th**2)/(4*K)
print("L1 Euler pi.K - L:", sp.simplify(sum(PIm[i, j]*Kij[i, j] for i in range(3) for j in range(3)) - Lg))
cb = (1+b)/(2+3*b)
Hgrav = 4*K*(sum(PIm[i, j]**2 for i in range(3) for j in range(3)) - cb*tr_pi**2)
print("L3 H_grav - L_grav:", sp.simplify(Hgrav - Lg))
print("c_beta =", cb, "; 4c-2 =", sp.simplify(4*cb - 2), "; at beta=0:", sp.simplify((4*cb-2).subs(b,0)))
print("H at beta=0 vs GR (pi.pi - pi^2/2):", sp.simplify(Hgrav.subs(b,0) - 4*K*(sum(PIm[i,j]**2 for i in range(3) for j in range(3)) - tr_pi**2/2).subs(b,0)))