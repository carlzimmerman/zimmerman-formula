"""Shared helpers for lane M (two-parameter algebras).  No physics claims live here; every claim is in an m0X script.

Basis order of the rotation-covariant kinematical algebras: J1 J2 J3 K1 K2 K3 P1 P2 P3 H [D].
A Lie algebra is a dict  f[(a,b)] = {e: coeff}  (a<b stored, antisymmetry implied) over sympy or python numbers.
"""
import sympy as sp, itertools

def eps(i, j, k):
    return sp.LeviCivita(i, j, k)

IJ = {'J': 0, 'K': 3, 'P': 6}
IH, ID = 9, 10

def rot_ansatz(par, with_D=True):
    """General rotation-covariant bracket on J,K,P,H(,D).  par = dict of the 21 structure constants (missing -> 0).
       [H,K]=a1 K+a2 P; [H,P]=b1 K+b2 P; [D,K]=p1 K+p2 P; [D,P]=q1 K+q2 P; [D,H]=f1 H+f2 D
       [K_i,K_j]=eps(c1 J+c2 K+c3 P); [P_i,P_j]=eps(d1 J+d2 K+d3 P); [K_i,P_j]=delta_ij(h1 H+h2 D)+eps(e2 J+e3 K+e4 P)
       plus the J-components  [H,K]+= a3 J, [H,P]+= b3 J, [D,K]+= p3 J, [D,P]+= q3 J  (needed for closure under the basis changes K->K+wJ, P->P+wJ)"""
    g = lambda k: par.get(k, 0)
    n = 11 if with_D else 10
    f = {}
    def add(a, b, e, c):
        if c == 0: return
        f.setdefault((a, b), {}); f[(a, b)][e] = f[(a, b)].get(e, 0) + c
    for i in range(3):
        for j in range(3):
            for k in range(3):
                e_ = eps(i, j, k)
                if e_ == 0: continue
                for X in 'JKP':
                    if X == 'J' and i > j: continue
                    add(IJ['J'] + i, IJ[X] + j, IJ[X] + k, e_)      # [J_i,X_j]=eps X_k
                cK = {IJ['J'] + k: g('c1'), IJ['K'] + k: g('c2'), IJ['P'] + k: g('c3')}
                cP = {IJ['J'] + k: g('d1'), IJ['K'] + k: g('d2'), IJ['P'] + k: g('d3')}
                cKP = {IJ['J'] + k: g('e2'), IJ['K'] + k: g('e3'), IJ['P'] + k: g('e4')}
                if i < j:
                    for e, c in cK.items(): add(IJ['K'] + i, IJ['K'] + j, e, e_ * c)
                    for e, c in cP.items(): add(IJ['P'] + i, IJ['P'] + j, e, e_ * c)
                for e, c in cKP.items(): add(IJ['K'] + i, IJ['P'] + j, e, e_ * c)
    # remove duplicated antisym storage of [J,J] (i<j only) handled by normalisation below
    for i in range(3):
        add(IJ['K'] + i, IJ['P'] + i, IH, g('h1'))
        if with_D: add(IJ['K'] + i, IJ['P'] + i, ID, g('h2'))
        add(IH, IJ['K'] + i, IJ['K'] + i, g('a1')); add(IH, IJ['K'] + i, IJ['P'] + i, g('a2')); add(IH, IJ['K'] + i, IJ['J'] + i, g('a3'))
        add(IH, IJ['P'] + i, IJ['K'] + i, g('b1')); add(IH, IJ['P'] + i, IJ['P'] + i, g('b2')); add(IH, IJ['P'] + i, IJ['J'] + i, g('b3'))
        if with_D:
            add(ID, IJ['K'] + i, IJ['K'] + i, g('p1')); add(ID, IJ['K'] + i, IJ['P'] + i, g('p2')); add(ID, IJ['K'] + i, IJ['J'] + i, g('p3'))
            add(ID, IJ['P'] + i, IJ['K'] + i, g('q1')); add(ID, IJ['P'] + i, IJ['P'] + i, g('q2')); add(ID, IJ['P'] + i, IJ['J'] + i, g('q3'))
    if with_D:
        add(ID, IH, IH, g('f1')); add(ID, IH, ID, g('f2'))
    return normalise(f), n

def normalise(f):
    """store each bracket once with a<b; combine [a,b] and -[b,a]."""
    out = {}
    for (a, b), v in f.items():
        if a == b: continue
        if a < b:
            key, s = (a, b), 1
        else:
            key, s = (b, a), -1
        d = out.setdefault(key, {})
        for e, c in v.items():
            d[e] = d.get(e, 0) + s * c
    return out

def br(f, a, b):
    """[a,b] as dict"""
    if a == b: return {}
    if a < b: return dict(f.get((a, b), {}))
    return {e: -c for e, c in f.get((b, a), {}).items()}

def br_vec(f, u, v):
    """bilinear bracket of dict-vectors u,v (basis idx -> coeff)"""
    out = {}
    for a, ca in u.items():
        for b, cb in v.items():
            for e, c in br(f, a, b).items():
                out[e] = out.get(e, 0) + ca * cb * c
    return out

def jacobi_residuals(f, n, expand=True):
    res = []
    for a, b, c in itertools.combinations(range(n), 3):
        tot = {}
        for (x, y, z) in ((a, b, c), (b, c, a), (c, a, b)):
            inner = br(f, x, y)
            for e, ce in inner.items():
                for t, ct in br(f, e, z).items():
                    tot[t] = tot.get(t, 0) + ce * ct
        for t, v in tot.items():
            v = sp.expand(v) if expand else v
            if v != 0: res.append(((a, b, c), t, v))
    return res

def jacobi_polys(f, n):
    """distinct nonzero Jacobi polynomials up to sign"""
    seen = {}
    for _, _, v in jacobi_residuals(f, n):
        p = sp.Poly(v)
        key = sp.srepr(sp.expand(v)); keyn = sp.srepr(sp.expand(-v))
        if key in seen or keyn in seen: continue
        seen[key] = sp.factor(v)
    return list(seen.values())

def is_lie(f, n):
    return len(jacobi_residuals(f, n)) == 0

def dense(f, n):
    """dense structure tensor C[a][b][e] (sympy) with C[a][b][e] = coeff of e in [a,b]"""
    C = [[[0] * n for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for e, c in br(f, a, b).items(): C[a][b][e] = c
    return C

def change_basis(C, T):
    """new generators e'_j = sum_i T[i,j] e_i  ->  structure tensor in the new basis"""
    n = len(C); T = sp.Matrix(T); Ti = T.inv()
    out = [[[0] * n for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            vec = sp.zeros(n, 1)
            for i in range(n):
                for j in range(n):
                    ti = T[i, a] * T[j, b]
                    if ti == 0: continue
                    for e in range(n): vec[e] += ti * C[i][j][e]
            vec = Ti * vec
            for e in range(n): out[a][b][e] = sp.simplify(vec[e])
    return out
