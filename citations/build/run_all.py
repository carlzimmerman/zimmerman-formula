#!/usr/bin/env python3
"""Rebuild and check the whole citation index:  python3 citations/build/run_all.py [--fresh]

  extract.py      evidence from every scanned script
  resolve_ay.py   author-year citations -> publications (new keys and keys cited from new or edited places, unless --fresh)
  resolve_bib.py  bibliography entries of the LaTeX papers -> publications (only new entries)
  fetch.py        verify every identifier against Crossref / DataCite / arXiv / INSPIRE
  build_index.py  script -> work -> people
  render.py       people, works, BibTeX, unverified list
  legacy.py       reconcile the previous surname index
  docs.py         CITATIONS.md and citations/README.md
  verify.py       the gate (non-zero exit on any failure)
"""
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from common import build_ref  # noqa: E402


def run(script, *args):
    print(f"\n=== {script} {' '.join(args)}", flush=True)
    r = subprocess.run([sys.executable, str(HERE / script), *args])
    if r.returncode != 0:
        sys.exit(f"{script} failed (exit {r.returncode})")


def main():
    fresh = "--fresh" in sys.argv
    os.environ["CITE_REF"] = build_ref()        # every stage reads this one commit, even if HEAD moves meanwhile
    print(f"building from commit {os.environ['CITE_REF'][:10]} (files as committed, not the working tree)", flush=True)
    run("extract.py")
    run("resolve_ay.py", *([] if fresh else ["--missing"]))
    run("resolve_bib.py")
    run("fetch.py")
    run("build_index.py")
    run("render.py")
    run("legacy.py")
    run("docs.py")
    run("verify.py")


if __name__ == "__main__":
    main()
