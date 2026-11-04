#!/usr/bin/env python3
"""FN1 check_brief: each quoted number in DECISION_BRIEF.md sits inside a checked fragment, and each fragment's literal
appears in the committed file named beside it (PAPER67_audit.py's pattern). Naming and rule checks follow.
Run: python3 -I -B check_brief.py (exit 0 only if all pass). --mutate bumps the last digit of each source literal; the twin
passes when at least 80 % of the bumped literals are then not found, with every survivor listed.
Criteria 72f9d70fd6. kappa = 1/2 FITTED; not theory closed; nothing here says the data favour the framework."""
import os, re, sys
sys.dont_write_bytecode = True
MUT = "--mutate" in sys.argv
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
BRIEF = open(os.path.join(HERE, "DECISION_BRIEF.md"), encoding="utf-8").read()
_ns = {}; exec(open(os.path.join(HERE, "check_brief_sources.py"), encoding="utf-8").read(), _ns); L = _ns["L"]   # (fragment in the brief, source file, literal in that file)
OUT = []
def P(s=""): print(s, flush=True); OUT.append(s)
_cache = {}
def rd(f):
    if f not in _cache: _cache[f] = open(os.path.join(ROOT, f), encoding="utf-8", errors="replace").read()
    return _cache[f]
def bump(t):
    for i in range(len(t) - 1, -1, -1):
        if t[i] in "0123456789": return t[:i] + str((int(t[i]) + 1) % 10) + t[i + 1:]
    return t + "!"
F = 0; n = 0
if MUT:
    caught = 0; surv = []
    for frag, f, lit in L:
        n += 1; ok = bump(lit) not in rd(f) or frag not in BRIEF; caught += ok
        if not ok: surv.append((lit, f))
    P(f"MUTATE: {caught} of {n} perturbed literals not found (line: at least 80 %)")
    P("(a literal can survive when the bumped digit happens to appear elsewhere in its file; each survivor is listed)")
    for lit, f in surv: P(f"  survivor {lit!r} {f}")
    open(os.path.join(HERE, "check_brief_MUTATE.out"), "w").write("\n".join(OUT) + "\n")
    sys.exit(0 if caught >= 0.8 * n else 1)
# 1. every fragment is in the brief and every literal in its source
for frag, f, lit in L:
    n += 1; a = frag in BRIEF; b = lit in rd(f)
    if not (a and b): F += 1; P(f"  FAIL {'BRIEF ' if not a else ''}{'SRC ' if not b else ''}{frag!r} | {f} | {lit!r}")
# 2. coverage: every number in the brief lies inside a checked fragment
text = BRIEF
text = re.sub(r"`[^`]*`", lambda m: " " * len(m.group(0)), text)                                  # code spans: file names, paths
text = re.sub(r"\b20\d\d-\d\d-\d\d\b", lambda m: " " * len(m.group(0)), text)                     # dates
text = re.sub(r"\b(?=[0-9a-f]*[a-f])[0-9a-f]{10}\b", lambda m: " " * len(m.group(0)), text)        # commit hashes
cov = [False] * len(BRIEF)
for frag, f, lit in L:
    for m in re.finditer(re.escape(frag), BRIEF):
        for i in range(m.start(), m.end()): cov[i] = True
nums = list(re.finditer(r"(?<![A-Za-z0-9_.])\d+(?:[.,]\d+)*(?:e[-−]?\d+)?(?![A-Za-z0-9_])", text))
unc = [m for m in nums if not all(cov[m.start():m.end()])]
n += 1
if unc:
    F += 1; P(f"  FAIL coverage: {len(unc)} of {len(nums)} numbers sit in no checked fragment")
    for m in unc[:60]: P(f"    uncovered {m.group(0)!r} at: {BRIEF[max(0, m.start() - 40):m.end() + 20]!r}")
else: P(f"  coverage: all {len(nums)} numbers sit in checked fragments")
# 3. naming and rule checks
low = " ".join(BRIEF.lower().split())   # whitespace-normalised, so a phrase broken across lines is still seen
import subprocess   # personal names to forbid come from the local git config, so none is written into a committed file
try: names = [w.lower() for w in subprocess.run(["git", "config", "user.name"], capture_output=True, text=True, cwd=HERE).stdout.split() if len(w) > 2]
except Exception: names = []
P(f"  names screened from the local git config: {len(names)}")
for bad in ["theory closed", "kappa derived", "κ derived", "measured flat", "/" + "users" + "/"] + names:
    n += 1
    if bad in low: F += 1; P(f"  FAIL found {bad!r}")
n += 1
fav = [m.start() for m in re.finditer("favour the framework", low)]
if any("nothing here says the data" not in low[max(0, i - 40):i] for i in fav): F += 1; P("  FAIL 'favour the framework' outside the disclaimer")
for need in ("κ = ½ FITTED", "not closed", "adopts nothing"):
    n += 1
    if need.lower() not in low: F += 1; P(f"  FAIL missing {need!r}")
P(f"{n - F} of {n} checks pass")
P("kappa = 1/2 FITTED; not theory closed; nothing here says the data favour the framework.")
open(os.path.join(HERE, "check_brief.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(1 if F else 0)
