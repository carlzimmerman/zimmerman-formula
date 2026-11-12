#!/usr/bin/env python3
"""
HOT1 -- where are the hot 30-40 kpc BHB stars? Criteria: FROZEN_CRITERIA.md (sha256 in FREEZE_STAMP.txt).
Usage: python3 -I -B hot1.py <path to MWS_BHB.fits>
Writes hot1.out (main), hot1_results.json, hot1_mut.out (mutation, separate).
Known-answer checks run first; the script stops before any label if one fails.
Sample functions copied from RAW1's raw1.py (load, build, Sgr frame, frame_affine, fit_disp); not imported.
kappa = 1/2 FITTED; not theory closed. Adopts nothing.
"""
import os, sys, json, math
import numpy as np
from scipy.optimize import minimize_scalar, brentq
from scipy import stats as SST
from astropy.io import fits
import astropy.units as u
from astropy.coordinates import SkyCoord, Galactocentric, CartesianRepresentation, CartesianDifferential
from astropy.coordinates.matrix_utilities import rotation_matrix

FITS = sys.argv[1]
HERE = os.path.dirname(os.path.abspath(__file__))
K474 = 4.740470463
NPERM = 5000
OUT = open(os.path.join(HERE, "hot1.out"), "w")
def say(s=""):
    print(s); OUT.write(str(s) + "\n"); OUT.flush()
def sec(t):
    say("\n" + "=" * 100); say(t); say("=" * 100)
FAIL = []
def check(name, ok, detail):
    say(f"  [{'PASS' if ok else 'FAIL'}] {name}: {detail}")
    if not ok: FAIL.append(name)
def stop_if_failed():
    if FAIL:
        say("\nKNOWN-ANSWER CHECK FAILED: " + ", ".join(FAIL) + ". Stopping before any label."); OUT.close(); sys.exit(2)

# ------------------------------------------------------------------ copied from raw1.py
BINS = [(20.0, 30.0), (30.0, 40.0), (40.0, 55.0), (55.0, 80.0)]
NOMINAL = dict(clip=400.0, R0=8.122, zsun=20.8, vsun=(12.9, 245.6, 7.78), sgr=15.0, dscale=1.0)

def prof_interval(nll, lo, hi):
    res = minimize_scalar(nll, bounds=(lo, hi), method="bounded", options=dict(xatol=1e-6))
    xb, nb = res.x, res.fun
    def side(direction):
        step = max(abs(xb) * 0.02, 1e-3); x = xb
        for _ in range(200):
            xn = x + direction * step
            if (direction < 0 and xn < lo) or (direction > 0 and xn > hi): return (lo if direction < 0 else hi)
            if nll(xn) - nb > 0.5:
                return brentq(lambda t: nll(t) - nb - 0.5, min(x, xn), max(x, xn), xtol=1e-6)
            x = xn; step *= 1.3
        return lo if direction < 0 else hi
    return xb, side(-1), side(+1), nb

def fit_disp(v, e):
    def nll_s(s):
        var = s * s + e * e
        mu = np.sum(v / var) / np.sum(1 / var)
        return 0.5 * np.sum((v - mu) ** 2 / var + np.log(var))
    sb, slo, shi, _ = prof_interval(nll_s, 1.0, 400.0)
    var = sb * sb + e * e; mu = np.sum(v / var) / np.sum(1 / var)
    return dict(sigma=float(sb), lo=float(slo), hi=float(shi), h=float(0.5 * (shi - slo)), mu=float(mu), n=int(len(v)))

def sgr_matrix():
    D = rotation_matrix((180 + 3.75) * u.deg, "z"); C = rotation_matrix((90 - 13.46) * u.deg, "x")
    B = rotation_matrix((180 + 14.111534) * u.deg, "z"); A = np.diag([1., 1., -1.])
    return A @ B @ C @ D
def sgr_lat_lon(l_deg, b_deg):
    l, b = np.radians(l_deg), np.radians(b_deg)
    x = np.array([np.cos(b) * np.cos(l), np.cos(b) * np.sin(l), np.sin(b)])
    xs = sgr_matrix() @ x
    return np.degrees(np.arctan2(xs[1], xs[0])) % 360.0, np.degrees(np.arcsin(np.clip(xs[2], -1, 1)))

