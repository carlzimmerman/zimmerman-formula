#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
h67_hff_cores.py -- HUNT ITEM 67: eta at 20-100 kpc in the four Hubble Frontier Fields clusters.
=================================================================================================
The item asks for eta(r) = M_lens(<r)/M_framework(<r) in the cores of A2744, AS1063, MACS0416 and MACS1149,
to +-0.1 per cluster, as a test of the "23-33% core lever" the cluster paper leans on.

VERDICT UP FRONT: NOT RUNNABLE from the on-disk tables, and this script's job is to show that with numbers
rather than to assert it.  `real_research/data/hff_granata_*.tsv` is VizieR J/A+A/709/A254 (Granata+2026),
which is MEMBER PHOTOMETRY -- ID, RA, Dec, F814W, circularised effective radius, Sersic index, F160W -- and
nothing else.  There is no convergence map, no lens-model mass profile, no X-ray gas profile and no velocity
dispersion in it.  eta needs BOTH M_lens(<r) and M_baryon(<r); the tables carry a minority share of one of
the two terms.

What this script does instead, all of it computable from the tables plus first principles:
  (1) proves the absence, column by column, and measures how sparsely the cores are even sampled;
  (2) builds the member stellar mass profile M_*(<R) for each cluster on two independent bands (F160W and
      F814W with separate mass-to-light ratios) so the photometric part is at least quantified and cross-checked;
  (3) computes Sigma_crit(z_lens, z_source = 2) from the repo cosmology and reports what fraction of the
      strong-lensing surface density the member stars can be -- the size of the term that is MISSING;
  (4) computes the Route A kernel boost nu(y) across 20-100 kpc, on both a_0 footings, and shows that it is
      NOT a parameter-free number there: it runs from 1.0 to 3.2 over the plausible baryon range, so the
      "23-33% core lever" is a statement about an assumed baryon budget, not a prediction of the kernel;
  (5) solves for the baryon mass the framework would NEED at 50 kpc to make the cluster a strong lens at all,
      and compares it with what the members supply;
  (6) computes the LambdaCDM/NFW alternative at the same radii.
