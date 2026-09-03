#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
h59_h60_cluster_T_Y_slopes.py -- HUNT ITEMS 59 and 60: the two cluster power-law indices the framework fixes with no
free parameter, measured on two independent eROSITA X-ray samples and on Planck's SZ catalogue.
=====================================================================================================================
Item 59  T - M_gas slope = 1/2.
    Framework statement, derived, not asserted.  Hydrostatic equilibrium for an isothermal atmosphere whose outer gas
    density runs as rho_g ~ r^-alpha_g:   (kT/mu m_p) alpha_g / r = g(r).  In the deep-MOND limit of Route A,
    nu(y) -> 1/sqrt(y) as y -> 0, so g -> sqrt(G M_b a_0)/r and the radius CANCELS:

        kT = (mu m_p / alpha_g) sqrt(G M_b a_0)          =>   d log kT / d log M_b = 1/2 EXACTLY.

    The 1/2 is the whole content; the zero point carries one O(1) structure constant alpha_g (the outer gas log-slope),
    so the zero point is NOT a clean test and is reported here as a derived alpha_g, not as a pass/fail.
    The item's own note says self-similar LambdaCDM with f_gas ~ M^{1/3} lands on the same 1/2 -- that coincidence is
    computed here FROM THE SAME DATA rather than quoted.

Item 60  Y_SZ - M_gas slope = 3/2.
    Y_500 = (sigma_T k / m_e c^2 mu_e m_p) M_gas <T>, an IDENTITY, so d log Y/d log M_gas = 1 + d log kT/d log M_gas
    for ANY theory.  Item 60 is therefore item 59 plus a definitional 1 -- stated up front so it is not sold as an
    independent hit.  What IS independent: the SZ measurement uses different photons from a different observatory, so
    its noise does not share the X-ray photons that T and M_gas share.  The test run here is the CLOSURE of the
    triangle (Y, M_gas, T) on the same objects, which can fail and which does fail at the 3-sigma level below.

Data
    eFEDS      Bahar+2022 A&A 661 A7 table2 (VizieR J/A+A/661/A7/table2), 542 clusters/groups, deep 140 deg^2 field.
    eRASS1     Bulbul+2024 A&A 685 A106 primary catalogue (on disk), 12,247 systems, shallow all-sky.
    PSZ2       Planck 2016 A&A 594 A27 union catalogue (VizieR J/A+A/594/A27/psz2), 1,653 SZ detections, Y5R500.
    Both a_0 footings.  Checks that can fail.  Four mutation controls.  LambdaCDM computed beside the framework.
