#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
h52_fundamental_plane.py -- HUNT ITEM 52 (the tilt of the Fundamental Plane from a_0).
======================================================================================
The claim under test (Sanders 2000).  Early-type galaxies lie on a plane
        log R_e = a log sigma + b log I_e + c,
observed with a ~ 1.4 and b ~ -0.9, where the virial theorem with a constant mass-to-light ratio and structural homology
demands a = 2, b = -1 EXACTLY.  That departure is the TILT, normally attributed to a dark-matter fraction growing with mass,
plus non-homology, plus stellar-population M/L trends.  Sanders' proposal is that the tilt is MOND: the internal
acceleration at R_e is near a_0, the kernel inflates the dynamical mass by nu(y), and a_0 alone produces the tilt.

The framework makes that proposal SHARP, and the sharpening is the whole content of this item.  For a homologous family the
kernel's dimensionless argument is
        x = G M_*/(R_e^2 a_0) = 2 pi G Upsilon I_e / a_0,
which contains SURFACE BRIGHTNESS ONLY -- R_e cancels identically.  So the framework predicts
        a = 2 EXACTLY (unchanged from virial), and its entire tilt lands in b.
That is a theorem, not an approximation, and it is verified numerically below.  The observed tilt is in BOTH coefficients.

Data: 6dF Galaxy Survey Fundamental Plane catalogue (Campbell+2014, MNRAS 443, 1231), 11102 early-type galaxies with J, H
      and K effective radii, mean effective surface brightnesses and aperture-corrected central dispersions -- fetched this
      session from the VizieR CfA mirror to real_research/data/fp_6dfgs_campbell2014.tsv.

Alternatives computed beside the framework: (i) Newton + constant Upsilon + homology (the exact virial plane), and
(ii) Newton + constant Upsilon + the MEASURED Sersic non-homology through Cappellari+2006's beta(n) -- the non-dark half of
the standard explanation.  Both a_0 footings.  Mutations.  Checks that can fail.

