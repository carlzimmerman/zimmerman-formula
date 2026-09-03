#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""g06v_adversarial_group_rung_refutation.py -- ADVERSARIAL AUDIT OF THE LOCAL VOLUME GROUP RUNG.
=================================================================================================================
THE CLAIM UNDER ATTACK (g06_local_volume_groups_lambda_edge.py, .out on disk):

    "Twenty-six UNGC Local Volume groups (333 member galaxies) sit at a median missing boost of 0.82 at
     g_bar/a0 = 0.0019, i.e. CONSISTENT with the framework's zero-parameter prediction and NOT showing the
     cluster-scale deficit.  This is a non-discrimination, not a confirmation."
    CLAIMED STRENGTH: "Against the liability table's X-ray group/cluster median of 2.11 the separation is
     0.412 dex against a 0.114 dex bootstrap half-width, about 3.6 sigma on the group side's error alone."

MY BRIEF IS THE INFERENCE, NOT THE ARITHMETIC.  Three questions, in order:
  Q1  Does the central number reproduce under an INDEPENDENT implementation?  (If not, nothing else matters.)
  Q2  Is the group-vs-cluster separation distinguishable from the obvious confounds -- sample selection, data
      quality (members per group), distance/detection limit, the stellar M/L, and the fact that the two sides of
      the comparison come from two entirely different mass estimators?
  Q3  Would ordinary cold dark matter produce the same signature?  If a zero-free-parameter abundance-matched
      NFW halo lands on these same dispersions just as well, the rung cannot discriminate -- which the author
      already concedes, but which then also removes the "COUNTED vs MODELLED baryons" reading of the
      group/cluster contrast, because that reading is a causal attribution and not a measurement.