"""
import os, sys, math
import numpy as np
from scipy.optimize import minimize
from scipy.integrate import quad
from astropy.io import fits
from hunt_lib import *

ck = Check(); rng = np.random.default_rng(5960)
DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "real_research", "data")
keV = 1.602176634e-16; m_p = 1.67262192e-27; mu_gas = 0.6; mu_e = 1.148
sigma_T = 6.6524587e-29; me_c2 = 8.1871058e-14
c_kms = 299792.458; H0_kms = 100*h
Ez = lambda z: np.sqrt(OM_M*(1 + np.asarray(z, dtype=float))**3 + OM_L)
def DA_Mpc(z):
    return quad(lambda t: c_kms/(H0_kms*float(Ez(t))), 0.0, z)[0]/(1+z)
def rho_c_z(z):
    return rho_crit*Ez(z)**2

# ------------------------------------------------------------------ loaders
def load_tsv(path, cols):
    hdr = None; rows = []
    for line in open(path, encoding="latin-1"):
        if line.startswith("#") or not line.strip(): continue
        f = line.rstrip("\n").split("\t")
        if hdr is None: hdr = f; continue
        if f[0].strip().startswith("---") or f[0].strip() == "": continue
        rows.append(f)
    idx = {k: i for i, k in enumerate(hdr)}
    out = {}
    for k in cols:
        v = []
        for r in rows:
            s = r[idx[k]].strip()
            try: v.append(float(s))
            except ValueError: v.append(np.nan)
        out[k] = np.array(v)
    out["_flags"] = {k: np.array([r[idx[k]].strip() for r in rows]) for k in hdr if k.startswith("l_")}
    return out

def load_efeds():
    """Bahar+2022 table2: R500 [arcmin], T500/Tcex500 [keV], Mgas500 [1e12 Msun], Yx500 [1e12 keV Msun]."""
    D = load_tsv(os.path.join(DATA, "efeds_bahar2022_table2.tsv"),
                 ["z", "R500", "T500", "e_T500", "E_T500", "Mgas500", "e_Mgas500", "E_Mgas500",
                  "Tcex500", "e_Tcex500", "E_Tcex500", "Yx500", "Texp"])
    z = D["z"]; T = D["T500"]; Mg = D["Mgas500"]*1e12
    eT = (D["e_T500"] + D["E_T500"])/2
    eMg = (D["e_Mgas500"] + D["E_Mgas500"])/2*1e12
    da = np.array([DA_Mpc(t) if np.isfinite(t) and t > 0 else np.nan for t in z])
    R500 = D["R500"]*(math.pi/(180*60))*da*1e3                     # arcmin -> kpc (physical, angular-diameter)
    M500 = 500*rho_c_z(np.nan_to_num(z))*(4*math.pi/3)*(R500*kpc)**3/Msun
    good = (D["_flags"]["l_Mgas500"] == "") & np.isfinite(eT) & np.isfinite(eMg) & (T > 0) & (Mg > 0) & (R500 > 0)
    return dict(z=z, T=T, eT=eT, Mg=Mg, eMg=eMg, R500=R500, M500=M500, good=good,
                Tcex=D["Tcex500"], eTcex=(D["e_Tcex500"] + D["E_Tcex500"])/2, name="eFEDS (Bahar+2022)")

def load_erass1():
    d = fits.open(os.path.join(DATA, "erass1cl_primary_v3.2.fits"))[1].data
    col = lambda c: np.array(d[c], dtype=float)
    z = col("BEST_Z"); T = col("KT"); Tl = col("KT_L"); Th = col("KT_H")
    Mg = col("MGAS500")*1e11; Mgl = col("MGAS500_L")*1e11; Mgh = col("MGAS500_H")*1e11
    good = np.isfinite(T) & (T > 0) & (Mg > 0) & np.isfinite(z) & (z > 0) & (z < 1.0)
    return dict(z=z, T=T, eT=(Th - Tl)/2, Mg=Mg, eMg=(Mgh - Mgl)/2, R500=col("R500"),
                M500=col("M500")*1e13, cts=col("CTS500"), ra=col("RA"), dec=col("DEC"),
                good=good, name="eRASS1 (Bulbul+2024)")

def load_psz2():
    D = load_tsv(os.path.join(DATA, "psz2_union.tsv"),
                 ["RAJ2000", "DEJ2000", "z", "SNR", "MSZ", "Y5R500", "e_Y5R500"])
    return dict(ra=D["RAJ2000"], dec=D["DEJ2000"], z=D["z"], snr=D["SNR"], msz=D["MSZ"],
                y5=D["Y5R500"]*1e-3, ey5=D["e_Y5R500"]*1e-3, name="PSZ2 union (Planck+2016)")

# ------------------------------------------------------------------ estimators
def slope_suite(x, y, sx, sy, nboot=400):
    """Four power-law-index estimators on log10 quantities, with a bootstrap error on each.
    fw   = OLS y|x           (the item's literal request: d log kT / d log M_gas)
    inv  = 1/OLS x|y         (the same relation read the other way round)
    orth = orthogonal / total-least-squares
    eiv  = maximum likelihood with the QUOTED measurement errors on both axes and a free intrinsic scatter in y."""
    def one(x, y, sx, sy):
        A = np.vstack([x, np.ones_like(x)]).T
        fw = np.linalg.lstsq(A, y, rcond=None)[0][0]
        B = np.vstack([y, np.ones_like(y)]).T
        inv = 1.0/np.linalg.lstsq(B, x, rcond=None)[0][0]
        vx, vy, cxy = x.var(), y.var(), np.cov(x, y)[0, 1]
        orth = ((vy - vx) + math.sqrt((vy - vx)**2 + 4*cxy**2))/(2*cxy)
        xp = np.median(x)
        def nll(p):
            a, b, ls = p; s = math.exp(ls)
            v = sy**2 + a*a*sx**2 + s*s
            r = y - (a*(x - xp) + b)
            return 0.5*np.sum(r*r/v + np.log(v))
        r = minimize(nll, [fw, np.median(y), math.log(0.1)], method="Nelder-Mead",
                     options=dict(maxiter=30000, maxfev=30000, xatol=1e-6, fatol=1e-6))
        return fw, inv, orth, r.x[0], math.exp(r.x[2])
    val = one(x, y, sx, sy)
    keys = ["fw", "inv", "orth", "eiv", "sint"]
    if nboot == 0:
        return dict(zip(keys, val)), dict(zip(keys, [float("nan")]*5))
    bsv = []
    for _ in range(nboot):
        i = rng.integers(0, len(x), len(x))
        try: bsv.append(one(x[i], y[i], sx[i], sy[i]))
        except Exception: pass
    bsv = np.array(bsv)
    return dict(zip(keys, val)), dict(zip(keys, bsv.std(axis=0)))

def logerr(v, e):
    return np.clip(np.nan_to_num(e/(np.maximum(v, 1e-30)*math.log(10)), nan=0.30), 0.01, 1.0)

P("="*120)
P("ITEM 59 -- the cluster temperature / gas-mass power-law index.  Framework: exactly 1/2, no free parameter.")
P("="*120)
info("derivation actually used (so the reader can see where 1/2 comes from and what else rides on it):")
info("  isothermal HSE with rho_gas ~ r^-alpha_g  =>  kT = (mu m_p/alpha_g) * nu(y) g_bar(r) r;  deep-MOND Route A")
info("  nu -> 1/sqrt(y) makes that (mu m_p/alpha_g) sqrt(G M_b a_0), radius-free, slope 1/2, zero point ~ 1/alpha_g.")

EF = load_efeds(); ER = load_erass1()
info(f"{EF['name']}: {EF['good'].sum()} systems with a measured (non-upper-limit) M_gas and a fitted T")
info(f"{ER['name']}: {ER['good'].sum()} systems with a finite KT and M_gas, z < 1")
info(f"median fractional error: eFEDS  T {np.median(EF['eT'][EF['good']]/EF['T'][EF['good']]):.2f}, "
     f"M_gas {np.median(EF['eMg'][EF['good']]/EF['Mg'][EF['good']]):.2f}   |   "
     f"eRASS1  T {np.median(ER['eT'][ER['good']]/ER['T'][ER['good']]):.2f}, "
     f"M_gas {np.median(ER['eMg'][ER['good']]/ER['Mg'][ER['good']]):.2f}")
info("-> the eRASS1 all-sky temperatures are 60-70% uncertain per object.  Any slope from the FULL catalogue is a")
info("   statement about the survey's faint end, not about cluster physics.  Both samples are therefore scanned in")
info("   data quality and in mass below, and the scan is reported whether or not it flatters the prediction.")

# ---- the scan that decides everything: slope vs data quality and vs mass floor
def fit_simple(x, y, nboot=400):
    s = np.polyfit(x, y, 1)[0]
    v = [np.polyfit(x[i], y[i], 1)[0] for i in (rng.integers(0, len(x), len(x)) for _ in range(nboot))]
    return s, float(np.std(v)), float(np.corrcoef(x, y)[0, 1])

P(""); info("SCAN A -- eRASS1, slope of log kT on log M_gas as the temperature quality improves:")
info(f"{'cut':>26} {'N':>6} {'r':>6} {'slope':>16} {'sigma from 1/2':>16}")
scanA = []
for c in (0, 100, 300, 1000, 3000):
    m = ER["good"] & (ER["cts"] > c)
    if m.sum() < 30: continue
    s, e, r = fit_simple(np.log10(ER["Mg"][m]), np.log10(ER["T"][m]))
    scanA.append((c, m.sum(), s, e))
    info(f"{'CTS500 > '+str(c):>26} {m.sum():6d} {r:6.2f} {f'{s:.3f} +- {e:.3f}':>16} {(s-0.5)/e:16.1f}")

P(""); info("SCAN B -- eFEDS (deep field, better spectra), slope as a floor is put on the gas mass:")
info(f"{'cut':>26} {'N':>6} {'r':>6} {'slope':>16} {'sigma from 1/2':>16}")
gEF = EF["good"] & (EF["eT"]/EF["T"] < 0.5)
scanB = []
for q in (0, 25, 40, 60, 70):
    thr = np.percentile(EF["Mg"][gEF], q)
    m = gEF & (EF["Mg"] > thr)
    if m.sum() < 30: continue
    s, e, r = fit_simple(np.log10(EF["Mg"][m]), np.log10(EF["T"][m]))
    scanB.append((thr, m.sum(), s, e))
    info(f"{'M_gas > %.1e Msun' % thr:>26} {m.sum():6d} {r:6.2f} {f'{s:.3f} +- {e:.3f}':>16} {(s-0.5)/e:16.1f}")

P(""); info("SCAN A/B are POST HOC: the two cuts used below (eRASS1 CTS>1000 and M_gas>1e13; eFEDS T-err<50% and the same")
info("mass floor) were chosen after looking at those scans, so the headline number is conditional and must be shown")
info("with its cut dependence, not quoted alone.  The full grid, eRASS1:")
info(f"{'':>14}" + "".join(f"{'M_gas>%.0e' % t:>14}" for t in (0, 3e12, 1e13, 3e13)))
for c in (300, 600, 1000, 2000):
    row = ""
    for t in (0, 3e12, 1e13, 3e13):
        m = ER["good"] & (ER["cts"] > c) & (ER["Mg"] > t)
        if m.sum() < 25: row += f"{'N<25':>14}"; continue
        s, e, _ = fit_simple(np.log10(ER["Mg"][m]), np.log10(ER["T"][m]), nboot=200)
        row += f"{f'{s:.2f}+-{e:.2f}':>14}"
    info(f"{'CTS>'+str(c):>14}" + row)
info("the grid moves between about 0.36 and 0.55 -- the 1/2 is not knife-edge on the cut, but it is not pinned to")
info("+-0.03 by these data either, and the eFEDS confirmation below is a genuinely independent survey, not a re-cut.")

# ---- the two "clean" subsamples: well-measured temperatures, cluster (not group) regime
mER = ER["good"] & (ER["cts"] > 1000) & (ER["Mg"] > 1e13)
mEF = gEF & (EF["Mg"] > 1e13)
res = {}
for lab, D, m in [("eRASS1 CTS>1000, M_gas>1e13", ER, mER), ("eFEDS T-err<50%, M_gas>1e13", EF, mEF)]:
    x, y = np.log10(D["Mg"][m]), np.log10(D["T"][m])
    sx, sy = logerr(D["Mg"][m], D["eMg"][m]), logerr(D["T"][m], D["eT"][m])
    v, e = slope_suite(x, y, sx, sy)
    res[lab] = (v, e, m.sum())
    P("")
    info(f"{lab}:  N = {m.sum()}, log M_gas spread {x.std():.2f} dex, correlation {np.corrcoef(x,y)[0,1]:.2f}")
    for k, nm in [("fw", "OLS  kT | M_gas   (the item's literal ask)"), ("inv", "1/OLS M_gas | kT  (relation read backwards)"),
                  ("orth", "orthogonal / TLS"), ("eiv", "EIV with quoted errors, scatter in kT")]:
        info(f"    {nm:44s} {v[k]:7.3f} +- {e[k]:.3f}   ({(v[k]-0.5)/max(e[k],1e-6):+6.1f} sigma from 1/2)")
    info(f"    intrinsic scatter in log kT at fixed M_gas: {v['sint']:.3f} +- {e['sint']:.3f} dex")

# ---- MUTATION CONTROL 1: which of those four estimators is actually unbiased, with THIS error budget?
P(""); info("MUTATION CONTROL 1 -- estimator bias.  Mock catalogues built with a TRUE slope of exactly 1/2, the observed")
info("log M_gas spread, and the observed per-object errors; each estimator is then run on the mock.  An estimator that")
info("does not return 0.50 here cannot be used to test 0.50 on the data.")
v0, e0, n0 = res["eRASS1 CTS>1000, M_gas>1e13"]
xr = np.log10(ER["Mg"][mER]); sxr = logerr(ER["Mg"][mER], ER["eMg"][mER]); syr = logerr(ER["T"][mER], ER["eT"][mER])
mock = []
for _ in range(150):
    xt = rng.normal(0, xr.std(), len(xr))
    yt = 0.5*xt + rng.normal(0, v0["sint"], len(xr))
    xo = xt + rng.normal(0, sxr); yo = yt + rng.normal(0, syr)
    vv, _ = slope_suite(xo, yo, sxr, syr, nboot=0)
    mock.append([vv["fw"], vv["inv"], vv["orth"], vv["eiv"]])
mock = np.array(mock)
for i, nm in enumerate(["OLS kT|M_gas", "1/OLS M_gas|kT", "orthogonal", "EIV"]):
    info(f"    {nm:18s} recovers {mock[:,i].mean():.3f} +- {mock[:,i].std():.3f} from an injected 0.500  "
         f"(bias {mock[:,i].mean()-0.5:+.3f})")
bias_fw = mock[:, 0].mean() - 0.5; bias_inv = mock[:, 1].mean() - 0.5
ck("M1 mutation control -- with the real error budget the forward regression and the EIV fit are nearly unbiased on an injected 1/2, while the inverse regression is biased HIGH by ~0.2; so the forward/EIV numbers are the ones that may be compared with 1/2 and the inverse number may not",
   abs(bias_fw) < 0.06 and bias_inv > 0.10,
   f"OLS kT|M_gas bias {bias_fw:+.3f}, inverse bias {bias_inv:+.3f}, orthogonal bias {mock[:,2].mean()-0.5:+.3f}")

# ---- MUTATION CONTROL 2: shuffle
xs, ys = np.log10(ER["Mg"][mER]).copy(), np.log10(ER["T"][mER]).copy()
sh = np.array([np.polyfit(xs, rng.permutation(ys), 1)[0] for _ in range(400)])
inj = np.polyfit(xs, ys + 0.30*(xs - xs.mean()), 1)[0] - np.polyfit(xs, ys, 1)[0]
ck("M2 mutation control -- shuffling the gas masses destroys the relation (slope consistent with zero) and an injected 0.30 slope is recovered to 1%, so the estimator is measuring the relation and not a normalisation artefact",
   abs(sh.mean()) < 3*sh.std() and abs(inj - 0.30) < 0.01,
   f"shuffled slope {sh.mean():+.4f} +- {sh.std():.4f}; injected 0.300 recovered as {inj:.4f}")

# ---- the verdict number for 59
s_er, e_er = v0["fw"], e0["fw"]
vE, eE, nE = res["eFEDS T-err<50%, M_gas>1e13"]
s_ef, e_ef = vE["fw"], eE["fw"]
P("")
info(f"the two independent samples, cluster regime, forward regression:  eRASS1 {s_er:.3f} +- {e_er:.3f} (N={n0}),"
     f"  eFEDS {s_ef:.3f} +- {e_ef:.3f} (N={nE})")
info(f"full-range value, groups included:  eRASS1 all counts {scanA[0][2]:.3f} +- {scanA[0][3]:.3f},"
     f"  eFEDS all masses {scanB[0][2]:.3f} +- {scanB[0][3]:.3f}")

# ---- the LambdaCDM alternative, computed from the same data rather than quoted
# ---- is the flattening at low mass a real curvature, or a data-quality gradient?
P(""); info("is the low-mass flattening a resolved BEND, or a level offset at the faint end?  Quadratic fit of log kT on")
info("log M_gas; the framework and self-similar LambdaCDM both require a pure power law, i.e. zero curvature:")
curv = {}
for lab, D, m in [("eRASS1 all", ER, ER["good"]), ("eRASS1 CTS>300", ER, ER["good"] & (ER["cts"] > 300)),
                  ("eRASS1 CTS>1000", ER, ER["good"] & (ER["cts"] > 1000)), ("eFEDS T-err<50%", EF, gEF)]:
    x, y = np.log10(D["Mg"][m]), np.log10(D["T"][m])
    A = np.vstack([x**2, x, np.ones_like(x)]).T
    q = np.linalg.lstsq(A, y, rcond=None)[0]
    bq = [np.linalg.lstsq(np.vstack([x[i]**2, x[i], np.ones_like(i)]).T, y[i], rcond=None)[0][0]
          for i in (rng.integers(0, len(x), len(x)) for _ in range(300))]
    curv[lab] = (q[0], float(np.std(bq)))
    info(f"    {lab:18s} N={m.sum():5d}: d2 log kT/d(log M_gas)^2 = {q[0]:+.4f} +- {np.std(bq):.4f} "
         f"({q[0]/np.std(bq):+.1f} sigma from a pure power law)")
ck("59 curvature AGAINST BOTH SIDES -- the eRASS1 relation is NOT a pure power law: the quadratic term is +0.065 +- 0.005 over the full catalogue and +0.074 +- 0.013 at CTS>300, so the T-M_gas relation steepens with mass.  Neither the framework's exact 1/2 nor self-similar LambdaCDM allows any curvature, so whichever index is quoted is a local tangent, not a law.  Stated against the finding as well: the significance falls to 1.4 sigma in the deepest cut and to 1.2 sigma in eFEDS, so a residual data-quality gradient is NOT excluded as the cause",
   curv["eRASS1 CTS>300"][0] > 3*curv["eRASS1 CTS>300"][1],
   "; ".join(f"{k}: {curv[k][0]:+.4f} +- {curv[k][1]:.4f}" for k in curv))

P(""); info("the LambdaCDM alternative, computed here and not quoted: self-similar kT ~ (M500 E(z))^{2/3} plus an")
info("f_gas-M500 slope s gives d log kT/d log M_gas = (2/3)/(1+s).  First the slope s measured inside each sample:")
lcdm_int = {}
for lab, D, m in [("eRASS1 CTS>1000, M_gas>1e13", ER, mER), ("eFEDS T-err<50%, M_gas>1e13", EF, mEF)]:
    ok2 = m & np.isfinite(D["M500"]) & (D["M500"] > 0)
    sg, eg, _ = fit_simple(np.log10(D["M500"][ok2]), np.log10(D["Mg"][ok2]/D["M500"][ok2]))
    st, et, _ = fit_simple(np.log10(D["M500"][ok2]), np.log10(D["T"][ok2]))
    lcdm_int[lab] = (sg, eg, (2.0/3.0)/(1.0 + sg))
    info(f"    {lab:32s} f_gas slope s = {sg:+.3f} +- {eg:.3f}; measured d log T/d log M500 = {st:.3f} +- {et:.3f}"
         f" (self-similar 0.667); chain -> {(2.0/3.0)/(1.0+sg):.3f}")
info("    those two internal values DISAGREE (s = +0.32 vs -0.03) and neither may be trusted: in both catalogues the")
info("    M500 and the M_gas are built from the same count rate and R500 is derived from M500, so f_gas-vs-M500 inside")
info("    one of these samples is largely a calibration relation.  That is exactly the confound hunt item 19 recorded.")
info("    So the LambdaCDM chain is instead evaluated over the EXTERNAL range the item itself quotes for f_gas slopes")
info("    from hydro simulations and from item 19, s = 0.20 to 0.40:")
pred_lo, pred_hi = (2.0/3.0)/(1.0 + 0.40), (2.0/3.0)/(1.0 + 0.20)
info(f"      s = 0.40 -> {pred_lo:.3f};   s = 0.30 -> {(2.0/3.0)/1.30:.3f};   s = 0.20 -> {pred_hi:.3f}")

ck("59 RESULT -- in the cluster regime with well-measured temperatures the index IS 1/2 in two independent eROSITA samples, but it is NOT a discriminating hit: the LambdaCDM chain (self-similar T plus an f_gas slope in the range 0.20-0.40) covers 0.476-0.556 and is indistinguishable from 1/2 at this precision, exactly as the item itself warned",
   abs(s_er - 0.5) < 3*e_er and abs(s_ef - 0.5) < 3*e_ef,
   f"eRASS1 {s_er:.3f} +- {e_er:.3f} (N={n0}, {(s_er-0.5)/e_er:+.1f} sigma from 1/2), eFEDS {s_ef:.3f} +- {e_ef:.3f} (N={nE}, {(s_ef-0.5)/e_ef:+.1f} sigma); LambdaCDM chain {pred_lo:.3f}-{pred_hi:.3f}")

ck("59 AGAINST INTEREST -- the SAME relation extended down into the group regime is NOT 1/2: the full-range forward slope is 0.25 +- 0.01 (eRASS1, all counts, N=3361) and 0.29 +- 0.02 (eFEDS, all masses, N=176), 9-34 sigma below the prediction, and the framework has no escape there because groups sit DEEPER in the deep-MOND regime, where the 1/2 should hold best",
   abs(scanA[0][2] - 0.5) > 5*scanA[0][3] and abs(scanB[0][2] - 0.5) > 5*scanB[0][3],
   f"eRASS1 full {scanA[0][2]:.3f} +- {scanA[0][3]:.3f} ({(scanA[0][2]-0.5)/scanA[0][3]:+.0f} sigma), eFEDS full {scanB[0][2]:.3f} +- {scanB[0][3]:.3f} ({(scanB[0][2]-0.5)/scanB[0][3]:+.0f} sigma)")
info("the honest reading of that split, both ways: the slope climbs MONOTONICALLY with data quality (eRASS1 0.25 at all")
info("counts -> 0.42 at CTS>1000) and with mass floor (eFEDS 0.29 -> 0.50), which is the signature of a low-count")
info("temperature bias plus X-ray flux selection at the faint end, not necessarily of physics.  It is NOT possible to")
info("separate those from these catalogues, so the group-regime miss is logged as an OPEN systematic on both sides")
info("(LambdaCDM's self-similar 2/3 fails there by even more) and NOT as a kill of the framework.")

# ---- zero point, both footings
P(""); info("zero point.  kT = (mu m_p/alpha_g) sqrt(G M_b a_0) has ONE O(1) unknown, the outer gas log-slope alpha_g.")
info("Solving for it at the sample median is the only honest use of the normalisation.  Baryons M_b = M_gas + M_star")
info("with the repo's standard stellar prescription f_star = clip(0.025 (M500/1e14)^-0.3, 0.01, 0.08).")
zero = {}; etaM = {}
for lab, D, m in [("eRASS1 CTS>1000, M_gas>1e13", ER, mER), ("eFEDS T-err<50%, M_gas>1e13", EF, mEF)]:
    M5 = D["M500"][m]; Mg = D["Mg"][m]; T = D["T"][m]; R5 = D["R500"][m]
    fs = np.clip(0.025*(M5/1e14)**(-0.3), 0.01, 0.08)
    Mb = Mg + fs*M5
    for foot, a0 in A0.items():
        kT_dm = mu_gas*m_p*np.sqrt(G*Mb*Msun*a0)/keV           # the alpha_g = 1 normalisation
        alpha = float(np.median(kT_dm/T))
        eta = (2.0/alpha)**2                                    # extra mass boost if alpha_g were the canonical 2
        gb = G*Mb*Msun/(R5*kpc)**2
        em = float(np.median(M5/(nu(gb/a0)*Mb)))                # the INDEPENDENT mass-side residual at R500
        zero[(lab, foot)] = (alpha, eta); etaM[(lab, foot)] = em
        info(f"    {lab:32s} {foot:10s} implied alpha_g = {alpha:.2f};  at the canonical alpha_g = 2 that is a further"
             f" mass factor eta_T = {eta:.2f};  mass-side eta at R500 on the same rows = {em:.2f}")
info("    the Newtonian/LambdaCDM version of the same line, for comparison: kT = (mu m_p/alpha_g) G M500/R500 gives")
gN = G*ER["M500"][mER]*Msun/(ER["R500"][mER]*kpc)**2
aN = float(np.median(mu_gas*m_p*gN*(ER["R500"][mER]*kpc)/keV/ER["T"][mER]))
info(f"    {'eRASS1 CTS>1000, M_gas>1e13':32s} {'LambdaCDM':10s} implied alpha_g = {aN:.2f} -- also O(1), also unconstrained")
al_c = zero[("eRASS1 CTS>1000, M_gas>1e13", "canonical")][0]
al_a = zero[("eRASS1 CTS>1000, M_gas>1e13", "alt")][0]
em_c = etaM[("eRASS1 CTS>1000, M_gas>1e13", "canonical")]
em_a = etaM[("eRASS1 CTS>1000, M_gas>1e13", "alt")]
rec_c, rec_a = al_c*math.sqrt(em_c), al_a*math.sqrt(em_a)
info("    the one non-trivial thing the zero point does say: the temperature side and the mass side must be reconciled")
info("    by the SAME missing factor.  Applying the mass-side eta measured on these very rows to the temperature")
info(f"    normalisation gives alpha_g = {rec_c:.2f} (canonical) / {rec_a:.2f} (alt) -- inside the physical 1.5-2.5 band for the")
info("    outer gas log-slope.  That is internal bookkeeping consistency, NOT evidence: the residual eta itself is the")
info("    unexplained part, and it is the same cluster residual the rest of the repo carries.")
ck("59 zero point AGAINST INTEREST -- the a_0 normalisation is NOT a test.  It buys exactly one number, the outer gas log-slope alpha_g, which comes out 1.18-1.36 on the two footings against a physical 1.5-2.5; read as a mass boost at alpha_g = 2 that is a cluster residual eta_T = 2.2-2.9, some 25-50% larger than the mass-side eta = 1.8-2.0 measured on the same rows.  The Newtonian version needs an equally free alpha_g = 2.8, so the zero point falsifies neither side",
   1.0 < al_c < 2.5 and 1.0 < al_a < 2.5 and abs(rec_c - 2.0) < 0.6,
   f"canonical alpha_g = {al_c:.2f} (eta_T = {(2/al_c)**2:.2f}, mass-side eta = {em_c:.2f}), alt alpha_g = {al_a:.2f} (eta_T = {(2/al_a)**2:.2f}, mass-side eta = {em_a:.2f}); reconciled alpha_g = {rec_c:.2f}/{rec_a:.2f}")

# ---- MUTATION CONTROL 3: a_0 must matter to the zero point
M5 = ER["M500"][mER]; fs = np.clip(0.025*(M5/1e14)**(-0.3), 0.01, 0.08); Mb = ER["Mg"][mER] + fs*M5
al_10 = np.median(mu_gas*m_p*np.sqrt(G*Mb*Msun*10*A0["canonical"])/keV/ER["T"][mER])
ck("M3 mutation control -- multiplying a_0 by ten moves the implied alpha_g by exactly sqrt(10), so the zero point really is carrying a_0 and is not insensitive to it",
   abs(al_10/al_c - math.sqrt(10)) < 0.02, f"alpha_g(a_0) = {al_c:.3f} -> alpha_g(10 a_0) = {al_10:.3f}, ratio {al_10/al_c:.4f} vs sqrt(10) = {math.sqrt(10):.4f}")

# =====================================================================================================
P(""); P("="*120)
P("ITEM 60 -- the SZ Y / gas-mass index.  Framework: exactly 3/2.  First: how much of that is a definition?")
P("="*120)
PZ = load_psz2()
info(f"{PZ['name']}: {len(PZ['ra'])} SZ detections with a marginal Y5R500 and a redshift")
info("Y_500 = (sigma_T k / m_e c^2 mu_e m_p) M_gas <T> is an IDENTITY for an isothermal atmosphere, so")
info("d log Y/d log M_gas = 1 + d log kT/d log M_gas in EVERY theory.  Item 60 therefore adds no new prediction to")
info("item 59; what it adds is an independent instrument.  The test actually run is the closure of the triangle.")

# verify the identity inside eRASS1 itself using its own Y_X = M_gas kT column
d = fits.open(os.path.join(DATA, "erass1cl_primary_v3.2.fits"))[1].data
YX = np.array(d["YX500"], dtype=float)
mm = ER["good"] & np.isfinite(YX) & (YX > 0)
ratio_YX = np.median(YX[mm]/(ER["Mg"][mm]/1e11*ER["T"][mm]))
ck("60 identity check -- eRASS1's own Y_X column equals M_gas x kT to 4%, confirming that the Y-M_gas index is the T-M_gas index plus one by construction and not by physics",
   abs(ratio_YX - 1.0) < 0.10, f"median Y_X/(M_gas kT) = {ratio_YX:.3f} (exactly 1 by definition)")

# ---- cross-match PSZ2 x eRASS1
def crossmatch(P_, E_, rad_arcmin=5.0, ra_shift=0.0, mask=None):
    ok = E_["good"] if mask is None else mask; ei = np.where(ok)[0]
    mi, mj, sep = [], [], []
    ra_p = P_["ra"] + ra_shift
    for i in range(len(ra_p)):
        if not (np.isfinite(P_["z"][i]) and np.isfinite(P_["y5"][i])): continue
        dra = (E_["ra"][ei] - ra_p[i])*math.cos(math.radians(P_["dec"][i]))
        dd = np.hypot(dra, E_["dec"][ei] - P_["dec"][i])*60.0
        j = int(np.argmin(dd))
        if dd[j] < rad_arcmin and abs(E_["z"][ei[j]] - P_["z"][i]) < 0.05*(1 + P_["z"][i]):
            mi.append(i); mj.append(ei[j]); sep.append(dd[j])
    return np.array(mi), np.array(mj), np.array(sep)

gasmask = np.isfinite(ER["Mg"]) & (ER["Mg"] > 0) & np.isfinite(ER["z"]) & (ER["z"] > 0)   # Y-M_gas needs no T
mi, mj, sep = crossmatch(PZ, ER, mask=gasmask)
info(f"PSZ2 x eRASS1 within 5 arcmin and |dz| < 0.05(1+z): {len(mi)} matches, median separation {np.median(sep):.2f} arcmin")
mi_s, mj_s, _ = crossmatch(PZ, ER, ra_shift=0.5, mask=gasmask)
ck("M4 mutation control -- shifting every Planck position by 0.5 deg in RA before matching collapses the match count, so the matches are real associations and not a chance-coincidence rate",
   len(mi_s) < 0.15*len(mi), f"{len(mi)} true matches vs {len(mi_s)} after a 0.5 deg shift ({100*len(mi_s)/len(mi):.1f}%)")

zm = PZ["z"][mi]; DAs = np.array([DA_Mpc(t) for t in zm]); arcmin = math.pi/(180*60)
Ysph = PZ["y5"][mi]/1.796*(DAs*arcmin)**2                     # arcmin^2 -> Mpc^2, 5R500 cylinder -> R500 sphere
eYsph = PZ["ey5"][mi]/1.796*(DAs*arcmin)**2
Mgm = ER["Mg"][mj]; eMgm = ER["eMg"][mj]; Tm = ER["T"][mj]; snr = PZ["snr"][mi]

P(""); info("SCAN C -- Y_SZ - M_gas index as the SZ detection significance is raised (the SZ survey is Y-selected, so")
info("the low-significance end is Malmquist-flattened; if that is what is happening the index must climb):")
info(f"{'cut':>26} {'N':>6} {'r':>6} {'slope':>16} {'sigma from 3/2':>16}")
scanC = []
for lo in (4.5, 6, 8, 10):
    m = (Ysph > 0) & (snr > lo)
    if m.sum() < 40: continue
    s, e, r = fit_simple(np.log10(Mgm[m]), np.log10(Ysph[m]))
    scanC.append((lo, m.sum(), s, e))
    info(f"{'PSZ2 SNR > '+str(lo):>26} {m.sum():6d} {r:6.2f} {f'{s:.3f} +- {e:.3f}':>16} {(s-1.5)/e:16.1f}")

mY = (Ysph > 0) & (snr > 8)
vY, eY_ = slope_suite(np.log10(Mgm[mY]), np.log10(Ysph[mY]),
                      logerr(Mgm[mY], eMgm[mY]), logerr(Ysph[mY], eYsph[mY]))
info("")
info(f"best SZ subsample (SNR > 8, N = {mY.sum()}):")
for k, nm in [("fw", "OLS  Y | M_gas"), ("inv", "1/OLS M_gas | Y"), ("orth", "orthogonal / TLS"), ("eiv", "EIV with quoted errors")]:
    info(f"    {nm:30s} {vY[k]:7.3f} +- {eY_[k]:.3f}   ({(vY[k]-1.5)/max(eY_[k],1e-6):+6.1f} sigma from 3/2)")

# ---- MUTATION CONTROL 5: which estimator is unbiased for the Y - M_gas error budget?
sxY = logerr(Mgm[mY], eMgm[mY]); syY = logerr(Ysph[mY], eYsph[mY]); xY = np.log10(Mgm[mY])
mockY = []
for _ in range(150):
    xt = rng.normal(0, xY.std(), len(xY))
    yt = 1.5*xt + rng.normal(0, vY["sint"], len(xY))
    vv, _ = slope_suite(xt + rng.normal(0, sxY), yt + rng.normal(0, syY), sxY, syY, nboot=0)
    mockY.append([vv["fw"], vv["inv"], vv["orth"], vv["eiv"]])
mockY = np.array(mockY)
info("")
info("MUTATION CONTROL 5 -- same estimator-bias mock for the Y - M_gas error budget, true index injected at 3/2:")
for i, nm in enumerate(["OLS Y|M_gas", "1/OLS M_gas|Y", "orthogonal", "EIV"]):
    info(f"    {nm:18s} recovers {mockY[:,i].mean():.3f} +- {mockY[:,i].std():.3f} from an injected 1.500  "
         f"(bias {mockY[:,i].mean()-1.5:+.3f})")
ck("M5 mutation control -- the forward and EIV estimators recover an injected 3/2 to better than 0.05 with the real Y and M_gas error budget, so the measured 1.22 is NOT an artefact of regression dilution; the inverse estimator overshoots by ~0.5 and is unusable, which is why its 1.81 is not quoted as the answer",
   abs(mockY[:, 0].mean() - 1.5) < 0.08 and abs(mockY[:, 3].mean() - 1.5) < 0.08 and mockY[:, 1].mean() - 1.5 > 0.25,
   f"forward bias {mockY[:,0].mean()-1.5:+.3f}, EIV bias {mockY[:,3].mean()-1.5:+.3f}, inverse bias {mockY[:,1].mean()-1.5:+.3f}")

# ---- the triangle closure on the SAME objects
mt = (Ysph > 0) & np.isfinite(Tm) & (Tm > 0) & (snr > 6)
sT3, eT3, _ = fit_simple(np.log10(Mgm[mt]), np.log10(Tm[mt]))
sY3, eY3, _ = fit_simple(np.log10(Mgm[mt]), np.log10(Ysph[mt]))
gap = sY3 - sT3 - 1.0; egap = math.hypot(eY3, eT3)
info("")
info(f"triangle closure on the SAME {mt.sum()} objects: d log Y/d log M_gas = {sY3:.3f} +- {eY3:.3f},"
     f"  d log kT/d log M_gas = {sT3:.3f} +- {eT3:.3f};  the identity requires the first minus the second to be exactly 1.")
info(f"    measured difference = {sY3 - sT3:.3f}, i.e. {gap:+.3f} +- {egap:.3f} away from the required 1.000")

# ---- absolute Y_SZ vs Y_X
K_Y = sigma_T/(me_c2*mu_e*m_p)
YXpred = K_Y*(Tm*keV)*(Mgm*Msun)/Mpc**2
mabs = (Ysph > 0) & np.isfinite(Tm) & (Tm > 0)
info("")
info("absolute check of my own SZ pipeline: Y_500(Planck marginal) against the identity's Y = K M_gas kT built from")
info("eRASS1.  If the conversion (units, the 1.796 cylinder-to-sphere factor, D_A) and both instruments were right the")
info("ratio would be 1.")
for lo, hi in [(0, 6), (6, 8), (8, 12), (12, 1e9)]:
    s = mabs & (snr >= lo) & (snr < hi)
    if s.sum() < 10: continue
    info(f"    SNR {lo:g}-{hi:g}: N = {s.sum():4d}, median Y_SZ/Y_X = {np.median(Ysph[s]/YXpred[s]):.2f}")
r_hi = np.median(Ysph[mabs & (snr > 8)]/YXpred[mabs & (snr > 8)])
r_lo = np.median(Ysph[mabs & (snr < 6)]/YXpred[mabs & (snr < 6)])
ck("60 AGAINST INTEREST -- my own SZ pipeline does not close absolutely: Y_SZ exceeds the identity's K M_gas kT by 1.9x at low SNR falling to 1.4x at SNR>8.  The SNR dependence is the known Y-theta degeneracy in the PSZ2 MARGINAL Y5R500 (Eddington bias), and the residual 1.4x at high SNR is unattributed here (eROSITA soft-band temperatures, the isothermal assumption, or the aperture factor).  Any Y normalisation from this pipeline is therefore untrustworthy at the 40% level and is NOT used as a test",
   r_lo > r_hi and r_hi > 1.15,
   f"median Y_SZ/Y_X = {r_lo:.2f} (SNR<6) -> {r_hi:.2f} (SNR>8); a closed pipeline would give 1.00")

ck("60 RESULT -- the measured index is 1.22 +- 0.09 at the best SZ significance cut, 2.9 sigma BELOW the framework's exact 3/2, and the mock above says that number is not a dilution artefact.  It is nevertheless NOT a kill: the index climbs 0.99 -> 1.22 as the SNR cut is raised, which is uncorrected Y-selection Malmquist bias in a Y-selected catalogue pushing the same way, and the mock covers regression dilution only, not selection.  The +-0.05 the item asks for is out of reach by a factor of two",
   abs(vY["fw"] - 1.5) > 2*eY_["fw"] and scanC[-2][2] > scanC[0][2],
   f"SNR>4.5: {scanC[0][2]:.3f} +- {scanC[0][3]:.3f}; SNR>8: {vY['fw']:.3f} +- {eY_['fw']:.3f} ({(vY['fw']-1.5)/eY_['fw']:+.1f} sigma from 3/2); SNR>10: {scanC[-1][2]:.3f} +- {scanC[-1][3]:.3f}")

ck("60 triangle closure FAILS -- on the SAME objects the SZ index minus the X-ray index is 0.75 +- 0.10 where the definition of Y forces exactly 1.000, a 2.5 sigma inconsistency, so at least one of the two measurements carries a selection or calibration bias of that size.  This is a check on the DATA, not on the framework, and it is the main reason the 3/2 test cannot be graded here",
   abs(gap) > 2*egap, f"Y index {sY3:.3f} - T index {sT3:.3f} = {sY3-sT3:.3f}, required 1.000, offset {gap:+.3f} +- {egap:.3f}")

P(""); P("="*120)
P("SUMMARY")
P("="*120)
info(f"59  d log kT/d log M_gas, cluster regime, well-measured T:  eRASS1 {s_er:.3f} +- {e_er:.3f},  eFEDS {s_ef:.3f} +- {e_ef:.3f}")
info(f"    framework 0.500 exactly; LambdaCDM chain {pred_lo:.3f}-{pred_hi:.3f} for f_gas slopes 0.20-0.40.  Consistent, NOT discriminating.")
info(f"    groups included the index falls to {scanA[0][2]:.3f} +- {scanA[0][3]:.3f} -- open systematic, both sides.")
info(f"    and the relation is not a pure power law at all in eRASS1: curvature {curv['eRASS1 all'][0]:+.4f} +- {curv['eRASS1 all'][1]:.4f}, which both")
info("    the framework and self-similar LambdaCDM forbid; 1.2-1.4 sigma only in the two cleanest cuts, so unresolved.")
info(f"    zero point buys one O(1) number: alpha_g = {al_c:.2f} (canonical) / {al_a:.2f} (alt), i.e. eta ~ {(2/al_c)**2:.2f}-{(2/al_a)**2:.2f}.")
info(f"60  d log Y_SZ/d log M_gas = {scanC[0][2]:.3f} +- {scanC[0][3]:.3f} (SNR>4.5) rising to {vY['fw']:.3f} +- {eY_['fw']:.3f} (SNR>8);")
info(f"    framework 1.500 exactly, so {(vY['fw']-1.5)/eY_['fw']:+.1f} sigma; but the rise with the SNR cut is uncorrected SZ-selection bias")
info(f"    pushing the same way, and the SZ/X-ray triangle does not close ({gap:+.3f} +- {egap:.3f} from the required 1).")
info("    and item 60 is item 59 + 1 by definition, so it was never an independent prediction to begin with.")
sys.exit(ck.done())
