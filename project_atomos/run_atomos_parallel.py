#!/usr/bin/env python3
"""
run_atomos_parallel.py — fan the autoresearch search across all cores.

run_atomos.py is a single-process loop (one core). This launcher spawns N independent worker
processes (default: cpu_count - 2, leaving headroom for the OS), each running the FULL search
(`run_atomos.py --all`) with a DIFFERENT RNG seed and its OWN results shard. Different seeds =
different stochastic search trajectories, so the workers cover different regions of the space in
parallel — embarrassingly parallel, no shared state, no lock contention. Each worker checkpoints
independently (the Bloom tried-set + best-bits per shard), so any worker can be killed/resumed
without touching the others.

Usage:
  python3 run_atomos_parallel.py                      # cpu-2 workers, 2h each, all targets
  python3 run_atomos_parallel.py --workers 14 --hours 2
  python3 run_atomos_parallel.py --status             # aggregate clues across all shards
  python3 run_atomos_parallel.py --stop               # kill all running workers

Monitor:  tail -f results/shard_0/progress.log     |     read clues: results/shard_*/CLUES.md
"""
from __future__ import annotations
import argparse, json, os, signal, subprocess, sys, time
from pathlib import Path

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"
PIDFILE = RESULTS / "parallel_pids.json"


def launch(workers: int, hours: float, checkpoint: int, seed_base: int,
           geometric: bool = True, resume: bool = False):
    RESULTS.mkdir(parents=True, exist_ok=True)
    procs = []
    for k in range(workers):
        shard = RESULTS / f"shard_{k}"
        shard.mkdir(parents=True, exist_ok=True)
        log = open(shard / "run.log", "a" if resume else "w")
        cmd = [sys.executable, str(HERE / "run_atomos.py"),
               "--all", "--hours", str(hours), "--seed", str(seed_base + k),
               "--checkpoint", str(checkpoint), "--results-dir", str(shard)]
        # GEOMETRIC MODE default ON: restrict each worker's dimensionless-factor pool to the
        # forced-geometric primitives (the a0 discipline). --no-geometric reverts to the full pool.
        if geometric:
            cmd.append("--geometric")
        # RESUME: continue this shard from its checkpoint (bloom tried-set + best-bits + the climb
        # state: max_depth, active_group, escalation) so a relaunch EXTENDS the run instead of restarting.
        if resume:
            cmd.append("--resume")
        # detached so the workers outlive this launcher (start_new_session = own process group)
        p = subprocess.Popen(cmd, stdout=log, stderr=subprocess.STDOUT,
                             cwd=str(HERE), start_new_session=True)
        procs.append({"worker": k, "pid": p.pid, "seed": seed_base + k, "shard": str(shard)})
        print(f"  worker {k:2d}  pid={p.pid}  seed={seed_base + k}  -> {shard.name}/")
    meta = {"started": time.strftime("%Y-%m-%d %H:%M:%S"), "workers": workers,
            "hours": hours, "checkpoint": checkpoint, "procs": procs}
    PIDFILE.write_text(json.dumps(meta, indent=2))
    print(f"\n{workers} workers launched, {hours}h each. PIDs -> {PIDFILE}")
    print(f"monitor:  tail -f {RESULTS}/shard_0/progress.log")
    print(f"aggregate clues:  python3 run_atomos_parallel.py --status")
    print(f"stop all:  python3 run_atomos_parallel.py --stop")


def _alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False


def status():
    if not PIDFILE.exists():
        print("no parallel run found (results/parallel_pids.json missing).")
        return
    meta = json.loads(PIDFILE.read_text())
    procs = meta["procs"]
    alive = sum(1 for p in procs if _alive(p["pid"]))
    print(f"started {meta['started']} | {len(procs)} workers | {alive} still running\n")
    total_evals = 0
    leads = []
    best = []  # (bits, target, formula, shard)
    for p in procs:
        shard = Path(p["shard"])
        stats = shard / "stats.json"
        kj = shard / "knowledge.json"
        run = "alive" if _alive(p["pid"]) else "done"
        n_eval = 0
        if kj.exists():
            try:
                n_eval = json.loads(kj.read_text()).get("n_eval", 0)
            except Exception:
                pass
        total_evals += n_eval
        # collect certified leads (the only thing that matters)
        lf = shard / "leads.jsonl"
        if lf.exists():
            for line in lf.read_text().splitlines():
                if line.strip():
                    leads.append((p["worker"], line))
        # top near-miss per shard (best bits)
        if stats.exists():
            try:
                st = json.loads(stats.read_text())
                for tgt, v in st.items():
                    best.append((v.get("best_bits", 0.0), tgt, v.get("wall", "?"), p["worker"]))
            except Exception:
                pass
        print(f"  worker {p['worker']:2d} [{run:>5}]  n_eval={n_eval:,}")
    print(f"\nTOTAL gate-evals across all shards: {total_evals:,}")
    print(f"CERTIFIED LEADS: {len(leads)}")
    for w, line in leads[:20]:
        print(f"  [w{w}] {line[:200]}")
    best.sort(reverse=True)
    print("\nTOP near-misses (best FDR-bits, by target):")
    seen = set()
    for bits, tgt, wall, w in best:
        if tgt in seen:
            continue
        seen.add(tgt)
        print(f"  {tgt:16s} best_bits={bits:6.1f}  wall={wall}  [w{w}]")
        if len(seen) >= 15:
            break


def stop():
    if not PIDFILE.exists():
        print("no parallel run found.")
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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=max(1, (os.cpu_count() or 4) - 2))
    ap.add_argument("--hours", type=float, default=2.0)
    ap.add_argument("--checkpoint", type=int, default=200)
    ap.add_argument("--seed-base", type=int, default=1000)
    ap.add_argument("--status", action="store_true", help="aggregate clues across shards")
    ap.add_argument("--stop", action="store_true", help="kill all running workers")
    # GEOMETRIC MODE default ON: every worker appends --geometric to its run_atomos.py command
    # (restrict the dimensionless-factor pool to forced-geometric primitives). --no-geometric reverts.
    ap.add_argument("--geometric", dest="geometric", action="store_true", default=True,
                    help="restrict each worker's dimensionless-factor pool to forced-geometric "
                         "primitives (DEFAULT ON)")
    ap.add_argument("--no-geometric", dest="geometric", action="store_false",
                    help="revert each worker to the full arbitrary-integer/transcendental germ pool")
    ap.add_argument("--resume", action="store_true",
                    help="continue each shard from its checkpoint (EXTEND a run instead of restarting)")
    args = ap.parse_args()
    if args.status:
        status()
    elif args.stop:
        stop()
    else:
        mode = f"geometric_mode={'ON' if args.geometric else 'OFF'}, {'RESUME' if args.resume else 'fresh'}"
        print(f"launching {args.workers} workers x {args.hours}h on {os.cpu_count()} logical cores "
              f"({mode})...\n")
        launch(args.workers, args.hours, args.checkpoint, args.seed_base,
               geometric=args.geometric, resume=args.resume)


if __name__ == "__main__":
    main()
