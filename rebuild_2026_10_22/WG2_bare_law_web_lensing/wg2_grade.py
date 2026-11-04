#!/usr/bin/env python3
"""WG2 grader (FROZEN_CRITERIA.md 8f484be581, Amendment A1 dca7a564b3): K3 Limber and K4 IC checks, Limber projection of each run's
total-potential spectra P_Psi(k, z), PR4 fit (PACKAGE and PLAIN), and the frozen labels (per run, per web rule, D9).
Run: python3 wg2_grade.py            (writes wg2_results.json, wg2.out)
     python3 wg2_grade.py --mutate   (reads runs/checks_MUTATE.json, K1 must FAIL; writes wg2_MUTATE_results.json, wg2_MUTATE.out)
kappa = 1/2 FITTED; the cold sector stays retired; nothing here says the data favour the framework; not theory closed."""
import os, sys, json, math, glob
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np
from scipy.stats import chi2 as CHI2

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE)); RUNS = os.path.join(HERE, "runs")
sys.path.insert(0, os.path.join(REPO, "campaign_fresh_gravity", "CFG917_cmb_lensing_gate")); import cfg917_lib as LB   # read only
sys.path.insert(0, HERE); import wg2_pm as PM
MUT = "--mutate" in sys.argv; TAG = "_MUTATE" if MUT else ""
OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(s)

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

# ------------------------------------------------------------------ checks
P(f"WG2{TAG}: the law alone on the web, baryons only, graded on Planck PR4 lensing 8-400 (8f484be581, A1 dca7a564b3). kappa = 1/2 FITTED.")
CK = json.load(open(os.path.join(RUNS, f"checks{TAG}.json")))
CHK = {"K1": CK["K1"], "K2": CK["K2"]}
P(f"  K1 growth (128^3, A1): {CK['K1']['ratio_over_expected']:.4f} -> {'PASS' if CK['K1']['pass_'] else 'FAIL'}")
P(f"  K2 QUMOND plane wave: {CK['K2']['max_rel_err']:.2e} -> {'PASS' if CK['K2']['pass_'] else 'FAIL'}")
gK = GEO["B2"]; Lk = np.array([10, 100, 1000]); Ck = (gK["ker"][None, :] * (gK["cg"][None, :] / (Lk[:, None] + 0.5)) ** 4).sum(axis=1)
e3 = float(np.max(np.abs(Ck / (4 * gK["chis"] / (3 * (Lk + 0.5) ** 4)) - 1))); CHK["K3"] = dict(max_rel_err=e3, tol=1e-3, pass_=e3 < 1e-3)
P(f"  K3 Limber analytic: {e3:.2e} -> {'PASS' if e3 < 1e-3 else 'FAIL'}")
REF = "R1_TIE_B2_As2.1e-09_N128_s200_zon50_canonical"
RUN = {os.path.basename(f)[:-5]: json.load(open(f)) for f in glob.glob(os.path.join(RUNS, "R*.json"))}
if REF in RUN:
    r0 = RUN[REF]; s0 = min(r0["snaps"], key=lambda s: -s["z"]); k = np.array(s0["k"]); m = (k >= 0.01) & (k <= 0.1)
    pin = np.interp(k, np.array(r0["k_in"]), np.array(r0["P_in"])); e4 = float(np.mean(np.array(s0["P_delta"])[m] / pin[m]))
    CHK["K4"] = dict(mean_ratio=e4, tol=0.10, pass_=abs(e4 - 1) < 0.10)
    P(f"  K4 ICs: measured / input P_delta at z_on, 0.01-0.1 h/Mpc: {e4:.4f} -> {'PASS' if CHK['K4']['pass_'] else 'FAIL'}")
else:
    CHK["K4"] = dict(pass_=False, note="reference run missing"); P("  K4: reference run missing -> FAIL")
ALLK = all(CHK[k]["pass_"] for k in ("K1", "K2", "K3", "K4"))
P(f"  all K checks: {'PASS' if ALLK else 'FAIL'}; {len(RUN)} runs on disk")

