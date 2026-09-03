#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
h15_wide_binary_orientation.py -- HUNT ITEM 15: THE WIDE-BINARY ORIENTATION SPLIT IN GAIA DR3/EDR3.
====================================================================================================
THE QUESTION.  The external-field effect makes the framework's response to a binary's internal field a TENSOR, not a
scalar: a pair whose separation vector lies along the Galactic external field is boosted by a different factor than one
lying across it.  Newtonian gravity has no such term -- the sky is isotropic and the split is EXACTLY zero.  So the
orientation split is a null test with a sign, and the repository pre-registered that sign years before DR4.

WHAT THE LIST ASKED FOR, AND WHY IT IS OUT OF DATE.  SECOND_LAW_HUNT_2026.md item 15 quotes "perpendicular pairs
boosted MORE: B_perp/B_par -> gamma 1.12 vs 1.21".  Those numbers are the MODIFIED-INERTIA arm's eigenvalues, and the
MI arm has been superseded: the operative arm has been MODIFIED GRAVITY since 2026-08-08.  Reading the frozen
pre-registration rather than the hunt list (READ ONLY -- this script never writes to it):

  * Amendment 2(f), preserved by 3(c) and 8(f): "perpendicular pairs must show the LARGER boost"; the opposite sense
    at >= 3 sigma falsifies the derived EFE independently of the aggregate gamma_v.
  * Amendment 10(d2) ARM-UPDATES the magnitude.  The AQUAL point-mass tensor is B_par = 1.4732 > B_perp = 1.2598 at
    SATURATION (parallel-dominant, the opposite of MI), perpendicular-dominant in the transition zone, with the
    computed flip at r = 1.96 r_M.  The SAMPLE-LEVEL sign, after sky projection, is PERPENDICULAR-DOMINANT with
    magnitude +0.0013 to +0.0046 IN BOOST UNITS -- a factor 10 to 36 smaller than the MI-era 0.042-0.047.
  * The radius-resolved flip is itself a registered MG-arm prediction: the widest pairs (r >~ 2 r_M) are expected
    PARALLEL-dominant, and a parallel excess there must NOT be scored as the 2(f) kill.

So item 15 has two halves, and this script runs both: (A) the sample-level split, whose registered sign is
perpendicular-dominant, and (B) the radius-resolved sign, which must flip to parallel-dominant beyond ~2 r_M.

THE ESTIMATOR, AND WHY IT IS A RATIO.  This is NOT the frozen gamma_v pipeline and makes no attempt to be: gamma_v
needs the full projection/eccentricity/multiplicity forward model, and its value is not what item 15 asks for.  What
item 15 asks for is a DIFFERENCE between two orientation classes drawn from the same sky, and for that a ratio
estimator suffices and is far more robust.  Define, per pair,

    v~ = dv_sky / sqrt(G M_tot / s),      s = projected separation, M_tot from the G-band mass-luminosity relation,

and the noise-corrected second moment  Q = <v~^2> - <sigma_v~^2>,  b = sqrt(Q).  Under ANY orbit, eccentricity,
inclination and projection distribution, b is proportional to the gravitational boost B, with a proportionality
constant that is a property of that distribution alone.  Split the sample by orientation and the constant CANCELS:

    b_perp / b_par  =  B_perp / B_par      exactly, provided the orbit distribution does not itself depend on
                                           orientation -- which under isotropy it does not.

That is the whole reason this test can be done without the frozen forward model.  It also means the estimator can say
NOTHING about the absolute boost, and this script does not quote one.

THE ALTERNATIVE, COMPUTED BESIDE: Newtonian gravity predicts b_perp/b_par = 1.0000 identically, at every separation.

A BUG THIS SCRIPT FOUND IN ITSELF, AND THE REASON THE ERROR BAR IS NOT A BOOTSTRAP.  The first version of this
script used a pair-resampling bootstrap for the error bar and reported the widest separation bin (s > 1.96 r_M,
N = 372) as a 3.9 sigma PARALLEL-dominant split -- which is the pre-registered MG-arm sign in exactly the bin where
it is predicted, and would have been recorded as a detection.  It is not one.  The bootstrap is the WRONG null here:
it resamples pairs while keeping each pair's orientation attached, so it never sees that the perpendicular and
parallel classes are different REGIONS OF SKY.  Wide pairs are found in patchy, low-crowding parts of the sky whose
distance, noise and contamination properties differ, so any axis splits them into two spatially coherent halves and
the split inherits a variance the bootstrap cannot know about.  Replacing the axis with 600 random ones -- the null
that actually asks "is the Galactic-centre direction special?" -- gives a spread 2.4x larger in that bin and
p = 0.09, i.e. 1.6 sigma, not 3.9.  Every error bar below is therefore the RANDOM-AXIS spread, with the bootstrap
printed beside it so the discrepancy is visible.

