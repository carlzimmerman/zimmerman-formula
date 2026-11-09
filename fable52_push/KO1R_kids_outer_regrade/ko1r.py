#!/usr/bin/env python3
"""KO1R: independent regrade of lane KO1 ("are KiDS's outer points the lens's own field?").

Written from fable52_push/KO1_kids_outer_points/FROZEN_CRITERIA.md (committed b1b91fae33) alone.  No KO1 script, json, out or
RESULT file was opened, listed or imported before this lane's own numbers were committed.  Data conventions (catalogue columns,
the record's isolation rebuild, what the per-lens sums are) were read from the record's CFG96 / CFG110 / CFG116 / CFG903 staging
scripts; every line of code here is new.

Inputs (git-ignored, on disk): real_research/data/lensing_rar/ lr_lenses.npz, cfg110_perlens.npz, cfg116_perlens.npz (WX only),
cfg96_isoflags.npz, cfg96_stack.npz, KiDS_DR4_brightsample.fits (+ _LePhare.fits).  The shear catalogue is not read.
Outputs (this folder): ko1r.json, ko1r.out, ko1r_MUTATE.json.
Run: OMP_NUM_THREADS=1 python3 -u ko1r.py        (one thread, well under 1.5 GB, a few minutes)

TEST lane, quarantined, not registered; relabels nothing.  Footings never pooled.
kappa = 1/2 FITTED; not theory closed. Adopts nothing.
"""
import os
import sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import itertools
import json
import math
import resource
import time

import numpy as np
from astropy.io import fits
from scipy.spatial import cKDTree

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
DATA = os.path.join(REPO, "real_research", "data", "lensing_rar")
CLOSE = "kappa = 1/2 FITTED; not theory closed. Adopts nothing."

# the record's constants (the CFG96 / CFG110 staging used these for the g_bar binning, so the model uses them too)
C_SI = 2.998e8; G = 6.674e-11; MSUN = 1.989e30; MPC = 3.0857e22; H0 = 70 * 1e3 / MPC
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
FOOT = ("canonical", "alt")
NPATCH = 50
O_BINS = (0, 1, 2, 3)                       # the four lowest g_bar bins of the staged grid
SETTINGS = ((0.3, 230.0), (0.3, 115.0), (0.5, 230.0), (0.5, 115.0))   # (Delta dex, W Mpc), in the criteria's order
SHIFTS = (0.0, 0.1, -0.1)                   # lens log M* shifts for the mass-scatter control
XS = (5.562, 53.64)                         # two-phase shares
GATE = 0.891                                # the record's KiDS gate line as printed in the criteria
TIE = 1e-9                                  # dex; a decimal tie log M*_j = log M*_l + Delta counts as ">=" (reading choice C3)
G_OUT = 1e-15                               # m/s^2, R_h = min(3 Mpc, sqrt(G Mgal / G_OUT))
SEED = 52

T0 = time.time()
OUT = []


def peak_mb():
    ru = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return ru / 1e6 if sys.platform == "darwin" else ru / 1e3


try:
    import psutil
    _PROC = psutil.Process()

    def cur_mb():
        return _PROC.memory_info().rss / 1e6
except ImportError:
    def cur_mb():
        return peak_mb()


def rss_mb():
    return peak_mb()


def say(s="", log=True):
    s = f"[{time.time() - T0:7.1f} s, {cur_mb():5.0f} MB now, {peak_mb():5.0f} MB peak] {s}"
    print(s, flush=True)
    if log:
        OUT.append(s)


CHK = {}


def check(name, ok, msg):
    CHK[name] = bool(ok)
    say(f"  [{'PASS' if ok else 'FAIL'}] {name}: {msg}")


RES = {"lane": "KO1R", "criteria": "fable52_push/KO1_kids_outer_points/FROZEN_CRITERIA.md (b1b91fae33)",
       "independence": "written from the criteria file alone; no KO1 script or output opened before this lane's commit"}
MUT = {"lane": "KO1R", "part": "MUTATE (M1-M4 of the KO1 criteria)"}


# ======================================================================================================== helpers
def comoving(zarr, n=2048):
    """Comoving distance in Mpc: flat, Omega_m 0.3, H0 70, trapezoid on [0, max z] with n nodes (the record's DC convention)."""
    zz = np.linspace(0, np.max(zarr), n)
    E = np.sqrt(0.3 * (1 + zz) ** 3 + 0.7)
    chi = np.concatenate([[0], np.cumsum(0.5 * (1 / E[1:] + 1 / E[:-1]) * np.diff(zz))]) * (C_SI / H0) / MPC
    return np.interp(zarr, zz, chi)


def unit_xyz(ra_deg, dec_deg):
    a = np.radians(ra_deg)
    d = np.radians(dec_deg)
    return np.c_[np.cos(d) * np.cos(a), np.cos(d) * np.sin(a), np.sin(d)]


def gal_mass(logms):
    """Mgal = M* (1 + 10^(-0.69 log M* + 6.63)), the record's cold-gas recipe."""
    return 10 ** logms * (1 + 10 ** (-0.69 * logms + 6.63))


