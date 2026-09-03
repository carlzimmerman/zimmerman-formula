#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
h31_almost_dark_btfr.py -- HUNT ITEM 31: almost-dark HI galaxies on the BTFR.
=============================================================================
The item as posed: gas-only systems have M_b = 1.33 M_HI with NO stellar mass-to-light ratio in it, so the deep-MOND
relation v^4 = G M_b a_0 becomes a ZERO-PARAMETER prediction and the BTFR zero-point (hence a_0) can be read off without
the Upsilon systematic that the first five passes of this hunt identified as the blocker of the whole programme.
"Kepler-grade if 20+ objects on the line, scatter <= 0.1 dex."

Sample: the 115 HI-bearing ultra-diffuse ALFALFA galaxies of Leisman+2017 (ApJ 842, 133; VizieR J/ApJ/842/133), the
        ALFALFA "almost darks" -- selected to be isolated, with mu_g,0 > 24 mag/arcsec^2 and M_HI/M_star ~ 10.
        Cross-matched (115/115) to the ALFALFA-SDSS value-added catalogue (Durbala+2020, AJ 160, 271; J/AJ/160/271)
        for the SDSS r-band axis ratio b/a and two independent stellar masses.  Both tables fetched this session.
Control: the same estimator run on 10^4 ordinary ALFALFA galaxies (alpha.100, Haynes+2018, J/ApJ/861/49) merged with the
        same SDSS catalogue -- if the estimator is biased, the control shows it, and any HUD offset must be measured
        DIFFERENTIALLY against the control at matched baryonic mass.

REPORT AGAINST INTEREST.  This item is a known kill-in-waiting: Mancera Pina+2019/2020 put gas-rich UDGs off the BTFR and
Mancera Pina+2022 (MNRAS 512, 3230) resolved AGC 114905 -- one of these very objects -- and stated that its rotation curve
"deviates strongly from the predictions of Modified Newtonian dynamics".  The job here is to measure the size of that
deficit on the framework's own footings, to check it against the published resolved case, and to test every escape
(finite HI radius, the external-field effect, the inclination) quantitatively rather than rhetorically.

Both footings.  Mutation controls.  Checks CAN fail.

*** SUPERSEDED IN PART -- READ h31b_almost_dark_selection_audit.py BEFORE QUOTING ANY NUMBER FROM THIS FILE. ***
The measurements below are correct and reproduce exactly in the audit, but their INTERPRETATION does not survive it.
This script's control is matched on baryonic mass alone, and ALFALFA's sensitivity falls as W50^(-1/2), so a wide
line is harder to detect than a narrow one at the same HI mass.  The control galaxies here are nearer (65 vs 79 Mpc)
and brighter (SNR 9.4 vs 8.2) than the almost-darks, so they are far less bitten by that width selection, and the
-0.265 dex "differential" is mostly the difference in detectability rather than a property of the almost-darks.
Matched instead on the detection ceiling W_max = (1000 F/(6.5 rms))^2/20 -- flux and noise only, no width in it, so
not a collider -- ordinary ALFALFA galaxies of the same mass, HI mass and inclination sit at -0.207 dex and the
almost-dark differential is -0.089 +- 0.033 dex, not -0.265.  THE "9.5 SIGMA LIABILITY" BELOW MUST NOT BE QUOTED.
Item 31's standing verdict is a NULL.
"""
import sys, math
import numpy as np
from scipy import stats
from hunt_lib import *
ck = Check(); rng = np.random.default_rng(31)

# ------------------------------------------------------------------ shared estimator
W_TURB = 20.0                     # km/s, FWHM of the turbulent broadening removed in quadrature (sigma_HI ~ 8.5 km/s)
def v_from_width(W50, inc_deg, w_turb=W_TURB):
    """Deprojected rotation speed from the ALFALFA 50% width: W_rot^2 = W50^2 - w_turb^2, v = W_rot/(2 sin i)."""
    Wr = np.sqrt(np.maximum(np.asarray(W50, float)**2 - w_turb**2, 0.0))
    s = np.sin(np.radians(np.asarray(inc_deg, float)))
    with np.errstate(divide="ignore", invalid="ignore"):
        return np.where(s > 0, Wr/(2*s), np.nan)
def v_btfr(Mb_msun, a0):
    """The framework's deep-MOND asymptote, km/s.  No free parameter once a_0 is fixed."""
    return (G*np.asarray(Mb_msun, float)*Msun*a0)**0.25/1e3
