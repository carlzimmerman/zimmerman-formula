#!/usr/bin/env python3
"""OS1_core_law_out_of_sample -- frozen criteria FROZEN_CRITERIA.md (71873e76d3).

Calibrate q once on SPARC (bg A rms) per footing, then grade X38's cluster cells and CD1's dwarfs at q_f.
SC1's machinery (X38 + EM1 + X30, read-only) is executed in a namespace up to SC1's checks.
    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 os1_out_of_sample.py            -> .out, _results.json
    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 os1_out_of_sample.py --mutate   -> SPARC sigma permuted
"""
import os, sys, io, csv, json, math, time, contextlib, resource
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
import numpy as np

T0 = time.time()
MUTATE = "--mutate" in sys.argv
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE)
TAG = "_MUTATE" if MUTATE else ""
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
def rss(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1e9 if sys.platform == "darwin" else 1e6)

SC1SRC = os.path.join(REB, "SC1_self_coupled_core_law", "sc1_core_law.py"); TS = open(SC1SRC).read()
code = TS[:TS.index('checks = [("K1", k1)]')]
code = code.replace('os.path.join(HERE, "sc1_x30_machinery.log")', repr(os.path.join(HERE, "os1_x30_machinery.log")))
NS = {"__file__": SC1SRC, "__name__": "sc1_ro"}; argv0 = sys.argv; sys.argv = [SC1SRC]
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(code, SC1SRC, "exec"), NS)
sys.argv = argv0
sparc, grade, BGS, line, FEET, HK, SREF = (NS[k] for k in ("sparc", "grade", "BGS", "line", "FEET", "HK", "SREF"))
X38J = json.load(open(os.path.join(REB, "X38_a0_surface_density_halos", "x38_sd_halos_results.json")))
SC1J = json.load(open(os.path.join(REB, "SC1_self_coupled_core_law", "sc1_core_law_results.json")))
P(f"OS1_core_law_out_of_sample {'MUTATE (SPARC sigma permuted)' if MUTATE else 'normal run'}  (frozen 71873e76d3)")
P(f"kappa = 1/2 FITTED; footings never pooled; cold dark energy, not matter; not theory closed; sigma_ref {SREF:.2f} km/s")
if MUTATE:
    rng = np.random.default_rng(20261025); NS["SIG_G"] = rng.permutation(NS["SIG_G"])

# ---- dwarfs (CD1 rule, per-dwarf Sigma)
G_, MSUN, PC = 6.674e-11, 1.989e30, 3.0857e16
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}; CAP = 0.254484
X1 = list(csv.DictReader(open(os.path.join(REB, "X1_hosted_recount", "x1_per_system.csv"))))
def dwarfs(foot, q):
    R = [r for r in X1 if r["footing"] == foot]; out = []
    for r in R:
        r12 = 4 / 3 * float(r["rh_pc"]) * PC; gN = G_ * (10 ** float(r["logMstar"]) * MSUN / 2) / r12 ** 2
        D, sd = float(r["Delta[Newton]"]), float(r["sdMC[Newton]"]); gobs = gN * 10 ** D
        sig = math.sqrt(gobs * r12 / 3) / 1e3
        cap = CAP * A0[foot] * (sig / SREF) ** q
        if D <= 0: out.append(dict(name=r["name"], cls=r["cls"], S=0.0, z=-np.inf, graded=True)); continue
        ratio = 10 ** D - 1
        if ratio < 0.1: out.append(dict(name=r["name"], cls=r["cls"], S=np.nan, z=np.nan, graded=False)); continue
        gh = gobs - gN; sdh = sd * 10 ** D / ratio
        out.append(dict(name=r["name"], cls=r["cls"], S=gh / cap, z=(math.log10(gh) - math.log10(cap)) / sdh, graded=True, sig=sig))
    g = [o for o in out if o["graded"]]
    fex = float(np.mean([o["z"] >= 2 for o in g])); medS = float(np.median([o["S"] for o in g]))
    cls = "EXCLUDE" if fex >= 0.25 else ("CONSISTENT" if fex < 0.05 and medS <= 1 else "PARTIAL")
    return cls, fex, medS, out

