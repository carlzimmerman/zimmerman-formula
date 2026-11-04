#!/usr/bin/env python3
"""FN1b: snapshot of KT33's stored known answers, so the lane runs from committed files. KT33 and KT34 were uncommitted in the
working tree when FN1b ran (2026-11-04). This copies, without computing anything, the first 25 in-prior rows per footing of
KT33's mw/grid_run/results.json (cell, width, and vc / K0 / cO of source_only and corrected) and the baseline
q_hessian_signed of cassini/run_002/results.json, with the SHA-256 of each source file and of the two vendored modules.
Run: python3 -I -B fn1b_ka_snapshot.py. kappa = 1/2 FITTED; not theory closed."""
import hashlib, json, os, sys
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE))); K33 = os.path.join(REPO, "rebuild_2026_10_22", "KT33_reciprocal_filter")
def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()
GR = os.path.join(K33, "mw", "grid_run", "results.json"); CR = os.path.join(K33, "cassini", "run_002", "results.json")
g = json.load(open(GR)); c = json.load(open(CR)); out = dict(sources={}, vendored={}, grid_run_first25={}, run002_baseline={})
for p in (GR, CR, os.path.join(K33, "mw", "mw_reciprocal.py"), os.path.join(K33, "cassini", "cassini_v2.py")): out["sources"][os.path.relpath(p, REPO)] = sha(p)
for f in ("mw_reciprocal.py", "cassini_v2.py"): out["vendored"]["vendor_kt33/" + f] = sha(os.path.join(HERE, "vendor_kt33", f))
for foot in ("canonical", "alt"):
    out["grid_run_first25"][foot] = [dict(cell=r["cell"], xi=r["xi"], source_only={k: r["source_only"][k] for k in ("vc", "K0", "cO")}, corrected={k: r["corrected"][k] for k in ("vc", "K0", "cO")}) for r in g["footings"][foot]["rows"][:25]]
    out["run002_baseline"][foot] = {arm: c["footings"][foot]["arms"][arm]["baseline"]["q_hessian_signed"] for arm in ("source_only_hessian", "reciprocal")}
same = all(out["sources"][os.path.relpath(os.path.join(K33, d, f), REPO)] == out["vendored"]["vendor_kt33/" + f] for d, f in (("mw", "mw_reciprocal.py"), ("cassini", "cassini_v2.py")))
out["vendored_equal_to_source"] = same
json.dump(out, open(os.path.join(HERE, "fn1b_ka_snapshot.json"), "w"), indent=1)
print(f"snapshot written; vendored modules byte-identical to KT33's: {same}"); sys.exit(0 if same else 1)
