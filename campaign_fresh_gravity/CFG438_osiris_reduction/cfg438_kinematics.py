#!/usr/bin/env python3
"""CFG438: H-alpha kinematics from our own OSIRIS DRP (GDL) mosaics.

Implements FROZEN_CRITERIA.md exactly. Usage:
    python3 cfg438_kinematics.py bx442            # true redshift, validation
    python3 cfg438_kinematics.py bx442 --mutate   # wrong redshift z=2.200
    python3 cfg438_kinematics.py a1689            # descriptive only
Inputs are read from ../_external_data/cfg438_work (outside git). Outputs are
written next to this script with the mode in the name.
"""
import argparse
import json
import os

import numpy as np
from astropy.cosmology import FlatLambdaCDM
from astropy.io import fits
from astropy.wcs import WCS
from scipy.ndimage import gaussian_filter
from scipy.optimize import curve_fit

HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.normpath(os.path.join(HERE, '..', '..', '..', '_external_data', 'cfg438_work'))
C = 299792.458
HA, N2R, N2B = 6564.61, 6585.27, 6549.86     # vacuum rest wavelengths (A)
COSMO = FlatLambdaCDM(H0=70.4, Om0=0.272)
# Frozen values. The post-freeze diagnostic (cfg438_diag_postfreeze.py) overrides them
# (SN_CUT=3, MODE_TAG='_DIAG_SN3'); the frozen verdict uses only these defaults.
SN_CUT = 5
MODE_TAG = ''

TARGETS = {
    'bx442': dict(cube='mosaic_bx442', z=2.1765, z_mutate=2.200, slit=3, scale=0.100),
    'a1689': dict(cube='mosaic_a1689', z=2.540, z_mutate=None, slit=5, scale=0.050),
}
LAW = dict(pa=168.0, vc=234.0, vc_hi=49.0, vc_lo=29.0, R=8.0, incl=42.0, incl_err=10.0,
           sig_m=66.0, sig_m_err=6.0, sig_z=71.0)


def rel(p):
    return os.path.relpath(p, os.path.join(HERE, '..', '..'))


def find_mosaic(name):
    d = os.path.join(WORK, name)
    fs = sorted(f for f in os.listdir(d) if f.endswith('.fits'))
    assert len(fs) == 1, fs
    return os.path.join(d, fs[0])


def load(target):
    fn = find_mosaic(TARGETS[target]['cube'])
    hdul = fits.open(fn)
    h = hdul[0].header
    data = hdul[0].data.astype(float)          # (axis3, axis2, wave)
    qual = hdul[2].data
    lam = (h['CRVAL1'] + (np.arange(data.shape[2]) + 1 - h['CRPIX1']) * h['CDELT1']) * 10.0  # A
    good = qual > 0
    data[~good] = np.nan
    cov = coverage(target, data.shape)
    mask = cov < 0.75 * cov.max()
    data[mask] = np.nan
    return fn, h, data, lam, cov


def coverage(target, shape):
    """Number of input cubes covering each mosaic spaxel.

    The DRP mosaic (mosaic_000) places each cube at integer offsets
    round(shift) - min(round(shift)) and does not save a frame-count map, so
    it is rebuilt here from the shifts the DRP printed in its log
    ('Found shifts to be') and each input cube's quality extension.
    """
    q = os.path.join(WORK, 'q_mos_' + target)
    drf = [f for f in os.listdir(q) if f.endswith('.done')][0]
    files = [l.split('"')[1] for l in open(os.path.join(q, drf)) if '<fits FileName' in l]
    log = open(os.path.join(q, 'run.log')).read().splitlines()
    end = [k for k, l in enumerate(log) if l.startswith('Pointing center')][0]
    num = []
    for l in log[:end]:
        t = l.split()
        try:
            if len(t) == 2:
                num.append([float(t[0]), float(t[1])])
        except ValueError:
            pass
    pairs = num[-len(files):]
    sx = np.round([p[0] for p in pairs]).astype(int)
    sy = np.round([p[1] for p in pairs]).astype(int)
    cov = np.zeros(shape[:2])
    for f, x, y in zip(files, sx, sy):
        qa = fits.open(os.path.join(WORK, 'cubes_' + target, f))[2].data   # (axis3, axis2, wave)
        good = (qa > 0).mean(axis=2) > 0.5
        ix, iy = x - sx.min(), y - sy.min()
        # IDL order cube(wave, x=axis2, y=axis3): x shift -> numpy axis 1, y shift -> numpy axis 0
        cov[iy:iy + good.shape[0], ix:ix + good.shape[1]] += good
    return cov


