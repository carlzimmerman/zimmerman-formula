#!/usr/bin/env python3
"""CFG485 POST-HOC VERIFICATION (written after the main run; no verdict weight; the frozen verdict is the main script's).
  V1  independent re-computation of the per-class M_gal-weighted unsettled fractions q = 1 - f in SI units: own M_b,true from CFG95's
      committed calibration constants (JSON, not exec), own cosmic age by quadrature, own matching of the LePhare rows.
  V2  independent chi2 for S, B2, B1 with the free two-halo amplitude, by Cholesky whitening + least squares, with the two-halo shape
      built from the g_bar bin edges alone (in CFG95's stack the template is exactly separable: T_k = const x h_k).
  V3  the no-two-halo chi2 (R7) from the stored model vectors.
  V4  what the data would need (a diagnostic, not a fit): the uniform late-type unsettled fraction c (early types fully settled) that
      best fits the split on top of the fully settled truncated model, with and without the free two-halo term, and the lambda that
      c implies at the median late-type proxy age and t_dyn.
  V5  the proxy's distribution: log sSFR and the share of lenses with t_age < 1 Gyr, per class.
Run: nice -n 15 python3 campaign_fresh_gravity/CFG485_kids_split_settling_completeness/cfg485_verify.py
"""
import os, sys, io, json, math, contextlib
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np
from scipy.integrate import quad
from scipy.stats import chi2 as CHI2
from astropy.io import fits

HERE = os.path.dirname(os.path.abspath(__file__))
CFGDIR = os.path.abspath(os.path.join(HERE, ".."))
REPO = os.path.abspath(os.path.join(CFGDIR, ".."))
LOG = []
def P(s=""):
    print(s, flush=True); LOG.append(s)
P(__doc__.split("Run: nice")[0].strip())
MAIN = json.load(open(os.path.join(HERE, "cfg485_settling_split_results.json")))["numbers"]
J95 = json.load(open(os.path.join(CFGDIR, "CFG95_kids_split_own_calibration_results.json")))["numbers"]
FOOTS = ("canonical", "alt"); SETS = ("released", "remeasured")
OUT = {}

# ------------------------------------------------------------------ V1: SI-unit re-computation of q
G = 6.67430e-11; MSUN = 1.98847e30; GYR = 3.15576e16; MPC = 3.0856775814913673e22   # GYR = seconds per Gyr
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
FB = 0.02237 / 0.14237
LR = os.path.join(REPO, "real_research", "data", "lensing_rar")
LN = np.load(os.path.join(LR, "lr_lenses.npz"))
lM, Mg, typ, zl = LN["logM"].astype(float), LN["Mgal"].astype(float), LN["typ"].astype(int), LN["z"].astype(float)
bs = fits.open(os.path.join(LR, "KiDS_DR4_brightsample.fits"), memmap=True)[1].data
lp = fits.open(os.path.join(LR, "KiDS_DR4_brightsample_LePhare.fits"), memmap=True)[1].data
# own matching: dictionary on rounded positions (different code path from CFG446's sorted-key search)
kb = {(round(float(a) * 1e7), round(float(d) * 1e7)): i for i, (a, d) in enumerate(zip(bs["RAJ2000"], bs["DECJ2000"]))}
ix = np.array([kb[(round(float(a) * 1e7), round(float(d) * 1e7))] for a, d in zip(LN["ra"], LN["dec"])])
mb_ = np.array(lp["MASS_BEST"][ix], "f8"); sb_ = np.array(lp["SFR_BEST"][ix], "f8")
H0 = 67.36 * 1e3 / MPC; Om = 0.3153; OL = 1 - Om
tU_tab_z = np.linspace(0.0, 1.0, 201)
tU_tab = np.array([quad(lambda a: 1.0 / (a * H0 * math.sqrt(Om / a ** 3 + OL)), 0.0, 1.0 / (1.0 + z), epsabs=0, epsrel=1e-12)[0] / GYR
                   for z in tU_tab_z])
