#!/usr/bin/env python3
"""CFG561 -- DO ISOLATED KiDS LENSES INSIDE COSMIC VOIDS LENS DIFFERENTLY FROM MATCHED LENSES OUTSIDE?
Settling (supply-limited cold fluid) predicts LOWER outer lensing in voids; a law-as-force without EFE (foil) predicts HIGHER;
LCDM a small difference at fixed M* (declared |D| < ~0.1 dex).  Pure data; a0 footings (9.3603e-11 / 1.1312e-10, kappa = 1/2
FITTED) irrelevant.  Criteria frozen and committed before this script: FROZEN_CRITERIA.md (4a5cebaa2).
  data   cfg110_perlens.npz, lr_lenses.npz, lr_esd_jackknife.npz, KiDS DR4 bright sample (pool), Mao+2017 BOSS DR12 voids (data/).
  set    KiDS-N (Dec > -15), 0.22 <= z_l <= 0.50.  p_void = max over voids of the photo-z-integrated chord probability
         (sigma_z = 0.02(1+z)).  VOID p >= 0.25, OUTSIDE p < 0.02; OUTSIDE reweighted to VOID's (logM*, z, colour) histogram.
  stat   D_K = log10[ESD_V / ESD_O] pooled over K (KO = bins 0-7 headline, K1 = 8-14); 50-patch jackknife.
MUTATE=1: p_void shuffled among analysis-set lenses (seed 561); the tracer C3 must FAIL -> rc 1.
Run: python3 campaign_fresh_gravity/CFG561_kids_lensing_voids/cfg561_voids.py   (MUTATE=1 for the control)
"""
import os, sys, json
import numpy as np
from astropy.io import fits
from astropy.cosmology import FlatLambdaCDM
from scipy.spatial import cKDTree
from scipy.stats import chi2 as CHI2, norm

HERE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(HERE)
sys.path.insert(0, CFG)
import CFG7_common as C

