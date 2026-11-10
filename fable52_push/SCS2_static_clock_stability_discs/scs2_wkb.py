"""SCS2 route 1: the full covariant WKB symbol of SCS1 (action (A), S = 1, gamma_L = 0, mu_K = 0, coupled to phi and psi) about
general static backgrounds.  Criteria FROZEN_CRITERIA.md (158c4cf770), amendments A1-A3.

The SCS1 route-1 machinery (Hessian of the covariant Lagrangian in the jets, chain-rule coefficient derivatives through N and
its derivative tensors, the symbol, its Hermitian part, the determinant) is executed from SCS1's committed source
(fable52_push/SCS1_static_clock_coupled_stability/scs1_wkb.py at d157012eae), up to its run section: copied, not imported.
1. Item 1: six generic backgrounds with no symmetry (ln N a random cubic in x, y, z), three directions, kr 1e3 and 1e5:
   the symbol against the hand form omega^2 = G (1 - K m)/m (mu_K = 0), G = div Pbar, m = khat.J''.khat (anisotropic).
2. KA3: TPA1's planar slab (N(x) from a point mass's radial profile, decoupled, mu_K*) reproduces TPA1's S = 1 rows.
3. Frozen points on the solved discs (local cubic fit of Phi), coupled symbol and hand form, growth, free fall.
SCS2_MUTATE in {M1, M2, M3}: at the frozen points, M1 G -> -div P, M2 planar divergence, M3 decoupled.
"""
import os, sys, json, math, time, glob, itertools, resource
import numpy as np
import mpmath as mp
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ARM = os.environ.get("SCS2_MUTATE", "")
assert ARM in ("", "M1", "M2", "M3")
ONLY = os.environ.get("SCS2_ONLY", "")                         # "KA1": run only the KA1 frequency block (see below)
assert ONLY in ("", "KA1")
FITMODE = os.environ.get("SCS2_FIT", "")                           # "" frozen (R, z) cubic; "A4": cubic in (ln r, theta[, phi])
assert FITMODE in ("", "A4")
FSUF = "_A4" if FITMODE == "A4" else ""
CACHE = os.environ.get("SCS2_CACHE", os.path.join(HERE, "_cache"))
SCS1 = os.path.join(HERE, "..", "SCS1_static_clock_coupled_stability", "scs1_wkb.py")
src = open(SCS1).read()
ns = {"__file__": os.path.abspath(SCS1), "__name__": "scs1_prefix"}
os.environ.pop("SCS1_MUTATE", None)
exec(src[: src.index('RES = {"lane": "SCS1"')], ns)           # Hessian build (about 4.5 min), symbol tools
sys.path.insert(0, HERE)
import scs2_aqual as S

OUTL = []
def P_(s=""):
    print(s, flush=True); OUTL.append(str(s))
t0 = time.time()
mp.mp.dps = 50
CD, CL, coeff_derivs, merge, add_GR = ns["CD"], ns["CL"], ns["coeff_derivs"], ns["merge"], ns["add_GR"]
symbol, hermitian, det_poly, roots_of, growth = ns["symbol"], ns["hermitian"], ns["det_poly"], ns["roots_of"], ns["growth"]
CKMS = S.C_KMS
IDX3 = [idx for order in range(4) for idx in itertools.combinations_with_replacement(range(3), order)]


def Ntensors_from_phi_derivs(D1, D2, D3, scale):
    """N = exp(Phi/c^2) in code units (length unit 'scale'); D1, D2, D3: Cartesian derivatives of Phi/c^2 (per kpc^n)."""
    a = [D1[i] * scale for i in range(3)]
    b = [[D2[i][j] * scale ** 2 for j in range(3)] for i in range(3)]
    c = [[[D3[i][j][k] * scale ** 3 for k in range(3)] for j in range(3)] for i in range(3)]
    T = {(): mp.mpf(1)}
    for i in range(3): T[(i,)] = a[i]
    for i, j in itertools.combinations_with_replacement(range(3), 2):
        T[(i, j)] = b[i][j] + a[i] * a[j]
    for i, j, k in itertools.combinations_with_replacement(range(3), 3):
        T[(i, j, k)] = c[i][j][k] + b[i][j] * a[k] + b[i][k] * a[j] + b[j][k] * a[i] + a[i] * a[j] * a[k]
    return T


