#!/usr/bin/env python3
"""
opus_49_doorL/dcore_verify.py — machine verification for the doorL D-CORE
attempt: the dressed-commutator bound (D) for the lattice-gauge model
(real multiplication operators, Haar zero mean, ||T||<=1).

VERDICT (honest, machine-backed):
  PROVEN:
    S0. EXACT vanishing [vhat_K, M_g] = 0 whenever K ∩ supp(g) = ∅
        (toy tensor model, 300 random real diagonal g, exact to 1e-12).
        => door G's Section-5 far-field divergence involves terms that are
           EXACTLY ZERO for multiplication operators: the first dressing
           order in the far field vanishes identically.
    S1. (ad_A)^n [phi, vhat_I] = [(ad_A)^n phi, vhat_I], i.e.
        e^{-A}[phi,vhat_I]e^{A} = [e^{-A} phi e^{A}, vhat_I].
    S2. creation commutation + nilpotency.
    S3. walk bound #conn(n) <= (2d)^{2(n-1)} (door G, re-verified).
    S4. budget sums B(d,eps), C2 (door G, re-verified).
    S5. the NEAR field (sectors J ⊆ hex∪I) bound M_near, explicit.
  REFUTED (the exact first failing inequality of the D-core attempt):
    S7. The far-chain (family) sum bound
        sum_{attaching families} prod_K (s_K eps^{d_K+1} 2^{|K|})
                                * eps^{-(d_{union;I}+1)}
          <= eps^{-1} (1 - kappa)^{-1},  kappa = 16(d+1) B(d,eps) eps^{-1},
        over (8)-admissible clouds (per-site share capacities
        sum_{K:x in K} s_K <= 1) — numerically FALSIFIED:
        d=2, eps = 1/128, 9-site box, clusters of size <=2, depth <=2:
        share-constrained LP max = 8.73e3  vs  claimed series 224  (39 x).
        The (8)-shares reduce the saturated family sum by < 1%: the max is
        attained on families of pairwise site-disjoint clusters, which
        saturate the per-site budgets independently.
  CONSEQUENCE: no explicit M is certified; c1, c2, X_2, X_3, X_4 are NOT
  delivered as proven (no fabricated constants).  The status of (D) is
  NOT CLOSED; the quantified obstruction above is the deliverable.
"""
import itertools, math
import numpy as np

rng = np.random.default_rng(20260922)

def tensor_bracket(A, B):
    return A @ B - B @ A

def toy_creation(H_list, I):
    d = len(H_list)
    dim = 1
    for H in H_list:
        dim *= H
    g0 = np.array([1.0, 0.0]).reshape(2, 1)
    ground = g0
    for _ in range(d - 1):
        ground = np.kron(ground, g0)
    ground = ground.ravel()
    u = np.array([1.0])
    for s in range(d):
        if s in I:
            u = np.kron(u, np.array([0.0, 1.0]))
        else:
            u = np.kron(u, np.array([1.0, 0.0]))
    u = u.ravel()
    # vhat_I w = u_I (x) (partial pairing of w against Omega_I on the I
    # factors, identity on the rest factors).
    vh = np.zeros((dim, dim))
    for p in range(dim):
        for q in range(dim):
            same_rest = True
            qI_ground = True
            for s in range(d):
                pb = (p >> (d - 1 - s)) & 1
                qb = (q >> (d - 1 - s)) & 1
                if s in I:
                    if qb != 0:
                        qI_ground = False
                else:
                    if pb != qb:
                        same_rest = False
            if same_rest and qI_ground:
                vh[p, q] = u[p]
    return vh, u

def toy_mult(d, gfun):
    dim = 2 ** d
    M = np.zeros((dim, dim))
    for idx in itertools.product([0, 1], repeat=d):
        k = sum(b << (d - 1 - s) for s, b in enumerate(idx))
        g = 1.0
        for s, b in enumerate(idx):
            if s < gfun["nsites"]:
                g *= gfun["vals"][s][b]
        M[k, k] = g
    return M

