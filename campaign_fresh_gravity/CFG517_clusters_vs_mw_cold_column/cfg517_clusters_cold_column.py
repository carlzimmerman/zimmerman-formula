#!/usr/bin/env python3
"""CFG517: do galaxy-cluster counts avoid the directions where the Milky Way's cold energy column is largest?

Frozen criteria: FROZEN_CRITERIA.md (committed alone first, 05fd82e81).
Cold-column maps: CFG514's QUMOND phantom (nu_mono, McMillan 2017 baryons; CFG514's committed code executed, not edited):
  ROUND = spherical shell average of the phantom (CFG514 MUTATE = CFG516 RM-phi; primary), DISC = full phantom (comparison).
Catalogues (on disk): PSZ2 union (primary), eRASS1 primary (robustness; X-ray foreground confound declared), MCXC (info).
Statistic: Poisson regression of NSIDE-32 pixel counts on x = ln C at fixed |b| band x hemisphere, SFD dust, ecliptic latitude.
CFG517_MUTATE=1: the cold map is rotated by 180 deg in longitude (towards <-> away from the GC); outputs *_MUTATE.
kappa = 1/2 is FITTED; both footings; the cold energy's mass is still required; not theory closed.
Run:  nice -n 15 python3 cfg517_clusters_cold_column.py   (<= 4 threads)
"""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ[_v] = "4"
import sys, json, math, time
import numpy as np
import healpy as hp
from astropy.io import fits
from astropy.wcs import WCS
from astropy.coordinates import SkyCoord
import astropy.units as u
from scipy.interpolate import RegularGridInterpolator

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
DATA = os.path.join(REPO, "real_research", "data")
MCXC_PATH = os.path.join(REPO, "gext_vectors_2026", "data", "raw", "mcxc.tsv")
SRC514 = os.path.join(HERE, "..", "CFG514_directional_milky_way", "cfg514_directional.py")
MUTATE = os.environ.get("CFG517_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUTATE else ""
ROT_MUT = 180.0 if MUTATE else 0.0
NSIDE, NSUB = 32, 256
ROTS = np.arange(40.0, 321.0, 10.0)          # 29 rotation-null offsets
OUT, CHECKS = [], []
rng_master = np.random.default_rng(517)


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True); OUT.append(s)


def check(cond, msg):
    CHECKS.append((bool(cond), msg)); P(f"  [{'PASS' if cond else 'FAIL'}] {msg}")
    return bool(cond)


T0 = time.time()
P("=" * 110)
P(f"CFG517 clusters vs the Milky Way's predicted cold-energy column  {'*** MUTATE: map rotated 180 deg in l ***' if MUTATE else 'PRIMARY'}")
P("=" * 110)

# ================================================================== 1. cold-column maps from CFG514's solver
src = open(SRC514).read()
head = src.split("# ------------------------------------------------------------------ build the framework / rival")[0]
ns = {"__file__": os.path.abspath(SRC514)}
exec(compile(head, "cfg514_head", "exec"), ns)
G, R0, A0 = ns["G"], ns["R0"], ns["A0"]
Grid, nu_mono, rho_baryon = ns["Grid"], ns["nu_mono"], ns["rho_baryon"]
phi_kepler = ns["phi_kepler"]
GR = Grid()
rho_b1 = rho_baryon(GR.RR, GR.ZZ)
Mb1 = 2 * np.sum(2 * math.pi * rho_b1 * GR.VOL)
phNR, phNZ = phi_kepler(Mb1, GR.rbR), phi_kepler(Mb1, GR.rbZ)
PhiN1 = GR.poisson(rho_b1, phNR, phNZ)
P(f"McMillan17 baryons on CFG514's grid: M_b = {Mb1:.4e} Msun (CFG514: 6.64e10)")

S_GRID = np.concatenate([[0], np.geomspace(1e-3, 100.0, 1500)])
LGRID = np.arange(0.0, 180.01, 1.0)
BGRID = np.arange(0.0, 90.01, 1.0)


def sight(l, b, s):
    l, b = np.radians(l), np.radians(b)
    X = R0 - s * np.cos(l) * np.cos(b); Y = s * np.sin(l) * np.cos(b); Z = s * np.sin(b)
    return np.hypot(X, Y), Z


def column_table(rho):
    """C(l, b) on l in [0,180], b in [0,90] (axisymmetric, mirror-symmetric model), Msun/pc^2 to 100 kpc."""
    it = RegularGridInterpolator((GR.Rc, GR.zc), rho, bounds_error=False, fill_value=None)
    tab = np.zeros((len(LGRID), len(BGRID)))
    for i, l in enumerate(LGRID):
        R, Z = sight(l, BGRID[:, None], S_GRID[None, :])
        R = np.clip(R, GR.Rc[0], GR.Rc[-1]); Z = np.clip(np.abs(Z), GR.zc[0], GR.zc[-1])
        v = it(np.stack([R, Z], -1))
        tab[i] = np.trapz(v, S_GRID, axis=1) / 1e6
    return RegularGridInterpolator((LGRID, BGRID), tab)


def fold_l(l):
    l = np.mod(l, 360.0)
    return np.where(l > 180, 360 - l, l)