def sky_offsets(h, shape):
    """East and North offsets (arcsec) of every spaxel from the reference pixel, from the DRP WCS."""
    w = WCS(h).celestial  # axes 2 (DEC) and 3 (RA)
    j3, j2 = np.mgrid[0:shape[0], 0:shape[1]]
    world = w.wcs_pix2world(np.stack([j2.ravel(), j3.ravel()], 1), 0)
    # celestial axes come out in the header order: axis2 = DEC, axis3 = RA
    dec = world[:, 0].reshape(shape)
    ra = world[:, 1].reshape(shape)
    ra0, dec0 = h['CRVAL3'], h['CRVAL2']
    east = (ra - ra0) * np.cos(np.radians(dec0)) * 3600.0
    north = (dec - dec0) * 3600.0
    return east, north


def smooth(data, scale):
    sig = 0.16 / 2.355 / scale
    out = np.empty_like(data)
    for k in range(data.shape[2]):
        im = data[:, :, k]
        m = np.isfinite(im)
        a = gaussian_filter(np.where(m, im, 0.0), sig)
        b = gaussian_filter(m.astype(float), sig)
        with np.errstate(invalid='ignore', divide='ignore'):
            out[:, :, k] = np.where(m & (b > 0.3), a / b, np.nan)
    return out


def model(lam, z, cont, aha, an2, v, sig):
    out = np.full_like(lam, cont)
    for lr, amp in ((HA, aha), (N2R, an2), (N2B, an2 / 2.95)):
        lc = lr * (1 + z) * (1 + v / C)
        s = lc * sig / C
        out = out + amp * np.exp(-0.5 * ((lam - lc) / s) ** 2)
    return out


def fit_spec(lam, spec, noise, z):
    lo, hi = 6530 * (1 + z), 6610 * (1 + z)
    m = (lam >= lo) & (lam <= hi) & np.isfinite(spec) & np.isfinite(noise) & (noise > 0)
    if m.sum() < 20:
        return None
    x, y, e = lam[m], spec[m], noise[m]
    f = lambda xx, cont, aha, an2, v, sig: model(xx, z, cont, aha, an2, v, sig)
    best = None
    for v0 in (-250.0, 0.0, 250.0):
        p0 = [np.median(y), max(np.nanmax(y) - np.median(y), 1e-6), 0.0, v0, 80.0]
        try:
            p, cov = curve_fit(f, x, y, p0=p0, sigma=e, absolute_sigma=True,
                               bounds=([-np.inf, 0, 0, -500, 15], [np.inf, np.inf, np.inf, 500, 300]),
                               maxfev=4000)
        except Exception:
            continue
        chi2 = np.sum(((y - f(x, *p)) / e) ** 2)
        if best is None or chi2 < best[2]:
            best = (p, cov, chi2)
    if best is None:
        return None
    p, cov, chi2 = best
    if not np.all(np.isfinite(cov)):
        return None
    # integrated H-alpha flux and its error (amp * sigma_lambda * sqrt(2 pi))
    lc = HA * (1 + z) * (1 + p[3] / C)
    sl = lc * p[4] / C
    flux = p[1] * sl * np.sqrt(2 * np.pi)
    # error propagation on (amp, sig)
    dfa = sl * np.sqrt(2 * np.pi)
    dfs = p[1] * lc / C * np.sqrt(2 * np.pi)
    var = dfa ** 2 * cov[1, 1] + dfs ** 2 * cov[4, 4] + 2 * dfa * dfs * cov[1, 4]
    ferr = np.sqrt(var) if var > 0 else np.inf
    at_bound = (abs(p[3]) > 499) or (p[4] < 15.5) or (p[4] > 299)
    return dict(flux=flux, ferr=ferr, sn=flux / ferr if ferr > 0 else 0.0, v=p[3], verr=np.sqrt(cov[3, 3]),
                sig=p[4], sigerr=np.sqrt(cov[4, 4]), n2=p[2], aha=p[1], at_bound=bool(at_bound),
                chi2r=chi2 / max(m.sum() - 5, 1))