def med_ci(x, n=2000):
    x = np.asarray(x, float); x = x[np.isfinite(x)]
    if len(x) < 3: return np.nan, np.nan
    bs = np.array([np.median(rng.choice(x, len(x))) for _ in range(n)])
    return float(np.median(x)), float(bs.std())

P("="*118); P("ITEM 31 -- almost-dark (HI-bearing ultra-diffuse) ALFALFA galaxies on the baryonic Tully-Fisher relation")
P("="*118)
h = load_huds()
Ms = np.where(np.isfinite(h["logMsM"]), h["logMsM"], h["logMsT"])
nM = np.isfinite(Ms).sum()
Mgas = 1.33*10**h["logMHI"]
Mb = Mgas + np.where(np.isfinite(Ms), 10**np.nan_to_num(Ms, nan=0.0), 0.0)
info(f"Leisman+2017 HUDs: N = {len(Mb)} ({(h['sset']=='R').sum()} restrictive, {(h['sset']=='B').sum()} broad); "
     f"SDSS b/a for {np.isfinite(h['ba']).sum()}, stellar mass for {nM}")
info(f"log M_HI median {np.median(h['logMHI']):.2f} [{h['logMHI'].min():.2f}, {h['logMHI'].max():.2f}]; "
     f"W50 median {np.median(h['W50']):.0f} km/s [{h['W50'].min():.0f}, {h['W50'].max():.0f}]; "
     f"distance median {np.median(h['dist']):.0f} Mpc")

# ---------------------------------------------------------------- 0. the item's own premise: is Upsilon irrelevant?
gas_frac = Mgas/Mb
info(f"gas share of the baryons M_gas/M_b: median {np.median(gas_frac):.3f}, 10th percentile {np.percentile(gas_frac,10):.3f}")
Mstar = np.where(np.isfinite(Ms), 10**np.nan_to_num(Ms, nan=0.0), 0.0)
ups_shift = 0.25*float(np.median(np.log10((Mgas + 2*Mstar)/Mb)))
ck("31.0 the item's PREMISE holds: these systems are gas-dominated, so the stellar mass-to-light ratio -- the systematic "
   "that five previous passes named as the blocker of this whole hunt -- drops out.  DOUBLING every stellar mass moves the "
   "predicted rotation speed by under 0.02 dex",
   abs(ups_shift) < 0.02, f"M_gas/M_b median {np.median(gas_frac):.3f}; doubling M_star moves log v_pred by {ups_shift:+.4f} dex")

# ---------------------------------------------------------------- 1. the estimator's CONTROL on ordinary galaxies
P(""); P("-"*118); P("1. THE CONTROL -- the same estimator on ordinary ALFALFA galaxies (this is what makes the result differential)")
P("-"*118)
a = load_alfalfa()
aMs = np.where(np.isfinite(a["logMsM"]), a["logMsM"], a["logMsT"])
aMb = 1.33*10**a["logMHI"] + np.where(np.isfinite(aMs), 10**np.nan_to_num(aMs, nan=0.0), 0.0)
base = (a["code"] == 1) & (a["pflag"] == 1) & (a["snr"] >= 6.5) & np.isfinite(a["ba"]) & np.isfinite(aMs) & (a["W50"] > 0)
info(f"alpha.100 x ALFALFA-SDSS, code-1 detections with clean photometry and SNR >= 6.5: N = {base.sum()}")
frac45 = (base & (a["inc"] > 45)).sum()/base.sum()
ck("31.1a the SDSS axis ratios of the control sample are consistent with RANDOM disc orientation -- the fraction with "
   "i > 45 deg is cos(45 deg) to better than 1% -- so the inclinations used below are not obviously broken",
   abs(frac45 - math.cos(math.radians(45))) < 0.02, f"f(i>45) = {frac45:.4f} vs cos 45 = {math.cos(math.radians(45)):.4f}")