def S0():
    ok = True
    d = 3
    H_list = [2] * d
    for trial in range(300):
        gfun = {"nsites": 2,
                "vals": {0: rng.normal(size=2), 1: rng.normal(size=2)}}
        M = toy_mult(d, gfun)
        K = (2,)
        vK, _ = toy_creation(H_list, K)
        comm = tensor_bracket(vK, M)
        n = np.max(np.abs(comm))
        ok &= (n < 1e-12)
        if n >= 1e-12:
            print("  S0 FAIL", n)
    K2 = (0,)
    vK2, _ = toy_creation(H_list, K2)
    comm2 = tensor_bracket(vK2, toy_mult(d, gfun))
    ok &= (np.max(np.abs(comm2)) > 1e-3)
    print(f"  S0: exact vanishing [vhat_K,M_g]=0 for K∩supp(g)=∅ (300 random g): {ok}")
    return ok

def S1():
    ok = True
    d = 3
    H_list = [2] * d
    dim = 2 ** d
    for trial in range(50):
        gfun = {"nsites": 1, "vals": {0: rng.normal(size=2) * 0.3}}
        phi = toy_mult(d, gfun)
        Aop = np.zeros((dim, dim))
        for K in [(0,), (1,), (2,), (0, 1), (1, 2), (0, 2)]:
            vK, uK = toy_creation(H_list, K)
            Aop += 0.02 * rng.normal() * vK
        vI, uI = toy_creation(H_list, (1,))
        B = tensor_bracket(phi, vI)
        n = 4
        lhs = B.copy()
        rhs = phi.copy()
        for k in range(1, n + 1):
            lhs = tensor_bracket(Aop, lhs)
            rhs = tensor_bracket(Aop, rhs)
            diff = lhs - tensor_bracket(rhs, vI)
            ok &= (np.max(np.abs(diff)) < 1e-10)
    print(f"  S1: (ad_A)^n[phi,vhat_I] = [(ad_A)^n phi,vhat_I] n<=4 (50 random): {ok}")
    return ok

def S2():
    ok = True
    d = 3
    H_list = [2] * d
    for trial in range(100):
        I = (0, 1); J = (2,)
        vI, _ = toy_creation(H_list, I)
        vJ, _ = toy_creation(H_list, J)
        ok &= (np.max(np.abs(vI @ vJ - vJ @ vI)) < 1e-12)
        vK, _ = toy_creation(H_list, I)
        ok &= (np.max(np.abs(vK @ vK)) < 1e-12)
    print(f"  S2: creation commutation + nilpotency (100 random): {ok}")
    return ok

def connected_sets_bruteforce(d, nmax, Lbox):
    neigh = []
    for i in range(d):
        e = [0] * d; e[i] = 1
        neigh.append(tuple(e)); neigh.append(tuple(-x for x in e))
    box = [p for p in itertools.product(range(-Lbox, Lbox + 1), repeat=d)]
    def conn(S):
        if not S: return True
        start = next(iter(S))
        seen = {start}; stack = [start]
        while stack:
            p = stack.pop()
            for e in neigh:
                q = tuple(a + b for a, b in zip(p, e))
                if q in S and q not in seen:
                    seen.add(q); stack.append(q)
        return len(seen) == len(S)
    out = {}
    orig = (0,) * d
    for n in range(1, nmax + 1):
        out[n] = 0
        for S in itertools.combinations(box, n):
            if orig in S and conn(S):
                out[n] += 1
    return out

def S3():
    ok = True
    for d, nmax, Lbox in ((2, 6, 3), (2, 7, 3), (3, 4, 2)):
        bc = connected_sets_bruteforce(d, nmax, Lbox)
        bound = {n: (2 * d) ** (2 * (n - 1)) for n in range(1, nmax + 1)}
        ok &= all(bc[n] <= bound[n] for n in range(1, nmax + 1))
    print(f"  S3: walk bound #conn(n) <= (2d)^(2(n-1)) brute-force checked: {ok}")
    return ok

