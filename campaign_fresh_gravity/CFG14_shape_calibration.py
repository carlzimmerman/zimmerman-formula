#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG14 -- IS P2's TRANSITION SHAPE EXCLUDED BY SPARC ONCE THE SHAPE ESTIMATOR IS CALIBRATED?

WHY.  CFG4 H3 (committed) fits the transition sharpness beta of nu_beta = (1 + y^-beta)^(1/2beta) to all 175 SPARC galaxies (the
record's statistic, one global Upsilon profiled) and finds beta = 0.48 (canonical) / 0.55 (alt), with P2 (beta = 1) outside the
galaxy-bootstrap 95% band.  CFG13's bias control showed the estimator returns beta ~ 0.55-0.59 for data that ARE P2 by construction.
A galaxy bootstrap measures the estimator's spread, not its bias.  The calibrated question: where does the REAL beta-hat fall in the
distribution beta-hat takes when the truth is P2, and when it is nu_mono (the contract kernel)?

THE ESTIMATOR: CFG4 H3's exactly (beta on its 49-point grid, Upsilon profiled on 0.30-1.20, the record's weights).
THE TRUTHS: P2 at its CFG4 best Upsilon (0.70 / 0.65), nu_mono at its (0.61 / 0.57).
THE NOISE (two declared models; 60 realizations each, seeds 1400-1459):
  A  per-galaxy offset N(0, 0.08 dex) on g_obs + per-point N(0, 2 eV/(V ln 10)) from SPARC's own velocity errors.
  B  per-galaxy stellar Upsilon scatter N(0, 0.10 dex) in the TRUTH's g_bar (the fit keeps one global Upsilon) + per-galaxy distance
     offset N(0, 0.08 dex) on g_obs + the same per-point errors.

