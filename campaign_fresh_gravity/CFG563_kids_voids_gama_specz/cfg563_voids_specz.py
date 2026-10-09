#!/usr/bin/env python3
"""CFG563 -- CFG561's VOID LENSING TEST REDONE WITH GAMA SPECTROSCOPIC REDSHIFTS AND A GAMA ENVIRONMENT CATALOGUE.
Settling predicts LOWER outer lensing for void lenses; a law-as-force without EFE (foil) HIGHER; LCDM a small difference at fixed
M* (|D| < ~0.1 dex) but also a lower 2-halo term around void galaxies.  Pure data; a0 footings (9.3603e-11 / 1.1312e-10, kappa = 1/2
FITTED) irrelevant.  Criteria frozen and committed before this script: FROZEN_CRITERIA.md (7f876f805).
  data   cfg110_perlens.npz, lr_lenses.npz, lr_esd_jackknife.npz; GAMA DR4 G3CGalv10 (CFG471, read only), Eardley+2015
         GalaxiesClassifiedv01, Alpaslan+2014 Fil/Tendril/VoidGals v02 (Data Central TAP).
  set    GAMA boxes, nearest G3CGal galaxy within 1.5", |z_spec - z_phot| < 0.1(1+z_spec), Eardley class with NQ > 2.
         VOID GeoS4 = 0, OUTSIDE GeoS4 in {1,2,3}; OUTSIDE reweighted to VOID's (logM*, z_spec, colour) histogram.
  stat   D_K = log10[ESD_V / ESD_O] pooled over K (KO = bins 0-7 headline, K1 = 8-14); June-patch jackknife.
MUTATE=1: the VOID/OUTSIDE flag shuffled among analysis-set lenses (seed 563); the tracer C3 must FAIL -> rc 1.
Run: python3 campaign_fresh_gravity/CFG563_kids_voids_gama_specz/cfg563_voids_specz.py   (MUTATE=1 for the control)
"""
import os, sys, json, hashlib
import numpy as np
import pandas as pd
from astropy.cosmology import FlatLambdaCDM
from scipy.spatial import cKDTree
from scipy.stats import chi2 as CHI2, norm

HERE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(HERE)
sys.path.insert(0, CFG)
import CFG7_common as C

