#!/usr/bin/env python3
"""X79_native_eta_mw_kids, part MW (criteria c7d5c7f1c1): GD3's stage-M Milky Way box (read-only, exec'd from its own
text) with route E's rule Sigma = max(Sigma_a0, eta_native(M200) Sigma_coll(M200)) in place of OS1's sigma law.
    X79_ETA=native|const|os1 [X79_ETAMULT=2] PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x79_mw.py
os1 = K1 identity (GD3's q_fS); const = eta 10.82 (c_f 4, reported); native = graded. kappa = 1/2 FITTED; not theory closed."""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ[_v] = "1"
import sys, json, math
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE)
MODE = os.environ.get("X79_ETA", "native"); MULT = float(os.environ.get("X79_ETAMULT", "1"))
GSRC = os.path.join(REB, "GD3_smooth_core_mw", "gd3_smooth_core_mw.py"); T = open(GSRC).read()
head = T[:T.index("checks = []")]
seg = T[T.index("# ================================================================== stage M"):T.index("# K2: Burkert + OS1 q_f reproduces GD2")]
old = '    Sig = SIG_A0[foot] * (vlast / math.sqrt(2) / SREF) ** q\n    lM = bg["a"] + bg["b"] * (math.log10(bar["Mb"]) - 10); M200 = 10 ** lM\n'
assert seg.count(old) == 1
seg = seg.replace(old, '    lM = bg["a"] + bg["b"] * (math.log10(bar["Mb"]) - 10); M200 = 10 ** lM\n    Sig = SIGRULE(foot, vlast, q, M200)\n')
NS = {"__file__": GSRC, "__name__": "gd3_ro"}
exec(compile(head, GSRC, "exec"), NS)
NS["REB"] = REB
# rule pieces
X43J = json.load(open(os.path.join(REB, "X43_collapse_core_floor", "x43_collapse_core_results.json")))
SCT = sorted((math.log10(float(k)), math.log10(v[0])) for k, v in X43J["sigma_coll_table"].items())
SC_LM, SC_LS = np.array([a for a, _ in SCT]), np.array([b for _, b in SCT])
def sigma_coll(M):                                   # X53's interpolation of X43's table (Msun/pc^2)
    l = math.log10(M)
    if l < SC_LM[0]:
        s = (SC_LS[1] - SC_LS[0]) / (SC_LM[1] - SC_LM[0]); return 10 ** (SC_LS[0] + s * (l - SC_LM[0]))
    if l > SC_LM[-1]:
        s = (SC_LS[-1] - SC_LS[-2]) / (SC_LM[-1] - SC_LM[-2]); return 10 ** (SC_LS[-1] + s * (l - SC_LM[-1]))
    return 10 ** float(np.interp(l, SC_LM, SC_LS))
S77 = json.load(open(os.path.join(REB, "X77_direct_core_surface_density", "x77_results.json")))["summary"]
EL = np.array([12.0, 13.0, 14.0]); EV = np.array([S77["1e+12_ng64"]["eta_med"], S77["1e+13_ng48"]["eta_med"], S77["1e+14_ng48"]["eta_med"]])
def eta_of(M): return MULT * (float(np.interp(math.log10(M), EL, EV)) if MODE == "native" else 4.0 / (3.0 * 0.6970726) * 4.0 ** 1.25)
GD3J = json.load(open(os.path.join(REB, "GD3_smooth_core_mw", "gd3_smooth_core_mw_results.json")))
QS = {f: GD3J["stageS"][f]["q_fS"] for f in ("canonical", "alt")}
STATE = {}
def SIGRULE(foot, vlast, q, M200):
    if MODE == "os1": return NS["SIG_A0"][foot] * (vlast / math.sqrt(2) / NS["SREF"]) ** q
    sc = eta_of(M200) * sigma_coll(M200) * 1e6           # Msun/kpc^2
    STATE[(foot, round(math.log10(M200), 3))] = sc > NS["SIG_A0"][foot]
    return max(NS["SIG_A0"][foot], sc)
NS["SIGRULE"] = SIGRULE
exec(compile(seg, GSRC + "[stage M]", "exec"), NS)
qd = QS if MODE == "os1" else {f: 0.0 for f in ("canonical", "alt")}
box, k3 = NS["run_box"]("smooth", qd, MODE)
P = NS["P"]; RES = dict(mode=MODE, mult=MULT, eta_table=dict(zip(["1e12", "1e13", "1e14"], EV.tolist())), graded={}, mcmillan={})
if MODE == "os1":
    d = max(abs(box[k]["best"]["D"] - GD3J["stageM"]["graded"][k]["best"]["D"]) for k in box)
    same = all(box[k]["cls"] == GD3J["stageM"]["graded"][k]["cls"] for k in box)
    P(f"K1 identity vs GD3 (all keys): classes same {same}, best D max |d| {d:.1e}: {'PASS' if same and d <= 1e-9 else 'FAIL'}")
    RES["K1"] = dict(same=same, max_d=d, ok=bool(same and d <= 1e-9))
GATE = {"canonical": True, "alt": False}                   # X77 full grade SPARC line
for foot in ("canonical", "alt"):
    k = f"{foot}|PRIMARY|A_c2b_refit"; c = box[k]; b = c["best"]; ip = c["best_in_prior"]
    lab = c["cls"] if GATE[foot] or MODE == "os1" else f"SPARC LINE FAILS (MW reported: {c['cls']})"
    RES["graded"][foot] = dict(c, label=lab)
    P(f"[{MODE} x{MULT:g}] {foot}: CLASS {lab}; Sig/Sig_a0 {c['Sig_ratio']:.3f}; cells all-4 {c['n_all']} (R_d {c['passing_Rd']}), V+K {c['n_VK']}")
    P(f"     best D {b['D']:.2f} at R_d {b['R_d']:.3f}: vc {b['vc_R0']:.1f}, Kz {b['K_R0']:.1f}, chi2_Kz {b['chi2_Kz']:.1f}, chi2_Ou {b['chi2_Ou']:.0f}")
    if ip: P(f"     best in-prior D {ip['D']:.2f} at R_d {ip['R_d']:.3f}, M* {ip['Mstar']:.3g}: vc {ip['vc_R0']:.1f}, Kz {ip['K_R0']:.1f}, chi2_Ou {ip['chi2_Ou']:.0f}")
    r = NS["grade"](NS["MCM"], foot, 172.98, NS["BGS"]["A_c2b_refit"], qd[foot], NS["B_smooth"]); RES["mcmillan"][foot] = r
    P(f"     McMillan: lgM200 {r['lgM200']:.2f}, Sig/Sig_a0 {r['Sig_ratio']:.3f}, vc {r['vc_R0']:.1f} (Eilers {NS['vE']:.1f} +- {NS['eE']:.1f}), Kz {r['K_R0']:.1f}, chi2_Ou {r['chi2_Ou']:.0f}")
RES["collapse_branch_active_frac"] = {f: float(np.mean([v for (ff, _), v in STATE.items() if ff == f])) if STATE else None for f in ("canonical", "alt")}
tag = f"_{MODE}" + ("" if MULT == 1 else f"x{MULT:g}")
json.dump(RES, open(os.path.join(HERE, f"x79_mw_results{tag}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"x79_mw{tag}.out"), "w").write("\n".join(NS["OUT"]) + "\n")
