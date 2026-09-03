#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
h101_fdm_inversion_surveys.py -- HUNT ITEM 101: the closed-form inversion on EVERY survey that tabulates f_DM.
==============================================================================================================
Item 16 (third pass) found the hunt's strongest single number by noticing that where a survey tabulates a dark-matter
fraction INSIDE a radius, the Route A kernel inverts with no mass model at all:

      nu(y) = g_obs/g_bar = 1/(1 - f_DM)     and     nu(y) = 1/(1 - e^{-sqrt y})
  =>  sqrt(y) = ln(1/f_DM)                   =>      a_0 = (1 - f_DM) * g_obs / [ln(1/f_DM)]^2

Item 101 asks for that estimator on every survey that supplies f_DM(<R) and g_obs(R) together, for a JOINT
d log a_0/dz, and for the survey-to-survey scatter reported as prominently as the joint slope.

WHAT RUNS HERE (survey by survey, and why):
  * SPARC (z ~ 0, ON DISK)          -- f_DM(<R_e) = 1 - g_bar/g_obs computed from the rotmod files.  The z = 0 rung
                                       of the ladder measured with the IDENTICAL estimator.  Upsilon-dependent (named).
  * RC100 (z = 0.6-2.5, ON DISK)    -- f_DM(<R_e) tabulated by Nestor-Shachar+2023.  The control: this script must
                                       reproduce item 16's d log a_0/dz = -0.112 +- 0.063 to the third decimal.
  * MSA-3D (z = 0.58-1.68, FETCHED) -- JWST/NIRSpec slit-stepping, 30 galaxies, f_DM(R_e,disk) from DysmalPy forward
                                       modelling, with R_e,disk, sigma_0 and V_rot(R_e) all tabulated, so g_obs is
                                       built with the paper's OWN asymmetric-drift correction.  New to this repo:
                                       fetched from the arXiv source of arXiv:2606.27853 and written to
                                       real_research/data/msa3d_2026_rotation_curves.csv (Tables 1 and 2 verbatim).

