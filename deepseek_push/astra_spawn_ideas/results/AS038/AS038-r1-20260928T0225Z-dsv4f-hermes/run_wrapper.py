#!/usr/bin/env python3
"""Wall-clock bounded runner for compute_as038.py (120 s hard limit, 1 thread).
Enforces the bounded-prototype contract and records the enforced bounds.
"""
import signal, sys, time, runpy, os

if os.environ.get('OMP_NUM_THREADS') is None:
    os.environ['OMP_NUM_THREADS'] = '1'
if os.environ.get('OPENBLAS_NUM_THREADS') is None:
    os.environ['OPENBLAS_NUM_THREADS'] = '1'

def handler(signum, frame):
    raise TimeoutError('wall-clock 120 s exceeded')

signal.signal(signal.SIGALRM, handler)
signal.alarm(120)
t0 = time.time()
sys.argv = ['compute_as038.py']
try:
    runpy.run_path('compute_as038.py', run_name='__main__')
    print('RUNPY_RETURNED %.3f s' % (time.time() - t0), file=sys.stderr)
except TimeoutError:
    print('TIMED_OUT after %.1f s' % (time.time() - t0), file=sys.stderr)
    raise SystemExit(3)
print('ELAPSED %.2f s (bound enforced: 120 s SIGALRM, 1 thread)' % (time.time() - t0), file=sys.stderr)
