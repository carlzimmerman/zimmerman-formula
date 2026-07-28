#!/usr/bin/env python3
"""
exhaust_parallel.py — the BY-TARGET parallel launcher for the deterministic exhauster.

WHAT THIS IS (Carl's PROJECT_ATOMOS flavor PUSH, 2026-06-25):
    exhaust.py COMPLETELY exhausts ONE target at depth-3 over the right-shape alphabet
    (now EXTENDED with the flavor-group / Koide / rep-dim germs). It is deterministic and
    exhaustive, so the natural parallelism is EMBARRASSINGLY by TARGET: each SM target is an
    INDEPENDENT complete exhaustion (no shared state, no RNG, no look-elsewhere coupling
    beyond the fixed n_targets multiplicity). This launcher splits the ~21 SM targets across
    N detached worker processes; each worker COMPLETELY exhausts its slice and writes:
        results_exhaust/shard_K/result.json   = [{target, space_size, n_dim_valid, hits[]}, ...]
        results_exhaust/shard_K/run.log       = the human-readable exhaust.py reports
    --status aggregates the shards into the per-target ledger; --stop kills running workers.

WHY BY-TARGET (not by-seed like run_atomos_parallel.py):
    run_atomos.py is a STOCHASTIC search -> its launcher fans DIFFERENT SEEDS over the SAME
    target set (different trajectories). exhaust.py is DETERMINISTIC + COMPLETE -> there is
    nothing stochastic to fan; the only axis to parallelize is the target set. Splitting
    targets keeps each worker's job a WHOLE exhaustion (completeness stays a per-target
    theorem inside the worker), and the shards simply partition the 21 targets.

GUARANTEES PRESERVED (the brief's absolute rules):
    (1) COMPLETENESS stays a THEOREM: each worker calls exhaust.run_target, which checks
        raw_emitted == sum(closed_form_count) per target. The shard JSON records
        completeness_ok per target; --status FAILS LOUD if any is False.
    (2) a0 RE-DERIVES: unchanged (exhaust.py --ground-truth uses the pinned a0 pool, which
        the flavor extension value-dedups away from). This launcher never touches a0's pool.
    (3) gate/ + scoring UNTOUCHED: workers import exhaust.run_target verbatim.
    (4) FDR stays EXACT: each worker passes n_targets_searched = the FULL target count (21),
        so the look-elsewhere multiplicity is the honest whole-sweep number, not the slice.
    (5) any GATE-PASSING hit is flagged (status != FDR-DEAD) for adversarial re-verification.

Usage:
  python3 exhaust_parallel.py --workers 14 --depth 3      # launch the full sweep, detached
  python3 exhaust_parallel.py --status                    # aggregate the per-target ledger
  python3 exhaust_parallel.py --status --json             # machine-readable aggregate
  python3 exhaust_parallel.py --stop                      # SIGTERM all running workers
  python3 exhaust_parallel.py --worker K --targets a,b,c --depth 3 --n-targets 21
                                                          # (internal) one worker's slice

stdlib only (subprocess fan-out); the workers pull numpy/sympy/mpmath via exhaust.py.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import signal
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

RESULTS = HERE / "results_exhaust"
PIDFILE = RESULTS / "exhaust_pids.json"


# =============================================================================
# THE TARGET SET — the 21 SM targets (the flavor push set)
#   = the canonical run_atomos `--all` precise+dimensionless set (19)
#   + the two TBM mixing angles pmns_sin2_12 (TBM 1/3) and pmns_sin2_23 (TBM 1/2),
#     which the flavor Clebsch germs (1/3, 1/2) directly test. The mixing sector is
#     where the geometry genuinely lives, so the flavor extension MUST aim at them.
# =============================================================================

_EXTRA_FLAVOR_TARGETS = ["pmns_sin2_12", "pmns_sin2_23"]


def sm_target_keys(include_holdout: bool = False) -> List[str]:
    """The SM target keys for the flavor push, in a deterministic order.

    include_holdout=False (default) EXCLUDES the held-back validation targets -- correct for any
    SEARCH, which must never fit them. include_holdout=True returns the FULL historical list and is
    correct for exactly two things:
      * the REPLAY GATE (--replay 6/7), which reproduces committed ground truth. A replay is a
        MACHINERY check, not a search: it neither fits nor selects. Excluding the holdout there
        silently BREAKS the project's main self-verification -- observed 2026-07-27, when the depth-6
        replay went 259 -> 258 hits and reported FAIL purely because koide_Q_lep was no longer swept.
      * RECORD RETENTION (_target_windows), because scoring a survivor's out-of-sample PREDICTION for
        a held-back target requires that values near it were retained in the first place.
    """
    import targets.pdg_constants as pdg
    ds = pdg.load()
    precise = ds.precise_targets(rel_thresh=1e-2)
    dimless = {t.key for t in ds.dimensionless()}
    out = [t.key for t in precise if t.key in dimless]
    # always include the live Koide interlock + the famous ratios (mirror select_targets)
    for k in ("koide_Q_lep", "r_mu_e", "r_p_e", "pmns_sin2_13", "ckm_lambda"):
        if k in ds and k not in out:
            out.append(k)
    # + the two TBM mixing angles the flavor germs directly test
    for k in _EXTRA_FLAVOR_TARGETS:
        if k in ds and k not in out:
            out.append(k)
    # ---- HOLDOUT GUARD (added 2026-07-27, AFTER a leak was found right here) --------------------
    # The hard-coded "always include" loops above BYPASSED the dataset-level holdout: koide_Q_lep was
    # re-added BY NAME even though PDGDataset.dimensionless() had already excluded it, so the running
    # deep-sample campaign was FITTING a target documented as held back. Dataset-level exclusion is
    # necessary but NOT sufficient when callers name targets explicitly. The filter is therefore
    # applied here LAST and unconditionally -- after every hard-coded addition -- so adding another
    # name above cannot reopen the leak.
    return out if include_holdout else [k for k in out if k not in pdg.HOLDOUT_KEYS]


def split_round_robin(keys: List[str], n: int) -> List[List[str]]:
    """Round-robin split so each worker gets a mix of cheap/expensive targets
    (the sharp ratios are cheap; the loose mixing angles can spend longer in the
    gate). Round-robin balances wall time better than contiguous chunks."""
    buckets: List[List[str]] = [[] for _ in range(n)]
    for i, k in enumerate(keys):
        buckets[i % n].append(k)
    return [b for b in buckets if b]  # drop empties if n > len(keys)


# =============================================================================
# THE WORKER — completely exhausts its slice of targets, writes a result shard
# =============================================================================

def run_worker(worker_id: int, target_keys: List[str], depth: int,
               n_targets: int, shard_dir: Path):
    """One worker: COMPLETELY exhaust each target in its slice at `depth` over the
    EXTENDED flavor pool, write the per-target ledger to shard/result.json.

    Imports exhaust.run_target VERBATIM (gate + completeness + FDR unchanged)."""
    import exhaust  # the deterministic exhauster (gate untouched)

    shard_dir.mkdir(parents=True, exist_ok=True)
    logf = open(shard_dir / "run.log", "w")
    results: List[dict] = []

    def log(msg):
        logf.write(msg + "\n")
        logf.flush()

    log(f"=== exhaust worker {worker_id} :: {len(target_keys)} targets :: depth {depth} "
        f":: n_targets(look-elsewhere)={n_targets} ===")
    log(f"targets: {', '.join(target_keys)}")

    for tk in target_keys:
        t0 = time.time()
        log(f"\n----- exhausting {tk} -----")
        try:
            # run_target: full enumerate -> dimensional filter -> exact FDR -> gate -> report.
            # leaf_keys=None, germ_keys=None  => the FULL right-shape pool with the EXTENDED
            # flavor germs (exhaust._default_germs() includes the flavor extension).
            rep = exhaust.run_target(
                tk, depth=depth, tol=None,
                leaf_keys=None, germ_keys=None,
                n_targets_searched=n_targets, verbose=False,
            )
        except Exception as e:  # a target must never crash the whole shard
            import traceback
            log(f"  ERROR on {tk}: {e}\n{traceback.format_exc()}")
            results.append(dict(target=tk, error=str(e), completeness_ok=False))
            _write_shard(shard_dir, worker_id, results, depth, n_targets)
            continue
        dt = time.time() - t0

        # COMPLETENESS THEOREM (the brief's rule 1): raw_emitted == sum(closed_form)
        comp_ok = bool(rep["completeness_ok"])

        # GATE-PASSING hits = anything the gate did NOT mark FDR-DEAD (flag for adversarial check)
        gate_hits = [h for h in rep["hits"] if "FDR-DEAD" not in h["status"]]
        any_hit = len(gate_hits) > 0

        entry = dict(
            target=tk,
            target_value=rep["target_value"],
            target_sigma=rep["target_sigma"],
            target_dimension=rep["target_dimension"],
            depth=rep["depth"],
            tol=rep["tol"],
            n_leaves=rep["n_leaves"],
            n_germs=rep["n_germs"],
            # EXACT SPACE SIZE (the closed-form raw tree count == emitted; completeness theorem)
            space_size=rep["closed_form_total"],
            raw_emitted=rep["raw_emitted"],
            structurally_distinct=rep["structurally_distinct"],
            # DIMENSIONALLY-VALID count (the reason a0 worked: net Label == target)
            n_dim_valid=rep["dim_valid"],
            distinct_reachable_values=rep["distinct_reachable_values"],
            completeness_ok=comp_ok,
            n_hits_in_window=rep["n_hits"],
            n_gate_passing=len(gate_hits),
            verdict=("HIT" if any_hit else "COMPLETE-NULL"),
            # the in-window matches (all of them, capped at 20 by run_target) + the gate-passers
            window_hits=rep["hits"],
            gate_passing_hits=gate_hits,
            wall_sec=round(dt, 2),
        )
        results.append(entry)
        log(f"  space_size={entry['space_size']:,}  n_dim_valid={entry['n_dim_valid']}  "
            f"distinct_values={entry['distinct_reachable_values']}  "
            f"completeness_ok={comp_ok}  in_window={entry['n_hits_in_window']}  "
            f"gate_passing={entry['n_gate_passing']}  -> {entry['verdict']}  ({dt:.1f}s)")
        if any_hit:
            for h in gate_hits:
                log(f"    GATE-PASSING HIT [{h['status']}]: {h['formula']} = {h['value']:.8g}  "
                    f"rel_err={h['rel_error']:.2e}  FDR_bits={h['fdr_bits']:.1f}")
        # checkpoint after EVERY target so --status sees partial progress
        _write_shard(shard_dir, worker_id, results, depth, n_targets)

    log(f"\n=== worker {worker_id} DONE :: {len(results)} targets exhausted ===")
    logf.close()
    _write_shard(shard_dir, worker_id, results, depth, n_targets, done=True)


def _write_shard(shard_dir: Path, worker_id: int, results: List[dict],
                 depth: int, n_targets: int, done: bool = False):
    payload = dict(
        worker=worker_id,
        depth=depth,
        n_targets_lookelsewhere=n_targets,
        done=done,
        n_targets_in_slice=len(results),
        results=results,
        updated=time.strftime("%Y-%m-%d %H:%M:%S"),
    )
    (shard_dir / "result.json").write_text(json.dumps(payload, indent=2, default=str))


# =============================================================================
# THE LAUNCHER — fan the targets across detached workers
# =============================================================================

def launch(workers: int, depth: int):
    RESULTS.mkdir(parents=True, exist_ok=True)
    keys = sm_target_keys()
    n_targets = len(keys)               # the HONEST look-elsewhere multiplicity (whole sweep)
    n_workers = min(workers, len(keys))
    buckets = split_round_robin(keys, n_workers)

    print(f"PROJECT_ATOMOS flavor PUSH — by-target deterministic exhaustion, depth {depth}")
    print(f"  {n_targets} SM targets  x  EXTENDED flavor germ pool  ->  {len(buckets)} workers")
    print(f"  look-elsewhere multiplicity (n_targets) = {n_targets} (honest whole-sweep)\n")

    procs = []
    for k, slice_keys in enumerate(buckets):
        shard = RESULTS / f"shard_{k}"
        shard.mkdir(parents=True, exist_ok=True)
        log = open(shard / "launch.log", "w")
        cmd = [sys.executable, str(HERE / "exhaust_parallel.py"),
               "--worker", str(k),
               "--targets", ",".join(slice_keys),
               "--depth", str(depth),
               "--n-targets", str(n_targets)]
        p = subprocess.Popen(cmd, stdout=log, stderr=subprocess.STDOUT,
                             cwd=str(HERE), start_new_session=True)
        procs.append({"worker": k, "pid": p.pid, "shard": str(shard),
                      "targets": slice_keys})
        print(f"  worker {k:2d}  pid={p.pid}  ({len(slice_keys)} targets: "
              f"{', '.join(slice_keys)})")
    meta = {"started": time.strftime("%Y-%m-%d %H:%M:%S"), "workers": len(buckets),
            "depth": depth, "n_targets": n_targets, "procs": procs}
    PIDFILE.write_text(json.dumps(meta, indent=2))
    print(f"\n{len(buckets)} workers launched (detached). PIDs -> {PIDFILE}")
    print(f"aggregate:  python3 exhaust_parallel.py --status")
    print(f"stop all:   python3 exhaust_parallel.py --stop")


def _alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False


# =============================================================================
# --status — aggregate the per-target ledger across shards
# =============================================================================

def status(as_json: bool = False):
    if not PIDFILE.exists():
        print("no exhaust run found (results_exhaust/exhaust_pids.json missing).")
        return
    meta = json.loads(PIDFILE.read_text())
    procs = meta["procs"]
    alive = sum(1 for p in procs if _alive(p["pid"]))

    per_target: Dict[str, dict] = {}
    completeness_all_ok = True
    workers_done = 0
    workers_running = 0
    for p in procs:
        shard = Path(p["shard"])
        running = _alive(p["pid"])
        rf = shard / "result.json"
        shard_done = False
        if rf.exists():
            try:
                payload = json.loads(rf.read_text())
                shard_done = bool(payload.get("done"))
                for e in payload.get("results", []):
                    per_target[e["target"]] = e
                    if not e.get("completeness_ok", False):
                        completeness_all_ok = False
            except Exception:
                pass
        if running:
            workers_running += 1
        elif shard_done:
            workers_done += 1

    total_hits = sum(e.get("n_gate_passing", 0) for e in per_target.values())
    n_complete = len(per_target)
    n_expected = meta["n_targets"]

    if as_json:
        agg = dict(
            started=meta["started"], depth=meta["depth"],
            n_targets=n_expected, n_exhausted=n_complete,
            workers_total=len(procs), workers_running=workers_running,
            workers_done=workers_done,
            completeness_all_ok=completeness_all_ok,
            total_gate_passing_hits=total_hits,
            per_target=per_target,
        )
        print(json.dumps(agg, indent=2, default=str))
        return

    print("=" * 100)
    print(f"PROJECT_ATOMOS flavor PUSH — AGGREGATE  (started {meta['started']}, depth "
          f"{meta['depth']})")
    print(f"  workers: {len(procs)} total | {workers_running} running | {alive} alive | "
          f"{workers_done} done")
    print(f"  targets exhausted: {n_complete} / {n_expected}")
    print(f"  COMPLETENESS (raw_emitted == closed_form, all targets): "
          f"{'OK (theorem holds)' if completeness_all_ok else 'FAILED — INVESTIGATE'}")
    print(f"  TOTAL GATE-PASSING HITS (flagged for adversarial re-verify): {total_hits}")
    print("-" * 100)
    print(f"{'target':22} {'space_size':>12} {'n_dim_valid':>12} {'distinct':>9} "
          f"{'in_win':>7} {'gate_pass':>10}  verdict")
    print("-" * 100)
    # order by the canonical target order for stable reading
    order = sm_target_keys()
    for tk in order:
        e = per_target.get(tk)
        if e is None:
            print(f"{tk:22} {'(running/pending)':>52}")
            continue
        if e.get("error"):
            print(f"{tk:22}  ERROR: {e['error']}")
            continue
        print(f"{tk:22} {e['space_size']:>12,} {e['n_dim_valid']:>12} "
              f"{e['distinct_reachable_values']:>9} {e['n_hits_in_window']:>7} "
              f"{e['n_gate_passing']:>10}  {e['verdict']}")
    print("-" * 100)
    # detail any gate-passing hit (the only thing worth a human's attention)
    flagged = [(tk, h) for tk in order
               for h in per_target.get(tk, {}).get("gate_passing_hits", [])]
    if flagged:
        print("GATE-PASSING HITS — ADVERSARIAL RE-VERIFICATION REQUIRED (NOT celebrated):")
        for tk, h in flagged:
            print(f"  [{tk}] [{h['status']}] {h['formula']} = {h['value']:.8g}  "
                  f"rel_err={h['rel_error']:.2e}  n_sigma={h['n_sigma']:.2f}  "
                  f"FDR_bits={h['fdr_bits']:.1f}  E_chance={h['e_chance']:.2e}")
    else:
        print("NO GATE-PASSING HITS across all exhausted targets — "
              "COMPLETE NULL (the honest expected result).")
    print("=" * 100)


def stop():
    if not PIDFILE.exists():
        print("no exhaust run found.")
        return
    meta = json.loads(PIDFILE.read_text())
    killed = 0
    for p in meta["procs"]:
        if _alive(p["pid"]):
            try:
                os.kill(p["pid"], signal.SIGTERM)
                killed += 1
            except OSError:
                pass
    print(f"sent SIGTERM to {killed} running workers.")


# =============================================================================
# CLI
# =============================================================================

def main():
    ap = argparse.ArgumentParser(description="By-target parallel launcher for the "
                                             "deterministic exhauster (flavor push).")
    ap.add_argument("--workers", type=int, default=14, help="number of detached workers (default 14).")
    ap.add_argument("--depth", type=int, default=3, help="exhaustion depth (default 3).")
    ap.add_argument("--status", action="store_true", help="aggregate the per-target ledger.")
    ap.add_argument("--json", action="store_true", help="machine-readable aggregate (with --status).")
    ap.add_argument("--stop", action="store_true", help="SIGTERM all running workers.")
    # internal worker mode
    ap.add_argument("--worker", type=int, default=None, help="(internal) worker id.")
    ap.add_argument("--targets", type=str, default=None, help="(internal) comma-separated slice.")
    ap.add_argument("--n-targets", type=int, default=None,
                    help="(internal) whole-sweep look-elsewhere multiplicity.")
    args = ap.parse_args()

    if args.status:
        status(as_json=args.json)
        return
    if args.stop:
        stop()
        return
    if args.worker is not None and args.targets is not None:
        keys = [k for k in args.targets.split(",") if k]
        n_targets = args.n_targets if args.n_targets is not None else len(keys)
        shard = RESULTS / f"shard_{args.worker}"
        run_worker(args.worker, keys, args.depth, n_targets, shard)
        return
    # default: launch the full sweep
    launch(args.workers, args.depth)


if __name__ == "__main__":
    main()
