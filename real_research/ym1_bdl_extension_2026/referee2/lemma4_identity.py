#!/usr/bin/env python3
"""
Task 2b: Lemma 4' (DERIVATION.md S9) exercised where its hypothesis |delta| < Delta/2 is actually MET by a
second eigenvalue, i.e. beyond threshold where the true gap < Delta/2.  Dense qutrit toy, n=6, plaquettes
(0,1,2,3),(2,3,4,5) (D=2), sector-valued C and B built from ED eigenvectors (no KT assumption):
   psi0/<Om|psi0> = e^{-C} Om  (C = -log of the unipotent sector operator),  e^{C} phi = (B + B(0)) Om.
Checks: (i) the S9 identity (H0^M - delta) b_M = eps Pi_M [B, e^C V e^-C] Om for every sector M;
        (ii) the contrapositive: gap < Delta/2  =>  2 lam q'(||C||_1) >= 1   (else Lemma 4' is false);
        (iii) the intermediate bound ||B||_1 <= 2 lam sum_k beta_{k+1} ||C||^k/k! ||B||_1 per the proof.
Also scans lam from 0.5 lam_c to 40 lam_c with the gap-adversarial diagonal V_p.
"""
import itertools, math
import numpy as np, scipy.linalg as sl
from toy import beta
n, q = 6, 3; dim = q ** n
plaqs = [(0, 1, 2, 3), (2, 3, 4, 5)]; D = 2
st = list(itertools.product(range(q), repeat=n)); idx = {s: i for i, s in enumerate(st)}
supp = [frozenset(w for w in range(n) if s[w]) for s in st]
secs = {}
for i, S in enumerate(supp): secs.setdefault(S, []).append(i)
rng = np.random.default_rng(3)
en = 1.0 + 0.0 * rng.random((n, q)); en[:, 0] = 0
E0 = np.array([sum(en[w, s[w]] for w in range(n)) for s in st])

def embed(op, sites):
    full = np.zeros((dim, dim), dtype=complex)
    T = op.reshape([q] * 8)
    for i, s in enumerate(st):
        loc_in = tuple(s[w] for w in sites)
        for a in itertools.product(range(q), repeat=4):
            v = T[a + loc_in]
            if v != 0:
                t = list(s)
                for j, w in enumerate(sites): t[w] = a[j]
                full[idx[tuple(t)], i] += v
    return full

def sector_op(vec):
    """operator sum_{M != 0} A[Pi_M vec]  (vec is a state; its sector-M part is c_M)"""
    out = np.zeros((dim, dim), dtype=complex)
    for M, ids in secs.items():
        if not M: continue
        for j, s in enumerate(st):
            if supp[j] & M: continue
            for i in ids:
                if vec[i] == 0: continue
                t = list(s)
                for w in M: t[w] = st[i][w]
                out[idx[tuple(t)], j] += vec[i]
    return out

def norm1(vec):
    return max(sum(np.linalg.norm(vec[ids]) for M, ids in secs.items() if u in M) for u in range(n))

b = [beta(k) for k in range(9)]
q_ = lambda m: b[0] + sum(b[k] * m ** k / math.factorial(k) for k in range(1, 9))
qp = lambda m: sum(b[k] * m ** (k - 1) / math.factorial(k - 1) for k in range(1, 9))
lo, hi = 0.0, 1.0
for _ in range(200):
    mid = (lo + hi) / 2
    (lo, hi) = (mid, hi) if q_(mid) - 2 * mid * qp(mid) > 0 else (lo, mid)
LAMC = lo / q_(lo)

dvec = -np.ones(q ** 4); dvec[0] = 1
Vloc = {"diag(+1 vac,-1 else)": np.diag(dvec).astype(complex)}
Z = rng.normal(size=(81, 81)) + 1j * rng.normal(size=(81, 81)); Hh = (Z + Z.conj().T) / 2
Vloc["random Hermitian"] = Hh / np.linalg.norm(Hh, 2)
Om = np.zeros(dim); Om[0] = 1
for name, Vl in Vloc.items():
    V = sum(embed(Vl, p) for p in plaqs)
    print(f"== V_p = {name} ==  (lam_c = {LAMC:.6f})")
    print("  lam/lam_c   gap     S9-identity-resid   ||C||_1    2lam q'(||C||_1)   gap<1/2 => crit>=1 ?")
    for f in (0.5, 1, 2, 5, 10, 15, 20, 21, 22, 25, 30, 40):
        lam = f * LAMC; eps = lam / D
        H = np.diag(E0) + eps * V
        ev, U = np.linalg.eigh(H)
        g = U[:, 0] / U[0, 0]
        C = -sl.logm(sector_op(g) + np.eye(dim)) if True else None
        cvec = C @ Om
        n1 = norm1(cvec)
        crit = 2 * lam * qp(n1)
        # take the first excited eigenvector phi and delta = E1 - E0
        delta = ev[1] - ev[0]; phi = U[:, 1]
        eC = sl.expm(sector_op(cvec)); emC = sl.expm(-sector_op(cvec))
        w = eC @ phi
        bvec = w.copy(); bvec[0] = 0
        Bop = sector_op(bvec)
        R = Bop @ (eC @ V @ emC) - (eC @ V @ emC) @ Bop
        rhs = eps * (R @ Om)
        resid = 0.0
        for M, ids in secs.items():
            if not M: continue
            lhs = (E0[ids] - delta) * bvec[ids]
            resid = max(resid, np.abs(lhs - rhs[ids]).max())
        ok = (delta >= 0.5) or (crit >= 1)
        print(f"  {f:7.1f}   {delta:.4f}   {resid:.2e}          {n1:.3e}   {crit:9.4f}          {'OK' if ok else 'VIOLATION'}")
