"""vector-field constructions of the algebras used in lane M (shared by m04, m05): dense structure tensors from polynomial vector fields on (t, x_1..x_d)."""
import numpy as np, sympy as sp, itertools
t = sp.Symbol('t')
def make_coords(d): return (t,) + tuple(sp.symbols('x1:%d' % (d + 1)))
def vfb(A, B, co):
    return [sp.expand(sum(A[v] * sp.diff(B[m], co[v]) - B[v] * sp.diff(A[m], co[v]) for v in range(len(co)))) for m in range(len(co))]
def decompose(field, gens, co):
    names = list(gens); cs = sp.symbols('c0:%d' % len(names)); eqs = []
    for m in range(len(co)):
        expr = sp.expand(field[m] - sum(cs[a] * gens[nm][m] for a, nm in enumerate(names)))
        if expr != 0: eqs += sp.Poly(expr, *co).coeffs()
    if not eqs: return np.zeros(len(names))
    sol = sp.solve(eqs, cs, dict=True)
    if not sol: raise ValueError("not closed")
    return np.array([float(sol[0].get(cs[a], 0)) for a in range(len(names))])
def tensor_from_vf(gens, co):
    names = list(gens); n = len(names); C = np.zeros((n, n, n))
    for a in range(n):
        for b in range(a + 1, n):
            v = decompose(vfb(gens[names[a]], gens[names[b]], co), gens, co)
            C[a, b, :] = v; C[b, a, :] = -v
    return names, C

def fam(d, eps=0, s=0, z=None):
    """generators J, P_i = d_i, K_i = t d_i + eps x_i d_t, H = d_t + s (t^2 d_t + t x.d), optional D_z = z t d_t + x.d.
       eps=0,s=0: Galilei.  s=+-1: Newton-Hooke.  eps=+-1 (s=0): Poincare / Euclid-type.  z: dilatation of exponent z."""
    co = make_coords(d); X = co[1:]; g = {}
    for (i, j) in itertools.combinations(range(d), 2):
        g['J%d%d' % (i + 1, j + 1)] = [0] + [(X[i] if k == j else 0) - (X[j] if k == i else 0) for k in range(d)]
    for i in range(d): g['P%d' % (i + 1)] = [0] + [1 if j == i else 0 for j in range(d)]
    for i in range(d): g['K%d' % (i + 1)] = [eps * X[i]] + [t if j == i else 0 for j in range(d)]
    g['H'] = [1 + s * t ** 2] + [s * t * x for x in X]
    if z is not None: g['D'] = [z * t] + list(X)
    return g, co

def cg(d, l):
    """conformal Galilei algebra of level l (2l integer): H, D = t d_t + l x.d, C = t^2 d_t + 2 l t x.d, P^(n)_i = t^n d_i, J"""
    co = make_coords(d); X = co[1:]; g = {}; l = sp.Rational(l)
    for (i, j) in itertools.combinations(range(d), 2):
        g['J%d%d' % (i + 1, j + 1)] = [0] + [(X[i] if k == j else 0) - (X[j] if k == i else 0) for k in range(d)]
    g['H'] = [sp.Integer(1)] + [0] * d; g['D'] = [t] + [l * x for x in X]; g['C'] = [t ** 2] + [2 * l * t * x for x in X]
    for n_ in range(int(2 * l) + 1):
        for i in range(d): g['P%d_%d' % (n_, i + 1)] = [0] + [t ** n_ if j == i else 0 for j in range(d)]
    return g, co

def so_pq(p, q):
    N = p + q; eta = np.diag([-1.0] * p + [1.0] * q); basis = []
    for i in range(N):
        for j in range(i + 1, N):
            M = np.zeros((N, N)); M[i, j] = eta[j, j]; M[j, i] = -eta[i, i]; basis.append(M)
    n = len(basis); A = np.array([b.flatten() for b in basis]).T
    C = np.zeros((n, n, n))
    for a in range(n):
        for b in range(n):
            com = basis[a] @ basis[b] - basis[b] @ basis[a]
            C[a, b, :] = np.linalg.lstsq(A, com.flatten(), rcond=None)[0]
    return C
def killing_sig(C):
    n = C.shape[0]; ad = [C[a].T for a in range(n)]
    B = np.array([[np.trace(ad[a] @ ad[b]) for b in range(n)] for a in range(n)])
    ev = np.linalg.eigvalsh((B + B.T) / 2); return int((ev < -1e-9).sum()), int((ev > 1e-9).sum())
