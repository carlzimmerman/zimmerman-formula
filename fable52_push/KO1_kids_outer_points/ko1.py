#!/usr/bin/env python3
"""KO1: are KiDS's outer points the lens's own field?   Criteria: FROZEN_CRITERIA.md (b1b91fae33), committed alone first;
AMENDMENT_A1.md (ae28af31fa): KA5's expectation by brute force, R4's chance level from shuffled positions.

Run (from this folder, one thread):
    python3 ko1.py              -> ko1.json, ko1.out
    python3 ko1.py --mutate     -> ko1_MUTATE.json, ko1_MUTATE.out
Optional: KO1_CACHE=<file.npz outside the repo> keeps the catalogue scans between the two runs.
Inputs are the staged, git-ignored files under real_research/data/lensing_rar/.  The shear catalogue is not read.
kappa = 1/2 FITTED; not theory closed.  Adopts nothing.
"""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import json, math, time
import numpy as np
from scipy.spatial import cKDTree

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
DATA = os.path.join(REPO, "real_research", "data", "lensing_rar")
B21 = os.path.join(DATA, "brouwer2021_rar")
MUTATE = "--mutate" in sys.argv
TAG = "ko1_MUTATE" if MUTATE else "ko1"
CACHE = os.environ.get("KO1_CACHE", "")
T0 = time.time()
OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(s)
CHK = {}
def check(name, ok, msg):
    CHK[name] = bool(ok); P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {msg}")

# ------------------------------------------------------------------ constants (the stage script's own, so bins agree)
G = 6.674e-11; Msun = 1.989e30; Mpc = 3.0857e22; c_SI = 2.998e8; H0_SI = 70e3 / Mpc
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
FOOT = ("canonical", "alt")
LINE = 10 ** -0.05                    # the record's KiDS gate line as a factor (0.891)
X_SHARE = 0.11958060485606123 / 0.0215    # SWT1's share, OD / OB
X_CAP = 53.64                         # ten times 5.364 (CFG804's census cap)
NPAT = 50
O = [0, 1, 2, 3]                      # outer bins
SIGMA_M_GATE, SIGMA_M_REP = 0.2, 0.1
SETTINGS = [(0.3, 230.0), (0.3, 115.0), (0.5, 230.0), (0.5, 115.0)]

def nu(y):
    return 0.5 + np.sqrt(0.25 + 1.0 / y)
def glaw(g, a0):
    return nu(g / a0) * g
def DC(z, n=2048):                    # the record's comoving distance (flat, Om 0.3, H0 70), verbatim convention
    zz = np.linspace(0, np.max(z), n); E = np.sqrt(0.3 * (1 + zz) ** 3 + 0.7)
    chi = np.concatenate([[0], np.cumsum(0.5 * (1 / E[1:] + 1 / E[:-1]) * np.diff(zz))]) * (c_SI / H0_SI) / Mpc
    return np.interp(z, zz, chi)
def unitvec(ra_deg, dec_deg):
    ra, dec = np.radians(ra_deg), np.radians(dec_deg)
    return np.c_[np.cos(dec) * np.cos(ra), np.cos(dec) * np.sin(ra), np.sin(dec)]
def fcold(logMs):
    return 10 ** (-0.69 * logMs + 6.63)
def mgal_of(logMs):
    return 10 ** logMs * (1 + fcold(logMs))

# ------------------------------------------------------------------ staged lensing sums
ln = np.load(os.path.join(DATA, "lr_lenses.npz"))
PL = np.load(os.path.join(DATA, "cfg110_perlens.npz"))
WG, WW, NN, EDGES = PL["WG"], PL["WW"], PL["NN"], PL["gbar_edges"]
FL = np.load(os.path.join(DATA, "cfg96_isoflags.npz")); f20, f30 = FL["f20"], FL["f30"]
ST = np.load(os.path.join(DATA, "cfg96_stack.npz")); patch = ST["patch"]
C116 = np.load(os.path.join(DATA, "cfg116_perlens.npz"))
NL = len(ln["ra"]); typ = ln["typ"]; zl = ln["z"]; logMs = ln["logM"]; Mg = ln["Mgal"] * Msun; chil = ln["chi"]
ALL = np.ones(NL, bool)
P(f"KO1 {'MUTATE ' if MUTATE else ''}run.  lenses {NL:,}; W20 {int(f20.sum()):,}; W30 {int(f30.sum()):,}; bins {len(EDGES) - 1}; outer bins O = {O}, "
  f"edges {EDGES[0]:.3e} to {EDGES[4]:.3e} m/s^2")

# KA1 -------------------------------------------------------------------------------------------------------------
P("\nKA1: per-lens sums against cfg96_stack (patch x type x bin)")
dev = 0.0
for tag, m in (("10", ALL), ("20", f20), ("30", f30)):
    for arr, key in ((WG, "wgE_"), (WW, "W_"), (NN, "NN_")):
        S = np.zeros((NPAT, 2, 15)); np.add.at(S, (patch[m], typ[m]), arr[m])
        ref = ST[key + tag]
        dev = max(dev, float(np.max(np.abs(S - ref)) / np.max(np.abs(ref))))
check("KA1 per-lens sums reproduce cfg96_stack (W10, W20, W30) to 1e-9", dev < 1e-9, f"max relative deviation {dev:.2e}")

# ------------------------------------------------------------------ model cells (area-weighted over each lens's annulus)
XG, WGL = np.polynomial.legendre.leggauss(24)
R3 = (3.0 * Mpc) ** 2
def bounds(k, Mg_arr):
    t_lo = G * Mg_arr / EDGES[k + 1]; t_hi = np.minimum(G * Mg_arr / EDGES[k], R3)
    return t_lo, t_hi, t_hi > t_lo
def law_cells(a0, Mg_arr=None):
    Mg_arr = Mg if Mg_arr is None else Mg_arr
    m = np.zeros((len(Mg_arr), len(O)))
    for c, k in enumerate(O):
        t_lo, t_hi, ok = bounds(k, Mg_arr)
        t = t_lo[:, None] + (t_hi - t_lo)[:, None] * (XG[None, :] + 1) / 2
        with np.errstate(divide="ignore", invalid="ignore"):
            f = glaw(G * Mg_arr[:, None] / t, a0)
        m[:, c] = np.where(ok, (f * WGL[None, :]).sum(1) / 2, 0.0)
    return m
