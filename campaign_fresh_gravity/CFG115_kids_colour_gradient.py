#!/usr/bin/env python3
"""CFG115 -- IS THE KiDS COLOUR DEPENDENCE AT FIXED g_bar A STEP OR A GRADIENT?  Six within-class colour-tertile bins of the isolated KiDS
lenses (the June lens stage's own LePhare rest-frame u - r, split at 2.0), common-weight lensing amplitudes over the 1-halo bins K1,
leave-one-patch-out jackknife; B's null (no colour dependence), a step at the valley, a linear gradient, and a step plus a within-class slope.

Criteria frozen and committed before any colour-binned lensing number: campaign_fresh_gravity/CFG115_FROZEN_CRITERIA.md (e416f3bea).
  data     cfg110_perlens.npz + lr_lenses.npz + June patch labels (CFG110's script exec'd read-only up to its model controls, MUTATE forced 0);
           u - r = MAG_ABS_u - MAG_ABS_r (KiDS_DR4_brightsample_LePhare.fits, row-aligned with KiDS_DR4_brightsample.fits), matched by exact
           (RA, Dec).  Bins: each class at its own colour tertiles.  A_c = log10(sum_k w_k ESD_ck / sum_k w_k ESD_all,k), w_k = the full sample's
           pair weights (the same for every bin), K1 = bins 8-14.
PRE-DECLARED (from the frozen file)
  C1  CONTROL  every lens matches the bright sample by exact position and (u - r > 2.0) reproduces lr_lenses' typ for every lens.
  C2  CONTROL  the six bins partition the sample; their summed K1 sums reproduce the full-sample and per-class sums (relative 1e-12).
  C3  CONTROL  200 random equal-count thirds per class: mean Hartlap chi2 of the within-class constancy test (4 dof) in [2.5, 5.5].
  R0  POWER (printed before any colour-bin amplitude): expected Delta chi2 of the within-class slope test for a pure linear gradient with the
               observed class difference, beta_true = (s_E - s_L) / (u_E - u_L); lambda >= 9 means a gradient of that size is distinguishable.
  H1  [HEADLINE; MUTATE must fail] a step: within each class the three amplitudes are constant (Hartlap chi2, 4 dof, p > 0.05) and
               Delta chi2(step - step+slope) < 4.
  R1-R5 (reported): B's null; the fits; the outer-tertile contrasts (boundary tertiles out); per-bin medians and profiles; the models'
               predicted amplitudes (B, colour-split LCDM, colour-blind Moster).
  R6  (POST HOC, added after the first run; reported only) the same amplitudes against a FIXED (non-jackknifed) full-sample reference:
               the frozen definition's jackknifed denominator leaves a near-null covariance direction (a normalisation constraint) that
               inflates zero-offset rows (R1, R5); the fixed reference is well-conditioned and every model gets a free common offset.
               Every other line of both logs is unchanged apart from timing.
MUTATE=1: every lens's K1 wgE x 10^(beta_inj (u - r - u_class)), beta_inj = (s_E - s_L)/(u_E - u_L) from the unmodified data -- H1 must FAIL.
Run: python3 campaign_fresh_gravity/CFG115_kids_colour_gradient.py   (MUTATE=1 for the control; about 3 minutes)
"""
import os, sys, io, math, contextlib
import numpy as np
from scipy import stats
from astropy.io import fits

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import CFG7_common as C
MUTATE = os.environ.get("MUTATE", "0") == "1"
R = C.Report("CFG115_kids_colour_gradient", MUTATE)
P, check = R.P, R.check
P(__doc__.split("Run: python3")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: a within-class colour gradient of the class-difference slope injected into the data -- H1 must FAIL ***")

_e = os.environ.get("MUTATE"); os.environ["MUTATE"] = "0"
F110 = os.path.join(HERE, "CFG110_kids_mass_split.py")
src = open(F110).read()
g110 = {"__file__": F110, "__name__": "cfg110"}
try:
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(src[:src.index('R.banner("C3  CONTROL (models)")')], "CFG110", "exec"), g110)
finally:
    os.environ.pop("MUTATE") if _e is None else os.environ.__setitem__("MUTATE", _e)
