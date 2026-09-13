#!/usr/bin/env python3
"""Principal-symbol gate for a nonlinear MOND interaction on a nonzero background.

The quadratic Minkowski calculation is insufficient for an exact MOND
constitutive function M(T).  This script freezes a local static weak-field
background with relative gradients p=Phi_,z and q=Psi_,z, then computes the
second variation of T4-T1 for a transverse relative vector perturbation
(h_0x,h_zx).  It keeps M'(Tbar) symbolic, so no rank, determinant, or DOF
answer is encoded in advance.

For the chosen background Tbar<0, the deep-MOND representative
M(T)=(-T)^(3/2) is also evaluated.  The result is local and bounded to this
invariant direction and this background orientation; it is not a universal
no-go theorem for arbitrary bimetric actions.
"""
from __future__ import annotations

import sympy as sp


eta = sp.diag(-1, 1, 1, 1)
w, k = sp.symbols("omega kappa", real=True)
p, q = sp.symbols("p q", real=True)
e01, e13, t = sp.symbols("e01 e13 t", real=True)


def connection_from_derivatives(dh):
    C = [[[sp.Integer(0) for _ in range(4)] for _ in range(4)] for _ in range(4)]
    for ell in range(4):
        for m in range(4):
            for n in range(4):
                C[ell][m][n] = sp.expand(
                    sum(
                        eta[ell, s]
                        * (dh[n][s, m] + dh[m][s, n] - dh[s][m, n])
                        for s in range(4)
                    )
                    / 2
                )
    return C


def invariants(C):
    T1 = sum(
        C[a][m][n]
        * C[b][r][s]
        * eta[a, b]
        * eta[m, r]
        * eta[n, s]
        for a in range(4)
        for b in range(4)
        for m in range(4)
        for n in range(4)
        for r in range(4)
        for s in range(4)
    )
    P = [
        sum(eta[m, n] * C[a][m][n] for m in range(4) for n in range(4))
        for a in range(4)
    ]
    T2 = sum(eta[a, b] * P[a] * P[b] for a in range(4) for b in range(4))
    V = [sum(C[a][a][mu] for a in range(4)) for mu in range(4)]
    T3 = sum(eta[m, n] * V[m] * V[n] for m in range(4) for n in range(4))
    T4 = sum(
        eta[m, n] * C[a][m][b] * C[b][n][a]
        for m in range(4)
        for n in range(4)
        for a in range(4)
        for b in range(4)
    )
    T5 = sum(P[a] * V[a] for a in range(4))
    return [sp.expand(value) for value in (T1, T2, T3, T4, T5)]


# Static background: h_00=-2 Phi, h_ii=-2 Psi and only z-derivatives p,q.
background = [sp.zeros(4, 4) for _ in range(4)]
background[3][0, 0] = -2 * p
for i in (1, 2, 3):
    background[3][i, i] = -2 * q

# Transverse vector perturbation, Fourier derivative k_m=(omega,0,0,kappa).
perturbation = sp.zeros(4, 4)
perturbation[0, 1] = perturbation[1, 0] = e01
perturbation[1, 3] = perturbation[3, 1] = e13
fourier = [w, 0, 0, k]
perturbation_derivatives = [fourier[index] * perturbation for index in range(4)]

Cbar = connection_from_derivatives(background)
Cdelta = connection_from_derivatives(perturbation_derivatives)
Ctotal = [
    [
        [Cbar[ell][m][n] + t * Cdelta[ell][m][n] for n in range(4)]
        for m in range(4)
    ]
    for ell in range(4)
]

T = invariants(Ctotal)
S = sp.expand(T[3] - T[0])  # T4-T1, the concrete MOND-alive direction
S0 = sp.factor(S.subs(t, 0))
S1 = sp.factor(sp.diff(S, t).subs(t, 0))
S2 = sp.factor(sp.diff(S, t, 2).subs(t, 0) / 2)

print("BACKGROUND PRINCIPAL-SYMBOL GATE: nonlinear T4-T1")
print("Tbar =", S0)
print("coefficient of perturbation amplitude =", S1)
print("quadratic coefficient S2 =", S2)

# Let M1=M'(Tbar).  Since S1 vanishes on this background, M'' does not enter
# the vector Hessian at quadratic order: delta^2 M = M1 * S2.
M1 = sp.symbols("M1", real=True)
L2 = sp.expand(M1 * S2)
H = sp.hessian(L2, [e01, e13])
W = sp.Matrix(
    2,
    2,
    lambda i, j: sp.expand(H[i, j]).coeff(w, 2),
)

print("vector Hessian H(e01,e13) =")
sp.pprint(H.applyfunc(sp.factor))
print("time-kinetic matrix W =")
sp.pprint(W.applyfunc(sp.factor))
print("det(W) =", sp.factor(W.det()))
print("det(H) =", sp.factor(H.det()))

# A concrete deep-MOND constitutive representative for this branch.
D = p**2 + 2 * q**2
M1_deep = -sp.Rational(3, 2) * sp.sqrt(D)  # d[(-T)^(3/2)]/dT at Tbar=-4D
W_deep = sp.simplify(W.subs(M1, M1_deep))
print("deep-MOND M(T)=(-T)^(3/2): M'(Tbar) =", M1_deep)
print("deep-MOND W =")
sp.pprint(W_deep.applyfunc(sp.factor))
print("deep-MOND det(W) =", sp.factor(W_deep.det()))
print("condition for a nonzero background: p^2+2q^2 != 0")
print("condition for a nondegenerate MOND principal symbol: M'(Tbar) != 0")
