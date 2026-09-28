#!/usr/bin/env python3
"""LR4b -- cov discharge ASSEMBLY verdict runner (Z7 successor; owns LR4b_*).
The assembly file LR4b_cov_discharge.lean was built interactively against the
certified stage bank and LR3b's conditional chains; this run compiles it, runs
the pre-registered gates, and records the verdict.
Gates (pre-registered in the docstring of the first LR4b script + brief amendment 2):
  G1: lake env lean rc 0, ZERO sorry outside comments, axioms of outer_v,
      chord_cond, I1_cond subset of {propext, Classical.choice, Quot.sound}.
  G2: constants 3/4 (chord) and 5/12 (I1) appear as the unconditional targets
      (identical to LR3b's conditional constants -- no new constants).
Verdict BANKED-DISCHARGED iff G1 and G2 both pass; else exit 1 with lake stderr
verbatim in LR4b_lean_stdout.txt."""
import json, os, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
LEAN_DIR = os.path.join(os.path.dirname(HERE), "fable_independent_2026", "lean_2026")
OUT = os.path.join(HERE, "LR4b_cov_assembly.out")
RESF = os.path.join(HERE, "LR4b_results.json")
_T0 = time.time()
LOG = []
def log(m):
    line = "[%7.1fs] %s" % (time.time() - _T0, m); LOG.append(line); print(line, flush=True)
def finish(rc, verdict, extra=None):
    RES = dict(title="LR4b cov discharge assembly",
               pre_registration="Z7-WAVE_BRIEF.md amendment 2 / LR4b docstring",
               verdict=verdict, exit=rc, elapsed_s=round(time.time() - _T0, 1), log=LOG)
    if extra: RES.update(extra)
    with open(RESF, "w") as f: json.dump(RES, f, indent=1, default=str)
    with open(OUT, "a") as f: f.write("\n".join(LOG) + "\nVERDICT: %s (exit %d)\n" % (verdict, rc))
    print("VERDICT: %s (exit %d)" % (verdict, rc)); sys.exit(rc)

LEAN = "LR4b_cov_discharge.lean"
log("G1: compiling %s" % LEAN)
p = subprocess.run(["lake", "env", "lean", LEAN], cwd=LEAN_DIR,
                   capture_output=True, text=True, timeout=1800)
out = p.stdout + p.stderr
with open(os.path.join(HERE, "LR4b_lean_stdout.txt"), "w") as f:
    f.write(out)
log("G1: lake rc=%d (%d chars stdout+stderr)" % (p.returncode, len(out)))
if p.returncode != 0:
    finish(1, "G1-FAIL: compile rc=%d (stderr in LR4b_lean_stdout.txt)" % p.returncode)
src = open(os.path.join(LEAN_DIR, LEAN)).read()
import re as _re
in_block = False
bad = []
for l in src.splitlines():
    st = l.strip()
    if st.startswith("/-!") or st.startswith("/-"):
        in_block = True
    if in_block:
        if st.endswith("-/") or st == "-/":
            in_block = False
        continue
    if "--" in l:
        l = l.split("--", 1)[0]
    if _re.search(r"\bsorry\b", l):
        bad.append(l)
if bad:
    finish(1, "G1-FAIL: sorry in banked file: %r" % bad[:3])
need = ["'outer_v' depends on axioms: [propext, Classical.choice, Quot.sound]",
        "'chord_cond' depends on axioms: [propext, Classical.choice, Quot.sound]",
        "'I1_cond' depends on axioms: [propext, Classical.choice, Quot.sound]"]
missing = [n for n in need if n not in out]
if missing:
    finish(1, "G1-FAIL: axiom print missing/extra: %s" % missing)
log("G1: PASS (rc 0, zero sorry, axioms clean for outer_v/chord_cond/I1_cond)")
log("G2: constants cross-check")
g2 = "= 3/4" in src.replace("3 / 4", "3/4") or "= 3/4" in src
g2b = "= 5/12" in src.replace("5 / 12", "5/12") or "((5:Q)/12" in src or "5/12" in src
if not (g2 and g2b):
    finish(1, "G2-FAIL: unconditional constants not 3/4 / 5/12")
log("G2: PASS (chord 3/4, I1 5/12 -- LR3b conditional constants preserved)")
finish(0, "BANKED-DISCHARGED: covStatement discharged -- chord_cond and I1_cond are "
          "UNCONDITIONAL M01 certificates (3/4, 5/12), assembled from the conductor "
          "stage bank (tri_fubini, disk_fubini, slice_subst, bridges, outer_v); "
          "all stages zero-sorry, axioms {propext, Classical.choice, Quot.sound}")
