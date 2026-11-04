#!/usr/bin/env python3
"""WG3 grader (FROZEN_CRITERIA.md bb3410083d, Amendment A1 ba8477ae8e): K4b on the T1 reference run, projection and PR4 grading
copied unchanged from WG2's wg2_grade.py lines 21-83 (WG2's grader runs on import, so it is copied, not imported), the T1 label over
its four members, T1T0 and T1V reported, K5, and the switch's ON fractions. WG2's R0 and R1-TIE are read from its results for context.
Run: python3 wg3_grade.py [--mutate]. kappa = 1/2 FITTED; the cold sector stays retired; not theory closed."""
import os, sys, json, math, glob
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np
from scipy.stats import chi2 as CHI2
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE); REPO = os.path.dirname(REB); RUNS = os.path.join(HERE, "runs")
sys.path.insert(0, os.path.join(REPO, "campaign_fresh_gravity", "CFG917_cmb_lensing_gate")); import cfg917_lib as LB   # read only
sys.path.insert(0, os.path.join(REB, "WG2_bare_law_web_lensing")); import wg2_pm as PM                               # read only
MUT = "--mutate" in sys.argv; TAG = "_MUTATE" if MUT else ""
OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(s)

# ---------------------------------------------------------------- copied unchanged from WG2's wg2_grade.py (lines 21-83)
H = PM.H; CH = 2997.92458 / H                      # c / H0 in Mpc
ZS = 1090.0
LS = np.arange(8, LB.LMAX + 1); L4 = (LS * (LS + 1.0)) ** 2 / (2 * math.pi)
D = LB.load_pr4()

# ------------------------------------------------------------------ geometry and Limber (WG1's engine, same E(a) as the runs)
def geom(bg):
    E, _ = PM.background(bg)
    z = np.concatenate([np.linspace(0.0, 10.0, 8001), np.geomspace(10.0, ZS, 4001)[1:]])
    f = CH / np.array([E(1 / (1 + zz)) for zz in z])
    chi = np.concatenate([[0.0], np.cumsum(0.5 * (f[1:] + f[:-1]) * np.diff(z))]); chis = float(chi[-1])
    cg = np.concatenate([np.geomspace(1e-3, 100.0, 160), np.linspace(100.0, chis, 700)[1:]])
    w = np.zeros_like(cg); w[1:] += 0.5 * np.diff(cg); w[:-1] += 0.5 * np.diff(cg)
    q = 2.0 * (chis - cg) / (cg * chis)
    return dict(cg=cg, zg=np.interp(cg, chi, z), ker=w * q ** 2 / cg ** 2, chis=chis)
GEO = {bg: geom(bg) for bg in ("B1", "B2")}

def snap_tables(run):
    """per snapshot: z, log k (1/Mpc), log Delta^2_Psi on bins up to k_cut = 0.5 k_Ny, and the high-k slope."""
    kny = math.pi * run["N"] / run["L"] * H; kcut = 0.5 * kny; tabs = []
    for s in sorted(run["snaps"], key=lambda s: s["z"]):
        k = np.array(s["k"]) * H; Pp = np.array(s["P_psi"]) / H ** 3
        d2 = k ** 3 * Pp / (2 * math.pi ** 2); m = (k <= kcut) & (d2 > 0)
        lk, ld = np.log(k[m]), np.log(d2[m])
        hi = (k[m] >= kcut / 2)
        slope = float(np.polyfit(lk[hi], ld[hi], 1)[0]) if hi.sum() >= 3 else -4.0
        tabs.append(dict(z=s["z"], lk=lk, ld=ld, slope=slope))
    return tabs, kcut

def logd2(t, lkq, zero_beyond):
    lk, ld = t["lk"], t["ld"]
    out = np.interp(lkq, lk, ld)                                           # flat below the first bin (np.interp clamps)
    hi = lkq > lk[-1]
    out = np.where(hi, ld[-1] + t["slope"] * (lkq - lk[-1]), out)
    return out, (hi if zero_beyond else np.zeros_like(hi)), (lkq >= lk[0]) & (lkq <= lk[-1])