def tp_cells(X, Mg_arr=None, quad=False):
    Mg_arr = Mg if Mg_arr is None else Mg_arr
    m = np.zeros((len(Mg_arr), len(O)))
    for c, k in enumerate(O):
        t_lo, t_hi, ok = bounds(k, Mg_arr)
        with np.errstate(divide="ignore", invalid="ignore"):
            if quad:
                t = t_lo[:, None] + (t_hi - t_lo)[:, None] * (XG[None, :] + 1) / 2
                v = ((4 / math.pi) * (1 + X) * G * Mg_arr[:, None] / t * WGL[None, :]).sum(1) / 2
            else:
                v = (4 / math.pi) * (1 + X) * G * Mg_arr * np.log(t_hi / t_lo) / (t_hi - t_lo)
        m[:, c] = np.where(ok, v, 0.0)
    return m
WGo, WWo = WG[:, O].copy(), WW[:, O].copy()
LAW = {f: law_cells(A0[f]) for f in FOOT}
TPS = tp_cells(X_SHARE); TPC = tp_cells(X_CAP)
qd = float(np.max(np.abs(tp_cells(X_CAP, quad=True) / np.where(TPC > 0, TPC, 1) - 1)[TPC > 0]))
nocov = int(((WWo > 0) & (LAW["canonical"] == 0)).sum())
check("numerics: 24-node quadrature against the closed form of the two-phase cell", qd < 1e-6, f"max relative difference {qd:.1e}")
check("coverage: no cell holds pairs outside its modelled annulus", nocov == 0, f"{nocov} cells with weight and no model")

def psum(arr, mask):
    pm = patch[mask]; a = arr[mask]
    return np.stack([np.bincount(pm, weights=a[:, c], minlength=NPAT) for c in range(arr.shape[1])], axis=1)
def amp(mask, Mo, WGx=None, WWx=None, cols=None, sk=None):
    """Amplitude of the stack of `mask` against the cell model Mo over the columns `cols` of O; jackknife over 50 patches."""
    WGx = WGo if WGx is None else WGx; WWx = WWo if WWx is None else WWx
    cols = list(range(len(O))) if cols is None else cols
    Sg = psum(WGx, mask)[:, cols]; Sw = psum(WWx, mask)[:, cols]; Sm = psum(WWx * Mo, mask)[:, cols]
    tg, tw, tm = Sg.sum(0), Sw.sum(0), Sm.sum(0)
    D = 4 * G * tg / tw; M = tm / tw
    Dl = 4 * G * (tg - Sg) / (tw - Sw); Ml = (tm - Sm) / (tw - Sw)
    if sk is None:
        sk = np.sqrt((NPAT - 1) / NPAT * ((Dl - Dl.mean(0)) ** 2).sum(0))
    A = float((D * M / sk ** 2).sum() / (M * M / sk ** 2).sum())
    Al = (Dl * Ml / sk ** 2).sum(1) / (Ml * Ml / sk ** 2).sum(1)
    s = float(np.sqrt((NPAT - 1) / NPAT * ((Al - Al.mean()) ** 2).sum()))
    return dict(A=A, s=s, Al=Al, D=D, M=M, sk=sk, n=int(mask.sum()), wshare=float(tw.sum() / WWo[:, cols].sum()))
def amp_model(mask, Mnum, Mden, sk, cols=None):
    cols = list(range(len(O))) if cols is None else cols
    tw = WWo[mask][:, cols].sum(0)
    a = (WWo[mask] * Mnum[mask])[:, cols].sum(0) / tw; b = (WWo[mask] * Mden[mask])[:, cols].sum(0) / tw
    return float((a * b / sk ** 2).sum() / (b * b / sk ** 2).sum())
def jdiff(r1, r2):
    d = r1["Al"] - r2["Al"]
    return float(r1["A"] - r2["A"]), float(np.sqrt((NPAT - 1) / NPAT * ((d - d.mean()) ** 2).sum()))
def label_of(A, s, cap):
    if s > 0.20: return "NO POWER"
    hi, lo = A + 2 * s, A - 2 * s
    if hi >= LINE and lo > cap: return "LAW LEVEL HOLDS"
    if hi < LINE and lo <= cap: return "BELOW THE LAW, TWO-PHASE WINDOW"
    if hi < LINE and lo > cap: return "BELOW THE LAW, BETWEEN"
    return "NOT SEPARATED"
def rd(x, n=4):
    return None if x is None else (round(float(x), n) if np.isfinite(x) else None)

# KA3 -------------------------------------------------------------------------------------------------------------
P("\nKA3: amplitude machinery")
r0 = amp(ALL, LAW["canonical"]); r13 = amp(ALL, LAW["canonical"], WGx=WGo * 1.3)
ka3a = abs(r13["A"] / r0["A"] - 1.3) < 1e-12
ka3b = max(abs(amp(ALL, LAW[f], WGx=WWo * LAW[f] / (4 * G))["A"] - 1) for f in FOOT)
rr = amp(ALL, LAW["canonical"]); ka3c = abs(amp(ALL, LAW["canonical"], WGx=WWo * TPC / (4 * G), sk=rr["sk"])["A"] - amp_model(ALL, TPC, LAW["canonical"], rr["sk"]))
check("KA3 WG x 1.3 -> A x 1.3; WG = WW x law -> A = 1; WG = WW x two-phase -> A = A_II", ka3a and ka3b < 1e-12 and ka3c < 1e-12,
      f"scale exact {ka3a}; |A - 1| {ka3b:.1e}; |A - A_II| {ka3c:.1e}")

# KA4 -------------------------------------------------------------------------------------------------------------
P("\nKA4: jackknife calibration on 200 random halvings of W10 (seed 52)")
rng = np.random.default_rng(52); zz = []
for _ in range(200):
    h = rng.random(NL) < 0.5
    a, b = amp(h, LAW["canonical"]), amp(~h, LAW["canonical"])
    zz.append((a["A"] - b["A"]) / math.hypot(a["s"], b["s"]))
