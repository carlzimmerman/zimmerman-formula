#!/usr/bin/env python3
"""G-P3 (FROZEN_CRITERIA.md 2.3): thread and resume equivalence, with real SIGTERMs, plus peak-footprint measurement.
Run: nice -n 15 /usr/bin/python3 resume_test.py --n 16 [--n 32]. Writes resume_test_n<N>.json."""
import argparse
import hashlib
import json
import re
import signal
import subprocess
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ENG = HERE / 'engine' / 'pmedium3d.py'
PY = '/usr/bin/python3'


def run(outdir, n, threads, extra=(), sigterm_after=None):
    cmd = ['/usr/bin/time', '-l', PY, str(ENG), '--n', str(n), '--amp', '0.03', '--footing', 'canonical', '--threads', str(threads), '--outdir', str(outdir), *extra]
    env = {**__import__('os').environ, 'OMP_NUM_THREADS': '1', 'OPENBLAS_NUM_THREADS': '1', 'VECLIB_MAXIMUM_THREADS': '1'}
    t0 = time.time(); p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=env)
    if sigterm_after is not None:
        time.sleep(sigterm_after)
        # /usr/bin/time forwards nothing; signal the python child directly
        kids = subprocess.run(['pgrep', '-P', str(p.pid)], capture_output=True, text=True).stdout.split()
        for k in kids: subprocess.run(['kill', '-TERM', k])
    out, err = p.communicate(); wall = time.time() - t0
    fp = re.search(r'(\d+)\s+peak memory footprint', err); rss = re.search(r'(\d+)\s+maximum resident set size', err)
    return dict(cmd=' '.join(cmd[2:]).replace(str(HERE) + '/', ''), exit=p.returncode, wall=wall,
                peak_footprint_gb=int(fp.group(1)) / 1e9 if fp else None, max_rss_gb=int(rss.group(1)) / 1e9 if rss else None,
                log_tail=out.strip().splitlines()[-2:])


def load(d, name):
    r = json.loads((d / name / 'result.json').read_text()); z = np.load(d / name / 'final_state.npz')
    return r, {k: z[k] for k in z.files}


def strip(r):
    r = dict(r); r.pop('engine', None); r.pop('final_state_sha256', None); return r


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--n', type=int, default=16); a = ap.parse_args(); n = a.n
    base = HERE / 'runs' / 'resume_test' / f'n{n}'
    name = f'n{n}_strong_can'
    for sub in 'ABC':
        d = base / sub / name
        if d.exists():
            for f in d.iterdir(): f.unlink()
    res = dict(criteria='FROZEN_CRITERIA.md 2.3', n=n, runs={})
    res['runs']['A_threads1'] = run(base / 'A', n, 1)
    res['runs']['B_threads4'] = run(base / 'B', n, 4)
    wall = res['runs']['A_threads1']['wall']
    c1 = run(base / 'C', n, 1, sigterm_after=0.35 * wall)
    ck = base / 'C' / name / 'checkpoint.npz'
    c1['checkpoint_exists'] = ck.exists(); c1['checkpoint_step'] = int(np.load(ck)['step']) if ck.exists() else None
    res['runs']['C1_sigterm'] = c1
    c2 = run(base / 'C', n, 1, ['--resume'], sigterm_after=0.35 * wall)
    c2['checkpoint_exists'] = ck.exists(); c2['checkpoint_step'] = int(np.load(ck)['step']) if ck.exists() else None
    res['runs']['C2_resume_then_sigterm'] = c2
    res['runs']['C3_resume_to_end'] = run(base / 'C', n, 1, ['--resume'])
    shaC = hashlib.sha256((base / 'C' / name / 'result.json').read_bytes()).hexdigest()
    res['runs']['C4_resume_on_complete'] = run(base / 'C', n, 1, ['--resume'])
    shaC2 = hashlib.sha256((base / 'C' / name / 'result.json').read_bytes()).hexdigest()
    rA, sA = load(base / 'A', name); rB, sB = load(base / 'B', name); rC, sC = load(base / 'C', name)
    same = lambda s1, s2: all(np.array_equal(s1[k], s2[k]) for k in s1) and s1.keys() == s2.keys()
    checks = dict(
        threads_1_vs_4_state_bitidentical=same(sA, sB),
        threads_1_vs_4_result_identical=strip(rA) == strip(rB),
        sigterm_exit_75=c1['exit'] == 75 and c2['exit'] == 75,
        checkpoints_written=bool(c1['checkpoint_exists'] and c2['checkpoint_exists'] and c2['checkpoint_step'] > c1['checkpoint_step'] > 0),
        resume_completes_exit_0=res['runs']['C3_resume_to_end']['exit'] == 0,
        resumed_state_bitidentical=same(sA, sC),
        resumed_result_identical=strip(rA) == strip(rC),
        resume_on_complete_exit0_unchanged=res['runs']['C4_resume_on_complete']['exit'] == 0 and shaC == shaC2,
        final_state_sha_A_C_equal=rA['final_state_sha256'] == rC['final_state_sha256'])
    res['checks'] = checks; res['G_P3'] = all(checks.values())
    res['peak_c'] = rA['rows'][-1]['contrast_c_max']; res['steps'] = rA['steps']
    (HERE / f'resume_test_n{n}.json').write_text(json.dumps(res, indent=1) + '\n')
    print(json.dumps(checks, indent=1)); print('G-P3', 'PASS' if res['G_P3'] else 'FAIL', {k: (v['wall'], v['peak_footprint_gb']) for k, v in res['runs'].items()})


if __name__ == '__main__':
    main()
