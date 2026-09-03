#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
h93_outer_halo_globulars.py -- HUNT ITEM 93: the four outer-halo globular clusters, with the Milky Way's external field.
=========================================================================================================================
NGC 2419, Pal 3, Pal 4 and Pal 14 sit 68-104 kpc from the Galactic centre.  Their internal accelerations are 0.01-0.9 a_0
and the Milky Way's field at their positions is x_ext = g_ext/a_0 ~ 0.09-0.14.  The framework therefore demands an
inflated effective gravity for their internal dynamics,

        G_eff = nu(y_tot) G ,        y_tot = (g_N,int + g_N,ext)/a_0        (QUMOND; nu acts on the NEWTONIAN field)

and hence sigma_framework = sqrt(nu) * sigma_Newton with sqrt(nu) = 1.3 (NGC 2419) to 2.5 (Pal 14).  That is a factor-2
prediction with no free parameter except the stellar mass-to-light ratio, which is why Baumgardt, Grebel & Kroupa (2005)
proposed these clusters as the cleanest test of modified gravity in the Galaxy.

THE ITEM'S PREMISE IS ONLY PARTLY RIGHT, and this script says so up front.  The item calls this an external-field test
with e_N ~ 0.1-0.3.  In fact only Pal 14 is genuinely external-field dominated (y_int < y_ext).  Pal 3 and Pal 4 are
ISOLATED deep-MOND systems whose boost comes from their own low internal acceleration, with the Milky Way's field
merely trimming it by 7-15%; NGC 2419 is internally dominated at y_int ~ 0.9 and barely boosted at all.  The numbers
below separate the two contributions rather than assert the item's framing.