zstd = float(np.std(zz))
check("KA4 std of z over random halvings in [0.8, 1.2]", 0.8 <= zstd <= 1.2, f"std {zstd:.3f}, mean {np.mean(zz):+.3f}")

# ------------------------------------------------------------------ the catalogue: isolation rebuild (KA2) and hosts
def scan(Lx, Lchi, LlogM, Lself, chord, Px, Pchi, PlogM, tree, dmass, strict, wins=(), hist_edges=None, CH=400):
    """Per lens: min |chi_j - chi_l| over pool objects j != self with log M*_j > (or >=) log M*_l + dmass and chord <= chord_l;
    counts inside each window of `wins`; optional histogram of |dchi| of all qualifying pairs."""
    n = len(Lchi); dmin = np.full(n, np.inf)
    cnt = {w: np.zeros(n, np.int64) for w in wins}
    H = np.zeros(len(hist_edges) - 1) if hist_edges is not None else None
    for i0 in range(0, n, CH):
        i1 = min(i0 + CH, n)
        lists = tree.query_ball_point(Lx[i0:i1], r=chord[i0:i1])
        c = np.fromiter((len(x) for x in lists), dtype=np.int64, count=len(lists))
        tot = int(c.sum())
        if tot == 0: continue
        k = np.repeat(np.arange(len(c)), c)
        j = np.fromiter((jj for x in lists for jj in x), dtype=np.int64, count=tot)
        li = i0 + k
        keep = j != Lself[li]
        keep &= (PlogM[j] > LlogM[li] + dmass) if strict else (PlogM[j] >= LlogM[li] + dmass)
        li, j = li[keep], j[keep]
        dc = np.abs(Pchi[j] - Lchi[li])
        np.minimum.at(dmin, li, dc)
        for w in wins:
            np.add.at(cnt[w], li[dc < w], 1)
        if H is not None:
            H += np.histogram(dc, bins=hist_edges)[0]
    return dmin, cnt, H

HEDGES = np.arange(0.0, 500.0 + 1e-9, 10.0)
CAT = {}
def load_catalogue():
    from astropy.io import fits
    P("\nloading the bright sample")
    HB = fits.open(os.path.join(DATA, "KiDS_DR4_brightsample.fits"), memmap=True); b = HB[1].data
    HL = fits.open(os.path.join(DATA, "KiDS_DR4_brightsample_LePhare.fits"), memmap=True); Lp = HL[1].data
    assert np.array_equal(np.asarray(b["ID"]), np.asarray(Lp["ID"]))
    C = CAT
    C["r"] = np.array(b["MAG_AUTO_CALIB"], dtype="f8"); C["z"] = np.array(b["zphot_ANNz2"], dtype="f8")
    C["masked"] = np.array(b["masked"]).astype(np.int64)
    C["logM"] = np.array(Lp["MASS_MED"], dtype="f8") + 0.15
    C["ur"] = np.array(Lp["MAG_ABS_u"] - Lp["MAG_ABS_r"], dtype="f8")
    C["ra"] = np.array(b["RAJ2000"], dtype="f8"); C["dec"] = np.array(b["DECJ2000"], dtype="f8")
    del b, Lp; HB.close(); HL.close()
    P(f"  {len(C['ra']):,} objects  [{time.time() - T0:.0f} s]")
    pool = (C["r"] < 20) & (C["z"] > 0.1) & (C["z"] < 0.5) & (C["masked"] == 0) & np.isfinite(C["logM"]) & (C["logM"] > 7)
    sel = pool & (C["logM"] < 11.0) & np.isfinite(C["ur"])
    C["ip"] = np.where(pool)[0]; C["il"] = np.where(sel)[0]; C["pos"] = np.searchsorted(C["ip"], C["il"])
    C["zP"] = C["z"][C["ip"]]; C["logMP"] = C["logM"][C["ip"]]; C["chiP"] = DC(C["zP"]); C["xP"] = unitvec(C["ra"][C["ip"]], C["dec"][C["ip"]])
    C["treeP"] = cKDTree(C["xP"])
def isolation(dmass):
    C = CAT; pos = C["pos"]
    return scan(C["xP"][pos], C["chiP"][pos], C["logMP"][pos], pos, 3.0 / C["chiP"][pos], C["xP"], C["chiP"], C["logMP"], C["treeP"], dmass, True, CH=500)[0]
def ka2_numbers(dmin_c):
    C = CAT; il, pos = C["il"], C["pos"]
    I0 = dmin_c >= 10
    same = (int(I0.sum()) == NL)
    if same:
        same = all(np.array_equal(a, ln[k]) for a, k in ((C["ra"][il][I0], "ra"), (C["dec"][il][I0], "dec"), (C["zP"][pos][I0], "z"),
                                                        (mgal_of(C["logMP"][pos][I0]), "Mgal")))
    ok20 = bool(same and np.array_equal((dmin_c >= 20)[I0], f20)); ok30 = bool(same and np.array_equal((dmin_c >= 30)[I0], f30))
    return I0, np.array([len(il), int(I0.sum()), float(same), float(ok20), float(ok30)])

cache = None
if CACHE and os.path.exists(CACHE) and not ("--fresh" in sys.argv):
    cache = dict(np.load(CACHE)); P(f"\ncatalogue scans read from the cache ({len(cache)} arrays)")

