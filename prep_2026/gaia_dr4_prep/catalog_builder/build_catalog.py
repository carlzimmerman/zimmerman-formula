#!/usr/bin/env python3
"""Step 2 of the DR4 wide-binary catalog chain: extract -> pipeline CSV.

    python3 build_catalog.py --release dr3     # validation (now)
    python3 build_catalog.py --release dr4     # 2 Dec 2026

Stages (each cached as an .npz in the extract directory, rerun with --force):
  A  load the 12 extract chunks
  B  phase-space neighbour counts; drop stars with > 30 neighbours
     (El-Badry+2021 Sec 2.1; transcribed from num_neighbors_edr3.py)
  C  pair search out to s = 1 pc with El-Badry's parallax and proper-motion
     consistency cuts (transcribed from find_binaries_edr3.py)
  D  remove duplicate pairs, resolved triples, and cluster members
     (pairs with >= 2 neighbouring pairs within 5 pc / 5 km/s / 2 sigma)
  E  30 shifted chance-alignment realisations (El-Badry Sec 3.1, App. A)
  F  R_chance = N_chance / N_candidates from 7-D Gaussian KDEs with the
     Table A1 features and bandwidth 0.2; candidates leave-10%-out
  G  the FROZEN_DR4_CUTS of wide_binary_pipeline.py, then write the CSV
     read by `wide_binary_pipeline.py --catalog`

Scope notes (declared, not hidden):
  * R_chance is computed with El-Badry's recipe on THIS extract
    (parallax > 3.5 mas, |b| > 10 deg), not on their 1-kpc all-sky sample,
    and only for candidates with s < 200 kAU.  Excluded candidates sit
    >= 3.7 KDE bandwidths away from any s <= 30 kAU pair in the (log theta,
    4/parallax) plane, so they contribute < 0.2% of any density used.
  * Shifted pairs get the star-level crowding cut but not the pair-level
    triple/cluster cleaning; El-Badry Sec 3.1 does not state that they do.
  * The A_V < 0.5 cut (SFD98) and Banik's Monte-Carlo vtilde-error cut
    need inputs not in the extract; stage G applies them only when those
    inputs are present, and says so in the report otherwise.
"""
import argparse
import json
import multiprocessing as mp
import sys
import time
from pathlib import Path

import numpy as np
from sklearn.neighbors import BallTree

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(HERE.parent))
MAS2RAD = np.pi / 180 / 3600 / 1000
S_MAX_AU = 206265.0            # El-Badry: 1 pc
S_KDE_AU = 200_000.0           # KDE truncation (see scope notes)
N_SHIFT = 30
BANDWIDTH = 0.2
SEED = 20261202
CTX = mp.get_context("fork")
CHANCE_MODE = "elbadry"        # set from --chance-mode; see stage E
NPROC = max(1, mp.cpu_count() - 1)


# ---------------------------------------------------------------- helpers
def delta_mu_and_sigma(pmra1, pmdec1, pmra2, pmdec2, e_ra1, e_de1, e_ra2, e_de2):
    """El-Badry eq. 3-4 (find_binaries_edr3.get_delta_mu_and_sigma)."""
    dra, dde = pmra1 - pmra2, pmdec1 - pmdec2
    dmu = np.sqrt(dra ** 2 + dde ** 2)
    with np.errstate(invalid="ignore", divide="ignore"):
        sig = np.sqrt((e_ra1 ** 2 + e_ra2 ** 2) * dra ** 2
                      + (e_de1 ** 2 + e_de2 ** 2) * dde ** 2) / dmu
    zero = np.sqrt(e_ra1 ** 2 + e_ra2 ** 2 + e_de1 ** 2 + e_de2 ** 2)
    sig = np.where(dmu > 0, sig, zero)        # El-Badry: all four variances when dmu = 0
    return dmu, sig


def galactic(ra, dec):
    aN, dN = np.radians(192.85948), np.radians(27.12825)
    r, d = np.radians(ra), np.radians(dec)
    b = np.degrees(np.arcsin(np.sin(d) * np.sin(dN) + np.cos(d) * np.cos(dN) * np.cos(r - aN)))
    l = (122.93192 - np.degrees(np.arctan2(np.cos(d) * np.sin(r - aN),
                                           np.sin(d) * np.cos(dN) - np.cos(d) * np.sin(dN) * np.cos(r - aN)))) % 360
    return l, b


def ang_sep_arcsec(ra1, dec1, ra2, dec2):
    r1, d1, r2, d2 = map(np.radians, (ra1, dec1, ra2, dec2))
    h = np.sin((d2 - d1) / 2) ** 2 + np.cos(d1) * np.cos(d2) * np.sin((r2 - r1) / 2) ** 2
    return np.degrees(2 * np.arcsin(np.sqrt(h))) * 3600