def frame_affine(R0, zsun):
    gc = Galactocentric(galcen_distance=R0 * u.kpc, z_sun=zsun * u.pc, galcen_v_sun=CartesianDifferential([0, 0, 0] * u.km / u.s))
    def tr(xyz):
        c = SkyCoord(CartesianRepresentation(np.asarray(xyz, float).T * u.kpc), frame="icrs").transform_to(gc)
        return np.vstack([c.x.to_value(u.kpc), c.y.to_value(u.kpc), c.z.to_value(u.kpc)]).T
    p0 = tr(np.zeros((1, 3)))[0]
    Rm = (tr(np.eye(3)) - p0).T
    return p0, Rm

def load():
    h = fits.open(FITS, memmap=False)
    rv, fm, ga = h["RVTAB"].data, h["FIBERMAP"].data, h["GAIA"].data
    return dict(tid=np.asarray(rv["TARGETID"]), tid_fm=np.asarray(fm["TARGETID"]), primary=np.asarray(rv["PRIMARY"]).astype(bool),
                vrad=np.asarray(rv["VRAD"], float), verr=np.asarray(rv["VRAD_ERR"], float),
                ra=np.asarray(rv["TARGET_RA"], float), dec=np.asarray(rv["TARGET_DEC"], float),
                dist=np.asarray(fm["DIST"], float), g=np.asarray(fm["MAG_DERED_G"], float), Mg=np.asarray(fm["ABS_MAG_G"], float),
                ref_id=np.asarray(fm["REF_ID"]), sid=np.asarray(ga["SOURCE_ID"]),
                pmra=np.asarray(ga["PMRA"], float), pmdec=np.asarray(ga["PMDEC"], float),
                epmra=np.asarray(ga["PMRA_ERROR"], float), epmdec=np.asarray(ga["PMDEC_ERROR"], float),
                ruwe=np.asarray(ga["RUWE"], float))

def build(D, cfg):
    """RAW1 S1-S6 (identical cuts); additionally returns Galactic l, b and B_Sgr of the kept stars."""
    m = D["primary"] & np.isfinite(D["vrad"]) & (D["verr"] > 0) & (D["dist"] > 0) & np.isfinite(D["g"]) & np.isfinite(D["Mg"])
    idx = np.where(m)[0]
    ra, dec = np.radians(D["ra"][idx]), np.radians(D["dec"][idx])
    d = D["dist"][idx] * cfg["dscale"]
    p0, Rm = frame_affine(cfg["R0"], cfg["zsun"])
    n = np.vstack([np.cos(dec) * np.cos(ra), np.cos(dec) * np.sin(ra), np.sin(dec)]).T
    ea = np.vstack([-np.sin(ra), np.cos(ra), np.zeros_like(ra)]).T
    no = np.vstack([-np.sin(dec) * np.cos(ra), -np.sin(dec) * np.sin(ra), np.cos(dec)]).T
    n, ea, no = n @ Rm.T, ea @ Rm.T, no @ Rm.T
    pos = p0 + d[:, None] * n; r = np.linalg.norm(pos, axis=1); rh = pos / r[:, None]
    vs = np.array(cfg["vsun"])
    vgsr = D["vrad"][idx] + n @ vs
    c = SkyCoord(ra=D["ra"][idx] * u.deg, dec=D["dec"][idx] * u.deg, frame="icrs").galactic
    lam, bet = sgr_lat_lon(c.l.deg, c.b.deg)
    keep = (np.abs(bet) >= cfg["sgr"]) & (r >= 20.0) & (r < 80.0)
    if cfg["clip"] is not None: keep &= np.abs(vgsr) <= cfg["clip"]
    k = np.where(keep)[0]
    okpm = (D["sid"][idx] > 0) & np.isfinite(D["pmra"][idx]) & np.isfinite(D["pmdec"][idx]) & np.isfinite(D["epmra"][idx]) \
           & np.isfinite(D["epmdec"][idx]) & (D["ruwe"][idx] < 1.4) & (D["sid"][idx] == D["ref_id"][idx])
    S = dict(d=d[k], r=r[k], pos=pos[k], n=n[k], ea=ea[k], no=no[k], rh=rh[k], vgsr=vgsr[k], verr=D["verr"][idx][k],
             l=c.l.deg[k], b=c.b.deg[k], Bsgr=bet[k], pmok=okpm[k], pmra=D["pmra"][idx][k], pmdec=D["pmdec"][idx][k], vs=vs)
    return S

