#!/usr/bin/env python3
"""Build PAPER70's supplement archive: every Lean source and build output, the closure tables, the frozen
criteria / README / RESULT files of the closure lanes, the prediction file, the PAPER70 TeX and audit.
Writes <papers_2026>/PAPER70_supplement_lean_and_record_2026.zip and a SHA256 manifest next to it.
Read-only on the repository; the zip is not committed (the manifest is). Run from anywhere."""
import hashlib, io, os, sys, zipfile, glob, subprocess, json
ROOT = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], cwd=os.path.dirname(os.path.abspath(__file__)), text=True).strip()
P = os.path.join(ROOT, "qwen_claude_field_theory", "papers_2026")
OUT = os.path.join(P, "PAPER70_supplement_lean_and_record_2026.zip")
MAN = os.path.join(P, "PAPER70_supplement_manifest.json")
LEAN = os.path.join(ROOT, "fable_independent_2026", "lean_2026")

def rel(p): return os.path.relpath(p, ROOT)
files = []
files += glob.glob(os.path.join(LEAN, "*.lean")) + glob.glob(os.path.join(LEAN, "*.out"))
for name in ("lakefile.lean", "lakefile.toml", "lake-manifest.json", "lean-toolchain", "README.md"):
    q = os.path.join(LEAN, name)
    if os.path.exists(q): files.append(q)
for d in ("closure_2026_11_05", "closure_2026_11_06", "closure_2026_11_07", "closure_2026_11_08", "closure_2026_11_09", "action_search_2026_11_05"):
    base = os.path.join(ROOT, d)
    files += glob.glob(os.path.join(base, "*.md")) + glob.glob(os.path.join(base, "*.json"))
    for pat in ("*/FROZEN_CRITERIA.md", "*/CRITERIA.md", "*/README.md", "*/RESULT.md", "*/REDUCTION.md", "*/ANALYSIS.md", "*/*.lean",
                "*/iter_*/FROZEN_CRITERIA.md", "*/iter_*/README.md", "*/iter_*/RESULT.md"):
        files += glob.glob(os.path.join(base, pat))
files += [os.path.join(ROOT, "closure_2026_11_07", "predictions_check.py"),
          os.path.join(P, "PAPER70_field_equations_closure_2026.tex"), os.path.join(P, "PAPER70_audit.py"),
          os.path.join(ROOT, "covariant_push_2026_10_22", "V3_FULL_PICTURE.md")]
files = sorted({f for f in files if os.path.isfile(f)})
head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
manifest = {"git_head": head, "count": len(files), "files": {}}
with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
    for f in files:
        data = open(f, "rb").read()
        z.writestr(rel(f), data)
        manifest["files"][rel(f)] = hashlib.sha256(data).hexdigest()
    z.writestr("MANIFEST.json", json.dumps(manifest, indent=1))
manifest["zip_sha256"] = hashlib.sha256(open(OUT, "rb").read()).hexdigest()
manifest["zip_bytes"] = os.path.getsize(OUT)
json.dump(manifest, open(MAN, "w"), indent=1)
print(f"{OUT}: {len(files)} files, {manifest['zip_bytes']/1e6:.1f} MB, sha256 {manifest['zip_sha256'][:16]}..., git {head[:10]}")