# ---------------------------------------------------------------- stage A
def stage_a(ext, chunks=range(12)):
    from astropy.io import fits
    cols = None
    parts = []
    for k in chunks:
        with fits.open(ext / f"chunk_{k:02d}.fits", memmap=True) as h:
            d = h[1].data
            cols = cols or [c.lower() for c in d.columns.names]
            parts.append({c: np.array(d[c]) for c in d.columns.names})
    S = {c.lower(): np.concatenate([p[c] for p in parts]) for c in parts[0]}
    _, uniq = np.unique(S["source_id"], return_index=True)
    S = {k: v[np.sort(uniq)] for k, v in S.items()}
    S["l"], S["b"] = galactic(S["ra"], S["dec"])
    return S


# ---------------------------------------------------------------- stage B
_G = {}


def _nbr_block(idx):
    S, tree, bright = _G["S"], _G["tree"], _G["bright"]
    plx, eplx = S["parallax"][idx], S["parallax_error"][idx]
    theta = 5 * 206265.0 / (1000 / plx) * np.pi / 180 / 3600
    inds = tree.query_radius(_G["coords"][idx], r=theta)
    out = np.zeros(len(idx))
    for i, js in enumerate(inds):
        js = bright[js]
        dpar = np.abs(plx[i] - S["parallax"][js]) / np.hypot(eplx[i], S["parallax_error"][js])
        dmu, sdmu = delta_mu_and_sigma(S["pmra"][idx[i]], S["pmdec"][idx[i]], S["pmra"][js],
                                       S["pmdec"][js], S["pmra_error"][idx[i]], S["pmdec_error"][idx[i]],
                                       S["pmra_error"][js], S["pmdec_error"][js])
        mu_max = 0.21095 * 5 * plx[i]
        out[i] = np.sum((dmu < mu_max + 2 * sdmu) & (dpar < 2) & (js != idx[i]))
    return out


def stage_b(S):
    bright = np.flatnonzero(S["phot_g_mean_mag"] < 18)
    coords = np.vstack([np.radians(S["dec"]), np.radians(S["ra"])]).T
    _G.update(S=S, bright=bright, coords=coords,
              tree=BallTree(coords[bright], leaf_size=10, metric="haversine"))
    blocks = np.array_split(np.arange(len(S["ra"])), 400)
    with CTX.Pool(NPROC) as pool:
        res = pool.map(_nbr_block, blocks)
    return np.concatenate(res)


# ---------------------------------------------------------------- stage C
def _pair_block(args):
    idx, shift, rng_seed = args
    S, tree, keep = _G["S"], _G["tree"], _G["keep"]
    ra, dec = S["ra"][idx].copy(), S["dec"][idx].copy()
    plx0 = S["parallax"][idx]
    if shift:
        rng = np.random.default_rng(rng_seed)
        step = np.full(len(idx), 0.5)                              # El-Badry: 0.5 deg
        if CHANCE_MODE == "scaled_clean":
            # a nearby star's search radius can exceed 0.5 deg (200 kAU at
            # d < 111 pc), letting it re-find its own real companion; shift by
            # at least 3 search radii so that cannot happen
            th_deg = S_KDE_AU / (1000 / plx0) / 3600
            step = np.maximum(0.5, 3 * th_deg)
        ra = (ra + step / np.cos(np.radians(dec))) % 360
        dec = np.clip(dec + step * rng.uniform(-1, 1, len(dec)), -89.999, 89.999)
    theta_max = S_MAX_AU / (1000 / plx0) * np.pi / 180 / 3600
    if shift:  # only chance alignments that can matter for the KDE (s < S_KDE_AU)
        theta_max = S_KDE_AU / (1000 / plx0) * np.pi / 180 / 3600
    q = np.vstack([np.radians(dec), np.radians(ra)]).T
    inds, dists = tree.query_radius(q, r=theta_max, return_distance=True)
    p1, p2, tt = [], [], []
    for i, (js, dd) in enumerate(zip(inds, dists)):
        js = keep[js]
        th = dd * 180 / np.pi * 3600
        me = idx[i]
        G1, Gj = S["phot_g_mean_mag"][me], S["phot_g_mean_mag"][js]
        bplx = np.where(Gj > G1, plx0[i], S["parallax"][js])      # brighter component's parallax
        dpar = np.abs(plx0[i] - S["parallax"][js]) / np.hypot(S["parallax_error"][me], S["parallax_error"][js])
        dmu, sdmu = delta_mu_and_sigma(S["pmra"][me], S["pmdec"][me], S["pmra"][js], S["pmdec"][js],
                                       S["pmra_error"][me], S["pmdec_error"][me],
                                       S["pmra_error"][js], S["pmdec_error"][js])
        with np.errstate(divide="ignore"):
            dmu_orb = np.where(th > 0, 0.44428 * bplx ** 1.5 * th ** -0.5, 1e9)
        sep = 1000 / bplx * th
        bmax = np.where(th < 4, 6.0, 3.0)
        m = (dpar < bmax) & (dmu < dmu_orb + 2 * sdmu) & (th > 0.001) & (sep < S_MAX_AU) & (js != me)
        if shift:
            m &= th > 0.5
        if m.any():
            p1.append(np.full(m.sum(), me, dtype=np.int64))
            p2.append(js[m].astype(np.int64))
            tt.append(th[m])
    if not p1:
        return np.zeros(0, np.int64), np.zeros(0, np.int64), np.zeros(0)
    return np.concatenate(p1), np.concatenate(p2), np.concatenate(tt)