def round_column_table(rho):
    """ROUND map, computed as a true angle average.
    Post-freeze numerical fix (disclosed): CFG514's Grid.shell_average assigns each cell the mean of the cells whose
    centres share a 3% log-r bin; with few cells per bin that mean is taken at a few polar angles only, so the
    'round' field carried +-10% angular noise (found by the M0 diagnostics on the first run). Here
    rho_bar(r) = int_0^1 rho_ph(R = r sqrt(1 - mu^2), z = r mu) dmu (400 mu points, the solver's own interpolated field),
    which is the spherical shell average of rho_ph, and C(psi) = int_0^100 rho_bar(|r_sun + s n|) ds."""
    it = RegularGridInterpolator((GR.Rc, GR.zc), rho, bounds_error=False, fill_value=None)
    rr = np.geomspace(1e-3, 120.0, 3000); mu = (np.arange(400) + 0.5) / 400
    R = np.clip(rr[:, None] * np.sqrt(1 - mu[None, :] ** 2), GR.Rc[0], GR.Rc[-1]); Z = np.clip(rr[:, None] * mu[None, :], GR.zc[0], GR.zc[-1])
    rbar = it(np.stack([R, Z], -1)).mean(1)
    psig = np.linspace(0, 180, 3601)
    r_s = np.sqrt(R0 ** 2 + S_GRID[None, :] ** 2 - 2 * R0 * S_GRID[None, :] * np.cos(np.radians(psig))[:, None])
    Cpsi = np.trapz(np.interp(r_s, rr, rbar), S_GRID, axis=1) / 1e6
    LL, BB = np.meshgrid(LGRID, BGRID, indexing="ij")
    ps = np.degrees(np.arccos(np.clip(np.cos(np.radians(LL)) * np.cos(np.radians(BB)), -1, 1)))
    # enclosed-mass consistency vs the grid's cell sum (CFG514 K5 analogue)
    Mbar = np.trapz(4 * np.pi * rr ** 2 * rbar, rr)
    Mgrid = GR.enclosed(rho, np.array([120.0]))[0]
    return RegularGridInterpolator((LGRID, BGRID), np.interp(ps, psig, Cpsi)), float(Mbar / Mgrid - 1)


MAPS = {}
MCHK = {}
for foot in ("canonical", "alt"):
    a0 = A0[foot]
    dR, dz = GR.grad(PhiN1, phNR, phNZ)
    nu_c = nu_mono(np.hypot(dR, dz) / a0)
    rho_ph = GR.phantom_source(PhiN1, phNR, phNZ, nu_c)
    MAPS[f"ROUND_{foot}"], MCHK[foot] = round_column_table(rho_ph)
    MAPS[f"DISC_{foot}"] = column_table(rho_ph)
    P(f"  ROUND_{foot}: angle-averaged profile M(<120 kpc) vs grid cell sum: {MCHK[foot]:+.3%}")
P(f"column tables built ({time.time()-T0:.0f} s)")


def colmap(name, l, b, dl=0.0):
    """column at (l, b) of the map rotated by dl in longitude (value at l is the unrotated map's value at l - dl)."""
    return MAPS[name](np.stack([fold_l(np.asarray(l) - dl), np.abs(np.asarray(b))], -1))


# ---- pixels
NPIX = hp.nside2npix(NSIDE)
PL, PB = hp.pix2ang(NSIDE, np.arange(NPIX), nest=True, lonlat=True)
COSPSI = np.cos(np.radians(PL)) * np.cos(np.radians(PB))
PSI = np.degrees(np.arccos(np.clip(COSPSI, -1, 1)))

# ---- M0 map controls
P("\n--- M0 map controls")
o_m0 = {}
for name in MAPS:
    C = colmap(name, PL, PB)
    lnC = np.log(C)
    k = np.floor(PSI).astype(int)
    spread = max(np.std(lnC[k == j]) for j in range(180) if np.sum(k == j) > 3)
    pole = C[np.abs(PB) > 60].mean(); plane = C[np.abs(PB) < 10].mean()
    gcd = C[(np.abs(PB) < 10) & ((PL < 30) | (PL > 330))].mean(); acd = C[(np.abs(PB) < 10) & (PL > 150) & (PL < 210)].mean()
    hb = np.abs(PB) >= 20
    tw = C[hb & (PSI < 70)].mean(); aw = C[hb & (PSI > 110)].mean()
    o_m0[name] = dict(max_spread_lnC_in_1deg_psi=float(spread), plane_over_pole=plane / pole, GC_over_AC=gcd / acd,
                      col_GCdir=gcd, col_anticentre=acd, col_pole=pole, col_plane=plane,
                      highb_towards_over_away=tw / aw, lnC_range_highb=[float(lnC[hb].min()), float(lnC[hb].max())])
    P(f"  {name:<16} plane/pole x{plane/pole:.2f}  GC/anticentre x{gcd/acd:.2f}  |b|>=20: psi<70 / psi>110 x{tw/aw:.2f}"
      f"  C range {C[hb].min():.0f}-{C[hb].max():.0f} Msun/pc^2  max ln C spread in 1-deg psi bins {spread:.4f}")
check(o_m0["ROUND_canonical"]["max_spread_lnC_in_1deg_psi"] < 0.01 and o_m0["ROUND_alt"]["max_spread_lnC_in_1deg_psi"] < 0.01,
      "M0a ROUND map is a function of psi only (ln C spread in 1-deg psi bins < 1%)")
