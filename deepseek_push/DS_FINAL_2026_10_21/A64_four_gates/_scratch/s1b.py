import sympy as sp
t, x, y, z = sp.symbols('t x y z', real=True)
e = sp.Symbol('eps')
Phi = sp.Function('Phi')(x, y, z)
Psi = sp.Function('Psi')(x, y, z)
co = [t, x, y, z]
g = sp.Matrix(4, 4, lambda i, j: 0)
g[0, 0] = -(1 + 2*e*Phi)
for i in (1, 2, 3):
    g[i, i] = 1 - 2*e*Psi
ginv = g.inv()
Gam = [[[sp.simplify(sum(ginv[k, l]*(sp.diff(g[l, i], co[j]) + sp.diff(g[l, j], co[i])
                               - sp.diff(g[i, j], co[l]))/2 for l in range(4)))
         for j in range(4)] for i in range(4)] for k in range(4)]
Rm = [[[[sp.simplify(sp.diff(Gam[l][i][j], co[k]) - sp.diff(Gam[l][i][k], co[j])
           + sum(Gam[l][k][m]*Gam[m][i][j] - Gam[l][j][m]*Gam[m][i][k] for m in range(4)))
         for l in range(4)] for j in range(4)] for i in range(4)] for k in range(4)]
Ric = sp.Matrix(4, 4, lambda i, j: sp.simplify(sum(Rm[k][i][k][j] for k in range(4))))
Rs = sp.simplify(sum(ginv[i, j]*Ric[i, j] for i in range(4) for j in range(4)))
Gdown = Ric - Rs*g/2
Gup = sp.Matrix(4, 4, lambda i, j: sp.simplify(sp.expand(sum(ginv[i, k]*Gdown[k, j] for k in range(4))).coeff(e, 1)))
lap = lambda f: sp.diff(f, x, 2) + sp.diff(f, y, 2) + sp.diff(f, z, 2)
print("G^0_0 =", Gup[0, 0])
print("G^0_0 + 2 lap Phi =", sp.simplify(Gup[0, 0] + 2*lap(Phi)))
trG = sp.simplify(sum(Gup[i, i] for i in range(1, 4)))
print("trace G^i_i =", trG, "   G^i_i - 2 lap(Psi-Phi) =", sp.simplify(trG - 2*lap(Psi-Phi)))
f = Phi - Psi
for (i, j) in [(1, 1), (2, 2), (1, 2)]:
    lhs = sp.simplify(Gup[i, j] - (sp.Rational(1, 3) if i == j else 0)*trG)
    rhs = sp.simplify(sp.diff(f, co[i], co[j]) - (sp.Rational(1, 3) if i == j else 0)*lap(f))
    print(f"({i}{j}) lhs={lhs}\n     lhs-rhs = {sp.simplify(lhs-rhs)}  lhs/rhs={sp.simplify(lhs/rhs) if rhs!=0 else 'na'}")
print("R lin =", sp.simplify(Rs.coeff(e, 1)))