def pair_search(S, keep, shift=False, seed=0):
    coords = np.vstack([np.radians(S["dec"][keep]), np.radians(S["ra"][keep])]).T
    _G.update(S=S, keep=keep, tree=BallTree(coords, leaf_size=20, metric="haversine"))
    blocks = np.array_split(keep, 400)
    args = [(b, shift, seed * 1000 + k) for k, b in enumerate(blocks)]
    with CTX.Pool(NPROC) as pool:
        res = pool.map(_pair_block, args)
    return tuple(np.concatenate([r[k] for r in res]) for k in range(3))


def orient(S, p1, p2, th, dedup=True):
    """Brighter component first.  Real pairs are found twice (i->j, j->i) and
    are de-duplicated; SHIFTED pairs are not, because (i shifted, j) and
    (j shifted, i) are distinct chance alignments (El-Badry: N(N+1) pairs,
    then kept with probability 1/2)."""
    swap = S["phot_g_mean_mag"][p1] > S["phot_g_mean_mag"][p2]
    a, b = np.where(swap, p2, p1), np.where(swap, p1, p2)
    if not dedup:
        return a, b, th
    key = np.minimum(a, b) * 10_000_000_000 + np.maximum(a, b)
    _, u = np.unique(key, return_index=True)
    u = np.sort(u)
    return a[u], b[u], th[u]


# ---------------------------------------------------------------- stage D
def remove_triples(a, b):
    ids = np.concatenate([a, b])
    vals, counts = np.unique(ids, return_counts=True)
    multi = set(vals[counts > 1].tolist())
    ok = np.array([(x not in multi) and (y not in multi) for x, y in zip(a, b)])
    return a[ok], b[ok]


def _cluster_block(idx):
    S, P, tree = _G["S"], _G["P"], _G["tree"]
    out = np.zeros(len(idx))
    th = 5 * P["plx"][idx] / 1000
    inds = tree.query_radius(_G["coords"][idx], r=th)
    for i, js in enumerate(inds):
        k = idx[i]
        dpar = np.abs(P["plx"][k] - P["plx"][js]) / np.hypot(P["eplx"][k], P["eplx"][js])
        dmu, sdmu = delta_mu_and_sigma(P["pmra"][k], P["pmdec"][k], P["pmra"][js], P["pmdec"][js],
                                       P["epmra"][k], P["epmdec"][k], P["epmra"][js], P["epmdec"][js])
        mu_max = 0.21095 * 5 * P["plx"][k]
        out[i] = np.sum((dmu < mu_max + 2 * sdmu) & (dpar < 2) & (js != k))
    return out


def remove_clusters(S, a, b):
    P = {"plx": S["parallax"][a], "eplx": S["parallax_error"][a], "pmra": S["pmra"][a],
         "pmdec": S["pmdec"][a], "epmra": S["pmra_error"][a], "epmdec": S["pmdec_error"][a]}
    coords = np.vstack([np.radians(S["dec"][a]), np.radians(S["ra"][a])]).T
    _G.update(S=S, P=P, coords=coords, tree=BallTree(coords, leaf_size=10, metric="haversine"))
    blocks = np.array_split(np.arange(len(a)), 200)
    with CTX.Pool(NPROC) as pool:
        n = np.concatenate(pool.map(_cluster_block, blocks))
    return a[n < 2], b[n < 2], n


# ---------------------------------------------------------------- stage F
def sigma18_map(ext):
    import healpy as hp
    from astropy.io import fits
    with fits.open(ext / "sigma18_hpx7.fits") as h:
        d = h[1].data
        pix, cnt = np.array(d["hpx7"], dtype=np.int64), np.array(d["n"], dtype=np.float64)
    m = np.zeros(hp.nside2npix(128))
    m[pix] = cnt
    return m