ref = {"DISC_canonical": (3.053, 3.246), "DISC_alt": (3.187, 3.369)}
dev = max(max(abs(o_m0[k]["GC_over_AC"] / v[0] - 1), abs(o_m0[k]["plane_over_pole"] / v[1] - 1)) for k, v in ref.items())
check(dev < 0.05, f"M0b DISC map reproduces CFG514 O9 GC/AC and plane/pole ratios: max dev {dev:.2%} (< 5%)")

# ---- M0 post-freeze diagnostics (added after the first run; disclosed in the README)
P("  post-freeze diagnostics (not frozen; added after M0a/M0b failed on the first run):")
# (i) M0a: the within-1-deg-bin spread expected from the psi gradient alone vs the deviation from a pure function of psi
for foot in ("canonical", "alt"):
    C = colmap(f"ROUND_{foot}", PL, PB); lnC = np.log(C)
    o = np.argsort(PSI); fit = np.interp(PSI, PSI[o], np.convolve(lnC[o], np.ones(1), "same"))
    # pure-psi reference: the same map evaluated along b = 0 at l = psi (a round column depends on psi only)
    ref1d = np.log(colmap(f"ROUND_{foot}", PSI, np.zeros_like(PSI)))
    dmax = float(np.max(np.abs(lnC - ref1d))); dmax20 = float(np.max(np.abs(lnC - ref1d)[np.abs(PB) >= 15]))
    k = np.floor(PSI).astype(int)
    grad_spread = max(np.std(ref1d[k == j]) for j in range(180) if np.sum(k == j) > 3)
    if foot == "canonical":
        check(dmax < 0.01 and abs(MCHK["canonical"]) < 0.01 and abs(MCHK["alt"]) < 0.01,
              f"M0a' (post-freeze, correctly specified) ROUND map deviates from a pure function of psi by {dmax:.4f} in ln C (< 0.01);"
              f" angle-averaged M(<120) vs grid {MCHK['canonical']:+.3%} / {MCHK['alt']:+.3%} (< 1%)")
    o_m0[f"ROUND_{foot}"].update(dev_from_pure_psi_max=dmax, dev_from_pure_psi_max_absb15=dmax20, spread_expected_from_psi_gradient=float(grad_spread))
    P(f"    ROUND_{foot}: |ln C(l,b) - ln C(psi, b=0)| max {dmax:.4f} (all sky), {dmax20:.4f} (|b| >= 15);"
      f" a pure function of psi has a 1-deg-bin spread of {grad_spread:.4f} from its gradient alone")
# (ii) M0b: the DISC map evaluated on CFG514's exact O9 cells (72 x 36 equal-area grid)
lg14 = np.linspace(0, 360, 72, endpoint=False) + 2.5
bg14 = np.degrees(np.arcsin(np.linspace(-1, 1, 37)[:-1] + 1 / 36))
for name in ("DISC_canonical", "DISC_alt"):
    LL, BB = np.meshgrid(lg14, bg14)
    C = colmap(name, LL, BB)
    pole = C[np.abs(bg14) > 60].mean(); plane = C[np.abs(bg14) < 10].mean()
    gcd = C[np.abs(bg14) < 10][:, (lg14 < 30) | (lg14 > 330)].mean(); acd = C[np.abs(bg14) < 10][:, (lg14 > 150) & (lg14 < 210)].mean()
    o_m0[name].update(cfg514_cells_GC_over_AC=gcd / acd, cfg514_cells_plane_over_pole=plane / pole, cfg514_cells_col_pole=pole)
    P(f"    {name} on CFG514's O9 cells: GC/AC x{gcd/acd:.3f}, plane/pole x{plane/pole:.3f}, pole column {pole:.1f}"
      f" (CFG514: {ref[name][0]:.3f}, {ref[name][1]:.3f})")

# ================================================================== 2. dust, ecliptic latitude, masks
P("\n--- SFD dust per NSIDE-32 pixel (mean of 64 NSIDE-256 sub-pixel centres)")
sl, sb = hp.pix2ang(NSUB, np.arange(hp.nside2npix(NSUB)), nest=True, lonlat=True)
ebv_sub = np.zeros_like(sl)
for fn, sel in (("SFD_dust_4096_ngp.fits", sb >= 0), ("SFD_dust_4096_sgp.fits", sb < 0)):
    h = fits.open(os.path.join(DATA, "dustmaps", "sfd", fn))
    w = WCS(h[0].header)
    x, y = w.all_world2pix(sl[sel], sb[sel], 0)
    xi = np.clip(np.round(x).astype(int), 0, 4095); yi = np.clip(np.round(y).astype(int), 0, 4095)
    ebv_sub[sel] = h[0].data[yi, xi]
EBV = ebv_sub.reshape(NPIX, -1).mean(1)
ecl = SkyCoord(l=PL * u.deg, b=PB * u.deg, frame="galactic").barycentrictrueecliptic
SECL = np.sin(np.radians(ecl.lat.deg))
P(f"  E(B-V) median at |b|>=20: {np.median(EBV[np.abs(PB) >= 20]):.3f}; NGP-region mean {EBV[PB > 80].mean():.3f}")


def angsep(l1, b1, l2, b2):
    l1, b1, l2, b2 = map(np.radians, (l1, b1, l2, b2))
    return np.degrees(np.arccos(np.clip(np.sin(b1) * np.sin(b2) + np.cos(b1) * np.cos(b2) * np.cos(l1 - l2), -1, 1)))


