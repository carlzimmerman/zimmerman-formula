#!/usr/bin/env python3
"""LR3 -- M01 Lean lane / M-roads: first-flight moment certificate (Z6-wave; owns LR3_*).
Gates (Z6-WAVE_BRIEF.md + amendments): R0 mechanical sympy re-derivation must
reproduce chord 3/4, E[int r^2] 5/12, E[int r^4] 17/60, E[int r^6] 149/700 AND the
rationals must appear in the certified Lean file; G1 = lake env lean rc 0, ZERO
sorry, axioms subset {propext, Classical.choice, Quot.sound} for every theorem.
The Lean file fable_independent_2026/lean_2026/LR3_m05_moments.lean was compiled
and verified (rc 0) before this lane run; the lane re-verifies under its own record."""
import json, os, re, subprocess, sys, time
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
LEAN_DIR = os.path.join(os.path.dirname(HERE), "fable_independent_2026", "lean_2026")
LEAN_FILE = "LR3_m05_moments.lean"
OUT = os.path.join(HERE, "LR3_m05_moments.out")
RESF = os.path.join(HERE, "LR3_results.json")
ALLOWED = {"propext", "Classical.choice", "Quot.sound"}
_T0 = time.time(); LOG = []
def log(m):
    line = "[%7.1fs] %s" % (time.time() - _T0, m); LOG.append(line); print(line, flush=True)
def finish(rc, verdict, extra=None):
    RES = dict(title="LR3 M05 first-flight moments Lean certificate",
               pre_registration="Z6-WAVE_BRIEF.md LR3 gates + amendments",
               verdict=verdict, exit=rc, elapsed_s=round(time.time() - _T0, 1), log=LOG)
    if extra: RES.update(extra)
    with open(RESF, "w") as f: json.dump(RES, f, indent=1, default=str)
    with open(OUT, "a") as f: f.write("\n".join(LOG) + "\nVERDICT: %s (exit %d)\n" % (verdict, rc))
    print("VERDICT: %s (exit %d)" % (verdict, rc)); sys.exit(rc)

# R0: mechanical sympy derivation from the definition
wq, vv = sp.symbols('w v', real=True)
U, S = sp.symbols('U sstar', positive=True)
vals = {}
for k in (1, 2, 3):
    Ik = sp.integrate((U ** 2 + wq ** 2) ** k, (wq, vv, S))
    inner = sp.expand(sp.integrate(Ik, (vv, -S, S)) / (2 * S))
    expr = sp.expand(3 * U * sp.sqrt(1 - U ** 2) * inner.subs(S, sp.sqrt(1 - U ** 2)))
    vals[k] = sp.nsimplify(sp.integrate(expr, (U, 0, 1)))
    log("R0: mechanical sympy E[int r^%d ds] = %s" % (2 * k, vals[k]))
ch = sp.nsimplify(3 * sp.integrate(U * (1 - U ** 2), (U, 0, 1)))
log("R0: chord = %s" % ch)
expect = {None: "3/4", 1: "5/12", 2: "17/60", 3: "149/700"}
ok0 = (str(ch) == expect[None] and all(str(vals[k]) == expect[k] for k in (1, 2, 3)))
lean_txt = open(os.path.join(LEAN_DIR, LEAN_FILE)).read()
in_file = all(re.search(r"\(\(%d\s*:\s*ℚ\)\s*/\s*%d\s*:\s*ℝ\)"
              % (sp.numer(sp.Rational(e)), sp.denom(sp.Rational(e))), lean_txt) is not None
              for e in expect.values())
log("R0 %s; rationals present in %s: %s" % ("PASS" if ok0 else "FAIL", LEAN_FILE, in_file))
if not (ok0 and in_file):
    finish(1, "R0-FAIL: mechanical derivation mismatch or Lean file cross-check failed")

# G1: compile + parse
with open(os.path.join(HERE, "LR3_lean_stdout_final.txt"), "w") as fo:
    p = subprocess.run(["lake", "env", "lean", LEAN_FILE], cwd=LEAN_DIR,
                       stdout=fo, stderr=subprocess.STDOUT, timeout=1800)
out = open(os.path.join(HERE, "LR3_lean_stdout_final.txt")).read()
with open(OUT, "a") as fo:
    fo.write("\n=== LR3 final run %s (lake env lean rc=%s) ===\n%s\n"
             % (time.strftime("%Y-%m-%d %H:%M:%S"), p.returncode, out))
errs = [l for l in out.splitlines() if "error" in l.lower()]
sorries = [l for l in out.splitlines() if "sorry" in l.lower()]
ax = {}
for l in out.splitlines():
    mm = re.match(r"'([^']+)' depends on axioms: \[(.*)\]", l.strip())
    if mm: ax[mm.group(1)] = set(a.strip() for a in mm.group(2).split(","))
ax_ok = len(ax) >= 4 and all(a <= ALLOWED for a in ax.values())
log("G1: rc=%d errors=%d sorries=%d axioms_ok=%s (%d theorems)" % (p.returncode, len(errs), len(sorries), ax_ok, len(ax)))
if p.returncode == 0 and not errs and not sorries and ax_ok:
    finish(0, "G1-CERTIFIED: val_chord 3/4, val_I1 5/12, val_I2 17/60, val_I3 149/700 zero-sorry, "
              "axioms in {propext, Classical.choice, Quot.sound}; M01 sec.6's chord blocker BYPASSED "
              "via the polynomial 1D reduction (M05's I2 table entry 1/4 corrected to 17/60, see M05B)")
finish(1, "G1-FAIL: compile/sorry/axioms gate failed (stdout preserved verbatim)")
