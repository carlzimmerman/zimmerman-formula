"""Set-function algebra for qubit creation operators (disjoint-union product), n <= 16.
f: complex array of length 2^n indexed by bitmask.  (f*g)(M) = sum_{K subset M} f(K) g(M\\K).
exp/log computed per-subset in the ranked zeta domain (truncated polynomials)."""
import numpy as np

def popcount_table(n):
    m = np.arange(1 << n)
    pc = np.zeros(1 << n, dtype=np.int64)
    for i in range(n):
        pc += (m >> i) & 1
    return pc

def ranked(f, n, pc):
    R = np.zeros((n + 1, 1 << n), dtype=complex)
    R[pc, np.arange(1 << n)] = f
    return R

def zeta(R, n, sign=+1):
    R = R.copy()
    for i in range(n):
        a = R.reshape(R.shape[0], 1 << (n - i - 1), 2, 1 << i)
        a[:, :, 1, :] += sign * a[:, :, 0, :]
    return R

def unranked(R, n, pc):
    return R[pc, np.arange(1 << n)]

def poly_mul(A, B, n):
    C = np.zeros_like(A)
    for a in range(n + 1):
        C[a:] += A[a][None, :] * B[: n + 1 - a]
    return C

def poly_exp(P, n):
    # P[0] must be 0 ; e_m = (1/m) sum_{j=1}^m j p_j e_{m-j}
    E = np.zeros_like(P); E[0] = 1.0
    for m in range(1, n + 1):
        acc = np.zeros(P.shape[1], dtype=complex)
        for j in range(1, m + 1):
            acc += j * P[j] * E[m - j]
        E[m] = acc / m
    return E

def conv(f, g, n, pc):
    A = zeta(ranked(f, n, pc), n); B = zeta(ranked(g, n, pc), n)
    return unranked(zeta(poly_mul(A, B, n), n, -1), n, pc)

def sexp(c, n, pc):
    """exp(C) as set function (value 1 at empty set); c[0] must be 0"""
    A = zeta(ranked(c, n, pc), n)
    return unranked(zeta(poly_exp(A, n), n, -1), n, pc)