TU = np.interp(zl, tU_tab_z, tU_tab)
bad = ~np.isfinite(mb_) | ~np.isfinite(sb_) | (mb_ < -90) | (sb_ < -90)
tage = np.where(bad, TU, np.minimum(10.0 ** np.clip(mb_ - sb_ - 9.0, -9, 3), TU))
EARLY, LATE = typ == 1, typ == 0
fcold = lambda lm: 10 ** (-0.69 * lm + 6.63)
s0, s1 = J95["sigma_fit"]["s0"], J95["sigma_fit"]["s1"]
v1 = {}
for foot in FOOTS:
    a_, b_ = J95["alpha"][foot]["a"], J95["alpha"][foot]["b"]
    de = a_ + b_ * (s0 + s1 * (lM + 0.25 - 11.0) - 2.3) + 0.25
    dl = math.log10(J95["Upsilon"][foot] / 0.5)
    d = np.where(EARLY, de, dl)
    Mb = 10 ** lM * (10 ** d + fcold(lM)) * MSUN                     # kg
    rM = np.sqrt(G * Mb / A0[foot]); re = rM / math.log(1 / (1 - FB))
    rho = (Mb / FB) / (4 * math.pi / 3 * re ** 3)
    x = np.sqrt(4 * math.pi * G * rho) * tage * GYR
    q = np.exp(-x)
    mine = dict(qe=float(np.sum(Mg[EARLY] * q[EARLY]) / np.sum(Mg[EARLY])), ql=float(np.sum(Mg[LATE] * q[LATE]) / np.sum(Mg[LATE])),
                qall=float(np.sum(Mg * q) / np.sum(Mg)))
    ref = {k: MAIN["primary"][foot][k] for k in ("qe", "ql", "qall")}
    dev = {k: abs(mine[k] / ref[k] - 1) for k in mine}
    v1[foot] = dict(mine=mine, main=ref, rel_dev=dev, tdyn_median_late_Gyr=float(np.median(1 / np.sqrt(4 * math.pi * G * rho[LATE]) / GYR)))
    P(f"  V1 {foot:9s}: q_early {mine['qe']:.4e} (main {ref['qe']:.4e}), q_late {mine['ql']:.4e} (main {ref['ql']:.4e}), "
      f"q_all {mine['qall']:.4e} (main {ref['qall']:.4e}); max rel. dev {max(dev.values()):.1e}")
OUT["V1"] = v1
OUT["V1_pass_1pct"] = all(max(v1[f]["rel_dev"].values()) < 0.01 for f in FOOTS)
P(f"  V1 agreement to 1%: {OUT['V1_pass_1pct']}")

# ------------------------------------------------------------------ CFG95 data/covariances (verified by the main run's C1)
_e = os.environ.get("MUTATE"); os.environ["MUTATE"] = "0"
p95 = os.path.join(CFGDIR, "CFG95_kids_split_own_calibration.py"); src = open(p95).read()
g95 = {"__file__": p95, "__name__": "lane95"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src[:src.index("# ================================================================== C1-C3")], "CFG95", "exec"), g95)
os.environ.pop("MUTATE") if _e is None else os.environ.__setitem__("MUTATE", _e)
CD, CK, HART, DOBS, DREM, EDGES, SUB, K1 = (g95[k] for k in ("CD", "CK", "HART", "DOBS", "DREM", "EDGES", "SUB", "K1"))
COV = {"released": (CD, 1.0), "remeasured": (CK, HART)}
DAT = {"released": DOBS, "remeasured": DREM}

# ------------------------------------------------------------------ V2: whitened least squares, template shape from the bin edges
h = np.zeros(15)
for k in range(15):
    lg = np.linspace(math.log(EDGES[k]), math.log(EDGES[k + 1]), SUB + 1); gs = np.exp(0.5 * (lg[1:] + lg[:-1]))
    h[k] = np.sum(gs ** -1 * gs ** 0.4) / np.sum(gs ** -1)
T = h[np.array(K1)]


def chi2_wls(d, m, cov, hart, with2h=True):
    L = np.linalg.cholesky(cov / hart)                     # C' = C / hart  =>  C'^-1 = hart C^-1
    r = np.linalg.solve(L, d - m)
    if not with2h:
        return float(r @ r), 0.0
    t = np.linalg.solve(L, T)
    A, *_ = np.linalg.lstsq(t[:, None], r, rcond=None)
    rr = r - t * A[0]
    return float(rr @ rr), float(A[0])


v2 = {}; worst = 0.0; worst3 = 0.0
for foot in FOOTS:
    pr = MAIN["primary"][foot]
    DS, DB2, DB1 = (np.array(pr[k]) for k in ("DS", "DB2", "DB1"))
    for s_ in SETS:
        cov, hart = COV[s_]
        mine = {nm: chi2_wls(DAT[s_], D, cov, hart)[0] for nm, D in (("S", DS), ("B2", DB2), ("B1", DB1))}
        none = {nm: chi2_wls(DAT[s_], D, cov, hart, False)[0] for nm, D in (("S", DS), ("B2", DB2), ("B1", DB1))}
        ref = {"S": pr[s_]["chi2_S"], "B2": pr[s_]["chi2_B2"], "B1": pr[s_]["chi2_B1"]}
        refn = {"S": pr[s_]["nofree_S"], "B2": pr[s_]["nofree_B2"], "B1": pr[s_]["nofree_B1"]}
        worst = max(worst, max(abs(mine[k] - ref[k]) for k in mine)); worst3 = max(worst3, max(abs(none[k] - refn[k]) for k in none))
        v2[f"{foot}|{s_}"] = dict(free2h=mine, none=none)
        P(f"  V2/V3 {foot:9s} {s_:10s}: free 2h S {mine['S']:.4f} B2 {mine['B2']:.4f} B1 {mine['B1']:.4f} (p_B1 {CHI2.sf(mine['B1'], 6):.3f}) | "
          f"no 2h S {none['S']:.3f} B2 {none['B2']:.3f} B1 {none['B1']:.3f} (p_B1 {CHI2.sf(none['B1'], 7):.1e})")
