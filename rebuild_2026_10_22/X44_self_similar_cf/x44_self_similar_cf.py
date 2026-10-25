#!/usr/bin/env python3
"""X44_self_similar_cf: the formation concentration from self-similar infall timing, and X43's rule regraded with it.

Frozen criteria: FROZEN_CRITERIA.md (c8dd02f5aa). X43's committed script is executed read-only (text copy) with c_f replaced
and its outputs renamed into this folder. One thread, a few minutes.

    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x44_self_similar_cf.py            -> .out, _results.json
    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x44_self_similar_cf.py --mutate   -> t_coll = t_ta (K1 must fail)
"""
import os, sys, json, math, time, io, contextlib
os.environ.setdefault("OMP_NUM_THREADS", "1")
from scipy.optimize import brentq

T0 = time.time()
MUTATE = "--mutate" in sys.argv
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE)
TAG = "_MUTATE" if MUTATE else ""
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)

P(f"X44_self_similar_cf  {'MUTATE run (t_coll = t_ta)' if MUTATE else 'normal run'}")
P("kappa = 1/2 FITTED; footings never pooled; route E, cold dark energy not matter; no simulation calibration; not theory closed")
COLL = 1.0 if MUTATE else 2.0                                                 # t_coll / t_ta
def gamma_of(eps): return 9 * eps / (1 + 3 * eps) if eps >= 2 / 3 else 2.0
def cf_ss(eps):
    g = gamma_of(eps); return COLL ** (2 / (3 * eps * (3 - g))), g            # 1 / x_c, x_c = (t_f/COLL / t_f)^{2/(3 eps)} mapped to radius
checks = []
cf, g = cf_ss(1.0)
k2 = abs(g - 2.25) < 1e-15
# K1: direct numerical solution of M_c/M_f = 2^{-2/(3 eps)} on M ~ r^{3 - gamma}
target = COLL ** (-2 / 3)
xc = brentq(lambda x: x ** (3 - g) - target, 1e-9, 1.0, xtol=1e-15)
k1 = abs(1 / xc - cf) < 1e-12 and abs(cf - 2 ** (8 / 9)) < 1e-12
P(f"c_f,SS (eps = 1, gamma = {g}) = {cf:.6f} (paper 2^(8/9) = {2 ** (8 / 9):.6f}); numerical 1/x_c = {1 / xc:.6f}")
P(f"K1 closed form vs numerical and vs 2^(8/9): {'PASS' if k1 else 'FAIL'};  K2 gamma(eps = 1) = 9/4: {'PASS' if k2 else 'FAIL'}")
checks += [("K1", k1), ("K2", k2)]
B1 = 3 * math.log(2) - math.pi / 2
eta = 4 / (3 * B1) * cf ** (g - 1)
P(f"eta(c_f,SS) = {eta:.3f}   (X43 used c_f 4 -> 14.83)")

# reported: eps from the local EPS slope at the cluster median, structural ratios
X41 = json.load(open(os.path.join(REB, "X41_collapse_floor_sigma", "x41_collapse_floor_results.json")))
P("reported: structural ratios of the infall solution read as 'c': r_ta/r_vir = 2 (spherical collapse); r_ta/r_1st caustic = 1/0.364 = 2.75 "
  "(Bertschinger 1985, literature); r_vir/r_1st caustic = 1.37")

def run_x43(cfv, tag):
    src = open(os.path.join(REB, "X43_collapse_core_floor", "x43_collapse_core.py")).read()
    assert src.count("CF = 4.0") == 1
    src = src.replace("CF = 4.0", f"CF = {cfv!r}")
    src = src.replace('f"x43_collapse_core{TAG}.out"', f'"x44_regrade_{tag}.out"').replace('f"x43_collapse_core_results{TAG}.json"', f'"x44_regrade_{tag}_results.json"')
    src = src.replace('"x43_x30_machinery"', '"x44_x30_machinery"')
    src = src.replace("sys.exit(0 if n == len(checks) else 1)", "pass")
    ns = {"__file__": os.path.join(HERE, "x43_copy.py"), "__name__": "x43_copy"}
    argv0 = sys.argv; sys.argv = [ns["__file__"]]
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(io.StringIO()):
        exec(compile(src, ns["__file__"], "exec"), ns)
    sys.argv = argv0
    return ns["RES"]

