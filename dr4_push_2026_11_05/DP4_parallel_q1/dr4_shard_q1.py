#!/usr/bin/env python3
"""DP4: split the cut-13 Q1 cone fetch into K sky-contiguous shards (criteria: FROZEN_CRITERIA.md, 43d86506d1).

NEW file. OFFLINE: it writes shard CSVs, a --neighbours-manifest JSON and prints the per-shard q1_cones_dr4.py commands;
it never opens a connection. Each printed command is the frozen query form (same --spec) and needs the owner's go on the
day, like every Q1 query. The driver combines the shard outputs natively (repeatable --neighbours / --neighbour-pairs,
or --neighbours-manifest).

  python3 dr4_shard_q1.py --pairs-csv <candidates.csv> --k 4 --out-dir <data dir> --spec dr4_all_source \
      --stage-a <dr4_extract>/stage_A.npz --cap-accepted-mb 2540 --cap-received-mb 3100 --max-queries 58900 [--plan]
"""
import sys
sys.dont_write_bytecode = True
import argparse, csv, json
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
READY = REPO / "prep_2026" / "gaia_dr4_prep" / "dr4_ready_1"


def read_pairs(path):
    rows = list(csv.DictReader(open(path)))
    return (np.array([int(r["source_id1"]) for r in rows], np.int64),
            np.array([int(r["source_id2"]) for r in rows], np.int64))


def shard_index(s1, k):
    """shard of each pair: contiguous blocks of the pairs sorted by source_id1 (nested HEALPix order = sky order)."""
    order = np.argsort(s1, kind="stable")
    sh = np.empty(len(s1), np.int64)
    for j, blk in enumerate(np.array_split(order, k)):
        sh[blk] = j
    return sh


def write_pairs(path, s1, s2):
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["source_id1", "source_id2"])
        w.writerows(zip(s1.tolist(), s2.tolist()))


def split(pairs_csv, k, out_dir, tag="q1"):
    s1, s2 = read_pairs(pairs_csv)
    sh = shard_index(s1, k)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    entries = []
    for j in range(k):
        m = sh == j
        p = out_dir / f"{tag}_shard{j:02d}_of{k:02d}_pairs.csv"
        write_pairs(p, s1[m], s2[m])
        entries.append(dict(table=f"{tag} shard {j} of {k}", neighbours=str(out_dir / f"{tag}_shard{j:02d}_of{k:02d}_neighbours.fits"),
                            pairs=str(p), include=True, n_pairs=int(m.sum())))
    man = out_dir / f"{tag}_shards_of{k:02d}_neighbours_manifest.json"
    man.write_text(json.dumps(entries, indent=1) + "\n")
    return entries, man


def commands(entries, spec, stage_a, out_dir, caps, tag="q1"):
    k = len(entries)
    cmds = []
    for j, e in enumerate(entries):
        c = (f"caffeinate -i python3 -B {READY.relative_to(REPO)}/q1_cones_dr4.py --spec {spec} --stage-a {stage_a} "
             f"--pairs-csv {e['pairs']} --tag {tag}_shard{j:02d}_of{k:02d} --out-dir {out_dir} "
             f"--manifest {out_dir}/manifest_{tag}_shard{j:02d}_of{k:02d}.json "
             f"--cap-accepted-mb {caps['accepted_mb'] / k:.1f} --cap-received-mb {caps['received_mb'] / k:.1f} "
             f"--max-queries {int(np.ceil(caps['max_queries'] / k))} --owner-go-recorded \"<the owner's go, verbatim>\"")
        cmds.append(c)
    return cmds


def plan_units(stage_a, pairs_csvs, spec_name):
    sys.path.insert(0, str(READY))
    import dr4_archive_fetch as F
    spec, _ = F.load_spec(spec_name)
    return [len(F.plan_pairs(stage_a, p, spec)["units"]) for p in pairs_csvs]


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--pairs-csv", required=True)
    ap.add_argument("--k", type=int, required=True)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--spec", default="dr4_all_source")
    ap.add_argument("--stage-a", required=True)
    ap.add_argument("--tag", default="q1")
    ap.add_argument("--cap-accepted-mb", type=float, required=True)
    ap.add_argument("--cap-received-mb", type=float, required=True)
    ap.add_argument("--max-queries", type=int, required=True)
    ap.add_argument("--plan", action="store_true", help="count planned units per shard and unsharded (offline)")
    a = ap.parse_args(argv)
    if a.k < 1:
        raise SystemExit("--k must be >= 1")
    entries, man = split(a.pairs_csv, a.k, a.out_dir, a.tag)
    print(f"{a.k} shards, {sum(e['n_pairs'] for e in entries):,d} pairs; driver manifest: {man}")
    caps = dict(accepted_mb=a.cap_accepted_mb, received_mb=a.cap_received_mb, max_queries=a.max_queries)
    for c in commands(entries, a.spec, a.stage_a, a.out_dir, caps, a.tag):
        print(c)
    if a.plan:
        u_all = plan_units(a.stage_a, [a.pairs_csv], a.spec)[0]
        u_sh = plan_units(a.stage_a, [e["pairs"] for e in entries], a.spec)
        print(f"planned units: unsharded {u_all:,d}; shards {u_sh} sum {sum(u_sh):,d} (ratio {sum(u_sh) / max(u_all, 1):.3f}); "
              f"wall time scales as max shard {max(u_sh):,d} / {u_all:,d} = {max(u_sh) / max(u_all, 1):.3f} of serial")
    print(f"driver: --cut13 cones-literal --neighbours-manifest {man}   (each shard's FITS must exist; missing cones raise ConeCoverageError)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
