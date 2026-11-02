#!/usr/bin/env python3
"""BK1 enumerator: port of hali_flow constrained_search grammar (FROZEN_CRITERIA.md). kappa = 1/2 FITTED; not theory closed."""
import math, numpy as np
C = 299792458.0; G = 6.6743e-11; PI = math.pi
LOG10 = np.log10
NUMS = [("pi", PI), ("2", 2.), ("3", 3.), ("4", 4.), ("6", 6.), ("2pi", 2 * PI), ("4pi", 4 * PI)]
EXPS = [2, 3, .5, -1, -2, 1.5, -.5, 1 / 3, 2 / 3]
UN = [("sqrt", .5), ("cbrt", 1 / 3), ("inv", -1.)] + [(f"pow{e:.4g}", e) for e in EXPS]
BIN = 1e-4; LO = -400.; NB = int((-2 * LO) / BIN) + 1
DIMS = dict(G=(3, -1, -2), c=(1, 0, -1), H0=(0, 0, -1), Lambda=(-2, 0, 0), rho=(-3, 1, 0), rho_c=(-3, 1, 0), a0=(1, 0, -2), f_b=(0, 0, 0), l_P=(1, 0, 0), t_P=(0, 0, 1), m_P=(0, 1, 0))
TARGET_DIMS = dict(none=(0, 0, 0), accel=(1, 0, -2), density=(-3, 1, 0), mass=(0, 1, 0))
def dkey(d): return np.round(np.asarray(d, float) * 720).astype(np.int64)

class Tree:
    """Trees as exponent vectors + log coefficient, with a node table for printing. Dedupe on (dim, value) at 1e-9 relative."""
    def __init__(s, leaves, dims=None):
        s.names = list(leaves); s.k = len(s.names); s.lv = np.array([math.log10(leaves[n]) for n in s.names]); D = dict(DIMS); D.update(dims or {}); s.D = np.array([D[n] for n in s.names], float)
        s.e = np.eye(s.k); s.c = np.zeros(s.k); s.d = np.ones(s.k, int); s.op = [("leaf", i, -1, 0.) for i in range(s.k)]; s.tried = {1: s.k}; s.distinct = {1: s.k}
    def vals(s, e=None, c=None): return (s.e if e is None else e) @ s.lv + (s.c if c is None else c)
    def dimk(s, e=None): return dkey((s.e if e is None else e) @ s.D)
    def _merge(s, E, Cc, Ops, d):
        E0 = np.vstack([s.e, E]); C0 = np.concatenate([s.c, Cc]); v = s.vals(E0, C0); dk = s.dimk(E0); key = np.round(v / 4.3e-10).astype(np.int64)
        order = np.lexsort((np.arange(len(v)), key, dk[:, 2], dk[:, 1], dk[:, 0])); same = np.zeros(len(v), bool); same[order[1:]] = (key[order[1:]] == key[order[:-1]]) & (dk[order[1:]] == dk[order[:-1]]).all(1)
        keep = np.where(~same[len(s.c):])[0]; s.e = np.vstack([s.e, E[keep]]); s.c = np.concatenate([s.c, Cc[keep]]); s.d = np.concatenate([s.d, np.full(len(keep), d)]); s.op += [Ops[i] for i in keep]; s.distinct[d] = len(keep)
    def layer(s, d):
        """depth d from unary and decoration on depth d-1, and binary on all pairs of depth < d."""
        prev = np.where(s.d == d - 1)[0]; n = len(s.d); E, Cc, Ops = [], [], []
        for nm, p in UN:
            E.append(s.e[prev] * p); Cc.append(s.c[prev] * p); Ops += [(nm, int(i), -1, p) for i in prev]
        for nm, x in NUMS:
            for sg, o in ((1, "x"), (-1, "/")):
                E.append(s.e[prev]); Cc.append(s.c[prev] + sg * math.log10(x)); Ops += [(o + nm, int(i), -1, 0.) for i in prev]
        I, J = np.triu_indices(n); E.append(s.e[I] + s.e[J]); Cc.append(s.c[I] + s.c[J]); Ops += [("*", int(i), int(j), 0.) for i, j in zip(I, J)]
        ne = I != J; A = np.concatenate([I, J[ne]]); B = np.concatenate([J, I[ne]]); E.append(s.e[A] - s.e[B]); Cc.append(s.c[A] - s.c[B]); Ops += [("d", int(i), int(j), 0.) for i, j in zip(A, B)]
        E = np.vstack(E); Cc = np.concatenate(Cc); s.tried[d] = len(Cc); s._merge(E, Cc, Ops, d)
    def expr(s, i):
        o, a, b, p = s.op[i]
        if o == "leaf": return s.names[a]
        if o == "*": return f"({s.expr(a)}*{s.expr(b)})"
        if o == "d": return f"({s.expr(a)}/{s.expr(b)})"
        if o[0] == "x": return f"({s.expr(a)}*{o[1:]})"
        if o[0] == "/": return f"({s.expr(a)}/{o[1:]})"
        return f"{o}({s.expr(a)})"