def sigma18_at(ra, dec, m):
    import healpy as hp
    out = np.empty(len(ra))
    vec = hp.ang2vec(ra, dec, lonlat=True)
    for i in range(len(ra)):
        pix = hp.query_disc(128, vec[i], np.radians(1.0), nest=True, inclusive=False)
        out[i] = m[pix].sum() / np.pi
    return out


def features(S, a, b, th, sig18):
    p1, p2 = S["parallax"][a], S["parallax"][b]
    e1, e2 = S["parallax_error"][a], S["parallax_error"][b]
    sdp = np.hypot(e1, e2)
    vperp1 = 4.74047 * np.hypot(S["pmra"][a], S["pmdec"][a]) / p1
    dmu, sdmu = delta_mu_and_sigma(S["pmra"][a], S["pmdec"][a], S["pmra"][b], S["pmdec"][b],
                                   S["pmra_error"][a], S["pmdec_error"][a],
                                   S["pmra_error"][b], S["pmdec_error"][b])
    from scipy.special import erf
    dmu_orb = 0.44428 * p1 ** 1.5 * th ** -0.5
    with np.errstate(invalid="ignore", divide="ignore"):
        z = np.where(sdmu > 0, (dmu - dmu_orb) / sdmu, -1e3)
    X = np.vstack([np.log10(th), 4 / p1, 4 * sdp, 4 * np.log10(np.maximum(sig18, 1.0)),
                   vperp1 / 50, np.abs(p1 - p2) / sdp, 2 * erf(z)]).T
    return X


def kde_density(train, query, weights_total):
    from sklearn.neighbors import KernelDensity
    kd = KernelDensity(kernel="gaussian", bandwidth=BANDWIDTH, rtol=1e-4, atol=0.0)
    kd.fit(train)
    chunks = np.array_split(np.arange(len(query)), NPROC * 4)
    with CTX.Pool(NPROC) as pool:
        logs = pool.map(kd.score_samples, [query[c] for c in chunks])
    return weights_total * np.exp(np.concatenate(logs))


def r_chance(Xc, Xs_list):
    """El-Badry eq. 8 with App. A: candidate KDE leave-10%-out; chance KDE
    from all shifted realisations combined, divided by the number of them."""
    rng = np.random.default_rng(SEED)
    fold = rng.integers(0, 10, len(Xc))
    Nc = np.empty(len(Xc))
    for f in range(10):
        tr, te = fold != f, fold == f
        Nc[te] = kde_density(Xc[tr], Xc[te], len(Xc))   # density x N (90% sample stands for N)
    Xs = np.vstack(Xs_list)
    Ns = kde_density(Xs, Xc, len(Xs)) / len(Xs_list)
    with np.errstate(divide="ignore", invalid="ignore"):
        return Ns / Nc


# ---------------------------------------------------------------- stage G
def frozen_cuts(S, a, b, R, extra):
    sys.path.insert(0, str(HERE.parent))
    from wide_binary_pipeline import mass_of_MG, G as GN, MSUN, AU
    p1, p2 = S["parallax"][a], S["parallax"][b]
    d1, d2 = 1000 / p1, 1000 / p2
    dist = 0.5 * (d1 + d2)
    sd = np.hypot(1000 * S["parallax_error"][a] / p1 ** 2, 1000 * S["parallax_error"][b] / p2 ** 2)
    th = ang_sep_arcsec(S["ra"][a], S["dec"][a], S["ra"][b], S["dec"][b])
    sep_au = 1000 / p1 * th
    g1, g2 = S["phot_g_mean_mag"][a], S["phot_g_mean_mag"][b]
    MG1, MG2 = g1 - 5 * np.log10(dist / 10), g2 - 5 * np.log10(dist / 10)
    M1, M2 = mass_of_MG(MG1), mass_of_MG(MG2)
    Mt = M1 + M2
    dpm = np.hypot(S["pmra"][a] - S["pmra"][b], S["pmdec"][a] - S["pmdec"][b])
    vsky = 4.74047 * dpm * dist / 1000
    vc = np.sqrt(GN * Mt * MSUN / (sep_au * AU)) / 1e3
    rv1, rv2 = S["radial_velocity"][a], S["radial_velocity"][b]
    erv = np.hypot(S["radial_velocity_error"][a], S["radial_velocity_error"][b])
    both_rv = np.isfinite(rv1) & np.isfinite(rv2)
    rv_bad = both_rv & (np.abs(rv1 - rv2) > np.maximum(3 * erv, 3 * vc))
    nss = (S["non_single_star"][a] > 0) | (S["non_single_star"][b] > 0)
    cut = {
        "|b|>15": np.abs(S["b"][a]) > 15,
        "G<17 both": (g1 < 17) & (g2 < 17),
        "d<250": dist < 250,
        "plx S/N>=40 both": (p1 / S["parallax_error"][a] >= 40) & (p2 / S["parallax_error"][b] >= 40),
        "plx consistency": np.abs(d1 - d2) < np.minimum(4 * sd, 8),
        "2<s<30 kAU": (sep_au > 2000) & (sep_au < 30000),
        "RUWE<1.4 both": (S["ruwe"][a] < 1.4) & (S["ruwe"][b] < 1.4),
        "ipd_frac_multi_peak<=2 both": (S["ipd_frac_multi_peak"][a] <= 2) & (S["ipd_frac_multi_peak"][b] <= 2),
        "mass range": (Mt > 0.464) & (Mt < 4.31),
        "RV screen": ~rv_bad,
        "NSS screen": ~nss,
        "triple search": ~extra["third"],
        "R_chance<0.01": R < 0.01,
    }
    if "AV_ok" in extra:
        cut["A_V<0.5"] = extra["AV_ok"]
    if "vt_err_ok" in extra:
        cut["vtilde error"] = extra["vt_err_ok"]
    keep = np.ones(len(a), bool)
    flow = []
    for name, m in cut.items():
        keep &= m
        flow.append((name, int(keep.sum())))
    ra2, dec2 = S["ra"][b], S["dec"][b]
    ra1, dec1 = np.radians(S["ra"][a]), np.radians(S["dec"][a])
    pa = np.degrees(np.arctan2(np.sin(np.radians(ra2) - ra1) * np.cos(np.radians(dec2)),
                               np.cos(dec1) * np.sin(np.radians(dec2))
                               - np.sin(dec1) * np.cos(np.radians(dec2)) * np.cos(np.radians(ra2) - ra1))) % 360
    table = {"sep_kAU": sep_au / 1e3, "v_perp_kms": vsky, "M1_msun": M1, "M2_msun": M2,
             "d_pc": dist, "l_gal": S["l"][a], "b_gal": S["b"][a], "pa_deg": pa,
             "source_id1": S["source_id"][a], "source_id2": S["source_id"][b], "R_chance": R}
    return keep, flow, table


