"""Bitwise comparison of two CFG960 run directories (same tag): run JSON (every number except timing/mem/runtime/engine sha) and
every .npz array. usage: python3 cmp_runs.py DIR_A DIR_B"""
import sys, os, json, glob, numpy as np
A, B = sys.argv[1], sys.argv[2]
SKIP = {"timing_s", "mem", "runtime_s", "maxrss_gb", "engine_sha256", "t", "resumed_after_step", "shellcheck_steps", "engine_sha256_segments"}
n = [0, 0]; bad = []
def walk(x, y, p):
    if isinstance(x, dict):
        for k in set(x) | set(y):
            if k in SKIP: continue
            if k not in x or k not in y: bad.append(p + "/" + k + " missing"); continue
            walk(x[k], y[k], p + "/" + k)
    elif isinstance(x, list):
        if len(x) != len(y): bad.append(p + " len"); return
        for i, (a, b) in enumerate(zip(x, y)): walk(a, b, f"{p}[{i}]")
    else:
        n[0] += 1
        same = (x == y) or (isinstance(x, float) and isinstance(y, float) and np.isnan(x) and np.isnan(y))
        if not same: bad.append(f"{p}: {x!r} != {y!r}")
for ja in glob.glob(os.path.join(A, "*.json")):
    if os.path.basename(ja) in ("job.json",): continue
    jb = os.path.join(B, os.path.basename(ja)); walk(json.load(open(ja)), json.load(open(jb)), os.path.basename(ja))
for za in sorted(glob.glob(os.path.join(A, "*.npz"))):
    zb = os.path.join(B, os.path.basename(za)); a = np.load(za); b = np.load(zb)
    for k in a.files:
        n[1] += 1
        if a[k].tobytes() != b[k].tobytes(): bad.append(f"{os.path.basename(za)}:{k} differs")
print(json.dumps(dict(dir_a=os.path.basename(A), dir_b=os.path.basename(B), json_numbers_compared=n[0], npz_arrays_compared=n[1],
                      n_differences=len(bad), first_differences=bad[:20], bit_identical=not bad)))
sys.exit(0 if not bad else 1)
