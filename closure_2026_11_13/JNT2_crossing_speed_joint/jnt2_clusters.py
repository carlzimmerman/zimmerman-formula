#!/usr/bin/env python3
"""JNT2 (FROZEN_CRITERIA.md, e186b314ef): X-COP and Lovisari groups under the crossing-speed joint. SRJ2's srj2_clusters.py
content copied (cited): SRJ1's srj1.py is executed read-only from its own path up to its CHECKS marker (RB1's loaders,
statistics and gates; SRJ1's make_system and run_all). A system above the boundary keeps the reference (f = 0); a system at
or below it gets SRJ1's joint at f.
  Primary (model) rule: make_system's v200 (RB1's anchored M200 at 200 rho_crit(z)) against v*(z) of the mode.
  Secondary (measured) rule: X-COP sqrt(G M_dyn(r_last) / r_last), groups sqrt(G M500 / R500), against v*(z).
  Mode S: v200 against v_stiff (TW-S); mode 0: no boundary (TW-0); H / D: v*/2, 2 v*.
  python3 jnt2_clusters.py [--mode main|S|0|H|D] -> jnt2_clusters[_MUTATE_<mode>].json / .out
Adopts nothing. kappa = 1/2 FITTED; not theory closed."""
import os, sys, json, math, io, contextlib, warnings
warnings.filterwarnings("ignore")
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
sys.dont_write_bytecode = True
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE); import jnt2_common as C
MODE = sys.argv[sys.argv.index("--mode") + 1] if "--mode" in sys.argv else "main"; assert MODE in C.MODES
SRJ = os.path.join(REPO, "closure_2026_11_12", "SRJ1_settled_joint_clusters")
SRC = os.path.join(SRJ, "srj1.py"); code = open(SRC).read()
S = {"__file__": SRC, "__name__": "srj1_lib"}; _a = sys.argv; sys.argv = [SRC]
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(code[:code.index("# ================================================================== CHECKS")], SRC, "exec"), S)
sys.argv = _a
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
FOOTS, run_all = S["FOOTS"], S["run_all"]; assert S["VST"] == C.VSTIFF
Gs, MSs, KPCs = S["G"], S["MS"], S["KPC"]
P(f"JNT2 clusters and groups, mode {MODE} (criteria e186b314ef). Adopts nothing. kappa = 1/2 FITTED; not theory closed.")
# measured speeds
VMX = {p["name"]: (math.sqrt(Gs * p["M_dyn"] * MSs / (p["r_kpc"] * KPCs)) / 1e3, PZ) for p in S["xcop_last"](S["WITH"], "last") for PZ in [S["PROF"][p["name"]]["z"]]}
VMG = {g["name"]: (math.sqrt(Gs * g["M5"] * MSs / (g["R5"] * KPCs)) / 1e3, g["z"]) for g in S["LOV"]}
def bnd(foot, z): return C.vstar_kms(foot, z, MODE)
ORIG = S["make_system"]; LOW = []; RULE = ["model"]
def make_split(kind, key, a_r, a_Mb, z, foot, f, part="bar", twin=None, fold_mb=None):
    S0 = ORIG(kind, key, a_r, a_Mb, z, foot, 0.0, part, twin, fold_mb)
    nm = key if kind == "xcop" else key["name"]
    if RULE[0] == "model": hi = S0["v"] > bnd(foot, z)
    else: hi = (VMX[nm][0] if kind == "xcop" else VMG[nm][0]) > bnd(foot, z)
    if hi: return S0
    LOW.append((kind, nm, round(S0["v"], 1)))
    return ORIG(kind, key, a_r, a_Mb, z, foot, f, part, twin, fold_mb)
RB1J = json.load(open(os.path.join(S["RB1D"], "rb1.json")))
RES = dict(lane="JNT2", part="clusters and groups", mode=MODE, criteria="e186b314ef", foot={}, note="Adopts nothing. kappa = 1/2 FITTED; not theory closed.")
def summ(r): return dict(labels=dict(a_last=r["a_last"]["label"], a_R500=r["a_R500"]["label"], a_last_NFW=r["a_last_NFW"]["label"], b=r["b"]["label"], c=r["c"]["label"]),
                         a_last=[r["a_last"][k] for k in ("median", "lo", "hi")], a_R500=[r["a_R500"][k] for k in ("median", "lo", "hi")], b_bins=r["b"]["bins"], c=[r["c"][k] for k in ("median", "lo", "hi")])