def project(run, zero_beyond=False):
    g = GEO[run["bg"]]; tabs, kcut = snap_tables(run)
    zs = np.array([t["z"] for t in tabs]); lz = np.log1p(zs)
    C = np.zeros(len(LS)); Cin = np.zeros(len(LS))
    for chi, z, kw in zip(g["cg"], g["zg"], g["ker"]):
        k = (LS + 0.5) / chi; lkq = np.log(k)
        if z >= zs[-1]:
            i0 = i1 = len(tabs) - 1; t = 0.0
        else:
            i1 = int(np.searchsorted(zs, z)); i0 = max(i1 - 1, 0); t = 0.0 if i1 == i0 else (math.log1p(z) - lz[i0]) / (lz[i1] - lz[i0])
        a0_, z0_, in0 = logd2(tabs[i0], lkq, zero_beyond); a1_, z1_, in1 = logd2(tabs[i1], lkq, zero_beyond)
        ld = (1 - t) * a0_ + t * a1_
        Pk = 2 * math.pi ** 2 * np.exp(ld) / k ** 3
        Pk = np.where(z0_ | z1_, 0.0, Pk)
        C += kw * Pk; Cin += kw * Pk * (in0 & in1)
    X = np.zeros(LB.LMAX + 1); X[LS] = L4 * C
    Xin = np.zeros(LB.LMAX + 1); Xin[LS] = L4 * Cin
    return X, Xin

def grade_X(X):
    A, sA = LB.pr4_amp(D, X); c2 = LB.pr4_chi2(D, X)
    u = LB.wsum(D["W"], X); b = LB.qform(u, D["Cinv"]); Ap = LB.qform(u, D["Cinv"], D["d"]) / b
    return dict(r=1 / A, A_fit=A, sA=sA, chi2_unscaled=c2, p_unscaled=float(CHI2.sf(c2, D["n"])), r_plain=1 / Ap)

def run_label(r):
    return "FAILS LOW" if r < 0.5 else ("FAILS HIGH" if r > 2 else "WITHIN x2")


# ---------------------------------------------------------------- WG3
P(f"WG3{TAG}: the record's bound-only switch (CFG354 T1) on WG2's baryons-only engine, graded on Planck PR4 8-400 (bb3410083d, A1 ba8477ae8e).")
CK = json.load(open(os.path.join(RUNS, f"checks{TAG}.json")))
CHK = {k: CK[k] for k in ("K1", "K2", "K8")}
for k in ("K1", "K2", "K8"):
    P(f"  {k}: {'PASS' if CK[k]['pass_'] else 'FAIL'}  {dict((a, b) for a, b in CK[k].items() if a != 'pass_')}")
gK = GEO["B2"]; Lk = np.array([10, 100, 1000]); Ck = (gK["ker"][None, :] * (gK["cg"][None, :] / (Lk[:, None] + 0.5)) ** 4).sum(axis=1)
e3 = float(np.max(np.abs(Ck / (4 * gK["chis"] / (3 * (Lk + 0.5) ** 4)) - 1))); CHK["K3"] = dict(max_rel_err=e3, pass_=e3 < 1e-3)
P(f"  K3 Limber analytic: {e3:.2e} -> {'PASS' if e3 < 1e-3 else 'FAIL'}")
RUN = {os.path.basename(f)[:-5]: json.load(open(f)) for f in glob.glob(os.path.join(RUNS, "T1*.json"))}
REF = "T1_TIE_B2_As2.1e-09_N128_s200_zon50_canonical"
if REF in RUN:
    r0 = RUN[REF]; s0 = max(r0["snaps"], key=lambda s: s["z"]); k = np.array(s0["k"]); m = (k >= 0.01) & (k <= 0.1)
    pin = np.interp(k, np.array(r0["k_in"]), np.array(r0["P_in"])); e4b = float(np.array(s0["P_delta"])[m].sum() / pin[m].sum())
    CHK["K4b"] = dict(ratio_of_sums=e4b, pass_=abs(e4b - 1) < 0.10)
    P(f"  K4b ICs, ratio of summed power: {e4b:.4f} -> {'PASS' if CHK['K4b']['pass_'] else 'FAIL'}")
else:
    CHK["K4b"] = dict(pass_=False); P("  K4b: reference run missing -> FAIL")
ALLK = all(CHK[k]["pass_"] for k in ("K1", "K2", "K3", "K4b", "K8"))
P(f"  all K checks: {'PASS' if ALLK else 'FAIL'}; {len(RUN)} runs on disk")

