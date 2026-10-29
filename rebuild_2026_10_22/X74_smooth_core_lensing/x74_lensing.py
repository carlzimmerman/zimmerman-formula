#!/usr/bin/env python3
"""X74_smooth_core_lensing: X53's committed x53_outer_lensing.py, executed from its own text with one change, the halo
shape: Burkert B(x) -> smooth B_S(x) = 4(asinh x - x/sqrt(1+x^2)), and eta(M) -> eta(M) * B1/B_S(1) (X70's re-derivation).
Frozen criteria: FROZEN_CRITERIA.md (bc08edb85a). One thread.
kappa = 1/2 FITTED; c_f EXTERNAL; footings never pooled; not theory closed.

    X74_SHAPE=S|B [X53_MUTATE=1] PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x74_lensing.py
    X74_SHAPE=B must reproduce X53's committed chi2 values (K1).
"""
import os, sys, json, math
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE)
SHAPE = os.environ.get("X74_SHAPE", "S"); assert SHAPE in ("S", "B")
MUT = os.environ.get("X53_MUTATE") == "1"
X53D = os.path.join(REB, "X53_outer_lensing_law_vs_halos"); SRC = os.path.join(X53D, "x53_outer_lensing.py")
src = open(SRC).read()


def rep(a, b):
    global src
    assert src.count(a) == 1, (a[:70], src.count(a)); src = src.replace(a, b)


B_S = 'def B(x):\n    x = np.asarray(x, float)\n    return 4 * (np.arcsinh(x) - x / np.sqrt(1 + x * x))\n'
if SHAPE == "S":
    rep("def B(x):\n    x = np.asarray(x, float); return np.log1p(x * x) + 2 * np.log1p(x) - 2 * np.arctan(x)\n", B_S)
    rep("    return 4.0 / (3.0 * B1) * cf ** 1.25\n", "    return 4.0 / (3.0 * B1) * cf ** 1.25 * B1 / float(B(1.0))\n")
    rep("(St / r0t) * r0t ** 3 / ((r + r0t) * (r * r + r0t * r0t))", "(St / r0t) * r0t ** 3 / (r * r + r0t * r0t) ** 1.5")
tag = f"_{SHAPE}" + ("_MUTATE" if MUT else "")
rep('os.path.join(HERE, f"x53_outer_lensing_results{SFX}.json")', repr(os.path.join(HERE, f"x74_lensing_results{tag}.json")))
rep('os.path.join(HERE, f"x53_outer_lensing{SFX}.out")', repr(os.path.join(HERE, f"x74_lensing{tag}.out")))
ns = {"__file__": SRC, "__name__": "__main__"}
sys.argv = [SRC]
try:
    exec(compile(src, SRC, "exec"), ns)
except SystemExit:
    pass

# ------------------------------------------------------------------ X74 grading (frozen) on top of the X53 run
R = json.load(open(os.path.join(HERE, f"x74_lensing_results{tag}.json")))
X = json.load(open(os.path.join(X53D, "x53_outer_lensing_results" + ("_MUTATE" if MUT else "") + ".json")))
BS1 = float(ns["B"](1.0)); B1 = ns["B1"]
out = dict(shape=SHAPE, mutate=MUT, B_S1=BS1 if SHAPE == "S" else None, eta_cf4=float(ns["eta_of"](1e12, "cf4")), footings={})
lines = [f"\n=== X74 [{SHAPE}{' MUTATE' if MUT else ''}]: eta(c_f 4) {out['eta_cf4']:.4f}" + (f"; B_S(1) {BS1:.5f}" if SHAPE == "S" else "")]
dmax = 0.0
for f in ("canonical", "alt"):
    o = {}
    for lab in ("primary", "all"):
        a, b = R["footings"][f][lab], X["footings"][f][lab]
        for m in ("L", "H", "L2H", "H2H"):
            dmax = max(dmax, abs(a[m]["chi2"] - b[m]["chi2"])) if SHAPE == "B" else dmax
        o[lab] = dict(dchi2_2h=a["dchi2_H2H_minus_L2H"], dchi2_2h_X53=b["dchi2_H2H_minus_L2H"], H2H=a["H2H"]["chi2"], H2H_X53=b["H2H"]["chi2"],
                      change=a["dchi2_H2H_minus_L2H"] - b["dchi2_H2H_minus_L2H"])
        lines.append(f"  [{f} {lab}] dchi2(H2H-L2H) {o[lab]['dchi2_2h']:+.1f} (X53 Burkert {o[lab]['dchi2_2h_X53']:+.1f}; change {o[lab]['change']:+.1f})")
    RF, XF = R["footings"][f], X["footings"][f]
    o["class"], o["class_X53"] = RF["verdict"], XF["verdict"]
    o["grade"] = "SHAPE DOES NOT MOVE THE LENSING GRADE" if RF["verdict"] == XF["verdict"] else "SHAPE MOVES THE LENSING GRADE"
    o["variants"] = RF.get("variants")
    lines.append(f"  [{f}] X53 rule: {RF['verdict']} (X53 Burkert: {XF['verdict']}) -> {o['grade']}")
    out["footings"][f] = o
out["verdict_X53_rule"] = R["verdict"]; out["verdict_X53"] = X["verdict"]
out["grade"] = {f: out["footings"][f]["grade"] for f in ("canonical", "alt")}
out["pre_registered_lt20"] = all(abs(out["footings"][f]["all"]["change"]) < 20 for f in ("canonical", "alt"))
if SHAPE == "B":
    out["K1_identity_max_d"] = dmax; lines.append(f"  K1 Burkert identity vs X53 chi2: max |d| {dmax:.1e}: {'PASS' if dmax <= 1e-9 else 'FAIL'}")
else:
    lines.append(f"  K2 B_S(1) = {BS1:.5f} (0.69707): {'PASS' if abs(BS1 - 0.69707) < 1e-5 else 'FAIL'}")
lines.append(f"  lane verdict (X53 rule): {R['verdict']} (X53: {X['verdict']}); pre-registered |change| < 20 on all radii: {out['pre_registered_lt20']}")
print("\n".join(lines))
open(os.path.join(HERE, f"x74_lensing{tag}.out"), "a").write("\n".join(lines) + "\n")
json.dump(out, open(os.path.join(HERE, f"x74_grade{tag}.json"), "w"), indent=1, default=float)
