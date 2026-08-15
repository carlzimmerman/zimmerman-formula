#!/usr/bin/env python3
"""bridge_scan.py -- the dimensional-bridge scanner: the shape of the original discovery,
made systematic.  Finds units-correct products of one domain's quantities that land on a
measured scale from another domain with an O(1) prefactor, chance-calibrated.

  python bridge_scan.py --target a0_can --pool c,G,rho_L            (positive control -> kappa=0.5)
  python bridge_scan.py --target m_pi --pool hbar,H0,G,c            (Weinberg relation control)
  python bridge_scan.py --target m_e --pool c,G,hbar,H0,Lambda,rho_L,a0_can,Q0

Method: for every subset (<= --max-terms) of the pool, solve the [m,kg,s] dimension-match
linear system EXACTLY (Fraction arithmetic); keep solutions with rational exponents of
denominator <= 3 and |n| <= 5/2; prefactor = target/value; HIT if 10^-2 <= prefactor <= 10^2.
Chance baseline: analytic -- P(hit) for a pseudo-target log-uniform within +-3 decades.
Surplus = hits/expected.  Hits are RAW BRIDGE CANDIDATES; their prefactors go to
mm_search --custom for the simplicity pass (a bridge is interesting only if BOTH the
dimensional hit beats chance AND the prefactor is simple -- kappa = 1/2 passes both).
"""
import argparse, itertools, json, os, sys
from fractions import Fraction as F

import numpy as np

# name: (SI value, [m, kg, s] dimension exponents, domain)
QUANTITIES = {
    "c":      (2.99792458e8,  (1, 0, -1),  "kinematic"),
    "G":      (6.67430e-11,   (3, -1, -2), "gravity"),
    "hbar":   (1.054571817e-34,(2, 1, -1), "quantum"),
    "H0":     (2.1927e-18,    (0, 0, -1),  "cosmo"),
    "Lambda": (1.1056e-52,    (-2, 0, 0),  "cosmo"),
    "rho_L":  (5.83e-27,      (-3, 1, 0),  "cosmo"),
    "rho_m":  (2.68e-27,      (-3, 1, 0),  "cosmo"),
    "kT_cmb": (3.762e-23,     (2, 1, -2),  "cosmo"),
    "m_e":    (9.1093837e-31, (0, 1, 0),   "SM"),
    "m_p":    (1.67262192e-27,(0, 1, 0),   "SM"),
    "m_pi":   (2.488e-28,     (0, 1, 0),   "SM"),
    "v_EW":   (3.9455e-8,     (2, 1, -2),  "SM"),
    "a0_can": (9.3619e-11,    (1, 0, -2),  "framework"),
    "a0_alt": (1.1279e-10,    (1, 0, -2),  "framework"),
    "Q0":     (2.75e-25,      (-1, 0, 0),  "framework"),
}
EXPS = [F(n, d) for d in (1, 2, 3) for n in range(-7, 8) if n != 0
        and abs(F(n, d)) <= F(5, 2) and F(n, d).denominator == d]


def solve_subset(names, tdim):
    """exact rational solutions of sum_i e_i * dim_i = tdim with e_i in EXPS."""
    dims = [QUANTITIES[n][1] for n in names]
    k = len(names)
    A = [[F(dims[j][r]) for j in range(k)] for r in range(3)]
    b = [F(tdim[r]) for r in range(3)]
    M = [row[:] + [b[i]] for i, row in enumerate(A)]
    piv, r = [], 0
    for c in range(k):
        pr = next((i for i in range(r, 3) if M[i][c] != 0), None)
        if pr is None:
            continue
        M[r], M[pr] = M[pr], M[r]
        M[r] = [x / M[r][c] for x in M[r]]
        for i in range(3):
            if i != r and M[i][c] != 0:
                M[i] = [x - M[i][c] * y for x, y in zip(M[i], M[r])]
        piv.append(c)
        r += 1
        if r == 3:
            break
    for i in range(r, 3):
        if M[i][k] != 0:
            return []
    free = [c for c in range(k) if c not in piv]
    sols = []
    for combo in itertools.product(EXPS, repeat=len(free)) if free else [()]:
        e = [F(0)] * k
        for f, v in zip(free, combo):
            e[f] = v
        ok = True
        for i, c in enumerate(piv):
            v = M[i][k] - sum(M[i][j] * e[j] for j in free)
            if v == 0 or abs(v) > F(5, 2) or v.denominator > 3:
                ok = False
                break
            e[c] = v
        if ok and all(x != 0 for x in e):
            sols.append(tuple(e))
    return sols


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", required=True, choices=sorted(QUANTITIES))
    ap.add_argument("--pool", required=True, help="comma-separated quantity names")
    ap.add_argument("--max-terms", type=int, default=4)
    ap.add_argument("--window", type=float, default=2.0, help="|log10 prefactor| <= window")
    a = ap.parse_args()

    tval, tdim, tdom = QUANTITIES[a.target]
    pool = [p for p in a.pool.split(",") if p != a.target]
    hits, n_combos = [], 0
    seen = set()
    for k in range(1, min(a.max_terms, len(pool)) + 1):
        for names in itertools.combinations(pool, k):
            for e in solve_subset(names, tdim):
                key = tuple(sorted(zip(names, e)))
                if key in seen:
                    continue
                seen.add(key)
                n_combos += 1
                logv = sum(float(x) * np.log10(QUANTITIES[n][0]) for n, x in zip(names, e))
                logpre = np.log10(tval) - logv
                if abs(logpre) <= a.window:
                    expr = "*".join(f"{n}^{x}" for n, x in zip(names, e))
                    doms = sorted({QUANTITIES[n][2] for n in names})
                    hits.append(dict(expr=expr, prefactor=round(10**logpre, 6),
                                     log10_prefactor=round(logpre, 4),
                                     domains="+".join(doms),
                                     bridge=(tdom not in doms)))
    expected = n_combos * min(1.0, 2 * a.window / 6.0)
    surplus = len(hits) / expected if expected > 0 else float("inf")
    hits.sort(key=lambda h: abs(h["log10_prefactor"]))
    os.makedirs("bridge_results", exist_ok=True)
    out = f"bridge_results/{a.target}_{len(pool)}pool.jsonl"
    row = dict(target=a.target, target_domain=tdom, pool=pool, n_dim_valid_combos=n_combos,
               n_hits=len(hits), expected_by_chance=round(expected, 2),
               surplus=round(surplus, 3), window_decades=a.window, top_hits=hits[:15])
    with open(out, "a") as f:
        f.write(json.dumps(row) + "\n")
    with open("REGISTRY_FDR.md", "a") as f:
        f.write(f"| bridge:{a.target}/{len(pool)}pool | auto | {n_combos} dim-valid combos, "
                f"window 1e-{a.window:.0f}..1e{a.window:.0f} | {n_combos} | analytic log-uniform | yes (engine) |\n")
    print(f"[bridge] {a.target} ({tdom}): {n_combos} dimensionally-valid combos, "
          f"{len(hits)} in-window, {expected:.1f} expected by chance, SURPLUS = {surplus:.2f}")
    for h in hits[:5]:
        tag = "CROSS-DOMAIN BRIDGE" if h["bridge"] else "same-domain"
        print(f"[bridge]   {h['expr']}  prefactor={h['prefactor']}  [{tag}]")
    print(f"[bridge] next: feed interesting prefactors to mm_search --custom (simplicity pass); {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