checks = []; RES = dict(frozen="71873e76d3", mutate=MUTATE, footings={}); classes = {}
for foot in FEET:
    bgA = BGS["A_c2b_refit"]; x38 = X38J["footings"][foot]
    if not MUTATE:
        s0 = sparc(foot, bgA["a"], bgA["b"], bgA["h"], 0.0); c0, _ = grade(foot, 0.0); d0c, d0f, d0m, _ = dwarfs(foot, 0.0)
        k0 = (abs(s0["rms"] - x38["sparc"]["A_c2b_refit"]["rms"]) < 1e-9
              and max(abs(c0["h0672"][k]["pred"] - x38["clusters"]["cells"]["h0672"][k]["pred"]) for k in c0["h0672"]) < 1e-6
              and abs(d0f - 0.011) < 0.005 and abs(d0m - {"canonical": 0.53, "alt": 0.44}[foot]) < 0.005)
        s13 = sparc(foot, bgA["a"], bgA["b"], bgA["h"], 1 / 3)
        k1 = abs(s13["rms"] - SC1J["footings"][foot]["sparc"]["A_c2b_refit"]["rms"]) < 5e-5
        P(f"\n=== [{foot}] K0 (q=0 = X38 + CD1: SPARC {s0['rms']:.4f}, dwarfs frac {d0f:.3f} med S {d0m:.3f}): {'PASS' if k0 else 'FAIL'}; "
          f"K1 (q=1/3 SPARC {s13['rms']:.4f} = SC1): {'PASS' if k1 else 'FAIL'}")
        checks += [(f"K0[{foot}]", k0), (f"K1[{foot}]", k1)]
    # calibration
    cache = {}
    def rms(q):
        if q not in cache: cache[q] = sparc(foot, bgA["a"], bgA["b"], bgA["h"], q)
        return cache[q]["rms"]
    coarse = [round(0.02 * i, 3) for i in range(61)]
    qc = min(coarse, key=rms)
    fine = sorted({round(qc + 0.002 * j, 4) for j in range(-10, 11) if 0 <= qc + 0.002 * j <= 1.2})
    qf = min(fine, key=rms); stf = cache[qf]; r0 = rms(0.0)
    P(f"   [{foot}] calibration: coarse min q {qc:.2f}; q_f = {qf:.3f}; SPARC A rms {stf['rms']:.4f} @ U {stf['U_median']:.2f} "
      f"(q=0: {r0:.4f}); line {'PASS' if line(stf) else 'FAIL'}   [{time.time() - T0:.0f} s]")
    curve = {q: cache[q]["rms"] for q in coarse}
    if MUTATE:
        RES["footings"][foot] = dict(q_f=qf, gain=r0 - stf["rms"]); continue
    if not line(stf):
        P(f"   STOP [{foot}]: SPARC line fails at q_f (frozen: stop)"); classes[foot] = "STOPPED"; continue
    sB = sparc(foot, BGS["B_cfg886_bg"]["a"], BGS["B_cfg886_bg"]["b"], BGS["B_cfg886_bg"]["h"], qf)
    P(f"   bg B at q_f: rms {sB['rms']:.4f} @ U {sB['U_median']:.2f} ({'PASS' if line(sB) else 'FAIL'})")
    # clusters
    cells, ok = grade(foot, qf); x38c = x38["clusters"]["cells"]; x38ok = x38["clusters"]["ok"]
    failing38 = [k for k in x38ok if not x38ok[k]]
    sZ38 = sum(max(abs(x38c[h][k]["Z"]) for h in HK) for k in failing38)
    sZ = sum(max(abs(cells[h][k]["Z"]) for h in HK) for k in failing38)
    newfail = [k for k in ok if x38ok.get(k, True) and not ok[k]]
    ccls = "PASS" if all(ok.values()) else ("IMPROVE" if not newfail and sZ <= 0.5 * sZ38 else "FAIL")
    for k in cells["h0672"]:
        a = cells["h0672"][k]; P(f"     {k:10s} meas {a['meas']:+.3f}+-{a['s']:.3f} pred {a['pred']:+.3f} Z {a['Z']:+.2f}" + ("" if ok[k] else "  FAIL"))
    P(f"   clusters at q_f: {ccls} (failing |Z| {sZ38:.2f} -> {sZ:.2f}; new fails {newfail or 'none'})")
    # dwarfs
    dcls, fex, medS, drows = dwarfs(foot, qf)
    bycls = {}
    for o in drows:
        if o["graded"]: bycls.setdefault(o["cls"], []).append(o)
    P(f"   dwarfs at q_f: {dcls} (frac z>=2 {fex:.3f}, median S {medS:.2f})")
    for k, v in sorted(bycls.items()):
        P(f"     {k:24s} n {len(v):3d} frac z>=2 {np.mean([o['z'] >= 2 for o in v]):.2f} median S {np.median([o['S'] for o in v]):.2f}")
    qx = next((q for q in [round(0.01 * i, 2) for i in range(121)] if dwarfs(foot, q)[0] == "EXCLUDE"), None)
    qc_ = next((q for q in [round(0.01 * i, 2) for i in range(121)] if dwarfs(foot, q)[0] != "CONSISTENT"), None)
    P(f"   (reported) dwarfs leave CONSISTENT at q = {qc_}; reach EXCLUDE at q = {qx}")
    near = {}
    for dq in (-0.05, 0.05):
        cv, okv = grade(foot, qf + dq); near[f"{qf + dq:.3f}"] = [k for k in okv if not okv[k]]
    P(f"   (reported) cluster fails at q_f -/+ 0.05: {near}")
    if ccls == "PASS" and dcls == "CONSISTENT": lc = "OS PASSES"
    elif ccls == "PASS": lc = "OS CLUSTERS PASS, DWARFS FAIL"
    elif dcls == "CONSISTENT": lc = "OS DWARFS HOLD, CLUSTERS SHORT"
    elif ccls == "FAIL" and dcls == "EXCLUDE": lc = "OS FAILS OUT OF SAMPLE"
    else: lc = "OS MIXED"
    classes[foot] = lc
    P(f"   CLASS [{foot}]: {lc}   [{time.time() - T0:.0f} s, RSS {rss():.2f} GB]")
    RES["footings"][foot] = dict(q_f=qf, sparc_A=dict(rms=stf["rms"], U=stf["U_median"]), sparc_B=dict(rms=sB["rms"], U=sB["U_median"]),
                                 rms_curve=curve, clusters=dict(cls=ccls, cells=cells, ok=ok, sumZ_x38=sZ38, sumZ=sZ, new_fail=newfail, near=near),
                                 dwarfs=dict(cls=dcls, frac=fex, medS=medS, q_leave_consistent=qc_, q_exclude=qx, rows=drows), cls=lc)