def sigma_inst():
    """Median Gaussian sigma (km/s) of isolated OH lines in the unsubtracted DRP sky cube."""
    d = os.path.join(WORK, 'cubes_sky')
    fs = [f for f in os.listdir(d) if f.endswith('.fits')] if os.path.isdir(d) else []
    if not fs:
        return 3e5 / (2.355 * 3100), 'fallback R=3100 (no sky cube)', []
    hd = fits.open(os.path.join(d, fs[0]))
    h = hd[0].header
    cube = hd[0].data.astype(float)
    q = hd[2].data
    cube[q == 0] = np.nan
    lam = (h['CRVAL1'] + (np.arange(cube.shape[2]) + 1 - h['CRPIX1']) * h['CDELT1']) * 10.0
    spec = np.nanmedian(cube.reshape(-1, cube.shape[2]), axis=0)
    from scipy.ndimage import median_filter
    basel = median_filter(spec, size=31, mode='nearest')
    rms = 1.4826 * np.nanmedian(np.abs(spec - basel))
    peaks = [i for i in range(6, len(spec) - 6)
             if spec[i] == np.nanmax(spec[i - 4:i + 5]) and spec[i] - basel[i] > 10 * rms]
    sigs = []
    for i in peaks:
        # isolation: no other peak within 8 channels
        if any(abs(i - j) < 8 and j != i for j in peaks):
            continue
        x = lam[i - 6:i + 7]
        y = spec[i - 6:i + 7]
        try:
            p, _ = curve_fit(lambda xx, a, mu, s, c: a * np.exp(-0.5 * ((xx - mu) / s) ** 2) + c,
                             x, y, p0=[y.max() - basel[i], lam[i], 2.0, basel[i]])
        except Exception:
            continue
        s_kms = abs(p[2]) / p[1] * C
        if 10 < s_kms < 200:
            sigs.append((float(p[1]), float(s_kms)))
    if len(sigs) >= 5:
        return float(np.median([s for _, s in sigs])), 'OH lines (%d) in DRP sky cube' % len(sigs), sigs
    return 3e5 / (2.355 * 3100), 'fallback R=3100 (only %d isolated OH lines)' % len(sigs), sigs


def tanh_pa(east, north, v, verr, x0, y0):
    dx, dy = east - x0, north - y0
    best = []
    for pa in range(360):
        t = np.radians(pa)
        d = dx * np.sin(t) + dy * np.cos(t)    # distance along PA (E of N), positive toward PA
        f = lambda dd, vs, vt, rt: vs + vt * np.tanh(dd / rt)
        try:
            p, _ = curve_fit(f, d, v, p0=[0, 100, 0.3], sigma=verr,
                             bounds=([-500, 0, 0.02], [500, 1000, 5]), maxfev=4000)
            chi2 = np.sum(((v - f(d, *p)) / verr) ** 2)
        except Exception:
            p, chi2 = [np.nan] * 3, np.inf
        best.append((chi2, pa, p))
    chis = np.array([b[0] for b in best])
    i = int(np.argmin(chis))
    dof = max(len(v) - 4, 1)
    resc = chis / (chis[i] / dof)
    ok = np.where(resc - resc[i] <= 1.0)[0]
    # 1-sigma range as the circular extent around the best PA
    offs = ((ok - i + 180) % 360) - 180
    return dict(pa=best[i][1], pa_lo=best[i][1] + int(offs.min()), pa_hi=best[i][1] + int(offs.max()),
                vsys=float(best[i][2][0]), vt=float(best[i][2][1]), rt=float(best[i][2][2]),
                chi2r=float(chis[i] / dof))