if cache is None:
    load_catalogue(); C = CAT
    P("\nKA2: the record's isolation, rebuilt with this lane's loader and pair finder")
    I0, ka2 = ka2_numbers(isolation(-1.0))
    P(f"  isolation scan done  [{time.time() - T0:.0f} s]")
    # ---------------------------------------------------------------- neighbour pool and the host scans
    cat_idx = C["il"][I0]                                         # catalogue row of each lens, in lr_lenses order
    nb = (C["r"] < 20) & (C["z"] >= 0.02) & (C["z"] <= 0.8) & np.isfinite(C["logM"]) & (C["logM"] > 7)
    inb = np.where(nb)[0]
    xN = unitvec(C["ra"][inb], C["dec"][inb]); chiN = DC(C["z"][inb]); logMN = C["logM"][inb]
    selfN = np.searchsorted(inb, cat_idx); assert np.all(inb[selfN] == cat_idx)
    treeN = cKDTree(xN)
    xL = xN[selfN]
    P(f"\nneighbour pool {len(inb):,} (masked = 1: {int((C['masked'][inb] == 1).sum()):,})")
    def rh_of(logM):                                             # the lens's outermost measured radius, physical Mpc
        return np.minimum(3.0, np.sqrt(G * mgal_of(logM) * Msun / 1e-15) / Mpc)
    def chord_of(logM):
        th = rh_of(logM) * (1 + zl) / chil
        return 2 * np.sin(th / 2)
    cache = {"ka2": ka2, "npool": np.array([len(inb), int((C['masked'][inb] == 1).sum())], dtype=float)}
    for dm in (0.3, 0.5):
        dmin, cnt, H = scan(xL, chil, logMs, selfN, chord_of(logMs), xN, chiN, logMN, treeN, dm, False, wins=(115.0, 230.0),
                            hist_edges=HEDGES if dm == 0.3 else None)
        cache[f"dmin_{dm}"] = dmin; cache[f"c115_{dm}"] = cnt[115.0]; cache[f"c230_{dm}"] = cnt[230.0]
        if H is not None: cache["hist_0.3"] = H
        P(f"  host scan Delta {dm}: host-free at W 230 {int((dmin >= 230).sum()):,}, at W 115 {int((dmin >= 115).sum()):,}  [{time.time() - T0:.0f} s]")
        for sh in (+0.1, -0.1):
            lm = logMs + sh
            cache[f"dmin_{dm}_{sh:+.1f}"] = scan(xL, chil, lm, selfN, chord_of(lm), xN, chiN, logMN, treeN, dm, False)[0]
        P(f"  mass-shifted scans done  [{time.time() - T0:.0f} s]")
    cache["rh"] = rh_of(logMs)
    # KA5: synthetic hosts ------------------------------------------------------------------------------------------
    rs = np.random.default_rng(52); pick = rs.choice(NL, 4000, replace=False)
    grp = np.repeat(np.arange(4), 1000)                           # 0 planted host; 1 outside the radius; 2 too light; 3 at |dchi| 300
    th = rh_of(logMs[pick]) * (1 + zl[pick]) / chil[pick]
    fac = np.where(grp == 1, 1.05, 0.5); dchi_s = np.where(grp == 3, 300.0, 50.0); dms = np.where(grp == 2, 0.29, 0.6)
    x0 = xL[pick]; ref = np.cross(x0, np.array([0.0, 0.0, 1.0])); ref /= np.linalg.norm(ref, axis=1)[:, None]
    ref2 = np.cross(x0, ref); ang = rs.uniform(0, 2 * math.pi, 4000)
    tdir = np.cos(ang)[:, None] * ref + np.sin(ang)[:, None] * ref2
    xs = np.cos(fac * th)[:, None] * x0 + np.sin(fac * th)[:, None] * tdir
    xA = np.vstack([xN, xs]); chiA = np.concatenate([chiN, chil[pick] + dchi_s]); logMA = np.concatenate([logMN, logMs[pick] + dms])
    dA = scan(xL[pick], chil[pick], logMs[pick], selfN[pick], chord_of(logMs)[pick], xA, chiA, logMA, cKDTree(xA), 0.3, False)[0]
    before = cache["dmin_0.3"][pick]
    # A1: the expectation by brute force over all (picked lens, synthetic object) pairs, independent of the tree
    ch_l = chord_of(logMs)[pick]; expect = before.copy()
    for i0 in range(0, 4000, 500):
        sl = slice(i0, i0 + 500)
        dist = np.linalg.norm(x0[sl][:, None, :] - xs[None, :, :], axis=2)
        q = (dist <= ch_l[sl][:, None]) & ((logMs[pick][None, :] + dms[None, :]) >= logMs[pick][sl][:, None] + 0.3)
        dch = np.abs((chil[pick] + dchi_s)[None, :] - chil[pick][sl][:, None])
        expect[sl] = np.minimum(before[sl], np.where(q, dch, np.inf).min(axis=1))
    ka5a = bool(np.allclose(dA, expect, rtol=0, atol=1e-6))
    ka5b = bool(np.all(dA[grp == 0] <= 50.0 + 1e-6))
    ncross = int((expect < np.where(grp == 0, np.minimum(before, 50.0), np.where(grp == 3, np.minimum(before, 300.0), before)) - 1e-9).sum())
    cache["ka5"] = np.array([ka5a, ka5b, ncross, int(((before >= 230) & (dA < 230)).sum())], dtype=float)
    # A1: chance |dchi| histogram from shuffled sky positions (each lens keeps its chi, mass and radius)
    perm = np.random.default_rng(52).permutation(NL)
    dsh, csh, Hs = scan(xL[perm], chil, logMs, selfN[perm], chord_of(logMs), xN, chiN, logMN, treeN, 0.3, False, wins=(115.0, 230.0), hist_edges=HEDGES)
    cache["hist_shuf_0.3"] = Hs; cache["hf_shuf"] = np.array([float((dsh >= 230).mean()), float((dsh >= 115).mean())])
    P(f"  shuffled-position scan done  [{time.time() - T0:.0f} s]")
    if CACHE:
        np.savez(CACHE, **cache); P("catalogue scans saved to the cache")
ka2 = cache["ka2"]
if not MUTATE:
    check("KA2 isolation rebuild reproduces lr_lenses, f20 and f30 exactly", ka2[0] == 605531 and ka2[1] == NL and ka2[2] == 1 and ka2[3] == 1 and ka2[4] == 1,
          f"candidates {int(ka2[0]):,} (record 605,531); isolated {int(ka2[1]):,} (record {NL:,}); rows equal {bool(ka2[2])}; f20 equal {bool(ka2[3])}; f30 equal {bool(ka2[4])}")
    P(f"  neighbour pool {int(cache['npool'][0]):,} objects (masked = 1: {int(cache['npool'][1]):,})")