# ------------------------------------------------------------------ HEALPix nside=1, RING (Gorski et al. 2005)
def ang2pix_ring(nside, theta, phi):
    theta = np.asarray(theta, float); phi = np.mod(np.asarray(phi, float), 2 * np.pi)
    z = np.cos(theta); za = np.abs(z); tt = phi / (0.5 * np.pi)
    npix = 12 * nside * nside; ncap = 2 * nside * (nside - 1)
    pix = np.empty(z.shape, dtype=np.int64)
    eq = za <= 2.0 / 3.0
    # equatorial
    t1 = nside * (0.5 + tt[eq]); t2 = nside * z[eq] * 0.75
    jp = np.floor(t1 - t2).astype(np.int64); jm = np.floor(t1 + t2).astype(np.int64)
    ir = nside + 1 + jp - jm; kshift = 1 - (ir & 1)
    ip = (jp + jm - nside + kshift + 1) // 2; ip = np.mod(ip, 4 * nside)
    pix[eq] = ncap + (ir - 1) * 4 * nside + ip
    # polar caps
    po = ~eq
    tp = tt[po] - np.floor(tt[po]); tmp = nside * np.sqrt(3 * (1 - za[po]))
    jp = np.floor(tp * tmp).astype(np.int64); jm = np.floor((1 - tp) * tmp).astype(np.int64)
    ir = jp + jm + 1; ip = np.floor(tt[po] * ir).astype(np.int64); ip = np.mod(ip, 4 * ir)
    pix[po] = np.where(z[po] > 0, 2 * ir * (ir - 1) + ip, npix - 2 * ir * (ir + 1) + ip)
    return pix
def cell_of(l_deg, b_deg):
    return ang2pix_ring(1, np.radians(90.0 - np.asarray(b_deg)), np.radians(np.asarray(l_deg)))
def gal_unit(l_deg, b_deg):
    l, b = np.radians(l_deg), np.radians(b_deg)
    return np.vstack([np.cos(b) * np.cos(l), np.cos(b) * np.sin(l), np.sin(b)]).T

# ------------------------------------------------------------------ statistics (vectorised over permutations)
def cell_masks(cells, nmin=15):
    out = []
    for c in range(12):
        m = cells == c
        if m.sum() >= nmin: out.append((c, m))
    return out
def stat_L1(V, masks):
    """V (P, N). returns L1 (P,), argmax cell id (P,), L1b (P,)."""
    P, N = V.shape
    mu = V.mean(1, keepdims=True); D2 = (V - mu) ** 2; MSall = D2.mean(1)
    best = np.zeros(P); arg = np.full(P, -1); bestz = np.full(P, -np.inf)
    for c, m in masks:
        n = m.sum(); a, b = D2[:, m], D2[:, ~m]
        MSc, MSr = a.mean(1), b.mean(1)
        varc, varr = V[:, m].var(1), V[:, ~m].var(1)
        lam = N * np.log(MSall) - n * np.log(varc) - (N - n) * np.log(varr)
        T = np.where(MSc > MSr, lam, 0.0)
        upd = T > best; best = np.where(upd, T, best); arg = np.where(upd, c, arg)
        z = (MSc - MSr) / np.sqrt(a.var(1, ddof=1) / n + b.var(1, ddof=1) / (N - n))
        bestz = np.maximum(bestz, z)
    return best, arg, bestz
def stat_L2(V, A, B):
    mu = V.mean(1, keepdims=True); D2 = (V - mu) ** 2
    a, b = D2[:, A], D2[:, B]
    return (a.mean(1) - b.mean(1)) / np.sqrt(a.var(1, ddof=1) / A.sum() + b.var(1, ddof=1) / B.sum())
def pairs_within(X, deg):
    cosmin = math.cos(math.radians(deg)); G = X @ X.T
    i, j = np.where(np.triu(G > cosmin, k=1)); return i, j
