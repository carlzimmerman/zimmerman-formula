#!/usr/bin/env python3
"""KO2: does each galaxy TYPE carry its own lensing signal out to Mpc radii?   Criteria: FROZEN_CRITERIA.md (59e3c9ee9a),
committed alone first; AMENDMENT_A1.md (e5fca3518f): KA-2b's reference is direct quadrature about the lens, the tables are
refined to 2,401 x 1,681, KA-2d checks edge-adjacent cells against that reference.  TEST lane, quarantined; adopts nothing.

Every KiDS lens's projected mass and every catalogued neighbour's projected mass are written as concentric g_bar bands of the
law's projected profile (centre point, inner bins 7-12, middle 4-6, outer 0-3, far), each band with one amplitude per class
(late/early x mass half, giants), the same for lenses and neighbours.  Neighbours enter through exact off-centre annulus kernels
(tables of J(r, delta)); chance projections are removed with five shuffles of the lens positions.  Weighted least squares over
all lenses and bins 0-12, jackknife over the 50 patches.  Primary R_ext(type) = a[ext] / a[inner], ext = middle + outer + far.

Run (from this folder, one thread):
    KO2_CACHE=<directory outside the repo> python3 ko2.py   -> ko2.json, ko2.out, ko2_MUTATE.json, ko2_MUTATE.out
On macOS the script re-launches itself with MallocMediumZone=0 MallocLargeCache=0 (memory stays under 2 GB).
The cache keeps the kernel tables, the per-lens neighbour columns (float32, ~0.5 GB) and the in-pass sums between runs.
Inputs: the staged, git-ignored files under real_research/data/lensing_rar/.  The shear catalogue is not read.
kappa = 1/2 FITTED; not theory closed.  Adopts nothing.
"""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
if sys.platform == "darwin" and os.environ.get("MallocMediumZone") != "0":
    # macOS malloc keeps freed medium-size blocks resident; without these two settings the neighbour pass holds ~1 GB more
    os.environ["MallocMediumZone"] = "0"; os.environ["MallocLargeCache"] = "0"
    os.execv(sys.executable, [sys.executable] + sys.argv)
import json, math, time
import numpy as np
from scipy.spatial import cKDTree
from scipy import sparse

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
DATA = os.path.join(REPO, "real_research", "data", "lensing_rar")
KO1DIR = os.path.join(REPO, "fable52_push", "KO1_kids_outer_points")
CACHE = os.environ.get("KO2_CACHE", "")
if not CACHE:
    sys.exit("set KO2_CACHE to a directory outside the repo")
os.makedirs(CACHE, exist_ok=True)
STAGE = os.environ.get("KO2_STAGE", "all")          # 'kernels' = model-only checks (no lensing data used), 'all'
T0 = time.time()
import resource
def mem():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 2 ** 20 if sys.platform == "darwin" else resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 2 ** 10
def relieve():
    """hand freed memory back to the system (macOS malloc keeps freed large blocks resident otherwise)."""
    if sys.platform == "darwin":
        try:
            import ctypes
            ctypes.CDLL(None).malloc_zone_pressure_relief(None, 0)
        except Exception:
            pass
def cur():
    try:
        return float(os.popen(f"ps -o rss= -p {os.getpid()}").read().strip()) / 1024
    except Exception:
        return float("nan")
OUT, OUTM = [], []
def P(s=""):
    print(s, flush=True); OUT.append(s)
def PM(s=""):
    print("[MUTATE] " + s, flush=True); OUTM.append(s)
CHK = {}
def check(name, ok, msg):
    CHK[name] = bool(ok); P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {msg}")
CHKM = {}
def checkm(name, ok, msg):
    CHKM[name] = bool(ok); PM(f"  [{'BITES' if ok else 'DOES NOT BITE'}] {name}: {msg}")

# ------------------------------------------------------------------ constants (KO1's)
G = 6.674e-11; Msun = 1.989e30; Mpc = 3.0857e22; c_SI = 2.998e8; H0_SI = 70e3 / Mpc
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
FOOT = ("canonical", "alt"); NF = 2
NPAT = 50
NB = 13                                     # data bins 0..12
W_PRI, W_BR = 230.0, 115.0
REACH = 2.0                                 # Mpc beyond R_h
DMIN = 0.005                                # Mpc, blend / duplicate guard
NSHUF = 5
S_SYS = 0.05
ABSENT_LINE = 0.30
KGRID = [0.5, 0.7, 1.0, 1.4, 2.0, 2.8, 4.0, 5.6, 8.0]
CLS_NAMES = ["late-low", "late-high", "early-low", "early-high", "giant"]
BAND_NAMES = ["centre", "inner", "middle", "outer", "far"]

def nu(y):
    return 0.5 + np.sqrt(0.25 + 1.0 / y)
def glaw(g, a0):
    return nu(g / a0) * g
def Qf(g, a0):
    """int_0^g nu(g'/a0) dg' (closed form): 4 G x the mean surface density inside R for the law's profile."""
    return g / 2 + np.sqrt(g) / 2 * np.sqrt(g + 4 * a0) + 2 * a0 * np.arcsinh(np.sqrt(g / (4 * a0)))
def Sf(g, a0):
    """4 G Sigma_law at the radius where g_bar = g."""
    return Qf(g, a0) - glaw(g, a0)
def DC(z, n=2048):
    zz = np.linspace(0, np.max(z), n); E = np.sqrt(0.3 * (1 + zz) ** 3 + 0.7)
    chi = np.concatenate([[0], np.cumsum(0.5 * (1 / E[1:] + 1 / E[:-1]) * np.diff(zz))]) * (c_SI / H0_SI) / Mpc
    return np.interp(z, zz, chi)
def unitvec(ra_deg, dec_deg):
    ra, dec = np.radians(ra_deg), np.radians(dec_deg)
    return np.c_[np.cos(dec) * np.cos(ra), np.cos(dec) * np.sin(ra), np.sin(dec)]
def mgal_of(logMs):
    return 10 ** logMs * (1 + 10 ** (-0.69 * logMs + 6.63))

# ------------------------------------------------------------------ staged lensing sums (weights are read in every stage; WG only in 'all')
ln = np.load(os.path.join(DATA, "lr_lenses.npz"))
PL = np.load(os.path.join(DATA, "cfg110_perlens.npz"))
WW, EDGES = PL["WW"], PL["gbar_edges"]
patch = np.load(os.path.join(DATA, "cfg96_stack.npz"))["patch"]
NL = len(ln["ra"]); typ = ln["typ"]; zl = ln["z"]; logMs = ln["logM"]; Mg = ln["Mgal"] * Msun; chil = ln["chi"]
e0 = EDGES[0]; e13 = EDGES[13]
XE = np.sqrt(e0 / EDGES)                     # band edges in units of l = sqrt(G M / e0)
BANDX = {1: (XE[13], XE[7]), 2: (XE[7], XE[4]), 3: (XE[4], XE[0]), 4: (XE[0], np.inf)}   # inner, middle, outer, far
MC = np.array([math.pi * Qf(e13, A0[f]) / e13 for f in FOOT])   # centre point mass in units Mgal / 4
RH = np.minimum(3.0, np.sqrt(G * Mg / e0) / Mpc)                # Mpc
DMAX = RH + REACH
DA = chil / (1 + zl)
RE = np.minimum(np.sqrt(G * Mg[:, None] / EDGES[None, :14]) / Mpc, 3.0)   # (NL, 14) cell edges, Mpc, capped at 3 Mpc
P(f"KO2 run (stage {STAGE}).  lenses {NL:,}; bins 0-12; edges {EDGES[0]:.3e} .. {EDGES[13]:.3e}; window {W_PRI:.0f} (bracket {W_BR:.0f}) Mpc; "
  f"reach R_h + {REACH} Mpc; shuffles {NSHUF}")

# ------------------------------------------------------------------ the catalogue (read first, so its memory is released before the tables)
from astropy.io import fits
HB = fits.open(os.path.join(DATA, "KiDS_DR4_brightsample.fits"), memmap=True); bcat = HB[1].data
HL = fits.open(os.path.join(DATA, "KiDS_DR4_brightsample_LePhare.fits"), memmap=True); Lp = HL[1].data
assert np.array_equal(np.asarray(bcat["ID"]), np.asarray(Lp["ID"]))
r_ = np.array(bcat["MAG_AUTO_CALIB"], dtype="f8"); z_ = np.array(bcat["zphot_ANNz2"], dtype="f8")
logM_ = np.array(Lp["MASS_MED"], dtype="f8") + 0.15
ur_ = np.array(Lp["MAG_ABS_u"], dtype="f8") - np.array(Lp["MAG_ABS_r"], dtype="f8")
ra_ = np.array(bcat["RAJ2000"], dtype="f8"); dec_ = np.array(bcat["DECJ2000"], dtype="f8")
del bcat, Lp; HB.close(); HL.close(); del HB, HL
import gc; gc.collect(); relieve()
P(f"  catalogue read: {len(r_):,} objects  [{time.time() - T0:.0f} s, now {(relieve(), cur())[1]:.0f}, peak {mem():.0f} MB]")

# ------------------------------------------------------------------ own columns (closed forms, KO1's 24-node Gauss-Legendre in R^2)
XG, WGL = np.polynomial.legendre.leggauss(24)
R3 = (3.0 * Mpc) ** 2
def band_kernel(g, B, a0):
    """4 G DeltaSigma of band B of a galaxy's own law profile, at the radius where g_bar = g (concentric)."""
    if B == 0:
        return g * Qf(e13, a0) / e13
    g1 = EDGES[{1: 7, 2: 4, 3: 0}[B]]; g2 = EDGES[{1: 13, 2: 7, 3: 4}[B]]
    inb = glaw(g, a0) - g * Qf(g2, a0) / g2
    beyond = g * (Qf(g1, a0) / g1 - Qf(g2, a0) / g2)
    return np.where(g >= g2, 0.0, np.where(g >= g1, inb, beyond))
