import sympy as sp

b = sp.symbols('beta', real=True)
# 9 INDEPENDENT entries; symmetrise with the 1/2(d/dK_ij + d/dK_ji) convention
K = sp.Matrix(3, 3, lambda i, j: sp.Symbol(f'K{i}{j}', real=True))
Kup = K  # flat space: index position irrelevant
th = sp.trace(K)
KijKij = sum(K[i, j] * Kup[i, j] for i in range(3) for j in range(3))
L = (KijKij - (1 + b) * th**2) / 4

pi = sp.zeros(3, 3)
for i in range(3):
    for j in range(3):
        pi[i, j] = sp.Rational(1, 2) * (sp.diff(L, K[i, j]) + sp.diff(L, K[j, i]))
pi = sp.simplify(pi)
print('pi - (K-(1+b)th d)/4 =', sp.simplify(pi - (K - (1 + b) * th * sp.eye(3)) / 4))

pitr = sp.simplify(sp.trace(pi))
print('pi_tr + (2+3b)th/4 =', sp.simplify(pitr + (2 + 3 * b) * th / 4))

cb = (1 + b) / (2 + 3 * b)
Leg = sp.simplify(sum(pi[i, j] * K[i, j] for i in range(3) for j in range(3)) - L)
print('pi.K - 2L =', sp.simplify(Leg - L))          # Euler: pi.K = 2L
expr = sp.simplify(4 * (sum(pi[i, j]**2 for i in range(3) for j in range(3)) - cb * pitr**2))
print('4(pi2 - cb pi_tr^2) - L =', sp.simplify(expr - L))