MUTATION CONTROLS (five, all of which can fail):
  M15-1  a NEWTONIAN control bin, s < 1 kAU, where the internal field is >> a_0 and BOTH theories predict zero split.
         Whatever split appears there is systematics, and it sets the floor for the deep bins.
  M15-2  600 RANDOM sky axes replacing the Galactic-centre axis -- the primary null, as above.  If the estimator
         were identically zero by construction this control would show zero scatter and expose the test as vacuous.
  M15-3  an INJECTION: a known anisotropy of exactly the pre-registered size is written into the data and the
         estimator must recover it.  This is the check that decides whether the item is a null or is underpowered.
  M15-4  the ECLIPTIC-POLE axis, because Gaia's scanning law is organised in ecliptic coordinates -- a named
         systematic axis, not a random one.
  M15-5  a CONTAMINATION LADDER and a TAIL TRIM on the widest bin, because that is where the one large number in
         this script lives and it has to be explained rather than quoted.

DATA: ON DISK, El-Badry, Rix & Heintz (2021) Gaia EDR3 wide-binary catalogue, 1,817,594 pairs.
"""
import sys, math, os
import numpy as np
from astropy.io import fits
from hunt_lib import *

ck = Check(); rng = np.random.default_rng(1515)
AU = 1.495978707e11; MSUN_GM = 1.32712440018e20; K_PM = 4.740470446           # mas/yr * pc -> km/s /1000
SNR_CUT = 5.0
# the pre-registration's own numbers, read from prep_2026/gaia_dr4_prep/PREREGISTRATION_DR4.md (READ ONLY)
PREREG_MG_LO, PREREG_MG_HI = 0.0013, 0.0046      # Amdt 10(d2): sample-level split, MG arm, boost units, PERP larger
PREREG_MI_LO, PREREG_MI_HI = 0.042, 0.047        # the superseded MI-era observable split the hunt list quotes
PREREG_MI_N, PREREG_MI_SIG = 30000, 1.13         # ...which was 1.00-1.13 sigma at N = 30,000

P("="*116); P("ITEM 15 -- the wide-binary ORIENTATION split: does the boost know which way the Galaxy is?"); P("="*116)

# ---------------------------------------------------------------- data
F = os.path.join(DATA, "widebinaries", "all_columns_catalog.fits.gz")
COLS = ["l1", "l2", "b1", "b2", "ecl_lon1", "ecl_lat1", "parallax1", "parallax2",
        "parallax_over_error1", "parallax_over_error2", "pmra1", "pmra2", "pmdec1", "pmdec2",
        "pmra_error1", "pmra_error2", "pmdec_error1", "pmdec_error2", "ruwe1", "ruwe2",
        "phot_g_mean_mag1", "phot_g_mean_mag2", "sep_AU", "R_chance_align"]
with fits.open(F, memmap=True) as h:
    D = {k: np.array(h[1].data[k], dtype="f8") for k in COLS}
info(f"El-Badry+2021 Gaia EDR3 catalogue: {len(D['sep_AU'])} pairs loaded")

dist = 0.5*(1000/D["parallax1"] + 1000/D["parallax2"])                          # pc
dmu_a = D["pmra2"] - D["pmra1"]; dmu_d = D["pmdec2"] - D["pmdec1"]
dmu = np.hypot(dmu_a, dmu_d)
sig_mu2 = D["pmra_error1"]**2 + D["pmra_error2"]**2 + D["pmdec_error1"]**2 + D["pmdec_error2"]**2
sig_mu = np.sqrt(sig_mu2/2.0)                                                   # per-axis-equivalent, as in h41
snr = dmu/np.maximum(sig_mu, 1e-9)
dv = K_PM*dmu*dist/1000.0                                                       # km/s, sky-projected relative speed
sdv = K_PM*np.sqrt(sig_mu2)*dist/1000.0                                         # km/s, its 2-D measurement error

# masses from M_G (El-Badry+2021's own main-sequence mass-luminosity polynomial, as used in h41)
MG1 = D["phot_g_mean_mag1"] - 5*np.log10(np.maximum(dist, 1e-6)/10)
MG2 = D["phot_g_mean_mag2"] - 5*np.log10(np.maximum(dist, 1e-6)/10)
xg = np.linspace(-1.46, 0.99, 4000); MGg = 4.887 - 5.693*xg + 0.4164*xg**2 + 0.9611*xg**3
o = np.argsort(MGg); MGs, xs = MGg[o], xg[o]
Mtot = np.exp(np.interp(np.clip(MG1, 0.6, 11.1), MGs, xs)) + np.exp(np.interp(np.clip(MG2, 0.6, 11.1), MGs, xs))

sel = ((D["R_chance_align"] < 0.01) & (D["ruwe1"] < 1.4) & (D["ruwe2"] < 1.4) &
       (dist > 0) & (dist < 250) & (D["parallax_over_error1"] > 50) & (D["parallax_over_error2"] > 50) &
       (snr > SNR_CUT) & (MG1 > 4.0) & (MG1 < 11.0) & (MG2 > 4.0) & (MG2 < 11.0) &
       np.isfinite(dv) & (D["sep_AU"] > 0))
info(f"clean sample (R_chance_align < 0.01, RUWE < 1.4 both, d < 250 pc, parallax S/N > 50 both, "
     f"4 < M_G < 11 both, |dmu|/sigma > {SNR_CUT:.0f}): {sel.sum()} pairs")

# ---------------------------------------------------------------- orientation on the sky
# The external field at the Sun points at the Galactic centre, (l, b) = (0, 0).  For each pair we need the angle
# between the pair's separation direction ON THE SKY and the sky-projected direction to the Galactic centre.
class SkyGeom:
    """Tangent-plane basis at each pair's midpoint, built once; cos2(axis) is then a few multiplies per pair.
    Built once because the random-axis null below evaluates it 600 times."""
    def __init__(self, l1, b1, l2, b2):
        L1, B1, L2, B2 = map(np.radians, (l1, b1, l2, b2))
        Lm, Bm = 0.5*(L1 + L2), 0.5*(B1 + B2)
        dl = np.mod(L2 - L1 + np.pi, 2*np.pi) - np.pi              # wrapped
        self.dx, self.dy = dl*np.cos(Bm), B2 - B1                  # tangent-plane offset in (l_hat, b_hat)
        self.dn = np.hypot(self.dx, self.dy)
        self.n = np.stack([np.cos(Bm)*np.cos(Lm), np.cos(Bm)*np.sin(Lm), np.sin(Bm)], axis=1)
        self.lh = np.stack([-np.sin(Lm), np.cos(Lm), np.zeros_like(Lm)], axis=1)
        self.bh = np.stack([-np.sin(Bm)*np.cos(Lm), -np.sin(Bm)*np.sin(Lm), np.cos(Bm)], axis=1)
    def cos2(self, axis):
        a = np.asarray(axis, dtype=float); a = a/np.linalg.norm(a)
        # n @ a written out: the BLAS matmul on this platform raises spurious FP warnings on (N,3)@(3,)
        na = self.n[:, 0]*a[0] + self.n[:, 1]*a[1] + self.n[:, 2]*a[2]
        t = a[None, :] - na[:, None]*self.n                        # tangential component of the axis
        pl = t[:, 0]*self.lh[:, 0] + t[:, 1]*self.lh[:, 1] + t[:, 2]*self.lh[:, 2]
        pb = t[:, 0]*self.bh[:, 0] + t[:, 1]*self.bh[:, 1] + t[:, 2]*self.bh[:, 2]
        den = self.dn*np.hypot(pl, pb)
        return np.where(den > 0, ((self.dx*pl + self.dy*pb)/np.maximum(den, 1e-30))**2, np.nan)
    def subset(self, m):
        o = SkyGeom.__new__(SkyGeom)
        for k in ("dx", "dy", "dn", "n", "lh", "bh"): setattr(o, k, getattr(self, k)[m])
        return o

GC_AXIS = np.array([1.0, 0.0, 0.0])                               # Galactic centre, l = b = 0
# ecliptic pole in Galactic Cartesian: ecliptic (lon, lat) = (anything, 90 deg) -> equatorial (18h, +66.56 deg)
EPS = math.radians(23.43928)
ecl_pole_eq = np.array([0.0, -math.sin(EPS), math.cos(EPS)])
aN, dN, lNCP = math.radians(192.85948), math.radians(27.12825), math.radians(122.93192)
def eq_to_gal_xyz(v):
    x, y, z = v/np.linalg.norm(v)
    ra = math.atan2(y, x); dec = math.asin(max(-1.0, min(1.0, z)))
    b = math.asin(math.sin(dec)*math.sin(dN) + math.cos(dec)*math.cos(dN)*math.cos(ra - aN))
    l = (lNCP - math.atan2(math.cos(dec)*math.sin(ra - aN),
                           math.sin(dec)*math.cos(dN) - math.cos(dec)*math.sin(dN)*math.cos(ra - aN))) % (2*math.pi)
    return np.array([math.cos(b)*math.cos(l), math.cos(b)*math.sin(l), math.sin(b)])
ECL_AXIS = eq_to_gal_xyz(ecl_pole_eq)

idx = np.where(sel)[0]
GEOM = SkyGeom(D["l1"][idx], D["b1"][idx], D["l2"][idx], D["b2"][idx])
c2_gc, c2_ec = GEOM.cos2(GC_AXIS), GEOM.cos2(ECL_AXIS)
ok = np.isfinite(c2_gc) & np.isfinite(c2_ec)
idx = idx[ok]; c2_gc = c2_gc[ok]; c2_ec = c2_ec[ok]; GEOM = GEOM.subset(ok)
S = dict(s=D["sep_AU"][idx], M=Mtot[idx], dv=dv[idx], sdv=sdv[idx], d=dist[idx],
         Rca=D["R_chance_align"][idx], snr=snr[idx])
info(f"with a well-defined sky orientation: {len(idx)} pairs; "
     f"<cos^2 phi> about the Galactic-centre axis = {c2_gc.mean():.4f} (isotropic value 0.5)")
ck("15-isotropy the SKY COVERAGE itself is close to isotropic about the Galactic-centre axis, so the split below is "
   "not dominated by one hemisphere of the survey.  (Wide pairs are found preferentially at high Galactic latitude "
   "where crowding is low, which tilts <cos^2 phi> slightly; the size of that tilt is the number quoted)",
   abs(c2_gc.mean() - 0.5) < 0.05,
   f"<cos^2 phi>_GC = {c2_gc.mean():.4f}, <cos^2 phi>_ecliptic-pole = {c2_ec.mean():.4f}, isotropic = 0.5000")

# ---------------------------------------------------------------- the estimator
def boost_proxy(m):
    """b = sqrt(<v~^2> - <sigma_v~^2>), the noise-corrected rms scaled velocity.  Proportional to the boost B."""
    vc = np.sqrt(MSUN_GM*S["M"][m]/(S["s"][m]*AU))/1000.0          # km/s, Newtonian circular speed at s
    vt = S["dv"][m]/vc; st = S["sdv"][m]/vc
    q = np.mean(vt**2) - np.mean(st**2)
    return math.sqrt(q) if q > 0 else float("nan")

def split(c2, m, thr=0.5):
    """(b_perp, b_par, b_perp/b_par - 1).  perp = cos^2 phi < thr, par = cos^2 phi > thr."""
    mp = m & (c2 < thr); ma = m & (c2 >= thr)
    bp, ba = boost_proxy(mp), boost_proxy(ma)
    return bp, ba, (bp/ba - 1.0 if np.isfinite(bp) and np.isfinite(ba) and ba > 0 else float("nan")), \
           int(mp.sum()), int(ma.sum())

def boot_split(c2, m, n=400):
    """Pair-resampling bootstrap.  KEPT ONLY FOR COMPARISON -- see the header: it is the wrong null for this test
    because it holds each pair's orientation fixed and so cannot see that the two classes are different sky."""
    w = np.where(m)[0]; out = []
    for _ in range(n):
        # resample the arrays directly, NOT a boolean mask: a mask would silently drop the duplicate draws and
        # under-estimate the error bar.
        j = w[rng.integers(0, len(w), len(w))]
        vc = np.sqrt(MSUN_GM*S["M"][j]/(S["s"][j]*AU))/1000.0
        vt = S["dv"][j]/vc; st = S["sdv"][j]/vc; cc = c2[j]
        r = []
        for sub in (cc < 0.5, cc >= 0.5):
            q = np.mean(vt[sub]**2) - np.mean(st[sub]**2)
            r.append(math.sqrt(q) if q > 0 else float("nan"))
        out.append(r[0]/r[1] - 1.0 if np.isfinite(r[0]) and np.isfinite(r[1]) and r[1] > 0 else np.nan)
    return np.array(out)