WG, WW, patch, typ, Mgal, zlen, K1, NPAT = (g110[k] for k in ("WG", "WW", "patch", "typ", "Mgal", "zlen", "K1", "NPAT"))
esd_and_loo, law_stack, lcdm_stack, LN = g110["esd_and_loo"], g110["law_stack"], g110["lcdm_stack"], g110["LN"]
NL = len(typ)
ALL = np.ones(NL, bool)
HART6, HART2 = (NPAT - 6 - 2) / (NPAT - 1), (NPAT - 2 - 2) / (NPAT - 1)
NAMES = ["L1", "L2", "L3", "E1", "E2", "E3"]

# ================================================================== C1: the colours
R.banner("C1 / C2  CONTROLS (colours and partition)")
LR = os.path.join(C.REPO, "real_research", "data", "lensing_rar")
bs = fits.open(os.path.join(LR, "KiDS_DR4_brightsample.fits"), memmap=True)[1].data
lp = fits.open(os.path.join(LR, "KiDS_DR4_brightsample_LePhare.fits"), memmap=True)[1].data
ids_ok = bool(np.array_equal(bs["ID"], lp["ID"]))
ra, dec = np.array(bs["RAJ2000"], "f8"), np.array(bs["DECJ2000"], "f8")
key = lambda a, d: np.round(a * 1e7).astype(np.int64) * 10 ** 10 + np.round((d + 90) * 1e7).astype(np.int64)
kb, kl = key(ra, dec), key(LN["ra"], LN["dec"])
order = np.argsort(kb, kind="stable"); ks = kb[order]
pos = np.minimum(np.searchsorted(ks, kl), len(ks) - 1)
idx = order[pos]
matched = bool(np.all(ks[pos] == kl)) and bool(np.all(ra[idx] == LN["ra"])) and bool(np.all(dec[idx] == LN["dec"]))
ur = np.array(lp["MAG_ABS_u"][idx] - lp["MAG_ABS_r"][idx], "f8")
typ_ok = bool(np.array_equal((ur > 2.0).astype(int), typ))
check("C1 CONTROL: every lens matches the bright sample by exact (RA, Dec) (IDs row-aligned) and (u - r > 2.0) reproduces lr_lenses' typ for every lens",
      f"{NL:,} lenses; IDs aligned {ids_ok}; exact match {matched}; typ reproduced {typ_ok}; u - r finite {bool(np.isfinite(ur).all())}",
      ids_ok and matched and typ_ok and bool(np.isfinite(ur).all()))

ED = {c: np.percentile(ur[typ == c], [100 / 3, 200 / 3]) for c in (0, 1)}
BIN = np.full(NL, -1)
for c in (0, 1):
    m = typ == c
    BIN[m & (ur < ED[c][0])] = 3 * c
    BIN[m & (ur >= ED[c][0]) & (ur < ED[c][1])] = 3 * c + 1
    BIN[m & (ur >= ED[c][1])] = 3 * c + 2
MASKS = [BIN == i for i in range(6)]
UMED = np.array([np.median(ur[m]) for m in MASKS])
UCLS = {c: float(np.median(ur[typ == c])) for c in (0, 1)}
tot = WG[:, K1].sum(0)
s6 = sum(WG[m][:, K1].sum(0) for m in MASKS)
dev = float(np.max(np.abs(s6 / tot - 1)))
for c in (0, 1):
    dev = max(dev, float(np.max(np.abs(sum(WG[m][:, K1].sum(0) for m in MASKS[3 * c:3 * c + 3]) / WG[typ == c][:, K1].sum(0) - 1))))
part = bool(np.all(BIN >= 0)) and sum(int(m.sum()) for m in MASKS) == NL
check("C2 CONTROL: the six bins partition the sample; their summed K1 sums reproduce the full-sample and per-class sums (relative 1e-12)",
      f"partition {part}; max relative deviation {dev:.1e}; tertile edges late {np.round(ED[0], 3).tolist()}, early {np.round(ED[1], 3).tolist()}",
      part and dev < 1e-12)

# ================================================================== the amplitudes and their jackknife
WK = WW[:, K1].sum(0)


def amps(wg, masks=MASKS):
    ea, la = esd_and_loo(ALL, wg)
    den, denl = float((WK * ea).sum()), (WK[None] * la).sum(1)
    A, AL = [], []
    for m in masks:
        e, l = esd_and_loo(m, wg)
        A.append(math.log10(float((WK * e).sum()) / den)); AL.append(np.log10((WK[None] * l).sum(1) / denl))
    return np.array(A), np.array(AL).T


