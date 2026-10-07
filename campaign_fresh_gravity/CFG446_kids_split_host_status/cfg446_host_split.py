#!/usr/bin/env python3
"""CFG446 -- IS THE KiDS EARLY/LATE SPLIT CARRIED BY EARLY TYPES THAT ARE GROUP CENTRALS?  The two-regime reading (cold_mass cm08-cm10,
CFG399: retained cold mass steps at host status) predicts that the early-minus-late 1-halo excess sits in early types with many faint
companions and that companion-poor early types sit at the late level.  LCDM also predicts richer centrals lens more: SUPPORTED would
not discriminate the framework from LCDM; FAILS would remove the two-regime explanation of B's failure.

Criteria frozen and committed before this script existed: campaign_fresh_gravity/CFG446_kids_split_host_status/FROZEN_CRITERIA.md (f0232a4c1).
  data     cfg110_perlens.npz (per-lens WG, WW per g_bar bin), lr_lenses.npz, lr_esd_jackknife.npz (June patches), KiDS DR4 bright sample.
  env      E1: pool companions with log M* < log M*_lens - 1 (the task's measure); E2 (departure): log M* < log M*_lens; R < 0.5 Mpc
           physical, |dz| < 2 x 0.018 (1+z_l); X = N_raw - N_bg, N_bg = mean over 10 random positions per lens (HEALPix-512 occupancy).
  split    terciles of X within each class (seeded tie-break).
  stat     A_S = (D_full^T C^-1 D_S) / (D_full^T C^-1 D_full), D_S = ESD(early S) - ESD(all late) on K1; jackknife (50 patches).
           Headline: (log M*, z)-matched poor and rich subsamples.  Verdicts: SUPPORTED |A_poor|/s < 2 and A_rich/s > 3;
           FAILS A_poor/s > 3 and A_poor >= 0.70; else NON-DISCRIMINATING.  Gate G: mean X(rich) - mean X(poor) >= 0.5.
  law      B's law predicts a negligible early-minus-late difference in K1 under both footings (CFG61's committed stacks; projected below).
MUTATE=1: X shuffled among early types (seed 446); M1 (|dA_matched|/s >= 1, E1 and E2) must FAIL -> rc 1.
Run: python3 campaign_fresh_gravity/CFG446_kids_split_host_status/cfg446_host_split.py   (MUTATE=1 for the control)
"""
import os, sys, json
import numpy as np
from astropy.io import fits
from scipy.spatial import cKDTree
from scipy.stats import chi2 as CHI2, norm
import healpy as hp

HERE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(HERE)
sys.path.insert(0, CFG)
import CFG7_common as C

MUTATE = os.environ.get("MUTATE", "0") == "1"
R = C.Report("cfg446_host_split", MUTATE)
P, check = R.P, R.check
P(__doc__.split("Run: python3")[0].strip())
P(f"  a0 footings: canonical 9.3603e-11, alt 1.1312e-10 m/s^2 (kappa = 1/2 FITTED); B's K1 prediction is the zero difference under both.")
if MUTATE:
    P("\n  *** MUTATE=1: X shuffled among early types -- the poor/rich contrast must vanish (M1 must FAIL) ***")

LR = os.path.join(C.REPO, "real_research", "data", "lensing_rar")
PL = np.load(os.path.join(LR, "cfg110_perlens.npz"))
LN = np.load(os.path.join(LR, "lr_lenses.npz"))
J = np.load(os.path.join(LR, "lr_esd_jackknife.npz"))
KG = 1.989e30 / (3.0857e16) ** 2
K1 = [8, 9, 10, 11, 12, 13, 14]
NPAT = 50
HART = (NPAT - 7 - 2) / (NPAT - 1)
WGk = PL["WG"][:, K1].astype(float); WWk = PL["WW"][:, K1].astype(float)
K2 = list(range(8))   # post-hoc reported tracer row only (bins 0-7, the outer / 2-halo range)
WGo = PL["WG"][:, K2].astype(float).sum(1); WWo = PL["WW"][:, K2].astype(float).sum(1)
typ, zl, chil, lml = LN["typ"], LN["z"], LN["chi"], LN["logM"]
patch = J["patch"]
NL = len(zl)
EARLY, LATE = typ == 1, typ == 0

