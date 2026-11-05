#!/usr/bin/env python3
"""WG6 grader (FROZEN_CRITERIA.md 1a7c1cdde9, engine ea103b0e2d): WG2's projection and PR4 grading copied unchanged (wg2_grade.py lines
21-83, GEO extended to B2D), with the WG6 engine's patched module so chi(z) comes from B2D. Per-mu labels over A_s 1e-9 / 4e-9, K5, G-gal,
and the frozen lane reading. Run: python3 wg6_grade.py [--mutate]. kappa = 1/2 FITTED; the screening term is by hand; not theory closed."""
import os, sys, json, math, glob
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np
from scipy.stats import chi2 as CHI2
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE); REPO = os.path.dirname(REB); RUNS = os.path.join(HERE, "runs")
sys.path.insert(0, os.path.join(REPO, "campaign_fresh_gravity", "CFG917_cmb_lensing_gate")); import cfg917_lib as LB   # read only
sys.path.insert(0, HERE); import wg6_pm; PM = wg6_pm.B
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
GEO = {bg: geom(bg) for bg in ("B1", "B2", "B1D", "B2D")}   # B1D, B2D as WG4

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


# ---------------------------------------------------------------- WG6
P(f"WG6{TAG}: NEW by-hand Yukawa screening of the phantom, a0 tracking rho_DE (DESI CPL), B2D, graded on Planck PR4 8-400 (1a7c1cdde9).")
CK = json.load(open(os.path.join(RUNS, f"checks{TAG}.json"))); GG = json.load(open(os.path.join(HERE, "wg6_ggal.json")))
CHK = {k: CK[k] for k in ("K1", "K2", "K10")}; CHK["K11"] = GG["K11"]
gK = GEO["B2D"]; Lk = np.array([10, 100, 1000]); Ck = (gK["ker"][None, :] * (gK["cg"][None, :] / (Lk[:, None] + 0.5)) ** 4).sum(axis=1)
e3 = float(np.max(np.abs(Ck / (4 * gK["chis"] / (3 * (Lk + 0.5) ** 4)) - 1))); CHK["K3"] = dict(max_rel_err=e3, pass_=e3 < 1e-3)
RUN = {os.path.basename(f)[:-5]: json.load(open(f)) for f in glob.glob(os.path.join(RUNS, "R1Y*.json"))}
REF = "R1Y0.03_DE_B2D_As2.1e-09_N128_s200_zon50_canonical"
if REF in RUN:
    r0 = RUN[REF]; s0 = max(r0["snaps"], key=lambda s: s["z"]); k = np.array(s0["k"]); m = (k >= 0.01) & (k <= 0.1)
    pin = np.interp(k, np.array(r0["k_in"]), np.array(r0["P_in"])); CHK["K4b"] = dict(ratio_of_sums=float(np.array(s0["P_delta"])[m].sum() / pin[m].sum()))
    CHK["K4b"]["pass_"] = abs(CHK["K4b"]["ratio_of_sums"] - 1) < 0.10
else:
    CHK["K4b"] = dict(pass_=False)
for k_, v in CHK.items():
    P(f"  {k_}: {'PASS' if v['pass_'] else 'FAIL'}")
ALLK = all(v["pass_"] for v in CHK.values()); P(f"  all K checks: {'PASS' if ALLK else 'FAIL'}; {len(RUN)} runs on disk")
G = {}
P(""); P("Runs: r (PACKAGE), PLAIN r, unscaled chi2 p, delta_rms z0")
for t in sorted(RUN):
    run = RUN[t]; X, _ = project(run); g = grade_X(X); zs = {round(s["z"], 3): s for s in run["snaps"]}
    G[t] = dict(mu=float(run["rule"][3:]), As=run["As"], N=run["N"], **g, label=run_label(g["r"]), delta_rms_z0=zs.get(0.0, {}).get("delta_rms"))
    P(f"  {t:<52} r {g['r']:9.4g} (plain {g['r_plain']:9.4g}) p {g['p_unscaled']:.2g} -> {run_label(g['r']):<10} drms z0 {G[t]['delta_rms_z0']:.4g}")
