#!/usr/bin/env python3
"""CFG646 (ii) propagation: the expulsion ratio P'/P multiplies the framework's measured gravitating P(k, z) at CFG596's
nodes, then cfg596_native.py's own projection, cuts, nuisances and fit give chi2(F') and dchi2' = chi2(F') - chi2(S0).
AN ESTIMATE, NOT A VERDICT (DECLARATIONS.md 3c1c5a42f).  S0 is untouched (the frozen control).
  PM-native ratios (cfg646_expulsion_pm.json, P1 nodes z = 0 / 0.5 / 1) and halo-model ratios (cfg646_expulsion_hm.json, z = 0, held in z).
  Indicative alt cross-check: the same on CFG596's --test530 pipeline (CFG530 L100 N512, held construction, pipeline-check box).
  nice -n 10 python3 cfg646_propagate.py -> cfg646_propagate.out / .json
kappa = 1/2 FITTED; footings never pooled; cold energy mass required; not theory closed."""
import os, sys, json, math, time, copy
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np
from scipy.stats import chi2 as CH
import cfg646_lib as LB
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
T0 = time.time()
PMJ = json.load(open(os.path.join(HERE, "cfg646_expulsion_pm.json")))["sources"]
HMJ = json.load(open(os.path.join(HERE, "cfg646_expulsion_hm.json")))
KHM = np.array(HMJ["k"])
ZK = {0.0: "z0", 0.5: "z0.5", 1.0: "z1"}
def interp_ratio(kq, k, r):
    return np.exp(np.interp(np.log(np.clip(kq, k[0], k[-1])), np.log(k), np.log(np.asarray(r))))
def ratio_fns(src, var):
    """{z: f(k)} for a PM post-process source (held from z = 0 if a node is missing)."""
    nodes = PMJ[src]["nodes"]; out = {}
    for z, key in ZK.items():
        nd = nodes.get(key, nodes["z0"]); k = np.array(nd["k"]); r = np.array(nd["ratio"][var])
        m = k <= 8.04; out[z] = (lambda kq, k=k[m], r=r[m]: interp_ratio(kq, k, r))
    return out
def ratio_hm(foot, from_shape, var):
    r = np.array(HMJ["foot"][foot][from_shape]["R_full"][var]); f = lambda kq: interp_ratio(kq, KHM, r)
    return {z: f for z in ZK}
RES = dict(lane="CFG646", part="ii_propagation", declarations="3c1c5a42f", note="ESTIMATE, not a verdict", runs={})

def score(NS, tag, foot, run, held, variants):
    Pmat, fit, subset, SURV = (NS[k] for k in ("Pmat", "fit", "subset", "SURV"))
    PS0 = Pmat(run, "S0"); PF = Pmat(run, "F")
    out = {}
    for sn, Sv in SURV.items():
        keep = LB.keep_mask(NS, Sv, run, PS0); D = subset(Sv, keep)
        s0 = fit(Sv, D, PS0); f0 = fit(Sv, D, PF)
        o = dict(N=D["N"], chi2_S0=s0["chi2"], chi2_F=f0["chi2"], dchi2=f0["chi2"] - s0["chi2"], p_S0=float(CH.sf(s0["chi2_data"], D["N"])),
                 p_F=float(CH.sf(f0["chi2_data"], D["N"])), variants={})
        P(f"  {tag} {sn}: N {D['N']}; baseline dchi2 {o['dchi2']:+.2f} (chi2 S0 {s0['chi2']:.1f} p {o['p_S0']:.3f}; F {f0['chi2']:.1f} p {o['p_F']:.2e})")
        for vn, fns in variants.items():
            r2 = copy.copy(run); r2["nodes"] = {z: (run["nodes"][z][0] * fns[z](run["k"]), run["nodes"][z][1]) for z in run["nodes"]}
            fv = fit(Sv, D, Pmat(r2, "F")); pv = float(CH.sf(fv["chi2_data"], D["N"]))
            fvn = fit(Sv, D, Pmat(r2, "F"), ia=False); s0n = fit(Sv, D, PS0, ia=False)
            o["variants"][vn] = dict(chi2=fv["chi2"], dchi2=fv["chi2"] - s0["chi2"], p=pv, shift=fv["chi2"] - f0["chi2"], dchi2_noIA=fvn["chi2"] - s0n["chi2"])
            P(f"    {vn:28s} dchi2' {fv['chi2'] - s0['chi2']:+7.2f} (shift {fv['chi2'] - f0['chi2']:+6.2f}; chi2(F') {fv['chi2']:.1f}, p {pv:.2e}; noIA dchi2' {fvn['chi2'] - s0n['chi2']:+.2f})")
        out[sn] = o
    RES["runs"][tag] = out

P("CFG646 (ii) propagation of the census gas expulsion through cfg596_native's projection -- ESTIMATE, not a verdict. kappa = 1/2 FITTED; not theory closed.")
NS = LB.load_ns()
for foot, run, held, extra, B0, F, S in LB.runs(NS):
    if foot != "canonical": continue
    V = {f"PM P1 {v}": ratio_fns("P1", v) for v in ("DIFF-F", "DIFF-S", "DIFF-U", "SHELL")}
    for fs in ("NFW", "MF"):
        for v in ("DIFF", "SHELL", "DIFF_U"):
            V[f"HM {v} from-{fs}"] = ratio_hm("canonical", fs, v)
    score(NS, "CFG596 L100 N1024 canonical", foot, run, held, V)
del NS
NS = LB.load_ns(test530=True)
for foot, run, held, extra, B0, F, S in LB.runs(NS):
    src = "530can" if foot == "canonical" else "530alt"
    V = {f"PM {src} {v}": ratio_fns(src, v) for v in ("DIFF-F", "DIFF-S", "SHELL")}
    V[f"HM DIFF from-NFW ({foot})"] = ratio_hm(foot, "NFW", "DIFF")
    score(NS, f"test530 L100 N512 {foot} (held; pipeline-check box, indicative)", foot, held, held, V)
P(f"\n({time.time() - T0:.0f} s)")
json.dump(RES, open(os.path.join(HERE, "cfg646_propagate.json"), "w"), indent=1)
open(os.path.join(HERE, "cfg646_propagate.out"), "w").write("\n".join(OUT) + "\n")
