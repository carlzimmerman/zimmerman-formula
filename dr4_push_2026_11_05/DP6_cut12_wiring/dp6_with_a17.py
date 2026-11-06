#!/usr/bin/env python3
"""DP6 launcher (criteria FROZEN_CRITERIA.md, ee74edfda2): run a frozen CLI script with the filed A17 cut 12 installed.

  python3 -B dr4_push_2026_11_05/DP6_cut12_wiring/dp6_with_a17.py --a17-manifest M.json [--reading A17_primary]
      [--report-json R.json] -- <script.py> <script args ...>
  python3 -B dr4_push_2026_11_05/DP6_cut12_wiring/dp6_with_a17.py --write-per-star OUT.npz --stage-a stage_A.npz

The target (dry_run_driver.py, seed_sweep.py, nss_off_rung.py, ...) runs in this process as __main__ (runpy), with its own
argv, after a17_cut12.install(). It imports the same build_catalog module object, so every frozen_cuts call in it uses the
A17 screen. No frozen file is edited. Network use is whatever the target's own flags allow.
"""
import sys
sys.dont_write_bytecode = True
import argparse, json, runpy
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    tail = []
    if "--" in argv:
        i = argv.index("--")
        argv, tail = argv[:i], argv[i + 1:]
    ap = argparse.ArgumentParser()
    ap.add_argument("--a17-manifest", default=None)
    ap.add_argument("--reading", default="A17_primary")
    ap.add_argument("--report-json", default=None)
    ap.add_argument("--write-per-star", default=None)
    ap.add_argument("--stage-a", default=None)
    a = ap.parse_args(argv)
    import a17_cut12 as A
    if a.write_per_star:
        if not a.stage_a:
            raise SystemExit("--write-per-star needs --stage-a")
        A.write_per_star(a.stage_a, a.write_per_star)
        print(f"per-star file written: {a.write_per_star} (non_single_star = 0; use make_pair_table --declare-neutral non_single_star)")
        return 0
    if not a.a17_manifest or not tail:
        raise SystemExit("usage: --a17-manifest M.json [--reading R] [--report-json J] -- <script.py> <args...>")
    A.install(a.a17_manifest, a.reading)
    script = Path(tail[0]).resolve()
    sys.argv = [str(script)] + tail[1:]
    sys.path.insert(0, str(script.parent))
    code = 0
    try:
        runpy.run_path(str(script), run_name="__main__")
    except SystemExit as e:
        code = e.code if isinstance(e.code, int) else (0 if e.code is None else 1)
    finally:
        if a.report_json:
            rep = A.last_report()
            Path(a.report_json).write_text(json.dumps(dict(reading=a.reading, manifest=str(a.a17_manifest), target=tail,
                                                           report=rep), indent=1, default=str) + "\n")
    return code


if __name__ == "__main__":
    sys.exit(main())