# ================================================================== C2: lens <-> bright sample
R.banner("C2  CONTROL: lenses in the bright sample")
bs = fits.open(os.path.join(LR, "KiDS_DR4_brightsample.fits"), memmap=True)[1].data
lp = fits.open(os.path.join(LR, "KiDS_DR4_brightsample_LePhare.fits"), memmap=True)[1].data
ids_ok = bool(np.array_equal(bs["ID"], lp["ID"]))
ra = np.array(bs["RAJ2000"], "f8"); dec = np.array(bs["DECJ2000"], "f8")
zb = np.array(bs["zphot_ANNz2"], "f8"); rmag = np.array(bs["MAG_AUTO_CALIB"], "f8"); msk = np.array(bs["masked"])
lmb = np.array(lp["MASS_MED"], "f8") + 0.15
ur = np.array(lp["MAG_ABS_u"] - lp["MAG_ABS_r"], "f8")
pool = (rmag < 20) & (zb > 0.1) & (zb < 0.5) & (msk == 0) & np.isfinite(lmb) & (lmb > 7)
key = lambda a, d: np.round(a * 1e7).astype(np.int64) * 10 ** 10 + np.round((d + 90) * 1e7).astype(np.int64)
kb, kl = key(ra, dec), key(LN["ra"], LN["dec"])
order = np.argsort(kb, kind="stable"); ks = kb[order]
pos = np.minimum(np.searchsorted(ks, kl), len(ks) - 1)
idx = order[pos]
matched = bool(np.all(ks[pos] == kl)) and bool(np.all(ra[idx] == LN["ra"])) and bool(np.all(dec[idx] == LN["dec"]))
typ_ok = bool(np.array_equal((ur[idx] > 2.0).astype(int), typ))
lm_ok = bool(np.array_equal(lmb[idx], lml)); z_ok = bool(np.array_equal(zb[idx], zl)); inpool = bool(pool[idx].all())
check("C2 CONTROL: all lenses match the bright sample by exact position; u - r > 2 reproduces typ; log M* = MASS_MED + 0.15; all in the pool",
      f"{NL:,} lenses; IDs aligned {ids_ok}; exact match {matched}; typ {typ_ok}; logM {lm_ok}; z {z_ok}; in pool {inpool}",
      ids_ok and matched and typ_ok and lm_ok and z_ok and inpool)

# ================================================================== environment counts
R.banner("ENVIRONMENT: E1 (< 10% lens mass) and E2 (< lens mass) companions, random-position background")
ip = np.where(pool)[0]
zP, lmP = zb[ip], lmb[ip]
raP, decP = np.radians(ra[ip]), np.radians(dec[ip])
tree = cKDTree(np.c_[np.cos(decP) * np.cos(raP), np.cos(decP) * np.sin(raP), np.sin(decP)])
theta = 0.5 * (1 + zl) / chil
win = 2 * 0.018 * (1 + zl)


def unitvec(ra_deg, dec_deg):
    a, d = np.radians(ra_deg), np.radians(dec_deg)
    return np.c_[np.cos(d) * np.cos(a), np.cos(d) * np.sin(a), np.sin(d)]


def counts(xyz, li):
    """xyz: query points (n x 3); li: the lens index whose (z, logM, theta) criteria apply.  Returns (N_E1, N_E2)."""
    n1 = np.zeros(len(li)); n2 = np.zeros(len(li))
    CH = 50000
    for i0 in range(0, len(li), CH):
        sl = slice(i0, i0 + CH); L = li[sl]
        lists = tree.query_ball_point(xyz[sl], r=2 * np.sin(theta[L] / 2))
        lens_k = np.repeat(np.arange(len(L)), [len(x) for x in lists])
        js = np.fromiter((j for x in lists for j in x), dtype=np.int64, count=int(sum(len(x) for x in lists)))
        Lk = L[lens_k]
        inw = np.abs(zP[js] - zl[Lk]) < win[Lk]
        e1 = inw & (lmP[js] < lml[Lk] - 1.0); e2 = inw & (lmP[js] < lml[Lk])
        n1[sl] = np.bincount(lens_k[e1], minlength=len(L)); n2[sl] = np.bincount(lens_k[e2], minlength=len(L))
    return n1, n2


NSIDE = 512
good = msk == 0
occ = np.zeros(hp.nside2npix(NSIDE), bool)
occ[hp.ang2pix(NSIDE, ra[good], dec[good], lonlat=True)] = True
south = LN["dec"] < -15.0


