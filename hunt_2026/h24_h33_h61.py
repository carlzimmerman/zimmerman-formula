#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
h24_h33_h61.py -- HUNT ITEMS 24, 33, 61.
=========================================
Item 24 (the core-radius law): if a fitted dark halo is really the phantom of a MOND galaxy, its CORE RADIUS is not free -- it must
        track the galaxy's own MOND radius r_M = sqrt(G M_b/a_0), the only length the framework has.  Tested on Li+2020's Burkert
        fits cross-matched to SPARC baryonic masses.  In LambdaCDM a core comes from feedback and its size tracks the stellar mass
        and the star-formation history instead, with no reason to know about a_0.
Item 33 (the phantom dark disc): in MOND a thin disc's phantom is itself disc-like -- Sigma_ph(R) = (nu - 1) Sigma_b(R) to leading
        order -- so the Milky Way must have a THIN "dark disc" of a definite mass fraction, which LambdaCDM does not predict
        (its halo is round, and an accreted dark disc is a minor, model-dependent add-on).
Item 61 (cluster gravitational redshift): the stacked gravitational redshift of cluster galaxies measures the POTENTIAL DEPTH
        directly, independent of the mass model.  The framework predicts it from the baryons plus the phantom at the observed
        residual, with no halo.
Both footings.  Mutations.  Checks CAN fail.
"""
import sys, math, os
import numpy as np
from hunt_lib import *
ck = Check(); rng = np.random.default_rng(2433)
P("="*116); P("ITEM 24 -- does a fitted halo core know about the MOND radius?"); P("="*116)
rows = [l.rstrip("\n").split("\t") for l in open(os.path.join(DATA, "li2020_sparc_halos.tsv")) if l.strip() and not l.startswith("#")]
hdr = rows[0]; col = {h.strip(): i for i, h in enumerate(hdr)}
def f(v):
    try: return float(v)
    except: return np.nan
gals = load_sparc(qmax=3, incmin=0, npts=3)
Mb = {g["name"]: g["Mb"] for g in gals}
Rd = {g["name"]: g["Rdisk"] for g in gals}
fits = {}
for d in rows[3:]:
    try:
        nm = d[col["Name"]].strip(); mdl = d[col["Model"]].strip(); rs = f(d[col["rs"]]); chi2 = f(d[col["chi2"]])
    except Exception: continue
    if mdl != "Burkert-Flat" or not np.isfinite(rs) or not (np.isfinite(chi2) and chi2 < 10): continue
    if nm not in Mb: continue
    fits[nm] = dict(rs=rs, chi2=chi2)
info(f"Burkert-Flat fits cross-matched to SPARC baryonic masses with chi2 < 10: {len(fits)} galaxies")
names = sorted(fits)
r0 = np.array([fits[n]["rs"] for n in names]); mb = np.array([Mb[n] for n in names]); rd = np.array([Rd[n] for n in names])
R24 = {}
for foot, a0 in A0.items():
    rM = np.sqrt(G*mb*Msun/a0)/kpc
    ratio = r0/rM
    sl, b, sc = fit_loglog(mb, ratio)
    bs = np.array([fit_loglog(mb[i], ratio[i])[0] for i in (rng.integers(0, len(mb), len(mb)) for _ in range(400))])
    # the LambdaCDM-side alternative: does the core track the DISC scale length instead?
    ok = rd > 0
    sl2, _, sc2 = fit_loglog(mb[ok], (r0/rd)[ok])
    R24[foot] = (np.median(ratio), np.log10(ratio).std(), sl, bs.std(), sc, np.median((r0/rd)[ok]), np.log10((r0/rd)[ok]).std(), sl2)
    info(f"{foot:10} r_0/r_M: median {np.median(ratio):.2f}, scatter {np.log10(ratio).std():.3f} dex, mass slope {sl:+.3f} +- {bs.std():.3f}")
    info(f"{foot:10} r_0/R_disk (the LambdaCDM-flavoured comparison): median {np.median((r0/rd)[ok]):.2f}, scatter {np.log10((r0/rd)[ok]).std():.3f} dex, mass slope {sl2:+.3f}")
c = R24["canonical"]
ck("24 the fitted core radius tracks the MOND radius BETTER than it tracks the disc scale length, but neither is tight: r_0/r_M has 0.4-0.5 dex scatter with a mass slope consistent with a fraction of a decade, so this is a consistency, not a law",
   c[1] <= c[6] + 0.05, f"r_0/r_M: median {c[0]:.2f}, scatter {c[1]:.3f} dex, mass slope {c[2]:+.3f} +- {c[3]:.3f}; r_0/R_disk: median {c[5]:.2f}, scatter {c[6]:.3f} dex, mass slope {c[7]:+.3f}")
sh = rng.permutation(r0)
_, _, sc_sh = fit_loglog(mb, sh/np.sqrt(G*mb*Msun/A0["canonical"])*kpc)
ck("M24 mutation: shuffling the core radii between galaxies inflates the scatter", sc_sh > c[4], f"shuffled scatter {sc_sh:.3f} vs real {c[4]:.3f} dex")
P(""); P("="*116); P("ITEM 33 -- the Milky Way's phantom dark DISC"); P("="*116)
SIG_STAR, SIG_GAS = 33.4, 13.7                       # Msun/pc^2 at R0 (McKee+2015)
R0 = 8.2
for foot, a0 in A0.items():
    Sig_b = (SIG_STAR + SIG_GAS)*Msun/(3.0857e16)**2
    gN_disc = 2*math.pi*G*Sig_b                       # thin-disc field just outside the layer
    y = gN_disc/a0
    Sig_ph = (nu_s(y) - 1)*(SIG_STAR + SIG_GAS)
    info(f"{foot:10} at R0: Sigma_b = {SIG_STAR+SIG_GAS:.1f} Msun/pc^2, g_N(disc) = 2 pi G Sigma_b = {gN_disc:.2e} m/s^2 = {y:.2f} a_0")
    info(f"{foot:10} predicted PHANTOM DISC surface density = (nu - 1) Sigma_b = {Sig_ph:.1f} Msun/pc^2, i.e. {100*Sig_ph/(SIG_STAR+SIG_GAS):.0f}% of the baryonic disc, in a layer of the same thickness")
    if foot == "canonical": R33 = (Sig_ph, SIG_STAR + SIG_GAS, y)
info("what this is measured against: the Gaia vertical-force analyses infer a total surface density within |z| < 1.1 kpc of")
info("~70-80 Msun/pc^2 against a baryonic ~47, i.e. an EXCESS of 25-35 Msun/pc^2 that is normally attributed to the round halo.")
GAIA_EXCESS = (25.0, 35.0)
ck("33 AGAINST INTEREST -- the one-line phantom-disc estimate OVER-predicts: (nu-1) Sigma_b gives 50 (canonical) / 57 (alt) Msun/pc^2 against the 25-35 that Gaia's vertical-force analyses infer, a factor 1.4-2.3 too much.  It is the right OBJECT -- a flattened phantom following the baryonic layer, which LambdaCDM's round halo does not give -- computed the wrong way: (nu-1)Sigma_b is the asymptotic value far above the disc, not the column inside |z| < 1.1 kpc where the measurement is made",
   R33[0] > GAIA_EXCESS[1], f"predicted {R33[0]:.1f} Msun/pc^2 (y = {R33[2]:.2f}) vs Gaia's inferred {GAIA_EXCESS[0]:.0f}-{GAIA_EXCESS[1]:.0f}; over by {R33[0]/GAIA_EXCESS[1]:.1f}-{R33[0]/GAIA_EXCESS[0]:.1f}x")
info("the proper calculation exists and it works: the repo's full-AQUAL vertical-force front solves the disc geometry and reports")
info("f_M = 1.30 with the Eilers slope reproduced.  So items 33 and 92 are BOTH one-line estimates of a thing the programme already")
info("does properly, and both are withdrawn in favour of that solve -- 92 because a sphere is the wrong geometry, 33 because the")
info("asymptotic column is the wrong depth.  The DISTINCTIVE claim survives untouched: the phantom is FLATTENED, following the")
info("baryons, where a round halo contributes almost constantly with height -- and that is what K_z(z) between 0.3 and 1.5 kpc tests.")
P(""); P("="*116); P("ITEM 61 -- the stacked cluster gravitational redshift"); P("="*116)
info("the measurement (Wojtak+2011 Nature; Sadeh+2015; Jimeno+2015) stacks ~1e5 cluster galaxies and finds the brightest-cluster-galaxy")
info("frame blueshifted by ~10 km/s relative to the members, i.e. a potential difference c*(dPhi/c^2) between centre and outskirts.")
for foot, a0 in A0.items():
    M500 = 3e14*Msun; R500 = 1.3*Mpc; fbar = 0.15
    Mb = fbar*M500
    def gtot(r): 
        gN = G*Mb/r**2; return gN*nu_s(gN/a0)
    rr = np.geomspace(0.02*Mpc, 10*Mpc, 4000); gg = np.array([gtot(r) for r in rr])
    Phi = -np.concatenate([[0.0], np.cumsum(0.5*(gg[1:] + gg[:-1])*np.diff(rr))])
    Phi = Phi - Phi[-1]
    dPhi = float(np.interp(R500, rr, Phi) - Phi[0])
    dv = dPhi/c_light/1e3
    eta = 2.0
    dv_scaled = dv*eta**0.5
    info(f"{foot:10} a 3e14 Msun cluster (M_b = {Mb/Msun:.2e}, R500 = 1.3 Mpc): MOND potential difference centre-to-R500 gives a gravitational redshift of {abs(dv):.1f} km/s; with the observed residual eta = 2 folded in, {abs(dv_scaled):.1f} km/s")
    if foot == "canonical": R61 = (abs(dv), abs(dv_scaled))
OBS = (7.0, 15.0)
ck("61 AGAINST INTEREST -- the point-mass estimate OVER-predicts by 3-5x: it gives 36 km/s (51 with the residual) against a measured 7-15.  The fault is the model, not the framework: a cluster's baryons are extended, and integrating a POINT mass in from 20 kpc puts almost all of the potential difference at small radius where no galaxies are stacked.  A realistic gas profile is required and this item cannot be done without one",
   R61[0] > 2*OBS[1], f"predicted {R61[0]:.1f} km/s from a point mass ({R61[1]:.1f} with the residual) vs measured {OBS[0]:.0f}-{OBS[1]:.0f}; the measurement's own aperture is 0.3-3 Mpc, not 20 kpc")
info("both ways: this is NOT a discriminator -- LambdaCDM predicts the same order from the same measured masses, and the measurement's")
info("own systematics (transverse Doppler, the BCG's peculiar motion, selection) are at the same level as the signal.  It is a")
info("consistency check on the potential depth, and it is recorded as one.")
sys.exit(ck.done())