def hand_w2(D1, D2, a0c, khat, scale, mode=""):
    """hand form at mu_K = 0 (code units): omega^2 = G (1 - K m)/m with G = div(grad psi/(1+u)), psi = Phi/c^2."""
    g = np.array([float(x) for x in D1]); H = np.array([[float(x) for x in row] for row in D2])
    gm = np.linalg.norm(g); u = gm / a0c; gh = g / gm
    # div (g/(1+u)) = tr(H)/(1+u) - (g . H . g)/(a0 gm (1+u)^2)
    divP = np.trace(H) / (1 + u) - (g @ H @ g) / (a0c * gm * (1 + u) ** 2)
    if mode == "M1": divP = -divP
    if mode == "M2":                                             # along-field part only: d(p)/ds, p = gm/(1+u)
        dgm = (H @ g) / gm                                       # grad |g|
        divP = (gh @ dgm) / (1 + u) ** 2
    kh = np.array(khat, float); c2 = (kh @ gh) ** 2
    Km = c2 / (1 + u) ** 2 + (1 - c2) / (1 + u)
    w2 = divP * (1 - Km) / Km
    if mode == "M3": w2 = divP / Km                               # decoupled
    return w2 * scale ** 2, divP, u                               # code units (1/scale^2)


def symbol_w2(Ntens, a0_code, kvec, coupled=True):
    params = dict(K=mp.mpf(1), a0=a0_code, mu=mp.mpf(0), Qinf=mp.mpf(1))
    Cs = add_GR(merge(coeff_derivs(CD, Ntens, params), coeff_derivs(CL, Ntens, params)))
    M, flds = symbol(Cs, kvec, decoupled=not coupled)
    rts = roots_of(det_poly(hermitian(M, flds), flds))
    w2 = [complex(r_ ** 2) for r_ in rts]
    return w2, float(growth(rts))


RES = {"lane": "SCS2", "route": 1, "criteria": "158c4cf770", "amendments": ["847f24db0b", "cb6ac0fe9a", "ac13205c89", "3cf66462aa"],
       "mutate_arm": ARM or None, "fit": "A4: cubic in (ln r, theta[, phi])" if FITMODE == "A4" else "frozen: cubic in (R, z) / (x, y, z)"}
P_(f"SCS1 Hessian ready ({time.time()-t0:.0f}s); local fit: {RES['fit']}")