def own_cells(Mg_all, k=1.0, CHO=20000):
    """(n, 13, 4, 2): own band columns per cell; and (n, 13, 2): the law's cell at mass k Mgal (k = 1: KO1's law cell)."""
    n = len(Mg_all); own = np.zeros((n, NB, 4, NF)); law = np.zeros((n, NB, NF))
    for c0 in range(0, n, CHO):
        Mg_arr = Mg_all[c0:c0 + CHO]; sl = slice(c0, c0 + CHO)
        for b in range(NB):
            t_lo = G * Mg_arr / EDGES[b + 1]; t_hi = np.minimum(G * Mg_arr / EDGES[b], R3); ok = t_hi > t_lo
            t = t_lo[:, None] + (t_hi - t_lo)[:, None] * (XG[None, :] + 1) / 2
            g = G * Mg_arr[:, None] / t
            for fi, f in enumerate(FOOT):
                for B in range(4):
                    own[sl, b, B, fi] = np.where(ok, (band_kernel(g, B, A0[f]) * WGL[None, :]).sum(1) / 2, 0.0)
                law[sl, b, fi] = np.where(ok, (glaw(k * g, A0[f]) * WGL[None, :]).sum(1) / 2, 0.0)
    return own, law
OWN, LAW1 = own_cells(Mg)
P(f"own columns done  [{time.time() - T0:.0f} s, now {(relieve(), cur())[1]:.0f}, peak {mem():.0f} MB]")

# ------------------------------------------------------------------ neighbour kernel tables J_B(r, delta)
NR, ND = 2401, 1681                                     # A1 (frozen: 801 x 561)
LNR = np.linspace(math.log(1e-3), math.log(60.0), NR); LND = np.linspace(math.log(1e-3), math.log(60.0), ND)
DLR = LNR[1] - LNR[0]; DLD = LND[1] - LND[0]
XQ, WQ = np.polynomial.legendre.leggauss(48)
TH = (XQ + 1) * math.pi / 2; WTH = WQ * math.pi / 2
def Fenc(x, a0):
    """band mass inside ring radius x of the law profile (excluding nothing), in units Mgal / 4:  pi Q(g)/g at g = e0/x^2."""
    g = e0 / x ** 2
    return math.pi * Qf(g, a0) / g
def m_band(r, delta, B, a0):
    """mass of band B inside the circle of radius r whose centre is delta from the band's centre (units Mgal / 4); r array."""
    x1, x2 = BANDX[B]
    m = np.zeros_like(r)
    # rings wholly inside the circle: x <= r - delta
    xb = np.minimum(x2, r - delta); okf = xb > x1
    if okf.any():
        m[okf] += Fenc(xb[okf], a0) - Fenc(x1, a0)
    # rings crossing the circle: |r - delta| < x < r + delta
    lo = np.maximum(np.abs(r - delta), x1); hi = np.minimum(r + delta, x2); okp = hi > lo
    if okp.any():
        a, b = lo[okp][:, None], hi[okp][:, None]
        x = (a + b) / 2 - (b - a) / 2 * np.cos(TH)[None, :]
        jac = (b - a) / 2 * np.sin(TH)[None, :]
        arg = np.clip((x * x + delta * delta - r[okp][:, None] ** 2) / (2 * x * delta), -1.0, 1.0)
        phi = np.arccos(arg) / math.pi
        s = Sf(e0 / x ** 2, a0) / e0
        m[okp] += (2 * math.pi * x * s * phi * jac * WTH[None, :]).sum(1)
    return m
def build_tables():
    fn = os.path.join(CACHE, f"ko2_tables_{NR}x{ND}.npy")
    if os.path.exists(fn):
        return np.load(fn)
    T = np.zeros((NR, ND, 8)); r = np.exp(LNR)
    for jd, dl in enumerate(np.exp(LND)):
        for bi, B in enumerate((1, 2, 3, 4)):
            for fi, f in enumerate(FOOT):
                m = m_band(r, dl, B, A0[f])
                cum = np.concatenate([[0.0], np.cumsum((m[1:] + m[:-1]) * DLR)])
                T[:, jd, 2 * bi + fi] = cum - m
    np.save(fn, T)
    return T
TAB = build_tables()
TABF = TAB.reshape(NR * ND, 8)
P(f"kernel tables {NR} x {ND} x 8 ready  [{time.time() - T0:.0f} s, now {(relieve(), cur())[1]:.0f}, peak {mem():.0f} MB]")

def dindex(delta):
    t = np.clip((np.log(np.maximum(delta, 1e-300)) - LND[0]) / DLD, 0.0, ND - 1 - 1e-9)
    j0 = t.astype(np.int64); return j0, t - j0
def jlook(r, j0, h):
    """(n, 10): J of [centre f0, centre f1, inner f0, inner f1, middle .., outer .., far ..] at radius r (units l)."""
    t = np.clip((np.log(np.maximum(r, 1e-300)) - LNR[0]) / DLR, 0.0, NR - 1 - 1e-9)
    i0 = t.astype(np.int64); f = t - i0
    base = i0 * ND + j0
    w00 = (1 - f) * (1 - h); w10 = f * (1 - h); w01 = (1 - f) * h; w11 = f * h
    J = TABF[base] * w00[:, None] + TABF[base + ND] * w10[:, None] + TABF[base + 1] * w01[:, None] + TABF[base + ND + 1] * w11[:, None]
    return J
def jpoint(r, delta):
    with np.errstate(divide="ignore", invalid="ignore"):
        v = np.where(r > delta, 2 * np.log(r / delta) - 1.0, 0.0)
    return v[:, None] * MC[None, :]
def kern_bins(REl, d, ell):
    """per-pair kernels (m/s^2), yielded per bin b as (b, K[npairs, 10])."""
    delta = d / ell; j0, h = dindex(delta)
    r_prev = REl[:, 0] / ell
    J_prev = np.concatenate([jpoint(r_prev, delta), jlook(r_prev, j0, h)], axis=1)
    for b in range(NB):
        r_next = REl[:, b + 1] / ell
        J_next = np.concatenate([jpoint(r_next, delta), jlook(r_next, j0, h)], axis=1)
        den = r_prev ** 2 - r_next ** 2
        valid = den > 1e-12 * r_prev ** 2
        with np.errstate(divide="ignore", invalid="ignore"):
            K = np.where(valid[:, None], (e0 / math.pi) * (J_prev - J_next) / den[:, None], 0.0)
        yield b, K
        r_prev, J_prev = r_next, J_next

# ------------------------------------------------------------------ KA-2: the kernels against brute force (model only)
P("\nKA-2: neighbour kernels")
def point_kernel_cells(q, rlo, rhi, mass):
    """exact annulus average (m/s^2) of a point of `mass` (units Mgal/4) at distance q (units l); E8's closed form in these units."""
    with np.errstate(divide="ignore", invalid="ignore"):
        Jh = np.where(rhi > q, 2 * np.log(rhi / q) - 1, 0.0); Jl = np.where(rlo > q, 2 * np.log(rlo / q) - 1, 0.0)
    return (e0 / math.pi) * mass * (Jh - Jl) / (rhi ** 2 - rlo ** 2)
def e8_formula(d2, t1, t2, m4G):
    """KO1 ko1_neighbours.py verbatim structure: 4 G m K / (pi (t2 - t1))."""
    with np.errstate(divide="ignore", invalid="ignore"):
        Kin = np.log(t2 / t1); Kmid = np.log(t2 / np.maximum(d2, 1e-300)) - 1.0
    K = np.where(d2 < t1, Kin, np.where(d2 < t2, Kmid, 0.0))
    return m4G * K / (math.pi * (t2 - t1))
rng = np.random.default_rng(52)
# (a) centre point: this lane's implementation against E8's formula, physical units
nt = 20000; lM = rng.uniform(8.0, 11.8, nt); Mj = mgal_of(lM) * Msun; ell = np.sqrt(G * Mj / e0) / Mpc
dd = rng.uniform(0.0, 5.0, nt); R2 = rng.uniform(0.05, 3.0, nt); R1 = R2 / rng.uniform(1.05, 1.6, nt)
mine = np.stack([(e0 / math.pi) * MC[fi] * ((jpoint(R2 / ell, dd / ell)[:, fi] / MC[fi]) - (jpoint(R1 / ell, dd / ell)[:, fi] / MC[fi])) / ((R2 / ell) ** 2 - (R1 / ell) ** 2)
                 for fi in range(NF)], 1)
ref = np.stack([e8_formula((dd * Mpc) ** 2, (R1 * Mpc) ** 2, (R2 * Mpc) ** 2, math.pi * G * Mj * Qf(e13, A0[f]) / e13) for f in FOOT], 1)
ka2a = float(np.max(np.abs(mine - ref)) / np.max(np.abs(ref)))
check("KA-2a centre point kernel against KO1 E8's closed form to 1e-9", ka2a < 1e-9, f"max deviation {ka2a:.1e} of the largest value, {nt:,} cases x 2 footings")
# (b) tables against the band drawn as 200,000 point masses (500 shells x 400 angles), realistic configurations
def ref_band(B, fi, rlo, rhi, delta):
    """A1 reference: the band's surface density integrated directly in polar coordinates about the LENS (4,096 angles; 2,000
    log radii from 1e-4 rhi, 400 of them inside the cell); enclosed mass from the circle means; the cell average by definition."""
    a0 = A0[FOOT[fi]]; x1, x2 = BANDX[B]
    R = np.concatenate([np.exp(np.linspace(math.log(1e-4 * rhi), math.log(rlo), 1600))[:-1], np.exp(np.linspace(math.log(rlo), math.log(rhi), 401))])
    psi = (np.arange(4096) + 0.5) * 2 * math.pi / 4096; cps = np.cos(psi)
    C = np.zeros(len(R))
    for i0 in range(0, len(R), 100):
        Rr = R[i0:i0 + 100][:, None]
        X = np.sqrt(np.maximum(Rr * Rr + delta * delta - 2 * Rr * delta * cps[None, :], 1e-300))
        inb = (X >= x1) & (X < x2)
        sv = np.where(inb, Sf(e0 / np.where(inb, X, 1.0) ** 2, a0) / e0, 0.0)
        C[i0:i0 + 100] = sv.mean(1)
    lnR = np.log(R); f = C * 2 * math.pi * R * R                    # dM / dlnR
    M = C[0] * math.pi * R[0] ** 2 + np.concatenate([[0.0], np.cumsum((f[1:] + f[:-1]) / 2 * np.diff(lnR))])
    k0 = 1599                                                       # index of rlo
    g2 = 2 * M[k0:]; I = float(((g2[1:] + g2[:-1]) / 2 * np.diff(lnR[k0:])).sum())
    return (e0 / math.pi) * (I - (M[-1] - M[k0])) / (rhi ** 2 - rlo ** 2)
