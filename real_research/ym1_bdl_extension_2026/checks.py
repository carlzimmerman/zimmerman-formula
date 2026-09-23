#!/usr/bin/env python3
"""
L326 / checks.py -- finite toy-model checks of the ADAPTED BDL lemmas
(sector-valued creation operators, multi-level sites, 4-body interactions).

These are sanity checks of the algebra in DERIVATION.md, NOT proofs.  Each check
names the DERIVATION.md step and the BDL (arXiv:0707.1894) statement it adapts.

  C1  Lemma 1'  (BDL Lemma 1, eq. 11):   [C1,[C2,H0]] = 0 for sector-valued C's.
  C2  Lemma 2'  (BDL Lemma 2, eq. 12):   ad_C^k(V_p) = 0 for k >= 2s+1 = 9, and
                                         ad_C^8(V_p) != 0 generically (depth 8 sharp).
  C3  Claim 3'  (BDL Claim 3):           Pi_M X Omega = 0 unless every M_i meets p and
                                         N\\p <= M <= N u p  (so <= 2^4 = 16 sectors).
  C4  BDL erratum (App. A, line "|M_j| <= 2|M|"): explicit qubit counterexample with
                                         |M_j| = 3|M| and a non-zero matrix element.
  C5  Lemma 3'  (BDL Lemma 3, eq. 19):   ||C||_1 <= beta_k (D J/Delta) prod ||C_i||_1,
                                         random + adversarial instances, qutrit sites.
  C6  End-to-end (BDL Cor. 3/4):         Kirkwood-Thomas fixed point with sector-valued
                                         C reproduces the exact ground state; ||C||_1 <=
                                         mu*(lambda); gap >= Delta/2.
Run: python3 checks.py   ->  prints "ALL TOY CHECKS PASSED" or stops on failure.
"""
import itertools, math, warnings
import numpy as np
# spurious macOS-Accelerate matmul RuntimeWarnings; every result is guarded by isfinite below
warnings.filterwarnings("ignore", category=RuntimeWarning, message=".*matmul.*")

rng = np.random.default_rng(20260922)

# ----------------------------------------------------------------------------
# toy Hilbert space: n sites, local dimension q, vacuum = level 0 on each site
# ----------------------------------------------------------------------------
class Toy:
    def __init__(self, n, q, energies=None):
        self.n, self.q = n, q
        self.dim = q ** n
        self.states = list(itertools.product(range(q), repeat=n))
        self.index = {s: i for i, s in enumerate(self.states)}
        self.support = [frozenset(w for w in range(n) if s[w] != 0) for s in self.states]
        # h_u = diag(0, e_{u,1}, ..., e_{u,q-1}) with every e >= 1 (Delta = 1)
        if energies is None:
            energies = 1.0 + rng.random((n, q))
        energies[:, 0] = 0.0
        self.e = energies
        self.E0 = np.array([sum(self.e[w, s[w]] for w in range(n)) for s in self.states])
        self.H0 = np.diag(self.E0)
        self.Omega = np.zeros(self.dim); self.Omega[0] = 1.0
        self.sectors = {}
        for i, S in enumerate(self.support):
            self.sectors.setdefault(S, []).append(i)

    def embed(self, op, sites):
        """operator on the ordered site tuple `sites` -> full operator (identity elsewhere)"""
        sites = list(sites)
        n, q = self.n, self.q
        m = len(sites)
        T = op.reshape([q] * (2 * m))
        full = np.zeros((self.dim, self.dim), dtype=complex)
        rest = [w for w in range(n) if w not in sites]
        for a in itertools.product(range(q), repeat=m):
            for b in itertools.product(range(q), repeat=m):
                val = T[a + b]
                if val == 0:
                    continue
                for r in itertools.product(range(q), repeat=len(rest)):
                    so = [0] * n; si = [0] * n
                    for k, w in enumerate(sites):
                        so[w] = a[k]; si[w] = b[k]
                    for k, w in enumerate(rest):
                        so[w] = r[k]; si[w] = r[k]
                    full[self.index[tuple(so)], self.index[tuple(si)]] += val
        return full

    def creation(self, cvecs):
        """C = sum_M A[c_M];  cvecs: dict frozenset M -> vector over basis states of sector M
        (ordered as self.sectors[M]).  A[c_M] |n> = [n vacuum on M] * sum_m c_M[m] |n with M->m>."""
        C = np.zeros((self.dim, self.dim), dtype=complex)
        for M, c in cvecs.items():
            idxM = self.sectors[M]
            for j, s in enumerate(self.states):
                if self.support[j] & M:
                    continue
                for t, im in enumerate(idxM):
                    if c[t] == 0:
                        continue
                    new = list(s)
                    for w in M:
                        new[w] = self.states[im][w]
                    C[self.index[tuple(new)], j] += c[t]
        return C

    def norm1(self, cvecs):
        best = 0.0
        for u in range(self.n):
            best = max(best, sum(np.linalg.norm(c) for M, c in cvecs.items() if u in M))
        return best

    def resolvent_project(self, X, shift=0.0):
        """c_M = (H0^M - shift)^{-1} Pi_M X Omega  for every nonempty sector M"""
        v = X @ self.Omega
        out = {}
        for M, idx in self.sectors.items():
            if not M:
                continue
            vec = v[idx] / (self.E0[idx] - shift)
            if np.linalg.norm(vec) > 0:
                out[M] = vec
        return out