MUTATE = os.environ.get("MUTATE", "0") == "1"
R = C.Report("cfg563_voids_specz", MUTATE)
P, check = R.P, R.check
P(__doc__.split("Run: python3")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: VOID/OUTSIDE flag shuffled among analysis-set lenses -- the tracer C3 must FAIL ***")

# ================================================================== inputs + hashes
EXT = os.path.join(CFG, "_external_data")
FILES = {os.path.join(EXT, "cfg471", "G3CGalv10.csv"): "051950e193e447ebf8bf7a9458c3ffe4ea368596b8042732ee933fc95f6ad9f8",
         os.path.join(EXT, "cfg563", "GalaxiesClassifiedv01.csv"): "95d9e2a17d788022f502191583f30582a22fe20e65b0247fe64492a6b8bea7b9",
         os.path.join(HERE, "data", "VoidGalsv02.csv"): "d9b788fe208dd91c3e75a1266e816140f9a136d5ef19adb64909f2b6e31a88f8",
         os.path.join(HERE, "data", "TendrilGalsv02.csv"): "77855fc6e98a88bdc99d4f7ea48c121e302093a048a753515edaeb51736331de",
         os.path.join(HERE, "data", "FilGalsv02.csv"): "c26715bb44f1b8988d40372c279d17b9cfb6e8a07b5627f882b31f32d5967635"}
for f, h in FILES.items():
    if hashlib.sha256(open(f, "rb").read()).hexdigest() != h:
        sys.exit(f"sha256 mismatch: {os.path.basename(f)} -- refusing to run")
P("  all five input tables match their logged sha256")

LR = os.path.join(C.REPO, "real_research", "data", "lensing_rar")
PL = np.load(os.path.join(LR, "cfg110_perlens.npz"))
LN = np.load(os.path.join(LR, "lr_lenses.npz"))
J = np.load(os.path.join(LR, "lr_esd_jackknife.npz"))
KG = 1.989e30 / (3.0857e16) ** 2
K1 = list(range(8, 15)); KO = list(range(8))
NPAT = 50
HART = (NPAT - 7 - 2) / (NPAT - 1)
WG = PL["WG"].astype(float); WW = PL["WW"].astype(float)
typ, zl, lml, ra, dec = LN["typ"], LN["z"], LN["logM"], LN["ra"], LN["dec"]
patch = J["patch"]
NL = len(zl)
EARLY, LATE = typ == 1, typ == 0

# ================================================================== C1a (copied from CFG561)
R.banner("C1a CONTROL: CFG88's full-sample K1 split from the per-lens sums (CFG561 C1)")
WGk, WWk = WG[:, K1], WW[:, K1]


def esd_loo(mask):
    g = WGk[mask]; v = WWk[mask]; pa_ = patch[mask]
    tg, tw = g.sum(0), v.sum(0)
    Sg = np.zeros((NPAT, 7)); Sw = np.zeros((NPAT, 7))
    np.add.at(Sg, pa_, g); np.add.at(Sw, pa_, v)
    return tg / tw / KG, (tg[None] - Sg) / (tw[None] - Sw) / KG


eL, lL = esd_loo(LATE); eE, lE = esd_loo(EARLY)
Dfull, Lfull = eE - eL, lE - lL
Rr = Lfull - Lfull.mean(0)
Ci = np.linalg.inv((NPAT - 1) / NPAT * (Rr.T @ Rr))
x2full = float(Dfull @ Ci @ Dfull) * HART
c88 = json.load(open(os.path.join(CFG, "CFG88_kids_split_jackknife_results.json")))["numbers"]
dD = float(np.max(np.abs(Dfull / np.array(c88["D"]) - 1)))
check("C1a CONTROL: D_full equals CFG88's K1 D (1e-6 rel) and the zero-model Hartlap chi2 equals CFG88's 35.0418 (1e-6 rel)",
      f"max rel dev {dD:.1e}; chi2 {x2full:.4f}/7 vs {c88['chi2']['L']:.4f} (p {CHI2.sf(x2full, 7):.2e})",
      dD < 1e-6 and abs(x2full / c88["chi2"]["L"] - 1) < 1e-6)

# ================================================================== footprint, cross-match (CFG471's)
R.banner("FOOTPRINT AND CROSS-MATCH (CFG471's boxes and 1.5\" radius)")
g = pd.read_csv(list(FILES)[0])
E = pd.read_csv(list(FILES)[1])
box = np.zeros(NL, bool)
for a, b, c, d in ((129, 141, -2, 3), (174, 186, -3, 2), (211.5, 223.5, -2, 3)):
    box |= (ra > a) & (ra < b) & (dec > c) & (dec < d)


def uv(a, d):
    a, d = np.radians(a), np.radians(d)
    return np.c_[np.cos(d) * np.cos(a), np.cos(d) * np.sin(a), np.sin(d)]


gtree = cKDTree(uv(g.RA.values, g.Dec.values))
dd, ii = gtree.query(uv(ra, dec))
sep = np.degrees(2 * np.arcsin(dd / 2)) * 3600
mt = box & (sep < 1.5)
dd2, _ = gtree.query(uv(ra, np.clip(dec + 60 / 3600, -90, 90)))
chance = float(np.sum(box & (np.degrees(2 * np.arcsin(dd2 / 2)) * 3600 < 1.5)) / max(mt.sum(), 1))
check("C2 CONTROL: chance-match rate (positions shifted +60\" in Dec) < 2% of the real match rate", f"{chance * 100:.3f}%", chance < 0.02)
zs = g.Z.values[ii]; cat = g.CATAID.values[ii]
okz = np.abs(zs - zl) < 0.1 * (1 + zs)
emap4 = dict(zip(E.CATAID, E.GeoS4)); emap10 = dict(zip(E.CATAID, E.GeoS10)); enq = dict(zip(E.CATAID, E.NQ))
geo4 = np.array([emap4.get(c, -1) for c in cat]); geo10 = np.array([emap10.get(c, -1) for c in cat])
nq = np.array([enq.get(c, 0) for c in cat])
ASET = mt & okz & (geo4 >= 0) & (nq > 2)
P(f"  footprint lenses {int(box.sum()):,}; matched {int(mt.sum()):,}; catastrophic photo-z dropped {int((mt & ~okz).sum()):,}; "
  f"with an Eardley class (NQ>2): {int(ASET.sum()):,}")
ia = np.where(ASET)[0]
ZS = zs[ia]
P(f"  analysis set {ia.size:,}: GeoS4 void {int(np.sum(geo4[ia] == 0)):,}, sheet {int(np.sum(geo4[ia] == 1)):,}, "
  f"filament {int(np.sum(geo4[ia] == 2)):,}, knot {int(np.sum(geo4[ia] == 3)):,}; z_spec {ZS.min():.3f}-{ZS.max():.3f} (median {np.median(ZS):.3f})")
alp = {}
for nm, f in (("void", "VoidGalsv02"), ("tendril", "TendrilGalsv02"), ("filament", "FilGalsv02")):
    alp[nm] = np.isin(cat[ia], pd.read_csv(os.path.join(HERE, "data", f + ".csv")).CATAID.values)
P(f"  Alpaslan classes in the analysis set: void {int(alp['void'].sum())}, tendril {int(alp['tendril'].sum())}, filament {int(alp['filament'].sum())}")

# ================================================================== jackknife regions
PATS = np.unique(patch[ia]); NP = len(PATS)
pidx = np.full(NPAT, -1); pidx[PATS] = np.arange(NP)
JP = pidx[patch[ia]]
SUB = np.zeros(len(ia), int)
for p in PATS:
    m = patch[ia] == p
    q = np.quantile(ra[ia][m], [1 / 3, 2 / 3])
    SUB[m] = 3 * pidx[p] + np.digitize(ra[ia][m], q)
P(f"  June patches holding analysis-set lenses: {NP} {PATS.tolist()}; sub-patches {len(np.unique(SUB))}")

# ================================================================== C1b footprint early/late
R.banner("C1b CONTROL: the K1 early/late split restricted to the GAMA footprint vs the full sample")


def logratio_jk(mA, mB, reg, nreg, x_num, x_den, wA=None, wB=None):
    wA = np.ones(mA.size) if wA is None else wA
    wB = np.ones(mB.size) if wB is None else wB

    def s(m, w, x):
        t = np.zeros(nreg); np.add.at(t, reg[m], (w * x)[m]); return t
    a, b, c, d = s(mA, wA, x_num), s(mA, wA, x_den), s(mB, wB, x_num), s(mB, wB, x_den)
    full = np.log10(a.sum() / b.sum() / (c.sum() / d.sum()))
    reps = np.log10((a.sum() - a) / (b.sum() - b) / ((c.sum() - c) / (d.sum() - d)))
    used = np.bincount(reg[mA | mB], minlength=nreg) > 0
    n = int(used.sum())
    sig = float(np.sqrt((n - 1) / n * np.sum((reps[used] - reps[used].mean()) ** 2)))
    return float(full), sig


GK1 = WG[:, K1].sum(1); WK1 = WW[:, K1].sum(1)
full_el = float(np.log10(GK1[EARLY].sum() / WK1[EARLY].sum() / (GK1[LATE].sum() / WK1[LATE].sum())))
ib = np.where(box)[0]
bp = pidx.copy(); PB = np.unique(patch[ib]); bp[PB] = np.arange(len(PB))
fp_el, fp_s = logratio_jk(EARLY[ib], LATE[ib], bp[patch[ib]], len(PB), GK1[ib], WK1[ib])
check("C1b CONTROL: footprint K1 early/late pooled log ratio within 3 sigma of the full-sample value",
      f"footprint {fp_el:+.4f} +- {fp_s:.4f} vs full {full_el:+.4f} ({(fp_el - full_el) / fp_s:+.2f} sigma; {len(PB)} patches)",
      abs(fp_el - full_el) < 3 * fp_s)

# ================================================================== C3 tracer: G3CGal neighbours
R.banner("C3 inputs: G3CGal neighbours within 8 Mpc/h comoving projected, |c dz|/(1+z) < 1000 km/s (lens excluded)")
cos = FlatLambdaCDM(H0=100, Om0=0.3089)
zg = np.linspace(0, 1.0, 4001); chig = cos.comoving_distance(zg).value
chi_of = lambda z: np.interp(z, zg, chig)
XL = uv(ra[ia], dec[ia])
theta = 8.0 / chi_of(ZS)
win = 1000.0 / 299792.458 * (1 + ZS)
gz = g.Z.values
NB = np.zeros(len(ia))
lists = gtree.query_ball_point(XL, r=2 * np.sin(theta / 2))
for k, lst in enumerate(lists):
    js = np.asarray(lst, dtype=np.int64)
    NB[k] = np.sum(np.abs(gz[js] - ZS[k]) < win[k]) - 1      # the matched lens itself is inside
assert NB.min() >= 0
P(f"  mean neighbours {NB.mean():.2f} (median {np.median(NB):.0f})")

# ================================================================== machinery
lmc = np.clip(np.digitize(lml[ia], np.arange(8.5, 11.0 + 1e-9, 0.1)) - 1, 0, 24)
zc = np.clip(np.digitize(ZS, np.arange(0.04, 0.265 + 1e-9, 0.025)) - 1, 0, 8)
cell = (lmc * 9 + zc) * 2 + typ[ia]
NC = 25 * 9 * 2
GA = {"K1": WG[ia][:, K1].sum(1), "KO": WG[ia][:, KO].sum(1)}
WA = {"K1": WW[ia][:, K1].sum(1), "KO": WW[ia][:, KO].sum(1)}


def match_w(vm, om):
    nv = np.bincount(cell[vm], minlength=NC).astype(float); no = np.bincount(cell[om], minlength=NC).astype(float)
    ok = no > 0
    w = np.zeros(len(ia)); w[om] = np.where(ok, nv / np.where(ok, no, 1), 0)[cell[om]]
    vkeep = vm & ok[cell]
    return vkeep, w, float(1 - vkeep.sum() / max(vm.sum(), 1))


def run(vflag, oflag, reg=JP, nreg=NP, cls=None):
    base = np.ones(len(ia), bool) if cls is None else cls[ia]
    vm, om = base & vflag, base & oflag
    vkeep, wo, drop = match_w(vm, om)
    out = dict(NV=int(vkeep.sum()), NO=int(om.sum()), drop=drop,
               NOeff=float(wo.sum() ** 2 / (wo ** 2).sum()) if om.any() else 0.0)
    for K in ("KO", "K1"):
        out[K] = logratio_jk(vkeep, om, reg, nreg, GA[K], WA[K], None, wo)
    out["T"] = logratio_jk(vkeep, om, reg, nreg, NB, np.ones(len(ia)), None, wo)
    return out


VF = geo4[ia] == 0
OF = geo4[ia] >= 1
if MUTATE:
    perm = np.random.default_rng(563).permutation(len(ia))
    VF, OF = VF[perm], OF[perm]

# ================================================================== power (C5) before any void number
R.banner("POWER / C5: 100 random analysis-set subsets of the VOID size vs their matched complement")
NVraw = int(VF.sum())
rng = np.random.default_rng(5630)
zz = {"KO": [], "K1": []}; ss = {"KO": [], "K1": []}
for t in range(100):
    pr = np.zeros(len(ia), bool); pr[rng.choice(len(ia), NVraw, replace=False)] = True
    o = run(pr, ~pr)
    for K in ("KO", "K1"):
        zz[K].append(o[K][0] / o[K][1]); ss[K].append(o[K][1])
pw = {}
for K in ("KO", "K1"):
    nnan = int(np.sum(~np.isfinite(zz[K])))   # a pooled ESD <= 0 in a random subset or a jackknife replicate -> log undefined
    sK = float(np.nanmedian(ss[K]))
    pw[K] = dict(sigma=sK, n_nan=nnan, std_z=float(np.nanstd(zz[K])), mean_z=float(np.nanmean(zz[K])),
                 P3sig_0p1dex=float(norm.cdf(0.1 / sK - 3)), P3sig_0p3dex=float(norm.cdf(0.3 / sK - 3)), bound2s=2 * sK)
    P(f"  {K}: N_void {NVraw:,}; expected sigma_D {sK:.4f} dex; null z std {pw[K]['std_z']:.3f} mean {pw[K]['mean_z']:+.3f}; "
      f"P(3 sigma | true 0.1 dex) {pw[K]['P3sig_0p1dex']:.3f}; P(3 sigma | 0.3 dex) {pw[K]['P3sig_0p3dex']:.3f}; "
      f"expected 2-sigma null bound {2 * sK:.3f} dex (NULL needs < 0.1); subsets with an undefined log ratio {nnan}/100")
# FIX after run 1 (disclosed): run 1 read P = NaN (undefined log ratios) as 'powered'; NaN or any undefined subset now counts
# as UNDERPOWERED, the only reading consistent with the frozen rule.  Run 1 is kept as cfg563_voids_specz_RUN1_powerNaN.*
UNDER = not (pw["KO"]["P3sig_0p1dex"] >= 0.5) or pw["KO"]["n_nan"] > 0
P(f"  declared before scoring: {'UNDERPOWERED' if UNDER else 'powered'} for a 0.1 dex outer offset (frozen rule P < 0.5)")
check("C5 (reported): null calibration -- std of D/sigma over 100 random subsets in [0.7, 1.3], KO and K1",
      f"KO {pw['KO']['std_z']:.3f}, K1 {pw['K1']['std_z']:.3f}", all(0.7 <= pw[K]["std_z"] <= 1.3 for K in pw), load_bearing=False)

# ================================================================== the measurement
R.banner("MEASUREMENT: VOID (GeoS4 = 0) vs matched OUTSIDE (GeoS4 = 1, 2, 3)")
M = run(VF, OF)
P(f"  VOID N {M['NV']:,} (dropped for empty cells {M['drop']:.4f}), OUTSIDE N {M['NO']:,} (effective {M['NOeff']:.0f})")
for K in ("KO", "K1"):
    d, s = M[K]
    P(f"  {K}: D = {d:+.4f} +- {s:.4f} dex ({d / s:+.2f} sigma); 2-sigma bound {abs(d) + 2 * s:.3f} dex")
P(f"  tracer T = log10(N_V/N_O) = {M['T'][0]:+.4f} +- {M['T'][1]:.4f} ({M['T'][0] / M['T'][1]:+.2f} sigma)")
check("C3 POSITIVE CONTROL: void lenses have fewer GAMA spec-z neighbours than matched outside lenses, T < 0 at > 3 sigma",
      f"T = {M['T'][0]:+.4f} +- {M['T'][1]:.4f} ({M['T'][0] / M['T'][1]:+.2f} sigma)", M["T"][0] / M["T"][1] < -3)


def verdict(d, s):
    if d < 0 and d / s < -3:
        return "SETTLING-SIGN"
    if d > 0 and d / s > 3:
        return "FORCE-SIGN"
    if abs(d / s) < 2 and abs(d) + 2 * s < 0.1:
        return "NULL (LCDM-consistent)"
    return "NON-DISCRIMINATING"


VK = {K: verdict(*M[K]) for K in ("KO", "K1")}

# ================================================================== sensitivity (reported)
R.banner("SENSITIVITY (reported only, never the verdict)")
SENS = {}
g10 = geo10[ia]; g4 = geo4[ia]
rows = [("GeoS10 void vs rest", g10 == 0, g10 >= 1, {}),
        ("GeoS4 void vs sheet+filament", g4 == 0, (g4 == 1) | (g4 == 2), {}),
        ("early only", VF, OF, dict(cls=EARLY)), ("late only", VF, OF, dict(cls=LATE)),
        ("Alpaslan void vs fil+tendril", alp["void"], alp["filament"] | alp["tendril"], {}),
        ("headline, 36 sub-patch jackknife", VF, OF, dict(reg=SUB, nreg=3 * NP))]
for nm, vf, of, kw in rows:
    if MUTATE and nm.startswith(("GeoS10", "GeoS4", "Alpaslan")):
        vf, of = vf[perm], of[perm]
    o = run(vf, of, **kw)
    SENS[nm] = o
    P(f"  {nm:34s}: N_V {o['NV']:5d}, N_O {o['NO']:5d}; KO {o['KO'][0]:+.4f} +- {o['KO'][1]:.4f} ({o['KO'][0] / o['KO'][1]:+.2f} s); "
      f"K1 {o['K1'][0]:+.4f} +- {o['K1'][1]:.4f} ({o['K1'][0] / o['K1'][1]:+.2f} s); T {o['T'][0]:+.4f} ({o['T'][0] / o['T'][1]:+.2f} s)")

R.banner("VERDICT")
P(f"  HEADLINE (outer bins KO): D = {M['KO'][0]:+.4f} +- {M['KO'][1]:.4f} dex -> {VK['KO']}"
  f"{' (UNDERPOWERED for 0.1 dex, declared before scoring)' if UNDER else ''}")
P(f"  1-halo K1 (same map, reported): D = {M['K1'][0]:+.4f} +- {M['K1'][1]:.4f} dex -> {VK['K1']}")
P("  LCDM's 2-halo term is also lower around void galaxies: a negative outer D is not unique to settling.  kappa fitted; "
  "cold mass still required; not theory closed.")
R.num("M", M); R.num("verdict", VK); R.num("power", pw); R.num("underpowered", UNDER); R.num("SENS", SENS)
R.num("C1", dict(dD=dD, chi2=x2full, fp_el=fp_el, fp_s=fp_s, full_el=full_el, chance=chance))
R.num("aset", dict(N=int(ia.size), NP=NP, patches=PATS.tolist()))
nf = R.write(HERE)
sys.exit(1 if nf else 0)
