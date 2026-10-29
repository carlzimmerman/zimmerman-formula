#!/usr/bin/env python3
"""CFG438B: BX442 cubes with Law+12's scaled AB differencing (S), super-dark and
per-frame telluric (T). Implements FROZEN_CRITERIA.md. Steps, in order:

    python3 cfg438b_build.py drfs          # DRP queues: super-dark, 40 science, 8 standards
    (run_queue.sh q_dark; then python3 cfg438b_build.py drfs --sci; run q_sci, q_std)
    python3 cfg438b_build.py diff          # S cubes: A - s(lambda) B
    python3 cfg438b_build.py tell [TEFF]   # telluric curves; T and ST cubes
    python3 cfg438b_build.py mosaic MODE   # mosaic DRF for MODE in S, T, ST (run it with run_queue.sh)
    python3 cfg438b_build.py grade MODE    # CFG438's frozen extraction, unchanged, on MODE's mosaic

Work tree (outside git): ../_external_data/cfg438b_work/. Each MODE gets its own
sub-tree laid out like cfg438_work (cubes_bx442, q_mos_bx442, mosaic_bx442,
cubes_sky -> CFG438's sky cube), so cfg438_kinematics.py runs on it unchanged.
"""
import glob
import importlib.util
import json
import os
import shutil
import sys

import numpy as np
from astropy.io import fits

HERE = os.path.dirname(os.path.abspath(__file__))
EXT = os.path.normpath(os.path.join(HERE, '..', '..', '..', '_external_data'))
RAW = os.path.join(EXT, 'cfg437_work', 'raw')
OLD = os.path.join(EXT, 'cfg438_work')
WORK = os.path.join(EXT, 'cfg438b_work')
K438 = os.path.join(HERE, '..', 'CFG438_osiris_reduction', 'cfg438_kinematics.py')
RECMAT = '/work/calib/s100714_c006___infl_Kn2_100.fits'
DARKS = ['OS.20110823.08047.fits', 'OS.20110823.10686.fits', 'OS.20110823.11624.fits',
         'OS.20110823.12562.fits', 'OS.20110823.13501.fits']
SUPERDARK = 'superdark_900s.fits'
HA_WIN = (20743.0, 20997.0)        # rest 6530-6610 A at z = 2.1765 (frozen validity window)
H, KB, CL = 6.62607015e-34, 1.380649e-23, 2.99792458e8

CHAIN = """  <module Name="Adjust Channel Levels" />
  <module Name="Remove Crosstalk" />
  <module Name="Glitch Identification" />
  <module Name="Extract Spectra" CalibrationFile="{recmat}" />
  <module Name="Assemble Data Cube" />
  <module Name="Correct Dispersion" />
  <module Name="Save DataSet Information" />
"""
FRAME = """<?xml version="1.0" encoding="UTF-8"?>
<DRF LogPath="/work/logs" ReductionType="ARP_SPEC">
<dataset InputDir="/raw" OutputDir="/work/{out}">
<fits FileName="{obj}" />
</dataset>
  <module Name="Subtract Frame" CalibrationFile="{sub}" />
""" + CHAIN + "</DRF>\n"
DARK = """<?xml version="1.0" encoding="UTF-8"?>
<DRF LogPath="/work/logs" ReductionType="CRP_SPEC">
<dataset InputDir="/raw" OutputDir="/work/calib">
{files}</dataset>
  <module Name="Combine Frames" Combine_Method="MEDIAN" />
  <module Name="Save DataSet Information" />
</DRF>
"""
MOSAIC = """<?xml version="1.0" encoding="UTF-8"?>
<DRF LogPath="/work/logs" ReductionType="ARP_SPEC">
<dataset InputDir="/work/{mode}/cubes_bx442" OutputDir="/work/{mode}/mosaic_bx442">
{files}</dataset>
  <module Name="Mosaic Frames" Combine_Method="MEANCLIP" Offset_Method="TEL" />
  <module Name="Save DataSet Information" />
</DRF>
"""