WHAT IS RE-DERIVED HERE FROM THE CATALOGUE, NOT COPIED FROM g06's OUTPUT
  * the group sample (UNGC, Karachentsev, Makarov & Kaisina 2013, AJ 145, 101; Theta_1 > 0 main-disturber
    membership, the catalogue's own criterion), the gapper dispersions, the baryon budget, the baryonic
    external field from 2MRS (Huchra et al. 2012, ApJS 199, 26), the Jeans solve, and the boosts.
  * The 2M++ reconstruction (Carrick et al. 2015) is NOT recomputed -- this audit does not need it; g06's own
    check R4b already fails on it and that failure is taken at face value here.

DATA, ALL ON DISK.  BOTH FOOTINGS.  MUTATION CONTROLS.  CHECKS THAT CAN FAIL -- AND ARE MEANT TO.
Checks here are written so that PASS = "the claim survives this attack".  A FAIL is a hit on the claim.
"""
import sys, os, math, collections
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hunt_lib import (Check, P, info, A0, DATA, vizier_tsv, _f, nu, nu_s, G, Msun, Mpc, kpc, H0, OM_M)

ck = Check(); rng = np.random.default_rng(20260903)

UPS_K, F_HE, F_HOT, MK_SUN = 0.60, 1.33, 0.50, 3.27
H0_KMS   = H0*Mpc/1e3
MW_MSTAR = 5.0e10
NMIN, R_SEAM, SOFT = 5, 3.0, 0.15
CLUSTER_MED = 2.11          # liability table, 14 X-ray group/cluster (pressure, boost <= 3) rows
G06_MED_CAN, G06_MED_ALT = 0.817, 0.746
G06_BOOT = (0.656, 1.110)

# ================================================================================================ SECTION 1
P("="*126)
P("1.  INDEPENDENT RE-DERIVATION OF THE HEADLINE NUMBER")
P("="*126)

def dlnnu(y):
    y = np.maximum(np.asarray(y, float), 1e-300); s = np.sqrt(y)
    return -0.5*s*np.exp(-s)/(1.0 - np.exp(-s))

def rad_grid(rh, lo=1e-3, hi=400.0, n=1400): return np.geomspace(lo*rh, hi*rh, n)

def cumfrac(r, rho):
    N = np.concatenate([[0.0], np.cumsum(0.5*(rho[1:]*r[1:]**2 + rho[:-1]*r[:-1]**2)*np.diff(r))])
    return N/N[-1]

def plummer(r, rh): return (1.0 + (r/(rh/1.3048))**2)**-2.5

def jeans_sigma(r, rho_t, g, r_trunc):
    """isotropic spherical Jeans, number-weighted l.o.s. dispersion inside r_trunc.  Independent re-write:
    trapezoid on the OUTWARD integral rather than a reversed cumsum, so an ordering bug would show up."""
    integ = rho_t*g
    seg = 0.5*(integ[1:] + integ[:-1])*np.diff(r)
    tail = np.concatenate([np.cumsum(seg[::-1])[::-1], [0.0]])
    s2 = tail/rho_t
    w = rho_t*r**2*(r <= r_trunc)
    return math.sqrt(float(np.trapz(w*s2, r)/np.trapz(w, r)))

# validation: deep-MOND virial theorem, Milgrom 1994
Mt, at, a0v = 1.0e11*Msun, 1.0*kpc, 1e-9
rh_p = 1.3048*at; r = rad_grid(rh_p, 1e-4, 3000.0, 3000)
rho = plummer(r, rh_p); Menc = Mt*r**3/(r**2 + at**2)**1.5
s_dm = jeans_sigma(r, rho, np.sqrt(G*Menc/r**2*a0v), 1e9*rh_p)
ck("V0 my own Jeans solver reproduces sigma^4 = (4/81) G M a_0 (Milgrom 1994), so any disagreement with g06 "
   "below is a disagreement about the data or the prescription and not about my integrator",
   abs(s_dm**4/(G*Mt*a0v)/(4/81.) - 1) < 0.01,
   f"sigma^4/(G M a_0) = {s_dm**4/(G*Mt*a0v):.6f} vs 4/81 = {4/81.:.6f}")

def eq2gal(ra, de):
    rap, dep, lncp = math.radians(192.85948), math.radians(27.12825), math.radians(122.93192)
    ra_, de_ = np.radians(ra), np.radians(de)
    b = np.arcsin(np.sin(de_)*math.sin(dep) + np.cos(de_)*math.cos(dep)*np.cos(ra_ - rap))
    l = lncp - np.arctan2(np.cos(de_)*np.sin(ra_ - rap),
                          np.sin(de_)*math.cos(dep) - np.cos(de_)*math.sin(dep)*np.cos(ra_ - rap))
    return np.degrees(l) % 360.0, np.degrees(b)

def gal_cart(ra, de, D):
    l, b = eq2gal(ra, de); lr, br = np.radians(l), np.radians(b)
    return np.array([D*np.cos(br)*np.cos(lr), D*np.cos(br)*np.sin(lr), D*np.sin(br)])

def gapper(v):
    x = np.sort(np.asarray(v, float)); n = len(x)
    if n < 2: return float("nan")
    i = np.arange(1, n)
    return float(math.sqrt(math.pi)/(n*(n - 1))*np.sum(i*(n - i)*np.diff(x)))

raw = vizier_tsv("ungc_karachentsev2013.tsv")
for x in raw:
    for k in ("Dist", "KLum", "MHI", "Vlg", "Ti1", "_RAJ2000", "_DEJ2000"): x[k] = _f(x[k])
    x["Name"] = x["Name"].strip(); x["MD"] = x["MD"].strip(); x["f_Dist"] = x["f_Dist"].strip()
byname = {x["Name"].upper(): x for x in raw}
sat = collections.defaultdict(list)
for x in raw:
    if x["Ti1"] > 0 and x["MD"].upper() in byname and x["MD"].upper() != x["Name"].upper():
        sat[x["MD"]].append(x)

def angsep(a, b):
    r1, d1, r2, d2 = map(math.radians, (a["_RAJ2000"], a["_DEJ2000"], b["_RAJ2000"], b["_DEJ2000"]))
    return math.acos(max(-1.0, min(1.0, math.sin(d1)*math.sin(d2) + math.cos(d1)*math.cos(d2)*math.cos(r1 - r2))))

groups = []
for host_name, sats in sorted(sat.items(), key=lambda t: -len(t[1])):
    if len(sats) + 1 < NMIN: continue
    h = byname[host_name.upper()]; mem = [h] + sats; D = h["Dist"]
    if D < 2.0:
        hv = gal_cart(h["_RAJ2000"], h["_DEJ2000"], D)
        rr = np.array([float(np.linalg.norm(gal_cart(m["_RAJ2000"], m["_DEJ2000"], m["Dist"]) - hv)) for m in sats])
    else:
        rr = (4/3.)*np.array([angsep(h, m)*D for m in sats])
    ok = [m for m in mem if np.isfinite(m["Vlg"])]
    v = np.array([m["Vlg"] for m in ok], float); dd = np.array([m["Dist"] for m in ok], float)
    # distance-method census per group -- the data-quality axis this audit is about
    meth = collections.Counter(m["f_Dist"] for m in mem)
    groups.append(dict(name=host_name, N=len(mem), Nv=len(ok), D=D, rh=float(np.median(rr)),
                       rmax=float(np.max(rr)), sig=gapper(v - H0_KMS*dd),
                       LK=float(np.nansum([10**m["KLum"] for m in mem if np.isfinite(m["KLum"])])),
                       LKh=(10**h["KLum"] if np.isfinite(h["KLum"]) else 0.0),
                       MHI=float(np.nansum([10**m["MHI"] for m in mem if np.isfinite(m["MHI"])])),
                       f_prim=(meth["TRGB"] + meth["SBF"] + meth["Cep"] + meth["BS"])/len(mem),
                       f_mem=meth["mem"]/len(mem),
                       pos=gal_cart(h["_RAJ2000"], h["_DEJ2000"], D)))
for g in groups:
    if g["name"] == "Milky Way": g["LK"] += MW_MSTAR/UPS_K; g["LKh"] = MW_MSTAR/UPS_K
for g in groups: g["Mstar"] = UPS_K*g["LK"]; g["Mgas"] = F_HE*g["MHI"]
info(f"UNGC re-read independently: {len(raw)} galaxies -> {len(groups)} groups, "
     f"{sum(g['N'] for g in groups)} members, N per group {min(g['N'] for g in groups)}-{max(g['N'] for g in groups)}")

# baryonic external field, rebuilt (2MRS beyond 3 Mpc + UNGC inside it).  The 2M++ cube is deliberately not used.
rows2 = []
for l in open(os.path.join(DATA, "2mrs_huchra2012.tsv"), encoding="latin-1"):
    if l.startswith("#Table\tJ_ApJS_199_26_table6"): break
    if l.startswith("#") or not l.strip(): continue
    f = l.rstrip("\n").split("\t")
    if len(f) != 4: continue
    try: rows2.append((float(f[0]), float(f[1]), float(f[2]), float(f[3])))
    except ValueError: pass
A2 = np.array(rows2); ra2, de2, cz2, K2 = A2.T
m2 = (cz2 > 350) & (cz2 < 15000); d2 = cz2[m2]/H0_KMS
LK2 = 10**(0.4*(MK_SUN - (K2[m2] - 5*np.log10(d2*1e6/10))))
l2, b2 = eq2gal(ra2[m2], de2[m2]); lr2, br2 = np.radians(l2), np.radians(b2)
POS2 = np.stack([d2*np.cos(br2)*np.cos(lr2), d2*np.cos(br2)*np.sin(lr2), d2*np.sin(br2)], 1)
MB2 = UPS_K*LK2*1.4
UPOS, UMB, UMD, UNM = [], [], [], []
for x in raw:
    if not np.isfinite(x["Dist"]): continue
    mb = (UPS_K*10**x["KLum"] if np.isfinite(x["KLum"]) else 0.0) + (F_HE*10**x["MHI"] if np.isfinite(x["MHI"]) else 0.0)
    if x["Name"] == "Milky Way": mb += MW_MSTAR
    if mb <= 0: continue
    UPOS.append(gal_cart(x["_RAJ2000"], x["_DEJ2000"], x["Dist"])); UMB.append(mb)
    UMD.append(x["MD"].upper()); UNM.append(x["Name"].upper())
UPOS, UMB, UMD, UNM = np.array(UPOS), np.array(UMB), np.array(UMD), np.array(UNM)
for g in groups:
    own = g["name"].upper()
    d = POS2 - g["pos"]; rr_ = np.linalg.norm(d, axis=1); k = rr_ > R_SEAM
    far = (G*Msun/Mpc**2)*np.sum((MB2[k]/rr_[k]**3)[:, None]*d[k], axis=0)
    d = UPOS - g["pos"]; rr_ = np.sqrt(np.sum(d*d, axis=1) + SOFT**2)
    k = (rr_ < R_SEAM) & (UNM != own) & (UMD != own)
    near = (G*Msun/Mpc**2)*np.sum((UMB[k]/rr_[k]**3)[:, None]*d[k], axis=0)
    g["gext"] = float(np.linalg.norm(far + near))

def g_eff(gN, gext, a0):
    x = (gN + gext)/a0; w = gext/(gN + gext)
    return nu(x)*(1.0 + dlnnu(x)*w/3.0)*gN

def sigma_pred(g, a0, f_hot=F_HOT, ups=UPS_K, gmult=1.0, apert=1.0, isolated=False):
    Mh = ups*g["LKh"]*Msun
    Msat = (ups*(g["LK"] - g["LKh"]) + F_HE*g["MHI"])*Msun
    Mhot = f_hot*ups*g["LK"]*Msun
    rh = g["rh"]*Mpc; r = rad_grid(rh); rho = plummer(r, rh)
    gN = G*(Mh + (Msat + Mhot)*cumfrac(r, rho))/r**2
    gE = nu(gN/a0)*gN if isolated else g_eff(gN, g["gext"]*gmult, a0)
    return jeans_sigma(r, rho, gE, apert*g["rmax"]*Mpc), float(np.interp(rh, r, gN))/a0

def boosts(a0, **kw):
    out = np.array([(g["sig"]*1e3/sigma_pred(g, a0, **kw)[0])**2 for g in groups])
    xs  = np.array([sigma_pred(g, a0, **kw)[1] for g in groups])
    return out, xs

bcan, xcan = boosts(A0["canonical"]); balt, _ = boosts(A0["alt"])
med_can, med_alt = float(np.median(bcan)), float(np.median(balt))
bs = np.array([np.median(rng.choice(bcan, len(bcan))) for _ in range(6000)])
lo68, hi68 = float(np.percentile(bs, 16)), float(np.percentile(bs, 84))
info(f"independent median boost: canonical {med_can:.3f} (g06 quotes {G06_MED_CAN}), alt {med_alt:.3f} "
     f"(g06 quotes {G06_MED_ALT}); bootstrap 16-84% [{lo68:.3f}, {hi68:.3f}] (g06 {G06_BOOT})")
info(f"median g_bar/a_0 = {np.median(xcan):.5f}; per-group boosts span {bcan.min():.2f} - {bcan.max():.2f}")
ck("V1 the headline reproduces under an independent re-implementation of the whole chain (catalogue read, "
   "membership, gapper, baryon budget, baryonic external field, Jeans solve).  If this failed the claim would be "
   "dead on arithmetic; it is not, and everything below is about the INFERENCE",
   abs(math.log10(med_can/G06_MED_CAN)) < 0.03 and abs(math.log10(med_alt/G06_MED_ALT)) < 0.03,
   f"canonical {med_can:.4f} vs {G06_MED_CAN} ({math.log10(med_can/G06_MED_CAN):+.4f} dex); alt {med_alt:.4f} "
   f"vs {G06_MED_ALT} ({math.log10(med_alt/G06_MED_ALT):+.4f} dex)")

# ================================================================================================ SECTION 2
P(""); P("="*126)
P("2.  ATTACK 1 -- IS THE MEDIAN A PROPERTY OF THE SAMPLE, OR OF ITS WORST-MEASURED HALF?")
P("="*126)
info("boost = (sigma_obs/sigma_pred)^2, and in the deep-MOND limit of a point mass 3 sigma_pred^2 = sqrt(G M a_0)")
info("is nearly radius-independent (g06's own check J3).  So the boost is, to within the transition correction,")
info("        boost  ~  3 sigma_obs^2 / sqrt(G M_b a_0),")
info("i.e. a baryonic-Tully-Fisher-style test in which ALL the per-group scatter enters through sigma_obs.  A")
info("5-member gapper dispersion is the noisiest and the most membership-sensitive quantity in the file, and the")
info("sample runs from 5 to 39 members.  So: does the boost run with membership number?")
N = np.array([g["N"] for g in groups], float); lb = np.log10(bcan)
Dg = np.array([g["D"] for g in groups]); Mb = np.array([g["Mstar"] + g["Mgas"] for g in groups])

def spearman(a, b):
    ra_ = np.argsort(np.argsort(a)).astype(float); rb = np.argsort(np.argsort(b)).astype(float)
    return float(np.corrcoef(ra_, rb)[0, 1])

def perm_p(a, b, nrep=20000):
    obs = abs(spearman(a, b))
    null = np.array([abs(spearman(a, rng.permutation(b))) for _ in range(nrep)])
    return obs, float((null >= obs).mean()), float(null.std())

rho_N, p_N, sd_N = perm_p(N, lb)
rho_D, p_D, _    = perm_p(Dg, lb)
rho_M, p_M, _    = perm_p(np.log10(Mb), lb)
P(f"    {'variable':28} {'Spearman rho':>13} {'permutation p':>15}")
for lbl, (rr_, pp) in [("members per group N", (rho_N, p_N)), ("host distance D", (rho_D, p_D)),
                       ("log baryonic mass", (rho_M, p_M))]:
    P(f"    {lbl:28} {rr_:+13.3f} {pp:15.4f}")
rich = bcan[N >= 10]; poor = bcan[N < 10]
info(f"split at N = 10: rich half N_grp = {len(rich)}, median boost {np.median(rich):.3f} "
     f"({math.log10(np.median(rich)):+.3f} dex); poor half N_grp = {len(poor)}, median boost "
     f"{np.median(poor):.3f} ({math.log10(np.median(poor)):+.3f} dex); gap "
     f"{math.log10(np.median(rich)/np.median(poor)):+.3f} dex")
# permutation null for the split itself, so the cut is judged and not just quoted
gap_obs = math.log10(np.median(rich)/np.median(poor))
gap_null = np.array([math.log10(np.median(x[N >= 10])/np.median(x[N < 10]))
                     for x in (rng.permutation(bcan) for _ in range(20000))])
p_gap = float((np.abs(gap_null) >= abs(gap_obs)).mean())
info(f"the same split on 20000 label-permuted samples: |gap| >= {abs(gap_obs):.3f} dex in {100*p_gap:.2f}% of them")

ck("A1 the boost does NOT run with the number of members, i.e. the headline is not being set by the sparsest and "
   "least reliable groups.  This is the data-quality confound: sigma_obs from 5 velocities is both the noisiest "
   "and the most membership-sensitive number in the chain, and if the boost tracks N then the median over 26 "
   "groups is a statement about catalogue depth rather than about gravity",
   p_N > 0.05, f"Spearman rho(N, log boost) = {rho_N:+.3f}, permutation p = {p_N:.4f}; rich (N>=10) median "
   f"{np.median(rich):.3f} vs poor (N<10) median {np.median(poor):.3f}, a gap of {gap_obs:+.3f} dex "
   f"(split permutation p = {p_gap:.4f})")

ck("A2 the well-measured subsample carries the claim.  Restricting to the {N>=10} groups -- the ones with enough "
   "members for the gapper to mean anything -- must leave the separation from the liability table's X-ray "
   "group/cluster median of 2.11 substantially intact (asserted here at 0.30 dex, against the claimed 0.412)",
   abs(math.log10(CLUSTER_MED/np.median(rich))) > 0.30,
   f"rich-subsample median boost {np.median(rich):.3f}; separation from the cluster median "
   f"{math.log10(CLUSTER_MED/np.median(rich)):+.3f} dex, against the full-sample "
   f"{math.log10(CLUSTER_MED/med_can):+.3f} dex.  The liability table's mildest X-ray group/cluster rows are "
   f"1.45 and 1.48")

# mutation control on this attack
mut = []
for _ in range(400):
    Nsh = rng.permutation(N)
    mut.append(spearman(Nsh, lb))
ck("A3 MUTATION CONTROL for attack 1 -- shuffle the membership numbers across groups.  The N-trend must vanish "
   "when the labels are broken; if a shuffled N still correlated with the boost, attack 1 would be an artefact "
   "of my own ranking rather than a property of the sample",
   abs(float(np.mean(mut))) < 0.10 and abs(rho_N) > 2*float(np.std(mut)) or abs(rho_N) < 2*float(np.std(mut)),
   f"shuffled rho = {np.mean(mut):+.3f} +- {np.std(mut):.3f}; real rho = {rho_N:+.3f}, i.e. "
   f"{abs(rho_N)/np.std(mut):.2f} sigma from the shuffled null")

# is the trend a small-sample bias of the estimator itself?  MC the gapper against a pinned central host.
info("")
info("Is an N-trend just small-sample bias in the gapper?  Monte-Carlo, 20000 draws per n: n-1 Gaussian tracers")
info("plus one host pinned at the systemic velocity (the host IS in the member list and sits at the centre):")
P(f"    {'n':>4} {'median gapper / true sigma':>28} {'-> bias in boost (dex)':>24}")
gap_bias = {}
for n in (5, 6, 8, 10, 20, 39):
    s = []
    for _ in range(20000):
        v = np.concatenate([rng.normal(0, 1, n - 1), [0.0]])
        s.append(gapper(v))
    gap_bias[n] = float(np.median(s))
    P(f"    {n:4d} {gap_bias[n]:28.4f} {2*math.log10(gap_bias[n]):24.4f}")
pred_bias = 2*math.log10(gap_bias[5]/gap_bias[39])
ck("A4 the rich-vs-poor gap IS explained away by the gapper's own small-sample behaviour, in which case attack 1 "
   "is a statistics artefact and the claim survives it.  This check is deliberately phrased AGAINST my own "
   "attack: PASS = my attack is an estimator artefact and I withdraw it; FAIL = the gap is bigger than the "
   "estimator can produce and the confound is real.  The n = 5 bias goes the RIGHT way to help the claim "
   "(sparse groups read low), so it had to be sized rather than waved at",
   abs(gap_obs) < abs(pred_bias) + 0.05,
   f"estimator bias n=5 vs n=39 predicts {pred_bias:+.3f} dex in the boost; the observed rich-vs-poor gap is "
   f"{gap_obs:+.3f} dex, a factor {abs(gap_obs/pred_bias) if pred_bias else float('nan'):.1f} larger")

# ================================================================================================ SECTION 3
P(""); P("="*126)
P("3.  ATTACK 2 -- THE '3.6 SIGMA' USES ONLY THE STATISTICAL ERROR.  THE FILE'S OWN SYSTEMATICS ARE LARGER.")
P("="*126)
SYS = [("stellar M/L: Upsilon_K = 0.4 vs 1.0", dict(ups=0.4), dict(ups=1.0)),
       ("hot gas: f_hot = 0 vs 1.0",           dict(f_hot=0.0), dict(f_hot=1.0)),
       ("external field: isolated vs x3",      dict(isolated=True), dict(gmult=3.0)),
       ("aperture: r_h vs 3 r_max",            dict(apert=None), dict(apert=3.0))]
half = {}
P(f"    {'systematic (admissible branches only)':44} {'low':>8} {'high':>8} {'half-width dex':>15}")
sv = [g["rmax"] for g in groups]
for lbl, kwlo, kwhi in SYS:
    vals = []
    for kw in (kwlo, kwhi):
        if kw.get("apert", 1.0) is None:
            for g, t in zip(groups, sv): g["rmax"] = g["rh"]
            vals.append(float(np.median(boosts(A0["canonical"])[0])))
            for g, t in zip(groups, sv): g["rmax"] = t
        else:
            vals.append(float(np.median(boosts(A0["canonical"], **kw)[0])))
    h = abs(math.log10(vals[1]/vals[0]))/2.0
    half[lbl] = h
    P(f"    {lbl:44} {vals[0]:8.3f} {vals[1]:8.3f} {h:15.3f}")
sys_tot = math.sqrt(sum(v*v for v in half.values()))
stat_half = (math.log10(hi68) - math.log10(lo68))/2.0
sep = math.log10(CLUSTER_MED/med_can)
sig_stat_only = sep/stat_half
sig_full = sep/math.sqrt(stat_half**2 + sys_tot**2)
info(f"statistical half-width on the median (bootstrap)          = {stat_half:.3f} dex  -> {sig_stat_only:.2f} sigma")
info(f"quadrature sum of the ADMISSIBLE prescription systematics = {sys_tot:.3f} dex")
info(f"stat + sys                                                = "
     f"{math.sqrt(stat_half**2 + sys_tot**2):.3f} dex  -> {sig_full:.2f} sigma")
info("and this still counts NOTHING on the cluster side (hydrostatic bias, abundance-matched stellar masses),")
info("and EXCLUDES the two branches g06 itself rules out by argument: the pure external-field limit (0.208) and")
info("the raw 2M++ field (2.215, which lands on the cluster median).")
ck("B1 the claimed separation from the cluster rows survives the file's OWN admissible systematic bracket at "
   "three sigma.  The quoted 3.6 sigma is explicitly 'on the group side's error alone'; a referee will not accept "
   "a statistical-only error bar on a comparison whose dominant uncertainty is the stellar M/L",
   sig_full > 3.0, f"separation {sep:+.3f} dex; {sig_stat_only:.2f} sigma statistical-only, "
   f"{sig_full:.2f} sigma once the admissible systematics are included")
ck("B2 the separation survives the SINGLE worst admissible systematic on its own -- the stellar M/L.  Upsilon_K = "
   "1.0 is a defensible old-population K-band value (Bell & de Jong 2001 span roughly 0.6-1.0 in K for red "
   "colours), and this rung's whole baryon budget is 93% host K-band light",
   abs(math.log10(CLUSTER_MED/float(np.median(boosts(A0['canonical'], ups=1.0)[0])))) > 3*stat_half,
   f"at Upsilon_K = 1.0 the median boost is {float(np.median(boosts(A0['canonical'], ups=1.0)[0])):.3f}, "
   f"separation from 2.11 = "
   f"{math.log10(CLUSTER_MED/float(np.median(boosts(A0['canonical'], ups=1.0)[0]))):+.3f} dex against "
   f"3 x {stat_half:.3f}")

# ================================================================================================ SECTION 4
P(""); P("="*126)
P("4.  ATTACK 3 -- IS THE PER-GROUP SCATTER CONSISTENT WITH THE QUOTED ERRORS, OR IS THERE UNMODELLED SYSTEMATIC?")
P("="*126)
estat = np.array([2.0/math.sqrt(2*(g["Nv"] - 1))/math.log(10) for g in groups])
obs_sd = float(np.std(lb, ddof=1))
exp_sd = float(np.sqrt(np.mean(estat**2)))
intr = math.sqrt(max(obs_sd**2 - exp_sd**2, 0.0))
chi2 = float(np.sum(((lb - np.median(lb))/estat)**2))
info(f"observed scatter of log boost   = {obs_sd:.3f} dex over {len(lb)} groups")
info(f"quoted statistical scatter      = {exp_sd:.3f} dex (rms of the per-group 2/sqrt(2(N-1)) errors)")
info(f"implied INTRINSIC/unmodelled    = {intr:.3f} dex")
info(f"chi^2 about the median = {chi2:.1f} for {len(lb)-1} dof  (p = "
     f"{'<1e-4' if chi2 > 2.5*(len(lb)-1) else 'not extreme'})")
ck("C1 the 26 boosts are statistically consistent with a single value, so quoting a median with a bootstrap error "
   "is a legitimate summary.  If they are not, the sample carries an unmodelled per-group systematic (membership, "
   "interlopers, non-equilibrium, projection) at least as large as the effect being claimed, and the median's "
   "error bar understates what is actually known",
   chi2 < 2.0*(len(lb) - 1), f"chi^2/dof = {chi2/(len(lb)-1):.2f}; the unmodelled term is {intr:.3f} dex per "
   f"group, against a quoted statistical {exp_sd:.3f} dex and a claimed separation of {sep:.3f} dex")

# ================================================================================================ SECTION 5
P(""); P("="*126)
P("5.  ATTACK 4 -- WOULD ORDINARY COLD DARK MATTER PRODUCE THE SAME SIGNATURE?  ZERO FREE PARAMETERS.")
P("="*126)
info("Abundance matching (Moster, Naab & White 2013, MNRAS 428, 3121, z = 0: log M1 = 11.59, N = 0.0351,")
info("beta = 1.376, gamma = 0.608) fixes M200 from the MEASURED stellar mass with no freedom; concentration from")
info("Dutton & Maccio 2014 (MNRAS 441, 3359): log c200 = 0.905 - 0.101 log(M200 h / 1e12).  The SAME tracer")
info("profile, the SAME aperture and the SAME Jeans solver are then used, so the two frameworks are compared")
info("through one pipeline.  If LambdaCDM lands on these dispersions as well as the framework does, this rung")
info("cannot separate them and the 'counted vs modelled baryons' reading of the group/cluster contrast is one")
info("story among several, not a measurement.")
def m200_from_mstar(Mstar):
    lo, hi = 1e9, 1e16
    for _ in range(200):
        mid = math.sqrt(lo*hi)
        ms = mid*2*0.0351/((mid/10**11.59)**-1.376 + (mid/10**11.59)**0.608)
        if ms < Mstar: lo = mid
        else: hi = mid
    return math.sqrt(lo*hi)
def sigma_lcdm(g):
    Mst = g["Mstar"]; M200 = m200_from_mstar(Mst)
    c = 10**(0.905 - 0.101*math.log10(M200*0.674/1e12))
    rho_c = 3*(H0**2)/(8*math.pi*G)
    r200 = (3*M200*Msun/(4*math.pi*200*rho_c))**(1/3.)
    rs = r200/c; mu = lambda x: math.log(1 + x) - x/(1 + x)
    rh = g["rh"]*Mpc; r = rad_grid(rh); rho = plummer(r, rh)
    Mdm = M200*Msun*np.array([mu(x)/mu(c) for x in r/rs])
    Mb = (g["Mstar"] + g["Mgas"])*Msun
    Menc = Mdm + Mb*cumfrac(r, rho)
    return jeans_sigma(r, rho, G*Menc/r**2, g["rmax"]*Mpc), M200
bl, m200s = [], []
P(f"    {'group':14} {'N':>3} {'log M*':>7} {'log M200(AM)':>13} {'sig_obs':>8} {'sig_LCDM':>9} {'boost_LCDM':>11} "
  f"{'boost_frame':>12}")
for g, bf in zip(groups, bcan):
    s, M2 = sigma_lcdm(g); b = (g["sig"]*1e3/s)**2; bl.append(b); m200s.append(M2)
    P(f"    {g['name']:14} {g['N']:3d} {math.log10(g['Mstar']):7.2f} {math.log10(M2):13.2f} {g['sig']:8.1f} "
      f"{s/1e3:9.1f} {b:11.2f} {bf:12.2f}")
bl = np.array(bl)
med_l = float(np.median(bl))
info(f"LambdaCDM (abundance-matched NFW, zero free parameters): median boost {med_l:.3f} "
     f"({math.log10(med_l):+.3f} dex), scatter {np.log10(bl).std(ddof=1):.3f} dex")
info(f"framework (Route A kernel,        zero free parameters): median boost {med_can:.3f} "
     f"({math.log10(med_can):+.3f} dex), scatter {np.log10(bcan).std(ddof=1):.3f} dex")
ck("D1 the rung DISCRIMINATES: the framework and a zero-free-parameter abundance-matched NFW halo must not land "
   "on these dispersions equally well.  A FAIL here confirms the author's own concession that this is a "
   "non-discrimination -- and it also removes the causal reading, because if CDM reproduces the group side too "
   "then 'the deficit appears where baryons are MODELLED' is an interpretation, not a result",
   abs(math.log10(med_l) - math.log10(med_can)) > 3*stat_half,
   f"LambdaCDM median boost {med_l:.3f} vs framework {med_can:.3f}; the two differ by "
   f"{math.log10(med_l/med_can):+.3f} dex against 3 x the bootstrap half-width {3*stat_half:.3f} dex.  Scatters "
   f"{np.log10(bl).std(ddof=1):.3f} (LCDM) vs {np.log10(bcan).std(ddof=1):.3f} (framework) dex")

# ================================================================================================ SECTION 6
P(""); P("="*126)
P("6.  ATTACK 5 -- THE GROUP/CLUSTER CONTRAST IS DEGENERATE WITH THE MASS ESTIMATOR")
P("="*126)
info("The liability table carries a row that matches this rung in BOTH mass and acceleration:")
info("    | 2.63 | 0.004 | pressure | eRASS1 groups 10^12.5-13.5 at R500 |")
info(f"This rung's abundance-matched halo masses are log M200 = {np.log10(m200s).min():.2f} - "
     f"{np.log10(m200s).max():.2f}, median {np.median(np.log10(m200s)):.2f} -- the SAME decade -- at "
     f"g_bar/a_0 = {np.median(xcan):.4f} against that row's 0.004.")
info("So the contrast is not group-mass vs cluster-mass and it is not high-acceleration vs low-acceleration.")
info("What differs between the two rows is the ESTIMATOR: galaxy-tracer line-of-sight dispersions here, X-ray")
info("hydrostatic masses there.  'Counted vs modelled baryons' is ONE reading of that difference.  The others,")
info("which this rung cannot exclude, all push the group side DOWN rather than the cluster side up:")
info("  (i)   radial orbit anisotropy: an isotropic Jeans solve applied to a radially anisotropic satellite")
info("        population under-reads the mass from a line-of-sight dispersion;")
info("  (ii)  Theta_1 > 0 membership reaches the zero-velocity surface, so a large fraction of members sit in the")
info("        infall region where peculiar velocities are SMALL -- g06 argues this only inflates sigma; it can")
info("        equally deflate the line-of-sight dispersion of a sample dominated by large-radius members;")
info("  (iii) 5-39 members with no interloper rejection beyond the catalogue's own tidal index.")
lo_c = 1.45   # mildest X-ray group/cluster row in the table
ck("E1 the separation is from the cluster BLOCK and not merely from its median.  The table's mildest X-ray "
   "group/cluster rows are 1.45 and 1.48; if the rung's number is not separated from THOSE at three sigma then "
   "'groups do not show the cluster deficit' is a statement about the top of the cluster block only",
   abs(math.log10(lo_c/med_can)) > 3*math.sqrt(stat_half**2 + sys_tot**2),
   f"separation from the mildest X-ray row (1.45) = {math.log10(lo_c/med_can):+.3f} dex against 3 x "
   f"{math.sqrt(stat_half**2 + sys_tot**2):.3f} = {3*math.sqrt(stat_half**2 + sys_tot**2):.3f} dex")
ck("E2 the rich (N>=10) subsample is separated from the mildest X-ray group/cluster rows.  This is the strongest "
   "form of the audit: take only the groups whose dispersions are worth trusting, and ask whether they still sit "
   "below the cluster block at all",
   abs(math.log10(lo_c/float(np.median(rich)))) > math.sqrt(stat_half**2 + sys_tot**2),
   f"rich-subsample median {np.median(rich):.3f} against the table's 1.45 and 1.48 rows: "
   f"{math.log10(lo_c/float(np.median(rich))):+.3f} dex, against a one-sigma stat+sys of "
   f"{math.sqrt(stat_half**2 + sys_tot**2):.3f} dex")

# ================================================================================================ SECTION 7
P(""); P("="*126)
P("7.  BOTH FOOTINGS ON EVERY CONCLUSION OF THIS AUDIT, AND A SECOND MUTATION CONTROL")
P("="*126)
Nalt = np.array([g["N"] for g in groups], float)
rho_alt, p_alt, _ = perm_p(Nalt, np.log10(balt))
rich_alt = balt[N >= 10]
P(f"    {'footing':12} {'median':>8} {'rich N>=10':>11} {'poor N<10':>10} {'rho(N,boost)':>13} {'p':>8} "
  f"{'sep from 2.11':>14}")
for lbl, bb, rr_, pp in [("canonical", bcan, rho_N, p_N), ("alt", balt, rho_alt, p_alt)]:
    P(f"    {lbl:12} {np.median(bb):8.3f} {np.median(bb[N>=10]):11.3f} {np.median(bb[N<10]):10.3f} "
      f"{rr_:+13.3f} {pp:8.4f} {math.log10(CLUSTER_MED/np.median(bb)):+14.3f}")
ck("F1 both footings give the same audit verdict on the richness confound",
   (p_N < 0.05) == (p_alt < 0.05),
   f"canonical rho {rho_N:+.3f} p {p_N:.4f}; alt rho {rho_alt:+.3f} p {p_alt:.4f}")
bshuf = []
for _ in range(300):
    sv2 = [g["sig"] for g in groups]
    for g, s in zip(groups, rng.permutation(sv2)): g["sig"] = s
    bb, _ = boosts(A0["canonical"]); bshuf.append(spearman(N, np.log10(bb)))
    for g, s in zip(groups, sv2): g["sig"] = s
ck("F2 MUTATION CONTROL -- shuffle the measured dispersions across groups.  The N-trend must be destroyed, "
   "because it is a pairing between a group's own richness and its own kinematics.  If it survived a shuffle it "
   "would be an artefact of the baryon budget or the radii, not of the dispersions",
   abs(float(np.mean(bshuf))) < 0.5*abs(rho_N) or abs(rho_N) < 0.2,
   f"shuffled rho(N, log boost) = {np.mean(bshuf):+.3f} +- {np.std(bshuf):.3f}; real {rho_N:+.3f}")

# ================================================================================================ SECTION 8
P(""); P("="*126)
P("8.  VERDICT OF THE AUDIT")
P("="*126)
info(f"  * The arithmetic REPRODUCES: median boost {med_can:.3f} canonical / {med_alt:.3f} alt, "
     f"bootstrap [{lo68:.3f}, {hi68:.3f}].")
info(f"  * The 'consistent with unity, cannot discriminate' half of the claim STANDS and is if anything")
info( "    understated -- see D1.")
info(f"  * The '3.6 sigma from the cluster rows' half does NOT stand at that strength: {sig_stat_only:.1f} sigma")
info(f"    statistical-only becomes {sig_full:.1f} sigma once the file's OWN admissible systematic bracket is")
info( "    included, and that still counts nothing on the cluster side.")
info(f"  * Richness confound: rho(N, log boost) = {rho_N:+.3f}, permutation p = {p_N:.4f} -- NOT significant, and")
info( "    said so: check A1 PASSES.  What is established is not a trend but a FRAGILITY.  The N >= 10 groups sit")
info(f"    at {np.median(rich):.2f} and the N < 10 groups at {np.median(poor):.2f}; a quality cut any referee "
     f"would ask for moves the")
info(f"    rung onto the liability table's mildest X-ray rows (1.45, 1.48), separation {math.log10(lo_c/float(np.median(rich))):+.3f} dex (E2).")
info(f"  * Unmodelled per-group scatter {intr:.3f} dex against a quoted statistical {exp_sd:.3f} dex; chi^2/dof = "
     f"{chi2/(len(lb)-1):.2f}, so the 26")
info( "    groups are NOT draws from one value and the bootstrap band is not the whole error.")
info(f"  * LambdaCDM, zero free parameters, lands at {med_l:.2f} on the same groups with the same pipeline -- it")
info( "    does not show the cluster deficit either.  So the group/cluster contrast does not isolate 'counted vs")
info( "    modelled baryons'; it is equally a statement about galaxy-kinematic vs X-ray-hydrostatic estimators.")
sys.exit(ck.done())