HOLES = (angsep(PL, PB, 280.47, -32.89) < 6.0) | (angsep(PL, PB, 302.80, -44.30) < 3.0)
MASKS = {"M-P": (20.0, 0.15), "M-1": (30.0, 0.10), "M-2": (15.0, 0.30)}
DE_FOOT = (PL > 180.5) & (PL < 359.5)


def mask(mname, foot=None):
    bmin, emax = MASKS[mname]
    m = (np.abs(PB) >= bmin) & (EBV < emax) & ~HOLES
    if foot == "eRASS1":
        m &= DE_FOOT
    return m


# ================================================================== 3. catalogues
P("\n--- catalogues (on disk)")


def read_psz2():
    rows = []
    hdr = None
    for line in open(os.path.join(DATA, "psz2_union.tsv"), encoding="latin-1"):
        if line.startswith("#") or not line.strip():
            continue
        f = line.rstrip("\n").split("\t")
        if hdr is None:
            hdr = [c.strip() for c in f]; continue
        if f[0].strip().startswith("-") or f[0].strip() == "":
            continue
        rows.append(dict(zip(hdr, [c.strip() for c in f])))
    gl = np.array([float(r["GLON"]) for r in rows]); gb = np.array([float(r["GLAT"]) for r in rows])
    z = np.array([float(r["z"]) for r in rows]); cos = np.array([int(r["COSMO"] or 0) for r in rows])
    return gl, gb, z, cos


def read_erass1():
    d = fits.open(os.path.join(DATA, "erass1cl_primary_v3.2.fits"))[1].data
    c = SkyCoord(ra=np.asarray(d["RA"], float) * u.deg, dec=np.asarray(d["DEC"], float) * u.deg).galactic
    return c.l.deg, c.b.deg, np.asarray(d["EXT_LIKE"], float), np.asarray(d["PCONT"], float)


def read_mcxc():
    ra, de = [], []
    hdr = None
    for line in open(MCXC_PATH, encoding="latin-1"):
        if line.startswith("#") or not line.strip():
            continue
        f = line.rstrip("\n").split("\t")
        if hdr is None:
            hdr = [c.strip() for c in f]; continue
        if (not f[0].strip()) or f[0].strip().startswith("-") or len(f) <= hdr.index("DEJ2000") or not f[hdr.index("RAJ2000")].strip():
            continue
        ra.append(f[hdr.index("RAJ2000")].strip()); de.append(f[hdr.index("DEJ2000")].strip())
    c = SkyCoord(ra, de, unit=(u.hourangle, u.deg)).galactic
    return c.l.deg, c.b.deg


gl, gb, pz, pcos = read_psz2()
el, eb, ext, pcont = read_erass1()
ml, mb = read_mcxc()
CATS = {
    "PSZ2": (gl, gb, None), "PSZ2_z": (gl[pz > 0], gb[pz > 0], None), "PSZ2_COSMO": (gl[pcos == 1], gb[pcos == 1], None),
    "eRASS1": (el[(ext >= 6) & (pcont < 0.5)], eb[(ext >= 6) & (pcont < 0.5)], "eRASS1"),
    "eRASS1_all": (el, eb, "eRASS1"), "eRASS1_EXT12": (el[(ext >= 12) & (pcont < 0.5)], eb[(ext >= 12) & (pcont < 0.5)], "eRASS1"),
    "MCXC": (ml, mb, None),
}
for k, (a, b, f) in CATS.items():
    P(f"  {k:<14} N = {len(a)}")
check(len(gl) == 1653 and len(el) == 12247, f"catalogue sizes PSZ2 {len(gl)} (1653), eRASS1 {len(el)} (12247)")


def counts(l, b):
    return np.bincount(hp.ang2pix(NSIDE, l, b, nest=True, lonlat=True), minlength=NPIX).astype(float)


# ================================================================== 4. the statistic
BAND_EDGES = np.array([15, 20, 30, 40, 50, 60, 90.001])


def nuisance(m):
    ab = np.abs(PB[m]); band = np.searchsorted(BAND_EDGES, ab, side="right") - 1
    key = band * 2 + (PB[m] >= 0)
    cols, names = [], []
    for kk in np.unique(key):
        cols.append((key == kk).astype(float)); names.append(f"band{BAND_EDGES[kk//2]:.0f}_{'N' if kk % 2 else 'S'}")
    E = EBV[m]; s = SECL[m]
    cont = [E, E ** 2, s, s ** 2, s ** 3]
    cont = [(c - c.mean()) / (c.std() + 1e-12) for c in cont]
    return np.column_stack(cols + cont), names + ["E", "E2", "s", "s2", "s3"], key