def table_band(B, fi, rlo, rhi, delta):
    j0, h = dindex(np.array([delta]))
    Jh = jlook(np.array([rhi]), j0, h)[0]; Jl = jlook(np.array([rlo]), j0, h)[0]
    c = 2 * (B - 1) + fi                                            # jlook returns the 8 table columns only
    return float((e0 / math.pi) * (Jh[c] - Jl[c]) / (rhi ** 2 - rlo ** 2))
cfg = []
for i in range(300):
    li = rng.integers(NL); b = int(rng.integers(NB)); lMj = rng.uniform(8.0, 11.8)
    ellj = math.sqrt(G * mgal_of(lMj) * Msun / e0) / Mpc
    rhi, rlo = RE[li, b], RE[li, b + 1]
    if rhi <= rlo * 1.0001:
        rhi, rlo = RE[li, 4], RE[li, 5]
    d = math.exp(rng.uniform(math.log(0.005), math.log(DMAX[li])))
    cfg.append((1 + i % 4, rlo / ellj, rhi / ellj, d / ellj))
ka2b = {}; KA2B_MAX = {}
for fi in range(NF):
    res = {B: [] for B in (1, 2, 3, 4)}
    for B, rlo, rhi, dl in cfg:
        res[B].append((table_band(B, fi, rlo, rhi, dl), ref_band(B, fi, rlo, rhi, dl)))
    for B, v in res.items():
        v = np.array(v); mx = np.max(np.abs(v[:, 1])); KA2B_MAX[(fi, B)] = float(mx)
        bad = np.abs(v[:, 0] - v[:, 1]) > 0.01 * np.abs(v[:, 1]) + 0.003 * mx
        ka2b[(fi, B)] = (int(bad.sum()), float(np.max(np.abs(v[:, 0] - v[:, 1])) / mx))
okb = all(v[0] == 0 for v in ka2b.values())
check("KA-2b (A1) tables against direct quadrature about the lens (300 configurations per footing)", okb,
      "; ".join(f"{FOOT[fi][:3]} {BAND_NAMES[B]}: {n} outside, max |diff| {m:.1e} of band max" for (fi, B), (n, m) in ka2b.items()))
# (c) uniform sheet: positions uniform in a disc reaching past every band edge -> zero mean
ka2c = []
for B in (0, 1, 2, 3):
    for (rlo, rhi) in ((0.05, 0.07), (0.2, 0.27), (0.6, 0.8), (1.5, 2.0)):
        x2 = 0.0 if B == 0 else BANDX[B][1]
        Rmax = rhi + x2 + 0.5
        dl = Rmax * np.sqrt(rng.random(200000))
        j0, h = dindex(dl)
        if B == 0:
            Kh = jpoint(np.full(dl.shape, rhi), dl)[:, 0]; Kl = jpoint(np.full(dl.shape, rlo), dl)[:, 0]
        else:
            c = 2 * (B - 1)
            Kh = jlook(np.full(dl.shape, rhi), j0, h)[:, c]; Kl = jlook(np.full(dl.shape, rlo), j0, h)[:, c]
        K = (e0 / math.pi) * (Kh - Kl) / (rhi ** 2 - rlo ** 2)
        mu, se = float(K.mean()), float(K.std() / math.sqrt(len(K)))
        ka2c.append((B, rlo, mu, se, abs(mu) <= 3 * se))
check("KA-2c a uniform sheet of bands or points gives zero mean shear (within 3 Monte Carlo errors)", all(x[4] for x in ka2c),
      "; ".join(f"{BAND_NAMES[B]} r {rlo}: {mu / se:+.2f} se" for B, rlo, mu, se, _ in ka2c))
# (d) A1: separation 1e-3 l, bin-aligned cells: cells not adjacent to the band's edges against the concentric closed form (0.5 %);
#     edge-adjacent cells against the A1 reference (KA-2b's tolerance, with that band's KA-2b maximum)
ka2d, ka2d_edge = 0.0, []
for fi, f in enumerate(FOOT):
    for b in range(NB):
        rhi, rlo = XE[b], XE[b + 1]
        t = rlo ** 2 + (rhi ** 2 - rlo ** 2) * (XG + 1) / 2; g = e0 / t
        for B in (1, 2, 3):
            tb = table_band(B, fi, rlo, rhi, 1e-3)
            edges = BANDX[B]
            adjacent = any(abs(rlo / e_ - 1) < 1e-9 or abs(rhi / e_ - 1) < 1e-9 for e_ in edges)
            if adjacent:
                rf = ref_band(B, fi, rlo, rhi, 1e-3); mx = KA2B_MAX[(fi, B)]
                ka2d_edge.append((fi, B, b, tb, rf, abs(tb - rf) <= 0.01 * abs(rf) + 0.003 * mx))
            else:
                conc = float((band_kernel(g, B, A0[f]) * WGL).sum() / 2)
                scale = float((glaw(g, A0[f]) * WGL).sum() / 2)
                ka2d = max(ka2d, abs(tb - conc) / scale)            # A2: in units of the law's value in the cell
check("KA-2d (A1, A2) separation 1e-3 l: non-adjacent cells against the concentric form to 0.5 % of the law's cell value, edge-adjacent cells against the reference",
      ka2d < 0.005 and all(x[5] for x in ka2d_edge),
      f"non-adjacent max deviation {ka2d:.2e} of the law's cell value; edge-adjacent {sum(x[5] for x in ka2d_edge)} of {len(ka2d_edge)} within tolerance, "
      f"max |table - reference| / band max {max(abs(x[3] - x[4]) / KA2B_MAX[(x[0], x[1])] for x in ka2d_edge):.1e}")
P(f"  [{time.time() - T0:.0f} s, now {(relieve(), cur())[1]:.0f}, peak {mem():.0f} MB]")
# ------------------------------------------------------------------ catalogue and pool (weights only; A2 moves this into the model-only stage)
P("\nKA-0a: lenses in the catalogue")
nb = (r_ < 20) & (z_ >= 0.02) & (z_ <= 0.8) & np.isfinite(logM_) & (logM_ > 7); inb = np.where(nb)[0]
NP_ = len(inb)
xN = unitvec(ra_[inb], dec_[inb]); chiN = DC(z_[inb]); logMN = logM_[inb]; urN = ur_[inb]
ellN = np.sqrt(G * mgal_of(logMN) * Msun / e0) / Mpc
# lenses' rows in the pool: exact (ra, dec) match through 16-byte keys (KO1's extras used a dict; same result, less memory)
kp = np.ascontiguousarray(np.c_[ra_[inb], dec_[inb]]).view(np.dtype((np.void, 16))).ravel()
kl = np.ascontiguousarray(np.c_[ln["ra"], ln["dec"]]).view(np.dtype((np.void, 16))).ravel()
okp = np.argsort(kp, kind="stable"); pos_ = np.minimum(np.searchsorted(kp[okp], kl), len(kp) - 1)
selfN = np.where(kp[okp][pos_] == kl, okp[pos_], -1)
del kp, kl, okp, pos_
found = bool(np.all(selfN >= 0))
okM = found and bool(np.array_equal(logMN[selfN], logMs))
okT = found and bool(np.array_equal((urN[selfN] > 2.0).astype(np.int64), typ))
untyped = int((~np.isfinite(urN)).sum()); ur_tie = int((urN == 2.0).sum())
check("KA-0a lenses in the pool by position with equal log M* and type", found and okM and okT,
      f"all found {found}; log M* equal {okM}; type equal {okT}")
P(f"  pool {NP_:,} objects; untyped (non-finite u - r) {untyped} ({100 * untyped / NP_:.3f} %: bracket 'untyped as early' "
  f"{'RUN' if untyped > 0.01 * NP_ else 'not needed'}); u - r exactly 2.0 (late by the record's rule): {ur_tie}")
treeN = cKDTree(xN); xL = xN[selfN]
del r_, z_, logM_, ur_, ra_, dec_, nb
P(f"  pool and tree ready  [{time.time() - T0:.0f} s, now {(relieve(), cur())[1]:.0f}, peak {mem():.0f} MB]")

# ------------------------------------------------------------------ classes (weights only) and the tie rule
wl = WW[:, :NB].sum(1)
THR = {}
for t in (0, 1):
    m = typ == t; o = np.argsort(logMs[m]); lv = logMs[m][o]; cw = np.cumsum(wl[m][o])
    v = float(lv[np.searchsorted(cw, 0.5 * cw[-1])])
    above = logMN[logMN > v]; vn = float(above.min())
    THR[t] = 0.5 * (v + vn)
def class_of(logm, ur, giant_ok=True):
    t = (ur > 2.0).astype(np.int64)
    thr = np.where(t == 1, THR[1], THR[0])
    c = 2 * t + (logm >= thr).astype(np.int64)
    if giant_ok:
        c = np.where(logm >= 11.0, 4, c)
    return c
