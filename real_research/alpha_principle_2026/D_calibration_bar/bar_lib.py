"""Shared machinery for the calibration bar (lane D). Grammar enumeration, window counting, look-elsewhere.

Grammar (see D_PREREGISTRATION.md): atoms {1..N, pi, e, Z}; unary {sqrt, sq, inv, ln}; binary {+,-,*,/,pow}.
Only positive values are kept. Distinct = relative 1e-12.
"""
import math
import numpy as np

T = 137.035999177          # 1/alpha, Thomson limit (CODATA 2022)
DELTA_CODATA = 1.6e-10     # relative uncertainty
Z = 2.0 * math.sqrt(8.0 * math.pi / 3.0)
LO, HI = 1e-30, 1e30
UN = ["", "sqrt", "sq", "inv", "ln"]
BN = ["+", "-", "*", "/", "^"]


def atoms(N):
    names = [str(i) for i in range(1, N + 1)] + ["pi", "e", "Z"]
    vals = np.array([float(i) for i in range(1, N + 1)] + [math.pi, math.e, Z])
    return names, vals


def clean(v):
    v = np.asarray(v, dtype=float)
    ok = np.isfinite(v) & (v > LO) & (v < HI)
    return ok


def unary(u, x):
    with np.errstate(all="ignore"):
        if u == 0:
            return x.copy()
        if u == 1:
            return np.sqrt(x)
        if u == 2:
            return x * x
        if u == 3:
            return 1.0 / x
        if u == 4:
            r = np.log(x)
            r[~(r > 0)] = np.nan
            return r
    raise ValueError(u)


def binary(op, x, y):
    with np.errstate(all="ignore"):
        if op == 0:
            return x + y
        if op == 1:
            r = x - y
            r[~(r > 0)] = np.nan
            return r
        if op == 2:
            return x * y
        if op == 3:
            return x / y
        if op == 4:
            return np.power(x, y)
    raise ValueError(op)


def dedupe(v, *payload):
    """Sort and keep the first of each group of values within relative 1e-12. Returns (v, *payload)."""
    o = np.argsort(v, kind="stable")
    v = v[o]
    keep = np.ones(v.size, dtype=bool)
    if v.size > 1:
        keep[1:] = (v[1:] - v[:-1]) > 1e-12 * v[1:]
    out = [v[keep]] + [p[o][keep] for p in payload]
    return tuple(out) if payload else out[0]


