import sympy as sp
b, K = sp.symbols('beta K', real=True, positive=True)
# general symmetric K_ij (flat h)
syms = {}
for i in range(3):
    for j in range(i, 3):
        syms[(i, j)] = sp.Symbol(f'K{i}{j}', real=True)
def mat(free=True):
    M = sp.zeros(3, 3)
    for (i, j), s in syms.items():
        M[i, j] = s
        M[j, i] = s
    return M
Kij = mat()
Kup = Kij  # flat
th = sp.trace(Kij)
Lg = (sum(Kij[i, j]*Kup[i, j] for i in range(3) for j in range(3)) - (1+b)*th**2)/(4*K)
# momenta by explicit differentiation wrt hdot_ij with K_ij = hdot_ij/2
hd = {}
for i in range(3):
    for j in range(i, 3):
        hd[(i, j)] = sp.Symbol(f'hd{i}{j}', real=True)
def L_of_hdot():
    M = sp.zeros(3, 3)
    for (i, j), s in hd.items():
        M[i, j] = s/2
        M[j, i] = s/2
    t = sp.trace(M)
    return (sum(M[i, j]*M[i, j] for i in range(3) for j in range(3)) - (1+b)*t**2)/(4*K)
pi = {}
for (i, j), s in hd.items():
    pi[(i, j)] = sp.simplify(sp.diff(L_of_hdot(), s))
# predicted
PIm = sp.zeros(3, 3)
for i in range(3):
    for j in range(3):
        PIm[i, j] = (Kij[i, j] - (1+b)*th*(1 if i == j else 0))/(4*K)
res = max(abs(sp.simplify(pi[(i, j)] - PIm[i, j])) for (i, j) in hd)
print("pi^ij from dL/dhdot residual:", res)
tr_pi = sp.simplify(sum(PIm[i, i] for i in range(3)))
print("pi =", tr_pi, " theta(pi) =", sp.simplify(-4*K*tr_pi/(2+3*b) - th))
# inverse
Kback = sp.zeros(3, 3)
for i in range(3):
    for j in range(3):
        Kback[i, j] = sp.simplify(4*K*(PIm[i, j] + (1+b)*(-4*K*tr_pi/(2+3*b))*K/(1)*(1 if i == j else 0)))
print("Kback check (should be 0):", sp.simplify(Kback[0, 0] - Kij[0, 0]))
# H_grav
cb = (1+b)/(2+3*b)
Hgrav = 4*K*(sum(PIm[i, j]**2 for i in range(3) for j in range(3)) - cb*tr_pi**2)
print("H_grav - L_grav =", sp.simplify(Hgrav - Lg))
print("c_beta =", cb, " 4c-2 =", sp.simplify(4*cb-2))