Both footings.  Checks that can fail.  Three mutation controls.
"""
import os, sys, math
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
from hunt_lib import *

ck = Check(); rng = np.random.default_rng(67)
DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "real_research", "data")
c_kms = 299792.458; H0_kms = 100*h
Ez = lambda z: math.sqrt(OM_M*(1 + z)**3 + OM_L)
def DC_Mpc(z): return quad(lambda t: c_kms/(H0_kms*Ez(t)), 0.0, z)[0]
def DA_Mpc(z): return DC_Mpc(z)/(1 + z)
def DA12_Mpc(z1, z2): return (DC_Mpc(z2) - DC_Mpc(z1))/(1 + z2)     # flat universe
def Sigma_crit(zl, zs):
    Dl, Ds, Dls = DA_Mpc(zl)*Mpc, DA_Mpc(zs)*Mpc, DA12_Mpc(zl, zs)*Mpc
    return c_light**2*Ds/(4*math.pi*G*Dl*Dls)                        # kg m^-2

CLUSTERS = {"a2744": ("Abell 2744",   0.307),
            "as1063": ("AS1063",      0.348),
            "m0416": ("MACS J0416",   0.396),
            "m1149": ("MACS J1149",   0.542)}
MSUN_AB = 4.5          # AB absolute magnitude of the Sun, near enough in both bands; the residual sits in M/L
ML_160, ML_814 = 1.2, 3.0     # rest-frame near-IR and rest-frame optical mass-to-light, red passive members

def read_hff(key):
    path = os.path.join(DATA, f"hff_granata_{key}.tsv")
    rows = [l.rstrip("\n").split("\t") for l in open(path, encoding="latin-1") if l.strip() and not l.startswith("#")]
    hdr = [x.strip() for x in rows[0]]; body = rows[3:]
    idx = {k: i for i, k in enumerate(hdr)}
    def num(k):
        out = []
        for r in body:
            try: out.append(float(r[idx[k]].strip()))
            except Exception: out.append(np.nan)
        return np.array(out)
    return hdr, dict(ra=num("RAJ2000"), dec=num("DEJ2000"), f814=num("F814W"), f160=num("F160W"),
                     re=num("ReF814W"), n=num("nF814W"))

P("="*120)
P("ITEM 67 -- eta at 20-100 kpc in the four HFF clusters.  Step 1: what is actually in the on-disk tables.")
P("="*120)
HDRS = {}
for k, (nm, z) in CLUSTERS.items():
    hdr, d = read_hff(k)
    HDRS[k] = hdr
    info(f"{nm:14s} z = {z:.3f}   N members = {len(d['ra']):4d}   columns = {hdr}")
allcols = sorted({c.lower() for hdr in HDRS.values() for c in hdr})
mass_words = ("mass", "mtot", "logm", "sigma", "vdisp", "kappa", "conv", "m500", "m200", "shear", "kt", "mgas")
found = [w for w in mass_words if any(w in c for c in allcols)]
ck("67 the tables carry NO mass information -- every column is photometric or positional (ID, RA, Dec, F814W, effective radius, Sersic index, F160W).  No convergence, no lens-model mass, no velocity dispersion, no gas.  eta cannot be formed from them at any radius",
   len(found) == 0, f"searched for {mass_words}; matched columns: {found if found else 'none'}; full column set {allcols}")

# ---------------------------------------------------------------- radial sampling of the cores
P(""); P("="*120)
P("Step 2: how well do these member catalogues even sample 20-100 kpc?")
P("="*120)
CORE = {}
info(f"{'cluster':14s} {'kpc/arcsec':>11} {'N<20kpc':>9} {'N 20-100':>9} {'N<100':>7} {'N<250':>7} {'max R (kpc)':>12}")
for k, (nm, z) in CLUSTERS.items():
    _, d = read_hff(k)
    da = DA_Mpc(z); kpc_as = da*1e3*(math.pi/(180*3600))
    j = int(np.nanargmin(d["f160"]))                                  # brightest member in F160W = BCG proxy = centre
    R = np.hypot((d["ra"] - d["ra"][j])*math.cos(math.radians(d["dec"][j])), d["dec"] - d["dec"][j])*3600*kpc_as
    CORE[k] = dict(z=z, R=R, d=d, kpc_as=kpc_as, j=j, da=da)
    info(f"{nm:14s} {kpc_as:11.2f} {int(np.sum(R < 20)):9d} {int(np.sum((R >= 20) & (R < 100))):9d} "
         f"{int(np.sum(R < 100)):7d} {int(np.sum(R < 250)):7d} {np.nanmax(R):12.0f}")
nmin = min(int(np.sum(CORE[k]["R"] < 100)) for k in CLUSTERS)
nmax = max(int(np.sum(CORE[k]["R"] < 100)) for k in CLUSTERS)
ck("67 the cores are sparsely sampled even in the one quantity the tables DO carry: between 5 and 36 members lie inside 100 kpc of the brightest member, so a radial profile in 20-100 kpc rests on a handful of galaxies per cluster and one cluster (MACS J1149) has essentially none",
   nmin < 10 and nmax < 60, f"members inside 100 kpc: {[int(np.sum(CORE[k]['R'] < 100)) for k in CLUSTERS]} for {[CLUSTERS[k][0] for k in CLUSTERS]}")

# ---------------------------------------------------------------- member stellar mass, two bands
P(""); P("="*120)
P("Step 3: the member stellar mass profile, built twice from two bands as its own cross-check.")
P("="*120)
info("distance modulus from the repo cosmology; no k-correction (it is absorbed into M/L, stated, not fitted);")
info(f"M/L = {ML_160} on F160W (rest-frame ~1 micron at these redshifts) and {ML_814} on F814W (rest-frame ~0.6 micron).")
info(f"{'cluster':14s} {'M*(<50) F160W':>15} {'M*(<50) F814W':>15} {'ratio':>7} {'M*(<100) F160W':>16} {'BCG M*':>11}")
for k, (nm, z) in CLUSTERS.items():
    C = CORE[k]; d = C["d"]; R = C["R"]
    DL = C["da"]*(1 + z)**2
    DM = 5*math.log10(DL*1e6/10)
    L160 = 10**(-0.4*(d["f160"] - DM - MSUN_AB)); L814 = 10**(-0.4*(d["f814"] - DM - MSUN_AB))
    C["Ms160"] = ML_160*L160; C["Ms814"] = ML_814*L814
    m50 = R < 50; m100 = R < 100
    C["M50_160"] = float(np.nansum(C["Ms160"][m50])); C["M50_814"] = float(np.nansum(C["Ms814"][m50]))
    C["M100_160"] = float(np.nansum(C["Ms160"][m100]))
    info(f"{nm:14s} {C['M50_160']:15.3e} {C['M50_814']:15.3e} {C['M50_814']/C['M50_160']:7.2f} "
         f"{C['M100_160']:16.3e} {ML_160*L160[C['j']]:11.3e}")
band_ratios = np.array([CORE[k]["M50_814"]/CORE[k]["M50_160"] for k in CLUSTERS])
ck("M67-1 mutation control -- the two photometric bands, with independent mass-to-light ratios, give the same enclosed stellar mass to within 30% in all four clusters, so the stellar term is not an artefact of one band's calibration.  It is also the ONLY term the tables can supply",
   np.all(np.abs(band_ratios - 1) < 0.30), f"M*(F814W)/M*(F160W) inside 50 kpc = {np.round(band_ratios, 2).tolist()}")

# ---------------------------------------------------------------- the size of the missing term
P(""); P("="*120)
P("Step 4: how big is the term the tables do NOT carry?  Sigma_crit from the repo cosmology, source at z = 2.")
P("="*120)
info("These four fields are the Frontier Fields BECAUSE they are among the strongest known lenses -- giant arcs at")
info("20-40 arcsec, i.e. mean convergence of order unity out to ~100-200 kpc.  Taking kappa_bar = 1 at 50 kpc as a")
info("deliberately CONSERVATIVE reference, the projected mass inside 50 kpc must be at least pi R^2 Sigma_crit.")
info(f"{'cluster':14s} {'Sigma_crit':>16} {'M_E(<50 kpc)':>14} {'M*_mem(<50)':>13} {'members / needed':>17}")
frac = {}
for k, (nm, z) in CLUSTERS.items():
    C = CORE[k]
    Sc = Sigma_crit(z, 2.0)                                          # kg/m^2
    Sc_msun_kpc2 = Sc/Msun*kpc**2
    ME = math.pi*50.0**2*Sc_msun_kpc2
    C["Sc"] = Sc_msun_kpc2; C["ME50"] = ME
    frac[k] = C["M50_160"]/ME
    info(f"{nm:14s} {Sc_msun_kpc2:12.3e} Msun/kpc2 {ME:14.3e} {C['M50_160']:13.3e} {100*frac[k]:16.1f}%")
fmax = max(frac.values())
ck("67 the missing term dominates: the tabulated member stars are 2-16% of the projected mass needed for strong lensing at 50 kpc, and the ICM, the intracluster light and the BCG halo -- none of which are in these tables -- must supply the rest.  A baryon budget known only to that fraction of itself cannot yield eta to +-0.1",
   fmax < 0.25, f"member stars / lensing mass inside 50 kpc = {', '.join(f'{CLUSTERS[k][0]} {100*frac[k]:.1f}%' for k in CLUSTERS)}")

# ---------------------------------------------------------------- what the kernel actually does at these radii
P(""); P("="*120)
P("Step 5: the Route A kernel across 20-100 kpc.  Is the '23-33% core lever' a prediction or an assumption?")
P("="*120)
info(f"{'r (kpc)':>8} {'M_b (Msun)':>12} {'y = g_b/a_0 can':>16} {'nu canonical':>13} {'y alt':>9} {'nu alt':>8}")
nus = []
for r in (20.0, 50.0, 100.0):
    for Mb in (1e12, 3e12, 1e13):
        g = G*Mb*Msun/(r*kpc)**2
        yc, ya = g/A0["canonical"], g/A0["alt"]
        nus.append((r, Mb, nu_s(yc), nu_s(ya)))
        info(f"{r:8.0f} {Mb:12.1e} {yc:16.2f} {nu_s(yc):13.3f} {ya:9.2f} {nu_s(ya):8.3f}")
nu_lo = min(min(x[2], x[3]) for x in nus); nu_hi = max(max(x[2], x[3]) for x in nus)
ck("67 AGAINST INTEREST -- the core lever is NOT a parameter-free prediction.  Over the plausible enclosed-baryon range at 20-100 kpc the Route A boost nu runs from 1.00 to 3.38 on the two footings; a '23-33%' core boost picks out one particular baryon budget rather than following from the kernel.  Quoting 23-33% as a prediction requires the baryon profile that these tables do not contain",
   nu_lo < 1.05 and nu_hi > 2.5, f"nu spans {nu_lo:.3f} to {nu_hi:.3f} over r = 20-100 kpc and M_b = 1e12-1e13 Msun, both footings")

# what baryon mass would the framework need to make the cluster a strong lens at 50 kpc?
PROJ = math.pi/2      # M_2D(<R)/M_3D(<R) for a singular isothermal sphere; larger for a cuspier profile
P(""); info("inverting the kernel: the baryon mass the framework needs inside 50 kpc for nu(y) M_b to reach the lensing")
info("mass, against what the member stars actually provide.  APPROXIMATION STATED: the kernel is evaluated on the 3-D")
info(f"enclosed mass while M_E is projected, so the requirement is quoted twice -- once against M_E and once against")
info(f"M_E / (pi/2) = M_E/{PROJ:.2f}, the isothermal-sphere deprojection, which is the conservative end.")
info(f"{'cluster':14s} {'footing':>10} {'M_b req (2D)':>13} {'M_b req (3D)':>13} {'nu there':>9} {'M*_mem(<50)':>13} {'shortfall 2D':>13} {'shortfall 3D':>13}")
short, short3 = [], []
for k, (nm, z) in CLUSTERS.items():
    C = CORE[k]
    for foot, a0 in A0.items():
        def solve(target):
            def f(lm):
                Mb = 10**lm
                return Mb*nu_s(G*Mb*Msun/(50.0*kpc)**2/a0) - target
            return 10**brentq(f, 9.0, 15.0, xtol=1e-10)
        Mreq = solve(C["ME50"]); Mreq3 = solve(C["ME50"]/PROJ)
        nu_there = nu_s(G*Mreq*Msun/(50.0*kpc)**2/a0)
        short.append(Mreq/C["M50_160"]); short3.append(Mreq3/C["M50_160"])
        info(f"{nm:14s} {foot:>10} {Mreq:13.3e} {Mreq3:13.3e} {nu_there:9.3f} {C['M50_160']:13.3e} "
             f"{Mreq/C['M50_160']:13.1f} {Mreq3/C['M50_160']:13.1f}")
ck("67 AGAINST INTEREST -- even with its own kernel switched on, the framework needs 6-40 times more baryonic mass inside 50 kpc than the tabulated member galaxies contain (3.6-24 on the conservative deprojected version), because at these radii nu has fallen to about 1.05 for the masses in question.  Whether the ICM plus the BCG halo plus the intracluster light close that gap is exactly the measurement the item wanted and exactly what the tables cannot answer",
   min(short3) > 3.0, f"required M_b / member M* inside 50 kpc = {min(short):.1f}-{max(short):.1f} projected, {min(short3):.1f}-{max(short3):.1f} deprojected, across four clusters and both footings")

# ---------------------------------------------------------------- the LambdaCDM alternative at the same radii
P(""); P("="*120)
P("Step 6: the LambdaCDM alternative computed at the same radii -- an NFW halo, c200 = 5, M200 = 1e15 Msun.")
P("="*120)
def nfw_M(r_kpc, M200, c200, z):
    rho_c = rho_crit*Ez(z)**2
    r200 = (M200*Msun/(200*rho_c*(4*math.pi/3)))**(1/3)/kpc
    rs = r200/c200
    m = lambda x: math.log(1 + x) - x/(1 + x)
    return M200*m(r_kpc/rs)/m(c200), r200
for k, (nm, z) in CLUSTERS.items():
    M50, r200 = nfw_M(50.0, 1e15, 5.0, z)
    M100, _ = nfw_M(100.0, 1e15, 5.0, z)
    info(f"{nm:14s} r200 = {r200:6.0f} kpc; NFW M(<50 kpc) = {M50:.3e}, M(<100 kpc) = {M100:.3e} Msun (3-D); "
         f"projected at pi/2 -> {PROJ*M50:.3e} against the required {CORE[k]['ME50']:.3e}")
M50_nfw, _ = nfw_M(50.0, 1e15, 5.0, 0.35)
meanME = float(np.mean([CORE[k]["ME50"] for k in CLUSTERS]))
ck("67 the LambdaCDM side is not blocked by the same wall, but it is not effortless either: a single textbook NFW (M200 = 1e15, c = 5) supplies 8e12 Msun inside 50 kpc in 3-D, about 1.2e13 projected, which is 0.7 of what strong lensing needs -- the real Frontier Fields close that with high concentration and merging substructure.  The framework has to find the SAME 1.5e13 in BARYONS with a kernel boost of only ~5% there, so the core is where the two pictures differ most and the item was worth asking even though the tables cannot answer it",
   0.3*meanME < PROJ*M50_nfw < 1.5*meanME,
   f"NFW 3-D M(<50 kpc) = {M50_nfw:.2e} Msun, projected {PROJ*M50_nfw:.2e}, against a mean required M_E(<50 kpc) = {meanME:.2e} Msun (ratio {PROJ*M50_nfw/meanME:.2f})")

# ---------------------------------------------------------------- mutation controls
P(""); P("="*120)
P("mutation controls")
P("="*120)
C = CORE["as1063"]
scr = []
for _ in range(400):
    ra = C["d"]["ra"][C["j"]] + rng.normal(0, 0.02, len(C["d"]["ra"]))       # scatter members over ~1 arcmin
    dec = C["d"]["dec"][C["j"]] + rng.normal(0, 0.02, len(C["d"]["dec"]))
    R = np.hypot((ra - C["d"]["ra"][C["j"]])*math.cos(math.radians(C["d"]["dec"][C["j"]])), dec - C["d"]["dec"][C["j"]])*3600*C["kpc_as"]
    scr.append(np.nansum(C["Ms160"][R < 50]))
ck("M67-2 mutation control -- randomising the member sky positions over the same field destroys the enclosed-mass concentration, so the M_*(<50 kpc) measured above is a real central concentration and not an artefact of the aperture",
   np.mean(scr) < 0.5*C["M50_160"], f"true M*(<50 kpc) = {C['M50_160']:.2e} Msun, randomised {np.mean(scr):.2e} +- {np.std(scr):.2e}")

g50 = G*3e12*Msun/(50.0*kpc)**2
ck("M67-3 mutation control -- a wrong a_0 changes the core boost by a measurable amount, so the kernel is genuinely live at these radii and the null result above is about missing DATA and not about an inert kernel",
   abs(nu_s(g50/(10*A0["canonical"])) - nu_s(g50/A0["canonical"])) > 0.15,
   f"nu at 50 kpc with M_b = 3e12: {nu_s(g50/A0['canonical']):.3f} (canonical), {nu_s(g50/A0['alt']):.3f} (alt), {nu_s(g50/(10*A0['canonical'])):.3f} (10 a_0)")

P(""); P("="*120)
P("VERDICT")
P("="*120)
info("67 = NOT RUNNABLE, not a null.  The item asks for eta = M_lens/M_framework to +-0.1 at 20-100 kpc; the on-disk")
info("HFF tables are member photometry (Granata+2026 structural parameters) with no mass column of any kind, 5-36")
info("members inside 100 kpc, and a stellar term that is 2-16% of the mass strong lensing requires there.")
info("What would make it runnable, stated so the next pass does not repeat this: (a) a published lens-model")
info("convergence map or cumulative M(<R) for each cluster, and (b) an X-ray gas profile into the core.  With those")
info("two the computation is short -- the kernel part is already written above and takes one line per radius.")
info("Recorded honestly: the parts that COULD be computed from the tables were, and two of them are results in their")
info("own right -- the kernel boost at 20-100 kpc is not a fixed 23-33% but a function of an unmeasured baryon")
info("budget, and the framework needs 6-40x (3.6-24x deprojected) the tabulated member stellar mass in the core to")
info("lens at all, with the kernel contributing only about 5% of it.")
sys.exit(ck.done())
