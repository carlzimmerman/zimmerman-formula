#!/usr/bin/env python3
"""
Task 2: Lemma 4' / Theorem near and beyond threshold on a genuinely many-body 4-body toy.
16 qubits on a 4x4 torus, plaquettes = the 16 2x2 blocks  => s = 4, D = 4 (the d=3 link-grouping D).
h_u = diag(0,1) (Delta = 1), eps = lam/D (J = 1).  For each V_p family and lam:
  * ED (scipy eigsh): true gap E1-E0 vs Delta/2
  * Kirkwood-Thomas fixed point (set-function algebra, independent of ED): c = eps (H0^M)^{-1} Pi_M e^C V e^{-C} Omega
    -> is e^{-C}Omega the ED ground state?  energy match?  ||C||_1 vs mu*(lam)  (Lemma 5')
  * Lemma 4' criterion with the ACTUAL ||C||_1 : 2 lam q'(||C||_1) < 1  must imply gap >= 1/2.
"""
import itertools, math, sys, json
import numpy as np, scipy.sparse as sp, scipy.sparse.linalg as sla
from setalg import popcount_table, conv, sexp
from toy import beta

n = 16; L = 4
site = lambda x, y: (x % L) * L + (y % L)
plaqs = [(site(x, y), site(x + 1, y), site(x, y + 1), site(x + 1, y + 1)) for x in range(L) for y in range(L)]
D = max(sum(u in p for p in plaqs) for u in range(n)); s = 4
assert D == 4
pc = popcount_table(n); dim = 1 << n
b = [beta(k) for k in range(0, 9)]
q = lambda m: b[0] + sum(b[k] * m ** k / math.factorial(k) for k in range(1, 9))
qp = lambda m: sum(b[k] * m ** (k - 1) / math.factorial(k - 1) for k in range(1, 9))
def mustar(lam):
    f = 0.0
    for _ in range(100000):
        g = lam * q(f)
        if g > 10: return float("inf")
        if abs(g - f) < 1e-16: return g
        f = g
    return f
lo, hi = 0.0, 1.0
for _ in range(200):
    mid = (lo + hi) / 2
    (lo, hi) = (mid, hi) if q(mid) - 2 * mid * qp(mid) > 0 else (lo, mid)
LAMC = lo / q(lo)

def local_to_full(Vloc, p):
    """sparse full operator for a 16x16 Vloc on ordered sites p (local index bit j <-> site p[j])"""
    rows, cols, vals = [], [], []
    m = np.arange(dim)
    loc = sum(((m >> p[j]) & 1) << j for j in range(4))
    base = m.copy()
    for j in range(4):
        base &= ~(1 << p[j])
    for a in range(16):
        for bb in range(16):
            v = Vloc[a, bb]
            if v == 0: continue
            sel = loc == bb
            src = m[sel]
            dst = base[sel] | sum(((a >> j) & 1) << p[j] for j in range(4))
            rows.append(dst); cols.append(src); vals.append(np.full(len(src), v))
    return sp.csr_matrix((np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))), shape=(dim, dim))

def families(rng):
    fam = {}
    d = -np.ones(16); d[0] = 1.0
    fam["diag(+1 vac, -1 else)"] = np.diag(d).astype(complex)          # adversarial for the gap
    # k=0-saturating reflection: Omega_p -> w, w_T ~ 1/|T|
    w = np.array([0.0] + [1.0 / bin(t).count("1") for t in range(1, 16)]); w /= np.linalg.norm(w)
    e0 = np.zeros(16); e0[0] = 1
    phi = (e0 - w) / np.linalg.norm(e0 - w)
    fam["reflection Om->w_T~1/|T|"] = (np.eye(16) - 2 * np.outer(phi, phi)).astype(complex)
    fam["-(reflection) "] = -fam["reflection Om->w_T~1/|T|"]
    X = np.array([[0, 1], [1, 0]]); XX = X
    for _ in range(3): XX = np.kron(XX, X)
    fam["XXXX"] = XX.astype(complex)
    Z = rng.normal(size=(16, 16)) + 1j * rng.normal(size=(16, 16)); Hh = (Z + Z.conj().T) / 2
    fam["random Hermitian"] = Hh / np.linalg.norm(Hh, 2)
    # mixed: diagonal adversary + reflection (normalised)
    M = fam["diag(+1 vac, -1 else)"] + fam["reflection Om->w_T~1/|T|"]; fam["diag+refl"] = M / np.linalg.norm(M, 2)
    return fam

