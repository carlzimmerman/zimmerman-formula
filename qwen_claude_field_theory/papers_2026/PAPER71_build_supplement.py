#!/usr/bin/env python3
"""Build PAPER71's supplement: every committed file under fable52_push/ at HEAD (criteria, amendments, scripts, outputs,
MUTATE outputs, RESULT files, Lean files and their twins), as one zip, with a manifest. Deterministic for a given commit.
Run: python3 PAPER71_build_supplement.py   (from anywhere inside the repository)
kappa = 1/2 FITTED; not theory closed; nothing here says the data favour the framework."""
import hashlib, json, os, subprocess, sys, zipfile
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
ZIP = os.path.join(HERE, "PAPER71_supplement_lanes_and_lean_2026.zip")
MAN = os.path.join(HERE, "PAPER71_supplement_manifest.json")
def git(*a):
    return subprocess.run(["git", "-C", ROOT, *a], capture_output=True, text=True, check=True).stdout.strip()
head = git("rev-parse", "HEAD")
dirty = git("status", "--porcelain", "--", "fable52_push")
if dirty:
    sys.exit("REFUSING: fable52_push has uncommitted changes:\n" + dirty)
subprocess.run(["git", "-C", ROOT, "archive", "--format=zip", "-o", ZIP, head, "fable52_push"], check=True)
z = zipfile.ZipFile(ZIP); names = [n for n in z.namelist() if not n.endswith("/")]
bad = [n for n in names if n.startswith("/") or "/Users/" in n]
if bad: sys.exit(f"REFUSING: absolute paths in the archive: {bad[:3]}")
for n in names:                                  # no personal paths inside text files
    if n.endswith((".md", ".py", ".txt", ".out", ".json", ".lean")):
        t = z.read(n).decode("utf-8", errors="replace")
        if "/Users/" in t:
            sys.exit(f"REFUSING: a home path appears inside {n}")
blob = open(ZIP, "rb").read()
man = dict(paper="PAPER71", git_head=head, count=len(names), zip_bytes=len(blob), sha256=hashlib.sha256(blob).hexdigest(),
           lanes=sorted({n.split("/")[1] for n in names if n.count("/") >= 2}),
           lean=sorted(n for n in names if n.endswith(".lean")), files=sorted(names))
json.dump(man, open(MAN, "w"), indent=1)
print(f"supplement: {man['count']} files, {man['zip_bytes'] / 1e6:.2f} MB, sha256 {man['sha256'][:16]}, git {head[:10]}")
print("lanes:", ", ".join(man["lanes"]))
print("kappa = 1/2 FITTED; not theory closed; nothing here says the data favour the framework.")
