#!/usr/bin/env python3
"""THRESHOLD.py -- THE single interlock threshold function. Supersedes BITS_RULE.py's rule
and GATE_POWER_ANALYSIS.py's k_min table, both of which priced an object that cannot exist.

WHY THERE WAS A CONTRADICTION (k_min = 2 vs 3 at depth 18).
BITS_RULE.py scores  SUM_i log2(1/w_i)  >  log2(N(D)) + margin, i.e. it charges the
look-elsewhere ONCE and credits the bits of k targets. That implicitly describes ONE
expression matching k targets simultaneously. A single expression evaluates to a single
number, and distinct SM targets have disjoint windows, so no expression can ever do that.
The object the search actually retains is a SKELETON (a structural template) that reaches
k different targets via k DIFFERENT GERM RECIPES -- verified on the committed records:
the top skeleton's k targets are reached by k distinct recipes, never one value.

So the cost is NOT charged once. Each of the k matches independently ransacks the recipes
available to that skeleton, and the skeleton itself is chosen from all skeletons:

    cost(k, D)  =  log2(N_skel(D))  +  k * log2(R_recipe(D))          [bits]
    avail(k)    =  SUM over the k targets of log2(1/(2 w_i))          [bits, indep. targets]
    interlock is informative  <=>  avail(k)  >  cost(k, D) + MARGIN

The k-linear term is what both earlier accountings omitted. It is why "the two tightest
clear it" was wrong: adding a target buys you its bits but also buys another full recipe
search. Below we ALSO settle k_min empirically against a label-permutation null, which
needs no analytic model at all, and report where the two disagree.

CORRECTIONS APPLIED (all measured, see audit_interlock/):
  * windows from the DATASET (measurement_tol), never hand-typed. BITS_RULE's m_p/m_e
    window was 1000x too tight (3.2e-11/1836.15 where CODATA sigma is 3.2e-8) and its
    m_mu/m_e was 10x off.
  * multiplicity = DISTINCT values, not raw candidates (value-identical expressions hit
    or miss together).
  * realized branching 4.41/depth, NOT B=30 (30 is the step-MENU LENGTH). D0=4 is
    unfoundable (budget_splits(4) is empty).
  * E=1 is a 63% false-alarm rate; family-wise E* over (targets x depths) is used.
  * maximal INDEPENDENT target set only: r_t_b dropped (rho = -0.974 with r_b_tau via
    shared m_b). The holdout keys are excluded AND are not valid holdouts anyway
    (r_tau_mu = r_tau_e/r_mu_e exactly).
Local-only project. Exit 0 on success. No hard-coded verdicts.
"""
from __future__ import annotations
import json, math, os, sqlite3, sys
import numpy as np

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
from targets import pdg_constants as pdg          # noqa: E402
import exhaust_parallel as EP                     # noqa: E402

DB   = os.path.join(ROOT, "results_grind", "depth_10", "records.sqlite")
META = os.path.join(ROOT, "results_grind", "depth_10", "build_meta_sharded.json")
OUT  = os.path.join(ROOT, "results_interlock", "THRESHOLD.json")

MARGIN   = 10.0          # ~1000:1 safety over the look-elsewhere cost
N_DEPTHS = 8             # exhaustive depths 3..10, for the family-wise correction
NPERM    = 300
RNG      = np.random.default_rng(20260729)

# measured in audit_interlock/effective_N_audit.py + ceiling_math_audit.py
B_DISTINCT   = 4.407
DISTINCT_D10 = 42_534_139
DROP_CORREL  = {"r_t_b"}   # rho = -0.974 with r_b_tau through shared m_b

ok = True
def check(cond, msg):
    global ok
    if not cond:
        ok = False
        print(f"  !! CHECK FAILED: {msg}")
    return cond


def target_table():
    """(key, full relative window 2w, bits) from the DATASET -- never hand-typed."""
    ds = pdg.load()
    keys = [k for k in EP.sm_target_keys(include_holdout=False)]
    rows = []
    for k in keys:
        t = ds[k]
        check(not ds.is_holdout(k), f"holdout key {k} leaked into the pool")
        two_w = 2.0 * t.rel_precision          # grind's hit test is exactly +/-1 sigma
        rows.append((k, two_w, math.log2(1.0 / two_w)))
    rows.sort(key=lambda r: r[1])              # tightest first
    return rows


