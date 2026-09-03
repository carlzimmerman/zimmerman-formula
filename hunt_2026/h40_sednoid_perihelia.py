#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
h40_sednoid_perihelia.py -- HUNT ITEM 40: THE SEDNOIDS.
========================================================
The hunt list asks for "a specific q distribution edge at the Sun's r_M scale (7,960 / 7,250 AU)".  THE FIRST RESULT
OF THIS SCRIPT IS THAT THE ITEM IS MIS-POSED: the sednoids' perihelia are 38-81 AU, TWO ORDERS OF MAGNITUDE inside
r_M, where the Sun's field is ~10^4 a_0 and the kernel's correction, for Route A, is exp(-r_M/q) ~ 10^-43.  There is
no q edge at r_M and the framework never said there was.  That half of the item is WITHDRAWN, with the numbers.

What the framework DOES say about these objects is a different and sharper thing, and it is computed here.  The
sednoids are "detached": their perihelia sit far outside Neptune's reach, so something raised them after they were
scattered, and in Newtonian gravity that something has to be the Galactic tide (too weak at a few hundred AU), a
stellar flyby, the Sun's birth cluster, or an undiscovered planet.  The framework adds one more torque for free.
Its size follows from the kernel and the Galactic external field with no free parameter, by expanding the algebraic
QUMOND field of the Sun in the (much smaller) external field:

   g = nu(|s + G_ext|/a_0)(s + G_ext),  |s| >> |G_ext|
     = [Newtonian] + (nu(y)-1) s          <- radial, CANNOT change angular momentum, so irrelevant here
                  + (nu(y)-1) G_ext       <- almost uniform; its GRADIENT is a tide, A1 = |nu'| (2y/r) x_ext a_0
                  + nu'(y)(s.G_ext)/a_0 s <- the anisotropic term, axis along G_ext; A2 = |nu'| y x_ext a_0/r = A1/2

with y = G M_sun/(a_0 r^2) = (r_M/r)^2.  For Route A, nu(y)-1 -> exp(-r_M/r) exactly, so the anomalous tide is
EXPONENTIALLY switched on with heliocentric distance -- nothing at all in the planetary region, everything beyond
~500 AU.  Compared throughout with the Galactic vertical tide A_gal = 4 pi G rho_0 = 5.7e-30 s^-2, which is the
Newtonian alternative and is the mechanism "Planet 9" exists to supplement.

Crucially the two tides have DIFFERENT SYMMETRY AXES -- the Galactic tide about the Galactic pole, the kernel's about
the Sun-Galactic-centre line -- so each object's geometric efficiency factor sin^2(i) must be measured from ITS OWN
axis.  Both are computed here from the orbit normals.

DATA: JPL SBDB, all 7,285 catalogued trans-Neptunian objects with full-precision elements, fetched this session to
real_research/data/tno/jpl_sbdb_tno.json.  44 have a > 150 AU and q > 38 AU.

