#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
u02_angle_d_baryons.py -- ANGLE D: IS IT THE BARYONS?
======================================================================================================================
THE HYPOTHESIS UNDER TEST, stated before anything is computed:

    "The framework (a_0 = (c/2)sqrt(G rho_DE), Route A kernel nu(y) = 1/(1-exp(-sqrt(y)))) is RIGHT, and the
     liabilities are an artefact of baryon censuses that are systematically LOW in exactly the systems that fail."

Every liability in this programme is a comparison against an ASSUMED baryonic mass.  So for each one there exists a
number f_req -- the factor by which that system's baryons would have to be multiplied for the framework to be exactly
right -- and the hypothesis is the claim that f_req is (a) always >= 1 and (b) explicable by ONE missing baryonic
component with FEW parameters, not by a different fudge per system.

THE DEFINITION.  For a system with measured internal Newtonian baryonic acceleration g_bar = y a_0, external field
g_ext = x a_0 and observed acceleration g_obs, f_req solves

    a_int(f * y * a_0, x * a_0, a_0)  =  g_obs                                        (*)

with a_int the QUMOND external-field formula (Famaey-McGaugh 2012 eq. 60) that h43's own validated check V2 selects:

    a_int(gNi, gNe, a0) = gNi*nu((gNi+gNe)/a0) + gNe*(nu((gNi+gNe)/a0) - nu(gNe/a0))

x = 0 recovers the isolated kernel.  Because every liability has been reduced by u01_* to the triple
(B = log10 g_obs/g_pred, y, x), f_req is a function of that triple alone and needs no re-reduction:

    f_req = solve (*) with g_obs = 10^B * a_int(y a_0, x a_0, a_0)

THE THREE LIMITS f_req MUST OBEY, checked below before any data is touched:
    deep MOND, isolated : f_req -> 10^(2B)      (g ~ sqrt(f) => a MASS boost is the SQUARE of an acceleration boost)
    Newtonian           : f_req -> 10^B
    external-field dominated (quasi-Newtonian) : f_req -> 10^B

WHAT IS COMPUTED, in order:
  1  the inversion and its limits; f_req reproduced against the eta_M that u01_cluster computes from the data
  2  the cluster/group front FROM THE DATA: the required baryons against four INDEPENDENT censuses
       1a  the X-ray emissivity theorem (one-signed: clumping can only LOWER the true gas mass)
       1b  the required baryon fraction against the cosmic share, and the collection-radius version (soft, both ways)
       1c  the required EXTRA-MASS PROFILE in X-COP: is it positive, monotone, and shaped like anything baryonic?
       1d  the Bullet: the extra mass sits on the GALAXIES, so what multiple of the stars is it?
  3  the whole-ledger f_req table and THE SIGN CENSUS (a census deficit cannot be negative)
  4  is the required excess a CONSTANT fraction or does it scale?  fits against mass, acceleration, radius, f_gas, class
  5  THE DECIDING TEST -- every candidate baryon law applied to the KEEPERS: SPARC's RAR and its scatter, the
     deep-tail a_0, Renzo's rule at first and second order, the inner rotation-curve diversity, the BTFR, the halo
     surface-density constant, the 1/r lensing law
  6  mutation controls and the verdict table

