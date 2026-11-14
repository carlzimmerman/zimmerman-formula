"""LGS4 collector: applies the rules of FROZEN_CRITERIA.md to the eight run files and writes lgs4_results.json / lgs4_collect.out."""
import json, os
import numpy as np
from scipy.stats import norm, chi2 as CHI2, ncx2

HERE = os.path.dirname(os.path.abspath(__file__))
OUTF = open(os.path.join(HERE, "lgs4_collect.out"), "w")
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUTF.write(s + "\n")
def load(sample, model):
    return json.load(open(os.path.join(HERE, f"lgs4_{sample}_{model}.json")))
RUNS = [("full", "cpl"), ("full", "lcdm"), ("full", "cpl_dm"), ("full", "lcdm_dm"), ("des_only", "cpl"), ("des_only", "lcdm"),
        ("rand197", "cpl"), ("rand197", "lcdm")]
R = {k: load(*k) for k in RUNS}
res = {}
def sig2(dchi2):          # two extra parameters: p = exp(-dchi2 / 2), as a two-sided Gaussian sigma (the paper's convention)
    p = float(np.exp(-0.5 * max(dchi2, 0.0))); return float(norm.isf(p / 2)) if p < 1 else 0.0
def blk(r, names, which="chain"):
    nm = r["chain"]["names"] if which == "chain" else r["names"]
    i = [nm.index(n) for n in names]
    c = np.array(r["chain"]["cov"] if which == "chain" else r["laplace"]["cov"])[np.ix_(i, i)]
    m = np.array(r["chain"]["mean"] if which == "chain" else r["best"]["x"])[i]
    return m, c

# ---------------- gates ----------------
g0 = all(r["nstep"] == r["frozen_nstep"] and max(r["chain"]["rhat_minus_1"]) < 0.01 and r["laplace"]["positive_definite"] for r in R.values())
P(f"G0 chains: frozen step count, max R-1 < 0.01 and a positive-definite Laplace covariance in all eight runs: {'PASS' if g0 else 'FAIL'}"
  f"   (max R-1 {max(max(r['chain']['rhat_minus_1']) for r in R.values()):.4f})")
PAPER_FULL = dict(om=(0.314, 0.005), w0=(-0.802, 0.056), wa=(-0.770, 0.220), H0=(67.37, 0.55))       # arXiv:2610.23657 Table 3
PAPER_DES = dict(om=(0.311, 0.009), w0=(-0.845, 0.098), wa=(-0.639, 0.315), H0=(67.71, 0.93))
PAPER_DM = dict(om=(0.311, 0.008), w0=(-0.845, 0.091), wa=(-0.653, 0.295), H0=(67.78, 0.85), dm=(0.013, 0.021))
def against(r, paper, tag):
    rows, ok = {}, True
    for n, (pm, ps) in paper.items():
        i = r["chain"]["names"].index(n); m = r["chain"]["mean"][i]; s = float(np.sqrt(r["chain"]["cov"][i][i]))
        good = abs(m - pm) <= 0.5 * ps and 0.75 <= s / ps <= 1.33; ok &= good
        rows[n] = dict(here=[m, s], paper=[pm, ps], diff_in_paper_sd=(m - pm) / ps, sd_ratio=s / ps, within=bool(good))
        P(f"   {tag} {n:3s}: here {m:+.4f} +- {s:.4f}   paper {pm:+.4f} +- {ps:.4f}   diff {(m - pm) / ps:+.2f} paper sd, sd ratio {s / ps:.2f}  {'ok' if good else 'OUT'}")
    return rows, bool(ok)
P("H1 full sample, CPL, against the paper's 'DES + legacy' row (gate: every mean within 0.5 paper sd, every sd ratio in 0.75-1.33):")
h1rows, h1 = against(R[("full", "cpl")], PAPER_FULL, "H1")
P(f"H1: {'PASS' if h1 else 'FAIL'}")
P("context (no gate): DES-only CPL against the paper's 'DES' row:"); ctx_des, _ = against(R[("des_only", "cpl")], PAPER_DES, "ctx")
P("context (no gate): full sample, CPL with a free legacy offset, against the paper's row:"); ctx_dm, _ = against(R[("full", "cpl_dm")], PAPER_DM, "ctx")
res["gates"] = dict(G0=bool(g0), H1=h1, H1_rows=h1rows, context_des=ctx_des, context_offset=ctx_dm)
EVAL = g0 and h1

# ---------------- P1: does the (w0, wa) centre move when the legacy set is dropped? ----------------
def p1(which):
    mf, cf = blk(R[("full", "cpl")], ["w0", "wa"], which); md, cd = blk(R[("des_only", "cpl")], ["w0", "wa"], which)
    d = md - mf; Cd = cd - cf; pd = bool(np.all(np.linalg.eigvalsh(Cd) > 0))
    if not pd: return dict(d=d.tolist(), positive_definite=False)
    T = float(d @ np.linalg.solve(Cd, d)); p = float(np.exp(-T / 2))
    return dict(d=d.tolist(), nested_sd=np.sqrt(np.diag(Cd)).tolist(), per_axis_sigma=(d / np.sqrt(np.diag(Cd))).tolist(), T=T, p=p,
                sigma=float(norm.isf(p / 2)) if p < 1 else 0.0, positive_definite=True, label="CONSISTENT" if p >= 0.05 else "SHIFTED")