av = v_from_width(a["W50"], a["inc"])
ctrl = base & (a["inc"] > 45) & np.isfinite(av) & (av > 0)
R1 = {}
for ft, a0 in A0.items():
    r = np.log10(av[ctrl]/v_btfr(aMb[ctrl], a0))
    m, e = med_ci(r)
    R1[ft] = (m, e, r.std())
    info(f"control, all masses, {ft:10}: median log(v_obs/v_pred) = {m:+.3f} +- {e:.3f} (bootstrap), scatter {r.std():.3f} dex, N = {ctrl.sum()}")
lo, hi = float(np.log10(Mb.min())), float(np.log10(Mb.max()))
mm = ctrl & (np.log10(aMb) >= lo) & (np.log10(aMb) <= hi)
CTRL = {}
for ft, a0 in A0.items():
    r = np.log10(av[mm]/v_btfr(aMb[mm], a0)); m, e = med_ci(r); CTRL[ft] = (m, e, r.std(), int(mm.sum()))
    info(f"control MASS-MATCHED to the HUDs (log M_b in [{lo:.2f}, {hi:.2f}]), {ft:10}: median {m:+.3f} +- {e:.3f}, scatter {r.std():.3f}, N = {mm.sum()}")
ck("31.1b (this is the check that licenses the rest) the estimator -- ALFALFA W50, turbulence removed in quadrature, "
   "deprojected with an SDSS axis-ratio inclination -- puts ORDINARY gas-rich galaxies on the framework's zero-parameter "
   "BTFR with no offset worth the name, on both footings.  So a HUD offset measured against this control is not the "
   "estimator's fault",
   abs(R1["canonical"][0]) < 0.06 and abs(R1["alt"][0]) < 0.06,
   f"all-mass control: canonical {R1['canonical'][0]:+.3f} +- {R1['canonical'][1]:.3f}, alt {R1['alt'][0]:+.3f} +- {R1['alt'][1]:.3f} dex in log v")

# ---------------------------------------------------------------- 2. the HUDs
P(""); P("-"*118); P("2. THE RESULT -- where the almost-darks actually sit"); P("-"*118)
hv = v_from_width(h["W50"], h["inc"])
ok = np.isfinite(hv) & (hv > 0) & np.isfinite(Mb)
info(f"{ok.sum()}/{len(Mb)} HUDs have a usable inclination and width")
HUD = {}
for ft, a0 in A0.items():
    vp = v_btfr(Mb, a0)
    r = np.log10(hv[ok]/vp[ok]); m, e = med_ci(r)
    HUD[ft] = (m, e, r.std())
    dif = m - CTRL[ft][0]; dife = math.hypot(e, CTRL[ft][1])
    info(f"{ft:10}: v_pred median {np.median(vp):.1f} km/s, v_obs median {np.median(hv[ok]):.1f} km/s; "
         f"median log(v_obs/v_pred) = {m:+.3f} +- {e:.3f} (scatter {r.std():.3f}); "
         f"DIFFERENTIAL vs the mass-matched control = {dif:+.3f} +- {dife:.3f} dex ({dif/dife:+.1f} sigma), "
         f"i.e. {4*dif:+.2f} dex in baryonic mass")
    if ft == "canonical": DIF = (dif, dife)
for s in ("R", "B"):
    m_ = ok & (h["sset"] == s)
    if m_.sum() > 5:
        r = np.log10(hv[m_]/v_btfr(Mb, A0["canonical"])[m_]); mm_, ee_ = med_ci(r)
        info(f"  Leisman '{s}' subsample (N = {m_.sum()}): median {mm_:+.3f} +- {ee_:.3f} dex")