def run(target, mutate):
    cfg = TARGETS[target]
    z = cfg['z_mutate'] if mutate else cfg['z']
    mode = target + ('_MUTATE' if mutate else '') + MODE_TAG
    fn, h, data, lam, cov = load(target)
    sm = smooth(data, cfg['scale'])
    ny, nx, nl = sm.shape
    flat = sm.reshape(-1, nl)
    noise = 1.4826 * np.nanmedian(np.abs(flat - np.nanmedian(flat, axis=0)), axis=0)
    east, north = sky_offsets(h, (ny, nx))
    sinst, sinst_src, ohl = sigma_inst()

    res = {}
    for j in range(ny):
        for i in range(nx):
            s = sm[j, i]
            if np.isfinite(s).sum() < 0.8 * nl:
                continue
            r = fit_spec(lam, s, noise, z)
            if r is not None:
                res[(j, i)] = r
    passing = {k: r for k, r in res.items() if r['sn'] >= SN_CUT and not r['at_bound']}
    out = dict(target=target, mode=mode, z_fit=z, mosaic=rel(fn), n_fitted=len(res),
               n_pass=len(passing), sigma_inst_kms=sinst, sigma_inst_source=sinst_src,
               oh_lines=ohl, smoothing_fwhm_arcsec=0.16)

    # summed spectrum of passing spaxels (or of the true-z passing set for MUTATE)
    sel = passing
    if mutate:
        tz = os.path.join(HERE, 'cfg438_%s_results.json' % target)
        if os.path.exists(tz):
            sel = {tuple(k): None for k in json.load(open(tz))['passing_spaxels']}
    if sel:
        idx = np.array(list(sel.keys()))
        summed = np.nansum(data[idx[:, 0], idx[:, 1], :], axis=0)
        # noise of the sum from the per-channel MAD over random equal-size spaxel sets
        rng = np.random.default_rng(438)
        allpix = np.argwhere(np.isfinite(data).sum(axis=2) > 0.8 * nl)
        sums = []
        for _ in range(200):
            pick = allpix[rng.choice(len(allpix), size=len(idx), replace=False)]
            sums.append(np.nansum(data[pick[:, 0], pick[:, 1], :], axis=0))
        sums = np.array(sums)
        snoise = 1.4826 * np.median(np.abs(sums - np.median(sums, axis=0)), axis=0)
        rs = fit_spec(lam, summed, snoise, z)
        out['summed'] = None if rs is None else {k: (float(v) if not isinstance(v, bool) else v) for k, v in rs.items()}
        out['summed_nspax'] = len(idx)
        np.savetxt(os.path.join(HERE, 'cfg438_%s_summed_spectrum.txt' % mode),
                   np.c_[lam, summed, snoise], header='lambda_A summed_flux noise', fmt='%.6g')

    if mutate or len(passing) < 10:
        json.dump(out, open(os.path.join(HERE, 'cfg438_%s_results.json' % mode), 'w'), indent=1, default=float)
        return out

    keys = list(passing.keys())
    J = np.array([k[0] for k in keys]); I = np.array([k[1] for k in keys])
    F = np.array([passing[k]['flux'] for k in keys])
    V = np.array([passing[k]['v'] for k in keys]); Ve = np.array([passing[k]['verr'] for k in keys])
    S = np.array([passing[k]['sig'] for k in keys]); Se = np.array([passing[k]['sigerr'] for k in keys])
    Sint = np.sqrt(np.clip(S ** 2 - sinst ** 2, 0, None))
    E, N = east[J, I], north[J, I]
    x0, y0 = np.sum(F * E) / F.sum(), np.sum(F * N) / F.sum()
    Ve_fit = np.sqrt(Ve ** 2 + 10.0 ** 2)   # 10 km/s floor for the PA fit
    kin = tanh_pa(E, N, V, Ve_fit, x0, y0)
    V = V - kin['vsys']

    # pseudo-slit V(R), sigma(R)
    t = np.radians(kin['pa'])
    dx, dy = east - x0, north - y0
    along = dx * np.sin(t) + dy * np.cos(t)
    perp = dx * np.cos(t) - dy * np.sin(t)
    halfw = cfg['slit'] * cfg['scale'] / 2.0
    kpc_as = COSMO.kpc_proper_per_arcmin(cfg['z']).value / 60.0
    rows = []
    vmap = np.full((ny, nx), np.nan); smap = np.full((ny, nx), np.nan); fmap = np.full((ny, nx), np.nan)
    vemap = np.full((ny, nx), np.nan); semap = np.full((ny, nx), np.nan)
    for k, (j, i) in enumerate(keys):
        vmap[j, i] = V[k]; smap[j, i] = Sint[k]; fmap[j, i] = F[k]; vemap[j, i] = Ve[k]
        semap[j, i] = Se[k] * S[k] / max(Sint[k], 1e-3)
    edges = np.arange(-3.0, 3.0001, 0.1)
    for a, b in zip(edges[:-1], edges[1:]):
        m = np.isfinite(vmap) & (np.abs(perp) <= halfw) & (along >= a) & (along < b)
        if m.sum() == 0:
            continue
        w = 1.0 / vemap[m] ** 2
        vv = np.sum(w * vmap[m]) / w.sum(); ve = 1 / np.sqrt(w.sum())
        ws = 1.0 / np.clip(semap[m], 1, None) ** 2
        ss = np.sum(ws * smap[m]) / ws.sum(); se = 1 / np.sqrt(ws.sum())
        rows.append(((a + b) / 2, int(m.sum()), vv, ve, ss, se))
    rows = np.array(rows)
    np.savetxt(os.path.join(HERE, 'cfg438_%s_slit_profile.txt' % mode), rows,
               header='r_arcsec(signed, + toward PA) n_spax v_kms v_err sigma_int_kms sigma_err', fmt='%.4f')
    fold = []
    for r in np.unique(np.round(np.abs(rows[:, 0]), 3)):
        p = rows[np.isclose(rows[:, 0], r)]; q = rows[np.isclose(rows[:, 0], -r)]
        if len(p) and len(q):
            vf = (p[0, 2] - q[0, 2]) / 2; vfe = 0.5 * np.hypot(p[0, 3], q[0, 3])
            sf = (p[0, 4] + q[0, 4]) / 2; sfe = 0.5 * np.hypot(p[0, 5], q[0, 5])
            fold.append((r, r * kpc_as, vf, vfe, sf, sfe))
    fold = np.array(fold) if fold else np.zeros((0, 6))
    sini = np.sin(np.radians(LAW['incl']))
    if target == 'bx442' and len(fold):
        fold_dep = np.c_[fold, fold[:, 2] / sini, fold[:, 3] / sini]
    else:
        fold_dep = np.c_[fold, np.full(len(fold), np.nan), np.full(len(fold), np.nan)]
    np.savetxt(os.path.join(HERE, 'cfg438_%s_VR_sigmaR.txt' % mode), fold_dep,
               header='R_arcsec R_kpc Vproj_fold Vproj_err sigma_int sigma_err Vdeproj(i=42) Vdeproj_err',
               fmt='%.4f')

    # flux-weighted mean intrinsic sigma + bootstrap
    rng = np.random.default_rng(438)
    sig_m = float(np.sum(F * Sint) / F.sum())
    boots = []
    for _ in range(1000):
        b = rng.integers(0, len(F), len(F))
        boots.append(np.sum(F[b] * Sint[b]) / F[b].sum())
    sig_m_err = float(np.std(boots))

    out.update(dict(passing_spaxels=[list(map(int, k)) for k in keys], centre_EN_arcsec=[float(x0), float(y0)],
                    kin=kin, kpc_per_arcsec=kpc_as, sigma_m_flux_weighted=sig_m, sigma_m_err=sig_m_err,
                    sigma_median=float(np.median(Sint)), v_range_obs=[float(np.percentile(V, 5)), float(np.percentile(V, 95))],
                    fold=fold_dep.tolist()))

    if target == 'bx442':
        val = {}
        rs = out.get('summed') or {}
        val['V1'] = dict(n_pass=len(passing), summed_sn=rs.get('sn'), summed_v=rs.get('v'),
                         verdict='PASS' if (len(passing) >= 30 and rs and rs['sn'] >= 10 and abs(rs['v']) <= 300) else 'FAIL')
        dpa = min(abs(((kin['pa'] - LAW['pa']) + 180) % 360 - 180), abs(((kin['pa'] - LAW['pa'] - 180) + 180) % 360 - 180))
        val['V2'] = dict(pa=kin['pa'], pa_1sig=[kin['pa_lo'], kin['pa_hi']], dpa_vs_168=dpa,
                         verdict='PASS' if dpa <= 20 else 'FAIL')
        if len(fold_dep):
            sel6 = fold_dep[fold_dep[:, 1] >= 6.0]
            row = sel6[-1] if len(sel6) else fold_dep[-1]
            vme, vmerr = row[6], row[7]
            pub = LAW['vc_hi'] if vme > LAW['vc'] else LAW['vc_lo']
            tol = np.hypot(pub, vmerr)
            d = abs(vme - LAW['vc'])
            val['V3'] = dict(R_kpc=row[1], R_arcsec=row[0], V_deproj=vme, V_err=vmerr, V_proj=row[2],
                             reached_6kpc=bool(len(sel6)), diff=d, tol_1x=tol,
                             verdict='PASS' if d <= tol else ('MARGINAL' if d <= 2 * tol else 'FAIL'))
            vmax_row = fold_dep[np.nanargmax(fold_dep[:, 6])]
            val['V3']['max_deproj_any_R'] = dict(R_kpc=vmax_row[1], V=vmax_row[6], err=vmax_row[7])
        tol4 = np.hypot(LAW['sig_m_err'], sig_m_err)
        d4 = abs(sig_m - LAW['sig_m'])
        val['V4'] = dict(sigma_m=sig_m, err=sig_m_err, diff=d4, tol_1x=tol4, sigma_z_pub=LAW['sig_z'],
                         verdict='PASS' if d4 <= tol4 else ('MARGINAL' if d4 <= 2 * tol4 else 'FAIL'))
        vs = [val[k]['verdict'] for k in ('V1', 'V2', 'V3', 'V4') if k in val]
        if all(v == 'PASS' for v in vs) and len(vs) == 4:
            lane = 'VALIDATED'
        elif val['V1']['verdict'] == 'PASS' and sum(v == 'FAIL' for v in vs) <= 1:
            lane = 'PARTIAL'
        else:
            lane = 'NOT VALIDATED'
        val['lane'] = lane
        out['validation'] = val

    json.dump(out, open(os.path.join(HERE, 'cfg438_%s_results.json' % mode), 'w'), indent=1, default=float)
    plot(mode, east, north, fmap, vmap, smap, x0, y0, kin, rows, fold_dep, cfg, target)
    return out


