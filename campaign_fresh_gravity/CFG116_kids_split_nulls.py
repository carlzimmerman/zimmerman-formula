#!/usr/bin/env python3
"""CFG116 -- DOES B'S ONE SPECIFIC FAILURE PASS THE STANDARD LENSING SYSTEMATICS NULLS?  The KiDS early/late lensing difference at fixed
g_bar (1-halo bins K1) under (H1) the cross-shear (B-mode) null and (H2) a source-separation split (near vs far background sources).

Criteria frozen and committed before any staging or number: campaign_fresh_gravity/CFG116_FROZEN_CRITERIA.md (e4083bd4f).
  data     cfg116_perlens.npz (CFG116_stage_perlens.py: one pass of the June estimator keeping near (z_l+0.2 < z_B <= z_l+0.5) and far
           (z_B > z_l+0.5) tangential sums and the cross-shear sums per lens per bin); CFG110's data prefix exec'd read-only (cfg110_perlens,
           lr_lenses, June patch labels, K1 = bins 8-14, 50-patch leave-one-out jackknife).  D = ESD(early) - ESD(late) per K1 bin.
PRE-DECLARED (from the frozen file)
  C1  CONTROL  near + far tangential sums reproduce cfg110_perlens (WG, WW, NN) per lens per bin to 1e-9 relative.
  C2  CONTROL  on the first 2,000 lenses the cross sums equal the tangential estimator at position angle + 45 deg to 1e-12.
  R0  POWER (printed before any cross or near/far number): expected chi2 of each null if a fraction eps = 0.25 / 0.5 of the early-late
               tangential difference leaked into it.
  H1  [HEADLINE; MUTATE must fail] the cross shear passes: the early-late cross difference (7 dof) and each class's cross profile (7 dof)
               are consistent with zero, Hartlap chi2 p > 0.01.
  H2  the early-late tangential difference does not depend on source separation: chi2 of D_near - D_far (7 dof) p > 0.01.
  R1-R4 (reported): B's null from far / near sources only; the class profiles; the far/near class amplitude ratios (dilution); the
               survey-level cross null (all lenses, 15 bins).
MUTATE=1: WX += 0.3 WG for every early-type lens -- H1 must FAIL (rc = 1).
Run: python3 campaign_fresh_gravity/CFG116_kids_split_nulls.py   (MUTATE=1 for the control)
"""
import os, sys, io, contextlib
import numpy as np
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import CFG7_common as C
MUTATE = os.environ.get("MUTATE", "0") == "1"
R = C.Report("CFG116_kids_split_nulls", MUTATE)
P, check = R.P, R.check
P(__doc__.split("Run: python3")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: 30% of each early-type lens's tangential sum leaked into its cross sum -- H1 must FAIL ***")

_e = os.environ.get("MUTATE"); os.environ["MUTATE"] = "0"
F110 = os.path.join(HERE, "CFG110_kids_mass_split.py")
src = open(F110).read()
g110 = {"__file__": F110, "__name__": "cfg110"}
try:
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(src[:src.index("# ------------------------------------------------------------------ the models on masks")], "CFG110", "exec"), g110)
finally:
    os.environ.pop("MUTATE") if _e is None else os.environ.__setitem__("MUTATE", _e)
WG, WW, NNL, typ, patch, K1, KG, NPAT = (g110[k] for k in ("WG", "WW", "NNL", "typ", "patch", "K1", "KG", "NPAT"))
LR = os.path.join(C.REPO, "real_research", "data", "lensing_rar")
S = np.load(os.path.join(LR, "cfg116_perlens.npz"))
WGn, WWn, NNn, WGf, WWf, NNf, WX, WGrot = (S[k].astype(float) for k in ("WGn", "WWn", "NNn", "WGf", "WWf", "NNf", "WX", "WGrot"))
H7, H15 = (NPAT - 7 - 2) / (NPAT - 1), (NPAT - 15 - 2) / (NPAT - 1)
EARLY, LATE, ALL = typ == 1, typ == 0, np.ones(len(typ), bool)


def esd_loo(wg, ww, mask, cols=K1):
    g = wg[mask][:, cols]; w = ww[mask][:, cols]; pa = patch[mask]
    tg, tw = g.sum(0), w.sum(0)
    Sg = np.zeros((NPAT, len(cols))); Sw = np.zeros((NPAT, len(cols)))
    np.add.at(Sg, pa, g); np.add.at(Sw, pa, w)
    return tg / tw / KG, (tg[None] - Sg) / (tw[None] - Sw) / KG