def idx(v): return np.floor((v - LO) / BIN).astype(np.int64)

class Window:
    """Target window on log10 value; Z from sigma, in the linear or the dex convention."""
    def __init__(s, name, value, sigma, dex=False, n=2.):
        s.name, s.value, s.sigma, s.dex, s.n = name, value, sigma, dex, n
        if dex: s.lo, s.hi = value - n * sigma, value + n * sigma
        else: s.lo, s.hi = (math.log10(value - n * sigma) if value > n * sigma else -math.inf), math.log10(value + n * sigma)
    def z(s, lv): return (lv - s.value) / s.sigma if s.dex else (10. ** lv - s.value) / s.sigma

def control_targets(w, M=1000, seed=20261102, span=None):
    """Scrambled targets at the same fractional half-window: LOCAL +- 1 dex, or SPAN over an occupied range."""
    r = np.random.default_rng(seed); c = w.value if w.dex else math.log10(w.value); a, b = (c - 1, c + 1) if span is None else span; t = r.uniform(a, b, M)
    if w.dex: return t + w.lo - w.value, t + w.hi - w.value
    fr = w.n * w.sigma / w.value; return t + (math.log10(1 - fr) if fr < 1 else -1e9), t + math.log10(1 + fr)

def bits_of(P, mult=15):
    return float("inf") if P <= 0 else -math.log2(min(1., P * mult))

