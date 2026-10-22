"""Minimal 3D Riemannian tools with explicit index conventions.

G[u][i][j] = Gamma^u_{ij}
R_ij      = d_k G^k_ij - d_j G^k_ik + G^k_kl G^l_ij - G^k_jl G^l_ik
R         = g^{ij} R_ij
"""
import sympy as sp


def christoffel(g, inv, cs):
    n = len(cs)
    G = [[[sp.S.Zero] * n for _ in range(n)] for _ in range(n)]
    for u in range(n):
        for i in range(n):
            for j in range(n):
                s = sp.S.Zero
                for l in range(n):
                    s += inv[u, l] * (sp.diff(g[i, l], cs[j]) + sp.diff(g[j, l], cs[i])
                                      - sp.diff(g[i, j], cs[l]))
                G[u][i][j] = sp.expand(s / 2)
    return G


def ricci_tensor(g, G, cs):
    n = len(cs)
    Ric = sp.zeros(n, n)
    for i in range(n):
        for j in range(n):
            s = sp.S.Zero
            for k in range(n):
                s += sp.diff(G[k][i][j], cs[k]) - sp.diff(G[k][i][k], cs[j])
                for l in range(n):
                    s += G[k][k][l] * G[l][i][j] - G[k][j][l] * G[l][i][k]
            Ric[i, j] = s
    return Ric


def ricci_scalar(g, cs):
    inv = g.inv()
    G = christoffel(g, inv, cs)
    Ric = ricci_tensor(g, G, cs)
    R = sum(inv[i, j] * Ric[i, j] for i in range(len(cs)) for j in range(len(cs)))
    return sp.simplify(sp.expand(R)), Ric, G


def extrinsic_curvature(h, N, shift, cs, t):
    """K_ij = (1/(2N))(d_t h_ij - D_i N_j - D_j N_i), shift = [N^x,N^y,N^z]."""
    n = len(cs)
    hinv = h.inv()
    G = christoffel(h, hinv, cs)
    K = sp.zeros(n, n)
    for i in range(n):
        for j in range(n):
            cov_shift = sp.diff(shift[j], cs[i]) + sp.diff(shift[i], cs[j])
            for l in range(n):
                cov_shift -= 2 * G[l][i][j] * shift[l]
            K[i, j] = (sp.diff(h[i, j], t) - cov_shift) / (2 * N)
    return sp.simplify(K)


def check():
    x, y, z = sp.symbols('x y z', real=True)
    cs = [x, y, z]
    r2 = x**2 + y**2 + z**2
    Om = 1 / (1 + r2 / 4)
    g = sp.diag(Om**2, Om**2, Om**2)
    R, _, _ = ricci_scalar(g, cs)
    print("  unit S3: R3 =", sp.simplify(R), "(expect 6)")
    f = sp.Function('f')(z)
    g2 = sp.diag(sp.Integer(1), sp.Integer(1), f**2)
    R2, _, _ = ricci_scalar(g2, cs)
    print("  flat reparam diag(1,1,f(z)^2): R3 =", sp.simplify(R2), "(expect 0)")
    A = sp.Function('A')(z)
    g3 = sp.diag(A, sp.Integer(1), sp.Integer(1))
    R3, _, _ = ricci_scalar(g3, cs)
    hand = -sp.diff(A, z, 2) / A + sp.Rational(1, 2) * (sp.diff(A, z) / A) ** 2
    print("  diag(A(z),1,1): R3-hand =", sp.simplify(R3 - hand), "(expect 0)")


if __name__ == "__main__":
    print("validating gr_tools:")
    check()