hi45 = ok & (h["inc"] > 45)
r = np.log10(hv[hi45]/v_btfr(Mb, A0["canonical"])[hi45]); m45, e45 = med_ci(r)
info(f"  HUDs with i > 45 deg only (N = {hi45.sum()}, the sub-sample least sensitive to the inclination): median {m45:+.3f} +- {e45:.3f} dex")
for wt in (0.0, 10.0, 30.0):
    with np.errstate(divide="ignore", invalid="ignore"):
        r = np.log10(v_from_width(h["W50"], h["inc"], wt)[ok]/v_btfr(Mb, A0["canonical"])[ok])
    info(f"  turbulence FWHM removed = {wt:4.0f} km/s: median {np.nanmedian(r[np.isfinite(r)]):+.3f} dex "
         f"(fiducial {W_TURB:.0f} km/s gives {HUD['canonical'][0]:+.3f})")
sp = stats.spearmanr(np.log10(Mb[ok]), np.log10(hv[ok]))
sl_h = np.polyfit(np.log10(hv[ok]), np.log10(Mb[ok]), 1)[0]
info(f"and AGAINST INTEREST a second time: within the HUD sample itself the baryonic mass and the rotation speed do "
     f"correlate (Spearman r = {sp.statistic:.2f}, p = {sp.pvalue:.1e}) but with a BTFR slope of {sl_h:.2f}, nowhere near "
     f"the framework's 4, over a mass range of only {np.percentile(np.log10(Mb[ok]),95)-np.percentile(np.log10(Mb[ok]),5):.1f} dex -- "
     f"so this sample constrains the BTFR ZERO-POINT and has almost no leverage on its slope")
ck("31.2 (a LIABILITY, reported against interest) the almost-dark galaxies do NOT lie on the framework's BTFR.  Measured "
   "with the estimator that the control shows is unbiased, they sit BELOW the zero-parameter prediction by about a quarter "
   "of a dex in rotation speed -- a factor of ~3 in baryonic mass -- and the deficit is significant against the "
   "mass-matched control of ordinary galaxies.  The item's Kepler-grade criterion (20+ objects on the line, scatter "
   "<= 0.1 dex) is not met and is not close.  This check asserts the DEFICIT, so it fails if the almost-darks are in fact "
   "on the line",
   (DIF[0] < -0.10) and (DIF[0]/DIF[1] < -3.0) and (HUD["canonical"][2] > 0.1),
   f"canonical {HUD['canonical'][0]:+.3f} +- {HUD['canonical'][1]:.3f}, alt {HUD['alt'][0]:+.3f} +- {HUD['alt'][1]:.3f} dex in log v; "
          f"differential vs control {DIF[0]:+.3f} +- {DIF[1]:.3f} dex = {DIF[0]/DIF[1]:+.1f} sigma; scatter {HUD['canonical'][2]:.3f} dex, not 0.1")

# ---------------------------------------------------------------- 3. the resolved anchor
P(""); P("-"*118); P("3. THE RESOLVED ANCHOR -- does this pipeline reproduce the one object with published interferometric kinematics?")
P("-"*118)
i_ag = list(h["agc"]).index("114905")
MHI_vla, Mst_vla = 9.7e8, 1.3e8                    # Mancera Pina+2022, VLA flux and SED fit
Mb_vla = 1.33*MHI_vla + Mst_vla
info(f"AGC 114905 (Mancera Pina+2022, MNRAS 512, 3230): M_HI = {MHI_vla:.2e}, M_star = {Mst_vla:.2e}, "
     f"M_bar = {Mb_vla:.2e} Msun; resolved HI inclination i = 32 +- 3 deg; flat rotation speed V_c ~ 23 km/s")
info(f"  this catalogue's entries for the same object: log M_HI = {h['logMHI'][i_ag]:.2f} (ALFALFA flux), "
     f"W50 = {h['W50'][i_ag]:.0f} km/s, SDSS b/a = {h['ba'][i_ag]:.2f} -> optical i = {h['inc'][i_ag]:.0f} deg "
     f"(the paper quotes an optical inclination 'around 45 deg' and does not use it)")