def third_star_flags(S, a, b):
    """Frozen 'triple search': a co-moving third source with G < 20 within
    30 kAU (projected, at the primary's distance) of either component."""
    coords = np.vstack([np.radians(S["dec"]), np.radians(S["ra"])]).T
    tree = BallTree(coords, leaf_size=20, metric="haversine")
    flags = np.zeros(len(a), bool)
    for comp in (a, b):
        th = 30000.0 / (1000 / S["parallax"][a]) * np.pi / 180 / 3600
        inds, dd = tree.query_radius(coords[comp], r=th, return_distance=True)
        for i, (js, d) in enumerate(zip(inds, dd)):
            js = js[(js != a[i]) & (js != b[i])]
            if len(js) == 0:
                continue
            k = a[i]
            thk = ang_sep_arcsec(S["ra"][k], S["dec"][k], S["ra"][js], S["dec"][js])
            dpar = np.abs(S["parallax"][k] - S["parallax"][js]) / np.hypot(S["parallax_error"][k], S["parallax_error"][js])
            dmu, sdmu = delta_mu_and_sigma(S["pmra"][k], S["pmdec"][k], S["pmra"][js], S["pmdec"][js],
                                           S["pmra_error"][k], S["pmdec_error"][k],
                                           S["pmra_error"][js], S["pmdec_error"][js])
            with np.errstate(divide="ignore"):
                orb = np.where(thk > 0, 0.44428 * S["parallax"][k] ** 1.5 * thk ** -0.5, 1e9)
            hit = (dpar < 3) & (dmu < orb + 2 * sdmu) & (S["phot_g_mean_mag"][js] < 20)
            flags[i] |= bool(hit.any())
    return flags


# ---------------------------------------------------------------- stage G1: A_V (SFD98)
DUST_DIR = REPO / "real_research" / "data" / "dustmaps"


def av_sfd98(S, path):
    """Banik+2024 Sec 2.4.1: A_V < 0.5 for both stars from the SFD98 maps
    (total line-of-sight extinction; conservative at < 250 pc).  Conversion
    A_V = 3.1 E(B-V) on the raw SFD scale (Banik do not state one; the
    Schlafly & Finkbeiner 2011 x0.86 recalibration is NOT applied, which
    makes the cut slightly stricter).  Maps: kbarbary/sfddata mirror of the
    SFD98 4096^2 NGP/SGP FITS files."""
    if path.exists():
        return dict(np.load(path))
    if not (DUST_DIR / "sfd" / "SFD_dust_4096_ngp.fits").exists():
        return None
    from dustmaps.config import config
    config["data_dir"] = str(DUST_DIR)
    from dustmaps.sfd import SFDQuery
    from astropy.coordinates import SkyCoord
    import astropy.units as u
    q = SFDQuery()
    ebv = np.asarray(q(SkyCoord(l=S["l"] * u.deg, b=S["b"] * u.deg, frame="galactic")), dtype=float)
    out = {"av": 3.1 * ebv, "ok_index": np.flatnonzero(3.1 * ebv < 0.5)}
    np.savez(path, **out)
    return out


