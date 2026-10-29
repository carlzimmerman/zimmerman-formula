#!/usr/bin/env python3
"""CFG438B POST-FREEZE DIAGNOSTIC: split-half invariance (DIAG_INVARIANCE_PLAN.md).

NOT part of any verdict. Usage:
    python3 cfg438b_diag_invariance.py prep SRC      # SRC = base (CFG438 cubes) or S; writes 4 split trees + mosaic DRFs
    (run_queue.sh <SRC>_<SPLIT>/q_mos_bx442 for SPLIT in N1 N2 HA HB)
    python3 cfg438b_diag_invariance.py run SRC       # I1-I5 -> cfg438b_diag_invariance_<SRC>.json
Uses CFG438's unchanged load/smooth/noise/fit_spec/tanh_pa.
"""
import importlib.util
import json
import os
import shutil
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
EXT = os.path.normpath(os.path.join(HERE, '..', '..', '..', '_external_data'))
OLD = os.path.join(EXT, 'cfg438_work')
WORK = os.path.join(EXT, 'cfg438b_work')
D438 = os.path.join(HERE, '..', 'CFG438_osiris_reduction')
SRCDIR = {'base': OLD, 'S': os.path.join(WORK, 'S')}
MOSAIC = """<?xml version="1.0" encoding="UTF-8"?>
<DRF LogPath="/work/logs" ReductionType="ARP_SPEC">
<dataset InputDir="/work/{tree}/cubes_bx442" OutputDir="/work/{tree}/mosaic_bx442">
{files}</dataset>
  <module Name="Mosaic Frames" Combine_Method="MEANCLIP" Offset_Method="TEL" />
  <module Name="Save DataSet Information" />
</DRF>
"""


def k438(work):
    spec = importlib.util.spec_from_file_location('k438_' + os.path.basename(work), os.path.join(D438, 'cfg438_kinematics.py'))
    k = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(k)
    k.WORK = work
    return k


def splits(src):
    cubes = sorted(f for f in os.listdir(os.path.join(SRCDIR[src], 'cubes_bx442')) if f.endswith('.fits'))
    assert len(cubes) == 40
    seqs = sorted({c[:12] for c in cubes})                 # sYYMMDD_aNNN, time order within each night
    assert len(seqs) == 20
    ha = set(seqs[0::2])
    return {'N1': [c for c in cubes if c.startswith('s110823')],
            'N2': [c for c in cubes if c.startswith('s110824')],
            'HA': [c for c in cubes if c[:12] in ha],
            'HB': [c for c in cubes if c[:12] not in ha]}


def prep(src):
    for name, cubes in splits(src).items():
        tree = '%s_%s' % (src, name)
        d = os.path.join(WORK, 'diag', tree)
        for s in ('cubes_bx442', 'q_mos_bx442', 'mosaic_bx442'):
            os.makedirs(os.path.join(d, s), exist_ok=True)
        sky = os.path.join(d, 'cubes_sky')
        if not os.path.exists(sky):
            os.symlink(os.path.join(OLD, 'cubes_sky'), sky)
        for c in cubes:
            shutil.copy(os.path.join(SRCDIR[src], 'cubes_bx442', c), os.path.join(d, 'cubes_bx442', c))
        with open(os.path.join(d, 'q_mos_bx442', '001.mosaic_bx442.waiting'), 'w') as fh:
            fh.write(MOSAIC.format(tree='diag/' + tree, files=''.join('<fits FileName="%s" />\n' % c for c in cubes)))
        print(tree, len(cubes))


def fit_all(work):
    """Every spaxel fitted exactly as cfg438_kinematics.run does, keyed by absolute sky position."""
    k = k438(work)
    fn, h, data, lam, cov = k.load('bx442')
    sm = k.smooth(data, 0.1)
    ny, nx, nl = sm.shape
    flat = sm.reshape(-1, nl)
    noise = 1.4826 * np.nanmedian(np.abs(flat - np.nanmedian(flat, axis=0)), axis=0)
    east, north = k.sky_offsets(h, (ny, nx))
    ra0, dec0 = h['CRVAL3'], h['CRVAL2']
    z = k.TARGETS['bx442']['z']
    res = {}
    for j in range(ny):
        for i in range(nx):
            s = sm[j, i]
            if np.isfinite(s).sum() < 0.8 * nl:
                continue
            r = k.fit_spec(lam, s, noise, z)
            if r is not None:
                # absolute offsets (arcsec) from a fixed sky point, comparable across mosaics
                E = east[j, i] + (ra0 - 356.5806) * np.cos(np.radians(12.7999)) * 3600.0
                N = north[j, i] + (dec0 - 12.7999) * 3600.0
                res[(j, i)] = dict(r, E=E, N=N)
    return k, data, lam, nl, res


def summed(k, data, lam, nl, idx, z):
    """Summed spectrum S/N and v over the given spaxels, noise as in cfg438_kinematics.run."""
    idx = np.array(idx)
    s = np.nansum(data[idx[:, 0], idx[:, 1], :], axis=0)
    rng = np.random.default_rng(438)
    allpix = np.argwhere(np.isfinite(data).sum(axis=2) > 0.8 * nl)
    sums = np.array([np.nansum(data[p[:, 0], p[:, 1], :], axis=0)
                     for p in (allpix[rng.choice(len(allpix), size=len(idx), replace=False)] for _ in range(200))])
    sn = 1.4826 * np.median(np.abs(sums - np.median(sums, axis=0)), axis=0)
    return k.fit_spec(lam, s, sn, z)