Vlos = 23.0*math.sin(math.radians(32.0))           # the line-of-sight projected amplitude is inclination-free
for ft, a0 in A0.items():
    vpv = v_btfr(Mb_vla, a0)
    i_req = math.degrees(math.asin(min(1.0, Vlos/vpv)))
    info(f"  {ft:10}: framework predicts V_flat = {vpv:.1f} km/s; matching the measured projected amplitude "
         f"{Vlos:.1f} km/s needs i = {i_req:.1f} deg")
vp_mond = v_btfr(Mb_vla, 1.2e-10); i_mond = math.degrees(math.asin(min(1.0, Vlos/vp_mond)))
ck("31.3 the pipeline is anchored: run on the ONE almost-dark galaxy with published resolved HI kinematics and with the "
   "standard MOND a_0 = 1.2e-10, it returns the inclination that the published paper says MOND requires (10.8 +- 0.3 deg) "
   "to within a degree -- so the deficit measured above is the same one the interferometry found, not an artefact here",
   abs(i_mond - 10.8) < 1.5, f"this pipeline needs i = {i_mond:.1f} deg at a_0 = 1.2e-10; Mancera Pina+2022 report 10.8 +- 0.3 deg "
                             f"(and measure 32 +- 3 deg); on the framework's footings {math.degrees(math.asin(min(1.0,Vlos/v_btfr(Mb_vla,A0['canonical'])))):.1f} deg "
                             f"(canonical) / {math.degrees(math.asin(min(1.0,Vlos/v_btfr(Mb_vla,A0['alt'])))):.1f} deg (alt)")

# ---------------------------------------------------------------- 4. the three escapes, priced
P(""); P("-"*118); P("4. THE ESCAPES, PRICED"); P("-"*118)
# (a) the HI disc does not reach the flat part
logD = 0.506*h["logMHI"] - 3.293                   # Wang+2016 MNRAS 460, 2143: HI size-mass relation, 0.06 dex scatter
R_HI = 0.5*10**logD                                # kpc, radius at Sigma_HI = 1 Msun/pc^2
info(f"HI radii from the Wang+2016 size-mass relation: median R_HI = {np.median(R_HI):.1f} kpc "
     f"(median optical half-light radius in this sample is {np.median(h['rh']):.1f} kpc)")
for ft, a0 in A0.items():
    gN = G*Mb*Msun/(R_HI*kpc)**2
    vR = np.sqrt(nu(gN/a0)*gN*(R_HI*kpc))/1e3      # Route A kernel evaluated AT the HI edge, not at infinity
    rat = float(np.median(np.log10(vR/v_btfr(Mb, a0))))
    if ft == "canonical": R_EDGE = rat
    info(f"  {ft:10}: median g_bar(R_HI)/a_0 = {np.median(gN/a0):.3f}; the kernel at R_HI gives "
         f"{np.median(vR):.1f} km/s vs the asymptote {np.median(v_btfr(Mb,a0)):.1f} km/s -> {rat:+.3f} dex")
ck("31.4a escape (a) CLOSED: 'the HI disc does not reach the flat part of the rotation curve'.  At the Wang+2016 HI "
   "radius the baryonic acceleration is already ~0.02 a_0, deep in the modified regime, so the Route A kernel evaluated "
   "there is within 0.02 dex of the asymptote.  The framework cannot hide the missing speed outside the measured disc",
   abs(R_EDGE) < 0.03, f"median log[v(R_HI)/v_flat] = {R_EDGE:+.4f} dex")