# ------------------------------------------------------------------ project and grade every run
G = {}
P(""); P("Runs: r = model / data amplitude (PACKAGE), PLAIN r, unscaled chi2 (9 bins), zero-beyond-k_cut r, in-box fraction (bins 1 / 5 / 9)")
for t in sorted(RUN):
    run = RUN[t]; X, Xin = project(run); X0, _ = project(run, zero_beyond=True)
    g = grade_X(X); g0 = grade_X(X0)
    fin = LB.wsum(D["W"], Xin) / LB.wsum(D["W"], X)
    zsn = {round(s["z"], 3): s for s in run["snaps"]}
    s_end = zsn.get(0.0, {}); s_z2 = zsn.get(2.0, {})
    G[t] = dict(rule=run["rule"], a0rule=run["a0rule"], bg=run["bg"], As=run["As"], N=run["N"], nstep=run["nstep"], z_on=run["z_on"], foot=run["foot"],
                **g, r_zero_beyond=g0["r"], inbox_frac=fin.tolist(), label=run_label(g["r"]),
                delta_rms_z0=s_end.get("delta_rms"), delta_rms_z2=s_z2.get("delta_rms"), y_med_z2=s_z2.get("y_med"), y_med_z0=s_end.get("y_med"),
                runtime_s=run.get("runtime_s"))
    P(f"  {t:<52} r {g['r']:9.3g} (plain {g['r_plain']:9.3g}) chi2 {g['chi2_unscaled']:10.3g} zero-beyond r {g0['r']:9.3g} "
      f"in-box {fin[0]:.2f}/{fin[4]:.2f}/{fin[8]:.2f} -> {run_label(g['r'])}; delta_rms z0 {G[t]['delta_rms_z0']}")

# ------------------------------------------------------------------ labels
def members(rule, a0r):
    return [G[t] for t in G if G[t]["rule"] == rule and (rule == "R0" or G[t]["a0rule"] == a0r) and G[t]["N"] == 128 and G[t]["nstep"] == 200
            and G[t]["z_on"] == 50 and G[t]["foot"] == "canonical" and G[t]["As"] in (1e-9, 4e-9)]
def rule_label(ms):
    if len(ms) != 4: return "INCOMPLETE"
    rs = [m["r"] for m in ms]
    if all(r < 0.5 for r in rs): return "FAILS LOW"
    if all(r > 2 for r in rs): return "FAILS HIGH"
    if all(0.5 <= r <= 2 for r in rs):
        ok = all(abs(m["r"] - 1) <= 0.056 and m["p_unscaled"] >= 1e-3 for m in ms)
        return "WITHIN x2" + (" (AMPLITUDE PASS)" if ok else "")
    return "STRADDLES"
LAB = {}
P(""); P("Labels per web rule (bracket B1/B2 x A_s 1e-9/4e-9; 128^3, 200 steps, z_on 50, canonical):")
for nm, rule, a0r in (("R0", "R0", None), ("R1-TIE", "R1", "TIE"), ("R1-RIVAL", "R1", "RIVAL")):
    ms = members(rule, a0r); lab = rule_label(ms) if ALLK else "NOT EVALUABLE"
    LAB[nm] = dict(label=lab, r=[m["r"] for m in ms], r_plain=[m["r_plain"] for m in ms], n=len(ms))
    P(f"  {nm:<9}: {lab}; r = " + ", ".join(f"{m['bg']}/As{m['As']:g} {m['r']:.3g}" for m in ms))

def find(**kw):
    for t in G:
        if all(G[t].get(k) == v for k, v in kw.items()): return G[t]
    return None