else:
    if not CAT: load_catalogue()
    P("\nM4: the isolation rebuild with the mass threshold changed to log M* - 0.5")
    _, k4 = ka2_numbers(isolation(-0.5))
    check("M4 the mutated isolation must FAIL KA2", not (k4[1] == NL and k4[2] == 1 and k4[3] == 1 and k4[4] == 1),
          f"isolated {int(k4[1]):,} (record {NL:,}); rows equal {bool(k4[2])}; f20 equal {bool(k4[3])}; f30 equal {bool(k4[4])}")
ka5 = cache["ka5"]
if not MUTATE:
    check("KA5 (A1) synthetic hosts: the finder equals the brute-force expectation, and every planted host is found", bool(ka5[0]) and bool(ka5[1]),
          f"array equal {bool(ka5[0])}; planted hosts found {bool(ka5[1])}; lenses also reached by another lens's object {int(ka5[2])}; host-free lenses flipped {int(ka5[3])}")

# ------------------------------------------------------------------ the cut, from weights only
P("\nthe cut (weights only; WW holds no shear)")
FW = {}
for dm, W in SETTINGS:
    hf = cache[f"dmin_{dm}"] >= W
    FW[(dm, W)] = (float(WWo[hf].sum() / WWo.sum()), int(hf.sum()))
    P(f"  Delta {dm} dex, W {W:.0f} Mpc: host-free {FW[(dm, W)][1]:,} lenses, outer-weight share f_w {FW[(dm, W)][0]:.4f}")
chosen = next((s for s in SETTINGS if FW[s][0] >= 0.20), max(SETTINGS, key=lambda s: FW[s][0]))
dmC, WC = chosen
HF = cache[f"dmin_{dmC}"] >= WC; HO = ~HF
P(f"  chosen by the frozen rule: Delta {dmC}, W {WC:.0f}  (f_w {FW[chosen][0]:.4f}, {FW[chosen][1]:,} lenses)")

# mass-scatter slope b per lens-mass tercile (selected setting)
q1, q2 = np.quantile(logMs, [1 / 3, 2 / 3]); terc = np.digitize(logMs, [q1, q2])
hp = cache[f"dmin_{dmC}_+0.1"] >= WC; hm = cache[f"dmin_{dmC}_-0.1"] >= WC
bt = [float((math.log(hp[terc == t].mean()) - math.log(hm[terc == t].mean())) / 0.2) for t in range(3)]
wt = np.array([WWo[HF & (terc == t)].sum() for t in range(3)]); wt = wt / wt.sum()
b_eff = float((wt * np.array(bt)).sum())
def corr_fac(sig):
    return 10 ** (b_eff * sig ** 2 / 2)
P(f"  mass-scatter slope b = d ln P(host-free) / d log M*: terciles {[round(x, 2) for x in bt]}, outer-weight shares {[round(float(x), 3) for x in wt]}, "
  f"effective {b_eff:.2f} per dex -> e = {b_eff * SIGMA_M_GATE ** 2:.3f} dex at sigma_M 0.2, factor {corr_fac(SIGMA_M_GATE):.3f} "
  f"(sigma_M 0.1: {corr_fac(SIGMA_M_REP):.3f})")

# ------------------------------------------------------------------ MUTATE variants of the data
WGrun = {f: WGo for f in FOOT}; HFrun = HF
MUT = {}
if MUTATE:
    P("\nMUTATE variants")
    cellid = typ * 6 + terc * 2 + (zl > np.median(zl))
    rngm = np.random.default_rng(52); HFp = HF.copy()
    for cid in np.unique(cellid):
        ii = np.where(cellid == cid)[0]; HFp[ii] = HF[ii][rngm.permutation(len(ii))]
    MUT["HFp"] = HFp

# ------------------------------------------------------------------ primary statistic
RES = dict(lane="KO1", criteria="b1b91fae33", amendment="ae28af31fa", mutate=MUTATE, constants=dict(G=G, Msun=Msun, Mpc=Mpc, line=LINE, X_share=X_SHARE, X_cap=X_CAP),
           outer_bins=O, gbar_edges_outer=[float(x) for x in EDGES[:5]], settings=[dict(delta=d, W=w, f_w=FW[(d, w)][0], n=FW[(d, w)][1]) for d, w in SETTINGS],
           chosen=dict(delta=dmC, W=WC), b_terciles=bt, b_eff=b_eff, corr_factor_gate=corr_fac(SIGMA_M_GATE), corr_factor_rep=corr_fac(SIGMA_M_REP), foot={})
WX = C116["WX"][:, O]
wdev = float(np.max(np.abs(C116["WWn"] + C116["WWf"] - WW)) / np.max(WW))
check("cfg116 near + far weights equal the cfg110 weights (so WX shares WW)", wdev < 1e-9, f"max relative deviation {wdev:.1e}")
def primary(foot, WGx, hf, tag=""):
    L = LAW[foot]
    r = amp(hf, L, WGx=WGx); h = amp(~hf, L, WGx=WGx); w10 = amp(ALL, L, WGx=WGx)
    aS = amp_model(hf, TPS, L, r["sk"]); aC = amp_model(hf, TPC, L, r["sk"])
    cf = corr_fac(SIGMA_M_GATE)
    l1 = label_of(r["A"], r["s"], aC); l2 = label_of(r["A"] * cf, r["s"] * cf, aC)
    lab = l1 if l1 == l2 else "NOT SEPARATED"
    if l1 == "NO POWER": lab = "NO POWER"
    d, sd = jdiff(h, r)
    return dict(r=r, h=h, w10=w10, A_II_share=aS, A_II_cap=aC, label_raw=l1, label_corr=l2, label=lab, diff=d, sdiff=sd)