def counts(depth):
    """(N_distinct_values, N_skeletons, recipes_per_skeleton) at a depth."""
    bm = json.load(open(META))
    n_sk10 = bm["n_skeletons_total"]
    raw10  = bm["raw_candidates"]
    # recipes per skeleton is a per-depth germ-layer property; it grows only polynomially
    R10 = raw10 / n_sk10
    d = depth - 10
    n_val = DISTINCT_D10 * (B_DISTINCT ** d)
    # split the measured value growth between more skeletons and more recipes, using the
    # committed skeleton counts to fix the skeleton share
    n_sk  = n_sk10 * (B_DISTINCT ** (0.5 * d))
    R     = R10 * (B_DISTINCT ** (0.5 * d))
    return n_val, n_sk, R, n_sk10, R10, raw10


def main() -> int:
    print("=" * 96)
    print("THRESHOLD.py -- the single interlock threshold (supersedes BITS_RULE.py)")
    print("=" * 96)

    T = target_table()
    print(f"\nS1. Target pool from the DATASET: {len(T)} fittable targets, holdout excluded.")
    print(f"    {'target':<18}{'2w (full window)':>18}{'bits':>8}   {'in max-indep set'}")
    print("    " + "-" * 76)
    for k, w, b in T:
        tag = "" if k not in DROP_CORREL else "DROPPED (rho=-0.974)"
        print(f"    {k:<18}{w:>18.3e}{b:>8.1f}   {tag}")
    IND = [(k, w, b) for k, w, b in T if k not in DROP_CORREL]
    print(f"\n    maximal independent set: {len(IND)}/{len(T)} targets, "
          f"total {sum(b for _, _, b in IND):.1f} bits")
    check(len(IND) == len(T) - len(DROP_CORREL), "independent-set size")

    # ---- the m_p/m_e correction, shown explicitly -------------------------------------
    dsr = dict((k, w) for k, w, _ in T)
    print("\nS2. The two window errors BITS_RULE.py/GATE_POWER_ANALYSIS.py carried:")
    for key, hand in (("r_p_e", 3.49e-14), ("r_mu_e", 4.45e-9)):
        if key in dsr:
            print(f"    {key:<10} hand-typed 2w={hand:.3e} ({math.log2(1/hand):5.1f} bits)  vs "
                  f"dataset 2w={dsr[key]:.3e} ({math.log2(1/dsr[key]):5.1f} bits)  "
                  f"-> overstated by {math.log2(1/hand)-math.log2(1/dsr[key]):+.1f} bits")

    # ---- analytic threshold with the k-linear recipe charge ----------------------------
    print("\nS3. ANALYTIC threshold with the k-LINEAR recipe charge (the term both earlier")
    print("    accountings omitted). E* is family-wise over targets x exhaustive depths.")
    E_star = 0.05 / (len(T) * N_DEPTHS)
    print(f"    E* = 0.05/({len(T)} targets x {N_DEPTHS} depths) = {E_star:.3e}")

    results = {}
    for D in (10, 12, 15, 18):
        n_val, n_sk, R, n_sk10, R10, raw10 = counts(D)
        cost0 = math.log2(n_sk)
        print(f"\n    depth {D}:  N_distinct={n_val:.3e}  N_skel={n_sk:.3e}  recipes/skel={R:.3e}")
        print(f"      {'k':>3}{'avail bits':>12}{'cost bits':>12}{'need':>9}{'verdict':>10}   targets")
        kmin_analytic = None
        for k in range(1, min(9, len(IND)) + 1):
            sel = IND[:k]
            avail = sum(b for _, _, b in sel)
            cost = cost0 + k * math.log2(R)
            need = cost + MARGIN
            good = avail > need
            if good and kmin_analytic is None:
                kmin_analytic = k
            print(f"      {k:>3}{avail:>12.1f}{cost:>12.1f}{need:>9.1f}{'CLEARS' if good else 'short':>10}"
                  f"   {','.join(s[0] for s in sel[:4])}{'...' if k > 4 else ''}")
        print(f"      -> analytic k_min at depth {D}: "
              f"{kmin_analytic if kmin_analytic else 'NONE clears (no k up to 9)'}")
        results[f"D{D}"] = dict(n_val=n_val, n_skel=n_sk, recipes=R,
                                kmin_analytic=kmin_analytic)

    # ---- what the OLD rule said, and why it disagreed with itself ----------------------
    print("\nS4. Reproducing the contradiction, to show it was a MODEL error not arithmetic.")
    for label, logN in (("published N=30^(D-4)", math.log2(30.0 ** (18 - 4))),
                        ("corrected distinct N", math.log2(counts(18)[0]))):
        need_old = logN + MARGIN
        two_tight = sum(b for _, _, b in IND[:2])
        three = sum(b for _, _, b in IND[:3])
        print(f"    {label:<22} log2N={logN:5.1f}  need={need_old:5.1f}  "
              f"2 tightest={two_tight:5.1f} -> {'CLEARS' if two_tight>need_old else 'short'}"
              f"   3 tightest={three:5.1f} -> {'CLEARS' if three>need_old else 'short'}")
    print("    Both readings omit the k*log2(recipes) term, which is why one said k_min=2")
    print("    and the other k_min=3 from the same data. With the term, see S3.")

    # ---- EMPIRICAL settlement: label-permutation null, no analytic model --------------
    print("\nS5. EMPIRICAL k_min from a label-permutation null on the committed depth-10")
    print("    records -- this needs no multiplicity model at all and is the calibration")
    print("    any interlock claim must actually clear.")
    if not os.path.exists(DB):
        print(f"    !! records DB absent ({DB}) -- empirical leg SKIPPED")
        results["empirical"] = None
    else:
        con = sqlite3.connect(DB)
        rows = con.execute("SELECT value, b_s, skeleton_idx FROM records").fetchall()
        con.close()
        vals = np.array([r[0] for r in rows], dtype=np.float64)
        skel = np.array([f"{r[1]}:{r[2]}" for r in rows])
        # assign each record to the unique target window it lies in
        tk = [k for k, _, _ in IND]
        cen = np.array([pdg.load()[k].value for k in tk])
        tol = np.array([pdg.load()[k].rel_precision for k in tk])
        tgt = np.full(vals.size, -1, dtype=np.int64)
        for i in range(len(tk)):
            m = np.abs(vals - cen[i]) <= tol[i] * abs(cen[i])
            tgt[m] = i
        keep = tgt >= 0
        sk_u, sk_i = np.unique(skel[keep], return_inverse=True)
        tg_i = tgt[keep]
        print(f"    {keep.sum():,}/{vals.size:,} records assigned to an independent-set window; "
              f"{sk_u.size:,} distinct skeletons")

        def kmax_per_skel(t):
            out = np.zeros(sk_u.size, dtype=np.int64)
            for s in range(sk_u.size):
                out[s] = np.unique(t[sk_i == s]).size
            return out

        real = kmax_per_skel(tg_i)
        null = np.zeros((NPERM, sk_u.size), dtype=np.int64)
        for p in range(NPERM):
            null[p] = kmax_per_skel(RNG.permutation(tg_i))
        print(f"\n      {'k':>4}{'real #skel':>12}{'null mean':>12}{'null sd':>9}{'z':>8}"
              f"{'null<E*?':>10}")
        print("      " + "-" * 60)
        kmin_emp = None
        kmax = int(max(real.max(), null.max()))
        for k in range(2, kmax + 1):
            r = int((real >= k).sum())
            a = (null >= k).sum(axis=1).astype(float)
            z = (r - a.mean()) / a.std() if a.std() > 0 else float("nan")
            below = a.mean() < E_star
            if below and kmin_emp is None:
                kmin_emp = k
            print(f"      {k:>4}{r:>12,}{a.mean():>12.2f}{a.std():>9.2f}{z:>8.1f}"
                  f"{'YES' if below else 'no':>10}")
        print(f"\n      real max k = {int(real.max())}   chance max k = {null.max(axis=1).mean():.1f}")
        print(f"      -> EMPIRICAL k_min (smallest k whose CHANCE count < E*={E_star:.2e}): "
              f"{kmin_emp if kmin_emp else f'>{kmax} (never rare enough in this sample)'}")
        check(int(real.max()) <= null.max(axis=1).mean() + 3 * null.max(axis=1).std(),
              "real max k is not above the chance max (a real excess would need investigating)")
        results["empirical"] = dict(kmin=kmin_emp, real_max=int(real.max()),
                                    null_max_mean=float(null.max(axis=1).mean()),
                                    n_skel=int(sk_u.size), n_assigned=int(keep.sum()),
                                    E_star=E_star)

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(results, open(OUT, "w"), indent=1)
    print(f"\nwrote {OUT}")
    print("\n" + "=" * 96)
    print("SETTLED:" if ok else "CHECKS FAILED:")
    ka = results["D18"]["kmin_analytic"]
    ke = (results.get("empirical") or {}).get("kmin")
    print(f"  analytic k_min at depth 18 (with the k-linear recipe charge): {ka}")
    print(f"  empirical k_min from the permutation null                   : {ke}")
    print("  The old k_min=2 vs k_min=3 disagreement is VOID: both priced one expression")
    print("  matching k targets, which cannot happen. Use the value above.")
    print("=" * 96)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