GRP = class_of(logMN, urN)
CLS = class_of(logMs, np.where(typ == 1, 3.0, 1.0), giant_ok=False)
assert np.array_equal(CLS, GRP[selfN])
near_thr = {t: int((np.abs(logMN - THR[t]) < 1e-4).sum()) for t in (0, 1)}
on_thr = {t: int((logMN == THR[t]).sum()) for t in (0, 1)}
P(f"  mass-half thresholds (WW-weighted lens medians moved off every catalogue value): late {THR[0]:.6f}, early {THR[1]:.6f}; "
  f"pool objects exactly on a threshold {on_thr}; within 1e-4 dex {near_thr}")
P("  lenses per class: " + ", ".join(f"{CLS_NAMES[c]} {int((CLS == c).sum()):,}" for c in range(4))
  + ";  pool per class: " + ", ".join(f"{CLS_NAMES[c]} {int((GRP == c).sum()):,}" for c in range(5)))

# ------------------------------------------------------------------ the neighbour pass
def chunk_columns(ids, qx, qself, Px, Pchi, Pell, Pgrp, tree, wins):
    """neighbour columns for the lenses `ids` queried at positions qx: {w: (n, 13, 5 groups, 10)}; and the pair count per window."""
    n = len(ids); out = {w: np.zeros((n, NB, 5, 2 * 5)) for w in wins}; npair = {w: 0 for w in wins}
    chord = 2 * np.sin(DMAX[ids] * (1 + zl[ids]) / chil[ids] / 2)
    lists = tree.query_ball_point(qx, r=chord)
    c = np.fromiter((len(x) for x in lists), dtype=np.int64, count=n); tot = int(c.sum())
    if tot == 0:
        return out, npair
    li = np.repeat(np.arange(n), c); j = np.fromiter((jj for x in lists for jj in x), dtype=np.int64, count=tot)
    del lists
    gl = ids[li]
    dchi = np.abs(Pchi[j] - chil[gl])
    keep = (j != qself[li]) & (dchi < max(wins))
    li, j, gl, dchi = li[keep], j[keep], gl[keep], dchi[keep]
    ch = np.linalg.norm(Px[j] - qx[li], axis=1)
    d = 2 * np.arcsin(np.minimum(ch / 2, 1.0)) * DA[gl]
    keep = (d >= DMIN) & (d < DMAX[gl])
    li, j, gl, dchi, d = li[keep], j[keep], gl[keep], dchi[keep], d[keep]
    if len(li) == 0:
        return out, npair
    Gk = li * 5 + Pgrp[j]
    order = np.argsort(Gk, kind="stable"); Gs = Gk[order]
    starts = np.concatenate([[0], np.flatnonzero(np.diff(Gs)) + 1]); gu = Gs[starts]; lu, cu = gu // 5, gu % 5
    wm = {w: (dchi < w)[order].astype(np.float64) for w in wins}
    for w in wins:
        npair[w] = int((dchi < w).sum())
    REl = RE[gl][order]; d_o = d[order]; ell_o = Pell[j][order]
    for b, K in kern_bins(REl, d_o, ell_o):
        for w in wins:
            out[w][lu, b, cu, :] += np.add.reduceat(K * wm[w][:, None], starts, axis=0)
    return out, npair

# ------------------------------------------------------------------ KA-3a: planted neighbours, tree against brute force (cross-talk included)
P("\nKA-3a: 2,000 planted neighbours")
rs = np.random.default_rng(52); pick = rs.choice(NL, 2000, replace=False)
fac = rs.uniform(0.2, 1.5, 2000); dchs = rs.choice([50.0, 150.0, 300.0], 2000); lMs = rs.uniform(9.5, 11.5, 2000); urs = rs.choice([1.0, 3.0], 2000)
th = fac * RH[pick] / DA[pick]
x0 = xL[pick]; refv = np.cross(x0, np.array([0.0, 0.0, 1.0])); refv /= np.linalg.norm(refv, axis=1)[:, None]; ref2 = np.cross(x0, refv)
ang = rs.uniform(0, 2 * math.pi, 2000); tdir = np.cos(ang)[:, None] * refv + np.sin(ang)[:, None] * ref2
xs = np.cos(th)[:, None] * x0 + np.sin(th)[:, None] * tdir
chis = chil[pick] + dchs; ells = np.sqrt(G * mgal_of(lMs) * Msun / e0) / Mpc; grps = class_of(lMs, urs)
trees = cKDTree(xs)
brute = {}
chordL = 2 * np.sin(DMAX * (1 + zl) / chil / 2)
for s0 in range(0, 2000, 25):
    ss = np.arange(s0, s0 + 25)
    c2 = 2.0 - 2.0 * (xL @ xs[ss].T)                                         # (NL, 25) squared chords, candidates only
    li, sj = np.nonzero(c2 <= (chordL[:, None] ** 2) * (1 + 1e-6) + 1e-15)
    sj = ss[sj]
    chd = np.linalg.norm(xs[sj] - xL[li], axis=1)                              # exact chord, as the tree path computes it
    ok0 = chd <= chordL[li]; li, sj, chd = li[ok0], sj[ok0], chd[ok0]
    dchi = np.abs(chis[sj] - chil[li]); d = 2 * np.arcsin(np.minimum(chd / 2, 1.0)) * DA[li]
    ok = (dchi < W_PRI) & (d >= DMIN) & (d < DMAX[li]); li, sj, d = li[ok], sj[ok], d[ok]
    if len(li) == 0: continue
    for b, K in kern_bins(RE[li], d, ells[sj]):
        for p_ in range(len(li)):
            key_ = (int(li[p_]), int(grps[sj[p_]]))
            if key_ not in brute: brute[key_] = np.zeros((NB, 10))
            brute[key_][b] += K[p_]
LR = np.array(sorted(set(k[0] for k in brute)), dtype=np.int64)
BRr = np.zeros((len(LR), NB, 5, 10)); BRm = np.zeros((len(LR), 5), bool)
for (l_, g_), v in brute.items():
    k_ = int(np.searchsorted(LR, l_)); BRr[k_, :, g_, :] = v; BRm[k_, g_] = True
del brute
maxval = float(np.max(np.abs(BRr))); maxdev, nonzero_tree_only = 0.0, 0
for c0 in range(0, NL, 4000):
    ids = np.arange(c0, min(c0 + 4000, NL))
    o, _ = chunk_columns(ids, xL[ids], np.full(len(ids), -1), xs, chis, ells, grps, trees, (W_PRI,))
    o = o[W_PRI]
    pos = np.searchsorted(LR, ids); inr = (pos < len(LR)) & (LR[np.minimum(pos, len(LR) - 1)] == ids)
    if inr.any():
        maxdev = max(maxdev, float(np.max(np.abs(o[inr] - BRr[pos[inr]]))))
        nonzero_tree_only += int((np.any(o[inr] != 0, axis=(1, 3)) & ~BRm[pos[inr]]).sum())
    nonzero_tree_only += int(np.any(o[~inr] != 0, axis=(1, 3)).sum())
nmulti = int((BRm.sum(1) > 1).sum())
check("KA-3a the tree-based columns equal a brute-force loop over all (lens, planted object) pairs to 1e-6", maxdev <= 1e-6 * maxval and nonzero_tree_only == 0,
      f"max deviation {maxdev / maxval:.1e} of the largest value; lenses reached {len(LR):,}, of which reached by more than one "
      f"planted class group {nmulti:,}; cells found by the tree only {nonzero_tree_only}")
P(f"  [{time.time() - T0:.0f} s, now {(relieve(), cur())[1]:.0f}, peak {mem():.0f} MB]")

if STAGE == "kernels":
    P("stage 'kernels' ends here (model-only checks).")
    sys.exit(0)

# ================================================================== from here on the lensing sums are used
WG = PL["WG"]; ST = np.load(os.path.join(DATA, "cfg96_stack.npz")); NN = PL["NN"]
C116 = np.load(os.path.join(DATA, "cfg116_perlens.npz")); WX = C116["WX"]
P("\nKA-0b: data integrity")
dev = 0.0
FL = np.load(os.path.join(DATA, "cfg96_isoflags.npz")); f20, f30 = FL["f20"], FL["f30"]
for tag, m in (("10", np.ones(NL, bool)), ("20", f20), ("30", f30)):
    for arr, key in ((WG, "wgE_"), (WW, "W_"), (NN, "NN_")):
        S = np.zeros((NPAT, 2, 15)); np.add.at(S, (patch[m], typ[m]), arr[m])
        ref = ST[key + tag]; dev = max(dev, float(np.max(np.abs(S - ref)) / np.max(np.abs(ref))))
wdev = float(np.max(np.abs(C116["WWn"] + C116["WWf"] - WW)) / np.max(WW))

check("KA-0b per-lens sums reproduce cfg96_stack (KO1 KA1) to 1e-9; cfg116 near + far weights equal WW", dev < 1e-9 and wdev < 1e-9,
      f"max deviation {dev:.1e}; weights {wdev:.1e}")

# ------------------------------------------------------------------ KA-1: KO1 reproduced, own columns against KO1's law cells
P("\nKA-1: KO1 reproduced")
def hostfree_ko1(fac=1.0, dm=0.3, W=230.0, CH=300):
    """ko1_shape.py's hostfree() verbatim (comparisons as KO1 made them)."""
    chord = 2 * np.sin(fac * RH * (1 + zl) / chil / 2); dmin = np.full(NL, np.inf)
    for i0 in range(0, NL, CH):
        i1 = min(i0 + CH, NL)
        lists = treeN.query_ball_point(xL[i0:i1], r=chord[i0:i1])
        c = np.fromiter((len(x) for x in lists), dtype=np.int64, count=len(lists)); tot = int(c.sum())
        if tot == 0: continue
        k = np.repeat(np.arange(len(c)), c); j = np.fromiter((jj for x in lists for jj in x), dtype=np.int64, count=tot); li = i0 + k
        keep = (j != selfN[li]) & (logMN[j] >= logMs[li] + dm); li, j = li[keep], j[keep]
        np.minimum.at(dmin, li, np.abs(chiN[j] - chil[li]))
    return dmin >= W