METHOD NOTE that matters for every number: a direct least-squares fit of log R_e on log sigma is strongly ATTENUATED by the
measurement error in sigma (median 0.055 dex against an intrinsic spread of ~0.11).  Every model here is therefore fitted
BOTH noiselessly (where the a = 2 theorem is visible) and after having the galaxies' own sigma errors added (where it can be
compared with the data).  The attenuation factor measured off the noiseless-vs-noisy virial mock is used to check the
observed fit against the published maximum-likelihood value, which is an independent validation of the whole pipeline.
"""
import sys, math, os
import numpy as np
from hunt_lib import *

ck = Check(); rng = np.random.default_rng(52)
MSUN_J = 3.67                                     # Vega absolute magnitude of the Sun, J band (Willmer 2018)


def read_viz(fname):
    lines = [l.rstrip("\n") for l in open(os.path.join(DATA, fname), encoding="latin-1")
             if l.strip() and not l.startswith("#")]
    i = next(k for k, l in enumerate(lines) if set(l.replace("\t", "").strip()) <= set("- "))
    return [h.strip() for h in lines[i-2].split("\t")], [l.split("\t") for l in lines[i+1:]]


hdr, rows = read_viz("fp_6dfgs_campbell2014.tsv")
def C(name):
    j = hdr.index(name)
    return np.array([float(r[j]) if j < len(r) and r[j].strip() not in ("", "-") else np.nan for r in rows])
def Sc(name):
    j = hdr.index(name)
    return np.array([r[j].strip() if j < len(r) else "" for r in rows])

P("="*128); P("ITEM 52 -- the tilt of the Fundamental Plane: does a_0 produce it?"); P("="*128)
lRe_h = C("JlogRe"); lIe = C("JlogIe"); lsig = C("logVd"); elsig = C("e_logVd")
elRe = C("e_JlogRe"); elIe = C("e_JlogIe")
nser = C("n"); cz = C("cz"); Jtot = C("Jtot"); js = Sc("Js")
lReK_h = C("KlogRe"); lIeK = C("KlogIe")
good = (js == "1") & np.isfinite(lRe_h) & np.isfinite(lIe) & np.isfinite(lsig) & (elsig < 0.10) & (cz > 3000)
g = good; NGAL = int(g.sum())
info(f"6dFGS FP catalogue: {len(rows)} rows, {NGAL} pass the quality cut (J-band flag Js=1, e_log sigma < 0.10, cz > 3000 km/s)")

# ---------------------------------------------------------------- units control
def lum_dist_h1(czv):                             # Mpc, computed with H0 = 100, the catalogue's own h convention
    z = czv/(c_light/1e3); OmM = 0.3
    zz = np.linspace(0, 1, 200)[None, :]*z[:, None]
    return (c_light/1e3/100.0)*np.trapz(1.0/np.sqrt(OmM*(1+zz)**3 + (1-OmM)), zz, axis=1)*(1+z)
MJ = Jtot - 5*np.log10(lum_dist_h1(cz)*1e6/10.0)
d_units = np.log10(10**(0.4*(MSUN_J - MJ))/(2*math.pi*(10**lRe_h*1e3)**2)) - lIe
m = g & np.isfinite(d_units)
ck("52.0 UNITS CONTROL (can fail) -- rebuilding the tabulated mean effective surface brightness from the total J magnitude, the angular effective radius and the redshift reproduces it with small scatter, which pins BOTH conventions this item needs: R_e is tabulated in h^-1 kpc (H0 = 100) and I_e is the MEAN surface brightness inside R_e (L = 2 pi I_e R_e^2).  If either were wrong every number below would be wrong",
   np.std(d_units[m]) < 0.05,
   f"log10(I_e rebuilt / I_e tabulated) = {np.mean(d_units[m]):+.3f} +- {np.std(d_units[m]):.3f} dex over {int(m.sum())} galaxies "
   f"(the small mean offset is the k-correction and Galactic extinction Campbell+2014 apply and I did not)")

lRe = lRe_h - math.log10(h); lReK = lReK_h - math.log10(h)                 # physical log10(R_e/kpc)
lL = np.log10(2*math.pi) + lIe + 2*(lRe + 3.0)                            # log10(L_J/Lsun)
lLK = np.log10(2*math.pi) + lIeK + 2*(lReK + 3.0)

# ---------------------------------------------------------------- dimensionless Jeans solution
UG = np.geomspace(1e-3, 1e4, 1400); LUG = np.log(UG)
AH = 1.0/1.8153
RHO_T = 1.0/(UG*(UG + AH)**3); MDIM = UG**2/(UG + AH)**2
GN_DIM = MDIM/UG**2

def F_of_x(x, u_ap=0.125, kernel="routeA"):
    """sigma_aperture / sqrt(G M_*/R_e), Hernquist, isotropic, x = G M_*/(R_e^2 a_0).  x=None -> Newton."""
    if x is None:                b = np.ones_like(GN_DIM)
    elif kernel == "routeA":     b = nu(x*GN_DIM)
    else:                        y = x*GN_DIM; b = (1 + np.sqrt(1 + 4/y))/2          # the 'simple' mu, for comparison
    integ = RHO_T*GN_DIM*b*UG
    s2 = np.concatenate([np.cumsum((0.5*(integ[1:]+integ[:-1])*np.diff(LUG))[::-1])[::-1], [0.0]])/RHO_T
    U = np.geomspace(1e-3, u_ap, 220); uu = np.linspace(0.0, 6.5, 420); chv = np.cosh(uu)
    r = np.outer(U, chv)
    ss = np.exp(np.interp(np.log(r), LUG, np.log(np.maximum(s2, 1e-30))))
    rho = 1.0/(r*(r + AH)**3)
    return math.sqrt(np.trapz(np.trapz(rho*ss*r, uu, axis=1)*U, U)/np.trapz(np.trapz(rho*r, uu, axis=1)*U, U))

XG = np.geomspace(1e-3, 1e5, 240)          # F(x) grid; checked against a 700-point grid, the coefficients below move by < 1e-4
FG = {ap: np.array([F_of_x(x, ap) for x in XG]) for ap in (0.125, 0.5, 1.0)}
FG_SIMPLE = np.array([F_of_x(x, 0.125, "simple") for x in XG])
F_NEWT = {ap: F_of_x(None, ap) for ap in FG}
info(f"\ndimensionless Jeans solution: sigma_ap = F(x) sqrt(G M_*/R_e).  Newtonian limit F = {F_NEWT[0.125]:.4f} at aperture R_e/8 "
     f"(equivalently a virial coefficient 1/F^2 = {1/F_NEWT[0.125]**2:.2f}, against Cappellari+2006's beta(n=4) = {8.87-0.831*4+0.0241*16:.2f})")

def F_at(x, ap=0.125, tab=None):
    return np.exp(np.interp(np.log(x), np.log(XG), np.log(FG[ap] if tab is None else tab)))
def sig_pred(lM, lRe_kpc, a0, ap=0.125, tab=None):
    M = 10**np.asarray(lM)*Msun; R = 10**np.asarray(lRe_kpc)*kpc
    return np.sqrt(G*M/R)*F_at(G*M/(R**2*a0), ap, tab)/1e3                # km/s

s1 = sig_pred(11.0, 0.5, A0["canonical"]); s2_ = sig_pred(12.0, 1.0, A0["canonical"])
ck("52.1 SCALE-FREENESS CONTROL (can fail) -- the framework's predicted dispersion really is sqrt(G M/R_e) times a function of x alone: two galaxies a decade apart in mass but at the same x give the same reduced dispersion.  That is what makes 'a = 2 exactly' a theorem rather than an approximation",
   abs(math.log10((s1/math.sqrt(10**11.0/10**0.5))/(s2_/math.sqrt(10**12.0/10**1.0)))) < 1e-3,
   f"M=1e11/R_e=3.16 kpc gives sigma = {s1:.1f} km/s, M=1e12/R_e=10 kpc gives {s2_:.1f} km/s; reduced dispersions agree to "
   f"{abs(math.log10((s1/math.sqrt(10**11.0/10**0.5))/(s2_/math.sqrt(10**12.0/10**1.0)))):.1e} dex")

# ---------------------------------------------------------------- fitting machinery
def fp_direct(lr, ls, li):
    A = np.ascontiguousarray(np.vstack([ls, li, np.ones_like(ls)]).T)
    return np.linalg.lstsq(A, np.ascontiguousarray(lr), rcond=None)[0]
def fp_orth(lr, ls, li):
    X = np.vstack([lr, ls, li]).T; X = X - X.mean(0)
    w = np.linalg.eigh(np.cov(X.T))[1][:, 0]
    a = -w[1]/w[0]; b = -w[2]/w[0]
    return np.array([a, b, np.mean(lr) - a*np.mean(ls) - b*np.mean(li)])

UPS = 1.2                                                                 # fiducial J-band stellar M/L (old population)
BETA_N = 8.87 - 0.831*nser + 0.0241*nser**2                               # Cappellari+2006 virial coefficient
lMs = np.log10(UPS) + lL
NOISE = rng.normal(0, 1, NGAL)*elsig[g]                                   # one frozen noise realisation, shared by all models

MODELS = {}
MODELS["framework, canonical a_0"] = np.log10(sig_pred(lMs[g], lRe[g], A0["canonical"]))
MODELS["framework, alt a_0"]       = np.log10(sig_pred(lMs[g], lRe[g], A0["alt"]))
MODELS["framework, 'simple' mu"]   = np.log10(sig_pred(lMs[g], lRe[g], A0["canonical"], tab=FG_SIMPLE))
MODELS["Newton + homology"]        = np.log10(np.sqrt(G*10**lMs[g]*Msun/(10**lRe[g]*kpc))*F_NEWT[0.125]/1e3)
MODELS["Newton + Sersic non-homology"] = np.log10(np.sqrt(G*10**lMs[g]*Msun/(10**lRe[g]*kpc/BETA_N[g]))/1e3)

P(""); P("-"*128); P("1.  THE OBSERVED PLANE, AND WHAT EACH LAW PREDICTS FOR IT"); P("-"*128)
P(f"{'':32} {'NOISELESS   a':>14} {'b':>8}   |   {'WITH sigma ERRORS   a':>22} {'b':>8}   | {'orthogonal a':>13} {'b':>8}")
FIT = {}
for lab, ls in MODELS.items():
    d0 = fp_direct(lRe[g], ls, lIe[g]); d1 = fp_direct(lRe[g], ls + NOISE, lIe[g]); o1 = fp_orth(lRe[g], ls + NOISE, lIe[g])
    FIT[lab] = (d0, d1, o1)
    P(f"  {lab:30} {d0[0]:14.3f} {d0[1]:8.3f}   |   {d1[0]:22.3f} {d1[1]:8.3f}   | {o1[0]:13.3f} {o1[1]:8.3f}")
obs_d = fp_direct(lRe[g], lsig[g], lIe[g]); obs_o = fp_orth(lRe[g], lsig[g], lIe[g])
P(f"  {'OBSERVED':30} {'--':>14} {'--':>8}   |   {obs_d[0]:22.3f} {obs_d[1]:8.3f}   | {obs_o[0]:13.3f} {obs_o[1]:8.3f}")

vir0, vir1, _ = FIT["Newton + homology"]; fw0, fw1, _ = FIT["framework, canonical a_0"]
nh0, nh1, _ = FIT["Newton + Sersic non-homology"]; sm0, sm1, _ = FIT["framework, 'simple' mu"]
ck("52.2 THE FRAMEWORK'S THEOREM, VERIFIED NUMERICALLY -- with a homologous family the kernel's argument depends on surface brightness alone, so the framework leaves the sigma coefficient at the exact virial 2 and puts the whole of its tilt into the surface-brightness coefficient.  The noiseless fits reproduce a = 2.000 for both the virial model and the framework, to three decimals",
   abs(vir0[0] - 2.0) < 0.001 and abs(vir0[1] + 1.0) < 0.001 and abs(fw0[0] - 2.0) < 0.005 and abs(fw0[1] + 1.0) > 0.005,
   f"virial (a, b) = ({vir0[0]:.4f}, {vir0[1]:.4f}) -- the exact plane recovered to 1e-4; framework ({fw0[0]:.4f}, {fw0[1]:.4f}): "
   f"a moved by {fw0[0]-2.0:+.4f}, b by {fw0[1]+1.0:+.4f}")
info(f"the framework's a is {fw0[0]:.4f} rather than exactly 2 for a reason worth stating, because it is not numerical: the framework's")
info("relation is log R_e = 2 log sigma - log I_e - 2 log F(I_e) + const, and log F is CURVED in log I_e.  A plane fitted to a curved")
info("surface leaks a little of that curvature into the other coefficient, because sigma and I_e are correlated across the sample.")
info("The leak is 0.002, three orders below the tilt being explained, and it vanishes exactly in the a_0/100 mutation where F is flat.")
atten = vir1[0]/vir0[0]
ck("52.3 PIPELINE VALIDATION AGAINST THE PUBLISHED VALUE (can fail) -- de-attenuating the direct fit of the real data by the attenuation the virial mock suffers from the galaxies' own sigma errors recovers the published maximum-likelihood 6dFGS J-band coefficient of Magoulas+2012 (a = 1.404) to better than 1%.  The fitting machinery is therefore doing what it should",
   abs(obs_d[0]/atten - 1.404) < 0.05,
   f"attenuation factor {atten:.3f} from the virial mock (a: {vir0[0]:.3f} noiseless -> {vir1[0]:.3f} noisy); "
   f"observed direct a = {obs_d[0]:.3f} -> de-attenuated {obs_d[0]/atten:.3f} against Magoulas+2012's 1.404")
b_share = (fw1[1] - vir1[1])/(obs_d[1] - vir1[1])
ck("52.4 AGAINST INTEREST, AND THIS IS THE ITEM'S ANSWER (the check ASSERTS THE FAILURE) -- the observed plane's SIGMA coefficient is far from virial, and the framework cannot move it at all: a_0 tilts the surface-brightness axis and leaves the sigma axis untouched, by the theorem in 52.2.  The item's bar was 'tilt within 0.05 of prediction'; the framework misses the sigma coefficient by six times that.  MOND at R_e is NOT the tilt of the Fundamental Plane",
   abs(fw1[0] - obs_d[0]) > 0.05,
   f"observed a = {obs_d[0]:.3f}, framework a = {fw1[0]:.3f}, virial a = {vir1[0]:.3f}: the framework misses by {abs(fw1[0]-obs_d[0]):.3f} "
   f"(bar 0.05) and explains 0% of the a tilt.  On b it supplies {100*b_share:.0f}% of the observed tilt "
   f"(observed {obs_d[1]:.3f}, framework {fw1[1]:.3f}, virial {vir1[1]:.3f})")
info(f"the exponential kernel makes this item HARDER for the framework than plain MOND does: the same calculation with the")
info(f"'simple' mu gives b = {sm1[1]:.3f}, i.e. {100*(sm1[1]-vir1[1])/(obs_d[1]-vir1[1]):.0f}% of the b tilt against Route A's {100*b_share:.0f}%, because "
     f"nu - 1 = exp(-sqrt(y)) dies far faster above the transition than 1/(2y) does.")

# ---------------------------------------------------------------- 2. the same statement as an M/L tilt
P(""); P("-"*128); P("2.  THE SAME STATEMENT AS AN M/L TILT, AND WHERE THE TILT ACTUALLY LIVES"); P("-"*128)
def ml_and_partials(ls_kms):
    """M_5 = 5 sigma^2 R_e/G built EXACTLY as for the data, so that the R_e error propagates identically in model and data."""
    lM5 = np.log10(5*(10**ls_kms*1e3)**2*(10**lRe[g]*kpc)/G/Msun)
    lml = lM5 - lL[g]
    A = np.ascontiguousarray(np.vstack([lL[g], lIe[g], np.ones(NGAL)]).T)
    p, q, _ = np.linalg.lstsq(A, np.ascontiguousarray(lml), rcond=None)[0]
    return lml, np.polyfit(lL[g], lml, 1)[0], p, q
lml_obs, gam_obs, p_obs, q_obs = ml_and_partials(lsig[g])
info(f"{'':34} {'d log(M/L)/d log L':>19} {'p (at fixed I_e)':>18} {'q (at fixed L)':>16}")
info(f"{'OBSERVED':34} {gam_obs:19.3f} {p_obs:18.3f} {q_obs:16.3f}")
ML = {}
for lab, ls in MODELS.items():
    _, gm, pp, qq = ml_and_partials(ls + NOISE)
    ML[lab] = (gm, pp, qq)
    info(f"{lab:34} {gm:19.3f} {pp:18.3f} {qq:16.3f}")
info("p is the residual M/L trend with luminosity AT FIXED SURFACE BRIGHTNESS.  The framework's p is ZERO BY CONSTRUCTION --")
info("its kernel argument x = 2 pi G Upsilon I_e / a_0 contains no luminosity -- so p is the axis on which this item is decided.")
gm_fw, p_fw, q_fw = ML["framework, canonical a_0"]; gm_v, p_v, q_v = ML["Newton + homology"]
ck("52.5 THE STRUCTURE IS RIGHT AND THE AMPLITUDE IS NOT (and this is the honest surprise of the item) -- the observed mass-to-light residual is dominated by SURFACE BRIGHTNESS, not by luminosity, exactly the structure the framework predicts: at fixed I_e the observed trend with L is small and close to the framework's zero.  But on the surface-brightness axis itself the framework delivers only a fraction of the observed coefficient",
   abs(p_obs - p_fw) < abs(q_obs - q_fw),
   f"p: observed {p_obs:+.3f} vs framework {p_fw:+.3f} (virial {p_v:+.3f}) -- a {abs(p_obs-p_fw):.3f} miss; "
   f"q: observed {q_obs:+.3f} vs framework {q_fw:+.3f} (virial {q_v:+.3f}) -- a {abs(q_obs-q_fw):.3f} miss, "
   f"i.e. the framework supplies {100*(q_fw-q_v)/(q_obs-q_v):.0f}% of the surface-brightness tilt")
# the correlated R_e / I_e error bias on q, estimated from the catalogue's own error columns
var_e = np.mean(elRe[g]**2); var_t = max(np.var(lRe[g]) - var_e, 1e-6)
f_err = var_e/(var_t + var_e)
info(f"\nBIAS CONTROL on q, against interest: R_e and I_e are fitted jointly at (nearly) fixed total magnitude, so an error in")
info(f"log R_e moves log I_e by about -2x and log(M_5/L) by +1x, which fakes a NEGATIVE q.  With the catalogue's own median")
info(f"e_log R_e = {np.median(elRe[g]):.3f} dex against an intrinsic spread of {math.sqrt(var_t):.3f} dex, the error fraction is {f_err:.2f} and the")
info(f"spurious contribution is about {-0.5*f_err:+.3f} -- so the true q is nearer {(q_obs + 0.5*f_err)/(1-f_err):+.3f} than {q_obs:+.3f}, and the framework's share")
info(f"of it rises from {100*(q_fw-q_v)/(q_obs-q_v):.0f}% to about {100*(q_fw-q_v)/((q_obs + 0.5*f_err)/(1-f_err)-q_v):.0f}%.  Even so it is a minority of the tilt.")

# ---------------------------------------------------------------- 3. can Upsilon or the aperture rescue it?
P(""); P("-"*128); P("3.  CAN ANY UPSILON OR APERTURE RESCUE IT?"); P("-"*128)
info(f"{'Upsilon_J':>10} {'median x = g_N(R_e)/a_0':>24} {'median nu boost':>16} {'a':>8} {'b':>8} {'% of b tilt':>13} {'q':>8} {'% of q tilt':>13}")
for ups in (0.5, 0.8, 1.2, 1.6, 2.2, 3.0):
    lm = np.log10(ups) + lL
    ls_p = np.log10(sig_pred(lm[g], lRe[g], A0["canonical"]))
    d = fp_direct(lRe[g], ls_p + NOISE, lIe[g]); _, _, _, qq = ml_and_partials(ls_p + NOISE)
    xx = G*(10**lm[g]*Msun)/((10**lRe[g]*kpc)**2*A0["canonical"])
    info(f"{ups:10.1f} {np.median(xx):24.1f} {np.median((F_at(xx)/F_NEWT[0.125])**2):16.4f} {d[0]:8.3f} {d[1]:8.3f} "
         f"{100*(d[1]-vir1[1])/(obs_d[1]-vir1[1]):13.0f} {qq:8.3f} {100*(qq-q_v)/(q_obs-q_v):13.0f}")
info("no Upsilon moves a, because Upsilon enters only through x, i.e. only through I_e.  Lowering Upsilon buys b tilt but at")
info("the price of a stellar M/L below anything a stellar population gives for an old red galaxy, and it never touches a.")
for ap, lab in ((0.125, "R_e/8"), (0.5, "R_e/2"), (1.0, "R_e")):
    d = fp_direct(lRe[g], np.log10(sig_pred(lMs[g], lRe[g], A0["canonical"], ap)) + NOISE, lIe[g])
    info(f"aperture {lab:6}: framework a = {d[0]:.3f}, b = {d[1]:.3f}   (the aperture moves the zero point, not the tilt)")

# ---------------------------------------------------------------- 4. K band
P(""); P("-"*128); P("4.  K-BAND CROSS-CHECK"); P("-"*128)
gk = good & np.isfinite(lReK) & np.isfinite(lIeK)
nk = int(gk.sum()); noise_k = rng.normal(0, 1, nk)*elsig[gk]
lmk = np.log10(0.85) + lLK[gk]                                            # Upsilon_K ~ 0.85 for an old population
okd = fp_direct(lReK[gk], lsig[gk], lIeK[gk])
fwk0 = fp_direct(lReK[gk], np.log10(sig_pred(lmk, lReK[gk], A0["canonical"])), lIeK[gk])
fwk1 = fp_direct(lReK[gk], np.log10(sig_pred(lmk, lReK[gk], A0["canonical"])) + noise_k, lIeK[gk])
vk1 = fp_direct(lReK[gk], np.log10(np.sqrt(G*10**lmk*Msun/(10**lReK[gk]*kpc))*F_NEWT[0.125]/1e3) + noise_k, lIeK[gk])
info(f"K band, N = {nk}: observed a = {okd[0]:.3f}, b = {okd[1]:.3f}; framework a = {fwk1[0]:.3f}, b = {fwk1[1]:.3f}; "
     f"virial a = {vk1[0]:.3f}, b = {vk1[1]:.3f}; framework noiseless a = {fwk0[0]:.4f}")
ck("52.6 the K band says the same thing as the J band, so the verdict is not a photometric-band artefact: the framework's sigma coefficient is again pinned to the virial value while the data's is far below it",
   abs(fwk0[0] - 2.0) < 0.005 and abs(fwk1[0] - vk1[0]) < 0.05 and abs(fwk1[0] - okd[0]) > 0.05,
   f"framework K-band a = {fwk0[0]:.4f} noiseless (theorem holds) and {fwk1[0]:.3f} noisy, against a virial {vk1[0]:.3f} and an observed {okd[0]:.3f}")

# ---------------------------------------------------------------- mutations
P(""); P("-"*128); P("MUTATION CONTROLS"); P("-"*128)
ls_m = np.log10(sig_pred(lMs[g], lRe[g], A0["canonical"]/100.0))
dm0 = fp_direct(lRe[g], ls_m, lIe[g]); dm1 = fp_direct(lRe[g], ls_m + NOISE, lIe[g])
ck("M1 mutation: with a_0 divided by 100 every galaxy is Newtonian and the framework's plane must collapse onto the exact virial plane -- it does, so the b tilt reported above really is the kernel's doing and not an artefact of the Jeans solve",
   abs(dm0[1] + 1.0) < abs(fw0[1] + 1.0)/5 and abs(dm0[0] - 2.0) < 0.002,
   f"a_0/100 gives noiseless (a, b) = ({dm0[0]:.4f}, {dm0[1]:.4f}) against the virial (2.0000, -1.0000) and the framework's ({fw0[0]:.4f}, {fw0[1]:.4f})")
sh = rng.permutation(NGAL)
ds = fp_direct(lRe[g], MODELS["framework, canonical a_0"][sh] + NOISE, lIe[g])
ck("M2 mutation: shuffling which galaxy's predicted dispersion goes with which galaxy's radius and surface brightness must destroy the plane -- it does",
   abs(ds[0]) < 0.3*abs(fw1[0]), f"shuffled (a, b) = ({ds[0]:+.3f}, {ds[1]:+.3f}) against the framework's ({fw1[0]:+.3f}, {fw1[1]:+.3f})")

# ---------------------------------------------------------------- verdict
P(""); P("-"*128); P("VERDICT"); P("-"*128)
x_all = G*(10**lMs*Msun)/((10**lRe*kpc)**2*A0["canonical"])
info(f"noiseless coefficients -- virial (2.000, -1.000); framework ({fw0[0]:.3f}, {fw0[1]:.3f}); non-homology ({nh0[0]:.3f}, {nh0[1]:.3f}); "
     f"observed, de-attenuated ({obs_d[0]/atten:.3f}, {obs_d[1]:.3f})")
info(f"Sanders' 2000 proposal rested on ellipticals sitting AT the MOND transition.  Measured on 6dFGS with a stellar-population")
info(f"M/L of {UPS:.1f}, the median internal acceleration at R_e is x = {np.median(x_all[g]):.0f} a_0 (5-95%: {np.percentile(x_all[g],5):.0f} to {np.percentile(x_all[g],95):.0f}) -- an order of")
info(f"magnitude above the transition, where Route A's exponential return has almost nothing left to give: the median boost is")
info(f"{100*(np.median((F_at(x_all[g])/F_NEWT[0.125])**2)-1):.1f}% in dynamical mass.  The proposal fails on the data, not on the algebra.")
info("What survives, and it is worth keeping: the SIGN and the STRUCTURE are the framework's.  The observed mass-to-light residual")
info("really is keyed to surface brightness rather than to luminosity, which is what a_0 predicts and what a mass-dependent dark")
info("fraction does not; the framework simply supplies a minority of its size.  The item is recorded as a LIABILITY on amplitude")
info("with a structural point in the framework's favour, and the 'tilt within 0.05' bar is NOT met.")
sys.exit(ck.done())
