#!/usr/bin/env python3
"""Identical to run_wrapper.py but with faulthandler: SIGUSR1 at 20 s and 40 s dumps the live stack."""
import signal, sys, time, runpy, os, faulthandler

faulthandler.register(signal.SIGUSR1, file=sys.stderr, all_threads=True)

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
print('ELAPSED %.2f s' % (time.time() - t0), file=sys.stderr)
