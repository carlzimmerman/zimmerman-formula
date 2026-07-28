#!/usr/bin/env python3
"""
sharded_build.py — parallelise the EXHAUSTIVE depth-D value build across cores, by skeleton index.

WHY. grind.py's streamed_build is single-threaded and its wall time scales ~14.5x per depth while the
raw candidate count scales only ~4.7x (measured: depth 8 = 8,123,807 raw / 383 s; depth 9 = 38,450,388
raw / 5,547 s). The superlinear part is the growing dedup set, not the enumeration. Extrapolated
single-threaded cost: depth 10 ~22 h, depth 11 ~13.5 d, depth 12 ~195 d. On a 16-core box that is a
waste, and an EXHAUSTIVE depth is worth far more than more sampling: a null there is a THEOREM, and
BITS_RULE.py shows a hit at depth 10 needs only ~39 bits to clear look-elsewhere versus ~79 at depth 18.

RULE 3 (verbatim reuse). This file adds NO logic to gate/ engine/ exhaust*.py / grind.py. It imports
the committed machinery unmodified and replicates streamed_build's split/skeleton/recipe loop and its
filter ORDER verbatim (evaluate -> finite&>0 -> dimensionless -> _value_key dedup). The ONLY change is
that shard `i` of `N` processes skeletons with (si % N == i), keeping its own dedup set.

WHY SHARDING BY SKELETON INDEX IS CORRECT. streamed_build accumulates one global `vals`/`seen_value`
across all budget splits. Dedup by _value_key is a SET UNION, which is order-independent, so
    union over shards of (values found by that shard)  ==  values found by the serial build.
Sharding by skeleton index (rather than by budget split) also load-balances: the splits are wildly
unequal in size, so by-split parallelism is limited by the largest one.

HONEST LIMITATION, stated because it is real. The serial build records values in FIRST-SEEN order and
spills the FIRST-SEEN formula for each in-window value. A sharded build sees skeletons in a different
order, so for a value reachable by several formulas the RECORDED FORMULA may differ from the serial
build's. That does NOT affect the value SET, the distinct count, or the hit set — so it does not affect
a null or a completeness claim. It only affects which of several equivalent formulas is attributed.
Do not use this script's records to claim "the formula is X"; use it for the value set and the hits.

USAGE
  python3 sharded_build.py --validate 8          # reproduce depth 8 serially-known counts, sharded
  python3 sharded_build.py --depth 10 --shard 0 --nshards 12    # one worker
  python3 sharded_build.py --depth 10 --merge --nshards 12      # union the shards
"""
from __future__ import annotations
import argparse, json, os, sys, time
from array import array
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

import exhaust_depthN_forced as DN                      # noqa: E402
import exhaust_depth5_forced as D5                      # noqa: E402
from exhaust import build_alphabet, _value_key          # noqa: E402
import parallel_skeleton_layer as PSL                    # noqa: E402
import sqlite3                                           # noqa: E402
# grind's retention helpers, imported VERBATIM so the record schema and the target windows are
# byte-identical to what the sweep expects. Needed because the sweep gates a hit by REBUILDING its
# ExprNode from (skeleton index, germ recipe) -- so without records there is nothing to gate.
from grind import _target_windows, _recipe_to_json, _db_open   # noqa: E402
from mpmath import mp                                    # noqa: E402

OUT = Path(os.environ.get("ATOMOS_RESULTS_DIR") or (_HERE / "results_grind"))


