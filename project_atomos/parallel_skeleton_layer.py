#!/usr/bin/env python3
"""
parallel_skeleton_layer.py — build DN._skeleton_value_nodes(alpha, b_s) across cores, once, and cache it.

WHY. Measured 2026-07-27: the skeleton layer enumerates 11 * 30^b_s step sequences at ~90,000 seq/s.
    b_s=4:       8,910,000 seqs  ->    99 s
    b_s=5:     267,300,000 seqs  ->  49.5 min
    b_s=6:   8,019,000,000 seqs  ->  24.7 HOURS      <- depth 10's largest split
sharded_build.py has every shard rebuild this layer independently, so 12 shards spent 12 x 25 h of
REDUNDANT work on one 8-billion-sequence enumeration before any of them touched its own slice. That is
the real bottleneck at depth 10 -- not the dedup, and not the inner loop. Caching alone does not fix it
(one build is still 25 h); the layer itself has to be PARALLELISED. 12 cores -> ~2 h.

HOW IT PARTITIONS. _skeleton_value_nodes walks length-b_s step sequences from each base leaf. The
recursion therefore branches cleanly on (base leaf) x (first step) = 11 x 30 = 330 INDEPENDENT buckets.
Dedup is by _value_key, and a union of sets is order-independent, so
    union over buckets of (values that bucket reaches)  ==  the serial layer's value set.
Bucket b is assigned to worker (b % nworkers).

WHAT IS CACHED, and why not the objects. The deduped OUTPUT is tiny -- a few tens of thousands of
skeletons from billions of sequences -- but Reachable/ExprNode objects are awkward to serialise. So the
cache stores, per distinct value, the GENERATING RECIPE: (base leaf index, tuple of step indices). A
node is rebuilt from that in O(b_s) operations, so loading ~10^4 skeletons is instant.

REPRESENTATIVE CAVEAT, stated because it is real. The serial layer keeps the FIRST-SEEN node for each
distinct value in ITS enumeration order; a sharded build may keep a different node for the same value.
That is harmless downstream: the germ decoration _decorate(node, op, gk, e) evaluates to
value(node) (op) germ^e, so it depends only on the base node's VALUE and its (always dimensionless)
LABEL. Two representatives with the same _value_key therefore produce identical decorated values, hence
an identical build. Only formula ATTRIBUTION can differ -- already a documented limitation of
sharded_build.py.

RULE 3 note, honestly: DN's step_menu and _apply are NESTED inside _skeleton_value_nodes and cannot be
imported. They are reconstructed here from the same ingredients (alpha.leaves, _POW_EXPONENTS,
_UNARY_PLAIN, {MUL,DIV}) in the same order, and --validate PROVES equivalence by reproducing DN's own
value set exactly at a depth cheap enough to run serially. Nothing is trusted that is not reproduced.

USAGE
  python3 parallel_skeleton_layer.py --validate 4                  # must match DN exactly
  python3 parallel_skeleton_layer.py --bs 6 --worker K --nworkers 12
  python3 parallel_skeleton_layer.py --bs 6 --merge --nworkers 12
"""
from __future__ import annotations
import argparse, json, os, pickle, sys, time
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

import exhaust_depthN_forced as DN                                  # noqa: E402
from engine.expr_tree import ExprNode, OpType                       # noqa: E402
from exhaust import build_alphabet, _value_key, _POW_EXPONENTS, _UNARY_PLAIN  # noqa: E402
from mpmath import mp                                                # noqa: E402

OUT = Path(os.environ.get("ATOMOS_RESULTS_DIR") or (_HERE / "results_grind")) / "skeleton_cache"


def build_menu(alpha):
    """Reconstruct DN's 30-entry step menu in DN's order (verified by --validate)."""
    menu = []
    for lk in alpha.leaves:
        for op in (OpType.MUL, OpType.DIV):
            menu.append(("app", lk, op))
    for e in _POW_EXPONENTS:
        menu.append(("pow", e, None))
    for u in _UNARY_PLAIN:
        menu.append(("un", u, None))
    return menu


def apply_step(node, step):
    kind = step[0]
    if kind == "app":
        _, lk, op = step
        return ExprNode(op, children=[node, DN._leaf_node(lk)])
    if kind == "pow":
        _, e, _ = step
        return ExprNode(OpType.POW, children=[node], exp=e)
    _, u, _ = step
    return ExprNode(u, children=[node])


def rebuild(alpha, menu, leaf_i, seq):
    node = DN._leaf_node(alpha.leaves[leaf_i])
    for si in seq:
        node = apply_step(node, menu[si])
    return node