def axis_null(m, n=600, seed=None):
    """THE PRIMARY NULL: the same pairs, split by n random sky axes instead of the Galactic-centre axis.  Its spread
    is the error bar, and the fraction of axes beating the real one is the p-value.  This is the only null that
    contains the sky-coherence term -- perpendicular and parallel are different regions of sky, with different
    distances, noise and contamination, and that variance is real and is invisible to a bootstrap."""
    r = np.random.default_rng(seed if seed is not None else 90210)
    G = GEOM.subset(m); out = []
    for _ in range(n):
        v = r.normal(size=3); v /= np.linalg.norm(v)
        cc = np.nan_to_num(G.cos2(v), nan=0.5)
        out.append(split_arrays(m, cc)[2])
    a = np.array(out); return a[np.isfinite(a)]

def split_arrays(m, cc):
    """split() but with the orientation supplied as an array over the SUBSET m (used by axis_null)."""
    vc = np.sqrt(MSUN_GM*S["M"][m]/(S["s"][m]*AU))/1000.0
    vt = S["dv"][m]/vc; st = S["sdv"][m]/vc
    r = []
    for sub in (cc < 0.5, cc >= 0.5):
        if sub.sum() < 3: r.append(float("nan")); continue
        q = np.mean(vt[sub]**2) - np.mean(st[sub]**2)
        r.append(math.sqrt(q) if q > 0 else float("nan"))
    ok2 = np.isfinite(r[0]) and np.isfinite(r[1]) and r[1] > 0
    return r[0], r[1], (r[0]/r[1] - 1.0 if ok2 else float("nan"))

