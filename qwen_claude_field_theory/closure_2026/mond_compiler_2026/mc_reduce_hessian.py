"""
mc_reduce_hessian.py -- REDUCTION B: the kinetic Hessian of the carrier multiplet.

Background: Minkowski metric, constant carrier VEVs with a spatial phi-gradient along z
(the MOND background).  Perturbations depend on (t, z).  Expanding to quadratic order,

    L2 = 1/2 [ H_AB d_t Xi_A d_t Xi_B + 2 C_AB d_t Xi_A d_z Xi_B
             + G_AB d_z Xi_A d_z Xi_B + Mm_AB Xi_A Xi_B ]

is extracted for every operator SEPARATELY, as a function of the 7 background parameters
    q     = d_z phi          (MOND field strength)
    chib  = chi
    ab0   = A_0 ,  abz = A_z
    Sa    = S_00 ,  Sd11 = traceless-3d part of S_ij   (axially symmetric, matching the
            static reduction: S_xx = S_yy = Sd11 + Sa/3, S_zz = -2 Sd11 + Sa/3)
    lamb  = lam

Carrier multiplet Xi_A (16 components):
    0  d.phi     1  d.chi
    2..5   d.A_0 d.A_1 d.A_2 d.A_3
    6  d.S_00                       7,8,9  d.S_0i
    10,11,12,13,14  d.S_ij traceless-3d (d11, d22, d12, d13, d23)
    15 d.lam
(the flat tracelessness eta^{mn} S_mn = 0 is imposed exactly by construction)

SCOPE NOTE (recorded, not hidden): the metric is held FIXED at eta, so this is the
CARRIER Hessian in the sense of the target's G5 (H_AB = d^2 L / d(Xi_A-dot) d(Xi_B-dot)).
Curvature-coupled operators (group C) have R = 0 on this background and therefore do NOT
contribute here; a candidate with significant group-C weight gets its Gate-H certificate
downgraded to PARTIAL.
"""
import os
import pickle
import sympy as sp
from mc_core import Ctx, trunc_eps, EPS
from mc_basis import OPS, N_OPS

CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cache_hess.pkl")

NCOMP = 16
COMP_NAMES = ["phi", "chi", "A0", "A1", "A2", "A3",
              "S00", "S01", "S02", "S03", "d11", "d22", "d12", "d13", "d23", "lam"]
BG_NAMES = ["q", "chib", "ab0", "abz", "Sa", "Sd11", "lamb"]


def build():
    t, x, y, z = sp.symbols('t x y z')
    coords = [t, x, y, z]
    q, chib, ab0, abz, Sa, Sd11, lamb = sp.symbols(' '.join(BG_NAMES))

    dfun = [sp.Function(f'd{i}')(t, z) for i in range(NCOMP)]
    d = [EPS * f for f in dfun]   # bookkeeping built into the ansatz

    phi = q * z + d[0]
    chi = chib + d[1]
    A = [ab0 + d[2], d[3], d[4], abz + d[5]]
    lam = lamb + d[15]

    a = Sa + d[6]
    b = [d[7], d[8], d[9]]
    dd11 = Sd11 + d[10]
    dd22 = Sd11 + d[11]
    dd33 = -dd11 - dd22
    dd12, dd13, dd23 = d[12], d[13], d[14]
    c11 = dd11 + a / 3
    c22 = dd22 + a / 3
    c33 = dd33 + a / 3
    S = sp.Matrix([[a,    b[0], b[1], b[2]],
                   [b[0], c11,  dd12, dd13],
                   [b[1], dd12, c22,  dd23],
                   [b[2], dd13, dd23, c33]])

    g = sp.diag(-1, 1, 1, 1)
    ctx = Ctx(coords, g, phi, chi, A, S, lam, build_curvature=False)

    # jet symbols
    e0 = [sp.Symbol(f'e0_{i}') for i in range(NCOMP)]
    e1 = [sp.Symbol(f'e1_{i}') for i in range(NCOMP)]
    e2 = [sp.Symbol(f'e2_{i}') for i in range(NCOMP)]
    subs_map = []
    for i in range(NCOMP):
        subs_map.append((sp.Derivative(dfun[i], t), e1[i]))
        subs_map.append((sp.Derivative(dfun[i], z), e2[i]))
    for i in range(NCOMP):
        subs_map.append((dfun[i], e0[i]))

    def reduce_one(L):
        ex = trunc_eps(L, 2).subs(EPS, 1)
        for aa, bb in subs_map:
            ex = ex.subs(aa, bb)
        ex = sp.expand(ex.doit())
        left = ex.atoms(sp.Derivative) | ex.atoms(sp.Function)
        if left:
            raise RuntimeError(f"unreduced objects: {left}")
        H = [[sp.diff(ex, e1[i], e1[j]) for j in range(NCOMP)] for i in range(NCOMP)]
        G = [[sp.diff(ex, e2[i], e2[j]) for j in range(NCOMP)] for i in range(NCOMP)]
        Mm = [[sp.diff(ex, e0[i], e0[j]) for j in range(NCOMP)] for i in range(NCOMP)]
        Cx = [[sp.diff(ex, e1[i], e2[j]) for j in range(NCOMP)] for i in range(NCOMP)]
        return H, G, Mm, Cx

    allH, allG, allM, allC, labels = [], [], [], [], []
    for k, o in enumerate(OPS):
        H, G, Mm, Cx = reduce_one(o["fn"](ctx))
        allH.append(H); allG.append(G); allM.append(Mm); allC.append(Cx)
        labels.append(o["id"])
        print(f"    [{k+1:2d}/{N_OPS}] {o['id']:5s} {o['label'][:52]}")

    flat = []
    for T in (allH, allG, allM, allC):
        for Mo in T:
            for i in range(NCOMP):
                for j in range(NCOMP):
                    flat.append(Mo[i][j])
    data = dict(labels=labels, flat_str=[sp.srepr(e) for e in flat],
                bg_names=BG_NAMES, comp_names=COMP_NAMES, ncomp=NCOMP, nops=N_OPS)
    with open(CACHE, "wb") as fh:
        pickle.dump(data, fh)
    print(f"  symbolic hessian cached -> {CACHE}")
    return _lambdify(data)


def _lambdify(data):
    bg = [sp.Symbol(s) for s in data["bg_names"]]
    flat = [sp.sympify(s) for s in data["flat_str"]]
    print("  lambdifying hessian tensors ...")
    fn = sp.lambdify(bg, flat, modules="numpy", cse=True)
    return dict(labels=data["labels"], fn=fn, ncomp=data["ncomp"], nops=data["nops"],
                bg_names=data["bg_names"], comp_names=data["comp_names"])


_RT = {}


def load():
    if _RT:
        return _RT
    if not os.path.exists(CACHE):
        r = build()
    else:
        with open(CACHE, "rb") as fh:
            data = pickle.load(fh)
        r = _lambdify(data)
    _RT.update(r)
    return r


def tensors(bgvals):
    """returns H,G,M,C each of shape (n_ops, NCOMP, NCOMP) at the given background."""
    import numpy as np
    r = load()
    v = np.asarray(r["fn"](*bgvals), dtype=float)
    n = r["nops"]
    v = v.reshape(4, n, NCOMP, NCOMP)
    return v[0], v[1], v[2], v[3]


if __name__ == "__main__":
    import time
    t0 = time.time()
    build()
    print(f"built in {time.time()-t0:.1f} s")
