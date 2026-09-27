#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XR32 (2/3) -- THE S8 A LENSING SURVEY WOULD INFER FROM THE CHAIN: xi+- in the KiDS-1000 and DES-Y3 set-ups, fitted with
LCDM templates the way the surveys fit, against the published KiDS-1000, KiDS-Legacy, DES Y3 and HSC Y3 values.

WHY.  A scale-dependent suppression is not a lower sigma8: a survey fits xi+- over its own scales with LCDM templates and
nuisance parameters that can absorb part of it (baryon feedback, intrinsic alignments).  XR32_matter_power builds the
chain's P(k, z); this part asks what S8 a survey would report, and whether that lands on the low-z weak-lensing values.

METHOD
  THE SET-UPS.
    KiDS-1000: five tomographic bins (Z_B 0.1-0.3-0.5-0.7-0.9-1.2).  n(z): lensfit-weighted stacks of Gaussian photo-z
      PDFs (Z_B, half the 68% interval) from the DR4.1 gold catalogue in the repository, moment-matched to Asgari+21 Table
      A.1's SOM means (0.26/0.40/0.56/0.79/0.98) and stds (0.16/0.16/0.20/0.16/0.25) -- an approximation (the SOM n(z)
      needs the spectroscopic calibration sample; its tails come out ~3x lighter than Table A.1's).  theta: 9 log bins
      0.5-300 arcmin, xi- only above 4 arcmin (225 points, Asgari+21 Table 3's DoF).  Covariance: analytic Gaussian
      (sample variance, shape noise from Table 1's n_eff and sigma_e, the mixed term, E and B shape noise), A = 777.4 deg^2.
    DES Y3: the official 2pt file (repository copy): source n(z), 20 theta bins 2.5-250 arcmin, the LCDM-optimised scale
      cuts (cosmosis-standard-library des-y3-LCDM-optimised-scale-cuts.ini), the official covariance.
    Both: Limber with l + 1/2 (checked against CAMB's own lensing source windows), NLA intrinsic alignments, xi+- averaged
      over each theta bin with theta d theta weights through analytic Bessel integrals.
  THE CHAIN'S DATA.  P_chain(k, z) = R(k, z) x P_template(k, z; Planck-2018 truth), R = XR32_common's halo-model response
    (the model XR32_matter_power documents), noiseless, no intrinsic alignment in the truth.  Normalised to Planck 2018
    (an ASSUMPTION pending XR26).
  THE FIT, the way the surveys fit.  LCDM templates on grids (Omega_m 0.18-0.46 in 0.02, S8 0.44-1.12 in 0.04; cubic
    interpolation): KiDS -- CAMB HMcode (mead2016) with A_bary in [2, 3.13] (eta_0 = 0.98 - 0.12 A_bary), NLA A_IA in
    [-6, 6] (Asgari+21's model and priors); DES -- CAMB Takahashi halofit, NLA A_1 in [-5, 5], eta_1 in [-3, 3], z_0 = 0.62.
    Fixed at the truth (disclosed): h, omega_b, n_s, sum m_nu; no photo-z or shear-calibration nuisances (priors centred
    on the truth).  Inferred S8 = the best fit (minimum chi^2 with the survey covariance); the Delta chi^2 = 1 width of
    the S8 profile is reported for the key cells; chi^2_min measures how well LCDM can mimic the chain.
  CONFIGURATIONS.  The ten histories of XR32_matter_power (delta_t0 5.31-25, conservative, pump, halo only, v_k 575/650);
    four recapture readings and two halo populations at the nominal cell; the phantom bracket: none / the 1.7 Mpc
    stand-in on both a0 footings (canonical 9.3603e-11, alt 1.1312e-10); sensitivities: running L(z), heat-kernel edge.
PRE-DECLARED (written 2026-09-27T14:01Z, before any full run)
  H2a [load-bearing; MUTATE must fail] no phantom, nominal, primary: survey-inferred S8 below the Planck-LCDM truth by
      >= 0.02 for both the KiDS-1000 and the DES-Y3 set-ups.
  H2b no phantom: inferred S8 <= the chain's linear S8 (0.832-normalised sigma8 ratio) for both set-ups.
  H2c 1.7 Mpc phantom: inferred S8 > the Planck truth for both set-ups.
  H2d no phantom, nominal: inferred S8 more than 2 sigma below KiDS-1000's and DES Y3's published values.
  H2e no phantom, nominal: the LCDM-template fit is poor, chi2_min >= 10 (KiDS-1000 set-up).
  Control: fitting the real DES Y3 xi+- (LCDM-optimised cuts) with the same templates returns S8 within 0.03 of 0.772.
CHECKS (load-bearing unless marked)
  C1 CONTROL: this lane's Limber C_ell for the KiDS-1000 n(z) against CAMB 1.6.6's own lensing source windows (HMcode-2020,
     Planck 2018; CAMB exact below l = 100, CAMB Limber above): all 15 bin pairs within 1% point-wise at l = 30-3000;
     xi+- through the same Hankel transform compared at theta >= 4 arcmin (reported beside it).
  C2 CONTROL: the Hankel transform against an analytic Gaussian (<= 1e-3) and the J_4 bin average against quadrature.
  C3 CONTROL: the fit recovers the truth from a no-conversion data vector: |S8 - S8_true| <= 0.003, both set-ups.
  C4 CONTROL: the real DES Y3 xi+- (LCDM-optimised cuts; multiplicative biases at their prior means) fitted with the same
     templates: best-fit S8 within 0.03 of the published 0.772.
  C5 (reported) the Delta chi^2 = 1 width of the truth fit's S8 profile against the published errors (0.018 / 0.018).
  C6 (reported) the KiDS n(z): stack moments, matched moments, tails beyond z = 2 against Table A.1.
  C7 (reported) the templates' sigma8 targeting.
  H2a-H2e as above.  Reported: every configuration's inferred S8, Omega_m, nuisances and chi^2_min, and the tension with
  each published value (in the published errors, and with Planck's 0.013 added in quadrature).
MUTATE=1: the conversion switched off (every halo keeps its carrier; T^2 = 1).  The no-phantom data are the truth; H2a
  must FAIL (rc = 1).
HISTORY (disclosed): the unit tests and smoke run listed in XR32_matter_power.py's docstring; the phantom stand-in's form
  and mass range were fixed there before this script's first run.  This script's first smoke run (scratch, not for the
  record) found a bug in XR32_common's bin-averaged J_4 (a small-argument branch dropped the antiderivative's constant, so
  bins straddling l theta = 0.1 picked up a spurious term): xi- was wrong by orders of magnitude, the DES fit ran to the S8
  bound (chi2 14729) and the KiDS covariance was near-singular.  Fixed (F(x) = x J1 - 4 J0 - 12 J2 + 4, checked against
  quadrature across the branch edge to 2e-4) before any recorded run.  The smoke runs showed C1's point-wise deviation
  (1.3%) at l ~ 44 in the lowest bin; a direct test traced it to CAMB: its limber_windows output dips ~1% below its own
  exact (non-Limber) result at l ~ 40-45.  C1 now compares with CAMB's exact C_ell below l = 100 (and its Limber C_ell
  above), point-wise at 1%, the size of CAMB's dip reported beside it.  The second smoke run completed (10/13: C1 as
  above, H2c and H2d falling); its outcomes were seen before the recorded runs and no hypothesis was changed.

Run from the repository root:  python3 real_research/cross_thread_review_2026_09_26/XR32_survey_s8.py   (MUTATE=1 first)
"""
import os, sys, json, math, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import XR32_common as X
import numpy as np
import camb
from camb.sources import SplinedSourceWindow

MUTATE = os.environ.get("MUTATE", "0") == "1"
OUTD = os.environ.get("XR32_OUTDIR", HERE)                              # smoke tests write to scratch, never the record
SLUG = "XR32_survey_s8"; SUF = "_MUTATE" if MUTATE else ""
P = X.Log(os.path.join(OUTD, SLUG + SUF + ".out"))
T0 = time.time(); CH = []; OUT = {"lane": "XR32", "part": "2/3 survey S8", "mutate": MUTATE, "checks": {}, "numbers": {}}


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok); CH.append((name, ok, load_bearing))
    OUT["checks"][name.split(" ")[0]] = {"ok": ok, "claim": name, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}]{'' if load_bearing else ' (reported)'} {name}"); P(f"         measured: {measured}")
    if reading: P(f"         reading:  {reading}")
    return ok


def banner(t): P("\n" + "=" * 118); P(t); P("=" * 118)
def el(): return f"[{time.time() - T0:.0f}s]"


P(__doc__.split("PRE-DECLARED")[0].strip())
if MUTATE: P("\n  *** MUTATE=1: conversion switched off; the no-phantom data are the truth; H2a must FAIL ***")
ZT = np.linspace(0.0, 4.0, 41)
OMG = np.round(np.arange(0.18, 0.4601, 0.02), 4); S8G = np.round(np.arange(0.44, 1.1201, 0.04), 4)
ABG = np.array([2.0, 2.3767, 2.7533, 3.13]); ETAG = np.array([-3.0, -1.5, 0.0, 1.5, 3.0])

# ================================================================================================ the set-ups
zc, nzk, nzinfo = X.kids_nz()
rows_k = X.kids_layout()
kb = X.kids_bins(); kb_rad = [(X.arcmin(a), X.arcmin(b)) for a, b in kb]
HK0, HK4 = X.Hankel(kb_rad, [0] * 9), X.Hankel(kb_rad, [4] * 9)
D = X.des_y3()
db = sorted({(r[3], r[5], r[6]) for r in D["rows"] if r[0] == "xip" and r[1] == 1 and r[2] == 1})
db_rad = [(X.arcmin(a), X.arcmin(b)) for _, a, b in db]
HD0, HD4 = X.Hankel(db_rad, [0] * len(db)), X.Hankel(db_rad, [4] * len(db))
PK = [(i, j) for i in range(5) for j in range(i, 5)]; PD = [(i, j) for i in range(4) for j in range(i, 4)]
P(f"  KiDS-1000: {len(rows_k)} points; DES Y3: {int(D['keep'].sum())} of {len(D['rows'])} after the LCDM-optimised cuts   {el()}")


def vec(survey, cl_cols):
    """cl_cols: dict pair -> (Nell,) C_ell of ONE component; returns the full xi+- vector in the survey's layout."""
    pairs = PK if survey == "kids" else PD
    M = np.stack([cl_cols[p] for p in pairs], axis=1)
    L = LIM_ELLS
    if survey == "kids":
        xp, xm = HK0.xi(L, M), HK4.xi(L, M)
        return np.array([(xp if r[0] == "xip" else xm)[r[3], pairs.index((r[1] - 1, r[2] - 1))] for r in rows_k])
    xp, xm = HD0.xi(L, M), HD4.xi(L, M)
    return np.array([(xp if r[0] == "xip" else xm)[r[3], pairs.index((r[1] - 1, r[2] - 1))] for r in D["rows"]])


def components(survey, Lim, Pg, etas=(0.0,)):
    """GG and, per eta, GI and II xi-vectors (per unit A_IA and A_IA^2)."""
    out = {}
    for e in etas:
        cl = Lim.cls(Pg, eta=e)
        if "gg" not in out: out["gg"] = vec(survey, {p: v[0] for p, v in cl.items()})
        out[("gi", e)] = vec(survey, {p: v[1] for p, v in cl.items()}); out[("ii", e)] = vec(survey, {p: v[2] for p, v in cl.items()})
    return out


LIM_ELLS = np.geomspace(1.0, 2e5, 170)
# the truth cosmologies (Planck 2018) in each survey's template model
tk = X.camb_setup(zs=ZT, nl="mead2016", A_bary=3.13); Ck = X.Cosmo(camb.get_results(tk), ZT)
td = X.camb_setup(zs=ZT, nl="takahashi"); Cd = X.Cosmo(camb.get_results(td), ZT)
S8T = float(Ck.res.get_sigma8_0()) * math.sqrt(Ck.Om / 0.3)
Lk = X.Limber(Ck, zc, nzk, ells=LIM_ELLS); Ld = X.Limber(Cd, D["z"], D["nz"], ells=LIM_ELLS)
P(f"  truth: Omega_m {Ck.Om:.5f}, S8 {S8T:.5f} (Planck 2018 posterior means; quoted 0.832 +- 0.013)   {el()}")

# ================================================================================================ C1, C2, C6 controls
banner("C1-C2, C6  CONTROLS: Limber and xi+- against CAMB's own lensing source windows; the Hankel transform; the KiDS n(z)")
base = X.ChainBase()
Lc = X.Limber(base.C, zc, nzk, ells=LIM_ELLS); Pgc = Lc.pk_grid(lambda k, z: base.C.P(k, z)); clm = Lc.cls(Pgc)
p2 = X.camb_setup(zs=None, nl="mead2020", lensing=True); p2.set_for_lmax(6000, lens_potential_accuracy=2)
p2.SourceWindows = [SplinedSourceWindow(z=zc, W=n, source_type="lensing") for n in nzk]
p2.SourceTerms.limber_windows = True; p2.SourceTerms.limber_phi_lmin = 10; p2.NonLinear = camb.model.NonLinear_both
cc = camb.get_results(p2).get_source_cls_dict(raw_cl=True)
p3 = X.camb_setup(zs=None, nl="mead2020", lensing=True); p3.set_for_lmax(150, lens_potential_accuracy=2)
p3.SourceWindows = [SplinedSourceWindow(z=zc, W=n, source_type="lensing") for n in nzk]
p3.SourceTerms.limber_windows = False; p3.NonLinear = camb.model.NonLinear_both
ce = camb.get_results(p3).get_source_cls_dict(raw_cl=True)
worst, wl, ell_c = 0.0, 0.0, np.arange(30, 3001)
cam = {}
for (i, j) in PK:
    c_ = np.array(cc[f"W{i + 1}xW{j + 1}"]); e_ = np.array(ce[f"W{i + 1}xW{j + 1}"]); cam[(i, j)] = c_
    ref = np.where(ell_c < 100, e_[np.minimum(ell_c, len(e_) - 1)], c_[ell_c])
    mine = np.interp(ell_c, LIM_ELLS, clm[(i, j)][0])
    worst = max(worst, float(np.max(np.abs(mine / ref - 1))))
    lo_ = ell_c < 100; wl = max(wl, float(np.max(np.abs(c_[ell_c][lo_] / e_[ell_c[lo_]] - 1))))
check("C1 CONTROL: Limber C_ell (KiDS-1000 n(z), HMcode-2020, Planck 2018) against CAMB 1.6.6: its exact (non-Limber) source-window C_ell at "
      "l = 30-99 and its Limber C_ell at l = 100-3000; all 15 pairs within 1% point-wise", f"max |ratio - 1| = {worst:.4f} (CAMB's own Limber "
      f"output departs from its exact one by up to {wl:.4f} at l < 100)", worst <= 0.01,
      "CAMB's limber_windows output has a ~1% transition dip at l ~ 40-45 (found in the smoke run), hence its exact result below l = 100")
ls = np.arange(2, 6001)
spl = {p: np.where(LIM_ELLS <= 5500, np.interp(LIM_ELLS, ls, cam[p][2:6001]), clm[p][0]) for p in PK}
xi_c = vec("kids", spl); xi_m = vec("kids", {p: clm[p][0] for p in PK})
sel = np.array([r[4] >= 4.0 for r in rows_k])
dxi = float(np.max(np.abs(xi_m[sel] / xi_c[sel] - 1)))
check("C1b (reported) xi+- from CAMB's C_ell (spliced to this lane's above l = 5500) and from this lane's, same Hankel transform, theta >= 4 arcmin",
      f"max |ratio - 1| = {dxi:.4f}", True, load_bearing=False)
OUT["numbers"]["C1"] = dict(max_cl_dev=worst, max_xi_dev_theta_ge_4=dxi)
s_ = 0.002; ellg = np.geomspace(1, 2e5, 170); xg = HK0.xi(ellg, np.exp(-ellg ** 2 * s_ ** 2 / 2))
an = np.array([(math.exp(-lo ** 2 / (2 * s_ * s_)) - math.exp(-hi ** 2 / (2 * s_ * s_))) / ((hi ** 2 - lo ** 2) / 2) / (2 * math.pi) for lo, hi in kb_rad])
from scipy import integrate, special
e2 = max(abs(X.jbar(np.array([l_]), X.arcmin(4.217), X.arcmin(8.585), 4)[0] - integrate.quad(lambda t: t * special.jv(4, l_ * t), X.arcmin(4.217), X.arcmin(8.585), limit=400)[0] / ((X.arcmin(8.585) ** 2 - X.arcmin(4.217) ** 2) / 2)) for l_ in (100.0, 3000.0, 30000.0))
ok2 = float(np.max(np.abs(xg / an - 1)[an > 1e-3 * an.max()]))
check("C2 CONTROL: the Hankel transform reproduces an analytic Gaussian (<= 1e-3) and the J_4 bin average matches quadrature (<= 1e-8)",
      f"Gaussian {ok2:.1e}; J_4 {e2:.1e}", ok2 <= 1e-3 and e2 <= 1e-8)
check("C6 (reported) the KiDS-1000 n(z): catalogue stacks moment-matched to Asgari+21 Table A.1", nzinfo, True,
      "means and stds hit Table A.1 exactly; the tails beyond z = 2 come out lighter (0.01-0.3% against 0.1-1%)", load_bearing=False)
OUT["numbers"]["C6"] = nzinfo

# ================================================================================================ covariances
Pgk = Lk.pk_grid(lambda k, z: Ck.P(k, z)); clk = Lk.cls(Pgk)
covk = X.gaussian_cov_kids(rows_k, LIM_ELLS, {p: v[0] for p, v in clk.items()})
ev = np.linalg.eigvalsh(covk)
P(f"  KiDS-1000 Gaussian covariance: {covk.shape}, min eigenvalue {ev.min():.2e} (> 0), condition {ev.max() / ev.min():.1e}   {el()}")
icov_k = np.linalg.inv(covk)
covd = D["cov"][np.ix_(D["keep"], D["keep"])]; icov_d = np.linalg.inv(covd)

# ================================================================================================ templates
banner("TEMPLATES: CAMB LCDM on (Omega_m, S8[, A_bary]); NLA intrinsic alignments")
GGk = np.zeros((len(OMG), len(S8G), len(ABG), len(rows_k))); GIk = np.zeros_like(GGk); IIk = np.zeros_like(GGk)
nd = int(D["keep"].sum())
GGd = np.zeros((len(OMG), len(S8G), nd)); GId = np.zeros((len(OMG), len(S8G), len(ETAG), nd)); IId = np.zeros_like(GId)
s8dev = 0.0
for iO, Om in enumerate(OMG):
    for survey in ("kids", "des"):
        pars = X.camb_setup(Om=float(Om), zs=ZT, nl="mead2016" if survey == "kids" else "takahashi", A_bary=3.13 if survey == "kids" else None)
        tr = camb.get_transfer_functions(pars); tr.power_spectra_from_transfer(pars.InitPower); s8r = float(tr.get_sigma8_0())
        Lim = None
        for iS, S8 in enumerate(S8G):
            sig8 = float(S8) / math.sqrt(float(Om) / 0.3)
            pars.InitPower.set_params(As=X.P18["As"] * (sig8 / s8r) ** 2, ns=X.P18["ns"])
            for iA, A in enumerate(ABG if survey == "kids" else [None]):
                if survey == "kids":
                    tr.Params.NonLinearModel.set_params(halofit_version="mead2016", HMCode_A_baryon=float(A), HMCode_eta_baryon=0.98 - 0.12 * float(A))
                tr.power_spectra_from_transfer(pars.InitPower)
                s8dev = max(s8dev, abs(float(tr.get_sigma8_0()) - sig8))
                C = X.Cosmo(tr, ZT)
                if Lim is None: Lim = X.Limber(C, zc if survey == "kids" else D["z"], nzk if survey == "kids" else D["nz"], ells=LIM_ELLS)
                comp = components(survey, Lim, Lim.pk_grid(lambda k, z: C.P(k, z)), (0.0,) if survey == "kids" else tuple(ETAG))
                if survey == "kids":
                    GGk[iO, iS, iA] = comp["gg"]; GIk[iO, iS, iA] = comp[("gi", 0.0)]; IIk[iO, iS, iA] = comp[("ii", 0.0)]
                else:
                    GGd[iO, iS] = comp["gg"][D["keep"]]
                    for ie, e in enumerate(ETAG):
                        GId[iO, iS, ie] = comp[("gi", e)][D["keep"]]; IId[iO, iS, ie] = comp[("ii", e)][D["keep"]]
    P(f"    Omega_m {Om:.2f} done   {el()}")
check("C7 (reported) the templates hit their sigma8 targets", f"max |sigma8 - target| = {s8dev:.1e}", True, load_bearing=False)
TSk = X.TemplateSet((OMG, S8G, ABG), GGk, GIk, IIk)
TSd = X.TemplateSet((OMG, S8G), GGd, GId, IId, etas=ETAG)
BDk = [(0.18, 0.46), (0.44, 1.12), (-6.0, 6.0), (2.0, 3.13)]; BDd = [(0.18, 0.46), (0.44, 1.12), (-5.0, 5.0), (-3.0, 3.0)]
STk = [(0.31, 0.83, 0.0, 3.0), (0.25, 0.75, 0.5, 2.5), (0.38, 0.70, -0.5, 2.2), (0.22, 0.95, 1.0, 3.1)]
STd = [(0.31, 0.83, 0.0, 0.0), (0.25, 0.75, 0.5, 1.0), (0.38, 0.70, -0.5, -1.0), (0.22, 0.95, 1.0, 0.0)]


def data_vec(survey, Rf):
    if survey == "kids":
        Pg = Lk.pk_grid(lambda k, z: Ck.P(k, z) * Rf(k, z)); cl = Lk.cls(Pg)
        return vec("kids", {p: v[0] for p, v in cl.items()})
    Pg = Ld.pk_grid(lambda k, z: Cd.P(k, z) * Rf(k, z)); cl = Ld.cls(Pg)
    return vec("des", {p: v[0] for p, v in cl.items()})[D["keep"]]


def fit_one(survey, dv, profile=False):
    ts, ic, bd, st = (TSk, icov_k, BDk, STk) if survey == "kids" else (TSd, icov_d, BDd, STd)
    x, f = X.fit(ts, dv, ic, bd, st)
    out = dict(S8=float(x[1]), Om=float(x[0]), A_IA=float(x[2]), nuis=float(x[3]), chi2=float(f))
    if profile:
        g = np.round(np.arange(max(0.46, x[1] - 0.08), min(1.10, x[1] + 0.08), 0.005), 4)
        pr = X.s8_profile(ts, dv, ic, bd, x, g) - f
        inside = g[pr <= 1.0]
        out["S8_1sigma"] = (float(inside.min()), float(inside.max())) if inside.size else None
    return out


# ================================================================================================ C3-C5 truth recovery, DES data
banner("C3-C5  CONTROLS: truth recovery; the real DES Y3 data")
one = lambda k, z: np.ones_like(np.atleast_1d(k), dtype=float)
TR = {s: fit_one(s, data_vec(s, one), profile=True) for s in ("kids", "des")}
P("    " + "; ".join(f"{s}: S8 {v['S8']:.4f} (truth {S8T:.4f}), Om {v['Om']:.3f}, A_IA {v['A_IA']:+.2f}, nuisance {v['nuis']:.2f}, chi2 {v['chi2']:.2e}, "
                     f"1 sigma {v['S8_1sigma']}" for s, v in TR.items()))
check("C3 CONTROL: the fit recovers the truth from the no-conversion data vector (|S8 - S8_true| <= 0.003, both set-ups)",
      "; ".join(f"{s} {v['S8'] - S8T:+.4f}" for s, v in TR.items()), all(abs(v["S8"] - S8T) <= 0.003 for v in TR.values()))
mfac = np.array([(1 + X.DES_M[r[1] - 1]) * (1 + X.DES_M[r[2] - 1]) for r in D["rows"]])[D["keep"]]


class Scaled:
    def __init__(self, ts, s): self.ts, self.s, self.axes = ts, s, ts.axes
    def model(self, p): return self.s * self.ts.model(p)


xr, fr = X.fit(Scaled(TSd, mfac), D["data"][D["keep"]], icov_d, BDd, STd)
check("C4 CONTROL: the real DES Y3 xi+- (LCDM-optimised cuts, m at its prior means) fitted with these templates: S8 within 0.03 of the published 0.772",
      f"S8 {xr[1]:.4f}, Om {xr[0]:.3f}, A_1 {xr[2]:+.2f}, eta_1 {xr[3]:+.2f}, chi2 {fr:.1f} for {nd} points", abs(xr[1] - 0.772) <= 0.03,
      "h, omega_b, n_s fixed at Planck's and no photo-z nuisances: a best fit, not DES's marginal posterior")
check("C5 (reported) the Delta chi^2 = 1 width of the truth fit's S8 profile against the published 1 sigma",
      f"KiDS {TR['kids']['S8_1sigma']} (published +-0.018); DES {TR['des']['S8_1sigma']} (published +0.018/-0.017)", True, load_bearing=False)
OUT["numbers"]["truth"] = dict(S8=S8T, Om=Ck.Om, fits=TR, des_data_fit=dict(S8=float(xr[1]), Om=float(xr[0]), A1=float(xr[2]), eta1=float(xr[3]), chi2=float(fr), n=nd))

# ================================================================================================ the chain's configurations
banner("THE CHAIN: inferred S8 by configuration (KiDS-1000 and DES-Y3 set-ups)")
NAMES = [n for n, _, _ in X.HISTORIES]
if MUTATE:
    R = X.record(); LC = R["LC"]
    comp0 = dict(dc=LC.copy(), dd=np.zeros_like(LC), rc=np.ones(LC.shape[1]), rd=np.zeros(LC.shape[1]), tot=LC.copy())
    H = {n: dict(Fz=X.history(k, True), vk=v, comp=comp0, T=X.Transfer(comp0, LC)) for n, k, v in X.HISTORIES}
else:
    H = X.solve_histories(NAMES)
P(f"  histories ready   {el()}")
PH = {"none": None, "L1.7 canonical": ("canonical", X.L_STANDIN, "sharp"), "L1.7 alt": ("alt", X.L_STANDIN, "sharp"),
      "running L canonical (sensitivity)": ("canonical", "running", "sharp"), "heat-kernel L1.7 canonical (sensitivity)": ("canonical", X.L_STANDIN, "heat")}
CFG = []
for rd in X.READINGS:
    for pn in ("none", "L1.7 canonical", "L1.7 alt"): CFG.append(("nominal (dt0 5.31)", rd, "lcdm", pn))
for pn in ("none", "L1.7 canonical"): CFG.append(("nominal (dt0 5.31)", X.READINGS[0], "cold", pn))
for pn in ("running L canonical (sensitivity)", "heat-kernel L1.7 canonical (sensitivity)"): CFG.append(("nominal (dt0 5.31)", X.READINGS[0], "lcdm", pn))
for n in NAMES:
    if n == "nominal (dt0 5.31)": continue
    for pn in ("none", "L1.7 canonical", "L1.7 alt"): CFG.append((n, X.READINGS[0], "lcdm", pn))
RES = {}
for (n, rd, sm, pn) in CFG:
    h_ = H[n]
    Rg = base.response(h_["T"], h_["Fz"], h_["vk"], rd, PH[pn], sm, MUTATE)
    Rf = X.R_fun(Rg)
    key = f"{n} | {rd} | pop {sm} | phantom {pn}"
    prof = (n == "nominal (dt0 5.31)" and rd == X.READINGS[0] and sm == "lcdm" and pn in ("none", "L1.7 canonical"))
    rr = {s: fit_one(s, data_vec(s, Rf), profile=prof) for s in ("kids", "des")}
    lin = X.P18_QUOTED["S8"][0] if MUTATE else None
    RES[key] = rr
    P(f"    {key}: KiDS S8 {rr['kids']['S8']:.4f} (Om {rr['kids']['Om']:.3f}, A_IA {rr['kids']['A_IA']:+.2f}, A_bary {rr['kids']['nuis']:.2f}, chi2 {rr['kids']['chi2']:.1f})"
      f" | DES S8 {rr['des']['S8']:.4f} (Om {rr['des']['Om']:.3f}, A_1 {rr['des']['A_IA']:+.2f}, eta {rr['des']['nuis']:+.2f}, chi2 {rr['des']['chi2']:.1f})   {el()}")
OUT["numbers"]["configs"] = RES

# ================================================================================================ the linear S8 of each history, and the comparison
kk = np.geomspace(1e-4, 50.0, 6000); x8 = kk * 8.0; W8 = 3 * (np.sin(x8) - x8 * np.cos(x8)) / x8 ** 3; Pl0 = base.C.P(kk, 0.0, lin=True)
S8LIN = {n: S8T * math.sqrt(X._trap(kk ** 2 * Pl0 * W8 ** 2 * H[n]["T"](kk, 0.0), kk) / X._trap(kk ** 2 * Pl0 * W8 ** 2, kk)) for n in NAMES}
OUT["numbers"]["S8_linear"] = S8LIN
banner("THE COMPARISON: inferred S8 against the published low-z weak-lensing values")
cmp_ = {}
for key, rr in RES.items():
    cmp_[key] = {}
    for s in ("kids", "des"):
        v = rr[s]["S8"]
        cmp_[key][s] = {pub: dict(t_pub=X.tension(v, val), t_with_planck=X.tension(v, val, X.P18_QUOTED["S8"][1])) for pub, val in X.PUB_WL.items()}
OUT["numbers"]["tensions"] = cmp_
PRIM_NONE = f"nominal (dt0 5.31) | {X.READINGS[0]} | pop lcdm | phantom none"
for key in [PRIM_NONE] + [k for k in RES if k != PRIM_NONE and (" phantom L1.7" in k or "halo only" in k or "dt0" in k) and X.READINGS[0] in k and "pop lcdm" in k][:12]:
    for s, pubs in (("kids", ("KiDS-1000 xi+- (Asgari+21 Table 3, best fit+PJ-HPD)", "KiDS-Legacy (Wright+25)", "HSC Y3 (Li+23 xi+-)")),
                    ("des", ("DES Y3 (Amon+22/Secco+22 LCDM-optimised)", "DES Y3 (Amon+22/Secco+22 fiducial)", "HSC Y3 (Dalal+23 C_ell)"))):
        P(f"    {key} [{s}] S8 {RES[key][s]['S8']:.4f}: " + "; ".join(f"{p.split(' (')[0]} {cmp_[key][s][p]['t_pub']:+.1f} sigma ({cmp_[key][s][p]['t_with_planck']:+.1f} with Planck's error)" for p in pubs))

# ================================================================================================ H2a-H2e
banner("H2a-H2e")
pn_ = RES[PRIM_NONE]
check("H2a without the phantom the conversion lowers the survey-inferred S8 below the Planck-LCDM truth by >= 0.02 in both set-ups (nominal, primary)",
      f"KiDS {pn_['kids']['S8'] - S8T:+.4f}, DES {pn_['des']['S8'] - S8T:+.4f} (truth {S8T:.4f})", all(pn_[s]["S8"] <= S8T - 0.02 for s in ("kids", "des")))
sl = S8LIN["nominal (dt0 5.31)"]
check("H2b without the phantom the inferred S8 is no higher than the chain's linear S8 (small scales add to the suppression), both set-ups",
      f"linear S8 {sl:.4f}; KiDS {pn_['kids']['S8']:.4f}, DES {pn_['des']['S8']:.4f}", all(pn_[s]["S8"] <= sl for s in ("kids", "des")))
ph_ = {f: RES[f"nominal (dt0 5.31) | {X.READINGS[0]} | pop lcdm | phantom L1.7 {f}"] for f in ("canonical", "alt")}
check("H2c with the 1.7 Mpc phantom stand-in the inferred S8 exceeds the Planck truth, both set-ups and both footings",
      "; ".join(f"{f}: KiDS {v['kids']['S8']:.4f}, DES {v['des']['S8']:.4f}" for f, v in ph_.items()),
      all(v[s]["S8"] > S8T for v in ph_.values() for s in ("kids", "des")))
tk_ = cmp_[PRIM_NONE]["kids"]["KiDS-1000 xi+- (Asgari+21 Table 3, best fit+PJ-HPD)"]["t_pub"]; td_ = cmp_[PRIM_NONE]["des"]["DES Y3 (Amon+22/Secco+22 LCDM-optimised)"]["t_pub"]
check("H2d without the phantom (nominal) the inferred S8 lies more than 2 sigma below KiDS-1000's and DES Y3's published values",
      f"KiDS-1000 xi+-: {tk_:+.2f} sigma; DES Y3 LCDM-optimised: {td_:+.2f} sigma (published errors)", tk_ < -2 and td_ < -2)
check("H2e without the phantom (nominal) LCDM templates fit the chain poorly in the KiDS-1000 set-up (chi2_min >= 10, noiseless)",
      f"chi2_min KiDS {pn_['kids']['chi2']:.1f} (225 points), DES {pn_['des']['chi2']:.1f} ({nd} points)", pn_["kids"]["chi2"] >= 10)

# ================================================================================================ summary
banner("SUMMARY")
allnone = {k: v for k, v in RES.items() if k.endswith("phantom none")}
allph = {k: v for k, v in RES.items() if k.endswith("phantom L1.7 canonical") or k.endswith("phantom L1.7 alt")}
sens = {k: v for k, v in RES.items() if "sensitivity" in k}
rng = lambda d, s: (min(v[s]["S8"] for v in d.values()), max(v[s]["S8"] for v in d.values()))
P(f"""  Truth (Planck 2018): S8 {S8T:.3f}.  Without the MOND phantom the chain's survey-inferred S8 is {pn_['kids']['S8']:.3f} (KiDS-1000 set-up) and
  {pn_['des']['S8']:.3f} (DES-Y3) at the nominal cell (linear S8 {sl:.3f}); over every history, reading and population: KiDS {rng(allnone, 'kids')[0]:.3f}-{rng(allnone, 'kids')[1]:.3f},
  DES {rng(allnone, 'des')[0]:.3f}-{rng(allnone, 'des')[1]:.3f}.  With the 1.7 Mpc phantom stand-in: KiDS {rng(allph, 'kids')[0]:.3f}-{rng(allph, 'kids')[1]:.3f}, DES {rng(allph, 'des')[0]:.3f}-{rng(allph, 'des')[1]:.3f}.
  chi2_min of those phantom fits: KiDS {min(v['kids']['chi2'] for v in allph.values()):.0f}-{max(v['kids']['chi2'] for v in allph.values()):.0f}, DES {min(v['des']['chi2'] for v in allph.values()):.0f}-{max(v['des']['chi2'] for v in allph.values()):.0f} (noiseless).
  Sensitivities (canonical, nominal): """ + "; ".join(f"{k.split('phantom ')[1]}: KiDS {v['kids']['S8']:.3f} (chi2 {v['kids']['chi2']:.0f}), DES {v['des']['S8']:.3f} (chi2 {v['des']['chi2']:.0f})" for k, v in sens.items()) + """.
  Published: KiDS-1000 0.764, KiDS-Legacy 0.815, DES Y3 0.759/0.772, HSC Y3 0.769/0.776.""")
n_fail = sum(1 for _, ok, lb in CH if lb and not ok)
OUT["summary"] = dict(n_checks=len(CH), load_bearing_failed=n_fail, runtime_s=round(time.time() - T0, 1))
json.dump(OUT, open(os.path.join(OUTD, f"{SLUG}_results{SUF}.json"), "w"), indent=1,
          default=lambda o: (o.tolist() if hasattr(o, "tolist") else (float(o) if isinstance(o, np.floating) else str(o))))
P(f"\n  checks: {sum(ok for _, ok, _ in CH)}/{len(CH)} pass; load-bearing failures: {n_fail}   {el()}")
sys.exit(1 if n_fail else 0)
