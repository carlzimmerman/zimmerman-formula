#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XR33 part 2/2 -- THE JOINT LENSING + DYNAMICS TEST OF THE CHAIN'S LAW ON SLACS, AND THE LCDM CONTROL.

QUESTION.  With the IMF normalisation the chain needs for the Einstein mass (part 1), does the chain's law also predict the SDSS
aperture velocity dispersions of the same lenses?  And does the same Jeans + lensing machinery, run with the standard stellar +
NFW decomposition, reproduce the published LCDM results (Auger+2010's dark fractions, Treu+2010's per-lens IMF)?

THE LAW.  As in part 1 (XR33_lensing_imf.py): spherical, g = g_N + a0 x_P2(y - y_th), PPN gamma = 1, band-pass cut at 2 L(z_l).
The tracer is the de Vaucouleurs light with Auger+2010's rest-frame-V r_e (exactly deprojected); orbits isotropic (Treu+2010,
Auger+2010's baseline), constant-beta brackets; the SDSS fibre (radius 1.5") with Gaussian seeing FWHM 1.5" (Posacki+2015's
'typical for SDSS'), brackets 1.0" and 1.8".  sigma_SDSS and its error from Auger+2009 (= Bolton+2008).

THE LCDM CONTROL.  Stars (de Vaucouleurs as above; Hernquist with a = r_e/1.8153 where reproducing Treu+2010) + NFW halo:
  LC1  NFW with break radius 30 kpc (Treu+2010) normalised to the lensing mass at a fixed Chabrier or Salpeter IMF: the projected
       dark fraction inside r_e/2 against Auger+2010 Table 1's f_DM (their power-law lensing + dynamics mass at r_e/2).
  LC2  per lens, the stellar mass and the halo normalisation from M_E and sigma_SDSS together (Treu+2010's method: Hernquist
       stars, isotropic, r_b = 30 kpc): log alpha_Salp against Treu+2010's per-lens values.
  LC3  (reported) Moster+2013 abundance-matched halos (Dutton & Maccio 2014 c200): alpha from lensing alone and the dispersions
       it predicts.

CHECKS.  V* and LC1/LC2 are controls (load-bearing).  J* are results (reported).  H7 is the pre-declared hypothesis (verdict);
P2 is the load-bearing MUTATE target.
  V1  Jeans machinery: a r^-3 tracer in a singular isothermal potential has sigma_ap = v_c/sqrt(3) for any aperture, seeing and
      constant beta (analytic).
  V2  the record's own spherical Jeans solver (hunt_2026/h53_h54_slacs_lenses.py, item 54b, committed f33d4e86a), re-typed with
      its constants, kernel, deprojection, grid, aperture and 70-lens sample, reproduces the committed sigma ratios (Salpeter):
      canonical 0.856 (V) / 0.955 (I); Newton 0.824 / 0.934.
  LC1 median |f_DM(model) - f_DM(Auger+2010)| <= 0.03 for both IMFs (59 lenses).
  LC2 median log alpha_Salp(this lane) - log alpha(Treu+2010) within +-0.05 dex, Pearson r >= 0.5, over the lenses in common.

PRE-DECLARED HYPOTHESIS (written before the first full run; not changed afterwards):
  H7  (verdict) joint lensing + dynamics in the chain's law: with the lensing-required IMF, the predicted aperture dispersion
      matches sigma_SDSS -- median sigma_pred/sigma_obs in [0.95, 1.05] on both footings (53 non-outliers, isotropic, FWHM 1.5").
  P2  (LOAD-BEARING, MUTATE target) the chain's phantom raises the predicted aperture dispersion at fixed IMF by >= 2% (median,
      both footings): the law is active inside the fibre.

MUTATE=1 sets a0 -> 0 everywhere (including the h53 control): V2 and P2 must FAIL (rc = 1); the LCDM controls do not use a0.

DISCLOSURES.  The committed h53 item 54b (sigma ratios 0.86 (V) / 0.96 (I), 'underpowered' because of the band of r_e) was read
before this hypothesis was written; part 1's smoke run (lensing IMF: log alpha_Salp ~ +0.10) had been seen; no dispersion of
this lane had been computed.  The first full run (session scratch, a code test) implemented LC2 as a point estimate (the root
of sigma_pred = sigma_obs, pinned at f* = 1 for 35 of 51 lenses) and failed it (+0.077 dex, r = 0.92); Treu+2010's estimator is
the posterior median of f* under a uniform prior on [0, 1], which LC2 now implements -- threshold unchanged.  That run's
chain results (H7, J) were seen before the recorded runs.