if MUTATE:
    real = json.load(open(os.path.join(HERE, "os1_out_of_sample_results.json")))
    for foot in FEET:
        rg = real["footings"][foot]["rms_curve"]["0.0"] - real["footings"][foot]["sparc_A"]["rms"]
        mg = RES["footings"][foot]["gain"]; okm = mg < rg / 3
        P(f"[{foot}] MUTATE: permuted-sigma q_f {RES['footings'][foot]['q_f']:.3f}, gain {mg:.4f} vs real gain {rg:.4f}: "
          f"{'gain killed' if okm else 'gain SURVIVES'}"); checks.append((f"MUT[{foot}]", okm))
else:
    RES["verdict"] = classes["canonical"] if classes["canonical"] == classes["alt"] else f"UNDECIDED (footings disagree: {classes})"
    P(f"\n=== VERDICT: {RES['verdict']}")
checks.append(("K2", rss() < 2.0))
n = sum(v for _, v in checks); P(f"\nchecks {n}/{len(checks)}: " + ", ".join(f"{k} {'PASS' if v else 'FAIL'}" for k, v in checks)
                                + f"; runtime {time.time() - T0:.0f} s; peak RSS {rss():.2f} GB")
RES["checks"] = {k: bool(v) for k, v in checks}
open(os.path.join(HERE, f"os1_out_of_sample{TAG}.out"), "w").write("\n".join(OUT) + "\n")
json.dump(RES, open(os.path.join(HERE, f"os1_out_of_sample_results{TAG}.json"), "w"), indent=1, default=float)
if MUTATE: sys.exit(1 if n == len(checks) else 0)
sys.exit(0 if n == len(checks) else 1)