FS = {"main": (0.75, 1.0, 1.25, 1.5, 2.0, 3.0), "S": (1.0,), "0": (1.0,), "H": (1.25, 2.0), "D": (1.25, 2.0)}[MODE]
for foot in FOOTS:
    R = RES["foot"][foot] = {}
    S["make_system"] = ORIG; r0 = run_all(foot, 0.0); g1 = RB1J["gate1"][foot]
    dev = max([abs(r0["a_last"][k] - g1["classes"]["C-X"][k]) for k in ("median", "lo", "hi")] + [abs(a - b) for a, b in zip(r0["b"]["bins"], RB1J["gate3"][foot]["main"]["bins"])]
              + [abs(r0["c"][k] - g1["classes"]["G-H"][k]) for k in ("median", "lo", "hi")])
    R["KA0"] = dict(max_dev=float(dev), pass_=bool(dev <= 1e-6)); R["reference"] = summ(r0)
    vx = {n: (v["v200"], v["z"]) for n, v in r0["a_last"]["per_cluster"].items()}; vg = {n: v["v200"] for n, v in r0["c"]["per_group"].items()}
    gz = {g["name"]: g["z"] for g in S["LOV"]}
    R["membership"] = dict(
        xcop={n: dict(z=z, v200=v, vmeas=VMX[n][0], vstar=bnd(foot, z), above_model=bool(v > bnd(foot, z)), above_measured=bool(VMX[n][0] > bnd(foot, z))) for n, (v, z) in vx.items()},
        groups={n: dict(z=gz[n], v200=v, vmeas=VMG[n][0], vstar=bnd(foot, gz[n]), above_model=bool(v > bnd(foot, gz[n])), above_measured=bool(VMG[n][0] > bnd(foot, gz[n]))) for n, v in vg.items()})
    mx, mg = R["membership"]["xcop"], R["membership"]["groups"]
    P(f"[{foot}] KA-0 reference against rb1.json: {dev:.1e} -> {'PASS' if R['KA0']['pass_'] else 'FAIL'}")
    P(f"[{foot}] X-COP above (model / measured): {sum(v['above_model'] for v in mx.values())} / {sum(v['above_measured'] for v in mx.values())} of {len(mx)}; v200 {min(v['v200'] for v in mx.values()):.0f}-{max(v['v200'] for v in mx.values()):.0f}, measured {min(v['vmeas'] for v in mx.values()):.0f}-{max(v['vmeas'] for v in mx.values()):.0f}, boundary {min(v['vstar'] for v in mx.values()):.0f}-{max(v['vstar'] for v in mx.values()):.0f} km/s")
    P(f"[{foot}] groups above (model / measured): {sum(v['above_model'] for v in mg.values())} / {sum(v['above_measured'] for v in mg.values())} of {len(mg)}; v200 {min(v['v200'] for v in mg.values()):.0f}-{max(v['v200'] for v in mg.values()):.0f}, measured {min(v['vmeas'] for v in mg.values()):.0f}-{max(v['vmeas'] for v in mg.values()):.0f}, boundary {min(v['vstar'] for v in mg.values()):.0f}-{max(v['vstar'] for v in mg.values()):.0f} km/s")
    S["make_system"] = make_split
    for rule in (("model", "measured") if MODE == "main" else ("model",)):
        RULE[0] = rule
        for f in FS:
            LOW.clear(); rj = run_all(foot, f); sj = summ(rj)
            d = max([abs(a - b) for k in ("a_last", "a_R500", "c") for a, b in zip(sj[k], R["reference"][k])] + [abs(a - b) for a, b in zip(sj["b_bins"], R["reference"]["b_bins"]) if np.isfinite(a)])
            low = sorted(set(LOW)); sj.update(max_diff_from_reference=float(d), n_xcop_law=len({x[1] for x in low if x[0] == "xcop"}), n_groups_law=len({x[1] for x in low if x[0] == "group"}))
            R[f"{rule}_f{f:.2f}"] = sj
            P(f"[{foot}] {rule:8s} f {f:.2f}: {sj['labels']}; q r_last {sj['a_last'][0]:.3f}; R500 {sj['a_R500'][0]:.3f} [{sj['a_R500'][1]:.3f}, {sj['a_R500'][2]:.3f}]; shape " + " / ".join(f"{x:+.3f}" for x in sj["b_bins"])
              + f"; groups q {sj['c'][0]:.3f} [{sj['c'][1]:.3f}, {sj['c'][2]:.3f}]; law given to X-COP {sj['n_xcop_law']}, groups {sj['n_groups_law']}; max |joint - ref| {d:.1e}")
    S["make_system"] = ORIG
tag = "" if MODE == "main" else f"_MUTATE_{MODE}"
json.dump(RES, open(os.path.join(HERE, f"jnt2_clusters{tag}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"jnt2_clusters{tag}.out"), "w").write("\n".join(OUT) + "\nAdopts nothing. kappa = 1/2 FITTED; not theory closed.\n")
