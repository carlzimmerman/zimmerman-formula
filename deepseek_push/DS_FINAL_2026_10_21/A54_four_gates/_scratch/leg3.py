import sympy as sp

b = sp.symbols('beta', real=True)
x, y, z = sp.symbols('x y z', real=True)
coords = [x, y, z]
h_, k_ = sp.symbols('h k', real=True)

# ---- Legendre with 9 independent entries and the 1/2 from dK/dhdot ----------
Kij = sp.Matrix(3, 3, lambda i, j: sp.Symbol(f'k{i}{j}', real=True))
th = sp.trace(Kij)
K2 = sum(Kij[i, j] ** 2 for i in range(3) for j in range(3))
Lg = (K2 - (1 + b) * th ** 2) / 4
pi = sp.zeros(3, 3)
for i in range(3):
    for j in range(3):
        pi[i, j] = sp.Rational(1, 2) * sp.diff(Lg, Kij[i, j])
SUBS = {Kij[1, 0]: Kij[0, 1], Kij[2, 0]: Kij[0, 2], Kij[2, 1]: Kij[1, 2]}
pi = sp.simplify(pi.subs(SUBS))
tgt = (Kij - (1 + b) * th * sp.eye(3)) / 4
print('L1 resid:', sp.simplify(sum(abs(v) for v in (pi - tgt).subs(SUBS))))
pitr = sp.simplify(sp.trace(pi))
th_of_pi = sp.simplify(-4 * pitr / (2 + 3 * b))
print('L2 theta resid:', sp.simplify(th_of_pi - th))
Kback = sp.zeros(3, 3)
for i in range(3):
    for j in range(3):
        Kback[i, j] = sp.simplify(4 * pi[i, j] + (1 + b) * th_of_pi * (1 if i == j else 0))
print('L2 Kback resid:', sp.simplify(sum(abs(v) for v in (Kback - Kij).subs(SUBS))))
cb = (1 + b) / (2 + 3 * b)
Hgrav = sp.simplify(4 * (sum(pi[i, j] ** 2 for i in range(3) for j in range(3)) - cb * pitr ** 2))
print('L3 resid:', sp.simplify((Hgrav - Lg).subs(SUBS)))

# ---- exact R3 for the TT metric diag(1+hc, 1-hc, 1) -------------------------
c = sp.cos(k_ * z)
A = 1 + h_ * c
B = 1 - h_ * c
Ap, Bp = sp.diff(A, z), sp.diff(B, z)
App, Bpp = sp.diff(A, z, 2), sp.diff(B, z, 2)
Rzz = -(sp.diff(Ap / (2 * A) + Bp / (2 * B), z)) - (Ap ** 2 / (4 * A ** 2) + Bp ** 2 / (4 * B ** 2))
Rxx = -Ap * 0 - sp.Rational(1, 2) * App - Ap / 4 * (Ap / A + Bp / B) + Ap ** 2 / (4 * A)
Ryy = -sp.Rational(1, 2) * Bpp - Bp / 4 * (Ap / A + Bp / B) + Bp ** 2 / (4 * B)
R = sp.simplify(Rxx / A + Ryy / B + Rzz)
R2 = sp.series(R, h_, 0, 3).removeO().coeff(h_, 2)
print('R3^(2)(z) =', sp.simplify(R2))
avg = sp.simplify(R2.subs(sp.cos(k_ * z) ** 4, sp.Rational(3, 8)).subs(
    sp.cos(k_ * z) ** 2, sp.Rational(1, 2)))
print('avg R3^(2) =', avg, '   vs -k^2h^2/4:', sp.simplify(avg + k_ ** 2 * h_ ** 2 / 4))
print('also series of R itself O(h^1):', sp.simplify(sp.series(R, h_, 0, 2).removeO().coeff(h_, 1)))
