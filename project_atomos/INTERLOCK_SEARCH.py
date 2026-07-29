#!/usr/bin/env python3
"""INTERLOCK_SEARCH.py -- multi-target interlock search, calibrated by PERMUTATION NULL.

WHAT THIS SEARCHES FOR. Not "one expression matching k constants" -- that is impossible
(one expression = one number, and distinct targets have disjoint windows). The object is a
SKELETON (structural template) that reaches k different targets via k DIFFERENT germ
recipes. That is what the committed records actually contain.

WHY A PERMUTATION NULL AND NOT ANALYTIC BITS. The analytic rule
`SUM_i log2(1/w_i) > log2(N(D)) + margin` charges the look-elsewhere ONCE while crediting k
targets, and it certifies noise: on the real depth-10 records a k=3 set advertises 93.8 bits
and clears a 78.7-bit threshold while its true independent content is 65.2. THRESHOLD.py
restores the missing k*log2(recipes) term; this script bypasses analytic modelling entirely
by comparing against a LABEL-PERMUTATION null that preserves (a) the per-skeleton hit
multiplicity and (b) the very lopsided per-target marginal. Chance alone puts a skeleton on
10 of 19 targets, so nothing below that is evidence of anything.

CONSTRAINTS ENFORCED (all established in audit_interlock/):
  * MAXIMAL INDEPENDENT TARGET SET only. r_t_b dropped (rho = -0.974 with r_b_tau via shared
    m_b). Holdout keys excluded -- and note they are NOT valid holdouts anyway
    (r_tau_mu = r_tau_e/r_mu_e exactly), so a survivor here is NOT out-of-sample validated.
  * Windows read from the DATASET (rel_precision, +/-1 sigma), never hand-typed.
  * Family-wise threshold over (targets x exhaustive depths).

POSITIVE CONTROL IS MANDATORY. `--selftest` plants a synthetic skeleton reaching k targets
ABOVE the chance ceiling and requires the search to flag it, and plants one BELOW the ceiling
and requires the search NOT to flag it. If either fails, the search is broken and any null it
reports is worthless -- the script exits nonzero and refuses to report a null.

Usage:
  python3 INTERLOCK_SEARCH.py --selftest          # controls only, fast
  python3 INTERLOCK_SEARCH.py --depth 10          # real search at a depth
  python3 INTERLOCK_SEARCH.py --depth 10 --nperm 1000
Local-only project. Exit 0 = trustworthy result. No hard-coded verdicts.
"""
from __future__ import annotations
import argparse, json, math, os, sqlite3, sys
import numpy as np

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
from targets import pdg_constants as pdg          # noqa: E402
import exhaust_parallel as EP                     # noqa: E402

OUTDIR      = os.path.join(ROOT, "results_interlock")
DROP_CORREL = {"r_t_b"}          # rho = -0.974 with r_b_tau (shared m_b)
N_DEPTHS    = 8                  # exhaustive depths 3..10, for the family-wise correction
ALPHA_FW    = 0.05


def log(msg, fh=None):
    print(msg, flush=True)
    if fh:
        fh.write(msg + "\n"); fh.flush()


def independent_targets():
    """Maximal independent set, tightest first, windows from the DATASET."""
    ds = pdg.load()
    rows = []
    for k in EP.sm_target_keys(include_holdout=False):
        if ds.is_holdout(k) or k in DROP_CORREL:
            continue
        t = ds[k]
        rows.append((k, float(t.value), float(t.rel_precision)))
    rows.sort(key=lambda r: r[2])
    return rows


def assign(values, tgts):
    """Map each value to the unique independent-set window it falls in, or -1."""
    out = np.full(values.size, -1, dtype=np.int64)
    for i, (_, cen, rel) in enumerate(tgts):
        m = np.abs(values - cen) <= rel * abs(cen)
        out[m] = i
    return out


