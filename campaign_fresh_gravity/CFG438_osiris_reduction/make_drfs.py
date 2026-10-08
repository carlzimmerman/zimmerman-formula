#!/usr/bin/env python3
"""CFG438: write OSIRIS DRP DRF XML queues for BX442 and A1689B11.2.

Reads the raw KOA lev0 headers (paths relative to the repo root's parent:
../_external_data/cfg437_work/raw) and writes queue directories into
../_external_data/cfg438_work/. Paths inside the DRFs are container paths
(/raw, /work), matching run_queue.sh.

Object/sky assignment (from headers, see README):
  BX442 (Kn2, 0.100"): every 900 s frame is on source; frames alternate
    between two positions 2.8" apart (A/B nod within the 1.6"x6.4" field).
    Each frame is reduced as frame minus its pair partner (a00Nxx1 <-> xx2).
  A1689B11.2 (Kn5, 0.050"): two pointings 5" apart in RA. The position at
    RA 197.87116 (8 frames) is the object, RA 197.87254 (5 frames) is sky.
    Each object frame minus the sky frame closest in time.
Glitch Identification only for the pre-2016 detector (BX442).
Clean Cosmic Rays skipped (Keck advice); MEANCLIP mosaic rejects outliers.
"""
import glob
import os

from astropy.io import fits

HERE = os.path.dirname(os.path.abspath(__file__))
EXT = os.path.normpath(os.path.join(HERE, '..', '..', '..', '_external_data'))
RAW = os.path.join(EXT, 'cfg437_work', 'raw')
WORK = os.path.join(EXT, 'cfg438_work')

RECMAT = {'Kn2': '/work/calib/s100714_c006___infl_Kn2_100.fits',
          'Kn5': '/work/calib/s170529_c009___infl_Kn5_050.fits'}

DRF = """<?xml version="1.0" encoding="UTF-8"?>
<DRF LogPath="/work/logs" ReductionType="ARP_SPEC">
<dataset InputDir="/raw" OutputDir="/work/{out}">
<fits FileName="{obj}" />
</dataset>
  <module Name="Subtract Frame" CalibrationFile="/raw/{sky}" />
  <module Name="Adjust Channel Levels" />
  <module Name="Remove Crosstalk" />
{glitch}  <module Name="Extract Spectra" CalibrationFile="{recmat}" />
  <module Name="Assemble Data Cube" />
  <module Name="Correct Dispersion" />
  <module Name="Save DataSet Information" />
</DRF>
"""

MOSAIC = """<?xml version="1.0" encoding="UTF-8"?>
<DRF LogPath="/work/logs" ReductionType="ARP_SPEC">
<dataset InputDir="/work/{cubes}" OutputDir="/work/{out}">
{files}</dataset>
  <module Name="Mosaic Frames" Combine_Method="MEANCLIP" Offset_Method="TEL" />
  <module Name="Save DataSet Information" />
</DRF>
"""


def headers():
    rows = []
    for f in sorted(glob.glob(os.path.join(RAW, 'OS.*.fits'))):
        h = fits.getheader(f)
        rows.append(dict(file=os.path.basename(f), obj=str(h.get('OBJECT')).strip(),
                         datafile=str(h.get('DATAFILE')).replace('.fits', ''),
                         itime=float(h.get('ITIME')), filt=str(h.get('SFILTER')).strip(),
                         ra=float(h.get('RA')), dec=float(h.get('DEC')),
                         t=float(os.path.basename(f).split('.')[2]),
                         date=os.path.basename(f).split('.')[1]))
    return rows


def write_queue(name, pairs, filt, glitch):
    q = os.path.join(WORK, 'q_' + name)
    os.makedirs(q, exist_ok=True)
    for k, (o, s) in enumerate(pairs):
        txt = DRF.format(out='cubes_' + name, obj=o, sky=s, recmat=RECMAT[filt],
                         glitch='  <module Name="Glitch Identification" />\n' if glitch else '')
        with open(os.path.join(q, '%03d.%s_%s.waiting' % (k + 1, name, o.replace('.', '_'))), 'w') as fh:
            fh.write(txt)
    os.makedirs(os.path.join(WORK, 'cubes_' + name), exist_ok=True)
    with open(os.path.join(q, 'PAIRS.txt'), 'w') as fh:
        for o, s in pairs:
            fh.write('%s - %s\n' % (o, s))
    return q


def main():
    rows = headers()
    # BX442: 900 s Kn2 science frames, pair partner = same sequence number, other frame
    bx = [r for r in rows if r['obj'] == 'BX442' and r['itime'] > 800 and r['filt'] == 'Kn2']
    assert len(bx) == 40, len(bx)
    byseq = {}
    for r in bx:
        byseq.setdefault((r['date'], r['datafile'][:-3]), []).append(r)
    pairs = []
    for key, fr in sorted(byseq.items()):
        assert len(fr) == 2, key
        a, b = fr
        assert abs(a['dec'] - b['dec']) * 3600 > 2.0  # the two nod positions
        pairs += [(a['file'], b['file']), (b['file'], a['file'])]
    write_queue('bx442', pairs, 'Kn2', glitch=True)

    # A1689B11.2: object = RA 197.8712 pointing, sky = RA 197.8725 pointing
    a1 = [r for r in rows if r['obj'] == 'A1689B11.2']
    assert len(a1) == 13
    obj = [r for r in a1 if r['ra'] < 197.872]
    sky = [r for r in a1 if r['ra'] > 197.872]
    assert len(obj) == 8 and len(sky) == 5
    pairs = []
    for r in obj:
        s = min(sky, key=lambda x: abs(x['t'] - r['t']))
        pairs.append((r['file'], s['file']))
    write_queue('a1689', pairs, 'Kn5', glitch=False)


def write_mosaic(name):
    """Mosaic DRF over every cube the frame queue produced (run after it)."""
    cubes = sorted(f for f in os.listdir(os.path.join(WORK, 'cubes_' + name)) if f.endswith('.fits'))
    q = os.path.join(WORK, 'q_mos_' + name)
    os.makedirs(q, exist_ok=True)
    os.makedirs(os.path.join(WORK, 'mosaic_' + name), exist_ok=True)
    files = ''.join('<fits FileName="%s" />\n' % c for c in cubes)
    with open(os.path.join(q, '001.mosaic_%s.waiting' % name), 'w') as fh:
        fh.write(MOSAIC.format(cubes='cubes_' + name, out='mosaic_' + name, files=files))
    return len(cubes)


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 2 and sys.argv[1] == '--mosaic':
        print(write_mosaic(sys.argv[2]), 'cubes')
    else:
        main()