def stat_L3(V, i, j, dv, chunk=500):
    out = np.empty(V.shape[0])
    for s in range(0, V.shape[0], chunk):
        out[s:s + chunk] = np.sum(np.abs(V[s:s + chunk, i] - V[s:s + chunk, j]) < dv, axis=1)
    return out
def pval(null, obs): return float((1 + np.sum(null >= obs - 1e-12)) / (1 + len(null)))
def perms(v, seed, P=NPERM):
    return np.random.default_rng(seed).permuted(np.tile(v, (P, 1)), axis=1)

def run_stats(v, cells, Bsgr, X, seedA, seedB, with_variants=True):
    masks = cell_masks(cells)
    A = (np.abs(Bsgr) >= 15) & (np.abs(Bsgr) < 30); B = np.abs(Bsgr) >= 30
    o1, oarg, o1b = stat_L1(v[None], masks); o2 = stat_L2(v[None], A, B)
    PV = perms(v, seedA); n1, _, n1b = stat_L1(PV, masks); n2 = stat_L2(PV, A, B)
    i, j = pairs_within(X, 10.0); o3 = stat_L3(v[None], i, j, 30.0)
    PV3 = perms(v, seedB); n3 = stat_L3(PV3, i, j, 30.0)
    R = dict(L1=float(o1[0]), L1_cell=int(oarg[0]), p1=pval(n1, o1[0]), L1b=float(o1b[0]), p1b=pval(n1b, o1b[0]),
             L2=float(o2[0]), p2=pval(n2, o2[0]), p2_two=float((1 + np.sum(np.abs(n2) >= abs(o2[0]) - 1e-12)) / (1 + len(n2))),
             nA=int(A.sum()), nB=int(B.sum()), L3=int(o3[0]), L3_null_mean=float(n3.mean()), p3=pval(n3, o3[0]), npairs10=int(len(i)),
             cells_used=[int(c) for c, _ in masks])
    if with_variants:
        i5, j5 = pairs_within(X, 5.0); o35 = stat_L3(v[None], i5, j5, 20.0); n35 = stat_L3(PV3, i5, j5, 20.0)
        R.update(L3v=int(o35[0]), L3v_null_mean=float(n35.mean()), p3v=pval(n35, o35[0]), npairs5=int(len(i5)))
    return R, (i, j)

def label(R, s_new, h_new, sN, sS, nb_mean):
    labs = []
    if R["p1"] < 0.01 and s_new is not None and s_new <= nb_mean + h_new: labs.append("LOCALISED")
    if R["p2"] < 0.01: labs.append("SAGITTARIUS RESIDUE")
    if R["p3"] < 0.01: labs.append("CLUMPED")
    if labs: return " + ".join(labs)
    if max(R["p1"], 0) >= 0.05 and R["p2"] >= 0.05 and R["p3"] >= 0.05 and sN > nb_mean and sS > nb_mean: return "DIFFUSE"
    return "UNDECIDED"

# ================================================================== K-H (no data)
sec("K-H HEALPix nside=1 RING cell assignment (no data)")
rng = np.random.default_rng(101); NMC = 10 ** 6
zz = rng.uniform(-1, 1, NMC); pp = rng.uniform(0, 2 * np.pi, NMC)
cnt = np.bincount(ang2pix_ring(1, np.arccos(zz), pp), minlength=12)
fr = cnt / NMC * 12
check("K-H a equal area", np.all(np.abs(fr - 1) < 0.03), "fraction x 12 per cell: " + " ".join(f"{x:.4f}" for x in fr))
tc = [(math.acos(2 / 3), 0.25 * math.pi, 0), (0.5 * math.pi, 0.0, 4), (math.acos(-2 / 3), 0.25 * math.pi, 8)]
okc = True; got = []
for th, ph, p in tc:
    for k in range(4):
        g = int(ang2pix_ring(1, np.array([th]), np.array([ph + 0.5 * math.pi * k]))[0]); got.append(g); okc &= (g == p + k)
check("K-H b pixel centres", okc, f"got {got}, want [0..3, 4..7, 8..11]")
stop_if_failed()