if ARM == "" and ONLY == "" and FITMODE == "":                      # item 1 and KA3 do not use the fit: run once, with the frozen run
    # ---------------- item 1: generic backgrounds with no symmetry
    rng = np.random.default_rng(1)
    rows1 = []
    for seed in range(1, 13):                                     # 1-6 frozen; 7-12 (added, reported) = seeds 1-6 with H negated
        rng = np.random.default_rng(seed if seed <= 6 else seed - 6)
        a0c = 1.0e-7                                              # code units (length unit L)
        g0 = rng.uniform(0.3, 5.0) * a0c * rng.normal(size=3); g0 = g0 / np.linalg.norm(g0) * rng.uniform(0.3, 5.0) * a0c
        H = rng.normal(size=(3, 3)) * a0c; H = 0.5 * (H + H.T)
        if seed > 6: H = -H
        T3 = rng.normal(size=(3, 3, 3)) * a0c
        T3 = sum(np.transpose(T3, p) for p in itertools.permutations(range(3))) / 6
        D1 = [mp.mpf(x) for x in g0]; D2 = [[mp.mpf(x) for x in row] for row in H]
        D3 = [[[mp.mpf(T3[i, j, k]) for k in range(3)] for j in range(3)] for i in range(3)]
        Nt = Ntensors_from_phi_derivs(D1, D2, D3, 1.0)
        gh = g0 / np.linalg.norm(g0)
        q = rng.normal(size=3); q -= (q @ gh) * gh; q /= np.linalg.norm(q)
        o = rng.normal(size=3); o /= np.linalg.norm(o)
        for dname, kh in (("along", gh), ("across", q), ("oblique", o)):
            for kr in (1000, 100000):
                kvec = [mp.mpf(kr) * mp.mpf(x) for x in kh]
                w2s, gr_ = symbol_w2(Nt, mp.mpf(a0c), kvec)
                wh, divP, u = hand_w2(D1, D2, a0c, kh, 1.0)
                best = min(w2s, key=lambda z: abs(z.real - wh)).real if w2s else float("nan")
                rows1.append(dict(seed=seed, u=u, divP=divP, direction=dname, kr=kr, symbol=best, hand=wh,
                                  rel=abs(best - wh) / abs(wh), sign_agree=bool(np.sign(best) == np.sign(wh))))
    frozen = [r_ for r_ in rows1 if r_["seed"] <= 6]
    mx = max(r_["rel"] for r_ in frozen); mx_all = max(r_["rel"] for r_ in rows1)
    RES["item1_general_background"] = dict(rows=rows1, max_rel_frozen_seeds=mx, max_rel_all_seeds=mx_all,
                                           pass_=bool(mx <= 1e-3 and all(r_["sign_agree"] for r_ in frozen)),
                                           added_seeds_pass=bool(mx_all <= 1e-3 and all(r_["sign_agree"] for r_ in rows1)),
                                           negative_G_seeds=sorted({r_["seed"] for r_ in rows1 if r_["divP"] < 0}))
    P_(f"item 1, generic no-symmetry backgrounds: {len(frozen)} frozen rows max rel {mx:.2e}; with the 6 added (H negated) "
       f"{len(rows1)} rows max rel {mx_all:.2e}; seeds with G < 0: {RES['item1_general_background']['negative_G_seeds']} -> "
       f"{'PASS' if RES['item1_general_background']['pass_'] else 'FAIL'} (added: {'PASS' if RES['item1_general_background']['added_seeds_pass'] else 'FAIL'})")

    # ---------------- KA3: TPA1's planar slab
    mustar = lambda foot: mp.mpf(ns["MUK_STAR"][foot]) / mp.mpf(ns["MPC"])
    TP = json.load(open(os.path.join(HERE, "..", "TPA1_two_phase_action", "tpa1_health.json")))
    s1 = [r_ for r_ in TP["phase_rows"] if r_["phase"] == "S1"]
    worst = 0.0; ef = []; cache = {}
    for r_ in s1:
        foot = r_["footing"]; Mb = mp.mpf(10) ** mp.mpf("10.45") * mp.mpf(1.98847e30)
        key = (foot, r_["y"], r_["n_star_over_mean"])
        if key not in cache:
            a0v = mp.mpf(ns["A0"][foot]); rr = mp.sqrt(mp.mpf(ns["G"]) * Mb / (a0v * mp.mpf(str(r_["y"]))))
            nd = mp.mpf(r_["n_star_over_mean"]) * ns["RHO_MEAN"]
            Ntens, params, info = ns["background"](foot, Mb, rr, mustar(foot), nd, "planar")
            cache[key] = (merge(coeff_derivs(CD, Ntens, params), coeff_derivs(CL, Ntens, params)), rr)
        Cs, rr = cache[key]
        kmag = mp.mpf(r_["k_lw"]) / mp.mpf(r_["l_w_m"]) * rr
        kvec = [kmag, 0, 0] if r_["direction"] == "longitudinal" else [0, kmag, 0]
        M, flds = symbol(Cs, kvec, decoupled=True)
        poly = M[("pi", "pi")]; w2 = -mp.re(poly.get(0, 0)) / mp.re(poly.get(2, 0)) / rr ** 2
        worst = max(worst, float(abs(w2 / r_["w2"] - 1)))
        if w2 < 0: ef.append(float(1 / (mp.sqrt(-w2) * mp.mpf(2.99792458e8)) / 3.15576e7))
    ka3 = dict(rows=len(s1), max_rel=worst, efold=[min(ef), max(ef)],
               pass_=bool(worst <= 1e-6 and f"{min(ef):.3g}" == "5.03e+06" and f"{max(ef):.3g}" == "6.25e+08"))
    RES["KA3_planar_slab_TPA1"] = ka3
    P_(f"KA3 planar slab = TPA1: {len(s1)} rows, max rel {worst:.2e}, e-fold {min(ef):.3g} to {max(ef):.3g} yr -> {'PASS' if ka3['pass_'] else 'FAIL'}")