def poisson_fit(X, N, w0=None, maxit=100):
    w = np.zeros(X.shape[1]) if w0 is None else w0.copy()
    if w0 is None:
        w[:] = 0.0
        # dummy intercepts: start at log of the band mean
        for j in range(X.shape[1]):
            col = X[:, j]
            if set(np.unique(col)) <= {0.0, 1.0} and col.sum() > 0:
                w[j] = math.log(max(N[col == 1].mean(), 1e-3))
    for it in range(maxit):
        eta = np.clip(X @ w, -30, 30); mu = np.exp(eta)
        g = X.T @ (N - mu); H = X.T @ (X * mu[:, None])
        step = np.linalg.solve(H + 1e-10 * np.eye(len(w)), g)
        ss = 1.0
        if np.max(np.abs(step)) > 2: ss = 2 / np.max(np.abs(step))
        w += ss * step
        if np.max(np.abs(step)) < 1e-9:
            break
    mu = np.exp(np.clip(X @ w, -30, 30))
    cov = np.linalg.inv(X.T @ (X * mu[:, None]))
    phi = np.sum((N - mu) ** 2 / mu) / max(len(N) - X.shape[1], 1)
    return w, cov, phi, mu


def prep(cat, mname):
    l, b, foot = CATS[cat]
    m = mask(mname, foot)
    N = counts(l, b)[m]
    Xn, names, key = nuisance(m)
    # drop band x hemisphere cells with zero clusters (no information on beta; intercept would diverge)
    keep = np.ones(m.sum(), bool)
    for kk in np.unique(key):
        if N[key == kk].sum() == 0:
            keep[key == kk] = False
    idx = np.where(m)[0][keep]
    Xn = Xn[keep]; N = N[keep]
    nz = [j for j in range(Xn.shape[1]) if np.any(Xn[:, j] != 0) and not (np.all(Xn[:, j] == 0))]
    Xn = Xn[:, nz]; names = [names[j] for j in nz]
    return idx, N, Xn, names


def xcol(mapname, idx, dl):
    lnC = np.log(colmap(mapname, PL[idx], PB[idx], dl))
    return lnC - np.median(lnC)


def fit_beta(N, Xn, x):
    X = np.column_stack([x, Xn])
    w, cov, phi, mu = poisson_fit(X, N)
    return w[0], math.sqrt(cov[0, 0]), phi, w, mu


def S_from_beta(beta, x):
    t1, t2 = np.quantile(x, [1 / 3, 2 / 3])
    dx = x[x >= t2].mean() - x[x <= t1].mean()
    return 1 - math.exp(beta * dx), dx


def run_cell(cat, mname, mapname, dl_base, with_null=True):
    idx, N, Xn, names = prep(cat, mname)
    x = xcol(mapname, idx, dl_base)
    beta, sp, phi, w, mu = fit_beta(N, Xn, x)
    corr = {nm: float(np.corrcoef(x, Xn[:, j])[0, 1]) for j, nm in enumerate(names) if np.std(Xn[:, j]) > 0}
    rot = []
    if with_null:
        for d in ROTS:
            xr = xcol(mapname, idx, dl_base + d)
            rot.append(fit_beta(N, Xn, xr)[0])
    rot = np.array(rot)
    s_rot = float(np.std(rot)) if len(rot) else float("nan")
    sig = max(sp * math.sqrt(max(phi, 1.0)), s_rot if np.isfinite(s_rot) else 0.0)
    S, dx = S_from_beta(beta, x)
    Slo = 1 - math.exp((beta + 1.96 * sig) * dx); Shi = 1 - math.exp((beta - 1.96 * sig) * dx)
    sPo = sp * math.sqrt(max(phi, 1.0))
    zP = beta / sPo
    if len(rot):
        med = float(np.median(rot)); smad = float(1.4826 * np.median(np.abs(rot - med)))
    else:
        med, smad = float("nan"), float("nan")
    SP95 = [1 - math.exp((beta + 1.96 * sPo) * S_from_beta(beta, x)[1]), 1 - math.exp((beta - 1.96 * sPo) * S_from_beta(beta, x)[1])]
    return dict(cat=cat, mask=mname, map=mapname, rot_deg=dl_base, Npix=int(len(N)), Nclus=int(N.sum()), z_poisson_only_postfreeze=float(zP), S95_poisson_only_postfreeze=SP95,
                rot_median_postfreeze=med, rot_sigma_MAD_postfreeze=smad, z_robust_null_postfreeze=float((beta - med) / smad) if smad > 0 else float("nan"),
                rot_rank_frac_below=float(np.mean(rot < beta)) if len(rot) else float("nan"),
                beta=float(beta), sig_poisson=float(sp), phi=float(phi), sig_rot=s_rot, sigma=float(sig), z=float(beta / sig),
                S=float(S), S95=[float(Slo), float(Shi)], dx_top_bot=float(dx), rot_betas=rot.tolist(),
                max_abs_corr_nuis=float(max(abs(v) for v in corr.values())), corr=corr), (idx, N, Xn, x, w)


# ---- direct contrast: psi < 70 vs psi > 110, band-matched (Mantel-Haenszel)
def contrast(cat, mname, dl=0.0):
    l, b, foot = CATS[cat]
    m = mask(mname, foot)
    N = counts(l, b)
    cpsi = np.cos(np.radians(PL - dl)) * np.cos(np.radians(PB))
    tw = m & (cpsi > math.cos(math.radians(70))); aw = m & (cpsi < math.cos(math.radians(110)))
    band = np.searchsorted(BAND_EDGES, np.abs(PB), side="right") - 1
    key = band * 2 + (PB >= 0)
    num = den = 0.0; var_ln = 0.0
    Nt_tot = Na_tot = 0.0
    for kk in np.unique(key[m]):
        st, sa = tw & (key == kk), aw & (key == kk)
        nt, na = st.sum(), sa.sum()
        if nt == 0 or na == 0:
            continue
        Nt, Na = N[st].sum(), N[sa].sum(); nb = nt + na
        num += Nt * na / nb; den += Na * nt / nb
        Nt_tot += Nt; Na_tot += Na
    R = num / den if den > 0 else float("nan")
    sig_ln = math.sqrt(1 / max(Nt_tot, 1) + 1 / max(Na_tot, 1))
    return R, sig_ln, Nt_tot, Na_tot