HFK = hostfree_ko1()
def psum(arr, mask):
    pm = patch[mask]; a = arr[mask]
    return np.stack([np.bincount(pm, weights=a[:, c], minlength=NPAT) for c in range(arr.shape[1])], axis=1)
def amp_ko1(mask, Mo, cols):
    """ko1_extra.py's amp() verbatim (stack against a cell model over columns `cols`, 50-patch jackknife)."""
    Sg = psum(WG[:, cols], mask); Sw = psum(WW[:, cols], mask); Sm = psum((WW[:, :Mo.shape[1]] * Mo)[:, cols], mask)
    tg, tw, tm = Sg.sum(0), Sw.sum(0), Sm.sum(0)
    D = 4 * G * tg / tw; M = tm / tw
    Dl = 4 * G * (tg - Sg) / (tw - Sw); Ml = (tm - Sm) / (tw - Sw)
    sk = np.sqrt((NPAT - 1) / NPAT * ((Dl - Dl.mean(0)) ** 2).sum(0))
    A = float((D * M / sk ** 2).sum() / (M * M / sk ** 2).sum())
    Al = (Dl * Ml / sk ** 2).sum(1) / (Ml * Ml / sk ** 2).sum(1)
    s = float(np.sqrt((NPAT - 1) / NPAT * ((Al - Al.mean()) ** 2).sum()))
    return dict(A=A, s=s, Al=Al)
def ko1_law_cells(a0):
    """ko1_extra.py's cells(glaw) for bins 0..12."""
    m = np.zeros((NL, NB))
    for k in range(NB):
        t_lo = G * Mg / EDGES[k + 1]; t_hi = np.minimum(G * Mg / EDGES[k], R3); ok = t_hi > t_lo
        t = t_lo[:, None] + (t_hi - t_lo)[:, None] * (XG[None, :] + 1) / 2
        with np.errstate(divide="ignore", invalid="ignore"):
            f = glaw(G * Mg[:, None] / t, a0)
        m[:, k] = np.where(ok, (f * WGL[None, :]).sum(1) / 2, 0.0)
    return m
OUTERW, MIDW, INNERW = [0, 1, 2, 3], [4, 5, 6], [7, 8, 9, 10, 11, 12]
E1 = json.load(open(os.path.join(KO1DIR, "ko1_extra.json")))["foot"]
ka1a = 0.0; KO1LAW = {}
for fi, f in enumerate(FOOT):
    L = ko1_law_cells(A0[f]); KO1LAW[f] = L
    for name, m in (("host-free late", HFK & (typ == 0)), ("host-free early", HFK & (typ == 1))):
        for wname, cols in (("outer", OUTERW), ("middle", MIDW), ("inner", INNERW)):
            q = amp_ko1(m, L, cols); refv = E1[f]["E1"][name][wname]
            ka1a = max(ka1a, abs(q["A"] / refv[0] - 1), abs(q["s"] / refv[1] - 1))
check("KA-1a KO1's host-free scan gives 40,667 and KO1's host-free late / early window amplitudes are reproduced to 1e-6",
      int(HFK.sum()) == 40667 and ka1a < 1e-6, f"host-free {int(HFK.sum()):,}; max relative deviation of A and s {ka1a:.1e}")
ka1b = max(float(np.max(np.abs(OWN[:, :, :, fi].sum(2) - KO1LAW[f]) / np.maximum(np.abs(KO1LAW[f]), 1e-300) * (KO1LAW[f] != 0))) for fi, f in enumerate(FOOT))
ka1b2 = max(float(np.max(np.abs(LAW1[:, :, fi] - KO1LAW[f]))) for fi, f in enumerate(FOOT))
check("KA-1b own columns with every amplitude 1 equal KO1's law cells (bins 0-12) to 1e-6", ka1b < 1e-6 and ka1b2 == 0.0,
      f"max relative deviation {ka1b:.1e}; law cell recomputation {ka1b2:.1e}")
nocov = int(((WW[:, :NB] > 0) & (LAW1[:, :, 0] == 0)).sum())
check("KA-1c coverage: no cell with weight lacks a model value", nocov == 0, f"{nocov} cells")
P(f"  [{time.time() - T0:.0f} s, now {(relieve(), cur())[1]:.0f}, peak {mem():.0f} MB]")

XFILES = [os.path.join(CACHE, f"ko2_X230_{f}.f32") for f in FOOT]     # raw float32, lens order, (NL, 13, 25) each
INPASS = os.path.join(CACHE, "ko2_inpass.npz")
NBASE = 41
def base_x(ids, fi, Xnb, cls):
    """(n, 13, 41) base columns: own (lens class x 4 bands) + neighbour (5 groups x 5 bands)."""
    n = len(ids); x = np.zeros((n, NB, NBASE))
    own = OWN[ids, :, :, fi]
    for c in range(4):
        m = cls == c
        if m.any():
            x[m, :, 4 * c:4 * c + 4] = own[m]
    x[:, :, 16:] = Xnb
    return x
def acc_init():
    return dict(N=np.zeros((NPAT, NBASE, NBASE)), v=np.zeros((NPAT, NBASE)), vX=np.zeros((NPAT, NBASE)), u=np.zeros((NPAT, NBASE)))
def acc_add(A, ids, x, wwm=None, wg=None):
    ww = WW[ids, :NB] if wwm is None else wwm
    wg = (WG[ids, :NB] if wg is None else wg) * (ww > 0)
    Z = np.einsum("nb,nbk,nbl->nkl", ww, x, x, optimize=True)
    oh = sparse.csr_matrix((np.ones(len(ids)), (patch[ids], np.arange(len(ids)))), shape=(NPAT, len(ids)))
    A["N"] += (oh @ Z.reshape(len(ids), -1)).reshape(NPAT, NBASE, NBASE)
    A["v"] += oh @ np.einsum("nb,nbk->nk", 4 * G * wg, x)
    A["vX"] += oh @ np.einsum("nb,nbk->nk", 4 * G * WX[ids, :NB] * (ww > 0), x)
    A["u"] += oh @ np.einsum("nb,nbk->nk", ww[:, :7], x[:, :7])