R4 = run_x43(4.0, "cf4")
X43J = json.load(open(os.path.join(REB, "X43_collapse_core_floor", "x43_collapse_core_results.json")))
d0 = max(abs(R4["footings"][f]["groups"]["Z"] - X43J["footings"][f]["groups"]["Z"]) for f in ("canonical", "alt"))
d1 = max(abs(R4["footings"][f]["clusters"]["cells"]["h0672"]["G-OUT-M3"]["Z"] - X43J["footings"][f]["clusters"]["cells"]["h0672"]["G-OUT-M3"]["Z"]) for f in ("canonical", "alt"))
k0 = d0 < 1e-9 and d1 < 1e-9
P(f"K0 c_f 4 reproduces X43 (groups Z, MGAS T3 OUTER Z): max |d| {max(d0, d1):.1e}: {'PASS' if k0 else 'FAIL'}   [{time.time() - T0:.0f} s]")
checks.append(("K0", k0))

RS = run_x43(float(cf), "cfSS")
RES = dict(frozen="c8dd02f5aa", mutate=MUTATE, c_f_SS=cf, gamma=g, eta=eta, footings={})
for f in ("canonical", "alt"):
    F = RS["footings"][f]; c0 = F["clusters"]["cells"]["h0672"]
    sp = F["sparc"]["A_c2b_refit"]; gr = F["groups"]
    fails = F["failing"]
    v = "SS PASSES" if not fails else "SS FAILS: " + ", ".join(fails)
    RES["footings"][f] = dict(verdict=v, sparc=dict(rms=sp["rms"], U=sp["U_median"], line=sp["line"]), groups=dict(Z=gr["Z"], verdict=gr["verdict"]),
                              MID_T3=c0["G-MID-T3"], MID_b=c0["G-MID-b"], OUT_M3=c0["G-OUT-M3"], n_fail=len(fails))
    P(f"\n=== [{f}] c_f,SS {cf:.3f} (eta {eta:.2f})")
    P(f"  SPARC bg A: rms {sp['rms']:.4f}, U {sp['U_median']:.2f}, line {'PASS' if sp['line'] else 'FAIL'}; groups Z {gr['Z']:+.2f} {gr['verdict']}")
    P(f"  MID T3 pred {c0['G-MID-T3']['pred']:.3f} Z {c0['G-MID-T3']['Z']:+.2f}; MID slope Z {c0['G-MID-b']['Z']:+.2f}; MGAS T3 OUTER Z {c0['G-OUT-M3']['Z']:+.2f}")
    P(f"  VERDICT [{f}]: {v}")
# reported: c_f needed for X43's binding keys, interpolating X43's sensitivity
for f in ("canonical", "alt"):
    rep = X43J["footings"][f]["reported"]; zs = {3.0: rep["c_f 3"]["groups"]["Z"], 4.0: X43J["footings"][f]["groups"]["Z"], 5.0: rep["c_f 5"]["groups"]["Z"]}
    need = 4.0 + (zs[4.0] - 2.0) / (zs[4.0] - zs[5.0]) if zs[4.0] > zs[5.0] else float("nan")
    P(f"  (reported) [{f}] groups reach Z = 2.0 at c_f ~ {need:.2f} (X43 sensitivity, linear between 4 and 5)")
V = {f: RES["footings"][f]["verdict"].split(":")[0] for f in RES["footings"]}
RES["verdict"] = RES["footings"]["canonical"]["verdict"] if V["canonical"] == V["alt"] else f"UNDECIDED {V}"
P(f"\n=== VERDICT (both footings): {RES['verdict']}")
P("\n=== CHECKS"); [P(f"  [{'PASS' if ok else 'FAIL'}] {k}") for k, ok in checks]
RES["checks"] = {k: bool(ok) for k, ok in checks}; n = sum(ok for _, ok in checks)
P(f"\nchecks {n}/{len(checks)}; runtime {time.time() - T0:.0f} s")
open(os.path.join(HERE, f"x44_self_similar_cf{TAG}.out"), "w").write("\n".join(OUT) + "\n")
json.dump(RES, open(os.path.join(HERE, f"x44_self_similar_cf_results{TAG}.json"), "w"), indent=1, default=float)
sys.exit(0 if n == len(checks) else 1)