# ================================================================== data, K-S
sec("Data and K-S sample check")
D = load()
check("K-S0 TARGETID RVTAB == FIBERMAP", bool(np.all(D["tid"] == D["tid_fm"])), f"{len(D['tid'])} rows")
S = build(D, dict(NOMINAL))
bidx = [np.where((S["r"] >= a) & (S["r"] < b))[0] for a, b in BINS]
counts = [len(x) for x in bidx]
check("K-S counts", counts == [865, 264, 241, 125], f"{counts} vs [865, 264, 241, 125]")
disp = [fit_disp(S["vgsr"][x], S["verr"][x]) for x in bidx]
check("K-S 30-40 dispersion", abs(disp[1]["sigma"] - 106.74) <= 0.05, f"{disp[1]['sigma']:.3f} [{disp[1]['lo']:.2f}, {disp[1]['hi']:.2f}] vs 106.74")
stop_if_failed()
for (a, b), dp in zip(BINS, disp): say(f"  bin {a:.0f}-{b:.0f}: N {dp['n']}, sigma {dp['sigma']:.2f} [{dp['lo']:.2f}, {dp['hi']:.2f}], mean {dp['mu']:.1f}")
nb_mean = 0.5 * (disp[0]["sigma"] + disp[2]["sigma"])
z_ex = (disp[1]["sigma"] - nb_mean) / math.sqrt(disp[1]["h"] ** 2 + (disp[0]["h"] ** 2 + disp[2]["h"] ** 2) / 4)
say(f"  neighbours' mean {nb_mean:.2f} km/s; excess of 30-40: {disp[1]['sigma'] - nb_mean:.2f} km/s, z_ex = {z_ex:.2f} "
    f"(one-sided Gaussian p {SST.norm.sf(z_ex):.4f})")

T = bidx[1]
v = S["vgsr"][T]; e = S["verr"][T]; cells = cell_of(S["l"][T], S["b"][T]); Bs = S["Bsgr"][T]; X = gal_unit(S["l"][T], S["b"][T])
say(f"  test bin: median VRAD_ERR {np.median(e):.1f} km/s (max {e.max():.1f})")

# ================================================================== K-N null calibration
sec("K-N 200 synthetic smooth bins at the real positions (5000 permutations each)")
masks = cell_masks(cells); A = (np.abs(Bs) >= 15) & (np.abs(Bs) < 30); B = np.abs(Bs) >= 30
i10, j10 = pairs_within(X, 10.0)
mu0, s0 = disp[1]["mu"], disp[1]["sigma"]
fires = np.zeros(3, int); pk = []
for t in range(200):
    r_ = np.random.default_rng(31 + t)
    vs_ = mu0 + r_.normal(0, s0, len(v)) + r_.normal(0, 1, len(v)) * e
    o1, _, _ = stat_L1(vs_[None], masks); o2 = stat_L2(vs_[None], A, B); o3 = stat_L3(vs_[None], i10, j10, 30.0)
    PV = perms(vs_, 5000 + t); n1, _, _ = stat_L1(PV, masks); n2 = stat_L2(PV, A, B); n3 = stat_L3(PV, i10, j10, 30.0)
    ps = (pval(n1, o1[0]), pval(n2, o2[0]), pval(n3, o3[0])); pk.append(ps)
    fires += np.array([p < 0.05 for p in ps])
for k, nm in enumerate(("L1", "L2", "L3")):
    check(f"K-N {nm} false-fire rate", 2 <= fires[k] <= 20, f"{fires[k]} / 200 at p < 0.05")
pk = np.array(pk)
say(f"  [INFO] fraction at p < 0.01: L1 {np.mean(pk[:, 0] < 0.01):.3f}, L2 {np.mean(pk[:, 1] < 0.01):.3f}, L3 {np.mean(pk[:, 2] < 0.01):.3f}")
stop_if_failed()