# (b) the external-field effect
vobs_med = float(np.median(hv[ok])); Mb_med = float(np.median(Mb)); R_med = float(np.median(R_HI))*kpc
gN_med = G*Mb_med*Msun/R_med**2; g_need = (vobs_med*1e3)**2/R_med
nu_need = g_need/gN_med
x_need = (math.log(1.0 - 1.0/nu_need))**2          # invert nu(x) = 1/(1 - exp(-sqrt(x)))
g_ext = math.sqrt(max((x_need*A0["canonical"])**2 - gN_med**2, 0.0))
eN = g_ext/A0["canonical"]
M_nb = 1e11*Msun
d_nb = math.sqrt(G*M_nb*A0["canonical"])/g_ext/kpc if g_ext > 0 else float("nan")
info(f"the median HUD needs nu_eff = {nu_need:.2f} at R_HI instead of the isolated value {float(np.median(nu(gN_med/A0['canonical']))):.2f}")
info(f"an external field would do it, but it takes g_ext = {eN:.2f} a_0 -- and a 1e11 Msun neighbour produces that only "
     f"within {d_nb:.0f} kpc")
ck("31.4b escape (b) CLOSED: the external-field effect cannot be the answer.  Suppressing the prediction by the observed "
   "amount needs an external field of order a_0 itself, which a 1e11 Msun neighbour supplies only inside a few tens of kpc "
   "-- and these objects are selected by Leisman+2017 to be ISOLATED, with no such neighbour",
   eN > 0.15, f"required g_ext = {eN:.3f} a_0 (canonical); a 1e11 Msun galaxy gives that at {d_nb:.0f} kpc")
# (c) the inclinations
sin_req = np.clip(np.sqrt(np.maximum(h["W50"]**2 - W_TURB**2, 0.0))/(2*v_btfr(Mb, A0["canonical"])), 0, 1)
i_req = np.degrees(np.arcsin(sin_req))
info(f"inclination the framework requires, object by object: median {np.median(i_req):.0f} deg "
     f"[10-90%: {np.percentile(i_req,10):.0f}, {np.percentile(i_req,90):.0f}]; SDSS gives a median of {np.nanmedian(h['inc']):.0f} deg")
ks = stats.ks_2samp(i_req[ok], h["inc"][ok])
info(f"required-vs-measured inclination distributions: two-sample KS D = {ks.statistic:.3f}, p = {ks.pvalue:.1e} "
     f"-- they are not the same distribution")
pen = -float(np.sum(np.log10(np.clip(1 - np.cos(np.radians(i_req[ok])), 1e-12, 1.0))))
info(f"read as a likelihood under random orientation (P(i < i_req) = 1 - cos i_req, objects independent), requiring every "
     f"one of them to be that face-on costs {pen:.0f} dex.  This is an upper bound on the cost: these objects are selected "
     f"on central surface brightness, which does bias the sample toward face-on, and that bias is NOT modelled here")
# how much of the offset a systematic optical-inclination bias would remove, calibrated on the one resolved object
scale = math.sin(math.radians(32.0))/math.sin(math.radians(45.0))
info(f"AGC 114905 is the calibration point for an optical-vs-kinematic inclination bias: optical ~45 deg, HI 32 deg. "
     f"Applying that same sin-ratio ({scale:.3f}) to the whole sample RAISES v_obs by {-math.log10(scale):+.3f} dex")
resid_after = HUD["canonical"][0] - math.log10(scale)
ck("31.4c escape (c) is the only one still open, and it is expensive.  For the framework to be right these galaxies "
   "must be far more face-on than SDSS says -- a median of about 23 deg required against 52 deg measured, two distributions "
   "the KS test separates at p ~ 1e-24.  Calibrating an "
   "optical-inclination bias on the single resolved object (optical 45 deg vs HI 32 deg) removes only about half the "
   "deficit and leaves a residual that is still a real offset -- and that calibration runs the WRONG way for the "
   "framework, since the resolved inclination is LOWER, not higher, than the value this analysis assumed",
   abs(resid_after) > 0.05,
   f"median required i = {np.median(i_req):.0f} deg vs measured {np.nanmedian(h['inc']):.0f} deg; after the AGC 114905-calibrated "
   f"correction the residual is still {resid_after:+.3f} dex in log v (= {4*resid_after:+.2f} dex in mass)")

