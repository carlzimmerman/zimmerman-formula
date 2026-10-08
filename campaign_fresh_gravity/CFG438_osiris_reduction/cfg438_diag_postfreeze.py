#!/usr/bin/env python3
"""CFG438 POST-FREEZE DIAGNOSTIC (not part of the frozen verdict).

After the frozen BX442 run returned only 27 spaxels at S/N >= 5, this asks
two questions with everything else held at the frozen settings:
  D1. Where is the H-alpha emission and what is the integrated systemic
      velocity? (summed spectrum over all fitted spaxels with S/N >= 3 inside
      a 1.0" radius of their flux-weighted centre)
  D2. With the S/N cut relaxed to 3 (Law+12 used a visual cut of about S/N 3),
      what kinematic PA, velocity range and sigma_m does the same machinery give?
Outputs: cfg438_bx442_DIAG_postfreeze.json, cfg438_bx442_DIAG_maps.png
"""
import importlib.util
import json
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('k', os.path.join(HERE, 'cfg438_kinematics.py'))
k = importlib.util.module_from_spec(spec)
spec.loader.exec_module(k)


def main():
    z = k.TARGETS['bx442']['z']
    fn, h, data, lam, cov = k.load('bx442')
    sm = k.smooth(data, 0.1)
    ny, nx, nl = sm.shape
    flat = sm.reshape(-1, nl)
    noise = 1.4826 * np.nanmedian(np.abs(flat - np.nanmedian(flat, axis=0)), axis=0)
    east, north = k.sky_offsets(h, (ny, nx))
    sinst = k.sigma_inst()[0]
    res = {}
    for j in range(ny):
        for i in range(nx):
            s = sm[j, i]
            if np.isfinite(s).sum() < 0.8 * nl:
                continue
            r = k.fit_spec(lam, s, noise, z)
            if r is not None and not r['at_bound']:
                res[(j, i)] = r
    out = {'note': 'POST-FREEZE DIAGNOSTIC; not used for the frozen verdict'}
    for cut in (5, 4, 3):
        p = {kk: r for kk, r in res.items() if r['sn'] >= cut}
        out['n_pass_sn%d' % cut] = len(p)
    p = {kk: r for kk, r in res.items() if r['sn'] >= 3}
    keys = list(p)
    J = np.array([a[0] for a in keys]); I = np.array([a[1] for a in keys])
    F = np.array([p[a]['flux'] for a in keys]); V = np.array([p[a]['v'] for a in keys])
    Ve = np.array([p[a]['verr'] for a in keys]); S = np.array([p[a]['sig'] for a in keys])
    E, N = east[J, I], north[J, I]
    x0, y0 = np.sum(F * E) / F.sum(), np.sum(F * N) / F.sum()
    # keep the main body: within 1.0" of the flux-weighted centre
    m = np.hypot(E - x0, N - y0) <= 1.0
    out['n_sn3_within_1arcsec'] = int(m.sum())
    x0, y0 = np.sum(F[m] * E[m]) / F[m].sum(), np.sum(F[m] * N[m]) / F[m].sum()
    # D1 summed spectrum
    summed = np.nansum(data[J[m], I[m], :], axis=0)
    rng = np.random.default_rng(438)
    allpix = np.argwhere(np.isfinite(data).sum(axis=2) > 0.8 * nl)
    sums = np.array([np.nansum(data[q[:, 0], q[:, 1], :], axis=0)
                     for q in (allpix[rng.choice(len(allpix), m.sum(), replace=False)] for _ in range(200))])
    snoise = 1.4826 * np.median(np.abs(sums - np.median(sums, axis=0)), axis=0)
    rs = k.fit_spec(lam, summed, snoise, z)
    out['D1_summed'] = {a: (float(b) if not isinstance(b, bool) else b) for a, b in rs.items()}
    # D2 kinematics at S/N >= 3 within 1"
    kin = k.tanh_pa(E[m], N[m], V[m], np.sqrt(Ve[m] ** 2 + 100.0), x0, y0)
    Sint = np.sqrt(np.clip(S[m] ** 2 - sinst ** 2, 0, None))
    dpa = min(abs(((kin['pa'] - 168) + 180) % 360 - 180), abs(((kin['pa'] - 348) + 180) % 360 - 180))
    out['D2'] = dict(kin=kin, dpa_vs_168=dpa, v_p5_p95=[float(np.percentile(V[m] - kin['vsys'], 5)),
                                                         float(np.percentile(V[m] - kin['vsys'], 95))],
                     sigma_m=float(np.sum(F[m] * Sint) / F[m].sum()), sigma_median=float(np.median(Sint)),
                     centre_EN=[float(x0), float(y0)])
    json.dump(out, open(os.path.join(HERE, 'cfg438_bx442_DIAG_postfreeze.json'), 'w'), indent=1, default=float)

    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    vmap = np.full((ny, nx), np.nan); fmap = np.full((ny, nx), np.nan); smap = np.full((ny, nx), np.nan)
    for q, (j, i) in enumerate(np.array(keys)[m]):
        vmap[j, i] = V[m][q] - kin['vsys']; fmap[j, i] = F[m][q]; smap[j, i] = Sint[q]
    fig, ax = plt.subplots(1, 4, figsize=(17, 4.4))
    for a, mm, lab, cm in ((ax[0], fmap, 'H-alpha flux', 'viridis'), (ax[1], vmap, 'v (km/s)', 'RdBu_r'),
                           (ax[2], smap, 'sigma_int (km/s)', 'magma')):
        kw = dict(vmin=-200, vmax=200) if cm == 'RdBu_r' else {}
        pc = a.pcolormesh(east, north, mm, cmap=cm, shading='nearest', **kw)
        a.set_xlim(x0 + 1.5, x0 - 1.5); a.set_ylim(y0 - 1.5, y0 + 1.5); a.set_aspect('equal')
        a.set_xlabel('East (arcsec)'); a.set_ylabel('North (arcsec)'); plt.colorbar(pc, ax=a, label=lab)
        for pa, ls in ((kin['pa'], 'k--'), (168, 'g:')):
            t = np.radians(pa)
            a.plot([x0 - 1.4 * np.sin(t), x0 + 1.4 * np.sin(t)], [y0 - 1.4 * np.cos(t), y0 + 1.4 * np.cos(t)], ls, lw=1)
    ax[0].set_title('BX442 S/N>=3 (POST-FREEZE diag)  PA=%d (dashed), Law 168 (dotted)' % kin['pa'], fontsize=8)
    ll = lam / (1 + z)
    w = (ll > 6500) & (ll < 6640)
    ax[3].step(ll[w], summed[w], where='mid', lw=0.8, label='summed (S/N>=3, r<1")')
    ax[3].fill_between(ll[w], -snoise[w], snoise[w], color='gray', alpha=0.3, step='mid', label='1-sigma noise')
    ax[3].axvline(6564.61, color='r', lw=0.5); ax[3].set_xlabel('rest wavelength at z=2.1765 (A)'); ax[3].legend(fontsize=7)
    fig.tight_layout(); fig.savefig(os.path.join(HERE, 'cfg438_bx442_DIAG_maps.png'), dpi=90)
    print(json.dumps(out, indent=1, default=float))




def rerun_full_at_sn3():
    """D3: the full frozen pipeline (PA, slit V(R), sigma(R), V1-V4 arithmetic) at S/N >= 3."""
    k.SN_CUT = 3
    k.MODE_TAG = '_DIAG_SN3'
    o = k.run('bx442', False)
    return o


if __name__ == '__main__':
    main()
    o = rerun_full_at_sn3()
    print(json.dumps({a: b for a, b in o.items() if a not in ('passing_spaxels', 'oh_lines')}, indent=1, default=float))