for foot in FOOT:
    P(f"\n================ footing {foot} (a0 {A0[foot]:.4e})")
    if not MUTATE:
        pr = primary(foot, WGo, HF)
        r, h, w10 = pr["r"], pr["h"], pr["w10"]
        x = amp(HF, LAW[foot], WGx=WX, sk=r["sk"])
        nullok = abs(x["A"]) <= 2.5 * x["s"]
        check(f"cross-shear null, host-free, O ({foot})", nullok, f"A_x {x['A']:+.3f} +- {x['s']:.3f}")
        P(f"  W10 stack     A {w10['A']:.3f} +- {w10['s']:.3f}   ({w10['n']:,} lenses)")
        P(f"  hosted        A {h['A']:.3f} +- {h['s']:.3f}   ({h['n']:,} lenses, weight share {h['wshare']:.3f})")
        P(f"  HOST-FREE     A_hf {r['A']:.3f} +- {r['s']:.3f}   ({r['n']:,} lenses, weight share {r['wshare']:.3f})")
        P(f"     per bin g_obs / law: {[round(float(a / b), 3) for a, b in zip(r['D'], r['M'])]}  +- {[round(float(a / b), 3) for a, b in zip(r['sk'], r['M'])]}")
        P(f"     W10 per bin        : {[round(float(a / b), 3) for a, b in zip(w10['D'], w10['M'])]}  +- {[round(float(a / b), 3) for a, b in zip(w10['sk'], w10['M'])]}")
        P(f"  hosted - host-free    {pr['diff']:+.3f} +- {pr['sdiff']:.3f}  ({pr['diff'] / pr['sdiff']:+.2f} sigma)")
        P(f"  two-phase exterior    A_II {pr['A_II_share']:.4f} (share X {X_SHARE:.3f}), {pr['A_II_cap']:.4f} (cap X {X_CAP})")
        cf = corr_fac(SIGMA_M_GATE)
        P(f"  mass-scatter corrected A_hf^c {r['A'] * cf:.3f} +- {r['s'] * cf:.3f} (sigma_M 0.2); {r['A'] * corr_fac(SIGMA_M_REP):.3f} (sigma_M 0.1)")
        P(f"  label raw: {pr['label_raw']};  corrected: {pr['label_corr']}")
        F = dict(A_w10=w10["A"], s_w10=w10["s"], A_hosted=h["A"], s_hosted=h["s"], n_hosted=h["n"], A_hf=r["A"], s_hf=r["s"], n_hf=r["n"],
                 wshare_hf=r["wshare"], per_bin_hf=[float(a / b) for a, b in zip(r["D"], r["M"])], per_bin_hf_err=[float(a / b) for a, b in zip(r["sk"], r["M"])],
                 per_bin_w10=[float(a / b) for a, b in zip(w10["D"], w10["M"])], per_bin_w10_err=[float(a / b) for a, b in zip(w10["sk"], w10["M"])],
                 g_obs_hf=[float(v) for v in r["D"]], g_law_hf=[float(v) for v in r["M"]],
                 diff_hosted_minus_hf=pr["diff"], s_diff=pr["sdiff"], A_II_share=pr["A_II_share"], A_II_cap=pr["A_II_cap"],
                 A_hf_corr=r["A"] * cf, s_hf_corr=r["s"] * cf, A_hf_corr_rep=r["A"] * corr_fac(SIGMA_M_REP),
                 cross_null=dict(A=x["A"], s=x["s"], ok=bool(nullok)), label_raw=pr["label_raw"], label_corr=pr["label_corr"])
        # ---------------- reported
        rep = {}
        sh = {"W10 not W20": ~f20, "W20 not W30": f20 & ~f30, "W30": f30}
        rep["R1_shells"] = {k: (lambda q: dict(A=q["A"], s=q["s"], n=q["n"]))(amp(m, LAW[foot])) for k, m in sh.items()}
        da, sa = jdiff(amp(~f20, LAW[foot]), amp(f30, LAW[foot])); rep["R1_shell_drop"] = dict(diff=da, s=sa)
        P("  R1 isolation shells: " + "; ".join(f"{k} {v['A']:.3f} +- {v['s']:.3f} ({v['n']:,})" for k, v in rep["R1_shells"].items())
          + f";  (W10 not W20) - W30 = {da:+.3f} +- {sa:.3f}")
        sub = {"late": HF & (typ == 0), "early": HF & (typ == 1), "mass tercile 1": HF & (terc == 0), "mass tercile 2": HF & (terc == 1),
               "mass tercile 3": HF & (terc == 2), "z low half": HF & (zl <= np.median(zl)), "z high half": HF & (zl > np.median(zl))}
        rep["R2_subsets"] = {}
        for k, m in sub.items():
            q = amp(m, LAW[foot]); rep["R2_subsets"][k] = dict(A=q["A"], s=q["s"], n=q["n"], wshare=q["wshare"])
        q3 = amp(HF, LAW[foot], cols=[0, 1, 2]); rep["R2_three_lowest_bins"] = dict(A=q3["A"], s=q3["s"],
                                                                                 A_II_cap=amp_model(HF, TPC, LAW[foot], q3["sk"], cols=[0, 1, 2]))
        w10t = {k: amp(ALL & (typ == t), LAW[foot]) for k, t in (("late", 0), ("early", 1))}
        rep["R2_w10_by_type"] = {k: dict(A=v["A"], s=v["s"]) for k, v in w10t.items()}
        P("  R2 host-free subsets: " + "; ".join(f"{k} {v['A']:.3f} +- {v['s']:.3f}" for k, v in rep["R2_subsets"].items()))
        P(f"     W10 by type: late {w10t['late']['A']:.3f} +- {w10t['late']['s']:.3f}, early {w10t['early']['A']:.3f} +- {w10t['early']['s']:.3f};"
          f"  three lowest bins A_hf {q3['A']:.3f} +- {q3['s']:.3f} (A_II cap {rep['R2_three_lowest_bins']['A_II_cap']:.3f})")
        nh = cache[f"c{int(WC)}_{dmC}"]
        rep["R3_by_host_count"] = {}
        for lab_, m in (("0", nh == 0), ("1", nh == 1), ("2", nh == 2), ("3+", nh >= 3)):
            q = amp(m, LAW[foot]); rep["R3_by_host_count"][lab_] = dict(A=q["A"], s=q["s"], n=q["n"])
        P("  R3 A by number of hosts: " + "; ".join(f"{k}: {v['A']:.3f} +- {v['s']:.3f} ({v['n']:,})" for k, v in rep["R3_by_host_count"].items()))
        WWn, WWf = C116["WWn"][:, O], C116["WWf"][:, O]
        qn = amp(HF, LAW[foot], WGx=C116["WGn"][:, O], WWx=WWn); qf = amp(HF, LAW[foot], WGx=C116["WGf"][:, O], WWx=WWf)
        rep["R5_near_far"] = dict(near=dict(A=qn["A"], s=qn["s"]), far=dict(A=qf["A"], s=qf["s"]))
        P(f"  R5 host-free, near sources {qn['A']:.3f} +- {qn['s']:.3f}; far sources {qf['A']:.3f} +- {qf['s']:.3f}")
        rep["all_settings"] = {}
        for dm, W in SETTINGS:
            m = cache[f"dmin_{dm}"] >= W; q = amp(m, LAW[foot])
            rep["all_settings"][f"{dm}_{int(W)}"] = dict(A=q["A"], s=q["s"], n=q["n"], f_w=FW[(dm, W)][0], A_II_cap=amp_model(m, TPC, LAW[foot], q["sk"]))
        P("  all four settings: " + "; ".join(f"({k}) {v['A']:.3f} +- {v['s']:.3f}" for k, v in rep["all_settings"].items()))
        F["reported"] = rep
        RES["foot"][foot] = F
    else:
        F = {}
        # M1 permuted flags
        p1 = primary(foot, WGo, MUT["HFp"]); pt = primary(foot, WGo, HF)
        z_true = pt["diff"] / pt["sdiff"]; z_perm = p1["diff"] / p1["sdiff"]
        power = abs(z_true) >= 2
        check(f"M1 permuted host-free flags: hosted - host-free inside 2 sigma ({foot})", abs(z_perm) < 2,
              f"permuted {p1['diff']:+.3f} +- {p1['sdiff']:.3f} ({z_perm:+.2f} sigma); true {pt['diff']:+.3f} +- {pt['sdiff']:.3f} ({z_true:+.2f} sigma)"
              + ("" if power else "  [the true difference is inside 2 sigma: M1 has no power]"))
        F["M1"] = dict(diff_perm=p1["diff"], s_perm=p1["sdiff"], diff_true=pt["diff"], s_true=pt["sdiff"], has_power=bool(power))
        # M2 injected deficit
        W2 = WGo.copy(); W2[HF] *= 0.4; p2 = primary(foot, W2, HF)
        check(f"M2 host-free signal x 0.4 -> BELOW THE LAW ({foot})", p2["label"].startswith("BELOW THE LAW"), f"A_hf {p2['r']['A']:.3f} +- {p2['r']['s']:.3f}; label {p2['label']}")
        F["M2"] = dict(A=p2["r"]["A"], s=p2["r"]["s"], label=p2["label"])
        # M3 injected law
        W3 = WGo.copy(); W3[HF] = (WWo * LAW[foot] / (4 * G))[HF]; p3 = primary(foot, W3, HF)
        check(f"M3 host-free signal = the law -> LAW LEVEL HOLDS ({foot})", p3["label"] == "LAW LEVEL HOLDS", f"A_hf {p3['r']['A']:.6f} +- {p3['r']['s']:.1e}; label {p3['label']}")
        F["M3"] = dict(A=p3["r"]["A"], s=p3["r"]["s"], label=p3["label"])
        RES["foot"][foot] = F