def headers():
    rows = []
    for f in sorted(glob.glob(os.path.join(RAW, 'OS.2011*.fits'))):
        h = fits.getheader(f)
        rows.append(dict(file=os.path.basename(f), obj=str(h.get('OBJECT')).strip(),
                         datafile=str(h.get('DATAFILE')).strip(), itime=float(h.get('ITIME')),
                         filt=str(h.get('SFILTER')).strip(), dec=float(h.get('DEC')),
                         airmass=float(h.get('AIRMASS')), t=float(f.split('.')[-2]),
                         date=os.path.basename(f).split('.')[1]))
        rows[-1]['tabs'] = int(rows[-1]['date'][-2:]) * 86400.0 + rows[-1]['t']   # all frames are 2011-08
    return rows


def nod_pairs(frames):
    """Pair frames by sequence (sYYMMDD_aNNN), partner = the other nod position."""
    byseq = {}
    for r in frames:
        byseq.setdefault((r['date'], r['datafile'][:-3]), []).append(r)
    out = []
    for key, fr in sorted(byseq.items()):
        assert len(fr) == 2, key
        a, b = fr
        assert abs(a['dec'] - b['dec']) * 3600 > 1.5, key
        out += [(a, b), (b, a)]
    return out


def write(q, name, txt):
    os.makedirs(os.path.join(WORK, q), exist_ok=True)
    with open(os.path.join(WORK, q, name), 'w') as fh:
        fh.write(txt)


def drfs(sci):
    rows = headers()
    os.makedirs(os.path.join(WORK, 'logs'), exist_ok=True)
    for d in ('calib', 'gdlstart'):      # recmats and the GDL port, as CFG438 ran them
        shutil.copytree(os.path.join(OLD, d), os.path.join(WORK, d), dirs_exist_ok=True)
    if not sci:
        write('q_dark', '001.superdark.waiting',
              DARK.format(files=''.join('<fits FileName="%s" />\n' % f for f in DARKS)))
        return
    made = sorted(glob.glob(os.path.join(WORK, 'calib', '*.fits')))
    made = [f for f in made if 'infl' not in os.path.basename(f)]
    assert len(made) == 1, made          # the Combine Frames output
    os.replace(made[0], os.path.join(WORK, 'calib', SUPERDARK))
    sci_fr = [r for r in rows if r['obj'] == 'BX442' and r['itime'] > 800 and r['filt'] == 'Kn2']
    assert len(sci_fr) == 40
    for k, r in enumerate(sorted(sci_fr, key=lambda r: r['t'])):
        write('q_sci', '%03d.sci_%s.waiting' % (k + 1, r['datafile']),
              FRAME.format(out='raw_sci', obj=r['file'], sub='/work/calib/' + SUPERDARK, recmat=RECMAT))
    std = [r for r in rows if r['obj'].startswith('HIP') and r['filt'] == 'Kn2']
    assert len(std) == 8, len(std)
    for k, (a, b) in enumerate(nod_pairs(std)):
        write('q_std', '%03d.std_%s.waiting' % (k + 1, a['datafile']),
              FRAME.format(out='std', obj=a['file'], sub='/raw/' + b['file'], recmat=RECMAT))
    for d in ('raw_sci', 'std'):
        os.makedirs(os.path.join(WORK, d), exist_ok=True)


def cube_name(datafile):
    return '%s_Kn2_100.fits' % datafile


def mode_tree(mode):
    d = os.path.join(WORK, mode)
    for s in ('cubes_bx442', 'q_mos_bx442', 'mosaic_bx442'):
        os.makedirs(os.path.join(d, s), exist_ok=True)
    sky = os.path.join(d, 'cubes_sky')
    if not os.path.exists(sky):
        os.symlink(os.path.join(OLD, 'cubes_sky'), sky)
    return d


