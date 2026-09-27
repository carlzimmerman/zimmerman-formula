#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XR33 part 1/2 -- GALAXY-SCALE STRONG LENSING FROM BARYONS ALONE IN THE DERIVATION CHAIN'S LAW, AND THE IMF IT REQUIRES.

QUESTION.  Does the chain's static law (FP7's AQUAL-type root with FP9's yield and band-pass; heat filter irrelevant at kpc)
reproduce the Einstein masses of SLACS early-type lenses (and S4TM, BELLS, SNELLS) from their baryons alone?  If so, what stellar
IMF normalisation does it need, and is that consistent with independent (spectroscopic; dynamics-with-halo) IMF evidence?

THE LAW (read from the chain; nothing re-derived):  PPN gamma = 1 (FP2 L6a, FP7 R7p), so the lensing mass is the dynamical mass;
in spherical symmetry the AQUAL root gives g = g_N + a0 x_P2(y - y_th), x_P2(D) = sqrt(D^2 + D) - D (FP7 A2: P2 EXACTLY; FP9 Y1),
y_th(z) = y_th(0.25) (Omega_L(0.25)/Omega_L(z))^p' and L(z) = L_Lambda Omega_L(z)^(n/2) with FP9's committed headline constants.
The band-pass removes the phantom beyond ~2L (FP6 G6e); it is applied here as a hard line-of-sight cut at 2 L(z_l) (primary),
with L and 10 Mpc as brackets.  The heat filter changes the law by <= 3e-5 at galaxy scales (FP1 B3) and is not modelled.

DATA (all published; copied/transcribed unchanged into XR33_data_*.tsv with provenance headers, except the first):
  SLACS  Auger et al. 2009, ApJ 705, 1099 (VizieR J/ApJ/705/1099; the record's real_research/data/slacs_auger2009_lenses.tsv):
         z_l, z_s, sigma_SDSS, R_E (kpc), log M_E, f*_Ein, log M* (Chabrier, Salpeter);  Auger et al. 2010, ApJ 724, 511, Table 1:
         rest-frame V effective radius r_e,V, sigma_e2, outlier flags (the 59 lenses with robust lensing + kinematics).
  S4TM   Shu et al. 2017, ApJ 851, 48 (VizieR J/ApJ/851/48): 40 grade-A lower-mass lenses, Chabrier M* from Shu et al. 2015.
  BELLS  Brownstein et al. 2012, ApJ 744, 41: 25 grade-A z ~ 0.5 lenses (22 early type); M* is NOT published -- derived here from
         F814W with a calibration on SLACS's own SPS masses (part S; a calibration-limited sample, reported, not load-bearing).
  SNELLS Smith, Lucey & Conroy 2015, MNRAS 449, 3441: three z < 0.055 lenses with R_Ein ~ 2 kpc (J-band L_Ein, Upsilon_ref).
  IMF    Conroy & van Dokkum 2012, ApJ 760, 71, Table 2 (spectroscopic, gravity-independent: 34 ETGs);  relations quoted from
         Cappellari et al. 2013, MNRAS 432, 1862 (ATLAS3D XX; dynamics with dark halos), Posacki et al. 2015, MNRAS 446, 493
         (lensing + dynamics with a halo), Treu et al. 2010, ApJ 709, 1195 and Auger et al. 2010, ApJ 721, L163 (SLACS + NFW);
         Barnabe et al. 2013, MNRAS 436, 253 (SSP slopes of two SLACS lenses).
  Cosmology for lens geometry: (Om, OL, h) = (0.3, 0.7, 0.7) -- the SLACS tables' own; M*/M_E scales as h^-1 (bracket).

UNITS OF THE IMF NORMALISATION.  alpha_Salp = M*(required)/M*(SPS, Salpeter) on Auger et al.'s scale (Salpeter - Chabrier =
0.25 dex); CvD12b's (M/L)/(M/L)_MW is converted with their 'Salpeter ~ 1.6'; SNELLS's Kroupa alpha with their 'Salpeter = 1.55'.

CHECKS.  C* = controls (load-bearing: the run is valid only if they pass).  L*, B*, S*, I* = results (reported).  H* = the
PRE-DECLARED HYPOTHESES below (verdicts; load-bearing only where marked).  P1 and H2 are the MUTATE targets.

  C1  lens geometry: M_E recomputed from R_E, z_l, z_s reproduces Auger's log M_E (and S4TM's log M_Ein from bSIE).
  C2  the Newtonian, stars-only limit reproduces Auger et al.'s stellar-only Einstein masses f*_Ein M_E (both IMFs) with r_e,V.
  C3  the record's own spherical MOND lensing solver (hunt_2026/h53_h54_slacs_lenses.py, committed f33d4e86a): its re-typed
      algorithm reproduces the committed .out numbers exactly (canonical, V band: boost 1.168, kappa_bar(Salpeter) 0.825, R_E ratio
      0.840; I band 1.136, 0.794), and this lane's integrator on the same inputs agrees with it (C3b).
  C4  the chain's law as implemented = FP7's closed form (mu_s(x) x = y, x = sqrt(y^2+y) - y); FP9's committed y_th(z) table and
      L(0) reproduced from its constants; XC4's committed nu_mono splice point y* = 2.3374124053 reproduced.
  C5  numerics: exact deprojection projects back to the Sersic law (<= 1e-4); the phantom's u-substitution projection equals a
      brute-force projection (<= 1e-5).
  C6  SNELLS: this lane's a0 -> 0 alpha reproduces SNELLS's own 'no dark matter' alpha (their Table, case c) for all three lenses.

PRE-DECLARED HYPOTHESES (written before the first full run; thresholds not changed afterwards):
  H1  (verdict) the chain reproduces the SLACS Einstein masses with a STANDARD IMF: median kappa_bar in [0.9, 1.1] for Chabrier or
      for Salpeter, on both footings.
  H2  (LOAD-BEARING, the MUTATE target) the IMF the chain requires is physically attainable: SLACS median alpha_Salp <= 1.275,
      the heaviest spectroscopic IMF among CvD12b's 34 early-type galaxies (NGC 4552, alpha_MW = 2.04 -> 2.04/1.6), both footings.
  H3  (verdict) the chain's required IMF agrees with spectroscopy at matched sigma: SLACS mean offset <log alpha_chain -
      log alpha_CvD(sigma)> within +-0.10 dex (CvD12b relation fitted here, sigma at R_e/8), both footings.
  H4  (verdict) one IMF(sigma) serves both radii: the chain's alpha_Salp from SNELLS (R_Ein ~ 0.2-0.7 R_e, sigma >= 320) is not
      below the chain's SLACS median at sigma_SDSS >= 280 by more than 0.10 dex, both footings.
  H5  (verdict) lower-mass lenses: the chain's S4TM mean offset from the CvD12b relation is within +-0.10 dex, both footings.
  H6  (reported only; calibration-limited) BELLS (z ~ 0.5, R_E ~ R_e): mean offset from the CvD12b relation within +-0.15 dex.
  P1  (LOAD-BEARING, MUTATE target) at the chain's required IMF the phantom supplies >= 5% of the SLACS Einstein mass (median).

