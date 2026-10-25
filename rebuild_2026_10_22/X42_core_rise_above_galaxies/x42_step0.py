#!/usr/bin/env python3
"""X42 Step 0 (stop rule, FROZEN_CRITERIA section 0): rerun X40b's committed script read-only in a scratch copy (only its
output directory redirected) and compare its graded numbers with the committed x40b_sd_scaling_results.json to 1e-6.

    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x42_step0.py      -> x42_step0.out, x42_step0_results.json; exit 0 iff identical
"""
import os, sys, json, subprocess, tempfile
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE)
SRC = os.path.join(REB, "X40b_core_surface_density_scaling", "x40b_sd_scaling.py")
REF = json.load(open(os.path.join(REB, "X40b_core_surface_density_scaling", "x40b_sd_scaling_results.json")))
txt = open(SRC).read()
old = 'HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE); REPO = os.path.dirname(REB)'
assert txt.count(old) == 1
tmp = tempfile.mkdtemp(prefix="x42_step0_")
txt = txt.replace(old, f'HERE = {tmp!r}; REB = {REB!r}; REPO = os.path.dirname(REB)')
scr = os.path.join(tmp, "x40b_sd_scaling.py"); open(scr, "w").write(txt)
env = dict(os.environ, PYTHONHASHSEED="0", OMP_NUM_THREADS="1"); env.pop("X40B_MUTATE", None)
rc = subprocess.run([sys.executable, scr], env=env, cwd=tmp, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE).returncode
NEW = json.load(open(os.path.join(tmp, "x40b_sd_scaling_results.json")))
diffs = []
def cmp(path, a, b):
    if isinstance(a, dict):
        for k in a:
            if k in ("runtime",): continue
            if k not in b: diffs.append((path + "/" + k, "missing")); continue
            cmp(path + "/" + k, a[k], b[k])
    elif isinstance(a, list):
        if len(a) != len(b): diffs.append((path, "len")); return
        for j, (x, y) in enumerate(zip(a, b)): cmp(f"{path}[{j}]", x, y)
    elif isinstance(a, bool) or isinstance(a, str) or a is None:
        if a != b: diffs.append((path, f"{a} != {b}"))
    elif isinstance(a, (int, float)):
        if abs(a - b) > 1e-6: diffs.append((path, f"{a} vs {b}"))
cmp("", REF, NEW)
lines = [f"X42 Step 0: scratch rerun of X40b (exit {rc}); compared every number in x40b_sd_scaling_results.json to 1e-6"]
for f in ("canonical", "alt"):
    F = NEW["footings"][f]
    lines.append(f"  [{f}] X38 groups mean {F['X38_groups']['mean']:+.4f} Z {F['X38_groups']['Z']:+.2f} {F['X38_groups']['verdict']}; "
                 f"(C) alpha_best {F['C']['alpha_best']:.2f} chi2 {F['C']['scan'][str(F['C']['alpha_best'])]['chi2_h0672'] if str(F['C']['alpha_best']) in F['C']['scan'] else F['C']['scan'][F['C']['alpha_best']]['chi2_h0672']:.2f}; "
                 f"A MID-T3 Z {F['A']['clusters']['cells']['h0672']['G-MID-T3']['Z']:+.2f}")
lines.append(f"  verdict {NEW['verdict']}")
lines.append(f"  differences: {len(diffs)}" + ("" if not diffs else " -> " + "; ".join(f"{p}: {d}" for p, d in diffs[:20])))
ok = rc == 0 and not diffs
lines.append(f"STEP 0: {'PASS (identical)' if ok else 'FAIL -> lane stops'}")
print("\n".join(lines))
open(os.path.join(HERE, "x42_step0.out"), "w").write("\n".join(lines) + "\n")
json.dump(dict(pass_=ok, exit=rc, n_diff=len(diffs), diffs=diffs[:50], verdict=NEW["verdict"],
               X38_groups={f: NEW["footings"][f]["X38_groups"] for f in ("canonical", "alt")},
               C_alpha_best={f: NEW["footings"][f]["C"]["alpha_best"] for f in ("canonical", "alt")}),
          open(os.path.join(HERE, "x42_step0_results.json"), "w"), indent=1)
sys.exit(0 if ok else 1)