# ---------------- frozen points on the solved discs
FIT = {}
def cubic_fit_axisym(g, Phi, i, j):
    """least-squares cubic in (R - R0, z - z0) over the 5 x 5 cell stencil; returns Phi derivatives at (R0, 0, z0) in
    Cartesian x, y, z (y azimuthal) up to third order, by the axisymmetric chain rule (sympy, built once)."""
    ii = range(max(0, i - 2), min(g.nr, i + 3)); jj = range(max(0, j - 2), min(g.nt, j + 3))
    R0 = g.rc[i] * math.sin(g.tc[j]); z0 = g.rc[i] * math.cos(g.tc[j])
    A = []; b = []
    for a_ in ii:
        for c_ in jj:
            R = g.rc[a_] * math.sin(g.tc[c_]) - R0; z = g.rc[a_] * math.cos(g.tc[c_]) - z0
            A.append([R ** p * z ** q for p in range(4) for q in range(4) if p + q <= 3]); b.append(Phi[a_, c_, 0])
    A = np.array(A); b = np.array(b); scale = max(abs(R0), abs(z0), g.rc[i])
    coef, *_ = np.linalg.lstsq(A / np.array([scale ** (p + q) for p in range(4) for q in range(4) if p + q <= 3]), b, rcond=None)
    coef = coef / np.array([scale ** (p + q) for p in range(4) for q in range(4) if p + q <= 3])
    return coef, R0, z0

xs_, ys_, zs_ = sp.symbols("xs ys zs"); R0s = sp.Symbol("R0", positive=True)
cs_ = sp.symbols("c0:10")
mons = [(p, q) for p in range(4) for q in range(4) if p + q <= 3]
Rexpr = sp.sqrt((R0s + xs_) ** 2 + ys_ ** 2) - R0s
PhiC = sum(cs_[k] * Rexpr ** p * zs_ ** q for k, (p, q) in enumerate(mons))
DER_FN = {}
for order in (1, 2, 3):
    for idx in itertools.combinations_with_replacement(range(3), order):
        e = PhiC
        for t in idx: e = sp.diff(e, (xs_, ys_, zs_)[t])
        DER_FN[idx] = sp.lambdify([R0s] + list(cs_), e.subs({xs_: 0, ys_: 0, zs_: 0}), "mpmath")

def derivs_at(coef, R0):
    c = [mp.mpf(float(x)) for x in coef]; R0m = mp.mpf(float(R0))
    D = {idx: fn(R0m, *c) for idx, fn in DER_FN.items()}
    D1 = [D[(i,)] for i in range(3)]
    D2 = [[D[tuple(sorted((i, j)))] for j in range(3)] for i in range(3)]
    D3 = [[[D[tuple(sorted((i, j, k)))] for k in range(3)] for j in range(3)] for i in range(3)]
    return D1, D2, D3

MON3 = [e for d in range(4) for e in itertools.product(range(4), repeat=3) if sum(e) == d]
def cubic_fit_3d(g, Phi, i, j, l):
    """least-squares cubic in (x, y, z) over the 5 x 5 x 5 cell stencil around cell (i, j, l); derivatives at its centre."""
    x0, y0, z0 = g.X[i, j, l], g.Y[i, j, l], g.Z[i, j, l]
    pts, vals = [], []
    for a_ in range(max(0, i - 2), min(g.nr, i + 3)):
        for b_ in range(max(0, j - 2), min(g.nt, j + 3)):
            for c_ in range(max(0, l - 2), min(g.np_, l + 3)):
                pts.append((g.X[a_, b_, c_] - x0, g.Y[a_, b_, c_] - y0, g.Z[a_, b_, c_] - z0)); vals.append(Phi[a_, b_, c_])
    P = np.array(pts); sc = np.abs(P).max()
    A = np.array([[(p[0] / sc) ** e[0] * (p[1] / sc) ** e[1] * (p[2] / sc) ** e[2] for e in MON3] for p in P])
    coef, *_ = np.linalg.lstsq(A, np.array(vals), rcond=None)
    cf = {e: coef[k] / sc ** sum(e) for k, e in enumerate(MON3)}
    def d(idx):
        e = [0, 0, 0]
        for t in idx: e[t] += 1
        fac = math.factorial(e[0]) * math.factorial(e[1]) * math.factorial(e[2])
        return mp.mpf(float(cf.get(tuple(e), 0.0) * fac))
    D1 = [d((i_,)) for i_ in range(3)]
    D2 = [[d((a, b)) for b in range(3)] for a in range(3)]
    D3 = [[[d((a, b, c)) for c in range(3)] for b in range(3)] for a in range(3)]
    return D1, D2, D3, (x0, y0, z0)