def draw_randoms(n, rng):
    """uniform on the sphere inside the two fields' bounding boxes, kept if in an occupied pixel; field chosen by area."""
    boxes = []
    for m in (~south, south):
        rau = np.where(m & south, (LN["ra"] + 180) % 360, LN["ra"])[m]
        boxes.append((rau.min() - 0.5, rau.max() + 0.5, LN["dec"][m].min() - 0.5, LN["dec"][m].max() + 0.5, m is south))
    areas = np.array([(b[1] - b[0]) * (np.sin(np.radians(b[3])) - np.sin(np.radians(b[2]))) for b in boxes])
    out_ra, out_dec = [], []
    got = 0
    while got < n:
        m = 2 * (n - got) + 1000
        which = rng.random(m) < areas[0] / areas.sum()
        r_ = np.empty(m); d_ = np.empty(m)
        for bi, sel in ((0, which), (1, ~which)):
            b = boxes[bi]; k = int(sel.sum())
            rr = rng.uniform(b[0], b[1], k)
            r_[sel] = (rr - 180) % 360 if b[4] else rr
            d_[sel] = np.degrees(np.arcsin(rng.uniform(np.sin(np.radians(b[2])), np.sin(np.radians(b[3])), k)))
        keep = occ[hp.ang2pix(NSIDE, r_, d_, lonlat=True)]
        out_ra.append(r_[keep]); out_dec.append(d_[keep]); got += int(keep.sum())
    return np.concatenate(out_ra)[:n], np.concatenate(out_dec)[:n]


KR = 10
rng = np.random.default_rng(446)
Nraw1, Nraw2 = counts(unitvec(LN["ra"], LN["dec"]), np.arange(NL))
rr_, rd_ = draw_randoms(NL * KR, rng)
li_r = np.repeat(np.arange(NL), KR)
B1, B2 = counts(unitvec(rr_, rd_), li_r)
Nbg1 = B1.reshape(NL, KR).mean(1); Nbg2 = B2.reshape(NL, KR).mean(1)
X = {"E1": Nraw1 - Nbg1, "E2": Nraw2 - Nbg2}
NRAW = {"E1": Nraw1, "E2": Nraw2}
P(f"  occupied HEALPix-{NSIDE} pixels: {int(occ.sum()):,} ({occ.sum() * hp.nside2pixarea(NSIDE, degrees=True):.0f} deg^2)")
for E in ("E1", "E2"):
    for nm, m in (("early", EARLY), ("late", LATE)):
        P(f"  {E} {nm:5s}: mean N_raw {NRAW[E][m].mean():.3f}, mean N_bg {(Nbg1 if E == 'E1' else Nbg2)[m].mean():.3f}, "
          f"mean X {X[E][m].mean():+.3f} +- {X[E][m].std() / np.sqrt(m.sum()):.3f}; fraction N_raw >= 1: {np.mean(NRAW[E][m] >= 1):.3f}")

# C3: an independent random set (one per lens), each carrying its lens's criteria
rng3 = np.random.default_rng(4461)
r3, d3 = draw_randoms(NL, rng3)
T1, T2 = counts(unitvec(r3, d3), np.arange(NL))
c3 = {}
for E, T, Bg in (("E1", T1, Nbg1), ("E2", T2, Nbg2)):
    xr = T - Bg
    c3[E] = (float(xr.mean()), float(xr.std() / np.sqrt(NL)))
check("C3 CONTROL: random-position background -- at independent random positions the mean X is 0 within 3 standard errors (E1, E2)",
      "; ".join(f"{E}: mean X_random {c3[E][0]:+.4f} +- {c3[E][1]:.4f} ({c3[E][0] / c3[E][1]:+.2f} SE)" for E in c3),
      all(abs(c3[E][0]) < 3 * c3[E][1] for E in c3))

if MUTATE:
    rngm = np.random.default_rng(446)
    for E in ("E1", "E2"):
        ie = np.where(EARLY)[0]
        X[E] = X[E].copy(); X[E][ie] = X[E][ie][rngm.permutation(len(ie))]

# ================================================================== the lensing machinery
def esd_loo(mask, w=None):
    ww_ = np.ones(int(mask.sum())) if w is None else w[mask]
    g = WGk[mask] * ww_[:, None]; v = WWk[mask] * ww_[:, None]; pa = patch[mask]
    tg, tw = g.sum(0), v.sum(0)
    Sg = np.zeros((NPAT, 7)); Sw = np.zeros((NPAT, 7))
    np.add.at(Sg, pa, g); np.add.at(Sw, pa, v)
    return tg / tw / KG, (tg[None] - Sg) / (tw[None] - Sw) / KG


