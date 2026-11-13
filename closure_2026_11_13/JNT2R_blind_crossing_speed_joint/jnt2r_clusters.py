#!/usr/bin/env python3
"""JNT2R (READING.md, 5abea0324b): X-COP clusters and Lovisari groups under the crossing-speed joint. SRJ1's srj1.py is
executed read-only, from its own path, up to its CHECKS marker (RB1's loaders, statistics and gates; SRJ1's make_system),
as SRJ2 did. A system above v*(z) keeps the reference (make_system at f = 0); a system at or below gets SRJ1's joint at f.
Memberships: P (fold M_b = M200 / (1 + X) against M_b*(z)), M (v500 = sqrt(G M500 / R500) against v*(z)), B (v200 of
RB1's anchored M200 against v*(z)); twins V (v200 > v_stiff), N (none), H / D (v*/2, 2 v*) at f 1.
  python3 jnt2r_clusters.py          -> jnt2r_clusters.json / .out
  python3 jnt2r_clusters.py --twin   -> jnt2r_clusters_MUTATE.json / .out (exits 1)
Adopts nothing. kappa = 1/2 FITTED; not theory closed."""
import os, sys, json, math, io, contextlib, warnings
warnings.filterwarnings("ignore")
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
sys.dont_write_bytecode = True
import numpy as np
TWIN = "--twin" in sys.argv
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE); import jnt2r_common as JC
SRJ = os.path.join(REPO, "closure_2026_11_12", "SRJ1_settled_joint_clusters")
SRC = os.path.join(SRJ, "srj1.py"); code = open(SRC).read()
S = {"__file__": SRC, "__name__": "srj1_lib"}; _a = sys.argv; sys.argv = [SRC]
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(code[:code.index("# ================================================================== CHECKS")], SRC, "exec"), S)
sys.argv = _a
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
VST, FOOTS, run_all, PROF, rho_crit = S["VST"], S["FOOTS"], S["run_all"], S["PROF"], S["rho_crit"]; G, MSUN, KPC = S["G"], S["MS"], S["KPC"]
P(f"JNT2R clusters and groups (READING 5abea0324b){' TWINS (deliberately wrong)' if TWIN else ''}. Adopts nothing. kappa = 1/2 FITTED; not theory closed.")
ORIG = S["make_system"]; MEM = {}
def v500(kind, key, z):
    if kind == "xcop":
        R5 = PROF[key]["R500"]; M5 = 500 * rho_crit(z, 0.7, 0.3) * 4 * math.pi / 3 * R5 ** 3
    else: R5, M5 = key["R5"], key["M5"]
    return math.sqrt(G * M5 * MSUN / (R5 * KPC)) / 1e3
MODE = ["P"]
def make_split(kind, key, a_r, a_Mb, z, foot, f, part="bar", twin=None, fold_mb=None):
    S0 = ORIG(kind, key, a_r, a_Mb, z, foot, 0.0, part, twin, fold_mb); m = MODE[0]
    if m == "N": ab = False
    elif m == "V": ab = S0["v"] > VST[foot]
    elif m == "B": ab = S0["v"] > JC.vstar(foot, z)
    elif m == "M": ab = v500(kind, key, z) > JC.vstar(foot, z)
    else: ab = JC.above(foot, S0["Mb_fold"], z, {"P": 1.0, "H": 0.5, "D": 2.0}[m])
    nm = key if kind == "xcop" else key["name"]
    MEM[(kind, nm)] = dict(above=bool(ab), z=z, v200=S0["v"], vcl=JC.vcl(S0["Mb_fold"], z), v500=v500(kind, key, z), vstar=JC.vstar(foot, z), lMb_fold=math.log10(S0["Mb_fold"]), lMbstar=math.log10(JC.mbstar(foot, z)))
    return S0 if ab else ORIG(kind, key, a_r, a_Mb, z, foot, f, part, twin, fold_mb)
def summ(r): return dict(a_last=[r["a_last"][k] for k in ("median", "lo", "hi")], a_last_label=r["a_last"]["label"], a_R500=[r["a_R500"][k] for k in ("median", "lo", "hi")],
                         a_R500_label=r["a_R500"]["label"], a_last_NFW_label=r["a_last_NFW"]["label"], b_bins=r["b"]["bins"], b_label=r["b"]["label"],
                         c=[r["c"][k] for k in ("median", "lo", "hi")], c_label=r["c"]["label"], c_n_above1=r["c"].get("n_above1"))