def worker(bs: int, wid: int, nworkers: int, verbose: bool = True) -> dict:
    alpha = build_alphabet()
    menu = build_menu(alpha)
    nm, nl = len(menu), len(alpha.leaves)
    seen, recipes = set(), []
    t0 = last = time.time()
    nseq = 0

    def emit(node, leaf_i, seq):
        nonlocal nseq
        nseq += 1
        try:
            v, lab = node.evaluate(alpha)
        except Exception:
            return
        if not lab.is_dimensionless():
            return
        try:
            if not mp.isfinite(v) or v <= 0:
                return
        except Exception:
            return
        vk = _value_key(v)
        if vk in seen:
            return
        seen.add(vk)
        recipes.append((vk, leaf_i, tuple(seq)))

    def walk(node, leaf_i, seq, remaining):
        nonlocal last
        if remaining == 0:
            emit(node, leaf_i, seq)
            if verbose and (nseq & 0xFFFFF) == 0:
                now = time.time()
                if now - last >= 60:
                    last = now
                    print(f"[skel w{wid}/{nworkers} b_s={bs}] seqs={nseq:,} distinct={len(seen):,} "
                          f"t={now-t0:.0f}s", flush=True)
            return
        for si in range(nm):
            walk(apply_step(node, menu[si]), leaf_i, seq + [si], remaining - 1)

    # buckets = (base leaf) x (first step); bucket index b -> worker b % nworkers
    b = 0
    for leaf_i in range(nl):
        base = DN._leaf_node(alpha.leaves[leaf_i])
        if bs == 0:
            if b % nworkers == wid:
                emit(base, leaf_i, [])
            b += 1
            continue
        for si in range(nm):
            if b % nworkers == wid:
                walk(apply_step(base, menu[si]), leaf_i, [si], bs - 1)
            b += 1
    OUT.mkdir(parents=True, exist_ok=True)
    p = OUT / f"bs{bs}_w{wid}of{nworkers}.pkl"
    with open(p, "wb") as f:
        pickle.dump({"bs": bs, "worker": wid, "nworkers": nworkers, "nseq": nseq,
                     "recipes": recipes}, f, protocol=4)
    print(f"[skel w{wid}/{nworkers} b_s={bs}] DONE seqs={nseq:,} distinct={len(seen):,} "
          f"wall={time.time()-t0:.0f}s", flush=True)
    return {"nseq": nseq, "distinct": len(seen)}


def merge(bs: int, nworkers: int) -> dict:
    seen, out, nseq = set(), [], 0
    for w in range(nworkers):
        p = OUT / f"bs{bs}_w{w}of{nworkers}.pkl"
        if not p.exists():
            raise SystemExit(f"missing worker {w} for b_s={bs}")
        d = pickle.load(open(p, "rb"))
        nseq += d["nseq"]
        for vk, leaf_i, seq in d["recipes"]:
            if vk not in seen:
                seen.add(vk); out.append((vk, leaf_i, seq))
    p = OUT / f"bs{bs}_MERGED.pkl"
    with open(p, "wb") as f:
        pickle.dump({"bs": bs, "nseq_total": nseq, "recipes": out}, f, protocol=4)
    print(f"[skel merge b_s={bs}] seqs={nseq:,} distinct={len(out):,} -> {p.name}")
    return {"nseq": nseq, "distinct": len(out)}


def load_layer(alpha, bs: int):
    """Rebuild the cached layer as DN-compatible Reachable objects. Returns None if uncached."""
    p = OUT / f"bs{bs}_MERGED.pkl"
    if not p.exists():
        return None
    menu = build_menu(alpha)
    d = pickle.load(open(p, "rb"))
    out = []
    for vk, leaf_i, seq in d["recipes"]:
        node = rebuild(alpha, menu, leaf_i, seq)
        v, lab = node.evaluate(alpha)
        out.append(DN.Reachable(v, lab, node.to_string(alpha), node.canonical_hash(), node))
    return out


def validate(bs: int, nworkers: int = 4) -> None:
    """THE GATE: the sharded+merged layer must reproduce DN's own value set EXACTLY."""
    alpha = build_alphabet()
    t0 = time.time()
    ref = DN._skeleton_value_nodes(alpha, bs)
    ref_keys = {_value_key(r.value) for r in ref}
    print(f"DN serial b_s={bs}: {len(ref):,} skeletons, {len(ref_keys):,} distinct keys "
          f"({time.time()-t0:.1f}s)")
    for w in range(nworkers):
        worker(bs, w, nworkers, verbose=False)
    m = merge(bs, nworkers)
    got = load_layer(alpha, bs)
    got_keys = {_value_key(r.value) for r in got}
    ok_n = len(got_keys) == len(ref_keys)
    ok_set = got_keys == ref_keys
    print(f"\n  sharded distinct keys = {len(got_keys):,}   serial = {len(ref_keys):,}   "
          f"{'MATCH' if ok_n else 'MISMATCH'}")
    print(f"  key SETS identical: {ok_set}")
    if not ok_set:
        print(f"    only-in-serial : {len(ref_keys - got_keys)}")
        print(f"    only-in-sharded: {len(got_keys - ref_keys)}")
    print(f"\n  VALIDATION {'PASSED' if (ok_n and ok_set) else 'FAILED'}")
    if not (ok_n and ok_set):
        raise SystemExit(1)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--bs", type=int)
    ap.add_argument("--worker", type=int)
    ap.add_argument("--nworkers", type=int, default=12)
    ap.add_argument("--merge", action="store_true")
    ap.add_argument("--validate", type=int, metavar="BS")
    a = ap.parse_args()
    if a.validate is not None:
        validate(a.validate, min(4, a.nworkers))
    elif a.merge:
        merge(a.bs, a.nworkers)
    else:
        worker(a.bs, a.worker, a.nworkers)