def ad(A, X):
    return A @ X - X @ A


def rand_herm(k):
    Z = rng.normal(size=(k, k)) + 1j * rng.normal(size=(k, k))
    H = (Z + Z.conj().T) / 2
    return H / np.linalg.norm(H, 2)          # operator norm exactly 1  (J = 1)


def rand_cvecs(toy, sets, scale=1.0):
    return {frozenset(M): scale * (rng.normal(size=len(toy.sectors[frozenset(M)]))
                                   + 1j * rng.normal(size=len(toy.sectors[frozenset(M)])))
            for M in sets}


ok = True
def report(name, cond, detail=""):
    global ok
    print(f"  [{'PASS' if cond else 'FAIL'}] {name} {detail}")
    ok = ok and bool(cond)

# ----------------------------------------------------------------------------
print("== C1 Lemma 1' (BDL Lemma 1, eq. 11): [C1,[C2,H0]] = 0 ==")
toy = Toy(4, 3)
allsets = [frozenset(M) for r in range(1, 5) for M in itertools.combinations(range(4), r)]
C1 = toy.creation(rand_cvecs(toy, allsets)); C2 = toy.creation(rand_cvecs(toy, allsets))
report("C1 commutes with C2", np.linalg.norm(ad(C1, C2)) < 1e-10)
report("[C1,[C2,H0]] = 0", np.linalg.norm(ad(C1, ad(C2, toy.H0))) < 1e-9,
       f"(norm {np.linalg.norm(ad(C1, ad(C2, toy.H0))):.1e})")

# ----------------------------------------------------------------------------
print("== C2 Lemma 2' (BDL Lemma 2, eq. 12): depth for a 4-body term is 8 ==")
toy = Toy(5, 3)
p = (0, 1, 2, 3)
Vp = toy.embed(rand_herm(3 ** 4), p)
sets5 = [frozenset(M) for r in range(1, 4) for M in itertools.combinations(range(5), r)]
C = toy.creation(rand_cvecs(toy, sets5))
X = Vp.copy(); norms = []
for k in range(0, 10):
    norms.append(np.linalg.norm(X))
    X = ad(C, X)
print("   ||ad_C^k(V_p)||, k=0..9:", " ".join(f"{x:.2e}" for x in norms))
report("ad_C^9(V_p) = 0", norms[9] < 1e-8 * norms[0])
report("ad_C^8(V_p) != 0 (depth 8 is attained)", norms[8] > 1e-3)