# ---------------- A4 (3cf66462aa): the cubic in the grid's own coordinates u = (ln r, theta, phi), Cartesian derivatives of
# Phi by the exact chain rule (Faa di Bruno to third order) with u's Cartesian derivative tensors from sympy.
_xx, _yy, _zz = sp.symbols("xx yy zz", real=True)
_US = [sp.log(sp.sqrt(_xx ** 2 + _yy ** 2 + _zz ** 2)), sp.atan2(sp.sqrt(_xx ** 2 + _yy ** 2), _zz), sp.atan2(_yy, _xx)]
U_DER = {}
for _a, _ue in enumerate(_US):
    for _order in (1, 2, 3):
        for _idx in itertools.combinations_with_replacement(range(3), _order):
            _e = _ue
            for _t in _idx:
                _e = sp.diff(_e, (_xx, _yy, _zz)[_t])
            U_DER[(_a, _idx)] = sp.lambdify((_xx, _yy, _zz), _e, "math")

def u_tensors(x0, y0, z0):
    u1 = np.zeros((3, 3)); u2 = np.zeros((3, 3, 3)); u3 = np.zeros((3, 3, 3, 3))
    for a in range(3):
        for i in range(3):
            u1[a, i] = U_DER[(a, (i,))](x0, y0, z0)
            for j in range(3):
                u2[a, i, j] = U_DER[(a, tuple(sorted((i, j))))](x0, y0, z0)
                for k in range(3):
                    u3[a, i, j, k] = U_DER[(a, tuple(sorted((i, j, k))))](x0, y0, z0)
    return u1, u2, u3

def sph_fit(g, Phi, i, j, l, centre=None):
    """A4: least-squares cubic in (ln r - ln r0, theta - theta0[, phi - phi0]) over the frozen 5 x 5 (x 5) stencil of cell
    (i, j, l), centred at the cell centre or at centre = (r0, theta0, phi0); returns D1, D2, D3 (Cartesian, per kpc^n) and
    the point (x0, y0, z0)."""
    three = g.np_ > 1
    r0, t0_, p0 = centre if centre is not None else (g.rc[i], g.tc[j], g.pc[l] if three else 0.0)
    nv = 3 if three else 2
    mons = [e for d in range(4) for e in itertools.product(range(4), repeat=nv) if sum(e) == d]
    A = []; b = []
    for a_ in range(max(0, i - 2), min(g.nr, i + 3)):
        for b_ in range(max(0, j - 2), min(g.nt, j + 3)):
            for c_ in (range(max(0, l - 2), min(g.np_, l + 3)) if three else (0,)):
                du = [math.log(g.rc[a_] / r0), g.tc[b_] - t0_] + ([g.pc[c_] - p0] if three else [])
                A.append([np.prod([du[v] ** e[v] for v in range(nv)]) for e in mons]); b.append(Phi[a_, b_, c_])
    coef, *_ = np.linalg.lstsq(np.array(A), np.array(b), rcond=None)
    cf = {e: coef[k] for k, e in enumerate(mons)}
    def F(idx):                                                  # derivative of the polynomial at u = 0
        e = [0] * nv
        for t in idx:
            if t >= nv:
                return 0.0
            e[t] += 1
        return cf.get(tuple(e), 0.0) * np.prod([math.factorial(x) for x in e])
    F1 = np.array([F((a,)) for a in range(3)])
    F2 = np.array([[F((a, c)) for c in range(3)] for a in range(3)])
    F3 = np.array([[[F((a, c, d)) for d in range(3)] for c in range(3)] for a in range(3)])
    x0 = r0 * math.sin(t0_) * math.cos(p0); y0 = r0 * math.sin(t0_) * math.sin(p0); z0 = r0 * math.cos(t0_)
    u1, u2, u3 = u_tensors(x0, y0, z0)
    D1n = np.einsum("a,ai->i", F1, u1)
    D2n = np.einsum("ab,ai,bj->ij", F2, u1, u1) + np.einsum("a,aij->ij", F1, u2)
    D3n = (np.einsum("abc,ai,bj,ck->ijk", F3, u1, u1, u1)
           + np.einsum("ab,aij,bk->ijk", F2, u2, u1) + np.einsum("ab,aik,bj->ijk", F2, u2, u1)
           + np.einsum("ab,ajk,bi->ijk", F2, u2, u1) + np.einsum("a,aijk->ijk", F1, u3))
    D1 = [mp.mpf(float(D1n[i_])) for i_ in range(3)]
    D2 = [[mp.mpf(float(D2n[i_, j_])) for j_ in range(3)] for i_ in range(3)]
    D3 = [[[mp.mpf(float(D3n[i_, j_, k_])) for k_ in range(3)] for j_ in range(3)] for i_ in range(3)]
    return D1, D2, D3, (x0, y0, z0)