PRE-DECLARED (before this script's first run)
  C1  CONTROL  the real data's beta-hat and Upsilon reproduce CFG4 H3's committed best (0.4847 / 0.5533; 0.44 / 0.46).
  C2  CONTROL  noiseless truths: P2 returns the grid point nearest 1 and its own Upsilon exactly (the estimator is unbiased without
      noise); nu_mono's noiseless beta-hat is reported.
  H1  [HEADLINE; MUTATE must fail] after calibration P2 is NOT excluded: the real beta-hat lies inside the central 95% of the
      P2-truth beta-hat distribution under BOTH noise models, both footings.  Expectation: uncertain.
  H2  nu_mono is not excluded: the real beta-hat inside the central 95% of the nu_mono-truth distribution, both models, both footings.
  R1  (reported) the bias (median beta-hat minus the truth's noiseless beta-hat), two-sided p-values of the real beta-hat under each
      truth, and the same calibration for CFG13's point-mass and embedded subsets (model A).
MUTATE=1: the noise is switched off (both models) -- the P2-truth distribution collapses onto beta = 1 and H1 must FAIL (rc = 1).
Run: python3 campaign_fresh_gravity/CFG14_shape_calibration.py   (MUTATE=1 for the control; a few minutes)
"""
import os, sys, math, json
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import CFG7_common as C7
C = C7.C4
MUTATE = os.environ.get("MUTATE", "0") == "1"
R = C7.Report("CFG14_shape_calibration", MUTATE)
P, check = R.P, R.check
P(__doc__.split("Run: python3")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: noise switched off -- H1 must FAIL ***")
np.seterr(all="ignore")
GL = json.load(open(os.path.join(HERE, "CFG4_galaxy_law_results.json")))["numbers"]
C13 = json.load(open(os.path.join(HERE, "CFG13_pointmass_shape_results.json")))["numbers"]["fits"]
A0 = C.A0

GAL = C.load_sparc()
NG = len(GAL)
UPS = np.round(np.arange(0.30, 1.2001, 0.01), 2)
KPC_S = 3.0857e19
Rm = np.concatenate([g["R"] for g in GAL]) * KPC_S
Vo = np.concatenate([g["Vobs"] for g in GAL])
eV = np.concatenate([g["eV"] for g in GAL])
Vg = np.concatenate([g["Vgas"] for g in GAL])
Vd = np.concatenate([g["Vdisk"] for g in GAL])
Vb = np.concatenate([g["Vbul"] for g in GAL])
GI = np.concatenate([np.full(len(g["R"]), i) for i, g in enumerate(GAL)])
VB2 = np.sign(Vg)[:, None] * Vg[:, None] ** 2 + UPS[None, :] * Vd[:, None] ** 2 + 1.4 * UPS[None, :] * Vb[:, None] ** 2
GB = VB2 * 1e6 / Rm[:, None]
GO_REAL = (Vo * 1e3) ** 2 / Rm
OK = (GB > 0) & (GO_REAL[:, None] > 0) & np.isfinite(GB) & (Vo > 0)[:, None]
WPT = (1.0 / (np.clip(eV, 1, None) / np.clip(Vo, 1, None)) ** 2)
WW = np.where(OK, WPT[:, None], 0.0)
BETAS = np.round(np.geomspace(0.25, 6.0, 49), 4)
J1 = int(np.argmin(np.abs(BETAS - 1.0)))
SIGP = 2.0 * np.clip(eV, 1, None) / np.clip(Vo, 1, None) / math.log(10)                  # per-point log10 error of g_obs
NREAL = 60

# the prediction table: log10(nu_beta(g_bar/a0) g_bar) for every beta, point and Upsilon (independent of the data)
LP = {}
for f in C.FOOTS:
    x = np.where(OK, GB, 1.0)
    LP[f] = np.stack([np.log10(C.nu_beta(x / A0[f], b) * x) for b in BETAS]).astype(np.float64)   # (nbeta, npts, NU)
Wsum = WW.sum(0)


def fit_beta(lgo, f, mask=None):
    """CFG4 H3's point estimate on log10 g_obs = lgo (per point): beta-hat and Upsilon-hat (global, profiled)."""
    w = WW if mask is None else WW * mask[:, None]
    ws = w.sum(0)
    a = (w * (lgo ** 2)[:, None]).sum(0)
    b = np.einsum("pu,p,kpu->ku", w, lgo, LP[f], optimize=True)
    c = np.einsum("pu,kpu->ku", w, LP[f] ** 2, optimize=True)
    mse = (a[None, :] - 2 * b + c) / ws[None, :]
    k, u = np.unravel_index(int(np.argmin(mse)), mse.shape)
    return float(BETAS[k]), float(UPS[u]), float(math.sqrt(mse[k, u]))


def truth_lgo(kname, f, model, rng, noise=True):
    U = GL["H2"][f"{f}|{kname}"]["U"]
    if model == "B" and noise:
        ug = U * 10 ** rng.normal(0.0, 0.10, NG)
        vb2 = np.sign(Vg) * Vg ** 2 + ug[GI] * Vd ** 2 + 1.4 * ug[GI] * Vb ** 2
    else:
        vb2 = np.sign(Vg) * Vg ** 2 + U * Vd ** 2 + 1.4 * U * Vb ** 2
    gb = vb2 * 1e6 / Rm
    with np.errstate(all="ignore"):
        g = np.where(gb > 0, C.KERNELS[kname](np.where(gb > 0, gb, 1.0) / A0[f]) * gb, GO_REAL)
    lg = np.log10(g)
    if noise:
        lg = lg + rng.normal(0.0, 0.08, NG)[GI] + rng.normal(0.0, 1.0, len(Rm)) * SIGP
    return lg


# ================================================================================================ C1, C2
R.banner("C1 / C2  CONTROLS: the real beta-hat, and noiseless truths")
LGO_REAL = np.log10(GO_REAL)
REAL = {f: fit_beta(LGO_REAL, f) for f in C.FOOTS}
dev1 = all(abs(REAL[f][0] - GL["H3"][f]["best_beta"]) < 1e-9 and abs(REAL[f][1] - GL["H3"][f]["U_best"]) < 1e-9 for f in C.FOOTS)
check("C1 CONTROL: the real beta-hat and Upsilon reproduce CFG4 H3's committed best",
      "; ".join(f"{f}: beta {REAL[f][0]} (CFG4 {GL['H3'][f]['best_beta']}), U {REAL[f][1]} ({GL['H3'][f]['U_best']})" for f in C.FOOTS), dev1)
NL = {}
for f in C.FOOTS:
    for kn in ("P2", "nu_mono"):
        NL[(f, kn)] = fit_beta(truth_lgo(kn, f, "A", None, noise=False), f)
        P(f"    noiseless {f:9s} {kn:8s}: beta-hat {NL[(f, kn)][0]:.4f}, U {NL[(f, kn)][1]:.2f} (truth U {GL['H2'][f'{f}|{kn}']['U']:.2f}), "
          f"rms {NL[(f, kn)][2]:.2e}")
c2 = all(NL[(f, "P2")][0] == BETAS[J1] and abs(NL[(f, "P2")][1] - GL["H2"][f"{f}|P2"]["U"]) < 1e-9 for f in C.FOOTS)
check("C2 CONTROL: noiseless P2 returns beta = the grid point nearest 1 and its own Upsilon (the estimator is unbiased without noise)",
      "; ".join(f"{f}: P2 {NL[(f, 'P2')][0]:.4f}@{NL[(f, 'P2')][1]:.2f}, nu_mono {NL[(f, 'nu_mono')][0]:.4f}@{NL[(f, 'nu_mono')][1]:.2f}"
                for f in C.FOOTS), c2)

# ================================================================================================ the calibration
R.banner("THE CALIBRATION: the distribution of beta-hat under each truth, two noise models")
PM = np.zeros(len(Rm), bool); EMB = np.zeros(len(Rm), bool)
Vb2s = np.sign(Vg) * Vg ** 2 + 0.5 * Vd ** 2 + 0.7 * Vb ** 2
Mb = Vb2s * Rm
off = 0
for g in GAL:
    n = len(g["R"]); sl = slice(off, off + n); mb = Mb[sl]
    with np.errstate(all="ignore"):
        rt = np.where(mb > 0, mb[-1] / mb, np.nan)
    PM[sl] = np.isfinite(rt) & (rt <= 1.10); EMB[sl] = np.isfinite(rt) & (rt >= 1.5)
    off += n
DIST = {}
for f in C.FOOTS:
    for kn in ("P2", "nu_mono"):
        for model in ("A", "B"):
            bs, bpm, bemb = [], [], []
            for s in range(NREAL):
                rng = np.random.default_rng(1400 + s)
                lg = truth_lgo(kn, f, model, rng, noise=not MUTATE)
                bs.append(fit_beta(lg, f)[0])
                if model == "A":
                    bpm.append(fit_beta(lg, f, PM)[0]); bemb.append(fit_beta(lg, f, EMB)[0])
            bs = np.array(bs)
            lo, hi = np.percentile(bs, [2.5, 97.5])
            breal = REAL[f][0]
            p2s = 2 * min(np.mean(bs <= breal), np.mean(bs >= breal))
            DIST[(f, kn, model)] = dict(median=float(np.median(bs)), lo95=float(lo), hi95=float(hi), p_two_sided=float(min(1.0, p2s)),
                                        inside=bool(lo <= breal <= hi), bias=float(np.median(bs) - NL[(f, kn)][0]),
                                        pm=bpm, emb=bemb)
            v = DIST[(f, kn, model)]
            P(f"    {f:9s} truth {kn:8s} model {model}: beta-hat median {v['median']:.3f}, central 95% [{v['lo95']:.3f}, {v['hi95']:.3f}] "
              f"(bias {v['bias']:+.3f}); the real beta-hat {breal:.4f}: {'INSIDE' if v['inside'] else 'outside'} (p = {v['p_two_sided']:.3f})")
h1 = all(DIST[(f, "P2", m)]["inside"] for f in C.FOOTS for m in ("A", "B"))
check("H1 [HEADLINE] after calibration P2 is NOT excluded: the real beta-hat lies inside the central 95% of the P2-truth "
      "distribution under both noise models, both footings" + ("  [MUTATE: no noise]" if MUTATE else ""),
      "; ".join(f"{f[:3]}/{m}: [{DIST[(f, 'P2', m)]['lo95']:.2f}, {DIST[(f, 'P2', m)]['hi95']:.2f}] vs {REAL[f][0]:.2f} "
                f"(p {DIST[(f, 'P2', m)]['p_two_sided']:.2f})" for f in C.FOOTS for m in ("A", "B")), h1)
h2 = all(DIST[(f, "nu_mono", m)]["inside"] for f in C.FOOTS for m in ("A", "B"))
check("H2 nu_mono is not excluded: the real beta-hat inside the central 95% of the nu_mono-truth distribution, both models, both "
      "footings", "; ".join(f"{f[:3]}/{m}: [{DIST[(f, 'nu_mono', m)]['lo95']:.2f}, {DIST[(f, 'nu_mono', m)]['hi95']:.2f}] "
                             f"(p {DIST[(f, 'nu_mono', m)]['p_two_sided']:.2f})" for f in C.FOOTS for m in ("A", "B")), h2)
sub = []
for f in C.FOOTS:
    for kn in ("P2", "nu_mono"):
        v = DIST[(f, kn, "A")]
        for lab, arr, key in (("point-mass", v["pm"], "PM"), ("embedded", v["emb"], "EMB")):
            lo, hi = np.percentile(arr, [2.5, 97.5]) if len(arr) else (np.nan, np.nan)
            real = C13[f"{f}|{key}"]["best_beta"]
            sub.append((f, kn, lab, float(np.median(arr)), float(lo), float(hi), real, bool(lo <= real <= hi)))
            P(f"    {f:9s} truth {kn:8s} {lab:10s} (model A): median {np.median(arr):.3f}, 95% [{lo:.3f}, {hi:.3f}]; CFG13's real "
              f"{real:.3f}: {'inside' if lo <= real <= hi else 'outside'}")
check("R1 (reported) the bias and p-values above; CFG13's subsets under the same calibration (model A)",
      "; ".join(f"{s[0][:3]}/{s[1]}/{s[2]}: [{s[4]:.2f}, {s[5]:.2f}] vs {s[6]:.2f} {'in' if s[7] else 'OUT'}" for s in sub), True,
      load_bearing=False)
R.num("real", REAL)
R.num("noiseless", {f"{k[0]}|{k[1]}": v for k, v in NL.items()})
R.num("dist", {f"{k[0]}|{k[1]}|{k[2]}": {kk: vv for kk, vv in v.items() if kk not in ("pm", "emb")} for k, v in DIST.items()})
R.num("subsets", [dict(footing=s[0], truth=s[1], subset=s[2], median=s[3], lo95=s[4], hi95=s[5], real=s[6], inside=s[7]) for s in sub])
nf = R.write()
sys.exit(1 if nf else 0)
