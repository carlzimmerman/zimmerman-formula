#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG306 (PAPER40 referee): independent physics checks of the CFG301 width chain as PAPER40 uses it.  Referee diagnostics, NOT frozen,
NOT an a0 measurement; kappa = 1/2 is FITTED; no sentence here says the data favour any law.

Reads committed inputs only (the MIGHTEE-HI COSMOS catalogue, CFG301's stage-A survivor IDs and stage-B JSON, CFG302's per-galaxy table,
CFG304's results JSON, the SPARC master table, the ALFALFA alpha.100/Durbala CSV).  Writes cfg306_physics_checks.out and
cfg306_physics_checks_results.json next to this file.

Sections
  P0  independent re-implementation of the chain and the median-residual estimator (own code, exponential kernel = nu_mono below y = 2.54);
      must reproduce CFG301's pooled and window s* to 1e-3 dex, and to 1e-9 with hzq_core's nu_mono.
  P1  velocity frame: k = 1 (PAPER40 primary: W50/(1+z)) against k = 0 (catalogue W50 already rest-frame).
  P2  kernel dependence of s* at y ~ 0.03: nu_mono/exponential, 'simple' (alpha = 1), 'standard' (n = 2), the framework's closed form
      sqrt(1 + 1/y), the delta-family at V26's delta = 4.1, and the pure deep limit; for MIGHTEE (k = 1 and k = 0) and for CC2's SPARC closure.
  P3  flux scale combined with the frame: HI-only (gas) and all-baryon shifts at the CFG304 ratios (-0.195 C1, -0.159 CFG301-like pairs,
      -0.137 z >= 0.02, -0.120 z >= 0.02 confusion-clean) for k = 1 and k = 0.
  P4  selection: the 23 discs removed by SNR_3D >= 8 and the 70-disc set before that cut; Spearman correlations of the per-galaxy
      residual with SNR_3D, W50, inclination, z, log M_b, gas fraction.
  P5  BTFR slope of the 47 (forward, inverse, bisector) and the per-galaxy residual scatter / robust error of the median.
  P7  molecular gas (M_H2 = 0.1 and 0.3 M_HI) and H0-consistent distances, for both frames.
  P6  width side on SPARC: SPARC x ALFALFA (UGC/NGC/IC name match) -> W50/(2 sin i) against V_flat, and the CC2 closure with the width
      velocity in place of V_flat on the same galaxies; SPARC M_HI against ALFALFA's (same distance) as a flux-scale transfer.
"""
import os, sys, json, math, re, hashlib
sys.dont_write_bytecode = True
import numpy as np
import pandas as pd
from scipy.optimize import brentq
from scipy.stats import spearmanr

HERE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(HERE)
REPO = os.path.dirname(CFG)
LOG = []
NUM = {}


def P(s=""):
    print(s, flush=True); LOG.append(str(s))


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


# ------------------------------------------------------------------ constants (CFG260's, checked against cfg260_core below)
G, MSUN, KPC = 6.6743e-11, 1.98847e30, 3.0857e19
A0C, A0A = 9.360324825027975e-11, 1.1312035414413022e-10
SREF = 1.20 / 0.93603
CSV = os.path.join(REPO, "data_assembly", "mightee_hi_catalogue_2026-10-02", "MIGHTEE_HI_COSMOS_catalogue.csv")
assert sha(CSV).startswith("bcf9e8558bc56448"), "catalogue sha differs"
L301 = os.path.join(CFG, "CFG301_mightee_hi_catalogue_width_chain")
JA = json.load(open(os.path.join(L301, "cfg301_stageA_results.json")))["numbers"]
JB = json.load(open(os.path.join(L301, "cfg301_stageB_results.json")))["numbers"]
J304 = json.load(open(os.path.join(CFG, "CFG304_mightee_flux_scale_alfalfa", "cfg304_flux_scale_alfalfa_results.json")))["numbers"]
JC2 = json.load(open(os.path.join(L301, "cfg301_CC2_results.json")))["numbers"]

# hzq_core's nu_mono (for the exact reproduction only)
sys.path.insert(0, os.path.join(CFG, "HZQ_common")); sys.path.insert(0, os.path.join(CFG, "CFG260_budhies_a0_z02"))
import contextlib, io
with contextlib.redirect_stdout(io.StringIO()):
    import hzq_core as H
    import cfg260_core as C
assert abs(C.G / G - 1) < 1e-12 and abs(C.MSUN / MSUN - 1) < 1e-12 and abs(C.KPC / KPC - 1) < 1e-12
assert abs(C.A0["canonical"] / A0C - 1) < 1e-12 and abs(C.A0["alt"] / A0A - 1) < 1e-12

# ------------------------------------------------------------------ kernels nu(y), y = g_bar/a0
KERN = {
    "exp (nu_mono, MLS16; PAPER40 primary)": lambda y: 1.0 / (1.0 - np.exp(-np.sqrt(y))),
    "simple (alpha=1)": lambda y: 0.5 + np.sqrt(0.25 + 1.0 / y),
    "standard (n=2)": lambda y: np.sqrt(0.5 + np.sqrt(0.25 + 1.0 / y ** 2)),
    "framework closed form sqrt(1+1/y)": lambda y: np.sqrt(1.0 + 1.0 / y),
    "delta-family delta=4.1 (V26 best fit)": lambda y: (1.0 - np.exp(-y ** (4.1 / 2))) ** (-1 / 4.1),
    "pure deep limit y^-1/2": lambda y: y ** -0.5,
}
KEXP = "exp (nu_mono, MLS16; PAPER40 primary)"


def nu_mono(y):
    return C.nuv(H.NU, y)


def s_star(D, gb, nu, a0=A0C):
    """median-residual root: median_i log10[D_i / nu(gb_i/(a0 s))] = 0, solved in log10 s (own implementation)."""
    D = np.asarray(D, float); gb = np.asarray(gb, float)
    f = lambda ls: float(np.median(np.log10(D / nu(gb / (a0 * 10 ** ls)))))
    lo, hi = -3.0, 3.0
    if f(lo) * f(hi) > 0:
        return float("nan")
    return brentq(f, lo, hi, xtol=1e-12)


def per_gal_s(D, gb, nu, a0=A0C):
    return np.array([s_star([d], [g], nu, a0) for d, g in zip(D, gb)])


# ------------------------------------------------------------------ the catalogue, my own frozen cut (must give CFG301's 47)
d = pd.read_csv(CSV, dtype={"ID_catalogue": str})
FL = ["low_confidence_flag", "blended_flag", "confused_flag", "bad_ellipse_flag", "contaminated_source_flag"]
golden = (d[FL].fillna(1).values == 0).all(axis=1)
base = golden & d.z_HI.between(0.02, 0.093) & d.incl_deg.between(45, 80) & (d.log_M_HI >= 9.0)
wok = np.isfinite(d.W_50_km_s) & np.isfinite(d.W_50_km_s_err) & (d.W_50_km_s >= 80) & (d.W_50_km_s_err / d.W_50_km_s <= 0.15)
fin = np.isfinite(d[["z_HI", "D_L_Mpc", "log_M_HI", "incl_deg", "log_M_stel"]].values.astype(float)).all(axis=1) & (d.log_M_stel > 0)
m47 = base & wok & (d.SNR_3D >= 8) & fin
m70 = base & wok & fin
srt = lambda mask: d[mask].sort_values(["z_HI", "ID_catalogue"], kind="mergesort").reset_index(drop=True)
S = srt(m47); S70 = srt(m70); SLOW = srt(m70 & ~(d.SNR_3D >= 8))
P(f"P0 my cut: golden {int(golden.sum())}, base {int(base.sum())}, +width {int((base & wok).sum())}, +SNR {int(m47.sum())}; IDs equal CFG301 stage A: {S.ID_catalogue.tolist() == JA['survivor_ids']}")
assert S.ID_catalogue.tolist() == JA["survivor_ids"]


def arrays(T):
    return dict(mhi=10 ** T.log_M_HI.values, ms=10 ** T.log_M_stel.values, z=T.z_HI.values.astype(float),
                sini=np.sin(np.radians(T.incl_deg.values)), W=T.W_50_km_s.values.astype(float))


def chain(a, k=1, gas_dex=0.0, all_dex=0.0, h0=70.0, rdex=0.0, delta=0.0, R_fixed_gas=False):
    ds = 70.0 / h0
    Mhi0 = a["mhi"] * ds ** 2
    Mhi = Mhi0 * 10 ** gas_dex
    Ms = a["ms"] * ds ** 2
    Mg = 1.33 * Mhi
    Mb = (Mg + Ms) * 10 ** all_dex
    Rm = Mhi0 if R_fixed_gas else Mhi
    R = 0.5 * 10 ** (0.506 * np.log10(Rm) - 3.293 + rdex) * KPC
    V = (a["W"] - delta) / (1 + a["z"]) ** k / (2 * a["sini"]) * 1e3
    gb = G * Mb * MSUN / R ** 2
    go = V ** 2 / R
    return dict(D=go / gb, gb=gb, V=V, Mb=Mb, Mg=Mg, Ms=Ms, R=R, y=gb / A0C)


a = arrays(S); N = len(S)
WIN = [np.asarray(x) for x in np.array_split(np.arange(N), 3)]
c0 = chain(a)
P("\nP0 REPRODUCTION (own estimator)")
rep = {}
for nm, idx in [("pooled", np.arange(N))] + [(f"W{i + 1}", w) for i, w in enumerate(WIN)]:
    ref = JB["pooled"]["log_s"] if nm == "pooled" else JB["results"][nm]["log_s"]
    l_exp = s_star(c0["D"][idx], c0["gb"][idx], KERN[KEXP])
    l_mono = s_star(c0["D"][idx], c0["gb"][idx], nu_mono)
    rep[nm] = dict(committed=ref, own_exp=l_exp, own_numono=l_mono, dev_exp=l_exp - ref, dev_numono=l_mono - ref)
    P(f"  {nm}: committed log s* {ref:+.10f}; own (exp kernel) {l_exp:+.10f} (dev {l_exp - ref:+.2e}); own (nu_mono) {l_mono:+.10f} (dev {l_mono - ref:+.2e})")
ok_rep = all(abs(r["dev_exp"]) < 1e-3 and abs(r["dev_numono"]) < 1e-9 for r in rep.values())
P(f"  reproduction {'PASS' if ok_rep else 'FAIL'} (exp within 1e-3 dex, nu_mono within 1e-9)")
NUM["P0_reproduction"] = dict(rows=rep, ok=ok_rep, y_quartiles=np.percentile(c0["y"], [25, 50, 75]).tolist(), y_max=float(c0["y"].max()))

a0 = lambda ls: 10 ** ls * A0C
dx = lambda x, ref: math.log10(x / ref)

# ------------------------------------------------------------------ P1 velocity frame
P("\nP1 VELOCITY FRAME (k = 1: W50/(1+z), PAPER40 primary; k = 0: catalogue W50 read as rest-frame)")
P1 = {}
for k in (1, 0):
    cc = chain(a, k=k)
    lp = s_star(cc["D"], cc["gb"], nu_mono)
    wins = [a0(s_star(cc["D"][w], cc["gb"][w], nu_mono)) for w in WIN]
    btfr = float(np.median(cc["V"] ** 4 / (G * cc["Mb"] * MSUN)))
    rb = np.random.default_rng(3061 + k); bl = []
    for _ in range(2000):
        ii = rb.integers(0, N, N); bl.append(s_star(cc["D"][ii], cc["gb"][ii], nu_mono))
    bq = np.percentile(bl, [2.5, 16, 84, 97.5])
    P(f"  k={k}: own bootstrap (B 2000) of the pooled a0: 68% {a0(bq[1]):.3e}-{a0(bq[2]):.3e}; 95% {a0(bq[0]):.3e}-{a0(bq[3]):.3e}; SD {np.std(bl):.3f} dex")
    P1[f"k{k}_boot"] = dict(q_a0=[a0(v) for v in bq], sd_dex=float(np.std(bl)))
    P1[f"k{k}"] = dict(log_s=lp, a0=a0(lp), windows_a0=wins, btfr_median=btfr, dlog_vs_canonical=dx(a0(lp), A0C), dlog_vs_alt=dx(a0(lp), A0A),
                       dlog_vs_sparc=dx(a0(lp), 1.20e-10), kappa_rhoL=0.5 * a0(lp) / A0C, kappa_rhoc=0.5 * a0(lp) / A0A,
                       drift_W3_W1=math.log10(wins[2] / wins[0]))
    P(f"  k={k}: pooled a0 {a0(lp):.4e} (canonical {P1[f'k{k}']['dlog_vs_canonical']:+.3f}, alt {P1[f'k{k}']['dlog_vs_alt']:+.3f}, SPARC 1.20 {P1[f'k{k}']['dlog_vs_sparc']:+.3f} dex); "
      f"kappa {P1[f'k{k}']['kappa_rhoL']:.3f} / {P1[f'k{k}']['kappa_rhoc']:.3f}; windows {', '.join(f'{w:.3e}' for w in wins)} (W3-W1 {P1[f'k{k}']['drift_W3_W1']:+.3f} dex); BTFR median {btfr:.3e}")
# recipe half-width at k = 0 (CFG301's four knobs, its rule: delta and H0 one-sided full shift, M* and D_HI half the two-sided difference)
for k in (1, 0):
    base_l = s_star(chain(a, k=k)["D"], chain(a, k=k)["gb"], nu_mono)
    def ls_of(**kw):
        cc = chain(a, k=k, **kw); return s_star(cc["D"], cc["gb"], nu_mono)
    def ls_ms(t):
        aa = dict(a, ms=a["ms"] * 10 ** t); cc = chain(aa, k=k); return s_star(cc["D"], cc["gb"], nu_mono)
    kd = abs(ls_of(delta=11.0) - base_l); km = abs(ls_ms(0.25) - ls_ms(-0.25)) / 2; kr = abs(ls_of(rdex=0.15) - ls_of(rdex=-0.15)) / 2; kh = abs(ls_of(h0=67.4) - base_l)
    half = math.sqrt(kd ** 2 + km ** 2 + kr ** 2 + kh ** 2)
    P1[f"k{k}_recipe"] = dict(delta=kd, mstar=km, dhi=kr, h0=kh, half=half)
    P(f"  k={k}: recipe knobs delta {kd:.3f}, M* {km:.3f}, D_HI {kr:.3f}, H0 {kh:.3f} -> half-width {half:.3f} dex (CFG301 committed at k=1: {JB['pooled']['recipe_half']:.3f})")
NUM["P1_frame"] = P1

# ------------------------------------------------------------------ P2 kernels (MIGHTEE and CC2 SPARC closure)
P("\nP2 KERNEL DEPENDENCE at the 47 discs' y (quartiles " + ", ".join(f"{v:.3f}" for v in np.percentile(c0["y"], [25, 50, 75])) + ")")
rows = []
for line in open(os.path.join(REPO, "real_research", "data", "SPARC_Lelli2016c.mrt")):
    t = line.split()
    if len(t) >= 18 and re.match(r"^[A-Z]", t[0]) and t[1].replace(".", "", 1).isdigit():
        k_ = ["name", "T", "D", "eD", "fD", "Inc", "eInc", "L36", "eL36", "Reff", "SBeff", "Rdisk", "SBdisk", "MHI", "RHI", "Vflat", "eVflat", "Q"]
        rows.append(dict(zip(k_, [t[0]] + [float(x) for x in t[1:18]])))
SP = pd.DataFrame(rows)
assert len(SP) == 175
spc = SP[(SP.Q <= 2) & (SP.Inc >= 30) & (SP.Vflat > 0) & (SP.MHI > 0)].reset_index(drop=True)
MHIs = spc.MHI.values * 1e9; Mbs = 1.33 * MHIs + 0.5 * spc.L36.values * 1e9
Rs = 0.5 * 10 ** (0.506 * np.log10(MHIs) - 3.293) * KPC
gbs = G * Mbs * MSUN / Rs ** 2; Ds = (spc.Vflat.values * 1e3) ** 2 / Rs / gbs
lcc2 = s_star(Ds, gbs, nu_mono)
P(f"  CC2 re-run (own code): N {len(spc)}, s* {10 ** lcc2:.4f} (committed {JC2['s']:.4f}; dev {lcc2 - JC2['log_s']:+.1e} dex)")
P2 = dict(cc2_check=dict(n=len(spc), s=10 ** lcc2, committed=JC2["s"]))
yS = gbs / A0C
P(f"  SPARC CC2 sample y at R: quartiles {', '.join(f'{v:.3f}' for v in np.percentile(yS, [25, 50, 75]))} (MIGHTEE: {', '.join(f'{v:.3f}' for v in np.percentile(c0['y'], [25, 50, 75]))})")
c1 = chain(a, k=0)
P2["rows"] = {}
for nm, nu in KERN.items():
    l1 = s_star(c0["D"], c0["gb"], nu); l0 = s_star(c1["D"], c1["gb"], nu); ls_ = s_star(Ds, gbs, nu)
    kf = float(np.median(c0["y"] * nu(c0["y"]) ** 2))
    P2["rows"][nm] = dict(a0_k1=a0(l1), a0_k0=a0(l0), cc2_a0=a0(ls_), mightee_minus_cc2_k1=l1 - ls_, mightee_minus_cc2_k0=l0 - ls_, kernel_factor_median=kf,
                          dlog_k1_vs_canonical=dx(a0(l1), A0C), dlog_k1_vs_alt=dx(a0(l1), A0A))
    P(f"  {nm:40s}: a0(k=1) {a0(l1):.3e}  a0(k=0) {a0(l0):.3e}  CC2-SPARC {a0(ls_):.3e}  MIGHTEE-CC2 {l1 - ls_:+.3f} (k=1) {l0 - ls_:+.3f} (k=0) dex; median y nu^2 {kf:.3f}")
ex = P2["rows"][KEXP]["a0_k1"]
spread = [math.log10(r["a0_k1"] / ex) for n, r in P2["rows"].items() if n != "pure deep limit y^-1/2"]
P2["kernel_spread_dex_k1"] = [min(spread), max(spread)]
P(f"  kernel spread of the k=1 a0 about the exp kernel (excluding the pure deep limit): {min(spread):+.3f} to {max(spread):+.3f} dex")
NUM["P2_kernels"] = P2

# ------------------------------------------------------------------ P3 flux scale x frame
P("\nP3 FLUX SCALE x FRAME (exact chain re-runs; 'gas' = M_HI shifted, R follows the size relation; 'all' = every baryon shifted at fixed R)")
Rc = J304["results"]["cat"]
ratios = {"C1 code-1 (CFG304 primary)": Rc["C1"]["OPT"]["median"]}
ph = json.load(open(os.path.join(CFG, "CFG304_mightee_flux_scale_alfalfa", "cfg304_posthoc_results.json")))
P(f"  CFG304 post hoc keys: {sorted(ph.get('numbers', ph).keys())[:12]}")
phn = ph.get("numbers", ph)


def find(dct, keys):
    for k_ in keys:
        if isinstance(dct, dict) and k_ in dct:
            dct = dct[k_]
        else:
            return None
    return dct


# the post hoc ratios quoted in the CFG304 README (z >= 0.02: -0.137 ALL N 19, -0.120 clean N 12; CFG301-like 7 pairs -0.159)
ratios["CFG301-like 7 pairs (CFG304 PH2)"] = -0.159
ratios["z >= 0.02, codes 1+2 (CFG304 PH1)"] = -0.137
ratios["z >= 0.02, confusion-clean (CFG304 PH1)"] = -0.120
ratios["CFG306 S2: code-1 trend in SNR_3D extrapolated to the 47"] = -0.115
ratios["CFG306 S2: code-1 trend in z extrapolated to the 47"] = -0.087
P3 = {}
for rn, R_ in ratios.items():
    for k in (1, 0):
        cg = chain(a, k=k, gas_dex=-R_); ca = chain(a, k=k, all_dex=-R_)
        lg = s_star(cg["D"], cg["gb"], nu_mono); la = s_star(ca["D"], ca["gb"], nu_mono)
        P3[f"{rn} | k={k}"] = dict(R=R_, k=k, a0_gas=a0(lg), a0_all=a0(la))
        P(f"  {rn:42s} R {R_:+.3f}  k={k}: gas-only a0 {a0(lg):.3e} (kappa {0.5 * a0(lg) / A0C:.3f}/{0.5 * a0(lg) / A0A:.3f}); all-baryon a0 {a0(la):.3e}")
NUM["P3_flux_frame"] = P3
P("\nP3b COMBINED GRID (illustration, not a measurement): frame k x width correction delta x HI-only flux shift")
P3b = {}
for k in (1, 0):
    for dl in (0.0, 5.0, 11.0):
        for R_ in (0.0, -0.087, -0.137, -0.195):
            cg = chain(a, k=k, delta=dl, gas_dex=-R_)
            lg = s_star(cg["D"], cg["gb"], nu_mono)
            P3b[f"k={k} delta={dl:g} R={R_:+.3f}"] = a0(lg)
        P(f"  k={k} delta={dl:4.1f} km/s: a0 at HI shift R = 0 / -0.087 / -0.137 / -0.195: " + " / ".join(f"{P3b[f'k={k} delta={dl:g} R={R_:+.3f}']:.3e}" for R_ in (0.0, -0.087, -0.137, -0.195)))
vals = list(P3b.values())
P(f"  grid range {min(vals):.3e} - {max(vals):.3e}")
NUM["P3b_grid"] = P3b

# ------------------------------------------------------------------ P4 selection
P("\nP4 SELECTION (the SNR_3D >= 8 cut and residual correlations)")
P4 = {}
for nm, T in (("47 (PAPER40)", S), ("70 (before SNR cut)", S70), ("23 removed by SNR_3D >= 8", SLOW)):
    aa = arrays(T); cc = chain(aa)
    lp = s_star(cc["D"], cc["gb"], nu_mono)
    bt = float(np.median(cc["V"] ** 4 / (G * cc["Mb"] * MSUN)))
    P4[nm] = dict(n=len(T), a0=a0(lp), btfr=bt, median_logMHI=float(np.median(T.log_M_HI)), median_z=float(np.median(T.z_HI)), median_W50=float(np.median(T.W_50_km_s)))
    P(f"  {nm:28s}: N {len(T)}  a0 {a0(lp):.3e}  BTFR median {bt:.3e}  median log M_HI {np.median(T.log_M_HI):.2f}  median z {np.median(T.z_HI):.3f}  median W50 {np.median(T.W_50_km_s):.0f}")
ps = per_gal_s(c0["D"], c0["gb"], nu_mono)
res = ps - JB["pooled"]["log_s"]
fg = c0["Mg"] / c0["Mb"]
cor = {}
for nm, x in (("SNR_3D", S.SNR_3D.values), ("W50", S.W_50_km_s.values), ("incl_deg", S.incl_deg.values), ("z_HI", S.z_HI.values),
              ("log_Mb", np.log10(c0["Mb"])), ("gas_fraction", fg), ("axis_ratio", S.axis_ratio.values), ("log_Mstar", S.log_M_stel.values)):
    r_, p_ = spearmanr(res, x)
    cor[nm] = dict(rho=float(r_), p=float(p_))
    P(f"  Spearman(per-galaxy log s*, {nm:12s}) rho {r_:+.3f}  p {p_:.3f}")
P4["correlations"] = cor
# a crude SNR-width selection probe on the 70: at fixed log M_HI, is SNR_3D anticorrelated with W50?
T = S70
X = np.column_stack([np.ones(len(T)), T.log_M_HI.values - 2 * np.log10(T.D_L_Mpc.values), np.log10(T.W_50_km_s.values)])
beta, *_ = np.linalg.lstsq(X, np.log10(T.SNR_3D.values), rcond=None)
P4["snr_fit_70"] = dict(coef_logflux=float(beta[1]), coef_logW50=float(beta[2]))
P(f"  log SNR_3D on log(flux proxy M_HI/D_L^2) and log W50 over the 70: coefficients {beta[1]:+.2f} (flux), {beta[2]:+.2f} (W50) [a negative W50 term = narrow lines favoured at fixed flux]")
NUM["P4_selection"] = P4

# ------------------------------------------------------------------ P5 BTFR slope and robust errors
P("\nP5 BTFR SLOPE AND THE ERROR OF THE MEDIAN")
lv = np.log10(c0["V"] / 1e3); lm = np.log10(c0["Mb"])
bf = np.polyfit(lv, lm, 1)[0]; bi = 1.0 / np.polyfit(lm, lv, 1)[0]
bis = (bf * bi - 1 + math.sqrt((1 + bf ** 2) * (1 + bi ** 2))) / (bf + bi)
rng = np.random.default_rng(306)
bs = []
for _ in range(4000):
    i = rng.integers(0, N, N); bs.append(1.0 / np.polyfit(lm[i], lv[i], 1)[0])
P5 = dict(forward=float(bf), inverse=float(bi), bisector=float(bis), inverse_boot68=np.percentile(bs, [16, 84]).tolist(), logMb_range=[float(lm.min()), float(lm.max())])
P(f"  slope of log M_b on log V: forward {bf:.2f}, inverse {bi:.2f} (68% {P5['inverse_boot68'][0]:.2f}-{P5['inverse_boot68'][1]:.2f}), bisector {bis:.2f}; log M_b {lm.min():.2f}-{lm.max():.2f}")
sd = float(np.std(ps)); mad = float(1.4826 * np.median(np.abs(ps - np.median(ps))))
P5.update(per_gal_sd=sd, per_gal_robust_sd=mad, median_err_est=float(1.2533 * mad / math.sqrt(N)), per_gal_median=float(np.median(ps)),
          hodges_lehmann=float(np.median([(ps[i] + ps[j]) / 2 for i in range(N) for j in range(i, N)])), trimmed20=float(np.mean(np.sort(ps)[int(0.2 * N):N - int(0.2 * N)])))
P(f"  per-galaxy log s*: SD {sd:.3f}, robust SD {mad:.3f} dex -> sqrt(pi/2) sigma/sqrt(N) error of the median {P5['median_err_est']:.3f} dex; "
  f"committed bootstrap 68% of the pooled log s*: {JB['pooled']['q'][1] - JB['pooled']['log_s']:+.3f} / {JB['pooled']['q'][2] - JB['pooled']['log_s']:+.3f} dex")
P(f"  location estimators of log s*: median-residual {JB['pooled']['log_s']:+.3f}; median of per-galaxy {P5['per_gal_median']:+.3f}; Hodges-Lehmann {P5['hodges_lehmann']:+.3f}; 20% trimmed mean {P5['trimmed20']:+.3f}")
NUM["P5_btfr_stats"] = P5

# ------------------------------------------------------------------ P6 width side and flux-scale transfer on SPARC x ALFALFA
P("\nP6 SPARC x ALFALFA (UGC = AGC number; NGC/IC by ALFALFA's optical-counterpart name)")
AL = pd.read_csv(os.path.join(REPO, "data_assembly", "alfalfa_sdss_local_control", "alfalfa_sdss.csv"), dtype={"sdss_objid": str})
AL["oc"] = AL.name_oc.fillna("").str.replace(" ", "").str.upper()
mt = []
for _, r in SP.iterrows():
    n = r["name"]; mm = None
    if re.match(r"^UGC\d+$", n):
        mm = AL[AL.agc == int(n[3:])]
    elif re.match(r"^NGC\d+$", n):
        mm = AL[AL.oc == "N" + str(int(n[3:]))]
    elif re.match(r"^IC\d+$", n):
        mm = AL[AL.oc == "I" + str(int(n[2:]))]
    if mm is not None and len(mm) == 1 and np.isfinite(mm.iloc[0].w50_kms):
        x = mm.iloc[0]
        mt.append(dict(name=n, Q=r.Q, Inc=r.Inc, D=r.D, MHI=r.MHI, L36=r.L36, Vflat=r.Vflat, dist_a=x.dist_mpc, logmhi_a=x.logmhi, w50=x.w50_kms, code=x.hi_code))
MT = pd.DataFrame(mt)
MT["dlogMHI_sparc_minus_alfalfa"] = np.log10(MT.MHI * 1e9) - (MT.logmhi_a + 2 * np.log10(MT.D / MT.dist_a))
sel = MT[(MT.Q <= 2) & (MT.Inc >= 30) & (MT.Vflat > 0) & (MT.code == 1)].reset_index(drop=True)
sel["dlogV"] = np.log10(sel.w50 / (2 * np.sin(np.radians(sel.Inc))) / sel.Vflat)
MHIx = sel.MHI.values * 1e9; Mbx = 1.33 * MHIx + 0.5 * sel.L36.values * 1e9; Rx = 0.5 * 10 ** (0.506 * np.log10(MHIx) - 3.293) * KPC; gbx = G * Mbx * MSUN / Rx ** 2
Vw = sel.w50.values / (2 * np.sin(np.radians(sel.Inc.values))) * 1e3; Vf = sel.Vflat.values * 1e3
l_vf = s_star(Vf ** 2 / Rx / gbx, gbx, nu_mono); l_w = s_star(Vw ** 2 / Rx / gbx, gbx, nu_mono)
l_w11 = s_star(((sel.w50.values - 11) / (2 * np.sin(np.radians(sel.Inc.values))) * 1e3) ** 2 / Rx / gbx, gbx, nu_mono)
bdl = []
for _ in range(4000):
    i = rng.integers(0, len(sel), len(sel)); bdl.append(np.median(sel.dlogV.values[i]))
P6 = dict(n_matched=len(MT), n_sel=len(sel), median_dlogMHI_all=float(np.median(MT.dlogMHI_sparc_minus_alfalfa)),
          median_dlogMHI_sel=float(np.median(sel.dlogMHI_sparc_minus_alfalfa)), median_dlogV=float(np.median(sel.dlogV)), dlogV_boot68=np.percentile(bdl, [16, 84]).tolist(),
          s_vflat=10 ** l_vf, s_w50=10 ** l_w, s_w50_delta11=10 ** l_w11, dlog_s_w50_minus_vflat=l_w - l_vf, dlog_s_w50d11_minus_vflat=l_w11 - l_vf,
          names=sel.name.tolist())
P(f"  matched with a W50: {len(MT)}; selected (Q<=2, i>=30, V_flat>0, ALFALFA code 1): {len(sel)}")
P(f"  SPARC M_HI minus ALFALFA M_HI at the SPARC distance: median {P6['median_dlogMHI_all']:+.3f} dex (all {len(MT)}), {P6['median_dlogMHI_sel']:+.3f} (selected)")
P(f"  log10[W50/(2 sin i) / V_flat]: median {P6['median_dlogV']:+.3f} dex (bootstrap 68% {P6['dlogV_boot68'][0]:+.3f} to {P6['dlogV_boot68'][1]:+.3f})")
P(f"  CC2 recipe on these {len(sel)}: s* with V_flat {10 ** l_vf:.3f}; with W50/(2 sin i) {10 ** l_w:.3f} ({l_w - l_vf:+.3f} dex); with (W50-11)/(2 sin i) {10 ** l_w11:.3f} ({l_w11 - l_vf:+.3f} dex)")
NUM["P6_sparc_alfalfa"] = P6

# ------------------------------------------------------------------ P7 molecular gas and H0-consistent distances (rows missing from PAPER40's Table 2)
P("\nP7 MOLECULAR GAS AND H0 (variants not in PAPER40's systematics table)")
P7 = {}
for k in (1, 0):
    for fh2 in (0.1, 0.3):
        ch = chain(a, k=k)
        Mb2 = ch["Mb"] + fh2 * a["mhi"]
        gb2 = G * Mb2 * MSUN / ch["R"] ** 2; D2 = (ch["V"] ** 2 / ch["R"]) / gb2
        l2 = s_star(D2, gb2, nu_mono)
        P7[f"k={k} M_H2={fh2:g} M_HI"] = a0(l2)
        P(f"  k={k}: M_H2 = {fh2:g} M_HI added to M_b (R unchanged): a0 {a0(l2):.3e} ({l2 - s_star(ch['D'], ch['gb'], nu_mono):+.3f} dex)")
    ch = chain(a, k=k, h0=67.4)
    l3 = s_star(ch["D"], ch["gb"], nu_mono)
    P7[f"k={k} H0=67.4"] = a0(l3)
    P(f"  k={k}: distances at H0 = 67.4 (the footing's H0): a0 {a0(l3):.3e}; kappa {0.5 * a0(l3) / A0C:.3f} / {0.5 * a0(l3) / A0A:.3f}")
NUM["P7_h2_h0"] = P7

json.dump(dict(lane="CFG306", script=os.path.basename(__file__), note="referee diagnostics; not frozen; not an a0 measurement; kappa = 1/2 FITTED", numbers=NUM),
          open(os.path.join(HERE, "cfg306_physics_checks_results.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, "cfg306_physics_checks.out"), "w").write(__doc__.strip() + "\n\n" + "\n".join(LOG) + "\n")
print("wrote cfg306_physics_checks.out and cfg306_physics_checks_results.json")