OUT["V2"] = v2; OUT["V2_max_abs_dev"] = worst; OUT["V3_max_abs_dev"] = worst3
P(f"  V2 max |chi2 - main| (free 2h, independent template shape) {worst:.1e}; V3 (no 2h) {worst3:.1e}")
P("  (D_S here is the stored vector, i.e. D_B2 + increment rounded to float64: the S-B2 difference below 1e-12 is not resolved by V2)")

# ------------------------------------------------------------------ V4: what the data would need (diagnostic)
_m = os.environ.get("CFG485_MUTATE"); os.environ["CFG485_MUTATE"] = "0"
pm = os.path.join(HERE, "cfg485_settling_split.py"); srcm = open(pm).read()
gm = {"__file__": pm, "__name__": "cfg485_main_prefix"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(srcm[:srcm.index("# ================================================================== per-lens settled fractions")], "cfg485", "exec"), gm)
os.environ.pop("CFG485_MUTATE") if _m is None else os.environ.__setitem__("CFG485_MUTATE", _m)
parts, CBE, idx = gm["parts"], gm["CBE"], gm["idx"]
v4 = {}
for foot in FOOTS:
    Phl, Barl, _, _ = parts(CBE[(foot, 0)]); Phe, Bare, _, _ = parts(CBE[(foot, 1)])
    D0 = ((Phe + Bare) - (Phl + Barl))[idx]             # fully settled truncated model
    U = Phl[idx]                                        # D rises by c * (late phantom) if late types are unsettled by c
    tdyn_l = v1[foot]["tdyn_median_late_Gyr"]; tage_l = float(np.median(tage[LATE]))
    for s_ in SETS:
        cov, hart = COV[s_]
        Ci = hart * np.linalg.inv(cov)
        for with2h in (True, False):
            X = np.stack([U, T], 1) if with2h else U[:, None]
            F = X.T @ Ci @ X; beta = np.linalg.solve(F, X.T @ Ci @ (DAT[s_] - D0)); cv = np.linalg.inv(F)
            c, sc = float(beta[0]), float(math.sqrt(cv[0, 0]))
            r = DAT[s_] - D0 - X @ beta; x2 = float(r @ Ci @ r)
            lam = (math.log(1 / c) * tdyn_l / tage_l) if 0 < c < 1 else float("nan")
            v4[f"{foot}|{s_}|{'2h' if with2h else 'no2h'}"] = dict(c=c, sig=sc, chi2=x2, dof=7 - X.shape[1], lam_needed=lam)
            P(f"  V4 {foot:9s} {s_:10s} {'free 2h' if with2h else 'no 2h  '}: needed late-type unsettled fraction c = {c:.3f} +- {sc:.3f} "
              f"(chi2 {x2:.2f}/{7 - X.shape[1]}); predicted M_gal-mean q_late {MAIN['primary'][foot]['ql']:.1e}; "
              f"lambda at median late t_age {tage_l:.2f} Gyr, t_dyn {tdyn_l:.3f} Gyr: {lam:.3f}")
OUT["V4"] = v4

# ------------------------------------------------------------------ V5: proxy distribution
lss = np.where(bad, np.nan, sb_ - mb_)
v5 = {}
for nm, m in (("early", EARLY), ("late", LATE)):
    v5[nm] = dict(log_sSFR_pct=np.nanpercentile(lss[m], [5, 25, 50, 75, 95]).tolist(), frac_tage_lt_1Gyr=float(np.mean(tage[m] < 1.0)),
                  frac_tage_lt_0p3Gyr=float(np.mean(tage[m] < 0.3)))
    P(f"  V5 {nm:5s}: log sSFR [/yr] 5/25/50/75/95% {np.round(v5[nm]['log_sSFR_pct'], 2).tolist()}; share t_age < 1 Gyr {v5[nm]['frac_tage_lt_1Gyr']:.3f}, "
      f"< 0.3 Gyr {v5[nm]['frac_tage_lt_0p3Gyr']:.3f}")
OUT["V5"] = v5
json.dump(OUT, open(os.path.join(HERE, "cfg485_verify_results.json"), "w"), indent=1)
open(os.path.join(HERE, "cfg485_verify.out"), "w").write("\n".join(LOG) + "\n")
