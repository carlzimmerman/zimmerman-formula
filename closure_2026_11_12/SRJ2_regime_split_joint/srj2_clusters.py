#!/usr/bin/env python3
"""SRJ2 (FROZEN_CRITERIA.md, b8a99499ad): clusters and groups under the regime-split settled joint. SRJ1's srj1.py is executed
read-only, from its own path, up to its CHECKS marker (RB1's loaders, statistics and gates, copied there; SRJ1's make_system).
Each system's v200 = sqrt(G M200 / R200) (RB1's anchored M200 at 200 rho_crit(z); FRZ1's v_vir definition) is read from
make_system; systems with v200 > VST keep the reference (f = 0); any system with v200 <= VST gets SRJ1's joint at f.
  C5: SRJ1's K1 (f = 0 against rb1.json) re-run here.
  python3 srj2_clusters.py -> srj2_clusters.json / .out
Adopts nothing. kappa = 1/2 FITTED; not theory closed."""
import os, sys, json, math, io, contextlib
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
sys.dont_write_bytecode = True
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
SRJ = os.path.join(REPO, "closure_2026_11_12", "SRJ1_settled_joint_clusters")
SRC = os.path.join(SRJ, "srj1.py"); code = open(SRC).read()
S = {"__file__": SRC, "__name__": "srj1_lib"}; _a = sys.argv; sys.argv = [SRC]
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(code[:code.index("# ================================================================== CHECKS")], SRC, "exec"), S)
sys.argv = _a
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
VST, FOOTS, run_all = S["VST"], S["FOOTS"], S["run_all"]; assert VST == {"canonical": 265.8, "alt": 288.1}
P("SRJ2 clusters and groups (criteria b8a99499ad). Adopts nothing. kappa = 1/2 FITTED; not theory closed.")
ORIG = S["make_system"]; LOW = []
def make_split(kind, key, a_r, a_Mb, z, foot, f, part="bar", twin=None, fold_mb=None):
    S0 = ORIG(kind, key, a_r, a_Mb, z, foot, 0.0, part, twin, fold_mb)
    if S0["v"] > VST[foot]: return S0
    LOW.append((kind, key if kind == "xcop" else key["name"], S0["v"]))
    return ORIG(kind, key, a_r, a_Mb, z, foot, f, part, twin, fold_mb)
RB1J = json.load(open(os.path.join(S["RB1D"], "rb1.json"))); RES = dict(lane="SRJ2", part="clusters and groups", criteria="b8a99499ad", foot={}, note="Adopts nothing. kappa = 1/2 FITTED; not theory closed.")
def lab(r): return dict(a_last=r["a_last"]["label"], a_R500=r["a_R500"]["label"], a_last_NFW=r["a_last_NFW"]["label"], b=r["b"]["label"], c=r["c"]["label"])
for foot in FOOTS:
    R = RES["foot"][foot] = {}
    S["make_system"] = ORIG; r0 = run_all(foot, 0.0); g1 = RB1J["gate1"][foot]; devs = []
    def cmp(mine, ref, keys=("median", "lo", "hi")): devs.extend(abs(mine[k] - ref[k]) for k in keys)
    cmp(r0["a_last"], g1["classes"]["C-X"]); cmp(r0["a_R500"], g1["brackets"]["C-X at R500"]); cmp(r0["c"], g1["classes"]["G-H"])
    devs.extend(abs(r0["a_last"]["per_cluster"][n]["q"] - v["f_ret"]) for n, v in g1["classes"]["C-X"]["per_cluster"].items())
    devs.extend(abs(a - b) for a, b in zip(r0["b"]["bins"], RB1J["gate3"][foot]["main"]["bins"]))
    R["C5"] = dict(max_dev=float(max(devs)), pass_=bool(max(devs) <= 1e-6))
    vx = {n: v["v200"] for n, v in r0["a_last"]["per_cluster"].items()}; vx5 = {n: v["v200"] for n, v in r0["a_R500"]["per_cluster"].items()}; vg = {n: v["v200"] for n, v in r0["c"]["per_group"].items()}
    R["v200"] = dict(xcop_last=vx, xcop_R500=vx5, groups=vg)
    R["n_below"] = dict(xcop=int(sum(v <= VST[foot] for v in list(vx.values()) + list(vx5.values()))), groups=int(sum(v <= VST[foot] for v in vg.values())))
    P(f"[{foot}] C5 (SRJ1's K1) reference against rb1.json: max |dev| {max(devs):.1e} -> {'PASS' if R['C5']['pass_'] else 'FAIL'}")
    P(f"[{foot}] X-COP v200 (anchor r_last) km/s: " + ", ".join(f"{n} {v:.0f}" for n, v in sorted(vx.items())) + f"; min at R500 anchor {min(vx5.values()):.0f}")
    P(f"[{foot}] groups v200 km/s: min {min(vg.values()):.0f}, median {np.median(list(vg.values())):.0f}, max {max(vg.values()):.0f}; at or below v_stiff {VST[foot]}: X-COP {R['n_below']['xcop']}, groups {R['n_below']['groups']}")
    R["reference"] = dict(labels=lab(r0), a_last=[r0["a_last"][k] for k in ("median", "lo", "hi")], a_R500=[r0["a_R500"][k] for k in ("median", "lo", "hi")],
                          a_last_NFW=[r0["a_last_NFW"][k] for k in ("median", "lo", "hi")], b_bins=r0["b"]["bins"], c=[r0["c"][k] for k in ("median", "lo", "hi")])
    P(f"[{foot}] reference: (a) q at r_last {R['reference']['a_last'][0]:.3f} [{R['reference']['a_last'][1]:.3f}, {R['reference']['a_last'][2]:.3f}] {r0['a_last']['label']}; "
      f"R500 bracket {R['reference']['a_R500'][0]:.3f} [{R['reference']['a_R500'][1]:.3f}, {R['reference']['a_R500'][2]:.3f}] {r0['a_R500']['label']}; M_NFW bracket {r0['a_last_NFW']['label']}; "
      f"(b) shape bins " + " / ".join(f"{x:+.3f}" for x in r0["b"]["bins"]) + f" {r0['b']['label']}; (c) groups {R['reference']['c'][0]:.3f} [{R['reference']['c'][1]:.3f}, {R['reference']['c'][2]:.3f}] {r0['c']['label']}")
    S["make_system"] = make_split
    for f in (0.75, 1.0, 1.25):
        LOW.clear(); rj = run_all(foot, f)
        d = max([abs(rj[k][s] - r0[k][s]) for k in ("a_last", "a_R500", "a_last_NFW", "c") for s in ("median", "lo", "hi")] + [abs(a - b) for a, b in zip(rj["b"]["bins"], r0["b"]["bins"]) if np.isfinite(a)])
        R[f"joint_f{f:.2f}"] = dict(labels=lab(rj), max_diff_from_reference=float(d), systems_given_the_law=sorted(set(LOW)))
        P(f"[{foot}] joint f {f:.2f}: labels {lab(rj)}; max |joint - reference| over all gate statistics {d:.1e}; systems given the law's layout: {sorted(set(LOW))}")
    S["make_system"] = ORIG
json.dump(RES, open(os.path.join(HERE, "srj2_clusters.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, "srj2_clusters.out"), "w").write("\n".join(OUT) + "\nAdopts nothing. kappa = 1/2 FITTED; not theory closed.\n")