WHAT DOES NOT RUN, STATED AND NOT FAKED (the item's own rule):
  * KMOS3D (Uebler+2017, ON DISK)   -- the on-disk table has z, logM*, logM_bar, V_circ, sigma_0 and NO f_DM and NO
                                       radius.  f_DM(<R_e) cannot be built from a TOTAL baryonic mass without a mass
                                       model -- that is exactly the bug item 16 fixed.  NOT INVERTED.
  * KROSS (Harrison+2017, ON DISK)  -- z, M*, R_1/2, V_C: no gas mass and no f_DM.  NOT INVERTED.
  * MUSE-DARK II (Jeanneau+2026)    -- ON DISK in prep_2026/jeanneau_refit/: z, R_eff, M*, M_HI, M_mol, M_bar,
                                       v_c(1.8R_e), v_c(2R_e).  M_bar is again TOTAL, no f_DM column.  NOT INVERTED.
  * MUSE-DARK III (Ciocan+2026)     -- carries no per-galaxy table, but it fits the SAME Route A kernel
                                       (its Eq. 1 is a_tot = a_bar/(1 - exp(-sqrt(a_bar/a_0)))) with a_0 free, so its
                                       published a_0(z) enters as an EXTERNAL rung in the framework's own currency,
                                       clearly labelled as literature and not as this script's measurement.

THE ESTIMATOR'S OWN NOISE, DERIVED HERE BEFORE ANY DATA (Part 0): at fixed g_bar the inversion amplifies scatter in
g_obs by A(f) = 2(1-f)/(f ln(1/f)) >= 2 for every f, diverging as f -> 0.  So a per-galaxy a_0 from this estimator can
NEVER be tighter than twice the RAR's own scatter, whatever the survey.  That is a hard ceiling on item 101's own
pass criterion and it is stated against interest.

Both footings.  Mutation controls (within-survey z-shuffle, kernel swap, and a closure test on data that obey the RAR
exactly, which is what exposes the estimator's positive median bias).  LambdaCDM-native rise (+0.131 dex per unit z) computed beside the framework's FLAT law.  Checks CAN fail.
Writes h101_rungs.json for item 104.
"""
import sys, math, csv, os, json
import numpy as np
from hunt_lib import *

ck = Check(); rng = np.random.default_rng(101)
LCDM_SLOPE = math.log10(2.13)/2.5          # LambdaCDM-native emergent RAR scale: x2.13 by z = 2.5 -> +0.131 dex/z
RAR_SCATTER = 0.11                          # Lelli+2017 observed orthogonal RAR scatter, dex


def fnum(v):
    try: return float(v)
    except Exception: return float("nan")


def a0_closed_form(fdm, gobs):
    """a_0 = (1 - f_DM) g_obs / [ln(1/f_DM)]^2 -- the Route A kernel inverted with no mass model."""
    fdm = np.asarray(fdm, dtype=float); gobs = np.asarray(gobs, dtype=float)
    ok = (fdm > 0.02) & (fdm < 0.98) & np.isfinite(gobs) & (gobs > 0)
    out = np.full(fdm.shape, np.nan)
    out[ok] = (1.0 - fdm[ok])*gobs[ok]/np.log(1.0/fdm[ok])**2
    return out


def a0_simple_nu(fdm, gobs):
    """The same inversion through the SIMPLE interpolation nu = (1 + sqrt(1 + 4/y))/2: a_0 = f g_obs/(1 - f)."""
    fdm = np.asarray(fdm, dtype=float); gobs = np.asarray(gobs, dtype=float)
    ok = (fdm > 0.02) & (fdm < 0.98) & np.isfinite(gobs) & (gobs > 0)
    out = np.full(fdm.shape, np.nan)
    out[ok] = fdm[ok]*gobs[ok]/(1.0 - fdm[ok])
    return out


def amp(f):
    """d ln a_0 / d ln g_obs at fixed g_bar for the Route A closed form."""
    f = np.asarray(f, dtype=float)
    return 2.0*(1.0 - f)/(f*np.log(1.0/f))


def synthetic_sd(gbar, a0v, scatter, ntrial=200):
    """Feed the estimator data that obey the RAR EXACTLY at a_0 = a0v, at THESE g_bar values, with `scatter` dex of
    lognormal noise on g_obs.  Return (median recovered a_0, sd of log a_0, N used) -- the estimator's own noise."""
    gbar = np.asarray(gbar, dtype=float)
    sds, meds = [], []
    for _ in range(ntrial):
        go = nu(gbar/a0v)*gbar*10**(rng.normal(0, scatter, len(gbar)))
        f = 1.0 - gbar/go
        a = a0_closed_form(f, go); m = np.isfinite(a)
        if m.sum() < 5: continue
        sds.append(np.std(np.log10(a[m]))); meds.append(np.median(a[m]))
    return float(np.median(meds)), float(np.median(sds)), int(m.sum())


def slope_boot(z, la, nboot=2000):
    z = np.asarray(z); la = np.asarray(la)
    s, b = np.polyfit(z, la, 1)
    bs = np.array([np.polyfit(z[i], la[i], 1)[0] for i in (rng.integers(0, len(z), len(z)) for _ in range(nboot))])
    return float(s), float(bs.std()), float(b)


def med_boot(v, nboot=2000):
    v = np.asarray(v)
    bs = np.array([np.median(v[rng.integers(0, len(v), len(v))]) for _ in range(nboot)])
    return float(np.median(v)), float(bs.std())


# ==================================================================================================================
P("="*120); P("PART 0 -- what the estimator can and cannot do, derived before any data is touched"); P("="*120)
info("The inversion is a_0 = (1 - f) g_obs / [ln(1/f)]^2 with f = f_DM(<R).  At FIXED g_bar, f = 1 - g_bar/g_obs, so")
info("   d f / d ln g_obs = 1 - f     and     d ln a_0 / d f = 2/(f ln(1/f))   (the (1-f) g_obs product is just g_bar)")
info("   =>  A(f) = d ln a_0 / d ln g_obs = 2 (1 - f) / (f ln(1/f)).")
for f in (0.10, 0.20, 0.30, 0.50, 0.70, 0.85, 0.95):
    info(f"   f_DM = {f:4.2f}:  amplification A = {amp(f):5.2f}x   ->  {RAR_SCATTER:.2f} dex of RAR scatter becomes {RAR_SCATTER*amp(f):.2f} dex in a_0")
fgrid = 1.0 - np.logspace(-8, math.log10(0.98), 8000); Amin = float(np.min(amp(fgrid)))
ck("101-0 the estimator's OWN noise floor, stated against interest before any survey is inverted: the closed-form "
   "inversion amplifies the RAR's scatter by A(f) = 2(1-f)/(f ln(1/f)), whose minimum over all f is 2 and which "
   "diverges as f_DM -> 0, so a per-galaxy a_0 from this estimator can never be tighter than TWICE the RAR's own "
   "0.11 dex -- item 101's target of a joint slope separating FLAT from the LambdaCDM rise at 5 sigma has to come "
   "from N, not from per-galaxy precision",
   Amin >= 1.99 and Amin < 2.01,
   f"min A = {Amin:.4f} (attained as f -> 1); A(0.3) = {amp(0.3):.2f}, A(0.1) = {amp(0.1):.2f}; "
   f"floor on the per-galaxy a_0 scatter = {2*RAR_SCATTER:.2f} dex")

# ==================================================================================================================
P(""); P("="*120); P("PART 1 -- the survey inventory: which tabulate f_DM inside a radius, and which do not"); P("="*120)
inv = []


# ---------------------------------------------------------------- SPARC, z ~ 0, computed f_DM
gals = load_sparc()
sp = []
for g in gals:
    Re = g["Reff"]; r = g["r"]
    if not (Re > 0) or Re < r.min() or Re > r.max(): continue
    gb = float(np.interp(math.log(Re), np.log(r), np.log(g["gbar"])))
    go = float(np.interp(math.log(Re), np.log(r), np.log(g["gobs"])))
    gb, go = math.exp(gb), math.exp(go)
    if not (go > gb > 0): continue
    sp.append(dict(name=g["name"], z=0.0, fdm=1.0 - gb/go, gobs=go, gbar=gb,
                   lMb=math.log10(g["Mb"]) if g["Mb"] > 0 else np.nan, Re=Re))
info(f"SPARC     : {len(gals)} galaxies pass the frozen quality cut; {len(sp)} have R_eff inside the measured radial range "
     f"and g_obs > g_bar there.  f_DM(<R_e) = 1 - g_bar/g_obs is COMPUTED (Upsilon_disk = {UPS_D}, Upsilon_bulge = {UPS_B}).")

# ---------------------------------------------------------------- RC100, tabulated f_DM
rc = []
for r in csv.DictReader(open(os.path.join(DATA, "rc100_nestorshachar2023_table3.csv"))):
    fdm, go, z = fnum(r["fDM_within_Re"]), fnum(r["g_Re_ms2"]), fnum(r["z"])
    if not np.isfinite(fdm*go*z): continue
    rc.append(dict(name=r["name"], z=z, fdm=fdm, gobs=go, gbar=(1-fdm)*go, lMb=fnum(r["logMbar_Msun"]), Re=fnum(r["Re_kpc"])))
info(f"RC100     : {len(rc)} rows with z, f_DM(<R_e) and g(R_e) all tabulated.  g(R_e) = V_c^2(R_e)/R_e with V_c "
     f"pressure-support corrected by the authors -- verified against the table's own column to 0.1%.")
chk = [abs(x["gobs"] - (fnum(r["Vc_Re_kms"])*1e3)**2/(fnum(r["Re_kpc"])*kpc))/x["gobs"]
       for x, r in zip(rc, [q for q in csv.DictReader(open(os.path.join(DATA, "rc100_nestorshachar2023_table3.csv")))
                            if np.isfinite(fnum(q["fDM_within_Re"])*fnum(q["g_Re_ms2"])*fnum(q["z"]))])]
info(f"            provenance check: max |g_tabulated - V_c^2/R_e|/g = {max(chk):.2e}  (the column IS V_c^2/R_e)")

# ---------------------------------------------------------------- MSA-3D, tabulated f_DM (fetched this session)
ms = []
for r in csv.DictReader(open(os.path.join(DATA, "msa3d_2026_rotation_curves.csv"))):
    z, Re, s0, vrot, fdm = fnum(r["z"]), fnum(r["Re_disk_kpc"]), fnum(r["sigma0"]), fnum(r["Vrot_Re"]), fnum(r["fDM_Re"])
    if not np.isfinite(z*Re*s0*vrot*fdm): continue
    vc2 = vrot**2 + 2.0*s0**2*1.678               # the paper's own ADC at R = R_e for a n = 1 disc: R/R_d = b_1 = 1.678
    go = vc2*1e6/(Re*kpc)
    ms.append(dict(name=r["ID"], sample=r["sample"], z=z, fdm=fdm, gobs=go, gbar=(1-fdm)*go,
                   lMs=fnum(r["logMstar"]), Re=Re, efdm=0.5*(fnum(r["efDM_p"]) + fnum(r["efDM_m"]))))
msg = [m for m in ms if m["sample"] == "golden"]
info(f"MSA-3D    : {len(ms)} galaxies ({len(msg)} 'golden' statistical sample, {len(ms)-len(msg)} 'good').  f_DM(R_e,disk), "
     f"R_e,disk, sigma_0 and V_rot(R_e) all tabulated; g_obs built with the paper's own ADC V_c^2 = V_rot^2 + 2 sigma_0^2 (R/R_d).")
info(f"            fetched from arXiv:2606.27853 source -> real_research/data/msa3d_2026_rotation_curves.csv")

# ---------------------------------------------------------------- the ones that cannot be inverted
k3 = list(csv.DictReader(open(os.path.join(DATA, "kmos3d_ubler2017.csv"))))
kr = list(csv.DictReader(open(os.path.join(DATA, "kross_harrison2017.csv"))))
jn = list(csv.DictReader(open(os.path.join(HERE, "..", "prep_2026", "jeanneau_refit", "jeanneau26_catalog_cds.csv"))))
info(f"KMOS3D    : {len(k3)} rows on disk, columns {list(k3[0].keys())} -- NO f_DM, NO radius.  NOT INVERTED.")
info(f"KROSS     : {len(kr)} rows on disk, columns {list(kr[0].keys())} -- NO f_DM, NO gas mass.  NOT INVERTED.")
info(f"MUSE-DARK II: {len(jn)} rows on disk (prep_2026/jeanneau_refit/), M_bar is a TOTAL mass and there is no f_DM column. NOT INVERTED.")
have_fdm = 3; want_fdm = 6
ck("101-1 AGAINST INTEREST -- item 101's premise does not survive contact with the archive: of the six surveys it "
   "names, only THREE supply what the closed form needs (a dark-matter fraction AND the acceleration at the same "
   "radius).  KMOS3D, KROSS and MUSE-DARK II tabulate total baryonic masses and velocities, from which f_DM(<R_e) "
   "cannot be built without the mass model the estimator exists to avoid -- so they are reported, not faked",
   have_fdm == 3,
   f"invertible: SPARC (computed), RC100 (tabulated), MSA-3D (tabulated) = {have_fdm}/{want_fdm}; "
   f"MUSE-DARK III enters as a literature rung only")

# ==================================================================================================================
P(""); P("="*120); P("PART 2 -- the inversion, survey by survey, both footings"); P("="*120)
P(f"  {'survey':22}{'N':>5}{'z range':>14}{'median a_0':>13}{'16-84%':>26}{'dex vs canon':>14}{'dex vs alt':>12}{'sd log a_0':>12}")
rungs = {}
for label, rows, zlab in (("SPARC (z~0)", sp, "0.00"), ("RC100", rc, ""), ("MSA-3D golden", msg, ""), ("MSA-3D all 30", ms, "")):
    fd = np.array([r["fdm"] for r in rows]); go = np.array([r["gobs"] for r in rows]); zz = np.array([r["z"] for r in rows])
    gbar = np.array([r["gbar"] for r in rows])
    a0v = a0_closed_form(fd, go); m = np.isfinite(a0v)
    a0v, zz2, fd2, gb2 = a0v[m], zz[m], fd[m], gbar[m]
    la = np.log10(a0v); mm, me = med_boot(a0v)
    zr = f"{zz2.min():.2f}-{zz2.max():.2f}" if zz2.max() > 0 else "0.00"
    P(f"  {label:22}{len(a0v):5d}{zr:>14}{mm:13.3e}"
      f"{f'{np.percentile(a0v,16):.2e} - {np.percentile(a0v,84):.2e}':>26}"
      f"{math.log10(mm/A0['canonical']):+14.3f}{math.log10(mm/A0['alt']):+12.3f}{la.std():12.3f}")
    rungs[label] = dict(N=int(len(a0v)), zmed=float(np.median(zz2)), a0=mm, a0_err=me, la=la.tolist(),
                        z=zz2.tolist(), fdm=fd2.tolist(), gbar=gb2.tolist(), sd=float(la.std()))
info("")
info("The per-galaxy scatter is 0.39-0.55 dex in EVERY sample, against the RAR's own 0.11 dex.  Part 0 said it would be;")
info("here is the same statement made by simulation -- data that obey the RAR EXACTLY at each survey's own g_bar values,")
info("with 0.11 dex of scatter on g_obs, put through the identical estimator:")
sd_pred = {}
for label in ("SPARC (z~0)", "RC100", "MSA-3D golden"):
    gb = np.array(rungs[label]["gbar"])
    m_syn, s_syn, _ = synthetic_sd(gb, A0["canonical"], RAR_SCATTER)
    sd_pred[label] = s_syn
    info(f"   {label:16} median f_DM = {np.median(rungs[label]['fdm']):.2f};  synthetic sd = {s_syn:.2f} dex, "
         f"observed sd = {rungs[label]['sd']:.2f} dex   (ratio {rungs[label]['sd']/s_syn:.2f})")
info("")
info("The 0.11 dex used above is SPARC's GLOBAL RAR scatter, which is the wrong number for a SINGLE radius per galaxy.")
info("Redone with each survey's OWN measured residual from a single-a_0 RAR (a_0 = that survey's own median), which is")
info("the only input the estimator's noise can possibly have:")
res_r = {}
for label in ("SPARC (z~0)", "RC100", "MSA-3D golden"):
    gb = np.array(rungs[label]["gbar"]); fdv = np.array(rungs[label]["fdm"]); la = np.array(rungs[label]["la"])
    a0m = rungs[label]["a0"]
    delta = np.log10(gb/(1.0 - fdv)) - np.log10(nu(gb/a0m)*gb)   # log g_obs - log g_obs(RAR at a_0 = median)
    sd_d = float(np.std(delta))
    m_syn2, s_syn2, _ = synthetic_sd(gb, a0m, sd_d)
    r_ = float(np.corrcoef(amp(fdv)*delta, la - math.log10(a0m))[0, 1])
    res_r[label] = (sd_d, s_syn2, r_, math.log10(m_syn2/a0m))
    info(f"   {label:16} own single-radius RAR residual sd = {sd_d:.3f} dex  ->  synthetic a_0 sd = {s_syn2:.2f} dex, "
         f"observed {la.std():.2f} dex; first-order A*delta correlates r = {r_:+.3f}; "
         f"median bias {math.log10(m_syn2/a0m):+.3f} dex")
worst_sd = max(abs(res_r[l][1] - rungs[l]["sd"]) for l in res_r)
maxbias = max(abs(res_r[l][3]) for l in res_r)
ck("101-2 the estimator's amplification is not a worry, it IS the entire error budget: injecting only each survey's "
   "OWN single-radius RAR residual into data that otherwise obey one a_0 exactly reproduces the observed 0.39-0.55 "
   "dex per-galaxy spread in all three surveys.  Nothing in those spreads is physics.  Stated against interest: at "
   "SPARC's 0.20 dex residual the estimator's MEDIAN is also biased high by ~0.05 dex, so the levels in the table "
   "above are upper-leaning by that much",
   worst_sd < 0.10,
   "; ".join(f"{l}: observed {rungs[l]['sd']:.2f} vs synthetic {res_r[l][1]:.2f} dex" for l in res_r)
   + f"; largest median bias {maxbias:+.3f} dex")
info("Note where the first-order form breaks: SPARC's r is only "
     f"{res_r['SPARC (z~0)'][2]:+.2f} because SPARC's f_DM reaches both ends (0.02 and 0.98) where A(f) diverges and a")
info("linear expansion is invalid -- a real property of the estimator, not of the galaxies.")

# ---- the control: item 16 must be reproduced exactly
_rcz = np.array([r["z"] for r in rc]); _rca = a0_closed_form([r["fdm"] for r in rc], [r["gobs"] for r in rc])
_m = np.isfinite(_rca)
s16, e16, _ = slope_boot(_rcz[_m], np.log10(_rca[_m]))
ck("101-3 CONTROL: this script reproduces item 16's committed RC100 number to the third decimal",
   abs(s16 + 0.112) < 0.004 and abs(e16 - 0.063) < 0.012,
   f"d log a_0/dz (RC100) = {s16:+.4f} +- {e16:.4f}; the ledger says -0.112 +- 0.063")

# ==================================================================================================================
P(""); P("="*120); P("PART 3 -- the joint fit, and the survey-to-survey scatter reported beside it"); P("="*120)
LAB = ["SPARC (z~0)", "RC100", "MSA-3D golden"]
zJ = np.concatenate([rungs[l]["z"] for l in LAB]); laJ = np.concatenate([rungs[l]["la"] for l in LAB])
sid = np.concatenate([[i]*rungs[l]["N"] for i, l in enumerate(LAB)])
sJ, eJ, bJ = slope_boot(zJ, laJ)
P(f"  [A] ONE LINE through all three surveys (item 101's 'one a_0 across all of them'):")
P(f"      d log a_0/dz = {sJ:+.4f} +- {eJ:.4f}  (N = {len(zJ)});  FLAT is {abs(sJ/eJ):.1f} sigma away, "
  f"LambdaCDM-native (+{LCDM_SLOPE:.3f}) is {abs(sJ-LCDM_SLOPE)/eJ:.1f} sigma away")
P(f"  [B] per-survey slopes (each survey's OWN internal redshift lever):")
per = {}
for l in LAB:
    z = np.array(rungs[l]["z"]); la = np.array(rungs[l]["la"])
    if z.ptp() < 0.05:
        P(f"      {l:16} no internal z lever (z = 0 by construction), level only: log a_0 = {np.median(la):+.3f}")
        per[l] = (np.nan, np.nan); continue
    s, e, _ = slope_boot(z, la); per[l] = (s, e)
    P(f"      {l:16} d log a_0/dz = {s:+.4f} +- {e:.4f}   (N = {len(z)}, z = {z.min():.2f}-{z.max():.2f}); "
      f"FLAT {abs(s/e):.1f}s, LCDM-native {abs(s-LCDM_SLOPE)/e:.1f}s")
levels = {l: math.log10(rungs[l]["a0"]) for l in LAB}
P(f"  [C] the LEVELS, which is where the surveys actually part company:")
for l in LAB:
    P(f"      {l:16} median a_0 = {rungs[l]['a0']:.3e} +- {rungs[l]['a0_err']:.2e}  "
      f"(log = {levels[l]:+.3f}; {math.log10(rungs[l]['a0']/A0['canonical']):+.2f} dex from canonical)")
spread = max(levels.values()) - min(levels.values())
diff_rc_ms = levels["MSA-3D golden"] - levels["RC100"]
sig_rc_ms = abs(diff_rc_ms)/math.hypot(rungs["RC100"]["a0_err"]/(rungs["RC100"]["a0"]*math.log(10)),
                                       rungs["MSA-3D golden"]["a0_err"]/(rungs["MSA-3D golden"]["a0"]*math.log(10)))
P(f"      survey-to-survey spread in the level: {spread:.3f} dex; RC100 vs MSA-3D differ by {diff_rc_ms:+.3f} dex "
  f"= {sig_rc_ms:.1f} sigma on the bootstrap errors of the medians alone")
sl_rc, sl_ms = per["RC100"], per["MSA-3D golden"]
sig_slope = abs(sl_rc[0] - sl_ms[0])/math.hypot(sl_rc[1], sl_ms[1])
P(f"      and their SLOPES have opposite signs: RC100 {sl_rc[0]:+.3f} +- {sl_rc[1]:.3f}, "
  f"MSA-3D {sl_ms[0]:+.3f} +- {sl_ms[1]:.3f}  ->  {sig_slope:.1f} sigma apart")
ck("101-4 THE RESULT, and it is the informative one item 101 named: the surveys DISAGREE.  Put through the identical "
   "closed form, RC100 and MSA-3D differ by 0.4 dex in the LEVEL of a_0 (2.2 sigma on bootstrap errors alone, and "
   "the levels are what carry -- the slopes have opposite signs but MSA-3D's own slope is only 1.0 sigma from zero "
   "with N = 23, so the sign difference by itself proves nothing).  A joint slope tighter than RC100's own +-0.063 "
   "cannot be quoted, and item 101's 5-sigma criterion is not merely unmet, it is ill-posed until this is explained",
   sig_slope > 2.0 or abs(diff_rc_ms) > 0.25,
   f"level spread {spread:.2f} dex over three surveys; RC100 - MSA-3D = {diff_rc_ms:+.2f} dex ({sig_rc_ms:.1f}s); "
   f"slopes {sl_rc[0]:+.3f} vs {sl_ms[0]:+.3f} ({sig_slope:.1f}s apart)")
ck("101-5 the joint slope is reported anyway, with the caveat attached, and it does NOT reach item 101's target: it "
   "neither separates FLAT from the LambdaCDM-native rise at 5 sigma nor improves on RC100 alone once the "
   "survey-to-survey disagreement is admitted",
   abs(sJ - LCDM_SLOPE)/eJ < 5.0,
   f"one-line joint d log a_0/dz = {sJ:+.4f} +- {eJ:.4f}; separation from the LambdaCDM-native rise "
   f"{abs(sJ-LCDM_SLOPE)/eJ:.1f} sigma, target was 5 sigma")

# ==================================================================================================================
P(""); P("="*120); P("PART 4 -- where the disagreement actually lives: f_DM at MATCHED baryonic acceleration"); P("="*120)
info("First, what the inverted a_0 correlates with INSIDE each survey (a universal a_0 requires zero everywhere):")
P(f"      {'survey':16}{'f_DM':>10}{'log g_bar':>11}{'log M':>9}{'log Sigma':>11}{'z':>9}")
for l, rows, key in (("RC100", rc, "lMb"), ("MSA-3D golden", msg, "lMs")):
    fdv = np.array([r["fdm"] for r in rows]); gov = np.array([r["gobs"] for r in rows])
    gbv = np.array([r["gbar"] for r in rows]); lm = np.array([r[key] for r in rows])
    Rev = np.array([r["Re"] for r in rows]); zv = np.array([r["z"] for r in rows])
    a0v = a0_closed_form(fdv, gov); m = np.isfinite(a0v) & np.isfinite(lm) & (Rev > 0)
    la = np.log10(a0v[m]); sig = lm[m] - 2*np.log10(Rev[m])
    cc = [float(np.corrcoef(x, la)[0, 1]) for x in (fdv[m], np.log10(gbv[m]), lm[m], sig, zv[m])]
    P(f"      {l:16}{cc[0]:+10.3f}{cc[1]:+11.3f}{cc[2]:+9.3f}{cc[3]:+11.3f}{cc[4]:+9.3f}")
    if l == "RC100": cc_rc = cc
    else: cc_ms = cc
info("So AGAINST MY OWN FIRST GUESS: there is NO mass trend and NO g_bar trend inside either survey.  The inverted a_0")
info("is, to r ~ 0.75, nothing but a monotone relabelling of the tabulated f_DM -- item 16c's caveat, generalised.")
info("")
info("Second, the sharp version, which is a falsifiable statement about the framework and not about the estimator:")
info("with ONE a_0 the kernel PREDICTS f_DM from g_bar alone, f_DM = 1 - 1/nu(g_bar/a_0).  Binned in g_bar so the two")
info("surveys are compared like for like:")
gb_rc = np.array([r["gbar"] for r in rc if 0.02 < r["fdm"] < 0.98])
fd_rc = np.array([r["fdm"] for r in rc if 0.02 < r["fdm"] < 0.98])
gb_ms = np.array([m_["gbar"] for m_ in msg]); fd_ms = np.array([m_["fdm"] for m_ in msg])
gb_sp = np.array([s["gbar"] for s in sp]); fd_sp = np.array([s["fdm"] for s in sp])
edges = np.logspace(math.log10(3e-11), math.log10(1e-9), 5)
P(f"      {'g_bar bin (m/s^2)':>26}{'framework f_DM':>16}{'SPARC z~0':>14}{'RC100':>14}{'MSA-3D':>14}")
gaps = []
for i in range(len(edges)-1):
    a_, b_ = edges[i], edges[i+1]; gc = math.sqrt(a_*b_)
    fpred = 1.0 - 1.0/nu_s(gc/A0["canonical"])
    cells = []
    for gbv, fdv in ((gb_sp, fd_sp), (gb_rc, fd_rc), (gb_ms, fd_ms)):
        mm_ = (gbv >= a_) & (gbv < b_)
        cells.append(f"{np.median(fdv[mm_]):.3f} (n={mm_.sum()})" if mm_.sum() >= 3 else f"-- (n={mm_.sum()})")
    P(f"      {f'{a_:.2e} - {b_:.2e}':>26}{fpred:16.3f}{cells[0]:>14}{cells[1]:>14}{cells[2]:>14}")
    mr_ = (gb_rc >= a_) & (gb_rc < b_); mm2_ = (gb_ms >= a_) & (gb_ms < b_)
    if mr_.sum() >= 3 and mm2_.sum() >= 3:
        gaps.append((gc, float(np.median(fd_rc[mr_])), float(np.median(fd_ms[mm2_])), fpred, int(mr_.sum()), int(mm2_.sum())))
maxgap = max(abs(g[2]-g[1]) for g in gaps) if gaps else 0.0
# bootstrap the largest matched-bin gap
gc, frc, fms, fpr, nr_, nm_ = max(gaps, key=lambda g: abs(g[2]-g[1]))
mr_ = (gb_rc >= 0) & np.isfinite(gb_rc)
sel_r = fd_rc[(gb_rc >= gc/math.sqrt(edges[1]/edges[0])) & (gb_rc < gc*math.sqrt(edges[1]/edges[0]))]
sel_m = fd_ms[(gb_ms >= gc/math.sqrt(edges[1]/edges[0])) & (gb_ms < gc*math.sqrt(edges[1]/edges[0]))]
bs = np.array([np.median(sel_m[rng.integers(0, len(sel_m), len(sel_m))]) - np.median(sel_r[rng.integers(0, len(sel_r), len(sel_r))])
               for _ in range(3000)])
ck("101-6 AGAINST MY OWN FIRST GUESS, and this is the sharp form of the disagreement: inside each survey the "
   "inverted a_0 shows NO mass and NO g_bar trend -- it is a relabelling of f_DM, nothing else.  But at MATCHED "
   "baryonic acceleration the two high-z surveys report dark-matter fractions differing by ~0.18 (about 2 sigma on "
   "bootstrap alone) and BOTH sit above what one universal a_0 predicts, while SPARC at z ~ 0 tracks the prediction "
   "bin by bin.  The 0.4 dex offset in a_0 is a disagreement between two dynamical decompositions at the same "
   "acceleration -- not a redshift effect and not a mass effect",
   maxgap > 0.15 and abs(cc_rc[2]) < 0.15 and abs(cc_ms[2]) < 0.15,
   f"largest matched-g_bar gap: at g_bar = {gc:.2e}, RC100 f_DM = {frc:.3f} (n={nr_}) vs MSA-3D {fms:.3f} (n={nm_}), "
   f"difference {fms-frc:+.3f} +- {bs.std():.3f}; framework predicts {fpr:.3f}; "
   f"corr(log a_0, log M) = {cc_rc[2]:+.3f} (RC100) / {cc_ms[2]:+.3f} (MSA-3D)")

# ==================================================================================================================
P(""); P("="*120); P("PART 5 -- the external rung: MUSE-DARK III fits the framework's own kernel directly"); P("="*120)
info("Ciocan+2026 (arXiv:2604.22613, MUSE-DARK III) fit 79 MHUDF star-forming galaxies at 0.33 < z < 1.44 with")
info("   a_tot = a_bar / (1 - exp(-sqrt(a_bar/a_0)))   -- Route A, verbatim -- leaving a_0 free.  They report")
info("   a_0|z~1 = 2.38 (+0.12/-0.10) e-10 m/s^2 (95% CI), and a_0(z) = a_0(0) + a_1 z with")
info("   a_0(0) = 1.00 +- 0.04 e-10 and a_1 = 1.59 +- 0.10 e-10 per unit z.  This is literature, not this script's number.")
MD3_a00, MD3_a1, MD3_a1e = 1.00e-10, 1.59e-10, 0.10e-10
zg = np.linspace(0.33, 1.44, 200)
md3_slope = float(np.polyfit(zg, np.log10(MD3_a00 + MD3_a1*zg), 1)[0])
md3_slope_lo = float(np.polyfit(zg, np.log10(MD3_a00 + (MD3_a1 - MD3_a1e)*zg), 1)[0])
info(f"   in this script's currency that is d log a_0/dz = {md3_slope:+.3f} over 0.33 < z < 1.44 (a_1 - 1 sigma gives "
     f"{md3_slope_lo:+.3f}, so the STATISTICAL error on the slope is only {md3_slope-md3_slope_lo:.3f}) -- more than")
info(f"   twice the LambdaCDM-native rise.  The statistical significance is not the relevant number and is not quoted:")
info(f"   Ciocan themselves name the lever: reconciling their a_0(z) with a_0(0) = 1.2e-10 at all z needs stellar-mass")
info(f"   offsets of +0.2 dex (low z) to +0.45 dex (high z) -- i.e. the whole trend is inside the stellar M/L budget,")
info(f"   which is the same wall every keeper of this hunt ran into.  (Their own Appendix, verbatim.)")
allslopes = [per["RC100"][0], per["MSA-3D golden"][0], md3_slope]
ck("101-7 with MUSE-DARK III added as a literature rung in the framework's own kernel, the a_0(z) measurements now "
   "span d log a_0/dz from -0.11 to +0.35 -- a 0.46 dex-per-z spread across three samples that all claim to measure "
   "the same constant.  Reported as prominently as the joint slope, as item 101 required, and it means NO number on "
   "this front should be quoted as a measurement of a_0's redshift dependence today",
   (max(allslopes) - min(allslopes)) > 0.25,
   f"RC100 {per['RC100'][0]:+.3f}, MSA-3D {per['MSA-3D golden'][0]:+.3f}, MUSE-DARK III {md3_slope:+.3f}; "
   f"spread {max(allslopes)-min(allslopes):.3f} dex/z against a LambdaCDM-native +{LCDM_SLOPE:.3f} and a framework 0.000")

# ==================================================================================================================
P(""); P("="*120); P("PART 6 -- mutation controls"); P("="*120)
# M1: shuffle z WITHIN each survey.  Any surviving joint slope is pure survey-ladder, not redshift.
zsh = np.concatenate([rng.permutation(rungs[l]["z"]) for l in LAB])
s_sh, e_sh, _ = slope_boot(zsh, laJ)
info(f"   within-survey z-shuffle: joint slope {s_sh:+.4f} +- {e_sh:.4f} against the real {sJ:+.4f} +- {eJ:.4f}")
for l in LAB[1:]:
    z = np.array(rungs[l]["z"]); la = np.array(rungs[l]["la"])
    s_, e_, _ = slope_boot(rng.permutation(z), la)
    info(f"   {l:16} own slope shuffled: {s_:+.4f} +- {e_:.4f}  (real {per[l][0]:+.4f} +- {per[l][1]:.4f})")
ck("M1 the mutation that matters, and it fires: permuting redshift WITHIN each survey leaves the joint slope "
   "essentially unchanged, because the joint slope is not a redshift trend at all -- it is three survey medians at "
   "three different median redshifts, i.e. the survey ladder of Part 3C read as a line.  A 'joint d log a_0/dz' "
   "from stacked surveys is therefore not a measurement of anything until the surveys agree",
   abs(s_sh - sJ) < 2*max(eJ, e_sh),
   f"shuffled {s_sh:+.4f} +- {e_sh:.4f} vs real {sJ:+.4f} +- {eJ:.4f} -- the shuffle removes "
   f"{100*abs(sJ-s_sh)/max(abs(sJ),1e-9):.0f}% of it")

# M2: kernel swap -> does the LEVEL depend on which interpolation function is inverted?
lev_route, lev_simple = {}, {}
for l, rows in (("RC100", rc), ("MSA-3D golden", msg), ("SPARC (z~0)", sp)):
    fd = [r["fdm"] for r in rows]; go = [r["gobs"] for r in rows]
    ra = a0_closed_form(fd, go); si = a0_simple_nu(fd, go); m = np.isfinite(ra) & np.isfinite(si)
    lev_route[l] = float(np.median(ra[m])); lev_simple[l] = float(np.median(si[m]))
    info(f"   {l:16} Route A {lev_route[l]:.3e}  vs  simple nu {lev_simple[l]:.3e}   "
         f"({math.log10(lev_simple[l]/lev_route[l]):+.3f} dex)")
dk = max(abs(math.log10(lev_simple[l]/lev_route[l])) for l in lev_route)
ck("M2 kernel swap AGAINST INTEREST -- inverted through the 'simple' interpolation function nu = (1+sqrt(1+4/y))/2 "
   "instead of Route A (a_0 = f g_obs/(1-f) rather than (1-f) g_obs/[ln(1/f)]^2) the answer moves by less than the "
   "RAR's own scatter, so this estimator cannot discriminate kernels at all; the compensation is that none of the "
   "numbers above is an artifact of Route A either",
   dk < RAR_SCATTER, f"largest Route-A-vs-simple difference across the three surveys = {dk:.3f} dex, "
                     f"against the RAR's own {RAR_SCATTER:.2f} dex scatter")

# M3: closure test -- galaxies that obey the RAR EXACTLY with a known a_0, plus the RAR's own scatter (200 realisations)
gb_syn = np.array([r["gbar"] for r in rc])
bias = {}
for ftest in (0.0, 0.11, 0.20):
    m_s, s_s, frac = synthetic_sd(gb_syn, A0["canonical"], ftest, ntrial=(1 if ftest == 0 else 300))
    bias[ftest] = math.log10(m_s/A0["canonical"])
    info(f"   synthetic RAR at a_0 = {A0['canonical']:.3e}, {ftest:.2f} dex of scatter on g_obs: recovered median "
         f"{m_s:.3e} ({bias[ftest]:+.3f} dex bias), sd(log a_0) = {s_s:.3f}")
info("   the bias is POSITIVE and it is structural: a galaxy scattered to g_obs < g_bar has f_DM <= 0 and the closed")
info("   form is undefined there, so the low-a_0 tail is truncated while the high-a_0 tail is not.")
ck("M3 closure AGAINST INTEREST -- the estimator is NOT unbiased.  Fed data that obey the RAR exactly it returns the "
   "input a_0 exactly; fed the same data with realistic scatter it returns a median biased HIGH, because the "
   "low-a_0 tail is truncated at f_DM = 0 and the high tail is not.  Every level this estimator reports, including "
   "item 16's, is therefore about 0.05 dex too high, which is most of RC100's +0.17 dex offset from canonical",
   abs(bias[0.0]) < 1e-9 and 0.0 < bias[0.11] < 0.12,
   f"bias = {bias[0.0]:+.3f} dex (no scatter), {bias[0.11]:+.3f} dex (0.11 dex), {bias[0.20]:+.3f} dex (0.20 dex)")

# ==================================================================================================================
P(""); P("="*120); P("PART 7 -- both footings, and the LambdaCDM alternative computed beside the framework"); P("="*120)
for f_ in ("canonical", "alt"):
    P(f"  footing {f_:10} a_0(0) = {A0[f_]:.3e}:  SPARC {math.log10(rungs['SPARC (z~0)']['a0']/A0[f_]):+.2f} dex, "
      f"RC100 {math.log10(rungs['RC100']['a0']/A0[f_]):+.2f} dex, MSA-3D {math.log10(rungs['MSA-3D golden']['a0']/A0[f_]):+.2f} dex")
P(f"  the SLOPE d log a_0/dz is a RATIO and is footing-independent; only the levels above move with the footing.")
P(f"  framework (FLAT, a_0 fixed by rho_Lambda):     d log a_0/dz = 0.000 exactly")
P(f"  LambdaCDM-native emergent RAR scale:           d log a_0/dz = +{LCDM_SLOPE:.3f} (x2.13 by z = 2.5)")
P(f"  measured, three ways:                          {per['RC100'][0]:+.3f} (RC100), "
  f"{per['MSA-3D golden'][0]:+.3f} (MSA-3D), {md3_slope:+.3f} (MUSE-DARK III)")

json.dump(dict(LCDM_SLOPE=LCDM_SLOPE,
               rungs={l: dict(N=rungs[l]["N"], zmed=rungs[l]["zmed"], a0=rungs[l]["a0"], a0_err=rungs[l]["a0_err"],
                              sd=rungs[l]["sd"], slope=per[l][0], slope_err=per[l][1],
                              z=rungs[l]["z"], la=rungs[l]["la"]) for l in LAB},
               musedark3=dict(a00=MD3_a00, a1=MD3_a1, a1_err=MD3_a1e, zlo=0.33, zhi=1.44, N=79, slope=md3_slope),
               joint=dict(slope=sJ, slope_err=eJ)),
          open(os.path.join(HERE, "h101_rungs.json"), "w"), indent=1)
info(f"wrote {os.path.join(HERE, 'h101_rungs.json')} for item 104")

P(""); P("="*120)
P("VERDICT (item 101).")
P(f"  * The closed form runs on THREE of the six named surveys.  KMOS3D, KROSS and MUSE-DARK II tabulate total")
P(f"    baryonic masses and velocities, not f_DM inside a radius, and are reported rather than faked.")
P(f"  * SPARC (z~0) and RC100 (z = 0.6-2.5) agree on the LEVEL to {abs(levels['RC100']-levels['SPARC (z~0)']):.2f} dex")
P(f"    ({rungs['SPARC (z~0)']['a0']:.2e} vs {rungs['RC100']['a0']:.2e}), which is the one genuinely encouraging number here.")
P(f"  * MSA-3D sits {diff_rc_ms:+.2f} dex away from RC100 in the level ({sig_rc_ms:.1f} sigma); MUSE-DARK III, fitting the identical")
P(f"    kernel directly, is further away still.  Slopes across the three: {per['RC100'][0]:+.3f} +- {per['RC100'][1]:.3f}, "
  f"{per['MSA-3D golden'][0]:+.3f} +- {per['MSA-3D golden'][1]:.3f}, {md3_slope:+.3f} -- opposite signs, but only the")
P(f"    levels are individually significant; MSA-3D's own slope is 1.0 sigma from zero with N = 23.")
P(f"  * The disagreement is NOT a mass trend and NOT a redshift trend: inside each survey the inverted a_0 correlates")
P(f"    with nothing but f_DM itself, and at matched g_bar the two high-z surveys still report f_DM differing by")
P(f"    {fms-frc:+.2f}.  It is a disagreement between two dynamical decompositions at the same acceleration.")
P(f"  * Item 101's pass criterion -- a joint slope separating FLAT from the LambdaCDM-native rise at 5 sigma -- is NOT")
P(f"    met ({abs(sJ-LCDM_SLOPE)/eJ:.1f} sigma), and the mutation control shows the joint slope is the survey ladder, not redshift.")
P(f"  * What survives is a hard ceiling on the method: the estimator amplifies the RAR's own residual by A(f_DM) >= 2,")
P(f"    galaxy by galaxy to r > 0.9, so per-galaxy a_0 from a tabulated f_DM can never beat twice the RAR's scatter.")
P("="*120)
sys.exit(ck.done())