RB1J = json.load(open(os.path.join(S["RB1D"], "rb1.json"))); RES = dict(lane="JNT2R", part="clusters and groups" + (" TWINS" if TWIN else ""), reading="5abea0324b", foot={}, note="Adopts nothing. kappa = 1/2 FITTED; not theory closed.")
FG = (0.75, 1.00, 1.25, 1.50, 2.00, 3.00)
RUNS = [(m, 1.0) for m in ("V", "N", "H", "D")] if TWIN else [(m, f) for m in ("P", "M", "B") for f in FG]
for foot in FOOTS:
    R = RES["foot"][foot] = {}
    S["make_system"] = ORIG; r0 = run_all(foot, 0.0); g1 = RB1J["gate1"][foot]; devs = []
    def cmp(mine, ref, keys=("median", "lo", "hi")): devs.extend(abs(mine[k] - ref[k]) for k in keys)
    cmp(r0["a_last"], g1["classes"]["C-X"]); cmp(r0["a_R500"], g1["brackets"]["C-X at R500"]); cmp(r0["c"], g1["classes"]["G-H"])
    devs.extend(abs(r0["a_last"]["per_cluster"][n]["q"] - v["f_ret"]) for n, v in g1["classes"]["C-X"]["per_cluster"].items())
    devs.extend(abs(a - b) for a, b in zip(r0["b"]["bins"], RB1J["gate3"][foot]["main"]["bins"]))
    R["K1"] = dict(max_dev=float(max(devs)), pass_=bool(max(devs) <= 1e-6)); R["reference"] = summ(r0)
    P(f"[{foot}] KA4 SRJ1's K1 (f 0 against rb1.json): max |dev| {max(devs):.1e} -> {'PASS' if R['K1']['pass_'] else 'FAIL'}")
    P(f"[{foot}] reference: (a) {R['reference']['a_last'][0]:.3f} {R['reference']['a_last_label']}, R500 {R['reference']['a_R500'][0]:.3f} {R['reference']['a_R500_label']}; (b) "
      + " / ".join(f"{x:+.3f}" for x in R["reference"]["b_bins"]) + f" {R['reference']['b_label']}; (c) {R['reference']['c'][0]:.3f} {R['reference']['c_label']}")
    S["make_system"] = make_split
    for m, f in RUNS:
        MODE[0] = m; MEM.clear(); rj = run_all(foot, f)
        d = max([abs(rj[k][s] - r0[k][s]) for k in ("a_last", "a_R500", "a_last_NFW", "c") for s in ("median", "lo", "hi")] + [abs(a - b) for a, b in zip(rj["b"]["bins"], r0["b"]["bins"]) if np.isfinite(a)])
        mem = {f"{k[0]}|{k[1]}": v for k, v in MEM.items()}
        nx = [k for k, v in mem.items() if k.startswith("xcop") and not v["above"]]; ng = [k for k, v in mem.items() if k.startswith("group") and not v["above"]]
        R[f"{m}|f{f:.2f}"] = dict(summ(rj), max_diff_from_reference=float(d), xcop_below=nx, groups_below=ng, n_xcop=sum(1 for k in mem if k.startswith("xcop")),
                                 n_groups=sum(1 for k in mem if k.startswith("group")), membership=mem)
        o = R[f"{m}|f{f:.2f}"]
        P(f"[{foot}] {m} f {f:.2f}: below v*: X-COP {len(nx)} / {o['n_xcop']}, groups {len(ng)} / {o['n_groups']}; (a) {o['a_last'][0]:.3f} [{o['a_last'][1]:.3f}, {o['a_last'][2]:.3f}] {o['a_last_label']}, "
          f"R500 {o['a_R500'][0]:.3f} {o['a_R500_label']}; (b) " + " / ".join(f"{x:+.3f}" for x in o["b_bins"]) + f" {o['b_label']}; (c) {o['c'][0]:.3f} [{o['c'][1]:.3f}, {o['c'][2]:.3f}] {o['c_label']}; max |joint - ref| {d:.1e}")
    S["make_system"] = ORIG
    key0 = "V|f1.00" if TWIN else "P|f1.00"; mem = R[key0]["membership"]
    P(f"[{foot}] membership ({key0}): " + "; ".join(f"{k.split('|')[1]} v_cl {v['vcl']:.0f} v200 {v['v200']:.0f} v500 {v['v500']:.0f} v* {v['vstar']:.0f} lMb {v['lMb_fold']:.2f}/{v['lMbstar']:.2f} {'ABOVE' if v['above'] else 'below'}" for k, v in sorted(mem.items())))
    if TWIN:
        R["TWN_reproduces_SRJ1"] = bool(abs(R["N|f1.00"]["b_bins"][0] - {"canonical": 0.153, "alt": 0.144}[foot]) <= 0.002 and R["N|f1.00"]["b_label"] == "FAILS")
        R["TWV_reproduces_SRJ2"] = bool(R["V|f1.00"]["max_diff_from_reference"] == 0.0)
        P(f"[{foot}] TW-N reproduces SRJ1's X-COP shape fail (first bin {R['N|f1.00']['b_bins'][0]:+.3f}): {R['TWN_reproduces_SRJ1']}; TW-V equals the reference (SRJ2): {R['TWV_reproduces_SRJ2']}")
tag = "_MUTATE" if TWIN else ""
json.dump(RES, open(os.path.join(HERE, f"jnt2r_clusters{tag}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"jnt2r_clusters{tag}.out"), "w").write("\n".join(OUT) + "\nAdopts nothing. kappa = 1/2 FITTED; not theory closed.\n")
sys.exit(1 if TWIN else 0)
