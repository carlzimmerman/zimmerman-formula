#!/usr/bin/env python3
"""mm_search.py -- the million-monkeys expression engine.  Bounded RAM, deterministic,
FDR built in.  The LLM never holds the search space: it launches this and reads 3 lines.

  python mm_search.py --target alpha_inv --pack base --cmax 5
  python mm_search.py --target ckm_lambda --pack zimm --cmax 5 --ksigma 2

Enumerates arithmetic expressions over the pack's generators (ops + - * / and sqrt),
complexity = node count <= cmax, value-deduplicated, capped per level (--cap).  A HIT is
|value - target| <= ksigma * sigma.  The CHANCE BASELINE is computed on the same value
table against 120 pseudo-targets log-uniform within x/3..x3 of the target with the SAME
relative window; SURPLUS = hits/expected.  Verdict suggestion: NULL unless surplus >= 5.
CONVENTION-grade targets are refused (tautology guard).  Results: mm_results/*.jsonl and
one auto-appended REGISTRY_FDR.md row.
"""
import argparse, json, math, os, random, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from targets_sm import SM_TARGETS
from targets_zimmerman import ZIMMERMAN, PACKS


def enumerate_values(gens, cmax, cap):
    levels = {1: {}}
    for name, v in gens:
        levels[1][round(v, 12)] = (name, v)
    total = len(gens)
    for c in range(2, cmax + 1):
        cur = {}
        for v, (ex, val) in list(levels[c - 1].items()):
            if val > 1e-14:
                for nv, nex in ((math.sqrt(val), f"sqrt({ex})"),):
                    k = round(nv, 12)
                    if 1e-14 < abs(nv) < 1e14 and k not in cur:
                        cur[k] = (nex, nv)
        for ca in range(1, c - 1):
            cb = c - 1 - ca
            if cb < 1 or cb not in levels or ca not in levels:
                continue
            for va, (ea, xa) in levels[ca].items():
                for vb, (eb, xb) in levels[cb].items():
                    for nv, nex in ((xa + xb, f"({ea}+{eb})"), (xa - xb, f"({ea}-{eb})"),
                                    (xa * xb, f"({ea}*{eb})"),
                                    (xa / xb if xb != 0 else None, f"({ea}/{eb})")):
                        if nv is None or not (1e-14 < abs(nv) < 1e14):
                            continue
                        k = round(nv, 12)
                        if k not in cur:
                            cur[k] = (nex, nv)
                    if len(cur) > cap:
                        break
                if len(cur) > cap:
                    break
            if len(cur) > cap:
                break
        levels[c] = cur
        total += len(cur)
    allv = {}
    for c in sorted(levels):
        for k, (ex, v) in levels[c].items():
            if k not in allv:
                allv[k] = (ex, v, c)
    return allv, total


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", required=True)
    ap.add_argument("--custom", default=None, help="value,rel_tol for an ad-hoc target (e.g. from bridge_scan prefactors): --target myname --custom 0.5006,0.02")
    ap.add_argument("--pack", default="base", choices=sorted(PACKS))
    ap.add_argument("--cmax", type=int, default=5)
    ap.add_argument("--cap", type=int, default=250000)
    ap.add_argument("--ksigma", type=float, default=2.0)
    ap.add_argument("--reltol", type=float, default=None,
                    help="required for sigma-less targets")
    a = ap.parse_args()

    if a.custom:
        v, rel = a.custom.split(",")
        tgt = dict(v=float(v), s=abs(float(v)) * float(rel), note="custom (bridge prefactor)")
    else:
        tgt = SM_TARGETS.get(a.target) or ZIMMERMAN.get(a.target)
    if not tgt:
        sys.exit(f"unknown target {a.target}")
    if ZIMMERMAN.get(a.target, {}).get("grade") == "CONVENTION":
        sys.exit(f"REFUSED: {a.target} is CONVENTION-grade -- a match would be a tautology")
    t = tgt["v"]
    sig = tgt.get("s")
    if sig:
        w = a.ksigma * sig / abs(t)
    elif a.reltol:
        w = a.reltol
    else:
        sys.exit("sigma-less target: pass --reltol explicitly (and defend it in the ledger)")

    allv, n_expr = enumerate_values(PACKS[a.pack], a.cmax, a.cap)
    hits = [(ex, v, c, abs(v - t) / (sig if sig else abs(t) * w))
            for (ex, v, c) in allv.values() if abs(v - t) <= w * abs(t)]
    hits.sort(key=lambda h: h[3])

    rng = random.Random(0)
    counts = []
    vals = [v for (_, v, _) in allv.values()]
    for _ in range(120):
        pt = t * 10 ** rng.uniform(-0.477, 0.477)
        lo, hi = pt * (1 - w), pt * (1 + w)
        if lo > hi:
            lo, hi = hi, lo
        counts.append(sum(1 for v in vals if lo <= v <= hi))
    exp = sum(counts) / len(counts)
    surplus = (len(hits) / exp) if exp > 0 else float("inf")

    os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)), "mm_results"), exist_ok=True)
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mm_results",
                       f"{a.target}_{a.pack}_c{a.cmax}.jsonl")
    row = dict(target=a.target, value=t, sigma=sig, pack=a.pack, cmax=a.cmax,
               window_rel=w, n_expr_enumerated=n_expr, n_distinct_values=len(allv),
               n_hits=len(hits), expected_by_chance=round(exp, 2),
               surplus=round(surplus, 3),
               verdict_suggestion=("CANDIDATE-ESCALATE" if surplus >= 5 and len(hits) > 0
                                   else "NULL"),
               top_hits=[dict(expr=ex, value=v, complexity=c, sigmas=round(s, 2))
                         for ex, v, c, s in hits[:12]])
    with open(out, "a") as f:
        f.write(json.dumps(row) + "\n")
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "REGISTRY_FDR.md"), "a") as f:
        f.write(f"| mm:{a.target}/{a.pack}/c{a.cmax} | auto | {n_expr} expressions, "
                f"window {w:.2e} rel | {n_expr} | 120 pseudo-targets on same table | yes (engine) |\n")
    print(f"[mm] {a.target} pack={a.pack} cmax={a.cmax}: {len(hits)} hits, "
          f"{exp:.1f} expected by chance, SURPLUS = {surplus:.2f}")
    print(f"[mm] suggestion: {row['verdict_suggestion']}  (details: {out})")
    if hits:
        print(f"[mm] best: {hits[0][0]} = {hits[0][1]:.10g} ({hits[0][3]:.2f} sigma)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