# ------------------------------------------------------------------ R4 and the published tables (not footing-dependent / both footings)
if not MUTATE:
    H = cache["hist_0.3"]; Hs = cache["hist_shuf_0.3"]; cen = 0.5 * (HEDGES[1:] + HEDGES[:-1])
    exc = H - Hs
    tot_exc = float(exc.sum()); in230 = float(exc[cen < 230].sum()); in115 = float(exc[cen < 115].sum())
    P(f"\nR4 (A1) |dchi| of more massive (>= 0.3 dex) pool objects inside R_h: {H.sum():,.0f} pairs around the lenses, {Hs.sum():,.0f} around shuffled positions; "
      f"excess below 500 Mpc {tot_exc:,.0f} = {tot_exc / NL:.3f} per lens; share inside 230 Mpc {in230 / tot_exc:.3f}, inside 115 Mpc {in115 / tot_exc:.3f}; "
      f"host-free fraction {HF.mean():.3f} against {cache['hf_shuf'][0]:.3f} for shuffled positions")
    RES["R4"] = dict(pairs=float(H.sum()), pairs_shuffled=float(Hs.sum()), excess_lt500=tot_exc, excess_per_lens=tot_exc / NL,
                     share_inside_230=in230 / tot_exc, share_inside_115=in115 / tot_exc, hostfree_fraction=float(HF.mean()),
                     hostfree_fraction_shuffled=float(cache["hf_shuf"][0]), hist=[float(v) for v in H], hist_shuffled=[float(v) for v in Hs])

    # ---- published tables
    KG4 = 4 * G * Msun / (3.0857e16) ** 2                      # 4 G x (1 Msun/pc^2) in m/s^2
    def rd_esd(fn):
        a = np.loadtxt(os.path.join(B21, fn)); a = a[np.argsort(a[:, 0])]
        return a[:, 0], KG4 * a[:, 1] / a[:, 4], KG4 * a[:, 3] / a[:, 4]
    def rd_cov(fn):
        a = np.loadtxt(os.path.join(B21, fn)); mu = np.unique(a[:, 0]); ru = np.unique(a[:, 2])
        n = len(mu) * len(ru); C = np.zeros((n, n))
        i = np.searchsorted(mu, a[:, 0]) * len(ru) + np.searchsorted(ru, a[:, 2]); j = np.searchsorted(mu, a[:, 1]) * len(ru) + np.searchsorted(ru, a[:, 3])
        C[i, j] = KG4 ** 2 * a[:, 4] / a[:, 6]
        return C, len(mu), len(ru)
    def amp_pub(g, d, C, a0, nlow=4):                         # g ascending; C in the same ascending order
        o = np.arange(nlow); M = glaw(g[o], a0); Ci = np.linalg.inv(C[np.ix_(o, o)])
        den = float(M @ Ci @ M); return float(M @ Ci @ d[o]) / den, 1 / math.sqrt(den)
    PUB = {}
    gk, dk, ek = rd_esd("Fig-4-5-C1_RAR-KiDS-isolated_Nobins.txt"); Ck, _, _ = rd_cov("Fig-4-5-C1_RAR-KiDS-isolated_covmatrix.txt")
    gg, dg, eg = rd_esd("Fig-4-C1_RAR-GAMA-isolated_Nobins.txt"); Cg, _, _ = rd_cov("Fig-4-C1_RAR-GAMA-isolated_covmatrix.txt")
    gh, dh, eh = rd_esd("Fig-4_RAR-KiDS-isolated_hotgas_Nobins.txt"); Ch, _, _ = rd_cov("Fig-4_RAR-KiDS-isolated_hotgas_covmatrix.txt")
    C9, nm9, nr9 = rd_cov("Fig-9_RAR-KiDS-isolated_Massbins_covmatrix.txt"); CA, nmA, nrA = rd_cov("Fig-A4_RAR-KiDS-all_Massbins_covmatrix.txt")
    cdiag = float(np.max(np.abs(np.sqrt(np.diag(Ck)) / ek - 1)))
    check("published tables: covariance diagonal equals the tabulated errors (KiDS isolated)", cdiag < 0.02, f"max relative difference {cdiag:.1e}")
    P("\nR6 / R7 published tables (B21), four lowest g_bar points, full covariance")
    for foot in FOOT:
        a0 = A0[foot]; q = {}
        q["kids_iso"] = amp_pub(gk, dk, Ck, a0)
        q["gama_iso"] = amp_pub(gg, dg, Cg, a0); q["kids_iso_hotgas"] = amp_pub(gh, dh, Ch, a0)
        ratio = q["gama_iso"][0] / q["kids_iso"][0]
        zgk = (q["gama_iso"][0] - q["kids_iso"][0]) / math.hypot(q["gama_iso"][1], q["kids_iso"][1])
        P(f"  {foot}: KiDS-bright isolated A {q['kids_iso'][0]:.3f} +- {q['kids_iso'][1]:.3f}; GAMA isolated A {q['gama_iso'][0]:.3f} +- {q['gama_iso'][1]:.3f} "
          f"(ratio {ratio:.3f}, difference {zgk:+.2f} sigma, treated as independent); with hot gas in g_bar {q['kids_iso_hotgas'][0]:.3f} +- {q['kids_iso_hotgas'][1]:.3f}")
        mb = {}
        for bnum in range(4):
            gi, di, _ = rd_esd(f"Fig-9_RAR-KiDS-isolated_Massbin-{bnum + 1}.txt"); ga, da_, _ = rd_esd(f"Fig-A4_RAR-KiDS-all_Massbin-{bnum + 1}.txt")
            sl = slice(bnum * nr9, (bnum + 1) * nr9)
            ai = amp_pub(gi, di, C9[sl, sl], a0); aa = amp_pub(ga, da_, CA[sl, sl], a0)
            mb[f"bin{bnum + 1}"] = dict(iso=ai, all=aa, iso_over_all=ai[0] / aa[0])
        P("     isolated / all per mass bin: " + "; ".join(f"{k}: {v['iso'][0]:.2f} +- {v['iso'][1]:.2f} / {v['all'][0]:.2f} +- {v['all'][1]:.2f} = {v['iso_over_all']:.2f}" for k, v in mb.items()))
        # R7: the W10 stack against B21's isolated points, bin by bin (the same g_bar bins)
        w10 = amp(ALL, LAW[foot]); o = np.arange(4)
        r7 = [float(w10["D"][i] / dk[o][i]) for i in range(4)]
        z7 = [float((w10["D"][i] - dk[o][i]) / math.hypot(w10["sk"][i], ek[o][i])) for i in range(4)]
        P(f"     R7 W10 stack / B21 isolated g_obs per outer bin: {[round(v, 3) for v in r7]} (z {[round(v, 2) for v in z7]})")
        PUB[foot] = dict(kids_iso=q["kids_iso"], gama_iso=q["gama_iso"], kids_iso_hotgas=q["kids_iso_hotgas"], gama_over_kids=ratio, z_gama_minus_kids=zgk,
                         massbins=mb, R7_ratio=r7, R7_z=z7)
    RES["published"] = PUB