def shard_build(depth: int, shard: int, nshards: int, verbose: bool = True) -> dict:
    """Enumerate the depth-D dimensionless value set for skeletons with si % nshards == shard."""
    alpha = build_alphabet()
    free_keys = D5._free_germ_keys(alpha)
    splits = DN.budget_splits(depth)
    seen, vals, raw, nsk = set(), array("d"), 0, 0
    wins = _target_windows()          # includes the holdout: retention is not a search (see grind.py:294)
    ddir0 = OUT / f"depth_{depth}" / "shards"
    ddir0.mkdir(parents=True, exist_ok=True)
    dbp = ddir0 / f"records_shard{shard}of{nshards}.sqlite"
    if dbp.exists():
        dbp.unlink()
    con = _db_open(dbp)
    pending: list = []
    n_retained = 0
    def _flush():
        nonlocal pending
        if pending:
            con.executemany("INSERT OR REPLACE INTO records VALUES (?,?,?,?,?,?,?)", pending)
            con.commit()
            pending = []
    # PERSIST THE VALUE KEYS. _value_key returns an mpmath-PRECISION STRING; a float64 round-trip
    # changes it, so re-keying floats at merge time collapses values the serial build keeps distinct.
    # That bug cost 413,199 of depth 8's 2,207,173 distinct values (19%) and was caught by --validate.
    keys_out: list = []
    t0 = last = time.time()
    for (b_s, g_s) in splits:
        # USE THE CACHED LAYER IF PRESENT. Measured: the layer costs 11*30^b_s sequences at ~90k/s, so
        # b_s=6 is ~25 h -- and EVERY shard was rebuilding it independently, which was the real depth-10
        # bottleneck (12 x 25 h of identical work before any shard reached its own slice). The cache is
        # built once, in parallel, by parallel_skeleton_layer.py and validated to reproduce DN's value
        # set EXACTLY. Falls back to DN verbatim when no cache exists, so behaviour is unchanged without one.
        skeletons = PSL.load_layer(alpha, b_s)
        if skeletons is None:
            skeletons = DN._skeleton_value_nodes(alpha, b_s)
        elif verbose:
            print(f"[shard {shard} d{depth}] using CACHED skeleton layer b_s={b_s}: "
                  f"{len(skeletons):,} skeletons", flush=True)
        recipes = list(DN._germ_recipes(alpha, free_keys, g_s))
        mine = [(si, sk) for si, sk in enumerate(skeletons) if si % nshards == shard]
        nsk += len(mine)
        if verbose:
            print(f"[shard {shard}/{nshards} d{depth}] split(b_s={b_s},g_s={g_s}): "
                  f"{len(mine)}/{len(skeletons)} skeletons x {len(recipes)} recipes", flush=True)
        for si, sk in mine:
            for recipe in recipes:
                node = sk.node
                for (gk, op, e) in recipe:
                    node = DN._decorate(node, op, gk, e)
                raw += 1
                # --- filter ORDER verbatim from grind.streamed_build / DN.constructive_gate_b_reachables
                try:
                    value, label = node.evaluate(alpha)
                except Exception:
                    continue
                try:
                    if not mp.isfinite(value) or value <= 0:
                        continue
                except Exception:
                    continue
                if not label.is_dimensionless():
                    continue
                vk = _value_key(value)
                if vk in seen:
                    continue
                seen.add(vk)
                fv = float(value)
                vals.append(fv)
                keys_out.append(vk)
                # retention: spill a formula record iff fv is inside ANY widened target window.
                # Filter order and record tuple copied verbatim from grind.streamed_build.
                for (_tk, tv, _tol, wabs) in wins:
                    if abs(fv - tv) <= wabs:
                        pending.append((len(vals) - 1, vk, fv, node.to_string(alpha),
                                        b_s, si, _recipe_to_json(recipe)))
                        n_retained += 1
                        if len(pending) >= 1000:
                            _flush()
                        break
                if (len(vals) & 0x3FFF) == 0 and verbose:
                    now = time.time()
                    if now - last >= 60:
                        last = now
                        print(f"[shard {shard} d{depth}] raw={raw:,} distinct={len(vals):,} "
                              f"t={now-t0:.0f}s", flush=True)
    _flush(); con.close()
    ddir = OUT / f"depth_{depth}" / "shards"
    ddir.mkdir(parents=True, exist_ok=True)
    with open(ddir / f"values_shard{shard}of{nshards}.f64", "wb") as f:
        vals.tofile(f); f.flush(); os.fsync(f.fileno())
    with open(ddir / f"keys_shard{shard}of{nshards}.txt", "w") as f:
        f.write("\n".join(keys_out)); f.write("\n"); f.flush(); os.fsync(f.fileno())
    meta = dict(depth=depth, shard=shard, nshards=nshards, raw_candidates=raw,
                distinct_by_value=len(vals), n_skeletons=nsk, n_retained_records=n_retained,
                wall_s=round(time.time()-t0, 1))
    (ddir / f"meta_shard{shard}of{nshards}.json").write_text(json.dumps(meta, indent=2))
    print(f"[shard {shard}/{nshards} d{depth}] DONE raw={raw:,} distinct={len(vals):,} "
          f"wall={meta['wall_s']}s", flush=True)
    return meta


