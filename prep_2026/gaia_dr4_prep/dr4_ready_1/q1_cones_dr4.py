#!/usr/bin/env python3
"""DR4-READY-1, items 1 and 4 of DR4_Q1_TOOLING_DESIGN_FROZEN.md (6742d206d): the release-day Q1 cone fetch for ANY list of pairs and any of the specs in dr4_archive_fetch.SPECS (NEW file; networked; needs --owner-go-recorded and explicit caps).
It is a thin command line over dr4_archive_fetch.run_fetch: plan (offline) -> schema probe -> resumable fetch -> exact cones -> local completeness -> output FITS + manifest -> optional spot check.  EVERY query form needs the owner's go on the day; the DR4 names
are the DRAFT data model's ('confirm on release day'): a correction goes into a --spec-json file (recorded in the manifest with its sha256), not into code.
Examples (release day; each needs the owner's go in the calculation chat, with filename, source, size, caps and location):
  python3 dr4_q1_estimate.py --n-pairs 49000                                  # the owner's pre-brief (offline)
  python3 q1_cones_dr4.py --spec dr4_all_source --stage-a <dr4_extract>/stage_A.npz --pairs-csv <candidates.csv> --tag dr4_all --out-dir <data dir> --manifest manifest_q1_dr4_all.json --plan-only
  caffeinate -i python3 q1_cones_dr4.py --spec dr4_all_source ... --cap-accepted-mb N --cap-received-mb M --max-queries Q --owner-go-recorded "<text>"      (resumable)
  python3 q1_cones_dr4.py --spec dr4_gaia_source_environment ...               # the optional Amendment 16(b) tables, one file each; the driver's --neighbours-manifest decides whether they are used
  python3 q1_cones_dr4.py --print-count-queries                               # the ADQL text of the Amendment 16(b) counts (never run by this tool)"""
import sys
sys.dont_write_bytecode = True
import argparse, json, subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import dr4_archive_fetch as F


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", choices=sorted(F.SPECS))
    ap.add_argument("--spec-json", default=None, help="a JSON file replacing keys of the spec (a release-day correction of a name); recorded with its sha256")
    ap.add_argument("--stage-a", help="stage_A.npz of the release's extract (source_id, ra, dec, parallax)")
    ap.add_argument("--pairs-csv", help="source_id1, source_id2 per row; the row index is the pair_id of the output")
    ap.add_argument("--tag")
    ap.add_argument("--out-dir")
    ap.add_argument("--manifest")
    ap.add_argument("--cap-accepted-mb", type=float, default=0)
    ap.add_argument("--cap-received-mb", type=float, default=0)
    ap.add_argument("--max-queries", type=int, default=0)
    ap.add_argument("--owner-go-recorded", type=str, default="")
    ap.add_argument("--plan-only", action="store_true")
    ap.add_argument("--spot-check", type=int, default=0, help="N random cones compared against position queries (a different query form: needs its own clearance)")
    ap.add_argument("--max-pairs", type=int, default=None, help="for offline tests only")
    ap.add_argument("--print-count-queries", action="store_true")
    a = ap.parse_args(argv)
    if a.print_count_queries:
        for k, q in F.release_day_count_queries("dr4").items():
            print(f"-- {k}\n{q};\n")
        return 0
    for k in ("spec", "stage_a", "pairs_csv", "tag", "out_dir", "manifest"):
        if getattr(a, k) is None:
            raise SystemExit(f"--{k.replace('_', '-')} is required")
    try:
        commit = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, cwd=str(HERE)).stdout.strip() or None
    except Exception:
        commit = None
    caps = dict(accepted_bytes=a.cap_accepted_mb * 1e6, received_bytes=a.cap_received_mb * 1e6, max_queries=a.max_queries)
    F.run_fetch(a.spec, a.stage_a, a.pairs_csv, a.out_dir, a.manifest, a.tag, caps=caps, go_text=a.owner_go_recorded, spec_json=a.spec_json, plan_only=a.plan_only, spot_n=a.spot_check, max_pairs=a.max_pairs, git_commit=commit)
    return 0


if __name__ == "__main__":
    sys.exit(main())
