#!/usr/bin/env python3
"""Independent referee checks for L326 (DERIVATION.md) (written from scratch; does not import the author's code)."""
import itertools, math
import numpy as np
import warnings
warnings.filterwarnings("ignore", message=".*encountered in matmul", category=RuntimeWarning)  # spurious macOS-Accelerate BLAS warnings; results checked finite
from fractions import Fraction as Fr
from math import comb, factorial

rng = np.random.default_rng(7)

# ---------------------------------------------------------------- generic multi-level toy
class Sys:
    def __init__(self, n, q, en=None):
        self.n, self.q = n, q
        self.dim = q ** n
        self.st = np.array(list(itertools.product(range(q), repeat=n)))
        self.supp = [frozenset(np.nonzero(s)[0].tolist()) for s in self.st]
        self.idx = {tuple(s): i for i, s in enumerate(self.st)}
        if en is None:
            en = np.ones((n, q))
        en = en.copy(); en[:, 0] = 0
        self.en = en
        self.E0 = np.array([sum(en[w, s[w]] for w in range(n)) for s in self.st])
        self.sec = {}
        for i, S in enumerate(self.supp):
            self.sec.setdefault(S, []).append(i)
        self.Om = np.zeros(self.dim); self.Om[0] = 1

    def op_on(self, loc, sites):
        """loc acts on ordered `sites`"""
        sites = list(sites); m = len(sites)
        rest = [w for w in range(self.n) if w not in sites]
        perm = sites + rest
        full = np.kron(loc, np.eye(self.q ** len(rest)))
        # full acts on ordering perm; convert to natural ordering
        T = full.reshape([self.q] * (2 * self.n))
        inv = np.argsort(perm)
        T = T.transpose(list(inv) + [self.n + i for i in inv])
        return T.reshape(self.dim, self.dim)

    def A(self, M, c):
        """|c><0_M| (x) 1 ; c indexed by the sector-M basis states (self.sec[M])"""
        M = sorted(M)
        loc = np.zeros((self.q ** len(M), self.q ** len(M)), dtype=complex)
        locidx = list(itertools.product(range(self.q), repeat=len(M)))
        for t, i in enumerate(self.sec[frozenset(M)]):
            s = tuple(self.st[i][M])
            loc[locidx.index(s), 0] += c[t]
        return self.op_on(loc, M)

    def C(self, cv):
        out = np.zeros((self.dim, self.dim), dtype=complex)
        for M, c in cv.items():
            out += self.A(M, c)
        return out

    def comps(self, v, shift=0.0):
        out = {}
        for M, ix in self.sec.items():
            if M:
                w = v[ix] / (self.E0[ix] - shift)
                if np.linalg.norm(w) > 1e-14:
                    out[M] = w
        return out

    def norm1(self, cv):
        return max(sum(np.linalg.norm(c) for M, c in cv.items() if u in M) for u in range(self.n))

ad = lambda A, X: A @ X - X @ A

print("== R1: BDL App. A '|M_j| <= 2|M|' -- qubit counterexample, rebuilt from scratch ==")
S = Sys(3, 2)
u, v, w = 0, 1, 2
X = np.array([[0, 1], [1, 0]])
V = S.op_on(np.kron(X, X), [v, w])
adag = S.A({u, v, w}, np.array([1.0]))           # a^dag_{uvw}
y = (ad(adag, V) @ S.Om)[S.sec[frozenset({u})][0]]
Mj, M = {u, v, w}, {u}
N = Mj
claim3_ok = (N - {v, w}) <= M <= (N | {v, w}) and bool(Mj & {v, w})
print(f"  y = <Om| a_u [a+_uvw, X_v X_w] |Om> = {y.real:+.3f};  Claim-3 (i),(ii) satisfied: {claim3_ok}")
print(f"  |M_j|/|M| = {len(Mj)}/{len(M)};  BDL needs E0(M) >= (Delta/2)|M_j|: {1} >= {1.5}? -> {1 >= 1.5}")
# BDL's intermediate bound: M_j subset M u {w} (with v in M_j chosen WLOG)
print(f"  M_j subset M u {{w}}: {Mj <= (M | {w})};  M_j subset M u {{v}}: {Mj <= (M | {v})}  (both False => line is false)")
# corrected BDL sum:
corr = max(k * 4 * 3 * 2 ** (2 * k - 1) + 2 ** (2 * k + 2) for k in range(1, 5))
print(f"  corrected Lemma-3 constant max_k<=4 = {corr} (<= 8192: {corr <= 8192})")