MUTATE = os.environ.get("MUTATE", "0") == "1"
R = C.Report("cfg561_voids", MUTATE)
P, check = R.P, R.check
P(__doc__.split("Run: python3")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: p_void shuffled among analysis-set lenses -- the tracer C3 must FAIL ***")

LR = os.path.join(C.REPO, "real_research", "data", "lensing_rar")
PL = np.load(os.path.join(LR, "cfg110_perlens.npz"))
LN = np.load(os.path.join(LR, "lr_lenses.npz"))
J = np.load(os.path.join(LR, "lr_esd_jackknife.npz"))
KG = 1.989e30 / (3.0857e16) ** 2
K1 = list(range(8, 15)); KO = list(range(8))
NPAT = 50
HART = (NPAT - 7 - 2) / (NPAT - 1)
WG = PL["WG"].astype(float); WW = PL["WW"].astype(float)
typ, zl, lml = LN["typ"], LN["z"], LN["logM"]
patch = J["patch"]
NL = len(zl)
EARLY, LATE = typ == 1, typ == 0

# ================================================================== C1 (copied from CFG446)
R.banner("C1  CONTROL: CFG88's full-sample K1 split from the per-lens sums (CFG446 C1)")
WGk, WWk = WG[:, K1], WW[:, K1]


def esd_loo(mask):
    g = WGk[mask]; v = WWk[mask]; pa = patch[mask]
    tg, tw = g.sum(0), v.sum(0)
    Sg = np.zeros((NPAT, 7)); Sw = np.zeros((NPAT, 7))
    np.add.at(Sg, pa, g); np.add.at(Sw, pa, v)
    return tg / tw / KG, (tg[None] - Sg) / (tw[None] - Sw) / KG


eL, lL = esd_loo(LATE); eE, lE = esd_loo(EARLY)
Dfull, Lfull = eE - eL, lE - lL
Rr = Lfull - Lfull.mean(0)
Ci = np.linalg.inv((NPAT - 1) / NPAT * (Rr.T @ Rr))
x2full = float(Dfull @ Ci @ Dfull) * HART
c88 = json.load(open(os.path.join(CFG, "CFG88_kids_split_jackknife_results.json")))["numbers"]
dD = float(np.max(np.abs(Dfull / np.array(c88["D"]) - 1)))
check("C1 CONTROL: D_full equals CFG88's K1 D (1e-6 rel) and the zero-model Hartlap chi2 equals CFG88's 35.0418 (1e-6 rel)",
      f"max rel dev {dD:.1e}; chi2 {x2full:.4f}/7 vs {c88['chi2']['L']:.4f} (p {CHI2.sf(x2full, 7):.2e})",
      dD < 1e-6 and abs(x2full / c88["chi2"]["L"] - 1) < 1e-6)

# ================================================================== C2 bright sample / pool (copied from CFG446)
R.banner("C2  CONTROL: lenses in the bright sample; neighbour pool")
bs = fits.open(os.path.join(LR, "KiDS_DR4_brightsample.fits"), memmap=True)[1].data
lp = fits.open(os.path.join(LR, "KiDS_DR4_brightsample_LePhare.fits"), memmap=True)[1].data
ra = np.array(bs["RAJ2000"], "f8"); dec = np.array(bs["DECJ2000"], "f8")
zb = np.array(bs["zphot_ANNz2"], "f8"); rmag = np.array(bs["MAG_AUTO_CALIB"], "f8"); msk = np.array(bs["masked"])
lmb = np.array(lp["MASS_MED"], "f8") + 0.15
pool = (rmag < 20) & (zb > 0.1) & (zb < 0.5) & (msk == 0) & np.isfinite(lmb) & (lmb > 7)
key = lambda a, d: np.round(a * 1e7).astype(np.int64) * 10 ** 10 + np.round((d + 90) * 1e7).astype(np.int64)
kb, kl = key(ra, dec), key(LN["ra"], LN["dec"])
order = np.argsort(kb, kind="stable"); ks = kb[order]
pos = np.minimum(np.searchsorted(ks, kl), len(ks) - 1)
idx = order[pos]
matched = bool(np.all(ks[pos] == kl)); z_ok = bool(np.array_equal(zb[idx], zl)); inpool = bool(pool[idx].all())
check("C2 CONTROL: all lenses match the bright sample by exact position, same z, all in the pool",
      f"{NL:,} lenses; exact {matched}; z {z_ok}; in pool {inpool}", matched and z_ok and inpool)

# ================================================================== analysis set + distances
cos = FlatLambdaCDM(H0=100, Om0=0.3089)
zg = np.linspace(0, 1.2, 4801); chig = cos.comoving_distance(zg).value
chi_of = lambda z: np.interp(z, zg, chig); z_of = lambda c: np.interp(c, chig, zg)
NORTH = LN["dec"] > -15
ASET = NORTH & (zl >= 0.22) & (zl <= 0.50)
ia = np.where(ASET)[0]
P(f"  analysis set: KiDS-N, 0.22 <= z <= 0.50: {ia.size:,} lenses (early {int(EARLY[ia].sum()):,}, late {int(LATE[ia].sum()):,})")


def unitvec(ra_deg, dec_deg):
    a, d = np.radians(ra_deg), np.radians(dec_deg)
    return np.c_[np.cos(d) * np.cos(a), np.cos(d) * np.sin(a), np.sin(d)]


XL = unitvec(LN["ra"][ia], LN["dec"][ia]); ZL = zl[ia]; SZ = 0.02 * (1 + ZL)
assert np.isfinite(XL).all() and np.isfinite(ZL).all()   # matmul "invalid value" warnings on this BLAS are spurious

rows = [l.split() for l in open(os.path.join(HERE, "data", "mao2017_table1.dat"))]
V = dict(samp=np.array([a[0] + a[1] for a in rows]), ra=np.array([float(a[3]) for a in rows]),
         dec=np.array([float(a[4]) for a in rows]), z=np.array([float(a[5]) for a in rows]), R=np.array([float(a[8]) for a in rows]))
vn = np.char.endswith(V["samp"], "North")
P(f"  voids: {len(rows)} in the catalogue, {int(vn.sum())} BOSS North; centres in the KiDS-N box: "
  f"{int(np.sum(vn & (V['ra'] > 128) & (V['ra'] < 240) & (np.abs(V['dec']) < 5)))}")


def pvoid(vra, vdec, vz, vR):
    p = np.zeros(len(ia))
    XV = unitvec(vra, vdec); DV = chi_of(vz)
    for k in range(len(vz)):
        ang = np.arccos(np.clip(XL @ XV[k], -1, 1))
        rp = DV[k] * ang
        m = rp < vR[k]
        if not m.any():
            continue
        h = np.sqrt(vR[k] ** 2 - rp[m] ** 2)
        z1, z2 = z_of(DV[k] - h), z_of(DV[k] + h)
        pk = norm.cdf((z2 - ZL[m]) / SZ[m]) - norm.cdf((z1 - ZL[m]) / SZ[m])
        p[m] = np.maximum(p[m], pk)
    return p


PV = pvoid(V["ra"][vn], V["dec"][vn], V["z"][vn], V["R"][vn])
PV05 = pvoid(V["ra"][vn], V["dec"][vn], V["z"][vn], 0.5 * V["R"][vn])
if MUTATE:
    perm = np.random.default_rng(561).permutation(len(ia))
    PV, PV05 = PV[perm], PV05[perm]
P(f"  p_void: fraction >= 0.25: {np.mean(PV >= 0.25):.4f}; >= 0.5: {np.mean(PV >= 0.5):.4f}; < 0.02: {np.mean(PV < 0.02):.4f}; "
  f"max {PV.max():.3f}")

# ================================================================== tracer counts (C3)
R.banner("C3 inputs: pool neighbours within 8 Mpc/h comoving projected, |dz| < 2 x 0.018(1+z)")
ipn = np.where(pool & (dec > -15))[0]
zP = zb[ipn]
tree = cKDTree(unitvec(ra[ipn], dec[ipn]))
theta = 8.0 / chi_of(ZL)
win = 2 * 0.018 * (1 + ZL)
NB = np.zeros(len(ia))
CH = 4000
for i0 in range(0, len(ia), CH):
    sl = slice(i0, i0 + CH)
    lists = tree.query_ball_point(XL[sl], r=2 * np.sin(theta[sl] / 2))
    lk = np.repeat(np.arange(len(lists)), [len(x) for x in lists])
    js = np.fromiter((j for x in lists for j in x), dtype=np.int64, count=int(sum(len(x) for x in lists)))
    inw = np.abs(zP[js] - ZL[sl][lk]) < win[sl][lk]
    NB[sl] = np.bincount(lk[inw], minlength=len(lists)) - 1   # lens itself is in the pool
P(f"  mean neighbours {NB.mean():.1f} (min {NB.min():.0f})")

# ================================================================== machinery on the analysis set
lmc = np.clip(np.digitize(lml[ia], np.arange(8.5, 11.0 + 1e-9, 0.1)) - 1, 0, 24)
zc = np.clip(np.digitize(ZL, np.arange(0.22, 0.50 + 1e-9, 0.025)) - 1, 0, 11)
cell = (lmc * 12 + zc) * 2 + typ[ia]
NC = 25 * 12 * 2
pa = patch[ia]
NPOP = int(np.unique(pa).size)
JF = (NPOP - 1) / NPOP
GA = {"K1": WG[ia][:, K1].sum(1), "KO": WG[ia][:, KO].sum(1)}
WA = {"K1": WW[ia][:, K1].sum(1), "KO": WW[ia][:, KO].sum(1)}
P(f"  jackknife: {NPOP} of {NPAT} patches populated in the analysis set; factor (n-1)/n = {JF:.4f}")


def match_w(vm, om):
    nv = np.bincount(cell[vm], minlength=NC).astype(float); no = np.bincount(cell[om], minlength=NC).astype(float)
    ok = no > 0
    w = np.zeros(len(ia)); w[om] = np.where(ok, nv / np.where(ok, no, 1), 0)[cell[om]]
    vkeep = vm & ok[cell]
    return vkeep, w, float(1 - vkeep.sum() / max(vm.sum(), 1))


def pooled_ratio(x_num, x_den, vm, wv, om, wo):
    """log10[(sum_V wv x_num / sum_V wv x_den) / (sum_O wo x_num / sum_O wo x_den)] and jackknife replicates."""
    def s(m, w, x):
        t = np.zeros(NPAT); np.add.at(t, pa[m], (w * x)[m]); return t
    a, b, c, d = s(vm, wv, x_num), s(vm, wv, x_den), s(om, wo, x_num), s(om, wo, x_den)
    full = np.log10(a.sum() / b.sum() / (c.sum() / d.sum()))
    reps = np.log10((a.sum() - a) / (b.sum() - b) / ((c.sum() - c) / (d.sum() - d)))
    used = np.isin(np.arange(NPAT), pa)
    sig = float(np.sqrt(JF * np.sum((reps[used] - reps[used].mean()) ** 2)))
    return float(full), sig, reps


def run(pv, vthr=0.25, othr=0.02, weighted=False, cls=None, quiet=False):
    base = np.ones(len(ia), bool) if cls is None else cls[ia]
    vm = base & (pv >= (othr if weighted else vthr)); om = base & (pv < othr)
    vkeep, wo, drop = match_w(vm, om)
    wv = pv.copy() if weighted else np.ones(len(ia))
    out = dict(NV=int(vkeep.sum()), NO=int(om.sum()), drop=drop, pV=float(np.average(pv[vkeep], weights=wv[vkeep])) if vkeep.any() else np.nan,
               pO=float(np.average(pv[om], weights=wo[om])) if om.any() else np.nan,
               NOeff=float(wo.sum() ** 2 / (wo ** 2).sum()) if om.any() else 0.0)
    for K in ("KO", "K1"):
        d, s, _ = pooled_ratio(GA[K], WA[K], vkeep, wv, om, wo)
        out[K] = (d, s)
    t, st, _ = pooled_ratio(NB, np.ones(len(ia)), vkeep, wv, om, wo)
    out["T"] = (t, st)
    return out


def corr(d, s, pV, pO):
    f = pV - pO
    dc = np.log10(max(1 + (10 ** d - 1) / f, 1e-6))
    hi = np.log10(max(1 + (10 ** (d + s) - 1) / f, 1e-6)); lo = np.log10(max(1 + (10 ** (d - s) - 1) / f, 1e-6))
    return float(dc), float((hi - lo) / 2)


# ================================================================== power (C5) before any void number
R.banner("POWER / C5: 100 random analysis-set subsets of the VOID size vs their matched complement")
NVraw = int(np.sum(PV >= 0.25))
rng = np.random.default_rng(5610)
zz = {"KO": [], "K1": []}; ss = {"KO": [], "K1": []}
for t in range(100):
    pr = np.zeros(len(ia)); pr[rng.choice(len(ia), NVraw, replace=False)] = 1.0
    o = run(pr)
    for K in ("KO", "K1"):
        zz[K].append(o[K][0] / o[K][1]); ss[K].append(o[K][1])
pV0 = float(PV[PV >= 0.25].mean()); pO0 = float(PV[PV < 0.02].mean())
pw = {}
for K in ("KO", "K1"):
    sK = float(np.median(ss[K])); f = pV0 - pO0
    pw[K] = dict(sigma=sK, std_z=float(np.std(zz[K])), mean_z=float(np.mean(zz[K])),
                 P3sig_0p1dex=float(norm.cdf(abs(np.log10(1 + (10 ** 0.1 - 1) * f)) / sK - 3)),
                 bound2s_corrected=corr(0.0, sK, pV0, pO0)[1] * 2)
    P(f"  {K}: N_void {NVraw:,}; expected sigma_D {sK:.4f} dex; null z std {np.std(zz[K]):.3f} mean {np.mean(zz[K]):+.3f}; "
      f"purity pV-pO {f:.3f}; P(3 sigma | true 0.1 dex) {pw[K]['P3sig_0p1dex']:.2f}; expected corrected 2-sigma bound "
      f"{pw[K]['bound2s_corrected']:.3f} dex")
check("C5 (reported): null calibration -- std of D/sigma over 100 random subsets in [0.7, 1.3], KO and K1",
      f"KO {pw['KO']['std_z']:.3f}, K1 {pw['K1']['std_z']:.3f}", all(0.7 <= pw[K]["std_z"] <= 1.3 for K in pw), load_bearing=False)

# ================================================================== the measurement
R.banner("MEASUREMENT: VOID (p >= 0.25) vs matched OUTSIDE (p < 0.02)")
M = run(PV)
P(f"  VOID N {M['NV']:,} (dropped for empty cells {M['drop']:.4f}), OUTSIDE N {M['NO']:,} (effective {M['NOeff']:.0f}); "
  f"purity pV {M['pV']:.3f}, pO {M['pO']:.4f}")
for K in ("KO", "K1"):
    d, s = M[K]; dc, sc = corr(d, s, M["pV"], M["pO"])
    P(f"  {K}: D = {d:+.4f} +- {s:.4f} dex ({d / s:+.2f} sigma); purity-corrected {dc:+.4f} +- {sc:.4f}; "
      f"corrected 2-sigma bound {abs(dc) + 2 * sc:.3f} dex")
    M[K + "_c"] = (dc, sc)
P(f"  tracer T = log10(N_V/N_O) = {M['T'][0]:+.4f} +- {M['T'][1]:.4f} ({M['T'][0] / M['T'][1]:+.2f} sigma)")
check("C3 POSITIVE CONTROL: void lenses have fewer pool neighbours than matched outside lenses, T < 0 at > 3 sigma",
      f"T = {M['T'][0]:+.4f} +- {M['T'][1]:.4f} ({M['T'][0] / M['T'][1]:+.2f} sigma)", M["T"][0] / M["T"][1] < -3)


def verdict(d, s, dc, sc):
    if d < 0 and d / s < -3:
        return "SETTLING-SIGN"
    if d > 0 and d / s > 3:
        return "FORCE-SIGN"
    if abs(d / s) < 2 and abs(dc) + 2 * sc < 0.1:
        return "NULL (LCDM-consistent)"
    return "NON-DISCRIMINATING"


VK = {K: verdict(*M[K], *M[K + "_c"]) for K in ("KO", "K1")}

# ================================================================== C4 random voids
R.banner("C4  CONTROL: 20 random void catalogues (z, R_eff kept).  DEPARTURE (disclosed): the frozen spec redrew ALL BOSS-North "
         "centres into the KiDS-N box (x~5 the real void density there; OUTSIDE emptied, run 1 NaN, kept as "
         "cfg561_voids_RUN1_C4misspecified.out).  Fix: only voids with centres in RA 118-248, Dec -1.2..+12 (the voids that can reach "
         "the lenses; BOSS-North centres stop at Dec -1.15) are redrawn, uniformly in that same box.")
rngv = np.random.default_rng(5611)
bx = vn & (V["ra"] > 118) & (V["ra"] < 248) & (V["dec"] > -1.2) & (V["dec"] < 12)
nvn = int(bx.sum())
P(f"  voids redrawn per catalogue: {nvn}")
rz = {"KO": [], "K1": [], "T": []}
for t in range(20):
    rra = rngv.uniform(118, 248, nvn)
    rde = np.degrees(np.arcsin(rngv.uniform(np.sin(np.radians(-1.2)), np.sin(np.radians(12)), nvn)))
    pr = pvoid(rra, rde, V["z"][bx], V["R"][bx])
    o = run(pr)
    for K in ("KO", "K1", "T"):
        rz[K].append(o[K][0] / o[K][1])
    P(f"  random {t:2d}: N_void {o['NV']:5d}; z_KO {rz['KO'][-1]:+.2f}, z_K1 {rz['K1'][-1]:+.2f}, z_T {rz['T'][-1]:+.2f}")
lim = 1.5 * 3 / np.sqrt(20)
c4 = {K: (float(np.mean(rz[K])), float(np.std(rz[K])), float(np.max(np.abs(rz[K])))) for K in rz}
check("C4 CONTROL: random voids -> null (mean z of D_KO and D_K1 within +-1.01, no |z| > 3.5)",
      "; ".join(f"{K}: mean {c4[K][0]:+.2f}, std {c4[K][1]:.2f}, max|z| {c4[K][2]:.2f}" for K in c4),
      all(abs(c4[K][0]) < lim and c4[K][2] < 3.5 for K in ("KO", "K1")))

# ================================================================== sensitivity (reported)
R.banner("POST HOC (added after run 1, reported only): does the void flag trace KiDS neighbour density at a wider aperture?")
NB20 = np.zeros(len(ia)); th20 = 20.0 / chi_of(ZL)
for i0 in range(0, len(ia), 2000):
    sl = slice(i0, i0 + 2000)
    lists = tree.query_ball_point(XL[sl], r=2 * np.sin(th20[sl] / 2))
    lk = np.repeat(np.arange(len(lists)), [len(x) for x in lists])
    js = np.fromiter((j for x in lists for j in x), dtype=np.int64, count=int(sum(len(x) for x in lists)))
    inw = np.abs(zP[js] - ZL[sl][lk]) < win[sl][lk]
    NB20[sl] = np.bincount(lk[inw], minlength=len(lists)) - 1
PH = {}
for nm, pv, thr in (("p >= 0.25, 20 Mpc/h", PV, 0.25), ("p >= 0.5, 20 Mpc/h", PV, 0.5)):
    vm = PV >= thr; om = PV < 0.02
    vk, wo, _ = match_w(vm, om)
    t20 = pooled_ratio(NB20, np.ones(len(ia)), vk, np.ones(len(ia)), om, wo)
    PH[nm] = t20[:2]
    P(f"  {nm}: T20 = {t20[0]:+.4f} +- {t20[1]:.4f} ({t20[0] / t20[1]:+.2f} sigma)")
R.num("posthoc_T20", PH)

R.banner("SENSITIVITY (reported only, never the verdict)")
SENS = {}
for nm, kw, pv in (("deep cores R = 0.5 R_eff", {}, PV05), ("p >= 0.5", dict(vthr=0.5), PV), ("p-weighted", dict(weighted=True), PV),
                   ("early only", dict(cls=EARLY), PV), ("late only", dict(cls=LATE), PV)):
    o = run(pv, **kw)
    SENS[nm] = o
    P(f"  {nm:26s}: N_V {o['NV']:5d}, pV {o['pV']:.3f}; KO {o['KO'][0]:+.4f} +- {o['KO'][1]:.4f} ({o['KO'][0] / o['KO'][1]:+.2f} s); "
      f"K1 {o['K1'][0]:+.4f} +- {o['K1'][1]:.4f} ({o['K1'][0] / o['K1'][1]:+.2f} s); T {o['T'][0]:+.4f} ({o['T'][0] / o['T'][1]:+.2f} s)")

R.banner("VERDICT")
P(f"  HEADLINE (outer bins KO): D = {M['KO'][0]:+.4f} +- {M['KO'][1]:.4f} dex -> {VK['KO']}")
P(f"  1-halo K1 (same map, reported): D = {M['K1'][0]:+.4f} +- {M['K1'][1]:.4f} dex -> {VK['K1']}")
P("  LCDM's 2-halo term is also lower around void galaxies: a negative outer D is not unique to settling.  kappa fitted; "
  "cold mass still required; not theory closed.")
R.num("M", M); R.num("verdict", VK); R.num("power", pw); R.num("C4", c4); R.num("SENS", SENS)
R.num("C1", dict(dD=dD, chi2=x2full)); R.num("aset", dict(N=int(ia.size), NPOP=NPOP))
nf = R.write(HERE)
sys.exit(1 if nf else 0)