def pair_chunks(tree, xq, rq, chunk):
    """Pair finder: yields (i0, k, j) for query points xq[i0:i0+chunk]; pool index j lies within chord rq of query i0+k."""
    for i0 in range(0, len(xq), chunk):
        lists = tree.query_ball_point(xq[i0:i0 + chunk], r=rq[i0:i0 + chunk])
        cnt = np.fromiter((len(x) for x in lists), dtype=np.int64, count=len(lists))
        k = np.repeat(np.arange(len(lists)), cnt)
        j = np.fromiter(itertools.chain.from_iterable(lists), dtype=np.int64, count=int(cnt.sum()))
        del lists
        if (i0 // chunk) % 40 == 0:
            say(f"    pair finder: {i0:,}/{len(xq):,} queries", log=False)
        yield i0, k, j


def jk_sigma(rep):
    """Delete-one jackknife sigma over axis 0."""
    n = rep.shape[0]
    return np.sqrt((n - 1) / n * ((rep - rep.mean(0)) ** 2).sum(0))


# ======================================================================================================== 1. catalogue + KA2
say("KO1R: independent regrade of KO1, from its frozen criteria alone")
HB = fits.open(os.path.join(DATA, "KiDS_DR4_brightsample.fits"), memmap=True)
HL = fits.open(os.path.join(DATA, "KiDS_DR4_brightsample_LePhare.fits"), memmap=True)
bs, lp = HB[1].data, HL[1].data
assert np.array_equal(np.asarray(bs["ID"]), np.asarray(lp["ID"]))
rmag = np.array(bs["MAG_AUTO_CALIB"], dtype="f8")
zph = np.array(bs["zphot_ANNz2"], dtype="f8")
masked = np.array(bs["masked"]).astype(np.int64)
logMs = np.array(lp["MASS_MED"], dtype="f8") + 0.15
u_r = np.array(lp["MAG_ABS_u"] - lp["MAG_ABS_r"], dtype="f8")
ra = np.array(bs["RAJ2000"], dtype="f8")
dec = np.array(bs["DECJ2000"], dtype="f8")
del bs, lp
HB.close(); HL.close()
say(f"bright sample {len(ra):,} objects; masked values {sorted(set(np.unique(masked).tolist()))}")

# the record's isolation (KA2): pool r < 20, 0.1 < z < 0.5, masked 0, finite log M* > 7; candidates log M* < 11, finite u - r;
# isolated at W if no pool galaxy with log M* > log M*_lens - 1 inside chord 3 / chi (comoving 3 Mpc) with |dchi| < W.
pool = (rmag < 20) & (zph > 0.1) & (zph < 0.5) & (masked == 0) & np.isfinite(logMs) & (logMs > 7)
cand = pool & (logMs < 11.0) & np.isfinite(u_r)
ipool = np.flatnonzero(pool)
icand = np.flatnonzero(cand)
cpos = np.searchsorted(ipool, icand)
zP, mP = zph[ipool], logMs[ipool]
chiP = comoving(zP)
xP = unit_xyz(ra[ipool], dec[ipool])
NC = len(icand)
treeP = cKDTree(xP)
hit = {W: np.zeros(NC, bool) for W in (10, 20, 30)}
hit_m4 = np.zeros(NC, bool)
npairs_iso = 0
for i0, k, j in pair_chunks(treeP, xP[cpos], 3.0 / chiP[cpos], 4000):
    ii = cpos[i0 + k]
    dchi = np.abs(chiP[ii] - chiP[j])
    q = (j != ii) & (mP[j] > mP[ii] - 1.0)
    npairs_iso += int(q.sum())
    for W in (10, 20, 30):
        hit[W][i0 + k[q & (dchi < W)]] = True
    q4 = (j != ii) & (mP[j] > mP[ii] - 0.5)                 # M4: threshold log M* - 0.5
    hit_m4[i0 + k[q4 & (dchi < 10)]] = True
del treeP
iso = {W: ~hit[W] for W in hit}
say(f"isolation rebuild: candidates {NC:,}, pool {len(ipool):,}, mass-qualified pairs {npairs_iso:,}; isolated W10/20/30 = "
    + " / ".join(f"{int(iso[W].sum()):,}" for W in (10, 20, 30)))

ln_npz = np.load(os.path.join(DATA, "lr_lenses.npz"))
LN = {k: ln_npz[k] for k in ln_npz.files}
ISO = np.load(os.path.join(DATA, "cfg96_isoflags.npz"))
f20_rec, f30_rec = ISO["f20"], ISO["f30"]


def ka2_compare(isolated):
    s = isolated
    fields = {"ra": ra[icand][s], "dec": dec[icand][s], "z": zP[cpos][s], "Mgal": gal_mass(mP[cpos])[s],
              "logM": mP[cpos][s], "typ": np.where(u_r[icand][s] > 2.0, 1, 0), "chi": chiP[cpos][s]}
    eq = {k: bool(len(v) == len(LN[k]) and np.array_equal(v, LN[k])) for k, v in fields.items()}
    return eq


eq2 = ka2_compare(iso[10])
f20_eq = bool(iso[10].sum() == len(f20_rec) and np.array_equal(iso[20][iso[10]], f20_rec))
f30_eq = bool(iso[10].sum() == len(f30_rec) and np.array_equal(iso[30][iso[10]], f30_rec))
ka2 = (NC == 605531) and (int(iso[10].sum()) == 181477) and all(eq2.values()) and f20_eq and f30_eq
check("KA2 isolation rebuild = lr_lenses.npz + f20/f30", ka2,
      f"candidates {NC:,} (605,531), lenses {int(iso[10].sum()):,} (181,477), fields equal {eq2}, f20 {f20_eq}, f30 {f30_eq}")
RES["KA2"] = {"candidates": NC, "lenses": int(iso[10].sum()), "W20": int(iso[20].sum()), "W30": int(iso[30].sum()),
              "fields_equal": eq2, "f20_equal": f20_eq, "f30_equal": f30_eq, "mass_qualified_pairs": npairs_iso, "pass": ka2}
iso_m4 = ~hit_m4
eq_m4 = ka2_compare(iso_m4)
m4_ka2 = (int(iso_m4.sum()) == 181477) and all(eq_m4.values())
MUT["M4"] = {"lenses_with_threshold_minus_0.5": int(iso_m4.sum()), "fields_equal": eq_m4, "KA2_passes": m4_ka2,
             "bites": not m4_ka2}
say(f"M4 (threshold log M* - 0.5): {int(iso_m4.sum()):,} lenses; KA2 would {'PASS (M4 does not bite)' if m4_ka2 else 'FAIL (M4 bites)'}")
lens_rows = icand[iso[10]]                                   # catalogue rows of the 181,477 lenses (= lr_lenses order)
del xP, chiP, zP, mP, hit, hit_m4

# ======================================================================================================== 2. host flags
# neighbour pool: r < 20, 0.02 <= z <= 0.8, finite log M* > 7, masked 0 or 1; the lens itself excluded by catalogue row
nbsel = (rmag < 20) & (zph >= 0.02) & (zph <= 0.8) & np.isfinite(logMs) & (logMs > 7) & np.isin(masked, (0, 1))
inb = np.flatnonzero(nbsel)
xN = unit_xyz(ra[inb], dec[inb])
chiN = comoving(zph[inb])
mN = logMs[inb].copy()
selfN = np.searchsorted(inb, lens_rows)
assert np.all(inb[selfN] == lens_rows)
NL = len(lens_rows)
zl, ml, Mg, chl_rec = LN["z"], LN["logM"], LN["Mgal"], LN["chi"]
chl = chiN[selfN]                                            # lens chi from the same comoving() call as the pool (reading C2)
typ = LN["typ"]
say(f"neighbour pool {len(inb):,} (masked = 1: {int((masked[inb] == 1).sum()):,}); lens self-rows matched; "
    f"max |chi(pool call) - chi(lr_lenses)| = {np.max(np.abs(chl - chl_rec)):.2e} Mpc")
del rmag, zph, masked, logMs, u_r, ra, dec


def r_host(shift):
    M = Mg if shift == 0.0 else gal_mass(ml + shift)
    return np.minimum(3.0, np.sqrt(G * M * MSUN / G_OUT) / MPC)


RH = {s: r_host(s) for s in SHIFTS}


def host_pass(qidx, xpool, chipool, mpool, specs, chunk=1000):
    """Count hosts of lenses qidx (indices into the 181,477) in a pool, for each spec
    (name, Delta, W, shift, chi in {'pool','rec'}, tie).  A host: log M*_j >= log M*_l + shift + Delta (within tie),
    d = theta chi_l / (1 + z_l) <= R_h,l(shift) with theta the great-circle angle, |chi_j - chi_l| < W."""
    tree = cKDTree(xpool)
    rmax = np.max(np.vstack([RH[s["shift"]] for s in specs]), axis=0)
    th_q = rmax[qidx] * (1 + zl[qidx]) / np.minimum(chl, chl_rec)[qidx] * (1 + 1e-9)
    rq = 2 * np.sin(th_q / 2)
    xq = xpool[selfN[qidx]]
    dmin = min(s["Delta"] + s["shift"] for s in specs) - 1e-6
    need_rec = any(s["chi"] == "rec" for s in specs)
    cnt = {s["name"]: np.zeros(len(qidx), np.int64) for s in specs}
    npr = 0
    for i0, k, j in pair_chunks(tree, xq, rq, chunk):
        li = qidx[i0 + k]
        q = (j != selfN[li]) & (mpool[j] - ml[li] >= dmin)
        k, j, li = k[q], j[q], li[q]
        npr += len(k)
        ch = np.sqrt(((xpool[j] - xq[i0 + k]) ** 2).sum(1))
        th = 2 * np.arcsin(np.minimum(ch / 2, 1.0))
        geo = {"pool": (th * chl[li] / (1 + zl[li]), np.abs(chipool[j] - chl[li]))}
        if need_rec:
            geo["rec"] = (th * chl_rec[li] / (1 + zl[li]), np.abs(chipool[j] - chl_rec[li]))
        nq = min(chunk, len(qidx) - i0)
        for s in specs:
            d, dc = geo[s["chi"]]
            h = (mpool[j] >= (ml[li] + s["shift"]) + s["Delta"] - s["tie"]) & (d <= RH[s["shift"]][li]) & (dc < s["W"])
            cnt[s["name"]][i0:i0 + nq] += np.bincount(k[h], minlength=nq)
    return cnt, npr


def sname(D, W, shift=0.0, tag=""):
    return f"D{D}_W{W:g}_s{shift:+.1f}{tag}"


specs = []
for D, W in SETTINGS:
    for s in SHIFTS:
        specs.append(dict(name=sname(D, W, s), Delta=D, W=W, shift=s, chi="pool", tie=TIE))
    specs.append(dict(name=sname(D, W, 0.0, "_strict"), Delta=D, W=W, shift=0.0, chi="pool", tie=0.0))
    specs.append(dict(name=sname(D, W, 0.0, "_chirec"), Delta=D, W=W, shift=0.0, chi="rec", tie=TIE))
ALL = np.arange(NL)
HC, npr_host = host_pass(ALL, xN, chiN, mN, specs)
say(f"host pass: {npr_host:,} candidate pairs (mass-prefiltered) over {NL:,} lenses")

# ======================================================================================================== 3. per-lens sums + KA1
P110 = np.load(os.path.join(DATA, "cfg110_perlens.npz"))
ge = P110["gbar_edges"]
WG, WW, NN = P110["WG"], P110["WW"], P110["NN"]
WX = np.load(os.path.join(DATA, "cfg116_perlens.npz"))["WX"]
ST = np.load(os.path.join(DATA, "cfg96_stack.npz"))
patch = ST["patch"]
edges_ok = np.allclose(ge[:5] / 1e-15, [1.00, 1.76, 3.11, 5.49, 9.69], atol=0.005) and len(ge) == 16
say(f"g_bar edges of O (1e-15 m/s^2): {np.round(ge[:5] / 1e-15, 3).tolist()} (criteria 1.00 1.76 3.11 5.49 9.69: {edges_ok})")

ka1_dev = {}
for W, fl in ((10, np.ones(NL, bool)), (20, f20_rec), (30, f30_rec)):
    for nm, arr, key in (("WG", WG, "wgE"), ("WW", WW, "W"), ("NN", NN, "NN")):
        S = np.zeros((NPATCH, 2, 15))
        np.add.at(S, (patch[fl], typ[fl]), arr[fl])
        ref = ST[f"{key}_{W}"]
        num = np.abs(S - ref)
        rel = np.where(ref != 0, num / np.where(ref != 0, np.abs(ref), 1.0), np.where(num == 0, 0.0, np.inf))
        ka1_dev[f"{nm}_W{W}"] = float(rel.max())
ka1 = max(ka1_dev.values()) <= 1e-9
check("KA1 per-lens sums by patch x type = cfg96_stack (W10/W20/W30)", ka1,
      f"max relative deviation {max(ka1_dev.values()):.2e} (gate 1e-9)")
RES["KA1"] = {"max_rel_dev": ka1_dev, "pass": ka1}

# ======================================================================================================== 4. models on O
GM = G * Mg * MSUN
g_cap = GM / (3.0 * MPC) ** 2                               # pairs end at 3 Mpc physical


def F_law(g, a0):
    """Antiderivative of g_law(g) / g^2 with g_law = nu(g/a0) g, nu(y) = 1/2 + sqrt(1/4 + 1/y)."""
    t = np.sqrt(0.25 + a0 / g)
    tm = (a0 / g) / (t + 0.5)                                # t - 1/2, cancellation-free
    return 0.5 * np.log(g) - 2 * t - 0.5 * np.log(tm / (t + 0.5))


nO = len(O_BINS)
m_law = {f: np.zeros((NL, nO)) for f in FOOT}
m_g = np.zeros((NL, nO))
empty = np.zeros((NL, nO), bool)
for kk, kb in enumerate(O_BINS):
    g1 = np.full(NL, ge[kb + 1])
    g2 = np.maximum(ge[kb], g_cap)
    e = g2 >= g1
    empty[:, kk] = e
    g2s = np.where(e, g1 * 0.5, g2)
    den = 1 / g2s - 1 / g1                                   # (R_hi^2 - R_lo^2) / GM
    m_g[:, kk] = np.where(e, 0.0, np.log(g1 / g2s) / den)
    for f in FOOT:
        m_law[f][:, kk] = np.where(e, 0.0, (F_law(g1, A0[f]) - F_law(g2s, A0[f])) / den)
WWO = WW[:, list(O_BINS)]
empty_ww = float(WWO[empty].sum())
check("K-empty cells beyond 3 Mpc carry no weight", empty_ww == 0.0, f"sum WW over empty (lens, bin) cells = {empty_ww}")
m_II = {X: (4 / math.pi) * (1 + X) * m_g for X in XS}

# quadrature cross-check of the closed-form annulus means
rng_q = np.random.default_rng(SEED)
xg, wg = np.polynomial.legendre.leggauss(96)
qdev = 0.0
for _ in range(400):
    l = int(rng_q.integers(NL)); kk = int(rng_q.integers(nO))
    if empty[l, kk]:
        continue
    R1 = math.sqrt(GM[l] / ge[O_BINS[kk] + 1]); R2 = min(math.sqrt(GM[l] / ge[O_BINS[kk]]), 3.0 * MPC)
    u = 0.5 * (math.log(R2) - math.log(R1)) * xg + 0.5 * (math.log(R2) + math.log(R1))
    R = np.exp(u)
    gN = GM[l] / R ** 2
    for f in FOOT:
        gl = gN * (0.5 + np.sqrt(0.25 + A0[f] / gN))
        val = 0.5 * (math.log(R2) - math.log(R1)) * np.sum(wg * gl * R ** 2) * 2 / (R2 ** 2 - R1 ** 2)
        qdev = max(qdev, abs(val / m_law[f][l, kk] - 1))
    val = 0.5 * (math.log(R2) - math.log(R1)) * np.sum(wg * gN * R ** 2) * 2 / (R2 ** 2 - R1 ** 2)
    qdev = max(qdev, abs(val / m_g[l, kk] - 1))
check("K-model closed form = quadrature (400 random cells)", qdev < 1e-9, f"max relative deviation {qdev:.1e}")

WGO = WG[:, list(O_BINS)]
WXO = WX[:, list(O_BINS)]
WWM = {f: WWO * m_law[f] for f in FOOT}
WWII = {X: WWO * m_II[X] for X in XS}
del WG, WW, NN, WX


def psum(arr, mask):
    pm = patch[mask]
    a = arr[mask]
    return np.stack([np.bincount(pm, weights=a[:, i], minlength=NPATCH) for i in range(a.shape[1])], axis=1)


def amp(mask, foot, Y=None, cols=None, sk=None, wwm=None, want_ii=True):
    """A(S) over bins cols of O: inverse-variance projection of D_k = 4 G ESD_k on the stack law model M_k, s_k the
    delete-one-patch jackknife of D_k; error of A = delete-one-patch jackknife of A with s_k fixed (model recomputed per
    replicate; the fixed-model variant is also returned)."""
    cols = list(range(nO)) if cols is None else list(cols)
    Y = WGO if Y is None else Y
    wwm = WWM[foot] if wwm is None else wwm
    pg, pw, pm = psum(Y[:, cols], mask), psum(WWO[:, cols], mask), psum(wwm[:, cols], mask)
    Tg, Tw, Tm = pg.sum(0), pw.sum(0), pm.sum(0)
    Dk, Mk = 4 * G * Tg / Tw, Tm / Tw
    Dp, Mp = 4 * G * (Tg - pg) / (Tw - pw), (Tm - pm) / (Tw - pw)
    skk = jk_sigma(Dp) if sk is None else sk
    iv = 1 / skk ** 2
    A = float((Dk * Mk * iv).sum() / (Mk * Mk * iv).sum())
    Ap = (Dp * Mp * iv).sum(1) / (Mp * Mp * iv).sum(1)
    Apf = (Dp * Mk * iv).sum(1) / (Mk * Mk * iv).sum()
    out = dict(A=A, s=float(jk_sigma(Ap)), s_fixed_model=float(jk_sigma(Apf)), Ap=Ap, sk=skk, Dk=Dk, Mk=Mk,
               n=int(mask.sum()), wsum=float(Tw.sum()))
    if want_ii:
        out["AII"] = {X: float(((psum(WWII[X][:, cols], mask).sum(0) / Tw) * Mk * iv).sum() / (Mk * Mk * iv).sum())
                      for X in XS}
    return out


def brief(r):
    o = {k: r[k] for k in ("A", "s", "s_fixed_model", "n", "wsum")}
    o["D_k"] = r["Dk"].tolist(); o["M_k"] = r["Mk"].tolist(); o["s_k"] = r["sk"].tolist()
    if "AII" in r:
        o["A_II"] = {str(X): v for X, v in r["AII"].items()}
    return o


def joint_diff(r1, r2):
    """r1['A'] - r2['A'] with the delete-one-patch jackknife of the difference (each side's s_k fixed)."""
    return float(r1["A"] - r2["A"]), float(jk_sigma(r1["Ap"] - r2["Ap"]))


# ======================================================================================================== 5. choice of the cut
WWO_l = WWO.sum(1)
cut_rows = []
chosen = None
for D, W in SETTINGS:
    hf = HC[sname(D, W)] == 0
    fw = float(WWO_l[hf].sum() / WWO_l.sum())
    row = dict(Delta=D, W=W, n_host_free=int(hf.sum()), n_hosted=int((~hf).sum()), f_w=fw,
               n_host_free_strict_ties=int((HC[sname(D, W, 0.0, "_strict")] == 0).sum()),
               n_host_free_chi_lr_lenses=int((HC[sname(D, W, 0.0, "_chirec")] == 0).sum()),
               flags_differ_strict_ties=int(((HC[sname(D, W, 0.0, "_strict")] == 0) != hf).sum()),
               flags_differ_chi_lr_lenses=int(((HC[sname(D, W, 0.0, "_chirec")] == 0) != hf).sum()),
               mean_hosts_of_hosted=float(HC[sname(D, W)][~hf].mean()))
    cut_rows.append(row)
    if chosen is None and fw >= 0.20:
        chosen = (D, W)
    say(f"setting (Delta {D}, W {W:g}): host-free {row['n_host_free']:,} / {NL:,}, f_w = {fw:.4f}; "
        f"flags changed by strict ties {row['flags_differ_strict_ties']}, by lr_lenses chi {row['flags_differ_chi_lr_lenses']}")
if chosen is None:
    chosen = max(SETTINGS, key=lambda dw: [r["f_w"] for r in cut_rows][SETTINGS.index(dw)])
    say(f"no setting reaches f_w 0.20; largest f_w taken: {chosen}")
DSEL, WSEL = chosen
HF = HC[sname(DSEL, WSEL)] == 0
say(f"selected setting (frozen rule): Delta {DSEL}, W {WSEL:g}; host-free {int(HF.sum()):,}")
RES["settings"] = cut_rows
RES["selected"] = {"Delta": DSEL, "W": WSEL, "n_host_free": int(HF.sum())}

# ======================================================================================================== 6. mass-scatter control
terc_edges = np.quantile(ml, [1 / 3, 2 / 3])
terc = np.digitize(ml, terc_edges)
b_t, P_t = [], []
for t in range(3):
    m = terc == t
    P = {s: float((HC[sname(DSEL, WSEL, s)][m] == 0).mean()) for s in SHIFTS}
    P_t.append(P)
    b_t.append((math.log(P[0.1]) - math.log(P[-0.1])) / 0.2)
w_t = np.array([WWO_l[HF & (terc == t)].sum() for t in range(3)])
w_t = w_t / w_t.sum()
MSC = {"tercile_edges_logM": terc_edges.tolist(), "P_host_free": [{f"{s:+.1f}": v for s, v in P.items()} for P in P_t],
       "b": b_t, "host_free_weight_share": w_t.tolist()}
for sig in (0.2, 0.1):
    e_t = [b * sig ** 2 for b in b_t]
    ebar = float(np.dot(w_t, e_t))
    MSC[f"sigma_{sig}"] = {"e_t_dex": e_t, "e_weighted_dex": ebar, "factor_10^(e/2)": 10 ** (ebar / 2)}
say("mass-scatter control: b per tercile = " + " / ".join(f"{b:+.3f}" for b in b_t)
    + f"; e(0.2) = {MSC['sigma_0.2']['e_weighted_dex']:+.5f} dex, factor {MSC['sigma_0.2']['factor_10^(e/2)']:.5f}")
RES["mass_scatter"] = MSC
FAC = MSC["sigma_0.2"]["factor_10^(e/2)"]


# ======================================================================================================== 7. labels
def table_label(A, s, aii53):
    if s > 0.20:
        return "NO POWER"
    hi, lo = A + 2 * s, A - 2 * s
    if hi >= GATE and lo > aii53:
        return "LAW LEVEL HOLDS"
    if hi < GATE and lo <= aii53:
        return "BELOW THE LAW, TWO-PHASE WINDOW"
    if hi < GATE and lo > aii53:
        return "BELOW THE LAW, BETWEEN"
    return "NOT SEPARATED"


def final_label(A, s, aii53, fac, gates_ok):
    l1 = table_label(A, s, aii53)
    l2 = table_label(A * fac, s * fac, aii53)
    if not gates_ok:
        return "NO VERDICT", l1, l2
    return (l1 if l1 == l2 else "NOT SEPARATED"), l1, l2


# ======================================================================================================== 8. KA3, null, KA4, KA5
ALLM = np.ones(NL, bool)
PRIM = {f: amp(HF, f) for f in FOOT}
ka3 = {}
for f in FOOT:
    r13 = amp(HF, f, Y=WGO * 1.3)
    rl = amp(HF, f, Y=WWO * m_law[f] / (4 * G))
    d_ii = {}
    for X in XS:
        rx = amp(HF, f, Y=WWO * m_II[X] / (4 * G))
        d_ii[str(X)] = abs(rx["A"] / rx["AII"][X] - 1)
    ka3[f] = {"scale_1.3_dev": abs(r13["A"] / PRIM[f]["A"] - 1.3) / 1.3, "law_plant_dev": abs(rl["A"] - 1),
              "two_phase_plant_dev": d_ii}
ka3_ok = all(v["scale_1.3_dev"] < 1e-12 and v["law_plant_dev"] < 1e-12 and max(v["two_phase_plant_dev"].values()) < 1e-12
             for v in ka3.values())
check("KA3 scale / law plant / two-phase plant", ka3_ok,
      "; ".join(f"{f}: {v['scale_1.3_dev']:.1e} / {v['law_plant_dev']:.1e} / {max(v['two_phase_plant_dev'].values()):.1e}"
                for f, v in ka3.items()))
RES["KA3"] = {"devs": ka3, "pass": ka3_ok}

NULL = {}
for f in FOOT:
    rx = amp(HF, f, Y=WXO, sk=PRIM[f]["sk"], want_ii=False)
    rx_own = amp(HF, f, Y=WXO, want_ii=False)
    NULL[f] = {"A_x": rx["A"], "s_A_x": rx["s"], "A_x_own_sk": rx_own["A"], "s_A_x_own_sk": rx_own["s"],
               "s_primary": PRIM[f]["s"], "ratio_to_s_primary": abs(rx["A"]) / PRIM[f]["s"],
               "pass": abs(rx["A"]) <= 2.5 * PRIM[f]["s"]}
null_ok = all(v["pass"] for v in NULL.values())
check("Null: cross-shear amplitude of the host-free set within 2.5 s", null_ok,
      "; ".join(f"{f}: A_x {v['A_x']:+.4f} (own jk {v['s_A_x']:.4f}), |A_x|/s = {v['ratio_to_s_primary']:.2f}"
                for f, v in NULL.items()))
RES["null_cross_shear"] = NULL

rng4 = np.random.default_rng(SEED)
zs = {f: [] for f in FOOT}
for it in range(200):
    h = np.zeros(NL, bool)
    h[rng4.permutation(NL)[:NL // 2]] = True
    for f in FOOT:
        r1, r2 = amp(h, f, want_ii=False), amp(~h, f, want_ii=False)
        zs[f].append((r1["A"] - r2["A"]) / math.hypot(r1["s"], r2["s"]))
ka4 = {f: {"std_z": float(np.std(zs[f], ddof=1)), "mean_z": float(np.mean(zs[f]))} for f in FOOT}
ka4_ok = all(0.8 <= v["std_z"] <= 1.2 for v in ka4.values())
check("KA4 jackknife calibration (200 halvings of W10, seed 52)", ka4_ok,
      "; ".join(f"{f}: std z {v['std_z']:.3f}, mean {v['mean_z']:+.3f}" for f, v in ka4.items()))
RES["KA4"] = {"by_footing": ka4, "pass": ka4_ok}

# KA5: synthetic hosts at known offsets around 1,000 host-free lenses, plus three decoys each around 1,000 others
rng5 = np.random.default_rng(SEED)
hf_idx = np.flatnonzero(HF)
pick = rng5.choice(hf_idx, 2000, replace=False)
tgt, dcy = pick[:1000], pick[1000:]


def place(l, d_mpc, psi):
    th = d_mpc * (1 + zl[l]) / chl[l]
    a, dd = np.radians(LN["ra"][l]), np.radians(LN["dec"][l])
    x = xN[selfN[l]]
    east = np.c_[-np.sin(a), np.cos(a), np.zeros_like(a)]
    north = np.c_[-np.sin(dd) * np.cos(a), -np.sin(dd) * np.sin(a), np.cos(dd)]
    v = x * np.cos(th)[:, None] + np.sin(th)[:, None] * (np.cos(psi)[:, None] * east + np.sin(psi)[:, None] * north)
    return v / np.linalg.norm(v, axis=1)[:, None]


sgn = lambda n: np.where(rng5.random(n) < 0.5, -1.0, 1.0)
synth_x, synth_chi, synth_m, synth_kind = [], [], [], []
# true hosts: d = 0.5 R_h, |dchi| = 0.5 W, log M* = lens + Delta + 0.05
synth_x.append(place(tgt, 0.5 * RH[0.0][tgt], rng5.uniform(0, 2 * math.pi, 1000)))
synth_chi.append(chl[tgt] + sgn(1000) * 0.5 * WSEL); synth_m.append(ml[tgt] + DSEL + 0.05); synth_kind += ["host"] * 1000
# decoys: (i) d = 1.05 R_h; (ii) |dchi| = 1.02 W; (iii) log M* = lens + Delta - 0.02
synth_x.append(place(dcy, 1.05 * RH[0.0][dcy], rng5.uniform(0, 2 * math.pi, 1000)))
synth_chi.append(chl[dcy] + sgn(1000) * 0.5 * WSEL); synth_m.append(ml[dcy] + DSEL + 0.05); synth_kind += ["far"] * 1000
synth_x.append(place(dcy, 0.5 * RH[0.0][dcy], rng5.uniform(0, 2 * math.pi, 1000)))
synth_chi.append(chl[dcy] + sgn(1000) * 1.02 * WSEL); synth_m.append(ml[dcy] + DSEL + 0.05); synth_kind += ["deep"] * 1000
synth_x.append(place(dcy, 0.5 * RH[0.0][dcy], rng5.uniform(0, 2 * math.pi, 1000)))
synth_chi.append(chl[dcy] + sgn(1000) * 0.5 * WSEL); synth_m.append(ml[dcy] + DSEL - 0.02); synth_kind += ["light"] * 1000
SX, SCHI, SM = np.vstack(synth_x), np.concatenate(synth_chi), np.concatenate(synth_m)
# each planted object against its own lens: recovered offsets, and whether it is that lens's host by the definition
own = np.concatenate([tgt, dcy, dcy, dcy])
kind = np.array(synth_kind)
ch_own = np.sqrt(((SX - xN[selfN[own]]) ** 2).sum(1))
d_own = 2 * np.arcsin(np.minimum(ch_own / 2, 1.0)) * chl[own] / (1 + zl[own])
q_own = (SM >= ml[own] + DSEL - TIE) & (d_own <= RH[0.0][own]) & (np.abs(SCHI - chl[own]) < WSEL)
own_geo = {kd: {"d_over_Rh_range": [float((d_own / RH[0.0][own])[kind == kd].min()), float((d_own / RH[0.0][own])[kind == kd].max())],
                "dchi_over_W_range": [float((np.abs(SCHI - chl[own]) / WSEL)[kind == kd].min()),
                                      float((np.abs(SCHI - chl[own]) / WSEL)[kind == kd].max())],
                "host_of_own_lens": int(q_own[kind == kd].sum())} for kd in ("host", "far", "deep", "light")}
own_ok = (own_geo["host"]["host_of_own_lens"] == 1000) and all(own_geo[kd]["host_of_own_lens"] == 0 for kd in ("far", "deep", "light"))
say("KA5 placement: " + "; ".join(f"{kd}: d/R_h {v['d_over_Rh_range'][0]:.4f}-{v['d_over_Rh_range'][1]:.4f}, "
                                  f"|dchi|/W {v['dchi_over_W_range'][0]:.4f}-{v['dchi_over_W_range'][1]:.4f}, "
                                  f"host of own lens {v['host_of_own_lens']}/1000" for kd, v in own_geo.items()))
spec5 =[dict(name="ka5", Delta=DSEL, W=WSEL, shift=0.0, chi="pool", tie=TIE)]
HC5, _ = host_pass(hf_idx, np.vstack([xN, SX]), np.concatenate([chiN, SCHI]), np.concatenate([mN, SM]), spec5)
found = set(hf_idx[HC5["ka5"] > 0].tolist())
# brute force over every host-free lens (no tree): which lenses do the synthetic objects host?
xl = xN[selfN[hf_idx]]
expect = np.zeros(len(hf_idx), bool)
for s0 in range(0, len(SM), 20):
    ch = np.sqrt(((xl[None, :, :] - SX[s0:s0 + 20, None, :]) ** 2).sum(2))
    d = 2 * np.arcsin(np.minimum(ch / 2, 1.0)) * (chl[hf_idx] / (1 + zl[hf_idx]))[None, :]
    h = ((SM[s0:s0 + 20, None] >= ml[hf_idx][None, :] + DSEL - TIE) & (d <= RH[0.0][hf_idx][None, :])
         & (np.abs(SCHI[s0:s0 + 20, None] - chl[hf_idx][None, :]) < WSEL))
    expect |= h.any(0)
expect_set = set(hf_idx[expect].tolist())
tgt_all = set(tgt.tolist()) <= found
dcy_flagged = len(set(dcy.tolist()) & found)
dcy_expected = len(set(dcy.tolist()) & expect_set)
extras = len(found - set(tgt.tolist()))
ka5 = tgt_all and (found == expect_set) and (dcy_flagged == dcy_expected) and own_ok
check("KA5 planted hosts flagged where the definition says (finder = brute force)", ka5,
      f"targets flagged {len(set(tgt.tolist()) & found)}/1000; decoy lenses flagged {dcy_flagged} (brute force {dcy_expected}); "
      f"other lenses legitimately hosted by a planted object {extras} (brute force {len(expect_set - set(tgt.tolist()))}); "
      f"finder set = brute-force set: {found == expect_set}")
RES["KA5"] = {"targets_flagged": len(set(tgt.tolist()) & found), "decoy_lenses_flagged": dcy_flagged,
              "decoy_lenses_brute": dcy_expected, "extra_lenses_flagged": extras,
              "finder_equals_brute_force": found == expect_set, "literal_exactly_targets": found == set(tgt.tolist()),
              "own_lens_placement": own_geo, "pass": ka5}
del SX, xl

GATES = {"KA1": ka1, "KA2": ka2, "KA3": ka3_ok, "KA4": ka4_ok, "KA5": ka5, "null": null_ok}
gates_ok = all(GATES.values())
RES["gates"] = GATES

# ======================================================================================================== 9. primary + R1
PRIMARY = {}
for f in FOOT:
    p = PRIM[f]
    lab, l_raw, l_cor = final_label(p["A"], p["s"], p["AII"][53.64], FAC, gates_ok)
    r_all = amp(ALLM, f)
    r_hst = amp(~HF, f)
    dif, sdif = joint_diff(r_hst, p)
    shells = {"W10_not_W20": amp(~f20_rec, f), "W20_not_W30": amp(f20_rec & ~f30_rec, f), "W30": amp(f30_rec, f)}
    br3 = amp(HF, f, cols=(0, 1, 2))
    PRIMARY[f] = {
        "label": lab, "label_raw": l_raw, "label_corrected": l_cor,
        "A_hf": p["A"], "s": p["s"], "s_fixed_model": p["s_fixed_model"],
        "A_II_5.562": p["AII"][5.562], "A_II_53.64": p["AII"][53.64],
        "A_hf_c": p["A"] * FAC, "s_c": p["s"] * FAC, "A_hf_c_sigma0.1": p["A"] * MSC["sigma_0.1"]["factor_10^(e/2)"],
        "A_hf_plus_2s": p["A"] + 2 * p["s"], "A_hf_minus_2s": p["A"] - 2 * p["s"],
        "host_free": brief(p), "W10_all": brief(r_all), "hosted": brief(r_hst),
        "A_hosted_minus_A_hf": dif, "s_diff_joint": sdif,
        "R1_shells": {k: brief(v) for k, v in shells.items()},
        "bracket_three_lowest": brief(br3),
    }
    say(f"[{f}] A_hf = {p['A']:.4f} +- {p['s']:.4f} (fixed-model jk {p['s_fixed_model']:.4f}); A_II(5.562) = {p['AII'][5.562]:.4f}, "
        f"A_II(53.64) = {p['AII'][53.64]:.4f}; A_hf^c = {p['A'] * FAC:.4f} +- {p['s'] * FAC:.4f}")
    say(f"[{f}] A(W10) = {r_all['A']:.4f} +- {r_all['s']:.4f}; A(hosted) = {r_hst['A']:.4f} +- {r_hst['s']:.4f}; "
        f"A(hosted) - A_hf = {dif:+.4f} +- {sdif:.4f}; shells W10\\W20 {shells['W10_not_W20']['A']:.4f}, "
        f"W20\\W30 {shells['W20_not_W30']['A']:.4f}, W30 {shells['W30']['A']:.4f}; bracket (3 bins) A_hf {br3['A']:.4f} +- {br3['s']:.4f}")
    say(f"[{f}] LABEL: {lab}  (raw {l_raw}; corrected {l_cor}; gates {'all pass' if gates_ok else GATES})")
RES["primary"] = PRIMARY

# ======================================================================================================== 9b. sensitivity (REPORTED, NOT GRADED)
# Added after the first full run showed the canonical corrected s^c within 2 % of the 0.20 NO POWER line.  The graded reading
# above is unchanged (e = host-free-WW-weighted mean of the tercile e's; NO POWER tested on s^c in the corrected label).
P_all = {s: float((HC[sname(DSEL, WSEL, s)] == 0).mean()) for s in SHIFTS}
b_all = (math.log(P_all[0.1]) - math.log(P_all[-0.1])) / 0.2
n_t = np.array([(HF & (terc == t)).sum() for t in range(3)], float)
SIG2 = 0.2 ** 2
EV = {"primary_WW_weighted_terciles": float(np.dot(w_t, b_t)) * SIG2,
      "count_weighted_terciles": float(np.dot(n_t / n_t.sum(), b_t)) * SIG2,
      "unweighted_tercile_mean": float(np.mean(b_t)) * SIG2,
      "single_b_all_lenses": b_all * SIG2}
SENS = {"b_all_lenses": b_all, "P_host_free_all": {f"{s:+.1f}": v for s, v in P_all.items()}, "variants": {}}
for nm, ev in EV.items():
    fac = 10 ** (ev / 2)
    SENS["variants"][nm] = {"e_dex": ev, "factor": fac}
    for f in FOOT:
        p = PRIM[f]
        lab, l1, l2 = final_label(p["A"], p["s"], p["AII"][53.64], fac, gates_ok)
        SENS["variants"][nm][f] = {"A_c": p["A"] * fac, "s_c": p["s"] * fac, "label": lab, "corrected": l2}
# per-lens version: each host-free lens's law model lowered by 10^(-e_t/2) for its tercile, A and s recomputed
scale_l = 10 ** (-np.array([b * SIG2 for b in b_t])[terc] / 2)
SENS["variants"]["per_lens_model_rescaled"] = {}
for f in FOOT:
    r = amp(HF, f, wwm=WWM[f] * scale_l[:, None], want_ii=False)
    p = PRIM[f]
    l2 = table_label(r["A"], r["s"], p["AII"][53.64])
    lab = l2 if (l2 == table_label(p["A"], p["s"], p["AII"][53.64]) and gates_ok) else ("NOT SEPARATED" if gates_ok else "NO VERDICT")
    SENS["variants"]["per_lens_model_rescaled"][f] = {"A_c": r["A"], "s_c": r["s"], "label": lab, "corrected": l2}
# NO POWER line tested on the uncorrected s in both computations
SENS["no_power_on_uncorrected_s"] = {}
for f in FOOT:
    p = PRIM[f]
    if p["s"] > 0.20:
        l2 = "NO POWER"
    else:
        hi, lo = p["A"] * FAC + 2 * p["s"] * FAC, p["A"] * FAC - 2 * p["s"] * FAC
        l2 = ("LAW LEVEL HOLDS" if (hi >= GATE and lo > p["AII"][53.64]) else
              "BELOW THE LAW, TWO-PHASE WINDOW" if (hi < GATE and lo <= p["AII"][53.64]) else
              "BELOW THE LAW, BETWEEN" if (hi < GATE and lo > p["AII"][53.64]) else "NOT SEPARATED")
    l1 = PRIMARY[f]["label_raw"]
    SENS["no_power_on_uncorrected_s"][f] = {"corrected": l2, "label": (l1 if l1 == l2 else "NOT SEPARATED") if gates_ok else "NO VERDICT"}
# host-free set from a plain float comparison log M*_j >= log M*_l + Delta (no tie tolerance), same e factor
HF_strict = HC[sname(DSEL, WSEL, 0.0, "_strict")] == 0
SENS["strict_float_ties"] = {"n_host_free": int(HF_strict.sum()),
                             "f_w": float(WWO_l[HF_strict].sum() / WWO_l.sum())}
for f in FOOT:
    r = amp(HF_strict, f)
    lab, l1, l2 = final_label(r["A"], r["s"], r["AII"][53.64], FAC, gates_ok)
    SENS["strict_float_ties"][f] = {"A_hf": r["A"], "s": r["s"], "A_II_53.64": r["AII"][53.64], "A_c": r["A"] * FAC,
                                    "s_c": r["s"] * FAC, "label": lab, "raw": l1, "corrected": l2}
say(f"sensitivity [ties by plain float comparison: {int(HF_strict.sum()):,} host-free]: "
    + "; ".join(f"{f} A_hf {SENS['strict_float_ties'][f]['A_hf']:.4f} +- {SENS['strict_float_ties'][f]['s']:.4f} -> "
                f"{SENS['strict_float_ties'][f]['label']}" for f in FOOT))
s_line = {f: 0.20 / PRIM[f]["s"] for f in FOOT}
SENS["factor_at_which_s_c_reaches_0.20"] = {f: v for f, v in s_line.items()}
SENS["e_dex_at_which_s_c_reaches_0.20"] = {f: 2 * math.log10(v) for f, v in s_line.items()}
RES["sensitivity_reported_not_graded"] = SENS
for nm, v in SENS["variants"].items():
    say(f"sensitivity [{nm}]: " + (f"e {v['e_dex']:+.4f} dex, factor {v['factor']:.4f}; " if "e_dex" in v else "")
        + "; ".join(f"{f} A_c {v[f]['A_c']:.4f} +- {v[f]['s_c']:.4f} -> {v[f]['label']}" for f in FOOT))
say("sensitivity [NO POWER on uncorrected s]: " + "; ".join(f"{f} -> {v['label']}" for f, v in SENS["no_power_on_uncorrected_s"].items())
    + " | s^c reaches 0.20 at e = " + ", ".join(f"{f} {v:.4f} dex" for f, v in SENS["e_dex_at_which_s_c_reaches_0.20"].items()))

# ======================================================================================================== 10. MUTATE (separate output)
rng1 = np.random.default_rng(SEED)
zhalf = (zl >= np.median(zl)).astype(int)
cell = typ * 6 + terc * 2 + zhalf
HFP = HF.copy()
for cval in np.unique(cell):
    idx = np.flatnonzero(cell == cval)
    HFP[idx] = HF[idx][rng1.permutation(len(idx))]
MUT["M1"] = {}
for f in FOOT:
    rp_hf, rp_h = amp(HFP, f, want_ii=False), amp(~HFP, f, want_ii=False)
    dp, sdp = joint_diff(rp_h, rp_hf)
    dt, sdt = PRIMARY[f]["A_hosted_minus_A_hf"], PRIMARY[f]["s_diff_joint"]
    MUT["M1"][f] = {"diff_permuted": dp, "s_permuted": sdp, "inside_2s": abs(dp) < 2 * sdp,
                    "true_diff": dt, "true_s": sdt, "true_diff_inside_2s_(M1_no_power)": abs(dt) < 2 * sdt}
for name, fn in (("M2", lambda f: np.where(HF[:, None], WGO * 0.4, WGO)),
                 ("M3", lambda f: np.where(HF[:, None], WWO * m_law[f] / (4 * G), WGO))):
    MUT[name] = {}
    for f in FOOT:
        r = amp(HF, f, Y=fn(f))
        lab, l1, l2 = final_label(r["A"], r["s"], r["AII"][53.64], FAC, gates_ok)
        MUT[name][f] = {"A": r["A"], "s": r["s"], "A_II_53.64": r["AII"][53.64], "label": lab, "raw": l1, "corrected": l2}
MUT["bites"] = {"M1": all(v["inside_2s"] for v in MUT["M1"].values()),
                "M2": all(v["label"].startswith("BELOW THE LAW") for v in MUT["M2"].values()),
                "M3": all(v["label"] == "LAW LEVEL HOLDS" for v in MUT["M3"].values()),
                "M4": MUT["M4"]["bites"]}
say("MUTATE: " + "; ".join(f"{k} {'bites' if v else 'DOES NOT BITE'}" for k, v in MUT["bites"].items())
    + " | M1 " + ", ".join(f"{f} {v['diff_permuted']:+.4f} +- {v['s_permuted']:.4f}" for f, v in MUT["M1"].items())
    + " | M2 " + ", ".join(f"{f} {v['label']} (A {v['A']:.3f})" for f, v in MUT["M2"].items())
    + " | M3 " + ", ".join(f"{f} {v['label']} (A {v['A']:.3f} +- {v['s']:.4f})" for f, v in MUT["M3"].items()))
MUT["closing"] = CLOSE

RES["checks"] = CHK
RES["not_done"] = ("R2 except the three-bin bracket, R3, R4, R5, R6, R7 and the Lean file are not part of this regrade "
                   "(the task names the primary statistic, the label, KA1/KA2, the host flags, A(W10), A(hosted) and the difference)")
RES["closing"] = CLOSE
say(f"done; peak RSS {rss_mb():.0f} MB")
say(CLOSE)
json.dump(RES, open(os.path.join(HERE, "ko1r.json"), "w"), indent=1, default=float)
json.dump(MUT, open(os.path.join(HERE, "ko1r_MUTATE.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, "ko1r.out"), "w").write("\n".join(OUT) + "\n" + CLOSE + "\n")
# kappa = 1/2 FITTED; not theory closed. Adopts nothing.