def plot(mode, east, north, fmap, vmap, smap, x0, y0, kin, rows, fold, cfg, target):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(1, 4, figsize=(17, 4.6))
    ext_e, ext_n = east, north
    for a, m, lab, cmap in ((ax[0], fmap, 'H-alpha flux (DRP units)', 'viridis'),
                            (ax[1], vmap, 'v (km/s)', 'RdBu_r'),
                            (ax[2], smap, 'sigma_int (km/s)', 'magma')):
        kw = {}
        if cmap == 'RdBu_r':
            lim = np.nanpercentile(np.abs(m), 95)
            kw = dict(vmin=-lim, vmax=lim)
        pc = a.pcolormesh(ext_e, ext_n, m, cmap=cmap, shading='nearest', **kw)
        a.set_xlim(x0 + 1.6, x0 - 1.6); a.set_ylim(y0 - 1.6, y0 + 1.6); a.set_aspect('equal')
        a.set_xlabel('East offset (arcsec)'); a.set_ylabel('North offset (arcsec)')
        plt.colorbar(pc, ax=a, label=lab)
        t = np.radians(kin['pa'])
        a.plot([x0 - 1.5 * np.sin(t), x0 + 1.5 * np.sin(t)], [y0 - 1.5 * np.cos(t), y0 + 1.5 * np.cos(t)], 'k--', lw=1)
    ax[0].set_title('%s  PA=%d deg' % (target.upper(), kin['pa']))
    a = ax[3]
    if len(rows):
        a.errorbar(rows[:, 0], rows[:, 2], rows[:, 3], fmt='o', ms=3, label='v (slit, projected)')
        a.errorbar(rows[:, 0], rows[:, 4], rows[:, 5], fmt='s', ms=3, label='sigma_int')
    if target == 'bx442':
        sini = np.sin(np.radians(LAW['incl']))
        a.axhline(LAW['vc'] * sini, color='gray', ls=':', label='Law+12 234 sin42')
        a.axhline(-LAW['vc'] * sini, color='gray', ls=':')
        a.axhline(LAW['sig_m'], color='C1', ls=':', label='Law+12 sigma_m 66')
    a.axhline(0, color='k', lw=0.5)
    a.set_ylim(-400, 400)
    a.set_xlabel('distance along PA (arcsec)'); a.set_ylabel('km/s'); a.legend(fontsize=7)
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, 'cfg438_%s_maps.png' % mode), dpi=90)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('target', choices=list(TARGETS))
    ap.add_argument('--mutate', action='store_true')
    a = ap.parse_args()
    o = run(a.target, a.mutate)
    print(json.dumps({k: v for k, v in o.items() if k not in ('passing_spaxels', 'fold', 'oh_lines')}, indent=1, default=float))