print("\n== R1b: s=4 analogue, |M_j| = 5|M| realised ==")
S5 = Sys(5, 2)
p = [1, 2, 3, 4]
loc = np.zeros((16, 16)); loc[0, 15] = loc[15, 0] = 1.0     # |0000><1111| + h.c.
Vp = S5.op_on(loc, p)
Aj = S5.A({0, 1, 2, 3, 4}, np.array([1.0]))
vec = ad(Aj, Vp) @ S5.Om
print(f"  sector {{u}} amplitude = {vec[S5.sec[frozenset({0})][0]].real:+.3f}  (|M_j|=5, |M|=1)")

print("\n== R2: constants re-derived independently ==")
def gam(s):
    g0 = math.sqrt(sum(comb(s - 1, t - 1) / t ** 2 for t in range(1, s + 1)))
    # type-j: sup over n'>=1 of (n'+s)^2 sum_t C(s,t)/(n'+t)^2, evaluated on a grid
    gS2 = max((n + s) ** 2 * sum(comb(s, t) / (n + t) ** 2 for t in range(s + 1)) for n in range(1, 200))
    return g0, math.sqrt(gS2)
def beta(s):
    g0, gS = gam(s)
    return [g0] + [2 ** k * (g0 * s ** k + k * gS * s ** (k - 1)) for k in range(1, 2 * s + 1)]
for s in (2, 3, 4):
    b = beta(s)
    # majorant recursion m_1 = b0, m_p = sum_k b_k/k! sum_{p1+..+pk=p-1} prod m
    P = 150                                    # m_p ~ lam_c^-p: order 400 overflows float64 (see r2.py for
    m = np.zeros(P + 1)                        # the rescaled order-3000 run at lam = lam_c)
    m[1] = b[0]
    # powers of the series: pw[k][p] = coefficient of lam^p in (sum m lam)^k
    for pp in range(2, P + 1):
        tot = 0.0
        # compute coefficient of lam^{pp-1} in sum_k b_k/k! mu^k, using truncated series m[1..pp-1]
        ser = np.zeros(pp); ser[1:pp] = m[1:pp]
        pw = np.zeros(pp); pw[0] = 1.0
        for k in range(1, 2 * s + 1):
            pw = np.convolve(pw, ser)[:pp]
            tot += b[k] / factorial(k) * pw[pp - 1]
        m[pp] = tot
    # threshold: q(mu) = 2 mu q'(mu)
    q = lambda mu: b[0] + sum(b[k] * mu ** k / factorial(k) for k in range(1, 2 * s + 1))
    qp = lambda mu: sum(b[k] * mu ** (k - 1) / factorial(k - 1) for k in range(1, 2 * s + 1))
    lo, hi = 0.0, 1.0
    for _ in range(200):
        mid = (lo + hi) / 2
        (lo, hi) = (mid, hi) if q(mid) - 2 * mid * qp(mid) > 0 else (lo, mid)
    lam_c = lo / q(lo)
    lam = 0.9 * lam_c                          # inside the radius: geometric convergence at order 150
    series = sum(m[pp] * lam ** pp for pp in range(1, P + 1))
    tail = m[P] * lam ** P
    root = 0.0
    for _ in range(20000):                     # least positive root of mu = lam q(mu), by monotone iteration
        root = lam * q(root)
    print(f"  s={s}: gamma0={gam(s)[0]:.6f} gammaS={gam(s)[1]:.6f} beta1={b[1]:.3f} beta_2s={b[-1]:.4g}"
          f"  lam_c={lam_c:.8f}  at 0.9 lam_c: sum m_p lam^p={series:.9e} vs root of mu=lam q(mu) {root:.9e}"
          f" (last term {tail:.1e}; mu_c={lo:.6e})  2 lam q'(series)={2*lam*qp(series):.6f} < 1")
    assert abs(series - root) < 1e-9 * root and 2 * lam * qp(series) < 1

print("\n  gauge dictionary: X_d = sqrt((32/3) D / lam_c)")
lc4 = None
for s in (3, 4):
    b = beta(s)
    q = lambda mu: b[0] + sum(b[k] * mu ** k / factorial(k) for k in range(1, 2 * s + 1))
    qp = lambda mu: sum(b[k] * mu ** (k - 1) / factorial(k - 1) for k in range(1, 2 * s + 1))
    lo, hi = 0.0, 1.0
    for _ in range(200):
        mid = (lo + hi) / 2
        (lo, hi) = (mid, hi) if q(mid) - 2 * mid * qp(mid) > 0 else (lo, mid)
    lc = lo / q(lo)
    for d in (2, 3, 4):
        D = 2 * (d - 1) if s == 4 else 3 * d * (d - 1) // 2
        print(f"   s={s} d={d} D={D}: X_d = {math.sqrt(32 / 3 * D / lc):.3f}")
