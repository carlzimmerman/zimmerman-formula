"""Chevalley-Eilenberg cohomology of a finite-dimensional real Lie algebra given by a dense structure tensor C[a,b,e] ([e_a,e_b] = C[a,b,e] e_e).
   H^2(g,R): central extensions.   H^2(g,g): infinitesimal deformations.   Ranks by SVD with an explicit gap report."""
import numpy as np, itertools, scipy.sparse as sps

def jacobi_defect(C):
    n = C.shape[0]
    # [[a,b],c] + [[b,c],a] + [[c,a],b]
    J = np.einsum('abe,ecf->abcf', C, C) + np.einsum('bce,eaf->abcf', C, C) + np.einsum('cae,ebf->abcf', C, C)
    return np.abs(J).max()

def rank_gap(M, tol=None):
    if M.shape[0] == 0 or M.shape[1] == 0: return 0, None, None
    s = np.linalg.svd(M, compute_uv=False)
    if tol is None: tol = max(M.shape) * s[0] * np.finfo(float).eps * 10 if s[0] > 0 else 0
    r = int((s > tol).sum())
    above = s[r - 1] if r > 0 else None
    below = s[r] if r < len(s) else 0.0
    return r, above, below

def pairs(n): return [(a, b) for a in range(n) for b in range(a + 1, n)]
def triples(n): return list(itertools.combinations(range(n), 3))

def H2_trivial(C):
    n = C.shape[0]; P2 = pairs(n); P3 = triples(n); i2 = {p: i for i, p in enumerate(P2)}
    # d1: C^1 (n) -> C^2 : (d phi)(a,b) = - sum_e C[a,b,e] phi(e)
    d1 = np.zeros((len(P2), n))
    for (a, b), r in i2.items():
        d1[r, :] = -C[a, b, :]
    # d2: C^2 -> C^3 : (d psi)(a,b,c) = -psi([a,b],c) + psi([a,c],b) - psi([b,c],a)
    def psi_index(x, y):  # psi(e_x,e_y) as (index, sign) ; zero if x==y
        if x == y: return None
        return (i2[(x, y)], 1) if x < y else (i2[(y, x)], -1)
    d2 = np.zeros((len(P3), len(P2)))
    for r, (a, b, c) in enumerate(P3):
        for (x, y, z, sg) in ((a, b, c, -1), (a, c, b, +1), (b, c, a, -1)):
            for e in range(n):
                co = C[x, y, e]
                if co == 0: continue
                pi = psi_index(e, z)
                if pi is not None: d2[r, pi[0]] += sg * co * pi[1]
    chk = abs(sps.csr_matrix(d2).dot(sps.csr_matrix(d1))).max()
    assert chk < 1e-9, "d2 d1 != 0 (defect %g): structure tensor violates Jacobi?" % chk
    r1 = rank_gap(d1); r2 = rank_gap(d2)
    return len(P2) - r2[0] - r1[0], (r1, r2)

def H2_adjoint(C):
    n = C.shape[0]; P2 = pairs(n); P3 = triples(n); i2 = {p: i for i, p in enumerate(P2)}
    # cochain index for phi in Hom(Lambda^2 g, g): (pair index)*n + m ; also 1-cochains xi in Hom(g,g): a*n + m
    def phi_val(x, y):   # returns list of (base index, sign) for phi(x,y)_m = sum over m of coordinate
        if x == y: return None
        return (i2[(x, y)], 1) if x < y else (i2[(y, x)], -1)
    N2 = len(P2) * n
    # d1: xi -> (d xi)(x,y)_m = [x,xi(y)]_m - [y,xi(x)]_m - xi([x,y])_m
    rows = []; cols = []; vals = []
    for (x, y), pr in i2.items():
        for e in range(n):     # xi(y) = xi_{y,e} e_e ; [x,e_e] = C[x,e,m] e_m
            for m in range(n):
                v = C[x, e, m]
                if v != 0: rows.append(pr * n + m); cols.append(y * n + e); vals.append(v)
                v = C[y, e, m]
                if v != 0: rows.append(pr * n + m); cols.append(x * n + e); vals.append(-v)
        for k in range(n):     # xi([x,y]) = sum_k C[x,y,k] xi(e_k) ; component m
            ck = C[x, y, k]
            if ck == 0: continue
            for m in range(n): rows.append(pr * n + m); cols.append(k * n + m); vals.append(-ck)
    d1 = sps.coo_matrix((vals, (rows, cols)), shape=(N2, n * n)).tocsr()
    # d2
    rows = []; cols = []; vals = []
    for r, (a, b, c) in enumerate(P3):
        base = r * n
        for (x, y, z, sg) in ((a, b, c, +1), (b, a, c, -1), (c, a, b, +1)):
            # sg [x, phi(y,z)]
            pv = phi_val(y, z)
            if pv is None: continue
            for e in range(n):
                for m in range(n):
                    v = C[x, e, m]
                    if v != 0: rows.append(base + m); cols.append(pv[0] * n + e); vals.append(sg * pv[1] * v)
        for (x, y, z, sg) in ((a, b, c, -1), (a, c, b, +1), (b, c, a, -1)):
            for k in range(n):
                ck = C[x, y, k]
                if ck == 0: continue
                pv = phi_val(k, z)
                if pv is None: continue
                for m in range(n): rows.append(base + m); cols.append(pv[0] * n + m); vals.append(sg * ck * pv[1])
    d2 = sps.coo_matrix((vals, (rows, cols)), shape=(len(P3) * n, N2)).tocsr()
    chk = abs(d2 @ d1).max() if d2.shape[0] and d1.shape[1] else 0
    assert chk < 1e-9, "d2 d1 != 0 (defect %g)" % chk
    r1 = rank_gap(d1.toarray()); r2 = rank_gap(d2.toarray())
    return N2 - r2[0] - r1[0], (r1, r2)

def derived_dim(C):
    """dim of [g,g]"""
    n = C.shape[0]
    M = C.reshape(n * n, n)
    return rank_gap(M)[0]

def abelianisation_classes(C):
    """number of cocycle classes supported on g/[g,g]: C(a,2), a = dim g - dim [g,g], provided the complementary generators commute (else 0 is returned with a flag)."""
    n = C.shape[0]; dd = derived_dim(C); a = n - dd
    return a * (a - 1) // 2, a