Run from the repository root:  python3 real_research/cross_thread_review_2026_09_26/XR33_jeans_lcdm.py   (MUTATE=1 for the control)
"""
import os, sys, io, json, math, time
import numpy as np
from scipy.special import gammainc
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import XR33_common as C

SLUG = "XR33_jeans_lcdm"
MUTATE = os.environ.get("MUTATE", "0") == "1"
DATA_DIR = os.environ.get("XR33_DATA_DIR", HERE)
OUTDIR = os.environ.get("XR33_OUTDIR", HERE)
SUFFIX = "_MUTATE" if MUTATE else ""
T0 = time.time()


class Tee(io.TextIOBase):
    def __init__(self, *streams):
        self.streams = streams

    def write(self, s):
        for st in self.streams:
            st.write(s)
        return len(s)

    def flush(self):
        for st in self.streams:
            st.flush()


_outf = open(os.path.join(OUTDIR, f"{SLUG}{SUFFIX}.out"), "w")
sys.stdout = Tee(sys.__stdout__, _outf)
OUT = {"lane": "XR33", "part": "2/2 Jeans + LCDM control", "mutate": MUTATE, "checks": {}, "numbers": {}, "hypotheses": {}}
CH = []


def P(*a):
    print(*a, flush=True)


def banner(t):
    P("\n" + "=" * 118 + "\n" + t + "\n" + "=" * 118)


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok)
    CH.append((name, ok, load_bearing))
    OUT["checks"][name.split()[0]] = {"claim": name, "ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}]{'' if load_bearing else ' (reported)'} {name}\n         measured: {measured}")
    if reading:
        P(f"         reading:  {reading}")
    return ok


def med(a):
    a = np.asarray(a, dtype=float)
    return float(np.median(a[np.isfinite(a)]))


P(__doc__.split("CHECKS.")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: a0 -> 0 everywhere (the h53 control included): V2 and P2 must FAIL ***")

A0 = C.a0_footings()
A0_H53 = 9.36e-11
if MUTATE:
    A0 = {k: 0.0 for k in A0}
    A0_H53 = 0.0
FOOTS = ("canonical", "alt")
fp9 = json.load(open(os.path.join(C.CHAIN, "FP9_web_galaxy_separator_results.json")))["numbers"]
Y25 = float(fp9["H2"]["y_th"]["0.25"])
_h6 = 0.6736; _H06 = 100 * _h6 * 1e3 / 3.0856775814913673e22; _rc6 = 3 * _H06 ** 2 / (8 * math.pi * 6.67430e-11)
_Or = (4 * 5.670374419e-8 * 2.7255 ** 4 / 2.99792458e8 ** 3) / _rc6 * (1 + 3.046 * (7 / 8) * (4 / 11) ** (4 / 3))
_Om6 = 0.02237 / _h6 ** 2 + 0.1200 / _h6 ** 2
_OL6 = 1 - _Om6 - _Or
OmL_z = lambda z: _OL6 / (_Or * (1 + z) ** 4 + _Om6 * (1 + z) ** 3 + _OL6)
yth_z = lambda z: Y25 * (OmL_z(0.25) / OmL_z(z)) ** 4.0
L_z = lambda z: 1.3 / OmL_z(0.25) * OmL_z(z) * 1e3                      # n = 2: L = L_Lambda Omega_L, kpc
COSMO = C.Cosmo(0.3, 0.7)
DV = C.Sersic(4.0)
HQ = C.Hernquist()
FWHM, RAP = 1.5, 1.5                                                     # arcsec


def load_tsv(path):
    lines = [l.rstrip("\n") for l in open(path, encoding="latin-1") if not l.startswith("#") and l.strip()]
    hdr = lines[0].split("\t")
    rows = []
    for l in lines[1:]:
        d = {}
        for k, v in zip(hdr, l.split("\t")):
            v = v.strip()
            try:
                d[k] = float(v)
            except ValueError:
                d[k] = v
        rows.append(d)
    return rows


path = os.path.join(C.DATA, "slacs_auger2009_lenses.tsv")
lines = [l.rstrip("\n") for l in open(path, encoding="latin-1")]
hi = [i for i, l in enumerate(lines) if l.startswith("recno")][0]
col = {c_: i for i, c_ in enumerate(lines[hi].split("\t"))}
AUG = {}
for l in lines[hi + 3:]:
    if not l.strip() or l.startswith("#"):
        continue
    r = l.split("\t")

    def F(k):
        try:
            return float(r[col[k]])
        except ValueError:
            return float("nan")
    AUG[r[col["SDSS"]].strip()] = dict(zl=F("zlens"), zs=F("zsrc"), sig=F("sigma"), esig=F("e_sigma"), RE=F("RE"), lME=F("Mass"),
                                       Fc=F("Fc"), Fs=F("Fs"), lMc=F("logMc"), lMs=F("logMs"), elMs=F("e_logMs"), ReV=F("Re(V)"), ReI=F("Re(I)"))
SLX = {r["name"]: r for r in load_tsv(os.path.join(DATA_DIR, "XR33_data_slacsX_auger2010_table1.tsv"))}
TREU = {r["name"]: r for r in load_tsv(os.path.join(DATA_DIR, "XR33_data_treu2010_table1.tsv"))}
S4 = load_tsv(os.path.join(DATA_DIR, "XR33_data_s4tm_shu2017.tsv"))
LENSES = []
for name, x in SLX.items():
    a = AUG[name]
    d = dict(name=name, zl=a["zl"], zs=a["zs"], sig=a["sig"], esig=a["esig"], RE=a["RE"], Fc=a["Fc"], Fs=a["Fs"], lMc=a["lMc"],
             lMs=a["lMs"], elMs=a["elMs"], Re=x["re_V_kpc"], outlier=int(x["outlier"]), fDMc=x["fDM_chab"], fDMs=x["fDM_salp"])
    d["Scr"] = COSMO.Sigma_cr(d["zl"], d["zs"])
    d["ME"] = math.pi * d["Scr"] * d["RE"] ** 2
    d["yth"], d["rcut"] = yth_z(d["zl"]), 2 * L_z(d["zl"])
    d["kpc_as"] = C.ARCSEC * COSMO.DA(d["zl"])
    LENSES.append(d)
P(f"\n  SLACS: {len(LENSES)} lenses ({sum(1 for d in LENSES if not d['outlier'])} non-outliers); a0 = {A0['canonical']:.4e} / "
  f"{A0['alt']:.4e} m/s^2; fibre radius {RAP}\", seeing FWHM {FWHM}\"")


def sig_ap(d, model, fwhm=FWHM, beta=0.0):
    return C.sigma_aperture(model, RAP * d["kpc_as"], fwhm * d["kpc_as"], beta=beta)


# ============================================================================================ V: Jeans machinery
banner("V  JEANS MACHINERY")


class _PL:
    def rho(self, X):
        return np.asarray(X, dtype=float) ** -3.0


class _SIS:
    def __init__(self):
        self.Re, self.prof = 5.0, _PL()

    def g(self, r):
        return 300.0 ** 2 / np.asarray(r)


v1 = [C.sigma_aperture(_SIS(), ra, fw, beta=b) / (300 / math.sqrt(3)) - 1 for ra, fw, b in ((3.0, 1.2, 0.0), (1.0, 3.0, 0.3), (8.0, 0.5, -0.3))]
check("V1 JEANS MACHINERY: a r^-3 tracer in a singular isothermal potential gives sigma_ap = v_c/sqrt(3) for any aperture, "
      "seeing and constant beta", "max rel dev " + f"{max(abs(v) for v in v1):.1e}", max(abs(v) for v in v1) < 1e-3)

G53, KPC53, MSUN53, MPC53 = 6.674e-11, 3.0857e19, 1.989e30, 3.0857e22
_zg = np.linspace(0, 4.0, 4001)
_ig = np.concatenate([[0.0], np.cumsum(0.5 * (1 / np.sqrt(0.3 * (1 + _zg[1:]) ** 3 + 0.7) + 1 / np.sqrt(0.3 * (1 + _zg[:-1]) ** 3 + 0.7)) * np.diff(_zg))])
DA53 = lambda z: (2.99792458e8 / (70e3 / MPC53)) * float(np.interp(z, _zg, _ig)) / (1 + z)
BN53 = 2 * 4.0 - 1 / 3. + 4 / (405 * 4.0) + 46 / (25515 * 4.0 ** 2)
PP53 = 1 - 0.6097 / 4.0 + 0.05463 / 4.0 ** 2
M3D53 = lambda x: gammainc(4.0 * (3 - PP53), BN53 * np.maximum(x, 1e-12) ** 0.25)
rho53 = lambda x: np.maximum(x, 1e-12) ** (-PP53) * np.exp(-BN53 * np.maximum(x, 1e-12) ** 0.25)
nu53 = lambda y: 1.0 / (1.0 - np.exp(-np.sqrt(np.maximum(np.asarray(y, dtype=float), 1e-12))))
_trap = np.trapezoid if hasattr(np, "trapezoid") else np.trapz


def jeans53(Mkg, Re_kpc, a0, Rap_kpc):
    Re = Re_kpc * KPC53
    rr = np.geomspace(1e-4 * Re, 2000 * KPC53, 2500)
    rho = rho53(rr / Re)
    gN = G53 * Mkg * M3D53(rr / Re) / rr ** 2
    g = nu53(gN / a0) * gN if a0 > 0 else gN
    integ = rho * g
    I = np.concatenate([np.cumsum((0.5 * (integ[1:] + integ[:-1]) * np.diff(rr))[::-1])[::-1], [0.0]])
    s2r = I / np.maximum(rho, 1e-300)
    RR = np.geomspace(rr[0] * 5, Rap_kpc * KPC53, 120)
    num, den = [], []
    for R in RR:
        m = rr > R * 1.000001
        w = rr[m] / np.sqrt(rr[m] ** 2 - R ** 2)
        num.append(2 * _trap(rho[m] * s2r[m] * w, rr[m]))
        den.append(2 * _trap(rho[m] * w, rr[m]))
    return math.sqrt(_trap(np.array(num) * RR, RR) / _trap(np.array(den) * RR, RR)) / 1e3


S53 = []
for name, a in AUG.items():
    if all(np.isfinite([a["zl"], a["zs"], a["RE"], a["lME"], a["Fc"], a["Fs"], a["lMc"], a["lMs"]])) and (np.isfinite(a["ReV"]) or np.isfinite(a["ReI"])):
        d = dict(a)
        for b in ("V", "I"):
            v = d["Re" + b] if np.isfinite(d["Re" + b]) else d["Re" + ("I" if b == "V" else "V")]
            d["Re_" + b] = v / 206264.806 * DA53(d["zl"]) / KPC53
        S53.append(d)
v2 = {}
for tag, a0 in (("canonical", A0_H53), ("newton", 0.0)):
    for b in ("V", "I"):
        v2[f"{tag}/{b}"] = float(np.median([jeans53(10 ** d["lMs"] * MSUN53, d["Re_" + b], a0, 1.5 / 206264.806 * DA53(d["zl"]) / KPC53) / d["sig"] for d in S53]))
v2c = {"canonical/V": 0.856, "canonical/I": 0.955, "newton/V": 0.824, "newton/I": 0.934}
OUT["numbers"]["V2"] = dict(reproduced=v2, committed=v2c, N=len(S53))
check("V2 THE RECORD'S OWN SPHERICAL JEANS SOLVER (h53 item 54b, committed f33d4e86a), re-typed, reproduces its committed "
      "Salpeter sigma_pred/sigma_obs medians exactly (70 lenses, 1.5\" fibre, no seeing, isotropic, nu_RAR, a0 = 9.36e-11)",
      "; ".join(f"{k} {v2[k]:.4f} vs {v2c[k]}" for k in v2c), len(S53) == 70 and all(abs(v2[k] - v2c[k]) <= 0.0005 + 1e-12 for k in v2c),
      "under MUTATE the 'canonical' row is computed at a0 = 0 and becomes the Newtonian one")
# this lane's Jeans on h53's inputs (no seeing, same radii, exact deprojection) against the re-typed h53 solver
if A0_H53 > 0:
    mm = []
    for d in S53[:20]:
        Re = d["Re_V"] * KPC53 / C.KPC_M
        m = C.LensModel(DV, Re, 10 ** d["lMs"] * MSUN53 / C.MSUN_KG, A0_H53, "nu_RAR", 0.0, rcut=2000.0)
        Rap = 1.5 / 206264.806 * DA53(d["zl"]) / KPC53 * KPC53 / C.KPC_M
        mm.append(C.sigma_aperture(m, Rap, 0.0) / jeans53(10 ** d["lMs"] * MSUN53, d["Re_V"], A0_H53, 1.5 / 206264.806 * DA53(d["zl"]) / KPC53) - 1)
    v2b = float(np.median(mm))
else:
    v2b = float("nan")
check("V2b (reported) this lane's Jeans integrator on h53's inputs (no seeing; exact instead of Prugniel-Simien deprojection) "
      "agrees with h53's solver", f"median rel dev {v2b:+.4%} (20 lenses)", np.isfinite(v2b) and abs(v2b) < 0.01, load_bearing=False)

# ============================================================================================ LC: the LCDM control
banner("LC  THE LCDM CONTROL: stars + NFW")
m2d_nfw30 = lambda R: float(C.nfw_M2D(np.atleast_1d(R), 30.0, 1.0)[0])
lc1 = {"Chabrier": [], "Salpeter": []}
for d in LENSES:
    for imf, lk, fk in (("Chabrier", "lMc", "fDMc"), ("Salpeter", "lMs", "fDMs")):
        Ms = 10 ** d[lk]
        rhos = (d["ME"] - Ms * float(DV.M2D(d["RE"] / d["Re"]))) / m2d_nfw30(d["RE"])     # may be < 0 where f* > 1 (as in Auger+2010)
        Rh = 0.5 * d["Re"]
        Mst = Ms * float(DV.M2D(0.5))
        fdm = 1 - Mst / (Mst + rhos * m2d_nfw30(Rh))
        lc1[imf].append(fdm - d[fk])
LC1 = {k: (float(np.median(v)), float(np.median(np.abs(v)))) for k, v in lc1.items()}
check("LC1 LCDM CONTROL -- AUGER+2010'S DARK FRACTIONS: stars (de Vaucouleurs, r_e,V) + NFW (break radius 30 kpc) normalised to the "
      "lensing mass reproduce Auger+2010 Table 1's projected f_DM inside r_e/2 at both IMFs",
      "; ".join(f"{k}: median diff {v[0]:+.3f}, median |diff| {v[1]:.3f}" for k, v in LC1.items()),
      all(v[1] <= 0.03 for v in LC1.values()),
      "Auger's f_DM uses the power-law lensing + dynamics mass at r_e/2; this uses the NFW-extrapolated lensing mass -- the "
      "extrapolation from R_E ~ 0.58 r_e to 0.5 r_e is short, so the two must agree")
OUT["numbers"]["LC1"] = LC1


def lcdm_joint(d, prof, fwhm=FWHM, beta=0.0, ngrid=51):
    """Treu+2010's per-lens method: one free parameter, the stellar fraction f* of M_E inside the Einstein cylinder (the NFW,
    r_b = 30 kpc, carries 1 - f*); uniform prior on [0, 1], Gaussian likelihood of sigma_SDSS; the posterior MEDIAN of f* is the
    estimator (their text).  Returns log alpha_Salp at that median and the posterior mass in the top 10% of the prior."""
    Ms = 10 ** d["lMs"]
    f2 = float(np.atleast_1d(prof.M2D(d["RE"] / d["Re"]))[0])
    fs = np.linspace(0.0, 1.0, ngrid)
    sp = []
    for f in fs:
        m = C.LensModel(prof, d["Re"], f * d["ME"] / f2, 0.0, "P2", 0.0, 0.0, 1e4, extra=(30.0, (1 - f) * d["ME"] / m2d_nfw30(d["RE"])))
        sp.append(sig_ap(d, m, fwhm, beta))
    like = np.exp(-0.5 * ((np.array(sp) - d["sig"]) / d["esig"]) ** 2)
    cdf = np.concatenate([[0.0], np.cumsum(0.5 * (like[1:] + like[:-1]) * np.diff(fs))])
    cdf /= cdf[-1]
    fmed = float(np.interp(0.5, cdf, fs))
    return math.log10(fmed * d["ME"] / (Ms * f2)), float(1 - np.interp(0.9, fs, cdf))


lc2 = []
for d in LENSES:
    if d["name"] in TREU:
        la, flag = lcdm_joint(d, HQ)
        lc2.append((la, TREU[d["name"]]["log_alpha"], flag, d["name"]))
lc2a = np.array([[x[0], x[1]] for x in lc2])
off2 = float(np.median(lc2a[:, 0] - lc2a[:, 1]))
r2 = float(np.corrcoef(lc2a[:, 0], lc2a[:, 1])[0, 1])
nb = sum(1 for x in lc2 if x[2] > 0.5)
check("LC2 LCDM CONTROL -- TREU+2010'S PER-LENS IMF: stars (Hernquist, a = r_e/1.8153) + NFW (r_b = 30 kpc), isotropic, alpha and the "
      "halo from M_E and sigma_SDSS together, reproduce Treu+2010's log alpha_Salp lens by lens",
      f"{len(lc2)} lenses in common: median (mine - Treu) {off2:+.3f} dex, Pearson r {r2:.2f}; median log alpha mine "
      f"{np.median(lc2a[:, 0]):+.3f} vs Treu {np.median(lc2a[:, 1]):+.3f}; {nb} lenses with > 50% of the posterior at f* > 0.9",
      abs(off2) <= 0.05 and r2 >= 0.5, "Treu's aperture/seeing treatment is not specified beyond the SDSS fibre; FWHM 1.5\" used here")
OUT["numbers"]["LC2"] = dict(N=len(lc2), offset=off2, r=r2, per_lens=[(x[3], round(x[0], 4), x[1], x[2]) for x in lc2])
# LC2 with the de Vaucouleurs stars (this lane's tracer) for reference, and LC3 (abundance matching)
lc2dv = [lcdm_joint(d, DV)[0] for d in LENSES if not d["outlier"]]
lc3 = []
for d in LENSES:
    M200 = C.moster13_halo(10 ** d["lMc"], d["zl"])
    rs, rhos, cc, r200 = C.nfw_from_M200(M200, d["zl"], COSMO)
    ac = C.solve_alpha(DV, d["Re"], 10 ** d["lMs"], d["RE"], d["ME"], 0.0, "P2", 0.0, 0.0, 1e4, extra=(rs, rhos))
    if np.isfinite(ac):
        m = C.LensModel(DV, d["Re"], ac * 10 ** d["lMs"], 0.0, "P2", 0.0, 0.0, 1e4, extra=(rs, rhos))
        lc3.append((math.log10(ac), sig_ap(d, m) / d["sig"], math.log10(M200)))
    else:
        lc3.append((float("nan"), float("nan"), math.log10(M200)))
lc3 = np.array(lc3)
P(f"  LC2 with de Vaucouleurs stars (53 non-outliers): median log alpha_Salp {np.median(lc2dv):+.3f}")
P(f"  LC3 Moster+2013 abundance-matched NFW (median log M200 {np.nanmedian(lc3[:, 2]):.2f}): lensing-only log alpha_Salp median "
  f"{np.nanmedian(lc3[:, 0]):+.3f} ({int(np.sum(~np.isfinite(lc3[:, 0])))} lenses need a negative stellar mass); its sigma_pred/"
  f"sigma_obs median {np.nanmedian(lc3[:, 1]):.3f}")
OUT["numbers"]["LC3"] = dict(log_alpha=float(np.nanmedian(lc3[:, 0])), sig_ratio=float(np.nanmedian(lc3[:, 1])), logM200=float(np.nanmedian(lc3[:, 2])),
                             LC2_devauc=float(np.median(lc2dv)))

# ============================================================================================ J: the chain's joint test
banner("J  THE CHAIN'S JOINT TEST: the lensing IMF's predicted sigma_SDSS, and the dynamics-only IMF")
JR = {}
for foot in FOOTS:
    a0 = A0[foot]
    rows = []
    for d in LENSES:
        mk = lambda alpha, a0_=a0, **kw: C.LensModel(kw.get("prof", DV), d["Re"], alpha * 10 ** d["lMs"], a0_, kw.get("kernel", "P2"),
                                                       d["yth"], kw.get("gas", 0.0), d["rcut"], kw.get("extra"))
        al = C.solve_alpha(DV, d["Re"], 10 ** d["lMs"], d["RE"], d["ME"], a0, "P2", d["yth"], 0.0, d["rcut"])
        sp = sig_ap(d, mk(al))
        s_newton = sig_ap(d, mk(al, 0.0))
        fdyn = lambda la: sig_ap(d, mk(10 ** la)) - d["sig"]
        try:
            ad = 10 ** brentq(fdyn, -1.0, 1.0, xtol=1e-5)
        except ValueError:
            ad = float("nan")
        rows.append(dict(name=d["name"], outlier=d["outlier"], la_lens=math.log10(al), la_dyn=math.log10(ad), ratio=sp / d["sig"],
                         chi=(sp - d["sig"]) / d["esig"], lift=sp / s_newton - 1, sig=d["sig"], esig=d["esig"]))
    JR[foot] = rows
    cl = [r for r in rows if not r["outlier"]]
    dl = np.array([r["la_dyn"] - r["la_lens"] for r in cl])
    P(f"  {foot:9s} (53 non-outliers): sigma_pred/sigma_obs median {med([r['ratio'] for r in cl]):.3f} (mean "
      f"{np.mean([r['ratio'] for r in cl]):.3f}); chi^2/N {np.mean([r['chi'] ** 2 for r in cl]):.2f} (sigma errors only); "
      f"log alpha_dyn - log alpha_lens: mean {np.nanmean(dl):+.3f} +- {np.nanstd(dl) / math.sqrt(np.sum(np.isfinite(dl))):.3f}, "
      f"median {np.nanmedian(dl):+.3f}; log alpha_dyn median {med([r['la_dyn'] for r in cl]):+.3f} vs lensing "
      f"{med([r['la_lens'] for r in cl]):+.3f}; the phantom lifts sigma by {med([r['lift'] for r in rows]):.3f} at fixed IMF")
    P(f"             all 59: sigma ratio median {med([r['ratio'] for r in rows]):.3f}")
OUT["numbers"]["J"] = {f: dict(sig_ratio=med([r["ratio"] for r in JR[f] if not r["outlier"]]),
                               dlog_alpha_mean=float(np.nanmean([r["la_dyn"] - r["la_lens"] for r in JR[f] if not r["outlier"]])),
                               la_dyn=med([r["la_dyn"] for r in JR[f] if not r["outlier"]]), la_lens=med([r["la_lens"] for r in JR[f] if not r["outlier"]]),
                               lift=med([r["lift"] for r in JR[f]]),
                               per_lens=[{k: (round(v, 5) if isinstance(v, float) else v) for k, v in r.items()} for r in JR[f]]) for f in FOOTS}

# brackets on the predicted dispersion at the lensing IMF (canonical)
BRJ = {}
a0c = A0["canonical"]
x19 = json.load(open(os.path.join(C.LANE, "XR19_web_runaway_results.json")))["numbers"]["X"]
fret = {"XR19 nominal": 1 - float(x19["nominal"]["Fesc0"]), "XR19 halo-only": 1 - float(x19["halo only (nominal)"]["Fesc0"])}
if a0c > 0:
    for lab, kw, extra_kw in (("beta = +0.2", {}, dict(beta=0.2)), ("beta = -0.2", {}, dict(beta=-0.2)),
                              ("seeing FWHM 1.0\"", {}, dict(fwhm=1.0)), ("seeing FWHM 1.8\"", {}, dict(fwhm=1.8)),
                              ("kernel nu_mono", dict(kernel="nu_mono"), {}), ("kernel nu_RAR", dict(kernel="nu_RAR"), {}),
                              ("Sersic n = 3", dict(prof=C.Sersic(3.0)), {}), ("Sersic n = 6", dict(prof=C.Sersic(6.0)), {}),
                              ("Hernquist stars", dict(prof=HQ), {})):
        rr_ = []
        for d in LENSES:
            if d["outlier"]:
                continue
            prof = kw.get("prof", DV)
            al = C.solve_alpha(prof, d["Re"], 10 ** d["lMs"], d["RE"], d["ME"], a0c, kw.get("kernel", "P2"), d["yth"], 0.0, d["rcut"])
            m = C.LensModel(prof, d["Re"], al * 10 ** d["lMs"], a0c, kw.get("kernel", "P2"), d["yth"], 0.0, d["rcut"])
            rr_.append(sig_ap(d, m, **extra_kw) / d["sig"])
        BRJ[lab] = med(rr_)
    for lab, fr in fret.items():
        rr_ = []
        for d in LENSES:
            if d["outlier"]:
                continue
            mdm = max(1.0 - d["Fs"], 0.0) * d["ME"]
            ext = (30.0, fr * mdm / m2d_nfw30(d["RE"]))
            al = C.solve_alpha(DV, d["Re"], 10 ** d["lMs"], d["RE"], d["ME"], a0c, "P2", d["yth"], 0.0, d["rcut"], extra=ext)
            m = C.LensModel(DV, d["Re"], al * 10 ** d["lMs"], a0c, "P2", d["yth"], 0.0, d["rcut"], extra=ext)
            rr_.append(sig_ap(d, m) / d["sig"])
        BRJ[f"dark fluid {lab} (f = {fr:.3f} of the Salpeter-LCDM dark mass)"] = med(rr_)
    P("  brackets (canonical; median sigma_pred/sigma_obs at the lensing IMF, 53 non-outliers; primary "
      f"{OUT['numbers']['J']['canonical']['sig_ratio']:.3f}): " + "; ".join(f"{k}: {v:.3f}" for k, v in BRJ.items()))
OUT["numbers"]["J_brackets"] = BRJ

# S4TM (reported): the same test on the lower-mass sample (F814W r_e, a redder band than rest V)
S4J = {}
for foot in FOOTS:
    a0 = A0[foot]
    rr_ = []
    for r in S4:
        Dl = COSMO.DA(r["zL"])
        d = dict(RE=r["bSIE"] * C.ARCSEC * Dl, Re=r["Reff"] * C.ARCSEC * Dl, kpc_as=C.ARCSEC * Dl, sig=r["sigma_SDSS"])
        d["ME"] = math.pi * COSMO.Sigma_cr(r["zL"], r["zS"]) * d["RE"] ** 2
        Mc = 10 ** r["logMs_chab"]
        al = C.solve_alpha(DV, d["Re"], Mc, d["RE"], d["ME"], a0, "P2", yth_z(r["zL"]), 0.0, 2 * L_z(r["zL"]))
        m = C.LensModel(DV, d["Re"], al * Mc, a0, "P2", yth_z(r["zL"]), 0.0, 2 * L_z(r["zL"]))
        rr_.append(sig_ap(d, m) / d["sig"])
    S4J[foot] = med(rr_)
P("  S4TM (40, reported): sigma_pred/sigma_obs median at the lensing IMF: " + "; ".join(f"{f} {v:.3f}" for f, v in S4J.items()))
OUT["numbers"]["S4TM_J"] = S4J

# ============================================================================================ H / P2
banner("H  THE PRE-DECLARED HYPOTHESIS AND THE MUTATE TARGET")
Jn = OUT["numbers"]["J"]
H7 = check("H7 joint lensing + dynamics in the chain's law: with the lensing-required IMF the predicted SDSS aperture dispersion "
           "matches sigma_SDSS -- median ratio in [0.95, 1.05], both footings (53 non-outliers, isotropic, FWHM 1.5\")",
           "; ".join(f"{f}: {Jn[f]['sig_ratio']:.3f} (log alpha_dyn - log alpha_lens mean {Jn[f]['dlog_alpha_mean']:+.3f})" for f in FOOTS),
           all(0.95 <= Jn[f]["sig_ratio"] <= 1.05 for f in FOOTS), load_bearing=False)
P2 = check("P2 THE CHAIN'S PHANTOM RAISES THE PREDICTED APERTURE DISPERSION AT FIXED IMF BY >= 2% (median, both footings)",
           "; ".join(f"{f}: {Jn[f]['lift']:+.4f}" for f in FOOTS), all(Jn[f]["lift"] >= 0.02 for f in FOOTS),
           "load-bearing MUTATE target: with a0 -> 0 the lift is exactly zero")
OUT["hypotheses"] = {"H7": bool(H7)}

n_lb = sum(1 for _, ok, lb in CH if lb and not ok)
n_ok = sum(1 for _, ok, _ in CH if ok)
banner("VERDICT")
P(f"  {n_ok}/{len(CH)} checks pass; load-bearing failures: {n_lb}")
P(f"  pre-declared hypothesis: H7 {'HELD' if H7 else 'FELL'}")
OUT["summary"] = dict(n_checks=len(CH), n_pass=n_ok, load_bearing_failures=n_lb, runtime_s=round(time.time() - T0, 1))
json.dump(OUT, open(os.path.join(OUTDIR, f"{SLUG}_results{SUFFIX}.json"), "w"), indent=1, default=str)
P(f"  ({time.time() - T0:.0f} s)")
sys.stdout.flush()
sys.exit(1 if n_lb else 0)