ref = find(rule="R1", a0rule="TIE", bg="B2", As=2.1e-9, N=128, nstep=200, z_on=50, foot="canonical")
k5 = find(rule="R1", a0rule="TIE", bg="B2", As=2.1e-9, N=192, nstep=200, z_on=50, foot="canonical")
k6 = find(rule="R1", a0rule="TIE", bg="B2", As=2.1e-9, N=128, nstep=400, z_on=50, foot="canonical")
k7 = find(rule="R1", a0rule="TIE", bg="B2", As=2.1e-9, N=128, nstep=200, z_on=200, foot="canonical")
alt = find(rule="R1", a0rule="TIE", bg="B2", As=2.1e-9, N=128, nstep=200, z_on=50, foot="alt")
K5 = K6 = None
if ref and k5:
    q = k5["r"] / ref["r"]; K5 = dict(r128=ref["r"], r192=k5["r"], ratio=q, same_label=k5["label"] == ref["label"],
                                     pass_=bool(k5["label"] == ref["label"] and 1 / 1.5 <= q <= 1.5))
    P(f"  K5 resolution: r 128^3 {ref['r']:.4g} vs 192^3 {k5['r']:.4g} (ratio {q:.3f}; labels {ref['label']} / {k5['label']}) -> {'PASS' if K5['pass_'] else 'FAIL: R1 labels carry NOT CONVERGED'}")
if ref and k6:
    q = k6["r"] / ref["r"]; K6 = dict(r200=ref["r"], r400=k6["r"], ratio=q, pass_=bool(abs(q - 1) <= 0.10))
    P(f"  K6 time step: r 200 steps {ref['r']:.4g} vs 400 {k6['r']:.4g} (ratio {q:.3f}) -> {'PASS' if K6['pass_'] else 'FAIL: all labels carry NOT CONVERGED'}")
if ref and k7: P(f"  K7 turn-on (reported): z_on 50 r {ref['r']:.4g}, z_on 200 r {k7['r']:.4g}")
if ref and alt: P(f"  alt footing (reported): canonical r {ref['r']:.4g}, alt r {alt['r']:.4g}")
NC_R1 = not (K5 and K5["pass_"]); NC_ALL = not (K6 and K6["pass_"])
for nm in LAB:
    tags = []
    if NC_ALL: tags.append("NOT CONVERGED (K6)")
    if NC_R1 and nm.startswith("R1"): tags.append("NOT CONVERGED (K5)")
    LAB[nm]["qualifiers"] = tags

labs = [LAB[n]["label"] for n in ("R0", "R1-TIE", "R1-RIVAL")]
if not ALLK: D9 = "NOT EVALUABLE (a K check failed)"
elif all(l.startswith("FAILS") for l in labs):
    D9 = "FAILS for the law alone under every web rule tried: " + "; ".join(f"{n} {LAB[n]['label']}" for n in ("R0", "R1-TIE", "R1-RIVAL"))
elif any(LAB[n]["label"].startswith("WITHIN") for n in ("R1-TIE", "R1-RIVAL")):
    D9 = "IN RANGE under " + ", ".join(n for n in ("R1-TIE", "R1-RIVAL") if LAB[n]["label"].startswith("WITHIN")) + " (not a CMB pass: the primary CMB has no fit without dust)"
else:
    D9 = "UNDECIDED: brackets straddle (" + "; ".join(f"{n} {LAB[n]['label']}" for n in ("R0", "R1-TIE", "R1-RIVAL")) + ")"
if (NC_ALL or NC_R1) and ALLK: D9 += " [qualifiers: " + ", ".join(sorted(set(sum((LAB[n]["qualifiers"] for n in LAB), [])))) + "]"
P(""); P(f"D9 (law alone): {D9}")
P(""); P("kappa = 1/2 FITTED; not theory closed; nothing here says the data favour the framework.")
RES = dict(lane="WG2_bare_law_web_lensing", criteria="8f484be581", amendment="dca7a564b3", mutate=MUT, checks=CHK, all_K_pass=ALLK, K5=K5, K6=K6,
           K7=dict(r_zon50=ref["r"] if ref else None, r_zon200=k7["r"] if k7 else None), alt=dict(r_canonical=ref["r"] if ref else None, r_alt=alt["r"] if alt else None),
           labels=LAB, D9=D9, runs=G)
json.dump(RES, open(os.path.join(HERE, f"wg2{TAG}_results.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"wg2{TAG}.out"), "w").write("\n".join(OUT) + "\n")