TWO LIMITATIONS STATED UP FRONT.  (1) The algebraic form g = nu(g_N)g_N is exact only in spherical symmetry, and in
this configuration it does not reconcile the Sun's own centre-of-mass acceleration nu(x_ext)G_ext with the field
~G_ext felt at small r; a proper AQUAL/QUMOND solve (Milgrom 2009; Blanchet & Novak 2011) resolves that and returns
an anomalous quadrupole Q2.  The coefficients here are the leading term of the same expansion and are good to a
factor ~2 -- which the exponential makes irrelevant for the crossover radius (a factor 2 in A moves it by 4%).
(2) The detached population is severely selection-limited and the observed q-a correlation is partly a survey
artefact; every correlation below is therefore also computed with a partialled out.  Both footings.  Mutations.
"""
import sys, math, os, json
import numpy as np
from scipy.stats import spearmanr, rankdata
from hunt_lib import *

ck = Check(); rng = np.random.default_rng(4040)
AU = 1.495978707e11; GYR = 3.1557e16; MSUN_GM = 1.32712440018e20   # G M_sun, m^3/s^2
AGE = 4.5*GYR
RHO0 = 0.10                       # Msun/pc^3, local dynamical density (Holmberg-Flynn; Gaia agrees at 0.08-0.12)
A_GAL = 4*math.pi*G*(RHO0*Msun/(3.0857e16)**3)
Q_SCATTER = 35.0                  # AU: the perihelion a Neptune-scattered object starts with

P("="*116); P("ITEM 40 -- the sednoids: the item's premise, then what the framework actually predicts"); P("="*116)
r_M = {ft: math.sqrt(MSUN_GM/a0)/AU for ft, a0 in A0.items()}
info(f"the Sun's MOND radius r_M = sqrt(G M_sun/a_0) = {r_M['canonical']:.0f} (canonical) / {r_M['alt']:.0f} (alt) AU")
info(f"the Galactic vertical tide, the Newtonian alternative: A_gal = 4 pi G rho_0 = {A_GAL:.2e} s^-2 at rho_0 = {RHO0} Msun/pc^3")

# ---------------------------------------------------------------- the data
J = json.load(open(os.path.join(DATA, "tno", "jpl_sbdb_tno.json")))
fld = {n: i for i, n in enumerate(J["fields"])}
def fv(r, k):
    try: return float(r[fld[k]])
    except (TypeError, ValueError): return np.nan
tno = []
for r in J["data"]:
    a, e, q, i_, om, w = (fv(r, k) for k in ("a", "e", "q", "i", "om", "w"))
    if not all(np.isfinite([a, e, q, i_, om, w])) or a <= 0 or e >= 1: continue
    tno.append(dict(name=r[fld["full_name"]].strip(), a=a, e=e, q=q, i=i_, om=om, w=w, Q=a*(1+e)))
etno = [t for t in tno if t["a"] > 150 and t["q"] > 38]
info(f"JPL SBDB: {len(tno)} TNOs with usable elements; {len(etno)} have a > 150 AU and q > 38 AU (the detached/extreme population)")
qs = np.array([t["q"] for t in etno])
info(f"their perihelia run {qs.min():.1f} to {qs.max():.1f} AU; the largest is 2012 VP113 at {qs.max():.1f} AU")

# ---------------------------------------------------------------- 40a: the item's premise
for ft, a0 in A0.items():
    y_q = MSUN_GM/(a0*(qs.max()*AU)**2)
    info(f"{ft:10} at the LARGEST sednoid perihelion ({qs.max():.1f} AU) the Sun's field is {y_q:.3e} a_0 and the kernel's "
         f"correction nu-1 = exp(-r_M/q) = {math.exp(-math.sqrt(y_q)):.1e}")
ck("40a AGAINST THE ITEM AS WRITTEN -- there is no perihelion edge at the Sun's MOND radius and there could not be: every "
   "sednoid perihelion is 90-200 times INSIDE r_M, where the kernel's correction is exp(-r_M/q) < 1e-38.  The 'q edge at "
   "7960 AU' half of item 40 is WITHDRAWN as mis-posed; r_M is an APHELION-scale quantity for these objects, not a "
   "perihelion-scale one",
   qs.max() < 0.02*r_M["canonical"],
   f"largest q = {qs.max():.1f} AU = r_M/{r_M['canonical']/qs.max():.0f}; nu-1 there = "
   f"{math.exp(-r_M['canonical']/qs.max()):.1e} (canonical)")

# ---------------------------------------------------------------- the anomalous tide
def nu_prime(y):
    """d nu/dy for Route A, exactly."""
    y = max(float(y), 1e-30); u = math.sqrt(y)
    if u > 700: return 0.0
    em = math.exp(-u)
    return -em/(2*u*(1 - em)**2)

def log10_A_mond(r_m_, a0, xext):
    """log10 of the anomalous tidal coefficient, computed in logs so the planetary region does not underflow."""
    y = MSUN_GM/(a0*r_m_**2); u = math.sqrt(y)
    # 3 |nu'| y x_ext a_0 / r  with |nu'| = e^-u /(2u(1-e^-u)^2);  for large u, (1-e^-u)^2 -> 1
    log_nup = (-u/math.log(10)) - math.log10(2*u) - 2*math.log10(1 - math.exp(-u)) if u < 700 \
              else (-u/math.log(10)) - math.log10(2*u)
    return math.log10(3.0) + log_nup + math.log10(y) + math.log10(xext) + math.log10(a0) - math.log10(r_m_)

def A_mond(r_m_, a0, xext):
    if xext <= 0: return 0.0
    L = log10_A_mond(r_m_, a0, xext)
    return 10**L if L > -300 else 0.0

def x_ext_newtonian(a0):
    """the Galactic field at the Sun is v_c^2/R0 (MONDian); invert x nu(x) = that for the Newtonian-equivalent."""
    g_tot = (233e3)**2/(8.2*kpc)
    t = g_tot/a0; lo, hi = 1e-4, 100.0
    for _ in range(200):
        mid = math.sqrt(lo*hi)
        if mid*nu_s(mid) < t: lo = mid
        else: hi = mid
    return math.sqrt(lo*hi), t

def orbit_avg_A(a_AU, e, a0, xext, n=1440):
    """time-average over one Kepler orbit: <A> = (1/2pi) int A(r(E)) (1 - e cos E) dE."""
    E = np.linspace(0, 2*math.pi, n); w = 1 - e*np.cos(E)
    return float(np.mean(np.array([A_mond(a_AU*AU*ww, a0, xext) for ww in w])*w))

P(""); P("="*116); P("what the framework actually predicts: an APHELION crossover where the kernel's tide beats the Galaxy's")
P("="*116)
XE = {}
for ft, a0 in A0.items():
    xe, gm = x_ext_newtonian(a0); XE[ft] = xe
    info(f"{ft:10} the Galactic field at the Sun: {gm:.2f} a_0 MONDian -> Newtonian-equivalent x_ext = {xe:.2f}")
info(f"{'r [AU]':>9} " + " ".join(f"{'log10(A_MOND/A_gal) ('+ft+')':>32}" for ft in A0))
for rAU in (10, 30, 100, 300, 500, 700, 1000, 2000, 3000, 5000):
    row = [log10_A_mond(rAU*AU, a0, XE[ft]) - math.log10(A_GAL) for ft, a0 in A0.items()]
    info(f"{rAU:9.0f} " + " ".join(f"{v:32.1f}" for v in row))
def crossover(a0, xext):
    lo, hi = 20.0, 20000.0
    for _ in range(300):
        mid = math.sqrt(lo*hi)
        if log10_A_mond(mid*AU, a0, xext) < math.log10(A_GAL): lo = mid
        else: hi = mid
    return math.sqrt(lo*hi)
CROSS = {ft: crossover(a0, XE[ft]) for ft, a0 in A0.items()}
info(f"the crossover -- where the kernel's anomalous tide equals the Galactic vertical tide -- is at r = "
     f"{CROSS['canonical']:.0f} (canonical) / {CROSS['alt']:.0f} AU.  Because the switch-on is exponential, a factor 2")
info(f"of theory error in A moves this radius by only ~4%, which is why the number is worth quoting at all.")
ck("40b the framework's real statement about the outer solar system is a SHARP APHELION SCALE, not a perihelion one: "
   "because Route A's return to Newton is exponential (nu-1 = exp(-r_M/r) exactly), the kernel's anomalous tide is "
   "switched on over less than a factor 3 in radius, and it overtakes the Galactic tide at ~450-500 AU.  A decade inside "
   "that it is 10^-100 of the Galaxy's; a factor 6 outside it is 10^4 times",
   400 < CROSS["canonical"] < 800 and (log10_A_mond(3000*AU, A0['canonical'], XE['canonical']) - math.log10(A_GAL)) > 4,
   f"crossover {CROSS['canonical']:.0f} / {CROSS['alt']:.0f} AU; log10(A_MOND/A_gal) = "
   f"{log10_A_mond(300*AU, A0['canonical'], XE['canonical']) - math.log10(A_GAL):.1f} at 300 AU, "
   f"{log10_A_mond(3000*AU, A0['canonical'], XE['canonical']) - math.log10(A_GAL):.1f} at 3000 AU")

# ---------------------------------------------------------------- orbit normals and the two symmetry axes
EPS = math.radians(23.43929111)
Rec = np.array([[1, 0, 0], [0, math.cos(EPS), -math.sin(EPS)], [0, math.sin(EPS), math.cos(EPS)]])
def unit(ra_deg, dec_deg):
    ra, de = math.radians(ra_deg), math.radians(dec_deg)
    return np.array([math.cos(de)*math.cos(ra), math.cos(de)*math.sin(ra), math.sin(de)])
NGP = unit(192.85948, 27.12825); GC = unit(266.40498, -28.93617)
def normal_eq(t):
    i_, om = math.radians(t["i"]), math.radians(t["om"])
    return Rec @ np.array([math.sin(i_)*math.sin(om), -math.sin(i_)*math.cos(om), math.cos(i_)])
for t in tno:
    n = normal_eq(t)
    t["s2_gal"]  = 1.0 - float(n @ NGP)**2      # sin^2(inclination to the GALACTIC PLANE) -- the Galactic tide's factor
    t["s2_mond"] = 1.0 - float(n @ GC)**2       # sin^2(inclination to the GC axis)        -- the kernel tide's factor
info("")
info("BUG FOUND AND FIXED IN THE MAKING: the first version of this script used sin^2 of the ECLIPTIC inclination as the")
info("Galactic tide's efficiency factor.  That is wrong -- the vertical tide's axis is the Galactic pole, which is 60 deg")
info("from the ecliptic pole -- and it made the Newtonian alternative look about 5x weaker than it is.  Corrected here:")
info(f"Sedna's ecliptic inclination is 11.9 deg (sin^2 = 0.04) but its inclination to the GALACTIC plane gives sin^2 = "
     f"{[t for t in etno if 'Sedna' in t['name']][0]['s2_gal']:.2f}.")

# ---------------------------------------------------------------- 40c/40d: does it detach what is detached?
P(""); P("="*116); P("does the kernel's tide detach the objects that are detached?"); P("="*116)
def dq_max(Aavg, a_AU, e, s2, t=AGE):
    """the SAME secular formula for both tides: |de/dt|_max = (5/2)(A/n) e sqrt(1-e^2) sin^2(i to the tide's own axis)."""
    n = math.sqrt(MSUN_GM/(a_AU*AU)**3)
    return a_AU*min(1.0, 2.5*(Aavg/n)*e*math.sqrt(max(1 - e*e, 0.0))*s2*t)
for t in etno:
    for ft, a0 in A0.items():
        Am = orbit_avg_A(t["a"], t["e"], a0, XE[ft])
        t["ratio_" + ft] = Am/A_GAL
        t["dq_mond_" + ft] = dq_max(Am, t["a"], t["e"], t["s2_mond"])
    t["dq_gal"] = dq_max(A_GAL, t["a"], t["e"], t["s2_gal"])
srt = sorted(etno, key=lambda t: -t["q"])
info(f"{'object':30} {'a[AU]':>8} {'q[AU]':>7} {'Q[AU]':>8} {'sin2 gal':>9} {'sin2 GC':>8} {'<A_M>/A_gal':>12} {'dq_MOND':>9} {'dq_gal':>8}")
for t in srt[:18]:
    info(f"{t['name'][:30]:30} {t['a']:8.1f} {t['q']:7.1f} {t['Q']:8.0f} {t['s2_gal']:9.2f} {t['s2_mond']:8.2f} "
         f"{t['ratio_canonical']:12.2e} {t['dq_mond_canonical']:9.1f} {t['dq_gal']:8.1f}")
need = np.array([t["q"] - Q_SCATTER for t in etno])
n_mond = sum(1 for t in etno if t["dq_mond_canonical"] > t["q"] - Q_SCATTER)
n_gal  = sum(1 for t in etno if t["dq_gal"]           > t["q"] - Q_SCATTER)
info(f"objects whose present perihelion could have been raised from q = {Q_SCATTER:.0f} AU in 4.5 Gyr, same formula both ways: "
     f"kernel tide {n_mond}/{len(etno)} (canonical), Galactic tide {n_gal}/{len(etno)}")

# which objects does the kernel's tide reach that the Galaxy's does not?  that is the framework's own window
only_mond = [t for t in etno if t["dq_mond_canonical"] > t["q"] - Q_SCATTER and t["dq_gal"] <= t["q"] - Q_SCATTER]
only_gal  = [t for t in etno if t["dq_gal"] > t["q"] - Q_SCATTER and t["dq_mond_canonical"] <= t["q"] - Q_SCATTER]
info(f"reachable by the kernel's tide but NOT by the Galaxy's: {len(only_mond)} objects "
     f"({', '.join(t['name'][:22] for t in only_mond)})")
info(f"reachable by the Galaxy's but not the kernel's: {len(only_gal)} objects")
ck("40c AGAINST INTEREST, and this is the fixed-bug result: once the Galactic tide is given its OWN inclination factor -- "
   "the inclination to the Galactic plane, not to the ecliptic, which the first version of this script got wrong -- the "
   "Newtonian alternative detaches almost as many of these objects as the kernel does.  The kernel's tide is 10^4 times "
   "stronger where it is strong, but by then the Galactic tide is already sufficient, so the framework's advantage is a "
   "narrow window in aphelion and a handful of objects, not a new explanation of the detached population",
   n_mond > n_gal and n_mond < 2*n_gal,
   f"kernel tide detaches {n_mond}/{len(etno)}, Galactic tide {n_gal}/{len(etno)}, same formula and same 4.5 Gyr; only "
   f"{len(only_mond)} objects are reached by the kernel and not by the Galaxy")

# the crossover test: the framework predicts detachment TURNS ON above Q ~ 500 AU
Qc = CROSS["canonical"]
lo = [t for t in etno if t["Q"] < Qc]; hi = [t for t in etno if t["Q"] >= Qc]
qlo = np.array([t["q"] for t in lo]); qhi = np.array([t["q"] for t in hi])
from scipy.stats import mannwhitneyu, hypergeom
U, p_mw = mannwhitneyu(qhi, qlo, alternative="greater")
top3_below = sum(1 for t in sorted(etno, key=lambda t: -t["q"])[:3] if t["Q"] < Qc)
p_top3 = hypergeom.sf(top3_below - 1, len(etno), len(lo), 3)
info(f"the framework's own edge, tested directly: {len(lo)} objects below the crossover ({Qc:.0f} AU), {len(hi)} above")
info(f"   below: median q = {np.median(qlo):.1f} AU, max {qlo.max():.1f}; above: median q = {np.median(qhi):.1f} AU, "
     f"max {qhi.max():.1f}")
info(f"   Mann-Whitney (is q higher ABOVE the edge, as the framework requires?) p = {p_mw:.3f}")
info(f"   the three highest perihelia known (80.6, 74.7, 65.9 AU) all sit BELOW the edge, where the kernel's tide is "
     f"10^-5 to 10^-1 of the Galaxy's; by chance that happens with p = {p_top3:.3f}")
ck("40d THE EDGE IS NOT ESTABLISHED, EITHER WAY, and neither reading may be quoted: the median perihelion is indeed higher "
   "above the crossover (44.9 vs 40.1 AU) as the framework wants, and the three most detached bodies known all sit below "
   "it where the mechanism does nothing, as the framework does not.  Neither fact reaches 3 sigma and both are degenerate "
   "with the same selection",
   min(p_mw, p_top3) > 0.0027,
   f"q higher above the edge: p = {p_mw:.3f}; the top three perihelia all below the edge: p = {p_top3:.3f}; N = {len(etno)}")

# the correlation route, and why it is structurally void
ratio = np.array([t["ratio_canonical"] for t in etno]); qq = np.array([t["q"] for t in etno])
aa = np.array([t["a"] for t in etno]); ee = np.array([t["e"] for t in etno])
lr = np.log10(np.maximum(ratio, 1e-300))
rho_raw, p_raw = spearmanr(lr, qq)
rho_qa, p_qa = spearmanr(np.log10(aa), qq)
def partial_spearman(x, y, z):
    rx, ry, rz = rankdata(x), rankdata(y), rankdata(z)
    ex = rx - np.polyval(np.polyfit(rz, rx, 1), rz); ey = ry - np.polyval(np.polyfit(rz, ry, 1), rz)
    return spearmanr(ex, ey)
rho_par, p_par = partial_spearman(lr, qq, np.log10(aa))
rho_re, _ = spearmanr(lr[np.argsort(aa)], ee[np.argsort(aa)])
info(f"raw Spearman rho(q, log A_MOND/A_gal) = {rho_raw:+.3f} (p = {p_raw:.4f}); rho(q, log a) = {rho_qa:+.3f} "
     f"(p = {p_qa:.4f}); with log a partialled out, rho = {rho_par:+.3f} (p = {p_par:.3f})")
ck("40e MY OWN TEST WITHDRAWN -- the correlation route to this item is structurally void and no version of it can work.  "
   "The tide ratio is a deterministic function of (a, e) and so is q = a(1-e), so the raw +0.52 is the population's q-a "
   "correlation and the partial -0.38 is the arithmetic fact that at fixed a a larger ratio means a larger e means a "
   "smaller q.  Neither number carries information about the tide.  The only test that could work is a forward model of "
   "the (a, e) distribution through the surveys' selection function, which is out of this script's scope",
   abs(rho_par + 0.38) < 0.15 and abs(rho_raw - rho_qa) < 0.15,
   f"raw rho = {rho_raw:+.3f} tracks rho(q, log a) = {rho_qa:+.3f} to {abs(rho_raw-rho_qa):.3f}; the partial "
   f"{rho_par:+.3f} is the forced q = a(1-e) anticorrelation, not a measurement")

# ---------------------------------------------------------------- 40f: the ephemeris corollary
P(""); P("="*116); P("the corollary the ephemerides already test"); P("="*116)
EPH_Q2 = 3e-27          # published ephemeris bound on an anomalous quadrupole |Q2| (Saturn ranging dominates)
for ft, a0 in A0.items():
    L_sat = log10_A_mond(9.58*AU, a0, XE[ft]); L_nep = log10_A_mond(30.1*AU, a0, XE[ft])
    y_sat = MSUN_GM/(a0*(9.58*AU)**2)
    simple = 3.0*(1/(2*y_sat**2))*y_sat*XE[ft]*a0/(9.58*AU)      # same expansion, nu-1 = 1/(2y): |nu'| = 1/(2y^2)
    info(f"{ft:10} Route A's anomalous quadrupole: 10^{L_sat:.0f} s^-2 at Saturn (9.58 AU), 10^{L_nep:.0f} at Neptune (30.1 AU)")
    info(f"{ft:10} the SAME expansion with a power-law-return kernel (nu-1 = 1/(2y), the 'simple'/alpha=1 family) gives "
         f"{simple:.1e} s^-2 at Saturn, against a published bound of ~{EPH_Q2:.0e}")
ck("40f the kernel's exponential return is what keeps the framework out of the planetary ephemerides: Route A's anomalous "
   "quadrupole at Saturn is exp(-r_M/r)-suppressed to 10^-380, where the same expansion with a power-law-return kernel "
   "lands within an order of magnitude of the published limit.  This is the outer-solar-system face of the repository's "
   "standing alpha = 1 ephemeris liability and it comes out the right way for Route A",
   log10_A_mond(9.58*AU, A0["canonical"], XE["canonical"]) < -100,
   f"Route A at Saturn 10^{log10_A_mond(9.58*AU, A0['canonical'], XE['canonical']):.0f} s^-2 vs the bound {EPH_Q2:.0e}; the "
   f"alpha=1 form at the same place is "
   f"{3.0*(1/(2*(MSUN_GM/(A0['canonical']*(9.58*AU)**2))))*XE['canonical']*A0['canonical']/(9.58*AU):.1e}")

# ---------------------------------------------------------------- 40g: the framework-only orientation signature
P(""); P("="*116); P("the signature that is the framework's alone: the tide's symmetry axis"); P("="*116)
info("the Galactic vertical tide is symmetric about the GALACTIC POLE; the kernel's anomalous tide is symmetric about the")
info("direction of the external field, i.e. about the SUN-GALACTIC-CENTRE line.  Two different axes, so the two mechanisms")
info("sculpt different orientation patterns.  Nothing in Newtonian gravity has the second axis at all.")
def report(sample, label):
    cg = np.array([1 - t["s2_mond"] for t in sample]); cn = np.array([1 - t["s2_gal"] for t in sample])
    bg = np.array([cg[rng.integers(0, len(cg), len(cg))].mean() for _ in range(4000)])
    bn = np.array([cn[rng.integers(0, len(cn), len(cn))].mean() for _ in range(4000)])
    info(f"{label:38} N = {len(sample):5d}: <cos^2(normal, GC)> = {cg.mean():.3f} +- {bg.std():.3f}, "
         f"<cos^2(normal, NGP)> = {cn.mean():.3f} +- {bn.std():.3f}   (isotropic = 0.333)")
    return cg.mean(), bg.std()
gc_e, gc_es = report(etno, "the 44 extreme objects")
classical = [t for t in tno if 39 < t["a"] < 48 and t["q"] > 35]
gc_c, gc_cs = report(classical, "classical belt (the selection control)")
dev = abs(gc_e - gc_c)/math.hypot(gc_es, gc_cs)
ck("40g UNDERPOWERED, and recorded as underpowered rather than as a null: the orientation test that would separate the "
   "kernel's tide (axis = the Galactic centre) from the Galactic tide (axis = the pole) needs the extreme objects' orbit "
   "normals to sit differently about the GC direction than a selection-matched control does.  With 44 objects the "
   "difference is under 2 sigma against a 3 sigma bar, and the ecliptic survey footprint dominates both samples.  This is "
   "the right test to inherit and it needs LSST's ETNO haul, not this one",
   dev < 3.0,
   f"<cos^2 to GC> = {gc_e:.3f} +- {gc_es:.3f} for the extreme objects vs {gc_c:.3f} +- {gc_cs:.3f} for the classical belt "
   f"-> {dev:.1f} sigma; both far from isotropic (0.333) because both are ecliptic-selected")

# ---------------------------------------------------------------- mutations
P("")
mut_cross = crossover(A0["canonical"]*100, XE["canonical"])
ck("M40 mutation: a_0 -> 100 a_0 shrinks r_M tenfold and must move the crossover radius by the same order -- if it does "
   "not, the exponential is not doing the work and the estimator is broken",
   abs(math.log10(mut_cross/CROSS["canonical"])) > 0.5,
   f"crossover moves {CROSS['canonical']:.0f} -> {mut_cross:.0f} AU under a_0 x100")
sh = np.array([abs(spearmanr(rng.permutation(lr), qq)[0]) for _ in range(2000)])
ck("M40b mutation: shuffling the ratios between objects destroys the raw correlation, confirming the estimator reads the "
   "pairing and not the marginals -- which is exactly why the pairing being forced by (a, e) makes the test void",
   sh.mean() < 0.5*abs(rho_raw) and (sh > abs(rho_raw)).mean() < 0.05,
   f"2000 shuffles: mean |rho| = {sh.mean():.3f}, {(sh > abs(rho_raw)).mean()*100:.1f}% exceed the real |{rho_raw:.3f}|")
ck("M40c mutation: with no external field the whole anomalous tide must vanish identically -- the effect is the EXTERNAL "
   "FIELD acting through the kernel, which is exactly why Newtonian gravity has no counterpart to it",
   A_mond(1000*AU, A0["canonical"], 0.0) == 0.0,
   f"x_ext = 0 gives A = {A_mond(1000*AU, A0['canonical'], 0.0):.1e} s^-2 where x_ext = {XE['canonical']:.2f} gives "
   f"{A_mond(1000*AU, A0['canonical'], XE['canonical']):.1e}")

P("")
info("SUMMARY OF ITEM 40, both ways.  The perihelion-edge-at-r_M prediction the list asked for does not exist and is")
info("withdrawn with its numbers.  The framework's genuine outer-solar-system statement is an exponentially sharp")
info("APHELION crossover at ~450-500 AU beyond which its tide dwarfs the Galaxy's by four orders of magnitude -- and the")
info("detached population cannot resolve it: the median perihelion IS higher above the edge as the framework wants")
info("(p = 0.05), but the three most detached bodies known sit BELOW it where the mechanism does nothing (p = 0.09), and")
info("the correlation route is void because q, a and the tide ratio are all functions of the same two orbital elements.")
info("Planet 9, a stellar flyby and the birth cluster are not displaced by this.  What is worth inheriting is the")
info("orientation test: the kernel's tide has a symmetry axis pointing at the Galactic centre and Newtonian gravity does not.")
sys.exit(ck.done())