# ------------------------------------------------------------------ labels
P("\n================ result")
kas_ok = all(v for k, v in CHK.items())
RES["checks"] = CHK
if not MUTATE:
    for foot in FOOT:
        F = RES["foot"][foot]
        l1, l2 = F["label_raw"], F["label_corr"]
        lab = "NO VERDICT" if not kas_ok else ("NO POWER" if l1 == "NO POWER" else (l1 if l1 == l2 else "NOT SEPARATED"))
        F["label"] = lab
        P(f"  KO1 {foot}: {lab}   (A_hf {F['A_hf']:.3f} +- {F['s_hf']:.3f}; corrected {F['A_hf_corr']:.3f} +- {F['s_hf_corr']:.3f}; line {LINE:.3f}; "
          f"two-phase cap {F['A_II_cap']:.3f}, share {F['A_II_share']:.3f})")
    P(f"  checks: {sum(CHK.values())} of {len(CHK)} pass" + ("" if kas_ok else "  -> NO VERDICT: " + ", ".join(k for k, v in CHK.items() if not v)))
else:
    P(f"  MUTATE checks: {sum(CHK.values())} of {len(CHK)} behave as required" + ("" if kas_ok else "  FAILED: " + ", ".join(k for k, v in CHK.items() if not v)))
RES["runtime_s"] = round(time.time() - T0, 1)
P(f"  runtime {RES['runtime_s']} s")
P("\nkappa = 1/2 FITTED; not theory closed. Adopts nothing.")

def clean(o):
    if isinstance(o, dict): return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [clean(v) for v in o]
    if isinstance(o, np.ndarray): return [clean(v) for v in o.tolist()]
    if isinstance(o, (np.floating, float)): return float(o) if np.isfinite(o) else None
    if isinstance(o, (np.integer,)): return int(o)
    if isinstance(o, (np.bool_,)): return bool(o)
    return o
json.dump(clean(RES), open(os.path.join(HERE, TAG + ".json"), "w"), indent=1)
open(os.path.join(HERE, TAG + ".out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if kas_ok else 1)