def jcov(L):
    Rr = L - L.mean(0)
    return (NPAT - 1) / NPAT * (Rr.T @ Rr)


def jsig(reps):
    return float(np.sqrt((NPAT - 1) / NPAT * np.sum((reps - reps.mean()) ** 2)))


eL, lL = esd_loo(LATE)
eE, lE = esd_loo(EARLY)
Dfull, Lfull = eE - eL, lE - lL
Cf = jcov(Lfull); Ci = np.linalg.inv(Cf)
den = float(Dfull @ Ci @ Dfull)
den_rep = np.einsum("pi,ij,pj->p", Lfull, Ci, Lfull)

R.banner("C1  CONTROL: CFG88's split from the per-lens sums")
c88 = json.load(open(os.path.join(CFG, "CFG88_kids_split_jackknife_results.json")))["numbers"]
x2full = float(Dfull @ Ci @ Dfull) * HART
dD = float(np.max(np.abs(Dfull / np.array(c88["D"]) - 1)))
check("C1 CONTROL: D_full equals CFG88's K1 D (1e-6 rel) and the zero-model Hartlap chi2 equals CFG88's 35.0418 (1e-6 rel)",
      f"max rel dev of D {dD:.1e}; chi2 {x2full:.4f}/7 vs {c88['chi2']['L']:.4f} (p {CHI2.sf(x2full, 7):.2e}); "
      f"D = {np.round(Dfull, 2).tolist()}", dD < 1e-6 and abs(x2full / c88["chi2"]["L"] - 1) < 1e-6)
c61 = json.load(open(os.path.join(CFG, "CFG61_kids_colour_split_results.json")))["numbers"]["RES"]
AB = {f: float((np.array(c61[f]["me"]) - np.array(c61[f]["ml"]))[K1] @ Ci @ Dfull) / den for f in ("canonical", "alt")}
P(f"  B's law, early-minus-late in amplitude units (CFG61 stacks): canonical {AB['canonical']:+.4f}, alt {AB['alt']:+.4f} -- the zero model")


def amp_of(mask, w=None, ref=(eL, lL)):
    e, l = esd_loo(mask, w)
    D, L = e - ref[0], l - ref[1]
    A = float(D @ Ci @ Dfull) / den
    reps = np.einsum("pi,ij,pj->p", L, Ci, Lfull) / den_rep
    Cs = jcov(L)
    x2 = float(D @ np.linalg.solve(Cs, D)) * HART
    return A, reps, x2


lmc = np.clip(np.digitize(lml, np.arange(8.5, 11.0 + 1e-9, 0.1)) - 1, 0, 24)
zc = np.clip(np.digitize(zl, np.arange(0.1, 0.5 + 1e-9, 0.05)) - 1, 0, 7)
cell = lmc * 8 + zc
P(f"  matching cells: {25 * 8}; lenses outside log M* 8.5-11.0 clipped to edge bins: {int(np.sum((lml < 8.5) | (lml >= 11.0))):,}")


def match_weights(sub, ref):
    nref = np.bincount(cell[ref], minlength=200).astype(float); ns = np.bincount(cell[sub], minlength=200).astype(float)
    w = np.zeros(NL)
    ok = ns > 0
    fac = np.where(ok, nref / np.where(ok, ns, 1), 0) * (sub.sum() / ref.sum())
    w[sub] = fac[cell[sub]]
    dropped = float(nref[~ok].sum() / nref.sum())
    return w, dropped