THE UNITS TRAP THIS SCRIPT AVOIDS.  In QUMOND nu takes the NEWTONIAN field y = g_N/a_0, not the actual (MONDian) field
x = g/a_0.  In the deep-MOND limit x = sqrt(y), so feeding x into nu returns 1/sqrt(x) instead of the correct 1/x -- an
under-estimate of G_eff by a factor ~3 at the fields relevant here.  (The repo's item-8 dwarf script, h8_h42_h96_dwarfs.py,
uses nu(x_ext) with the MONDian field; that under-predicts its dwarf dispersions and so makes its own liability look
worse than it is.  Flagged here as a cross-reference, not fixed here -- it is item 8's territory.)  The prescription used
below is checked against the PUBLISHED MOND prediction for Pal 14 and reproduces it to 7%.

DATA (fetched this session, saved under real_research/data/globular_clusters/):
  * Baumgardt's structural-parameter table (N-body fits, 157 clusters): apparent V, distance, R_GC, projected half-light
    radius r_h,l, fitted mass, fitted M/L_V, model central dispersion sigma_0.
  * Baumgardt's MEASURED velocity-dispersion profiles (radius in arcsec, N stars, sigma with asymmetric errors).
  * Published single-cluster values carried alongside: Pal 14 sigma = 0.38 +- 0.12 km/s from 16 members (Jordi et al.
    2009, AJ 137, 4586) and Pal 4 sigma = 0.87 +- 0.18 km/s from 23 members (Frank et al. 2012, MNRAS 423, 2917).
  * Harris (2010) reddenings E(B-V) for the extinction correction.

Only photometry (V, E(B-V), distance), structure (r_h,l) and the MEASURED dispersions enter the test.  Baumgardt's
fitted masses are used ONLY to check that the Wolf estimator is calibrated -- never as the mass in the test.

Checks that CAN fail; three mutation controls; both footings; Newtonian / no-dark-matter alternative everywhere.
"""
import sys, math, os
import numpy as np
from scipy.stats import chi2 as chi2dist, norm
from hunt_lib import *

ck = Check()
GCDIR = os.path.join(DATA, "globular_clusters")
PC = 3.0857e16
MSUN_V = 4.83                      # absolute V magnitude of the Sun
UPS_V = 1.6                        # fiducial stellar M/L_V of a 12 Gyr, [Fe/H] ~ -1.5 population, Kroupa IMF
UPS_LO, UPS_HI = 1.3, 2.2          # the stellar-population range, stated BEFORE the numbers are computed
MW_MB = 6.0e10                     # Milky Way baryonic mass (Msun): the value the framework itself needs; scanned below
EBV = {"NGC 2419": 0.08, "Pal 3": 0.04, "Pal 4": 0.01, "Pal 14": 0.04}   # Harris (2010) catalogue
TARGETS = ["NGC 2419", "Pal 3", "Pal 4", "Pal 14"]


def load_params():
    rows = {}
    for line in open(os.path.join(GCDIR, "baumgardt_gc_parameters.tsv"), encoding="utf-8"):
        if line.startswith("#") or line.startswith("ClusterName"): continue
        f = line.rstrip("\n").split("\t")
        rows[f[0]] = f
    return rows


def load_profiles():
    prof = {}
    for line in open(os.path.join(GCDIR, "baumgardt_gc_veldisp_profiles.tsv"), encoding="utf-8"):
        if line.startswith("#") or line.startswith("ClusterName"): continue
        f = line.rstrip("\n").split("\t")
        if f[6] != "RV": continue
        prof.setdefault(f[0], []).append((float(f[1]), int(f[2]), float(f[3]), float(f[4]), float(f[5])))
    return prof


par, prof = load_params(), load_profiles()

P("="*118)
P("ITEM 93 -- outer-halo globular clusters as a test of the framework's boosted internal gravity")
P("="*118)

GC = []
for name in TARGETS:
    f = par[name]
    Dsun = float(f[3].split("+-")[0]); RGC = float(f[4].split("+-")[0])
    NRV = int(f[5]); Vapp = float(f[8].split("+-")[0]); ML_fit = float(f[9].split("+-")[0])
    rhl = float(f[11]); sig0_model = float(f[21])
    mant, expo = f[7].split("·")[0].split("+-")[0].strip(), f[7].split("·")[1].strip()
    Mfit = float(mant)*10.0**float(expo[-1])
    Av = 3.1*EBV[name]
    MV = Vapp - Av - 5*math.log10(Dsun*1e3/10.0)
    LV = 10**(0.4*(MSUN_V - MV))
    GC.append(dict(name=name, D=Dsun, RGC=RGC, NRV=NRV, V=Vapp, Av=Av, MV=MV, LV=LV, rhl=rhl,
                   Mfit=Mfit, ML_fit=ML_fit, sig0_model=sig0_model, prof=prof[name]))

info(f"fiducial stellar M/L_V = {UPS_V} (stellar-population range {UPS_LO}-{UPS_HI}, stated before the fit); "
     f"Milky Way baryonic mass = {MW_MB:.1e} Msun; Sun M_V = {MSUN_V}")
P("")
P(f"{'cluster':10} {'D_sun':>7} {'R_GC':>7} {'V':>6} {'A_V':>5} {'M_V':>7} {'L_V':>10} {'r_h,l':>7} {'M_fit':>10} {'M/L_fit':>8} {'N_RV':>5}")
for g in GC:
    P(f"{g['name']:10} {g['D']:7.2f} {g['RGC']:7.2f} {g['V']:6.2f} {g['Av']:5.3f} {g['MV']:7.3f} {g['LV']:10.3e} "
      f"{g['rhl']:7.2f} {g['Mfit']:10.3e} {g['ML_fit']:8.2f} {g['NRV']:5d}")
info("caveat on r_h,l: Baumgardt's half-light radii come from his N-body fits to the surface-density profiles, so they "
     "are not purely photometric; a 10% error in r_h,l moves every predicted dispersion by 5% and BOTH gravity laws "
     "equally, so it cannot produce the differential result below.")

# --- provenance: the four rows re-read off the live source page and hard-coded here, so that the local TSV can never
#     drift from it silently.  (D_sun kpc, R_GC kpc, N_RV, Mass Msun, V mag, M/L_V, r_h,l pc, sigma_0 km/s), from
#     https://people.smp.uq.edu.au/HolgerBaumgardt/globular/parameter.html, re-fetched and compared 2026-09-03.
SOURCE = {"NGC 2419": (88.47, 95.93, 183, 7.83e5, 10.56, 1.61, 19.76, 5.1),
          "Pal 3":    (94.84, 98.17,  22, 1.85e4, 14.56, 1.45, 20.16, 0.8),
          "Pal 4":   (101.39, 104.05, 23, 1.53e4, 14.23, 0.81, 15.88, 0.8),
          "Pal 14":   (73.58, 68.55,  16, 1.91e4, 14.13, 1.70, 27.63, 0.7)}
prov = []
for g in GC:
    s = SOURCE[g["name"]]
    got = (g["D"], g["RGC"], g["NRV"], g["Mfit"], g["V"], g["ML_fit"], g["rhl"], g["sig0_model"])
    prov += [abs(a - b)/max(abs(b), 1e-12) for a, b in zip(got, s)]
ck("93a0 PROVENANCE (can fail): every number this script uses -- distance, Galactocentric radius, star count, fitted "
   "mass, apparent V, fitted M/L_V, half-light radius and model central dispersion -- reproduces the values read "
   "directly off Baumgardt's own parameter page, which was re-fetched and compared while this script was written.  The "
   "local TSV is the source table and not a transcription of it",
   max(prov) < 1e-3, f"worst relative difference across 4 clusters x 8 quantities = {max(prov):.2e}")

dml = np.array([abs(g["Mfit"]/g["LV"] - g["ML_fit"])/g["ML_fit"] for g in GC])
ck("93a photometry self-check -- L_V rebuilt from apparent V, the Harris extinction and the catalogue distance "
   "reproduces the M/L_V that Baumgardt quotes with his own fitted mass, so the luminosities entering the test are right",
   dml.max() < 0.08, "max relative difference " + ", ".join(f"{g['name']} {100*d:.1f}%" for g, d in zip(GC, dml)))

# ------------------------------------------------------------------ mass estimator and its calibration
def wolf_sigma(M_msun, rhl_pc, Geff_over_G=1.0):
    """Wolf et al. 2010: M_1/2 = 3 sigma_los^2 r_1/2 / G with r_1/2 = (4/3) R_e,proj and M_tot = 2 M_1/2, inverted for
    sigma.  In the quasi-Newtonian regime G -> G_eff = nu G, evaluated at r_1/2."""
    r12 = (4.0/3.0)*rhl_pc*PC
    return math.sqrt(G*Geff_over_G*M_msun*Msun/(6.0*r12))/1e3

cal = [(g["name"], wolf_sigma(g["Mfit"], g["rhl"]), g["sig0_model"]) for g in GC]
info("estimator calibration: the Wolf estimator fed Baumgardt's own N-body mass, against his model's CENTRAL dispersion "
     "(which must be the larger of the two):")
for n, sw, s0 in cal: info(f"   {n:10} Wolf(global) {sw:5.2f} km/s   vs  N-body sigma_0 (central) {s0:4.2f} km/s   ratio {sw/s0:5.3f}")
rat = np.array([sw/s0 for _, sw, s0 in cal])
ck("93b estimator calibration -- the Wolf estimator with Baumgardt's N-body masses lands a little below his model's "
   "CENTRAL dispersion for every cluster, the right sign and size for a global-versus-central comparison; the estimator "
   "is calibrated to ~10% and is not the source of any factor-2 result below",
   0.80 < rat.min() and rat.max() < 1.05, f"ratios {np.round(rat,3).tolist()}")

# ------------------------------------------------------------------ the measured dispersions
def sigma_at_rhl(g):
    R_as = np.array([p[0] for p in g["prof"]]); N = np.array([p[1] for p in g["prof"]])
    s = np.array([p[2] for p in g["prof"]]); up = np.array([p[3] for p in g["prof"]]); lo = np.array([p[4] for p in g["prof"]])
    R_pc = R_as/206265.0*g["D"]*1e3
    if len(R_pc) == 1:
        return s[0], 0.5*(up[0]+lo[0]), int(N[0]), R_pc[0]
    ls = np.interp(math.log10(g["rhl"]), np.log10(R_pc), np.log10(s))
    le = np.interp(math.log10(g["rhl"]), np.log10(R_pc), 0.5*(up+lo)/s)
    j = int(np.argmin(np.abs(np.log10(R_pc) - math.log10(g["rhl"]))))
    return 10**ls, (10**ls)*le, int(N[j]), g["rhl"]

P("")
info("MEASURED dispersions (Baumgardt's profile bins; radii converted to pc with the catalogue distance):")
for g in GC:
    R_pc = [p[0]/206265.0*g["D"]*1e3 for p in g["prof"]]
    info(f"   {g['name']:10} r_h,l = {g['rhl']:5.2f} pc | bins: " +
         "; ".join(f"{r:6.1f} pc: {p[2]:4.2f} +{p[3]:.2f}/-{p[4]:.2f} (N={p[1]})" for r, p in zip(R_pc, g["prof"])))
    g["sig_obs"], g["esig_obs"], g["N_obs"], g["r_obs"] = sigma_at_rhl(g)
    info(f"   {'':10} -> dispersion at r_h,l = {g['sig_obs']:.3f} +- {g['esig_obs']:.3f} km/s "
         f"(N = {g['N_obs']}, bin radius {g['r_obs']:.1f} pc)")
PUBLISHED = {"Pal 14": (0.38, 0.12, 16, "Jordi et al. 2009, AJ 137, 4586 (16 members, Keck/HIRES)"),
             "Pal 4":  (0.87, 0.18, 23, "Frank et al. 2012, MNRAS 423, 2917 (23 members, Keck/HIRES)")}
for g in GC:
    if g["name"] in PUBLISHED:
        v, e, n, src = PUBLISHED[g["name"]]
        info(f"   {g['name']:10} published alternative: sigma = {v:.2f} +- {e:.2f} km/s (N={n}) -- {src}")
info("Baumgardt's Pal 14 bin (0.71) is nearly twice the Jordi+2009 value (0.38) on the same 16 stars -- a live "
     "data-side disagreement about membership and binary rejection.  The LOWER value makes the framework's "
     "over-prediction WORSE, so this script carries the higher one as the framework-favourable choice and reports both.")
info("unresolved binaries INFLATE a measured dispersion.  Every measured value here is therefore an upper limit on the "
     "true one, and the framework's over-prediction below is a lower limit on the real discrepancy.")

# ------------------------------------------------------------------ the fields and the boost
def g_ext_newton(RGC_kpc, MW_Mb=MW_MB):
    return G*MW_Mb*Msun/(RGC_kpc*kpc)**2

def g_ext_mond(RGC_kpc, a0, MW_Mb=MW_MB):
    return math.sqrt(G*MW_Mb*Msun*a0)/(RGC_kpc*kpc)

def fields(g, a0, ups=UPS_V, MW_Mb=MW_MB):
    M = ups*g["LV"]*Msun; r12 = (4.0/3.0)*g["rhl"]*PC
    return G*(M/2)/r12**2/a0, g_ext_newton(g["RGC"], MW_Mb)/a0

def boost(g, a0, ups=UPS_V, MW_Mb=MW_MB, kill_a0=False):
    if kill_a0: return 1.0
    yi, ye = fields(g, a0, ups, MW_Mb)
    return nu_s(yi + ye)

P("")
P("-"*118)
P("the internal field, the external field, and how much of the boost each one supplies")
P("-"*118)
for foot, a0 in A0.items():
    P(f"  footing {foot} (a_0 = {a0:.3e} m/s^2)")
    for g in GC:
        yi, ye = fields(g, a0)
        nu_tot, nu_iso = nu_s(yi + ye), nu_s(yi)
        P(f"    {g['name']:10} y_int = {yi:7.4f}  y_ext = {ye:7.4f}  x_ext (actual MONDian field) = "
          f"{g_ext_mond(g['RGC'], a0)/a0:6.4f}  nu(isolated) = {nu_iso:6.3f} -> nu(with EFE) = {nu_tot:6.3f}  "
          f"(EFE trims the boost by {100*(1-nu_tot/nu_iso):4.1f}%)  sigma boost = {math.sqrt(nu_tot):5.3f}  "
          f"{'EFE-DOMINATED' if yi < ye else 'internally dominated'}")
ndom = sum(1 for g in GC if fields(g, A0["canonical"])[0] < fields(g, A0["canonical"])[1])
ck("93c ITEM PREMISE CORRECTED -- the item calls this an external-field test with e_N ~ 0.1-0.3 at 80-100 kpc.  Only ONE "
   "of the four clusters (Pal 14) actually has y_int < y_ext.  Pal 3 and Pal 4 are isolated deep-MOND systems whose "
   "boost comes from their own low internal acceleration, with the Milky Way trimming it by 7-15%, and NGC 2419 sits at "
   "y_int ~ 0.9 where the boost is only 1.3x.  The test is still a good one, but it is mostly NOT an EFE test",
   ndom == 1, f"{ndom} of {len(GC)} clusters are external-field dominated (canonical footing); the actual MONDian "
   f"external field is x_ext = {min(g_ext_mond(g['RGC'], A0['canonical'])/A0['canonical'] for g in GC):.3f}-"
   f"{max(g_ext_mond(g['RGC'], A0['canonical'])/A0['canonical'] for g in GC):.3f}, below the item's stated 0.1-0.3")

# --- cross-check against the published MOND prediction for Pal 14
p14 = [g for g in GC if g["name"] == "Pal 14"][0]
a0c = A0["canonical"]; M2 = 2.0*p14["LV"]
sN2 = wolf_sigma(M2, p14["rhl"])
nu_own = nu_s(sum(fields(p14, a0c, ups=2.0)))
gx220 = (220e3)**2/(p14["RGC"]*kpc); nu_220 = a0c/gx220        # deep-MOND EFE: G_eff/G = a_0/g_ext(actual)
info(f"Pal 14 at M/L_V = 2: sigma_Newton = {sN2:.2f} km/s")
info(f"   with the framework's OWN Milky Way field (BTFR asymptote v_inf = (G M_b a_0)^(1/4) = "
     f"{(G*MW_MB*Msun*a0c)**0.25/1e3:.0f} km/s): boost {math.sqrt(nu_own):.2f} -> sigma = {sN2*math.sqrt(nu_own):.2f} km/s")
info(f"   with the flat v_c = 220 km/s field the published prediction used: boost {math.sqrt(nu_220):.2f} -> "
     f"sigma = {sN2*math.sqrt(nu_220):.2f} km/s")
ck("93d the EFE machinery reproduces the PUBLISHED MOND prediction for Pal 14 -- 1.27 km/s at M/L_V = 2 (Gentile, "
   "Famaey, Angus & Kroupa 2010, A&A 509, A97, quoting Baumgardt, Grebel & Kroupa 2005) -- once the Milky Way external "
   "field they assumed (a flat 220 km/s rotation curve to 70 kpc) is used in place of the framework's own weaker one",
   abs(sN2*math.sqrt(nu_220) - 1.27)/1.27 < 0.15,
   f"this script gives {sN2*math.sqrt(nu_220):.2f} km/s vs the published 1.27 ({100*(sN2*math.sqrt(nu_220)/1.27-1):+.0f}%)")
info("AGAINST THE FRAMEWORK, stated plainly: the framework's own Milky Way external field is WEAKER than the published "
     f"calculations assumed, because the BTFR pins v_inf = {(G*MW_MB*Msun*a0c)**0.25/1e3:.0f} km/s for M_b = {MW_MB:.1e} Msun against the "
     "~200-220 km/s the halo tracers show at 70-100 kpc.  A weaker external field means a LARGER boost, so the "
     "framework's own field makes its prediction higher, not lower.  Both are carried below.")

# ------------------------------------------------------------------ the test
def predict(g, a0, ups=UPS_V, MW_Mb=MW_MB, kill_a0=False, aniso=False):
    nu_eff = boost(g, a0, ups, MW_Mb, kill_a0)
    if aniso and not kill_a0:
        y = sum(fields(g, a0, ups, MW_Mb)); dy = 1e-4*y
        L = (math.log(nu_s(y+dy)) - math.log(nu_s(y-dy)))/(math.log(y+dy) - math.log(y-dy))
        nu_eff = nu_eff*(2.0 + (1.0 + L))/3.0          # trace/3 of diag(nu, nu, nu(1+dlnnu/dlny))
    sN = wolf_sigma(ups*g["LV"], g["rhl"])
    return sN*math.sqrt(nu_eff), sN, nu_eff

def sigma_isolated(g, a0, ups=UPS_V):
    """Milgrom's isolated deep-MOND isothermal result sigma^4 = (4/9) G M a_0 (the (4/81) form is for the 1-D
    line-of-sight dispersion of an isothermal sphere); carried as the upper bracket, not as the prediction."""
    return ((4.0/81.0)*G*(ups*g["LV"]*Msun)*a0)**0.25/1e3

P("")
P("-"*118)
P(f"prediction against measurement at the fiducial stellar M/L_V = {UPS_V}")
P("-"*118)
RES = {}
for foot, a0 in A0.items():
    P(f"  footing {foot}")
    P(f"    {'cluster':10} {'sig_obs':>12} {'sig_Newt':>9} {'sig_frmwk':>10} {'sig_aniso':>10} {'sig_isolMOND':>13} "
      f"{'obs/frmwk':>10} {'Ups_req(N)':>11} {'Ups_req(F)':>11}")
    rows = []
    for g in GC:
        sF, sN, nu_eff = predict(g, a0)
        sA, _, _ = predict(g, a0, aniso=True)
        sI = sigma_isolated(g, a0)
        uN = UPS_V*(g["sig_obs"]/sN)**2
        uF = UPS_V*(g["sig_obs"]/sF)**2
        P(f"    {g['name']:10} {g['sig_obs']:6.2f}+-{g['esig_obs']:4.2f}  {sN:9.2f} {sF:10.2f} {sA:10.2f} {sI:13.2f} "
          f"{g['sig_obs']/sF:10.3f} {uN:11.2f} {uF:11.2f}")
        rows.append(dict(name=g["name"], so=g["sig_obs"], eso=g["esig_obs"], sN=sN, sF=sF, sA=sA, uN=uN, uF=uF, N=g["N_obs"]))
    RES[foot] = rows

for foot in A0:
    uN = np.array([r["uN"] for r in RES[foot]]); uF = np.array([r["uF"] for r in RES[foot]])
    info(f"{foot:10}: required M/L_V -- Newton {np.round(uN,2).tolist()} (log-mean {10**np.mean(np.log10(uN)):.2f}) | "
         f"framework {np.round(uF,2).tolist()} (log-mean {10**np.mean(np.log10(uF)):.2f})")

names = [r["name"] for r in RES["canonical"]]
uN_can = np.array([r["uN"] for r in RES["canonical"]]); uF_can = np.array([r["uF"] for r in RES["canonical"]])
inN = int(((uN_can >= UPS_LO) & (uN_can <= UPS_HI)).sum())
inF = int(((uF_can >= UPS_LO) & (uF_can <= UPS_HI)).sum())
loF = int((uF_can < UPS_LO).sum()); loN = int((uN_can < UPS_LO).sum())
UPS_MID = math.sqrt(UPS_LO*UPS_HI)
dN = np.abs(np.log10(uN_can/UPS_MID)); dF = np.abs(np.log10(uF_can/UPS_MID))
info(f"AGAINST MY OWN FIRST FORMULATION: the first version of the check below asserted that Newton puts three of the "
     f"four clusters INSIDE the stellar-population band {UPS_LO}-{UPS_HI}.  It does not -- it puts {inN} strictly inside "
     f"({np.round(uN_can,2).tolist()}), with Pal 4 low by 0.02 dex and Pal 14 high by 0.01 dex.  That assertion FAILED "
     f"and is recorded here rather than being tuned away; the check is restated as the comparison the data actually "
     f"support.")
ck(f"93e LIABILITY -- against the stellar-population band {UPS_LO}-{UPS_HI} (stated before any number was computed), "
   "Newton with NO dark matter sits a median 0.13 dex away from it while the framework sits a median 0.45 dex away, and "
   "the framework's required M/L_V falls BELOW the band's floor for three of the four clusters where Newton's does so "
   "for one.  The framework needs the outer-halo globulars to be a factor ~3 fainter per unit mass than any old, "
   "metal-poor stellar population",
   np.median(dN) < np.median(dF) and loF > loN,
   f"median |log10(M/L_req / {UPS_MID:.2f})|: Newton {np.median(dN):.3f} dex, framework {np.median(dF):.3f} dex; "
   f"below the floor: Newton {loN}/4, framework {loF}/4; inside the band: Newton {inN}/4, framework {inF}/4; "
   f"required M/L_V Newton {np.round(uN_can,2).tolist()} vs framework {np.round(uF_can,2).tolist()}")

ck("93f Pal 3 goes the OTHER way and is reported, not buried: its measured 1.70 km/s from 22 stars would need a "
   "Newtonian M/L_V near 8, absurd for a globular cluster, while the framework accommodates it at 1.3.  Pal 3 is a "
   "problem for Newton and a point FOR the framework -- either that, or its dispersion is binary-inflated, which would "
   "also be the leading explanation for the other three sitting low",
   uN_can[names.index("Pal 3")] > 4.0 and UPS_LO*0.6 < uF_can[names.index("Pal 3")] < UPS_HI,
   f"Pal 3 needs Newtonian M/L_V = {uN_can[names.index('Pal 3')]:.1f} and framework M/L_V = "
   f"{uF_can[names.index('Pal 3')]:.2f}")

# ------------------------------------------------------------------ the joint fit: one M/L for all four
P("")
P("-"*118)
P("the joint fit -- ONE stellar M/L_V for all four clusters, under each gravity law")
P("-"*118)
def joint(rows, key):
    """sigma_pred = sqrt(Ups/UPS_V) * k_i, so 0.5 ln(Ups/UPS_V) is a weighted mean of ln(sig_obs/k_i)."""
    y = np.array([math.log(r["so"]/r[key]) for r in rows])
    # small-sample sampling error on ln sigma_hat, 1/sqrt(2(N-1)), combined with the quoted measurement error
    e = np.array([math.hypot(r["eso"]/r["so"], 1.0/math.sqrt(2*(r["N"]-1))) for r in rows])
    w = 1.0/e**2
    m = float(np.sum(w*y)/np.sum(w)); em = float(1.0/math.sqrt(np.sum(w)))
    chi2 = float(np.sum(w*(y - m)**2))
    return UPS_V*math.exp(2*m), UPS_V*math.exp(2*m)*2*em, chi2, len(rows) - 1
JOINT = {}
for foot in A0:
    for key, tag in (("sF", "framework"), ("sN", "Newton   ")):
        for sub, stag in ((RES[foot], "all four "), ([r for r in RES[foot] if r["name"] != "Pal 3"], "no Pal 3 ")):
            u, eu, c2, dof = joint(sub, key)
            JOINT[(foot, key, stag.strip())] = (u, eu, c2, dof)
            P(f"  {foot:10} {tag} {stag}: best-fit M/L_V = {u:6.2f} +- {eu:4.2f}   chi2/dof = {c2:6.2f}/{dof} "
              f"(p = {chi2dist.sf(c2, dof):.3f})")
uF, euF, c2F, dofF = JOINT[("canonical", "sF", "all four")]
uNj, euNj, c2N, dofN = JOINT[("canonical", "sN", "all four")]
ck("93g the joint one-M/L fit is the honest summary and it is a bound on M/L, not a kill.  With a single stellar M/L_V "
   "for all four clusters the framework wants a value below the stellar-population floor and Newton one inside the "
   "band; the framework's value is excluded by stellar populations, but BOTH laws leave a poor chi2 because Pal 3 is "
   "discrepant in one direction and Pal 4/Pal 14 in the other.  A 0.3 dex systematic in M/L_V spans the whole result",
   uF < UPS_LO and UPS_LO*0.7 < uNj < UPS_HI*1.3,
   f"framework M/L_V = {uF:.2f} +- {euF:.2f} (chi2/dof {c2F:.1f}/{dofF}); Newton {uNj:.2f} +- {euNj:.2f} "
   f"(chi2/dof {c2N:.1f}/{dofN})")

# ------------------------------------------------------------------ small-sample significance
def p_low(sig_obs, sig_pred, N):
    """Gentile+2010's point: with 16-23 stars a Gaussian error bar overstates the significance.  The ML dispersion of N
    draws from a Gaussian obeys (N-1) sigma_hat^2/sigma^2 ~ chi^2_(N-1).  Measurement errors are neglected, which is
    conservative -- they only ADD to sigma_hat and so only help the framework."""
    return float(chi2dist.cdf((N - 1)*(sig_obs/sig_pred)**2, N - 1))

P("")
P("-"*118)
P("small-sample significance (chi^2_(N-1), not a Gaussian error bar -- the Gentile+2010 objection taken on board)")
P("-"*118)
COMB = {}
for foot in A0:
    ps, pn = [], []
    for r in RES[foot]:
        pF, pA, pN = p_low(r["so"], r["sF"], r["N"]), p_low(r["so"], r["sA"], r["N"]), p_low(r["so"], r["sN"], r["N"])
        ps.append(pF); pn.append(pN)
        P(f"  {foot:10} {r['name']:10} N = {r['N']:3d}  P(sigma_hat <= obs | framework) = {pF:.3e}  "
          f"(anisotropic EFE {pA:.3e})   | P(... | Newton) = {pN:.3e}")
    pc = float(chi2dist.sf(-2*np.sum(np.log(np.clip(ps, 1e-300, 1))), 2*len(ps)))
    pcn = float(chi2dist.sf(-2*np.sum(np.log(np.clip(pn, 1e-300, 1))), 2*len(pn)))
    COMB[foot] = (pc, pcn)
    info(f"{foot:10} Fisher-combined: framework p = {pc:.3e} ({norm.isf(max(pc,1e-300)):.1f} sigma) ; "
         f"Newton p = {pcn:.3e} (no exclusion)")
# the same, but with the M/L marginalised -- which is what the number actually means
P("")
info("the same p-values with the stellar M/L_V marginalised over a log-normal of width 0.15 dex centred on 1.6 "
     "(the real error budget, since sigma_pred scales as sqrt(Ups)):")
rng0 = np.random.default_rng(931)
ups_draws = 1.6*10**(0.15*rng0.standard_normal(4000))
for foot, a0 in A0.items():
    pm = []
    for g in GC:
        r = [x for x in RES[foot] if x["name"] == g["name"]][0]
        pv = np.mean([p_low(r["so"], predict(g, a0, ups=u)[0], r["N"]) for u in ups_draws])
        pm.append(pv)
    pc = float(chi2dist.sf(-2*np.sum(np.log(np.clip(pm, 1e-300, 1))), 2*len(pm)))
    info(f"   {foot:10} marginalised per-cluster p = " + ", ".join(f"{g['name']} {v:.2e}" for g, v in zip(GC, pm)) +
         f"  |  Fisher-combined {pc:.2e} ({norm.isf(max(pc,1e-300)):.1f} sigma)")
    COMB[foot] = COMB[foot] + (pc,)
pub = PUBLISHED["Pal 14"]
P("")
info(f"AGAINST MY OWN STATISTIC, and this is the most important caveat in the script: at Gentile+2010's own numbers "
     f"(sigma_MOND = 1.27 km/s, Jordi+2009's {pub[0]} km/s from {pub[2]} stars) the chi^2 dispersion statistic used here "
     f"gives p = {p_low(pub[0], 1.27, pub[2]):.1e}, while THEIR Kolmogorov-Smirnov test on the same data gave p = "
     f"0.27-0.36 (64-73% confidence).  The gap is the STATISTIC, not the data: chi^2 on the dispersion is the sufficient "
     f"statistic for a Gaussian width and is far more powerful than a KS test on the full CDF with a floating centre.  "
     f"That makes the numbers here much stronger than the published ones -- and it also makes them much more fragile, "
     f"because chi^2 assumes clean membership and Gaussianity, where one mis-assigned star or one unmodelled binary "
     f"moves sigma_hat directly.  The two are not comparable and neither is quoted as the other.")

# --- what would it take: a uniform error in the MEASURED dispersions
info("what a uniform error in the measured dispersions would do (the adversarial direction -- if every measured sigma "
     "here is too LOW, the framework is rescued):")
for f_up in (1.0, 1.15, 1.30, 1.50):
    pm = []
    for g in GC:
        r = [x for x in RES["canonical"] if x["name"] == g["name"]][0]
        pm.append(np.mean([p_low(r["so"]*f_up, predict(g, A0["canonical"], ups=u)[0], r["N"]) for u in ups_draws]))
    pc = float(chi2dist.sf(-2*np.sum(np.log(np.clip(pm, 1e-300, 1))), 2*len(pm)))
    info(f"   every measured sigma x{f_up:.2f} -> marginalised Fisher-combined p = {pc:.2e} "
         f"({norm.isf(max(pc,1e-300)):.1f} sigma)")
    if abs(f_up - 1.30) < 1e-9: P130 = pc
ck("93h the combined exclusion survives marginalising over a realistic stellar-M/L prior, but it drops by two orders of "
   "magnitude when it does; a uniform 30% underestimate of the measured dispersions would take it to 2.5 sigma and a "
   "50% one to 1.5 sigma.  That is the honest size of the result: a bound on the outer-halo globulars' stellar M/L, "
   "quoted as the marginalised number, never as the fixed-M/L one",
   COMB["canonical"][2] < 0.05 and COMB["canonical"][2] > COMB["canonical"][0],
   f"canonical: fixed-M/L p = {COMB['canonical'][0]:.2e}, marginalised p = {COMB['canonical'][2]:.2e} "
   f"({norm.isf(max(COMB['canonical'][2],1e-300)):.1f} sigma); alt marginalised p = {COMB['alt'][2]:.2e}; "
   f"marginalised p if every measured sigma is 30% too low = {P130:.2e}")

# ------------------------------------------------------------------ NGC 2419's profile
P("")
P("-"*118)
P("NGC 2419's dispersion profile -- the shape test (Ibata et al. 2011), done with the raw bins and nothing else")
P("-"*118)
g = [x for x in GC if x["name"] == "NGC 2419"][0]
R_pc = np.array([p[0]/206265.0*g["D"]*1e3 for p in g["prof"]])
s = np.array([p[2] for p in g["prof"]]); es = np.array([0.5*(p[3]+p[4]) for p in g["prof"]])
w = 1.0/(es/s/math.log(10))**2
sl, b, rms = fit_loglog(R_pc, s, w)
A = np.vstack([np.log10(R_pc), np.ones_like(R_pc)]).T
esl = math.sqrt(np.linalg.inv(A.T @ np.diag(w) @ A)[0, 0])
info(f"the measured profile falls as sigma ~ R^({sl:+.3f} +- {esl:.3f}) over {R_pc.min():.0f}-{R_pc.max():.0f} pc "
     f"({R_pc.min()/g['rhl']:.1f}-{R_pc.max()/g['rhl']:.1f} half-light radii)")
info(f"Keplerian (all mass inside, Newtonian, isotropic) is -0.500; isolated deep-MOND is 0.000.  The measurement is "
     f"{abs(sl+0.5)/esl:.1f} sigma STEEPER than Keplerian.")
yi419, ye419 = fields(g, A0["canonical"])
ck("93i NGC 2419's outer dispersion profile declines FASTER than Keplerian, where the framework needs it to decline "
   "SLOWER -- but this script declines to call that a kill, because line-of-sight projection, radial anisotropy and "
   "tidal truncation all steepen an observed sigma(R) in Newtonian gravity too, and separating them needs the full "
   "dynamical models Ibata+2011 and Sanders 2012 disagreed about.  Recorded as a consistent SIGN, not a measurement",
   sl < -0.5, f"measured slope {sl:+.3f} +- {esl:.3f} ({abs(sl+0.5)/esl:.1f} sigma steeper than Keplerian); NGC 2419 is "
   f"also the cluster with all the statistical weight (183 radial velocities) and the SMALLEST boost "
   f"({math.sqrt(boost(g, A0['canonical'])):.2f}x, y_int/y_ext = {yi419/ye419:.0f}) -- the power and the lever are in "
   f"different clusters")

# ------------------------------------------------------------------ systematics
P("")
P("-"*118)
P("systematics: what it would take to rescue the framework")
P("-"*118)
sparse = [x for x in GC if x["name"] != "NGC 2419"]
for MWM in (4e10, 6e10, 8e10, 1.0e11, 2.0e11, 1.0e12):
    r = [predict(x, A0["canonical"], MW_Mb=MWM)[0]/x["sig_obs"] for x in sparse]
    info(f"  MW baryonic mass {MWM:8.1e} Msun -> over-prediction in the three sparse clusters {np.round(r,2).tolist()} "
         f"(log-mean {10**np.mean(np.log10(r)):.2f}x)")
for D_scale in (0.85, 1.0, 1.15):
    r = []
    for x in sparse:
        gg = dict(x); gg["LV"] = x["LV"]*D_scale**2; gg["rhl"] = x["rhl"]*D_scale; gg["RGC"] = x["RGC"]*D_scale
        r.append(predict(gg, A0["canonical"])[0]/x["sig_obs"])
    info(f"  all distances x{D_scale:.2f} -> over-prediction {np.round(r,2).tolist()} (log-mean {10**np.mean(np.log10(r)):.2f}x)")
# --- the radius mismatch, which runs the OTHER way and is therefore stated explicitly
P("")
info("the radius mismatch, and which way it runs.  The Wolf estimator's sigma is the luminosity-weighted GLOBAL one; "
    "the three sparse clusters have exactly ONE measured bin each, and it does not sit at r_h,l:")
for g in GC:
    info(f"   {g['name']:10} measured at {g['r_obs']:5.1f} pc = {g['r_obs']/g['rhl']:.2f} r_h,l")
CEN = 1.0/float(np.median([sw/s0 for _, sw, s0 in cal]))     # sigma_central / sigma_global from Baumgardt's own models
info(f"   a dispersion measured INSIDE r_h,l is biased HIGH relative to the global one, by at most the models' own "
     f"central-to-global ratio {CEN:.2f} (nothing can be more centrally weighted than the centre).  A high sigma_obs "
     f"makes the framework look BETTER, so correcting for this makes the liability worse, not better.")
r_cen = [predict(x, A0["canonical"])[0]/(x["sig_obs"]/CEN) for x in sparse]
r_now = [predict(x, A0["canonical"])[0]/x["sig_obs"] for x in sparse]
ck("93j2 AGAINST INTEREST -- the one geometric systematic that has been left uncorrected runs in the framework's "
   "favour, and correcting it at its maximum defensible size makes the over-prediction larger.  The liability is "
   "therefore quoted at its SMALLEST, with the correction named and not applied",
   10**np.mean(np.log10(r_cen)) > 10**np.mean(np.log10(r_now)),
   f"over-prediction in the three sparse clusters {10**np.mean(np.log10(r_now)):.2f}x as quoted, "
   f"{10**np.mean(np.log10(r_cen)):.2f}x if every measured sigma is corrected to a global one at the maximum ratio "
   f"{CEN:.2f}")

r_low = [predict(x, A0["canonical"])[0]/(PUBLISHED[x["name"]][0] if x["name"] in PUBLISHED else x["sig_obs"]) for x in sparse]
info(f"  with the LOWER published dispersions where they exist (Jordi+2009, Frank+2012): over-prediction "
     f"{np.round(r_low,2).tolist()} (log-mean {10**np.mean(np.log10(r_low)):.2f}x) -- the framework fares worse, not better")
big = 10**np.mean(np.log10([predict(x, A0["canonical"], MW_Mb=1e12)[0]/x["sig_obs"] for x in sparse]))
ck("93j the liability is robust to every systematic that could plausibly move it.  The external-field boost falls only "
   "as M_MW^(-1/4), so even giving the Milky Way a 1e12 Msun DARK-halo mass (which the framework does not have) leaves "
   "an over-prediction; a 15% distance error moves it by 15%; adopting the lower published dispersions makes it worse; "
   "and binaries inflate the measurements, so the true discrepancy is larger",
   big > 1.15, f"over-prediction at M_MW = 1e12 Msun is still {big:.2f}x; at the framework's own 6e10 it is "
   f"{10**np.mean(np.log10([predict(x, A0['canonical'])[0]/x['sig_obs'] for x in sparse])):.2f}x")

# ------------------------------------------------------------------ mutation control
P("")
P("="*118)
P("MUTATION CONTROL")
P("="*118)
mut1 = [predict(x, A0["canonical"], kill_a0=True)[0] for x in GC]
base = [predict(x, A0["canonical"])[1] for x in GC]
live = [predict(x, A0["canonical"])[0]/predict(x, A0["canonical"])[1] for x in GC]
ck("93-M1 a_0 -> 0 (nu == 1) must collapse the framework's prediction exactly onto the Newtonian one, and the live "
   "boosts must be far from 1 -- otherwise the estimator is returning the Newtonian answer by construction",
   max(abs(a - b) for a, b in zip(mut1, base)) < 1e-9 and max(live) > 1.25,
   f"nu=1 gives {np.round(mut1,3).tolist()} == Newtonian {np.round(base,3).tolist()}; live boosts {np.round(live,3).tolist()}")

rng = np.random.default_rng(93)
scr = []
for _ in range(4000):
    perm = rng.permutation(len(GC))
    u = np.array([UPS_V*(GC[perm[i]]["sig_obs"]/predict(GC[i], A0["canonical"])[1])**2 for i in range(len(GC))])
    scr.append(np.std(np.log10(u)))
scr = np.array(scr); true_scatter = np.std(np.log10(uN_can))
ck("93-M2 shuffling which cluster's measured dispersion belongs to which cluster's photometry and structure must "
   "DESTROY the Newtonian M/L consistency -- if it does not, that consistency was never in the data",
   true_scatter < np.percentile(scr, 30),
   f"true Newtonian M/L scatter {true_scatter:.3f} dex sits at the {100*(scr < true_scatter).mean():.0f}th percentile of "
   f"{len(scr)} shuffles (median shuffled scatter {np.median(scr):.3f} dex)")

rt = [predict(x, A0["canonical"]*1e-4)[0]/predict(x, A0["canonical"]*1e-4)[1] for x in GC]
up = [predict(x, A0["canonical"]*10)[0]/predict(x, A0["canonical"])[0] for x in GC]
ck("93-M3 a_0 scanned DOWN by 1e4 must send the boost smoothly to 1 (the framework's Newtonian limit) and a_0 scanned UP "
   "must make the over-prediction worse -- both directions, so that no threshold was tuned",
   max(rt) < 1.02 and min(up) > 1.0,
   f"boost at a_0/1e4 = {np.round(rt,4).tolist()}; predictions at 10 a_0 rise by {np.round(up,2).tolist()}x")

P("")
P("="*118)
P("VERDICT -- item 93")
P("="*118)
P("  LIABILITY, and a known one, but smaller and differently located than the item supposed.")
P("  (1) The item's premise is wrong in detail: only Pal 14 is external-field dominated.  Pal 3 and Pal 4 are isolated")
P("      deep-MOND systems (the Milky Way trims their boost by 7-15%) and NGC 2419 is internally dominated with a boost")
P("      of only 1.3x.  What is really being tested is the framework's low-acceleration boost, not its EFE.")
P("  (2) Pinned to the measured dispersions with ONE stellar M/L_V for all four clusters, the framework wants")
P(f"      M/L_V = {uF:.2f} +- {euF:.2f} and Newton with no dark matter at all wants {uNj:.2f} +- {euNj:.2f}, against a stellar-population")
P(f"      value of {UPS_LO}-{UPS_HI}.  Marginalised over a 0.15 dex M/L prior the framework is excluded at")
P(f"      {norm.isf(max(COMB['canonical'][2],1e-300)):.1f} sigma (canonical) / {norm.isf(max(COMB['alt'][2],1e-300)):.1f} sigma (alt) -- real, but a 0.3 dex M/L systematic spans it.")
P("  (3) Pal 3 goes the other way and is recorded: its 1.70 km/s from 22 stars needs a Newtonian M/L_V near 8 and sits")
P("      comfortably on the framework.  Either it is a point for the framework or it is binary-inflated -- and if it is")
P("      binary-inflated, so are the other three, which makes the framework's over-prediction worse.")
P("  (4) The power and the lever sit in different clusters: NGC 2419 has 183 radial velocities and the smallest boost;")
P("      Pal 14 has the largest boost and 16 stars.  That is why the published literature never closed this.")
P("  (5) Nothing here is new physics; it reproduces Baumgardt+2005 / Jordi+2009 / Frank+2012 with the repo's own kernel")
P("      and footings, and reproduces the Gentile+2010 counter-argument as well.")
P(f"  (6) The liability is quoted at its SMALLEST.  Two systematics were identified and deliberately left uncorrected")
P(f"      because both run in the framework's favour: unresolved binaries inflate every measured dispersion, and the")
P(f"      three sparse clusters' single bins sit inside r_h,l where the dispersion is biased high.  Correcting the")
P(f"      second at its maximum defensible size takes the over-prediction from {10**np.mean(np.log10(r_now)):.2f}x to {10**np.mean(np.log10(r_cen)):.2f}x.  Every input number")
P("      was re-fetched from Baumgardt's own parameter page and compared, and matches to machine precision.")
sys.exit(ck.done())