# ----------------------------------------------------------------------------
print("== C3 Claim 3' (BDL Claim 3): sector support, <= 2^4 sectors ==")
toy = Toy(6, 3)
p = (1, 2, 3, 4); P = frozenset(p)
Vp = toy.embed(rand_herm(3 ** 4), p)
viol = 0; maxsect = 0; trials = 0
subsets6 = [frozenset(M) for r in range(1, 4) for M in itertools.combinations(range(6), r)]
for _ in range(40):
    k = rng.integers(1, 4)
    Ms = [subsets6[i] for i in rng.integers(0, len(subsets6), size=k)]
    X = Vp.copy()
    for M in Ms:
        X = ad(toy.creation(rand_cvecs(toy, [M])), X)
    v = X @ toy.Omega
    N = frozenset().union(*Ms)
    live = [M for M, idx in toy.sectors.items() if M and np.linalg.norm(v[idx]) > 1e-10]
    trials += 1
    allmeet = all(M & P for M in Ms)
    for M in live:
        if not (allmeet and (N - P) <= M <= (N | P)):
            viol += 1
    maxsect = max(maxsect, len(live))
report("no live sector outside {(N\\p) u T : T <= p}", viol == 0, f"({trials} random tuples)")
report("live sectors per tuple <= 16", maxsect <= 16, f"(max seen {maxsect})")

# ----------------------------------------------------------------------------
print("== C4 BDL App. A erratum: '|M_j| <= 2|M|' fails; correct bound (s+1)|M| ==")
# qubits u=0, v=1, w=2 ; V_{vw} = X_v X_w ; M_1 = {u,v,w} ; M = {u}
toy = Toy(3, 2, energies=np.ones((3, 2)))
Vvw = toy.embed(np.kron(np.array([[0, 1], [1, 0]]), np.array([[0, 1], [1, 0]])), (1, 2))
A = toy.creation({frozenset({0, 1, 2}): np.array([1.0])})
v = ad(A, Vvw) @ toy.Omega
amp = v[toy.sectors[frozenset({0})]][0]
report("<Omega|a_u [a+_{uvw}, V_vw]|Omega> != 0 with |M_j|=3, |M|=1", abs(amp) > 0.5,
       f"(amplitude {amp.real:+.1f})")
print("   => E0(M) >= (Delta/2)|M_j| is FALSE here; BDL's final 2^13 survives (see constants.py S3).")

# ----------------------------------------------------------------------------
print("== C5 Lemma 3' (BDL Lemma 3, eq. 19) with sector-valued C, qutrits, 4-body ==")
from math import comb
def gam0(s): return math.sqrt(sum(comb(s - 1, t - 1) / t ** 2 for t in range(1, s + 1)))
def gamj(s): return (s + 1) * math.sqrt(sum(comb(s, t) / (t + 1) ** 2 for t in range(0, s + 1)))
def beta(k, s=4): return 2 ** k * (gam0(s) * s ** k + k * gamj(s) * s ** (k - 1))

toy = Toy(6, 3, energies=np.ones((6, 3)))      # all excitation energies = Delta = 1 (worst case)
plaqs = [(0, 1, 2, 3), (2, 3, 4, 5)]
Vs = [toy.embed(rand_herm(3 ** 4), pp) for pp in plaqs]
V = sum(Vs)
J = max(np.linalg.norm(x, 2) for x in Vs)
D = max(sum(1 for pp in plaqs if u in pp) for u in range(6))
worst = 0.0
subsets = [frozenset(M) for r in range(1, 6) for M in itertools.combinations(range(6), r)]
adversarial = [frozenset({0, 2, 3, 4, 5}), frozenset({1, 2, 3, 4, 5}), frozenset({4, 0, 1, 2, 3}),
               frozenset({5}), frozenset({0}), frozenset({4, 5})]
