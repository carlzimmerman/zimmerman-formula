#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
g05v_adversarial_gc_dispersion_provenance.py
==========================================================================================================
ADVERSARIAL VERIFICATION of check S5 in g05_dsph_prescription_fixed_and_expanded.py.

THE CLAIM UNDER TEST (g05 S5, and item 4 of its verdict):
  "Outer-halo globular clusters, equally pressure-supported but containing no dark matter under LCDM either,
   sit far BELOW the kernel where dwarf spheroidals at the same internal acceleration sit above it.  Support
   type does not predict the sign of the residual; dark-matter content does."
  Quoted numbers: Pal 4 -0.874 (x_i=0.061), Pal 14 -1.306 (x_i=0.013), Pal 3 -0.844 (x_i=0.027),
  NGC 2419 -0.211 (x_i=1.08); MEDIAN -0.859 dex.  Dwarf spheroidals over x_i = 0.01-1.2: median +0.114 on
  N = 12.  "At Upsilon_V = 1 the clusters move to -0.558 dex, still strongly negative."

THE LENS: the estimator and the arithmetic.  g05 hard-codes four observed dispersions.  Where does each one
come from?  This repository's own committed h93_outer_halo_globulars.py reads the SAME two Baumgardt tables
from real_research/data/globular_clusters/ and gets DIFFERENT numbers for two of the four clusters.

WHAT THIS SCRIPT DOES.
  1. Reproduces g05's four residuals bit-for-bit from g05's own hard-coded inputs, with an independent
     re-implementation of the QUMOND sphere average, so any disagreement is g05's arithmetic and not mine.
  2. PROVENANCE: matches each of g05's four hard-coded dispersions against every column of Baumgardt's
     parameter table and every bin of his measured velocity-dispersion profile table, and names which is which.
  3. Recomputes the cluster median under each defensible dispersion choice, including the one h93 -- this
     repository's own committed globular-cluster script -- actually used.
  4. Re-derives the "Upsilon_V = 1" caveat number by rerunning the pipeline instead of adding log10(2).
  5. Asks whether the SIGN of the claim survives all of it.  (It does.  The NUMBERS do not.)

DATA (all already on disk, all cited at point of use):
  Baumgardt & Hilker 2018, MNRAS 478, 1520; Baumgardt & Vasiliev 2021, MNRAS 505, 5957; Baumgardt et al. 2023
    -- real_research/data/globular_clusters/baumgardt_gc_parameters.tsv        (structural, N-body fits)
    -- real_research/data/globular_clusters/baumgardt_gc_veldisp_profiles.tsv  (MEASURED dispersion profiles)
  Jordi et al. 2009, AJ 137, 4586 (Pal 14, 16 members); Frank et al. 2012, MNRAS 423, 2917 (Pal 4, 23 members)
  Harris 2010 (arXiv:1012.3224) extinction; Wolf et al. 2010, MNRAS 406, 1220 (the mass estimator)
  Local Volume Database, Pace 2024, ApJS 273, 15 -- the dwarf-spheroidal comparison side
