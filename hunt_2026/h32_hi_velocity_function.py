#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
h32_hi_velocity_function.py -- HUNT ITEM 32: the HI velocity function from the baryonic mass function.
======================================================================================================
The item as posed: convolve the baryonic mass function with v^4 = G M_b a_0 and see whether the observed HI velocity
(width) function comes out, with no halo velocity function anywhere in the calculation.  "LambdaCDM: velocity function
too steep at low v.  Kepler-grade if the predicted VF is within errors at 30-100 km/s."

Why this is a real test and not a tautology.  In LambdaCDM the mass function of galaxies and the velocity function of
galaxies are two different objects joined by a halo: n(V) comes from the HALO mass function through V_max(M_halo), and
the well-known result is that it is far too steep at low V (Zavala+09; Papastergis+11 measured a factor ~8 excess at
w = 50 km/s and ~100 extrapolated to 20).  In the framework there is no second function: v = (G M_b a_0)^{1/4} maps the
baryonic mass function onto the velocity function point by point, with a_0 fixed by Lambda and nothing else free.  So
the framework makes a ZERO-PARAMETER prediction of one published function from another published function.

Inputs, all published or fetched this session:
  * the alpha.100 HI MASS function and the alpha.100 HI WIDTH function, both from the SAME analysis of the SAME 21827
    sources -- Oman 2022, MNRAS 509, 3268, Table 1 (this matters: a mass function and a width function fitted by
    different authors with different completeness limits could not be compared at the amplitude level).
        HIMF  (Schechter):          log phi* = -2.26 +- 0.02, log M* = 9.92 +- 0.01, alpha = -1.29 +- 0.02
        HIWF  (modified Schechter): log phi* = -1.67, w* = 307 km/s, alpha = -0.63, beta = 2.0   (all-statistical)
                                    log phi* = -1.67, w* = 300 km/s, alpha = -0.56, beta = 2.1   (counting-only)
  * ALFALFA alpha.100 itself (Haynes+2018, J/ApJ/861/49) and the ALFALFA-SDSS value-added catalogue
    (Durbala+2020, J/AJ/160/271), for the baryonic-mass-to-HI-mass relation, the inclination distribution, and an
    independent 1/V_max cross-check.
