#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
PAPER40 v1.1 figures (a width-chain estimate of the MOND acceleration scale from MIGHTEE-HI COSMOS).

v1.1 change: the catalogue W50 are REST-FRAME (CFG309, criteria ec54de4ac, results 53f8fa937, confirming referee CFG306's C1), so the
primary chain reads W50 without the (1+z) division (frame exponent k = 0).  CFG301's committed k = 1 numbers are kept as a disclosed variant.

Builds, from committed inputs only:
  fig1_paper40_levels.pdf  the implied a0 per redshift window and pooled at k = 0 (CFG309's re-run of CFG301's committed chain), the k = 1
                           variant (CFG301), the gas-only single-dish flux-scale reading (CFG306 P3, k = 0) and the direct BTFR rows, against
                           the two footings, SPARC's fitted scale and the MIGHTEE-HI/LADUMA resolved fit;
  fig2_paper40_btfr.pdf    V = W50/(2 sin i) against M_b for the 47 discs with the deep-MOND line V^4 = G M_b a0 on both footings;
  PAPER40_figures_numbers.json  every number the figures and the paper's own diagnostic rows use.

Inputs (all committed): the MIGHTEE-HI COSMOS catalogue (data_assembly/mightee_hi_catalogue_2026-10-02/, sha256 prefix bcf9e8558bc56448),
CFG301's stage-A survivor IDs and stage-B results, CFG309's FRAME stage-B results and summary, CFG306's physics-check JSON, CFG302's
per-galaxy table, CFG304's results JSON, CFG301's estimator and kernel via hzq_core (CFG223's median-residual s*, nu_mono) and its
constants via cfg260_core.

The chain is re-implemented here from cfg301_width_chain.py and is GATED.  Before anything is plotted the script must reproduce
  (a) CFG301's committed k = 1 pooled s*, window s*, the -0.30 dex baryon band, the H0 = 67.4 knob and the BTFR medians (1e-9);
  (b) CFG309's committed k = 0 pooled s*, window s*, the H0, delta and M* knobs and the BTFR medians (1e-9);
  (c) CFG306's committed k = 0 gas-only flux-scale readings (P3) and k = 0 kernel rows (P2) (1e-6 relative; CFG306 used its own code);
  (d) the frozen cut, re-applied to the catalogue, returns CFG301's 47 IDs in order.
If any reproduction fails the script exits 1 and writes nothing.

POST HOC diagnostic rows, labelled as such in the paper (not frozen; all at k = 0 unless labelled): the flux scale (gas alone, R following
the size relation; all baryons at fixed R), the inclination thickness q0, MIGHTEE's own size relation, the kernel, delta = 5 km/s, molecular
gas, the SNR_3D threshold, per-galaxy residual correlations and a joint fit in z and log M_HI, the BTFR slope, and the join of the 47 discs
with CFG302's cube table.  kappa = 1/2 is FITTED.  No verdict words.

Usage:  python3 make_paper40_figures.py           (writes the two PDFs and the JSON next to this file)
        python3 make_paper40_figures.py --check   (reproduction gates only; writes nothing)
"""
import os, sys, json, math
sys.dont_write_bytecode = True
import numpy as np
import pandas as pd
from scipy.stats import spearmanr

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
CFG = os.path.join(REPO, "campaign_fresh_gravity")
LANE = os.path.join(CFG, "CFG301_mightee_hi_catalogue_width_chain")
L309 = os.path.join(CFG, "CFG309_mightee_width_frame")
L306 = os.path.join(CFG, "CFG306_paper40_referee")
sys.path.insert(0, os.path.join(CFG, "HZQ_common")); sys.path.insert(0, os.path.join(CFG, "CFG260_budhies_a0_z02"))
import contextlib, io
with contextlib.redirect_stdout(io.StringIO()):
    import hzq_core as H                      # CFG223's estimator (verbatim copy) and nu_mono, exactly as CFG301 uses them
    import cfg260_core as C                   # CFG260's constants (G, MSUN, KPC, FP0's full-precision a0 on both footings)

G, MSUN, KPC = C.G, C.MSUN, C.KPC
A0C, A0A = C.A0["canonical"], C.A0["alt"]
NU = H.NU
CSV = os.path.join(REPO, "data_assembly", "mightee_hi_catalogue_2026-10-02", "MIGHTEE_HI_COSMOS_catalogue.csv")
JA = json.load(open(os.path.join(LANE, "cfg301_stageA_results.json")))["numbers"]
JB = json.load(open(os.path.join(LANE, "cfg301_stageB_results.json")))["numbers"]                       # k = 1 (CFG301 as committed)
JF = json.load(open(os.path.join(L309, "cfg309_cfg301chain_stageB_FRAME_results.json")))["numbers"]      # k = 0 (CFG309 FRAME)
SF = json.load(open(os.path.join(L309, "cfg309_cfg301chain_FRAME_summary.json")))["frame"]
P306 = json.load(open(os.path.join(L306, "cfg306_physics_checks_results.json")))["numbers"]
J302 = json.load(open(os.path.join(CFG, "CFG302_mightee_cube_raw_widths", "cfg302_raw_widths_results.json")))["numbers"]
J304 = json.load(open(os.path.join(CFG, "CFG304_mightee_flux_scale_alfalfa", "cfg304_flux_scale_alfalfa_results.json")))["numbers"]
# the published whole-sample RAR level of Varasteanu et al. 2026 (arXiv:2608.03576: a0 = (1.50 +- 0.05) x 10^-10 m s^-2; CFG279 README),
# fitted with the same exponential (McGaugh-Lelli-Schombert) function but with resolved curves and resolved M/L -- a reference line only
A0_V26 = 1.50e-10
REC0 = dict(delta=0.0, sini=None, tau_ms=0.0, tau_b=0.0, rdex=0.0, h0=70.0, gas_dex=0.0, h2=0.0, k=1, size=(0.506, -3.293))
RECP = dict(REC0, k=0)                                                                                   # v1.1 primary: rest-frame W50
CHECK_ONLY = "--check" in sys.argv

# kernels nu(y), y = g_bar / a0 (the primary is nu_mono, equal to the exponential form below y = 2.54)
KERN = {
    "exp": lambda y: C.nuv(NU, y),
    "simple": lambda y: 0.5 + np.sqrt(0.25 + 1.0 / y),
    "standard": lambda y: np.sqrt(0.5 + np.sqrt(0.25 + 1.0 / y ** 2)),
    "closed_form": lambda y: np.sqrt(1.0 + 1.0 / y),
    "delta4.1": lambda y: (1.0 - np.exp(-y ** (4.1 / 2))) ** (-1 / 4.1),
}
K306 = {"exp": "exp (nu_mono, MLS16; PAPER40 primary)", "simple": "simple (alpha=1)", "standard": "standard (n=2)",
        "closed_form": "framework closed form sqrt(1+1/y)", "delta4.1": "delta-family delta=4.1 (V26 best fit)"}


def chain(a, W, rec):
    """cfg301_width_chain.py's chain, plus post hoc handles: gas_dex (a shift of M_HI alone: the gas and, through the size relation, R),
    k (the (1+z) frame exponent; k = 0 reads the catalogue W50 as rest-frame), size (the D_HI relation), h2 (M_H2 / M_HI added to M_b, R fixed)."""
    ds = 70.0 / rec["h0"]
    Mhi = a["mhi"] * ds ** 2 * 10 ** rec["gas_dex"]
    Ms = a["ms"] * ds ** 2 * 10 ** rec["tau_ms"]
    Mg = 1.33 * Mhi
    tb = 10 ** rec["tau_b"]
    Mg, Ms = Mg * tb, Ms * tb
    Mb = Mg + Ms + rec["h2"] * Mhi * tb
    R = 0.5 * 10 ** (rec["size"][0] * np.log10(Mhi) + rec["size"][1] + rec["rdex"]) * KPC
    sini = a["sini"] if rec["sini"] is None else rec["sini"]
    Wc = (np.asarray(W, float) - rec["delta"]) / (1 + a["z"]) ** rec["k"]
    V = Wc / (2 * sini) * 1e3
    gb = G * Mb * MSUN / R ** 2
    go = V ** 2 / R
    return dict(D=go / gb, gb=gb, V=V, Mb=Mb, Mg=Mg, Ms=Ms, R=R, y=gb / A0C)


def est(dd, a0=A0C, nu=NU):
    l, u = H.AI.implied(dd["D"], dd["gb"], nu, a0)
    return float(l[0]), bool(u[0])


def arrays(T):
    return dict(mhi=10 ** T.log_M_HI.values, ms=10 ** T.log_M_stel.values, z=T.z_HI.values.astype(float), sini=np.sin(np.radians(T.incl_deg.values)))


# ------------------------------------------------------------------ the 47 survivors, in CFG301's order (z_HI, ID)
d = pd.read_csv(CSV, dtype={"ID_catalogue": str})
assert H.sha(CSV) == "bcf9e8558bc56448", "catalogue sha256 prefix differs from CFG301's"
srt = lambda mask: d[mask].sort_values(["z_HI", "ID_catalogue"], kind="mergesort").reset_index(drop=True)
S = d[d.ID_catalogue.isin(set(JA["survivor_ids"]))].sort_values(["z_HI", "ID_catalogue"], kind="mergesort").reset_index(drop=True)
assert S.ID_catalogue.tolist() == JA["survivor_ids"], "survivor order differs from CFG301 stage A"
N = len(S)
a = arrays(S)
W = S.W_50_km_s.values.astype(float)
WIN = [np.asarray(x) for x in np.array_split(np.arange(N), 3)]
gate = []


def g(name, mine, committed, tol=1e-9, rel=False):
    dev = abs(mine / committed - 1) if rel else abs(mine - committed)
    gate.append(dict(name=name, mine=mine, committed=committed, dev=dev, ok=bool(dev <= tol)))


# (a) CFG301, k = 1
dd1 = chain(a, W, REC0)
l1, _ = est(dd1)
g("[CFG301 k=1] pooled log10 s*", l1, JB["pooled"]["log_s"])
for i, w in enumerate(WIN):
    g(f"[CFG301 k=1] W{i + 1} log10 s*", est({k: v[w] for k, v in dd1.items()})[0], JB["results"][f"W{i + 1}"]["log_s"])
g("[CFG301 k=1] pooled band -0.30 dex s*", 10 ** est(chain(a, W, dict(REC0, tau_b=-0.30)))[0], JB["pooled"]["bands"]["-0.30"], rel=True)
g("[CFG301 k=1] pooled H0 = 67.4 log10 s*", est(chain(a, W, dict(REC0, h0=67.4)))[0], JB["recipe"]["pooled"]["rows"]["h0"]["log_s"][0])
a0b1 = dd1["V"] ** 4 / (G * dd1["Mb"] * MSUN)
gasdom = dd1["Mg"] > dd1["Ms"]
g("[CFG301 k=1] BTFR median (i)", float(np.median(a0b1)), JB["btfr"]["(i) all survivors"]["median"], rel=True)
g("[CFG301 k=1] BTFR median (ii)", float(np.median(a0b1[gasdom])), JB["btfr"]["(ii) gas-dominated (M_gas > M*)"]["median"], rel=True)
g("[CFG301] y max (README 0.084)", float(dd1["y"].max()), 0.084, tol=5e-4)
# (b) CFG309, k = 0 (the v1.1 primary)
dd0 = chain(a, W, RECP)
lP, _ = est(dd0)
g("[CFG309 k=0] pooled log10 s*", lP, JF["pooled"]["log_s"])
g("[CFG309 k=0] pooled a0 (summary JSON)", 10 ** lP * A0C, SF["a0"], rel=True)
for i, w in enumerate(WIN):
    g(f"[CFG309 k=0] W{i + 1} log10 s*", est({k: v[w] for k, v in dd0.items()})[0], JF["results"][f"W{i + 1}"]["log_s"])
lh0 = est(chain(a, W, dict(RECP, h0=67.4)))[0]
g("[CFG309 k=0] pooled H0 = 67.4 log10 s*", lh0, JF["recipe"]["pooled"]["rows"]["h0"]["log_s"][0])
g("[CFG309 k=0] pooled delta = 11 log10 s*", est(chain(a, W, dict(RECP, delta=11.0)))[0], JF["recipe"]["pooled"]["rows"]["delta"]["log_s"][0])
g("[CFG309 k=0] pooled M* +0.25 log10 s*", est(chain(a, W, dict(RECP, tau_ms=0.25)))[0], JF["recipe"]["pooled"]["rows"]["tau_ms"]["log_s"][1])
a0b = dd0["V"] ** 4 / (G * dd0["Mb"] * MSUN)
g("[CFG309 k=0] BTFR median (i)", float(np.median(a0b)), JF["btfr"]["(i) all survivors"]["median"], rel=True)
g("[CFG309 k=0] BTFR median (ii)", float(np.median(a0b[gasdom])), JF["btfr"]["(ii) gas-dominated (M_gas > M*)"]["median"], rel=True)
# (c) CFG306, k = 0: gas-only single-dish readings and kernel rows
P3 = P306["P3_flux_frame"]
FLUXROWS = {"C1 code-1 (CFG304 primary)": "c1", "CFG301-like 7 pairs (CFG304 PH2)": "pairs7", "z >= 0.02, codes 1+2 (CFG304 PH1)": "zge002",
            "z >= 0.02, confusion-clean (CFG304 PH1)": "zge002_clean", "CFG306 S2: code-1 trend in SNR_3D extrapolated to the 47": "snr_extrap",
            "CFG306 S2: code-1 trend in z extrapolated to the 47": "z_extrap"}
fluxk0 = {}
for lab, key in FLUXROWS.items():
    r = P3[f"{lab} | k=0"]
    lg = est(chain(a, W, dict(RECP, gas_dex=-r["R"])))[0]
    la = est(chain(a, W, dict(RECP, tau_b=-r["R"])))[0]
    fluxk0[key] = dict(label=lab, R=r["R"], a0_gas=10 ** lg * A0C, dlog_gas=lg - lP, a0_all=10 ** la * A0C, dlog_all=la - lP)
    g(f"[CFG306 P3 k=0] gas-only a0 at R {r['R']:+.3f} ({key})", 10 ** lg * A0C, r["a0_gas"], tol=1e-6, rel=True)
kern = {}
for kk, fn in KERN.items():
    lk = est(dd0, nu=fn)[0]; lk1 = est(dd1, nu=fn)[0]
    kern[kk] = dict(a0=10 ** lk * A0C, dlog_vs_primary=lk - lP, a0_k1=10 ** lk1 * A0C)
    g(f"[CFG306 P2 k=0] kernel {kk} a0", 10 ** lk * A0C, P306["P2_kernels"]["rows"][K306[kk]]["a0_k0"], tol=1e-6, rel=True)
# (d) the frozen cut re-applied (CFG301 FROZEN_CRITERIA order), parameterised in the SNR_3D threshold
FL = ["low_confidence_flag", "blended_flag", "confused_flag", "bad_ellipse_flag", "contaminated_source_flag"]
golden = (d[FL].fillna(1).values == 0).all(axis=1)
base = golden & d.z_HI.between(0.02, 0.093) & d.incl_deg.between(45, 80) & (d.log_M_HI >= 9.0)
wok = np.isfinite(d.W_50_km_s) & np.isfinite(d.W_50_km_s_err) & (d.W_50_km_s >= 80) & (d.W_50_km_s_err / d.W_50_km_s <= 0.15)
fin = np.isfinite(d[["z_HI", "D_L_Mpc", "log_M_HI", "incl_deg", "log_M_stel"]].values.astype(float)).all(axis=1) & (d.log_M_stel > 0)
cut = lambda thr: base & wok & (d.SNR_3D >= thr) & fin
g("[cut] SNR_3D >= 8 returns CFG301's 47 IDs in order (1 = yes)", float(srt(cut(8)).ID_catalogue.tolist() == JA["survivor_ids"]), 1.0, tol=0)

print("REPRODUCTION GATES (this script's chain against CFG301 k=1, CFG309 k=0 and CFG306 k=0 committed JSONs):")
for r in gate:
    print(f"  [{'PASS' if r['ok'] else 'FAIL'}] {r['name']}: mine {r['mine']:.12g}, committed {r['committed']:.12g}, |dev| {r['dev']:.1e}")
if not all(r["ok"] for r in gate):
    sys.exit("reproduction gate FAILED -- nothing written")
if CHECK_ONLY:
    print(f"{sum(r['ok'] for r in gate)}/{len(gate)} reproduction checks pass (--check: nothing written)")
    sys.exit(0)

# ------------------------------------------------------------------ POST HOC rows at k = 0 (selection fixed at CFG301's 47 unless stated)
post = {}
post["frame_k1_variant"] = dict(log_s=l1, a0=10 ** l1 * A0C, dlog_vs_primary=l1 - lP, z_median=float(np.median(a["z"])))
R304 = J304["results"]["cat"]["C1"]["OPT"]["median"]
# the single-dish flux scale: gas alone (R follows the size relation) at every CFG304/CFG306 ratio, and all baryons at fixed R
post["flux_k0"] = fluxk0
# (b) the intrinsic thickness q0 of the inclination formula cos^2 i = (q^2 - q0^2)/(1 - q0^2) (the catalogue uses q0 = 0.2)
qax = S.axis_ratio.values.astype(float)
def incl_of(q0):
    return np.degrees(np.arccos(np.sqrt(np.clip((qax ** 2 - q0 ** 2) / (1 - q0 ** 2), 0.0, 1.0))))
post["q0_check_max_dev_deg"] = float(np.max(np.abs(incl_of(0.2) - S.incl_deg.values)))
for q0 in (0.10, 0.30):
    l_ = est(chain(dict(a, sini=np.sin(np.radians(incl_of(q0)))), W, RECP))[0]
    post[f"q0_{q0:.2f}"] = dict(log_s=l_, a0=10 ** l_ * A0C, dlog_vs_primary=l_ - lP)
# (c) MIGHTEE's own HI size-mass relation (Rajohnson et al. 2022: slope 0.501, intercept -3.252)
lsz = est(chain(a, W, dict(RECP, size=(0.501, -3.252))))[0]
post["size_rajohnson2022"] = dict(log_s=lsz, dlog_vs_primary=lsz - lP,
                                  dlogD_at_median=float((0.501 - 0.506) * np.median(S.log_M_HI.values) + (-3.252 + 3.293)), median_logMHI=float(np.median(S.log_M_HI.values)))
# (d) the kernel (computed above, checked against CFG306 P2)
post["kernel_k0"] = kern
# (e) line width: delta = 5 km/s (the SPARC x ALFALFA W50-vs-V_flat offset at MIGHTEE-like masses, CFG306 P6) and delta = 11 (CFG309 recipe)
l5 = est(chain(a, W, dict(RECP, delta=5.0)))[0]
post["delta5"] = dict(log_s=l5, a0=10 ** l5 * A0C, dlog_vs_primary=l5 - lP)
# (f) molecular gas
for h in (0.1, 0.3):
    lh = est(chain(a, W, dict(RECP, h2=h)))[0]
    post[f"h2_{h:.1f}"] = dict(log_s=lh, a0=10 ** lh * A0C, dlog_vs_primary=lh - lP)
# (g) selection: the SNR_3D threshold (the frozen cut is 8), and the discs the cut removes
sel = {}
for thr in (0.0, 6.0, 7.0, 8.0, 9.0, 10.0, 12.0):
    T = srt(cut(thr)); ddt = chain(arrays(T), T.W_50_km_s.values.astype(float), RECP)
    lt = est(ddt)[0]
    sel[f"{thr:g}"] = dict(n=int(len(T)), log_s=lt, a0=10 ** lt * A0C, dlog_vs_primary=lt - lP)
T = srt(base & wok & fin & ~(d.SNR_3D >= 8)); ddt = chain(arrays(T), T.W_50_km_s.values.astype(float), RECP)
lt = est(ddt)[0]
sel["removed_by_8"] = dict(n=int(len(T)), log_s=lt, a0=10 ** lt * A0C, dlog_vs_primary=lt - lP, median_logMHI=float(np.median(T.log_M_HI)))
post["selection_snr"] = sel
# (h) per-galaxy implied log s* (each galaxy's own root), residual correlations and a joint fit in z and log M_HI
ps = np.array([est({"D": dd0["D"][[i]], "gb": dd0["gb"][[i]]})[0] for i in range(N)])
res = ps - lP
fg = dd0["Mg"] / dd0["Mb"]
cor = {}
for nm, x in (("W50", W), ("gas_fraction", fg), ("log_Mstar", S.log_M_stel.values), ("log_Mb", np.log10(dd0["Mb"])), ("z", a["z"]),
              ("log_MHI", S.log_M_HI.values), ("SNR_3D", S.SNR_3D.values), ("incl_deg", S.incl_deg.values), ("axis_ratio", qax)):
    r_, p_ = spearmanr(res, x)
    cor[nm] = dict(rho=float(r_), p=float(p_))
X = np.column_stack([np.ones(N), a["z"] - np.median(a["z"]), S.log_M_HI.values - np.median(S.log_M_HI.values)])
beta = np.linalg.lstsq(X, res, rcond=None)[0]
rng = np.random.default_rng(40)
bb = []
for _ in range(4000):
    i = rng.integers(0, N, N); bb.append(np.linalg.lstsq(X[i], res[i], rcond=None)[0])
bb = np.array(bb)
post["residuals_k0"] = dict(per_gal_robust_sd=float(1.4826 * np.median(np.abs(ps - np.median(ps)))), spearman=cor,
                            joint_fit=dict(note="OLS of per-galaxy log s* - pooled on (z - median z) and (log M_HI - median); bootstrap 4000",
                                           b_z=float(beta[1]), b_z_68=np.percentile(bb[:, 1], [16, 84]).tolist(), b_z_95=np.percentile(bb[:, 1], [2.5, 97.5]).tolist(),
                                           b_mhi=float(beta[2]), b_mhi_68=np.percentile(bb[:, 2], [16, 84]).tolist(), b_mhi_95=np.percentile(bb[:, 2], [2.5, 97.5]).tolist()))
# (i) the BTFR slope of the 47 at k = 0 (inverse: log V on log M_b)
lv = np.log10(dd0["V"] / 1e3); lm = np.log10(dd0["Mb"])
bi = 1.0 / np.polyfit(lm, lv, 1)[0]
bs = []
for _ in range(4000):
    i = rng.integers(0, N, N); bs.append(1.0 / np.polyfit(lm[i], lv[i], 1)[0])
post["btfr_slope_k0"] = dict(inverse=float(bi), inverse_68=np.percentile(bs, [16, 84]).tolist())
# (j) the cube flux scale for exactly these 47 discs (join with CFG302's committed per-galaxy table)
c302 = pd.read_csv(os.path.join(CFG, "CFG302_mightee_cube_raw_widths", "cfg302_per_galaxy.csv"))
j = c302[c302.ID.isin(set(S.ID_catalogue))]
jp = j[j.primary == 1]; jd = jp[jp.detected.astype(str) == "True"]
post["cfg302_join"] = dict(n_in_table=int(len(j)), n_primary=int(len(jp)), n_detected=int(len(jd)), median_ratio_primary=float(np.median(jp.ratio_S)),
                           median_logratio_S_detected=float(np.median(jd.logratio_S)), median_logratio_W50_detected=float(np.median(jd.logratio_W50.dropna())))
for k_, v_ in post.items():
    print(f"POST HOC {k_}: {v_}")

# ------------------------------------------------------------------ kappa on both footings (kappa = 1/2 x a0 / a0_footing), statistics and recipe, k = 0
q = JF["pooled"]["q"]; half = JF["pooled"]["recipe_half"]
kap = {}
for nm, a0f in (("rho_Lambda", A0C), ("rho_crit", A0A)):
    s = JF["pooled"]["a0"] / a0f
    kap[nm] = dict(kappa=0.5 * s, stat68=[0.5 * 10 ** q[1] * A0C / a0f, 0.5 * 10 ** q[2] * A0C / a0f], stat95=[0.5 * 10 ** q[0] * A0C / a0f, 0.5 * 10 ** q[3] * A0C / a0f],
                   recipe=[0.5 * s * 10 ** (-half), 0.5 * s * 10 ** half], h0_674=0.5 * 10 ** lh0 * A0C / a0f,
                   single_dish_gas=0.5 * fluxk0["snr_extrap"]["a0_gas"] / a0f)
    print(f"kappa ({nm}, k = 0): {kap[nm]['kappa']:.4f}; stat 68% {kap[nm]['stat68'][0]:.4f}-{kap[nm]['stat68'][1]:.4f}; 95% {kap[nm]['stat95'][0]:.4f}-{kap[nm]['stat95'][1]:.4f}; "
          f"x10^+-recipe {kap[nm]['recipe'][0]:.4f}-{kap[nm]['recipe'][1]:.4f}; at H0 = 67.4 {kap[nm]['h0_674']:.4f}; single-dish gas-only {kap[nm]['single_dish_gas']:.4f}")

# ------------------------------------------------------------------ figures
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"font.size": 8.5, "axes.linewidth": 0.6, "xtick.major.width": 0.6, "ytick.major.width": 0.6, "pdf.fonttype": 42,
                     "axes.edgecolor": "#52514e", "xtick.color": "#52514e", "ytick.color": "#52514e", "axes.labelcolor": "#0b0b0b"})
BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"           # validated categorical slots 1-3 (all-pairs, light mode)
INK, INK2, GRID = "#0b0b0b", "#52514e", "#d9d8d4"
U = 1e-10

# Fig 1: the levels (k = 0 primary)
fig, ax = plt.subplots(figsize=(6.9, 3.3))
items = []
for i in range(3):
    r = JF["results"][f"W{i + 1}"]
    items.append((f"W{i + 1}\nz {r['z_med']:.3f}\nN {r['n']}", r["a0"], [10 ** v * A0C for v in r["q"]], r["recipe_half"], BLUE, "o", True))
r = JF["pooled"]
items.append((f"pooled\nz 0.03-0.09\nN {r['n']}", r["a0"], [10 ** v * A0C for v in r["q"]], r["recipe_half"], BLUE, "D", True))
r1 = JB["pooled"]
items.append(("pooled, $W_{50}$\nread as obs.-\nframe (v1.0)", r1["a0"], [10 ** v * A0C for v in r1["q"]], None, INK2, "D", False))
fc, fl_, fh = fluxk0["snr_extrap"]["a0_gas"], fluxk0["pairs7"]["a0_gas"], fluxk0["z_extrap"]["a0_gas"]
items.append(("single-dish\nflux scale\n(gas only)", fc, [fl_, fl_, fh, fh], None, ORANGE, "^", False))
for key, lab in (("(i) all survivors", "BTFR, all\nN 47\n(+kernel)"), ("(ii) gas-dominated (M_gas > M*)", "BTFR, gas-\ndom., N 37\n(+kernel)")):
    b = JF["btfr"][key]
    items.append((lab, b["median"], b["q"], b["recipe_half"], AQUA, "s", True))
refs = [(A0C, "canonical footing ($\\rho_\\Lambda$) 0.936", (0, (5, 2.5)), INK),
        (A0A, "alt footing ($\\rho_{\\rm crit}$) 1.131", (0, (6, 1.5, 1.5, 1.5)), INK),
        (1.20e-10, "SPARC $g_\\dagger$ (McGaugh+16) 1.20", (0, (1, 1.6)), INK2),
        (A0_V26, "MIGHTEE-HI/LADUMA resolved\nRAR fit (V26) 1.50", (0, (1, 3)), INK2)]
for (yv, lab, ls, col), va in zip(refs, ("top", "top", "bottom", "bottom")):
    ax.axhline(yv / U, color=col, lw=0.8, ls=ls, zorder=1)
    ax.text(len(items) - 0.35, yv / U * (0.992 if va == "top" else 1.008), lab, fontsize=6.4, color=col, ha="left", va=va)
for k, (lab, v, qq, rh, col, mk, filled) in enumerate(items):
    if rh is not None:
        ax.add_patch(plt.Rectangle((k - 0.22, v / U * 10 ** (-rh)), 0.44, v / U * (10 ** rh - 10 ** (-rh)), facecolor=col, alpha=0.13, edgecolor="none", zorder=2))
    if qq is not None:
        ax.plot([k, k], [qq[0] / U, qq[3] / U], color=col, lw=0.9, zorder=3, solid_capstyle="round")
        ax.plot([k, k], [qq[1] / U, qq[2] / U], color=col, lw=2.6, zorder=3, solid_capstyle="round")
    ax.plot(k, v / U, marker=mk, ms=7.5 if mk != "^" else 8.5, mfc=(col if filled else "white"), mec=col, mew=1.4, zorder=4, ls="none")
    ax.text(k + 0.27, v / U, f"{v / U:.2f}", fontsize=6.6, color=INK, va="center", ha="left", zorder=5)
ax.set_yscale("log"); ax.set_ylim(0.6, 2.6)
ax.set_yticks([0.7, 1.0, 1.5, 2.0, 2.5]); ax.set_yticklabels(["0.7", "1.0", "1.5", "2.0", "2.5"]); ax.minorticks_off()
ax.set_xticks(range(len(items))); ax.set_xticklabels([it[0] for it in items], fontsize=6.3)
ax.set_xlim(-0.6, len(items) + 1.75)
ax.set_ylabel("$a_0$  [$10^{-10}$ m s$^{-2}$]")
ax.yaxis.grid(True, color=GRID, lw=0.5, zorder=0); ax.set_axisbelow(True)
for sp in ("top", "right"):
    ax.spines[sp].set_visible(False)
fig.tight_layout()
f1 = os.path.join(HERE, "fig1_paper40_levels.pdf"); fig.savefig(f1, metadata={"CreationDate": None}); plt.close(fig)

# Fig 2: the BTFR (k = 0)
V = dd0["V"] / 1e3; Mb = dd0["Mb"]
sV = S.W_50_km_s_err.values / (2 * a["sini"])
sMb = np.sqrt((dd0["Mg"] * math.log(10) * S.log_M_HI_err.values) ** 2 + (dd0["Ms"] * math.log(10) * S.log_M_stel_err.values) ** 2) / Mb / math.log(10)
fig, ax = plt.subplots(figsize=(5.0, 3.6))
xx = np.linspace(9.2, 11.0, 50)
lines = []
for a0v, lab, ls in ((A0C, "$V^4=GM_ba_0$, canonical $a_0$ (0.936)", (0, (5, 2.5))), (A0A, "$V^4=GM_ba_0$, alt $a_0$ (1.131)", (0, (6, 1.5, 1.5, 1.5)))):
    vv = (G * 10 ** xx * MSUN * a0v) ** 0.25 / 1e3
    lines += ax.plot(xx, np.log10(vv), color=INK, lw=0.9, ls=ls, zorder=2, label=lab)
bmed = JF["btfr"]["(i) all survivors"]["median"]
vv = (G * 10 ** xx * MSUN * bmed) ** 0.25 / 1e3
lines += ax.plot(xx, np.log10(vv), color=AQUA, lw=1.0, zorder=2, label=f"median $V^4/(GM_b)$ ({bmed / U:.2f}, incl. kernel)")
leg_lines = ax.legend(handles=lines, loc="lower right", fontsize=6.6, frameon=False, title="[$10^{-10}$ m s$^{-2}$]", title_fontsize=6.6)
ax.add_artist(leg_lines)
pts = []
for sl, col, mk, lab, filled in ((gasdom, BLUE, "o", f"gas-dominated ($M_{{\\rm gas}}>M_\\star$), N {int(gasdom.sum())}", True),
                                 (~gasdom, ORANGE, "s", f"star-dominated, N {int((~gasdom).sum())}", False)):
    ax.errorbar(np.log10(Mb[sl]), np.log10(V[sl]), xerr=sMb[sl], yerr=sV[sl] / V[sl] / math.log(10), fmt="none", ecolor=col, elinewidth=0.6, alpha=0.6, zorder=3)
    pts += ax.plot(np.log10(Mb[sl]), np.log10(V[sl]), marker=mk, ms=5.2, ls="none", mfc=(col if filled else "white"), mec=col, mew=1.1, zorder=4, label=lab)
ax.set_xlabel("$\\log_{10}\\,M_b$  [M$_\\odot$]   ($M_b=1.33\\,M_{\\rm HI}+M_\\star$)")
ax.set_ylabel("$\\log_{10}\\,V$  [km s$^{-1}$]   ($V=W_{50}/(2\\sin i)$, rest frame)")
ax.set_xlim(9.15, 11.05)
ax.legend(handles=pts, loc="upper left", fontsize=6.8, frameon=False)
ax.grid(True, color=GRID, lw=0.5, zorder=0); ax.set_axisbelow(True)
for sp in ("top", "right"):
    ax.spines[sp].set_visible(False)
fig.tight_layout()
f2 = os.path.join(HERE, "fig2_paper40_btfr.pdf"); fig.savefig(f2, metadata={"CreationDate": None}); plt.close(fig)

out = dict(paper="PAPER40", version="1.1", primary_frame="k = 0 (catalogue W50 rest-frame; CFG309)",
           inputs=dict(catalogue_sha256_prefix="bcf9e8558bc56448", cfg301_stageA="cfg301_stageA_results.json", cfg301_stageB="cfg301_stageB_results.json",
                       cfg309_frame="cfg309_cfg301chain_stageB_FRAME_results.json", cfg306="cfg306_physics_checks_results.json"),
           reproduction_gate=gate, reproduction_ok=bool(all(r["ok"] for r in gate)), post_hoc_rows=post, kappa=kap,
           h0_674=dict(log_s=lh0, s=10 ** lh0, a0=10 ** lh0 * A0C, dlog_vs_primary=lh0 - lP),
           per_galaxy=dict(ID=S.ID_catalogue.tolist(), V_kms=V.tolist(), log_Mb=np.log10(Mb).tolist(), gas_dominated=gasdom.tolist(), y=dd0["y"].tolist(), log_s=ps.tolist()),
           figures=[os.path.basename(f1), os.path.basename(f2)])
json.dump(out, open(os.path.join(HERE, "PAPER40_figures_numbers.json"), "w"), indent=1)
print(f"wrote {os.path.basename(f1)}, {os.path.basename(f2)}, PAPER40_figures_numbers.json; {len(gate)}/{len(gate)} reproduction checks pass")
