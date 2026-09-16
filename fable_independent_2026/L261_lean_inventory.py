#!/usr/bin/env python3
"""L261 (part C) -- THE LEAN INVENTORY OF 2026-09-13..16, RECOMPILED (L258 part D re-run on the enlarged file set).  Every Lean certificate in the agent tracks and this
track's Mondlean.lean is compiled with `lake env lean` against the repository's Mathlib, with
`#print axioms` appended for every theorem and lemma, and the result recorded per file: exit code, the
theorems whose axioms are not the standard three (propext, Classical.choice, Quot.sound), error lines,
and any `sorry`.  Writes L261_lean_inventory.json next to this script.  Third parties re-run it with
    python3 fable_independent_2026/L261_lean_inventory.py
(the Mathlib build under fable_independent_2026/lean_2026/.lake is required; ~2 minutes)."""
import os, re, subprocess, json, sys, time, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
PROJ = os.path.join(HERE, "lean_2026")
DIRS = ["glm53_push/lean", "qwen38_push/lean", "hy4_push/lean", "grok_push/lean", "deepseek_push/lean", "deepseek_moa/lean", "kimik3_push", "kimik3_push/lean", "hermes_push/lean", "lean",
        "gemini38_flash_push"]
files = []
for d in DIRS:
    p = os.path.join(REPO, d)
    if os.path.isdir(p):
        files += [os.path.join(p, f) for f in sorted(os.listdir(p)) if f.endswith(".lean")]
files.append(os.path.join(PROJ, "Mondlean.lean"))
STD = ("propext", "Classical.choice", "Quot.sound")
summary, tmpdir = {}, tempfile.mkdtemp(prefix="l261lean_")
for f in files:
    src = open(f).read()
    names, stack = [], []
    for line in src.splitlines():
        m = re.match(r"^\s*namespace\s+([\w.']+)", line)
        if m: stack.append(m.group(1)); continue
        m = re.match(r"^\s*end\s+([\w.']+)\s*$", line)
        if m and stack and stack[-1] == m.group(1): stack.pop(); continue
        m = re.match(r"^(?:private\s+|protected\s+|noncomputable\s+)*(theorem|lemma)\s+([\w.']+)", line)
        if m: names.append(".".join(stack + [m.group(2)]))
    tmp = os.path.join(tmpdir, "chk_" + os.path.basename(f))
    with open(tmp, "w") as g:
        g.write(src + "\n\n" + "\n".join(f"#print axioms {n}" for n in names) + "\n")
    t0 = time.time()
    try:
        r = subprocess.run(["lake", "env", "lean", tmp], cwd=PROJ, capture_output=True, text=True, timeout=1800)
        code, out = r.returncode, r.stdout + r.stderr
    except subprocess.TimeoutExpired:
        code, out = -999, "TIMEOUT"
    axioms = {m.group(1): [a.strip() for a in m.group(2).split(",") if a.strip()]
              for m in re.finditer(r"'([\w.']+)' depends on axioms: \[([^\]]*)\]", out)}
    for m in re.finditer(r"'([\w.']+)' does not depend on any axioms", out): axioms[m.group(1)] = []
    nonstd = {k: v for k, v in axioms.items() if any(a not in STD for a in v)}
    errors = [l.replace(tmp, os.path.basename(f)) for l in out.splitlines() if ": error" in l and "#print" not in l]
    rel = os.path.relpath(f, REPO)
    summary[rel] = dict(exit=code, seconds=round(time.time() - t0, 1), theorems=len(names),
                        axiom_prints=len(axioms), theorems_on_nonstandard_axioms=nonstd,
                        n_errors=len(errors), errors=errors[:12],
                        src_sorry=len(re.findall(r"\bsorry\b", re.sub(r"/-.*?-/|--[^\n]*", "", src, flags=re.S))),
                        src_axiom_decls=len(re.findall(r"^\s*axiom\b", src, re.M)))
    print(f"{rel}: exit={code} theorems={len(names)} errors={len(errors)} nonstandard={len(nonstd)} sorry_in_source={summary[rel]['src_sorry']} ({summary[rel]['seconds']}s)", flush=True)
tot = dict(files=len(summary), theorems=sum(v["theorems"] for v in summary.values()),
           files_exit0=sum(1 for v in summary.values() if v["exit"] == 0),
           theorems_on_nonstandard_axioms=sum(len(v["theorems_on_nonstandard_axioms"]) for v in summary.values()),
           files_with_errors=[k for k, v in summary.items() if v["n_errors"]])
print("TOTAL:", json.dumps(tot))
json.dump(dict(total=tot, files=summary), open(os.path.join(HERE, "L261_lean_inventory.json"), "w"), indent=1)