# ================================================================== K-P planted stream
sec("K-P planted stream: 30 stars in a 10-deg cap, v = +150 +- 15 km/s")
r_ = np.random.default_rng(4242)
vp = mu0 + r_.normal(0, s0, len(v)) + r_.normal(0, 1, len(v)) * e
j0 = r_.integers(len(v)); c0 = X[j0]
near = np.argsort(-(X @ c0))[:30]
uu = r_.uniform(math.cos(math.radians(10.0)), 1.0, 30); aa = r_.uniform(0, 2 * np.pi, 30)
e1 = np.cross(c0, [0.0, 0.0, 1.0]); e1 /= np.linalg.norm(e1); e2 = np.cross(c0, e1)
Xp = X.copy(); Xp[near] = uu[:, None] * c0 + np.sqrt(1 - uu ** 2)[:, None] * (np.cos(aa)[:, None] * e1 + np.sin(aa)[:, None] * e2)
lp = np.degrees(np.arctan2(Xp[:, 1], Xp[:, 0])) % 360; bp = np.degrees(np.arcsin(np.clip(Xp[:, 2], -1, 1)))
vp[near] = r_.normal(150.0, 15.0, 30)
_, Bp = sgr_lat_lon(lp, bp)
RP, _ = run_stats(vp, cell_of(lp, bp), Bp, Xp, 4243, 4244, with_variants=False)
say(f"  centre l {lp[j0]:.1f} b {bp[j0]:.1f}; planted stars' cells {sorted(set(cell_of(lp[near], bp[near]).tolist()))}")
check("K-P L1", RP["p1"] < 0.01, f"L1 {RP['L1']:.2f} (cell {RP['L1_cell']}), p {RP['p1']:.4f}")
check("K-P L3", RP["p3"] < 0.01, f"L3 {RP['L3']} pairs vs null mean {RP['L3_null_mean']:.1f}, p {RP['p3']:.4f}")
say(f"  [INFO] planted L1b p {RP['p1b']:.4f}; L2 z {RP['L2']:.2f} p {RP['p2']:.4f}")
stop_if_failed()

# ================================================================== the measurement
def analyse(v, tag, seedA=20261112, seedB=20261113):
    R, (pi, pj) = run_stats(v, cells, Bs, X, seedA, seedB)
    # removal of top cell
    if R["L1_cell"] >= 0:
        keep = cells != R["L1_cell"]; dn = fit_disp(v[keep], e[keep]); R["drop_top"] = dn
        s_new, h_new = dn["sigma"], dn["h"]
    else:
        s_new, h_new = None, None
    north = S["b"][T] > 0
    R["north"] = fit_disp(v[north], e[north]); R["south"] = fit_disp(v[~north], e[~north])
    R["label"] = label(R, s_new, h_new, R["north"]["sigma"], R["south"]["sigma"], nb_mean)
    R["pairs"] = (pi, pj)
    return R

sec("Test bin 30-40 kpc: L1, L1b, L2, L3")
RR = analyse(v, "real")
say(f"cells with >= 15 stars: {RR['cells_used']}; occupancy all cells: {np.bincount(cells, minlength=12).tolist()}")
for c in range(12):
    m = cells == c
    if m.sum() >= 5:
        dc = fit_disp(v[m], e[m])
        say(f"  cell {c:2d}: n {m.sum():3d}, mean v_gsr {v[m].mean():+7.1f}, ML sigma {dc['sigma']:6.1f} [{dc['lo']:.1f}, {dc['hi']:.1f}], "
            f"rms about bin mean {math.sqrt(np.mean((v[m] - v.mean()) ** 2)):6.1f}, median l {np.median(S['l'][T][m]):5.1f} b {np.median(S['b'][T][m]):+5.1f}")
    else:
        say(f"  cell {c:2d}: n {m.sum():3d}")
say(f"L1 (signed LR) = {RR['L1']:.3f} at cell {RR['L1_cell']}, p = {RR['p1']:.4f}")
say(f"L1b (dispersion z, reported) = {RR['L1b']:.3f}, p = {RR['p1b']:.4f}")
if "drop_top" in RR:
    dt = RR["drop_top"]; say(f"  bin without top cell: N {dt['n']}, sigma {dt['sigma']:.2f} [{dt['lo']:.2f}, {dt['hi']:.2f}]; threshold {nb_mean:.2f} + {dt['h']:.2f}")
dA = fit_disp(v[A], e[A]); dB = fit_disp(v[B], e[B])
say(f"L2 Sgr proximity: 15-30 deg N {RR['nA']} sigma {dA['sigma']:.2f} [{dA['lo']:.2f}, {dA['hi']:.2f}] mean {dA['mu']:+.1f}; "
    f">= 30 deg N {RR['nB']} sigma {dB['sigma']:.2f} [{dB['lo']:.2f}, {dB['hi']:.2f}] mean {dB['mu']:+.1f}")