def cubic_fit_axisym_at(g, Phi, i, j, R0, z0):
    """as cubic_fit_axisym, but the polynomial is centred at the given (R0, z0) inside the stencil of cell (i, j)."""
    ii = range(max(0, i - 2), min(g.nr, i + 3)); jj = range(max(0, j - 2), min(g.nt, j + 3))
    A = []; b = []
    for a_ in ii:
        for c_ in jj:
            R = g.rc[a_] * math.sin(g.tc[c_]) - R0; z = g.rc[a_] * math.cos(g.tc[c_]) - z0
            A.append([R ** p * z ** q for p in range(4) for q in range(4) if p + q <= 3]); b.append(Phi[a_, c_, 0])
    sc = np.array([max(abs(R0), abs(z0)) ** (p + q) for p in range(4) for q in range(4) if p + q <= 3])
    coef, *_ = np.linalg.lstsq(np.array(A) / sc, np.array(b), rcond=None)
    return coef / sc


# ---------------- KA1 (frozen): the point mass at log M_b 10.45, 30 kpc, reproduces SCS1's route-1 frequencies to 1 %
# (added to this script after the main frozen-point run had started; run alone with SCS2_ONLY=KA1 -> scs2_wkb_KA1.json)
if ARM == "" and ONLY in ("", "KA1"):
    S1 = json.load(open(os.path.join(HERE, "..", "SCS1_static_clock_coupled_stability", "scs1_wkb.json")))
    ref = {}
    for r_ in S1["configs"]["primary_mu0"]["rows"]:
        if r_["point"] == "30 kpc" and r_["logM"] == "10.45" and r_["kr"] == 1000 and r_["direction"] in ("radial", "tangential"):
            ref[(r_["footing"], r_["direction"])] = complex(r_["omega2"][0]).real * (r_["r_kpc"] * 3.0857e19) ** 2
    FROZEN_REF = {("canonical", "radial"): 1.1154e-7, ("canonical", "tangential"): 4.9785e-8}
    ka1 = dict(rows=[], frozen_ref=str(FROZEN_REF))
    for foot in ("canonical", "alt"):
        f = os.path.join(CACHE, f"KA1_point_{foot}.npz")
        bg = S.load_cache(f); g = bg["g"]; c2 = CKMS ** 2; a0 = bg["a0"]
        R0, z0 = 30.0 * math.sin(math.pi / 4), 30.0 * math.cos(math.pi / 4)
        i = int(np.argmin(np.abs(g.rc - 30.0))); j = int(np.argmin(np.abs(g.tc - math.pi / 4)))
        if FITMODE == "A4":
            D1, D2, D3, _ = sph_fit(g, bg["Phi"] / c2, i, j, 0, centre=(30.0, math.pi / 4, 0.0))
        else:
            coef = cubic_fit_axisym_at(g, bg["Phi"] / c2, i, j, R0, z0)
            D1, D2, D3 = derivs_at(coef, R0)
        r_pt = 30.0
        Nt = Ntensors_from_phi_derivs(D1, D2, D3, r_pt)
        gvec = np.array([float(x) for x in D1]); gh = gvec / np.linalg.norm(gvec)
        perp = np.cross(gh, [0, 1, 0]); perp /= np.linalg.norm(perp)
        for dname, kh in (("radial", gh), ("tangential", perp), ("tangential_azimuthal", np.array([0.0, 1.0, 0.0]))):
            kvec = [mp.mpf(1000) * mp.mpf(float(x)) for x in kh]
            w2s, _ = symbol_w2(Nt, mp.mpf(a0 / c2 * r_pt), kvec)
            wh, _, u = hand_w2(D1, D2, a0 / c2, kh, r_pt)
            best = min(w2s, key=lambda z: abs(z.real - wh)).real
            key = (foot, "radial" if dname == "radial" else "tangential")
            rel_scs1 = abs(best / ref[key] - 1)
            rel_frozen = abs(best / FROZEN_REF[key] - 1) if key in FROZEN_REF else None
            ka1["rows"].append(dict(footing=foot, direction=dname, kr=1000, w2_symbol_code=best, w2_hand_code=wh,
                                    scs1_w2_code=ref[key], rel_to_scs1=rel_scs1, rel_to_frozen_number=rel_frozen, u=u))
            P_(f"KA1 freq [{foot} {dname}] omega^2 r^2 = {best:.5e} (hand {wh:.5e}); SCS1 {ref[key]:.5e}; rel {rel_scs1:.2e}"
               + (f"; frozen number rel {rel_frozen:.2e}" if rel_frozen is not None else ""))
    mx = max(r_["rel_to_scs1"] for r_ in ka1["rows"])
    mxf = max(r_["rel_to_frozen_number"] for r_ in ka1["rows"] if r_["rel_to_frozen_number"] is not None)
    ka1.update(max_rel_to_scs1=mx, max_rel_to_frozen_numbers=mxf, pass_=bool(mx <= 1e-2 and mxf <= 1e-2))
    RES["KA1_point_mass_frequencies"] = ka1
    P_(f"KA1 point mass, route-1 frequencies vs SCS1 (30 kpc, kr 1e3): max rel {mx:.2e} (frozen numbers {mxf:.2e}) -> "
       f"{'PASS' if ka1['pass_'] else 'FAIL'}")
    if ONLY == "KA1":
        RES["seconds"] = round(time.time() - t0, 1)
        RES["footer"] = "kappa = 1/2 FITTED; not theory closed. Adopts nothing."
        with open(os.path.join(HERE, f"scs2_wkb_KA1{FSUF}.json"), "w") as fh:
            json.dump(RES, fh, indent=1, default=str)
        P_("kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
        with open(os.path.join(HERE, f"scs2_wkb_KA1{FSUF}.out"), "w") as fh:
            fh.write("\n".join(OUTL) + "\n")
        sys.exit(0)


def frozen_points(bg):
    g = bg["g"]; dp = bg["dp"]; nt = g.nt
    ok = np.isfinite(dp); ok[: S.NMASK if hasattr(S, "NMASK") else 22] = False
    ok[:22] = False; ok[-3:] = False
    plane_rows = [nt - 1, nt - 2] if g.tmode == "half" else [nt // 2 - 2, nt // 2 - 1, nt // 2, nt // 2 + 1]
    ok[:, plane_rows, :] = False
    if g.tmode == "full": ok[:, :1, :] = ok[:, :1, :]
    pts = []
    flat = np.where(ok, dp, np.inf)
    order = np.argsort(flat, axis=None)
    for k in order[:3]:
        i, j, l = np.unravel_index(k, g.shape)
        if dp[i, j, l] < 0: pts.append(("most_negative", i, j, l))
    # sign-change cells: negative cells with a positive neighbour
    sc = []
    for (i, j, l) in zip(*np.nonzero(ok & (dp < 0))):
        nb = [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]
        if any(0 <= a < g.nr and 0 <= b < nt and np.isfinite(dp[a, b, l]) and dp[a, b, l] > 0 for a, b in nb):
            sc.append((i, j, l))
    for (i, j, l) in sc[:: max(1, len(sc) // 3)][:3]:
        pts.append(("sign_change", i, j, l))
    Rd = bg["Rd"]
    def cell_at(r, theta):
        i = int(np.argmin(np.abs(g.rc - r))); j = int(np.argmin(np.abs(g.tc - theta))); return i, j
    j_above = (nt - 3) if g.tmode == "half" else (nt // 2 - 3)
    for (name, r, th) in (("plane_Rd", Rd, None), ("plane_3Rd", 3 * Rd, None), ("axis_Rd", Rd, 0.0), ("45deg_3Rd", 3 * Rd, math.pi / 4)):
        i = int(np.argmin(np.abs(g.rc - r)))
        j = j_above if th is None else int(np.argmin(np.abs(g.tc - th)))
        pts.append((name, i, j, 0))
    return pts

rows = []
files = sorted(f for f in glob.glob(os.path.join(CACHE, "*.npz")) if not f.endswith("_coarse.npz"))
for f in files:
    tag = os.path.basename(f)[:-4]
    bg = S.load_cache(f); g = bg["g"]
    a0 = bg["a0"]; c2 = CKMS ** 2
    for (name, i, j, l) in frozen_points(bg):
        if FITMODE == "A4":
            D1, D2, D3, (x0, y0, z0) = sph_fit(g, bg["Phi"] / c2, i, j, l)
            R0, r_pt = math.hypot(x0, y0), math.sqrt(x0 ** 2 + y0 ** 2 + z0 ** 2)
        elif g.np_ > 1:
            D1, D2, D3, (x0, y0, z0) = cubic_fit_3d(g, bg["Phi"] / c2, i, j, l)
            R0, r_pt = math.hypot(x0, y0), math.sqrt(x0 ** 2 + y0 ** 2 + z0 ** 2)
        else:
            coef, R0, z0 = cubic_fit_axisym(g, bg["Phi"] / c2, i, j)
            D1, D2, D3 = derivs_at(coef, R0)
            r_pt = math.hypot(R0, z0)
        Nt = Ntensors_from_phi_derivs(D1, D2, D3, r_pt)
        a0_code = mp.mpf(a0 / c2 * r_pt)
        gvec = np.array([float(x) for x in D1]); gh = gvec / np.linalg.norm(gvec)
        perp = np.cross(gh, [0, 1, 0]); perp /= max(np.linalg.norm(perp), 1e-300)
        for dname, kh in (("along", gh), ("across", perp), ("azimuthal", np.array([0.0, 1.0, 0.0]))):
            for kr in (10, 1000, 100000):
                kvec = [mp.mpf(kr) * mp.mpf(float(x)) for x in kh]
                wh, divP_fit, u = hand_w2(D1, D2, a0 / c2, kh, r_pt, mode=ARM)
                if ARM in ("", "M3"):
                    w2s, gr_ = symbol_w2(Nt, a0_code, kvec, coupled=(ARM != "M3"))
                    best = min(w2s, key=lambda z: abs(z.real - wh)).real if w2s else float("nan")
                else:
                    best, gr_ = float("nan"), float("nan")
                G_grid = 4 * math.pi * S.G * bg["dp"][i, j, l] / c2           # kpc^-2
                rho_loc = (bg["dp"][i, j, l] + bg["Mc"][i, j, l] / (g.V[i, j, l])) if True else 0
                ff = math.sqrt(4 * math.pi * S.G * abs(rho_loc)) / 1.0         # (km/s)/kpc
                rate = math.sqrt(-wh) / r_pt * CKMS if wh < 0 else 0.0         # (km/s)/kpc
                kmskpc_to_yr = 3.0857e16 / 3.15576e7
                rows.append(dict(tag=tag, point=name, r_kpc=r_pt, R_kpc=R0, z_kpc=z0, direction=dname, kr=kr, u=u,
                                 G_fit_kpc2=divP_fit, G_grid_kpc2=G_grid, w2_hand_code=wh, w2_symbol_code=best,
                                 rel_symbol_hand=(abs(best - wh) / abs(wh) if wh != 0 and best == best else None),
                                 growing=bool(wh < 0), efold_yr=(kmskpc_to_yr / rate if rate > 0 else None),
                                 t_ff_yr=(kmskpc_to_yr / ff if ff > 0 else None),
                                 r_over_vc_yr=r_pt / math.sqrt(max(np.linalg.norm(gvec) * c2 * r_pt, 1e-300)) * kmskpc_to_yr))
    P_(f"[{tag}] points {len(frozen_points(bg))}; growing rows {sum(1 for r_ in rows if r_['tag'] == tag and r_['growing'])}; {time.time()-t0:.0f}s")

RES["rows"] = rows
if ARM in ("", "M3"):
    rels = [r_["rel_symbol_hand"] for r_ in rows if r_["rel_symbol_hand"] is not None and r_["kr"] >= 1000]
    RES["symbol_vs_hand_kr_ge_1e3_max_rel"] = max(rels) if rels else None
    P_(f"frozen points: symbol vs hand (kr >= 1e3) max rel {RES['symbol_vs_hand_kr_ge_1e3_max_rel']}")
RES["seconds"] = round(time.time() - t0, 1)
RES["peak_rss_GB"] = round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9, 3)
RES["footer"] = "kappa = 1/2 FITTED; not theory closed. Adopts nothing."
suffix = (f"_MUTATE_{ARM}" if ARM else "") + FSUF
with open(os.path.join(HERE, f"scs2_wkb{suffix}.json"), "w") as fh:
    json.dump(RES, fh, indent=1, default=str)
P_(f"runtime {RES['seconds']} s, peak RSS {RES['peak_rss_GB']} GB")
P_("kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
with open(os.path.join(HERE, f"scs2_wkb{suffix}.out"), "w") as fh:
    fh.write("\n".join(OUTL) + "\n")

# kappa = 1/2 FITTED; not theory closed. Adopts nothing.