def search(T, tdim, windows, cap=200000, G2=False, log=print):
    """Depth 1-3 exact from T; depth 4 binary, unary, decoration, dimension pruned before evaluation; depth 5 decoration of depth 4 in the dimension."""
    tk = dkey(tdim); dk = T.dimk(); v = T.vals(); groups = {}
    for i, row in enumerate(map(tuple, dk)): groups.setdefault(row, []).append(i)
    groups = {k: np.array(x) for k, x in groups.items()}; tt = tuple(tk); n3 = len(v)
    H = {d: np.zeros(NB, np.int64) for d in (1, 2, 3, 4, 5)}
    for d in (1, 2, 3):
        m = (T.d == d) & (dk == tk).all(1)
        if m.any(): np.add.at(H[d], np.clip(idx(v[m]), 0, NB - 1), 1)
    rows = {w.name: [] for w in windows}; zh = {w.name: np.zeros(16, np.int64) for w in windows}; ZE = np.arange(-2, 2.01, .25); stats = dict(dimcorrect={d: int(((T.d == d) & (dk == tk).all(1)).sum()) for d in (1, 2, 3)})
    def take(lv, op, a, b):
        np.add.at(H[4], np.clip(idx(lv), 0, NB - 1), 1)
        for w in windows:
            m = (lv >= w.lo) & (lv <= w.hi)
            if m.any():
                z = w.z(lv[m]); zh[w.name] += np.histogram(z, ZE)[0]; R = rows[w.name]; R.append((lv[m], np.full(m.sum(), op), a[m], b[m]))
                if sum(len(r[0]) for r in R) > 4 * cap:
                    rows[w.name] = [prune(R, w, cap)]
    # depth 4 unary and decoration of depth 3
    L3 = np.where(T.d == 3)[0]; n4d = 0
    dk3 = T.dimk(T.e[L3]); e3 = T.e[L3]; c3 = T.c[L3]
    for u, (nm, p) in enumerate(UN):
        m = (dkey(e3 @ T.D * p) == tk).all(1)
        if m.any(): take((e3[m] @ T.lv + c3[m]) * p, 10 + u, L3[m], L3[m]); n4d += int(m.sum())
    m3 = (dk3 == tk).all(1)
    for u, (nm, x) in enumerate(NUMS):
        if m3.any():
            for sg in (1, -1): take(e3[m3] @ T.lv + c3[m3] + sg * math.log10(x), 30 + u + (0 if sg > 0 else 10), L3[m3], L3[m3]); n4d += int(m3.sum())
    # depth 4 binary on all pairs of depth <= 3, dimension pruned before evaluation
    formal = len(UN) * len(L3) + 2 * len(NUMS) * len(L3) + n3 * (n3 + 1) // 2 + n3 * n3
    for ka, A in groups.items():
        kb_m = tuple(tk - np.array(ka)); kb_d = tuple(np.array(ka) - tk)
        if kb_m in groups:
            B = groups[kb_m]
            if ka <= kb_m:
                for s in range(0, len(A), 4000):
                    a = A[s:s + 4000]; lv = v[a][:, None] + v[B][None, :]; ai = np.repeat(a, len(B)); bi = np.tile(B, len(a)); lv = lv.ravel()
                    if ka == kb_m: mk = bi >= ai; lv, ai, bi = lv[mk], ai[mk], bi[mk]
                    take(lv, 1, ai, bi); n4d += len(lv)
        if kb_d in groups:
            B = groups[kb_d]
            for s in range(0, len(A), 4000):
                a = A[s:s + 4000]; lv = (v[a][:, None] - v[B][None, :]).ravel(); ai = np.repeat(a, len(B)); bi = np.tile(B, len(a)); take(lv, 2, ai, bi); n4d += len(lv)
    # depth 5, decoration of depth 4 in the dimension: shift of the histogram
    for nm, x in NUMS:
        sh = int(round(math.log10(x) / BIN))
        H[5][sh:] += H[4][:-sh]; H[5][:-sh] += H[4][sh:]
    stats["dimcorrect"][4] = n4d; stats["dimcorrect"][5] = 2 * len(NUMS) * n4d
    stats["tried_formal"] = {str(k): int(x) for k, x in T.tried.items()}; stats["tried_formal"]["4"] = int(formal); stats["tried_formal"]["5_dim_only"] = stats["dimcorrect"][5]; stats["distinct"] = {str(k): int(x) for k, x in T.distinct.items()}
    # G2: a + b, |a - b| of equal target dimension over depth <= 3
    HG = None
    if G2 and tt in groups:
        g = groups[tt]; vv = v[g]; HG = np.zeros(NB, np.int64); nn = 0
        for s in range(0, len(g), 2000):
            a = vv[s:s + 2000][:, None]; b = vv[None, :]; mk = np.arange(s, min(s + 2000, len(g)))[:, None] < np.arange(len(g))[None, :]; hi = np.maximum(a, b)[mk]; lo = np.minimum(a, b)[mk]; r = 10. ** (lo - hi); nn += 2 * len(hi)
            np.add.at(HG, np.clip(idx(hi + np.log10(1 + r)), 0, NB - 1), 1); dd = 1 - r; ok = dd > 1e-12; np.add.at(HG, np.clip(idx(hi[ok] + np.log10(dd[ok])), 0, NB - 1), 1)
        stats["G2_tried"] = int(nn)
    return H, HG, rows, zh, stats