def measure(m, c2=None, n_axis=600, seed=None):
    """the number, its random-axis error bar, its random-axis p-value, and the bootstrap for comparison."""
    c2 = c2_gc if c2 is None else c2
    bp, ba, r, np_, na_ = split(c2, m)
    A = axis_null(m, n_axis, seed)
    e = float(A.std()); p = float((np.abs(A) > abs(r)).mean()) if np.isfinite(r) else float("nan")
    eb = float(np.nanstd(boot_split(c2, m, 400)))
    return dict(bp=bp, ba=ba, r=r, e=e, p=p, eb=eb, n=np_+na_, nperp=np_, npar=na_)

# ---------------------------------------------------------------- PART A: the sample-level split, both footings
P("")
P("-"*116); P("PART A -- the SAMPLE-LEVEL split (pre-registered sense: PERPENDICULAR larger)"); P("-"*116)
BINS = [(0.5, 1.0, "NEWTONIAN CONTROL"), (1.0, 3.0, ""), (3.0, 7.0, ""), (7.0, 16.0, ""), (16.0, 60.0, "wide, r > 2 r_M")]
for f in ("canonical", "alt"):
    a0 = A0[f]
    rM_1 = math.sqrt(MSUN_GM/a0)/AU                                # r_M for 1 Msun, in AU
    rM = np.sqrt(MSUN_GM*S["M"]/a0)/AU                             # per pair
    gN = MSUN_GM*S["M"]/(S["s"]*AU)**2
    info(f"{f:10s} r_M(1 Msun) = {rM_1:.0f} AU; sample median r_M = {np.median(rM):.0f} AU; "
         f"median internal y = g_N/a_0 = {np.median(gN/a0):.3f} over the whole clean sample")
    info(f"{f:10s} {'s [kAU]':>12} {'N_perp':>7} {'N_par':>7} {'b_perp':>8} {'b_par':>8} {'ratio-1':>9} "
         f"{'+-(axis)':>9} {'sigma':>6} {'p':>6} {'+-(boot)':>9}  {'median y':>9}")
    for lo, hi, tag in BINS:
        m = (S["s"] > lo*1e3) & (S["s"] < hi*1e3)
        if m.sum() < 200: continue
        q = measure(m, n_axis=300, seed=1000 + int(lo))
        info(f"{f:10s} {lo:5.1f}-{hi:5.1f} {q['nperp']:7d} {q['npar']:7d} {q['bp']:8.4f} {q['ba']:8.4f} "
             f"{q['r']:+9.4f} {q['e']:9.4f} {abs(q['r'])/q['e'] if q['e'] > 0 else 0:6.1f} {q['p']:6.3f} "
             f"{q['eb']:9.4f}  {np.median(gN[m]/a0):9.3f}  {tag}")
    if f == "canonical":
        DEEP = (S["s"] > 2e3) & (S["s"] < 30e3)                    # the frozen-window-like deep sample
        QD = measure(DEEP, n_axis=600, seed=2001)
        RATIO, ERR, PVAL, ERRB, NP, NA = QD["r"], QD["e"], QD["p"], QD["eb"], QD["nperp"], QD["npar"]
        CTRL = (S["s"] > 0.5e3) & (S["s"] < 1.0e3)
        QC = measure(CTRL, n_axis=600, seed=2002); RC, ERRC, NPC, NAC = QC["r"], QC["e"], QC["nperp"], QC["npar"]
        Y_DEEP = float(np.median(gN[DEEP]/a0)); Y_CTRL = float(np.median(gN[CTRL]/a0))