def diff():
    """S: A - s(lambda) B with s = median_spaxels(A) / median_spaxels(B) per channel."""
    out = os.path.join(mode_tree('S'), 'cubes_bx442')
    sci = [r for r in headers() if r['obj'] == 'BX442' and r['itime'] > 800 and r['filt'] == 'Kn2']
    log = []
    for a, b in nod_pairs(sci):
        A = fits.open(os.path.join(WORK, 'raw_sci', cube_name(a['datafile'])))
        B = fits.open(os.path.join(WORK, 'raw_sci', cube_name(b['datafile'])))
        da, db = A[0].data.astype(float), B[0].data.astype(float)
        ga, gb = A[2].data > 0, B[2].data > 0
        ma = np.nanmedian(np.where(ga, da, np.nan).reshape(-1, da.shape[2]), axis=0)
        mb = np.nanmedian(np.where(gb, db, np.nan).reshape(-1, db.shape[2]), axis=0)
        s = np.where(np.isfinite(ma / mb) & (mb != 0), ma / mb, 1.0)
        A[0].data = (da - s * db).astype(np.float32)
        A[1].data = np.sqrt(A[1].data.astype(float) ** 2 + (s * B[1].data) ** 2).astype(np.float32)
        A[2].data = (A[2].data * gb).astype(np.uint8)
        A[0].header['HISTORY'] = 'CFG438B S: minus %s scaled per channel (Law+12)' % b['datafile']
        A.writeto(os.path.join(out, cube_name(a['datafile'])), overwrite=True)
        log.append(dict(obj=a['datafile'], sub=b['datafile'], s_median=float(np.median(s)),
                        s_p5=float(np.percentile(s, 5)), s_p95=float(np.percentile(s, 95))))
    json.dump(log, open(os.path.join(HERE, 'cfg438b_S_scales.json'), 'w'), indent=1)
    print(len(log), 'S cubes')


def lam_of(h, n):
    return (h['CRVAL1'] + (np.arange(n) + 1 - h['CRPIX1']) * h['CDELT1']) * 10.0  # A


def telluric(teff):
    """One normalised transmission curve per standard frame (frozen recipe)."""
    rows = {r['datafile']: r for r in headers()}
    curves = []
    for f in sorted(glob.glob(os.path.join(WORK, 'std', '*_Kn2_100.fits'))):
        hd = fits.open(f)
        h, d, q = hd[0].header, hd[0].data.astype(float), hd[2].data
        d[q == 0] = np.nan
        lam = lam_of(h, d.shape[2])
        img = np.nansum(d, axis=2)
        j0, i0 = np.unravel_index(np.nanargmax(img), img.shape)
        jj, ii = np.mgrid[0:img.shape[0], 0:img.shape[1]]
        ap = (jj - j0) ** 2 + (ii - i0) ** 2 <= 5.0 ** 2          # 0.5" at 0.1"/spaxel
        spec = np.nansum(d[ap], axis=0)
        # summed S/N: median level over the robust channel-to-channel scatter
        sn = float(np.nanmedian(spec) / (1.4826 * np.nanmedian(np.abs(np.diff(spec))) / np.sqrt(2)))
        lm = lam * 1e-10
        bb = 1.0 / (lm ** 5 * (np.exp(H * CL / (lm * KB * teff)) - 1.0))
        t = spec / bb
        t /= np.nanmedian(t)
        df = os.path.basename(f).replace('_Kn2_100.fits', '')
        w = (lam >= HA_WIN[0]) & (lam <= HA_WIN[1])
        curves.append(dict(file=df, star=rows[df]['obj'], airmass=rows[df]['airmass'], tabs=rows[df]['tabs'],
                           date=rows[df]['date'], sn=sn, centre=[int(j0), int(i0)],
                           t_min_ha=float(np.nanmin(t[w])), t_max_ha=float(np.nanmax(t[w])),
                           lam=lam, curve=t))
    return curves