def jcov(AL):
    d = AL - AL.mean(0)
    return (AL.shape[0] - 1) / AL.shape[0] * d.T @ d


def gls(A, Ci, X):
    F = X.T @ Ci @ X
    th = np.linalg.solve(F, X.T @ Ci @ A)
    r = A - X @ th
    return th, np.linalg.inv(F), float(r @ Ci @ r)


cls = np.array([0, 0, 0, 1, 1, 1])
X_step = np.stack([(cls == 0).astype(float), (cls == 1).astype(float)], 1)
X_grad = np.stack([np.ones(6), UMED - 2.0], 1)
X_ss = np.column_stack([X_step, UMED - np.where(cls == 0, UCLS[0], UCLS[1])])

WGu = WG.copy()
A_cls, _ = amps(WGu, [typ == 0, typ == 1])
BETA_TRUE = (A_cls[1] - A_cls[0]) / (UCLS[1] - UCLS[0])
WGx = WGu
if MUTATE:
    fac = 10 ** (BETA_TRUE * (ur - np.where(typ == 0, UCLS[0], UCLS[1])))
    WGx = WGu.copy(); WGx[:, K1] = WGu[:, K1] * fac[:, None]
    P(f"    MUTATE: beta_inj = {BETA_TRUE:+.4f} dex per mag injected within each class (factor range {fac.min():.3f}-{fac.max():.3f})")
A6, AL6 = amps(WGx)
C6 = jcov(AL6)
Ci6 = HART6 * np.linalg.inv(C6)

# ================================================================== C3 and R0 (before any colour-bin amplitude is printed)
R.banner("C3 / R0  COVARIANCE CALIBRATION AND POWER (printed before the colour-bin amplitudes)")
rng = np.random.default_rng(115)
nulls = []
for t in range(200):
    rb = np.full(NL, -1)
    for c in (0, 1):
        ii = rng.permutation(np.where(typ == c)[0])
        for j, part_ in enumerate(np.array_split(ii, 3)):
            rb[part_] = 3 * c + j
    An, ALn = amps(WGx, [rb == i for i in range(6)])
    nulls.append(gls(An, HART6 * np.linalg.inv(jcov(ALn)), X_step)[2])
mn = float(np.mean(nulls))
check("C3 CONTROL: mean Hartlap chi2 of the within-class constancy test (4 dof) over 200 random equal-count thirds in [2.5, 5.5]",
      f"mean {mn:.2f}, median {np.median(nulls):.2f}, fraction p < 0.05: {np.mean([stats.chi2.sf(x, 4) < 0.05 for x in nulls]):.3f}", 2.5 <= mn <= 5.5)
A_true = (A_cls[0] + A_cls[1]) / 2 + BETA_TRUE * (UMED - (UCLS[0] + UCLS[1]) / 2)
lam = gls(A_true, Ci6, X_step)[2]
sig_b = math.sqrt(gls(A_true, Ci6, X_ss)[1][2, 2])
check("R0 (reported) POWER: expected Delta chi2 of the within-class slope test for a pure linear gradient with the class difference (lambda >= 9 = distinguishable)",
      f"class amplitudes late {A_cls[0]:+.4f}, early {A_cls[1]:+.4f} (the known split); class median u-r {UCLS[0]:.3f} / {UCLS[1]:.3f}; beta_true {BETA_TRUE:+.4f} dex/mag; "
      f"sigma(beta_w) {sig_b:.4f}; lambda = {lam:.2f}; jackknife sigma of the six amplitudes {np.round(np.sqrt(np.diag(C6)), 4).tolist()}", True, load_bearing=False)

# ================================================================== H1
R.banner("H1  STEP OR GRADIENT (six within-class colour-tertile amplitudes over K1)")
P("    bin   N        med u-r   A_c        +- jk")
for i in range(6):
    P(f"    {NAMES[i]}    {int(MASKS[i].sum()):7,}  {UMED[i]:6.3f}   {A6[i]:+.4f}   {math.sqrt(C6[i, i]):.4f}")