a, b = p1("chain"), p1("laplace")
for nm, x in (("chains", a), ("Laplace", b)):
    if x["positive_definite"]:
        P(f"P1 ({nm}): shift des_only - full (w0, wa) = ({x['d'][0]:+.4f}, {x['d'][1]:+.4f}); nested-sample sd ({x['nested_sd'][0]:.4f}, {x['nested_sd'][1]:.4f}); "
          f"per axis ({x['per_axis_sigma'][0]:+.2f}, {x['per_axis_sigma'][1]:+.2f}) sigma; 2D T = {x['T']:.3f}, p = {x['p']:.3f} ({x['sigma']:.2f} sigma) -> {x['label']}")
    else:
        P(f"P1 ({nm}): C_des - C_full is not positive definite -> no statistic")
if not (a["positive_definite"] and b["positive_definite"]): l1 = "NOT EVALUABLE"
elif a["label"] != b["label"]: l1 = "UNSTABLE"
else: l1 = a["label"]
res["P1"] = dict(chain=a, laplace=b, label=l1)

# ---------------- P2: distance from constant dark energy, per sample ----------------
p2 = {}
for s in ("full", "des_only", "rand197"):
    d = R[(s, "lcdm")]["best"]["chi2"] - R[(s, "cpl")]["best"]["chi2"]; p2[s] = dict(dchi2=float(d), sigma=sig2(d))
    P(f"P2 {s:9s}: chi2(constant dark energy) - chi2(CPL) = {d:.3f} -> {sig2(d):.2f} sigma")
sd = p2["des_only"]["sigma"]; l2 = "BELOW 2 SIGMA" if sd < 2 else ("2 TO 3 SIGMA" if sd < 3 else "ABOVE 3 SIGMA")
mf, cf = blk(R[("full", "cpl")], ["w0", "wa"]); md, cd = blk(R[("des_only", "cpl")], ["w0", "wa"])
dl = mf - np.array([-1.0, 0.0]); rho = float((dl @ np.linalg.solve(cd, dl)) / (dl @ np.linalg.solve(cf, dl)))
lam = max(p2["full"]["dchi2"] - 2, 0.0) * rho; obs = p2["des_only"]["dchi2"]
pA = float(ncx2.cdf(obs, 2, lam)) if lam > 0 else float(CHI2.cdf(obs, 2)); pB = float(CHI2.sf(obs, 2))
p2["expectation"] = dict(information_kept=rho, noncentrality=lam, mean_dchi2_if_real=lam + 2, sigma_if_real=sig2(lam + 2), sd_dchi2_if_real=float(np.sqrt(2 * (2 + 2 * lam))),
                         prob_this_low_or_lower_if_real=pA, mean_dchi2_if_legacy_made=2.0, prob_this_high_or_higher_if_legacy_made=pB)
P(f"P2 context: along the full-sample offset from w = -1, DES-only keeps {rho:.2f} of the information. If the full-sample signal is real, the DES-only "
  f"chi2 gain should average {lam + 2:.2f} ({sig2(lam + 2):.2f} sigma; sd {np.sqrt(2 * (2 + 2 * lam)):.2f}); if the legacy set made it, 2.00 (chi2, 2 dof).")
P(f"P2 context: observed {obs:.2f}. Probability of a gain this low or lower if real: {pA:.3f}; this high or higher if legacy-made: {pB:.3f}")
P(f"P2 des_only label: {l2}")
res["P2"] = dict(**p2, label=l2)

# ---------------- P3: an offset on the legacy set, or w(z)? (full sample) ----------------
c = {m: R[("full", m)]["best"]["chi2"] for m in ("lcdm", "lcdm_dm", "cpl", "cpl_dm")}
N = R[("full", "cpl")]["n_sn"] + 13 + 15 + 3 + 1; lnN = float(np.log(N))
G = c["lcdm_dm"] - c["cpl"]
l3 = "W(Z) FITS BETTER THAN AN OFFSET" if G >= lnN + 4 else ("AN OFFSET FITS BETTER THAN W(Z)" if G <= -2 else "CANNOT TELL")
P(f"P3 chi2_min, full sample: constant dark energy {c['lcdm']:.3f}; + offset {c['lcdm_dm']:.3f}; CPL {c['cpl']:.3f}; CPL + offset {c['cpl_dm']:.3f}")
P(f"P3 G = chi2(constant + offset) - chi2(CPL) = {G:+.3f}; one extra parameter costs 2 (AIC) to ln N = {lnN:.2f} (BIC, N = {N}); "
  f"dAIC {G - 2:+.2f}, dBIC {G - lnN:+.2f} (positive favours CPL) -> {l3}")