MUTATE=1 sets a0 -> 0 everywhere (the chain's law becomes Newton on the baryons, and the h53 control runs at a0 = 0): C3, P1
and H2 must FAIL (rc = 1) -- an a0-free universe needs alpha_Salp ~ 1/f*_Salp, heavier than any spectroscopic IMF.

DISCLOSURES.  (1) The committed h53/h54 result (nu_RAR kernel: kappa_bar(Salp) 0.79-0.85, R_E short 14-18%) was read before
these hypotheses were written; this lane's own P2 numbers were not computed before the docstring was fixed.  (2) Smoke tests
of the shared machinery (deprojection, projection, Jeans, h53 re-typing, data transcription, the SLACS X r_e,V validation of C2)
were run in the session scratch before the first full run.  (3) The dark fluid is carried only as a labelled bracket (XR19).
(4) The first full run of this script went to the session scratch as a code test (one crash fixed: a scalar index in C3b).
After it, and with no threshold changed: the dark-fluid bracket, first anchored on abundance-matched halos (median log M200
14.05, the Chabrier-LCDM halo Auger+2010 disfavour), was re-anchored on the dark mass LCDM lensing requires at a Salpeter IMF
(the abundance-matched anchor kept as the upper bracket); and LCDM's own IMF (Treu+2010, SNELLS default) was added to part I
so that a failure shared with LCDM is visible.

Run from the repository root:  python3 real_research/cross_thread_review_2026_09_26/XR33_lensing_imf.py   (MUTATE=1 for the control)
"""
import os, sys, io, json, math, time
import numpy as np
from scipy.special import gammainc
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import XR33_common as C

SLUG = "XR33_lensing_imf"
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
OUT = {"lane": "XR33", "part": "1/2 lensing + IMF", "mutate": MUTATE, "checks": {}, "numbers": {}, "hypotheses": {}}
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


RNG = np.random.default_rng(3301)


def boot_med(a, n=2000):
    a = np.asarray(a, dtype=float)
    a = a[np.isfinite(a)]
    bs = np.array([np.median(a[RNG.integers(0, len(a), len(a))]) for _ in range(n)])
    return float(np.median(a)), float(bs.std())


P(__doc__.split("CHECKS.")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: a0 -> 0 everywhere (Newton on the baryons; the h53 control at a0 = 0): C3, P1 and H2 must FAIL ***")

# ============================================================================================ inputs from the chain
A0 = C.a0_footings()
A0_H53 = 9.36e-11                                             # hunt_lib.A0["canonical"] used by the committed h53
if MUTATE:
    A0 = {k: 0.0 for k in A0}
    A0_H53 = 0.0
FOOTS = ("canonical", "alt")
fp9 = json.load(open(os.path.join(C.CHAIN, "FP9_web_galaxy_separator_results.json")))["numbers"]
YTH_COMMITTED = {float(k): float(v) for k, v in fp9["H2"]["y_th"].items()}
CONST9 = {row[0]: row[1] for row in fp9["constants"]}
N_BP = float(CONST9["n"])
L_LAMBDA = float(CONST9["L_Lambda"].split()[0])               # Mpc (rounded in the table; L(0.25) = 1.3 Mpc is the headline)
P_PRIME = float(CONST9["p'"])
Y25 = YTH_COMMITTED[0.25]
# FP6's Omega_L(z) (its exact constants), on which FP9's running is defined
_h6 = 0.6736; _c6 = 2.99792458e8; _Mpc6 = 3.0856775814913673e22; _G6 = 6.67430e-11
_H06 = 100 * _h6 * 1e3 / _Mpc6; _rc6 = 3 * _H06 ** 2 / (8 * math.pi * _G6)
_Og = (4 * 5.670374419e-8 * 2.7255 ** 4 / _c6 ** 3) / _rc6
_Or = _Og * (1 + 3.046 * (7 / 8) * (4 / 11) ** (4 / 3))
_Om6 = 0.02237 / _h6 ** 2 + 0.1200 / _h6 ** 2
_OL6 = 1 - _Om6 - _Or
OmL_z = lambda z: _OL6 / (_Or * (1 + z) ** 4 + _Om6 * (1 + z) ** 3 + _OL6)
yth_z = lambda z: Y25 * (OmL_z(0.25) / OmL_z(z)) ** P_PRIME
L25 = 1.3                                                     # FP9 headline L(0.25) [Mpc]
L_LAMBDA_EXACT = L25 / OmL_z(0.25) ** (N_BP / 2)
L_z = lambda z: L_LAMBDA_EXACT * OmL_z(z) ** (N_BP / 2) * 1e3   # kpc (physical)
P(f"\n  inputs: a0 = {A0['canonical']:.4e} / {A0['alt']:.4e} m/s^2 (FP0); FP9 (H_Y): n = {N_BP}, L(0.25) = {L25} Mpc "
  f"(L_Lambda = {L_LAMBDA_EXACT:.3f} Mpc), y_th(0.25) = {Y25:g}, p' = {P_PRIME}")

COSMO = C.Cosmo(0.3, 0.7)
DV = C.Sersic(4.0)


def load_tsv(path):
    lines = [l.rstrip("\n") for l in open(path, encoding="latin-1") if not l.startswith("#") and l.strip()]
    hdr = lines[0].split("\t")
    rows = []
    for l in lines[1:]:
        p = l.split("\t")
        d = {}
        for k, v in zip(hdr, p):
            v = v.strip()
            try:
                d[k] = float(v)
            except ValueError:
                d[k] = v
        rows.append(d)
    return rows


def load_auger2009():
    path = os.path.join(C.DATA, "slacs_auger2009_lenses.tsv")
    lines = [l.rstrip("\n") for l in open(path, encoding="latin-1")]
    hi = [i for i, l in enumerate(lines) if l.startswith("recno")][0]
    hdr = lines[hi].split("\t")
    col = {c_: i for i, c_ in enumerate(hdr)}
    out = {}
    for l in lines[hi + 3:]:
        if not l.strip() or l.startswith("#"):
            continue
        r = l.split("\t")

        def F(k):
            try:
                return float(r[col[k]])
            except ValueError:
                return float("nan")
        out[r[col["SDSS"]].strip()] = dict(zl=F("zlens"), zs=F("zsrc"), sig=F("sigma"), esig=F("e_sigma"), RE=F("RE"),
                                           lME=F("Mass"), Fc=F("Fc"), Fs=F("Fs"), lMc=F("logMc"), elMc=F("e_logMc"),
                                           lMs=F("logMs"), elMs=F("e_logMs"), Imag=F("Imag"), ReV=F("Re(V)"), ReI=F("Re(I)"),
                                           mtype=r[col["MType"]].strip(), comp=r[col["f_MType"]].strip())
    return out


AUG = load_auger2009()
SLX = {r["name"]: r for r in load_tsv(os.path.join(DATA_DIR, "XR33_data_slacsX_auger2010_table1.tsv"))}
S4 = load_tsv(os.path.join(DATA_DIR, "XR33_data_s4tm_shu2017.tsv"))
BE = load_tsv(os.path.join(DATA_DIR, "XR33_data_bells_brownstein2012.tsv"))
SN = load_tsv(os.path.join(DATA_DIR, "XR33_data_snells_smith2015.tsv"))
CVD = load_tsv(os.path.join(DATA_DIR, "XR33_data_cvd12b_table2.tsv"))
TREU = {r["name"]: r for r in load_tsv(os.path.join(DATA_DIR, "XR33_data_treu2010_table1.tsv"))}

LENSES = []
for name, x in SLX.items():
    a = AUG[name]
    d = dict(name=name, zl=a["zl"], zs=a["zs"], sig=a["sig"], esig=a["esig"], RE=a["RE"], lME_tab=a["lME"], Fc=a["Fc"], Fs=a["Fs"],
             lMc=a["lMc"], elMc=a["elMc"], lMs=a["lMs"], elMs=a["elMs"], Re=x["re_V_kpc"], sig_e2=x["sig_e2"],
             outlier=int(x["outlier"]), fDMc=x["fDM_chab"], fDMs=x["fDM_salp"], comp=a["comp"])
    d["Scr"] = COSMO.Sigma_cr(d["zl"], d["zs"])
    d["ME"] = math.pi * d["Scr"] * d["RE"] ** 2
    d["yth"] = yth_z(d["zl"])
    d["rcut"] = 2 * L_z(d["zl"])
    LENSES.append(d)
P(f"\n  SLACS: {len(LENSES)} lenses with Auger+2010's rest-frame-V effective radius ({sum(1 for d in LENSES if not d['outlier'])} "
  f"non-outliers); median z_l {med([d['zl'] for d in LENSES]):.3f}, R_E {med([d['RE'] for d in LENSES]):.2f} kpc, r_e,V "
  f"{med([d['Re'] for d in LENSES]):.2f} kpc, R_E/r_e {med([d['RE'] / d['Re'] for d in LENSES]):.3f}, sigma_SDSS "
  f"{med([d['sig'] for d in LENSES]):.0f} km/s")

# ============================================================================================ C1-C6 controls
banner("C  CONTROLS")
dME = np.array([math.log10(d["ME"]) - d["lME_tab"] for d in LENSES])
s4g = []
for r in S4:
    Dl = COSMO.DA(r["zL"])
    r["RE"] = r["bSIE"] * C.ARCSEC * Dl
    r["Scr"] = COSMO.Sigma_cr(r["zL"], r["zS"])
    r["ME"] = math.pi * r["Scr"] * r["RE"] ** 2
    r["Re"] = r["Reff"] * C.ARCSEC * Dl
    s4g.append(math.log10(r["ME"]) - r["logMein"])
s4g = np.array(s4g)
check("C1 LENS GEOMETRY: M_E = pi Sigma_cr R_E^2 recomputed from R_E, z_l, z_s in (0.3, 0.7, 0.7) reproduces Auger+2009's tabulated "
      "log M_E (59 SLACS) and, from bSIE, Shu+2017's log M_Ein (40 S4TM)",
      f"SLACS median {np.median(dME):+.4f} dex, rms {dME.std():.4f}; S4TM median {np.median(s4g):+.4f}, rms {s4g.std():.4f}",
      abs(np.median(dME)) < 0.005 and dME.std() < 0.006 and abs(np.median(s4g)) < 0.005 and s4g.std() < 0.006,
      "the table values are rounded to 0.01 dex (SLACS) and 0.01 dex (S4TM); S4TM's own WMAP7 geometry differs by < 0.001 dex")

c2 = {}
for imf, lk, fk in (("Chabrier", "lMc", "Fc"), ("Salpeter", "lMs", "Fs")):
    r_ = np.array([10 ** d[lk] * float(DV.M2D(d["RE"] / d["Re"])) / (d[fk] * d["ME"]) for d in LENSES])
    c2[imf] = (float(np.median(r_)), float(np.log10(r_).std()))
check("C2 NEWTONIAN STARS-ONLY LIMIT: a de Vaucouleurs stellar body with Auger+2010's rest-frame-V r_e and Auger+2009's M* puts "
      "exactly Auger+2009's stellar-only Einstein mass f*_Ein M_E inside R_E (both IMFs)",
      f"model/Auger: Chabrier median {c2['Chabrier'][0]:.4f} (rms {c2['Chabrier'][1]:.4f} dex), Salpeter {c2['Salpeter'][0]:.4f} "
      f"(rms {c2['Salpeter'][1]:.4f} dex)",
      all(abs(v[0] - 1) < 0.02 and v[1] < 0.02 for v in c2.values()),
      "this settles the record's h53 validation-B offset (-8%/+12% with the observed-band radii): Auger used r_e interpolated to "
      "rest-frame 5500 A; with it the stellar model is Auger's own to rounding")
OUT["numbers"]["C2"] = c2

# ---- C3: the record's h53 spherical lensing solver, re-typed (constants, kernel, deprojection, grid and sample as committed)
G53, KPC53, MSUN53, C53, MPC53 = 6.674e-11, 3.0857e19, 1.989e30, 2.99792458e8, 3.0857e22
_zg = np.linspace(0, 4.0, 4001)
_ig = np.concatenate([[0.0], np.cumsum(0.5 * (1 / np.sqrt(0.3 * (1 + _zg[1:]) ** 3 + 0.7) + 1 / np.sqrt(0.3 * (1 + _zg[:-1]) ** 3 + 0.7)) * np.diff(_zg))])
DA53 = lambda z: (C53 / (70e3 / MPC53)) * float(np.interp(z, _zg, _ig)) / (1 + z)
BN53 = 2 * 4.0 - 1 / 3. + 4 / (405 * 4.0) + 46 / (25515 * 4.0 ** 2)
PP53 = 1 - 0.6097 / 4.0 + 0.05463 / 4.0 ** 2
M2D53 = lambda x: float(gammainc(8.0, BN53 * max(float(x), 1e-12) ** 0.25))
M3D53 = lambda x: gammainc(4.0 * (3 - PP53), BN53 * np.maximum(x, 1e-12) ** 0.25)
nu53 = lambda y: 1.0 / (1.0 - np.exp(-np.sqrt(np.maximum(np.asarray(y, dtype=float), 1e-12))))
_trap = np.trapezoid if hasattr(np, "trapezoid") else np.trapz


def boost53(Mkg, Re_kpc, a0, Rm, rmax_kpc=3000.0, n=6000):
    if a0 <= 0:
        return 1.0
    Re = Re_kpc * KPC53
    rr = np.geomspace(1e-5 * Re, rmax_kpc * KPC53, n)
    Mb = Mkg * M3D53(rr / Re)
    gN = G53 * Mb / rr ** 2
    dM = np.gradient(nu53(gN / a0) * Mb - Mb, rr)
    w = np.where(rr <= Rm, 1.0, 1.0 - np.sqrt(np.clip(1.0 - (Rm / np.maximum(rr, 1e-30)) ** 2, 0, 1)))
    return 1.0 + float(_trap(dM * w, rr)) / (Mkg * M2D53(Rm / Re))


S53 = []
for name, a in AUG.items():
    if all(np.isfinite([a["zl"], a["zs"], a["RE"], a["lME"], a["Fc"], a["Fs"], a["lMc"], a["lMs"]])) and (np.isfinite(a["ReV"]) or np.isfinite(a["ReI"])):
        d = dict(a)
        for b in ("V", "I"):
            v = d["Re" + b] if np.isfinite(d["Re" + b]) else d["Re" + ("I" if b == "V" else "V")]
            d["Re_" + b] = v / 206264.806 * DA53(d["zl"]) / KPC53
        S53.append(d)


def solve_u53(d, a0, b):
    Ms = 10 ** d["lMs"] * MSUN53
    den = M2D53(d["RE"] / d["Re_" + b])
    g = lambda u: d["Fs"] * boost53(Ms, d["Re_" + b], a0, u * d["RE"] * KPC53) * M2D53(u * d["RE"] / d["Re_" + b]) / den - u ** 2
    return brentq(g, 0.05, 5.0, xtol=1e-6) if g(0.05) * g(5.0) < 0 else float("nan")


BV = np.array([boost53(10 ** d["lMs"] * MSUN53, d["Re_V"], A0_H53, d["RE"] * KPC53) for d in S53])
BI = np.array([boost53(10 ** d["lMs"] * MSUN53, d["Re_I"], A0_H53, d["RE"] * KPC53) for d in S53])
FS53 = np.array([d["Fs"] for d in S53])
uV = np.array([solve_u53(d, A0_H53, "V") for d in S53])
rep = dict(N=len(S53), B_V=float(np.median(BV)), kappa_V=float(np.median(BV * FS53)), B_I=float(np.median(BI)),
           kappa_I=float(np.median(BI * FS53)), RE_ratio_V=float(np.nanmedian(uV)))
committed = dict(N=70, B_V=1.168, kappa_V=0.825, B_I=1.136, kappa_I=0.794, RE_ratio_V=0.840)
OUT["numbers"]["C3"] = dict(reproduced=rep, committed=committed)
c3ok = rep["N"] == 70 and all(abs(rep[k] - committed[k]) <= 0.0005 + 1e-12 for k in ("B_V", "kappa_V", "B_I", "kappa_I", "RE_ratio_V"))
check("C3 THE RECORD'S OWN SPHERICAL MOND LENSING SOLVER (h53_h54_slacs_lenses.py, committed f33d4e86a), re-typed with its "
      "constants, nu_RAR kernel, Prugniel-Simien deprojection, grid and 70-lens sample, reproduces its committed .out exactly",
      f"N {rep['N']}; boost(V) {rep['B_V']:.4f} vs 1.168; kappa_bar(Salp, V) {rep['kappa_V']:.4f} vs 0.825; boost(I) "
      f"{rep['B_I']:.4f} vs 1.136; kappa_bar(Salp, I) {rep['kappa_I']:.4f} vs 0.794; R_E ratio(V) {rep['RE_ratio_V']:.4f} vs 0.840",
      c3ok, "a0 = 9.36e-11 (the hunt's rounded canonical value); under MUTATE the same computation at a0 = 0 cannot reproduce it")
# C3b: this lane's integrator on h53's inputs (nu_RAR, a0 = 9.36e-11, observed V-band r_e, exact deprojection instead of PS)
if A0_H53 > 0:
    mine = []
    for d in S53[:70]:
        m = C.LensModel(DV, d["Re_V"] * KPC53 / C.KPC_M, 10 ** d["lMs"] * MSUN53 / C.MSUN_KG, A0_H53, "nu_RAR", 0.0, rcut=3000.0)
        mine.append(1 + float(m.M2D_phantom(d["RE"] * KPC53 / C.KPC_M)[0]) / float(m.M2D_star(d["RE"] * KPC53 / C.KPC_M)[0]))
    mine = np.array(mine)
    c3b = float(np.median(mine / BV) - 1)
else:
    c3b = float("nan")
check("C3b this lane's projection integrator on h53's inputs (same kernel, a0, radii; exact instead of Prugniel-Simien "
      "deprojection) agrees with h53's boost lens by lens",
      f"median (mine/h53 - 1) = {c3b:+.4%}", np.isfinite(c3b) and abs(c3b) < 0.005,
      "the residual is the Prugniel-Simien approximation plus h53's np.gradient grid; the physics is the same")

# ---- C4: the chain's law as implemented
ytest = np.logspace(-6, 6, 25)
h_, _ = C._p2(ytest)
xcl = np.sqrt(ytest ** 2 + ytest) - ytest
mus = h_ / (1 - 2 * h_)
c4_law = float(np.max(np.abs(h_ - xcl) / xcl))
c4_first = float(np.max(np.abs(mus * h_ - ytest) / ytest))
yt_rep = {z: yth_z(z) for z in (0.0, 0.25, 1.0, 2.0)}
c4_yth = max(abs(yt_rep[z] / YTH_COMMITTED[z] - 1) for z in yt_rep)
L0 = L_z(0.0) / 1e3
check("C4 THE CHAIN'S LAW AS IMPLEMENTED: the phantom equals FP7 A2's closed form x = sqrt(y^2+y) - y and satisfies the AQUAL "
      "first integral mu_s(x) x = y (mu_s = x/(1-2x)); FP9's committed y_th(z) table and L(0) = 1.69 Mpc follow from its constants; "
      "XC4's committed nu_mono splice y* = 2.3374124053 is reproduced",
      f"max rel |h - x_cl| {c4_law:.1e}; max rel |mu_s x - y| {c4_first:.1e}; y_th(0/0.25/1/2) = "
      + "/".join(f"{v:.3g}" for v in yt_rep.values()) + f" (max rel dev {c4_yth:.1e}); L(0) = {L0:.3f} Mpc; y* = {C.YS_MONO:.10f}",
      c4_law < 1e-9 and c4_first < 1e-9 and c4_yth < 2e-3 and abs(L0 - 1.69) < 0.006 and abs(C.YS_MONO - 2.3374124053) < 1e-9)

# ---- C5: numerics
Xs = np.array([0.1, 0.3, 0.6, 1.0, 2.0])
back = []
for Xi in Xs:
    u = np.linspace(0, math.acosh(3e3 / Xi), 20000)
    r = Xi * np.cosh(u)
    back.append(float(DV.M3D(np.array([Xi]))[0]) + _trap(4 * math.pi * r ** 2 * DV.rho(r) * (1 - np.tanh(u)) * Xi * np.sinh(u), u))
c5a = float(np.max(np.abs(np.array(back) / DV.M2D(Xs) - 1)))
mt = C.LensModel(DV, 7.0, 10 ** 11.5, 9.3603e-11, "P2", 0.0, rcut=1e4)
Rt = np.array([2.0, 4.0, 8.0])
uph = mt.M2D_phantom(Rt)
rr = np.geomspace(1e-4, 1e4, 400000)
yy = C.G * mt.Mb(rr) / (rr ** 2 * mt.a0)
hh, _ = C._p2(yy)
Mph = (mt.a0 / C.G) * rr ** 2 * hh
rm = np.sqrt(rr[1:] * rr[:-1])
bf = np.array([np.sum(np.diff(Mph) * np.where(rm <= R, 1.0, 1 - np.sqrt(np.clip(1 - (R / rm) ** 2, 0, 1)))) + Mph[0] for R in Rt])
c5b = float(np.max(np.abs(uph / bf - 1)))
check("C5 NUMERICS: the exact Abel deprojection of the de Vaucouleurs law projects back to the incomplete-gamma law, and the "
      "phantom's u-substitution projection equals a brute-force (400k-shell) projection",
      f"deprojection round trip max rel dev {c5a:.1e}; phantom projection max rel dev {c5b:.1e}", c5a < 1e-4 and c5b < 1e-5)

# ============================================================================================ L: SLACS in the chain's law
banner("L  SLACS (59 lenses, 53 non-outliers) IN THE CHAIN'S LAW: Einstein masses at fixed IMF, predicted Einstein radii, "
       "and the IMF normalisation required")


def chain_alpha(d, a0, kernel="P2", Mref_key="lMc", prof=DV, Re=None, gasfrac=0.0, rcut=None, extra=None, yth=None):
    return C.solve_alpha(prof, d["Re"] if Re is None else Re, 10 ** d[Mref_key], d["RE"], d["ME"], a0, kernel,
                         d["yth"] if yth is None else yth, gasfrac, d["rcut"] if rcut is None else rcut, extra)


LRES = {}
for foot in FOOTS:
    a0 = A0[foot]
    rows = []
    for d in LENSES:
        mc = C.LensModel(DV, d["Re"], 10 ** d["lMc"], a0, "P2", d["yth"], 0.0, d["rcut"])
        ms = C.LensModel(DV, d["Re"], 10 ** d["lMs"], a0, "P2", d["yth"], 0.0, d["rcut"])
        kc = float(mc.M2D(d["RE"])[0]) / d["ME"]
        ks = float(ms.M2D(d["RE"])[0]) / d["ME"]
        yE = C.G * float(ms.Mb(d["RE"])) / (d["RE"] ** 2 * a0 * C.A_UNIT) if a0 > 0 else float("nan")
        rEc = C.solve_RE(mc, d["Scr"]) / d["RE"]
        rEs = C.solve_RE(ms, d["Scr"]) / d["RE"]
        ac = chain_alpha(d, a0)
        as_ = ac * 10 ** (d["lMc"] - d["lMs"])
        mreq = C.LensModel(DV, d["Re"], ac * 10 ** d["lMc"], a0, "P2", d["yth"], 0.0, d["rcut"])
        share = float(mreq.M2D_phantom(d["RE"])[0]) / d["ME"]
        rows.append(dict(name=d["name"], kc=kc, ks=ks, yE_salp=yE, rEc=rEc, rEs=rEs, la_chab=math.log10(ac), la_salp=math.log10(as_),
                         share=share, sig=d["sig"], sig_e2=d["sig_e2"], outlier=d["outlier"], elM=d["elMs"]))
    LRES[foot] = rows
    kc = [r["kc"] for r in rows]; ks = [r["ks"] for r in rows]
    las = [r["la_salp"] for r in rows]
    m_las, e_las = boot_med(las)
    P(f"  {foot:9s}: y_N(R_E) at Salpeter median {med([r['yE_salp'] for r in rows]):.2f};  kappa_bar = M_2D(R_E)/M_E: Chabrier "
      f"{med(kc):.3f}, Salpeter {med(ks):.3f};  R_E(pred)/R_E(obs): Chabrier {med([r['rEc'] for r in rows]):.3f}, Salpeter "
      f"{med([r['rEs'] for r in rows]):.3f};  required log alpha_Salp {m_las:+.3f} +- {e_las:.3f} (median; mean "
      f"{np.mean(las):+.3f}, scatter {np.std(las):.3f} vs median SPS error {med([r['elM'] for r in rows]):.3f}); log alpha_Chab "
      f"{med([r['la_chab'] for r in rows]):+.3f};  phantom share of M_E {med([r['share'] for r in rows]):.3f}")
    clean = [r for r in rows if not r["outlier"]]
    P(f"             non-outliers (53): log alpha_Salp median {med([r['la_salp'] for r in clean]):+.3f}, kappa_bar Salpeter "
      f"{med([r['ks'] for r in clean]):.3f}")
OUT["numbers"]["L"] = {f: dict(kappa_chab=med([r["kc"] for r in LRES[f]]), kappa_salp=med([r["ks"] for r in LRES[f]]),
                               RE_ratio_chab=med([r["rEc"] for r in LRES[f]]), RE_ratio_salp=med([r["rEs"] for r in LRES[f]]),
                               log_alpha_salp=boot_med([r["la_salp"] for r in LRES[f]]), log_alpha_chab=med([r["la_chab"] for r in LRES[f]]),
                               phantom_share=med([r["share"] for r in LRES[f]]),
                               per_lens=[{k: (round(v, 5) if isinstance(v, float) else v) for k, v in r.items()} for r in LRES[f]])
                        for f in FOOTS}
check("L1 (reported) the chain's Einstein masses at the two standard IMFs and the IMF it requires (both footings)",
      "; ".join(f"{f}: kappa_bar Chab {OUT['numbers']['L'][f]['kappa_chab']:.3f} / Salp {OUT['numbers']['L'][f]['kappa_salp']:.3f}, "
                f"log alpha_Salp {OUT['numbers']['L'][f]['log_alpha_salp'][0]:+.3f}" for f in FOOTS), True, load_bearing=False)
P1_ok = all(OUT["numbers"]["L"][f]["phantom_share"] >= 0.05 for f in FOOTS)
check("P1 AT THE CHAIN'S REQUIRED IMF THE PHANTOM SUPPLIES >= 5% OF THE SLACS EINSTEIN MASS (median; both footings) -- the chain's "
      "law is active at R_E, a few a0",
      "; ".join(f"{f}: {OUT['numbers']['L'][f]['phantom_share']:.3f}" for f in FOOTS), P1_ok,
      "load-bearing MUTATE target: with a0 -> 0 the share is exactly zero")

# ---- kernel sensitivity (labelled; never pooled with the chain's P2)
KS = {}
for kern in ("nu_mono", "nu_RAR"):
    for foot in FOOTS:
        las = [math.log10(chain_alpha(d, A0[foot], kern) * 10 ** (d["lMc"] - d["lMs"])) for d in LENSES] if A0[foot] > 0 else [float("nan")]
        KS[(kern, foot)] = med(las)
P("  kernel sensitivity (the record's other kernels; NOT the chain's law): median log alpha_Salp " +
  "; ".join(f"{k}/{f} {v:+.3f}" for (k, f), v in KS.items()))
OUT["numbers"]["kernels"] = {f"{k}/{f}": v for (k, f), v in KS.items()}

# ============================================================================================ B: brackets
banner("B  BRACKETS ON THE REQUIRED IMF (median shift of log alpha_Salp over the 59 SLACS lenses, canonical footing)")
a0c = A0["canonical"]
base = np.array([r["la_salp"] for r in LRES["canonical"]])
BR = {}


def bracket(label, fn):
    vals = np.array([fn(d) for d in LENSES])
    la = np.log10(vals * np.array([10 ** (d["lMc"] - d["lMs"]) for d in LENSES]))
    BR[label] = float(np.nanmedian(la - base))
    P(f"    {label:58s} d log alpha = {BR[label]:+.4f}")


if a0c > 0:
    bracket("band-pass cut at L(z_l) instead of 2 L(z_l)", lambda d: chain_alpha(d, a0c, rcut=L_z(d["zl"])))
    bracket("no band-pass (line of sight to 10 Mpc)", lambda d: chain_alpha(d, a0c, rcut=1e4))
    bracket("no yield (y_th = 0)", lambda d: chain_alpha(d, a0c, yth=0.0))
    for gf in (0.02, 0.05, 0.10):
        bracket(f"hot gas {gf:.0%} of the stellar mass, same profile", lambda d, gf=gf: chain_alpha(d, a0c, gasfrac=gf))
    for n_ in (3.0, 6.0):
        prof_n = C.Sersic(n_)
        bracket(f"Sersic n = {n_:g} at fixed M*, r_e (profile systematic)", lambda d, p=prof_n: chain_alpha(d, a0c, prof=p))
    bracket("r_e +3.5% (Auger's quoted model error)", lambda d: chain_alpha(d, a0c, Re=d["Re"] * 1.035))
    bracket("r_e -3.5%", lambda d: chain_alpha(d, a0c, Re=d["Re"] / 1.035))
BR["h = 0.674 instead of 0.7 (M*/M_E ~ h^-1, y unchanged)"] = math.log10(0.674 / 0.7)
P(f"    {'h = 0.674 instead of 0.7 (M*/M_E ~ h^-1, y unchanged)':58s} d log alpha = {BR['h = 0.674 instead of 0.7 (M*/M_E ~ h^-1, y unchanged)']:+.4f}")

# ---- the external field: angle-averaged algebraic (QUMOND-type) internal monopole with a uniform external field
GL_MU, GL_W = np.polynomial.legendre.leggauss(48)


def m2d_efe(d, alpha_chab, a0_si, ge, rcut):
    a0 = a0_si * C.A_UNIT
    r = np.geomspace(1e-4 * d["Re"], rcut, 60000)
    Mb = alpha_chab * 10 ** d["lMc"] * DV.M3D(r / d["Re"])
    gN = C.G * Mb / r ** 2
    gE = ge * a0
    nu = lambda Y: 1.0 + C._p2(Y)[0] / np.maximum(Y, 1e-300)
    Gt = np.sqrt(gN[:, None] ** 2 + gE ** 2 - 2 * gN[:, None] * gE * GL_MU[None, :])
    gr = nu(Gt / a0) * (gN[:, None] - gE * GL_MU[None, :]) + nu(np.array(ge)) * gE * GL_MU[None, :]
    gint = 0.5 * np.sum(gr * GL_W[None, :], axis=1)
    Mph = r ** 2 * gint / C.G - Mb
    rm = np.sqrt(r[1:] * r[:-1])
    R = d["RE"]
    w = np.where(rm <= R, 1.0, 1 - np.sqrt(np.clip(1 - (R / rm) ** 2, 0, 1)))
    return alpha_chab * 10 ** d["lMc"] * float(DV.M2D(R / d["Re"])) + float(np.sum(np.diff(Mph) * w) + Mph[0])


EFE = {}
if a0c > 0:
    for ge in (0.0, 0.01, 0.03, 0.1, 0.3):
        shifts = []
        for d, r0 in zip(LENSES, LRES["canonical"]):
            a_ = 10 ** r0["la_chab"]
            m1 = m2d_efe(d, a_, a0c, ge, d["rcut"])
            m2 = m2d_efe(d, a_ * 1.05, a0c, ge, d["rcut"])
            slope = math.log(m2 / m1) / math.log(1.05)
            shifts.append(-math.log10(m1 / d["ME"]) / slope)
        EFE[ge] = float(np.median(shifts))
    EFE = {ge: v - EFE[0.0] for ge, v in EFE.items()}
    P("    external field (algebraic, angle-averaged; relative to g_e = 0): " + "; ".join(f"g_e = {ge:g} a0: {v:+.4f}" for ge, v in EFE.items()))
OUT["numbers"]["B"] = dict(brackets=BR, efe={str(k): v for k, v in EFE.items()})
efe_ok = bool(EFE) and abs(EFE[0.1]) <= 0.02
check("B1 (reported) THE EXTERNAL FIELD DOES NOT MATTER at R_E: g_e <= 0.1 a0 moves the median required IMF by <= 0.02 dex (the "
      "phantom it removes lies at r >~ sqrt(GM/g_e) ~ 70 kpc, weighted by R_E^2/2r^2 in the Einstein cylinder)",
      "; ".join(f"{ge:g} a0: {v:+.4f}" for ge, v in EFE.items()) if EFE else "not run (a0 = 0)", efe_ok, load_bearing=False)
bp_ok = bool(BR) and all(abs(BR[k]) < 0.01 for k in BR if k.startswith(("band-pass", "no band-pass", "no yield")))
check("B2 (reported) the chain's separator is irrelevant at R_E: band-pass cut (L, 2L, none) and yield on/off move the median "
      "required IMF by < 0.01 dex",
      "; ".join(f"{k}: {v:+.4f}" for k, v in BR.items() if k.startswith(("band-pass", "no band-pass", "no yield"))) if BR else "not run",
      bp_ok, load_bearing=False)

# ---- the dark fluid bracket (XR19): retained fraction x the LCDM dark mass, kernel-invisible (FP10 L11a's design)
#      primary anchor: the dark mass SLACS lensing requires in LCDM at a Salpeter IMF (Treu+2010: <log alpha> = 0.00), i.e. an NFW
#      of break radius 30 kpc (Treu+2010's choice) normalised to (1 - f*_Salp) M_E inside R_E;  upper anchor: Moster+2013
#      abundance-matched halos at the Chabrier M* (Dutton & Maccio 2014 c200) -- the Chabrier-LCDM halo Auger+2010 disfavour.
x19 = json.load(open(os.path.join(C.LANE, "XR19_web_runaway_results.json")))["numbers"]["X"]
FRET = {"XR19 nominal (1 - F_esc(0))": 1 - float(x19["nominal"]["Fesc0"]), "XR19 halo-only (1 - F_esc(0))": 1 - float(x19["halo only (nominal)"]["Fesc0"])}
DF = {}
for d in LENSES:
    M200 = C.moster13_halo(10 ** d["lMc"], d["zl"])
    rs, rhos, cc, r200 = C.nfw_from_M200(M200, d["zl"], COSMO)
    d["nfw_am"] = (rs, rhos)
    d["M200"] = M200
    mdm = max(1.0 - d["Fs"], 0.0) * d["ME"]
    d["nfw_lens"] = (30.0, mdm / float(C.nfw_M2D(np.array([d["RE"]]), 30.0, 1.0)[0]))
if a0c > 0:
    for anchor in ("nfw_lens", "nfw_am"):
        for lab, fr in FRET.items():
            vals = []
            for d, r0 in zip(LENSES, LRES["canonical"]):
                ac = chain_alpha(d, a0c, extra=(d[anchor][0], d[anchor][1] * fr))
                vals.append(math.log10(ac * 10 ** (d["lMc"] - d["lMs"])) - r0["la_salp"])
            DF[f"{anchor}: {lab}"] = (fr, float(np.nanmedian(vals)))
    P("    dark fluid retained as f x the LCDM dark matter, kernel-invisible (Newtonian only): " +
      "; ".join(f"{k}: f = {v[0]:.3f} -> d log alpha {v[1]:+.4f}" for k, v in DF.items()))
    P(f"      anchors: nfw_lens = NFW (r_s 30 kpc) carrying (1 - f*_Salp) M_E inside R_E (median share of M_E "
      f"{med([max(1 - d['Fs'], 0) for d in LENSES]):.3f}); nfw_am = Moster+2013 halo, median log M200 "
      f"{med([math.log10(d['M200']) for d in LENSES]):.2f} (the Chabrier-LCDM halo; an upper bracket)")
OUT["numbers"]["dark_fluid"] = {k: {"f_ret": v[0], "dlog_alpha": v[1]} for k, v in DF.items()}

# ============================================================================================ S: S4TM, BELLS, SNELLS
banner("S  THE OTHER SAMPLES: S4TM (lower masses), BELLS (z ~ 0.5, R_E ~ R_e), SNELLS (R_Ein ~ 2 kpc)")
S4RES = {f: [] for f in FOOTS}
for r in S4:
    r["lMc"] = r["logMs_chab"]
    r["lMs"] = r["logMs_chab"] + 0.25
    r["yth"] = yth_z(r["zL"])
    r["rcut"] = 2 * L_z(r["zL"])
    r["zl"] = r["zL"]
    for foot in FOOTS:
        a0 = A0[foot]
        ac = C.solve_alpha(DV, r["Re"], 10 ** r["lMc"], r["RE"], r["ME"], a0, "P2", r["yth"], 0.0, r["rcut"])
        S4RES[foot].append(dict(name=r["name"], la_salp=math.log10(ac) - 0.25 if np.isfinite(ac) else float("nan"),
                                sig=r["sigma_SDSS"], Re=r["Re"], RE=r["RE"]))
for foot in FOOTS:
    P(f"  S4TM {foot:9s}: median log alpha_Salp {med([x['la_salp'] for x in S4RES[foot]]):+.3f} (N = {len(S4RES[foot])}; median "
      f"sigma {med([x['sig'] for x in S4RES[foot]]):.0f} km/s, R_E/R_e {med([x['RE'] / x['Re'] for x in S4RES[foot]]):.2f})")

# BELLS: stellar masses from F814W calibrated on SLACS's own SPS masses: log M*_Chab = -0.4 (I - DM) + c(z)
cal = np.array([(a["zl"], a["Imag"], a["lMc"]) for a in AUG.values() if np.isfinite(a["Imag"]) and np.isfinite(a["lMc"])])
ycal = cal[:, 2] + 0.4 * (cal[:, 1] - np.array([COSMO.distmod(z) for z in cal[:, 0]]))
p1 = np.polyfit(cal[:, 0], ycal, 1)
p2 = np.polyfit(cal[:, 0], ycal, 2)
rms1 = float(np.std(ycal - np.polyval(p1, cal[:, 0])))
P(f"  BELLS calibration on {len(cal)} SLACS lenses (z {cal[:, 0].min():.2f}-{cal[:, 0].max():.2f}): log M*_Chab + 0.4 (I - DM) = "
  f"{p1[1]:.4f} {p1[0]:+.4f} z (rms {rms1:.3f} dex); quadratic bracket {p2[2]:.3f} {p2[1]:+.3f} z {p2[0]:+.3f} z^2")
BERES = {f: [] for f in FOOTS}
for r in BE:
    if not str(r["class"]).startswith("E"):
        continue
    Dl = COSMO.DA(r["zL"])
    r["RE"] = r["thetaE"] * C.ARCSEC * Dl
    r["Scr"] = COSMO.Sigma_cr(r["zL"], r["zS"])
    r["ME"] = math.pi * r["Scr"] * r["RE"] ** 2
    r["Re"] = r["Reff"] * C.ARCSEC * Dl
    Ic = r["I814"] - r["A_I"]
    DM_ = COSMO.distmod(r["zL"])
    r["lMc"] = -0.4 * (Ic - DM_) + float(np.polyval(p1, r["zL"]))
    r["lMc2"] = -0.4 * (Ic - DM_) + float(np.polyval(p2, r["zL"]))
    for foot in FOOTS:
        a0 = A0[foot]
        yt = yth_z(r["zL"]); rc = 2 * L_z(r["zL"])
        ac = C.solve_alpha(DV, r["Re"], 10 ** r["lMc"], r["RE"], r["ME"], a0, "P2", yt, 0.0, rc)
        ac2 = C.solve_alpha(DV, r["Re"], 10 ** r["lMc2"], r["RE"], r["ME"], a0, "P2", yt, 0.0, rc)
        BERES[foot].append(dict(name=r["name"], la_salp=math.log10(ac) - 0.25, la_salp_quad=math.log10(ac2) - 0.25,
                                sig=r["sigma_BOSS"], z=r["zL"], RE_Re=r["RE"] / r["Re"]))
for foot in FOOTS:
    P(f"  BELLS {foot:9s}: median log alpha_Salp {med([x['la_salp'] for x in BERES[foot]]):+.3f} (quadratic calibration "
      f"{med([x['la_salp_quad'] for x in BERES[foot]]):+.3f}); N = {len(BERES[foot])}, median z {med([x['z'] for x in BERES[foot]]):.2f}, "
      f"R_E/R_e {med([x['RE_Re'] for x in BERES[foot]]):.2f}")

# SNELLS: the stellar mass inside R_Ein is alpha Ups_ref L_Ein (their aperture photometry); the profile sets the phantom
SNRES = {f: [] for f in FOOTS}
c6 = []
for r in SN:
    xE = r["rEin_kpc"] / r["reff_kpc"]
    ME = r["MEin_1e10"] * 1e10
    for foot in list(FOOTS) + ["newton"]:
        a0 = 0.0 if foot == "newton" else A0[foot]

        def f_(la, a0=a0):
            Mtot = 10 ** la * r["Upsref"] * r["LEin_1e10"] * 1e10 / float(DV.M2D(xE))
            m = C.LensModel(DV, r["reff_kpc"], Mtot, a0, "P2", yth_z(r["zl"]), 0.0, 2 * L_z(r["zl"]))
            return math.log10(float(m.M2D(r["rEin_kpc"])[0]) / ME)
        la = brentq(f_, -1.0, 1.5, xtol=1e-10)
        if foot == "newton":
            c6.append((10 ** la, r["alpha_noDM"]))
        else:
            Mtot = 10 ** la * r["Upsref"] * r["LEin_1e10"] * 1e10 / float(DV.M2D(xE))
            m = C.LensModel(DV, r["reff_kpc"], Mtot, a0, "P2", yth_z(r["zl"]), 0.0, 2 * L_z(r["zl"]))
            yE = C.G * float(m.Mb(r["rEin_kpc"])) / (r["rEin_kpc"] ** 2 * a0 * C.A_UNIT) if a0 > 0 else float("nan")
            SNRES[foot].append(dict(name=r["name"], alpha_K=10 ** la, la_salp=la - math.log10(1.55), sig=r["sigma"], yE=yE,
                                    share=float(m.M2D_phantom(r["rEin_kpc"])[0]) / ME))
c6ok = all(abs(a / b - 1) < 0.012 for a, b in c6)
check("C6 SNELLS: this lane's Newtonian (a0 -> 0) IMF factor from M_Ein, L_Ein and Upsilon_ref reproduces SNELLS's own 'no dark "
      "matter' alpha (Smith+2015 Table, case c) for all three lenses",
      "; ".join(f"{a:.3f} vs {b:.2f}" for a, b in c6), c6ok, "agreement to their two-decimal rounding of M_Ein, L_Ein")
for foot in FOOTS:
    P(f"  SNELLS {foot:9s}: " + "; ".join(f"{x['name']}: y_N(R_Ein) {x['yE']:.1f}, phantom share {x['share']:.3f}, alpha_Kroupa "
                                          f"{x['alpha_K']:.3f} -> log alpha_Salp {x['la_salp']:+.3f}" for x in SNRES[foot]))
OUT["numbers"]["S"] = dict(S4TM={f: med([x["la_salp"] for x in S4RES[f]]) for f in FOOTS},
                           BELLS={f: dict(linear=med([x["la_salp"] for x in BERES[f]]), quadratic=med([x["la_salp_quad"] for x in BERES[f]])) for f in FOOTS},
                           BELLS_calibration=dict(linear=list(map(float, p1)), quadratic=list(map(float, p2)), rms=rms1, N=len(cal)),
                           SNELLS={f: SNRES[f] for f in FOOTS}, SNELLS_newton_vs_published=c6)

# ============================================================================================ I: the independent IMF evidence
banner("I  THE REQUIRED IMF AGAINST INDEPENDENT IMF EVIDENCE (Salpeter units, Auger+ SPS scale)")
cvd = [r for r in CVD if str(r["name"]).startswith("NGC")]
ls_ = np.log10(np.array([r["sigma"] for r in cvd]) / 200.0)
la_mw = np.log10(np.array([r["ML_K"] / r["ML_K_MW"] for r in cvd]))
bcv, acv = np.polyfit(ls_, la_mw, 1)
scv = float(np.std(la_mw - (acv + bcv * ls_), ddof=2))
SALP_MW = 1.6
amax_salp = float(np.max(10 ** la_mw)) / SALP_MW
P(f"  CvD12b (34 ETGs, spectroscopic): log alpha_MW = {acv:+.3f} {bcv:+.3f} log(sigma_Re/8 / 200) (rms {scv:.3f} dex); Salpeter = "
  f"1.6 in these units; heaviest: {cvd[int(np.argmax(la_mw))]['name']} alpha_MW {10 ** la_mw.max():.2f} -> alpha_Salp {amax_salp:.3f}")
cvd_salp = lambda s8: acv + bcv * np.log10(np.asarray(s8, dtype=float) / 200.0) - math.log10(SALP_MW)
ap_corr = lambda sig, Rap, Rtarget: sig * (Rtarget / Rap) ** (-0.04)            # Jorgensen+1995 aperture power law
atlas = lambda se: -0.12 + 0.35 * np.log10(np.asarray(se) / 130.0)              # Cappellari+2013 (ATLAS3D XX), Salpeter units
posacki = lambda se: -0.06 + 0.38 * np.log10(np.asarray(se) / 200.0)            # Posacki+2015, Salpeter units
IMF = {}
for foot in FOOTS:
    rows = LRES[foot]
    s8 = np.array([ap_corr(r["sig_e2"], 0.5, 0.125) for r in rows])            # sigma(R_e/2) -> sigma(R_e/8)
    se = np.array([ap_corr(r["sig_e2"], 0.5, 1.0) for r in rows])              # -> sigma(R_e)
    la = np.array([r["la_salp"] for r in rows])
    dcv = la - cvd_salp(s8)
    err = np.sqrt(np.array([r["elM"] for r in rows]) ** 2 + scv ** 2)
    IMF[foot] = dict(dCvD_mean=float(np.mean(dcv)), dCvD_median=float(np.median(dcv)), dCvD_err=float(np.std(dcv) / math.sqrt(len(dcv))),
                     chi2_per_N=float(np.mean((dcv / err) ** 2)), dATLAS=float(np.median(la - atlas(se))), dPosacki=float(np.median(la - posacki(se))))
    sub = [r for r in rows if r["sig"] >= 280]
    IMF[foot]["slacs_sig280"] = med([r["la_salp"] for r in sub])
    IMF[foot]["N_sig280"] = len(sub)
    s4 = S4RES[foot]
    s4_8 = np.array([ap_corr(x["sig"], 1.5 * C.ARCSEC * COSMO.DA(r_["zL"]) / x["Re"], 0.125) for x, r_ in zip(s4, S4)])
    d4 = np.array([x["la_salp"] for x in s4]) - cvd_salp(s4_8)
    IMF[foot]["S4TM_dCvD_mean"] = float(np.nanmean(d4))
    be = BERES[foot]
    beR = [r_ for r_ in BE if str(r_["class"]).startswith("E")]
    good = [(x, r_) for x, r_ in zip(be, beR) if np.isfinite(r_["sigma_BOSS"])]
    b8 = np.array([ap_corr(r_["sigma_BOSS"], 1.0 * C.ARCSEC * COSMO.DA(r_["zL"]) / r_["Re"], 0.125) for x, r_ in good])
    dB = np.array([x["la_salp"] for x, r_ in good]) - cvd_salp(b8)
    dBq = np.array([x["la_salp_quad"] for x, r_ in good]) - cvd_salp(b8)
    IMF[foot]["BELLS_dCvD_mean"] = float(np.mean(dB))
    IMF[foot]["BELLS_dCvD_mean_quad"] = float(np.mean(dBq))
    sn = SNRES[foot]
    IMF[foot]["SNELLS_la_salp"] = float(np.mean([x["la_salp"] for x in sn]))
    IMF[foot]["SNELLS_dCvD_mean"] = float(np.mean([x["la_salp"] - cvd_salp(x["sig"]) for x in sn]))
    P(f"  {foot:9s}: SLACS chain - CvD12b: mean {IMF[foot]['dCvD_mean']:+.3f} +- {IMF[foot]['dCvD_err']:.3f} dex (median "
      f"{IMF[foot]['dCvD_median']:+.3f}; chi2/N {IMF[foot]['chi2_per_N']:.2f} with SPS error + relation scatter); chain - "
      f"ATLAS3D XX (dynamics + halo) {IMF[foot]['dATLAS']:+.3f}; chain - Posacki+15 (lensing + dynamics + halo) "
      f"{IMF[foot]['dPosacki']:+.3f}")
    P(f"             S4TM chain - CvD12b mean {IMF[foot]['S4TM_dCvD_mean']:+.3f}; BELLS {IMF[foot]['BELLS_dCvD_mean']:+.3f} "
      f"(quadratic calibration {IMF[foot]['BELLS_dCvD_mean_quad']:+.3f}); SNELLS {IMF[foot]['SNELLS_dCvD_mean']:+.3f}; "
      f"SNELLS mean log alpha_Salp {IMF[foot]['SNELLS_la_salp']:+.3f} vs SLACS (sigma_SDSS >= 280, N = {IMF[foot]['N_sig280']}) "
      f"{IMF[foot]['slacs_sig280']:+.3f}")
# the LCDM-with-NFW IMF of the same lenses (Treu+2010, per lens) and the two SLACS lenses with SSP slopes (Barnabe+2013)
tr = [(r0["la_salp"], TREU[r0["name"]]["log_alpha"]) for r0 in LRES["canonical"] if r0["name"] in TREU]
if tr:
    tr = np.array(tr)
    P(f"  Treu+2010 (SLACS, stars + NFW, lensing + dynamics) on the {len(tr)} lenses in common: median log alpha_Salp "
      f"{np.median(tr[:, 1]):+.3f}; the chain's (canonical) {np.median(tr[:, 0]):+.3f}; median difference chain - LCDM "
      f"{np.median(tr[:, 0] - tr[:, 1]):+.3f} dex")
    IMF["treu_common"] = dict(N=len(tr), lcdm=float(np.median(tr[:, 1])), chain=float(np.median(tr[:, 0])), diff=float(np.median(tr[:, 0] - tr[:, 1])))
for nm, xs in (("J0936+0913", "x = 2.10 +- 0.15 (slightly sub-Salpeter)"), ("J0912+0029", "x = 2.60 +- 0.30 (super-Salpeter)")):
    rr_ = [r0 for r0 in LRES["canonical"] if r0["name"] == nm]
    if rr_:
        P(f"  Barnabe+2013 SSP slope for {nm}: {xs}; the chain requires log alpha_Salp {rr_[0]['la_salp']:+.3f} (canonical)")
# the same two tests applied to LCDM's own IMF (Treu+2010 per lens; SNELLS's default EAGLE dark matter): is the pincer shared?
lc = []
for r0 in LRES["canonical"]:
    if r0["name"] in TREU:
        lc.append((TREU[r0["name"]]["log_alpha"], ap_corr(r0["sig_e2"], 0.5, 0.125), r0["sig"]))
lc = np.array(lc)
lc_dcvd = float(np.mean(lc[:, 0] - cvd_salp(lc[:, 1])))
lc_280 = float(np.median(lc[lc[:, 2] >= 280, 0]))
sn_lcdm = float(np.mean([math.log10(r["alpha_default"] / 1.55) for r in SN]))
P(f"  LCDM's own IMF on the same tests: Treu+2010 - CvD12b mean {lc_dcvd:+.3f} dex; SNELLS (EAGLE dark matter) mean log alpha_Salp "
  f"{sn_lcdm:+.3f} vs Treu+2010 at sigma_SDSS >= 280 ({int(np.sum(lc[:, 2] >= 280))} lenses) {lc_280:+.3f} (diff {sn_lcdm - lc_280:+.3f})")
IMF["lcdm_same_tests"] = dict(treu_minus_cvd=lc_dcvd, snells_default=sn_lcdm, treu_sig280=lc_280, diff=sn_lcdm - lc_280)
OUT["numbers"]["I"] = dict(CvD12b_fit=dict(a=float(acv), b=float(bcv), rms=scv, alpha_salp_max=amax_salp), **{f: IMF[f] for f in FOOTS},
                           treu=IMF.get("treu_common"), lcdm_same_tests=IMF.get("lcdm_same_tests"))

# ============================================================================================ H: the pre-declared hypotheses
banner("H  THE PRE-DECLARED HYPOTHESES")
Lf = OUT["numbers"]["L"]
H = {}
H["H1"] = check("H1 the chain reproduces the SLACS Einstein masses with a STANDARD IMF (median kappa_bar in [0.9, 1.1] for Chabrier "
                "or for Salpeter, both footings)",
                "; ".join(f"{f}: Chab {Lf[f]['kappa_chab']:.3f}, Salp {Lf[f]['kappa_salp']:.3f}" for f in FOOTS),
                all(any(0.9 <= Lf[f][k] <= 1.1 for k in ("kappa_chab", "kappa_salp")) for f in FOOTS), load_bearing=False)
H["H2"] = check("H2 THE REQUIRED IMF IS PHYSICALLY ATTAINABLE: SLACS median alpha_Salp <= 1.275 (the heaviest spectroscopic IMF "
                "of CvD12b's 34 ETGs), both footings",
                "; ".join(f"{f}: alpha_Salp {10 ** Lf[f]['log_alpha_salp'][0]:.3f}" for f in FOOTS) + f"; ceiling {amax_salp:.3f}",
                all(10 ** Lf[f]["log_alpha_salp"][0] <= 1.275 for f in FOOTS),
                "load-bearing MUTATE target: an a0-free law needs alpha_Salp ~ 1/f*_Salp")
H["H3"] = check("H3 the chain's IMF agrees with spectroscopy at matched sigma: SLACS mean offset from the CvD12b relation within "
                "+-0.10 dex, both footings",
                "; ".join(f"{f}: {IMF[f]['dCvD_mean']:+.3f} +- {IMF[f]['dCvD_err']:.3f}" for f in FOOTS),
                all(abs(IMF[f]["dCvD_mean"]) <= 0.10 for f in FOOTS), load_bearing=False)
H["H4"] = check("H4 one IMF(sigma) serves both radii: the chain's SNELLS mean log alpha_Salp is not below its SLACS (sigma >= 280) "
                "median by more than 0.10 dex, both footings",
                "; ".join(f"{f}: SNELLS {IMF[f]['SNELLS_la_salp']:+.3f} vs SLACS {IMF[f]['slacs_sig280']:+.3f} "
                          f"(diff {IMF[f]['SNELLS_la_salp'] - IMF[f]['slacs_sig280']:+.3f})" for f in FOOTS),
                all(IMF[f]["SNELLS_la_salp"] - IMF[f]["slacs_sig280"] >= -0.10 for f in FOOTS), load_bearing=False)
H["H5"] = check("H5 lower-mass lenses: the chain's S4TM mean offset from the CvD12b relation is within +-0.10 dex, both footings",
                "; ".join(f"{f}: {IMF[f]['S4TM_dCvD_mean']:+.3f}" for f in FOOTS),
                all(abs(IMF[f]["S4TM_dCvD_mean"]) <= 0.10 for f in FOOTS), load_bearing=False)
H["H6"] = check("H6 (reported; calibration-limited) BELLS mean offset from the CvD12b relation within +-0.15 dex, both footings "
                "(linear SLACS calibration; the quadratic bracket shown)",
                "; ".join(f"{f}: {IMF[f]['BELLS_dCvD_mean']:+.3f} (quad {IMF[f]['BELLS_dCvD_mean_quad']:+.3f})" for f in FOOTS),
                all(abs(IMF[f]["BELLS_dCvD_mean"]) <= 0.15 for f in FOOTS), load_bearing=False)
OUT["hypotheses"] = {k: bool(v) for k, v in H.items()}

# ============================================================================================ verdict
n_lb = sum(1 for _, ok, lb in CH if lb and not ok)
n_ok = sum(1 for _, ok, _ in CH if ok)
banner("VERDICT")
P(f"  {n_ok}/{len(CH)} checks pass; load-bearing failures: {n_lb}")
P("  pre-declared hypotheses: " + ", ".join(f"{k} {'HELD' if v else 'FELL'}" for k, v in H.items()))
OUT["summary"] = dict(n_checks=len(CH), n_pass=n_ok, load_bearing_failures=n_lb, runtime_s=round(time.time() - T0, 1))
json.dump(OUT, open(os.path.join(OUTDIR, f"{SLUG}_results{SUFFIX}.json"), "w"), indent=1, default=str)
P(f"  ({time.time() - T0:.0f} s)")
sys.stdout.flush()
sys.exit(1 if n_lb else 0)