say(f"   z = {RR['L2']:.3f}, one-sided p = {RR['p2']:.4f}, two-sided p = {RR['p2_two']:.4f}")
say(f"L3 pairs < 10 deg and < 30 km/s: {RR['L3']} (of {RR['npairs10']} close pairs), null mean {RR['L3_null_mean']:.1f}, p = {RR['p3']:.4f}")
say(f"L3 variant < 5 deg and < 20 km/s: {RR['L3v']} (of {RR['npairs5']}), null mean {RR['L3v_null_mean']:.1f}, p = {RR['p3v']:.4f}")

# 3-D variant
pm = S["pmok"][T]; Ti = T[pm]
w1 = K474 * S["d"][Ti] * S["pmra"][Ti] + S["ea"][Ti] @ S["vs"]; w2 = K474 * S["d"][Ti] * S["pmdec"][Ti] + S["no"][Ti] @ S["vs"]
V3 = S["vgsr"][Ti][:, None] * S["n"][Ti] + w1[:, None] * S["ea"][Ti] + w2[:, None] * S["no"][Ti]
rh = S["rh"][Ti]; ps_ = S["pos"][Ti]; Rc = np.hypot(ps_[:, 0], ps_[:, 1])
ph = np.vstack([-ps_[:, 1] / Rc, ps_[:, 0] / Rc, np.zeros(len(Ti))]).T; th = np.cross(ph, rh)
sph = np.vstack([np.sum(V3 * rh, 1), np.sum(V3 * th, 1), np.sum(V3 * ph, 1)]).T
X3 = X[pm]; i3, j3 = pairs_within(X3, 10.0)
def count3(SPH):
    VV = SPH[:, 0:1] * rh + SPH[:, 1:2] * th + SPH[:, 2:3] * ph
    return int(np.sum(np.linalg.norm(VV[i3] - VV[j3], axis=1) < 50.0))
o3d = count3(sph); r3 = np.random.default_rng(20261114)
n3d = np.array([count3(sph[r3.permutation(len(sph))]) for _ in range(NPERM)])
p3d = pval(n3d, o3d)
say(f"L3 3-D variant ({len(Ti)} stars with usable PMs; < 10 deg and |Delta V| < 50 km/s): {o3d} (of {len(i3)}), null mean {n3d.mean():.1f}, p = {p3d:.4f}")

sec("Reported without a label")
for nm, m in (("Galactic north b > 0", S["b"][T] > 0), ("Galactic south b < 0", S["b"][T] < 0),
              ("sub-bin 30-35", S["r"][T] < 35), ("sub-bin 35-40", S["r"][T] >= 35)):
    dd = fit_disp(v[m], e[m]); say(f"  {nm}: N {dd['n']}, sigma {dd['sigma']:.2f} [{dd['lo']:.2f}, {dd['hi']:.2f}], mean {dd['mu']:+.1f}")
kur = float(SST.kurtosis(v, fisher=True, bias=True)); sw = SST.shapiro(v)
say(f"  bin mean v_gsr {v.mean():+.2f} km/s; excess kurtosis {kur:+.3f}; Shapiro-Wilk W {sw.statistic:.4f}, p {sw.pvalue:.4f}")

sec("Control bins (same statistics)")
CTRL = {}
for bi in (0, 2):
    Tc = bidx[bi]; vc = S["vgsr"][Tc]
    Rc_, _ = run_stats(vc, cell_of(S["l"][Tc], S["b"][Tc]), S["Bsgr"][Tc], gal_unit(S["l"][Tc], S["b"][Tc]), 20261120 + bi, 20261120 + bi + 100)
    CTRL[f"{BINS[bi][0]:.0f}-{BINS[bi][1]:.0f}"] = Rc_
    say(f"  bin {BINS[bi][0]:.0f}-{BINS[bi][1]:.0f} (N {len(Tc)}): L1 p {Rc_['p1']:.4f} (cell {Rc_['L1_cell']}), L1b p {Rc_['p1b']:.4f}, "
        f"L2 z {Rc_['L2']:+.2f} p {Rc_['p2']:.4f}, L3 {Rc_['L3']} vs {Rc_['L3_null_mean']:.1f} p {Rc_['p3']:.4f}, L3(5,20) p {Rc_['p3v']:.4f}")