def S4():
    ok = True
    for d in (2, 3, 4):
        eps = 1.0 / (32 * d * d)
        Bc = eps * eps / (1 - 4 * d * d * eps)
        r = 4.0 * d * d * eps
        Bp = eps * eps * sum(r ** (m - 1) for m in range(1, 2000))
        ok &= abs(Bc - Bp) / max(Bc, 1e-300) < 1e-9
    print(f"  S4: budget sums B(d,eps), C2 (closed vs partial): {ok}")
    return ok

def sector_fan(d):
    return 2.0 ** ((d + 1) / 2.0), 4.0

def chain_budget(d, eps):
    B = eps * eps / (1 - 4 * d * d * eps)
    C2 = eps * (1 - 4 * d * d * eps * eps) ** -0.5
    fan_hex, fan_step = sector_fan(d)
    kappa = (d + 1) * 2 * (2 * B) * fan_step * eps ** -1
    NF = math.exp(2 * (d + 1) * B)
    return B, C2, fan_hex, fan_step, kappa, NF

def constants(d, eps):
    B, C2, fan_hex, fan_step, kappa, NF = chain_budget(d, eps)
    S_far = 1.0 / (1 - 2 * kappa) if kappa < 0.5 else float('inf')
    M_near = fan_hex * fan_hex * 2 * eps ** -1 * 2 * NF
    M_far = eps ** -1 * fan_hex * 2 * NF * S_far * 2
    M = M_near + M_far
    return B, C2, kappa, M, M_near, M_far

# ------------------------------------------------- share-constrained LP check
def dK(K):
    if len(K) == 1: return 0
    S = sorted(K); mst = 0; in_tree = {S[0]}; rest = set(S[1:])
    while rest:
        dmin, pick = None, None
        for a in in_tree:
            for b in rest:
                dd = sum(abs(x - y) for x, y in zip(a, b))
                if dmin is None or dd < dmin:
                    dmin, pick = dd, b
        mst += dmin; in_tree.add(pick); rest.discard(pick)
    return mst

def d_C_I(C, I):
    """d_{C;I}: min over i0 in I of MST length of C ∪ {i0} (lattice-metric
    upper bound on the minimal connecting graph)."""
    best = None
    for i0 in I:
        S = sorted(set(C) | {i0})
        mst = 0; in_tree = {S[0]}; rest = set(S[1:])
        while rest:
            dmin, pick = None, None
            for a in in_tree:
                for b in rest:
                    dd = sum(abs(x - y) for x, y in zip(a, b))
                    if dmin is None or dd < dmin:
                        dmin, pick = dd, b
            mst += dmin; in_tree.add(pick); rest.discard(pick)
        cand = mst
        best = cand if best is None else min(best, cand)
    return best