th_s, cov_s, x_s = gls(A6, Ci6, X_step)
th_g, cov_g, x_g = gls(A6, Ci6, X_grad)
th_w, cov_w, x_w = gls(A6, Ci6, X_ss)
p_s = float(stats.chi2.sf(x_s, 4))
dx = x_s - x_w
h1 = (p_s > 0.05) and (dx < 4)
check("H1 [HEADLINE] A STEP: within each class the three amplitudes are constant (4 dof, p > 0.05) and Delta chi2(step - step+slope) < 4"
      + ("  [MUTATE: gradient injected]" if MUTATE else ""),
      f"step chi2 {x_s:.2f}/4 (p {p_s:.3f}); within-class slope beta_w {th_w[2]:+.4f} +- {math.sqrt(cov_w[2, 2]):.4f} dex/mag, Delta chi2 {dx:.2f}", h1)

# ================================================================== reported rows
R.banner("REPORTED ROWS")
x0 = float(A6 @ Ci6 @ A6)
check("R1 (reported) B's law (no colour dependence, A_c = 0): chi2, 6 dof", f"{x0:.2f}/6 (p {stats.chi2.sf(x0, 6):.2e})", True, load_bearing=False)
check("R2 (reported) the fits: step, gradient, step + within-class slope",
      f"step: s_L {th_s[0]:+.4f}, s_E {th_s[1]:+.4f}, s_E - s_L {th_s[1] - th_s[0]:+.4f} +- {math.sqrt(cov_s[0, 0] + cov_s[1, 1] - 2 * cov_s[0, 1]):.4f}, chi2 {x_s:.2f}/4; "
      f"gradient: alpha {th_g[0]:+.4f}, beta {th_g[1]:+.4f} +- {math.sqrt(cov_g[1, 1]):.4f}, chi2 {x_g:.2f}/4; step+slope chi2 {x_w:.2f}/3; "
      f"chi2(step) - chi2(gradient) = {x_s - x_g:+.2f}", True, load_bearing=False)
D2 = np.array([A6[0] - A6[1], A6[5] - A6[4]]); DL2 = np.stack([AL6[:, 0] - AL6[:, 1], AL6[:, 5] - AL6[:, 4]], 1)
C2m = jcov(DL2); x2o = float(D2 @ (HART2 * np.linalg.inv(C2m)) @ D2)
check("R3 (reported) the outer-tertile contrasts (boundary tertiles L3, E1 left out): A(L1) - A(L2), A(E3) - A(E2); chi2 against zero, 2 dof",
      f"{D2[0]:+.4f} +- {math.sqrt(C2m[0, 0]):.4f}, {D2[1]:+.4f} +- {math.sqrt(C2m[1, 1]):.4f}; chi2 {x2o:.2f}/2 (p {stats.chi2.sf(x2o, 2):.3f})", True, load_bearing=False)
rows = []
for i, m in enumerate(MASKS):
    e, l = esd_and_loo(m, WGx)
    rows.append(f"{NAMES[i]}: N {int(m.sum()):,}, u-r {UMED[i]:.3f}, log M_gal {np.median(np.log10(Mgal[m])):.3f}, z {np.median(zlen[m]):.3f}, "
                f"ESD {np.round(e, 1).tolist()}")
check("R4 (reported) per bin: N, median u - r, median log M_gal, median z, ESD over K1 (Msun/pc^2)", "; ".join(rows), True, load_bearing=False)
wcls = {c: WW[typ == c][:, K1].sum(0) for c in (0, 1)}


def model_amps(fn_bin, ref):
    out = []
    for i, m in enumerate(MASKS):
        e = fn_bin(m, i)[K1]
        out.append(math.log10(float((WK * e).sum()) / float((WK * ref).sum())))
    return np.array(out)


refB = law_stack(ALL, "canonical")[K1]
refL = (wcls[0] * lcdm_stack(typ == 0, "blue")[K1] + wcls[1] * lcdm_stack(typ == 1, "red")[K1]) / (wcls[0] + wcls[1])
refM = lcdm_stack(ALL, "moster")[K1]
MA = dict(B=model_amps(lambda m, i: law_stack(m, "canonical"), refB),
          L=model_amps(lambda m, i: lcdm_stack(m, "blue" if i < 3 else "red"), refL),
          M=model_amps(lambda m, i: lcdm_stack(m, "moster"), refM))