G = {}
P(""); P("Runs: r (PACKAGE), PLAIN r, ON fraction f (volume / mass weighted) at z 2, 1, 0")
for t in sorted(RUN):
    run = RUN[t]; X, Xin = project(run); g = grade_X(X)
    zs = {round(s["z"], 3): s for s in run["snaps"]}
    fon = {z: (zs[z].get("f_vol"), zs[z].get("f_mass")) for z in (2.0, 1.0, 0.0) if z in zs}
    G[t] = dict(rule=run["rule"], bg=run["bg"], As=run["As"], N=run["N"], nstep=int(t.split("_s")[1].split("_")[0]), z_on=run["z_on"], **g,
                label=run_label(g["r"]), f_on=fon, delta_rms_z0=zs.get(0.0, {}).get("delta_rms"))
    P(f"  {t:<46} r {g['r']:10.4g} (plain {g['r_plain']:10.4g}) -> {run_label(g['r']):<10} f " +
      " ".join(f"z{z:g} {v[0]:.2e}/{v[1]:.2e}" for z, v in fon.items()) + f"; delta_rms z0 {G[t]['delta_rms_z0']:.4g}")

def members(rule):
    return [G[t] for t in G if G[t]["rule"] == rule and G[t]["N"] == 128 and G[t]["nstep"] == 200 and G[t]["z_on"] == 50 and G[t]["As"] in (1e-9, 4e-9)]
def rule_label(ms):
    if len(ms) != 4: return "INCOMPLETE"
    rs = [m["r"] for m in ms]
    if all(r < 0.5 for r in rs): return "FAILS LOW"
    if all(r > 2 for r in rs): return "FAILS HIGH"
    if all(0.5 <= r <= 2 for r in rs): return "WITHIN x2"
    return "STRADDLES"
LAB = {}
P(""); P("Labels (bracket B1/B2 x A_s 1e-9/4e-9; 128^3, 200 steps, z_on 50, a0 flat, canonical):")
for nm in ("T1", "T1T0"):
    ms = members(nm); lab = (rule_label(ms) if ALLK else "NOT EVALUABLE") if nm == "T1" else rule_label(ms) + " (reported)"
    LAB[nm] = dict(label=lab, r={f"{m['bg']}/As{m['As']:g}": m["r"] for m in ms})
    P(f"  {nm:<5}: {lab}; r = " + ", ".join(f"{m['bg']}/As{m['As']:g} {m['r']:.4g}" for m in ms))
ref = G.get(REF); k5 = G.get("T1_TIE_B2_As2.1e-09_N192_s200_zon50_canonical"); t1v = G.get("T1V_TIE_B2_As2.1e-09_N128_s200_zon50_canonical")
K5 = None
if ref and k5:
    K5 = dict(r128=ref["r"], r192=k5["r"], same_label=ref["label"] == k5["label"], pass_=ref["label"] == k5["label"])
    P(f"  K5 resolution: r 128^3 {ref['r']:.4g} vs 192^3 {k5['r']:.4g}; labels {ref['label']} / {k5['label']} -> {'PASS' if K5['pass_'] else 'FAIL: T1 carries NOT CONVERGED'}")
    if not K5["pass_"] and ALLK: LAB["T1"]["label"] += " [NOT CONVERGED (K5)]"
if t1v: P(f"  T1V (reported): r {t1v['r']:.4g} -> {t1v['label']}")
W2 = json.load(open(os.path.join(REB, "WG2_bare_law_web_lensing", "wg2_results.json")))["labels_A2_post_result"]
P(f"  context (WG2, under its A2): R0 {W2['R0']['label']} {['%.3g' % x for x in W2['R0']['r']]}; R1-TIE {W2['R1-TIE']['label']} {['%.3g' % x for x in W2['R1-TIE']['r']]}")
lt = LAB["T1"]["label"]
if not ALLK: LINE = "NOT EVALUABLE (a K check failed)"
elif lt.startswith("FAILS"):
    LINE = f"T1 {lt}: no rule tried lands there -- off, QUMOND on, or the record's bound-only switch (T1)"
elif lt.startswith("WITHIN"):
    LINE = "T1 WITHIN x2: a hit to verify (K5, K8 and a 256^3 check frozen before running)"
else:
    LINE = f"T1 {lt}"
P(""); P(f"Record line: {LINE}")
P(""); P("kappa = 1/2 FITTED; not theory closed; nothing here says the data favour the framework.")
json.dump(dict(lane="WG3_bound_only_web_rule", criteria="bb3410083d", amendment="ba8477ae8e", mutate=MUT, checks=CHK, all_K_pass=ALLK, K5=K5,
               labels=LAB, record_line=LINE, runs=G), open(os.path.join(HERE, f"wg3{TAG}_results.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"wg3{TAG}.out"), "w").write("\n".join(OUT) + "\n")