Both footings.  Mutation controls.  Checks CAN fail.  REPORT AGAINST INTEREST.
"""
import sys, math
import numpy as np
from scipy.integrate import quad
from scipy.optimize import curve_fit
from hunt_lib import *
ck = Check(); rng = np.random.default_rng(32)
LN10 = math.log(10)

# ---------------------------------------------------------------- the two published functions
MF  = dict(lphi=-2.26, lMs=9.92, al=-1.29)                       # Oman 2022 Table 1, alpha.100 HIMF
WF  = dict(lphi=-1.67, ws=307.0, al=-0.63, be=2.0)               # Oman 2022 Table 1, alpha.100 HIWF (all-stat)
WFc = dict(lphi=-1.67, ws=300.0, al=-0.56, be=2.1)               # the same, counting-uncertainties only
WF_AL_ERR = (1.12, 0.41)                                         # +/- on alpha (all-stat);  counting-only: +0.21/-0.16
def phi_M(lM, p=MF):
    x = 10**(np.asarray(lM, float) - p["lMs"]); return LN10*10**p["lphi"]*x**(p["al"]+1)*np.exp(-x)
def phi_W(lw, p=WF):
    x = 10**np.asarray(lw, float)/p["ws"]; return LN10*10**p["lphi"]*x**p["al"]*np.exp(-x**p["be"])

P("="*118); P("ITEM 32 -- the HI velocity (width) function predicted from the HI mass function with no halo anywhere")
P("="*118)
lmg = np.linspace(7.0, 11.5, 4000); lwg = np.linspace(math.log10(20), 3.0, 4000)
nM = float(np.trapz(phi_M(lmg), lmg)); nW = float(np.trapz(phi_W(lwg), lwg))
info(f"published HIMF integrated over M_HI > 1e7:  n = {nM:.4f} Mpc^-3")
info(f"published HIWF integrated over w50 > 20 km/s: n = {nW:.4f} Mpc^-3;  ratio {nM/nW:.3f}")
ck("32.0 the two published functions are mutually consistent at the level the amplitude test needs: fitted independently "
   "to the same 21827 sources, they integrate to total number densities that agree to about 25%.  That 0.1 dex is the "
   "IRREDUCIBLE FLOOR on any amplitude comparison below and it is stated here before any framework number is computed",
   0.6 < nM/nW < 1.6, f"n(HIMF, M_HI > 1e7)/n(HIWF, w > 20) = {nM/nW:.3f} = {math.log10(nM/nW):+.3f} dex")

# ---------------------------------------------------------------- 1. ingredient checks on the catalogues
P(""); P("-"*118); P("1. INGREDIENTS, EACH CHECKED"); P("-"*118)
a = load_alfalfa()
wsmo = np.where(a["W50"] < 400, a["W50"]/20.0, 20.0)
snr_calc = (1000*a["flux"]/a["W50"])*np.sqrt(wsmo)/a["rms"]
g = np.isfinite(snr_calc) & (a["snr"] > 0) & (snr_calc > 0)
rat = float(np.median(snr_calc[g]/a["snr"][g]))
ck("32.1a the catalogue's own signal-to-noise definition is reproduced from its published columns to better than 1% in "
   "the median -- which is what licenses the distance limit D_lim = D sqrt(SNR/6.5) used in the independent 1/V_max "
   "cross-check in section 4",
   abs(rat - 1.0) < 0.02, f"median SNR(recomputed)/SNR(catalogue) = {rat:.4f}, scatter {np.std(np.log10(snr_calc[g]/a['snr'][g])):.3f} dex, N = {g.sum()}")
base = (a["code"] == 1) & (a["pflag"] == 1) & (a["snr"] >= 6.5) & np.isfinite(a["ba"]) & (a["W50"] > 0)
f45 = (base & (a["inc"] > 45)).sum()/base.sum()
ck("32.1b the inclination distribution of the detected sample is consistent with RANDOM disc orientation, so the "
   "sin i convolution applied to the framework's prediction below is the right one and is not itself a fitted ingredient",
   abs(f45 - math.cos(math.radians(45))) < 0.02, f"f(i > 45 deg) = {f45:.4f} vs cos 45 deg = {math.cos(math.radians(45)):.4f}, N = {base.sum()}")
aMs = np.where(np.isfinite(a["logMsM"]), a["logMsM"], a["logMsT"])
mok = np.isfinite(aMs) & (a["code"] == 1) & np.isfinite(a["logMHI"])
lMb_o = np.log10(1.33*10**a["logMHI"][mok] + 10**np.nan_to_num(aMs[mok], nan=0.0)); lMH_o = a["logMHI"][mok]
AB, BB = np.polyfit(lMH_o, lMb_o, 1); SB = float(np.std(lMb_o - (AB*lMH_o + BB)))
info(f"the ONLY empirical ingredient the framework needs beyond a_0: log M_b = {AB:.4f} log M_HI {BB:+.4f} "
     f"(scatter {SB:.3f} dex, N = {mok.sum()}), measured on the ALFALFA-SDSS cross-match")
ck("32.1c that relation is close to but not exactly proportional (slope 1.13, not 1.00): gas fractions fall with mass, "
   "so the BARYONIC mass function is shallower than the HI mass function by that factor, and the framework's predicted "
   "velocity-function slope is 4(alpha_HI+1)/1.13, not 4(alpha_HI+1).  Getting this wrong would bias the predicted slope "
   "by 13%",
   1.0 < AB < 1.3, f"d log M_b/d log M_HI = {AB:.4f}; stellar mass is {np.median(10**np.nan_to_num(aMs[mok],nan=0.0)/(1.33*10**a['logMHI'][mok])):.2f} x the gas mass in the median")

# ---------------------------------------------------------------- 2. the framework's prediction
P(""); P("-"*118); P("2. THE FRAMEWORK'S ZERO-PARAMETER PREDICTION: HIMF --> HIWF"); P("-"*118)
W_TURB = 20.0                                  # km/s, turbulent FWHM added in quadrature to the rotational width
NMC, LMIN, LMAX = 900000, 6.0, 11.5
lgrid = np.linspace(LMIN, LMAX, 4000); pgrid = phi_M(lgrid); pgrid = pgrid/pgrid.sum()
NORM = float(np.trapz(phi_M(lgrid), lgrid))/NMC             # Mpc^-3 carried by each Monte-Carlo galaxy
def predict_widths(a0, w_turb=W_TURB, lmin=LMIN, scat=SB, seed=1):
    """Returns (widths, log M_HI drawn, Mpc^-3 carried by each sample).  The per-sample weight MUST be recomputed when
    the input mass function is truncated -- NMC samples then carry a smaller total number density, and using the
    full-grid weight would inflate the truncated prediction by n(full)/n(truncated)."""
    r = np.random.default_rng(seed)
    m = lgrid >= lmin; pp = pgrid*m; pp = pp/pp.sum()
    norm = float(np.trapz(np.where(m, phi_M(lgrid), 0.0), lgrid))/NMC
    lMH = r.choice(lgrid, size=NMC, p=pp)
    lMb = AB*lMH + BB + r.normal(0, scat, NMC)
    v = (G*10**lMb*Msun*a0)**0.25/1e3
    sini = np.sin(np.arccos(r.uniform(0, 1, NMC)))
    return np.sqrt((2*v*sini)**2 + w_turb**2), lMH, norm
def phi_of(w, w0, norm=None, dex=0.05):
    b = (w > w0*10**-dex) & (w < w0*10**dex); return b.sum()*(NORM if norm is None else norm)/(2*dex)
WPTS = (30., 50., 80., 120., 200.)
RES = {}
for ft, a0 in A0.items():
    w, lMH, _nrm = predict_widths(a0)
    row = []
    for w0 in WPTS:
        pr = phi_of(w, w0); ob = float(phi_W(math.log10(w0))); obc = float(phi_W(math.log10(w0), WFc))
        row.append((w0, pr, ob, pr/ob))
        info(f"{ft:10} w50 = {w0:5.0f} km/s: framework {pr:.4f}, published HIWF {ob:.4f} (counting-only fit {obc:.4f}) "
             f"Mpc^-3 dex^-1 -> ratio {pr/ob:5.2f} ({math.log10(pr/ob):+.2f} dex)")
    RES[ft] = dict(row=row, w=w, lMH=lMH)
    lo, hi = phi_of(w, 30.), phi_of(w, 100.)
    RES[ft]["slope"] = (math.log10(hi) - math.log10(lo))/(math.log10(100) - math.log10(30))
r50 = [x[3] for x in RES["canonical"]["row"]]
FLOOR = abs(math.log10(nM/nW))                       # the two published fits' own mutual normalisation, check 32.0
d80 = abs(math.log10(dict((x[0], x[3]) for x in RES["canonical"]["row"])[80.]))
d120 = abs(math.log10(dict((x[0], x[3]) for x in RES["canonical"]["row"])[120.]))
d50 = math.log10(dict((x[0], x[3]) for x in RES["canonical"]["row"])[50.])
ck("32.2a the framework turns one published function into the other with NO free parameter and matches it to within "
   "the irreducible amplitude floor -- the 0.125 dex by which the two published fits disagree with each other -- at "
   "w50 = 80 and 120 km/s.  No threshold is chosen here: the comparison is against the floor that check 32.0 measured "
   "before any framework number was computed",
   max(d80, d120) < FLOOR,
   f"|log ratio| = {d80:.3f} at 80 km/s and {d120:.3f} at 120 km/s, against the floor {FLOOR:.3f} dex; "
   f"alt footing {abs(math.log10(dict((x[0],x[3]) for x in RES['alt']['row'])[80.])):.3f} and "
   f"{abs(math.log10(dict((x[0],x[3]) for x in RES['alt']['row'])[120.])):.3f}")
ck("32.2a2 AGAINST INTEREST, and this is a real miss rather than a rounding: at w50 = 50 km/s the framework "
   "over-predicts the number density by 0.23 dex, which is nearly TWICE the amplitude floor.  The agreement is good at "
   "80-120 km/s and degrades monotonically toward the narrow end.  This check asserts the MISS, so it fails if the "
   "framework is in fact within the floor at 50 km/s",
   d50 > FLOOR,
   f"log ratio at 50 km/s = {d50:+.3f} dex (factor {10**d50:.2f}) against the {FLOOR:.3f} dex floor; at 200 km/s the "
   f"framework UNDER-predicts by {math.log10(dict((x[0],x[3]) for x in RES['canonical']['row'])[200.]):+.3f} dex")
w, lMH = RES["canonical"]["w"], RES["canonical"]["lMH"]
b30 = (w > 30*10**-0.05) & (w < 30*10**0.05)
fx = float(np.mean(lMH[b30] < 7.5))
info(f"diagnosis of the w = 30 km/s point: {100*fx:.0f}% of the predicted sources there come from log M_HI < 7.5, "
     f"i.e. from EXTRAPOLATING the published Schechter function below where ALFALFA measures it")
w_t7, _, n_t7 = predict_widths(A0["canonical"], lmin=7.0, seed=2)
r30_ext = RES["canonical"]["row"][0][3]
r30_trc = phi_of(w_t7, 30., n_t7)/float(phi_W(math.log10(30)))
r50_trc = phi_of(w_t7, 50., n_t7)/float(phi_W(math.log10(50)))
info(f"  truncating the HIMF at log M_HI = 7.0 (ALFALFA's own floor) moves the w = 30 km/s prediction from "
     f"{RES['canonical']['row'][0][1]:.4f} to {phi_of(w_t7, 30., n_t7):.4f} Mpc^-3 dex^-1, i.e. from a ratio of "
     f"{r30_ext:.2f} to {r30_trc:.2f} -- from over-predicting to under-predicting")
info(f"  the same truncation moves w = 50 km/s only from {RES['canonical']['row'][1][3]:.2f} to {r50_trc:.2f}, so the "
     f"50-150 km/s comparison is NOT sensitive to where the mass function is stopped and the 30 km/s one is entirely so")
ck("32.2b AGAINST INTEREST, and against the item as posed: the bottom of the range the item asked about does not "
   "actually test the framework.  With the published Schechter extrapolated to 1e6 Msun the framework over-predicts the "
   "number of 30 km/s sources by a factor of 3; truncated at ALFALFA's own 1e7 floor it under-predicts them.  The answer "
   "at 30 km/s is set by where the mass function is stopped, not by a_0, so 'within errors at 30-100 km/s' is not "
   "established and cannot be with these ingredients",
   (r30_ext > 2.0) and (r30_trc < 1.0),
   f"w = 30 km/s: framework/observed = {r30_ext:.2f} with the Schechter extrapolated to 1e6, {r30_trc:.2f} truncated at "
   f"1e7; at w = 50 km/s the same two choices give {RES['canonical']['row'][1][3]:.2f} and {r50_trc:.2f}")
for wt in (0.0, 10.0, 30.0):
    ww, _, _ = predict_widths(A0["canonical"], w_turb=wt, seed=3)
    info(f"  turbulent FWHM {wt:4.0f} km/s: ratio at w = 30 is {phi_of(ww,30.)/float(phi_W(math.log10(30))):.2f}, "
         f"at w = 80 is {phi_of(ww,80.)/float(phi_W(math.log10(80))):.2f}")
for sc in (0.0, 0.40):
    ww, _, _ = predict_widths(A0["canonical"], scat=sc, seed=4)
    info(f"  M_b(M_HI) scatter {sc:.2f} dex: ratio at w = 50 is {phi_of(ww,50.)/float(phi_W(math.log10(50))):.2f}, "
         f"at w = 200 is {phi_of(ww,200.)/float(phi_W(math.log10(200))):.2f}")

# ------------------------------------------- what the amplitude test is REALLY measuring, stated against interest
P(""); P("  WHAT THE AMPLITUDE TEST IS AND IS NOT.  It is not independent evidence.  Mapping the HI mass function onto a")
P("  width function through w = 2 (G M_b a_0)^(1/4) sin i tests exactly one number -- the BTFR zero-point -- re-expressed")
P("  as number densities.  Measured directly on the same catalogue it is:")
inc_ok = (a["code"] == 1) & (a["pflag"] == 1) & (a["snr"] >= 6.5) & np.isfinite(a["ba"]) & np.isfinite(aMs) & (a["W50"] > 0) & (a["inc"] > 45)
vv = np.sqrt(np.maximum(a["W50"]**2 - W_TURB**2, 0.0))/(2*np.sin(np.radians(a["inc"])))
aMb_all = 1.33*10**a["logMHI"] + np.where(np.isfinite(aMs), 10**np.nan_to_num(aMs, nan=0.0), 0.0)
ZP = {}
for ft, a0 in A0.items():
    rr_ = np.log10(vv[inc_ok]/((G*aMb_all[inc_ok]*Msun*a0)**0.25/1e3))
    ZP[ft] = float(np.median(rr_[np.isfinite(rr_)]))
    info(f"  {ft:10}: median log(v_obs/v_pred) over {int(inc_ok.sum())} detected alpha.100 galaxies = {ZP[ft]:+.3f} dex")
info("  so the width function agreeing to ~0.1 dex in amplitude and the BTFR zero-point agreeing to ~0.01 dex in log v "
     "are THE SAME STATEMENT, not two.  Quote one of them, never both as independent.")
info("  and that zero-point is itself measured on DETECTED galaxies, which ALFALFA selects with a width-dependent "
     "limit (SNR ~ W50^(-1/2); see h31b_almost_dark_selection_audit.py).  That selection biases the detected zero-point "
     "LOW by roughly 0.06 dex at the observed scatter, so the true zero-point is slightly HIGHER than measured and the "
     "framework's predicted width function should sit slightly to the RIGHT of the one computed above -- which would "
     "reduce the 50 km/s over-prediction and deepen the 200 km/s under-prediction.  Not corrected for here; flagged.")
ck("32.2a3 the item's independent content is therefore the SHAPE and the LambdaCDM comparison, not the amplitude.  "
   "This check records that the amplitude agreement and the BTFR zero-point are one number: they must agree, and if "
   "they did not, the calculation would be wrong",
   abs(ZP["canonical"]) < 0.05,
   f"BTFR zero-point {ZP['canonical']:+.3f} (canonical) / {ZP['alt']:+.3f} (alt) dex in log v, i.e. "
   f"{4*ZP['canonical']:+.3f} dex in mass -- the same information as the amplitude ratios above")

# the shape, fitted the way the paper fits it
P("")
lwf = np.log10(np.logspace(math.log10(25), math.log10(500), 26))
def msf(lw, lphi, ws, al, be):
    x = 10**lw/ws; return np.log10(LN10*10**lphi*x**al*np.exp(-x**be))
yy = np.array([math.log10(max(phi_of(RES["canonical"]["w"], 10**x), 1e-8)) for x in lwf])
try:
    pf, _ = curve_fit(msf, lwf, yy, p0=[-1.7, 300., -0.6, 2.0], maxfev=40000)
    info(f"fitting the SAME modified Schechter form to the framework's predicted width function over 25-500 km/s gives "
         f"log phi* = {pf[0]:+.2f}, w* = {pf[1]:.0f} km/s, alpha = {pf[2]:+.2f}, beta = {pf[3]:.2f}")
except Exception as e:
    pf = [np.nan]*4; info(f"modified-Schechter fit failed: {e}")
info(f"the published alpha.100 values are log phi* = {WF['lphi']:+.2f}, w* = {WF['ws']:.0f} km/s, "
     f"alpha = {WF['al']:+.2f} (+{WF_AL_ERR[0]:.2f}/-{WF_AL_ERR[1]:.2f}), beta = {WF['be']:.1f}")
sl_pred = RES["canonical"]["slope"]
al_fit = float(pf[2])
n_sig = (al_fit - WF["al"])/WF_AL_ERR[1]                     # the difference is negative, so the minus error applies
n_sig_c = (al_fit - WFc["al"])/0.16
info(f"the framework's ANALYTIC low-width slope is 4(alpha_HI + 1)/(d log M_b/d log M_HI) = "
     f"4 x {MF['al']+1:+.2f}/{AB:.2f} = {4*(MF['al']+1)/AB:+.2f}, which is {(4*(MF['al']+1)/AB - WF['al'])/WF_AL_ERR[1]:+.1f} sigma "
     f"from the published value on the all-statistical error bar")
info(f"the like-for-like number is the FITTED alpha = {al_fit:+.2f} (same functional form, same width range as the paper); "
     f"the raw Monte-Carlo 30-100 km/s log-slope is {sl_pred:+.2f}, steeper still because the turbulence floor piles "
     f"sources up near 20-30 km/s")
ck("32.2c AGAINST INTEREST, the shape: the framework predicts a STEEPER low-width slope than ALFALFA measures, on every "
   "way of reading it.  Fitting the paper's own functional form to the framework's predicted width function gives alpha "
   "= -1.26 against the published -0.63: a 1.5 sigma tension on the published all-statistical error bar and a 4 sigma one "
   "on its counting-only error bar.  This check asserts the TENSION and would fail if the slopes agreed",
   (al_fit < WF["al"]) and (abs(n_sig_c) > 2.0),
   f"fitted {al_fit:+.2f} vs published {WF['al']:+.2f} (+{WF_AL_ERR[0]:.2f}/-{WF_AL_ERR[1]:.2f}) = {n_sig:+.1f} sigma all-stat, "
   f"and vs {WFc['al']:+.2f} +- 0.16 counting-only = {n_sig_c:+.1f} sigma; analytic value {4*(MF['al']+1)/AB:+.2f}, "
   f"raw 30-100 km/s slope {sl_pred:+.2f}")
info("the likeliest explanation is NOT a_0: it is that a 50% line width is not a flat rotation speed, and the mapping "
     "between them is mass dependent.  Fits of the BTFR with W50 give a slope near 3.3 where fits with V_flat give 4 "
     "(Bradford+16; Lelli+16; Ponomareva+18).  A slope of 3.3 instead of 4 is exactly a shallower velocity function, and "
     "the framework has no way to distinguish itself from that systematic using widths alone.")

# ---------------------------------------------------------------- 3. the alternative
P(""); P("-"*118); P("3. THE ALTERNATIVE COMPUTED BESIDE IT: LambdaCDM's halo velocity function"); P("-"*118)
Om, Ob, ns, s8 = OM_M, OM_B, 0.9649, 0.8111
rho_m = 2.775e11*Om*h**2                                   # Msun/Mpc^3, comoving
def T_EH(k):                                               # Eisenstein & Hu 1998, no-wiggle shape
    om = Om*h*h; ob = Ob*h*h; fb = ob/om; th = 2.7255/2.7
    s = 44.5*math.log(9.83/om)/math.sqrt(1 + 10*ob**0.75)
    ag = 1 - 0.328*math.log(431*om)*fb + 0.38*math.log(22.3*om)*fb*fb
    Gam = Om*h*(ag + (1 - ag)/(1 + (0.43*k*s)**4)); q = k*th*th/Gam/h
    L = np.log(2*math.e + 1.8*q); C = 14.2 + 731/(1 + 62.5*q); return L/(L + C*q*q)
def Wtop(x): return 3*(np.sin(x) - x*np.cos(x))/x**3
def sig2(R, A=1.0):
    f = lambda lk: np.exp(lk)**(3+ns)*T_EH(np.exp(lk))**2*Wtop(np.exp(lk)*R)**2/(2*math.pi**2)
    return A*quad(f, math.log(1e-4), math.log(1e3), limit=200)[0]
ANORM = s8**2/sig2(8.0/h)
sigM = lambda M: math.sqrt(sig2((3*M/(4*math.pi*rho_m))**(1/3.), ANORM))
def dndlogM(M):                                            # Sheth-Tormen
    dl = 1e-3; dln = (math.log(sigM(M*10**(dl/2))) - math.log(sigM(M*10**(-dl/2))))/dl
    nu_ = 1.686/sigM(M); Aq, aa, pp = 0.3222, 0.707, 0.3
    return Aq*math.sqrt(2*aa/math.pi)*(1 + (aa*nu_*nu_)**(-pp))*nu_*math.exp(-aa*nu_*nu_/2)*(rho_m/M)*(-dln)
def vmax_of(M):                                            # NFW, Dutton & Maccio 2014 c(M) at z = 0
    R200 = (3*M*Msun/(4*math.pi*200*rho_crit))**(1/3.); V200 = math.sqrt(G*M*Msun/R200)/1e3
    c = 10**(0.905 - 0.101*math.log10(M*h/1e12))
    return V200*math.sqrt(0.2162*c/(math.log(1+c) - c/(1+c)))
lMh = np.arange(7.5, 15.01, 0.05)
vmh = np.array([vmax_of(10**x) for x in lMh]); nnh = np.array([dndlogM(10**x) for x in lMh])
n14 = float(np.trapz(nnh[lMh >= 14], lMh[lMh >= 14]))
ck("32.3a the LambdaCDM side is validated before it is used: the Sheth-Tormen mass function built here from an "
   "Eisenstein-Hu transfer function normalised to sigma_8 = 0.811 gives a cluster abundance n(> 1e14 Msun) of the "
   "right size, and a low-mass logarithmic slope of -0.9 as it must",
   1e-6 < n14 < 1e-4, f"n(> 1e14) = {n14:.2e} Mpc^-3 (literature ~1e-5); d log n/d log M at 1e10 = "
   f"{(math.log10(dndlogM(10**10.1))-math.log10(dndlogM(10**9.9)))/0.2:.2f}; V_max(1e10) = {vmax_of(1e10):.1f} km/s")
phiV = nnh/np.gradient(np.log10(vmh), lMh)
NH = 600000
# BUG FIX (found in audit): halos must be sampled from dn/dlogM over the UNIFORM lMh grid, i.e. proportional to nnh.
# Sampling proportional to phiV = nnh/(dlogV/dlogM) -- as an earlier version did -- re-weights by the local slope of
# the V_max(M) relation.  That slope is nearly constant (1/3 minus a slow concentration term), so the error was ~2%,
# but it was an error; the total normalisation is unchanged because int phiV dlogV == int nnh dlogM.
ph = nnh/nnh.sum(); rr = np.random.default_rng(77)
drw = rr.choice(lMh, size=NH, p=ph); NORMH = float(np.trapz(nnh, lMh))/NH
Vh = np.interp(drw, lMh, vmh); wh = 2*Vh*np.sin(np.arccos(rr.uniform(0, 1, NH)))
FAC = {}
for w0 in WPTS:
    b = (wh > w0*10**-0.05) & (wh < w0*10**0.05); phw = b.sum()*NORMH/0.1
    ob = float(phi_W(math.log10(w0))); FAC[w0] = phw/ob
    info(f"w50 = {w0:5.0f} km/s: LambdaCDM halo width function {phw:.4f} vs observed {ob:.4f} Mpc^-3 dex^-1 "
         f"-> LambdaCDM over by {phw/ob:5.1f} x   (framework over by {RES['canonical']['row'][WPTS.index(w0)][3]:.2f} x)")
ck("32.3b the classic result is reproduced from scratch: mapping the LambdaCDM halo velocity function to HI widths the "
   "naive way overshoots the measured ALFALFA width function by an order of magnitude at 50 km/s -- Papastergis+2011 "
   "report a factor ~8 there and ~100 extrapolated to 20 km/s, and this independent calculation gives the same",
   4 < FAC[50.] < 25, f"LambdaCDM/observed = {FAC[30.]:.0f} x at w = 30, {FAC[50.]:.0f} x at 50, {FAC[80.]:.1f} x at 80, "
   f"{FAC[200.]:.2f} x at 200")
adv = FAC[50.]/RES["canonical"]["row"][1][3]
ck("32.3c (the item's actual content, and it is a WORKS) the framework has NO velocity-function problem, because it has "
   "no halo velocity function: the observed width function IS its baryonic mass function stretched by v ~ M_b^(1/4).  At "
   "50 km/s the framework misses by a factor of 1.7 where LambdaCDM's halo function misses by 11, and at 30 km/s by 3 "
   "where LambdaCDM misses by 35 -- one order of magnitude closer at both.  This is not a fit: a_0 is fixed by Lambda "
   "and every other ingredient is measured",
   adv > 4, f"framework is {adv:.1f} x closer than the LambdaCDM halo function at w = 50 km/s and "
   f"{FAC[30.]/RES['canonical']['row'][0][3]:.1f} x closer at w = 30")
info("both ways, and this is the standard LambdaCDM answer: the halo-to-width mapping used above is the naive one.  Real "
     "HI discs in small halos do not reach V_max, and low-mass halos may host no detectable HI at all -- either escape "
     "removes the excess.  What cannot be arranged away is that the framework needs neither escape.")

# ---------------------------------------------------------------- 4. an independent 1/V_max cross-check
P(""); P("-"*118); P("4. INDEPENDENT CROSS-CHECK -- building both functions from alpha.100 with one 1/V_max estimator")
P("-"*118)
OMEGA = 6900*(math.pi/180)**2; SNRLIM, DMAX, DMIN = 6.5, 250.0, 2.0
sel = (a["code"] == 1) & (a["dist"] > DMIN) & (a["dist"] < DMAX) & np.isfinite(a["logMHI"]) & (a["snr"] >= SNRLIM) & (a["W50"] > 0)
dlim = np.minimum(a["dist"]*np.sqrt(a["snr"]/SNRLIM), DMAX)
wvm = 1.0/((OMEGA/3.0)*(dlim**3 - DMIN**3))
bb = np.arange(6.0, 11.2, 0.2); cc = 0.5*(bb[1:] + bb[:-1])
hh, _ = np.histogram(a["logMHI"][sel], bins=bb, weights=wvm[sel]); nn_, _ = np.histogram(a["logMHI"][sel], bins=bb)
mine = hh/0.2
u = (cc > 7.4) & (cc < 8.8) & (nn_ > 20)
al_mine = np.polyfit(cc[u], np.log10(mine[u]), 1)[0] - 1.0
mid_ = (cc > 8.9) & (cc < 10.3) & (nn_ > 20)
rat_mid = float(np.median(mine[mid_]/phi_M(cc[mid_])))
info(f"my 1/V_max HIMF vs the published one: median ratio {rat_mid:.2f} over log M_HI = 8.9-10.3, "
     f"but the faint-end slope comes out alpha = {al_mine:.2f} against the published {MF['al']:+.2f}")
ck("32.4 AGAINST MY OWN ESTIMATOR: a 1/V_max mass function built here from the same catalogue matches the published one "
   "in the middle but is far too steep at the faint end -- the known large-scale-structure bias of 1/V_max, which is "
   "exactly why the published 2D-stepwise functions were used for the test above and not this.  If section 2 had been "
   "run on my own 1/V_max the framework's predicted slope would have been {:.1f}, spuriously".format(4*(al_mine+1)/AB),
   abs(al_mine - MF["al"]) > 0.15,
   f"my alpha = {al_mine:.2f} vs published {MF['al']:.2f}; middle-decade amplitude ratio {rat_mid:.2f}")

# ---------------------------------------------------------------- 5. mutations
P(""); P("-"*118); P("5. MUTATION CONTROLS"); P("-"*118)
w4, _, _ = predict_widths(4*A0["canonical"], seed=9)
rot = lambda ww: np.sqrt(np.maximum(ww**2 - W_TURB**2, 0.0))          # strip the turbulence floor: this is 2 v sin i
shift = math.log10(np.median(rot(w4))/np.median(rot(RES["canonical"]["w"])))
shift_obs = math.log10(np.median(w4[w4 > 100])/np.median(RES["canonical"]["w"][RES["canonical"]["w"] > 100]))
ck("M32a mutation: a_0 raised by 4x must slide the predicted ROTATIONAL widths by exactly 0.25 log10(4) = +0.151 dex, "
   "and it does -- so the amplitude comparison in section 2 really is an a_0 measurement and not a shape coincidence.  "
   "(On the raw widths the shift is diluted to about +0.10 dex by the 20 km/s turbulence floor, which is itself a "
   "reminder that the narrow end of this test is floor-dominated)",
   abs(shift - 0.25*math.log10(4)) < 0.01,
   f"rotational widths move {shift:+.4f} dex against the exact +{0.25*math.log10(4):.4f}; raw widths above 100 km/s move "
   f"{shift_obs:+.4f} dex; raw widths overall move "
   f"{math.log10(np.median(w4)/np.median(RES['canonical']['w'])):+.4f}")
r4 = phi_of(w4, 50.)/float(phi_W(math.log10(50)))
info(f"  and it costs accuracy: at w = 50 km/s the 4a_0 mutation gives a ratio of {r4:.2f} against the framework's "
     f"{RES['canonical']['row'][1][3]:.2f}")
lflat = np.linspace(LMIN, LMAX, 4000)
pf_flat = np.ones_like(lflat)/len(lflat)
rr2 = np.random.default_rng(11)
lMH_f = rr2.choice(lflat, size=NMC, p=pf_flat)
v_f = (G*10**(AB*lMH_f + BB)*Msun*A0["canonical"])**0.25/1e3
w_f = np.sqrt((2*v_f*np.sin(np.arccos(rr2.uniform(0, 1, NMC))))**2 + W_TURB**2)
cnt = lambda ww, w0: max(int((np.abs(np.log10(ww/w0)) < 0.05).sum()), 1)
sl_flat = (math.log10(cnt(w_f, 100.)) - math.log10(cnt(w_f, 30.)))/(math.log10(100) - math.log10(30))
ck("M32b mutation: replacing the measured HI mass function with a FLAT one changes the predicted low-width slope by more "
   "than a full unit -- so section 2 is testing the mass function's SHAPE carried through the framework's map, not an "
   "insensitive integral that any input would satisfy",
   abs(sl_flat - sl_pred) > 0.5,
   f"flat input gives a 30-100 km/s log-slope of {sl_flat:+.2f} against the framework's {sl_pred:+.2f} "
   f"and the observed {WF['al']:+.2f}")

P(""); P("="*118); P("VERDICT -- ITEM 32: a partial pass, and the strongest thing in it is the comparison, not the fit")
P("="*118)
P(f"  The framework converts the published ALFALFA HI mass function into the published ALFALFA HI width function with")
P(f"  ZERO free parameters -- a_0 from Lambda, the baryon correction and the inclination distribution both measured -- and")
P(f"  lands within a factor {min(x[3] for x in RES['canonical']['row'][1:4]):.2f}-{max(x[3] for x in RES['canonical']['row'][1:4]):.2f} over w50 = 50-150 km/s, against an irreducible {abs(math.log10(nM/nW)):.2f} dex floor set by the two")
P(f"  published fits' own mutual normalisation.  It is INSIDE that floor at 80 and 120 km/s and outside it at 50 km/s,")
P(f"  where it over-predicts by {d50:+.2f} dex -- a real miss, not a rounding.")
P(f"  AND THE AMPLITUDE IS NOT INDEPENDENT EVIDENCE: it is the BTFR zero-point ({ZP['canonical']:+.3f} dex in log v on the same")
P(f"  catalogue) re-expressed as number densities.  The independent content of this item is the SHAPE and the LambdaCDM")
P(f"  comparison.  The zero-point is itself measured on width-selected detections, which biases it low (see h31b).")
P(f"  At 30 km/s it over-predicts by {r30_ext:.1f} x with the Schechter extrapolated to 1e6")
P(f"  and UNDER-predicts by {r30_trc:.2f} x truncated at ALFALFA's own 1e7 floor, so the item's 'within errors at 30-100 km/s'")
P(f"  is not established at the bottom end -- and that point is set by where the mass function stops, not by a_0.")
P(f"  The predicted low-width slope, {al_fit:+.2f} fitted the paper's own way ({4*(MF['al']+1)/AB:+.2f} analytically), is steeper than the")
P(f"  measured {WF['al']:+.2f}; that is a real tension of 1.5 to 4 sigma depending on which published error bar is used, and the honest")
P(f"  reading is the velocity-definition systematic (W50 vs V_flat gives BTFR slopes 3.3 vs 4), not a_0.")
P(f"  What is NOT ambiguous is the alternative computed beside it.  LambdaCDM's halo velocity function, built here from")
P(f"  scratch and validated on the cluster abundance, overshoots the same measured width function by {FAC[50.]:.0f} x at 50 km/s and")
P(f"  {FAC[30.]:.0f} x at 30 -- the known 'velocity function problem', reproduced independently.  The framework is an order of")
P(f"  magnitude closer at both, and it is closer WITHOUT a halo occupation function, a V_max-to-W50 correction, or any")
P(f"  free parameter.  Recorded as a WORKS on the comparison and a partial miss on the absolute shape.")
P(f"")
P(f"  Two corrections made in audit, both stated rather than buried:")
P(f"   * the LambdaCDM halos were being drawn with weights proportional to dn/dlogV over a uniform log-MASS grid, which")
P(f"     re-weights by the local slope of V_max(M).  Fixed to dn/dlogM.  The slope is nearly constant so the error was")
P(f"     about 1% -- it moved the 50 km/s excess from 11.1x to {FAC[50.]:.1f}x -- but it was an error.")
P(f"   * check 32.2a originally compared the 50-120 km/s ratios against a hand-picked factor of 1.8 while the worst was")
P(f"     1.69.  That threshold was doing work it had not earned; it is now compared against the 0.125 dex floor that")
P(f"     check 32.0 measures from the two published fits BEFORE any framework number is computed, and on that footing")
P(f"     the 50 km/s point FAILS and is reported as a miss.")
P(f"  Literature inputs verified this session against Oman 2022 MNRAS 509, 3268 Table 1: the alpha.100 HIMF")
P(f"  (log phi* = -2.26, log M* = 9.92, alpha = -1.29) and HIWF (log phi* = -1.67, w* = 307, alpha = -0.63, beta = 2.0,")
P(f"  all-statistical; 300/-0.56/2.1 counting-only) and the 21827-source sample size all match the published values.")
sys.exit(ck.done())