def diff(wg, ww):
    e1, l1 = esd_loo(wg, ww, EARLY); e0, l0 = esd_loo(wg, ww, LATE)
    return e1 - e0, l1 - l0


def jcov(L):
    d = L - L.mean(0)
    return (L.shape[0] - 1) / L.shape[0] * d.T @ d


def chi(r, Cm, h):
    return float(r @ np.linalg.solve(Cm, r)) * h


def amp(wg, ww, mask):
    num, den = wg[mask][:, K1].sum(), ww[mask][:, K1].sum()
    Sg = np.zeros(NPAT); Sw = np.zeros(NPAT)
    np.add.at(Sg, patch[mask], wg[mask][:, K1].sum(1)); np.add.at(Sw, patch[mask], ww[mask][:, K1].sum(1))
    return np.log10(num / den), np.log10((num - Sg) / (den - Sw))


# ================================================================== C1 / C2
R.banner("C1 / C2  CONTROLS")
dev = 0.0
for a, b, lab in ((WGn + WGf, WG, "WG"), (WWn + WWf, WW, "WW"), (NNn + NNf, NNL, "NN")):
    nz = np.abs(b) > 0
    dev = max(dev, float(np.max(np.abs(a[nz] - b[nz]) / np.abs(b[nz]))), float(np.max(np.abs(a[~nz]))) if (~nz).any() else 0.0)
check("C1 CONTROL: near + far tangential sums reproduce cfg110_perlens (WG, WW, NN) per lens per bin to 1e-9 relative",
      f"max relative deviation {dev:.1e}; far share of the K1 pair weight: early {WWf[EARLY][:, K1].sum() / WW[EARLY][:, K1].sum():.3f}, "
      f"late {WWf[LATE][:, K1].sum() / WW[LATE][:, K1].sum():.3f}", dev < 1e-9)
n2 = WGrot.shape[0]
d2 = float(np.max(np.abs(WX[:n2] - WGrot)) / np.max(np.abs(WGrot)))
check("C2 CONTROL: on the first 2,000 lenses the cross sums equal the tangential estimator at position angle + 45 deg (to 1e-12, relative to max)",
      f"max |WX - WG(phi + 45)| / max|WG(phi + 45)| = {d2:.1e}", d2 < 1e-12)

WXu = WX.copy()
if MUTATE:
    WXu[EARLY] = WX[EARLY] + 0.3 * WG[EARLY]

# ================================================================== R0: power, before any null number
R.banner("R0  POWER (covariances only; printed before any cross or near/far number)")
Dt, Lt = diff(WG, WW)
Dx, Lx = diff(WXu, WW)
Dn, Ln = diff(WGn, WWn); Df, Lf = diff(WGf, WWf)
Cx, Cnf = jcov(Lx), jcov(Ln - Lf)
pw = {e: (chi(e * Dt, Cx, H7), chi(e * Dt, Cnf, H7)) for e in (0.25, 0.5)}
check("R0 (reported) POWER: expected chi2 (7 dof) if a fraction eps of the early-late tangential difference leaked into the cross difference / into near-minus-far",
      "; ".join(f"eps {e}: cross {v[0]:.1f}, near-far {v[1]:.1f}" for e, v in pw.items())
      + f"; the tangential difference itself: chi2 {chi(Dt, jcov(Lt), H7):.1f}/7 (the known split)", True, load_bearing=False)

# ================================================================== H1 / H2
R.banner("H1 / H2  THE NULLS")
x_d = chi(Dx, Cx, H7); p_d = float(stats.chi2.sf(x_d, 7))
xc = {}
for lab, m in (("late", LATE), ("early", EARLY)):
    e, l = esd_loo(WXu, WW, m); xc[lab] = (chi(e, jcov(l), H7), e)
pc = {k: float(stats.chi2.sf(v[0], 7)) for k, v in xc.items()}
P(f"    cross ESD (Msun/pc^2) late {np.round(xc['late'][1], 2).tolist()}  early {np.round(xc['early'][1], 2).tolist()}")
P(f"    cross difference {np.round(Dx, 2).tolist()} +- {np.round(np.sqrt(np.diag(Cx)), 2).tolist()};  tangential difference {np.round(Dt, 2).tolist()}")
h1 = p_d > 0.01 and all(v > 0.01 for v in pc.values())
check("H1 [HEADLINE] THE CROSS SHEAR PASSES: early-late cross difference and each class's cross profile consistent with zero (7 dof each, p > 0.01)"
      + ("  [MUTATE: 30% leak]" if MUTATE else ""),
      f"difference {x_d:.2f}/7 (p {p_d:.3f}); late {xc['late'][0]:.2f}/7 (p {pc['late']:.3f}); early {xc['early'][0]:.2f}/7 (p {pc['early']:.3f})", h1)