# ================================================================== 5. run the cells
RES = dict(mutate=MUTATE, rot_mut_deg=ROT_MUT, M0=o_m0, cells={}, contrast={}, injection={}, I2={})
P("\n" + "=" * 110 + "\nCELLS: beta = d ln(density) / d ln(cold column) at fixed |b| band x hemisphere, dust, ecliptic latitude\n" + "=" * 110)
P(f"  {'catalogue':<13} {'mask':<4} {'map':<16} {'Npix':>5} {'Ncl':>5} {'beta':>8} {'sP':>6} {'phi':>5} {'s_rot':>6} {'sigma':>6} {'z':>6}   S(top vs bottom tercile) [95%]       max|corr nuis|  [post-freeze info: z Poisson-only; fraction of the 29 rotations with beta below]")
cell_list = []
for cat in CATS:
    for mname in MASKS:
        maps = list(MAPS) if (mname == "M-P" and cat in ("PSZ2", "eRASS1", "MCXC")) else ["ROUND_canonical", "ROUND_alt"]
        for mp in maps:
            cell_list.append((cat, mname, mp))
CACHE = {}
for cat, mname, mp in cell_list:
    r, aux = run_cell(cat, mname, mp, ROT_MUT)
    key = f"{cat}|{mname}|{mp}"
    RES["cells"][key] = r; CACHE[key] = aux
    P(f"  {cat:<13} {mname:<4} {mp:<16} {r['Npix']:5d} {r['Nclus']:5d} {r['beta']:+8.4f} {r['sig_poisson']:6.4f} {r['phi']:5.2f} {r['sig_rot']:6.4f} {r['sigma']:6.4f} {r['z']:+6.2f}"
          f"   {r['S']:+.3f} [{r['S95'][0]:+.3f}, {r['S95'][1]:+.3f}]   {r['max_abs_corr_nuis']:.2f}   zP {r['z_poisson_only_postfreeze']:+.2f}  rank {r['rot_rank_frac_below']:.2f}")

P("\n--- post-freeze info: beta as a function of the map rotation dl (round canonical, mask M-P); dl = 0 is the real orientation")
for cat in ("PSZ2", "eRASS1", "MCXC"):
    r = RES["cells"][f"{cat}|M-P|ROUND_canonical"]
    P(f"  {cat:<7} dl=0: {r['beta']:+.3f} | " + " ".join(f"{int(d)}:{b:+.2f}" for d, b in zip(ROTS, r["rot_betas"])))
    P(f"          robust null (median, 1.4826 MAD of the 29 rotations): {r['rot_median_postfreeze']:+.3f}, {r['rot_sigma_MAD_postfreeze']:.3f}"
      f" -> z_robust = {r['z_robust_null_postfreeze']:+.2f}; Poisson-only z = {r['z_poisson_only_postfreeze']:+.2f},"
      f" S 95% (Poisson-only) [{r['S95_poisson_only_postfreeze'][0]:+.3f}, {r['S95_poisson_only_postfreeze'][1]:+.3f}]")

P("\n--- direct contrast: density ratio psi < 70 deg (towards GC) / psi > 110 deg (away), band-matched, mask M-P")
for cat in CATS:
    R, sl_, Nt, Na = contrast(cat, "M-P", ROT_MUT)
    rot = np.array([contrast(cat, "M-P", ROT_MUT + d)[0] for d in ROTS])
    lr = np.log(rot[np.isfinite(rot) & (rot > 0)])
    srot = float(np.std(lr)) if len(lr) > 5 else float("nan")
    sig = max(sl_, srot) if np.isfinite(srot) else sl_
    RES["contrast"][cat] = dict(n_rot_finite=int(len(lr)), ratio=R, sig_ln_poisson=sl_, sig_ln_rot=srot, sig_ln=sig, z=math.log(R) / sig, N_towards=Nt, N_away=Na)
    P(f"  {cat:<13} towards/away = {R:.3f}  (N {Nt:.0f} / {Na:.0f}); sigma(ln) Poisson {sl_:.3f}, rotation {srot:.3f}; z = {math.log(R)/sig:+.2f}")