# ---------------------------------------------------------------- 5. the alternative
P(""); P("-"*118); P("5. THE ALTERNATIVE COMPUTED BESIDE IT -- what LambdaCDM has to do with the same objects"); P("-"*118)
h_ = 0.674                                         # Dutton & Maccio 2014 z = 0: log10 c200 = 0.905 - 0.101 log10(M200 h/1e12)
def c200_DM14(M200_msun):
    return 10**(0.905 - 0.101*np.log10(M200_msun*h_/1e12))
def vmax_of_M200(M200_msun):
    M = M200_msun*Msun
    R200 = (3*M/(4*math.pi*200*rho_crit))**(1/3.)
    V200 = math.sqrt(G*M/R200)/1e3
    c = float(c200_DM14(M200_msun))
    return V200*math.sqrt(0.2162*c/(math.log(1+c) - c/(1+c)))
def M200_of_vmax(v):
    lo, hi_ = 7.0, 14.0
    for _ in range(80):
        mid = 0.5*(lo+hi_)
        if vmax_of_M200(10**mid) < v: lo = mid
        else: hi_ = mid
    return 10**(0.5*(lo+hi_))
M200 = np.array([M200_of_vmax(v) for v in hv[ok]])
fb = Mb[ok]/M200
info(f"Newtonian, baryons only (no halo, no boost) at R_HI: median v = "
     f"{float(np.median(np.sqrt(G*Mb*Msun/(R_HI*kpc))/1e3)):.1f} km/s against the measured {vobs_med:.1f} -- so these are "
     f"NOT Newtonian systems either; something boosts them, just less than the framework says")
info(f"LambdaCDM: matching V_max to the measured speed with the Dutton-Maccio c(M) relation gives median "
     f"log M200 = {float(np.median(np.log10(M200))):.2f}, i.e. a baryon fraction M_b/M200 = {float(np.median(fb)):.3f} "
     f"against the cosmic {OM_B/OM_M:.3f}")
ck("31.5 both ways: the same objects are a problem for LambdaCDM too -- pinning V_max to the observed speed forces halos "
   "so small that these galaxies would have retained an implausible share of the cosmic baryon budget.  The difference is "
   "that LambdaCDM has free parameters to spend on it (concentration, feedback, a lower inclination) and the framework, "
   "having none, simply predicts the wrong number",
   float(np.median(fb)) > 0.3*OM_B/OM_M,
   f"median M_b/M200 = {float(np.median(fb)):.3f} = {float(np.median(fb))/(OM_B/OM_M):.2f} x cosmic; "
   f"Mancera Pina+2022 reach the same conclusion for AGC 114905 (only c200 ~ 0.3 fits, 'unfeasible')")

# ---------------------------------------------------------------- 6. mutations
P(""); P("-"*118); P("6. MUTATION CONTROLS"); P("-"*118)
shuf_r = np.array([stats.spearmanr(np.log10(rng.permutation(Mb[ok])), np.log10(hv[ok])).statistic for _ in range(2000)])
ck("M31a mutation: the measured mass-speed correlation inside the HUD sample is destroyed by shuffling the baryonic "
   "masses against the widths, so the estimator is reading a real correlation and not noise -- but note that this same "
   "check shows how WEAK the leverage is: the correlation is only r ~ 0.5 over 0.8 dex of mass",
   sp.statistic > np.percentile(shuf_r, 99.9),
   f"measured Spearman r = {sp.statistic:.3f}; 2000 shuffles give {np.median(shuf_r):+.3f} with a 99.9th percentile of "
   f"{np.percentile(shuf_r,99.9):.3f}")
r4 = np.log10(hv[ok]/v_btfr(Mb[ok], 4*A0["canonical"]))
ck("M31b mutation: a_0 raised by 4x must move the residual by exactly -0.25 x log10(4) = -0.151 dex, and it does -- the "
   "estimator's sensitivity to a_0 is the textbook one, so the measured offset really is an a_0 statement",
   abs((np.median(r4) - HUD["canonical"][0]) + 0.25*math.log10(4)) < 0.005,
   f"shift {np.median(r4)-HUD['canonical'][0]:+.4f} dex vs the exact -{0.25*math.log10(4):.4f}")
