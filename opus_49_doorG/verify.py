#!/usr/bin/env python3
"""
opus_49_doorG/verify.py — machine verification for the doorG cluster-expansion
constant-tracking attempt.

The mathematical facts verified here:
S1. Connected-cluster counting bound: #connected sets of size n containing
    a fixed site in Z^d  <= (2d)^{2(n-1)} (walk bound), checked against exact
    brute-force counts on small boxes.
S2. Budget sums B(d,eps) = sum_{m>=1} (2d)^{2(m-1)} eps^{m+1}
    = eps^2/(1-4d^2 eps), closed form vs truncation; regime eps < 1/(4d^2).
S3. NEGATIVE RESULT (the honest blocker): the crude far-cluster weight
    sum_{r>=1} (2r+1)^d eps^{1-r} diverges for every eps in (0,1), so eq. (14)
    of arXiv:math-ph/0411042v1 is NOT derivable from Lemma-1-type norm bounds
    + counting alone.  The alternating dressed structure exp(-A)[Phi,.]exp(A)
    is essential; its quantitative form (hypothesis (D)) is the first
    unproved inequality.  Verified: partial sums grow without bound for
    several plausible eps, and the per-term growth condition eps<1 is
    necessary for even one far shell to decay.
S4. The dressed-remainder conditional content: if (D) closes with the natural
    compounded counting constant q(d,eps), the remainder bound is
    rou(d,eps) = sum_{r>=1} (2r+1)^d (q/eps)^r; we exhibit explicit eps(d)
    with q/eps = 1/2 and evaluate rou(d) numerically.  CONDITIONAL.
S5. Conditional constants c1 = 1/(2L), c2 = 4L style, L(d) built from rou(d),
    and the CONDITIONAL X_2, X_3, X_4 via
    X_d = max(1, sqrt(2 A_d/c1), sqrt(2 c2 A_d)), A_d = (32/3)*d(d-1)/2.
    All S5 numbers are CONDITIONAL on (D); nothing here is claimed as proven
    constants — the report marks exactly what is proven (S1,S2,S3 and the
    reduction chain) and what is conditional (S4,S5).
S6. doorE arithmetic re-verification: exact A_d; consolidation identity
    X_d = max(1, sqrt(2 A_d/theta)), theta = min(c1, 1/c2).
"""
import itertools
import math
from fractions import Fraction
import random

def connected_sets_bruteforce(d, nmax, Lbox):
    """Exact count of connected subsets of size n containing the origin,
    inside the box [-Lbox,Lbox]^d, by exhaustive enumeration."""
    neigh = []
    for i in range(d):
        e = [0]*d; e[i] = 1
        neigh.append(tuple(e)); neigh.append(tuple(-x for x in e))
    box = [p for p in itertools.product(range(-Lbox, Lbox+1), repeat=d)]
    def conn(S):
        if not S: return True
        start = next(iter(S))
        seen = {start}; stack = [start]
        while stack:
            p = stack.pop()
            for e in neigh:
                q = tuple(a+b for a, b in zip(p, e))
                if q in S and q not in seen:
                    seen.add(q); stack.append(q)
        return len(seen) == len(S)
    out = {}
    orig = (0,)*d
    for n in range(1, nmax+1):
        out[n] = 0
        for S in itertools.combinations(box, n):
            if orig in S and conn(S):
                out[n] += 1
    return out

def gfull_growth(d, nmax, Lbox):
    """Count connected sets containing origin by frontier-growth (dedup on
    canonical 'ordered' sets).  This is a different algorithm than brute
    force; used as an independent check on small boxes."""
    neigh = []
    for i in range(d):
        e = [0]*d; e[i] = 1
        neigh.append(tuple(e)); neigh.append(tuple(-x for x in e))
    counts = {n: 0 for n in range(1, nmax+1)}
    seen = set()
    def rec(S, n):
        if n > nmax: return
        fr = frozenset(S)
        if fr in seen: return
        seen.add(fr)
        counts[n] += 1
        if n == nmax: return
        for p in S:
            for e in neigh:
                q = tuple(a+b for a, b in zip(p, e))
                if q in S or any(abs(c) > Lbox for c in q): continue
                rec(S | {q}, n+1)
    rec({(0,)*d}, 1)
    return counts