x_nf = chi(Dn - Df, Cnf, H7); p_nf = float(stats.chi2.sf(x_nf, 7))
P(f"    D_near {np.round(Dn, 2).tolist()}\n    D_far  {np.round(Df, 2).tolist()}")
check("H2 THE SPLIT DOES NOT DEPEND ON SOURCE SEPARATION: chi2 of D_near - D_far (7 dof) p > 0.01",
      f"{x_nf:.2f}/7 (p {p_nf:.3f})", p_nf > 0.01)

# ================================================================== reported rows
R.banner("REPORTED ROWS")
xf, xn = chi(Df, jcov(Lf), H7), chi(Dn, jcov(Ln), H7)
am = {}
for tag, (wg, ww) in (("near", (WGn, WWn)), ("far", (WGf, WWf)), ("all", (WG, WW))):
    ae, le = amp(wg, ww, EARLY); al, ll = amp(wg, ww, LATE)
    d = le - ll; am[tag] = (ae - al, float(np.sqrt((NPAT - 1) / NPAT * np.sum((d - d.mean()) ** 2))))
check("R1 (reported) B's null (the early-late difference against zero, 7 dof) from far sources only and near sources only; early-late amplitude (dex)",
      f"far {xf:.1f}/7 (p {stats.chi2.sf(xf, 7):.1e}); near {xn:.1f}/7 (p {stats.chi2.sf(xn, 7):.1e}); amplitude near {am['near'][0]:+.3f} +- {am['near'][1]:.3f}, "
      f"far {am['far'][0]:+.3f} +- {am['far'][1]:.3f}, all {am['all'][0]:+.3f} +- {am['all'][1]:.3f}", True, load_bearing=False)
rows = []
for lab, m in (("late", LATE), ("early", EARLY)):
    en, _ = esd_loo(WGn, WWn, m); ef, _ = esd_loo(WGf, WWf, m)
    rows.append(f"{lab}: near {np.round(en, 1).tolist()}, far {np.round(ef, 1).tolist()}")
check("R2 (reported) the class tangential profiles over K1 from near and far sources (Msun/pc^2)", "; ".join(rows), True, load_bearing=False)
rr = []
for lab, m in (("late", LATE), ("early", EARLY)):
    an, ln_ = amp(WGn, WWn, m); af, lf_ = amp(WGf, WWf, m)
    d = lf_ - ln_
    rr.append(f"{lab} far - near {af - an:+.3f} +- {np.sqrt((NPAT - 1) / NPAT * np.sum((d - d.mean()) ** 2)):.3f} dex")
check("R3 (reported) the far/near ratio of each class's amplitude (dilution by associated galaxies lowers the near-source ESD)", "; ".join(rr), True, load_bearing=False)
ea, la = esd_loo(WXu, WW, ALL, cols=list(range(15)))
x15 = chi(ea, jcov(la), H15)
check("R4 (reported) the survey-level cross null: all lenses, all 15 bins", f"{x15:.2f}/15 (p {stats.chi2.sf(x15, 15):.3f})", True, load_bearing=False)

if h1 and p_nf > 0.01:
    reading = "the split passes both nulls at this power: class-dependent B-mode systematics and source-side dilution/alignment are excluded as its origin"
elif not h1:
    reading = "a class-dependent B-mode systematic is present: the split's significance is suspect"
else:
    reading = "the split depends on source separation: a source-side systematic contributes (R1, R3 say which way)"
P(f"\n    READING (declared): {reading}")
R.num("Dt", Dt.tolist()); R.num("Dx", Dx.tolist()); R.num("Dn", Dn.tolist()); R.num("Df", Df.tolist())
R.num("H1", dict(diff=[x_d, p_d], late=[xc["late"][0], pc["late"]], early=[xc["early"][0], pc["early"]])); R.num("H2", [x_nf, p_nf])
R.num("R0", {str(e): v for e, v in pw.items()}); R.num("R1", dict(far=xf, near=xn, amp={k: list(v) for k, v in am.items()})); R.num("R4", x15)
R.num("reading", reading)
nf = R.write()
sys.exit(1 if nf else 0)