rc = np.log10(av[mm]/v_btfr(aMb[mm], A0["canonical"]))
draws = np.array([np.median(rc[rng.integers(0, len(rc), int(ok.sum()))]) for _ in range(2000)])
ck("M31c mutation: 2000 random mass-matched draws of ORDINARY galaxies, each the same size as the HUD sample, never "
   "reproduce the offset -- so the deficit belongs to the almost-darks and not to the sample size",
   float(np.mean(draws <= HUD["canonical"][0])) < 0.01,
   f"draws of N = {ok.sum()}: median {np.median(draws):+.3f}, 1st percentile {np.percentile(draws,1):+.3f}; "
   f"fraction at or below the HUDs' {HUD['canonical'][0]:+.3f} is {float(np.mean(draws <= HUD['canonical'][0])):.4f}")

P(""); P("="*118); P("VERDICT -- ITEM 31: LIABILITY, and a real one"); P("="*118)
P(f"  The almost-darks were the best place in this hunt to measure a_0 without a stellar mass-to-light ratio, and they")
P(f"  do not cooperate.  115 HI-bearing ultra-diffuse ALFALFA galaxies sit {HUD['canonical'][0]:+.3f} +- {HUD['canonical'][1]:.3f} dex")
P(f"  (canonical) / {HUD['alt'][0]:+.3f} +- {HUD['alt'][1]:.3f} dex (alt) BELOW the zero-parameter prediction in rotation speed --")
P(f"  {4*HUD['canonical'][0]:+.2f} dex in baryonic mass, {4*DIF[0]:+.2f} dex differentially -- with a scatter of {HUD['canonical'][2]:.2f} dex,")
P(f"  where the item asked for 0.1.  The alt footing is WORSE than the canonical, so no footing rescues it.")
P(f"  The same estimator puts {CTRL['canonical'][3]} ordinary gas-rich galaxies of the same baryonic mass at {CTRL['canonical'][0]:+.3f} dex, so this is")
P(f"  differential and it is {abs(DIF[0]/DIF[1]):.0f} sigma.  Three escapes were priced: the HI disc DOES reach the modified regime")
P(f"  ({R_EDGE:+.3f} dex), the external-field effect would need {eN:.2f} a_0 in objects selected to be isolated, and the")
P(f"  inclination escape needs a median {np.median(i_req):.0f} deg where SDSS measures {np.nanmedian(h['inc']):.0f} deg.  Only the last is alive, it is the one the")
P(f"  published resolved work also identifies, and on the single object where interferometry exists this pipeline")
P(f"  reproduces that paper's MOND-required inclination to within a degree.")
P(f"  Recorded on the standing ledger.  It is not a clean kill -- optical inclinations of ultra-diffuse discs are the")
P(f"  weakest link and the one resolved case shows them biased HIGH -- but it is a genuine negative that the framework")
P(f"  cannot argue away, and it is independent of the stellar mass-to-light ratio, which was the point of the item.")
P("")
P("*"*118)
P("  SUPERSEDED: the paragraph above was written before the selection audit and it is WRONG about the size and the")
P("  significance.  h31b_almost_dark_selection_audit.py shows that ALFALFA's width-dependent detection limit")
P("  (SNR ~ W50^(-1/2)) manufactures most of this: 50% of these galaxies would be undetectable if they sat on the")
P("  framework's BTFR, and the control used above was nearer and brighter and so escaped the same cut.  Against a")
P("  control matched on the detection ceiling the almost-dark differential is -0.089 +- 0.033 dex, not -0.265, and the")
P("  9.5 sigma is a statistical error bar on a number whose systematic is larger.  ITEM 31 STANDS AS A NULL.")
P("*"*118)
sys.exit(ck.done())