class Grammar:
    """Holds the enumerated sub-expression sets for a given N."""

    def __init__(self, N):
        self.N = N
        self.anames, self.avals = atoms(N)
        A = len(self.avals)
        # L1: leaves with optional unary decoration
        vals, meta = [], []
        for u in range(5):
            r = unary(u, self.avals)
            ok = clean(r)
            vals.append(r[ok])
            meta.append(np.stack([np.full(ok.sum(), u), np.nonzero(ok)[0]], axis=1))
        v = np.concatenate(vals)
        m = np.concatenate(meta)
        self.L1, m = dedupe(v, m)
        self.L1meta = m
        self.L1s = 5 * A  # syntactic
        # B1
        bv, bi, bj, bo = [], [], [], []
        n = self.L1.size
        ii, jj = np.meshgrid(np.arange(n), np.arange(n), indexing="ij")
        ii = ii.ravel(); jj = jj.ravel()
        for op in range(5):
            r = binary(op, self.L1[ii], self.L1[jj])
            ok = clean(r)
            bv.append(r[ok]); bi.append(ii[ok]); bj.append(jj[ok]); bo.append(np.full(ok.sum(), op))
        self.B1, self.B1i, self.B1j, self.B1o = dedupe(np.concatenate(bv), np.concatenate(bi), np.concatenate(bj), np.concatenate(bo))
        # T1 = B1 and U(B1)
        tv, tb, tu = [], [], []
        for u in range(5):
            r = unary(u, self.B1)
            ok = clean(r)
            tv.append(r[ok]); tb.append(np.nonzero(ok)[0]); tu.append(np.full(ok.sum(), u))
        self.T1, self.T1b, self.T1u = dedupe(np.concatenate(tv), np.concatenate(tb), np.concatenate(tu))
        self.T1s = 5 * (5 * self.L1s ** 2)
        # E1
        self.E1 = dedupe(np.concatenate([self.L1, self.T1]))
        self.E1s = self.L1s + self.T1s

    # ---- B2 blocks (op, order): order 0 = L1 (op) T1 ; order 1 = T1 (op) L1
    def blocks(self):
        for op in range(5):
            yield op, 0
            if op in (1, 3, 4):
                yield op, 1

    def block_values(self, op, order):
        if order == 0:
            X = self.L1[:, None]; Y = self.T1[None, :]
        else:
            X = self.T1[:, None]; Y = self.L1[None, :]
        Xb, Yb = np.broadcast_arrays(X, Y)
        r = binary(op, Xb.ravel(), Yb.ravel())
        return r

    def build_E2(self):
        parts = []
        for op, order in self.blocks():
            r = self.block_values(op, order)
            r = r[clean(r)]
            parts.append(r)
        B2raw = np.concatenate(parts)
        self.B2syn = 2 * 5 * self.L1s * self.T1s  # syntactic B2 count (both orders, 5 ops, before root deco)
        dec = [B2raw]
        for u in range(1, 5):
            r = unary(u, B2raw)
            dec.append(r[clean(r)])
        self.T2 = dedupe(np.concatenate(dec))          # exactly two binary ops, root optionally decorated
        self.T2syn = 5 * self.B2syn
        self.E2 = dedupe(np.concatenate([self.E1, self.T2]))
        self.E2s = self.E1s + self.T2syn
        return self.E2

    def name_L1(self, k):
        u, a = self.L1meta[k]
        base = self.anames[a]
        return base if u == 0 else f"{UN[u]}({base})"

    def name_T1(self, k):
        b = self.T1b[k]; u = self.T1u[k]
        s = f"({self.name_L1(self.B1i[b])} {BN[self.B1o[b]]} {self.name_L1(self.B1j[b])})"
        return s if u == 0 else f"{UN[u]}{s}"

    def find_hits_E2(self, target, tol, limit=50):
        """Names of B2/E1 expressions within tol of target (second pass with provenance)."""
        out = []
        lo, hi = target * (1 - tol), target * (1 + tol)
        for k in np.nonzero((self.E1 > lo) & (self.E1 < hi))[0][:limit]:
            out.append(("E1-value", float(self.E1[k])))
        for op, order in self.blocks():
            r = self.block_values(op, order)
            for u in range(5):
                rr = unary(u, r) if u else r
                idx = np.nonzero((rr > lo) & (rr < hi))[0]
                for q in idx:
                    if order == 0:
                        li, ti = divmod(int(q), self.T1.size)
                        s = f"{self.name_L1(li)} {BN[op]} {self.name_T1(ti)}"
                    else:
                        ti, li = divmod(int(q), self.L1.size)
                        s = f"{self.name_T1(ti)} {BN[op]} {self.name_L1(li)}"
                    s = s if u == 0 else f"{UN[u]}({s})"
                    out.append((s, float(rr[q])))
                    if len(out) >= limit:
                        return out
        return out


def count_window(sorted_vals, center, w):
    return int(np.searchsorted(sorted_vals, center * (1 + w), "right") - np.searchsorted(sorted_vals, center * (1 - w), "left"))


def lam_from_counts(count_w, w, tol):
    """Expected chance hits within relative tol given a count in the relative window w (locally flat density)."""
    return count_w * tol / w


def p_from_lam(lam):
    return -math.expm1(-lam)


def look_elsewhere(density_per_rel, delta_eff, n_targets=1):
    """density_per_rel = distinct grammar values per unit relative deviation near the target. lambda = density * 2 delta * n_targets."""
    lam = density_per_rel * 2.0 * delta_eff * n_targets
    return lam, p_from_lam(lam)


