#!/usr/bin/env python3
"""FINAL-13 delta: re-hash the pre-existing lean_2026 sources and diff against the T0 manifest.

Pre-existing = the 354 .lean files present in the tree at T0 (all git-tracked at HEAD),
excluding the .lake build/package tree.

Reports:
  - new names        (present now, not at T0)
  - deleted/renamed  (at T0, gone now)
  - overlap          (present both)
  - byte-identical?  every overlap file's sha256 unchanged
  - changed          overlap files whose sha256 moved
"""

import hashlib
import os
import sys

ROOT = "/Users/carlzimmerman/new_physics/zimmerman-formula/fable_independent_2026/lean_2026"
LANE = "/Users/carlzimmerman/new_physics/zimmerman-formula/hy4_preview_push/FINAL-13_LEAN_AUDIT"


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def tree():
    out = {}
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d != ".lake"]
        for fn in filenames:
            if fn.endswith(".lean"):
                full = os.path.join(dirpath, fn)
                rel = os.path.relpath(full, ROOT)
                out[rel] = sha256(full)
    return out


def load_manifest(path):
    d = {}
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.rstrip("\n")
            if not line:
                continue
            h, _, name = line.partition("  ")
            d[name.lstrip("./").lstrip("/")] = h
    return d


def main():
    base = load_manifest(os.path.join(LANE, "manifest_baseline.sha256"))
    now = tree()

    new_names = sorted(set(now) - set(base))
    gone = sorted(set(base) - set(now))
    overlap = sorted(set(base) & set(now))
    changed = sorted(n for n in overlap if base[n] != now[n])
    same = [n for n in overlap if base[n] == now[n]]

    # provenance for new names: which lane / audit lane produced them
    provenance = {
        "FINAL9to12/FINAL9_StaticHalo.lean": "FINAL-13 audit copy of lane FINAL-9 (lean_static)",
        "FINAL9to12/Final10Stress.lean": "FINAL-13 audit copy of lane FINAL-10 (lean_stress)",
        "FINAL9to12/Final11Budget.lean": "FINAL-13 audit copy of lane FINAL-11 (lean_budget)",
        "FINAL9to12/FINAL12_background_conservation.lean": "FINAL-13 audit copy of lane FINAL-12 (lean_background)",
    }

    print("PRE-EXISTING (T0) : %d" % len(base))
    print("NOW               : %d" % len(now))
    print("new names         : %d" % len(new_names))
    print("overlap           : %d" % len(overlap))
    print("deleted/renamed   : %d" % len(gone))
    print("byte-identical    : %d / %d  -> %s"
          % (len(same), len(overlap), "YES" if not changed else "NO"))
    if changed:
        print("CHANGED FILES:")
        for n in changed:
            print("   %s\n      T0 %s\n      T1 %s" % (n, base[n][:16], now[n][:16]))
    if gone:
        print("DELETED/RENAMED:")
        for n in gone:
            print("   " + n)
    print("NEW NAMES:")
    for n in new_names:
        print("   %-52s %s" % (n, provenance.get(n, "<unattributed - sibling lane scratch>")))

    with open(os.path.join(LANE, "manifest_now.sha256"), "w", encoding="utf-8") as fh:
        for n in sorted(now):
            fh.write("%s  ./%s\n" % (now[n], n))
    return 0 if not changed and not gone else 2


if __name__ == "__main__":
    sys.exit(main())
