#!/usr/bin/env python3
"""LR3b -- reduction-lemma lane (Z6-wave; owns LR3b_*). Gates (Z6-WAVE_BRIEF.md
amendment 2): G2a = step1 (linear substitution) zero-sorry; G2b = chord_cond 3/4 and
I1_cond 5/12 CONDITIONAL on cov (stated hypothesis, never sorry'd), with the (u,v)
side fully evaluated; G2b-full (discharging cov) recorded OPEN. exit 0 iff G2a AND
G2b-conditional; verdict CERTIFIED-G2a-CONDITIONAL."""
import json, os, re, subprocess, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
LEAN_DIR = os.path.join(os.path.dirname(HERE), "fable_independent_2026", "lean_2026")
LEAN_FILE = "LR3b_m05_reduction.lean"
OUT = os.path.join(HERE, "LR3b_reduction.out")
RESF = os.path.join(HERE, "LR3b_results.json")
ALLOWED = {"propext", "Classical.choice", "Quot.sound"}
_T0 = time.time(); LOG = []
def log(m):
    line = "[%7.1fs] %s" % (time.time() - _T0, m); LOG.append(line); print(line, flush=True)
def finish(rc, verdict):
    RES = dict(title="LR3b reduction lemma lane",
               pre_registration="Z6-WAVE_BRIEF.md amendment 2 (LR3b gates)",
               verdict=verdict, exit=rc, elapsed_s=round(time.time() - _T0, 1), log=LOG)
    with open(RESF, "w") as f: json.dump(RES, f, indent=1, default=str)
    with open(OUT, "a") as f: f.write("\n".join(LOG) + "\nVERDICT: %s (exit %d)\n" % (verdict, rc))
    print("VERDICT: %s (exit %d)" % (verdict, rc)); sys.exit(rc)
with open(os.path.join(HERE, "LR3b_lean_stdout_final.txt"), "w") as fo:
    p = subprocess.run(["lake", "env", "lean", LEAN_FILE], cwd=LEAN_DIR,
                       stdout=fo, stderr=subprocess.STDOUT, timeout=1800)
out = open(os.path.join(HERE, "LR3b_lean_stdout_final.txt")).read()
with open(OUT, "a") as fo:
    fo.write("\n=== LR3b final run %s (lake env lean rc=%s) ===\n%s\n"
             % (time.strftime("%Y-%m-%d %H:%M:%S"), p.returncode, out))
errs = [l for l in out.splitlines() if "error" in l.lower()]
sorries = [l for l in out.splitlines() if "sorry" in l.lower()]
ax = {}
for l in out.splitlines():
    mm = re.match(r"'([^']+)' depends on axioms: \[(.*)\]", l.strip())
    if mm: ax[mm.group(1)] = set(a.strip() for a in mm.group(2).split(","))
need = {"step1", "chord_cond", "I1_cond"}
ax_ok = need <= set(ax) and all(ax[k] <= ALLOWED for k in need)
log("G2a/G2b: rc=%d errors=%d sorries=%d axioms_ok=%s (theorems: %s)"
    % (p.returncode, len(errs), len(sorries), ax_ok, sorted(ax)))
if p.returncode == 0 and not errs and not sorries and ax_ok:
    finish(0, "CERTIFIED-G2a-CONDITIONAL: step1 (linear substitution, mathlib "
              "integral_comp_mul_left) + chord_cond 3/4 + I1_cond 5/12 zero-sorry, conditional "
              "on the stated cov hypothesis (never sorry'd); G2b-full (discharging cov: triangle "
              "Fubini + u=sqrt(r^2-v^2) singular substitution) remains the recorded OPEN piece")
finish(1, "G2a/G2b-FAIL: compile/sorry/axioms gate failed (stdout preserved verbatim)")