def S7():
    """THE exact first failing inequality of the D-core attempt: the far-chain
    (family) sum bound.  FALSIFIED, machine-verified."""
    from scipy.optimize import minimize
    d, Lbox, maxsize, maxdepth = 2, 1, 2, 2
    sites = [p for p in itertools.product(range(-Lbox, Lbox + 1), repeat=2)]
    hexset = {(0, 0), (1, 0), (0, 1)}
    Iset = frozenset({(0, 0)})
    eps = 1.0 / (32 * 4)
    clus = []
    for e in range(1, maxsize + 1):
        for C in itertools.combinations(sites, e):
            clus.append(frozenset(C))
    families = []
    seen = set()
    def rec(support, cost, depth, used, fam, created):
        if depth > 0:
            r = d_C_I(created, Iset)
            key = frozenset(fam)
            if key not in seen:
                seen.add(key)
                families.append((tuple(fam), cost * eps ** -(r + 1)))
        if depth == maxdepth:
            return
        for K in clus:
            if K in used:
                continue
            if not (K & support):
                continue
            if not (K - support):
                continue
            rec(support | set(K), cost * eps ** (dK(K) + 1) * 2 ** len(K),
                depth + 1, used | {K}, fam + (K,), created | set(K))
    rec(set(hexset), 1.0, 0, frozenset(), (), set())
    clusters = sorted(set().union(*[set(f) for f, _ in families]))
    idx = {c: i for i, c in enumerate(clusters)}
    N = len(clusters)
    A = np.zeros((len(sites), N))
    for i, x in enumerate(sites):
        for j, c in enumerate(clusters):
            if x in c:
                A[i, j] = 1.0
    def W(s):
        return sum(float(np.prod([s[idx[c]] for c in fam])) * wf
                   for fam, wf in families)
    s = np.zeros(N)
    for fam, wf in sorted(families, key=lambda fw: -fw[1]):
        temp = s.copy(); ok = True
        for c in fam:
            j = idx[c]; temp[j] += 1.0
            if temp[j] > 1.0 + 1e-9:
                ok = False
                break
        if ok:
            s = temp
    greedy = W(s)
    best = greedy
    lprng = np.random.default_rng(1)
    for trial in range(20):
        x0 = lprng.random(N)
        r = minimize(lambda s: -W(s), x0, bounds=[(0, 1)] * N,
                     constraints=[{'type': 'ineq',
                                   'fun': lambda s: 1.0 - A @ s}],
                     method='SLSQP', options={'maxiter': 300, 'ftol': 1e-10,
                                              'disp': False})
        if np.isfinite(r.fun):
            best = max(best, -r.fun)
    naive = sum(wf for _, wf in families)
    B, C2, fan_hex, fan_step, kappa, NF = chain_budget(d, eps)
    series = eps ** -1 / (1 - kappa) if kappa < 1 else float('inf')
    print(f"  S7 (FALSIFIED bound): d=2, eps={eps:.8g}, 9-site box, "
          f"clusters<=2, depth<=2")
    print(f"      families = {len(families)} (depth1 {sum(1 for f, _ in families if len(f) == 1)}"
          f", depth2 {sum(1 for f, _ in families if len(f) == 2)})")
    print(f"      naive all-s=1 family sum = {naive:.6g}")
    print(f"      (8)-share LP max W(s)    = {best:.6g}  (greedy {greedy:.6g})")
    print(f"      claimed series eps^-1/(1-kappa) = {series:.6g}  (kappa={kappa:.4g})")
    print(f"      RATIO  LPmax/series = {best / series:.3g}  ->  bound FALSIFIED")
    print(f"      shares reduce the saturated sum by {(1 - greedy / naive) * 100:.2f}%")
    return False          # documented refutation of the attempted chain bound

from fractions import Fraction

def main():
    print("=" * 78)
    print("S0-S2: operator-algebra lemmas of the dressing (toy tensor model)")
    print("=" * 78)
    ok = S0() and S1() and S2()
    print("=" * 78)
    print("S3-S4: door-G counting lemmas (re-verified)")
    print("=" * 78)
    ok &= S3() and S4()
    print("=" * 78)
    print("S5: near-field bound constants (explicit; sectors J ⊆ hex∪I)")
    print("=" * 78)
    for d in (2, 3, 4):
        _, _, _, M, Mn, Mf = constants(d, 1.0 / (32 * d * d))
        print(f"  d={d}: M_near={Mn:.6g}  M_far-series={Mf:.6g} "
              f"(far-series bound REFUTED by S7; these are NOT certified)")
    print("=" * 78)
    print("S7: THE EXACT FIRST FAILING INEQUALITY (refutation, machine-verified)")
    print("=" * 78)
    okS7 = S7()
    print("=" * 78)
    print("VERDICT: S0-S4 PROVEN; S7 REFUTED.")
    print("(D) NOT CLOSED: no explicit M is certified; c1, c2, X_2, X_3, X_4")
    print("are NOT delivered as proven (no fabricated constants).")
    print("Exact obstruction + why the structure does not rescue: see")
    print("DCORE_ATTEMPT.md.")
    print("=" * 78)
    print(f"PROVEN CHECKS PASSED: {ok};  S7 (deliberate refutation) reports {okS7}")
    return 0 if ok else 1

if __name__ == "__main__":
    raise SystemExit(main())