def prune(R, w, cap):
    lv = np.concatenate([r[0] for r in R]); op = np.concatenate([r[1] for r in R]); a = np.concatenate([r[2] for r in R]); b = np.concatenate([r[3] for r in R])
    _, u = np.unique(np.round(lv / 4.3e-10).astype(np.int64), return_index=True); lv, op, a, b = lv[u], op[u], a[u], b[u]; o = np.argsort(np.abs(w.z(lv)))[:cap]
    return lv[o], op[o], a[o], b[o]

def cumulative(H, depths=(1, 2, 3, 4, 5)):
    out = {}; run = np.zeros(NB, np.int64)
    for d in depths: run = run + H[d]; out[d] = np.concatenate([[0], np.cumsum(run)])
    return out

def counts(cum, lo, hi):
    a = np.clip(np.ceil((np.asarray(lo) - LO) / BIN).astype(np.int64), 0, NB); b = np.clip(np.floor((np.asarray(hi) - LO) / BIN).astype(np.int64) + 1, 0, NB); return cum[b] - cum[a]

def grade(cum, w, H=None, span=None, M=1000):
    """Real hits vs scrambled at the same fractional window, per cumulative depth; d*, P, bits."""
    lo, hi = control_targets(w, M=M, span=span); R = dict(depth={}); dstar = None
    for d in sorted(cum):
        real = int(counts(cum[d], [w.lo if np.isfinite(w.lo) else -400], [w.hi])[0]); ct = counts(cum[d], lo, hi); P = float((ct > 0).mean()); R["depth"][d] = dict(real=real, ctrl_mean=float(ct.mean()), ctrl_P=P, fdr=(min(1., float(ct.mean()) / real) if real else None))
        if real and dstar is None: dstar = d
    R["dstar"] = dstar
    if dstar is not None: R["P"] = R["depth"][dstar]["ctrl_P"]; R["bits"] = bits_of(R["P"]); R["bits_25"] = bits_of(R["P"], 25)
    width = (w.hi - w.lo) if np.isfinite(w.lo) else float("nan"); R["ceiling_bits"] = math.log2(2. / width) if width > 0 else None; R["window"] = [w.lo, w.hi]
    return R

REG = dict(einstein=8 * PI, friedmann=3., poisson=4 * PI, sheet=2 * PI, sphere=4 * PI / 3, virial=18 * PI ** 2)
def decompose(cf, tol=1e-9):
    """Gate 3, mechanical: cf = product of at most two registry factors of distinct laws at +-{1/2, 1, 2}, times at most one free from {1/2, 2}. Returns list of decompositions."""
    P = [.5, 1., 2., -.5, -1., -2.]; names = list(REG); out = []
    for free, fv in ((None, 1.), ("1/2", .5), ("2", 2.)):
        if abs(cf / fv - 1) < tol: out.append(((), free))
        for i, a in enumerate(names):
            for p in P:
                x = REG[a] ** p * fv
                if abs(cf / x - 1) < tol: out.append((((a, p),), free))
                for b in names[i + 1:]:
                    for q in P:
                        if abs(cf / (x * REG[b] ** q) - 1) < tol: out.append((((a, p), (b, q)), free))
    return out
def mech_rate(M=20000, seed=7):
    """Control: chance a log-uniform O(1) coefficient decomposes at tol 1e-9 is about zero; at the set size, report the size of the reachable set."""
    P = [.5, 1., 2., -.5, -1., -2.]; names = list(REG); S = set()
    for fv in (1., .5, 2.):
        S.add(round(math.log10(fv), 9))
        for i, a in enumerate(names):
            for p in P:
                x = REG[a] ** p * fv; S.add(round(math.log10(x), 9))
                for b in names[i + 1:]:
                    for q in P: S.add(round(math.log10(x * REG[b] ** q), 9))
    return len(S)