# ================================================================== 6. injection I1 (real catalogue thinned) and I2 (synthetic)
P("\n" + "=" * 110 + "\nINJECTIONS (round canonical map, mask M-P)\n" + "=" * 110)
for cat in ("PSZ2", "eRASS1", "MCXC"):
    key = f"{cat}|M-P|ROUND_canonical"
    r0 = RES["cells"][key]
    l, b, foot = CATS[cat]
    idx, N, Xn, x, w = CACHE[key]
    # suppression defined by the TRUE (unrotated) map's top tercile, always
    x_true = xcol("ROUND_canonical", idx, 0.0)
    top_pix = set(idx[x_true >= np.quantile(x_true, 2 / 3)].tolist())
    cpix = hp.ang2pix(NSIDE, l, b, nest=True, lonlat=True)
    in_top = np.array([p in top_pix for p in cpix])
    dbs, dSs = [], []
    for seed in range(50):
        rg = np.random.default_rng(1000 + seed)
        keep = ~(in_top & (rg.random(len(l)) < 0.20))
        Ni = counts(l[keep], b[keep])[idx]
        bi = fit_beta(Ni, Xn, x)[0]
        dbs.append(bi - r0["beta"]); dSs.append(S_from_beta(bi, x)[0] - r0["S"])
    dbs = np.array(dbs); dSs = np.array(dSs)
    power = float(np.mean(np.abs(dbs)) / r0["sigma"])
    sgn = float(np.sign(np.mean(dbs)))
    b3 = 3 * r0["sigma"]; Smin3 = 1 - math.exp(-b3 * r0["dx_top_bot"])
    RES["injection"][cat] = dict(S_min_detectable_3sigma_loglinear=Smin3, mean_dbeta=float(dbs.mean()), std_dbeta=float(dbs.std()), power_z=power, mean_dS=float(dSs.mean()),
                                 sigma_S_approx=float(r0["sigma"] * r0["dx_top_bot"]),
                                 sign_dbeta=sgn)
    P(f"  I1 {cat:<8} 20% thinning of top-tercile pixels (50 seeds): mean d beta {dbs.mean():+.4f} +- {dbs.std():.4f};"
      f" power |d beta|/sigma = {power:.2f}; 3-sigma detectable S (log-linear) {Smin3:.2f}; mean dS {dSs.mean():+.3f} (target +0.20; sigma_S ~ {r0['sigma']*r0['dx_top_bot']:.3f})")
    # I2 synthetic: null model (beta fixed 0), 200 mocks
    w0, cov0, phi0, mu0 = poisson_fit(Xn, N)
    rg = np.random.default_rng(2000 + len(cat))
    top = x_true >= np.quantile(x_true, 2 / 3)
    fp = 0; Ss = []
    for k in range(200):
        Nm = rg.poisson(mu0).astype(float)
        bm, sm = fit_beta(Nm, Xn, x)[:2]
        if abs(bm / sm) >= 3: fp += 1
        Ni = rg.poisson(mu0 * np.where(top, 0.8, 1.0)).astype(float)
        Ss.append(S_from_beta(fit_beta(Ni, Xn, x)[0], x)[0])
    RES["I2"][cat] = dict(false_pos_rate=fp / 200, mean_S_injected=float(np.mean(Ss)), std_S_injected=float(np.std(Ss)))
    P(f"  I2 {cat:<8} null mocks: |z_P| >= 3 in {fp}/200 ({fp/200:.1%}); 20% injected: mean S = {np.mean(Ss):.3f} +- {np.std(Ss):.3f}")
    if not MUTATE:
        check(power >= 3 if cat == "PSZ2" else True, f"I1 {cat} power for 20% suppression = {power:.2f}" + (" (>= 3 needed for the verdict)" if cat == "PSZ2" else " (info)"))
        check(abs(dSs.mean() - 0.20) <= 2 * r0["sigma"] * r0["dx_top_bot"], f"I1 {cat} mean recovered dS {dSs.mean():+.3f} within 2 sigma_S of 0.20")
        check(fp / 200 <= 0.02, f"I2a {cat} false-positive rate {fp/200:.1%} (<= 2%)")
        check(abs(np.mean(Ss) - 0.20) <= 0.03, f"I2b {cat} mean recovered S {np.mean(Ss):.3f} within 0.03 of 0.20")
    else:
        # MUTATE A on the injection: analysed with the rotated map, the injected response must have the opposite sign
        check(sgn > 0, f"MUTATE-A {cat}: injected suppression (true-map top tercile) seen through the 180-deg map gives d beta {dbs.mean():+.4f}"
                       f" (must be > 0, opposite to the primary's negative response)")

# ================================================================== 7. verdict
prim = RES["cells"]["PSZ2|M-P|ROUND_canonical"]
v = {}
if not MUTATE:
    robust_keys = ["PSZ2|M-1|ROUND_canonical", "PSZ2|M-2|ROUND_canonical", "PSZ2|M-P|ROUND_alt", "eRASS1|M-P|ROUND_canonical"]
    sgn = np.sign(prim["z"])
    rob = all(np.sign(RES["cells"][k]["z"]) == sgn and abs(RES["cells"][k]["z"]) >= 2 for k in robust_keys)
    power_ok = RES["injection"]["PSZ2"]["power_z"] >= 3
    ctrl_ok = all(c for c, _ in CHECKS)
    collin_ok = prim["max_abs_corr_nuis"] <= 0.8
    eras = RES["cells"]["eRASS1|M-P|ROUND_canonical"]
    if abs(prim["z"]) >= 3 and rob and ctrl_ok and collin_ok:
        verdict = "DEPENDENCE FOUND (pending MUTATE-A flip: see _MUTATE run)" + (" -- SUPPRESSION" if sgn < 0 else " -- ENHANCEMENT (not obscuration)")
    elif abs(prim["z"]) < 3 and power_ok and ctrl_ok and collin_ok:
        verdict = "NO OBSCURATION"
    else:
        verdict = "NOT DIAGNOSTIC"
    v = dict(verdict=verdict, primary_z=prim["z"], primary_beta=prim["beta"], primary_sigma=prim["sigma"], primary_S=prim["S"],
             primary_S95=prim["S95"], robust_same_sign_2sigma=bool(rob), psz2_power=RES["injection"]["PSZ2"]["power_z"],
             controls_all_pass=bool(ctrl_ok), collinearity_ok=bool(collin_ok),
             eRASS1_z=eras["z"], eRASS1_flag=("eRASS1 |z| >= 3 alone: X-ray-foreground-confounded, catalogue-specific" if abs(eras["z"]) >= 3 and abs(prim["z"]) < 3 else ""))
    P("\n" + "=" * 110)
    P(f"VERDICT: {verdict}")
    P(f"  primary PSZ2 / M-P / ROUND canonical: beta = {prim['beta']:+.4f} +- {prim['sigma']:.4f} (z {prim['z']:+.2f});"
      f" S = {prim['S']:+.3f}, 95% [{prim['S95'][0]:+.3f}, {prim['S95'][1]:+.3f}]; PSZ2 power for 20% = {v['psz2_power']:.2f}")
    P(f"  eRASS1 primary: z = {eras['z']:+.2f}, S = {eras['S']:+.3f} [{eras['S95'][0]:+.3f}, {eras['S95'][1]:+.3f}]  {v['eRASS1_flag']}")