def match(ra, rb, tol=0.05):
    pb = np.array([[r['E'], r['N']] for r in rb.values()])
    kb = list(rb.keys())
    out = []
    for ka, a in ra.items():
        d = np.hypot(pb[:, 0] - a['E'], pb[:, 1] - a['N'])
        m = int(np.argmin(d))
        if d[m] < tol:
            out.append((ka, kb[m]))
    return out


def robust_std(x):
    x = np.asarray(x)
    return float(1.4826 * np.median(np.abs(x - np.median(x)))) if len(x) else float('nan')


def run(src):
    z = 2.1765
    full_work = SRCDIR[src]
    kf, dataf, lamf, nlf, rf = fit_all(full_work)
    base_pass = [tuple(p) for p in json.load(open(os.path.join(D438, 'cfg438_bx442_results.json')))['passing_spaxels']]
    if src == 'base':
        ref = [rf[p] for p in base_pass]
    else:
        ref = [r for r in rf.values() if r['sn'] >= 5 and not r['at_bound']]
    ok = lambda r, c: r['sn'] >= c and not r['at_bound']
    out = dict(src=src, n_full_pass5=sum(ok(r, 5) for r in rf.values()))
    sf = summed(kf, dataf, lamf, nlf, [p for p, r in rf.items() if any(abs(r['E'] - q['E']) < 0.05 and abs(r['N'] - q['N']) < 0.05 for q in ref)], z)
    out['full_summed'] = dict(sn=sf['sn'], v=sf['v'], verr=sf['verr'])
    halves = {}
    for name in ('N1', 'N2', 'HA', 'HB'):
        kh, datah, lamh, nlh, rh = fit_all(os.path.join(WORK, 'diag', '%s_%s' % (src, name)))
        sel = [p for p, r in rh.items() if any(abs(r['E'] - q['E']) < 0.05 and abs(r['N'] - q['N']) < 0.05 for q in ref)]
        sh = summed(kh, datah, lamh, nlh, sel, z)
        n = len(splits(src)[name])
        pas = {p: r for p, r in rh.items() if ok(r, 5)}
        pa = None
        if len(pas) >= 10:
            P = list(pas.values())
            F = np.array([r['flux'] for r in P]); E = np.array([r['E'] for r in P]); N = np.array([r['N'] for r in P])
            kin = kh.tanh_pa(E, N, np.array([r['v'] for r in P]), np.sqrt(np.array([r['verr'] for r in P]) ** 2 + 100.0),
                             np.sum(F * E) / F.sum(), np.sum(F * N) / F.sum())
            pa = dict(pa=kin['pa'], lo=kin['pa_lo'], hi=kin['pa_hi'])
        halves[name] = dict(res=rh, n_frames=n, n_pass5=len(pas), summed=dict(sn=sh['sn'], v=sh['v'], verr=sh['verr']),
                            sn_ratio_vs_full=sh['sn'] / sf['sn'], sn_ratio_white=np.sqrt(n / 40.0), pa=pa)
    for a, b in (('N1', 'N2'), ('HA', 'HB')):
        ra, rb = halves[a]['res'], halves[b]['res']
        pairs = [(x, y) for x, y in match(ra, rb) if ok(ra[x], 3) and ok(rb[y], 3)]
        pulls = {q: [(ra[x][q] - rb[y][q]) / np.hypot(ra[x][e], rb[y][e]) for x, y in pairs]
                 for q, e in (('v', 'verr'), ('sig', 'sigerr'), ('flux', 'ferr'))}
        dv = [halves[a]['summed']['v'] - halves[b]['summed']['v'],
              np.hypot(halves[a]['summed']['verr'], halves[b]['summed']['verr'])]
        out['I1_' + a + b] = dict(n_matched=len(pairs), **{'pull_rstd_' + q: robust_std(p) for q, p in pulls.items()},
                                  **{'pull_std_' + q: float(np.std(p)) if p else None for q, p in pulls.items()})
        out['I3_' + a + b] = dict(v_a=halves[a]['summed']['v'], v_b=halves[b]['summed']['v'], dv=dv[0], dv_err=dv[1])
    out['I2'] = {n: dict(sn=h['summed']['sn'], ratio=h['sn_ratio_vs_full'], white=h['sn_ratio_white']) for n, h in halves.items()}
    out['I4'] = dict(threshold=5 / np.sqrt(52 / 40.0), n_forecast_52=sum(ok(r, 5 / np.sqrt(52 / 40.0)) for r in rf.values()),
                     n_now=out['n_full_pass5'],
                     half_counts={n: h['n_pass5'] for n, h in halves.items()},
                     half_counts_white_forecast={n: sum(ok(r, 5 * np.sqrt(40.0 / h['n_frames'])) for r in rf.values())
                                                 for n, h in halves.items()})
    out['I5'] = {n: h['pa'] for n, h in halves.items()}
    json.dump(out, open(os.path.join(HERE, 'cfg438b_diag_invariance_%s.json' % src), 'w'), indent=1, default=float)
    print(json.dumps(out, indent=1, default=float))


if __name__ == '__main__':
    {'prep': prep, 'run': run}[sys.argv[1]](sys.argv[2])
