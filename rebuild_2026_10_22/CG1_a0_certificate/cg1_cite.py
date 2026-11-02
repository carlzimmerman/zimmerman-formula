#!/usr/bin/env python3
"""CG1 part D: committed files citing the certificate, read at the frozen-criteria commit. Lists, edits nothing. kappa = 1/2 FITTED; not theory closed."""
import csv, re, subprocess, sys, os
COMMIT = "d9db83969f"; REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TA = r"calibration/calibrate|gate is trustworthy|8/8 rows|project_atomos/gate|forced_kernel_detector|CERTIFIED [(]B|a0_kernel|GATE_SPEC|attack5_fdr|gate/fdr"
TB = r"(a0|a₀|a_0)[^|]{0,60}CERTIFIED|CERTIFIED[^|]{0,60}(a0|a₀|a_0)"
TC = r"forced.?kernel"
def grep(p, ci=False):
    r = subprocess.run(["git", "grep", "-c", "-I", "-E"] + (["-i"] if ci else []) + [p, COMMIT, "--", ".", ":!.claude", ":!rebuild_2026_10_22/CG1_a0_certificate", ":!rebuild_2026_10_22/BK1_forced_kernel_scales"], capture_output=True, text=True, cwd=REPO); d = {}
    for l in r.stdout.splitlines():
        _, f, n = l.split(":", 2); d[f] = int(n)
    return d
a, b, c = grep(TA), grep(TB), grep(TC, True)
def kind(f):
    if re.search(r"(PAPER|paper|papers/|submission|zenodo|\.tex$|^book/|pdf/)", f): return "paper"
    if f.endswith((".py", ".lean", ".sh")): return "code"
    if f.endswith((".json", ".jsonl", ".csv", ".tsv", ".out")): return "data"
    return "note"
rows = []
for f in sorted(set(a) | set(b) | set(c)):
    rows.append((f, "A names gate or calibration" if f in a else "B a0 + CERTIFIED" if f in b else "C forced-kernel wording", kind(f), a.get(f, 0), b.get(f, 0), c.get(f, 0)))
with open("CITATIONS.tsv", "w", newline="") as h:
    w = csv.writer(h, delimiter="\t", lineterminator="\n"); w.writerow(["file", "tier", "kind", "n_A", "n_B", "n_C"]); w.writerows(rows)
from collections import Counter
C_ = Counter((r[1], r[2]) for r in rows); out = [f"{k}: {v}" for k, v in sorted(C_.items())] + [f"total {len(rows)}"] + ["papers:"] + ["\t".join(map(str, r)) for r in rows if r[2] == "paper"]
open("cg1_cite.out", "w").write("\n".join(out) + "\n"); print("\n".join(out))