else:
    v = dict(primary_z_MUTATE=prim["z"], primary_beta_MUTATE=prim["beta"])
    P(f"\nMUTATE (180-deg map): PSZ2 primary beta = {prim['beta']:+.4f} +- {prim['sigma']:.4f} (z {prim['z']:+.2f});"
      f" eRASS1 z = {RES['cells']['eRASS1|M-P|ROUND_canonical']['z']:+.2f}")
RES["verdict"] = v
RES["checks"] = [dict(ok=c, msg=m) for c, m in CHECKS]
RES["runtime_s"] = time.time() - T0
P(f"\nchecks: {sum(c for c,_ in CHECKS)}/{len(CHECKS)} pass; runtime {time.time()-T0:.0f} s")

# ================================================================== 8. figure
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
fig = plt.figure(figsize=(15, 10))
lnRound = np.log10(colmap("ROUND_canonical", PL, PB, ROT_MUT)); lnDisc = np.log10(colmap("DISC_canonical", PL, PB, ROT_MUT))
ring = lambda a: hp.reorder(a, n2r=True)
hp.mollview(ring(lnRound), sub=(2, 2, 1), fig=fig.number, title="ROUND cold column to 100 kpc, log10 Msun/pc^2 (canonical)" + (" [rotated 180]" if MUTATE else ""),
            cmap="viridis", unit="")
mP = mask("M-P").astype(float)
hp.projscatter(gl, gb, lonlat=True, s=3, c="w", edgecolors="k", linewidths=0.2, label="PSZ2")
hp.graticule(dpar=30, dmer=60, alpha=0.3)
hp.mollview(ring(lnDisc), sub=(2, 2, 2), fig=fig.number, title="DISC (phantom disc) column to 100 kpc, log10 Msun/pc^2", cmap="viridis", unit="")
hp.projscatter(*CATS["eRASS1"][:2], lonlat=True, s=0.5, c="r", alpha=0.5)
hp.graticule(dpar=30, dmer=60, alpha=0.3)
mm = np.where(mP > 0, lnRound, hp.UNSEEN)
hp.mollview(ring(mm), sub=(2, 2, 3), fig=fig.number, title="mask M-P over ROUND column; PSZ2 white, eRASS1 red", cmap="viridis", unit="")
hp.projscatter(*CATS["eRASS1"][:2], lonlat=True, s=0.3, c="r", alpha=0.4)
hp.projscatter(gl, gb, lonlat=True, s=3, c="w", edgecolors="k", linewidths=0.2)
ax = fig.add_subplot(2, 2, 4)
for cat, col in (("PSZ2", "C0"), ("eRASS1", "C3")):
    r = RES["cells"][f"{cat}|M-P|ROUND_canonical"]
    ax.hist(r["rot_betas"], bins=12, alpha=0.4, color=col, label=f"{cat} rotation null")
    ax.axvline(r["beta"], color=col, lw=2, label=f"{cat} beta {r['beta']:+.3f} (z {r['z']:+.2f})")
    ax.axvline(r["beta"] + RES["injection"][cat]["mean_dbeta"], color=col, ls="--", label=f"{cat} + 20% injected")
ax.set_xlabel("beta = d ln(cluster density) / d ln(cold column)"); ax.legend(fontsize=8); ax.set_title("statistic vs rotation null and injection")
plt.tight_layout()
plt.savefig(os.path.join(HERE, f"cfg517_skymap{TAG}.png"), dpi=110)


def _clean(o):
    if isinstance(o, dict): return {k: _clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [_clean(v) for v in o]
    if isinstance(o, (np.floating,)): return float(o)
    if isinstance(o, (np.integer,)): return int(o)
    if isinstance(o, np.bool_): return bool(o)
    return o


json.dump(_clean(RES), open(os.path.join(HERE, f"cfg517_results{TAG}.json"), "w"), indent=1)
open(os.path.join(HERE, f"cfg517_clusters_cold_column{TAG}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if all(c for c, _ in CHECKS) else 1)