def lab(ms):
    if len(ms) != 2: return "INCOMPLETE"
    rs = [m["r"] for m in ms]
    if all(r < 0.5 for r in rs): return "FAILS LOW"
    if all(r > 2 for r in rs): return "FAILS HIGH"
    if all(0.5 <= r <= 2 for r in rs):
        return "WITHIN x2" + (" (AMPLITUDE PASS)" if all(abs(m["r"] - 1) <= 0.056 and m["p_unscaled"] >= 1e-3 for m in ms) else "")
    return "STRADDLES"
LAB = {}
P(""); P("Labels per mu (A_s 1e-9 / 4e-9), with G-gal:")
for mu in ("0.01", "0.03", "0.1"):
    ms = [G[t] for t in G if abs(G[t]["mu"] - float(mu)) < 1e-12 and G[t]["N"] == 128 and G[t]["As"] in (1e-9, 4e-9)]
    L_ = lab(ms) if ALLK else "NOT EVALUABLE"; gg = GG["G_gal"][mu]
    LAB[mu] = dict(label=L_, r=[m["r"] for m in sorted(ms, key=lambda m: m["As"])], G_gal_pass=gg["pass_"], G_gal_ratio_1Mpc=gg["ratios"]["1.0"])
    P(f"  mu {mu:<5}/Mpc (1/mu {1 / float(mu):.0f} Mpc): {L_}; r = {', '.join('%.4g' % x for x in LAB[mu]['r'])}; G-gal {'PASS' if gg['pass_'] else 'FAIL'} (force ratio at 1 Mpc {gg['ratios']['1.0']:.4f})")
ref = G.get(REF); k5 = G.get("R1Y0.03_DE_B2D_As2.1e-09_N192_s200_zon50_canonical"); K5 = None
if ref and k5:
    K5 = dict(r128=ref["r"], r192=k5["r"], pass_=ref["label"] == k5["label"])
    P(f"  K5 resolution (mu 0.03): r 128^3 {ref['r']:.4g} vs 192^3 {k5['r']:.4g}; labels {ref['label']} / {k5['label']} -> {'PASS' if K5['pass_'] else 'FAIL: mu 0.03 carries NOT CONVERGED'}")
    if not K5["pass_"] and ALLK: LAB["0.03"]["label"] += " [NOT CONVERGED (K5)]"
labs = [LAB[m]["label"] for m in ("0.01", "0.03", "0.1")]
hit = [m for m in ("0.01", "0.03", "0.1") if LAB[m]["label"].startswith("WITHIN") and LAB[m]["G_gal_pass"] and "NOT CONVERGED" not in LAB[m]["label"]]
if not ALLK: LINE = "NOT EVALUABLE (a K check failed)"
elif hit: LINE = "a screening length of " + " / ".join(f"{1 / float(m):.0f} Mpc" for m in hit) + " lands within x2: FITTED, not derived, allowed by the galaxy-lensing gate"
elif all(l.startswith("FAILS HIGH") for l in labs): LINE = "screening within the galaxy-allowed range can't supply the factor (every mu FAILS HIGH)"
elif all(l.startswith("FAILS LOW") for l in labs): LINE = "every allowed screening overshoots low"
elif labs[0].startswith("FAILS HIGH") and labs[-1].startswith("FAILS LOW"): LINE = "the allowed range crosses the measured amplitude between bracket members; no interpolated value is a result, and any value inside is FITTED"
else: LINE = "brackets mixed: " + "; ".join(f"mu {m} {LAB[m]['label']}" for m in ("0.01", "0.03", "0.1"))
P(""); P(f"Lane reading: {LINE}"); P(""); P("kappa = 1/2 FITTED; not theory closed; nothing here says the data favour the framework.")
json.dump(dict(lane="WG6_screened_phantom_web", criteria="1a7c1cdde9", engine="ea103b0e2d", mutate=MUT, checks=CHK, all_K_pass=ALLK, K5=K5,
               labels=LAB, reading=LINE, runs=G), open(os.path.join(HERE, f"wg6{TAG}_results.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"wg6{TAG}.out"), "w").write("\n".join(OUT) + "\n")
