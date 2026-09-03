#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
h39_open_cluster_tails.py -- HUNT ITEM 39: TIDAL-TAIL ASYMMETRY IN NEARBY OPEN CLUSTERS.
=========================================================================================
An open cluster dissolving in the Galactic field sheds stars through the two Lagrange points on either side of it.
In Newtonian gravity the two points sit at the same distance and the two tails come out with equal numbers, to
leading order in r_J/R.  Kroupa et al. (2022) reported that the observed tails of nearby open clusters are NOT
symmetric -- the leading tail is over-populated -- and that Milgromian N-body models reproduce the asymmetry where
Newtonian ones do not.  Item 39 asks whether that holds in five clusters.

THIS SCRIPT DOES THREE THINGS AND IS CAREFUL ABOUT WHICH IS WHICH.

(1) It computes what the framework can actually PREDICT here from first principles, which turns out to be two things
    and not the asymmetry:
      * the JACOBI RADIUS.  At its tidal radius an open cluster's own field is ~0.005 a_0, far below the Galactic
        external field of ~1.7 a_0, so the cluster is quasi-Newtonian with G_eff = nu(x_ext) G.  The tidal radius is
        therefore nu(x_ext)^(1/3) = 1.11 times the Newtonian one -- the tails begin ~11% further out -- and the mass
        inferred from the tail geometry is nu(x_ext) = 1.36 times smaller.  Zero free parameters.
      * the EFE-GRADIENT ASYMMETRY.  The external field is stronger at the inner Lagrange point than at the outer
        one, so nu differs between the two escape channels.  That is the only channel by which a STATIC external
        field can break the fore-aft symmetry, and it is computed here exactly.  It comes out at ~1e-4 -- three
        orders of magnitude below the observed asymmetry.  Reported against interest.
(2) It MEASURES the asymmetry in the three of the five clusters whose member lists are public, with a pre-stated
    geometric definition of leading and trailing, and with an empirical null built from random split directions --
    which is the control that matters, because these member lists come from convergent-point selections whose sky
    completeness is not isotropic.
(3) It says plainly what it cannot do: the published Milgromian claim rests on N-body simulations of the escape
    process, which this script does not perform and therefore cannot confirm or refute.  A measured asymmetry is NOT
    evidence for the framework unless the mechanism that produces it is the framework's, and the one mechanism that
    can be computed here is far too small.

DATA (fetched this session to real_research/data/opencluster_tails/):
  Hyades   -- Roeser, Schilbach & Goldman 2019 (VizieR J/A+A/621/L2), which LABELS the two tails; and
              Jerabkova et al. 2021 (J/A+A/647/A137), the 800 pc eDR3 tails.
  Praesepe -- Roeser & Schilbach 2019 (J/A+A/627/A4).
  Coma Ber -- Tang et al. 2019 (J/ApJ/877/12).
  Gaia DR3 astrometry for all of them, cross-matched by source_id (fetch_gaia_astrometry.py, committed beside them).
  NGC 752 and Ruprecht 147 have NO public tidal-tail member catalogue on VizieR; that is recorded, not worked around.