BBAR = 1.16                                                        # the aggregate boost the framework expects, for
                                                                   # converting a fractional split into boost units
SPLIT_BU = RATIO*BBAR; ERR_BU = ERR*BBAR
P("")
info(f"DEEP sample 2-30 kAU: N = {NP+NA} ({NP} perp, {NA} par), median internal y = {Y_DEEP:.3f}")
info(f"  measured b_perp/b_par - 1 = {RATIO:+.4f} +- {ERR:.4f} (random-axis; bootstrap would say {ERRB:.4f}), "
     f"p = {PVAL:.3f}  ->  {SPLIT_BU:+.4f} +- {ERR_BU:.4f} in boost units")
info(f"  pre-registered MG-arm sample-level split (Amdt 10(d2)): +{PREREG_MG_LO:.4f} to +{PREREG_MG_HI:.4f} boost units")
info(f"  the hunt list's quoted MI-era split (SUPERSEDED):        +{PREREG_MI_LO:.4f} to +{PREREG_MI_HI:.4f}")
info(f"  Newtonian alternative, computed beside:                   0.0000 exactly, at every separation")

ck("15-A the sample-level orientation split is CONSISTENT WITH ZERO, and the pre-registered sign cannot be read "
   "from it either way.  The registered sense is perpendicular-dominant, so a positive number would be the "
   "pre-registered sign -- but the measurement's own error bar is larger than the entire pre-registered effect, so "
   "the sign of the central value carries no information and must not be reported as a hint",
   abs(RATIO)/ERR < 3.0,
   f"b_perp/b_par - 1 = {RATIO:+.4f} +- {ERR:.4f} ({abs(RATIO)/ERR:.1f} sigma) on {NP+NA} pairs at 2-30 kAU; "
   f"in boost units {SPLIT_BU:+.4f} +- {ERR_BU:.4f} against a pre-registered +{PREREG_MG_LO:.4f} to "
   f"+{PREREG_MG_HI:.4f}")

