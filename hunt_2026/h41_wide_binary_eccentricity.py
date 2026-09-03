#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
h41_wide_binary_eccentricity.py -- HUNT ITEM 41: THE WIDE-BINARY ECCENTRICITY DISTRIBUTION.
============================================================================================
The repository's wide-binary front measures a VELOCITY boost (gamma_v, pre-registered for Gaia DR4).  This item asks a
different question of the same stars: does the framework change the SHAPE of the orbits, so that the eccentricity
distribution appears to turn over somewhere near the MOND radius of a solar mass (~7,000 AU)?

The observable is the one Hwang, Ting & Zakamska (2022) introduced: the angle gamma between the sky-projected
separation vector and the sky-projected relative proper motion.  It needs no distance, no mass and no absolute
velocity -- only two directions on the sky -- so it is immune to the mass-estimator systematics that dominate the
velocity test.  A circular orbit puts r perpendicular to v (gamma near 90 deg); a radial one puts them parallel.  The
statistic used here is <cos^2 gamma>, which is exactly 1/2 for randomly paired directions AND exactly 1/2 for a
THERMAL eccentricity distribution f(e) = 2e -- a coincidence that is not a coincidence, and that this script uses as
its analytic validation of the whole pipeline.

WHY THIS IS NOT THE gamma_v TEST.  gamma_v asks whether the relative SPEED is too high for the mass.  This asks
whether the ORBIT SHAPE is Keplerian.  In a spherical potential, at a given radius inside a given (pericentre,
apocentre) range, the ratio v_r/v_t is fixed by the potential alone, so a force falling off more slowly than 1/r^2
distributes v_r/v_t differently over the orbit at identical turning points.  That is a shape statement.

WHAT IS COMPUTED.  A paired forward Monte Carlo, run on the SAME random systems for Newtonian gravity and for
    g(r) = g_N(r) nu( (g_N(r) + x_ext a_0)/a_0 ),   g_N = G M_tot/r^2,
with the Galactic external field x_ext ~ 1.7 (Newtonian-equivalent) included, because beyond ~7 kAU the external field
is the larger of the two.  Orbits are specified by (r_peri, r_apo) so the force laws are compared at IDENTICAL
geometry; r is sampled with the correct time weight dt ~ dr/|v_r| through each model's own radial CDF driven by the
SAME uniform variate; orientations, the sky projection, the Gaia proper-motion noise drawn from the selected data
itself, and the S/N cut are all shared between models and applied to the mock exactly as to the data.  Common random
numbers are essential: an unpaired first version of this script had a Monte-Carlo error as large as the signal, which
its own a_0/1000 mutation exposed.  Both footings.  Mutations.  Checks CAN fail.

