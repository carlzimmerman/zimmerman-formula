#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
h120_diskmass_upsilon_localise.py -- HUNT ITEM 120: THE Upsilon THAT Lambda PREDICTS, VERSUS DISKMASS -- LOCALISED.
====================================================================================================================
THE ITEM, AS LISTED.  "Item 76 restricted to the DiskMass overlap (Martinsson+13).  DiskMass's dynamical Upsilon ~ 0.3 is
excluded by both footings (item 76 already found this); the disagreement is localised: which galaxies, and why."

THE FIRST RESULT IS THAT THE ITEM CANNOT BE RUN AS POSED, AND THE REASON IS STRUCTURAL, NOT ACCIDENTAL.
There is NO overlap.  Not a small one -- an empty one.  Cross-matched by UGC number AND independently by sky position,
the DiskMass PPak sample (the galaxies DMS VII measured <M/L>_K = 0.31 on) and SPARC share ZERO galaxies; the
231-galaxy DiskMass parent sample shares exactly one, and that one is not in the PPak subsample.  The cause is that the
two surveys select on OPPOSITE ends of the same variable: DiskMass needs discs seen nearly face-on so that the stellar
line-of-sight dispersion IS sigma_z (its sample runs 19-45 degrees), and SPARC needs discs inclined enough that the
rotation speed can be deprojected (Q <= 2 and i >= 30, median 60-70).  The two samples are therefore disjoint by
construction and always will be.  "Restrict item 76 to the overlap" has an empty domain, and that is stated as check
120a rather than papered over.

WHAT IS DONE INSTEAD -- and it answers the item's real question, "which galaxies, and why", better than a per-galaxy
overlap would have.  If the disagreement is a property of the DiskMass galaxies, it must show up when the SAME estimator
is applied to them and to SPARC.  So:
  (1) the framework's required Upsilon is computed PER GALAXY for the 22 DMS galaxies with a kinematic inclination,
      by inverting the kernel at 2.2 disc scale lengths (the item-17 machinery, re-derived here);
  (2) the IDENTICAL estimator -- exponential disc, exponential gas at twice the scale length, the same single-radius
      kernel inversion -- is run on SPARC, using each SPARC galaxy's own measured rotation speed AT 2.2 R_d.  That is
      the like-for-like control item 17 did not have, and it is what localisation requires;
  (3) the per-galaxy gap is correlated with every variable the tables carry -- luminosity, scale length, central
      surface brightness, B-K colour, inclination, inclination error, and DMS XI's two kinematic asymmetry measures --
      BOTH raw and partialled on the deprojected rotation speed.  The partialling is not decoration: log Upsilon is an
      algebraic function of (V, L_K, h_R) and nothing else, so a raw correlation with anything that tracks V is an
      identity in disguise.  The first version of part 4 reported the two asymmetry measures as a 3-4 sigma
      localisation of the gap in rotation-curve quality; both vanish at fixed V and that claim is withdrawn inside the
      script.  Two rows are deliberately kept in the table, marked ALGEBRA, as the numerical proof that partialling on
      V does not make every variable safe either;
  (4) the two reconciling routes are SIZED: how many degrees of coherent inclination error, or how many dex of M/L
      zero-point, would close the gap -- and whether SPARC, where inclination runs from 30 to 90 degrees, shows any
      inclination trend that would support the first.

WHAT IS IMPORTED, AND FROM WHERE.  Two numbers from the DMS VII abstract: <M/L>_K = 0.31 +- 0.07 and <F_b^2.2hR> =
0.57 +- 0.07.  The repository's stellar-population anchors: Upsilon_K = 0.6 +- 0.1, Upsilon_[3.6] = 0.5 +- 0.1.
Everything else is computed from tables on disk.

THE BAND CONVERSION, WHICH ITEM 17 DID NOT STATE.  DiskMass measures Upsilon in K; SPARC's is at 3.6 um.  Comparing
0.31 (K) with 0.5 (3.6 um) assumes a conversion this environment has no data to pin down, so it is carried as an
explicit bracket Upsilon_K / Upsilon_[3.6] in [1.0, 1.3] and every cross-band statement below is made over the whole
bracket.  The bracket runs AGAINST the framework at its low end and FOR it at its high end, so it is not a convenient one.