def tell(teff):
    curves = telluric(teff)
    assert len(curves) == 8, len(curves)
    rows = {r['datafile']: r for r in headers()}
    choice = {}
    for mode, src in (('T', os.path.join(OLD, 'cubes_bx442')), ('ST', os.path.join(WORK, 'S', 'cubes_bx442'))):
        out = os.path.join(mode_tree(mode), 'cubes_bx442')
        for f in sorted(glob.glob(os.path.join(src, '*_Kn2_100.fits'))):
            df = os.path.basename(f).replace('_Kn2_100.fits', '')
            r = rows[df]
            # nearest in airmass, ties broken by nearest in time
            c = min(curves, key=lambda c: (abs(c['airmass'] - r['airmass']), abs(c['tabs'] - r['tabs'])))
            choice[df] = c['file']
            hd = fits.open(f)
            assert np.allclose(lam_of(hd[0].header, hd[0].data.shape[2]), c['lam'])
            tc = np.where(np.isfinite(c['curve']) & (c['curve'] > 0), c['curve'], np.nan)
            hd[0].data = (hd[0].data / tc).astype(np.float32)
            hd[1].data = (hd[1].data / tc).astype(np.float32)
            hd[2].data = (hd[2].data * np.isfinite(tc)).astype(np.uint8)
            hd[0].header['HISTORY'] = 'CFG438B T: divided by telluric from %s (Teff %.0f K)' % (c['file'], teff)
            hd.writeto(os.path.join(out, os.path.basename(f)), overwrite=True)
    summ = dict(teff=teff, curves=[{k: v for k, v in c.items() if k not in ('lam', 'curve')} for c in curves],
                choice=choice)
    summ['valid_std_sn_ge_50'] = all(c['sn'] >= 50 for c in curves)
    used = set(choice.values())
    summ['valid_curve_0p5_1p5_in_ha'] = all(0.5 <= c['t_min_ha'] and c['t_max_ha'] <= 1.5
                                            for c in curves if c['file'] in used)
    json.dump(summ, open(os.path.join(HERE, 'cfg438b_telluric.json'), 'w'), indent=1, default=float)
    np.savetxt(os.path.join(HERE, 'cfg438b_telluric_curves.txt'),
               np.column_stack([curves[0]['lam']] + [c['curve'] for c in curves]),
               header='lambda_A ' + ' '.join(c['file'] for c in curves), fmt='%.6g')
    print(json.dumps({k: v for k, v in summ.items() if k != 'choice'}, indent=1, default=float))


def mosaic(mode):
    d = mode_tree(mode)
    cubes = sorted(f for f in os.listdir(os.path.join(d, 'cubes_bx442')) if f.endswith('.fits'))
    assert len(cubes) == 40, len(cubes)
    write(os.path.join(mode, 'q_mos_bx442'), '001.mosaic_bx442.waiting',
          MOSAIC.format(mode=mode, files=''.join('<fits FileName="%s" />\n' % c for c in cubes)))
    print('queue', os.path.join(mode, 'q_mos_bx442'))


def grade(mode):
    """CFG438's frozen extraction, unchanged, pointed at MODE's tree; outputs in out_MODE/."""
    spec = importlib.util.spec_from_file_location('k438', K438)
    k = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(k)
    k.WORK = os.path.join(WORK, mode)
    k.HERE = os.path.join(HERE, 'out_' + mode)
    os.makedirs(k.HERE, exist_ok=True)
    res = {'true': k.run('bx442', False)}
    if mode == 'ST':
        res['mutate'] = k.run('bx442', True)
    keep = ('n_pass', 'summed', 'kin', 'validation', 'verdict', 'sigma_m_flux_weighted', 'sigma_m_err')
    print(json.dumps({m: {a: b for a, b in r.items() if a in keep} for m, r in res.items()}, indent=1, default=float))


if __name__ == '__main__':
    step = sys.argv[1]
    if step == 'drfs':
        drfs('--sci' in sys.argv)
    elif step == 'diff':
        diff()
    elif step == 'tell':
        tell(float(sys.argv[2]) if len(sys.argv) > 2 else 9500.0)
    elif step == 'mosaic':
        mosaic(sys.argv[2])
    elif step == 'grade':
        grade(sys.argv[2])