sec("LABEL (test bin 30-40 kpc)")
say(f"LABEL: {RR['label']}")
say(f"  L1 p {RR['p1']:.4f}; L2 p {RR['p2']:.4f}; L3 p {RR['p3']:.4f}; north sigma {RR['north']['sigma']:.2f}, south sigma {RR['south']['sigma']:.2f} (threshold {nb_mean:.2f})")
say(f"  significance of the excess over the neighbours: z_ex = {z_ex:.2f}")
POST = {}
if any(k in RR["label"] for k in ("LOCALISED", "SAGITTARIUS", "CLUMPED")):
    say("POST HOC (not graded):")
    rem = {}
    if "LOCALISED" in RR["label"]: rem["top cell"] = cells == RR["L1_cell"]
    if "SAGITTARIUS" in RR["label"]: rem["Sgr 15-30 group"] = A
    if "CLUMPED" in RR["label"]:
        mm = np.zeros(len(v), bool); pi, pj = RR["pairs"]; cl = np.abs(v[pi] - v[pj]) < 30.0; mm[pi[cl]] = True; mm[pj[cl]] = True
        rem["stars in counted pairs"] = mm
    for nm, mm in rem.items():
        dd = fit_disp(v[~mm], e[~mm])
        fn = [round(fo * dd["sigma"] / 106.74, 3) for fo in (1.205, 1.155, 1.135, 1.114)]
        say(f"  without {nm} ({mm.sum()} stars): sigma {dd['sigma']:.2f} [{dd['lo']:.2f}, {dd['hi']:.2f}]; f_new (census can, census alt, rc can, rc alt) {fn}")
        POST[nm] = dict(removed=int(mm.sum()), disp=dd, f_new=fn)

# ================================================================== mutation (separate file)
MUT = open(os.path.join(HERE, "hot1_mut.out"), "w")
vm = np.random.default_rng(777).permutation(v)
RM = analyse(vm, "mutation")
ok = not any(k in RM["label"] for k in ("LOCALISED", "SAGITTARIUS", "CLUMPED"))
for line in (f"HOT1 mutation M1: real 30-40 v_gsr shuffled once (seed 777), whole labelled analysis re-run.",
             f"L1 {RM['L1']:.3f} (cell {RM['L1_cell']}) p {RM['p1']:.4f}; L1b p {RM['p1b']:.4f}; L2 z {RM['L2']:.3f} p {RM['p2']:.4f}; L3 {RM['L3']} p {RM['p3']:.4f}",
             f"north {RM['north']['sigma']:.2f} south {RM['south']['sigma']:.2f}",
             f"label {RM['label']}; mutation passes (not LOCALISED / SAGITTARIUS RESIDUE / CLUMPED): {ok}",
             "kappa = 1/2 FITTED; not theory closed. Adopts nothing."):
    print("[MUT] " + line); MUT.write(line + "\n")
MUT.close()

def clean(o):
    if isinstance(o, dict): return {str(k): clean(x) for k, x in o.items() if k != "pairs"}
    if isinstance(o, (list, tuple)): return [clean(x) for x in o]
    if isinstance(o, (np.floating, np.integer)): return o.item()
    if isinstance(o, np.bool_): return bool(o)
    if isinstance(o, np.ndarray): return clean(o.tolist())
    return o
json.dump(clean(dict(counts=counts, disp=disp, nb_mean=nb_mean, z_ex=z_ex, KN_fires=fires, planted=RP, real=RR,
                     sgr_groups=dict(A=dA, B=dB), L3_3d=dict(count=o3d, null_mean=float(n3d.mean()), p=p3d, n=int(len(Ti))),
                     kurtosis=kur, shapiro=[float(sw.statistic), float(sw.pvalue)], controls=CTRL, post_hoc=POST, mutation=RM)),
          open(os.path.join(HERE, "hot1_results.json"), "w"), indent=1)
say("\nkappa = 1/2 FITTED; not theory closed. Adopts nothing.")
OUT.close()