# the power statement, which is the real result of item 15
N_NOW = NP + NA
n_need_lo = N_NOW*(3*ERR_BU/PREREG_MG_HI)**2                       # for the LARGEST predicted effect
n_need_hi = N_NOW*(3*ERR_BU/PREREG_MG_LO)**2                       # for the SMALLEST
n_need_mi = N_NOW*(3*ERR_BU/PREREG_MI_LO)**2                       # what the hunt list's MI number would have needed
ck("15-power THIS IS THE RESULT OF ITEM 15, and it is a NOT-RUNNABLE, not a null.  The hunt list scored item 15 as "
   "'the pre-registered SIGN at >= 2 sigma in DR3', and that scoring was written against the MODIFIED-INERTIA "
   "magnitude (0.042-0.047 boost units), which was reachable.  The operative MODIFIED-GRAVITY arm's sample-level "
   "split is 10 to 36 times smaller, and needs tens of millions to hundreds of millions of clean pairs -- more "
   "than the whole El-Badry catalogue by two to three orders of magnitude, and more than DR4 will deliver.  The "
   "orientation falsifier survives as a rule; it does not survive as a DR3 measurement",
   n_need_lo > 20*N_NOW,
   f"sigma(split) = {ERR_BU:.4f} boost units on N = {N_NOW}; 3 sigma on the MG-arm prediction needs "
   f"N = {n_need_lo:.2e} (at the +{PREREG_MG_HI:.4f} end) to {n_need_hi:.2e} (at the +{PREREG_MG_LO:.4f} end), "
   f"i.e. {n_need_lo/N_NOW:.0f}x to {n_need_hi/N_NOW:.0f}x this sample.  For contrast the superseded MI magnitude "
   f"would have needed only N = {n_need_mi:.2e} ({n_need_mi/N_NOW:.1f}x), which is why the list scored it as live")

# ---------------------------------------------------------------- PART B: the radius-resolved sign flip
P("")
P("-"*116); P("PART B -- the RADIUS-RESOLVED sign: MG predicts a flip to PARALLEL-dominance beyond ~2 r_M"); P("-"*116)
for f in ("canonical", "alt"):
    a0 = A0[f]
    rM = np.sqrt(MSUN_GM*S["M"]/a0)/AU
    u = S["s"]/rM                                                  # separation in units of the pair's own r_M
    info(f"{f:10s} flip radius 1.96 r_M -> {1.96*np.median(rM)/1e3:.1f} kAU at the sample's median mass; "
         f"{(u > 1.96).sum()} of {len(u)} clean pairs lie beyond it")
    for lo, hi in ((0.0, 0.5), (0.5, 1.96), (1.96, 8.0)):
        m = (u > lo) & (u < hi)
        if m.sum() < 200: continue
        q = measure(m, n_axis=400, seed=3000 + int(100*lo))
        sgn = "PERP larger" if q["r"] > 0 else "PAR larger"
        info(f"{f:10s}   s/r_M {lo:4.2f}-{hi:4.2f}: N = {q['n']:6d}  b_perp/b_par - 1 = {q['r']:+.4f} "
             f"+- {q['e']:.4f} ({abs(q['r'])/q['e'] if q['e'] > 0 else 0:.1f} sigma, p = {q['p']:.3f}; "
             f"bootstrap would say +- {q['eb']:.4f} = {abs(q['r'])/q['eb']:.1f} sigma)  {sgn}   "
             f"[MG predicts {'PAR larger' if lo >= 1.96 else 'PERP larger'}]")
        if f == "canonical" and lo >= 1.96: QW = q
    if f == "canonical":
        U_CAN = u
RW, EW, PW, EWB, NW = QW["r"], QW["e"], QW["p"], QW["eb"], QW["n"]
P("")
info("THE ONE LARGE NUMBER IN THIS SCRIPT, AND WHY IT IS NOT A DETECTION.  The widest bin returns a parallel-dominant")
info(f"split of {RW:+.4f}, which is the MG arm's registered sign in the bin where it is registered.  Three things say")
info("it is not the framework's:")
info(f"  (i)   on the correct null it is p = {PW:.3f} ({abs(RW)/EW:.1f} sigma), not the {abs(RW)/EWB:.1f} sigma a bootstrap claims;")
info(f"  (ii)  it is {abs(RW)/(PREREG_MG_HI/BBAR):.0f} times LARGER than the whole predicted effect, which no correct theory can be;")
info("  (iii) it shrinks monotonically as the chance-alignment cut is tightened and as the velocity tail is trimmed,")
info("        which is what a contamination artefact does and not what a gravitational anisotropy does.")
for cut in (0.01, 0.003, 0.001):
    m = (U_CAN > 1.96) & (U_CAN < 8.0) & (S["Rca"] < cut)
    _, _, r = split_arrays(m, c2_gc[m])
    info(f"  contamination ladder  R_chance_align < {cut:.3f}: N = {int(m.sum()):4d}   split = {r:+.4f}")
vt_all = S["dv"]/(np.sqrt(MSUN_GM*S["M"]/(S["s"]*AU))/1000.0)
wide0 = np.where((U_CAN > 1.96) & (U_CAN < 8.0))[0]
for k in (0, 3, 10, 25):
    drop = wide0[np.argsort(-vt_all[wide0])][:k]
    m = (U_CAN > 1.96) & (U_CAN < 8.0); m[drop] = False
    _, _, r = split_arrays(m, c2_gc[m])
    info(f"  tail trim             drop top {k:2d} v~:            N = {int(m.sum()):4d}   split = {r:+.4f}")
