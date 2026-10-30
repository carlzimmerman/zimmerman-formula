#!/usr/bin/env python3
"""X76 lensing: X53's committed script with the smooth core and the fair-share galaxy halo rule (x76_patch), z = 0.285.
X76_FAIR=0 must reproduce X74_smooth_core_lensing's smooth chi2 (K1).  kappa = 1/2 FITTED; not theory closed.
    X76_FAIR=1|0 [X53_MUTATE=1] PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x76_lensing.py
"""
import os, sys, json
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE); sys.path.insert(0, HERE)
import x76_patch as XP
ON = os.environ.get("X76_FAIR", "1") == "1"; MUT = os.environ.get("X53_MUTATE") == "1"
X53D = os.path.join(REB, "X53_outer_lensing_law_vs_halos"); SRC = os.path.join(X53D, "x53_outer_lensing.py")
src = XP.patch(open(SRC).read())
tag = ("_fair" if ON else "_sparc") + ("_MUTATE" if MUT else "")
for a, b in (('os.path.join(HERE, f"x53_outer_lensing_results{SFX}.json")', repr(os.path.join(HERE, f"x76_lensing_results{tag}.json"))),
             ('os.path.join(HERE, f"x53_outer_lensing{SFX}.out")', repr(os.path.join(HERE, f"x76_lensing{tag}.out")))):
    assert src.count(a) == 1; src = src.replace(a, b)
ns = {"__file__": SRC, "__name__": "__main__"}; ns.update(XP.ns_globals(ON, 0.285)); sys.argv = [SRC]
try:
    exec(compile(src, SRC, "exec"), ns)
except SystemExit:
    pass
R = json.load(open(os.path.join(HERE, f"x76_lensing_results{tag}.json")))
X = json.load(open(os.path.join(REB, "X74_smooth_core_lensing", "x74_lensing_results_S" + ("_MUTATE" if MUT else "") + ".json")))
lines = [f"\n=== X76 lensing [{'fair share' if ON else 'SPARC (identity)'}{' MUTATE' if MUT else ''}], z_ta 0.285, R_nat {XP.RNAT:.4f}"]
d = 0.0; out = {}
for f in ("canonical", "alt"):
    for lab in ("primary", "all"):
        a, b = R["footings"][f][lab], X["footings"][f][lab]
        d = max([d] + [abs(a[m]["chi2"] - b[m]["chi2"]) for m in ("L", "H", "L2H", "H2H")])
        out[f"{f}|{lab}"] = dict(dchi2=a["dchi2_H2H_minus_L2H"], sparc=b["dchi2_H2H_minus_L2H"])
        lines.append(f"  [{f} {lab}] dchi2(H2H-L2H) {a['dchi2_H2H_minus_L2H']:+.1f} (SPARC smooth {b['dchi2_H2H_minus_L2H']:+.1f}); class {R['footings'][f]['verdict']}")
    out[f"{f}|meta"] = R["footings"][f]["meta"]
    lines.append(f"  [{f}] bin <log M_halo> {[round(R['footings'][f]['meta'][str(b)]['lM200_wmean'] if str(b) in R['footings'][f]['meta'] else R['footings'][f]['meta'][b]['lM200_wmean'], 2) for b in range(4)]}")
if not ON:
    lines.append(f"  K1 SPARC identity vs X74_smooth_core_lensing: max |d chi2| {d:.1e}: {'PASS' if d <= 1e-9 else 'FAIL'}"); out["K1"] = d
print("\n".join(lines)); open(os.path.join(HERE, f"x76_lensing{tag}.out"), "a").write("\n".join(lines) + "\n")
json.dump(out, open(os.path.join(HERE, f"x76_lensing_grade{tag}.json"), "w"), indent=1, default=float)