if not (all(os.path.exists(f) for f in XFILES) and os.path.exists(INPASS)):
    P("\nneighbour pass: real positions and five shuffles; columns = real - mean(shuffles)")
    perms = [np.random.default_rng(52 + s).permutation(NL) for s in range(NSHUF)]
    XM = [open(fn + ".tmp", "wb") for fn in XFILES]
    ACC115 = [acc_init() for _ in FOOT]; ACCM2 = [acc_init() for _ in FOOT]
    npairs = {"real_230": 0, "real_115": 0, "shuf_230": 0}
    CH = 1200
    for c0 in range(0, NL, CH):
        ids = np.arange(c0, min(c0 + CH, NL))
        real, npr = chunk_columns(ids, xL[ids], selfN[ids], xN, chiN, ellN, GRP, treeN, (W_PRI, W_BR))
        npairs["real_230"] += npr[W_PRI]; npairs["real_115"] += npr[W_BR]
        sh = []
        for s in range(NSHUF):
            o, nps = chunk_columns(ids, xL[perms[s][ids]], selfN[perms[s][ids]], xN, chiN, ellN, GRP, treeN, (W_PRI, W_BR))
            sh.append(o); npairs["shuf_230"] += nps[W_PRI]
        X230 = real[W_PRI] - sum(o[W_PRI] for o in sh) / NSHUF
        X115 = real[W_BR] - sum(o[W_BR] for o in sh) / NSHUF
        XM2 = sh[0][W_PRI] - sum(o[W_PRI] for o in sh[1:]) / (NSHUF - 1)
        for fi in range(NF):
            sel = slice(fi, 10, 2)                               # footing fi of the 10 (band, footing) entries
            X230f = X230[..., sel].reshape(len(ids), NB, 25)
            XM[fi].write(np.ascontiguousarray(X230f, dtype=np.float32).tobytes())
            acc_add(ACC115[fi], ids, base_x(ids, fi, X115[..., sel].reshape(len(ids), NB, 25), CLS[ids]))
            acc_add(ACCM2[fi], ids, base_x(ids, fi, XM2[..., sel].reshape(len(ids), NB, 25), CLS[ids]))
        if (c0 // CH) % 10 == 0:
            P(f"  lenses {c0 + len(ids):,} / {NL:,}; pairs so far (real, 230 Mpc) {npairs['real_230']:,}  [{time.time() - T0:.0f} s, now {(relieve(), cur())[1]:.0f}, peak {mem():.0f} MB]")
    for fi in range(NF):
        XM[fi].close()
    del XM
    for fn in XFILES:
        os.replace(fn + ".tmp", fn)
    sv = {"npairs": np.array([npairs["real_230"], npairs["real_115"], npairs["shuf_230"]], float)}
    for fi in range(NF):
        for k in ("N", "v", "vX", "u"):
            sv[f"b115_{fi}_{k}"] = ACC115[fi][k]; sv[f"m2_{fi}_{k}"] = ACCM2[fi][k]
    np.savez(INPASS, **sv)
    P(f"neighbour pass done  [{time.time() - T0:.0f} s, now {(relieve(), cur())[1]:.0f}, peak {mem():.0f} MB]")
IP = dict(np.load(INPASS))
NPAIRS = IP["npairs"]
P(f"\npairs inside reach: real 230 Mpc {int(NPAIRS[0]):,} ({NPAIRS[0] / NL:.0f} per lens), 115 Mpc {int(NPAIRS[1]):,}; around shuffled positions {int(NPAIRS[2]) / NSHUF:,.0f} per shuffle")
def read_X(fi, c0, n):
    """the stored neighbour columns of lenses c0 .. c0 + n - 1 (float64)."""
    return np.fromfile(XFILES[fi], dtype=np.float32, count=n * NB * 25, offset=c0 * NB * 25 * 4).reshape(n, NB, 25).astype(np.float64)
del TAB, TABF                                                      # the tables are not needed after the pass

# ------------------------------------------------------------------ post-pass accumulation (window 230) for every specification
zmed = float(np.median(zl))
q1, q2 = np.quantile(logMs, [1 / 3, 2 / 3]); terc = np.digitize(logMs, [q1, q2])
cellid = terc * 2 + (zl > zmed)
rngm = np.random.default_rng(52); typP = typ.copy()
for cid in np.unique(cellid):
    ii = np.where(cellid == cid)[0]; typP[ii] = typ[ii][rngm.permutation(len(ii))]
CLS_M1 = class_of(logMs, np.where(typP == 1, 3.0, 1.0), giant_ok=False)
binmask = {"all": np.ones(NB), "no_bin3": np.r_[1, 1, 1, 0, np.ones(9)], "no_bin0": np.r_[0, np.ones(12)]}
SPECS = {"main": dict(lens=None, bins="all"), "zlow": dict(lens=zl <= zmed, bins="all"), "zhigh": dict(lens=zl > zmed, bins="all"),
         "no_bin3": dict(lens=None, bins="no_bin3"), "no_bin0": dict(lens=None, bins="no_bin0"), "hostfree_ko1": dict(lens=HFK, bins="all")}
def law_k_cells(Mg_arr, k, fi):
    """the law's cells (n, 13) at mass k Mgal for footing fi (KO1's quadrature)."""
    out = np.zeros((len(Mg_arr), NB))
    for b in range(NB):
        t_lo = G * Mg_arr / EDGES[b + 1]; t_hi = np.minimum(G * Mg_arr / EDGES[b], R3); ok = t_hi > t_lo
        t = t_lo[:, None] + (t_hi - t_lo)[:, None] * (XG[None, :] + 1) / 2
        out[:, b] = np.where(ok, (glaw(k * G * Mg_arr[:, None] / t, A0[FOOT[fi]]) * WGL[None, :]).sum(1) / 2, 0.0)
    return out
ACC = {fi: {s: acc_init() for s in list(SPECS) + ["M1", "M3"]} for fi in range(NF)}
VK = {fi: np.zeros((len(KGRID), NPAT, NBASE)) for fi in range(NF)}
WG_M3 = WG[:, :NB].copy(); WG_M3[np.ix_(typ == 0, np.arange(7))] *= 0.4
CH = 5000
for fi in range(NF):
    for c0 in range(0, NL, CH):
        ids = np.arange(c0, min(c0 + CH, NL))
        Xnb = read_X(fi, c0, len(ids))
        x = base_x(ids, fi, Xnb, CLS[ids])
        for s, sp in SPECS.items():
            ww = WW[ids, :NB] * binmask[sp["bins"]][None, :]
            if sp["lens"] is not None:
                ww = ww * sp["lens"][ids][:, None]
            acc_add(ACC[fi][s], ids, x, wwm=ww)
        acc_add(ACC[fi]["M3"], ids, x, wg=WG_M3[ids])
        oh = sparse.csr_matrix((np.ones(len(ids)), (patch[ids], np.arange(len(ids)))), shape=(NPAT, len(ids)))
        for kk in range(len(KGRID)):
            VK[fi][kk] += oh @ np.einsum("nb,nbk->nk", WW[ids, :NB] * law_k_cells(Mg[ids], KGRID[kk], fi), x)
        acc_add(ACC[fi]["M1"], ids, base_x(ids, fi, Xnb, CLS_M1[ids]))
    P(f"post-pass sums, footing {FOOT[fi]}  [{time.time() - T0:.0f} s, now {(relieve(), cur())[1]:.0f}, peak {mem():.0f} MB]")

# ------------------------------------------------------------------ designs (linear maps from the 41 base columns)
def own_col(c, B): return 4 * c + B
def nb_col(g, B): return 16 + 5 * g + B
def design(kind, closure="continued"):
    """returns T (41 x p) and the parameter names."""
    cols, names = [], []
    def add(entries, name):
        v = np.zeros(NBASE)
        for e_ in entries: v[e_] += 1.0
        cols.append(v); names.append(name)
    far = [4] if closure == "continued" else []
    if kind == "primary":
        for c in range(5):
            o = c < 4
            add(([own_col(c, 0)] if o else []) + [nb_col(c, 0)], (c, "centre"))
            add(([own_col(c, 1)] if o else []) + [nb_col(c, 1)], (c, "inner"))
            add(([own_col(c, 2), own_col(c, 3)] if o else []) + [nb_col(c, 2), nb_col(c, 3)] + [nb_col(c, B) for B in far], (c, "ext"))
    elif kind == "secondary":
        for c in range(5):
            o = c < 4
            add(([own_col(c, 0)] if o else []) + [nb_col(c, 0)], (c, "centre"))
            add(([own_col(c, 1)] if o else []) + [nb_col(c, 1)], (c, "inner"))
            add(([own_col(c, 2)] if o else []) + [nb_col(c, 2)], (c, "middle"))
            add(([own_col(c, 3)] if o else []) + [nb_col(c, 3)] + [nb_col(c, B) for B in far], (c, "outer"))
    elif kind == "untied":
        for c in range(4):
            add([own_col(c, 0)], (c, "centre")); add([own_col(c, 1)], (c, "inner")); add([own_col(c, 2), own_col(c, 3)], (c, "ext"))
        for g in range(5):
            add([nb_col(g, 0)], ("nb", g, "centre")); add([nb_col(g, 1)], ("nb", g, "inner"))
            add([nb_col(g, 2), nb_col(g, 3)] + [nb_col(g, B) for B in far], ("nb", g, "ext"))
    elif kind == "own_primary":
        for c in range(4):
            add([own_col(c, 0)], (c, "centre")); add([own_col(c, 1)], (c, "inner")); add([own_col(c, 2), own_col(c, 3)], (c, "ext"))
    elif kind == "own_secondary":
        for c in range(4):
            add([own_col(c, 0)], (c, "centre")); add([own_col(c, 1)], (c, "inner")); add([own_col(c, 2)], (c, "middle")); add([own_col(c, 3)], (c, "outer"))
    return np.array(cols).T, names
def solve(A, T, vkey="v", vvec=None):
    """amplitudes and the 50 delete-one-patch amplitudes."""
    N = A["N"]; v = A[vkey] if vvec is None else vvec
    Nt, vt = N.sum(0), v.sum(0)
    M = T.T @ Nt @ T; b = T.T @ vt
    sc = 1 / np.sqrt(np.diag(M))
    a = sc * np.linalg.solve(M * sc[:, None] * sc[None, :], b * sc)
    al = np.zeros((NPAT, T.shape[1]))
    for p in range(NPAT):
        Mp = T.T @ (Nt - N[p]) @ T; bp = T.T @ (vt - v[p])
        al[p] = sc * np.linalg.solve(Mp * sc[:, None] * sc[None, :], bp * sc)
    return a, al
def jk(xl):
    xl = np.asarray(xl); return float(np.sqrt((NPAT - 1) / NPAT * ((xl - xl.mean(0)) ** 2).sum(0)))
# class weights per type (weights only): W_tm ~ sum WW (law cell)^2
WCL = {}
for fi in range(NF):
    w = np.array([float((WW[CLS == c, :NB] * LAW1[CLS == c, :, fi] ** 2).sum()) for c in range(4)])
    WCL[fi] = {0: w[:2] / w[:2].sum(), 1: w[2:] / w[2:].sum()}
def ratio_stat(a, al, names, fi, num_band, den_band="inner"):
    """R(t) = sum_m W a[(t,m), num] / sum_m W a[(t,m), den], per type, with jackknife; also the numerator and denominator."""
    out = {}
    for t in (0, 1):
        cs = (2 * t, 2 * t + 1); W = WCL[fi][t]
        inum = [names.index((c, num_band)) for c in cs]; iden = [names.index((c, den_band)) for c in cs]
        num, den = float(W @ a[inum]), float(W @ a[iden]); numl, denl = al[:, inum] @ W, al[:, iden] @ W
        out[t] = dict(R=num / den, s=jk(numl / denl), Rl=numl / denl, num=num, s_num=jk(numl), numl=numl, den=den, s_den=jk(denl), denl=denl)
    return out
def floor_of(fi, kind, num_band):
    T, names = design(kind)
    fl = {0: [], 1: []}
    for kk in range(len(KGRID)):
        A = ACC[fi]["main"]
        a, al = solve(A, T, vvec=VK[fi][kk])
        r = ratio_stat(a, al, names, fi, num_band)
        for t in (0, 1): fl[t].append(r[t]["R"])
    return {t: (float(min(v)), [float(x) for x in v]) for t, v in fl.items()}
def label_of(R, s_jk, floor):
    st = math.sqrt(s_jk ** 2 + S_SYS ** 2)
    if st > (floor - ABSENT_LINE) / 2: return "NO POWER", st
    hi, lo = R + 2 * st, R - 2 * st
    if hi >= floor and lo > ABSENT_LINE: return "PRESENT", st
    if hi < floor and lo <= ABSENT_LINE: return "ABSENT", st
    if hi < floor and lo > ABSENT_LINE: return "REDUCED", st
    return "NOT SEPARATED", st
DEFINITE = ("PRESENT", "ABSENT", "REDUCED")
TYPN = {0: "late", 1: "early"}
def rd(x, n=4):
    return None if x is None else round(float(x), n)

# ------------------------------------------------------------------ KA-3b plants, KA-4 halvings, null
P("\nKA-3b: plant and recover (model at chosen amplitudes + the measured cross-shear sums as noise)")
Tp, Np_ = design("primary")
RES = dict(lane="KO2", criteria="59e3c9ee9a", constants=dict(G=G, Msun=Msun, Mpc=Mpc, a0=A0, window=W_PRI, bracket_window=W_BR, reach=REACH,
           shuffles=NSHUF, s_sys=S_SYS, absent_line=ABSENT_LINE, kgrid=KGRID), thresholds=dict(late=THR[0], early=THR[1], on=on_thr, within_1e4=near_thr),
           classes=dict(lenses={CLS_NAMES[c]: int((CLS == c).sum()) for c in range(4)}, pool={CLS_NAMES[c]: int((GRP == c).sum()) for c in range(5)}),
           pairs=dict(real_230=int(NPAIRS[0]), real_115=int(NPAIRS[1]), shuffled_230_per_shuffle=float(NPAIRS[2] / NSHUF)), foot={})
FLOORS = {fi: dict(primary=floor_of(fi, "own_primary", "ext"), secondary=floor_of(fi, "own_secondary", "outer"), mid=floor_of(fi, "own_secondary", "middle")) for fi in range(NF)}
ka3b_ok = True; PLANTS = {}
for fi, f in enumerate(FOOT):
    A = ACC[fi]["main"]; PLANTS[f] = {}
    for pname, atrue in (("law everywhere", np.ones(len(Np_))),
                         ("late truncated", np.array([0.0 if (nm[0] in (0, 1) and nm[1] == "ext") else 1.0 for nm in Np_]))):
        vpl = np.einsum("pkl,l->pk", A["N"], Tp @ atrue) + A["vX"]
        a, al = solve(A, Tp, vvec=vpl)
        sa = np.array([jk(al[:, k]) for k in range(len(Np_))])
        within = bool(np.all(np.abs(a - atrue) <= 3 * sa))
        ka3b_ok &= within
        r = ratio_stat(a, al, Np_, fi, "ext")
        labs = {TYPN[t]: label_of(r[t]["R"], r[t]["s"], FLOORS[fi]["primary"][t][0])[0] for t in (0, 1)}
        PLANTS[f][pname] = dict(all_within_3sigma=within, max_pull=float(np.max(np.abs(a - atrue) / sa)),
                                R_ext={TYPN[t]: (r[t]["R"], r[t]["s"]) for t in (0, 1)}, labels=labs)
        P(f"  {f:9s} {pname:15s}: all amplitudes within 3 sigma {within} (max pull {np.max(np.abs(a - atrue) / sa):.2f}); "
          f"R_ext late {r[0]['R']:+.3f} +- {r[0]['s']:.3f}, early {r[1]['R']:+.3f} +- {r[1]['s']:.3f}; labels {labs}")
check("KA-3b plants recovered: every amplitude within 3 jackknife sigma (two plants, both footings)", ka3b_ok, "see lines above")

P("\nKA-4: 100 random halvings of the lenses (seed 52), weighted ext amplitude per type")
hrng = np.random.default_rng(52); HALF = hrng.random((100, NL)) < 0.5
ka4 = {}
for fi in range(NF):
    Zl = np.zeros((NL, len(Np_), len(Np_))); vl = np.zeros((NL, len(Np_)))
    for c0 in range(0, NL, CH):
        ids = np.arange(c0, min(c0 + CH, NL))
        x = base_x(ids, fi, read_X(fi, c0, len(ids)), CLS[ids]) @ Tp
        Zl[ids] = np.einsum("nb,nbk,nbl->nkl", WW[ids, :NB], x, x, optimize=True)
        vl[ids] = np.einsum("nb,nbk->nk", 4 * G * WG[ids, :NB], x)
    zz = {0: [], 1: []}; npp = len(Np_)
    Z2 = Zl.reshape(NL, npp * npp)
    for h in range(100):
        grp = patch * 2 + HALF[h].astype(np.int64)
        oh = sparse.csr_matrix((np.ones(NL), (grp, np.arange(NL))), shape=(2 * NPAT, NL))
        SZ = oh @ Z2; SV = oh @ vl
        res_h = []
        for hv in (1, 0):
            Ah = dict(N=SZ[hv::2].reshape(NPAT, npp, npp), v=SV[hv::2])
            a, al = solve(Ah, np.eye(npp))
            res_h.append(ratio_stat(a, al, Np_, fi, "ext"))
        for t in (0, 1):
            zz[t].append((res_h[0][t]["num"] - res_h[1][t]["num"]) / math.hypot(res_h[0][t]["s_num"], res_h[1][t]["s_num"]))
    ka4[fi] = {t: float(np.std(zz[t])) for t in (0, 1)}
    del Zl, vl, Z2
check("KA-4 std of z over 100 random halvings in [0.8, 1.2] for each type (both footings)",
      all(0.8 <= ka4[fi][t] <= 1.2 for fi in range(NF) for t in (0, 1)),
      "; ".join(f"{FOOT[fi]} late {ka4[fi][0]:.3f}, early {ka4[fi][1]:.3f}" for fi in range(NF)))

P("\nNull: the fit with the cross-shear sums WX in place of WG")
nullok = True; NULL = {}
for fi, f in enumerate(FOOT):
    a, al = solve(ACC[fi]["main"], Tp, vkey="vX"); r = ratio_stat(a, al, Np_, fi, "ext"); NULL[f] = {}
    for t in (0, 1):
        zi = r[t]["den"] / r[t]["s_den"]; ze = r[t]["num"] / r[t]["s_num"]
        nullok &= abs(zi) <= 2.5 and abs(ze) <= 2.5
        NULL[f][TYPN[t]] = dict(inner=(r[t]["den"], r[t]["s_den"]), ext=(r[t]["num"], r[t]["s_num"]))
        P(f"  {f:9s} {TYPN[t]:5s}: weighted inner {r[t]['den']:+.3e} +- {r[t]['s_den']:.3e} ({zi:+.2f} sigma); ext {r[t]['num']:+.3e} +- {r[t]['s_num']:.3e} ({ze:+.2f} sigma)")
check("Null: cross-shear weighted inner and ext amplitudes within 2.5 sigma of zero (each type, both footings)", nullok, "see lines above")

# ------------------------------------------------------------------ the primary fit, brackets, labels
def share_nb(A, T, a, al):
    """neighbour share of the model in bins 0-6: (u_nb . T a) / (u . T a), with jackknife."""
    u = A["u"]; ut = u.sum(0)
    def sh(uu, aa):
        ta = T @ aa; return float(uu[16:] @ ta[16:]) / float(uu @ ta)
    s0 = sh(ut, a); sl = np.array([sh(ut - u[p], al[p]) for p in range(NPAT)])
    return s0, jk(sl), sl
for fi, f in enumerate(FOOT):
    P(f"\n================ footing {f} (a0 {A0[f]:.4e})")
    F = {}
    fl_p = FLOORS[fi]["primary"]; fl_s = FLOORS[fi]["secondary"]
    P(f"  law's floor (own-only fit to the law at mass factors {KGRID}): R_ext late {fl_p[0][0]:.4f}, early {fl_p[1][0]:.4f}; "
      f"R_own late {fl_s[0][0]:.4f}, early {fl_s[1][0]:.4f}")
    F["floor"] = dict(primary={TYPN[t]: fl_p[t] for t in (0, 1)}, secondary={TYPN[t]: fl_s[t] for t in (0, 1)}, mid={TYPN[t]: FLOORS[fi]["mid"][t] for t in (0, 1)})
    fits = {}
    for nm, (A, kind, clo) in {"primary": (ACC[fi]["main"], "primary", "continued"), "B1 window 115": (dict((k, IP[f"b115_{fi}_{k}"]) for k in ("N", "v", "vX", "u")), "primary", "continued"),
                               "B2 closure zero": (ACC[fi]["main"], "primary", "zero"), "B3 untied": (ACC[fi]["main"], "untied", "continued"),
                               "secondary": (ACC[fi]["main"], "secondary", "continued")}.items():
        T, names = design(kind, clo); a, al = solve(A, T)
        nb_ = "outer" if kind == "secondary" else "ext"
        r = ratio_stat(a, al, names, fi, nb_)
        fl = fl_s if kind == "secondary" else fl_p
        labs = {t: label_of(r[t]["R"], r[t]["s"], fl[t][0]) for t in (0, 1)}
        fits[nm] = dict(T=T, names=names, a=a, al=al, r=r, labs=labs, A=A)
        if kind == "secondary":
            fits[nm]["rmid"] = ratio_stat(a, al, names, fi, "middle")
    final = {}
    for t in (0, 1):
        lab = fits["primary"]["labs"][t][0]
        contra = [nm for nm in ("B1 window 115", "B2 closure zero", "B3 untied") if fits[nm]["labs"][t][0] in DEFINITE and lab in DEFINITE and fits[nm]["labs"][t][0] != lab]
        if contra: lab = "NOT SEPARATED"
        if not all(CHK.values()): lab = "NO VERDICT"
        final[t] = (lab, contra)
    for nm, ft in fits.items():
        P(f"  {nm:16s}: " + ";  ".join(f"{TYPN[t]} R {ft['r'][t]['R']:+.3f} +- {ft['r'][t]['s']:.3f} (s_tot {ft['labs'][t][1]:.3f}) -> {ft['labs'][t][0]}" for t in (0, 1)))
    for t in (0, 1):
        P(f"  >>> KO2 {f} {TYPN[t].upper()}: {final[t][0]}" + (f"  (bracket contradiction: {final[t][1]})" if final[t][1] else ""))
    pr = fits["primary"]
    s0, ss_, _ = share_nb(pr["A"], pr["T"], pr["a"], pr["al"])
    d_el = pr["r"][1]["R"] - pr["r"][0]["R"]; s_el = jk(pr["r"][1]["Rl"] - pr["r"][0]["Rl"])
    P(f"  R2 early - late R_ext {d_el:+.3f} +- {s_el:.3f} ({d_el / s_el:+.2f} sigma);  R5 neighbour share of the model in bins 0-6 {s0:.3f} +- {ss_:.3f}")
    P("  R1 primary amplitudes (centre / inner / ext): " + "; ".join(f"{CLS_NAMES[c]} " + "/".join(f"{pr['a'][pr['names'].index((c, B))]:+.2f}({jk(pr['al'][:, pr['names'].index((c, B))]):.2f})" for B in ("centre", "inner", "ext")) for c in range(5)))
    sc = fits["secondary"]
    P("  R1 secondary amplitudes (centre / inner / middle / outer): " + "; ".join(f"{CLS_NAMES[c]} " + "/".join(f"{sc['a'][sc['names'].index((c, B))]:+.2f}({jk(sc['al'][:, sc['names'].index((c, B))]):.2f})" for B in ("centre", "inner", "middle", "outer")) for c in range(5)))
    P(f"  R1 R_mid = a[middle]/a[inner] (secondary): late {sc['rmid'][0]['R']:+.3f} +- {sc['rmid'][0]['s']:.3f}, early {sc['rmid'][1]['R']:+.3f} +- {sc['rmid'][1]['s']:.3f}")
    rep = {}
    for nm in ("zlow", "zhigh", "no_bin3", "no_bin0", "hostfree_ko1"):
        a, al = solve(ACC[fi][nm], pr["T"]); r = ratio_stat(a, al, pr["names"], fi, "ext"); rep[nm] = r
        P(f"  {'R3' if nm.startswith('z') else ('R4' if nm.startswith('no') else 'R6')} {nm:12s}: late {r[0]['R']:+.3f} +- {r[0]['s']:.3f}, early {r[1]['R']:+.3f} +- {r[1]['s']:.3f}")
    zd = {t: (rep["zhigh"][t]["R"] - rep["zlow"][t]["R"], jk(rep["zhigh"][t]["Rl"] - rep["zlow"][t]["Rl"])) for t in (0, 1)}
    zflag = {t: zd[t][0] > 2 * zd[t][1] for t in (0, 1)}
    P(f"  R3 high - low z: late {zd[0][0]:+.3f} +- {zd[0][1]:.3f}, early {zd[1][0]:+.3f} +- {zd[1][1]:.3f}; flag (unseen neighbours in the own term) {zflag}")
    # R7: KO1-style plain stacks, all late and all early
    r7 = {}
    for t in (0, 1):
        m = typ == t; L = KO1LAW[f]
        ro, rm_, ri = amp_ko1(m, L, OUTERW), amp_ko1(m, L, MIDW), amp_ko1(m, L, INNERW)
        Rl_ = ro["Al"] / ri["Al"]
        r7[TYPN[t]] = dict(outer=(ro["A"], ro["s"]), middle=(rm_["A"], rm_["s"]), inner=(ri["A"], ri["s"]), R_s=(ro["A"] / ri["A"], jk(Rl_)))
    P("  R7 KO1-style plain stacks, all lenses: " + "; ".join(f"{k} outer {v['outer'][0]:.3f} +- {v['outer'][1]:.3f} | middle {v['middle'][0]:.3f} +- {v['middle'][1]:.3f} | "
                                                          f"inner {v['inner'][0]:.3f} +- {v['inner'][1]:.3f} | R_s {v['R_s'][0]:.3f} +- {v['R_s'][1]:.3f}" for k, v in r7.items()))
    F.update(label={TYPN[t]: final[t][0] for t in (0, 1)}, bracket_contradictions={TYPN[t]: final[t][1] for t in (0, 1)},
             fits={nm: dict(names=[str(x) for x in ft["names"]], a=ft["a"], s=[jk(ft["al"][:, k]) for k in range(len(ft["names"]))],
                            R={TYPN[t]: dict(R=ft["r"][t]["R"], s_jk=ft["r"][t]["s"], s_tot=ft["labs"][t][1], label=ft["labs"][t][0],
                                             num=ft["r"][t]["num"], s_num=ft["r"][t]["s_num"], den=ft["r"][t]["den"], s_den=ft["r"][t]["s_den"]) for t in (0, 1)},
                            **({"R_mid": {TYPN[t]: (ft["rmid"][t]["R"], ft["rmid"][t]["s"]) for t in (0, 1)}} if "rmid" in ft else {}))
                   for nm, ft in fits.items()},
             early_minus_late=(d_el, s_el), neighbour_share_bins0_6=(s0, ss_),
             reported={nm: {TYPN[t]: (r[t]["R"], r[t]["s"]) for t in (0, 1)} for nm, r in rep.items()},
             z_high_minus_low={TYPN[t]: zd[t] for t in (0, 1)}, z_flag={TYPN[t]: bool(zflag[t]) for t in (0, 1)}, R7_plain_stacks=r7,
             plants=PLANTS[f], null=NULL[f], ka4={TYPN[t]: ka4[fi][t] for t in (0, 1)})
    RES["foot"][f] = F
    # ---------------------------------------------------------------- MUTATE (separate outputs)
    PM(f"================ footing {f}")
    MUTR = {}
    # M1 type labels permuted within mass tercile x z half
    a, al = solve(ACC[fi]["M1"], pr["T"]); r1 = ratio_stat(a, al, pr["names"], fi, "ext")
    d1 = r1[1]["R"] - r1[0]["R"]; s1 = jk(r1[1]["Rl"] - r1[0]["Rl"]); power1 = abs(d_el / s_el) >= 2
    checkm(f"M1 permuted type labels: early - late within 2 sigma of zero ({f})", abs(d1 / s1) < 2,
           f"permuted {d1:+.3f} +- {s1:.3f} ({d1 / s1:+.2f} sigma); true {d_el:+.3f} +- {s_el:.3f} ({d_el / s_el:+.2f} sigma)" + ("" if power1 else "  [the true difference is inside 2 sigma: M1 has no power]"))
    MUTR["M1"] = dict(diff=d1, s=s1, true=(d_el, s_el), has_power=bool(power1), R={TYPN[t]: (r1[t]["R"], r1[t]["s"]) for t in (0, 1)})
    # M2 neighbour positions shuffled
    AM2 = dict((k, IP[f"m2_{fi}_{k}"]) for k in ("N", "v", "vX", "u"))
    a, al = solve(AM2, pr["T"]); s2, ss2, _ = share_nb(AM2, pr["T"], a, al); r2 = ratio_stat(a, al, pr["names"], fi, "ext")
    power2 = abs(s0 / ss_) >= 2
    checkm(f"M2 neighbour positions shuffled: neighbour share in bins 0-6 within 2 sigma of zero ({f})", abs(s2 / ss2) < 2,
           f"shuffled {s2:+.3f} +- {ss2:.3f} ({s2 / ss2:+.2f} sigma); true {s0:+.3f} +- {ss_:.3f} ({s0 / ss_:+.2f} sigma); R_ext late {r2[0]['R']:+.3f}, early {r2[1]['R']:+.3f}"
           + ("" if power2 else "  [the true share is inside 2 sigma: M2 has no power]"))
    MUTR["M2"] = dict(share=(s2, ss2), true=(s0, ss_), has_power=bool(power2), R={TYPN[t]: (r2[t]["R"], r2[t]["s"]) for t in (0, 1)})
    # M3 late signal x 0.4 in bins 0-6
    a, al = solve(ACC[fi]["M3"], pr["T"]); r3 = ratio_stat(a, al, pr["names"], fi, "ext")
    d3 = r3[0]["R"] - pr["r"][0]["R"]; s3 = jk(r3[0]["Rl"] - pr["r"][0]["Rl"])
    checkm(f"M3 late WG x 0.4 in bins 0-6: R_ext(late) falls by more than 2 sigma ({f})", d3 < -2 * s3,
           f"mutated {r3[0]['R']:+.3f} +- {r3[0]['s']:.3f} against {pr['r'][0]['R']:+.3f}; change {d3:+.3f} +- {s3:.3f} ({d3 / s3:+.2f} sigma)")
    MUTR["M3"] = dict(R_late=(r3[0]["R"], r3[0]["s"]), change=(d3, s3))
    RES.setdefault("mutate", {})[f] = MUTR

# ------------------------------------------------------------------ wrap up
P("\n================ result")
kas_ok = all(CHK.values())
for f in FOOT:
    P(f"  KO2 {f}: LATE {RES['foot'][f]['label']['late']}, EARLY {RES['foot'][f]['label']['early']}   "
      f"(R_ext late {RES['foot'][f]['fits']['primary']['R']['late']['R']:+.3f} +- {RES['foot'][f]['fits']['primary']['R']['late']['s_tot']:.3f}, "
      f"early {RES['foot'][f]['fits']['primary']['R']['early']['R']:+.3f} +- {RES['foot'][f]['fits']['primary']['R']['early']['s_tot']:.3f} (s_tot); "
      f"secondary R_own late {RES['foot'][f]['fits']['secondary']['R']['late']['label']}, early {RES['foot'][f]['fits']['secondary']['R']['early']['label']})")
P(f"  checks: {sum(CHK.values())} of {len(CHK)} pass" + ("" if kas_ok else "  -> NO VERDICT: " + ", ".join(k for k, v in CHK.items() if not v)))
PM(f"MUTATE: {sum(CHKM.values())} of {len(CHKM)} bite")
RES["checks"] = CHK; RES["runtime_s"] = round(time.time() - T0, 1)
P(f"  runtime {RES['runtime_s']} s")
P("\nkappa = 1/2 FITTED; not theory closed. Adopts nothing.")
PM("kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
def clean(o):
    if isinstance(o, dict): return {str(k): clean(v) for k, v in o.items() if not str(k).startswith("_")}
    if isinstance(o, (list, tuple)): return [clean(v) for v in o]
    if isinstance(o, np.ndarray): return [clean(v) for v in o.tolist()]
    if isinstance(o, (np.floating, float)): return float(o) if np.isfinite(o) else None
    if isinstance(o, np.integer): return int(o)
    if isinstance(o, np.bool_): return bool(o)
    return o
mut = RES.pop("mutate", {})
json.dump(clean(RES), open(os.path.join(HERE, "ko2.json"), "w"), indent=1)
open(os.path.join(HERE, "ko2.out"), "w").write("\n".join(OUT) + "\n")
json.dump(clean(dict(lane="KO2", criteria="59e3c9ee9a", mutate=mut, checks=CHKM)), open(os.path.join(HERE, "ko2_MUTATE.json"), "w"), indent=1)
open(os.path.join(HERE, "ko2_MUTATE.out"), "w").write("\n".join(OUTM) + "\n")
sys.exit(0 if kas_ok else 1)