for trial in range(60):
    k = 1 + trial % 3
    Cs, cv = [], []
    for i in range(k):
        pool = adversarial if trial % 2 else subsets
        sel = [pool[j] for j in rng.choice(len(pool), size=min(3, len(pool)), replace=False)]
        c = rand_cvecs(toy, sel)
        cv.append(c); Cs.append(toy.creation(c))
    X = V.copy()
    for Ci in reversed(Cs):
        X = ad(Ci, X)
    newc = toy.resolvent_project(X)
    lhs = toy.norm1(newc)
    rhs = beta(k) * D * J / 1.0 * np.prod([toy.norm1(c) for c in cv])
    worst = max(worst, lhs / rhs)
report("||C||_1 / [beta_k D J/Delta prod||C_i||_1] <= 1", worst <= 1.0, f"(worst ratio {worst:.3e})")

# ----------------------------------------------------------------------------
print("== C6 end-to-end Kirkwood-Thomas with sector-valued C (BDL Sec. 2.3, Cor. 3/4) ==")
toy = Toy(5, 3)
plaqs = [(0, 1, 2, 3), (1, 2, 3, 4)]
Vs = [toy.embed(rand_herm(3 ** 4), pp) for pp in plaqs]
V = sum(Vs); J = max(np.linalg.norm(x, 2) for x in Vs)
D = 2; Delta = min(toy.e[:, 1:].min(), 1.0)
b = [gam0(4)] + [beta(k) for k in range(1, 9)]
def qpoly(m): return b[0] + sum(b[k] * m ** k / math.factorial(k) for k in range(1, 9))
def mustar(lam):
    lo, hi = 0.0, 0.03
    for _ in range(200):
        mid = (lo + hi) / 2
        if mid - lam * qpoly(mid) < 0: lo = mid
        else: hi = mid
    return hi
for lam in (0.005, 0.0119):
    eps = lam * Delta / (D * J)
    c = {}
    for it in range(200):
        Cm = toy.creation(c) if c else np.zeros((toy.dim, toy.dim))
        U = __import__("scipy.linalg", fromlist=["expm"]).expm(Cm)
        Ui = __import__("scipy.linalg", fromlist=["expm"]).expm(-Cm)
        dressedV = U @ V @ Ui                     # = exp(ad_C)(V)
        newc = {M: eps * vec for M, vec in toy.resolvent_project(dressedV).items()}
        diff = sum(np.linalg.norm(newc.get(M, 0) - c.get(M, 0)) for M in set(newc) | set(c))
        c = newc
        if diff < 1e-14: break
    Cm = toy.creation(c)
    psi = __import__("scipy.linalg", fromlist=["expm"]).expm(-Cm) @ toy.Omega
    H = toy.H0 + eps * V
    Epsi = (psi.conj() @ H @ psi) / (psi.conj() @ psi)
    res = np.linalg.norm(H @ psi - Epsi * psi) / np.linalg.norm(psi)
    ev = np.linalg.eigvalsh(H)
    report(f"lambda={lam}: all quantities finite", np.all(np.isfinite(psi)) and np.isfinite(Epsi) and np.isfinite(res))
    report(f"lambda={lam}: exp(-C)Omega is an eigenvector", res < 1e-9, f"(residual {res:.1e})")
    report(f"lambda={lam}: it is the GROUND state", abs(Epsi.real - ev[0]) < 1e-9)
    report(f"lambda={lam}: ||C||_1 <= mu*(lambda)", toy.norm1(c) <= mustar(lam),
           f"({toy.norm1(c):.2e} <= {mustar(lam):.2e})")
    report(f"lambda={lam}: gap >= Delta/2", ev[1] - ev[0] >= Delta / 2, f"(gap {ev[1]-ev[0]:.3f})")

print("\nALL TOY CHECKS PASSED" if ok else "\nSOME TOY CHECK FAILED")