check("R5 (reported) the models' predicted amplitudes for the six bins (same definition) and chi2 against the data (6 dof)",
      "; ".join(f"{lab}: {np.round(v, 4).tolist()} chi2 {float((A6 - v) @ Ci6 @ (A6 - v)):.1f}" for lab, v in
                (("B's law", MA["B"]), ("colour-split LCDM", MA["L"]), ("colour-blind Moster", MA["M"]))), True, load_bearing=False)

ea0, _ = esd_and_loo(ALL, WGx)
D0 = float((WK * ea0).sum())
A6f, AL6f = [], []
for m in MASKS:
    e, l = esd_and_loo(m, WGx)
    A6f.append(math.log10(float((WK * e).sum()) / D0)); AL6f.append(np.log10((WK[None] * l).sum(1) / D0))
A6f, AL6f = np.array(A6f), np.array(AL6f).T
C6f = jcov(AL6f); Ci6f = HART6 * np.linalg.inv(C6f)
ev, evf = np.linalg.eigvalsh(C6), np.linalg.eigvalsh(C6f)
X_off = np.ones((6, 1))
F6 = {lab: gls(A6f, Ci6f, X) for lab, X in (("offset", X_off), ("step", X_step), ("gradient", X_grad), ("step+slope", X_ss))}
MOFF = {lab: gls(A6f - v, Ci6f, X_off)[2] for lab, v in (("B's law", MA["B"]), ("colour-split LCDM", MA["L"]), ("colour-blind Moster", MA["M"]))}
check("R6 (post hoc, reported only; added after the first run) amplitudes against a fixed (non-jackknifed) full-sample reference; every model with a free common offset",
      f"covariance condition number: frozen {ev.max() / ev.min():.0f} (smallest eigenvalue {ev.min():.1e}), fixed reference {evf.max() / evf.min():.1f}; "
      f"B's null + offset chi2 {F6['offset'][2]:.2f}/5 (p {stats.chi2.sf(F6['offset'][2], 5):.1e}); step {F6['step'][2]:.2f}/4; gradient {F6['gradient'][2]:.2f}/4; "
      f"step+slope {F6['step+slope'][2]:.2f}/3 (beta_w {F6['step+slope'][0][2]:+.4f} +- {math.sqrt(F6['step+slope'][1][2, 2]):.4f}); "
      f"Delta chi2 (step - step+slope) {F6['step'][2] - F6['step+slope'][2]:.2f}; models + offset: "
      + ", ".join(f"{k} {v:.1f}/5 (p {stats.chi2.sf(v, 5):.1e})" for k, v in MOFF.items()), True, load_bearing=False)
R.num("R6", dict(cond=[float(ev.max() / ev.min()), float(evf.max() / evf.min())], fits={k: v[2] for k, v in F6.items()}, models=MOFF,
                 beta_w=[float(F6["step+slope"][0][2]), float(math.sqrt(F6["step+slope"][1][2, 2]))]))

if lam < 9:
    reading = "non-discriminating: the data cannot tell a step from a gradient of the class-difference size (lambda < 9)"
elif h1:
    reading = "a step at the valley: a within-class gradient of the class-difference size is excluded at this power"
elif dx >= 9:
    reading = "a gradient: a within-class colour slope is detected (R3 says whether it survives without the boundary tertiles)"
else:
    reading = "leaning towards a gradient, not established"
P(f"\n    READING (declared): {reading}")
R.num("edges", {str(c): ED[c].tolist() for c in (0, 1)}); R.num("umed", UMED.tolist()); R.num("A6", A6.tolist()); R.num("C6", C6.tolist())
R.num("class", dict(A=A_cls.tolist(), umed=[UCLS[0], UCLS[1]], beta_true=BETA_TRUE)); R.num("power", dict(lam=lam, sig_beta=sig_b))
R.num("fits", dict(step=dict(th=th_s.tolist(), chi2=x_s), grad=dict(th=th_g.tolist(), chi2=x_g), ss=dict(th=th_w.tolist(), chi2=x_w)))
R.num("C3_mean", mn); R.num("R3", dict(d=D2.tolist(), chi2=x2o)); R.num("R5", {k: v.tolist() for k, v in MA.items()}); R.num("reading", reading)
nf = R.write()
sys.exit(1 if nf else 0)