def k_per_skeleton(skel_idx, tgt_idx, n_skel):
    """Distinct targets reached by each skeleton. Vectorised: unique (skel,tgt) pairs."""
    pair = skel_idx.astype(np.int64) * (tgt_idx.max() + 2) + tgt_idx
    uniq = np.unique(pair)
    sk = (uniq // (tgt_idx.max() + 2)).astype(np.int64)
    return np.bincount(sk, minlength=n_skel)


def calibrate(skel_idx, tgt_idx, n_skel, nperm, rng, fh=None):
    """Permutation null on the max-k statistic and on the >=k counts."""
    real_k = k_per_skeleton(skel_idx, tgt_idx, n_skel)
    real_max = int(real_k.max()) if real_k.size else 0
    null_max = np.zeros(nperm, dtype=np.int64)
    kmax_scan = max(real_max, 1) + 6
    null_ge = np.zeros((nperm, kmax_scan + 1), dtype=np.int64)
    for p in range(nperm):
        pk = k_per_skeleton(skel_idx, rng.permutation(tgt_idx), n_skel)
        null_max[p] = pk.max() if pk.size else 0
        for k in range(2, kmax_scan + 1):
            null_ge[p, k] = int((pk >= k).sum())
    return real_k, real_max, null_max, null_ge, kmax_scan


def report(real_k, real_max, null_max, null_ge, kmax_scan, n_tgt, fh=None):
    """Flag skeletons whose k beats the permutation ceiling at family-wise alpha."""
    e_star = ALPHA_FW / (n_tgt * N_DEPTHS)
    log(f"\n  {'k':>4}{'real #skel':>12}{'chance mean':>13}{'chance sd':>11}{'z':>8}"
        f"{'chance<E*':>11}", fh)
    log("  " + "-" * 60, fh)
    k_required = None
    for k in range(2, kmax_scan + 1):
        r = int((real_k >= k).sum())
        a = null_ge[:, k].astype(float)
        z = (r - a.mean()) / a.std() if a.std() > 0 else float("nan")
        rare = a.mean() < e_star
        if rare and k_required is None:
            k_required = k
        log(f"  {k:>4}{r:>12,}{a.mean():>13.2f}{a.std():>11.2f}{z:>8.1f}"
            f"{'YES' if rare else 'no':>11}", fh)
    # p-value of the observed maximum against the permutation distribution of maxima
    p_max = float((null_max >= real_max).mean())
    log(f"\n  observed max k = {real_max}   chance max k = {null_max.mean():.2f} "
        f"+/- {null_max.std():.2f}   p(chance >= observed) = {p_max:.4f}", fh)
    log(f"  family-wise E* = {e_star:.3e}  ->  a claim needs k >= "
        f"{k_required if k_required else f'>{kmax_scan}'}", fh)
    flagged = (p_max < e_star) and (k_required is not None) and (real_max >= k_required)
    return dict(real_max=real_max, p_max=p_max, e_star=e_star,
                k_required=k_required, flagged=bool(flagged),
                chance_max_mean=float(null_max.mean()))


def synth(n_skel_bg, k_plant, n_tgt, rng, hits_per_target=3):
    """Background skeletons with realistic lopsided marginals + one planted skeleton."""
    # lopsided per-target marginal, like the real data (loose targets take almost all hits)
    w = np.geomspace(1.0, 400.0, n_tgt)
    w = w / w.sum()
    sk, tg = [], []
    for s in range(n_skel_bg):
        nh = int(rng.integers(1, 30))
        sk.extend([s] * nh)
        tg.extend(rng.choice(n_tgt, size=nh, p=w).tolist())
    plant = n_skel_bg
    chosen = rng.choice(n_tgt, size=k_plant, replace=False)
    for t in chosen:
        sk.extend([plant] * hits_per_target)
        tg.extend([int(t)] * hits_per_target)
    return np.array(sk, dtype=np.int64), np.array(tg, dtype=np.int64), n_skel_bg + 1


def selftest(nperm, seed) -> int:
    rng = np.random.default_rng(seed)
    tgts = independent_targets()
    n_tgt = len(tgts)
    log("=" * 92)
    log("SELFTEST -- planted positive and negative controls (MANDATORY before any null)")
    log("=" * 92)
    log(f"  independent target set: {n_tgt} targets "
        f"(holdout excluded, {sorted(DROP_CORREL)} dropped on correlation)")

    # first: what IS the chance ceiling on synthetic background alone?
    sk, tg, ns = synth(2000, 0, n_tgt, np.random.default_rng(seed + 1))
    _, _, nm, _, _ = calibrate(sk, tg, ns, nperm, np.random.default_rng(seed + 2))
    ceiling = nm.mean() + 3 * nm.std()
    log(f"\n  synthetic background chance ceiling (mean+3sd of max k): {ceiling:.1f}")

    results = {}
    # POSITIVE control: plant well above the ceiling -> MUST be flagged
    k_pos = min(n_tgt, int(math.ceil(ceiling)) + 4)
    sk, tg, ns = synth(2000, k_pos, n_tgt, np.random.default_rng(seed + 3))
    rk, rmax, nm, ng, kx = calibrate(sk, tg, ns, nperm, np.random.default_rng(seed + 4))
    log(f"\n  POSITIVE CONTROL: planted one skeleton on k={k_pos} independent targets")
    pos = report(rk, rmax, nm, ng, kx, n_tgt)
    results["positive"] = dict(planted_k=k_pos, **pos)
    log(f"  -> {'PASS: recovered' if pos['flagged'] else 'FAIL: MISSED the plant'}")

    # NEGATIVE control: plant inside the chance band -> MUST NOT be flagged
    k_neg = max(2, int(ceiling) - 3)
    sk, tg, ns = synth(2000, k_neg, n_tgt, np.random.default_rng(seed + 5))
    rk, rmax, nm, ng, kx = calibrate(sk, tg, ns, nperm, np.random.default_rng(seed + 6))
    log(f"\n  NEGATIVE CONTROL: planted one skeleton on k={k_neg} (inside the chance band)")
    neg = report(rk, rmax, nm, ng, kx, n_tgt)
    results["negative"] = dict(planted_k=k_neg, **neg)
    log(f"  -> {'PASS: correctly not flagged' if not neg['flagged'] else 'FAIL: FALSE POSITIVE'}")

    os.makedirs(OUTDIR, exist_ok=True)
    json.dump(results, open(os.path.join(OUTDIR, "SELFTEST.json"), "w"), indent=1)
    good = results["positive"]["flagged"] and not results["negative"]["flagged"]
    log("\n" + "=" * 92)
    log("SELFTEST PASSED -- the search can recover a real interlock and rejects a fake one."
        if good else
        "SELFTEST FAILED -- DO NOT TRUST ANY NULL FROM THIS SEARCH.")
    log("=" * 92)
    return 0 if good else 1


def real_search(depth, nperm, seed) -> int:
    db = os.path.join(ROOT, "results_grind", f"depth_{depth}", "records.sqlite")
    if not os.path.exists(db):
        log(f"ERROR: no records at {db}")
        return 2
    os.makedirs(OUTDIR, exist_ok=True)
    fh = open(os.path.join(OUTDIR, f"interlock_depth{depth}.log"), "w")
    log("=" * 92, fh)
    log(f"INTERLOCK SEARCH -- depth {depth}, permutation-calibrated", fh)
    log("=" * 92, fh)

    tgts = independent_targets()
    n_tgt = len(tgts)
    log(f"  independent target set: {n_tgt} targets; holdout excluded; "
        f"dropped on correlation: {sorted(DROP_CORREL)}", fh)
    log("  NOTE: the holdout keys are NOT valid out-of-sample tests "
        "(r_tau_mu = r_tau_e/r_mu_e exactly), so nothing here is holdout-validated.", fh)

    con = sqlite3.connect(db)
    rows = con.execute("SELECT value, b_s, skeleton_idx FROM records").fetchall()
    con.close()
    vals = np.array([r[0] for r in rows], dtype=np.float64)
    skl = np.array([f"{r[1]}:{r[2]}" for r in rows])
    tgt = assign(vals, tgts)
    keep = tgt >= 0
    dropped = int((~keep).sum())
    sk_u, sk_i = np.unique(skl[keep], return_inverse=True)
    log(f"  {int(keep.sum()):,}/{vals.size:,} records lie in an independent-set window "
        f"({dropped:,} dropped: holdout/correlated/outside)", fh)
    log(f"  {sk_u.size:,} distinct skeletons carry those hits", fh)

    rk, rmax, nm, ng, kx = calibrate(sk_i, tgt[keep], sk_u.size, nperm,
                                     np.random.default_rng(seed), fh)
    log(f"\n  LABEL-PERMUTATION NULL ({nperm} permutations; preserves per-skeleton hit "
        f"multiplicity and per-target marginal)", fh)
    res = report(rk, rmax, nm, ng, kx, n_tgt, fh)

    if res["flagged"]:
        best = np.argsort(-rk)[:5]
        log("\n  *** CANDIDATE INTERLOCKS (assess before believing) ***", fh)
        for b in best:
            log(f"      skeleton {sk_u[b]}: k={int(rk[b])} independent targets", fh)
    else:
        log(f"\n  NULL: no skeleton reaches k >= {res['k_required']} "
            f"(observed max {res['real_max']}, chance max {res['chance_max_mean']:.1f}, "
            f"p={res['p_max']:.4f}). Nothing survives.", fh)

    res.update(depth=depth, n_records=int(vals.size), n_assigned=int(keep.sum()),
               n_dropped=dropped, n_skeletons=int(sk_u.size), n_targets=n_tgt, nperm=nperm)
    json.dump(res, open(os.path.join(OUTDIR, f"interlock_depth{depth}.json"), "w"), indent=1)
    log(f"\nwrote {OUTDIR}/interlock_depth{depth}.json", fh)
    fh.close()
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--depth", type=int, default=None)
    ap.add_argument("--nperm", type=int, default=300)
    ap.add_argument("--seed", type=int, default=20260729)
    a = ap.parse_args()
    if a.selftest:
        return selftest(a.nperm, a.seed)
    if a.depth is None:
        ap.error("give --depth D or --selftest")
    # controls gate the real run: refuse to report a null from an unvalidated search
    log("running mandatory controls before the real search ...\n")
    if selftest(min(a.nperm, 200), a.seed) != 0:
        log("\nREFUSING to run the real search: controls failed.")
        return 1
    log("\n")
    return real_search(a.depth, a.nperm, a.seed)


if __name__ == "__main__":
    sys.exit(main())