# ---------------------------------------------------------------- stage G2: Banik eq. 10
def fetch_correlations(release, source_ids, cache):
    """parallax_pmra_corr, parallax_pmdec_corr for the stars that survive the
    other cuts (small second query; the main extract omits them)."""
    if cache.exists():
        z = np.load(cache)
        if np.isin(source_ids, z["source_id"]).all():
            return {k: z[k] for k in z.files}
    from astroquery.gaia import Gaia
    ids = np.unique(source_ids)
    got = {"source_id": [], "parallax_pmra_corr": [], "parallax_pmdec_corr": []}
    for k in range(0, len(ids), 2000):
        chunk = ",".join(str(int(x)) for x in ids[k:k + 2000])
        q = (f"SELECT source_id, parallax_pmra_corr, parallax_pmdec_corr "
             f"FROM gaia{release}.gaia_source WHERE source_id IN ({chunk})")
        r = Gaia.launch_job_async(q).get_results()
        for c in got:
            got[c].append(np.array(r[c]))
    out = {c: np.concatenate(v) for c, v in got.items()}
    np.savez(cache, **out)
    return out


def vt_error_mc(S, a, b, th, corr, n_trials=212, seed=SEED):
    """Banik+2024 Sec 2.3/2.4.6, transcribed: parallax and proper motion drawn
    from each star's 3x3 Gaia covariance (positions taken at face value); the
    mean distance from the inverse-variance-weighted parallax; the LOS
    separation from P(x) ~ x^-2.6 / sqrt(x^2 - 1), x = r/r_sky >= 1, split
    evenly with a random sign; masses from each star's own distance with a
    5.5% Gaussian scatter.  Returns (vtilde_adopted, sigma_vtilde)."""
    from wide_binary_pipeline import mass_of_MG, G as GN, MSUN, AU
    rng = np.random.default_rng(seed)
    idx = {int(s_): i for i, s_ in enumerate(corr["source_id"])}

    def cov(k):
        j = np.array([idx[int(x)] for x in S["source_id"][k]])
        e = np.vstack([S["parallax_error"][k], S["pmra_error"][k], S["pmdec_error"][k]]).T
        r_pa, r_pd = corr["parallax_pmra_corr"][j], corr["parallax_pmdec_corr"][j]
        r_ad = S["pmra_pmdec_corr"][k]
        C = np.zeros((len(k), 3, 3))
        C[:, 0, 0], C[:, 1, 1], C[:, 2, 2] = e[:, 0] ** 2, e[:, 1] ** 2, e[:, 2] ** 2
        C[:, 0, 1] = C[:, 1, 0] = r_pa * e[:, 0] * e[:, 1]
        C[:, 0, 2] = C[:, 2, 0] = r_pd * e[:, 0] * e[:, 2]
        C[:, 1, 2] = C[:, 2, 1] = r_ad * e[:, 1] * e[:, 2]
        return np.linalg.cholesky(C + 1e-18 * np.eye(3))

    L1, L2 = cov(a), cov(b)
    m1 = np.vstack([S["parallax"][a], S["pmra"][a], S["pmdec"][a]]).T
    m2 = np.vstack([S["parallax"][b], S["pmra"][b], S["pmdec"][b]]).T
    g1, g2 = S["phot_g_mean_mag"][a], S["phot_g_mean_mag"][b]
    th_rad = th / 3600 * np.pi / 180

    def vt_of(o1, o2, push):
        w1, w2 = S["parallax_error"][a] ** -2, S["parallax_error"][b] ** -2
        plx = (w1 * o1[:, 0] + w2 * o2[:, 0]) / (w1 + w2)
        dbar = 1000 / plx                                           # pc
        rsky = th_rad * dbar                                        # pc
        dlos = rsky * np.sqrt(np.maximum(push ** 2 - 1, 0.0))
        sgn = rng.choice([-1.0, 1.0], len(a))
        dd1, dd2 = dbar + sgn * dlos / 2, dbar - sgn * dlos / 2
        M1 = mass_of_MG(g1 - 5 * np.log10(dd1 / 10)) * (1 + 0.055 * rng.standard_normal(len(a)))
        M2 = mass_of_MG(g2 - 5 * np.log10(dd2 / 10)) * (1 + 0.055 * rng.standard_normal(len(a)))
        vx = 4.74047 * (o1[:, 1] * dd1 - o2[:, 1] * dd2) / 1000     # km/s
        vy = 4.74047 * (o1[:, 2] * dd1 - o2[:, 2] * dd2) / 1000
        vc = np.sqrt(GN * (M1 + M2) * MSUN / (rsky * 206265 * AU)) / 1e3
        return np.hypot(vx, vy) / vc

    def draw_x(n):
        """Inverse CDF of P(x) ~ x^-2.6 / sqrt(x^2-1) on x >= 1 (tabulated)."""
        xs = np.concatenate([1 + np.logspace(-8, 0, 4000), np.logspace(np.log10(2.0), 4, 4000)[1:]])
        pdf = xs ** -2.6 / np.sqrt(xs ** 2 - 1)
        cdf = np.concatenate([[0], np.cumsum(0.5 * (pdf[1:] + pdf[:-1]) * np.diff(xs))])
        cdf /= cdf[-1]
        return np.interp(rng.random(n), cdf, xs)

    trials = np.empty((n_trials, len(a)))
    for t in range(n_trials):
        o1 = m1 + np.einsum("nij,nj->ni", L1, rng.standard_normal((len(a), 3)))
        o2 = m2 + np.einsum("nij,nj->ni", L2, rng.standard_normal((len(a), 3)))
        trials[t] = vt_of(o1, o2, draw_x(len(a)))
    return np.std(trials, axis=0)