VOL = dict(h=0.60, obc=0.65, wb=0.005, w0=2.0, wa=5.0, dm=2.0)
def lnZ(r):
    k = len(r["names"]); C = np.array(r["laplace"]["cov"])
    return -0.5 * r["best"]["chi2"] + 0.5 * k * np.log(2 * np.pi) + 0.5 * np.linalg.slogdet(C)[1] - sum(np.log(VOL[n]) for n in r["names"])
ev = dict(full_cpl_vs_const=float(lnZ(R[("full", "cpl")]) - lnZ(R[("full", "lcdm")])), des_cpl_vs_const=float(lnZ(R[("des_only", "cpl")]) - lnZ(R[("des_only", "lcdm")])),
          full_cpl_offset_vs_const_offset=float(lnZ(R[("full", "cpl_dm")]) - lnZ(R[("full", "lcdm_dm")])), full_cpl_vs_const_offset=float(lnZ(R[("full", "cpl")]) - lnZ(R[("full", "lcdm_dm")])))
P(f"P3 context, Laplace evidence ratios with the paper's priors (ln B, positive favours the first): CPL vs constant, full {ev['full_cpl_vs_const']:+.2f} (paper +1.70); "
  f"DES-only {ev['des_cpl_vs_const']:+.2f} (paper -1.79); both with the offset {ev['full_cpl_offset_vs_const_offset']:+.2f} (paper -1.39); "
  f"CPL without offset vs constant with offset {ev['full_cpl_vs_const_offset']:+.2f} (not in the paper)")
res["P3"] = dict(chi2=c, G=float(G), N=N, lnN=lnN, dAIC=float(G - 2), dBIC=float(G - lnN), laplace_lnB=ev, label=l3)

# ---------------- P4: size control ----------------
l4 = "CONTROL QUIET" if p2["rand197"]["sigma"] >= p2["full"]["sigma"] - 0.5 else "CONTROL ALSO DROPS"
mr, cr = blk(R[("rand197", "cpl")], ["w0", "wa"]); sh = (mr - mf) / np.sqrt(np.diag(cf))
P(f"P4 rand197: {p2['rand197']['sigma']:.2f} sigma against {p2['full']['sigma']:.2f} for the full sample; centre moves ({sh[0]:+.2f}, {sh[1]:+.2f}) full-sample sd; "
  f"sd ratio rand197 / full ({np.sqrt(cr[0, 0] / cf[0, 0]):.3f}, {np.sqrt(cr[1, 1] / cf[1, 1]):.3f}) -> {l4}")
res["P4"] = dict(sigma_rand=p2["rand197"]["sigma"], sigma_full=p2["full"]["sigma"], shift_in_full_sd=sh.tolist(), label=l4)

# ---------------- P5: how much of an offset does each model want? ----------------
def offs(m):
    r = R[("full", m + "_dm")]; i = r["chain"]["names"].index("dm"); s = float(np.sqrt(max(c[m] - c[m + "_dm"], 0)))
    lab = "OFFSET DETECTED" if s >= 3 else ("OFFSET HINTED" if s >= 2 else "NO OFFSET")
    return dict(dm_best=r["best"]["x"][-1], dm_mean=r["chain"]["mean"][i], dm_sd=float(np.sqrt(r["chain"]["cov"][i][i])), dchi2=float(c[m] - c[m + "_dm"]), sigma=s, label=lab)
p5 = dict(constant=offs("lcdm"), cpl=offs("cpl"))
for k, v in p5.items():
    P(f"P5 legacy offset inside {'constant dark energy' if k == 'constant' else 'CPL'}: {v['dm_mean']:+.4f} +- {v['dm_sd']:.4f} mag (best fit {v['dm_best']:+.4f}); chi2 gain {v['dchi2']:.3f} -> {v['sigma']:.2f} sigma -> {v['label']}")
res["P5"] = p5

# ---------------- reading ----------------
if not EVAL: reading = "NOT EVALUABLE AS FROZEN"
elif l4 != "CONTROL QUIET": reading = "NOT TIED TO THE LEGACY SET"
elif l1 == "CONSISTENT" and l3 == "W(Z) FITS BETTER THAN AN OFFSET": reading = "READS AS A SIGNAL SEEN WITH LESS DATA"
elif l3 == "AN OFFSET FITS BETTER THAN W(Z)" and l2 == "BELOW 2 SIGMA": reading = "READS AS LEGACY-MADE"
else: reading = "THE SPLIT CANNOT TELL"
P(f"\nLABELS: P1 {l1}; P2 (des_only) {l2}; P3 {l3}; P4 {l4}; P5 constant {p5['constant']['label']}, CPL {p5['cpl']['label']}")
P(f"READING: {reading}" + ("" if EVAL else "  (a gate failed: the labels above carry no weight)"))
res["labels"] = dict(P1=l1, P2=l2, P3=l3, P4=l4, P5_constant=p5["constant"]["label"], P5_cpl=p5["cpl"]["label"]); res["reading"] = reading; res["evaluable"] = bool(EVAL)
json.dump(res, open(os.path.join(HERE, "lgs4_results.json"), "w"), indent=1)