def main():
    print("="*80)
    print("S1: connected-cluster counting bound  #conn(n) <= (2d)^(2(n-1))")
    print("="*80)
    ok1 = True
    # brute force on small boxes (exact)
    for d, nmax, Lbox in ((2, 6, 3), (2, 8, 3), (3, 4, 3)):
        bc = connected_sets_bruteforce(d, nmax, Lbox)
        bound = {n: (2*d)**(2*(n-1)) for n in range(1, nmax+1)}
        held = all(bc[n] <= bound[n] for n in range(1, nmax+1))
        ok1 &= held
        print(f"  d={d} box={Lbox}: exact counts { {n:bc[n] for n in range(1,nmax+1)} }")
        print(f"  walk bound next: { {n:bound[n] for n in range(1,nmax+1)} }  -> holds: {held}")
    # independent growth-method sanity on tiny boxes
    gc = gfull_growth(2, 5, 4)
    print(f"  d=2 growth-method counts (box 4): {gc}")
    ok1 &= all(gc[n] <= (4)**(2*(n-1)) or n > 5 for n in gc)
    print(f"S1 RESULT: {ok1}\n")

    print("="*80)
    print("S2: budget sums B(d,eps) = sum_m (2d)^(2(m-1)) eps^(m+1)")
    print("="*80)
    ok2 = True
    for d in (2, 3, 4):
        eps = 1.0/(8*d*d)
        Bc = eps*eps/(1 - 4*d*d*eps)
        # partial sum in a numerically safe way: term_m = (4 d^2 eps)^(m-1) * eps^2
        r = 4.0*d*d*eps
        Bp = eps*eps*sum(r**(m-1) for m in range(1, 2000))
        ok2 &= abs(Bc - Bp)/max(Bc, 1e-300) < 1e-9
        print(f"  d={d} eps=1/(8d^2): closed-form B={Bc:.8g}; partial sum={Bp:.8g}; "
              f"4d^2 eps={4*d*d*eps:.4g} < 1: {4*d*d*eps<1}")
    print(f"S2 RESULT: {ok2}\n")

    print("="*80)
    print("S3: NEGATIVE RESULT — crude far-cluster weight diverges for every eps<1")
    print("="*80)
    # The crude far-field weight for single-site clusters at distance r is
    #   eps^{d_K+1} * eps^{-(d_{J;I}+1)} ~ eps^1 * eps^{-(r+1)} = eps^{-r},
    # summed over ~ (2r+1)^d sites per shell.  So the total crude weight is
    #   sum_r (2r+1)^d eps^{-r}.
    for d in (2, 3, 4):
        for eps in (0.5, 0.15, 1/(8*d*d), 1/(64*d*d)):
            S = sum((2*r+1)**d * eps**(-r) for r in range(1, 60))
            term60 = (2*60+1)**d * eps**(-60)
            print(f"  d={d} eps={eps:.6g}: partial(r<=59)={S:.4g}  last term={term60:.3g}")
    print("  -> each term grows unboundedly for any eps in (0,1); the crude")
    print("     bound alone can never close the far field.  (14)-type estimates")
    print("     therefore REQUIRE the alternating (dressed) cancellation.\n")

    print("="*80)
    print("S4: dressed-remainder conditional content  (hypothesis (D))")
    print("="*80)
    from math import e as E
    data = {}
    for d in (2, 3, 4):
        # condition q/eps < 1 with q = 2^(d+4)*e*B*(1+B)^2*d  (our compounded
        # counting constant); pick eps(d) so q/eps = 1/2.
        def qoe(epsx):
            if 4*d*d*epsx >= 1: return float('inf')
            B = epsx*epsx/(1 - 4*d*d*epsx)
            return 2**(d+4)*E*B*(1+B)**2*d/epsx
        lo, hi = 1e-13, 1/(4*d*d) - 1e-9
        for _ in range(300):
            mid = (lo+hi)/2
            if qoe(mid) > 0.5: hi = mid
            else: lo = mid
        epsx = (lo+hi)/2
        B = epsx*epsx/(1 - 4*d*d*epsx)
        q = 2**(d+4)*E*B*(1+B)**2*d
        rou = sum((2*r+1)**d / 2.0**r for r in range(1, 60))
        data[d] = (epsx, B, q, rou)
        print(f"  d={d}: eps={epsx:.8g} | B={B:.6g} | q={q:.6g} | q/eps={q/epsx:.4g} | "
              f"rou(d)<={rou:.6g}  (convergent since q/eps=1/2<1)")
    print("  CONDITIONAL: these are the numbers one WOULD get if (D) holds with the\n"
          "  natural compounded counting constant.  NOT proven.\n")

    print("="*80)
    print("S5: CONDITIONAL constants and X_2,X_3,X_4  (CONDITIONAL on (D))")
    print("="*80)
    A = {d: float(Fraction(32,3)*Fraction(d*(d-1),2)) for d in (2,3,4)}
    for d in (2,3,4):
        epsx, B, q, rou = data[d]
        M = rou
        L = M * (1+2*B) * math.exp(2*B*(1+B))
        c1 = 1/(2*L)
        c2 = 4*L
        Xd = max(1.0, math.sqrt(2*A[d]/c1), math.sqrt(2*c2*A[d]))
        eta = A[d]/Xd**2
        print(f"  d={d}: M={M:.5g} L={L:.5g} | cond. c1={c1:.4g} cond. c2={c2:.4g}")
        print(f"        cond. X_{d} = {Xd:.5g}   (check eta={eta:.4g} <= c1/2={c1/2:.4g}: {eta<=c1/2}; "
              f"c2 eta={c2*eta:.4g} <= 1/2: {c2*eta<=0.5})")
    print("  *** These X_d are CONDITIONAL on unproved (D). They are NOT claimed")
    print("      as theorems; the unconditional facts are the reduction chain,\n"
          "      S1-S2 and the negative result S3. ***\n")

    print("="*80)
    print("S6: doorE re-verification (A_d exact, consolidation identity)")
    print("="*80)
    ok6 = True
    for d in (2,3,4,5,6,8):
        print(f"  A_{d} = {Fraction(32,3)*Fraction(d*(d-1),2)} = {float(Fraction(32,3)*Fraction(d*(d-1),2)):.6g}")
    rnd = random.Random(7)
    for _ in range(20000):
        c1 = 10**rnd.uniform(-6, 2); c2 = 10**rnd.uniform(-6, 2)
        X1 = max(1.0, math.sqrt(2*A[3]/c1), math.sqrt(2*c2*A[3]))
        X2 = math.sqrt(2*A[3]/min(c1, 1/c2))
        ok6 &= (abs(X1 - max(1.0, X2)) < 1e-9)
    print(f"  consolidation identity over 20k random (c1,c2): {ok6}")
    ok = ok1 and ok2 and ok6
    print("="*80)
    print("ALL PROVEN CHECKS PASSED" if ok else "SOME PROVEN CHECKS FAILED")

if __name__ == '__main__':
    main()