#!/usr/bin/env python3
"""EXR1R fetches: one paced stream (>= 1.5 s between requests), generic client name, nothing personal.

  python3 exr1r_fetch.py scs [file]  : cone searches listed in _external_data/exr1r_erass1/missing_scs*.json
  python3 exr1r_fetch.py ul          : upper limits listed in missing_ul.json (one POST)
  python3 exr1r_fetch.py check       : 20 cached upper-limit positions (seed 20261112) re-queried live in one POST,
                                       compared field by field with the cache -> exr1r_live_check.json
Raw responses go to _external_data/exr1r_erass1/ (outside git) with MANIFEST_live.json (url, time, sha256).
kappa = 1/2 FITTED; not theory closed.
"""
import glob
import hashlib
import json
import os
import sys
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
LIVE = os.path.join(ROOT, '_external_data', 'exr1r_erass1')
FETCH = os.path.join(ROOT, '_external_data', 'exr1_erass1', 'fetch')
UA = {'User-Agent': 'python-client/1.0'}
MAN = os.path.join(LIVE, 'MANIFEST_live.json')
_last = [0.0]


def pace():
    dt = time.time() - _last[0]
    if dt < 1.5:
        time.sleep(1.5 - dt)
    _last[0] = time.time()


def record(url, method, fname, data):
    man = json.load(open(MAN)) if os.path.exists(MAN) else []
    man.append({'url': url, 'method': method, 'file': fname, 'bytes': len(data),
                'sha256': hashlib.sha256(data).hexdigest(),
                'time': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())})
    json.dump(man, open(MAN, 'w'), indent=1)


def get(url):
    pace()
    req = urllib.request.Request(url, headers=UA)
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                return r.read()
        except Exception as e:  # noqa: BLE001
            print('retry', attempt + 1, url[:90], e, flush=True)
            time.sleep(5)
            pace()
    raise RuntimeError('failed ' + url)


def post_json(url, payload):
    pace()
    body = json.dumps(payload).encode()
    req = urllib.request.Request(url, data=body, headers=dict(UA, **{'Content-Type': 'application/json'}))
    with urllib.request.urlopen(req, timeout=300) as r:
        return r.read()


def next_index(prefix):
    ex = glob.glob(os.path.join(LIVE, prefix + '*'))
    return len(ex)


def do_scs(path):
    todo = json.load(open(path))
    n0 = next_index('scs_live_')
    for k, c in enumerate(todo):
        url = (f"https://erosita.mpe.mpg.de/erodat/catalogue/SCS?CAT=DR1_Main&RA={c['ra']:.6f}&DEC={c['dec']:.6f}"
               f"&SR={c['sr']:.6f}&VERB=1")
        data = get(url)
        fn = f'scs_live_{n0 + k:04d}.xml'
        open(os.path.join(LIVE, fn), 'wb').write(data)
        record(url, 'GET', fn, data)
        if (k + 1) % 10 == 0:
            print('cones', k + 1, '/', len(todo), flush=True)
    print('done', len(todo))


def do_ul(path):
    todo = json.load(open(path))
    url = 'https://erosita.mpe.mpg.de/erodat/upperlimit/service_multi'
    q = [{'ra': c['ra'], 'dec': c['dec'], 'band': '024', 'dr_survey': 'DR1_eRASS1'} for c in todo]
    data = post_json(url, q)
    fn = f'ul_live_{next_index("ul_live_"):03d}.json'
    open(os.path.join(LIVE, fn), 'wb').write(data)
    record(url, 'POST', fn, data)
    print('upper limits', len(json.loads(data)['limits']))


def do_check():
    import numpy as np
    recs = []
    for f in sorted(glob.glob(os.path.join(FETCH, 'ul', '*.json'))):
        recs += json.load(open(f))['limits']
    pick = np.random.default_rng(20261112).choice(len(recs), 20, replace=False)
    sel = [recs[i] for i in pick]
    url = 'https://erosita.mpe.mpg.de/erodat/upperlimit/service_multi'
    q = [{'ra': r['ra'], 'dec': r['dec'], 'band': '024', 'dr_survey': 'DR1_eRASS1'} for r in sel]
    data = post_json(url, q)
    fn = f'check_live_{next_index("check_live_"):03d}.json'
    open(os.path.join(LIVE, fn), 'wb').write(data)
    record(url, 'POST', fn, data)
    live = json.loads(data)['limits']
    keys = ['Count', 'Bkg_counts', 'Bkg_SourceMap', 'Exposure', 'UL_B', 'UL_S', 'de_sky', 'field']
    rows, nmatch = [], 0
    for a, b in zip(sel, live):
        same = all(a.get(k) == b.get(k) for k in keys) and abs(a['ra'] - b['ra']) < 1e-9
        nmatch += same
        rows.append({'ra': a['ra'], 'dec': a['dec'], 'identical': same,
                     'diff': {k: [a.get(k), b.get(k)] for k in keys if a.get(k) != b.get(k)}})
    out = {'n': len(sel), 'identical': nmatch, 'file': fn, 'rows': rows,
           'note': 'cached raw records (EXR1 fetch, 2026-11-13 UTC) against the live service, field by field'}
    json.dump(out, open(os.path.join(HERE, 'exr1r_live_check.json'), 'w'), indent=1)
    print('live check:', nmatch, 'of', len(sel), 'identical')


if __name__ == '__main__':
    os.makedirs(LIVE, exist_ok=True)
    mode = sys.argv[1]
    if mode == 'scs':
        do_scs(sys.argv[2] if len(sys.argv) > 2 else os.path.join(LIVE, 'missing_scs.json'))
    elif mode == 'ul':
        do_ul(os.path.join(LIVE, 'missing_ul.json'))
    elif mode == 'check':
        do_check()