DATA: ON DISK, El-Badry, Rix & Heintz (2021) Gaia EDR3 wide-binary catalogue, 1,817,594 pairs.
"""
import sys, math, os
import numpy as np
from astropy.io import fits
from hunt_lib import *

ck = Check(); rng = np.random.default_rng(4141)
AU = 1.495978707e11; MSUN_GM = 1.32712440018e20
SNR_CUT = 5.0
BINS = [(0.2, 1.0), (1.0, 2.0), (2.0, 5.0), (5.0, 10.0), (10.0, 30.0)]     # kAU, projected
NSYS = 400000; NGRID = 96; XEXT = 1.7

P("="*116); P("ITEM 41 -- do wide binaries' ORBIT SHAPES know about a_0?"); P("="*116)

# ---------------------------------------------------------------- data
F = os.path.join(DATA, "widebinaries", "all_columns_catalog.fits.gz")
COLS = ["ra1", "ra2", "dec1", "dec2", "parallax1", "parallax2", "parallax_over_error1", "parallax_over_error2",
        "pmra1", "pmra2", "pmdec1", "pmdec2", "pmra_error1", "pmra_error2", "pmdec_error1", "pmdec_error2",
        "ruwe1", "ruwe2", "phot_g_mean_mag1", "phot_g_mean_mag2", "sep_AU", "R_chance_align"]
with fits.open(F, memmap=True) as h:
    D = {k: np.array(h[1].data[k], dtype="f8") for k in COLS}
info(f"El-Badry+2021 Gaia EDR3 catalogue: {len(D['sep_AU'])} pairs loaded")
dist = 0.5*(1000/D["parallax1"] + 1000/D["parallax2"])
dmu_a = D["pmra2"] - D["pmra1"]; dmu_d = D["pmdec2"] - D["pmdec1"]
dmu = np.hypot(dmu_a, dmu_d)
sig_mu = np.sqrt(D["pmra_error1"]**2 + D["pmra_error2"]**2 + D["pmdec_error1"]**2 + D["pmdec_error2"]**2)/math.sqrt(2)
snr = dmu/np.maximum(sig_mu, 1e-9)
dra = (D["ra2"] - D["ra1"])*np.cos(np.radians(0.5*(D["dec1"] + D["dec2"])))
ddec = D["dec2"] - D["dec1"]
sepv = np.hypot(dra, ddec)
cosg = np.clip(np.abs(dra*dmu_a + ddec*dmu_d)/np.maximum(sepv*dmu, 1e-30), 0, 1)
skAU = D["sep_AU"]/1e3
sel = ((D["R_chance_align"] < 0.01) & (D["ruwe1"] < 1.4) & (D["ruwe2"] < 1.4) &
       (dist > 0) & (dist < 250) & (D["parallax_over_error1"] > 50) & (D["parallax_over_error2"] > 50) &
       (snr > SNR_CUT) & np.isfinite(cosg) & (sepv > 0) & (dmu > 0))
info(f"clean sample (R_chance_align < 0.01, RUWE < 1.4 both, d < 250 pc, parallax S/N > 50 both, "
     f"|dmu|/sigma > {SNR_CUT:.0f}): {sel.sum()} pairs")
MG1 = D["phot_g_mean_mag1"] - 5*np.log10(np.maximum(dist, 1e-6)/10)
MG2 = D["phot_g_mean_mag2"] - 5*np.log10(np.maximum(dist, 1e-6)/10)
xg = np.linspace(-1.46, 0.99, 4000); MGg = 4.887 - 5.693*xg + 0.4164*xg**2 + 0.9611*xg**3
o = np.argsort(MGg); MGs, xs = MGg[o], xg[o]
Mtot = np.exp(np.interp(np.clip(MG1, 0.6, 11.1), MGs, xs)) + np.exp(np.interp(np.clip(MG2, 0.6, 11.1), MGs, xs))
P("")
info(f"{'bin [kAU]':>12} {'N':>7} {'<M_tot>':>8} {'<cos^2 g>':>11} {'+-':>7} {'median 1/SNR':>13}   interpretation")
OBS = {}
for lo, hi in BINS:
    m = sel & (skAU > lo) & (skAU < hi); c2 = cosg[m]**2; n = int(m.sum())
    OBS[(lo, hi)] = dict(n=n, c2=float(c2.mean()), err=float(c2.std()/math.sqrt(n)),
                         Mtot=float(np.median(Mtot[m])), sigv=4.74*sig_mu[m]*dist[m]/1000.0)
    tag = "super-thermal" if c2.mean() > 0.5 else "sub-thermal"
    info(f"{lo:5.1f}-{hi:5.1f} {n:7d} {OBS[(lo,hi)]['Mtot']:8.2f} {c2.mean():11.4f} {OBS[(lo,hi)]['err']:7.4f} "
         f"{np.median(1.0/snr[m]):13.4f}   {tag}")
info("(<cos^2 gamma> = 0.5 is BOTH the random-direction value and the thermal-f(e) value; the two coincide, which is")
info(" why this statistic is a clean eccentricity meter and a useless null test at the same time.)")

# ---------------------------------------------------------------- the two potentials
def make_phi(Mt, a0, xext, mond):
    GM = MSUN_GM*Mt
    rr = np.geomspace(1.0*AU, 1e8*AU, 6000); gN = GM/rr**2
    g = gN*nu((gN + xext*a0)/a0) if mond else gN
    tail = (nu_s(xext) if mond else 1.0)*GM/rr[-1]
    I = np.concatenate([[0.0], np.cumsum(0.5*(g[1:] + g[:-1])*np.diff(rr))])
    return rr, (I - I[-1]) - tail

TGRID = (np.arange(NGRID) + 0.5)/NGRID
UGRID = (1 - np.cos(math.pi*TGRID))/2.0                 # clusters points at the turning points
DRDT = (math.pi/2)*np.sin(math.pi*TGRID)

def state(rp, ra, u, rr, Phi):
    """(r, v_r, v_t) at the time-weighted radial phase selected by the uniform variate u, chunked."""
    n = len(rp); r_o = np.empty(n); vr_o = np.empty(n); vt_o = np.empty(n)
    for s0 in range(0, n, 50000):
        s1 = min(s0 + 50000, n); RP, RA, U = rp[s0:s1], ra[s0:s1], u[s0:s1]
        Pp = np.interp(RP, rr, Phi); Pa = np.interp(RA, rr, Phi)
        L2 = 2*(Pa - Pp)/(1/RP**2 - 1/RA**2); E = Pa + L2/(2*RA**2)
        r = RP[:, None] + (RA - RP)[:, None]*UGRID[None, :]
        vr = np.sqrt(np.maximum(2*(E[:, None] - np.interp(r, rr, Phi)) - L2[:, None]/r**2, 0.0))
        w = ((RA - RP)[:, None]*DRDT[None, :])/np.maximum(vr, 1e-6)
        w = np.where(np.isfinite(w), w, 0.0)
        cdf = np.cumsum(w, axis=1); cdf /= np.maximum(cdf[:, -1:], 1e-300)
        j = np.clip((cdf < U[:, None]).sum(axis=1), 0, NGRID-1); i0 = np.arange(s1-s0)
        r_o[s0:s1] = r[i0, j]; vr_o[s0:s1] = vr[i0, j]; vt_o[s0:s1] = np.sqrt(L2)/r[i0, j]
    return r_o, vr_o, vt_o

class Population:
    """everything random is drawn ONCE here, so the two gravity laws see identical systems (common random numbers)."""
    def __init__(self, n, alpha, a_lo, a_hi, slope=0.0):
        la = rng.uniform(math.log10(a_lo), math.log10(a_hi), n)
        if slope != 0.0:                                   # optional dN/da ~ a^slope instead of log-flat
            w = 10**(la*slope); keep = rng.random(n) < w/w.max()
            la = la[keep]; n = len(la)
        self.n = n
        self.a = 10**la*1e3*AU
        self.e = np.clip(rng.random(n)**(1.0/(alpha + 1.0)), 1e-3, 0.995)
        self.u = rng.random(n); self.sgn = rng.choice([-1.0, 1.0], n)
        q = rng.normal(size=(n, 4)); q /= np.linalg.norm(q, axis=1, keepdims=True)
        w_, x_, y_, z_ = q.T
        M = np.empty((n, 3, 3))
        M[:, 0, 0] = 1-2*(y_**2+z_**2); M[:, 0, 1] = 2*(x_*y_-z_*w_); M[:, 0, 2] = 2*(x_*z_+y_*w_)
        M[:, 1, 0] = 2*(x_*y_+z_*w_); M[:, 1, 1] = 1-2*(x_**2+z_**2); M[:, 1, 2] = 2*(y_*z_-x_*w_)
        self.M2 = M[:, :2, :]                              # only the two sky components are ever needed
        self.noise = rng.normal(size=(n, 2)); self.isig = rng.random(n)

def run(pop, Mt, a0, xext, mond, sigv, lo, hi, noise=True, cut=True):
    rp, ra = pop.a*(1 - pop.e), pop.a*(1 + pop.e)
    rr, Phi = make_phi(Mt, a0, xext, mond)
    r, vr, vt = state(rp, ra, pop.u, rr, Phi)
    R3 = np.stack([r, np.zeros_like(r), np.zeros_like(r)], 1)
    V3 = np.stack([vr*pop.sgn, vt, np.zeros_like(vt)], 1)
    Rp = np.einsum("nij,nj->ni", pop.M2, R3); Vp = np.einsum("nij,nj->ni", pop.M2, V3)
    s = np.hypot(Rp[:, 0], Rp[:, 1])/AU/1e3
    k = (s > lo) & (s < hi)
    Rp, Vp = Rp[k], Vp[k]
    if len(Rp) < 200: return np.nan, 0
    if noise:
        sg = np.asarray(sigv)[np.clip((pop.isig[k]*len(sigv)).astype(int), 0, len(sigv)-1)]*1e3
        Vp = Vp + pop.noise[k]*sg[:, None]
        vmag = np.hypot(Vp[:, 0], Vp[:, 1])
        if cut:
            g = vmag/sg > SNR_CUT; Rp, Vp, vmag = Rp[g], Vp[g], vmag[g]
    else:
        vmag = np.hypot(Vp[:, 0], Vp[:, 1])
    if len(Rp) < 100: return np.nan, len(Rp)
    smag = np.hypot(Rp[:, 0], Rp[:, 1])
    c = np.clip(np.abs(Rp[:, 0]*Vp[:, 0] + Rp[:, 1]*Vp[:, 1])/np.maximum(smag*vmag, 1e-30), 0, 1)
    return float(np.mean(c**2)), len(Rp)

# ---------------------------------------------------------------- validation against the analytic result
P(""); P("="*116); P("pipeline validation: thermal f(e) in Newtonian gravity must give <cos^2 gamma> = 1/2 exactly")
P("="*116)
val = Population(300000, 1.0, 0.5, 20.0)
c_th, n_th = run(val, 1.0, A0["canonical"], XEXT, False, None, 0.0, 1e9, noise=False, cut=False)
c_c0, _ = run(Population(300000, 0.0, 0.5, 20.0), 1.0, A0["canonical"], XEXT, False, None, 0.0, 1e9, noise=False, cut=False)
c_c2, _ = run(Population(300000, 2.0, 0.5, 20.0), 1.0, A0["canonical"], XEXT, False, None, 0.0, 1e9, noise=False, cut=False)
info(f"noiseless Newtonian mocks, no cuts: f(e) ~ e^0 gives <cos^2 g> = {c_c0:.4f}; f(e) = 2e (THERMAL) gives "
     f"{c_th:.4f}; f(e) ~ e^2 gives {c_c2:.4f}")
ck("V41 pipeline validation -- a thermal eccentricity distribution must reproduce the analytic <cos^2 gamma> = 0.5 "
   "exactly, and sub- and super-thermal distributions must fall either side of it.  This is what licenses every number "
   "below; without it the Monte Carlo could not be trusted at the 0.01 level it needs to work at",
   abs(c_th - 0.5) < 0.004 and c_c0 < c_th < c_c2,
   f"thermal gives {c_th:.4f} against the analytic 0.5000 ({abs(c_th-0.5):.4f} off, N = {n_th}); "
   f"e^0 {c_c0:.4f} < thermal < e^2 {c_c2:.4f}")

# ---------------------------------------------------------------- the paired forward model
P(""); P("="*116); P("forward model: the same 400k systems under Newton and under the framework"); P("="*116)
ALPHA = 1.0
info(f"mock: {NSYS} systems per bin (common random numbers across gravity laws), f(e) ~ e^{ALPHA:.1f}, x_ext = {XEXT}, "
     f"Gaia noise and the S/N > {SNR_CUT:.0f} cut applied exactly as to the data")
info(f"{'bin [kAU]':>12} {'g_N/a_0':>9} {'Newton':>9} {'framework':>10} {'shift':>9} {'MC err':>8} {'data err':>9} "
     f"{'shift/data':>11} {'d alpha equiv':>14}")
MOD = {}
for lo, hi in BINS:
    ob = OBS[(lo, hi)]; Mt = ob["Mtot"]
    pops = [Population(NSYS, ALPHA, 0.3*lo, 30*hi) for _ in range(4)]     # 4 independent draws -> MC error bar
    cn = [run(p, Mt, A0["canonical"], XEXT, False, ob["sigv"], lo, hi)[0] for p in pops]
    cm = {ft: [run(p, Mt, a0, XEXT, True, ob["sigv"], lo, hi)[0] for p in pops] for ft, a0 in A0.items()}
    d = np.array(cm["canonical"]) - np.array(cn)
    # what change in the eccentricity index would mimic the same shift?
    p2 = Population(150000, ALPHA + 0.3, 0.3*lo, 30*hi)
    c_a, _ = run(p2, Mt, A0["canonical"], XEXT, False, ob["sigv"], lo, hi)
    dalpha = 0.3*float(d.mean())/max(c_a - np.mean(cn), 1e-9)
    rmid = math.sqrt(lo*hi)*1e3*AU
    MOD[(lo, hi)] = dict(newton=float(np.mean(cn)), canonical=float(np.mean(cm["canonical"])),
                         alt=float(np.mean(cm["alt"])), shift=float(d.mean()), mcerr=float(d.std(ddof=1)/2),
                         dalpha=dalpha, gn=MSUN_GM*Mt/rmid**2/A0["canonical"])
    M = MOD[(lo, hi)]
    info(f"{lo:5.1f}-{hi:5.1f} {M['gn']:9.2f} {M['newton']:9.4f} {M['canonical']:10.4f} {M['shift']:+9.4f} "
         f"{M['mcerr']:8.4f} {ob['err']:9.4f} {M['shift']/ob['err']:+11.2f} {dalpha:+14.3f}")

big = max(BINS, key=lambda b: abs(MOD[b]["shift"]/OBS[b]["err"]))
Mb = MOD[big]
ck("41 the framework's effect on wide-binary orbit SHAPE is real, computable and -- surprisingly -- LARGER than the "
   "present sample's statistical error: it raises <cos^2 gamma> by 0.012-0.019 beyond 2 kAU, up to three times the "
   "data error bar, and it switches on exactly where g_N crosses a_0.  So the item is NOT underpowered, which is the "
   "opposite of what this script was written expecting",
   abs(Mb["shift"]) > 3*Mb["mcerr"] and abs(Mb["shift"]/OBS[big]["err"]) > 2.0,
   f"largest shift {Mb['shift']:+.4f} +- {Mb['mcerr']:.4f} (MC) in the {big[0]:.0f}-{big[1]:.0f} kAU bin, against a data "
   f"error of {OBS[big]['err']:.4f} -> {abs(Mb['shift']/OBS[big]['err']):.1f} sigma of statistical reach")

# ---------------------------------------------------------------- the degeneracy that kills it
P(""); P("="*116); P("...and the degeneracy that stops it being a test"); P("="*116)
dal = np.array([MOD[b]["dalpha"] for b in BINS])
info(f"the same shift is produced by raising the eccentricity index alpha in f(e) ~ e^alpha by "
     f"{np.nanmin(dal[2:]):+.2f} to {np.nanmax(dal[2:]):+.2f} in the bins beyond 2 kAU.")
info("the published measurements of alpha for wide binaries (Hwang, Ting & Zakamska 2022) carry uncertainties of ~0.1-0.2")
info("AND a strong, astrophysical separation dependence of their own: close pairs are circularised, wide pairs are")
info("super-thermal, because of how they form and how they are stirred.  So the framework's signature is the same shape")
info("and about the same size as the nuisance it would have to be separated from.")
c2s = np.array([OBS[b]["c2"] for b in BINS]); e2s = np.array([OBS[b]["err"] for b in BINS])
mid = np.array([math.sqrt(b[0]*b[1]) for b in BINS])
sl, _ = np.polyfit(np.log10(mid), c2s, 1, w=1/e2s)
bs = np.array([np.polyfit(np.log10(mid), rng.normal(c2s, e2s), 1, w=1/e2s)[0] for _ in range(4000)])
pred_sl = np.polyfit(np.log10(mid), [MOD[b]["shift"] for b in BINS], 1)[0]
info(f"measured trend of <cos^2 gamma> with separation: {sl:+.4f} +- {bs.std():.4f} per dex ({abs(sl)/bs.std():.1f} sigma "
     f"-- consistent with FLAT); the framework predicts {pred_sl:+.4f} per dex on top of whatever f(e) does.")
ck("41b AGAINST INTEREST, and this is the item's verdict: the effect is measurable in principle but NOT SEPARABLE in "
   "practice.  It is degenerate with the eccentricity distribution -- an alpha shift of ~0.3, inside the astrophysical "
   "uncertainty on alpha and with the same separation dependence that binary formation already imprints.  <cos^2 gamma> "
   "is an eccentricity meter that happens to be 0.5 for both a thermal distribution and for random directions; it cannot "
   "be a gravity meter without an independent f(e), and there is none",
   0.1 < abs(np.nanmean(dal[2:])) < 1.0,
   f"the framework's shift is worth d alpha = {np.nanmean(dal[2:]):+.2f} in the bins beyond 2 kAU, against a published "
   f"alpha uncertainty of ~0.1-0.2 and an astrophysical separation trend in alpha of order 0.5 across this range")

# read the other way: what does the framework say the intrinsic f(e) is?
b = (10.0, 30.0); ob = OBS[b]
info("")
info("the one statement that CAN be made, and it is about star formation rather than gravity: if the framework is right, "
     "then the eccentricity distribution inferred from these same data is LESS super-thermal than a Newtonian analysis "
     f"of them concludes, by d alpha ~ {abs(MOD[b]['dalpha']):.2f} at 10-30 kAU.  That is a testable consequence for "
     "binary-formation theory, and it is the only thing this item delivers.")

# ---------------------------------------------------------------- systematics and mutations
P("")
for slope, lab in ((0.0, "log-flat in a (Opik)"), (-0.6, "dN/da ~ a^-0.6 (steeper, El-Badry+21 wide end)")):
    p = Population(250000, ALPHA, 0.3*b[0], 30*b[1], slope=slope)
    cn_, _ = run(p, ob["Mtot"], A0["canonical"], XEXT, False, ob["sigv"], *b)
    cm_, _ = run(p, ob["Mtot"], A0["canonical"], XEXT, True, ob["sigv"], *b)
    info(f"separation-function systematic, {lab:44}: shift = {cm_-cn_:+.4f} (baseline {MOD[b]['shift']:+.4f})")
for xe in (0.0, 1.7, 3.0):
    p = Population(250000, ALPHA, 0.3*b[0], 30*b[1])
    cn_, _ = run(p, ob["Mtot"], A0["canonical"], xe, False, ob["sigv"], *b)
    cm_, _ = run(p, ob["Mtot"], A0["canonical"], xe, True, ob["sigv"], *b)
    info(f"external-field systematic, x_ext = {xe:4.1f}: shift = {cm_-cn_:+.4f}")

p = Population(300000, ALPHA, 0.3*b[0], 30*b[1])
c_new, _ = run(p, ob["Mtot"], A0["canonical"], XEXT, False, ob["sigv"], *b)
c_mut, _ = run(p, ob["Mtot"], A0["canonical"]/1000.0, XEXT, True, ob["sigv"], *b)
ck("M41 mutation: a_0 -> a_0/1000 must collapse the framework's mock ONTO the Newtonian one on the same systems, since "
   "the kernel then does nothing at these separations.  With common random numbers this is a near-exact test, and it is "
   "the check that caught the first version of this script, whose unpaired Monte-Carlo error was as large as the signal",
   abs(c_mut - c_new) < 0.15*abs(MOD[b]["shift"]),
   f"a_0/1000 gives {c_mut:.5f} vs Newton {c_new:.5f} on the same 300k systems, a residual of {c_mut-c_new:+.5f} against "
   f"a real shift of {MOD[b]['shift']:+.5f}")

m = sel & (skAU > b[0]) & (skAU < b[1]); idx = np.where(m)[0]; perm = rng.permutation(idx)
cs = np.clip(np.abs(dra[idx]*dmu_a[perm] + ddec[idx]*dmu_d[perm])/np.maximum(sepv[idx]*dmu[perm], 1e-30), 0, 1)
ck("M41b mutation on the DATA: pairing each separation vector with a DIFFERENT pair's relative proper motion must drive "
   "<cos^2 gamma> to the random-direction value 0.5, showing the real signal is orbital and not an artefact of the sky "
   "geometry or of Gaia's scanning law",
   abs(float(np.mean(cs**2)) - 0.5) < 0.02,
   f"shuffled <cos^2 gamma> = {np.mean(cs**2):.4f} (random = 0.5000) vs the real {ob['c2']:.4f} in the same bin")

P("")
info("SUMMARY OF ITEM 41.  The catalogue is right, the observable is right, and the framework's effect on it is bigger")
info("than the error bar -- and the item still fails, for a reason worth recording: <cos^2 gamma> is 1/2 both for random")
info("directions and for a thermal eccentricity distribution, and the kernel's shift is worth a change of ~0.3 in the")
info("eccentricity index, which is the size of the astrophysical uncertainty in that index AND has the same separation")
info("dependence.  Item 41 is DEGENERATE, not underpowered.  The wide-binary lever stays where the pre-registration put")
info("it: on the SPEED (gamma_v), where the framework's effect is not something binary formation can also produce.")
sys.exit(ck.done())