# ---------------------------------------------------------------- driver
def cached(path, force, fn):
    if path.exists() and not force:
        return dict(np.load(path, allow_pickle=False))
    t0 = time.time()
    out = fn()
    np.savez(path, **out)
    print(f"  wrote {path.name} in {time.time() - t0:.0f} s")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--release", choices=("dr3", "dr4"), required=True)
    ap.add_argument("--force", default="", help="comma list of stages to recompute, e.g. C,E")
    ap.add_argument("--chance-mode", choices=("elbadry", "scaled_clean"), default="elbadry",
                    help="elbadry: 0.5 deg shift, uncleaned (as published); scaled_clean: shift >= 3 "
                         "search radii and triple-cleaned like the candidates")
    ap.add_argument("--test-chunks", type=int, default=0,
                    help="smoke test on the first N chunks, cached in <extract>/test/")
    args = ap.parse_args()
    global CHANCE_MODE
    CHANCE_MODE = args.chance_mode
    sfx = "" if CHANCE_MODE == "elbadry" else f"_{CHANCE_MODE}"
    force = set(args.force.upper().split(",")) if args.force else set()
    ext = REPO / "real_research" / "data" / "widebinaries" / f"{args.release}_extract"
    src = ext
    if args.test_chunks:
        global N_SHIFT
        N_SHIFT = 3
        ext = src / "test"
        ext.mkdir(exist_ok=True)
        for f in ("sigma18_hpx7.fits",):
            if (src / f).exists() and not (ext / f).exists():
                (ext / f).symlink_to(src / f)
    report = {"release": args.release}

    print("[A] load extract")
    S = cached(ext / "stage_A.npz", "A" in force,
               lambda: stage_a(src, range(args.test_chunks) if args.test_chunks else range(12)))
    report["n_sources"] = int(len(S["ra"]))
    print(f"    {report['n_sources']:,d} sources")

    print("[B] neighbour counts")
    B = cached(ext / "stage_B.npz", "B" in force, lambda: {"n_nbr": stage_b(S)})
    keep = np.flatnonzero(B["n_nbr"] <= 30)
    report["n_uncrowded"] = int(len(keep))
    print(f"    {len(keep):,d} stars with <= 30 neighbours")

    print("[C] pair search (s < 1 pc)")
    C = cached(ext / "stage_C.npz", "C" in force,
               lambda: dict(zip(("a", "b", "th"), orient(S, *pair_search(S, keep)))))
    report["n_initial_pairs"] = int(len(C["a"]))
    print(f"    {len(C['a']):,d} initial candidate pairs")

    print("[D] triples + clusters")
    def _d():
        th_of = {(x, y): t for x, y, t in zip(C["a"].tolist(), C["b"].tolist(), C["th"].tolist())}
        a, b = remove_triples(C["a"], C["b"])
        a, b, _ = remove_clusters(S, a, b)
        th = np.array([th_of[(x, y)] for x, y in zip(a.tolist(), b.tolist())])
        return {"a": a, "b": b, "th": th}
    D = cached(ext / "stage_D.npz", "D" in force, _d)
    report["n_clean_pairs"] = int(len(D["a"]))
    print(f"    {len(D['a']):,d} cleaned candidate pairs")

    print(f"[E] {N_SHIFT} shifted realisations")
    def _e():
        out = {}
        rng = np.random.default_rng(SEED)
        for r in range(N_SHIFT):
            p1, p2, th = orient(S, *pair_search(S, keep, shift=True, seed=r + 1), dedup=False)
            m = rng.random(len(p1)) < 0.5                     # N(N+1) -> N(N+1)/2
            p1, p2, th = p1[m], p2[m], th[m]
            if CHANCE_MODE == "scaled_clean":                 # same triple cleaning as candidates
                ids = np.concatenate([p1, p2])
                v, c = np.unique(ids, return_counts=True)
                multi = np.isin(p1, v[c > 1]) | np.isin(p2, v[c > 1])
                p1, p2, th = p1[~multi], p2[~multi], th[~multi]
            out[f"a{r}"], out[f"b{r}"], out[f"th{r}"] = p1, p2, th
            print(f"    realisation {r}: {m.sum():,d} chance pairs")
        return out
    E = cached(ext / f"stage_E{sfx}.npz", "E" in force, _e)

    print("[F] R_chance")
    def _f():
        m18 = sigma18_map(ext)
        sep_c = 1000 / S["parallax"][D["a"]] * D["th"]
        sel = sep_c < S_KDE_AU
        a, b, th = D["a"][sel], D["b"][sel], D["th"][sel]
        Xc = features(S, a, b, th, sigma18_at(S["ra"][a], S["dec"][a], m18))
        Xs = []
        for r in range(N_SHIFT):
            ea, eb, et = E[f"a{r}"], E[f"b{r}"], E[f"th{r}"]
            Xs.append(features(S, ea, eb, et, sigma18_at(S["ra"][ea], S["dec"][ea], m18)))
        R = r_chance(Xc, Xs)
        return {"a": a, "b": b, "th": th, "R": R, "Xc": Xc}
    F = cached(ext / f"stage_F{sfx}.npz", "F" in force, _f)
    print(f"    R computed for {len(F['a']):,d} pairs with s < {S_KDE_AU:.0f} au; "
          f"R < 0.01 for {(F['R'] < 0.01).sum():,d}")

    print("[G] frozen cuts")
    extra = {"third": np.zeros(len(F["a"]), bool)}
    pre, _, _ = frozen_cuts(S, F["a"], F["b"], F["R"], extra)   # every cut except the triple search
    idx = np.flatnonzero(pre)
    extra["third"][idx] = third_star_flags(S, F["a"][idx], F["b"][idx])
    # Banik eq. 10: sigma(vtilde) <= 0.1 max(1, vtilde/2), vtilde from the observables
    pre2, _, tab0 = frozen_cuts(S, F["a"], F["b"], F["R"], extra)
    idx2 = np.flatnonzero(pre2)
    corr = fetch_correlations(args.release,
                              np.concatenate([S["source_id"][F["a"][idx2]], S["source_id"][F["b"][idx2]]]),
                              ext / "stage_G_corr.npz")
    sig_vt = vt_error_mc(S, F["a"][idx2], F["b"][idx2], F["th"][idx2], corr)
    from wide_binary_pipeline import G as GN, MSUN, AU
    vc0 = np.sqrt(GN * (tab0["M1_msun"][idx2] + tab0["M2_msun"][idx2]) * MSUN
                  / (tab0["sep_kAU"][idx2] * 1e3 * AU)) / 1e3
    vt0 = tab0["v_perp_kms"][idx2] / vc0
    ok = np.zeros(len(F["a"]), bool)
    ok[idx2] = sig_vt <= 0.1 * np.maximum(1.0, vt0 / 2)
    extra["vt_err_ok"] = ok
    z = av_sfd98(S, ext / "AV_sfd98.npz")
    if z is not None:
        extra["AV_ok"] = (z["av"][F["a"]] < 0.5) & (z["av"][F["b"]] < 0.5)
    keepG, flow, table = frozen_cuts(S, F["a"], F["b"], F["R"], extra)
    report["cut_flow"] = flow
    report["not_applied"] = [c for c in ("A_V<0.5", "vtilde error")
                             if c not in [f[0] for f in flow]]
    for name, n in flow:
        print(f"    {name:32s} {n:>8,d}")
    if report["not_applied"]:
        print(f"    NOT APPLIED (inputs absent): {report['not_applied']}")
    out_csv = ext / f"wide_binaries_{args.release}{sfx}.csv"
    import csv
    cols = list(table)
    with open(out_csv, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(cols)
        for i in np.flatnonzero(keepG):
            w.writerow([table[c][i] for c in cols])
    report["n_final"] = int(keepG.sum())
    report["csv"] = str(out_csv.relative_to(REPO))
    report["chance_mode"] = CHANCE_MODE
    (HERE / f"build_report_{args.release}{sfx}.json").write_text(json.dumps(report, indent=2) + "\n")
    print(f"[done] {report['n_final']:,d} pairs -> {out_csv.name}")


if __name__ == "__main__":
    main()