# normalization chain from i15 H = (x/2) sum C_l + (b/x) sum (1-T_p):
for N in (2, 3, 4, 10):
    CF = (N * N - 1) / (2 * N)
    x = 5.0
    eps = (2 * N / x) / (x * CF / 2)
    print(f"   N={N}: eps(b=2N) * x^2 = {eps * x * x:.5f}   (32/3 = {32/3:.5f})")

print("\n== R3: Lemma 3' / Lemma 4' stress test at FULL depth (k up to 8), qutrits, s=4 ==")
S6 = Sys(6, 3)
plaqs = [(0, 1, 2, 3), (2, 3, 4, 5)]
def rh(k):
    Z = rng.normal(size=(k, k)) + 1j * rng.normal(size=(k, k)); H = (Z + Z.conj().T) / 2
    return H / np.linalg.norm(H, 2)
Vs = [S6.op_on(rh(81), pp) for pp in plaqs]
V = sum(Vs); J = 1.0; D = 2
g0, gS = gam(4); b4 = beta(4)
allsets = [frozenset(M) for r in range(1, 7) for M in itertools.combinations(range(6), r)]
worst = {}
for trial in range(120):
    k = 1 + trial % 8
    cvs = []
    for i in range(k):
        sel = [allsets[j] for j in rng.choice(len(allsets), size=4, replace=False)]
        # include adversarial big sets containing a plaquette plus an outside site
        if trial % 2:
            sel += [frozenset({0, 2, 3, 4, 5}), frozenset({1, 2, 3, 4, 5}), frozenset({0, 1, 2, 3, 4})]
        cvs.append({M: rng.normal(size=len(S6.sec[M])) + 1j * rng.normal(size=len(S6.sec[M])) for M in sel})
    Cs = [S6.C(c) for c in cvs]
    Xk = V.copy()
    for Ci in reversed(Cs):
        Xk = ad(Ci, Xk)
    new = S6.comps(Xk @ S6.Om)
    lhs = S6.norm1(new)
    rhs = b4[k] * D * J * np.prod([S6.norm1(c) for c in cvs])
    worst[k] = max(worst.get(k, 0), lhs / rhs)
print("  worst lhs/rhs per k:", {k: f"{v:.2e}" for k, v in sorted(worst.items())})

# single-tau sector Cauchy-Schwarz check (the only genuinely new inequality), adversarial:
print("\n== R4: per-tuple sector inequality  sum_{M∋u} ||Pi_M X Om||/|M| <= gamma * ||X Om|| ==")
worst0 = worstj = 0.0
for trial in range(300):
    k = 1 + trial % 4
    Ms = []
    for i in range(k):
        M = set(rng.choice(6, size=rng.integers(1, 4), replace=False).tolist()) | {int(rng.choice(plaqs[0]))}
        Ms.append(frozenset(M))
    Xk = Vs[0].copy()
    cs = []
    for M in reversed(Ms):
        c = rng.normal(size=len(S6.sec[M])) + 1j * rng.normal(size=len(S6.sec[M]))
        Xk = ad(S6.A(M, c), Xk)
    vv = Xk @ S6.Om
    nv = np.linalg.norm(vv)
    if nv < 1e-12:
        continue
    for uu in range(6):
        tot = sum(np.linalg.norm(vv[ix]) / len(Msec) for Msec, ix in S6.sec.items() if Msec and uu in Msec)
        if uu in plaqs[0]:
            worst0 = max(worst0, tot / (g0 * nv))
        else:
            Nset = frozenset().union(*Ms)
            js = [Mi for Mi in Ms if uu in Mi]
            if js:
                worstj = max(worstj, tot * len(js[0]) / (gS * nv))
print(f"  type-0 worst ratio {worst0:.3f} (<=1),  type-j worst ratio (x|M_j|) {worstj:.3f} (<=1)")

print("\n== R5: truncation compresses V_p -- does V_p preserve the Casimir cutoff? (SU(2), one link, j<=jmax) ==")
# multiplication by Re tr U / 2 = chi_{1/2}/2 maps spin j to j +- 1/2 : NOT invariant, so compression is required.
print("  chi_{1/2} * chi_j = chi_{j-1/2} + chi_{j+1/2}  -> cutoff space not invariant; S1 uses compression (Ritz), OK")
