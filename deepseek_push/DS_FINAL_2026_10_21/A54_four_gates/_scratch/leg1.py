import sympy as sp

# flat h, general symmetric K_ij, general beta
b, N = sp.symbols('beta N', real=True)
K = sp.Matrix(3, 3, lambda i, j: sp.Symbol(f'K{min(i,j)}{max(i,j)}', real=True))
print('K symmetric:', K == K.T)
th = sp.trace(K)
KijKij = sum(K[i, j]**2 for i in range(3) for j in range(3))

L = (KijKij - (1 + b) * th**2) / 4          # sqrt(h)=1, K_normalisation=1
# pi^ij = dL/dK_ij  (with symmetric-variable convention: d(KijKij)/dK_ij = 2K_ij)
pi = sp.zeros(3, 3)
for i in range(3):
    for j in range(i, 3):
        val = sp.diff(L, K[i, j])
        pi[i, j] = val
        pi[j, i] = val
print('pi =', pi)
print('check pi = (K - (1+b) theta delta)/4 :',
      sp.simplify(pi - (K - (1 + b) * th * sp.eye(3)) / 4))

pitr = sp.trace(pi)
print('pi_trace =', sp.simplify(pitr), ' vs -(2+3b)theta/4:',
      sp.simplify(pitr + (2 + 3 * b) * th / 4))

# Legendre transform back
cb = (1 + b) / (2 + 3 * b)
Leg = sum(pi[i, j] * K[i, j] for i in range(3) for j in range(3)) - L
print('Legendre (pi.K - L) - L =', sp.simplify(Leg - L))
# and in terms of pi:  4*(pi_ij pi_ij - cb pi^2)
expr = 4 * (sum(pi[i, j]**2 for i in range(3) for j in range(3)) - cb * pitr**2)
print('4(pi^2 - cb pi^2) - L =', sp.simplify(expr - L))