def kt_solve(V, eps, E0, maxit=250, damp=0.8):
    c = np.zeros(dim, dtype=complex)
    Ed = E0.copy(); Ed[0] = 1.0
    for it in range(maxit):
        psi = sexp(-c, n, pc)
        u = conv(sexp(c, n, pc), V @ psi, n, pc)
        cn = eps * u / Ed; cn[0] = 0
        diff = np.abs(cn - c).max()
        if not np.all(np.isfinite(cn)) or diff > 1e6: return None, None, it
        c = (1 - damp) * c + damp * cn
        if diff < 1e-12: break
    return c, eps * u[0], it

def norm1(c):
    a = np.abs(c)
    return max(a[((np.arange(dim) >> u) & 1) == 1].sum() for u in range(n))

if __name__ == "__main__":
    rng = np.random.default_rng(5)
    E0 = pc.astype(float)                   # all excitation energies = Delta = 1
    H0 = sp.diags(E0)
    lams = [0.5, 1, 2, 5, 10, 20, 22, 25]
    out = {}
    print(f"toy: n={n} qubits, {len(plaqs)} 4-body plaquettes, D={D}, s={s}; lam_c(s=4) = {LAMC:.8f}")
    for name, Vloc in families(rng).items():
        V = sum(local_to_full(Vloc, p) for p in plaqs)
        print(f"\n== V_p = {name} ==")
        print("  lam/lam_c   lam      ED gap   >=1/2?  KT conv  |<psi_KT|g>|  E_KT-E0_ED   ||C||_1   mu*(lam)  ratio  2lam q'(||C||)  L4'-says-gap>=1/2")
        rows = []
        for f in lams:
            lam = f * LAMC; eps = lam / D
            for sgn in (+1,):
                H = (H0 + sgn * eps * V).tocsr()
                ev, evec = sla.eigsh(H, k=4, which="SA", tol=1e-12)
                o = np.argsort(ev); ev = ev[o]; g = evec[:, o[0]]
                gap = ev[1] - ev[0]
                c, Ekt, it = kt_solve(sgn * V, eps, E0)
                if c is not None:
                    psi = sexp(-c, n, pc)
                    ov = abs(np.vdot(psi, g)) / np.linalg.norm(psi)
                    n1 = norm1(c); ms = mustar(lam)
                    crit = 2 * lam * qp(n1)
                    rows.append(dict(f=f, lam=lam, gap=gap, ov=ov, dE=float(Ekt.real - ev[0]), n1=n1, mu=ms, crit=crit))
                    flag = "VIOLATION" if (crit < 1 and gap < 0.5) else ""
                    print(f"  {f:7.1f}  {lam:.5f}  {gap:.5f}  {'yes' if gap>=0.5 else 'NO '}   {it:5d}   {ov:.12f}  {Ekt.real-ev[0]:+.2e}  {n1:.3e}  {ms:.3e}  {n1/ms if np.isfinite(ms) else float('nan'):.3f}   {crit:.4f}   {'yes' if crit<1 else 'no'} {flag}")
                else:
                    rows.append(dict(f=f, lam=lam, gap=gap, ov=None))
                    print(f"  {f:7.1f}  {lam:.5f}  {gap:.5f}  {'yes' if gap>=0.5 else 'NO '}   KT DIVERGED (it {it})   mu*={mustar(lam):.3e}")
        out[name] = rows
    json.dump(out, open("gap_kt_ed.json", "w"), indent=1, default=float)