def decoys(n=400, seed=20260928, umin=0.05, umax=1.2):
    rng = np.random.default_rng(seed)
    u = rng.uniform(umin, umax, n) * rng.choice([-1.0, 1.0], n)
    return T * np.exp(u)


# ---------------------------------------------------------------- the bar itself
BAR_P = 1e-3           # look-elsewhere p must be below this
BAR_DELTA = 5e-10      # about 3 x delta_CODATA


def evaluate(delta, N_eff, rho_frac, n_targets=1, predicted_precision=0.0, fitted_reals=0, scale_stated=True):
    """Apply the bar. delta = achieved |v/T-1|; N_eff = declared number of distinct values in the family the formula was drawn from;
    rho_frac = fraction of family values per unit relative deviation near the target (from calibration).
    Returns dict with lambda, p and per-criterion verdicts."""
    delta_eff = max(delta, predicted_precision)
    lam = N_eff * rho_frac * 2.0 * delta_eff * n_targets
    p = p_from_lam(lam)
    c1 = p < BAR_P
    c2 = (delta <= BAR_DELTA) or (predicted_precision > 0 and delta <= 2 * predicted_precision)
    c3 = fitted_reals == 0
    c4 = bool(scale_stated)
    return dict(delta=delta, delta_eff=delta_eff, lam=lam, p=p, c1_lookelsewhere=bool(c1), c2_precision=bool(c2),
                c3_no_fitted_real=bool(c3), c4_scale_stated=c4, clears=bool(c1 and c2 and c3 and c4))


# ---------------------------------------------------------------- MDL-style family size for a candidate expression
def catalan(n):
    return math.comb(2 * n, n) // (n + 1)


def mdl_size(expr, intmax=12, nconst=3):
    """Number of syntactically distinct typed trees of the shape of `expr` in a grammar with integer literals up to
    max(intmax, largest literal in expr), nconst named constants (default 3: pi, e, Z; kappa=1/2 is 1/2), 5 binary ops, 5 unary options (incl. none) at every node.
    For a two-binary-op expression and intmax=12 this equals the E2(12) syntactic count (5.27e8) exactly (checked in d2).
    Returns (log2 size, dict of parts)."""
    import ast
    tree = ast.parse(expr, mode="eval").body
    stats = dict(nb=0, leaves=0, nodes=0, maxint=intmax, unary=0)

    def walk(n):
        if isinstance(n, ast.BinOp) and isinstance(n.op, ast.Pow) and isinstance(n.right, ast.Constant) and n.right.value in (2, 0.5, -1):
            walk(n.left)          # square / sqrt / reciprocal are unary decorations, as in E2
        elif isinstance(n, ast.BinOp):
            stats["nb"] += 1; stats["nodes"] += 1
            walk(n.left); walk(n.right)
        elif isinstance(n, ast.UnaryOp):
            walk(n.operand)
        elif isinstance(n, ast.Call):
            stats["unary"] += 1
            for a in n.args:
                walk(a)
        elif isinstance(n, ast.Constant):
            stats["leaves"] += 1; stats["nodes"] += 1
            v = n.value
            if isinstance(v, int):
                stats["maxint"] = max(stats["maxint"], abs(v))
            else:
                from fractions import Fraction
                fr = Fraction(v).limit_denominator(1000)
                stats["maxint"] = max(stats["maxint"], abs(fr.numerator), fr.denominator)
        elif isinstance(n, ast.Name):
            stats["leaves"] += 1; stats["nodes"] += 1
        else:
            raise ValueError(ast.dump(n))
    walk(tree)
    nb = stats["nb"]
    A = stats["maxint"] + nconst
    nodes = 2 * nb + 1
    lg = math.log2(catalan(nb)) + nb * math.log2(5) + (nb + 1) * math.log2(A) + nodes * math.log2(5)
    stats.update(A=A, log2size=lg)
    return lg, stats


def load_cal(path=None):
    import json, os
    p = path or os.path.join(os.path.dirname(os.path.abspath(__file__)), "calibration.json")
    return json.load(open(p))
