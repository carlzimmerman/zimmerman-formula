#!/usr/bin/env python3
"""X79_native_eta_mw_kids, part KiDS (criteria c7d5c7f1c1): X53's x53_outer_lensing.py with X74_smooth_core_lensing's
smooth-core patch, plus one change: eta_of(M, "cf4") returns X77's eta_native(M) (lg-M interpolation, flat outside).
    X79_ETA=native|const [X79_ETAMULT=2] PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x79_kids.py
const must reproduce X74_smooth_core_lensing's x74_lensing_results_S.json chi2 (K2). kappa = 1/2 FITTED; not theory closed."""
import os, sys, json, math
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
os.environ.pop("X53_MUTATE", None)
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE)
MODE = os.environ.get("X79_ETA", "native"); MULT = float(os.environ.get("X79_ETAMULT", "1"))
X53D = os.path.join(REB, "X53_outer_lensing_law_vs_halos"); SRC = os.path.join(X53D, "x53_outer_lensing.py"); src = open(SRC).read()
def rep(a, b):
    global src
    assert src.count(a) == 1, (a[:70], src.count(a)); src = src.replace(a, b)
B_S = 'def B(x):\n    x = np.asarray(x, float)\n    return 4 * (np.arcsinh(x) - x / np.sqrt(1 + x * x))\n'
rep("def B(x):\n    x = np.asarray(x, float); return np.log1p(x * x) + 2 * np.log1p(x) - 2 * np.arctan(x)\n", B_S)     # X74 patch
rep("    return 4.0 / (3.0 * B1) * cf ** 1.25\n", "    return 4.0 / (3.0 * B1) * cf ** 1.25 * B1 / float(B(1.0))\n")
rep("(St / r0t) * r0t ** 3 / ((r + r0t) * (r * r + r0t * r0t))", "(St / r0t) * r0t ** 3 / (r * r + r0t * r0t) ** 1.5")
rep("def eta_of(M, cfmode):\n", "def _eta_of_x53(M, cfmode):\n")
NEW = f'''_S77 = json.load(open({os.path.join(REB, "X77_direct_core_surface_density", "x77_results.json")!r}))["summary"]
_EL = np.array([12.0, 13.0, 14.0]); _EV = np.array([_S77["1e+12_ng64"]["eta_med"], _S77["1e+13_ng48"]["eta_med"], _S77["1e+14_ng48"]["eta_med"]])
def eta_of(M, cfmode):
    if cfmode != "cf4": return _eta_of_x53(M, cfmode)
    return {MULT!r} * ({"float(np.interp(math.log10(M), _EL, _EV))" if MODE == "native" else '_eta_of_x53(M, "cf4")'})
'''
rep(B_S, NEW + B_S)
tag = f"_{MODE}" + ("" if MULT == 1 else f"x{MULT:g}")
rep('os.path.join(HERE, f"x53_outer_lensing_results{SFX}.json")', repr(os.path.join(HERE, f"x79_kids_results{tag}.json")))
rep('os.path.join(HERE, f"x53_outer_lensing{SFX}.out")', repr(os.path.join(HERE, f"x79_kids{tag}.out")))
ns = {"__file__": SRC, "__name__": "__main__"}; sys.argv = [SRC]
try:
    exec(compile(src, SRC, "exec"), ns)
except SystemExit:
    pass
R = json.load(open(os.path.join(HERE, f"x79_kids_results{tag}.json")))
X = json.load(open(os.path.join(REB, "X74_smooth_core_lensing", "x74_lensing_results_S.json")))
L = [f"\n=== X79 KiDS [{MODE} x{MULT:g}]: eta(1e12/1e13/1e14) " + ", ".join(f"{ns['eta_of'](10.0 ** l, 'cf4'):.3f}" for l in (12, 13, 14))]
out = dict(mode=MODE, mult=MULT, footings={})
d = 0.0
for f in ("canonical", "alt"):
    o = {}
    for lab in ("primary", "all"):
        a, b = R["footings"][f][lab], X["footings"][f][lab]
        d = max([d] + [abs(a[m]["chi2"] - b[m]["chi2"]) for m in ("L", "H", "L2H", "H2H")])
        o[lab] = dict(dchi2=a["dchi2_H2H_minus_L2H"], dchi2_c4=b["dchi2_H2H_minus_L2H"], H2H=a["H2H"]["chi2"], H2H_c4=b["H2H"]["chi2"])
        L.append(f"  [{f} {lab}] dchi2(H2H-L2H) {o[lab]['dchi2']:+.1f} (smooth c_f 4: {o[lab]['dchi2_c4']:+.1f}); H2H chi2 {o[lab]['H2H']:.1f} (c_f 4: {o[lab]['H2H_c4']:.1f})")
    o["verdict"] = R["footings"][f]["verdict"]; o["verdict_c4"] = X["footings"][f]["verdict"]
    L.append(f"  [{f}] X53 rule: {o['verdict']} (c_f 4: {o['verdict_c4']})"); out["footings"][f] = o
if MODE == "const" and MULT == 1:
    out["K2_max_d"] = d; L.append(f"  K2 identity vs X74_smooth_core_lensing chi2: max |d| {d:.1e}: {'PASS' if d <= 1e-9 else 'FAIL'}")
print("\n".join(L)); open(os.path.join(HERE, f"x79_kids{tag}.out"), "a").write("\n".join(L) + "\n")
json.dump(out, open(os.path.join(HERE, f"x79_kids_grade{tag}.json"), "w"), indent=1, default=float)
