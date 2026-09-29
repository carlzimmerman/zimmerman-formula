#!/usr/bin/env python3
"""P4 -- re-run the Lean certificates of AH3 (fable_independent_2026/lean_2026/AH3_alpha_nogo.lean) and its MUTATE control, read-only.

Pre-registered in P_PREREGISTRATION.md (statement S06).  Runs `lake env lean <file>` in the Lean project directory (writes nothing there) and asserts:
  L1  the real file compiles (exit 0) and prints exactly the ten '#print axioms' lines of the committed .out (standard axioms only);
  L2  the MUTATE file exits 1 with exactly three 'error:' lines, at the same line numbers as the committed AH3_alpha_nogo_MUTATE.out (18, 26, 39);
  L3  the real file contains no 'sorry' and no 'axiom' declaration.
It does NOT check that the premise of the no-go (an observable depending on e only through eE/H^2) holds for any physical quantity: see P_REPORT.md.

Run:     PYTHONDONTWRITEBYTECODE=1 python3 p4_lean_rerun.py
CONTROL: PYTHONDONTWRITEBYTECODE=1 python3 p4_lean_rerun.py MUTATE
         (the ONLY trigger is argv[1] == "MUTATE": the MUTATE Lean file is treated as if it were the real one, so L1 must fail -> exit 1)
"""
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LEAN = os.path.abspath(os.path.join(HERE, "..", "..", "..", "fable_independent_2026", "lean_2026"))
MUT = len(sys.argv) > 1 and sys.argv[1] == "MUTATE"
FAILS = []


def chk(tag, ok, note=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {tag} {note}")
    if not ok:
        FAILS.append(tag)


def lean(fname):
    p = subprocess.run(["lake", "env", "lean", fname], cwd=LEAN, capture_output=True, text=True, timeout=900)
    return p.returncode, p.stdout + p.stderr


real_file = "AH3_alpha_nogo_MUTATE.lean" if MUT else "AH3_alpha_nogo.lean"
rc, out = lean(real_file)
committed = [l for l in open(os.path.join(LEAN, "AH3_alpha_nogo.out")).read().strip().splitlines() if "depends on axioms" in l]
lines = [l for l in out.strip().splitlines() if "depends on axioms" in l]
chk("L1 real file exits 0", rc == 0, f"(exit {rc})")
chk("L1 real file prints the ten committed '#print axioms' lines, identical", lines == committed and len(lines) == 10, f"({len(lines)} lines)")
chk("L1 every line lists only propext, Classical.choice, Quot.sound", all(re.search(r"\[propext, Classical\.choice, Quot\.sound\]$", l) for l in lines))
src = open(os.path.join(LEAN, "AH3_alpha_nogo.lean")).read()
chk("L3 no 'sorry' (outside the sentence 'Zero sorry.') and no 'axiom' declaration in the real file", "sorry" not in src.replace("Zero sorry.", "") and not re.search(r"^axiom ", src, re.M))
rcm, outm = lean("AH3_alpha_nogo_MUTATE.lean")
errs = sorted(int(m.group(1)) for m in re.finditer(r"AH3_alpha_nogo_MUTATE\.lean:(\d+):\d+: error", outm))
cerrs = sorted(int(m.group(1)) for m in re.finditer(r"AH3_alpha_nogo_MUTATE\.lean:(\d+):\d+: error", open(os.path.join(LEAN, "AH3_alpha_nogo_MUTATE.out")).read()))
chk("L2 MUTATE file exits 1", rcm == 1, f"(exit {rcm})")
chk("L2 exactly three errors, at the committed line numbers", errs == cerrs and len(errs) == 3, f"({errs} vs committed {cerrs})")
print("\nFAILED:", FAILS if FAILS else "none")
sys.exit(1 if FAILS else 0)
