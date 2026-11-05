#!/usr/bin/env python3
"""AZ32: fresh radial spectra and explicitly restricted tensor diagnostic."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import resource
import signal
import subprocess
import sys
import time

sys.dont_write_bytecode = True
for key in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS',
            'VECLIB_MAXIMUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    os.environ[key] = '1'
os.environ.pop('V3X_MUTATE', None)
os.environ.pop('V3W_MUTATE', None)
import numpy as np
import scipy
import sympy
import mpmath as mp

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ap = argparse.ArgumentParser()
ap.add_argument('--mutate', action='store_true')
ap.add_argument('--resume', action='store_true')
ap.add_argument('--part', choices=('spectrum', 'tensor', 'all'), default='all')
args = ap.parse_args()
MODE = 'mutate' if args.mutate else 'main'
OUT = HERE / MODE
OUT.mkdir(exist_ok=True)
STOP = []
signal.signal(signal.SIGTERM, lambda s, f: STOP.append(s))
signal.signal(signal.SIGINT, lambda s, f: STOP.append(s))
START = time.monotonic()
FILES = [str(HERE.relative_to(ROOT) / 'run.py'),
         str(HERE.relative_to(ROOT) / 'FROZEN_CRITERIA.md'),
         'complete_theory_2026_11_04/CT14_Cpp_health/ct14_h3_w4b.py',
         'rebuild_2026_10_22/V3X_v3s_close_undecided/v3x_w4c_health.py',
         'rebuild_2026_10_22/V3X_v3s_close_undecided/v3x_w4c_health.json',
         'rebuild_2026_10_22/V3X_v3s_close_undecided/v3x_solver.py',
         'rebuild_2026_10_22/V3W_v3s_weak_spots/w4_health_gw.py',
         'covariant_push_2026_10_22/C6_literal_cassini/c6_solver.py',
         'doors_push_2026_10_22/D7d_screened_q2/d7d_solver.py',
         'doors_push_2026_10_22/D7b_cassini_Q2/d7b_cassini_q2_results.json',
         'rebuild_2026_10_22/X3_switched_stiffness/x3_switched_stiffness_results.json']
HASH = {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in FILES}
FP = hashlib.sha256(json.dumps(HASH, sort_keys=True).encode()).hexdigest()


def atomic(path, obj):
    tmp = path.with_suffix(path.suffix + '.tmp')
    with tmp.open('w') as f:
        json.dump(obj, f, indent=2, allow_nan=False)
        f.write('\n'); f.flush(); os.fsync(f.fileno())
    os.replace(tmp, path)


def checkpoint(name, fn):
    if STOP:
        print('YIELD at checkpoint', flush=True)
        sys.exit(75)
    path = OUT / (name + '.json')
    if path.exists():
        if not args.resume:
            raise RuntimeError('Existing result requires --resume: ' + name)
        obj = json.loads(path.read_text())
        if obj['fingerprint'] != FP or obj['mode'] != MODE:
            raise RuntimeError('Checkpoint source/mode changed: ' + name)
        print('RESUME', name, flush=True)
        return obj['data']
    t = time.monotonic()
    result = fn()
    atomic(path, dict(fingerprint=FP, mode=MODE, seconds=time.monotonic()-t, data=result))
    print('DONE', name, 'seconds', round(time.monotonic()-t, 2), flush=True)
    return result


atomic(OUT / 'provenance.json', dict(inputs=HASH, fingerprint=FP,
    commit=subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
    software=dict(python=sys.version.split()[0], numpy=np.__version__, scipy=scipy.__version__,
                  sympy=sympy.__version__, mpmath=mp.__version__), mode=MODE))


def radial():
    # Execute only the audited loader and pure operator definitions. The
    # historical script's loop and output-writing section are not executed.
    src = (ROOT / FILES[2]).read_text().split('ND = (12, 16, 24, 32, 48)')[0]
    env = {'__file__': str(ROOT / FILES[2]), '__name__': 'az32_readonly'}
    exec(compile(src, FILES[2] + '[definitions]', 'exec'), env)
    ns, rec, spectrum_f = env['ns'], env['REC'], env['spectrum_f']
    result = {}
    for foot in ('canonical', 'alt'):
        B = ns['background'](foot)
        g, rho, vm = B['g'], B['rho'], B['vm']
        lam = B['Lam']; dom = g.r <= lam * (1 + 1e-12)
        profiles = {'lo': rho[dom].min(axis=1) + B['rgal_lo'],
                    'hi': rho[dom].max(axis=1) + B['rgal_hi']}
        bounds = {'lo': float(1 + vm[dom].min()), 'hi': float((1 + vm[dom].max())**2)}
        gamma = (-1 if args.mutate else 1) * lam**2 / 2
        cases = {}
        for nd in (12, 16, 24, 32, 48):
            rf, rc = ns['grid_r'](1e-4, lam, nd)
            for ell in range(5):
                for br in ('lo', 'hi'):
                    name = f'{foot}_nd{nd}_l{ell}_{br}'
                    def evaluate():
                        return spectrum_f(ns['interp_rho'](g.r[dom], profiles[br], rf),
                                          ns['interp_rho'](g.r[dom], profiles[br], rc),
                                          rf, rc, ell, gamma, bounds[br])
                    cases[f'{nd}|{ell}|{br}'] = checkpoint(name, evaluate)
        deviation = max(abs(a/float(b)-1)
            for nd in (12, 16) for ell in range(5) for br in ('lo', 'hi')
            for a, b in zip(cases[f'{nd}|{ell}|{br}']['omega2_low'][:3],
                           rec[foot]['cases'][f'nd{nd}|l{ell}|{br}|neumann']['omega2_low'][:3]))
        ladder = {f'{aa}->{bb}': max(abs(a/b-1)
            for ell in range(5) for br in ('lo', 'hi')
            for a, b in zip(cases[f'{aa}|{ell}|{br}']['omega2_low'][:3],
                           cases[f'{bb}|{ell}|{br}']['omega2_low'][:3]))
                  for aa, bb in ((12,16),(16,24),(24,32),(32,48))}
        # For wrong-sign stiffness the original inverse-based positive-mode
        # algorithm is not applicable. Precision agreement is tested on the
        # unmutated operator, separately from the deliberately negative one.
        rf, rc = ns['grid_r'](1e-4, lam, 24)
        def spot():
            af = ns['interp_rho'](g.r[dom], profiles['lo'], rf)
            ac = ns['interp_rho'](g.r[dom], profiles['lo'], rc)
            high = ns['spectrum'](af, ac, rf, rc, 4, lam**2/2, bounds['lo'], 'neumann', 30, 3)
            low = spectrum_f(af, ac, rf, rc, 4, lam**2/2, bounds['lo'])
            delta = max(abs(float(a)/b-1) for a,b in zip(high['omega2_low'][:3],low['omega2_low'][:3]))
            return dict(high=high['omega2_low'][:3], low=low['omega2_low'][:3], relative_error=delta)
        sp = checkpoint(foot+'_precision24', spot)
        checks = dict(background_residual=B['fin']<1e-9,
                      known_answer=deviation<=1e-8,
                      precision=sp['relative_error']<=1e-8,
                      positive=all(c['all_positive'] and c['A_pd'] and c['V_min']>0 and c['V_ge_gamma'] for c in cases.values()),
                      convergence=ladder['32->48']<.05)
        label = ('PASS' if all(checks.values()) else
                 ('FAIL' if not checks['positive'] and checks['precision'] else 'UNDECIDED'))
        result[foot] = dict(label=label, checks=checks, known_answer_relative=deviation,
            background_residual=B['fin'], ladder=ladder, min_omega2=min(c['omega2_low'][0] for c in cases.values()),
            precision=sp, cases=cases, background_resources=ns['SIDE'])
        atomic(OUT/'spectrum_partial.json', result)
        print('SPECTRUM', foot, label, checks, ladder, flush=True)
    return result


def tensor():
    src = (ROOT / FILES[6]).read_text().split('# ============================================================ W4b/W4c items')[0]
    env = {'__file__': str(ROOT / FILES[6]), '__name__': 'az32_tensor_readonly'}
    exec(compile(src, FILES[6]+'[TT-only]', 'exec'), env)
    result = {}
    with mp.workdps(80):
        for foot, row in env['W4a'].items():
            c2 = mp.mpf(1) + (mp.mpf('1e-8') if args.mutate else 0)
            k = 2*mp.pi*100/mp.mpf('299792458')
            mass = mp.mpf(str(row['max_abs_m2']))
            deviations = [mp.sqrt(c2)/mp.sqrt(1+sgn*mass/(c2*k*k))-1 for sgn in (-1,1)]
            lo, hi = min(deviations), max(deviations)
            approx = mass/(2*k*k)
            small_error = max(abs(abs(v)-approx) for v in deviations) if not args.mutate else None
            checks = dict(principal_TT=bool(env['no_quad'] and env['lin_total']),
                          GR_limit=bool(env['m2_off']==0),
                          massless_group_speed=bool(mp.sqrt(1)/mp.sqrt(1)==1),
                          observed_band=bool(lo>=mp.mpf('-3e-15') and hi<=mp.mpf('7e-16')),
                          approximation=bool(small_error is None or small_error<mp.mpf('1e-45')))
            result[foot] = dict(label='PASS' if all(checks.values()) else 'FAIL', checks=checks,
                cT2=str(c2), group_speed_deviation=[str(lo),str(hi)],
                approximation_error=str(small_error), scan=row)
    return dict(footings=result, exact=env['RES']['W4a'],
                scope='restricted TT diagnostic only; full constrained mixed modes UNDECIDED',
                source='https://arxiv.org/abs/1710.05834v2')


all_results = {}
if args.part in ('spectrum', 'all'):
    all_results['spectrum'] = checkpoint('spectrum_result', radial)
if args.part in ('tensor', 'all'):
    all_results['tensor'] = checkpoint('tensor_result', tensor)
stable = all(hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h for p,h in HASH.items())
rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024)
all_results.update(inputs_unchanged=stable, rss_bytes=rss, seconds=time.monotonic()-START,
                   statement='kappa = 1/2 FITTED; not theory closed', mode=MODE,
                   full_W4c='UNDECIDED: radial bracket and restricted TT results do not close full mixed modes')
atomic(OUT/f'results_{args.part}.json', all_results)
passed = stable and rss<1e9
if 'spectrum' in all_results:
    passed &= all(r['label']=='PASS' for r in all_results['spectrum'].values())
if 'tensor' in all_results:
    passed &= all(r['label']=='PASS' for r in all_results['tensor']['footings'].values())
print('FINAL', MODE, args.part, 'PASS' if passed else 'CHECKS FAILED', flush=True)
sys.exit(0 if passed else 1)