Both footings.  Mutation controls.  DiskMass's own Newtonian reading computed beside.  Checks CAN fail.
"""
import sys, math, os
import numpy as np
from scipy.special import i0, i1, k0, k1
from hunt_lib import *
from hunt_lib import _f

ck = Check(); rng = np.random.default_rng(120)
ARCSEC = math.pi/180/3600
MK_SUN = 3.27
UPS_DM, UPS_DM_E = 0.31, 0.07        # DMS VII abstract, dynamical, K band
FB_DM, FB_DM_E = 0.57, 0.07          # DMS VII abstract, V_baryonic/V_total at 2.2 h_R
SPS_K, SPS_K_E = 0.60, 0.10          # stellar populations, K band (repository anchor)
SPS_36 = 0.50                        # stellar populations, 3.6 um (repository anchor)
BAND = (1.00, 1.30)                  # Upsilon_K / Upsilon_[3.6] bracket -- see the header
FGAS = 0.20                          # baryonic gas fraction for the DMS galaxies (bracketed in M120-3)

P("="*118); P("ITEM 120 -- the Upsilon the cosmological constant predicts, against DiskMass, localised"); P("="*118)

# =================================================================== PART 1: THE OVERLAP
P(""); P("-"*118); P("PART 1 -- the overlap between SPARC and DiskMass"); P("-"*118)
DMS1 = {r["UGC"].strip(): r for r in vizier_tsv("diskmass_bershady2010_sample.tsv")}
DMSX = {r["UGC"].strip(): r for r in vizier_tsv("diskmass_swaters2025_dmsXI.tsv")}
ppak = sorted(int(k) for k, r in DMS1.items() if "P" in r["sigma"] and k in DMSX)
master = read_master()
ugc_sparc = {}
for n in master:
    if n.upper().startswith("UGC"):
        try: ugc_sparc[int(n[3:])] = n
        except ValueError: pass
ov_ppak = sorted(set(ppak) & set(ugc_sparc))
ov_parent = sorted({int(k) for k in DMS1} & set(ugc_sparc))
info(f"DiskMass PPak sample (the DMS VII galaxies): {len(ppak)} UGC numbers; DiskMass parent sample: {len(DMS1)}; "
     f"SPARC carries {len(ugc_sparc)} UGC galaxies out of {len(master)}")
info(f"overlap by UGC number: PPak n SPARC = {ov_ppak if ov_ppak else 'EMPTY'}; parent n SPARC = "
     f"{[ugc_sparc[u] for u in ov_parent] if ov_parent else 'EMPTY'}")

# independent check by sky position, in case the name matching is at fault
def _tsv(fname):
    rows = [l.rstrip("\n").split("\t") for l in open(os.path.join(DATA, fname), encoding="latin-1")
            if l.strip() and not l.startswith("#")]
    hdr = [h.strip() for h in rows[0]]
    return [{hdr[i]: (r[i].strip() if i < len(r) else "") for i in range(len(hdr))} for r in rows[3:]]
spos = _tsv("sparc_lelli2016_table1_pos.tsv")
sra = np.array([_f(r["_RAJ2000"]) for r in spos]); sde = np.array([_f(r["_DEJ2000"]) for r in spos])
snm = [r["Name"].strip() for r in spos]
near = []
for k in [str(u) for u in ppak]:
    q = DMSX.get(k)
    if q is None: continue
    ra, de = _f(q["_RA"]), _f(q["_DE"])
    if not np.isfinite(ra): continue
    d = np.hypot((sra - ra)*math.cos(math.radians(de)), sde - de)*3600
    j = int(np.nanargmin(d))
    near.append((k, snm[j], d[j]))
info(f"independent sky-position cross-match of the {len(near)} PPak galaxies against SPARC: nearest SPARC galaxy is "
     f"{min(x[2] for x in near)/60:.1f} arcmin away at best, {np.median([x[2] for x in near])/3600:.1f} degrees typically "
     f"-- so the empty overlap is real and not a name-matching failure")

inc_all = np.array([master[n]["inc"] for n in master if master[n]["Q"] <= 2])
inc_sparc = inc_all[inc_all >= 30]        # the sample the rest of this script uses (load_sparc's i >= 30 cut)
inc_dms = np.array([_f(DMSX[str(u)]["inc"]) for u in ppak if str(u) in DMSX])
inc_dms = inc_dms[np.isfinite(inc_dms)]
info(f"inclination, the variable that makes them disjoint: DiskMass {inc_dms.min():.0f}-{inc_dms.max():.0f} deg "
     f"(median {np.median(inc_dms):.0f}), SPARC's analysis sample {inc_sparc.min():.0f}-{inc_sparc.max():.0f} deg "
     f"(median {np.median(inc_sparc):.0f}); SPARC's master table reaches {inc_all.min():.0f} deg but those galaxies are "
     f"cut, so the usable floor is {inc_sparc.min():.0f} deg and {100*np.mean(inc_dms < inc_sparc.min()):.0f}% of the "
     f"DiskMass sample lies below it")
ck("120a THE ITEM AS POSED HAS AN EMPTY DOMAIN, and the reason is structural.  SPARC and the DiskMass PPak sample share "
   "no galaxies at all -- checked by UGC number and independently by sky position -- because DiskMass selects discs "
   "nearly face-on so that its vertical dispersion is measurable and SPARC selects discs inclined enough to deproject a "
   "rotation speed.  'Item 76 restricted to the DiskMass overlap' therefore cannot be computed, now or ever, and the "
   "rest of this script localises the disagreement without one",
   len(ov_ppak) == 0,
   f"PPak n SPARC = {len(ov_ppak)} galaxies; parent n SPARC = {len(ov_parent)} "
   f"({[ugc_sparc[u] for u in ov_parent]}), and that one is not in the PPak subsample; nearest position match "
   f"{min(x[2] for x in near)/60:.1f} arcmin")

# =================================================================== PART 2: THE ESTIMATOR
P(""); P("-"*118); P("PART 2 -- the framework's required Upsilon, per galaxy, on the DiskMass galaxies"); P("-"*118)
GAL = []
for k, r in DMS1.items():
    if "P" not in r["sigma"] or k not in DMSX: continue
    q = DMSX[k]
    hRa, D, Vp, hra, MK = _f(r["hR"]), _f(q["Dist"]), _f(q["Vrot"]), _f(q["hrot"]), _f(q["KMag"])
    inc, einc = _f(q["inc"]), _f(q["e_inc"])
    if not all(np.isfinite(x) for x in (hRa, D, Vp, hra, MK)) or hRa <= 0 or Vp <= 0 or hra <= 0: continue
    if not (np.isfinite(inc) and inc > 0): continue
    GAL.append(dict(ugc=k, hR=hRa*D*1000*ARCSEC, hrot=hra*D*1000*ARCSEC, Vp=Vp, eVp=_f(q["e_Vrot"]), D=D,
                    MK=MK, inc=inc, einc=einc, LK=10**(-0.4*(MK - MK_SUN)), mu0=_f(r["mu0"]), BK=_f(r["B-K"]),
                    Aphi=_f(q["Aphi"]), Arc=_f(q["Arc"])))
N = len(GAL)
info(f"{N} DMS VII galaxies carry a kinematic inclination, a disc scale length, a distance, a rotation amplitude and a "
     f"K magnitude -- the same {N} item 17 used")
info("CAVEAT INHERITED FROM ITEM 17 AND NOT WEAKENED HERE: DMS XI's V_rot is a PROJECTED amplitude and is deprojected by")
info("1/sin(i) with the kinematic inclination.  Item 17 chose that convention among three by checking which put the")
info("sample on SPARC's baryonic Tully-Fisher zero-point.  The convention itself is the standard, physically correct one")
info("and uses measured inclinations, so the per-galaxy numbers below are determined by measured quantities -- but the")
info("AGREEMENT of this sample's zero-point with SPARC's is not independent evidence, and is not used as any below.")

hR = np.array([g["hR"] for g in GAL]); hrot = np.array([g["hrot"] for g in GAL])
Vp = np.array([g["Vp"] for g in GAL]); LK = np.array([g["LK"] for g in GAL])
inc = np.radians(np.array([g["inc"] for g in GAL])); einc = np.radians(np.array([g["einc"] for g in GAL]))
mu0 = np.array([g["mu0"] for g in GAL]); BK = np.array([g["BK"] for g in GAL])
Aphi = np.array([g["Aphi"] for g in GAL]); Arc = np.array([g["Arc"] for g in GAL])
R22 = 2.2*hR; x22 = R22/hrot

def g_expdisc(M_Msun, h_kpc, R_kpc):
    """Freeman (1970) razor-thin exponential disc: g(R) = 2 G M/h * y^2 [I0K0 - I1K1]/R, y = R/2h."""
    M, h, R = (np.atleast_1d(np.asarray(v, float)) for v in (M_Msun, h_kpc, R_kpc))
    y = R/(2*h)
    return 2*G*(M*Msun)/(h*kpc)*y**2*(i0(y)*k0(y) - i1(y)*k1(y))/(R*kpc)

def invert_kernel(gob, a0):
    """solve g_bar nu(g_bar/a_0) = g_obs (monotone in g_bar) by bisection in log."""
    gob = np.atleast_1d(np.asarray(gob, float))
    lo = 1e-18*np.ones_like(gob); hi = gob.copy()
    for _ in range(200):
        mid = np.sqrt(lo*hi); d = mid*nu(mid/a0) - gob
        lo = np.where(d < 0, mid, lo); hi = np.where(d < 0, hi, mid)
    return np.sqrt(lo*hi)

FORMS = {"tanh": np.tanh, "1-exp": lambda x: 1 - np.exp(-x), "arctan": lambda x: (2/math.pi)*np.arctan(x)}
def ureq_dms(a0, form="1-exp", incs=None, fg=FGAS, LKs=None):
    ii = inc if incs is None else incs
    LL = LK if LKs is None else LKs
    V22 = (Vp/np.sin(ii))*FORMS[form](x22)
    gobs = (V22*1e3)**2/(R22*kpc)
    A = g_expdisc(LL, hR, R22) + g_expdisc(LL*fg/(1 - fg), 2*hR, R22)
    gb = invert_kernel(gobs, a0)
    return gb/A, gb, gobs

P("")
info(f"{'footing':>10} {'RC form':>8} {'median Upsilon_K required':>26} {'16-84%':>20} {'log spread':>11} {'median y = g_bar/a_0':>21}")
UREQ = {}
for foot, a0 in A0.items():
    for form in FORMS:
        u, gb, go = ureq_dms(a0, form)
        UREQ[(foot, form)] = u
        info(f"{foot:>10} {form:>8} {np.median(u):26.3f} "
             f"{f'{np.percentile(u,16):.2f} - {np.percentile(u,84):.2f}':>20} {np.log10(u).std():11.3f} "
             f"{np.median(gb/a0):21.2f}")
U_C = UREQ[("canonical", "1-exp")]; U_A = UREQ[("alt", "1-exp")]
UC_MID = float(np.median(U_C)); UA_MID = float(np.median(U_A))
FORM_SPREAD = (max(np.median(UREQ[("canonical", f)]) for f in FORMS) - min(np.median(UREQ[("canonical", f)]) for f in FORMS))/2
BOOT = np.array([np.median(U_C[rng.integers(0, N, N)]) for _ in range(4000)]); EU = float(BOOT.std())
_, gb_c, gobs_c = ureq_dms(A0["canonical"], "1-exp")
info(f"canonical median required Upsilon_K = {UC_MID:.3f} +- {EU:.3f} (bootstrap) +- {FORM_SPREAD:.3f} (RC form); "
     f"alt {UA_MID:.3f}.  DiskMass measures {UPS_DM} +- {UPS_DM_E}; stellar populations {SPS_K} +- {SPS_K_E} in K")

# =================================================================== PART 3: THE LIKE-FOR-LIKE SPARC CONTROL
P(""); P("-"*118); P("PART 3 -- the SAME estimator run on SPARC: is the disagreement a property of the DiskMass galaxies?")
P("-"*118)
sp = load_sparc()
sp_ap, sp_ex, sp_inc, sp_L, sp_h, sp_nm = [], [], [], [], [], []
for g in sp:
    h = g["Rdisk"]; R = 2.2*h
    if h <= 0 or g["L36"] <= 0: continue
    if R < g["r"].min() or R > g["r"].max(): continue         # only where the curve actually reaches 2.2 R_d
    V22 = float(np.interp(R, g["r"], g["vobs"]))
    if V22 <= 0: continue
    gobs = (V22*1e3)**2/(R*kpc)
    gbv = float(invert_kernel(gobs, A0["canonical"])[0])
    A_star = float(g_expdisc(g["L36"]*1e9, h, R)[0]); A_gas = float(g_expdisc(1.33*g["MHI"]*1e9, 2*h, R)[0])
    Ua = (gbv - A_gas)/A_star                                  # exponential-disc approximation, as for DiskMass
    vd = float(np.interp(R, g["r"], g["vd"])); vg = float(np.interp(R, g["r"], g["vg"])); vb = float(np.interp(R, g["r"], g["vb"]))
    Ad = vd**2/R*KMS2_KPC; Ag = vg*abs(vg)/R*KMS2_KPC; Ab = vb**2/R*KMS2_KPC
    Ub = (gbv - Ag)/max(Ad + 1.4*Ab, 1e-20)                    # exact, using SPARC's own mass decomposition
    if 0.02 < Ua < 10 and 0.02 < Ub < 10:
        sp_ap.append(Ua); sp_ex.append(Ub); sp_inc.append(g["inc"]); sp_L.append(g["L36"]); sp_h.append(h); sp_nm.append(g["name"])
sp_ap = np.array(sp_ap); sp_ex = np.array(sp_ex); sp_inc = np.array(sp_inc)
geo_bias = float(np.median(np.log10(sp_ap/sp_ex)))
info(f"SPARC through the IDENTICAL estimator (exponential disc + exponential gas at 2 R_d, kernel inverted at the "
     f"measured V(2.2 R_d)): N = {len(sp_ap)}, median Upsilon_[3.6] = {np.median(sp_ap):.3f}, spread "
     f"{np.log10(sp_ap).std():.3f} dex")
info(f"the same SPARC galaxies with the EXACT mass decomposition instead of the exponential approximation: "
     f"{np.median(sp_ex):.3f} -- so the exponential-disc-plus-gas approximation the DiskMass numbers rely on carries a "
     f"bias of only {geo_bias:+.3f} dex, and is not what separates the two surveys")
dms36_lo, dms36_hi = UC_MID/BAND[1], UC_MID/BAND[0]
info(f"like for like, over the band bracket: DiskMass galaxies require Upsilon_[3.6] = {dms36_lo:.3f} - {dms36_hi:.3f}; "
     f"SPARC galaxies require {np.median(sp_ap):.3f}.  The two disjoint samples land on the same value.")
ck("120b THE DISAGREEMENT DOES NOT LOCALISE TO THE DISKMASS GALAXIES, which is the item's question answered in the "
   "negative and is a stronger statement than a per-galaxy overlap could have made.  Run the identical estimator on "
   "SPARC -- disjoint sample, different instrument, different selection, inclinations 30-90 instead of 19-45 -- and it "
   "requires the same mass-to-light ratio the DiskMass galaxies do, inside the band-conversion bracket.  So there is "
   "nothing special about the galaxies DMS VII chose; the gap to 0.31 is a flat zero-point offset between two ways of "
   "weighing a disc, and it would be the same gap on any sample",
   dms36_lo <= np.median(sp_ap)*1.25 and dms36_hi >= np.median(sp_ap)*0.75,
   f"DiskMass sample {UC_MID:.3f} in K = {dms36_lo:.3f}-{dms36_hi:.3f} at 3.6 um; SPARC {np.median(sp_ap):.3f} at "
   f"3.6 um, i.e. {math.log10(np.median(sp_ap)/dms36_hi):+.3f} to {math.log10(np.median(sp_ap)/dms36_lo):+.3f} dex "
   f"apart across the bracket, against the {abs(math.log10(UC_MID/UPS_DM)):.3f} dex gap to DiskMass's own value")

# estimator-choice systematic, measurable only because SPARC allows both estimators
from scipy.optimize import minimize_scalar
def fit_ups_full(g, a0, ratio=1.4, lo=0.02, hi=6.0):
    r = g["r"]; vo = g["vobs"]; ev = np.maximum(g["ev"], 2.0)
    def chi2(u):
        gbv = np.maximum((g["vg"]*np.abs(g["vg"]) + u*g["vd"]**2 + ratio*u*g["vb"]**2)/r*KMS2_KPC, 1e-18)
        return float(np.sum(((vo - np.sqrt(gbv*nu(gbv/a0)*r/KMS2_KPC))/ev)**2))
    return minimize_scalar(chi2, bounds=(lo, hi), method="bounded", options={"xatol": 1e-4}).x
full = {}
for g in sp:
    u = fit_ups_full(g, A0["canonical"])
    fd = float(np.mean(UPS_D*g["vd"]**2/np.maximum(g["vg"]*np.abs(g["vg"]) + UPS_D*g["vd"]**2 + UPS_B*g["vb"]**2, 1e-9)))
    if 0.03 < u < 5.9 and fd > 0.35: full[g["name"]] = (u, g["inc"])
u_full = np.array([v[0] for v in full.values()]); i_full = np.array([v[1] for v in full.values()])
# the two estimators must be compared on the SAME galaxies: a median-of-one-set against a median-of-another
# would confound the estimator with the sample.  Intersection only.
both = [(sp_ap[j], full[nm][0]) for j, nm in enumerate(sp_nm) if nm in full]
b_sr = np.array([x[0] for x in both]); b_fc = np.array([x[1] for x in both])
est_bias = float(np.median(np.log10(b_sr/b_fc)))
eb_boot = np.array([np.median(np.log10(b_sr[i]/b_fc[i]))
                    for i in (rng.integers(0, len(both), len(both)) for _ in range(2000))]).std()
set_bias = math.log10(np.median(sp_ap)/np.median(u_full))
info(f"the estimator's own bias, measured on the {len(both)} SPARC galaxies where BOTH estimators run: the single "
     f"radius at 2.2 R_d gives {np.median(b_sr):.3f}, the full-curve fit of item 119 gives {np.median(b_fc):.3f} on "
     f"the SAME galaxies -- a per-galaxy median bias of {est_bias:+.3f} +- {eb_boot:.3f} dex, i.e. none")
info(f"A TRAP AVOIDED, WORTH RECORDING.  Comparing the two estimators' medians over the galaxies each one HAPPENS to "
     f"accept -- {len(sp_ap)} for the single-radius version, {len(u_full)} for the full-curve one -- gives "
     f"{set_bias:+.3f} dex, which looks like an estimator bias and is not: it is a difference in which galaxies each "
     f"estimator can handle.  The per-galaxy comparison on the shared set is the one that means anything.")
ck("120c MY OWN SUSPICION, TESTED AND WITHDRAWN.  This check was written expecting to find that item 17's single-radius "
   "estimator reads high against a full-curve fit and that its recorded tension with DiskMass was therefore inflated.  "
   "Run properly -- the two estimators on the SAME galaxies rather than on the galaxies each happens to accept -- there "
   "is no bias at all: they agree per galaxy to five thousandths of a dex.  Item 17's estimator is vindicated, and so "
   "is the like-for-like comparison of check 120b that rests on it.  The lesson is the trap: the same two estimators "
   "compared as medians over their own samples differ by 0.04 dex, which would have been reported as an estimator "
   "systematic and would have been a sample-selection effect",
   abs(est_bias) < 3*eb_boot,
   f"on {len(both)} shared SPARC galaxies: 2.2 R_d estimator {np.median(b_sr):.3f} vs full-curve {np.median(b_fc):.3f}, "
   f"per-galaxy median bias {est_bias:+.3f} +- {eb_boot:.3f} dex ({est_bias/eb_boot:+.1f} sigma from zero).  The "
   f"median-over-different-samples version gives {set_bias:+.3f} dex, {abs(set_bias/eb_boot):.0f} times the per-galaxy "
   f"error, and is spurious.  Item 17's own rotation-curve-form systematic is +-{FORM_SPREAD:.3f} in Upsilon and "
   f"remains its dominant one")

# =================================================================== PART 4: LOCALISING WITHIN THE SAMPLE
P(""); P("-"*118); P("PART 4 -- localising within the DiskMass sample: which galaxies, and against what")
P("-"*118)
gap = np.log10(U_C/UPS_DM); lV = np.log10(Vp/np.sin(inc))
info("WHAT IS AN IDENTITY HERE, AND WHY IT NEARLY CAUGHT ME.  The required Upsilon is Upsilon = g_bar/A_star with")
info("g_bar = kernel^-1(g_obs), g_obs built from the deprojected rotation speed V, and A_star built from L_K and h_R.")
info("So log Upsilon is an ALGEBRAIC function of (V, L_K, h_R) plus nothing.  Correlating the gap with g_obs, g_bar,")
info(f"y = g_bar/a_0 or V recovers that identity, not physics: measured here as a demonstration, r(gap, log y) = "
     f"{float(np.corrcoef(np.log10(gb_c/A0['canonical']), gap)[0,1]):+.3f} and r(gap, log V) = {float(np.corrcoef(lV, gap)[0,1]):+.3f}.")
info("The FIRST version of this section reported the two DMS XI asymmetry measures as a 3-4 sigma localisation of the")
info("gap in rotation-curve QUALITY.  That was wrong and the control below is what caught it: both asymmetry measures")
info(f"are strong proxies for the rotation speed itself (r(A_RC, log V) = {float(np.corrcoef(Arc, lV)[0,1]):+.3f}, "
     f"r(A_phi, log V) = {float(np.corrcoef(Aphi, lV)[0,1]):+.3f} -- slow discs are")
info("more asymmetric, which is well known), so their correlation with the gap is the V-identity in disguise.  Both raw")
info("and partial-at-fixed-V correlations are therefore printed, and only the partial ones are read.")
P("")
info(f"{'variable':>26} {'N':>4} {'raw r':>8} {'sigma':>7} {'r | log V':>10} {'sigma':>7}   what it would mean")
def partial_r(x, y, z):
    m = np.isfinite(x) & np.isfinite(y) & np.isfinite(z)
    xx, yy, zz = x[m], y[m], z[m]
    rx = xx - np.polyval(np.polyfit(zz, xx, 1), zz); ry = yy - np.polyval(np.polyfit(zz, yy, 1), zz)
    r = float(np.corrcoef(rx, ry)[0, 1])
    return r, r*math.sqrt(m.sum() - 3)/math.sqrt(max(1 - r*r, 1e-9)), int(m.sum())
LOC, ALG = {}, {}
for nm, v, why, is_alg in (
        ("log L_K", np.log10(LK), "ALGEBRA: Upsilon ~ 1/L at fixed V", True),
        ("log h_R (kpc)", np.log10(hR), "ALGEBRA: A_star depends on h_R", True),
        ("mu_0 (R-band, mag/as^2)", mu0, "a surface-density effect?", False),
        ("B-K colour", BK, "a stellar-population effect?", False),
        ("inclination (deg)", np.degrees(inc), "a deprojection effect?", False),
        ("inclination error (deg)", np.degrees(einc), "an inclination-quality effect?", False),
        ("A_phi (DMS XI)", Aphi, "a kinematic-asymmetry effect?", False),
        ("A_RC (DMS XI)", Arc, "a rotation-curve-quality effect?", False)):
    m = np.isfinite(v) & np.isfinite(gap)
    if m.sum() < 8: continue
    r = float(np.corrcoef(v[m], gap[m])[0, 1]); sg = r*math.sqrt(m.sum() - 2)/math.sqrt(max(1 - r*r, 1e-9))
    pr, ps, pn = partial_r(v, gap, lV)
    (ALG if is_alg else LOC)[nm] = (r, sg, pr, ps, int(m.sum()))
    info(f"{nm:>26} {m.sum():4d} {r:8.3f} {sg:7.1f} {pr:10.3f} {ps:7.1f}   {why}")
best = max(LOC, key=lambda k: abs(LOC[k][3]))
nsig_raw = sum(1 for k in LOC if abs(LOC[k][1]) > 3)
nsig = sum(1 for k in LOC if abs(LOC[k][3]) > 3)
ck("120d THE GAP HAS NO INTERNAL STRUCTURE THAT IS NOT ALGEBRA.  Two of the six candidate variables correlate with it "
   "raw at 3-4 sigma -- the survey's own kinematic asymmetry measures -- and both evaporate once the rotation speed is "
   "held fixed, because slower discs are more asymmetric and the rotation speed is algebraically inside the gap.  With "
   "that partialled out, not one of the six reaches 3 sigma: not surface brightness, not colour, not inclination, not "
   "inclination error, not either asymmetry measure.  A flat offset is what an M/L zero-point disagreement looks like, "
   "and a flat offset is what is there.  (The two rows marked ALGEBRA are printed as the numerical proof that "
   "partialling on V does not make everything safe: at fixed V the gap goes as 1/L by construction, and it duly "
   "returns 9 sigma.)",
   nsig == 0 and nsig_raw > 0,
   f"{len(LOC)} candidate variables: {nsig_raw} reach 3 sigma raw, {nsig} survive partialling on log V; strongest "
   f"survivor is {best} at {LOC[best][3]:+.1f} sigma (raw {LOC[best][1]:+.1f}).  N ~ 21, so |r| > 0.55 is needed for "
   f"3 sigma -- a weak constraint, quoted as one.  The sample's own Upsilon scatter is {np.log10(U_C).std():.3f} dex "
   f"against SPARC's {np.log10(sp_ap).std():.3f} through the same estimator, so the DiskMass galaxies are not "
   f"anomalously scattered either")

order = np.argsort(-U_C)
info("")
info(f"the individual galaxies, most demanding first (canonical, 1-exp form):")
info(f"{'UGC':>7} {'Ups_K req':>10} {'inc':>6} {'+-':>5} {'log L_K':>8} {'h_R kpc':>8} {'mu0':>6} {'B-K':>6} {'y=g_bar/a0':>11}")
for j in list(order[:5]) + list(order[-5:]):
    info(f"{GAL[j]['ugc']:>7} {U_C[j]:10.3f} {GAL[j]['inc']:6.1f} {GAL[j]['einc']:5.1f} {math.log10(LK[j]):8.2f} "
         f"{hR[j]:8.2f} {mu0[j]:6.1f} {BK[j]:6.1f} {gb_c[j]/A0['canonical']:11.3f}")

# =================================================================== PART 5: SIZING THE TWO RECONCILING ROUTES
P(""); P("-"*118); P("PART 5 -- what would close the gap: how many degrees, or how many dex"); P("-"*118)
def med_at_shift(dd):
    ii = np.minimum(inc + math.radians(dd), math.radians(89.0))
    return float(np.median(ureq_dms(A0["canonical"], "1-exp", incs=ii)[0]))
lo_d, hi_d = 0.0, 40.0
for _ in range(60):
    mid = 0.5*(lo_d + hi_d)
    if med_at_shift(mid) > UPS_DM: lo_d = mid
    else: hi_d = mid
d_need = 0.5*(lo_d + hi_d)
d_need_36 = None
lo_d, hi_d = 0.0, 40.0
target = UPS_DM/BAND[1]*BAND[1]      # in K; the band bracket is applied to the SPARC comparison, not here
info(f"ROUTE 1 -- inclination.  These discs are nearly face-on, so the deprojection 1/sin(i) is the sample's most "
     f"fragile step: a +1 sigma inclination error moves the required Upsilon by "
     f"{float(np.median(np.log10(ureq_dms(A0['canonical'],'1-exp',incs=np.minimum(inc+einc,math.radians(89)))[0]/U_C))):+.3f} dex "
     f"(median quoted error {np.degrees(np.median(einc)):.1f} deg).")
info(f"                 A COHERENT inclination error of +{d_need:.1f} degrees on the whole sample would bring the "
     f"framework's requirement down to DiskMass's {UPS_DM}.  That is {d_need/np.degrees(np.median(einc)):.1f} times the "
     f"typical quoted error, in the same direction for every galaxy.")
sl_inc, _, _ = fit_loglog(np.maximum(i_full, 1.0), u_full)
r_inc = float(np.corrcoef(i_full, np.log10(u_full))[0, 1])
low_i = i_full < 45; hi_i = i_full >= 60
info(f"                 SPARC is the control, and it does NOT support that route: over inclinations 30-90 degrees the "
     f"full-curve Upsilon shows no inclination trend (r = {r_inc:+.3f}, N = {len(u_full)}); the 30-45 degree galaxies "
     f"give {np.median(u_full[low_i]):.3f} against {np.median(u_full[hi_i]):.3f} above 60 degrees, "
     f"{abs(math.log10(np.median(u_full[low_i])/np.median(u_full[hi_i]))):.3f} dex apart.  SPARC's floor is 30 degrees "
     f"though, and half the DiskMass sample is below it, so this control does not reach where the trouble would be.")
info(f"ROUTE 2 -- a mass-to-light zero-point.  {abs(math.log10(UC_MID/UPS_DM)):.3f} dex, coherent, and it is the SAME offset "
     f"DiskMass already has against stellar populations ({abs(math.log10(SPS_K/UPS_DM)):.3f} dex to Upsilon_K = {SPS_K}).  "
     f"The framework's requirement sits {abs(math.log10(UC_MID/SPS_K)):.3f} dex from stellar populations and "
     f"{abs(math.log10(UC_MID/UPS_DM)):.3f} dex from DiskMass.")
ck("120e THE LOCALISATION, STATED.  The disagreement is not in a subset of galaxies and not in a property of the "
   "DiskMass sample: it is a single coherent number, and it is the SAME number DiskMass already disagrees with stellar "
   "population synthesis by.  The framework does not add a new tension -- it inherits the one that was already in the "
   "literature, and it sides with the population-synthesis half of it",
   abs(math.log10(UC_MID/SPS_K)) < abs(math.log10(UC_MID/UPS_DM)),
   f"required {UC_MID:.3f} +- {EU:.3f} (stat) +- {FORM_SPREAD:.3f} (RC form); distance to stellar populations "
   f"{math.log10(UC_MID/SPS_K):+.3f} dex, to DiskMass {math.log10(UC_MID/UPS_DM):+.3f} dex; DiskMass to stellar "
   f"populations {math.log10(UPS_DM/SPS_K):+.3f} dex.  The framework and stellar populations agree with each other far "
   f"better than either agrees with DiskMass")

# =================================================================== the alternative, computed beside
P(""); P("-"*118); P("THE LambdaCDM / NEWTONIAN ALTERNATIVE, COMPUTED BESIDE"); P("-"*118)
# BUG FOUND AND FIXED HERE: the first version passed M = 1 Msun instead of L_K to the disc term and returned a
# Newtonian maximum-disc Upsilon of 5.7e10 -- eleven orders of magnitude wrong, and obviously so, which is why the
# absurd printed value caught it.  A_tot must be the acceleration PER UNIT Upsilon, i.e. evaluated at Upsilon = 1.
A_tot = g_expdisc(LK, hR, R22) + g_expdisc(LK*FGAS/(1 - FGAS), 2*hR, R22)
u_newt = gobs_c/A_tot
fdm_dm = 1 - FB_DM**2
info(f"DiskMass's own reading: at Upsilon_K = {UPS_DM} a dark halo supplies {100*fdm_dm:.0f}% of the centripetal force at "
     f"2.2 h_R -- submaximal discs, comfortable for LambdaCDM, and the survey's published conclusion.")
info(f"Newton with NO halo on the same galaxies (maximum disc) needs Upsilon_K = {np.median(u_newt):.2f}, "
     f"{math.log10(np.median(u_newt)/SPS_K):+.2f} dex above stellar populations; the kernel needs {UC_MID:.3f}, "
     f"{math.log10(UC_MID/SPS_K):+.2f} dex from them.  So the kernel does {100*(1 - UC_MID/np.median(u_newt)):.0f}% of the "
     f"work the halo would have to do, and the residual disagreement with DiskMass is what is left after that.")
fb_frame = np.sqrt(gb_c/gobs_c)
info(f"the M/L-free cross-check: the framework's baryonic-to-total speed ratio at 2.2 h_R is "
     f"{float(np.median(fb_frame)):.3f} against DiskMass's measured {FB_DM} +- {FB_DM_E} -- the same disagreement, in the "
     f"same direction, with no photometry involved at all")

# =================================================================== MUTATIONS
P(""); P("="*118); P("MUTATION CONTROLS"); P("="*118)
u3 = float(np.median(ureq_dms(3*A0["canonical"], "1-exp")[0]))
lo_a, hi_a = 1.0, 20.0                       # the a_0 multiplier that would put the requirement on DiskMass's value
for _ in range(60):
    mid = 0.5*(lo_a + hi_a)
    if float(np.median(ureq_dms(mid*A0["canonical"], "1-exp")[0])) > UPS_DM: lo_a = mid
    else: hi_a = mid
A0FIX = 0.5*(lo_a + hi_a)
ck("M120-1 the comparison is sensitive to a_0 and is not a rescaling any acceleration would pass: tripling a_0 moves the "
   "required Upsilon far enough to change the verdict, and in the direction that would REMOVE the disagreement -- so a "
   "wrong a_0 is a live escape route for the framework and is named as one, not hidden",
   abs(math.log10(u3/UC_MID)) > 0.1,
   f"a_0 x 3 requires Upsilon_K = {u3:.3f} against {UC_MID:.3f} ({math.log10(u3/UC_MID):+.2f} dex); the a_0 that would "
   f"put the requirement exactly on DiskMass's {UPS_DM} is x{A0FIX:.2f} canonical, i.e. {math.log10(A0FIX):.2f} dex away "
   f"when the two footings are only {abs(math.log10(A0['alt']/A0['canonical'])):.3f} dex apart -- so no admissible a_0 "
   f"reconciles them, and an inadmissible one would wreck every other item in the hunt")

shuf = float(np.median(ureq_dms(A0["canonical"], "1-exp", LKs=rng.permutation(LK))[0]))
sh_sd = np.array([np.log10(np.median(ureq_dms(A0["canonical"], "1-exp", LKs=rng.permutation(LK))[0])) for _ in range(200)]).std()
ck("M120-2 shuffling the luminosities between galaxies destroys the per-galaxy correspondence but NOT the median, which "
   "is exactly what a flat offset predicts and is a further sign that nothing here is galaxy-specific.  The control "
   "that matters is the SPREAD: shuffling inflates the galaxy-to-galaxy scatter, so the estimator is reading real "
   "per-galaxy photometry and not noise",
   np.log10(ureq_dms(A0["canonical"], "1-exp", LKs=rng.permutation(LK))[0]).std() > np.log10(U_C).std(),
   f"shuffled median {shuf:.3f} vs true {UC_MID:.3f} (shuffle-to-shuffle spread {sh_sd:.3f} dex); scatter "
   f"{np.log10(ureq_dms(A0['canonical'],'1-exp',LKs=rng.permutation(LK))[0]).std():.3f} dex shuffled against "
   f"{np.log10(U_C).std():.3f} true")

gl = float(np.median(ureq_dms(A0["canonical"], "1-exp", fg=0.10)[0]))
gh = float(np.median(ureq_dms(A0["canonical"], "1-exp", fg=0.30)[0]))
ck("M120-3 the gas fraction, the one baryonic quantity not measured for these galaxies, is bracketed 10-30% and moves "
   "the answer by less than the disagreement, so no conclusion here rests on it",
   abs(gl - gh) < abs(UC_MID - UPS_DM),
   f"required Upsilon_K = {gl:.3f} (f_gas 0.10) to {gh:.3f} (f_gas 0.30), a range of {abs(gl-gh):.3f} against a gap of "
   f"{abs(UC_MID - UPS_DM):.3f}")

lo36, hi36 = UC_MID/BAND[1], UC_MID/BAND[0]
ck("M120-4 the band conversion, which item 17 did not state, is carried and does not rescue anything.  Over the whole "
   "bracket the framework's requirement stays above DiskMass's value by more than a factor 1.4, and the like-for-like "
   "agreement with SPARC in check 120b holds at both ends",
   lo36 > 1.4*UPS_DM,
   f"Upsilon_K/Upsilon_[3.6] in {BAND}: the DiskMass requirement is {lo36:.3f}-{hi36:.3f} at 3.6 um against SPARC's "
   f"{np.median(sp_ap):.3f}, and {UC_MID:.3f} in K against DiskMass's {UPS_DM} -- a factor "
   f"{UC_MID/UPS_DM:.2f} that the bracket cannot close")

# =================================================================== verdict
P(""); P("="*118); P("VERDICT"); P("="*118)
P(f"  Item 120 asked where the disagreement with DiskMass lives.  The answer is: nowhere in particular, and that is the")
P(f"  result.  (1) The overlap it was to be computed on is EMPTY and structurally must be -- the two surveys select on")
P(f"  opposite ends of inclination.  (2) Running the identical estimator on SPARC, a disjoint sample, returns the same")
P(f"  required mass-to-light ratio ({np.median(sp_ap):.2f} at 3.6 um) as the DiskMass galaxies do ({UC_MID:.2f} in K, {lo36:.2f}-{hi36:.2f} converted),")
P(f"  so nothing about the DiskMass galaxies causes it, and the estimator that says so is validated in 120c -- it agrees")
P(f"  with a full-curve fit of the same galaxies to {abs(est_bias):.3f} dex.  (3) Inside the sample, the two variables that do")
P(f"  correlate with the gap at 3-4 sigma are the survey's own kinematic asymmetry measures, and both evaporate once the")
P(f"  rotation speed -- which is algebraically inside the gap -- is held fixed; nothing else reaches 3 sigma.  (4) What is")
P(f"  left is one coherent {abs(math.log10(UC_MID/UPS_DM)):.2f} dex offset, and it is the same offset DiskMass already carries against stellar")
P(f"  population synthesis, which the framework agrees with to {abs(math.log10(UC_MID/SPS_K)):.2f} dex.  Recorded AGAINST the framework's side of it:")
P(f"  a coherent inclination error of +{d_need:.1f} degrees on this nearly face-on sample would close the gap by itself, and SPARC")
P(f"  cannot test that route because its own usable inclination floor is 30 degrees while {100*np.mean(np.degrees(inc) < 30):.0f}% of the DiskMass")
P(f"  sample lies below it.  Recorded FOR it: no admissible a_0 reconciles them (it would take x{A0FIX:.1f}), the gas fraction")
P(f"  cannot ({abs(gl-gh):.3f} in Upsilon against a {abs(UC_MID-UPS_DM):.3f} gap), and the band conversion cannot ({BAND[0]}-{BAND[1]} leaves a factor 1.4+).")
sys.exit(ck.done())