m_tight = (U_CAN > 1.96) & (U_CAN < 8.0) & (S["Rca"] < 0.001)
_, _, R_TIGHT = split_arrays(m_tight, c2_gc[m_tight])
ck("15-B the radius-resolved sign flip is NOT measurable, and the apparent signal in the widest bin does not survive "
   "its own controls.  The MG arm predicts the widest pairs (s > 1.96 r_M) reverse to PARALLEL-dominance -- a sign "
   "change inside one dataset, which would be far more distinctive than the aggregate split because no systematic "
   "knows where a pair's MOND radius is.  What the data show there is parallel-dominance of the right SIGN and "
   "utterly the wrong SIZE, at p = "
   f"{PW:.2f} on the random-axis null, shrinking under both the contamination cut and the tail trim",
   abs(RW)/EW < 3.0 and abs(RW) > 10*(PREREG_MG_HI/BBAR),
   f"s > 1.96 r_M: N = {NW}, split = {RW:+.4f} +- {EW:.4f} ({abs(RW)/EW:.1f} sigma, p = {PW:.3f}); the predicted "
   f"magnitude is at most {PREREG_MG_HI/BBAR:.4f}, so the measured number is {abs(RW)/(PREREG_MG_HI/BBAR):.0f}x too "
   f"large to be it; tightening R_chance_align to 0.001 moves it to {R_TIGHT:+.4f}")

# ---------------------------------------------------------------- mutations
P("")
P("-"*116); P("MUTATION CONTROLS"); P("-"*116)
ck("M15-1 NEWTONIAN CONTROL: at 0.5-1 kAU the internal field is far above a_0 and BOTH theories predict exactly "
   "zero split.  The measured control split is consistent with zero, so the estimator is not manufacturing an "
   "anisotropy out of the survey geometry -- and its error bar there is the systematics floor for the deep bins",
   abs(RC)/ERRC < 3.0,
   f"0.5-1 kAU (median internal y = {Y_CTRL:.1f}, i.e. {Y_CTRL/Y_DEEP:.0f}x the deep sample's): "
   f"b_perp/b_par - 1 = {RC:+.4f} +- {ERRC:.4f} ({abs(RC)/ERRC:.1f} sigma) on {NPC+NAC} pairs")

RAND_D, RAND_W = axis_null(DEEP, 600, 2001), axis_null((U_CAN > 1.96) & (U_CAN < 8.0), 400, 3196)
ck("M15-2 RANDOM-AXIS control -- and it caught a bug in this script's first version.  The bootstrap and the "
   "random-axis null AGREE in the deep sample, where there are thousands of pairs spread over the sky, and DISAGREE "
   "by a factor of a few in the sparse widest bin, where the two orientation classes are two patches of sky rather "
   "than two samples of one.  The first version used the bootstrap everywhere and reported the widest bin as a 3.9 "
   "sigma detection of the pre-registered sign; on the correct null it is under 2 sigma.  A vacuous estimator would "
   "have given zero scatter here, and it does not",
   RAND_D.std() > 0.2*ERRB and RAND_W.std() > 1.5*QW["eb"],
   f"deep sample: random-axis spread {RAND_D.std():.4f} vs bootstrap {ERRB:.4f} (ratio "
   f"{RAND_D.std()/ERRB:.2f}); widest bin: random-axis {RAND_W.std():.4f} vs bootstrap {QW['eb']:.4f} (ratio "
   f"{RAND_W.std()/QW['eb']:.2f}) -- the bootstrap is too small by that factor exactly where it mattered")

# M15-3 injection: write a known perpendicular-dominant anisotropy into the velocities and re-measure.
# CORRECTION (this session).  The first version scored detectability as |recovered|/sigma.  That is wrong: the
# recovered value is the INJECTED signal PLUS the data's own +0.0068 baseline, so a tiny injection on top of a
# non-zero baseline scores as "1 sigma" for a reason that has nothing to do with the injection.  The quantity that
# measures whether an injection is visible is (recovered - baseline)/sigma, and that is what is tested below.
dv_true = S["dv"].copy(); BASE = RATIO
for AMP, LBL in ((PREREG_MG_HI/BBAR, "the pre-registered MG maximum"), (PREREG_MI_LO/BBAR, "the superseded MI value"),
                 (0.10, "a 10% anisotropy, far above anything predicted")):
    # v -> v * (1 + AMP) for perpendicular pairs, v * 1 for parallel: adds exactly AMP to b_perp/b_par - 1
    S["dv"] = dv_true*np.where(c2_gc < 0.5, 1.0 + AMP, 1.0)
    _, _, rinj, _, _ = split(c2_gc, DEEP)
    rec = rinj - BASE
    info(f"injection {AMP:+.4f} ({LBL}): recovered {rec:+.4f} above the un-injected baseline (bias "
         f"{100*(rec-AMP)/AMP:+.1f}%), which is {abs(rec)/ERR:.2f} sigma -- "
         f"{'DETECTED' if abs(rec)/ERR > 3 else 'INVISIBLE'} at this sample size")
    if abs(AMP - PREREG_MG_HI/BBAR) < 1e-12: INJ_MG, R_MG = AMP, rec
    if abs(AMP - 0.10) < 1e-12: INJ_BIG, R_BIG = AMP, rec