def terciles(Xv, cls, seed=446):
    ii = np.where(cls)[0]
    rk = np.random.default_rng(seed).random(len(ii))
    o = ii[np.lexsort((rk, Xv[ii]))]
    n = len(o); t = [o[: n // 3], o[n // 3: 2 * n // 3], o[2 * n // 3:]]
    ms = []
    for a in t:
        m = np.zeros(NL, bool); m[a] = True; ms.append(m)
    return ms


def verdict(Ap, sp, Ar, sr):
    if abs(Ap) / sp < 2 and Ar / sr > 3:
        return "TWO-REGIME EXPLANATION SUPPORTED"
    if Ap / sp > 3 and Ap >= 0.70:
        return "FAILS"
    return "NON-DISCRIMINATING"


RES = {}
for E in ("E1", "E2"):
    R.banner(f"{E}: EARLY TYPES SPLIT BY COMPANION EXCESS X ({'< 10% lens mass' if E == 'E1' else '< lens mass, departure'})")
    poor, mid, rich = terciles(X[E], EARLY)
    lpoor, lmid, lrich = terciles(X[E], LATE)
    part = (np.array_equal(poor | mid | rich, EARLY) and not np.any(poor & mid) and not np.any(poor & rich) and not np.any(mid & rich)
            and np.array_equal(lpoor | lmid | lrich, LATE) and not np.any(lpoor & lrich) and not np.any(lpoor & lmid) and not np.any(lmid & lrich))
    check(f"C4 CONTROL ({E}): the terciles partition each class exactly", f"early {[int(m.sum()) for m in (poor, mid, rich)]}, "
          f"late {[int(m.sum()) for m in (lpoor, lmid, lrich)]}", part)
    out = {}
    for nm, m in (("poor", poor), ("mid", mid), ("rich", rich)):
        P(f"  early {nm:4s}: N {int(m.sum()):6,}; mean X {X[E][m].mean():+.3f}; frac N_raw>=1 {np.mean(NRAW[E][m] >= 1):.3f}; "
          f"median log M* {np.median(lml[m]):.2f}; median z {np.median(zl[m]):.3f}")
    gX = float(X[E][rich].mean() - X[E][poor].mean())
    gate = gX >= 0.5
    check(f"G ({E}) informativeness: mean X(rich) - mean X(poor) >= 0.5", f"{gX:.3f}", gate, load_bearing=False)
    for mode in ("unmatched", "matched"):
        if mode == "matched":
            wp, dp = match_weights(poor, EARLY); wr, dr = match_weights(rich, EARLY); wm, dm = match_weights(mid, EARLY)
            P(f"  matched: all-early fraction dropped in empty cells: poor {dp:.4f}, mid {dm:.4f}, rich {dr:.4f}")
        else:
            wp = wr = wm = None
        Ap, rp, xp = amp_of(poor, wp); Ar, rr, xr = amp_of(rich, wr); Am, rm, xm = amp_of(mid, wm)
        sp, sr, sm = jsig(rp), jsig(rr), jsig(rm)
        dA, sdA = Ar - Ap, jsig(rr - rp)
        v = verdict(Ap, sp, Ar, sr) if gate else "NON-DISCRIMINATING (gate G failed: measure carries too few companions)"
        P(f"  [{mode}] A_poor {Ap:+.3f} +- {sp:.3f} ({Ap / sp:+.2f} s; chi2 {xp:.1f}/7 p {CHI2.sf(xp, 7):.1e}) | "
          f"A_mid {Am:+.3f} +- {sm:.3f} ({Am / sm:+.2f} s) | A_rich {Ar:+.3f} +- {sr:.3f} ({Ar / sr:+.2f} s; chi2 {xr:.1f}/7 p {CHI2.sf(xr, 7):.1e})")
        P(f"  [{mode}] dA = A_rich - A_poor = {dA:+.3f} +- {sdA:.3f} ({dA / sdA:+.2f} s); verdict: {v}")
        out[mode] = dict(A=[Ap, Am, Ar], s=[sp, sm, sr], chi2=[xp, xm, xr], dA=dA, sdA=sdA, verdict=v)
    out["gate"] = gX
    # late-type check (reported): late rich vs late poor, relative to all late, in template units
    lres = {}
    for mode in ("unmatched", "matched"):
        wp = match_weights(lpoor, LATE)[0] if mode == "matched" else None
        wr = match_weights(lrich, LATE)[0] if mode == "matched" else None
        Ap, rp, _ = amp_of(lpoor, wp); Ar, rr, _ = amp_of(lrich, wr)
        lres[mode] = (Ar - Ap, jsig(rr - rp))
    P(f"  late-type check (reported): A(late rich) - A(late poor) = unmatched {lres['unmatched'][0]:+.3f} +- {lres['unmatched'][1]:.3f}, "
      f"matched {lres['matched'][0]:+.3f} +- {lres['matched'][1]:.3f}")
    out["late_dA"] = lres
    # R-TRACE (post hoc, reported only; added after the first run): does X trace environment at all?  Pooled outer-bin (0-7) ESD
    # ratio, log10[(sum w WG / sum w WW)_rich / (...)_poor], matched weights, jackknife over patches.
    wp = match_weights(poor, EARLY)[0]; wr = match_weights(rich, EARLY)[0]

    def pooled(m, w):
        g = np.zeros(NPAT); v = np.zeros(NPAT)
        np.add.at(g, patch[m], (w * WGo)[m]); np.add.at(v, patch[m], (w * WWo)[m])
        return g.sum() / v.sum(), (g.sum() - g) / (v.sum() - v)
    (fr, lr_), (fp, lp_) = pooled(rich, wr), pooled(poor, wp)
    tr, trr = np.log10(fr / fp), np.log10(lr_ / lp_)
    P(f"  R-TRACE (post hoc, reported): outer bins 0-7, matched, log10 ESD(rich)/ESD(poor) = {tr:+.3f} +- {jsig(trr):.3f} dex "
      f"({tr / jsig(trr):+.2f} s)")
    out["trace_outer"] = (float(tr), jsig(trr))
    sp_m = out["matched"]["s"][0]
    pw = 1 / sp_m
    P(f"  R0 power (matched): 1/s_A(poor) = {pw:.2f}, 1/s_A(rich) = {1 / out['matched']['s'][2]:.2f}; "
      f"P(FAIL | A_poor = 1) ~ {norm.cdf(pw - 3):.2f}; P(|z_poor| < 2 | A_poor = 0) ~ {norm.cdf(2) - norm.cdf(-2):.2f}"
      + ("  -> UNDERPOWERED to FAIL" if pw < 3 else ""))
    out["power"] = dict(inv_s_poor=pw, inv_s_rich=1 / out["matched"]["s"][2], underpowered_to_fail=bool(pw < 3))
    if out["matched"]["verdict"].split(" (")[0] != out["unmatched"]["verdict"].split(" (")[0]:
        P(f"  FLAG: matched and unmatched verdicts disagree")
    RES[E] = out
    # C5: null calibration (100 random equal thirds of the early types), matched
    if E == "E1":
        rngn = np.random.default_rng(446)
        zz = []
        ie = np.where(EARLY)[0]
        for t in range(100):
            o = ie[rngn.permutation(len(ie))]; n = len(o)
            a = np.zeros(NL, bool); b = np.zeros(NL, bool); a[o[: n // 3]] = True; b[o[2 * n // 3:]] = True
            wa = match_weights(a, EARLY)[0]; wb = match_weights(b, EARLY)[0]
            A1, r1, _ = amp_of(a, wa); A2, r2, _ = amp_of(b, wb)
            zz.append((A2 - A1) / jsig(r2 - r1))
        zz = np.array(zz)
        check("C5 CONTROL: null calibration -- std of dA/s_dA over 100 random equal thirds (matched) in [0.7, 1.3]",
              f"std {zz.std():.3f}, mean {zz.mean():+.3f}, fraction |z| >= 1: {np.mean(np.abs(zz) >= 1):.2f}", 0.7 <= zz.std() <= 1.3)
        R.num("C5", dict(std=float(zz.std()), mean=float(zz.mean())))

R.banner("M1 / VERDICTS")
m1 = {E: abs(RES[E]["matched"]["dA"]) / RES[E]["matched"]["sdA"] for E in RES}
check("M1 (load-bearing in MUTATE only): the poor/rich contrast is present, |dA_matched|/s >= 1, E1 and E2",
      "; ".join(f"{E}: {m1[E]:.2f} s" for E in m1), all(v >= 1 for v in m1.values()), load_bearing=MUTATE)
head = "E1" if RES["E1"]["gate"] >= 0.5 else "E2"
P(f"  E1 verdict (matched): {RES['E1']['matched']['verdict']}   [unmatched: {RES['E1']['unmatched']['verdict']}]")
P(f"  E2 verdict (matched): {RES['E2']['matched']['verdict']}   [unmatched: {RES['E2']['unmatched']['verdict']}]")
P(f"  HEADLINE (frozen rule: E1 if it passes gate G, else E2): {head} -> {RES[head]['matched']['verdict']}"
  + ("  [UNDERPOWERED to FAIL]" if RES[head]["power"]["underpowered_to_fail"] else ""))
P("  LCDM also predicts richer centrals lens more: SUPPORTED would not discriminate the framework from LCDM.")
R.num("RES", RES); R.num("headline", dict(measure=head, verdict=RES[head]["matched"]["verdict"]))
R.num("C1", dict(D=Dfull.tolist(), chi2=x2full)); R.num("C3", c3); R.num("AB_law", AB)
nf = R.write(HERE)
sys.exit(1 if nf else 0)