def merge(depth: int, nshards: int) -> dict:
    """Union the shard value sets. The union is order-independent, so the distinct COUNT equals the
    serial build's; see the module docstring on formula attribution."""
    ddir = OUT / f"depth_{depth}" / "shards"
    seen, vals, raw_tot, nsk_tot = set(), array("d"), 0, 0
    vk_index: dict = {}      # value_key -> index in the MERGED array (see the remap note below)
    for i in range(nshards):
        mp_ = ddir / f"meta_shard{i}of{nshards}.json"
        vp = ddir / f"values_shard{i}of{nshards}.f64"
        kp = ddir / f"keys_shard{i}of{nshards}.txt"
        if not (mp_.exists() and vp.exists() and kp.exists()):
            raise SystemExit(f"missing shard {i} (need meta+values+keys): run it before merging")
        m = json.loads(mp_.read_text()); raw_tot += m["raw_candidates"]; nsk_tot += m["n_skeletons"]
        a = array("d"); a.fromfile(open(vp, "rb"), vp.stat().st_size // 8)
        # union on the PERSISTED mpmath-precision keys, paired positionally with the float values.
        # NEVER re-key from float64 here -- that was the 19%-loss bug.
        with open(kp) as fh:
            ks = fh.read().split("\n")
        if ks and ks[-1] == "":
            ks.pop()
        if len(ks) != len(a):
            raise SystemExit(f"shard {i}: {len(ks)} keys vs {len(a)} values -- corrupt shard")
        for k, v in zip(ks, a):
            if k not in seen:
                seen.add(k); vk_index[k] = len(vals); vals.append(v)
    # ---- merge the per-shard record DBs, REMAPPING idx to the MERGED position -----------------
    # BUG FOUND 2026-07-28 by grind's own REBUILD MISMATCH guard, and it was mine. Each shard wrote
    # idx = len(vals)-1, which is SHARD-LOCAL. In grind's serial build that IS the global index; here it
    # is not. Two consequences, both silent: (a) the sweep looks up values[idx] in the MERGED array and
    # compares it to the record's stored value, which then disagree -- that is the mismatch that fired;
    # (b) `idx INTEGER PRIMARY KEY` means colliding shard-local indices were REPLACED on insert, so
    # records were LOST as well as misaligned. Fix: key the remap on value_key, whose merged position is
    # known because `seen`/`vals` above were built in merged order.
    out = OUT / f"depth_{depth}"
    dbo = out / "records.sqlite"
    if dbo.exists():
        dbo.unlink()
    cono = _db_open(dbo)
    nrec = ndrop = 0
    for i in range(nshards):
        dbi = ddir / f"records_shard{i}of{nshards}.sqlite"
        if not dbi.exists():
            raise SystemExit(f"missing record DB for shard {i}")
        ci = sqlite3.connect(str(dbi))
        rows = ci.execute("SELECT idx, value_key, value, formula, b_s, skeleton_idx, recipe "
                          "FROM records").fetchall()
        ci.close()
        fixed = []
        for (_idx, vkey, val, formula, b_s, sk_i, rec) in rows:
            gi = vk_index.get(vkey)
            if gi is None:          # a record whose value never made the merged set: impossible, but loud
                ndrop += 1
                continue
            fixed.append((gi, vkey, val, formula, b_s, sk_i, rec))
        if fixed:
            cono.executemany("INSERT OR REPLACE INTO records VALUES (?,?,?,?,?,?,?)", fixed)
            nrec += len(fixed)
    cono.commit()
    nuniq = cono.execute("SELECT COUNT(*) FROM records").fetchone()[0]
    cono.close()
    print(f"[merge d{depth}] records: {nrec:,} remapped -> {nuniq:,} rows"
          f"{f' ({ndrop} DROPPED -- investigate)' if ndrop else ''}")
    with open(out / "values_merged.f64", "wb") as f:
        vals.tofile(f); f.flush(); os.fsync(f.fileno())
    meta = dict(depth=depth, build="sharded-merged", nshards=nshards,
                raw_candidates=raw_tot, distinct_by_value=len(vals),
                n_skeletons_total=nsk_tot,
                note="distinct count is union-exact vs the serial build; first-seen FORMULA "
                     "attribution may differ (see module docstring)")
    (out / "build_meta_sharded.json").write_text(json.dumps(meta, indent=2))
    print(f"[merge d{depth}] raw={raw_tot:,} distinct={len(vals):,}")
    return meta


def validate(depth: int, nshards: int = 4) -> None:
    """Reproduce a serially-known depth with the SHARDED path. This is the correctness gate: if the
    sharded+merged distinct count does not equal the committed serial one, the shard logic is wrong."""
    serial = json.loads((OUT / f"depth_{depth}" / "build_meta.json").read_text())
    print(f"serial depth {depth}: raw={serial['raw_candidates']:,} "
          f"distinct={serial['distinct_by_value']:,}")
    for i in range(nshards):
        shard_build(depth, i, nshards, verbose=False)
    m = merge(depth, nshards)
    ok_raw = m["raw_candidates"] == serial["raw_candidates"]
    ok_dis = m["distinct_by_value"] == serial["distinct_by_value"]
    print(f"\n  raw      sharded={m['raw_candidates']:,} serial={serial['raw_candidates']:,} "
          f"-> {'MATCH' if ok_raw else 'MISMATCH'}")
    print(f"  distinct sharded={m['distinct_by_value']:,} serial={serial['distinct_by_value']:,} "
          f"-> {'MATCH' if ok_dis else 'MISMATCH'}")
    print(f"\n  VALIDATION {'PASSED' if (ok_raw and ok_dis) else 'FAILED'}")
    if not (ok_raw and ok_dis):
        raise SystemExit(1)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--depth", type=int)
    ap.add_argument("--shard", type=int)
    ap.add_argument("--nshards", type=int, default=12)
    ap.add_argument("--merge", action="store_true")
    ap.add_argument("--validate", type=int, metavar="D")
    a = ap.parse_args()
    if a.validate is not None:
        validate(a.validate, min(4, a.nshards))
    elif a.merge:
        merge(a.depth, a.nshards)
    else:
        shard_build(a.depth, a.shard, a.nshards)