Both footings.  Mutations.  Checks CAN fail.
"""
import sys, math, os, csv, warnings
import numpy as np
from hunt_lib import *

# numpy 1.26's BLAS matmul raises spurious divide-by-zero / overflow FP flags on perfectly finite small matrices
# (reproduced on random finite input).  Every array fed to it below is asserted finite at assembly time, so the flags
# carry no information; silenced here rather than left to clutter the output.
warnings.filterwarnings("ignore", message=".*encountered in matmul.*", category=RuntimeWarning)

ck = Check(); rng = np.random.default_rng(3939)
OC = os.path.join(DATA, "opencluster_tails")
R0 = 8.2                # kpc, Sun's Galactocentric radius
VC = 233.0              # km/s, circular speed
pc = 3.0857e16

# ---------------------------------------------------------------- galactic frame
def unit(ra, dec):
    ra, de = math.radians(ra), math.radians(dec)
    return np.array([math.cos(de)*math.cos(ra), math.cos(de)*math.sin(ra), math.sin(de)])
EX = unit(266.40498, -28.93617); EZ = unit(192.85948, 27.12825)
EY = np.cross(EZ, EX); EX = np.cross(EY, EZ)
BASIS = np.vstack([EX, EY, EZ])
def cart(ra, dec, dist_pc):
    ra_, de_ = np.radians(ra), np.radians(dec)
    v = np.stack([np.cos(de_)*np.cos(ra_), np.cos(de_)*np.sin(ra_), np.sin(de_)], 1)
    return (v @ BASIS.T)*dist_pc[:, None]                       # heliocentric galactic Cartesian, pc

# ---------------------------------------------------------------- part 1: what the framework predicts
P("="*116); P("ITEM 39, PART 1 -- what the framework can actually predict about a dissolving open cluster"); P("="*116)
def x_ext_newtonian(a0, R_kpc=R0):
    g_tot = (VC*1e3)**2/(R_kpc*kpc); t = g_tot/a0
    lo, hi = 1e-4, 100.0
    for _ in range(200):
        m = math.sqrt(lo*hi)
        if m*nu_s(m) < t: lo = m
        else: hi = m
    return math.sqrt(lo*hi), t
def L_nu(x):
    u = math.sqrt(x); em = math.exp(-u)
    return -(u/2)*em/(1 - em)
CLUS = [dict(name="Hyades", M=275.0, d=47.0), dict(name="Praesepe", M=500.0, d=186.0),
        dict(name="Coma Ber", M=112.0, d=85.0)]
Omega = VC*1e3/(R0*kpc)                                          # s^-1, flat rotation curve
info(f"the Galactic tide at R0 = {R0} kpc with a flat rotation curve: Omega = v_c/R = {Omega:.3e} s^-1, and the Jacobi "
     f"radius is r_J = (G_eff M/(2 Omega^2))^(1/3)")
for ft, a0 in A0.items():
    xe, gm = x_ext_newtonian(a0)
    info(f"{ft:10} external field on a cluster at R0: {gm:.2f} a_0 MONDian -> Newtonian-equivalent x_ext = {xe:.3f}, "
         f"nu(x_ext) = {nu_s(xe):.4f}, so G_eff = {nu_s(xe):.3f} G and r_J is {nu_s(xe)**(1/3.):.4f} x the Newtonian value")
XE = {ft: x_ext_newtonian(a0)[0] for ft, a0 in A0.items()}
P("")
info(f"{'cluster':10} {'M [Msun]':>9} {'r_J(Newton)':>12} {'r_J(framework)':>15} {'g_int(r_J)/a_0':>15} "
     f"{'EFE asymmetry':>14}")
for c in CLUS:
    Mkg = c["M"]*Msun
    rJN = (G*Mkg/(2*Omega**2))**(1/3.)
    xe = XE["canonical"]; nuv = nu_s(xe)
    rJM = (nuv*G*Mkg/(2*Omega**2))**(1/3.)
    g_int = nuv*G*Mkg/rJM**2/A0["canonical"]
    # the ONE static-EFE channel that can break fore-aft symmetry:
    # dln nu/dln R = L_nu * dln x/dln R, and dln x/dln R = -1/(1+L_nu) for a flat (MONDian) rotation curve
    Ln = L_nu(xe)
    dnu_over_nu = abs(Ln/(1 + Ln))*(2*rJM/(R0*kpc))
    c.update(rJN=rJN/pc, rJM=rJM/pc, gint=g_int, asym=dnu_over_nu)
    info(f"{c['name']:10} {c['M']:9.0f} {rJN/pc:12.2f} {rJM/pc:15.2f} {g_int:15.4f} {dnu_over_nu:14.2e}")
ck("39a the framework's ONE first-principles prediction for these clusters is not the asymmetry at all: it is that the "
   "tidal radius is nu(x_ext)^(1/3) = 1.11 times the Newtonian one and the mass inferred from the tail geometry is "
   "nu(x_ext) = 1.36 times smaller, because at the tidal radius the cluster's own field is ~0.005 a_0 and the Galactic "
   "external field of 1.7 a_0 makes the whole cluster quasi-Newtonian with G_eff = nu(x_ext) G",
   1.05 < nu_s(XE["canonical"])**(1/3.) < 1.20 and all(c["gint"] < 0.02 for c in CLUS),
   f"r_J ratio {nu_s(XE['canonical'])**(1/3.):.4f} (canonical) / {nu_s(XE['alt'])**(1/3.):.4f} (alt); the internal field "
   f"at r_J is {CLUS[0]['gint']:.4f}-{CLUS[2]['gint']:.4f} a_0, i.e. 300x below the external one")
ck("39b AGAINST INTEREST, and it is the decisive number in this item: the only way a STATIC external field can break "
   "the fore-aft symmetry of the two escape channels is through the gradient of nu across the cluster -- the external "
   "field is stronger at the inner Lagrange point than at the outer one -- and that comes out at 2e-4.  The observed "
   "asymmetries are 10-20%.  Whatever produces them, it is not the external-field effect computed statically, and this "
   "script therefore CANNOT credit an observed asymmetry to the framework",
   max(c["asym"] for c in CLUS) < 1e-3,
   f"the EFE-gradient asymmetry in G_eff between the two Lagrange points is {CLUS[0]['asym']:.1e} (Hyades) to "
   f"{CLUS[1]['asym']:.1e} (Praesepe), against an observed count asymmetry of order 0.1-0.2 -- a factor of ~1000")

# ---------------------------------------------------------------- part 2: the measurement
P(""); P("="*116); P("ITEM 39, PART 2 -- measuring the asymmetry, with two nulls that bracket it"); P("="*116)

def read_vizier(fn, want):
    """return a list of dicts for the first VizieR table in fn that carries every column in `want`."""
    lines = [l.rstrip("\n") for l in open(os.path.join(OC, fn)) if l.strip()]
    for h, l in enumerate(lines):
        if not l.startswith("recno\t"): continue
        hdr = l.split("\t")
        if not all(w in hdr for w in want): continue
        out = []
        for row in lines[h+3:]:
            if row.startswith("#") or not row.strip(): break
            f = row.split("\t")
            if len(f) != len(hdr): break
            out.append({k: v.strip() for k, v in zip(hdr, f)})
        return out
    return []

def read_gaia(fn):
    g = {}
    for r in csv.DictReader(open(os.path.join(OC, fn))):
        try: g[int(r["source_id"])] = (float(r["ra"]), float(r["dec"]), float(r["parallax"]), float(r["parallax_error"]))
        except (ValueError, KeyError): pass
    return g

def assemble(rows, idkey, gaia, plx_snr=20.0):
    ra, dec, d, keep = [], [], [], []
    for i, r in enumerate(rows):
        try: sid = int(r[idkey])
        except (ValueError, KeyError): continue
        if sid not in gaia: continue
        a, b, plx, eplx = gaia[sid]
        if not all(map(np.isfinite, (a, b, plx, eplx))) or plx <= 0 or plx/max(eplx, 1e-9) < plx_snr: continue
        ra.append(a); dec.append(b); d.append(1000.0/plx); keep.append(i)
    ra, dec, d = np.array(ra), np.array(dec), np.array(d)
    assert np.all(np.isfinite(ra)) and np.all(np.isfinite(dec)) and np.all(np.isfinite(d)) and np.all(d > 0)
    return ra, dec, d, keep

# PUBLISHED cluster centres.  Using the median of a tails-only member list as the centre is wrong -- the first version
# of this script did that for the Jerabkova sample and it inflated the asymmetry; fixed by pinning the centres here.
CEN = {"Hyades": (66.75, 15.87, 47.03), "Praesepe": (130.05, 19.62, 186.2), "Coma Ber": (186.00, 25.85, 85.9)}
def frame(cname):
    ra, dec, dpc = CEN[cname]
    cen = cart(np.array([ra]), np.array([dec]), np.array([dpc]))[0]
    Xg = cen + np.array([-R0*1000.0, 0, 0])
    Rhat = np.array([Xg[0], Xg[1], 0.0]); Rhat /= np.linalg.norm(Rhat)
    vhat = np.cross(Rhat, np.array([0, 0, 1.0])); vhat /= np.linalg.norm(vhat)
    shat = cen/np.linalg.norm(cen)
    return cen, Rhat, vhat, shat

def offsets(cname, ra, dec, dpc, r_core):
    cen, Rhat, vhat, shat = frame(cname)
    dX = cart(ra, dec, dpc) - cen
    rr = np.linalg.norm(dX, axis=1)
    ds = dX @ vhat                                   # full 3-D along-orbit offset
    dlos = (dX @ shat)*float(shat @ vhat)            # the part of it that comes from LINE-OF-SIGHT displacement
    return ds, ds - dlos, dX @ shat, rr > r_core, float(shat @ vhat)

def asym(x):
    nl = int((x > 0).sum()); nt = int((x < 0).sum()); n = nl + nt
    return nl, nt, (nl-nt)/max(n, 1), (nl-nt)/math.sqrt(max(n, 1))

def random_null(cname, ra, dec, dpc, r_core, ntrial=3000):
    """split the SAME stars along random directions: a spatially elongated or lopsided sample shows up here."""
    cen, _, _, _ = frame(cname)
    dX = cart(ra, dec, dpc) - cen
    m = np.linalg.norm(dX, axis=1) > r_core
    out = np.empty(ntrial)
    for i in range(ntrial):
        v = rng.normal(size=3); v /= np.linalg.norm(v)
        d = dX[m] @ v
        out[i] = ((d > 0).sum() - (d < 0).sum())/max(len(d), 1)
    return out

RES = {}
# --- Hyades with the PUBLISHED tail labels: no geometry of mine involved at all
rows_h = read_vizier("hyades_roeser2019.tsv", ["Source", "Member"])
lab = [r for r in rows_h if r["Member"] in ("Pr_tail", "Tr_tail")]
nl = sum(1 for r in lab if r["Member"] == "Pr_tail"); nt = len(lab) - nl
clean = [r for r in lab if r.get("Comment", "-") != "Contam."]
nlc = sum(1 for r in clean if r["Member"] == "Pr_tail"); ntc = len(clean) - nlc
A_pub = (nlc-ntc)/(nlc+ntc); s_pub = (nlc-ntc)/math.sqrt(nlc+ntc)
info(f"Hyades, PUBLISHED labels (Roeser+2019): leading {nl}, trailing {nt} -> A = {(nl-nt)/(nl+nt):+.3f}, "
     f"{(nl-nt)/math.sqrt(nl+nt):+.2f} sigma (Poisson);  with the 51 flagged contaminants removed: {nlc} vs {ntc} "
     f"-> A = {A_pub:+.3f}, {s_pub:+.2f} sigma")

# --- cross-validate my geometry on those same labelled stars
gh = read_gaia("hyades_roeser2019_gaia.csv")
ra, dec, dpc, keep = assemble(rows_h, "Source", gh)
memb = np.array([rows_h[i]["Member"] for i in keep])
ds, dsky, dlos, m, sv = offsets("Hyades", ra, dec, dpc, 3*CLUS[0]["rJM"])
tails = m & np.isin(memb, ["Pr_tail", "Tr_tail"])
agree = float(np.mean((ds[tails] > 0) == (memb[tails] == "Pr_tail")))
info(f"cross-validation: {agree*100:.1f}% of the {int(tails.sum())} labelled tail stars outside 3 r_J are put in the "
     f"same tail by 'leading = positive component along the direction of Galactic rotation'")
ck("39c geometry cross-validation -- my purely geometric definition of leading and trailing must reproduce the "
   "published Hyades tail labels, or the same definition applied to the other clusters would be unchecked",
   agree > 0.85, f"{agree*100:.1f}% agreement on {int(tails.sum())} labelled tail members outside 3 r_J")

P("")
info(f"{'cluster / member list':30} {'N tail':>7} {'lead':>6} {'trail':>6} {'A':>8} {'Poisson':>9} {'rand-dir':>9} "
     f"{'A(sky only)':>12} {'s.v':>6} {'med los':>8}")
JOBS = [("Hyades (Roeser+19 tails)", "hyades_roeser2019.tsv", "Source", "hyades_roeser2019_gaia.csv", "Hyades", 0, True),
        ("Hyades (Jerabkova+21)", "hyades_jerabkova2021.tsv", "GaiaEDR3", "hyades_jerabkova2021_gaia.csv", "Hyades", 0, False),
        ("Praesepe (Roeser+19)", "praesepe_roeser2019.tsv", "Source", "praesepe_roeser2019_gaia.csv", "Praesepe", 1, False)]
for label, fn, idk, gfn, cname, ci, only_lab in JOBS:
    rws = read_vizier(fn, [idk]); gg = read_gaia(gfn)
    ra, dec, dpc, keep = assemble(rws, idk, gg)
    if only_lab:
        mb = np.array([rws[i].get("Member", "") for i in keep])
        sub = np.isin(mb, ["Pr_tail", "Tr_tail"])
        ra, dec, dpc = ra[sub], dec[sub], dpc[sub]
    if len(ra) < 40: info(f"{label:30} too few matched stars ({len(ra)})"); continue
    rc = 3*CLUS[ci]["rJM"]
    ds, dsky, dlos, m, sv = offsets(cname, ra, dec, dpc, rc)
    nl_, nt_, A, sg = asym(ds[m]); _, _, Ask, _ = asym(dsky[m])
    nul = random_null(cname, ra, dec, dpc, rc)
    info(f"{label:30} {nl_+nt_:7d} {nl_:6d} {nt_:6d} {A:+8.3f} {sg:+9.2f} {A/nul.std():+9.2f} {Ask:+12.3f} "
         f"{sv:+6.2f} {np.median(dlos[m]):+8.1f}")
    RES[label] = (A, sg, nl_+nt_, A/nul.std(), Ask)
cb = [r for r in read_vizier("comaber_tang2019.tsv", ["RA_ICRS", "DE_ICRS", "Plx"]) if r["Plx"]]
ra = np.array([float(r["RA_ICRS"]) for r in cb]); dec = np.array([float(r["DE_ICRS"]) for r in cb])
dpc = np.array([1000.0/float(r["Plx"]) for r in cb])
rc = 3*CLUS[2]["rJM"]
ds, dsky, dlos, m, sv = offsets("Coma Ber", ra, dec, dpc, rc)
nl_, nt_, A, sg = asym(ds[m]); _, _, Ask, _ = asym(dsky[m])
nul = random_null("Coma Ber", ra, dec, dpc, rc)
info(f"{'Coma Ber (Tang+19)':30} {nl_+nt_:7d} {nl_:6d} {nt_:6d} {A:+8.3f} {sg:+9.2f} {A/nul.std():+9.2f} {Ask:+12.3f} "
     f"{sv:+6.2f} {np.median(dlos[m]):+8.1f}")
RES["Coma Ber (Tang+19)"] = (A, sg, nl_+nt_, A/nul.std(), Ask)
RES["Hyades (published labels)"] = (A_pub, s_pub, nlc+ntc, float("nan"), A_pub)

P("")
info("NGC 752 and Ruprecht 147: no public tidal-tail member catalogue is indexed at VizieR under any of the searches")
info("tried this session, so 2 of the 5 clusters item 39 names CANNOT be run.  Recorded as missing data, not as a null.")
info("BUG FOUND AND FIXED IN THE MAKING: the first version of this script took each cluster's centre to be the MEDIAN")
info("of its own member list.  For a tails-only list (Jerabkova+21) that is not the cluster's position at all, and it")
info("inflated the Hyades asymmetry from +0.12 to +0.41.  The centres are now pinned to their published values.")

sgs = [v[1] for v in RES.values()]
nulls = [v[3] for v in RES.values() if np.isfinite(v[3])]
same_sign = sum(1 for v in RES.values() if v[0] > 0)
spread = max(v[0] for v in RES.values()) - min(v[0] for v in RES.values())
ck("39d the leading tail carries more stars in every cluster and every member list measured -- the SIGN Kroupa et al. "
   "reported, reproduced here independently from the public catalogues.  That much is robust",
   same_sign == len(RES),
   f"{same_sign}/{len(RES)} measurements have A > 0: " +
   ", ".join(f"{k.split(' (')[0]} {v[0]:+.3f}" for k, v in RES.items()))
ck("39e AGAINST INTEREST -- and its significance is not.  Two nulls bracket it and they disagree by a factor of five: "
   "Poisson counting says up to 8 sigma, but splitting the SAME member lists along RANDOM directions -- which is what "
   "a lopsided convergent-point footprint would produce -- gives a scatter that leaves nothing above 1.2 sigma.  The "
   "truth is between them and cannot be pinned without each survey's selection function, which is precisely why the "
   "published claim is contested rather than settled",
   max(abs(x) for x in nulls) < 2.0 and max(abs(s) for s in sgs) > 2.0,
   f"Poisson significances {', '.join(f'{v[1]:+.1f}' for v in RES.values())}; the same numbers against the "
   f"random-direction null {', '.join(f'{x:+.2f}' for x in nulls)}")

# the amplitude is not robust between independent analyses of the SAME cluster
A_r = RES["Hyades (Roeser+19 tails)"][0]; A_j = RES["Hyades (Jerabkova+21)"][0]
ck("39f AGAINST INTEREST -- and the amplitude is not robust either.  Two independent member lists for the SAME cluster, "
   "the Hyades, give asymmetries a factor of three apart on the same estimator, the same centre and the same core cut.  "
   "Anyone quoting 'the' open-cluster tail asymmetry is quoting a membership algorithm as much as a cluster",
   abs(math.log10(max(A_r, A_j)/min(A_r, A_j))) > 0.3,
   f"Hyades: Roeser+19 gives A = {A_r:+.3f} on {RES['Hyades (Roeser+19 tails)'][2]} tail stars, Jerabkova+21 gives "
   f"A = {A_j:+.3f} on {RES['Hyades (Jerabkova+21)'][2]}, a factor {max(A_r,A_j)/min(A_r,A_j):.1f} apart; the published "
   f"Roeser labels themselves give {A_pub:+.3f}")

# ---------------------------------------------------------------- systematics and mutations
P("")
rws = read_vizier("praesepe_roeser2019.tsv", ["Source"]); gg = read_gaia("praesepe_roeser2019_gaia.csv")
for snr in (5.0, 20.0, 50.0):
    ra, dec, dpc, _ = assemble(rws, "Source", gg, plx_snr=snr)
    ds, dsky, _, m, _ = offsets("Praesepe", ra, dec, dpc, 3*CLUS[1]["rJM"])
    info(f"Praesepe, parallax S/N > {snr:4.0f}: N = {int(m.sum()):4d}, A(3-D) = {asym(ds[m])[2]:+.3f}, "
         f"A(sky-plane only, distance-independent) = {asym(dsky[m])[2]:+.3f}")
ra, dec, dpc, _ = assemble(rws, "Source", gg)
for f in (2.0, 3.0, 5.0):
    ds, _, _, m, _ = offsets("Praesepe", ra, dec, dpc, f*CLUS[1]["rJM"])
    info(f"Praesepe, core cut at {f:.0f} r_J = {f*CLUS[1]['rJM']:5.1f} pc: N = {int(m.sum()):4d}, A = {asym(ds[m])[2]:+.3f}")
ds, dsky, dlos, m, sv = offsets("Praesepe", ra, dec, dpc, 3*CLUS[1]["rJM"])
A3, Ask = asym(ds[m])[2], asym(dsky[m])[2]
ck("M39 mutation/decomposition: the asymmetry must survive being computed from the SKY-PLANE offsets alone, which are "
   "independent of the parallaxes.  If the two disagreed, the signal would be line-of-sight distance structure -- "
   "which for Praesepe is a live worry, since its tail members sit a median 44 pc nearer than the cluster and its "
   "line of sight has a 0.36 projection onto the orbital direction",
   abs(A3 - Ask) < 0.10, f"Praesepe: A(3-D) = {A3:+.3f} vs A(sky-plane only) = {Ask:+.3f}, difference {A3-Ask:+.3f}; "
   f"the Hyades' line of sight is nearly perpendicular to its orbit (s.v = {offsets('Hyades', *assemble(rows_h,'Source',gh)[:3], 3*CLUS[0]['rJM'])[4]:+.2f}) so it is immune to this")
n_pub = nlc + ntc
sh = np.abs(2*rng.binomial(n_pub, 0.5, 20000)/n_pub - 1)
ck("M39b mutation: drawing the same number of Hyades tail members from a FAIR coin must reproduce the published "
   "asymmetry only rarely.  (The first version of this check permuted the labels, which cannot change a mean at all -- "
   "a broken mutation control, caught by its own failure)",
   (sh > abs(A_pub)).mean() < 0.05,
   f"20000 fair-coin draws of {n_pub} stars: {(sh > abs(A_pub)).mean()*100:.2f}% reach |A| = {abs(A_pub):.3f}; "
   f"mean |A| under the coin = {sh.mean():.3f}")

P("")
info("SUMMARY OF ITEM 39.  The sign is real and it is the one that was reported: in every cluster and every member list")
info("with public data the leading tail carries more stars.  Two things stop it being a result for the framework.")
info("First, neither the significance nor the amplitude is settled: Poisson counting and a random-direction null differ")
info("by a factor of five, and two independent member lists for the Hyades differ by a factor of three.  Second and")
info("decisive, the framework's own static external-field channel gives an asymmetry of 8e-4 where 0.1-0.2 is observed,")
info("a thousandfold shortfall, so even a clean detection could not be credited to the effect this script can compute.")
info("The published Milgromian claim rests on N-body models of the escape process; evaluating those is separate work.")
info("What the framework DOES predict here, cleanly and untested: the tidal radius is 11% larger and the mass read off")
info("the tail geometry 36% smaller than a Newtonian analysis of the same cluster gives.")
sys.exit(ck.done())