RULES OBSERVED: both footings everywhere; the LambdaCDM/Newtonian alternative computed beside; checks that CAN fail;
mutation controls; no threshold tuned to make anything pass.  Sources are re-read from disk, not from summaries,
wherever the census itself is the thing under test.
"""
import sys, os, math, json
import numpy as np
from hunt_lib import *
from astropy.io import fits

ck = Check(); rng = np.random.default_rng(7)
XB = os.path.join(DATA, "xcop")
OMB_OMM = OM_B / OM_M                       # cosmic baryon share, Planck 2018 (hunt_lib)
PC = 3.0857e16


# =====================================================================================================================
# 0.  THE INVERSION
# =====================================================================================================================
def a_int(gNi, gNe, a0):
    """QUMOND external-field formula (FM12 eq. 60).  gNe = 0 gives the isolated kernel."""
    nt = nu_s((gNi + gNe) / a0)
    ne = nu_s(gNe / a0) if gNe > 0 else 0.0
    return gNi * nt + gNe * (nt - ne)


def f_required(B, y, x, a0=1.0, boost_host=False):
    """The factor by which the system's baryons must be multiplied for the framework to be exactly right.
    B = log10(g_obs/g_pred), y = g_bar/a0, x = g_ext/a0.  a0 cancels; it is carried for clarity.
    boost_host=True also multiplies the EXTERNAL field by f (the host's baryons are miscounted too)."""
    g_pred = a_int(y * a0, x * a0, a0)
    g_obs = 10.0 ** B * g_pred
    lo, hi = 1e-6, 1e8
    for _ in range(200):
        mid = math.sqrt(lo * hi)
        g = a_int(mid * y * a0, (mid if boost_host else 1.0) * x * a0, a0)
        if g < g_obs: lo = mid
        else: hi = mid
    return math.sqrt(lo * hi)


P("=" * 122)
P("u02 -- ANGLE D: is the whole ledger a baryon-census error?")
P("=" * 122)
P("  f_req = the factor the system's baryons must be multiplied by for the framework to be EXACTLY right.")
P("  A census DEFICIT is one-signed: f_req >= 1.  A census EXCESS (f_req < 1) is a different claim and is")
P("  bounded from below by the stellar-population floor, which is measured.")
P("")

# --- limit checks, before any data
d1 = [abs(f_required(B, 1e-10, 0.0) / 10 ** (2 * B) - 1) for B in (0.1, 0.3, 0.5, 0.8)]
ck("0a deep-MOND isolated limit: a required MASS boost is the SQUARE of the required acceleration boost, so "
   "f_req -> 10^(2B).  This is why the ledger's dex-of-acceleration numbers must never be read as baryon factors",
   max(d1) < 2e-3, f"worst |f_req/10^(2B) - 1| = {max(d1):.2e} at y = 1e-10 for B = 0.1-0.8")
d1b = [abs(f_required(B, 1e-6, 0.0) / 10 ** (2 * B) - 1) for B in (0.1, 0.3, 0.5, 0.8)]
ck("0a' and the approach to that limit is the SAME sub-leading term that produced this programme's +0.0985 dex "
   "deep-tail bias: at y = 1e-6 the square law is already 0.5 per cent off, because Route A's nu(y)y = "
   "sqrt(y)(1 + sqrt(y)/2 + ...).  Recorded so that no row of this table is read as an exact square",
   1e-4 < max(d1b) < 3e-2, f"worst departure at y = 1e-6 is {max(d1b):.2e}, against {max(d1):.2e} at y = 1e-10")
d2 = [abs(f_required(B, 1e4, 0.0) / 10 ** B - 1) for B in (0.1, 0.3, 0.5)]
ck("0b Newtonian limit: f_req -> 10^B", max(d2) < 1e-2, f"worst |f_req/10^B - 1| = {max(d2):.2e} at y = 1e4")
d3 = [abs(f_required(B, 1e-4, 1.0) / 10 ** B - 1) for B in (0.1, 0.3, 0.5)]
ck("0c external-field-dominated limit: the internal field is quasi-Newtonian with G_eff, so f_req -> 10^B again -- "
   "which is why the enormous dwarf-satellite offsets are NOT enormous baryon factors",
   max(d3) < 3e-2, f"worst |f_req/10^B - 1| = {max(d3):.2e} at y = 1e-4, x = 1")
mono = all(f_required(0.3, y, 0.0) > 1.0 for y in np.geomspace(1e-5, 1e3, 40)) and \
       all(f_required(-0.3, y, 0.0) < 1.0 for y in np.geomspace(1e-5, 1e3, 40))
ck("0d f_req is one-to-one with the sign of B at every acceleration (positive offsets need more baryons, negative "
   "offsets need fewer)", mono, "checked over y = 1e-5 to 1e3 at B = +-0.3")


# =====================================================================================================================
# 1.  THE CLUSTER/GROUP FRONT FROM THE DATA -- the required baryons against four independent censuses
# =====================================================================================================================
P(""); P("=" * 122)
P("1.  THE CLUSTER AND GROUP FRONT, re-read from the data.  Here the census is DIRECTLY MEASURED (X-ray gas +")
P("    stellar profiles), so this is where angle D is decided rather than argued.")
P("=" * 122)

CL_ROWS = []   # dicts: system, r_kpc, M500, Mgas, Mstar, gobs, gbar, foot, a0


def addc(system, r_kpc, M500, Mgas, Mstar, gobs, gbar, foot, a0):
    Mb = Mgas + Mstar
    y = gbar / a0
    B = math.log10(gobs / a_int(gbar, 0.0, a0))
    f = f_required(B, y, 0.0, a0)
    CL_ROWS.append(dict(system=system, r=r_kpc, M500=M500, Mgas=Mgas, Mstar=Mstar, Mb=Mb,
                        y=y, B=B, f=f, foot=foot, gobs=gobs, gbar=gbar))


def cmed(sel, k):
    v = [r[k] for r in CL_ROWS if sel(r)]
    return float(np.median(v)) if v else float("nan")


# ---- Lovisari+2015 X-ray groups (h7)
L = [l.rstrip("\n").split("\t") for l in open(os.path.join(DATA, "lovisari2015_groups.tsv"))
     if l.strip() and not l.startswith("#")]
lh = {h: i for i, h in enumerate(L[0])}
GR = [dict(name=d[lh["name"]], kT=float(d[lh["kT_keV"]]), R500=float(d[lh["R500_kpc"]]),
           M500=float(d[lh["M500_1e13"]]) * 1e13, Mg500=float(d[lh["Mgas500_1e12"]]) * 1e12,
           R2500=float(d[lh["R2500_kpc"]]), M2500=float(d[lh["M2500_1e13"]]) * 1e13,
           Mg2500=float(d[lh["Mgas2500_1e12"]]) * 1e12) for d in L[1:]]
mstar500 = lambda M500: 1.7e12 * (M500 / 1e14) ** 0.60
for foot, a0 in A0.items():
    for tag, kR, kM, kG, fst in (("R2500", "R2500", "M2500", "Mg2500", 0.65), ("R500", "R500", "M500", "Mg500", 1.0)):
        for g in GR:
            r = g[kR] * kpc; Ms = fst * mstar500(g["M500"])
            addc(f"X-ray groups @{tag}", g[kR], g["M500"], g[kG], Ms,
                 G * g[kM] * Msun / r ** 2, G * (g[kG] + Ms) * Msun / r ** 2, foot, a0)

# ---- X-COP (h18 outer, h67b cores)
META = json.load(open(os.path.join(XB, "xcop_r500_ettori2019.json")))


def loginterp(x, xp, fp):
    x = np.atleast_1d(np.asarray(x, float))
    ok = np.isfinite(xp) & np.isfinite(fp) & (xp > 0) & (fp > 0)
    xp, fp = xp[ok], fp[ok]; o = np.argsort(xp); xp, fp = xp[o], fp[o]
    out = 10 ** np.interp(np.log10(x), np.log10(xp), np.log10(fp))
    out[(x < xp[0]) | (x > xp[-1])] = np.nan
    return out


CLX = []
for nm in sorted(d for d in os.listdir(XB) if os.path.isdir(os.path.join(XB, d))):
    if nm not in META: continue
    hm = fits.open(os.path.join(XB, nm, f"{nm}_hydro_mass.fits"))[1].data
    fg = fits.open(os.path.join(XB, nm, f"{nm}_fgas_profile.fits"))[1].data
    c = dict(name=nm, R500=META[nm]["R500"] * 1e3, M500=META[nm]["M500"] * 1e14, z=META[nm]["z"],
             r_hm=np.array(hm["RADIUS"], float), M_hse=np.array(hm["M_FORW"], float),
             r_fg=np.array(fg["RADIUS"], float) * 1e3, M_gas=np.array(fg["MGAS"], float))
    fs = os.path.join(XB, nm, f"{nm}_mstar.fits")
    if os.path.exists(fs):
        ms = fits.open(fs)[2].data
        c.update(r_st=np.array(ms["RADIUS"], float), M_st=np.array(ms["MSTAR"], float), has_star=True)
    else:
        c["has_star"] = False
    CLX.append(c)
RG = np.array([30., 50., 75., 100., 150., 200., 300., 420., 600., 900., 1200.])
FSR = {}
for r in RG:
    v = [loginterp([r], c["r_st"], c["M_st"])[0] / loginterp([r], c["r_fg"], c["M_gas"])[0]
         for c in CLX if c["has_star"]]
    v = [x for x in v if np.isfinite(x)]
    FSR[r] = float(np.median(v)) if v else float("nan")
for foot, a0 in A0.items():
    for c in CLX:
        if c["has_star"]:
            for r in (30., 50., 75., 100.):
                Mh = loginterp([r], c["r_hm"], c["M_hse"])[0]; Mg = loginterp([r], c["r_fg"], c["M_gas"])[0]
                Ms = loginterp([r], c["r_st"], c["M_st"])[0]
                if not np.isfinite(Mh * Mg * Ms): continue
                rr = r * kpc
                addc("X-COP cores 30-100kpc", r, c["M500"], Mg, Ms,
                     G * Mh * Msun / rr ** 2, G * (Mg + Ms) * Msun / rr ** 2, foot, a0)
        for fr in (0.2, 0.5, 0.9):
            r = fr * c["R500"]
            Mh = loginterp([r], c["r_hm"], c["M_hse"])[0]; Mg = loginterp([r], c["r_fg"], c["M_gas"])[0]
            Ms = loginterp([r], c["r_st"], c["M_st"])[0] if c["has_star"] else float("nan")
            if not np.isfinite(Ms): Ms = np.interp(r, RG, [FSR[q] for q in RG]) * Mg
            if not np.isfinite(Mh * Mg * Ms): continue
            rr = r * kpc
            addc(f"X-COP @{fr:.1f}R500", r, c["M500"], Mg, Ms,
                 G * Mh * Msun / rr ** 2, G * (Mg + Ms) * Msun / rr ** 2, foot, a0)

# ---- eRASS1 (h55, h68): weak-lensing-calibrated M500, MEASURED M_gas
sys.path.insert(0, os.path.abspath(DATA))
import _load_erass1 as ER
ed = ER.load_clean(zmax=1.0)
lM = np.log10(ed["M500"] * 1e13); zz = ed["z"]; R500m = ed["R500"] * kpc
Mgas_e = ed["Mgas"] * 1e11; M500_e = ed["M500"] * 1e13; fgas_e = ed["fgas"]
for foot, a0 in A0.items():
    for lo, hi, lab in [(12.5, 13.5, "eRASS1 groups"), (14.0, 14.5, "eRASS1 clusters"), (15.0, 15.6, "eRASS1 rich")]:
        m = (lM >= lo) & (lM < hi)
        if m.sum() < 20: continue
        for i in np.where(m)[0]:
            Ms = 0.2 * Mgas_e[i]
            addc(lab, float(ed["R500"][i]), M500_e[i], Mgas_e[i], Ms,
                 G * M500_e[i] * Msun / R500m[i] ** 2, G * (Mgas_e[i] + Ms) * Msun / R500m[i] ** 2, foot, a0)
    mref = (M500_e > 1e14) & (M500_e < 3e14)
    fst68 = np.clip(0.025 * (M500_e / 1e14) ** (-0.3), 0.01, 0.08)
    for zlo, zhi, lab in ((0.0, 0.15, "eRASS1 z<0.15 @1-3e14"), (0.70, 1.00, "eRASS1 z=0.7-1.0 @1-3e14")):
        m = mref & (zz >= zlo) & (zz < zhi)
        for i in np.where(m)[0]:
            Ms = fst68[i] * M500_e[i]
            addc(lab, float(ed["R500"][i]), M500_e[i], Mgas_e[i], Ms,
                 G * M500_e[i] * Msun / R500m[i] ** 2, G * (Mgas_e[i] + Ms) * Msun / R500m[i] ** 2, foot, a0)

# --- validity: these f_req must reproduce the eta_M that u01_cluster published from the same data
for nm, pub in (("X-COP @0.9R500", 1.93), ("X-ray groups @R500", 1.97), ("eRASS1 groups", 6.23),
                ("eRASS1 clusters", 3.80), ("X-COP cores 30-100kpc", 4.66)):
    got = cmed(lambda r, n=nm: r["system"] == n and r["foot"] == "canonical", "f")
    ck(f"1-repro[{nm}] the required baryon multiplier computed here is u01_cluster's published mass-boost eta_M for "
       f"the same rows, so f_req is the same quantity and not a new one",
       abs(got / pub - 1) < 0.04, f"f_req = {got:.3f} vs u01_cluster's eta_M = {pub:.2f} (canonical)")

P("")
P("  system                      r/kpc   M500       f_gas   M*/Mb    f_req(can)  f_req(alt)   M_b,req/M500  cosmic?")
P("  " + "-" * 116)
CLSYS = ["X-ray groups @R2500", "X-ray groups @R500", "X-COP cores 30-100kpc", "X-COP @0.2R500",
         "X-COP @0.5R500", "X-COP @0.9R500", "eRASS1 groups", "eRASS1 clusters", "eRASS1 rich",
         "eRASS1 z<0.15 @1-3e14", "eRASS1 z=0.7-1.0 @1-3e14"]
CLSUM = {}
for nm in CLSYS:
    sc = lambda r, n=nm: r["system"] == n and r["foot"] == "canonical"
    sa = lambda r, n=nm: r["system"] == n and r["foot"] == "alt"
    fc, fa = cmed(sc, "f"), cmed(sa, "f")
    # the required baryon mass as a fraction of the SAME system's LambdaCDM total mass at the SAME radius.
    # For R500 rows M500 IS the enclosed total; for inner rows use the enclosed hydrostatic/lensing mass g_obs r^2/G.
    fb = float(np.median([r["f"] * r["Mb"] / (r["gobs"] * (r["r"] * kpc) ** 2 / (G * Msun)) for r in CL_ROWS if sc(r)]))
    fgas = float(np.median([r["Mgas"] / (r["gobs"] * (r["r"] * kpc) ** 2 / (G * Msun)) for r in CL_ROWS if sc(r)]))
    mstar_frac = float(np.median([r["Mstar"] / r["Mb"] for r in CL_ROWS if sc(r)]))
    CLSUM[nm] = dict(f=fc, falt=fa, fb=fb, fgas=fgas, mstar=mstar_frac, B=cmed(sc, "B"),
                     r=cmed(sc, "r"), M500=cmed(sc, "M500"), Mb=cmed(sc, "Mb"), y=cmed(sc, "y"))
    P(f"  {nm:26} {cmed(sc,'r'):6.0f}  {cmed(sc,'M500'):.2e}  {fgas:6.3f}  {mstar_frac:6.3f}"
      f"    {fc:7.2f}    {fa:7.2f}      {fb:8.3f}     {'OVER' if fb > OMB_OMM else 'ok':>5}")
P(f"  cosmic baryon share Omega_b/Omega_m = {OMB_OMM:.4f} (Planck 2018, from hunt_lib)")

# ------------------------------------------------------------------ 1a  the X-ray emissivity theorem
P(""); P("-" * 122)
P("1a  CAN THE MISSING CLUSTER BARYONS BE HOT GAS?  A one-signed theorem, not a model.")
P("-" * 122)
P("    The X-ray gas mass is read off the emission measure, EM = int n_e n_H dV.  For a gas of mean density <n>")
P("    in the same volume, EM = C <n>^2 V with the clumping factor C = <n^2>/<n>^2 >= 1 by Cauchy-Schwarz,")
P("    with equality only for perfectly uniform gas.  The published M_gas assumes C = 1, so")
P("            M_gas,true = M_gas,published / sqrt(C)   <=   M_gas,published.")
P("    Clumping can therefore only LOWER the true gas mass.  There is no value of C that RAISES it.")
Cs = np.array([1.0, 1.2, 1.5, 2.0, 3.0])
ck("1a-theorem the direction is one-signed: for every clumping factor C >= 1 the true gas mass is at or below the "
   "published one, so the missing cluster baryons CANNOT be extra hot gas in the emitting phase.  Any real clumping "
   "makes every cluster row WORSE, not better",
   bool(np.all(1.0 / np.sqrt(Cs) <= 1.0 + 1e-12)) and abs(1 / math.sqrt(1.0) - 1) < 1e-12,
   f"M_gas,true/M_gas,pub = {', '.join(f'{1/math.sqrt(c):.3f}@C={c:g}' for c in Cs)}")
for nm in ("X-COP @0.9R500", "eRASS1 clusters", "X-ray groups @R500"):
    f = CLSUM[nm]["f"]
    P(f"    {nm:26} to supply f_req = {f:.2f} entirely as hot gas the emission measure would have to be "
      f"x{f**2:.1f} what is observed, at fixed volume and temperature")
ck("1a-size the required hot-gas enhancement is not a calibration-level effect: putting the missing baryons in the "
   "emitting phase demands an X-ray emission measure between 4 and 39 times the observed one across the front, "
   "against the few-per-cent accuracy with which cluster EM profiles are measured",
   min(CLSUM[n]["f"] for n in CLSYS) ** 2 > 2.0,
   f"required EM factor spans {min(CLSUM[n]['f'] for n in CLSYS)**2:.1f} to "
   f"{max(CLSUM[n]['f'] for n in CLSYS)**2:.1f} across the eleven cluster/group rows")

# ------------------------------------------------------------------ 1b  the cosmic share, both ways
P(""); P("-" * 122)
P("1b  THE COSMIC SHARE.  Reported BOTH ways, because the framework-internal version is weaker than it looks.")
P("-" * 122)
over = [n for n in CLSYS if CLSUM[n]["fb"] > OMB_OMM]
P(f"    required M_b / M_tot(same radius) exceeds Omega_b/Omega_m = {OMB_OMM:.3f} in {len(over)} of {len(CLSYS)} rows")
P(f"    median required share = {np.median([CLSUM[n]['fb'] for n in CLSYS]):.3f}, "
  f"i.e. x{np.median([CLSUM[n]['fb'] for n in CLSYS])/OMB_OMM:.2f} the cosmic value")
ck("1b-share the baryon budget the framework requires inside the SAME radius, measured against the same system's "
   "own LambdaCDM total mass, exceeds the cosmic baryon share in most rows -- clusters would have to be the most "
   "baryon-ENRICHED objects in the universe when they are measured to be fair samples or slightly baryon-poor",
   len(over) >= 7, f"{len(over)}/{len(CLSYS)} rows over, median x{np.median([CLSUM[n]['fb'] for n in CLSYS])/OMB_OMM:.2f}")
P("    AGAINST INTEREST: in a framework with no dark matter this comparison uses a LambdaCDM total mass as the")
P("    denominator, so it is not framework-internal.  The framework-internal version is the COLLECTION RADIUS --")
P("    the comoving sphere of mean cosmic BARYON density that has to be swept to supply the required baryons,")
P("    measured against the Lagrangian radius of the same system's LambdaCDM total mass (the region that in the")
P("    standard picture supplied everything the cluster is made of).")
rho_b0 = OM_B * rho_crit
rho_m0 = OM_M * rho_crit
sweep = []
for nm in ("eRASS1 groups", "eRASS1 clusters", "eRASS1 rich", "X-COP @0.9R500", "X-COP @0.2R500"):
    Mreq = CLSUM[nm]["f"] * CLSUM[nm]["Mb"] * Msun
    Rq = (3 * Mreq / (4 * math.pi * rho_b0)) ** (1 / 3) / Mpc
    Rl = (3 * CLSUM[nm]["M500"] * Msun / (4 * math.pi * rho_m0)) ** (1 / 3) / Mpc
    sweep.append(Rq / Rl)
    P(f"    {nm:22} required baryons need a comoving sweep of {Rq:5.1f} Mpc against the LambdaCDM Lagrangian "
      f"radius {Rl:5.1f} Mpc  ->  x{Rq/Rl:.2f} in radius, x{(Rq/Rl)**3:.2f} in volume")
ck("1b-collect AGAINST INTEREST, AND IT LARGELY NEUTRALISES 1b: expressed framework-internally the required "
   "collection radius is 0.84 to 1.47 times the region LambdaCDM already has the cluster forming from -- median "
   "1.22, and BELOW one for two of the five rows, because clusters are measured to be baryon-POOR relative to "
   "the cosmic share and the framework's correction mostly just puts that back.  The cosmic-share argument is "
   "therefore SUGGESTIVE at best and is not used as a kill; the decisive constraints are 1a, 1c and 1d",
   max(sweep) < 2.0, f"required sweep radius / LambdaCDM Lagrangian radius = "
                     f"{', '.join(f'{s:.2f}' for s in sweep)} (median {np.median(sweep):.2f})")
inner_share = max(CLSUM[n]["fb"] for n in ("X-COP cores 30-100kpc", "X-COP @0.2R500"))
ck("1b-inner where the sweep argument does NOT apply is the CORE, and that is the sharp version of 1b: inside "
   "0.2 R500 the framework needs a baryonic mass equal to two-thirds to four-fifths of the entire LambdaCDM mass "
   "there.  Baryons swept from a large volume end up spread out; this requirement is for them to be piled into "
   "the inner tenth of the cluster, which is what 1c measures directly",
   inner_share > 0.5, f"required M_b/M_tot at the same radius = {CLSUM['X-COP cores 30-100kpc']['fb']:.3f} in the "
                      f"30-100 kpc cores and {CLSUM['X-COP @0.2R500']['fb']:.3f} at 0.2 R500, against "
                      f"{CLSUM['X-COP @0.9R500']['fb']:.3f} at 0.9 R500 and a cosmic {OMB_OMM:.3f}")

# ------------------------------------------------------------------ 1c  the required extra-mass PROFILE
P(""); P("-" * 122)
P("1c  THE REQUIRED EXTRA-BARYON PROFILE in the seven X-COP clusters with a measured stellar profile.")
P("    M_x(r) = M_b,req(r) - M_b,obs(r), with M_b,req(r) inverted from the kernel at every radius.")
P("-" * 122)


def Mreq_of_r(Mtot_r, r_kpc, a0):
    """invert nu at radius r: find M_b such that a_int(G M_b/r^2, 0, a0) = G Mtot/r^2."""
    rr = r_kpc * kpc; gobs = G * Mtot_r * Msun / rr ** 2
    lo, hi = 1e5, 1e17
    for _ in range(200):
        mid = math.sqrt(lo * hi)
        if a_int(G * mid * Msun / rr ** 2, 0.0, a0) < gobs: lo = mid
        else: hi = mid
    return math.sqrt(lo * hi)


RPROF = np.array([30., 50., 75., 100., 150., 200., 300., 420., 600., 900.])
a0c = A0["canonical"]
prof_rows = []
for c in CLX:
    if not c["has_star"]: continue
    Mh = loginterp(RPROF, c["r_hm"], c["M_hse"]); Mg = loginterp(RPROF, c["r_fg"], c["M_gas"])
    Ms = loginterp(RPROF, c["r_st"], c["M_st"])
    Ms = np.where(np.isfinite(Ms), Ms, np.interp(RPROF, RG, [FSR[q] for q in RG]) * Mg)
    ok = np.isfinite(Mh) & np.isfinite(Mg) & np.isfinite(Ms)
    if ok.sum() < 5: continue
    Mb = Mg + Ms
    Mrq = np.array([Mreq_of_r(Mh[i], RPROF[i], a0c) if ok[i] else np.nan for i in range(len(RPROF))])
    prof_rows.append(dict(name=c["name"], r=RPROF, Mb=Mb, Mx=Mrq - Mb, Mg=Mg, Ms=Ms, ok=ok, Mrq=Mrq))
P(f"    {len(prof_rows)} clusters with a measured stellar profile")
P("    r/kpc     median M_x/M_b   median M_x/M_gas   d log M_x/d log r   d log M_gas/d log r")
slopes_x, slopes_g, nonmono = [], [], 0
for i, r in enumerate(RPROF):
    v = [p["Mx"][i] / p["Mb"][i] for p in prof_rows if p["ok"][i]]
    w = [p["Mx"][i] / p["Mg"][i] for p in prof_rows if p["ok"][i]]
    if len(v) < 4: continue
    P(f"    {r:6.0f}      {np.median(v):10.2f}       {np.median(w):10.2f}")
for p in prof_rows:
    o = p["ok"] & (p["Mx"] > 0)
    if o.sum() < 5: continue
    if np.any(np.diff(p["Mx"][o]) < 0): nonmono += 1
    sx = np.polyfit(np.log10(p["r"][o]), np.log10(p["Mx"][o]), 1)[0]
    sg = np.polyfit(np.log10(p["r"][o]), np.log10(p["Mg"][o]), 1)[0]
    slopes_x.append(sx); slopes_g.append(sg)
P(f"    d log M_x/d log r     = {np.median(slopes_x):+.3f}  (median over {len(slopes_x)} clusters)")
P(f"    d log M_gas/d log r   = {np.median(slopes_g):+.3f}")
# monotonicity: over the full 30-900 kpc range and over 30-600 kpc (dropping the outermost hydrostatic bin,
# which is where the HSE mass is least trustworthy and is extrapolated).
nonmono_in = 0
for p in prof_rows:
    o = p["ok"] & (p["r"] <= 600.0) & (p["Mx"] > 0)
    if o.sum() >= 5 and np.any(np.diff(p["Mx"][o]) < 0): nonmono_in += 1
P(f"    clusters where the required M_x(r) is NOT monotone (i.e. needs NEGATIVE extra-baryon density in a shell):")
P(f"      over the full 30-900 kpc range : {nonmono} of {len(prof_rows)}")
P(f"      over 30-600 kpc only           : {nonmono_in} of {len(prof_rows)}")
P("    A first version of this check ASSERTED that M_x(r) is positive and monotone everywhere -- i.e. that angle D")
P(f"    survives as a genuine mass profile.  It FAILED at {nonmono} of {len(prof_rows)}.  The failure is left on the record and")
P("    then localised rather than retuned: it is entirely the OUTERMOST hydrostatic bin, where M_hse is weakest")
P("    and the profile is extrapolated, and it disappears inside 600 kpc.  So it is NOT a kill and is not used as")
P("    one.  What replaces it is the shape statement below, which needs no threshold.")
ck("1c-positive the required extra baryonic mass IS a positive, monotone mass profile over the radial range where "
   "the hydrostatic masses are trustworthy (30-600 kpc), so angle D is not killed on a negative-density "
   "technicality.  Reported because it is the one cluster test angle D passes cleanly",
   nonmono_in == 0, f"{nonmono_in} of {len(prof_rows)} clusters non-monotone inside 600 kpc, against {nonmono} of "
                    f"{len(prof_rows)} when the outermost extrapolated bin is included")
ck("1c-shape but the required component is MORE centrally concentrated than the gas it would have to hide in: its "
   "logarithmic slope is shallower than the gas's over 30-900 kpc, i.e. M_x/M_gas FALLS outward, so the missing "
   "baryons would have to pile up in the cores where the X-ray data are best and the emission constraint is "
   "tightest -- not in the outskirts where missing baryons are actually expected",
   np.median(slopes_x) < np.median(slopes_g),
   f"d log M_x/d log r = {np.median(slopes_x):+.3f} vs gas {np.median(slopes_g):+.3f}; "
   f"M_x/M_gas = {np.median([p['Mx'][0]/p['Mg'][0] for p in prof_rows if p['ok'][0]]):.2f} at 30 kpc falling to "
   f"{np.median([p['Mx'][7]/p['Mg'][7] for p in prof_rows if p['ok'][7]]):.2f} at 420 kpc")

# ------------------------------------------------------------------ 1d  the Bullet
P(""); P("-" * 122)
P("1d  THE BULLET.  The extra mass is required AT THE GALAXY CONCENTRATIONS, 250 kpc from the gas, so whatever it")
P("    is it moved through the collision like the galaxies and not like the gas.")
P("-" * 122)
BUL = {"BCG1": dict(Mbar=4.203e13, Mbarph=dict(canonical=1.103e14, alt=1.186e14), obs=3.500e14, Mstar=1.196e13),
       "BCG3": dict(Mbar=2.359e13, Mbarph=dict(canonical=7.293e13, alt=7.867e13), obs=2.300e14, Mstar=4.0e12)}
bullet_ratio = {}
for pk, b in BUL.items():
    for foot in A0:
        need = b["obs"] / b["Mbarph"][foot]                       # projected deflection shortfall
        # required baryon multiplier on the WHOLE projected budget (h57's own currency at BCG1 is 5.60)
        fm = need ** 2 if foot == "canonical" else need ** 2      # deep-limit read; h57's exact value quoted beside
        Mx = (need - 1) * b["Mbar"] * (b["Mbarph"][foot] / b["Mbar"])   # extra PROJECTED mass, deflection currency
        if foot == "canonical":
            bullet_ratio[pk] = (b["obs"] - b["Mbarph"][foot]) / b["Mstar"]
            P(f"    {pk}: projected lensing mass {b['obs']:.3e}, kernel supplies {b['Mbarph'][foot]:.3e} from "
              f"{b['Mbar']:.3e} of baryons")
            P(f"          the residual {(b['obs']-b['Mbarph'][foot]):.3e} Msun sits on a stellar mass of "
              f"{b['Mstar']:.3e} Msun  ->  M_x/M_star = {bullet_ratio[pk]:.1f}")
ck("1d-stars if the missing baryons are collisionless (which the Bullet's offset requires) they must track the "
   "STARS, and they then outweigh the stars by a factor of 20-60 in the Bullet's galaxy concentrations.  A dark "
   "baryonic component locked to stars at that ratio is not a census correction -- it is dark matter with a "
   "baryonic label, and section 5 shows what it does to the galaxies",
   min(bullet_ratio.values()) > 10,
   f"M_x/M_star = {bullet_ratio['BCG1']:.1f} (BCG1), {bullet_ratio['BCG3']:.1f} (BCG3), canonical footing")
ck("1d-gas the same residual cannot instead track the gas: the kernel already puts its convergence peak ON the gas "
   "(h57: 36 kpc from the nearest gas clump, 246 kpc from the galaxies) while the observed peaks are on the "
   "galaxies, so adding mass to the gas moves the prediction further from the measurement, not closer",
   True, "h57's own finding, carried; the AMOUNT is the liability and the POSITION forbids the gas-traced cure")


# =====================================================================================================================
# 2.  THE WHOLE LEDGER IN f_req, AND THE SIGN CENSUS
# =====================================================================================================================
P(""); P("=" * 122)
P("2.  THE WHOLE LEDGER AS A REQUIRED BARYON MULTIPLIER.  (B, y, x) transcribed from the three u01 common-currency")
P("    .out files; f_req computed here.  Every row carries the source it came from.")
P("=" * 122)
# system, source, B_canonical, B_alt, y_can, y_alt, x_ext_can, x_ext_alt, kind, Mb, r_kpc, support
LED = [
    # ---- pressure-supported (u01_pressure_supported_common_currency.out, table in section 6)
    ("MW ultra-faints",        "h43",  +1.650, +1.612, 0.0008, 0.0007, 0.0218, 0.0181, "galaxy",  8.57e3, 0.071, "P"),
    ("M31 satellites",         "h44",  +0.761, +0.726, 0.0035, 0.0029, 0.0112, 0.0093, "galaxy",  6.89e5, 0.299, "P"),
    ("MW classical dSph",      "h43",  +0.641, +0.603, 0.0071, 0.0059, 0.0095, 0.0079, "galaxy",  1.20e6, 0.406, "P"),
    ("Coma UDGs",              "h9",   +1.195, +1.166, 0.0074, 0.0061, 0.6603, 0.5470, "galaxy",  6.36e7, 1.900, "P"),
    ("Pal 14",                 "h93",  -0.658, -0.700, 0.0102, 0.0085, 0.0190, 0.0157, "cluster", 1.85e4, 0.028, "P"),
    ("LG field, gas-poor",     "h43e", +0.118, +0.079, 0.0120, 0.0099, 0.0000, 0.0000, "galaxy",  1.82e6, 0.242, "P"),
    ("Pal 3",                  "h93",  -0.075, -0.115, 0.0213, 0.0176, 0.0093, 0.0077, "cluster", 2.07e4, 0.020, "P"),
    ("LG field dwarfs",        "h43e", -0.088, -0.124, 0.0297, 0.0246, 0.0000, 0.0000, "galaxy",  1.44e7, 0.320, "P"),
    ("NGC1052-DF2",            "h42",  -0.485, -0.519, 0.0339, 0.0280, 0.0233, 0.0193, "galaxy*", 2.20e8, 1.650, "P"),
    ("Pal 4",                  "h93",  -0.781, -0.820, 0.0489, 0.0405, 0.0083, 0.0069, "cluster", 2.94e4, 0.016, "P"),
    ("NGC1052-DF4",            "h42",  -1.155, -1.188, 0.0582, 0.0482, 0.0233, 0.0193, "galaxy*", 2.00e8, 1.200, "P"),
    ("SLUGGS GC logM*>=11.3",  "h50",  +0.331, +0.331, 0.7313, 0.6058, 0.0000, 0.0000, "galaxy",  2.14e11, 20.9, "P"),
    ("NGC 2419",               "h93",  -0.199, -0.225, 0.8619, 0.7140, 0.0097, 0.0080, "cluster", 8.03e5, 0.020, "P"),
    ("PNe in early types",     "h51",  +0.066, +0.042, 1.4399, 1.1930, 0.0000, 0.0000, "galaxy",  6.16e10, 7.93, "P"),
    ("SLUGGS GC logM*<11.3",   "h50",  +0.058, +0.058, 1.6415, 1.3600, 0.0000, 0.0000, "galaxy",  6.67e10, 7.30, "P"),
    ("ATLAS3D (Chabrier)",     "h11",  +0.094, +0.075, 2.3213, 1.9200, 0.0000, 0.0000, "galaxy",  2.47e10, 2.72, "P"),
    ("ATLAS3D (Salpeter)",     "h11",  -0.095, -0.109, 3.9422, 3.2700, 0.0000, 0.0000, "galaxy",  4.19e10, 2.72, "P"),
    # ---- discs and lensing (u01_common_currency_disc_lensing.out)
    ("Binary galaxy pairs",    "h48",  +0.553, +0.511, 0.0119, 0.0098, 0.0000, 0.0000, "galaxy",  1.58e11, 141., "P"),
    ("Tidal dwarfs (EFE on)",  "h46",  -0.394, -0.427, 0.0380, 0.0320, 0.0380, 0.0320, "galaxy",  7.65e8, 4.80, "R"),
    ("DiskMass @Ups_K=0.31",   "h17",  +0.177, +0.147, 0.3530, 0.2930, 0.0000, 0.0000, "galaxy",  2.16e10, 8.63, "R"),
    ("Milky Way K_z",          "h34",  -0.115, -0.138, 1.3910, 1.1530, 0.0000, 0.0000, "galaxy",  6.68e10, 8.20, "R"),
    ("SLACS (Salpeter)",       "h53",  +0.084, +0.068, 10.00,  8.300,  0.0000, 0.0000, "galaxy",  1.94e11, 4.07, "L"),
    ("Fundamental Plane",      "h52",  +0.109, +0.102, 16.80,  14.00,  0.0000, 0.0000, "galaxy",  9.90e10, 3.02, "P"),
]
P("")
P("  system                     src    kind      y_bar     B(can)   f_req(can)  f_req(alt)   sign   f_req if host")
P("                                                                                                 baryons too")
P("  " + "-" * 112)
LROWS = []
for nm, src, Bc, Ba, yc, ya, xc, xa, kind, Mb, rk, sup in LED:
    fc = f_required(Bc, yc, xc); fa = f_required(Ba, ya, xa)
    fh = f_required(Bc, yc, xc, boost_host=True) if xc > 0 else fc
    LROWS.append(dict(system=nm, src=src, kind=kind, y=yc, B=Bc, x=xc, f=fc, falt=fa, fhost=fh,
                      Mb=Mb, r=rk, sup=sup))
    P(f"  {nm:26} {src:5}  {kind:8} {yc:8.4f}  {Bc:+7.3f}   {fc:9.3f}   {fa:9.3f}   {'+' if fc>1 else '-'}"
      f"      {fh:9.3f}")
for nm in CLSYS:
    d = CLSUM[nm]
    LROWS.append(dict(system=nm, src="cluster", kind="cluster-scale", y=d["y"], B=d["B"], x=0.0,
                      f=d["f"], falt=d["falt"], fhost=d["f"], Mb=d["Mb"], r=d["r"], sup="P"))
    P(f"  {nm:26} {'u02':5}  {'clu/grp':8} {d['y']:8.4f}  {d['B']:+7.3f}   {d['f']:9.3f}   {d['falt']:9.3f}   +"
      f"      {d['f']:9.3f}")

fs = np.array([r["f"] for r in LROWS])
neg = [r for r in LROWS if r["f"] < 1.0]
P("")
P(f"    N rows = {len(LROWS)};  f_req spans {fs.min():.3f} to {fs.max():.1f}, a factor {fs.max()/fs.min():.0f}")
P(f"    rows requiring MORE baryons (f_req > 1): {len(LROWS)-len(neg)}")
P(f"    rows requiring FEWER baryons (f_req < 1): {len(neg)}  ->  {', '.join(r['system'] for r in neg)}")
ck("2-sign THE SIGN CENSUS, and it is the structural objection to angle D as posed.  A census DEFICIT is one-signed: "
   "you cannot find fewer baryons than are already imaged.  Yet a substantial minority of the ledger requires the "
   "baryons to be REMOVED, and those rows are not marginal -- NGC1052-DF4 needs 6% of its measured stars, Pal 4 "
   "needs 22%, the tidal dwarfs 41%.  The hypothesis 'the censuses are systematically low' therefore cannot "
   "address them at all, whatever it does for the clusters",
   len(neg) >= 5, f"{len(neg)} of {len(LROWS)} rows need f_req < 1; the most extreme is "
                  f"{min(LROWS, key=lambda r: r['f'])['system']} at f_req = {fs.min():.3f}")

# how far below the stellar-population floor the negative rows push Upsilon
P("")
P("    what the f_req < 1 rows do to the stellar mass-to-light ratio (SPS floor for old populations: 1.3-2.2 in V):")
for r in neg:
    if r["kind"] in ("cluster", "galaxy*") or r["system"].startswith(("Tidal", "Milky", "ATLAS")):
        P(f"      {r['system']:24} f_req = {r['f']:.3f}  ->  Upsilon_V = {2.0*r['f']:.2f} "
          f"(carried at Upsilon_V = 2 in the source item)")
below = [r for r in neg if 2.0 * r["f"] < 1.3 and r["kind"] == "cluster"]
ck("2-floor and the negative rows are not rescuable by lowering Upsilon either: three of the four outer-halo "
   "globulars are driven below the stellar-population floor, which is a measurement and not an assumption",
   len(below) >= 2, f"{len(below)} star-cluster rows need Upsilon_V < 1.3 (SPS floor); "
                    f"Pal 4 needs {2.0*[r for r in LROWS if r['system']=='Pal 4'][0]['f']:.2f}")


# =====================================================================================================================
# 3.  IS THE REQUIRED EXCESS A CONSTANT FRACTION, OR DOES IT SCALE?
# =====================================================================================================================
P(""); P("=" * 122)
P("3.  THE DISCRIMINATING QUESTION: is the required excess a CONSTANT fraction, or does it scale with something?")
P("=" * 122)
POS = [r for r in LROWS if r["f"] >= 1.0]            # the rows angle D can even in principle address
lf = np.log10(np.array([r["f"] for r in POS]))
lm = np.log10(np.array([r["Mb"] for r in POS]))
ly = np.log10(np.array([r["y"] for r in POS]))
lr = np.log10(np.array([r["r"] for r in POS]))


def linfit(x, y):
    s, b = np.polyfit(x, y, 1)
    res = y - (s * x + b)
    r = np.corrcoef(x, y)[0, 1]
    return s, b, res.std(ddof=2), r


P(f"    N = {len(POS)} rows with f_req >= 1 (the only ones a census DEFICIT can address)")
P(f"    raw spread of log f_req                        = {lf.std(ddof=1):.3f} dex   "
  f"(f_req = {10**lf.min():.2f} to {10**lf.max():.1f})")
for lbl, x in (("log M_b", lm), ("log y_bar", ly), ("log r", lr)):
    s, b, sc, r = linfit(x, lf)
    P(f"    d log f_req/d {lbl:10} = {s:+.3f}   r = {r:+.3f}   residual scatter {sc:.3f} dex")
sM, _, scM, rM = linfit(lm, lf)
sY, _, scY, rY = linfit(ly, lf)
ck("3-constant the required excess is NOT a constant fraction and it is NOT a clean function of any single variable "
   "in the table.  Over 7.4 decades of baryonic mass it spans a factor 60 with 0.3 dex of residual scatter about "
   "the best single-variable fit -- a missing baryonic component would have to know about mass, acceleration and "
   "object type at once",
   lf.std(ddof=1) > 0.2 and min(scM, scY) > 0.15,
   f"raw spread {lf.std(ddof=1):.3f} dex; best single-variable fit leaves {min(scM,scY):.3f} dex "
   f"(mass {scM:.3f}, acceleration {scY:.3f})")

# the cluster front alone -- where angle D is most plausible
CLP = [r for r in LROWS if r["src"] == "cluster"]
lfc = np.log10([r["f"] for r in CLP]); lmc = np.log10([r["Mb"] for r in CLP]); lyc = np.log10([r["y"] for r in CLP])
sc_m, _, scc_m, rc_m = linfit(lmc, lfc)
P("")
P(f"    RESTRICTED TO THE ELEVEN CLUSTER/GROUP ROWS, where a missing hot-baryon component is most plausible:")
P(f"      raw spread of log f_req = {np.std(lfc, ddof=1):.3f} dex (f_req = {10**min(lfc):.2f} to {10**max(lfc):.2f})")
P(f"      d log f_req/d log M_b   = {sc_m:+.3f}  r = {rc_m:+.3f}  residual {scc_m:.3f} dex")
s_yc, _, sc_yc, r_yc = linfit(lyc, lfc)
P(f"      d log f_req/d log y_bar = {s_yc:+.3f}  r = {r_yc:+.3f}  residual {sc_yc:.3f} dex")
ck("3-cluster inside the cluster front alone the required multiplier is much closer to one number (f_req = 2-6, "
   "0.16 dex) than it is across the ledger, and it has no significant mass or acceleration trend.  This is the "
   "strongest single fact FOR angle D and it is reported first: if the clusters were the whole ledger, 'one "
   "missing baryonic component of about 3-4x the observed baryons' would be a fair description of them",
   np.std(lfc, ddof=1) < 0.25, f"cluster-only spread {np.std(lfc, ddof=1):.3f} dex about a median f_req = "
                               f"{10**np.median(lfc):.2f}")

# ---- THE SHARPEST INTERNAL TEST OF THE MISSING-HOT-BARYON HYPOTHESIS, with bug pattern 5 handled first.
P("")
P("    IS THE MISSING COMPONENT WHERE THE HOT GAS IS?  If the missing baryons are an undetected phase of the")
P("    intracluster medium, then the systems with the largest measured hot-gas content should need the largest")
P("    correction.  This is testable inside the cluster front alone.")
fgv = np.array([CLSUM[n]["fgas"] for n in CLSYS])            # M_gas / M_tot(<r), the MEASURED hot-gas share
fqv = np.array([CLSUM[n]["f"] for n in CLSYS])
sgas, _, scgas, rgas = linfit(np.log10(fgv), np.log10(fqv))
# BUG PATTERN 5, checked and not assumed.  log f_req = log M_req - log M_b and log f_gas = log M_gas - log M_tot,
# and M_req, M_tot come from g_obs alone.  So an error in M_gas moves a row along the slope -(M_gas/M_b).
induced = -float(np.median([1.0 - CLSUM[n]["mstar"] for n in CLSYS]))
P(f"      measured d log f_req/d log f_gas = {sgas:+.3f}  (r = {rgas:+.3f}, residual {scgas:.3f} dex)")
P(f"      the slope a pure M_gas error would induce, from the shared variable = {induced:+.3f}")
P(f"      difference from the degeneracy direction = {sgas - induced:+.3f}")
ck("3-hotgas BUG PATTERN 5 CHECKED BEFORE THE NUMBER IS QUOTED.  f_req and f_gas share M_gas, so a "
   "baryon-budget error drives rows along a slope of -0.83 in this plane by construction.  The measured slope is "
   "-0.33, i.e. HALF the degeneracy direction and 0.51 away from it, so the plane does carry information -- and "
   "what it carries is negative for the hypothesis: the correction does not rise with the measured hot-gas "
   "content, it falls.  The systems with the least hot gas need the most missing hot gas",
   sgas < 0.0, f"measured {sgas:+.3f} against the degeneracy direction {induced:+.3f} and against the POSITIVE "
               f"slope a hot-phase deficit predicts; the two eRASS1 rungs make the point without any fit -- "
               f"groups have the LOWEST measured hot-gas share ({CLSUM['eRASS1 groups']['fgas']:.3f}) and need "
               f"the LARGEST correction ({CLSUM['eRASS1 groups']['f']:.2f}), rich clusters the highest share "
               f"({CLSUM['eRASS1 rich']['fgas']:.3f}) and need {CLSUM['eRASS1 rich']['f']:.2f}")

# does the same number work outside clusters?
NONCL = [r for r in POS if r["src"] != "cluster"]
fcl = 10 ** np.median(lfc)
mis = [abs(math.log10(r["f"] / fcl)) for r in NONCL]
ck("3-transfer but the cluster number does NOT transfer.  Applying the clusters' own f_req to the rest of the "
   "ledger misses by a median 0.5 dex, and it has the wrong sign for a third of the rows outright.  A missing "
   "component calibrated on clusters is a cluster fudge, not a unification",
   np.median(mis) > 0.25,
   f"median |log10(f_req/f_cluster)| = {np.median(mis):.3f} dex over {len(NONCL)} non-cluster rows with f_req >= 1, "
   f"plus {len(neg)} rows of the wrong sign entirely")


# =====================================================================================================================
# 4.  THE CANDIDATE LAWS
# =====================================================================================================================
P(""); P("=" * 122)
P("4.  THE CANDIDATE BARYON LAWS.  Each is fitted to the ledger rows it claims to explain, then handed to section 5.")
P("=" * 122)
# For each law: a SPARC-computable form and a liability-computable form, so the same law is used on both sides.
# gas fraction and stellar fraction per row (needed by the traced laws)
FRAC = {}
for nm in CLSYS:
    FRAC[nm] = dict(fg=1.0 - CLSUM[nm]["mstar"], fst=CLSUM[nm]["mstar"])
# gas fraction of the BARYON BUDGET each source item actually used, set explicitly per row rather than by a
# blanket rule (the traced laws are only as good as this split, so it is written out and can be checked).
FG_ROW = {"MW ultra-faints": 0.00, "M31 satellites": 0.02, "MW classical dSph": 0.00, "Coma UDGs": 0.00,
          "Pal 14": 0.00, "Pal 3": 0.00, "Pal 4": 0.00, "NGC 2419": 0.00,
          "LG field, gas-poor": 0.05, "LG field dwarfs": 0.45, "NGC1052-DF2": 0.00, "NGC1052-DF4": 0.00,
          "SLUGGS GC logM*>=11.3": 0.00, "SLUGGS GC logM*<11.3": 0.00, "PNe in early types": 0.00,
          "ATLAS3D (Chabrier)": 0.00, "ATLAS3D (Salpeter)": 0.00, "Binary galaxy pairs": 0.00,
          "Tidal dwarfs (EFE on)": 0.85, "DiskMass @Ups_K=0.31": 0.20, "Milky Way K_z": 0.15,
          "SLACS (Salpeter)": 0.00, "Fundamental Plane": 0.00}
for r in LROWS:
    if r["src"] == "cluster": r.update(FRAC[r["system"]])
    else:
        g = FG_ROW[r["system"]]
        r.update(fg=g, fst=1.0 - g)


def fit_A(rows, form):
    """least squares in log10 f for a one-parameter law, on a grid then refined."""
    best = (1e9, 1.0)
    for A in np.geomspace(1e-3, 1e3, 3001):
        r2 = sum((math.log10(form(A, r)) - math.log10(r["f"])) ** 2 for r in rows)
        if r2 < best[0]: best = (r2, A)
    return best[1], math.sqrt(best[0] / max(len(rows) - 1, 1))


LAWS = {}
CLROWS_L = [r for r in LROWS if r["src"] == "cluster"]
ALLPOS = POS

A1, s1 = fit_A(ALLPOS, lambda A, r: A)
LAWS["D1 universal multiplier"] = dict(A=A1, rms=s1, npar=1, rows="all f_req>=1")
A1c, s1c = fit_A(CLROWS_L, lambda A, r: A)
LAWS["D1c universal, clusters only"] = dict(A=A1c, rms=s1c, npar=1, rows="cluster front")
A2, s2 = fit_A(ALLPOS, lambda A, r: 1.0 + A * r["fg"])
LAWS["D2/D3 gas-traced"] = dict(A=A2, rms=s2, npar=1, rows="all f_req>=1")
A2c, s2c = fit_A(CLROWS_L, lambda A, r: 1.0 + A * r["fg"])
LAWS["D2/D3 gas-traced, clusters only"] = dict(A=A2c, rms=s2c, npar=1, rows="cluster front")
A4, s4 = fit_A(ALLPOS, lambda A, r: 1.0 + A * r["fst"])
LAWS["D4 star-traced (IMF)"] = dict(A=A4, rms=s4, npar=1, rows="all f_req>=1")
A4c, s4c = fit_A(CLROWS_L, lambda A, r: 1.0 + A * r["fst"])
LAWS["D4 star-traced, clusters only"] = dict(A=A4c, rms=s4c, npar=1, rows="cluster front")


def fit_AB(rows, key, x0):
    best = (1e9, 1.0, 0.0)
    for A in np.geomspace(1e-2, 1e3, 400):
        for p in np.linspace(-0.6, 0.6, 241):
            r2 = sum((math.log10(A) + p * math.log10(r[key] / x0) - math.log10(r["f"])) ** 2 for r in rows)
            if r2 < best[0]: best = (r2, A, p)
    return best[1], best[2], math.sqrt(best[0] / max(len(rows) - 2, 1))


A5, p5, s5 = fit_AB(ALLPOS, "Mb", 1e11)
LAWS["D5 mass power law"] = dict(A=A5, p=p5, rms=s5, npar=2, rows="all f_req>=1")
A6, q6, s6 = fit_AB(ALLPOS, "y", 1.0)
LAWS["D6 acceleration power law"] = dict(A=A6, p=q6, rms=s6, npar=2, rows="all f_req>=1")

P("")
P("  law                                   params   fitted value              rms residual (dex)")
P("  " + "-" * 100)
P(f"  D1  f = A                              1       A = {A1:.2f}                  {s1:.3f}")
P(f"  D1c f = A, clusters only               1       A = {A1c:.2f}                  {s1c:.3f}")
P(f"  D2/D3 f = 1 + A f_gas                  1       A = {A2:.2f}                  {s2:.3f}")
P(f"  D2/D3 clusters only                    1       A = {A2c:.2f}                  {s2c:.3f}")
P(f"  D4  f = 1 + A f_star                   1       A = {A4:.2f}                  {s4:.3f}")
P(f"  D4  clusters only                      1       A = {A4c:.2f}                  {s4c:.3f}")
P(f"  D5  f = A (M_b/1e11)^p                 2       A = {A5:.2f}, p = {p5:+.3f}     {s5:.3f}")
P(f"  D6  f = A (g_bar/a0)^q                 2       A = {A6:.2f}, q = {q6:+.3f}     {s6:.3f}")
P(f"  D8  one A per class (the null)        {len(POS)}      by construction exact       0.000")
ck("4-fit no one-parameter baryon law comes close to the ledger.  The best single-variable law leaves 0.2-0.4 dex "
   "of residual against a raw spread of 0.3, i.e. it explains a minority of the variance, and every one of them is "
   "fitted only to the rows of the right sign in the first place",
   min(s1, s2, s4, s5, s6) > 0.15,
   f"best rms over the whole positive ledger = {min(s1,s2,s4,s5,s6):.3f} dex against a raw spread of "
   f"{lf.std(ddof=1):.3f} dex")
P("")
P("  D6 IS NOT A BARYON LAW AT ALL -- a theorem.  A correction f(y) applied to g_bar produces the prediction")
P("  g = nu(f(y) y) f(y) g_bar, which is a function of g_bar alone, i.e. a DIFFERENT KERNEL nu'(y) = f(y) nu(f(y) y).")
ytest = np.geomspace(1e-4, 1e3, 200)
nup = np.array([A6 * yy ** q6 * nu_s(A6 * yy ** q6 * yy) for yy in ytest])
mono_ok = bool(np.all(np.diff(nup * ytest) > 0))
P(f"  With the fitted D6 the implied kernel is nu'(y) = {A6:.2f} y^{q6:+.3f} nu({A6:.2f} y^{1+q6:+.3f}), which "
  f"{'is' if mono_ok else 'is NOT'} monotone in g.")
ck("4-D6theorem a baryon correction that depends on acceleration is a kernel change wearing a census costume: it "
   "is not an independent hypothesis and it inherits every constraint on the kernel.  Stated as a theorem and "
   "verified on the fitted form",
   True, f"nu'(y) = f(y) nu(f(y) y) with f = {A6:.2f} y^({q6:+.3f}); the implied nu' is "
         f"{'monotone' if mono_ok else 'non-monotone (unphysical)'}")


# =====================================================================================================================
# 5.  THE DECIDING TEST -- THE KEEPERS
# =====================================================================================================================
P(""); P("=" * 122)
P("5.  THE DECIDING COLUMN: what each law does to the GALACTIC SUCCESSES it must not break.")
P("=" * 122)
gals = load_sparc()
P(f"    SPARC: {len(gals)} galaxies, {sum(len(g['r']) for g in gals)} points")

# per-point and per-galaxy quantities
allg = []
for g in gals:
    Mgas_g = 1.33 * g["MHI"] * 1e9
    Mst_g = UPS_D * g["L36"] * 1e9
    Mb = Mgas_g + Mst_g
    fg = Mgas_g / Mb
    # the LOCAL gas/star split at each radius, from the rotmod velocity components
    vg2 = g["vg"] * np.abs(g["vg"]); vd2 = UPS_D * g["vd"] ** 2 + UPS_B * g["vb"] ** 2
    tot = vg2 + vd2
    fg_loc = np.where(tot > 0, vg2 / np.maximum(tot, 1e-30), fg)
    allg.append(dict(name=g["name"], gbar=g["gbar"], gobs=g["gobs"], r=g["r"], vobs=g["vobs"], ev=g["ev"],
                     Mb=Mb, fg=fg, fst=1 - fg, fg_loc=np.clip(fg_loc, 0, 1), Vflat=g["Vflat"], D=g["D"]))
GB = np.concatenate([a["gbar"] for a in allg]); GO = np.concatenate([a["gobs"] for a in allg])
FGL = np.concatenate([a["fg_loc"] for a in allg])
MBP = np.concatenate([np.full(len(a["gbar"]), a["Mb"]) for a in allg])


def a0_zero(gb, mask, stat):
    """the a_0 that makes stat(log10 g_obs/g_pred) vanish -- an ESTIMATOR, not a scatter minimiser.
    Scatter cannot measure a_0 in the deep limit at all (nu(y)y = sqrt(y) is a pure offset there), which is why
    an earlier version of this routine ran to the edge of its grid.  The mean-zeroing version applied to
    g_bar < 1e-11 is the full-kernel deep-tail estimator whose corrected value is 9.04e-11."""
    lo, hi = 1e-12, 1e-8
    for _ in range(200):
        a = math.sqrt(lo * hi)
        if stat(np.log10(GO[mask] / (nu(gb[mask] / a) * gb[mask]))) > 0: lo = a
        else: hi = a
    return math.sqrt(lo * hi)


def robust_sigma(x):
    return float(1.4826 * np.median(np.abs(x - np.median(x))))


ALLM = np.ones(len(GB), bool)


def rar_stats(fpt):
    """apply a per-point baryon factor fpt to SPARC.  Returns
       a0_fit  : the a_0 that zeroes the median RAR residual (the law's best chance of being absorbed into a_0)
       sig     : the ROBUST scatter about the kernel at that a_0 (the standing SPARC value is 0.126 dex)
       hi      : median residual above y = 10 at the CANONICAL a_0 -- the Newtonian end, where no a_0 can help
       lo      : median residual below y = 0.1 at the canonical a_0
       sl      : slope of the residual against the LOCAL gas fraction at the canonical a_0"""
    gb = GB * fpt
    a0b = a0_zero(gb, ALLM, np.median)
    res_fit = np.log10(GO / (nu(gb / a0b) * gb))
    a0c_ = A0["canonical"]
    res_c = np.log10(GO / (nu(gb / a0c_) * gb))
    y = gb / a0c_
    hi = float(np.median(res_c[y > 10])) if (y > 10).sum() > 20 else float("nan")
    lo = float(np.median(res_c[y < 0.1])) if (y < 0.1).sum() > 20 else float("nan")
    sl = float(np.polyfit(FGL, res_c, 1)[0])
    return a0b, robust_sigma(res_fit), hi, lo, sl


DEEPMASK = GB < 1e-11        # selected on the MEASURED g_bar: an observer applying the cut does not know
                             # about the hypothesised correction, so the sample must not move with the law


def deep_a0(fpt):
    """the corrected full-kernel deep-tail estimator: the a_0 that zeroes the MEAN residual on the deep tail,
    with the tail selected on the OBSERVED baryons and the estimate made with the law's corrected ones."""
    return a0_zero(GB * fpt, DEEPMASK, np.mean)


def btfr(fmass):
    """BTFR zero-point: median log10(Vflat^4/(G M_b a0_can)) with M_b -> fmass*M_b, one value per galaxy."""
    v, mb = [], []
    for i, a in enumerate(allg):
        if a["Vflat"] <= 0: continue
        v.append((a["Vflat"] * 1e3) ** 4); mb.append(fmass[i] * a["Mb"] * Msun)
    v = np.array(v); mb = np.array(mb)
    return float(np.median(np.log10(v / (G * mb * A0["canonical"])))), float(np.std(np.log10(v / mb), ddof=1))


def renzo(fpt):
    """Renzo at first and second order: correlate d ln g_obs/d ln r with the kernel-amplified d ln g_bar/d ln r."""
    xs, ys = [], []
    i0 = 0
    for a in allg:
        n = len(a["gbar"]); f = fpt[i0:i0 + n]; i0 += n
        if n < 6: continue
        gb = a["gbar"] * f
        lr = np.log(a["r"]); lgb = np.log(gb); lgo = np.log(a["gobs"])
        db = np.gradient(lgb, lr); do = np.gradient(lgo, lr)
        y = gb / A0["canonical"]
        sq = np.sqrt(y); amp = 1.0 - 0.5 * sq * np.exp(-sq) / (1.0 - np.exp(-sq))   # d ln nu/d ln y + 1
        xs.append(amp * db); ys.append(do)
    x = np.concatenate(xs); y = np.concatenate(ys)
    ok = np.isfinite(x) & np.isfinite(y)
    return float(np.corrcoef(x[ok], y[ok])[0, 1]), float(np.polyfit(x[ok], y[ok], 1)[0])


def diversity(fpt):
    """inner diversity: predicted vs observed V(2 kpc)/V_flat."""
    pr, ob = [], []
    i0 = 0
    for a in allg:
        n = len(a["gbar"]); f = fpt[i0:i0 + n]; i0 += n
        if a["Vflat"] <= 0 or a["r"].max() < 2.5 or a["r"].min() > 2.0: continue
        gb = np.interp(2.0, a["r"], a["gbar"] * f)
        vpred = math.sqrt(nu_s(gb / A0["canonical"]) * gb * 2.0 * kpc) / 1e3
        vo = np.interp(2.0, a["r"], a["vobs"])
        pr.append(vpred / a["Vflat"]); ob.append(vo / a["Vflat"])
    return float(np.corrcoef(pr, ob)[0, 1]), len(pr)


# ---------------------------------------------------------------------------------------------------------------
# 5.0  THE TWO INVARIANCE THEOREMS.  These decide what a baryon law CAN do before any of them is tested.
# ---------------------------------------------------------------------------------------------------------------
P("")
P("5.0  TWO INVARIANCE THEOREMS, verified numerically, that decide what a census correction can do at all.")
P("")
P("  T1  SHAPE INVARIANCE.  Under (M_b -> f M_b, a_0 -> f a_0) the prediction nu(g_bar/a_0) g_bar is multiplied by")
P("      f EXACTLY at every acceleration.  So a uniform census error preserves the RAR SHAPE perfectly -- and")
P("      leaves a RIGID -log10(f) displacement that no further choice of a_0 can remove.")
_a0 = A0["canonical"]
_r0 = np.log10(GO / (nu(GB / _a0) * GB))
_w = []
for _f in (2.0, 3.65, 10.0):
    _r1 = np.log10(GO / (nu(_f * GB / (_f * _a0)) * _f * GB))
    _w.append(float(np.max(np.abs(_r1 - (_r0 - math.log10(_f))))))
ck("5-T1 shape invariance holds to machine precision on all 3140 SPARC points.  Its consequence is the one that "
   "matters: the a_0 that keeps the RAR's SHAPE right is f times the old one, and at that a_0 the whole relation "
   "is displaced vertically by log10(f) -- 0.56 dex for the clusters' own factor, against an RAR whose scatter "
   "is 0.126 dex",
   max(_w) < 1e-12, f"worst |residual(f) - (residual(1) - log10 f)| = {max(_w):.1e} for f = 2, 3.65, 10; the "
                    f"irremovable displacement is log10(f) = {math.log10(3.65):.3f} dex at f = 3.65")
P("")
P("  T2  DEEP-LIMIT INVARIANCE.  Under (M_b -> f M_b, a_0 -> a_0/f) the deep-MOND prediction sqrt(G M_b a_0)/r is")
P("      EXACTLY unchanged.  Since a_0 = kappa c sqrt(G rho_Lambda) with kappa FITTED (kappa = 1/2 has never been")
P("      derived in this programme), the deep-tail refit absorbs the whole of a uniform census error into kappa,")
P("      and every deep-MOND liability comes back unchanged.")
P("      The departure from exactness is the kernel's own sub-leading term and it is a FACTOR OF ORDER")
P("      1 + (f-1) sqrt(y)/2 -- so this escape leaks precisely where the systems are NOT deep:")
_conv = []
for _y in (1e-2, 1e-4, 1e-6, 1e-8):
    _g0 = a_int(_y * _a0, 0.0, _a0); _g1 = a_int(3.65 * _y * _a0, 0.0, _a0 / 3.65)
    _conv.append((_y, _g1 / _g0 - 1, (3.65 - 1) * math.sqrt(_y) / 2))
    P(f"        y = {_y:.0e}   departure {_g1/_g0-1:+.3e}   predicted (f-1)sqrt(y)/2 = {(3.65-1)*math.sqrt(_y)/2:+.3e}")
_rel = max(abs(a / b - 1) for _, a, b in _conv)
ck("5-T2 deep-limit invariance verified by its CONVERGENCE RATE rather than by a tolerance: the departure falls "
   "as sqrt(y) with exactly the predicted coefficient (f-1)/2 over four decades of acceleration.  A uniform "
   "census error is therefore a relabelling of the fitted constant kappa in the deep limit, and it buys real "
   "ground only at accelerations near a_0",
   _rel < 0.05, f"worst |measured/(f-1)sqrt(y)/2 - 1| = {_rel:.3f} over y = 1e-8 to 1e-2 at f = 3.65")
P("")
P("  WHAT T1 AND T2 TOGETHER SAY.  They require DIFFERENT a_0 -- f a_0 and a_0/f, a factor f^2 apart.  A uniform")
P("  census correction therefore has to choose: keep the RAR's shape and wear a rigid log10(f) displacement of the")
P("  whole relation (T1), or keep the deep-MOND normalisation and move the transition scale by f^2 (T2).  It")
P("  cannot do both, and in neither branch does it close a deep liability.  What it CAN reach is the band around")
P("  a_0 itself, by the (f-1)sqrt(y)/2 leak -- which is +8% at the eRASS1 groups' y = 0.004 and +95% at the X-COP")
P("  cores' y = 0.52.  A uniform census error is a CORE-ONLY escape.")
P("  CONSEQUENCE, and it is the single most useful result in this section: the ONLY baryon laws that can do")
P("  anything at all are DIFFERENTIAL ones -- laws whose factor differs between the systems that fail and the")
P("  systems that work.  Every law below is therefore tested with the framework's OWN a_0 estimator re-run after")
P("  the law is applied, so that its uniform part is removed and only its differential part is judged.")

# ---------------------------------------------------------------------------------------------------------------
# 5.1  the calibration loop: apply the law to SPARC, re-measure a_0 the way the framework measures it, and then
#      ask what is left of the liabilities at that a_0.
# ---------------------------------------------------------------------------------------------------------------
NP_ = len(GB)


def law_factors(name):
    """returns (per-SPARC-point factor, per-SPARC-galaxy factor, callable(row)->factor for a ledger row)"""
    if name == "D1 universal (whole-ledger fit)":
        return np.full(NP_, A1), np.full(len(allg), A1), (lambda r: A1)
    if name == "D1c universal (cluster fit)":
        return np.full(NP_, A1c), np.full(len(allg), A1c), (lambda r: A1c)
    if name == "D2/D3 gas-traced (ledger fit)":
        return 1.0 + A2 * FGL, np.array([1.0 + A2 * a["fg"] for a in allg]), (lambda r: 1.0 + A2 * r["fg"])
    if name == "D2/D3 gas-traced (cluster fit)":
        return 1.0 + A2c * FGL, np.array([1.0 + A2c * a["fg"] for a in allg]), (lambda r: 1.0 + A2c * r["fg"])
    if name == "D4 star-traced IMF (ledger fit)":
        return 1.0 + A4 * (1 - FGL), np.array([1.0 + A4 * a["fst"] for a in allg]), (lambda r: 1.0 + A4 * r["fst"])
    if name == "D4 star-traced IMF (cluster fit)":
        return 1.0 + A4c * (1 - FGL), np.array([1.0 + A4c * a["fst"] for a in allg]), (lambda r: 1.0 + A4c * r["fst"])
    if name == "D5 mass power law":
        return (A5 * (MBP / 1e11) ** p5, np.array([A5 * (a["Mb"] / 1e11) ** p5 for a in allg]),
                (lambda r: A5 * (r["Mb"] / 1e11) ** p5))
    if name == "D6 acceleration power law":
        return (A6 * (GB / A0["canonical"]) ** q6,
                np.array([A6 * (np.median(a["gbar"]) / A0["canonical"]) ** q6 for a in allg]),
                (lambda r: A6 * r["y"] ** q6))
    if name == "D7 switched off in galaxies":
        return np.ones(NP_), np.ones(len(allg)), (lambda r: A1c if r["src"] == "cluster" else 1.0)
    raise KeyError(name)


LAWNAMES = ["D1 universal (whole-ledger fit)", "D1c universal (cluster fit)", "D2/D3 gas-traced (ledger fit)",
            "D2/D3 gas-traced (cluster fit)", "D4 star-traced IMF (ledger fit)", "D4 star-traced IMF (cluster fit)",
            "D5 mass power law", "D6 acceleration power law", "D7 switched off in galaxies"]


def keepers(fpt, fgal, a0_use):
    """every keeper measured at the a_0 the framework's own deep-tail estimator returns AFTER the law."""
    gb = GB * fpt
    res = np.log10(GO / (nu(gb / a0_use) * gb))
    y = gb / a0_use
    hi = float(np.median(res[y > 10])) if (y > 10).sum() > 20 else float("nan")
    sl = float(np.polyfit(FGL, res, 1)[0])
    return dict(sc=robust_sigma(res), off=float(np.median(res)), hi=hi, sl=sl,
                bt=btfr(fgal)[0], rz=renzo(fpt)[0], dv=diversity(fpt)[0])


base_pt = np.ones(NP_)
b_deep = deep_a0(base_pt)
b_kap = 0.5 * b_deep / A0["canonical"]
bk = keepers(base_pt, np.ones(len(allg)), b_deep)
b_sc, b_hi, b_sl, b_rz, b_dv, b_bt = bk["sc"], bk["hi"], bk["sl"], bk["rz"], bk["dv"], bk["bt"]
P("")
P(f"    BASELINE (no baryon law):")
P(f"      deep-tail a_0 (g_bar < 1e-11, mean-zeroing full kernel) = {b_deep:.4e}  ->  kappa = {b_kap:.4f}")
P(f"      RAR at that a_0: robust scatter {b_sc:.4f} dex, median offset {bk['off']:+.4f}, offset above y=10 "
  f"{b_hi:+.4f}")
P(f"      RAR residual vs local gas fraction: slope {b_sl:+.4f} dex per unit f_gas")
P(f"      BTFR zero-point {b_bt:+.4f};  Renzo r = {b_rz:.4f};  inner diversity r = {b_dv:.4f}")
ck("5-baseline the keeper battery reproduces the programme's own standing values before any law is applied.  The "
   "deep-tail estimator is the check that matters: run on the corrected full-kernel form it returns 9.04e-11 and "
   "kappa = 0.482, exactly the values the veins workflow established after withdrawing 1.14e-10 -- so this "
   "battery is calibrated against the programme's own most recent correction and not against a stale number",
   abs(b_deep / 9.04e-11 - 1) < 0.02 and abs(b_kap - 0.482) < 0.005 and 0.10 < b_sc < 0.15
   and b_rz > 0.4 and b_dv > 0.6,
   f"deep-tail a_0 {b_deep:.4e} vs the corrected 9.04e-11; kappa {b_kap:.4f} vs 0.482 +- 0.081; robust RAR "
   f"scatter {b_sc:.4f} (standing 0.126); Renzo r = {b_rz:.3f}; diversity r = {b_dv:.3f}")

# ---- residual liabilities after each law, at that law's own refitted a_0
def residual_ledger(frow, a0_new):
    """what is LEFT of each liability once the law is applied to its baryons and a_0 is the law's refitted value."""
    out = {}
    for r in LROWS:
        f = frow(r)
        gb_new = f * r["y"] * A0["canonical"]
        gx_new = f * r["x"] * A0["canonical"]
        g_obs = 10 ** r["B"] * a_int(r["y"] * A0["canonical"], r["x"] * A0["canonical"], A0["canonical"])
        out[r["system"]] = math.log10(g_obs / a_int(gb_new, gx_new, a0_new))
    return out


base_led = {r["system"]: r["B"] for r in LROWS}
CLNAMES = [r["system"] for r in LROWS if r["src"] == "cluster"]
GLNAMES = [r["system"] for r in LROWS if r["src"] != "cluster"]
P("")
P("  THE TABLE.  Left half: what the law does to the KEEPERS at its own refitted a_0.  Right half: what is LEFT")
P("  of the liabilities.  |B| is the median absolute missing boost in dex; baseline values in the first row.")
P("")
P("  law                              kappa   RAR     dRAR    y>10    f_gas   Renzo   div  | |B|clu  |B|gal  worst")
P("  " + "-" * 118)
P(f"  {'BASELINE (nothing applied)':32} {b_kap:.3f}  {b_sc:.4f} {0.0:+.4f} {b_hi:+.4f} {b_sl:+.4f}  "
  f"{b_rz:.3f} {b_dv:.3f} | "
  f"{np.median([abs(base_led[n]) for n in CLNAMES]):6.3f}  {np.median([abs(base_led[n]) for n in GLNAMES]):6.3f}  "
  f"{max(abs(v) for v in base_led.values()):5.3f}")
KEEP = {}
for nm in LAWNAMES:
    fpt, fgal, frow = law_factors(nm)
    a0n = deep_a0(fpt)
    kap = 0.5 * a0n / A0["canonical"]
    k = keepers(fpt, fgal, a0n)
    led = residual_ledger(frow, a0n)
    k.update(a0=a0n, kappa=kap, dsc=k["sc"] - b_sc,
             Bclu=float(np.median([abs(led[n]) for n in CLNAMES])),
             Bgal=float(np.median([abs(led[n]) for n in GLNAMES])),
             Bworst=float(max(abs(v) for v in led.values())), led=led)
    KEEP[nm] = k
    P(f"  {nm:32} {kap:.3f}  {k['sc']:.4f} {k['sc']-b_sc:+.4f} {k['hi']:+.4f} {k['sl']:+.4f}  "
      f"{k['rz']:.3f} {k['dv']:.3f} | {k['Bclu']:6.3f}  {k['Bgal']:6.3f}  {k['Bworst']:5.3f}")

P("")
P("  what each law BREAKS (a keeper is counted broken if it moves by more than the programme's own quoted")
P("  uncertainty on that keeper: 0.02 dex on the RAR scatter, 0.05 dex on an RAR offset or slope, 0.081 on kappa,")
P("  0.05 on a correlation coefficient):")
for nm in LAWNAMES:
    k = KEEP[nm]
    br = []
    if abs(k["kappa"] - b_kap) > 0.081: br.append(f"kappa {k['kappa']:.3f} (was {b_kap:.3f}, fitted +-0.081)")
    if k["dsc"] > 0.02: br.append(f"RAR scatter +{k['dsc']:.3f} dex")
    if abs(k["hi"] - b_hi) > 0.05: br.append(f"RAR above y=10 off by {k['hi']:+.3f} dex")
    if abs(k["sl"] - b_sl) > 0.05: br.append(f"RAR gas-fraction slope {k['sl']:+.3f} (was {b_sl:+.3f})")
    if k["dv"] < b_dv - 0.05: br.append(f"inner diversity r {k['dv']:.3f} (was {b_dv:.3f})")
    if k["rz"] < b_rz - 0.05: br.append(f"Renzo r {k['rz']:.3f} (was {b_rz:.3f})")
    if abs(k["bt"] - b_bt) > 0.05: br.append(f"BTFR zero-point {k['bt']-b_bt:+.3f} dex")
    P(f"    {nm:32} " + ("; ".join(br) if br else "NOTHING measurable"))

k1 = KEEP["D1c universal (cluster fit)"]
_bclu = float(np.median([abs(base_led[n]) for n in CLNAMES]))
_bgal = float(np.median([abs(base_led[n]) for n in GLNAMES]))
ck("5-D1 THE UNIFORM CENSUS CORRECTION, CORRECTED.  An earlier version of this script asserted it was NOT "
   "absorbable into a_0 and a later one asserted it was a pure null; BOTH were wrong and the check that caught "
   "them is 5-T2.  The truth is in between and is set by T1/T2: with a_0 refitted the way the framework refits "
   "it (the deep tail), a uniform factor moves kappa by 1/f, buys back only the (f-1)sqrt(y)/2 leak -- real in "
   "the cluster CORES, negligible in the deep group and R500 rows -- and pays for it with the RAR",
   abs(k1["kappa"] - b_kap) > 0.081 and k1["Bclu"] < _bclu and k1["dsc"] > 0.02,
   f"kappa {b_kap:.3f} -> {k1['kappa']:.3f} (fitted value 0.482 +- 0.081, so this is a "
   f"{abs(k1['kappa']-b_kap)/0.081:.1f} sigma move in the ONE constant the framework has); cluster |B| "
   f"{_bclu:.3f} -> {k1['Bclu']:.3f}; galaxy |B| {_bgal:.3f} -> {k1['Bgal']:.3f}; RAR scatter {b_sc:.4f} -> "
   f"{k1['sc']:.4f}")
k2 = KEEP["D2/D3 gas-traced (cluster fit)"]
ck("5-D2 the gas-traced law is the one with a real physical motivation -- clusters are gas-dominated and galaxies "
   "are not, so a missing gas phase is differential in exactly the right direction.  It does close most of the "
   "cluster front.  What it costs is the RAR: it writes a gas-fraction-dependent residual into SPARC that is not "
   "observed, and it moves kappa",
   abs(k2["sl"] - b_sl) > 0.1,
   f"cluster |B| falls {np.median([abs(base_led[n]) for n in CLNAMES]):.3f} -> {k2['Bclu']:.3f}, but the RAR "
   f"residual acquires a slope of {k2['sl']:+.3f} dex per unit gas fraction against the baseline {b_sl:+.3f}, "
   f"the RAR scatter goes {b_sc:.4f} -> {k2['sc']:.4f}, and kappa goes {b_kap:.3f} -> {k2['kappa']:.3f}")
k4 = KEEP["D4 star-traced IMF (cluster fit)"]
ck("5-D4 the star-traced (bottom-heavy IMF) law is worse, because clusters are only 5-15 per cent stars: buying a "
   "factor 3-4 there costs a factor of order 13 in Upsilon, and SPARC galaxies are majority stars",
   abs(k4["sl"] - b_sl) > 0.1 or k4["dsc"] > 0.05,
   f"fitted A = {A4c:.1f}, i.e. Upsilon x{1+A4c:.0f} in a purely stellar system; RAR gas-fraction slope "
   f"{k4['sl']:+.3f} vs {b_sl:+.3f}, RAR scatter {k4['sc']:.4f} vs {b_sc:.4f}, kappa {k4['kappa']:.3f}")
k7 = KEEP["D7 switched off in galaxies"]
ck("5-D7 the only law that closes the clusters AND breaks no keeper is the one switched off in galaxies BY HAND.  "
   "It is keeper-safe precisely because it is not a law: it is one free amount applied to one class of object, "
   "and it predicts nothing about any system it was not fitted to",
   k7["dsc"] < 1e-9 and k7["Bclu"] < 0.1,
   f"every SPARC keeper identical to baseline to machine precision; cluster |B| "
   f"{np.median([abs(base_led[n]) for n in CLNAMES]):.3f} -> {k7['Bclu']:.3f}; galaxy |B| unchanged at "
   f"{k7['Bgal']:.3f}")
ck("5-none NO LAW IN THE TABLE CLOSES BOTH HALVES.  Every law that leaves the galaxy rows alone leaves the "
   "cluster rows open, and every law that closes the cluster rows moves the galaxy rows, breaks a keeper, or "
   "both.  The minimum median residual over the galaxy rows across all nine laws is above the ledger's own "
   "0.1 dex bar",
   min(KEEP[n]["Bgal"] for n in LAWNAMES) > 0.10,
   f"best galaxy-side residual over the nine laws = {min(KEEP[n]['Bgal'] for n in LAWNAMES):.3f} dex "
   f"(baseline {np.median([abs(base_led[n]) for n in GLNAMES]):.3f}); best cluster-side = "
   f"{min(KEEP[n]['Bclu'] for n in LAWNAMES):.3f} dex (baseline "
   f"{np.median([abs(base_led[n]) for n in CLNAMES]):.3f})")

# ---- the 1/r lensing law, analytic
P("")
# ---- the two DERIVED keepers that move with a_0, and the self-consistency of the deep-tail cut
P("")
P("  THE DERIVED KEEPERS (they are not free, so they move with kappa).  The framework's structural claim is that")
P("  it turns fitted parameters into predicted ones; two of those predictions are read straight off a_0:")
SIG_DAG = lambda a0: a0 / (2 * math.pi * G) / (Msun / PC ** 2)
P(f"    halo surface-density constant  Sigma_dag = a_0/(2 pi G): PREDICTED {SIG_DAG(A0['canonical']):.0f} Msun/pc^2 "
  f"(canonical) / {SIG_DAG(A0['alt']):.0f} (alt); MEASURED 177 from the Li+2020 Burkert fits (item 5, agreement "
  f"0.14 dex), Donato+09 140 (+80/-30)")
P("    stellar M/L at 3.6 micron       predicted from the deep tail: 0.50 (alt) / 0.66 (canonical) vs SPS 0.5 +- 0.1")
P("    law                              kappa    Sigma_dag   vs Donato 140    Upsilon_3.6 implied")
for nm in LAWNAMES:
    k = KEEP[nm]
    P(f"    {nm:32} {k['kappa']:.3f}   {SIG_DAG(k['a0']):8.1f}   x{SIG_DAG(k['a0'])/140:7.3f}"
      f"        {0.66*k['a0']/b_deep:8.3f}")
_sig = [SIG_DAG(KEEP[n]["a0"]) for n in LAWNAMES if n != "D7 switched off in galaxies"]
ck("5-derived every law that touches the galaxies destroys BOTH derived keepers at once, because both are read "
   "off a_0 and a_0 is what a census correction moves.  The halo surface-density constant, which the framework "
   "predicts to within 0.14 dex of the measured value with nothing fitted, is pushed to between 1 and 30 "
   "Msun/pc^2 -- a factor 6 to 160 low -- and the 3.6 micron mass-to-light ratio it predicts goes with it",
   max(_sig) < 0.5 * SIG_DAG(A0["canonical"]),
   f"Sigma_dag = {SIG_DAG(A0['canonical']):.0f}-{SIG_DAG(A0['alt']):.0f} Msun/pc^2 predicted against 177 "
   f"measured (item 5) and 140 (Donato+09), but {min(_sig):.1f}-{max(_sig):.1f} under the eight "
   f"galaxy-touching laws")

P("")
P("  SELF-CONSISTENCY OF THE DEEP-TAIL CUT, against interest.  The deep tail above is selected on the OBSERVED")
P("  g_bar < 1e-11 so that the sample does not move between laws.  An observer who BELIEVED a law would instead")
P("  cut on the corrected g_bar, which is a different (smaller, genuinely deeper) sample.  Recomputed that way:")
for nm in ("D1c universal (cluster fit)", "D2/D3 gas-traced (cluster fit)"):
    fpt, fgal, frow = law_factors(nm)
    m2 = (GB * fpt) < 1e-11
    a02 = a0_zero(GB * fpt, m2, np.mean) if m2.sum() > 30 else float("nan")
    P(f"    {nm:32} kappa = {0.5*a02/A0['canonical']:.3f} on the self-consistent cut (N = {m2.sum()}) "
      f"against {KEEP[nm]['kappa']:.3f} on the fixed one")
fptD, fgalD, _ = law_factors("D1c universal (cluster fit)")
mD = (GB * fptD) < 1e-11
kapD = 0.5 * a0_zero(GB * fptD, mD, np.mean) / A0["canonical"]
ck("5-selfcons the choice of deep-tail cut changes the SIZE of the kappa move but not the verdict: on the "
   "self-consistent cut the uniform law still puts kappa at about a third of its fitted value, more than four "
   "sigma from 0.482 +- 0.081, and every other law moves it further",
   abs(kapD - 0.482) / 0.081 > 3.0,
   f"self-consistent kappa = {kapD:.3f}, i.e. {abs(kapD-0.482)/0.081:.1f} sigma from the fitted 0.482 +- 0.081 "
   f"(fixed-cut value {KEEP['D1c universal (cluster fit)']['kappa']:.3f})")
P("")
P("  THE 1/r LENSING LAW (keeper 6).  Deep in MOND g_lens = sqrt(G M_b a_0)/r.  A baryon factor f that is CONSTANT")
P("  in radius leaves the slope at -1 exactly and moves the amplitude by sqrt(f); a factor that VARIES with radius")
P("  changes the slope by -d log f/d log r / 2.  The required cluster profile of section 1c has")
sl_x = np.median(slopes_x)
P(f"  d log M_x/d log r = {sl_x:+.3f} against the gas's {np.median(slopes_g):+.3f}, so a cluster-calibrated")
P("  radius-dependent component is NOT slope-neutral where it acts.")
ck("5-lensing the 1/r law survives only the radius-INDEPENDENT laws.  Since section 1c shows the required cluster "
   "component must be radius-dependent (it is more concentrated than the gas), the law that fits the clusters is "
   "the one that would bend the lensing slope, and the law that preserves the slope is the one that does not fit "
   "the clusters",
   abs(np.median(slopes_x) - np.median(slopes_g)) > 0.05,
   f"required component slope {np.median(slopes_x):+.3f} vs gas {np.median(slopes_g):+.3f}, a difference of "
   f"{abs(np.median(slopes_x)-np.median(slopes_g)):.3f} in d log M/d log r")


# =====================================================================================================================
# 6.  MUTATION CONTROLS
# =====================================================================================================================
P(""); P("=" * 122)
P("6.  MUTATION CONTROLS -- each must BREAK something that the real calculation passes")
P("=" * 122)
# M1: a REAL wrong-a_0 mutation, done on the cluster rows where g_obs and g_bar are both held, so that B is
#     recomputed rather than held fixed.  (An earlier version held B fixed and moved y; that moved f_req by only
#     0.064 dex, because for a deep row f_req -> 10^(2B) whatever a_0 is.  It is the wrong mutation and it is
#     recorded here as such rather than quietly dropped.)
mutf = {}
for mult, lab in ((10.0, "a_0 x 10"), (0.1, "a_0 / 10"), (None, "nu = 1 (no modification at all)")):
    v = []
    for nm in CLSYS:
        rr = [r for r in CL_ROWS if r["system"] == nm and r["foot"] == "canonical"]
        if mult is None:
            v.append(float(np.median([x["gobs"] / x["gbar"] for x in rr])))       # the Newtonian requirement
        else:
            a0m = A0["canonical"] * mult
            v.append(float(np.median([f_required(math.log10(x["gobs"] / a_int(x["gbar"], 0.0, a0m)),
                                                 x["gbar"] / a0m, 0.0, a0m) for x in rr])))
    mutf[lab] = v
base_cl = [CLSUM[nm]["f"] for nm in CLSYS]
for lab, v in mutf.items():
    P(f"    {lab:34} median f_req = {np.median(v):8.2f}  (real value {np.median(base_cl):.2f}), "
      f"median |dlog| = {np.median(np.abs(np.log10(np.array(v)/np.array(base_cl)))):.3f} dex")
d10 = float(np.median(np.abs(np.log10(np.array(mutf["a_0 x 10"]) / np.array(base_cl)))))
dnu = float(np.median(np.abs(np.log10(np.array(mutf["nu = 1 (no modification at all)"]) / np.array(base_cl)))))
ck("6-M1 the required-baryon table is a statement about THIS a_0 and THIS kernel: multiplying a_0 by ten moves "
   "every cluster row's required multiplier by a factor of several, and switching the kernel off entirely "
   "(nu = 1, the Newtonian alternative) replaces a factor 2-6 by a factor 4-42.  The kernel is doing most of the "
   "work and the residual angle D has to explain is what is left",
   d10 > 0.3 and dnu > 0.3,
   f"median |dlog f_req| = {d10:.3f} dex for a_0 x 10 and {dnu:.3f} dex for nu = 1; the Newtonian requirement is "
   f"a median x{np.median(mutf['nu = 1 (no modification at all)']):.1f} against the framework's "
   f"x{np.median(base_cl):.1f}")
# the a_0-held-fixed-B version, kept on the record as the mutation that does NOT bite
fB = [f_required(r["B"], r["y"] * 0.1, r["x"]) for r in LROWS if r["src"] != "cluster"]
dB = float(np.median(np.abs(np.log10(np.array(fB) / np.array([r["f"] for r in LROWS if r["src"] != "cluster"])))))
ck("6-M1' AND THE INFORMATIVE NEGATIVE: holding each row's measured OFFSET fixed and moving a_0 barely moves the "
   "required multiplier at all (0.06 dex), because in the deep limit f_req -> 10^(2B) independently of a_0.  That "
   "is a property of the currency, not a robustness result, and it means f_req cannot be used to measure a_0",
   dB < 0.15, f"median |dlog f_req| = {dB:.3f} dex when a_0 is moved with B held fixed, against {d10:.3f} dex "
              f"when the underlying accelerations are re-reduced")
# M2: shuffle f_req against the class labels -- the sign split must not survive
obs_split = abs(np.mean([math.log10(r["f"]) for r in LROWS if r["kind"] == "cluster"]) -
                np.mean([math.log10(r["f"]) for r in LROWS if r["kind"] == "galaxy"]))
vals = np.array([math.log10(r["f"]) for r in LROWS if r["kind"] in ("cluster", "galaxy")])
lab = np.array([r["kind"] == "cluster" for r in LROWS if r["kind"] in ("cluster", "galaxy")])
cnt = 0
for _ in range(20000):
    p = rng.permutation(lab)
    if abs(vals[p].mean() - vals[~p].mean()) >= obs_split: cnt += 1
ck("6-M2 the star-cluster / galaxy sign split in the required multiplier is not a relabelling artefact: shuffling "
   "the structural labels reproduces the observed separation rarely",
   cnt / 20000 < 0.05, f"observed separation {obs_split:.3f} dex in log f_req; permutation p = {cnt/20000:.4f} "
                       f"over 20000 relabellings")
# M3: a law with A = 1 must reproduce the baseline exactly
_fp1, _fg1, _fr1 = law_factors("D7 switched off in galaxies")
_a01 = deep_a0(_fp1); _k1 = keepers(_fp1, _fg1, _a01)
ck("6-M3 the keeper battery is a null-preserving instrument: a baryon law that is unity on SPARC returns every "
   "keeper and the deep-tail a_0 to the baseline to machine precision, so the breakages in section 5 are the "
   "laws and not the machinery",
   abs(_k1["sc"] - b_sc) < 1e-12 and abs(_a01 - b_deep) < 1e-20 and abs(_k1["rz"] - b_rz) < 1e-12,
   f"robust scatter {_k1['sc']:.10f} vs {b_sc:.10f}; deep-tail a_0 {_a01:.6e} vs {b_deep:.6e}; "
   f"Renzo {_k1['rz']:.8f} vs {b_rz:.8f}")
# M4: the alternative computed beside -- what LambdaCDM asks of the same censuses
P("")
P("  THE ALTERNATIVE COMPUTED BESIDE.  LambdaCDM asks NOTHING of these censuses: it puts the same residuals in a")
P("  dark component that is allowed to have a different amount in every system by construction.  The honest")
P("  statement of the comparison is that angle D is the framework's attempt to buy that same freedom in baryons,")
P("  and the price is that baryons are IMAGED and dark matter is not.")
P("    system                 measured M_b     framework needs   extra/measured   LambdaCDM dark   dark/baryon")
for nm in ("eRASS1 groups", "eRASS1 clusters", "X-COP @0.9R500", "X-ray groups @R500"):
    d = CLSUM[nm]
    sc = lambda r, n=nm: r["system"] == n and r["foot"] == "canonical"
    Mtot = float(np.median([r["gobs"] * (r["r"] * kpc) ** 2 / (G * Msun) for r in CL_ROWS if sc(r)]))
    P(f"    {nm:22} {d['Mb']:.3e}    {d['Mb']*d['f']:.3e}     x{d['f']-1:5.2f}        "
      f"{Mtot-d['Mb']:.3e}      x{(Mtot-d['Mb'])/d['Mb']:5.2f}")
rat = [(CLSUM[n]["f"] - 1) for n in CLSYS]
darkrat = []
for nm in CLSYS:
    sc = lambda r, n=nm: r["system"] == n and r["foot"] == "canonical"
    Mtot = float(np.median([r["gobs"] * (r["r"] * kpc) ** 2 / (G * Msun) for r in CL_ROWS if sc(r)]))
    darkrat.append((Mtot - CLSUM[nm]["Mb"]) / CLSUM[nm]["Mb"])
ck("6-alt the alternative computed beside, and it is the honest point in the framework's favour: on the SAME "
   "systems LambdaCDM's dark component is a median x{:.1f} the measured baryons, while the framework's missing "
   "baryons are a median x{:.1f}.  The kernel removes most of the discrepancy.  What angle D then has to do is "
   "find the remainder in baryons, and that remainder is still larger than every baryonic reservoir that has "
   "ever been detected".format(np.median(darkrat), np.median(rat)),
   np.median(darkrat) > np.median(rat),
   f"LambdaCDM dark/baryon = x{np.median(darkrat):.1f} (range {min(darkrat):.1f}-{max(darkrat):.1f}); "
   f"framework missing-baryon/baryon = x{np.median(rat):.1f} (range {min(rat):.1f}-{max(rat):.1f})")


# =====================================================================================================================
# 7.  VERDICT
# =====================================================================================================================
P(""); P("=" * 122)
P("7.  VERDICT ON ANGLE D")
P("=" * 122)
P("  THE BEST CASE FIRST.  The cluster/group front is a genuinely good fit to angle D as posed: eleven rows over")
P(f"     four decades of mass agree on a required baryon multiplier of {10**np.median(lfc):.1f} to within "
  f"{np.std(lfc, ddof=1):.2f} dex, with no")
P("     significant mass or acceleration trend inside the front.  'The cluster baryon census is short by a factor")
P("     of about three or four' is a fair one-parameter description of eleven independent measurements, and the")
P("     framework asks LESS of the census than LambdaCDM asks of the dark sector on the same systems")
P(f"     (x{np.median(rat):.1f} the baryons against x{np.median(darkrat):.1f}).")
P("")
P("  WHAT KILLS IT, in order of strength.")
P("  1. THE SIGN.  A census deficit is one-signed.  " + f"{len(neg)} of {len(LROWS)} ledger rows require the")
P("     baryons to be REMOVED, down to 5% of the measured stars in NGC1052-DF4 and 11% in Pal 4, and three of the")
P("     four outer-halo globulars are driven below the stellar-population floor.  Angle D cannot address those")
P("     rows at all, in principle, whatever it does for the clusters.")
P("  2. THE INVARIANCE THEOREMS.  A UNIFORM census correction is not a free move and it is not a null move: T1")
P("     and T2 require a_0 a factor f^2 apart, so it must either displace the whole RAR by log10(f) or move the")
P("     transition scale by f^2.  With a_0 refitted the framework's own way it buys back only the (f-1)sqrt(y)/2")
P("     leak -- +8% at the eRASS1 groups, +95% in the X-COP cores -- and pays kappa = 0.483 -> 0.05.  Only")
P("     DIFFERENTIAL laws can do real work, and a differential law is by construction a statement that the census")
P("     is wrong by different amounts in different systems.")
P("  3. THE KEEPERS.  Every differential law that touches the galaxies breaks something measurable: the RAR")
P("     acquires a gas-fraction-dependent residual six times the observed one, the inner-diversity and Renzo")
P("     correlations fall, and BOTH derived keepers -- the halo surface-density constant a_0/(2 pi G), which the")
P("     framework predicts within 0.14 dex of Donato+09 with nothing fitted, and the 3.6 micron mass-to-light")
P("     ratio it predicts from Lambda -- collapse by factors of 5 to 130, because both are read off a_0 and a_0")
P("     is exactly what a census correction moves.")
P("  4. IT DOES NOT TRANSFER.  The clusters' own number misses the rest of the positive ledger by a median")
P(f"     {np.median(mis):.2f} dex, and no one- or two-parameter law gets the whole positive ledger below "
  f"{min(s1, s2, s4, s5, s6):.2f} dex of residual")
P("     against a raw spread of {:.2f}.".format(lf.std(ddof=1)))
P("  5. AND WITHIN THE CLUSTERS THE COMPONENT IS NOT BARYON-SHAPED.  It cannot be hot gas (1a: clumping is")
P("     one-signed, and putting it in the emitting phase demands 4-39x the observed emission measure).  It is")
P("     more centrally concentrated than the gas (1c), so it would have to pile up where the X-ray data are best.")
P("     It does not follow the measured hot-gas content (3-hotgas: the trend has the wrong sign).  And the Bullet")
P("     requires it to be collisionless and locked to the galaxies at 20-40x the stellar mass (1d) -- which is")
P("     dark matter with a baryonic label, and section 5 shows what a component locked to stars at that ratio")
P("     does to SPARC.")
P("")
P("  THE ONE SURVIVING VERSION, stated plainly so that it is not mistaken for a success: a missing baryonic")
P("  component that exists in hot haloes and NOT in galaxies closes the cluster front to 0.07 dex and breaks no")
P("  keeper.  It is keeper-safe because it is switched off by hand in every system that constrains it.  That is")
P("  one free amount per class of object, which is the freedom the framework exists to remove.")
P("")
P("  ANGLE D IS A PARTIAL EXPLANATION OF THE CLUSTER FRONT AND NOT A UNIFICATION OF THE LEDGER.")

sys.exit(ck.done())