BOTH a_0 FOOTINGS.  MUTATION CONTROLS.  CHECKS CAN FAIL AND SEVERAL DO.
"""
import sys, math, csv, os
import numpy as np
from hunt_lib import *

ck = Check()
PC = 3.0857e16
MW_MB, M31_MB = 6.0e10, 1.2e11
UPS_V = 2.0
MSUN_V = 4.83
GCDIR = os.path.join(DATA, "globular_clusters")
EBV = {"NGC 2419": 0.08, "Pal 3": 0.04, "Pal 4": 0.01, "Pal 14": 0.04}   # Harris 2010

# ---------------------------------------------------------------------------------------------------------
# independent re-implementation of g05's prescription (written from the QUMOND flux theorem, not copied)
def g_sphere(x_i, x_e, ntheta=4001):
    """<g_r> = <S_r> over a sphere, S = nu(|g_N|/a0) g_N, g_N/a0 = x_e zhat - x_i rhat.  Units of a_0, inward."""
    x_i = max(float(x_i), 1e-300)
    if x_e <= 0.0:
        return nu_s(x_i)*x_i
    th = np.linspace(0.0, math.pi, ntheta)
    st, ct = np.sin(th), np.cos(th)
    gx, gz = -x_i*st, x_e - x_i*ct
    Sr = nu(np.hypot(gx, gz))*(gx*st + gz*ct)
    return -float(np.trapz(Sr*st, th)/np.trapz(st, th))

def g_fm12(x_i, x_e):
    """Famaey & McGaugh 2012, Living Rev. Rel. 15, 10, eq. 60 (Lelli et al. 2015 form)."""
    nt = nu_s(x_i + x_e); ne = nu_s(x_e) if x_e > 0 else 0.0
    return x_i*nt + x_e*(nt - ne)

def gc_row(V, EBVv, Dsun, Rgc, rhl_pc, sig_obs, a0, ups=UPS_V, presc="sphere", r12_pc=None, hostmb=MW_MB):
    """Wolf et al. 2010: g(r_1/2) = 3 sigma^2 / r_1/2, r_1/2 = (4/3) R_e,proj, enclosed baryonic mass M/2."""
    MV = V - 3.1*EBVv - 5*math.log10(Dsun*1e3/10.0)
    LV = 10**(0.4*(MSUN_V - MV)); M = ups*LV
    r12 = (r12_pc if r12_pc is not None else (4.0/3.0)*rhl_pc)*PC
    x_i = G*(0.5*M*Msun)/r12**2/a0
    x_e = G*hostmb*Msun/(Rgc*kpc)**2/a0
    gp = (g_sphere if presc == "sphere" else g_fm12)(x_i, x_e)*a0
    sig_pred = math.sqrt(gp*r12/3.0)/1e3
    return dict(MV=MV, LV=LV, M=M, x_i=x_i, x_e=x_e, sig_pred=sig_pred,
                res=2.0*math.log10(sig_obs/sig_pred))

# g05's hard-coded table, verbatim: name, D_sun kpc, R_GC kpc, V, E(B-V), r_h,l pc, sigma_obs
G05_GC = [("Pal 4",    101.39, 104.05, 14.23, 0.01, 15.88, 0.87),
          ("Pal 14",    73.58,  68.55, 14.13, 0.04, 27.63, 0.38),
          ("Pal 3",     94.84,  98.17, 14.56, 0.04, 20.16, 0.80),
          ("NGC 2419",  88.47,  95.93, 10.56, 0.08, 19.76, 5.10)]
G05_QUOTED = {"Pal 4": -0.874, "Pal 14": -1.306, "Pal 3": -0.844, "NGC 2419": -0.211}
a0c = A0["canonical"]

P("="*120)
P("PART 1.  REPRODUCING g05's FOUR NUMBERS INDEPENDENTLY.  If I cannot, the bug is arithmetic and I say where.")
P("="*120)
info(f"{'cluster':10} {'M_V':>7} {'L_V':>10} {'x_i':>8} {'x_e':>8} {'sig_pred':>9} {'my dex':>8} {'g05 dex':>8} {'diff':>8}")
mine, dmax = {}, 0.0
for nm, D, R, V, E, rhl, so in G05_GC:
    r = gc_row(V, E, D, R, rhl, so, a0c)
    mine[nm] = r; d = r["res"] - G05_QUOTED[nm]; dmax = max(dmax, abs(d))
    info(f"{nm:10} {r['MV']:7.2f} {r['LV']:10.3e} {r['x_i']:8.4f} {r['x_e']:8.5f} {r['sig_pred']:9.2f} "
         f"{r['res']:+8.3f} {G05_QUOTED[nm]:+8.3f} {d:+8.4f}")
med_g05 = float(np.median([mine[n]["res"] for n in G05_QUOTED]))
ck("V1 g05's four cluster residuals and its median reproduce EXACTLY under an independent re-implementation of the "
   "same prescription, so there is no coding error inside g05's globular-cluster block.  Whatever is wrong with the "
   "claim is wrong in the INPUTS, not in the arithmetic that consumes them",
   dmax < 0.002 and abs(med_g05 - (-0.859)) < 0.002,
   f"worst per-cluster difference {dmax:.4f} dex; my median {med_g05:+.3f} against g05's quoted -0.859")

# ---------------------------------------------------------------------------------------------------------
P(""); P("="*120)
P("PART 2.  PROVENANCE.  Where does each of g05's four hard-coded dispersions actually come from?")
P("="*120)
par = {}
for line in open(os.path.join(GCDIR, "baumgardt_gc_parameters.tsv"), encoding="utf-8"):
    if line.startswith("#") or line.startswith("ClusterName"): continue
    f = line.rstrip("\n").split("\t"); par[f[0]] = f
prof = {}
for line in open(os.path.join(GCDIR, "baumgardt_gc_veldisp_profiles.tsv"), encoding="utf-8"):
    if line.startswith("#") or line.startswith("ClusterName"): continue
    f = line.rstrip("\n").split("\t")
    if f[6] != "RV": continue
    prof.setdefault(f[0], []).append((float(f[1]), int(f[2]), float(f[3]), float(f[4]), float(f[5])))

info("Baumgardt's parameter table column 22 is sigma0[km/s] -- the CENTRAL velocity dispersion of his fitted")
info("N-body MODEL.  His separate profile table carries the MEASURED dispersion in radial bins, with star counts.")
info("The Wolf et al. 2010 estimator that g05 inverts wants the dispersion AT r_1/2, not the model centre.")
P("")
info(f"{'cluster':10} {'g05 used':>9} {'sigma0 (MODEL)':>15} {'measured bins (R arcsec: sigma, N)':>52} {'at r_hl':>9}")
def sig_at_rhl(nm, rhl_pc, Dkpc):
    """log-log interpolate the measured profile to r_h,l; a single-bin cluster returns that bin."""
    b = sorted(prof[nm]); Rpc = [p[0]/206265.0*Dkpc*1e3 for p in b]; s = [p[2] for p in b]
    if len(b) == 1: return s[0], b[0][1], Rpc[0]
    lg = np.interp(math.log10(rhl_pc), np.log10(Rpc), np.log10(s))
    return float(10**lg), sum(p[1] for p in b), rhl_pc
prov_rows = []
for nm, D, R, V, E, rhl, so in G05_GC:
    s0 = float(par[nm][21])
    sr, Nr, Rr = sig_at_rhl(nm, rhl, D)
    bins = "; ".join(f"{p[0]:.0f}\": {p[2]:.2f} (N={p[1]})" for p in sorted(prof[nm]))
    prov_rows.append((nm, so, s0, sr, Nr, bins))
    info(f"{nm:10} {so:9.2f} {s0:15.2f} {bins:>52} {sr:9.3f}")
info("")
info("PUBLISHED DIRECT MEASUREMENTS, carried alongside: Pal 14 sigma = 0.38 +- 0.12 km/s from 16 members")
info("   (Jordi et al. 2009, AJ 137, 4586); Pal 4 sigma = 0.87 +- 0.18 km/s from 23 members (Frank et al. 2012,")
info("   MNRAS 423, 2917).  Baumgardt's own bins on the SAME stars give 0.71 and 0.88.")

is_model = {nm: abs(so - s0) < 1e-9 for nm, so, s0, sr, Nr, b in prov_rows}
nmodel = sum(is_model.values())
ck("V2 (THE PROVENANCE IS NOT WHAT THE CLAIM SAYS IT IS) g05 describes Pal 3 and NGC 2419 as coming 'from "
   "Baumgardt's own N-body fits'.  They come from ONE COLUMN of that fit -- sigma0, the MODEL CENTRAL dispersion -- "
   "and g05 then feeds that central value into a Wolf et al. 2010 estimator that is defined at the half-light "
   "radius.  Baumgardt's separately tabulated MEASURED dispersions for those same two clusters exist, are in this "
   "repository, and are used by this repository's own committed h93_outer_halo_globulars.py",
   nmodel == 2 and all(is_model[n] for n in ("Pal 3", "NGC 2419")),
   f"exact column matches to sigma0: " + ", ".join(f"{n}={'sigma0' if is_model[n] else 'not sigma0'}" for n in G05_QUOTED))

d3_model, d3_meas = 0.80, float(prof["Pal 3"][0][2])
ck("V3 (THE SMOKING GUN, AND IT FAILS) for Pal 3 the model central dispersion g05 uses and the measured dispersion "
   "Baumgardt tabulates from the SAME 22 stars the model was fitted to disagree by a factor of more than two.  "
   "Pal 3 is the ONE cluster of the four whose measurement the N-body model does not reproduce -- for Pal 4 and "
   "Pal 14 the model sigma0 and the measured bin agree to 10 per cent -- and it is precisely that cluster where g05 "
   "substitutes the model number for the measurement.  The substitution moves Pal 3 by 0.65 dex in the direction "
   "that supports the claim.  This repository's own h93 uses the measured 1.70 and states in its check 93f that "
   "'Pal 3 goes the OTHER way ... a problem for Newton and a point FOR the framework'",
   abs(d3_meas/d3_model - 1.0) < 0.15,
   f"Pal 3: g05 uses sigma = {d3_model:.2f} km/s (Baumgardt sigma0, model central); Baumgardt's MEASURED bin is "
   f"{d3_meas:.2f} +0.38/-0.30 km/s from 22 stars at 11.1 pc.  Ratio {d3_meas/d3_model:.2f}, i.e. "
   f"{2*math.log10(d3_meas/d3_model):+.3f} dex in acceleration.  For comparison the model reproduces the measurement "
   f"for Pal 4 ({float(par['Pal 4'][21]):.2f} vs {prof['Pal 4'][0][2]:.2f}) and Pal 14 "
   f"({float(par['Pal 14'][21]):.2f} vs {prof['Pal 14'][0][2]:.2f})")

s2419_rhl = sig_at_rhl("NGC 2419", 19.76, 88.47)[0]
ck("V4 (an APERTURE error, this repository's own listed bug pattern, and it fails) NGC 2419's dispersion profile "
   "falls by a factor 3.4 from 16 pc to 92 pc.  g05 uses the model CENTRAL dispersion 5.10 km/s as if it were the "
   "dispersion at the half-light radius 19.76 pc.  Interpolating Baumgardt's measured profile to r_h,l gives 4.77 "
   "km/s.  Small on its own -- 0.06 dex -- but it is the same class of substitution as V3 and it also runs toward "
   "the claim",
   abs(5.10 - s2419_rhl) < 0.10,
   f"NGC 2419: g05 uses 5.10 km/s (model central); measured profile interpolated to r_h,l = 19.76 pc gives "
   f"{s2419_rhl:.2f} km/s, i.e. {2*math.log10(s2419_rhl/5.10):+.3f} dex")

ck("V5 (the Pal 14 choice, disclosed by g05 but made the OPPOSITE way to this repository's own convention) g05 "
   "takes the LOWER of the two dispersions available for Pal 14 (Jordi et al. 2009, 0.38 km/s) where Baumgardt's "
   "bin on the SAME 16 stars gives 0.71.  h93 carries the HIGHER value and says so explicitly: 'The LOWER value "
   "makes the framework's over-prediction WORSE, so this script carries the higher one as the framework-favourable "
   "choice.'  g05 reverses that convention without saying it did, and it is worth 0.54 dex on the most extreme of "
   "the four points",
   abs(2*math.log10(0.71/0.38)) < 0.20,
   f"Pal 14: Jordi 0.38 vs Baumgardt bin 0.71 on the same 16 stars = {2*math.log10(0.71/0.38):+.3f} dex; g05's "
   f"quoted -1.306 becomes {mine['Pal 14']['res'] + 2*math.log10(0.71/0.38):+.3f}")

# ---------------------------------------------------------------------------------------------------------
P(""); P("="*120)
P("PART 3.  THE MEDIAN UNDER EVERY DEFENSIBLE DISPERSION CHOICE, BOTH FOOTINGS.")
P("="*120)
CHOICES = {
 "g05 as published (Frank, Jordi, sigma0, sigma0)":
    {"Pal 4": 0.87, "Pal 14": 0.38, "Pal 3": 0.80, "NGC 2419": 5.10},
 "h93's choice: Baumgardt MEASURED bins at r_h,l":
    {"Pal 4": 0.88, "Pal 14": 0.71, "Pal 3": 1.70, "NGC 2419": round(s2419_rhl, 3)},
 "direct published where it exists, measured otherwise":
    {"Pal 4": 0.87, "Pal 14": 0.38, "Pal 3": 1.70, "NGC 2419": round(s2419_rhl, 3)},
 "MODEL sigma0 for all four (fully model-dependent)":
    {n: float(par[n][21]) for n in G05_QUOTED},
}
GEOM = {n: (D, R, V, E, rhl) for n, D, R, V, E, rhl, so in G05_GC}
med_by_choice = {}
for foot, a0 in A0.items():
    P(""); info(f"FOOTING {foot}  (a_0 = {a0:.3g} m/s^2)")
    info(f"{'dispersion choice':56} " + " ".join(f"{n:>10}" for n in G05_QUOTED) + f" {'MEDIAN':>9}")
    for lab, sig in CHOICES.items():
        rr = {}
        for n in G05_QUOTED:
            D, R, V, E, rhl = GEOM[n]
            rr[n] = gc_row(V, E, D, R, rhl, sig[n], a0)["res"]
        m = float(np.median(list(rr.values()))); med_by_choice[(foot, lab)] = m
        info(f"{lab:56} " + " ".join(f"{rr[n]:+10.3f}" for n in G05_QUOTED) + f" {m:+9.3f}")

mg05 = med_by_choice[("canonical", "g05 as published (Frank, Jordi, sigma0, sigma0)")]
mh93 = med_by_choice[("canonical", "h93's choice: Baumgardt MEASURED bins at r_h,l")]
ck("V6 (THE QUOTED MEDIAN IS WRONG BY 0.34 DEX AND THE ERROR RUNS TOWARD THE CLAIM) replacing the two model "
   "central dispersions and the low Pal 14 value with the measured dispersions this repository already has on disk "
   "-- the ones its own h93 uses -- moves the cluster median from the quoted -0.859 dex to about -0.52.  Two of the "
   "four quoted per-cluster numbers change by more than half a dex: Pal 3 from -0.844 to about -0.19 and Pal 14 "
   "from -1.306 to about -0.76.  The claim's headline arithmetic does not stand as published",
   abs(mh93 - mg05) < 0.10,
   f"canonical: g05 as published {mg05:+.3f} dex; on the measured dispersions {mh93:+.3f} dex; difference "
   f"{mh93-mg05:+.3f}.  Every one of the four substitutions moves the median UP (less negative), i.e. every one of "
   f"g05's input choices ran toward its own conclusion")

# ---------------------------------------------------------------------------------------------------------
P(""); P("="*120)
P("PART 4.  THE 'Upsilon_V = 1' CAVEAT, RE-DERIVED RATHER THAN ASSUMED.")
P("="*120)
info("g05 reports the Upsilon_V = 1 median as median(residual) + log10(2).  That is the NEWTONIAN scaling: it")
info("assumes g_pred is proportional to the mass.  Three of the four clusters sit at x_i = 0.013-0.061, deep in")
info("the modified regime, where d ln(nu(x) x)/d ln x is about 0.54-0.56, not 1.  The correct shift is smaller.")
info(f"{'Upsilon_V':>10} {'Pal 4':>9} {'Pal 14':>9} {'Pal 3':>9} {'NGC 2419':>10} {'MEDIAN':>9}")
ups_med = {}
for ups in (1.0, 1.6, 2.0):
    rr = {}
    for n in G05_QUOTED:
        D, R, V, E, rhl = GEOM[n]
        rr[n] = gc_row(V, E, D, R, rhl, dict(G05_GC and CHOICES["g05 as published (Frank, Jordi, sigma0, sigma0)"])[n],
                       a0c, ups=ups)["res"]
    ups_med[ups] = float(np.median(list(rr.values())))
    info(f"{ups:10.1f} {rr['Pal 4']:+9.3f} {rr['Pal 14']:+9.3f} {rr['Pal 3']:+9.3f} {rr['NGC 2419']:+10.3f} {ups_med[ups]:+9.3f}")
claimed_u1 = -0.859 + math.log10(2.0)
ck("V7 (AN ARITHMETIC ERROR IN THE STATED CAVEAT, and this one runs AGAINST the claim) g05's caveat says the "
   "clusters move to -0.558 dex at Upsilon_V = 1, obtained by adding log10(2).  Rerunning the pipeline at "
   "Upsilon_V = 1 gives about -0.69, because in the modified regime halving the mass lowers the predicted "
   "acceleration by only about a factor 1.5, not 2.  The stated caveat number is 0.13 dex too forgiving of the "
   "author's own point; the true Upsilon_V = 1 median is MORE negative than advertised",
   abs(ups_med[1.0] - claimed_u1) < 0.03,
   f"rerun at Upsilon_V = 1 gives median {ups_med[1.0]:+.3f} dex; the quoted 'median + log10(2)' gives "
   f"{claimed_u1:+.3f}; error {claimed_u1 - ups_med[1.0]:+.3f} dex.  At Upsilon_V = 1.6 (h93's fiducial) "
   f"{ups_med[1.6]:+.3f}, at 2.0 {ups_med[2.0]:+.3f}")

# ---------------------------------------------------------------------------------------------------------
P(""); P("="*120)
P("PART 5.  THE DWARF-SPHEROIDAL SIDE OF THE COMPARISON, REBUILT INDEPENDENTLY.")
P("="*120)
def fnum(v):
    try:
        x = float(v)
        return x if np.isfinite(x) else None
    except (TypeError, ValueError):
        return None
def load_lvd(fname, host_mb, host_name):
    out = []
    for r in csv.DictReader(open(os.path.join(DATA, "dsph", fname))):
        sig = fnum(r["vlos_sigma"]); ul = fnum(r["vlos_sigma_ul"])
        MV = fnum(r["M_V"]); rh = fnum(r["rhalf_sph_physical"]) or fnum(r["rhalf_physical"])
        Dh = fnum(r["distance_host"]) or fnum(r["distance_gc"])
        if sig is None or ul is not None or MV is None or rh is None or sig <= 0 or rh <= 0: continue
        if fnum(r["confirmed_galaxy"]) != 1: continue
        lMs = fnum(r["mass_stellar"]); lMHI = fnum(r["mass_HI"])
        out.append(dict(name=r["name"], MV=MV, rh=rh, sig=sig,
                        Ms=(10**lMs if lMs is not None else 10**(0.4*(4.83-MV))*UPS_V),
                        MHI=(10**lMHI if lMHI is not None else 0.0),
                        Dhost=Dh, Dgc=fnum(r["distance_gc"]), Dm31=fnum(r["distance_m31"]),
                        host=host_name, host_mb=host_mb))
    return out
mw_all  = load_lvd("lvd_dwarf_mw.csv",  MW_MB,  "MW")
m31_all = load_lvd("lvd_dwarf_m31.csv", M31_MB, "M31")
fld_all = load_lvd("lvd_dwarf_local_field.csv", None, "field")
ROTATING_EXCLUDE = {"LMC", "SMC"}
DISRUPTING = {"Sagittarius", "Bootes III", "Tucana III", "Tucana IV"}
def classify(d, host):
    if d["name"] in ROTATING_EXCLUDE or d["name"] in DISRUPTING: return None
    if d["MHI"] > 0.3*max(d["Ms"], 1): return None
    if host == "field": return "isolated"
    if host == "M31":   return "m31"
    return "classical" if d["MV"] <= -7.7 else "ultrafaint"
classes = {"classical": [], "ultrafaint": [], "m31": [], "isolated": []}
for src, host in ((mw_all, "MW"), (m31_all, "M31"), (fld_all, "field")):
    for d in src:
        c = classify(d, host)
        if c: classes[c].append(d)
def dsph_row(d, a0):
    r12 = (4.0/3.0)*d["rh"]*PC
    Mb = d["Ms"] + 1.33*d["MHI"]
    x_i = G*(0.5*Mb*Msun)/r12**2/a0
    hm = d["host_mb"]
    if hm is not None and d["Dhost"] and d["Dhost"] > 0:
        x_e = G*hm*Msun/(d["Dhost"]*kpc)**2/a0
    else:
        x_e = ((G*MW_MB*Msun/(d["Dgc"]*kpc)**2 if d["Dgc"] else 0.0) +
               (G*M31_MB*Msun/(d["Dm31"]*kpc)**2 if d["Dm31"] else 0.0))/a0
    return math.log10(3.0*(d["sig"]*1e3)**2/r12/(g_sphere(x_i, x_e)*a0)), x_i
over = sorted([(d["name"],) + dsph_row(d, a0c) for k in ("classical", "m31", "isolated") for d in classes[k]
               if 0.01 <= dsph_row(d, a0c)[1] <= 1.2], key=lambda t: t[2])
info(f"dwarf spheroidals with 0.01 <= x_i <= 1.2 (the clusters' range), N = {len(over)}:")
for n, r, xi in over: info(f"      {n:22} x_i = {xi:.4f}   {r:+7.3f} dex")
med_over = float(np.median([t[1] for t in over]))
ck("V8 the dwarf-spheroidal side of g05's comparison reproduces independently: N = 12 objects over the clusters' "
   "internal-acceleration range with a median of +0.114 dex.  The dwarf side of the claim is not where the problem is",
   len(over) == 12 and abs(med_over - 0.114) < 0.01,
   f"N = {len(over)}, median {med_over:+.3f} dex against g05's quoted +0.114 on N = 12")

# ---------------------------------------------------------------------------------------------------------
P(""); P("="*120)
P("PART 6.  DOES THE SIGN OF THE CLAIM SURVIVE?  Every dispersion choice x every Upsilon_V x both footings.")
P("="*120)
worst = None
info(f"{'dispersion choice':56} {'Ups':>5} {'foot':>10} {'GC median':>10} {'dSph med':>9} {'gap':>8}")
rows_all = []
for lab, sig in CHOICES.items():
    for ups in (1.0, 1.6, 2.0):
        for foot, a0 in A0.items():
            rr = []
            for n in G05_QUOTED:
                D, R, V, E, rhl = GEOM[n]
                rr.append(gc_row(V, E, D, R, rhl, sig[n], a0, ups=ups)["res"])
            mgc = float(np.median(rr))
            ov = [dsph_row(d, a0)[0] for k in ("classical", "m31", "isolated") for d in classes[k]
                  if 0.01 <= dsph_row(d, a0)[1] <= 1.2]
            md = float(np.median(ov))
            rows_all.append((lab, ups, foot, mgc, md, md - mgc))
            if worst is None or mgc > worst[3]: worst = rows_all[-1]
for lab, ups, foot, mgc, md, gap in rows_all:
    info(f"{lab:56} {ups:5.1f} {foot:>10} {mgc:+10.3f} {md:+9.3f} {gap:+8.3f}")
ck("V9 (AND THIS ONE PASSES -- THE DIRECTION OF THE CLAIM SURVIVES EVERYTHING I CAN THROW AT IT) under every "
   "dispersion choice, every stellar mass-to-light ratio from 1 to 2, and both a_0 footings, the outer-halo "
   "globular clusters still sit BELOW the kernel and the dwarf spheroidals at the same internal acceleration still "
   "sit above it.  The qualitative statement -- support type does not predict the sign of the residual -- is not "
   "refuted by the input errors.  Only the numbers are",
   max(r[3] for r in rows_all) < -0.15 and min(r[5] for r in rows_all) > 0.25,
   f"least negative cluster median over all {len(rows_all)} combinations: {worst[3]:+.3f} dex "
   f"({worst[0]}, Ups={worst[1]}, {worst[2]}); smallest dwarf-minus-cluster gap {min(r[5] for r in rows_all):+.3f} dex")

alt_presc = []
for n in G05_QUOTED:
    D, R, V, E, rhl = GEOM[n]
    alt_presc.append(gc_row(V, E, D, R, rhl, CHOICES["h93's choice: Baumgardt MEASURED bins at r_h,l"][n], a0c,
                            presc="fm12")["res"])
ck("V10 the prescription systematic g05 itself flags (its own P4 and S2, the 0.28 dex spread between the exact "
   "sphere average and the published one-dimensional formula) does not rescue the clusters either",
   float(np.median(alt_presc)) < -0.15,
   f"on the measured dispersions: sphere average {mh93:+.3f} dex, FM12 eq.60 {float(np.median(alt_presc)):+.3f} dex")

# ---------------------------------------------------------------------------------------------------------
P(""); P("="*120)
P("PART 7.  MUTATION CONTROLS.")
P("="*120)
def gc_newt(V, EBVv, Dsun, rhl_pc, sig_obs, ups=UPS_V):
    """nu = 1 everywhere: the prediction must collapse to Newton, so the residual becomes log10(M_dyn/M_bar)."""
    MV = V - 3.1*EBVv - 5*math.log10(Dsun*1e3/10.0)
    M = ups*10**(0.4*(MSUN_V - MV)); r12 = (4.0/3.0)*rhl_pc*PC
    return 2*math.log10(sig_obs/(math.sqrt(G*(0.5*M*Msun)/r12**2*r12/3.0)/1e3))
newt = [gc_newt(GEOM[n][2], GEOM[n][3], GEOM[n][0], GEOM[n][4],
                CHOICES["h93's choice: Baumgardt MEASURED bins at r_h,l"][n], ups=1.6) for n in G05_QUOTED]
ck("M1 MUTATION CONTROL: with nu = 1 the same pipeline is plain Newtonian gravity, and on the measured "
   "dispersions at a stellar-population Upsilon_V = 1.6 the four clusters must sit near zero -- they contain no "
   "dark matter.  They do, which is the independent evidence that the geometry, the estimator and the photometry "
   "in this script are right and that the negative MOND residual is the boost and not a bookkeeping error",
   abs(float(np.median(newt))) < 0.25,
   "Newtonian residuals at Ups=1.6: " + ", ".join(f"{n} {v:+.3f}" for n, v in zip(G05_QUOTED, newt)) +
   f"; median {float(np.median(newt)):+.3f} dex")

sq2 = []
for n in G05_QUOTED:
    D, R, V, E, rhl = GEOM[n]
    s = CHOICES["g05 as published (Frank, Jordi, sigma0, sigma0)"][n]
    sq2.append(gc_row(V, E, D, R, rhl, s*math.sqrt(2), a0c)["res"] - gc_row(V, E, D, R, rhl, s, a0c)["res"])
ck("M2 MUTATION CONTROL on the data: inflating every cluster dispersion by sqrt(2) must move every residual by "
   "exactly +log10(2) and nothing else may respond",
   max(abs(v - math.log10(2.0)) for v in sq2) < 1e-9,
   f"max deviation {max(abs(v - math.log10(2.0)) for v in sq2):.2e} dex")

r12_alt = []
for n in G05_QUOTED:
    D, R, V, E, rhl = GEOM[n]
    rhm = float(par[n][12])                      # Baumgardt's own 3-D half-MASS radius
    r12_alt.append(abs(rhm/((4.0/3.0)*rhl) - 1.0))
ck("M3 GEOMETRY CONTROL: the (4/3) deprojection g05 applies to the projected half-light radius must land on "
   "Baumgardt's independently tabulated 3-D half-MASS radius.  It does, to 3 per cent, for all four clusters.  The "
   "radius is NOT one of the errors here",
   max(r12_alt) < 0.05,
   "(4/3) r_h,l against tabulated r_h,m: " + ", ".join(f"{n} {100*v:.1f}%" for n, v in zip(G05_QUOTED, r12_alt)))

newt_model = [gc_newt(GEOM[n][2], GEOM[n][3], GEOM[n][0], GEOM[n][4], float(par[n][21]), ups=1.6)
              for n in G05_QUOTED]
newt_meas  = [gc_newt(GEOM[n][2], GEOM[n][3], GEOM[n][0], GEOM[n][4],
                      CHOICES["h93's choice: Baumgardt MEASURED bins at r_h,l"][n], ups=1.6) for n in G05_QUOTED]
ck("M4 (THE CIRCULARITY, AND IT FAILS) Baumgardt's sigma0 is the output of a NEWTONIAN N-body model fitted to the "
   "cluster.  Substituting it for a measurement therefore imports the Newtonian answer by construction: at "
   "Upsilon_V = 1.6 the four sigma0 values scatter by only 0.10 dex about Newton, where the four MEASURED "
   "dispersions scatter by 0.35 dex.  A quantity that is Newtonian by construction cannot be used as the observed "
   "side of a test of whether gravity is Newtonian.  If Pal 3's 22-star measurement is thought unreliable -- and at "
   "a Newtonian M/L_V near 8 it may well be binary-inflated -- the honest move is to DROP Pal 3, not to replace it "
   "with a Newtonian model output; dropping it leaves the cluster median at the Pal 4 / NGC 2419 / Pal 14 value",
   float(np.std(newt_model, ddof=1)) > 0.5*float(np.std(newt_meas, ddof=1)),
   f"Newtonian residuals at Ups=1.6 from MODEL sigma0: " + ", ".join(f"{n} {v:+.3f}" for n, v in zip(G05_QUOTED, newt_model)) +
   f" (scatter {float(np.std(newt_model, ddof=1)):.3f}); from MEASURED bins: " +
   ", ".join(f"{n} {v:+.3f}" for n, v in zip(G05_QUOTED, newt_meas)) + f" (scatter {float(np.std(newt_meas, ddof=1)):.3f})")

drop3 = sorted([r for n, r in zip(G05_QUOTED, [gc_row(*GEOM[n][2:4], GEOM[n][0], GEOM[n][1], GEOM[n][4],
                CHOICES["h93's choice: Baumgardt MEASURED bins at r_h,l"][n], a0c)["res"] for n in G05_QUOTED])
                if n != "Pal 3"])
info(f"   Pal 3 dropped entirely, measured dispersions elsewhere: residuals " +
     ", ".join(f"{v:+.3f}" for v in drop3) + f", median {float(np.median(drop3)):+.3f} dex")

ov_alt = [dsph_row(d, A0["alt"])[0] for k in ("classical", "m31", "isolated") for d in classes[k]
          if 0.01 <= dsph_row(d, A0["alt"])[1] <= 1.2]
ck("M5 (BOTH-FOOTINGS VIOLATION, AND IT FAILS) g05's check S5 is computed on the canonical footing ONLY -- a0c is "
   "hard-coded in its globular-cluster block and in the dwarf comparison set it is compared against.  On the alt "
   "footing a_0 = 1.13e-10 the dwarf spheroidals over the clusters' acceleration range sit essentially ON the "
   "kernel, not above it.  The clusters stay below on both footings, so the GAP survives, but the half of the "
   "claim that says the dwarfs 'sit above it' at these accelerations holds on one footing of the two",
   abs(float(np.median(ov_alt))) > 0.05,
   f"dwarf median over 0.01 <= x_i <= 1.2: canonical {med_over:+.3f} dex on N={len(over)}, "
   f"alt {float(np.median(ov_alt)):+.3f} dex on N={len(ov_alt)}")

P(""); P("="*120); P("VERDICT")
P("="*120)
P("  THE CLAIM'S DIRECTION SURVIVES.  ITS NUMBERS DO NOT.")
P("")
P(f"  The arithmetic inside g05's globular-cluster block is correct: I reproduce all four residuals and the")
P(f"  median -0.859 to {dmax:.4f} dex with an independent implementation (V1).  The errors are in the INPUTS.")
P("")
P(f"  1. Pal 3.  g05 uses 0.80 km/s, which is column 22 of Baumgardt's parameter table -- sigma0, the CENTRAL")
P(f"     dispersion of his fitted N-body MODEL -- and feeds it to a Wolf et al. 2010 estimator defined at the")
P(f"     half-light radius.  Baumgardt's MEASURED dispersion for Pal 3, from the same 22 stars, is 1.70")
P(f"     +0.38/-0.30 km/s.  Pal 3 is the only one of the four where model and measurement disagree (they agree")
P(f"     to 10 per cent for Pal 4 and Pal 14), and it is the one g05 replaces.  Pal 3 goes from -0.844 to")
P(f"     {gc_row(*GEOM['Pal 3'][2:4], GEOM['Pal 3'][0], GEOM['Pal 3'][1], GEOM['Pal 3'][4], 1.70, a0c)['res']:+.3f}.")
P(f"     This repository's own committed h93 uses 1.70 and concludes the opposite about Pal 3 (its check 93f).")
P(f"  2. NGC 2419.  Same substitution, smaller: the model central 5.10 km/s used at r_h,l where the measured")
P(f"     profile interpolates to {s2419_rhl:.2f}.  An aperture error, {2*math.log10(s2419_rhl/5.10):+.3f} dex.")
P(f"  3. Pal 14.  g05 takes the lower of two dispersions for the same 16 stars, reversing h93's stated")
P(f"     convention of carrying the framework-favourable one.  Worth {2*math.log10(0.71/0.38):+.3f} dex.")
P(f"  4. The Upsilon_V = 1 caveat is computed as median + log10(2), the Newtonian scaling, on objects at")
P(f"     x_i = 0.013-0.061 where the correct exponent is about 0.55.  Rerun, it is {ups_med[1.0]:+.3f}, not -0.558.")
P("")
P(f"  NET: the quoted median -0.859 dex becomes {mh93:+.3f} dex on the measured dispersions this repository")
P(f"  already holds on disk -- a {mh93 - mg05:+.3f} dex correction.  Two of the four quoted per-cluster numbers")
P(f"  move by more than half a dex.  ALL FOUR input choices ran toward the claim.")
P("")
P(f"  WHAT STILL STANDS (V9, V10, M1).  Under every dispersion choice, Upsilon_V from 1 to 2, both footings and")
P(f"  both external-field prescriptions, the clusters remain below the kernel (worst case {worst[3]:+.3f} dex) and")
P(f"  the dwarf spheroidals at the same x_i remain above it, with a gap of at least")
P(f"  {min(r[5] for r in rows_all):+.3f} dex.  The Newtonian mutation puts the clusters on zero at Ups = 1.6,")
P(f"  which is what a dark-matter-free system should do.  So 'support type does not predict the sign of the")
P(f"  residual' is NOT refuted -- but it must be quoted at a cluster median near {mh93:+.2f} dex, not -0.86, and")
P(f"  Pal 3 must be quoted as the object that argues the other way, not as a -0.844 point in favour.")
sys.exit(ck.done())
