#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
g05v_gc_discriminant_adversarial.py -- ADVERSARIAL AUDIT of check S5 in g05_dsph_prescription_fixed_and_expanded.py
====================================================================================================================
THE CLAIM UNDER ATTACK (g05 check S5, and item 4 of g05's verdict):

  "Outer-halo globular clusters, equally pressure-supported but containing no dark matter under LCDM either, sit far
   BELOW the kernel where dwarf spheroidals at the same internal acceleration sit above it.  Support type does not
   predict the sign of the residual; DARK-MATTER CONTENT does."
   Numbers: Pal 4 -0.874, Pal 14 -1.306, Pal 3 -0.844, NGC 2419 -0.211; median -0.859 dex.  dSph over the same
   x_i = 0.01-1.2: median +0.114 dex on N=12.

MY JOB IS TO REFUTE IT.  I attack the INFERENCE on seven fronts.  A check here PASSES when the claim SURVIVES that
attack and FAILS when the attack LANDS.  Two of the seven land, and one of them lands hard.

  V1  TRANSCRIPTION.  Rebuild g05's four clusters from the on-disk Baumgardt catalogue instead of its literal tuple.
  V2  THE DISPERSIONS THEMSELVES -- and THIS IS WHERE THE CLAIM BREAKS.  g05 took four dispersions from four
      different places: two from the literature and two from the "sigma0" column of the Baumgardt PARAMETER table.
      That column is the CENTRAL dispersion of a fitted NEWTONIAN N-body model, which is exactly my brief's named
      failure mode (a quantity derived under the theory being tested).  The repository ALSO holds Baumgardt's
      MEASURED velocity-dispersion PROFILES -- the file's own header says "These are the DATA, not model curves".
      Use the measured bin at each cluster's half-light radius, which is what the Wolf estimator asks for.
  V3  SAMPLE SELECTION.  Four clusters hand-picked from a 157-cluster catalogue that is on disk.  Run every cluster
      meeting pre-stated, answer-blind criteria through the identical pipeline.
  V4  THE MASS-TO-LIGHT DECOMPOSITION.  Split each residual into the Newtonian M/L part (which says nothing about
      this framework) and the kernel-boost part (which does).
  V5  IS THE "MATCH" A MATCH?  Test the x_i overlap of the two classes, and the exact-permutation significance.
  V6  THE DISCRIMINANT.  Is "dark-matter content" identified against the degenerate alternatives (baryonic mass,
      physical size), and is it an independent variable on the dwarf side at all?
  V7  BOTH FOOTINGS AND MUTATION CONTROLS.

DATA, all public, all on disk:
  Baumgardt & Hilker 2018 (MNRAS 478, 1520); Baumgardt & Vasiliev 2021 (MNRAS 505, 5957); Baumgardt et al. 2020,2023
    -- globular_clusters/baumgardt_gc_parameters.tsv and baumgardt_gc_veldisp_profiles.tsv (retrieved 2026-09-03)
  Local Volume Database, Pace 2024 ApJS 273, 15 -- dsph/lvd_dwarf_*.csv
  Frank et al. 2012, MNRAS 423, 2917 (Pal 4, 23 members); Jordi et al. 2009, AJ 137, 4586 (Pal 14, 16-17 members)
  Wolf et al. 2010, MNRAS 406, 1220 (the mass estimator); Harris 2010 (arXiv:1012.3224) reddenings.

BOTH a_0 FOOTINGS.  MUTATION CONTROLS.  CHECKS CAN FAIL AND THREE DO.
"""
import sys, math, csv, os, re
import numpy as np
from itertools import combinations
from hunt_lib import *

ck = Check()
rng = np.random.default_rng(20260903)

MW_MB, M31_MB = 6.0e10, 1.2e11   # host baryonic masses, Msun (McGaugh 2016, ApJ 816, 42) -- g05's values
UPS_V = 2.0                      # g05's assumed photometric stellar M/L_V
PC    = 3.0857e16
GCF   = os.path.join(DATA, "globular_clusters", "baumgardt_gc_parameters.tsv")
VDF   = os.path.join(DATA, "globular_clusters", "baumgardt_gc_veldisp_profiles.tsv")
a0c   = A0["canonical"]

# --- g05's prescription, lifted verbatim so I attack ITS number and not a different one -------------------------
def g_qumond_sphere(x_i, x_e, ntheta=2001):
    x_i = max(float(x_i), 1e-300)
    if x_e <= 0.0:
        return nu_s(x_i)*x_i
    th = np.linspace(0.0, math.pi, ntheta)
    st, ctm = np.sin(th), np.cos(th)
    gx, gz = -x_i*st, x_e - x_i*ctm
    Sr = nu(np.sqrt(gx*gx + gz*gz))*(gx*st + gz*ctm)
    return -float(np.trapz(Sr*st, th)/np.trapz(st, th))

def gc_row(LV, Dsun_kpc, Rgc_kpc, rhl_pc, sig_kms, a0, ups=UPS_V):
    """Wolf et al. 2010 estimator on a cluster.  Returns (residual dex, x_i, x_e, sigma_pred, M_phot, r12_m)."""
    M   = ups*LV
    r12 = (4.0/3.0)*rhl_pc*PC
    xi  = G*(0.5*M*Msun)/r12**2/a0
    xe  = G*MW_MB*Msun/(Rgc_kpc*kpc)**2/a0
    sp  = math.sqrt(g_qumond_sphere(xi, xe)*a0*r12/3.0)/1e3
    return 2.0*math.log10(sig_kms/sp), xi, xe, sp, M, r12

# ===============================================================================================================
P("="*122)
P("V1.  TRANSCRIPTION.  Rebuild g05's four clusters from the on-disk Baumgardt catalogue, not its literal tuple.")
P("="*122)

def bnum(s):
    """Baumgardt cells: '1.53 +- 0.28 · 104' means 1.53e4 (the '104' is 10^4)."""
    s = s.strip()
    if not s or s == "-": return float("nan")
    exp = 0.0
    if "·" in s:
        base, _, tail = s.partition("·")
        te = re.search(r"10\s*(\d+)", tail.replace(" ", ""))
        if te: exp = float(te.group(1))
        s = base
    m = re.match(r"\s*([-+]?\d+\.?\d*)", s.strip())
    return float(m.group(1))*10.0**exp if m else float("nan")

CAT, header = {}, None
for line in open(GCF, encoding="latin-1"):
    if line.startswith("#"): continue
    parts = line.rstrip("\n").split("\t")
    if header is None: header = parts; continue
    if len(parts) < 23: continue
    d = dict(zip(header, parts))
    nm = d["ClusterName"].split("  ")[0].strip()
    CAT[nm] = dict(name=nm, Dsun=bnum(d["R_sun[kpc]"]), Rgc=bnum(d["R_GC[kpc]"]), NRV=bnum(d["N_RV"]),
                   Mdyn=bnum(d["Mass[Msun]"]), V=bnum(d["V[mag]"]), MLV=bnum(d["M/L_V"]),
                   rhl=bnum(d["rh_l[pc]"]), sig0=bnum(d["sigma0[km/s]"]))
info(f"Baumgardt parameter rows parsed: {len(CAT)}")

# Harris 2010 E(B-V), the values g05 hard-codes; used only to reproduce g05's L_V.
EBV     = {"Pal 4": 0.01, "Pal 14": 0.04, "Pal 3": 0.04, "NGC 2419": 0.08}
SIG_G05 = {"Pal 4": 0.87, "Pal 14": 0.38, "Pal 3": 0.80, "NGC 2419": 5.10}
SRC_G05 = {"Pal 4": "Frank et al. 2012, 23 members (LITERATURE)",
           "Pal 14": "Jordi et al. 2009, 16-17 members (LITERATURE)",
           "Pal 3": "Baumgardt sigma0 column = NEWTONIAN N-BODY MODEL",
           "NGC 2419": "Baumgardt sigma0 column = NEWTONIAN N-BODY MODEL"}
G05_QUOTED = {"Pal 4": -0.874, "Pal 14": -1.306, "Pal 3": -0.844, "NGC 2419": -0.211}
G05_XI     = {"Pal 4": 0.0610, "Pal 14": 0.0130, "Pal 3": 0.0270, "NGC 2419": 1.0800}
FOUR = ("Pal 4", "Pal 14", "Pal 3", "NGC 2419")

info(f"{'cluster':10} {'Dsun':>7} {'Rgc':>7} {'V':>6} {'rh_l':>6} {'my dex':>9} {'g05 dex':>9} {'diff':>8} {'my x_i':>9} {'g05 x_i':>8}")
rebuilt, dmax, ximax = {}, 0.0, 0.0
for nm in FOUR:
    c = CAT[nm]
    MV = c["V"] - 5*math.log10(c["Dsun"]*1e3/10.0) - 3.1*EBV[nm]
    LV = 10**(0.4*(4.83 - MV))
    r, xi, xe, sp, M, r12 = gc_row(LV, c["Dsun"], c["Rgc"], c["rhl"], SIG_G05[nm], a0c)
    rebuilt[nm] = dict(res=r, xi=xi, xe=xe, sp=sp, M=M, r12=r12, LV=LV, sig=SIG_G05[nm], cat=c)
    dmax = max(dmax, abs(r - G05_QUOTED[nm])); ximax = max(ximax, abs(xi - G05_XI[nm])/G05_XI[nm])
    info(f"{nm:10} {c['Dsun']:7.2f} {c['Rgc']:7.2f} {c['V']:6.2f} {c['rhl']:6.2f} {r:+9.3f} {G05_QUOTED[nm]:+9.3f} "
         f"{r-G05_QUOTED[nm]:+8.4f} {xi:9.4f} {G05_XI[nm]:8.4f}")
ck("V1 the four hard-coded clusters are faithful transcriptions of the on-disk Baumgardt catalogue: rebuilding them "
   "from the file reproduces every residual to a thousandth of a dex.  There is no data-entry error to find, so the "
   "attack has to be on the inference and on the choice of inputs, not on the arithmetic",
   dmax < 0.002 and ximax < 0.05,
   f"worst residual difference {dmax:.4f} dex; worst fractional x_i difference {100*ximax:.1f} per cent, which is "
   f"g05's own rounding of x_i to three decimals in its printed table")

# ===============================================================================================================
P(""); P("="*122)
P("V2.  THE DISPERSIONS.  Two of g05's four are outputs of a NEWTONIAN N-BODY FIT.  The MEASURED profiles are on disk.")
P("="*122)
info("g05's four dispersions come from three different kinds of source, and it says so:")
for nm in FOUR: info(f"   {nm:10} sigma = {SIG_G05[nm]:.2f} km/s   {SRC_G05[nm]}")
info("")
info("The 'sigma0' column of the Baumgardt PARAMETER table is the central dispersion of his fitted N-body model,")
info("and those models are NEWTONIAN.  My brief names this failure mode explicitly: a quantity derived under the")
info("theory being tested cannot be used at face value to test a competitor.  But the repository also holds")
info("baumgardt_gc_veldisp_profiles.tsv, whose own header reads: 'MEASURED velocity dispersion profiles ... These")
info("are the DATA, not model curves.'  Type RV rows are line-of-sight dispersions from the member velocities.")
info("The Wolf et al. 2010 estimator wants the dispersion at the half-light radius, so take the RV profile there.")

PROF, hdr = {}, None
for line in open(VDF, encoding="latin-1"):
    if line.startswith("#"): continue
    parts = line.rstrip("\n").split("\t")
    if hdr is None: hdr = parts; continue
    if len(parts) < 7 or parts[6].strip() != "RV": continue
    try:
        PROF.setdefault(parts[0].strip(), []).append((float(parts[1]), int(parts[2]), float(parts[3])))
    except ValueError:
        continue
for k in PROF: PROF[k].sort()
info(f"clusters with at least one MEASURED (type RV) dispersion bin: {len(PROF)}")

def sigma_at_rhl(nm, c):
    """Measured LOS dispersion at the projected half-light radius, log-log interpolated across the RV bins
    (clamped to the end bins).  Returns (sigma_kms, n_stars_total, n_bins, R_e_arcsec)."""
    bins = PROF.get(nm)
    if not bins: return None
    Re_as = c["rhl"]/(c["Dsun"]*1e3)*206265.0
    R = np.array([b[0] for b in bins]); N = np.array([b[1] for b in bins]); S = np.array([b[2] for b in bins])
    if len(bins) == 1:
        s = float(S[0])
    else:
        s = float(np.exp(np.interp(math.log(Re_as), np.log(R), np.log(S))))
    return s, int(N.sum()), len(bins), Re_as

info("")
info(f"{'cluster':10} {'R_e (as)':>9} {'RV bins (R arcsec: N, sigma)':>44} {'sigma(R_e)':>11} {'g05 sigma':>10} {'ratio':>7}")
meas = {}
for nm in FOUR:
    c = CAT[nm]
    s, ntot, nb, Re_as = sigma_at_rhl(nm, c)
    meas[nm] = s
    bl = "; ".join(f"{b[0]:.0f}: {b[1]}, {b[2]:.2f}" for b in PROF[nm])
    info(f"{nm:10} {Re_as:9.1f} {bl:>44} {s:11.2f} {SIG_G05[nm]:10.2f} {s/SIG_G05[nm]:7.2f}")

info("")
info("Recomputing the four residuals with the MEASURED dispersion at R_e, everything else identical to g05:")
info(f"{'cluster':10} {'g05 dex':>9} {'measured dex':>13} {'change':>9}")
res_meas = {}
for nm in FOUR:
    c = CAT[nm]
    r = gc_row(rebuilt[nm]["LV"], c["Dsun"], c["Rgc"], c["rhl"], meas[nm], a0c)[0]
    res_meas[nm] = r
    info(f"{nm:10} {rebuilt[nm]['res']:+9.3f} {r:+13.3f} {r-rebuilt[nm]['res']:+9.3f}")
med_g05  = float(np.median([rebuilt[nm]["res"] for nm in FOUR]))
med_meas = float(np.median([res_meas[nm] for nm in FOUR]))
ck("V2 (THE ATTACK LANDS, AND IT IS THE ONE THAT MATTERS) g05's four dispersions are a MIXTURE of literature values "
   "and two entries from the sigma0 column of the Baumgardt parameter table, which is a fitted NEWTONIAN N-body "
   "model's central dispersion.  Replacing all four with the MEASURED dispersion at the half-light radius, from the "
   "measured-profile file already sitting in this repository, moves the median by more than half a dex.  Pal 3 alone "
   "moves by +0.65 dex: its measured dispersion is 1.70 km/s from 22 stars where g05 used the model's 0.80.  Pal 14 "
   "moves by +0.53: Baumgardt's compilation of the SAME stars Jordi et al. measured gives 0.71, not 0.38.  A headline "
   "number that halves when you swap a model output for the measurement it was fitted to is not a measured number",
   abs(med_meas - med_g05) < 0.15,
   f"g05 median {med_g05:+.3f} dex -> measured-dispersion median {med_meas:+.3f} dex, a shift of {med_meas-med_g05:+.3f}.  "
   "Per cluster: " + ", ".join(f"{nm} {rebuilt[nm]['res']:+.3f}->{res_meas[nm]:+.3f}" for nm in FOUR))

# ===============================================================================================================
P(""); P("="*122)
P("V3.  SAMPLE SELECTION.  Four clusters chosen by hand out of 157 that are sitting on disk.")
P("="*122)
info("PRE-STATED, ANSWER-BLIND CRITERIA, fixed before any residual was computed:")
info("   (i)   a MEASURED (type RV) dispersion profile with at least 15 member velocities in total;")
info("   (ii)  x_e = G M_MW,bar / R_GC^2 / a_0 < 1, so the external field does not quench the kernel to Newton and")
info("         the object can actually test something;")
info("   (iii) x_i inside the SAME 0.01 <= x_i <= 1.2 band g05 used to define its dwarf-spheroidal comparison set.")
info("No cut on R_GC, on how famous the cluster is, or on which way the residual points.")
info("")
info("L_V is taken as M_dyn / (M/L_V) from the catalogue, which recovers Baumgardt's own DEREDDENED luminosity")
info("exactly and removes extinction as an error source (a first pass of this audit set A_V = 0 and produced")
info("nonsense for reddened bulge clusters -- e.g. Liller 1 at 57 Msun -- which is why that route was abandoned).")

pool = []
for nm, c in CAT.items():
    if not all(np.isfinite(c[k]) for k in ("Dsun", "Rgc", "rhl", "Mdyn", "MLV")): continue
    if c["rhl"] <= 0 or c["MLV"] <= 0: continue
    got = sigma_at_rhl(nm, c)
    if got is None: continue
    s, ntot, nb, Re_as = got
    if ntot < 15 or s <= 0: continue
    LV = c["Mdyn"]/c["MLV"]
    r, xi, xe, sp, M, r12 = gc_row(LV, c["Dsun"], c["Rgc"], c["rhl"], s, a0c)
    if xe >= 1.0 or not (0.01 <= xi <= 1.2): continue
    pool.append(dict(name=nm, res=r, xi=xi, xe=xe, sig=s, ntot=ntot, nb=nb, Rgc=c["Rgc"],
                     MLV=c["MLV"], M=M, r12=r12))
pool.sort(key=lambda d: d["xi"])
info("")
info(f"ALL catalogue clusters meeting the criteria: N = {len(pool)}")
info(f"{'cluster':16} {'N_RV':>5} {'bins':>5} {'R_GC':>7} {'x_i':>8} {'x_e':>7} {'sig(Re)':>8} {'M(Ups=2)':>10} {'M/L_dyn':>8} {'dex':>8}")
for d in pool:
    star = "  <- in g05" if d["name"] in G05_QUOTED else ""
    info(f"{d['name']:16} {d['ntot']:5d} {d['nb']:5d} {d['Rgc']:7.1f} {d['xi']:8.4f} {d['xe']:7.3f} {d['sig']:8.2f} "
         f"{d['M']:10.2e} {d['MLV']:8.2f} {d['res']:+8.3f}{star}")
pres = np.array([d["res"] for d in pool])
neg = int((pres < 0).sum())
in4 = [d["res"] for d in pool if d["name"] in G05_QUOTED]
out4 = [d["res"] for d in pool if d["name"] not in G05_QUOTED]
med_in = float(np.median(in4)) if in4 else float("nan")
med_out = float(np.median(out4)) if out4 else float("nan")
ck("V3 (THE SELECTION ATTACK DOES NOT LAND, AND I RECORD THAT IT DOES NOT) I expected g05's four to be the extreme "
   "tail of their own population -- they are, after all, exactly the four the MOND literature has flagged for twenty "
   "years (Baumgardt et al. 2005, ApJ 634, 1093; Ibata et al. 2011, ApJ 738, 186; Sanders 2012, MNRAS 419, L6).  "
   "They are not.  Expanding to every catalogue cluster meeting answer-blind criteria, on measured dispersions, "
   "17 of 20 are still negative and the sixteen clusters g05 did NOT use sit within a tenth of a dex of the four it "
   "did.  The class-level statement is real; only the -0.859 magnitude is not, and that is V2's doing, not selection",
   len(pool) >= 6 and neg >= 0.8*len(pool) and abs(med_in - med_out) < 0.3,
   f"N = {len(pool)} clusters, {neg} negative ({100*neg/len(pool):.0f} per cent), median {float(np.median(pres)):+.3f} dex, "
   f"range {pres.min():+.3f} to {pres.max():+.3f}.  g05's four inside this pool: median {med_in:+.3f}; the "
   f"{len(out4)} it did not use: median {med_out:+.3f}; difference {med_in-med_out:+.3f} dex")

# ===============================================================================================================
P(""); P("="*122)
P("V4.  THE MASS-TO-LIGHT DECOMPOSITION.  How much of the residual is the kernel and how much is Upsilon_V = 2?")
P("="*122)
info("g_obs/g_pred = [g_obs / g_Newt(Ups_V L)] x [1/boost].  The first bracket is a purely NEWTONIAN statement --")
info("log10 of the dynamical-to-assumed-photometric mass ratio -- and says nothing about this framework.  Only the")
info("second is the kernel's prediction.  If the first carried most of the residual, the claim would be about M/L.")
info(f"{'cluster':10} {'g05 dex':>9} {'log10 boost':>12} {'Newt part':>10} {'M/L needed':>11} {'Baumgardt M/L_V':>16}")
newt, kern = [], []
for nm in FOUR:
    b = rebuilt[nm]
    gN = G*(0.5*b["M"]*Msun)/b["r12"]**2
    boost = math.log10(g_qumond_sphere(b["xi"], b["xe"])*a0c/gN)
    npart = b["res"] + boost
    newt.append(npart); kern.append(-boost)
    info(f"{nm:10} {b['res']:+9.3f} {boost:12.3f} {npart:+10.3f} {UPS_V*10**npart:11.2f} {b['cat']['MLV']:16.2f}")
frac_newt, frac_kern = float(np.median(newt)), float(np.median(kern))
ck("V4 (THE ATTACK DOES NOT LAND) I expected the assumed Upsilon_V = 2 to be carrying most of the cluster deficit, "
   "because these mass-segregated outer-halo clusters have low dynamical M/L.  It is not: the Newtonian M/L part is "
   "a small minority of the residual and the kernel's own boost carries the great majority of it.  This attack fails "
   "and I record that it fails -- to the extent the clusters ARE below the kernel, it is the kernel doing it",
   abs(frac_newt) < 0.4*abs(frac_kern),
   f"median Newtonian M/L part {frac_newt:+.3f} dex against median kernel-boost part {-frac_kern:+.3f} dex, i.e. the "
   f"M/L assumption is {100*abs(frac_newt)/abs(med_g05):.0f} per cent of the quoted -0.859.  Upsilon_V these clusters "
   f"would need under Newton: " + ", ".join(f"{nm} {UPS_V*10**newt[i]:.2f}" for i, nm in enumerate(FOUR)))

info("")
info("The Upsilon_V scan, on g05's own dispersions, since Upsilon_V is the only free knob on the cluster side:")
info(f"{'Upsilon_V':>10} " + " ".join(f"{nm:>10}" for nm in FOUR) + f" {'median':>9}")
ups_med = {}
for ups in (0.8, 1.0, 1.5, 2.0, 3.0):
    row = [gc_row(rebuilt[nm]["LV"], CAT[nm]["Dsun"], CAT[nm]["Rgc"], CAT[nm]["rhl"], SIG_G05[nm], a0c, ups=ups)[0]
           for nm in FOUR]
    ups_med[ups] = float(np.median(row))
    info(f"{ups:10.1f} " + " ".join(f"{v:+10.3f}" for v in row) + f" {ups_med[ups]:+9.3f}")
ck("V4b g05's own Upsilon_V = 1 caveat is an ASSERTED number where a computed one belongs, and it is wrong -- though "
   "wrong AGAINST g05's own point.  g05 shifted the median by log10(2) = 0.301, which is the NEWTONIAN response to "
   "halving the mass; three of its four clusters are in the modified regime where the response is smaller.  The "
   "correctly recomputed Upsilon_V = 1 median is more negative than g05 claims, not less",
   abs(ups_med[1.0] - (med_g05 + math.log10(2.0))) < 0.05,
   f"g05 asserts -0.558 at Upsilon_V = 1; recomputed it is {ups_med[1.0]:+.3f}.  Full scan: " +
   ", ".join(f"Ups={u}: {ups_med[u]:+.3f}" for u in sorted(ups_med)))

# ===============================================================================================================
P(""); P("="*122)
P("V5.  IS THE 'MATCH' A MATCH?  The dwarf-spheroidal comparison set, rebuilt, and the overlap tested.")
P("="*122)

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

ROTATING_EXCLUDE = {"LMC", "SMC"}
DISRUPTING = {"Sagittarius", "Bootes III", "Tucana III", "Tucana IV"}
def classify(d, host):
    if d["name"] in ROTATING_EXCLUDE or d["name"] in DISRUPTING: return None
    if d["MHI"] > 0.3*max(d["Ms"], 1): return None
    if host == "field": return "isolated"
    if host == "M31":   return "m31"
    return "classical" if d["MV"] <= -7.7 else "ultrafaint"

classes = {"classical": [], "ultrafaint": [], "m31": [], "isolated": []}
for src, host in ((load_lvd("lvd_dwarf_mw.csv", MW_MB, "MW"), "MW"),
                  (load_lvd("lvd_dwarf_m31.csv", M31_MB, "M31"), "M31"),
                  (load_lvd("lvd_dwarf_local_field.csv", None, "field"), "field")):
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
    g_obs = 3.0*(d["sig"]*1e3)**2/r12
    return math.log10(g_obs/(g_qumond_sphere(x_i, x_e)*a0)), x_i, x_e, Mb, r12

dov = []
for k in ("classical", "m31", "isolated"):
    for d in classes[k]:
        r, xi, xe, Mb, r12 = dsph_row(d, a0c)
        if 0.01 <= xi <= 1.2:
            dov.append(dict(name=d["name"], res=r, xi=xi, Mb=Mb, r12=r12, cls=k, sig=d["sig"]))
dov.sort(key=lambda z: z["xi"])
info(f"dwarf spheroidals with 0.01 <= x_i <= 1.2 (g05's comparison set): N = {len(dov)}, median "
     f"{float(np.median([d['res'] for d in dov])):+.3f} dex   [g05 quotes N = 12, +0.114 -- reproduced]")
info(f"{'dwarf':22} {'class':10} {'x_i':>8} {'M_b':>10} {'r_1/2 pc':>9} {'residual':>9}")
for d in dov:
    info(f"{d['name']:22} {d['cls']:10} {d['xi']:8.4f} {d['Mb']:10.2e} {d['r12']/PC:9.1f} {d['res']:+9.3f}")

gc4 = [rebuilt[n] for n in FOUR]
xg = np.array([b["xi"] for b in gc4]); xd = np.array([d["xi"] for d in dov])
mg = np.array([b["M"] for b in gc4]);  md = np.array([d["Mb"] for d in dov])
rg = np.array([b["r12"] for b in gc4]); rd = np.array([d["r12"] for d in dov])
frac_inside = float(np.mean([(xd.min() <= v <= xd.max()) for v in xg]))
info("")
info(f"   x_i       clusters {np.median(xg):.4f} ({xg.min():.4f}-{xg.max():.4f})   "
     f"dwarfs {np.median(xd):.4f} ({xd.min():.4f}-{xd.max():.4f})   median ratio {np.median(xd)/np.median(xg):.2f}")
info(f"   M_b/Msun  clusters {np.median(mg):.2e}   dwarfs {np.median(md):.2e}   "
     f"{math.log10(np.median(md)/np.median(mg)):.2f} dex apart")
info(f"   r_1/2/pc  clusters {np.median(rg)/PC:.0f}   dwarfs {np.median(rd)/PC:.0f}   "
     f"{math.log10(np.median(rd)/np.median(rg)):.2f} dex apart")
ck("V5a the acceleration match is a real match and not a slogan: the two classes' x_i distributions overlap, their "
   "medians sit within a factor 2, and three of the four clusters lie inside the dwarfs' own x_i range",
   0.33 < np.median(xd)/np.median(xg) < 3.0 and frac_inside >= 0.7,
   f"cluster x_i {xg.min():.4f}-{xg.max():.4f} against dwarf x_i {xd.min():.4f}-{xd.max():.4f}; median ratio "
   f"{np.median(xd)/np.median(xg):.2f}; {int(frac_inside*4)} of 4 clusters inside the dwarf range")

def exact_sep_p(gcvals, dvals):
    allr = np.array(list(gcvals) + [d["res"] for d in dvals]); n1 = len(gcvals)
    idx = list(range(len(allr)))
    obs = float(np.median(allr[:n1]) - np.median(allr[n1:]))
    ex = [abs(float(np.median(allr[list(c)]) - np.median(allr[[i for i in idx if i not in c]])))
          for c in combinations(idx, n1)]
    return obs, float(np.mean(np.array(ex) >= abs(obs))), len(ex)

sep_g05, p_g05, ncomb = exact_sep_p([b["res"] for b in gc4], dov)
sep_ms, p_ms, _       = exact_sep_p([res_meas[nm] for nm in FOUR], dov)
info("")
info(f"   exact permutation over all C(16,4) = {ncomb} label assignments:")
info(f"      on g05's dispersions:      separation {sep_g05:+.3f} dex, p = {p_g05:.4f}")
info(f"      on MEASURED dispersions:   separation {sep_ms:+.3f} dex, p = {p_ms:.4f}")
ck("V5b (THE SIGN SURVIVES THE DISPERSION SWAP, EVEN THOUGH THE SIZE DOES NOT) with the measured dispersions the "
   "separation shrinks by more than half a dex, but the clusters still sit below the dwarfs and the exact "
   "permutation test still rejects at the two-sigma level.  So the DIRECTION of g05's S5 survives V2 even though its "
   "magnitude does not",
   p_ms < 0.05 and sep_ms < 0.0,
   f"g05 dispersions: {sep_g05:+.3f} dex, p = {p_g05:.4f}.  Measured dispersions: {sep_ms:+.3f} dex, p = {p_ms:.4f} "
   f"over {ncomb} exact assignments")

# ===============================================================================================================
P(""); P("="*122)
P("V6.  THE DISCRIMINANT.  Is it DARK-MATTER CONTENT, or one of several perfectly degenerate labels?")
P("="*122)
info("The claim is not merely 'clusters sit below'.  It is that the SIGN is predicted by DARK-MATTER CONTENT rather")
info("than by support type.  For that to be a discriminant, dark-matter content must be identified against every")
info("other variable that separates the two classes.  It is not.")
sep_M = float(np.median([math.log10(d["Mb"]) for d in dov]) - np.median([math.log10(b["M"]) for b in gc4]))
sep_R = float(np.median([math.log10(d["r12"]) for d in dov]) - np.median([math.log10(b["r12"]) for b in gc4]))
ov_M = sum(1 for d in dov if d["Mb"] <= max(b["M"] for b in gc4))
ov_R = sum(1 for d in dov if d["r12"] <= max(b["r12"] for b in gc4))
info(f"   baryonic mass: {sep_M:.2f} dex apart, {ov_M} of {len(dov)} dwarfs overlapping the cluster range")
info(f"   physical size: {sep_R:.2f} dex apart, {ov_R} of {len(dov)} dwarfs overlapping the cluster range")
ck("V6a (THE ATTACK LANDS) at matched internal acceleration the two classes are ALSO separated by more than two "
   "decades in baryonic mass and more than one in physical size, with ZERO overlap in either.  'Dark-matter "
   "content', 'baryonic mass' and 'physical size' are three names for the same partition of these sixteen objects.  "
   "A two-class comparison cannot tell them apart, so naming dark matter as THE predictor is a choice and not a "
   "measurement -- a kernel that failed as a function of system size or of baryonic mass, which would be a framework "
   "LIABILITY rather than a vindication of dark matter, fits this data exactly as well",
   ov_M > 0.25*len(dov) or ov_R > 0.25*len(dov),
   f"baryonic-mass separation {sep_M:.2f} dex with {ov_M}/{len(dov)} overlap; size separation {sep_R:.2f} dex with "
   f"{ov_R}/{len(dov)} overlap.  Two classes, three degenerate candidate predictors, no power to separate them")

fdm, resd = [], []
for k in ("classical", "m31", "isolated"):
    for d in classes[k]:
        r, xi, xe, Mb, r12 = dsph_row(d, a0c)
        if not (0.01 <= xi <= 1.2): continue
        fdm.append(math.log10(3.0*(d["sig"]*1e3)**2*r12/G/Msun/Mb)); resd.append(r)
fdm, resd = np.array(fdm), np.array(resd)
rr = float(np.corrcoef(fdm, resd)[0, 1]); sl = float(np.polyfit(fdm, resd, 1)[0])
info("")
info("And the dark-matter variable is not independent on the dwarf side: a dwarf's dark-matter content is measured")
info("as M_dyn/M_bar with M_dyn = 3 sigma^2 r_1/2 / G -- the SAME sigma and r_1/2 that build the residual.")
ck("V6b (THE ATTACK LANDS) inside the dwarf sample the residual and the dark-matter fraction are two monotone "
   "functions of one number: M_dyn is built from the very sigma and r_1/2 that build the residual.  They correlate at "
   "r = 0.95 BY CONSTRUCTION, not by physics.  'Dark-matter content predicts the residual' is therefore near-"
   "tautological wherever dark-matter content is inferred dynamically.  The only non-circular half of the claim is "
   "the cluster side, where 'no dark matter' is a structure-formation statement rather than a dynamical inference",
   abs(rr) < 0.8,
   f"log10(M_dyn/M_bar) against residual on the {len(fdm)} matched dwarfs: r = {rr:+.3f}, slope {sl:+.3f} dex per dex")

# ===============================================================================================================
P(""); P("="*122)
P("V7.  BOTH FOOTINGS, AND THE MUTATION CONTROLS.")
P("="*122)
foot = {}
for fname, a0 in A0.items():
    g05v = [gc_row(rebuilt[nm]["LV"], CAT[nm]["Dsun"], CAT[nm]["Rgc"], CAT[nm]["rhl"], SIG_G05[nm], a0)[0] for nm in FOUR]
    msv  = [gc_row(rebuilt[nm]["LV"], CAT[nm]["Dsun"], CAT[nm]["Rgc"], CAT[nm]["rhl"], meas[nm], a0)[0] for nm in FOUR]
    dd = [dsph_row(d, a0)[0] for k in ("classical", "m31", "isolated") for d in classes[k] if 0.01 <= dsph_row(d, a0)[1] <= 1.2]
    foot[fname] = (float(np.median(g05v)), float(np.median(msv)), float(np.median(dd)), len(dd))
    info(f"   {fname:10} a_0={a0:.3g}:  clusters(g05 sigma) {foot[fname][0]:+.3f}   "
         f"clusters(measured sigma) {foot[fname][1]:+.3f}   dwarfs {foot[fname][2]:+.3f} (N={foot[fname][3]})")
ck("V7 both a_0 footings tell the same story, in both directions: g05's headline is footing-independent, and so is "
   "the fact that it halves when the measured dispersions replace the model ones.  a_0 is not the issue here",
   all(v[0] < -0.5 and v[1] > v[0] + 0.3 and v[1] < 0.0 for v in foot.values()),
   "; ".join(f"{f}: g05 {v[0]:+.3f}, measured {v[1]:+.3f}, dwarfs {v[2]:+.3f}" for f, v in foot.items()))

m1 = []
for nm in FOUR:
    b = rebuilt[nm]
    gN = G*(0.5*b["M"]*Msun)/b["r12"]**2
    direct = math.log10(3.0*(SIG_G05[nm]*1e3)**2/b["r12"]/gN)
    m1.append(direct - (b["res"] + math.log10(g_qumond_sphere(b["xi"], b["xe"])*a0c/gN)))
ck("M1 MUTATION CONTROL: with the kernel switched off the cluster residual must reduce EXACTLY to the Newtonian "
   "dynamical-to-photometric mass ratio computed independently, so V4's decomposition is arithmetic and not a story",
   max(abs(v) for v in m1) < 1e-9, f"max discrepancy {max(abs(v) for v in m1):.3e} dex")

m2 = [gc_row(rebuilt[nm]["LV"], CAT[nm]["Dsun"], CAT[nm]["Rgc"], CAT[nm]["rhl"], SIG_G05[nm]*math.sqrt(10), a0c)[0]
      - rebuilt[nm]["res"] for nm in FOUR]
ck("M2 MUTATION CONTROL on the data: inflating every observed dispersion by sqrt(10) must move every residual by "
   "exactly +1.000 dex and nothing else in the pipeline may respond",
   max(abs(v - 1.0) for v in m2) < 1e-9, f"shifts {', '.join(f'{v:+.9f}' for v in m2)}")

sep_z, p_z, _ = exact_sep_p([0.0]*4, dov)
ck("M3 MUTATION CONTROL on the claim: if the clusters sat ON the kernel instead of below it, the same exact "
   "permutation test must stop rejecting.  It does, so V5b is testing the data and not the machinery",
   p_z > 0.05,
   f"clusters forced to 0.000 dex: separation {sep_z:+.3f} dex, exact p = {p_z:.4f}, against p = {p_ms:.4f} for the "
   f"measured-dispersion data and p = {p_g05:.4f} for g05's")

# ===============================================================================================================
P(""); P("="*122); P("VERDICT ON THE CLAIM"); P("="*122)
P("  THE DIRECTION SURVIVES.  THE NUMBER DOES NOT, AND NEITHER DOES THE WORD 'DARK MATTER'.")
P("")
P("  WHAT SURVIVED EVERY ATTACK I COULD MOUNT:")
P(f"   * The four clusters are faithful to the on-disk catalogue: worst residual difference {dmax:.4f} dex (V1).")
P(f"   * The acceleration match is real -- three of four clusters lie inside the dwarfs' own x_i range (V5a).")
P(f"   * Even after every correction below, the clusters still sit BELOW the dwarfs at matched x_i, {sep_ms:+.3f} dex,")
P(f"     exact permutation p = {p_ms:.4f} (V5b), on both a_0 footings (V7).")
P(f"   * The deficit is NOT a stellar mass-to-light artefact.  I expected it to be and it is not: the Newtonian M/L")
P(f"     part is {frac_newt:+.3f} dex against a kernel-boost part of {-frac_kern:+.3f} dex (V4).  That attack failed.")
P(f"   * It is NOT a cherry-pick either, and I expected it to be.  Every one of the {len(pool)} catalogue clusters meeting")
P(f"     answer-blind criteria on measured dispersions: {neg} of {len(pool)} negative, class median {float(np.median(pres)):+.3f} dex, and the")
P(f"     {len(out4)} clusters g05 did not use sit at {med_out:+.3f} against {med_in:+.3f} for the four it did (V3).  That attack failed too.")
P("  So the FIRST sentence of the claim -- 'support type does not predict the sign of the residual' -- STANDS, and")
P(f"  it stands at the CLASS level, not just on four objects: {float(np.median(pres)):+.2f} dex on {len(pool)} clusters against {float(np.median([d['res'] for d in dov])):+.2f} on 12 dwarfs.")
P("")
P("  WHAT DID NOT SURVIVE:")
P(f"   1. THE NUMBER.  -0.859 dex is not the measurement.  Two of g05's four dispersions are taken from the sigma0")
P(f"      column of the Baumgardt PARAMETER table, which is the central dispersion of a fitted NEWTONIAN N-body")
P(f"      model -- a quantity derived under the theory being tested.  The MEASURED profiles are in this repository")
P(f"      (baumgardt_gc_veldisp_profiles.tsv, header: 'These are the DATA, not model curves').  Using the measured")
P(f"      dispersion at each cluster's half-light radius the median goes {med_g05:+.3f} -> {med_meas:+.3f} dex.  Pal 3 moves")
P(f"      +{res_meas['Pal 3']-rebuilt['Pal 3']['res']:.3f} dex on its own: measured 1.70 km/s from 22 stars where g05 used the model's 0.80.")
P(f"      Pal 14 moves +{res_meas['Pal 14']-rebuilt['Pal 14']['res']:.3f}: Baumgardt's compilation of the SAME stars Jordi et al. measured gives 0.71,")
P(f"      not 0.38.  g05's own weakest-link statement flagged the Pal 14 discrepancy and then used the small value")
P(f"      anyway; it did not flag that Pal 3's number is a model output at all.")
P(f"   2. THE MAGNITUDE AGAIN, INDEPENDENTLY.  The full answer-blind class of {len(pool)} clusters gives {float(np.median(pres)):+.3f} dex, not")
P(f"      -0.859.  Two independent routes -- swapping the model dispersions for measured ones on g05's own four, and")
P(f"      expanding to the whole class -- both land near -0.4 to -0.5 dex.  '-0.859' should be retired (V2, V3).")
P(f"   3. THE DISCRIMINANT IS NOT IDENTIFIED.  At matched x_i the classes are also {sep_M:.2f} dex apart in baryonic mass")
P(f"      ({ov_M}/{len(dov)} overlap) and {sep_R:.2f} dex apart in size ({ov_R}/{len(dov)} overlap).  'Dark-matter content', 'baryonic mass'")
P(f"      and 'physical size' name the SAME partition of these sixteen objects.  A kernel that fails as a function")
P(f"      of size or mass -- a framework liability, NOT a vindication of dark matter -- predicts this data equally")
P(f"      well.  Two classes cannot separate three degenerate labels (V6a).")
P(f"   4. AND ON THE DWARF SIDE THE DARK-MATTER VARIABLE IS CIRCULAR.  M_dyn = 3 sigma^2 r_1/2 / G is built from the")
P(f"      same sigma and r_1/2 as the residual: r = {rr:+.3f} by construction (V6b).  Only the cluster side's 'no dark")
P(f"      matter' is an independent statement, so the claim rests on one non-circular half.")
P(f"   5. A SMALL ONE, AGAINST g05'S OWN INTEREST.  Its Upsilon_V = 1 caveat, -0.558 dex, is asserted by adding")
P(f"      log10(2) -- the NEWTONIAN response -- when three of four clusters are in the modified regime.  Recomputed")
P(f"      it is {ups_med[1.0]:+.3f} dex (V4b).")
P("")
P("  WHAT MAY BE QUOTED AFTER THIS FILE:")
P("   * 'Globular clusters, equally pressure-supported, sit BELOW the framework's kernel where dwarf spheroidals at")
P(f"     the same internal acceleration sit above it -- {sep_ms:+.2f} dex on g05's four with measured dispersions (exact")
P(f"     permutation p = {p_ms:.2f}), and {float(np.median(pres)):+.2f} dex on the full answer-blind class of {len(pool)}.  Support type does")
P("     not predict the sign of the residual.'")
P("   * That MOND over-predicts outer-halo cluster dispersions is long known (Baumgardt et al. 2005; Ibata et al.")
P("     2011; Sanders 2012); nothing here is new except the branch-free prescription.")
P(f"  NOT: '-0.859 dex' or 'median -0.859'.  It is inflated by two model dispersions; both independent routes give")
P(f"  about {float(np.median(pres)):+.2f} to {med_meas:+.2f} dex.")
P("  NOT: '...dark-matter content does.'  That is one of at least three degenerate readings of a two-class")
P("  comparison, and the dark-matter variable is not independently measured on the side carrying the weight.")
sys.exit(ck.done())
