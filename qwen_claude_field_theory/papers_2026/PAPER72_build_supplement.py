#!/usr/bin/env python3
"""Build PAPER72's supplement: every committed file of the lanes the paper cites (KO2, RB1, RB2, CO1, PD1, PD2, the owner's decision and the re-run record
under closure_2026_11_09/; HE1, ONE1, TPA1, FB1, KO3F under fable52_push/), as one zip, with a manifest.
The shared checkout has diverged from origin (PD1 and PD2 are committed on origin only), so each lane path is taken from whichever
of HEAD and origin/main last committed to it; the manifest records the ref and commit for each. Untracked files are not included
and are listed (unless the same path is committed on the chosen ref); a tracked file modified in the working tree stops the build. Deterministic for given commits (fixed entry dates).
Run: python3 PAPER72_build_supplement.py   (from anywhere inside the repository)
kappa = 1/2 FITTED; not theory closed; nothing here says the data favour the framework."""
import hashlib, io, json, os, subprocess, sys, tarfile, zipfile
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
ZIP = os.path.join(HERE, "PAPER72_supplement_lanes_2026.zip")
MAN = os.path.join(HERE, "PAPER72_supplement_manifest.json")
PATHS = [
 "closure_2026_11_09/KO2_kids_own_field_by_type",
 "closure_2026_11_09/RB1_form_b_hot_systems",
 "closure_2026_11_09/RB2_form_b_hosted_rows",
 "closure_2026_11_09/PD1_phantom_is_dust",
 "closure_2026_11_09/PD2_sheet_captured_phantom_dust",
 "closure_2026_11_09/CO1_form_b_cosmology_computed",
 "closure_2026_11_09/OWNER_DECISION_2026-11-09_FINAL_FORM_B.md",
 "closure_2026_11_09/RERUNS_2026-11-09.md",
 "fable52_push/HE1_held_out_envelope",
 "fable52_push/ONE1_counted_once",
 "fable52_push/TPA1_two_phase_action",
 "fable52_push/FB1_form_b_from_the_action",
 "fable52_push/KO3F_spec_veto_power_forecast",
]
REFS = ("HEAD", "origin/main")
def git(*a, check=True):
    return subprocess.run(["git", "-C", ROOT, *a], capture_output=True, text=True, check=check).stdout.strip()
def gitb(*a):
    return subprocess.run(["git", "-C", ROOT, *a], capture_output=True, check=True).stdout
dirty = [l for l in git("status", "--porcelain", "--", *PATHS).splitlines() if not l.startswith("??")]
if dirty:
    sys.exit("REFUSING: tracked lane files have uncommitted changes:\n" + "\n".join(dirty))
untracked = sorted(l[3:] for l in git("status", "--porcelain", "--untracked-files=all", "--", *PATHS).splitlines() if l.startswith("??"))
chosen = {}
for p in PATHS:
    best = None
    for ref in REFS:
        c = git("log", "-1", "--format=%ct %H", ref, "--", p, check=False)
        if c and git("ls-tree", "-r", "--name-only", ref, "--", p):
            t, h = c.split()
            if best is None or int(t) > best[0]: best = (int(t), ref, h)
    if best is None:
        sys.exit(f"REFUSING: {p} is committed on neither HEAD nor origin/main")
    chosen[p] = dict(ref=best[1], ref_commit=git("rev-parse", best[1]), last_commit=best[2])
files = {}
for p, c in chosen.items():
    tf = tarfile.open(fileobj=io.BytesIO(gitb("archive", "--format=tar", c["ref"], "--", p)))
    for m in tf.getmembers():
        if m.isfile(): files[m.name] = tf.extractfile(m).read()
names = sorted(files)
bad = [n for n in names if n.startswith("/") or "/Users/" in n]
if bad: sys.exit(f"REFUSING: absolute paths in the archive: {bad[:3]}")
for n in names:                                  # no personal paths inside text files
    if n.endswith((".md", ".py", ".txt", ".out", ".json", ".lean", ".sh")) and b"/Users/" in files[n]:
        sys.exit(f"REFUSING: a home path appears inside {n}")
with zipfile.ZipFile(ZIP, "w", zipfile.ZIP_DEFLATED) as z:
    for n in names:
        zi = zipfile.ZipInfo(n, date_time=(2026, 11, 9, 0, 0, 0)); zi.compress_type = zipfile.ZIP_DEFLATED
        zi.external_attr = 0o644 << 16
        z.writestr(zi, files[n])
untracked = [u for u in untracked if u not in files]   # present in the archive from origin/main
blob = open(ZIP, "rb").read()
lanes = sorted({n.split("/")[1] for n in names if n.count("/") >= 2})
man = dict(paper="PAPER72", git_head=git("rev-parse", "HEAD"), origin_main=git("rev-parse", "origin/main"), sources=chosen,
           count=len(names), zip_bytes=len(blob), sha256=hashlib.sha256(blob).hexdigest(), lanes=lanes,
           lean=sorted(n for n in names if n.endswith(".lean")), untracked_not_included=untracked, files=names)
json.dump(man, open(MAN, "w"), indent=1)
print(f"supplement: {man['count']} files, {man['zip_bytes'] / 1e6:.2f} MB, sha256 {man['sha256'][:16]}, "
      f"HEAD {man['git_head'][:10]}, origin {man['origin_main'][:10]}")
for p, c in chosen.items(): print(f"  {p}: {c['ref']} (last commit {c['last_commit'][:10]})")
print("lanes:", ", ".join(lanes))
if untracked: print(f"untracked, not included ({len(untracked)}):", ", ".join(untracked))
print("kappa = 1/2 FITTED; not theory closed; nothing here says the data favour the framework.")