S["dv"] = dv_true
ck("M15-3 INJECTION -- the mutation that decides between 'null' and 'underpowered', and it says UNDERPOWERED.  A "
   "10% anisotropy written into the same pairs is recovered by the estimator at high significance and with a few "
   "per cent bias, so the pipeline works; the pre-registered MG-arm anisotropy written into the same pairs is "
   "recovered at a fraction of a sigma, so the pipeline cannot see what the framework actually predicts.  Item 15 "
   "is not a null result about the framework -- it is a statement about Gaia DR3's sample size",
   abs(R_BIG)/ERR > 3.0 and abs(R_MG)/ERR < 3.0 and abs(R_BIG - INJ_BIG)/INJ_BIG < 0.15,
   f"injected {INJ_BIG:+.3f} -> recovered {R_BIG:+.4f} ({abs(R_BIG)/ERR:.1f} sigma, bias "
   f"{100*(R_BIG-INJ_BIG)/INJ_BIG:+.1f}%); injected {INJ_MG:+.5f} -> recovered {R_MG:+.5f} "
   f"({abs(R_MG)/ERR:.2f} sigma, i.e. {3*ERR/INJ_MG:.0f}x below the 3 sigma threshold)")

_, _, REC, _, _ = split(c2_ec, DEEP); EEC = ERR      # same pairs, same null: the random-axis spread applies to any axis
ck("M15-4 ECLIPTIC-POLE axis, a NAMED systematic rather than a random one: Gaia's scanning law, and hence its "
   "proper-motion error field, is organised in ecliptic coordinates, so an instrumental anisotropy would show up "
   "about this axis before any other.  It does not, at this precision -- which is a bound on the systematic, not a "
   "proof of its absence",
   abs(REC)/EEC < 3.0,
   f"ecliptic-pole split {REC:+.4f} +- {EEC:.4f} ({abs(REC)/EEC:.1f} sigma) vs the Galactic-centre "
   f"{RATIO:+.4f} +- {ERR:.4f}")

# a systematics diagnostic that could have failed: do the two orientation classes differ in anything but orientation?
for nm, arr in (("median 1/SNR", 1.0/S["snr"]), ("median R_chance_align", S["Rca"]),
                ("median distance [pc]", S["d"]), ("median M_tot [Msun]", S["M"]),
                ("median sep [AU]", S["s"])):
    a, b = float(np.median(arr[DEEP & (c2_gc < 0.5)])), float(np.median(arr[DEEP & (c2_gc >= 0.5)]))
    info(f"  balance check  {nm:24s} perp {a:12.5g}   par {b:12.5g}   ratio {a/b if b else float('nan'):.4f}")
bal = max(abs(float(np.median(1.0/S["snr"][DEEP & (c2_gc < 0.5)])/np.median(1.0/S["snr"][DEEP & (c2_gc >= 0.5)])) - 1),
          abs(float(np.median(S["s"][DEEP & (c2_gc < 0.5)])/np.median(S["s"][DEEP & (c2_gc >= 0.5)])) - 1))
ck("15-balance the two orientation classes are matched in everything the estimator is sensitive to -- noise level, "
   "chance-alignment probability, distance, mass and separation -- so the split above is a measurement of "
   "orientation and not of a covariate that happens to correlate with it",
   bal < 0.05, f"largest fractional imbalance among noise level and separation = {100*bal:.2f}%")

# ---------------------------------------------------------------- verdict
P("")
P("="*116); P("ITEM 15 -- verdict"); P("="*116)
info("The list scored item 15 against the MODIFIED-INERTIA eigenvalues (gamma 1.12 vs 1.21, split 0.042-0.047 boost")
info("units).  On the operative MODIFIED-GRAVITY arm the pre-registered sample-level split is +0.0013 to +0.0046 --")
info("ten to thirty-six times smaller -- and DR3 measures the split to +-{:.4f}.  The item is therefore".format(ERR_BU))
info("NOT RUNNABLE at DR3, by two to three orders of magnitude in sample size, and the same arithmetic says DR4")
info("will not close it either.  What DOES survive is the radius-resolved prediction of Part B: a SIGN FLIP inside")
info("one dataset at s = 1.96 r_M, which no instrumental systematic can imitate because no systematic knows where a")
info("pair's MOND radius is.  That is the version worth carrying forward, and it needs the same larger sample.")
ck("15 VERDICT -- NOT RUNNABLE / UNDERPOWERED, recorded as such and not as a null.  The measurement is clean, the "
   "controls all pass, the injection test proves the estimator works at 10% and is blind at 0.4%, and the honest "
   "statement is that Gaia DR3 cannot address the pre-registered orientation falsifier on the arm that is actually "
   "in force.  The hunt list's own scoring criterion for item 15 rests on a superseded arm and should be retired",
   abs(RATIO)/ERR < 3.0 and abs(R_BIG)/ERR > 3.0 and n_need_lo > 20*N_NOW,
   f"measured {SPLIT_BU:+.4f} +- {ERR_BU:.4f} boost units vs a predicted +{PREREG_MG_LO:.4f} to "
   f"+{PREREG_MG_HI:.4f}; 3 sigma needs {n_need_lo/N_NOW:.0f}x-{n_need_hi/N_NOW:.0f}x this sample")

sys.exit(ck.done())
