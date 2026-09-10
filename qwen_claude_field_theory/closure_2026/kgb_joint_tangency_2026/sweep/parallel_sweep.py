#!/usr/bin/env python3
"""Finite local CPU search. Numerical candidates are never theory certificates."""
import os

# Must precede every numerical import, including in multiprocessing spawn children.
for _key in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS',
             'VECLIB_MAXIMUM_THREADS', 'NUMEXPR_NUM_THREADS', 'BLIS_NUM_THREADS'):
    os.environ[_key] = '1'

import argparse
from concurrent.futures import ProcessPoolExecutor, wait, FIRST_COMPLETED
import fcntl
import hashlib
from importlib.metadata import version
import json
import math
import multiprocessing
from pathlib import Path
import random
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
CONTROL = dict(parameters=[306704.1420152562, .1800733844324149, 3057.7826875767923, .1],
               u1=4754.976244138632, f=3.29992587867242, j=38.55121957650046)
DEFAULT_WORKERS = min(8, max(1, (os.cpu_count() or 1) - 2))


def source_hashes():
    paths = [ROOT / p for p in ('search.py', 'clock_joint.py', 'parametric.py',
             'derivatives/fast.py', 'candidate_health.py', 'refine_joint.py', 'sweep/parallel_sweep.py')]
    # Conservative transitive local dependency snapshot; includes some unused helpers.
    for name in ('kgb_universal_clock_2026', 'kgb_nonaffine_clock_2026',
                 'kgb_mass_compatibility_2026', 'kgb_joint_action_2026',
                 'kgb_shared_pressure_2026', 'ticking_kgb_inverse_2026'):
        paths.extend((ROOT.parent / name).rglob('*.py'))
    return {str(p.relative_to(ROOT.parent)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(set(paths))}


def make_job(index, seed):
    mode = 'geometry' if index % 2 == 0 else 'clock'
    if index == 0:
        return dict(index=0, mode=mode, start=CONTROL['parameters'][:],
                    fixed=CONTROL['u1'], control=True)
    rng = random.Random(f'joint-sweep-v1:{seed}:{index}')
    # Log-uniform starts strictly inside the solver bounds, not complete coverage.
    ranges = [(.01, 1e7), (1e-4, 10), (1e-6, 1e6), (1e-4, 10)]
    if mode == 'clock':
        ranges[-1] = (1e-4, 5000)
    start = [math.exp(rng.uniform(math.log(lo), math.log(hi))) for lo, hi in ranges]
    fixed = math.exp(rng.uniform(math.log(1e-4), math.log(5000 if mode == 'geometry' else 10)))
    return dict(index=index, mode=mode, start=start, fixed=fixed, control=False)


def call_solver(job, max_nfev):
    if job['mode'] == 'geometry':
        import search
        return search.solve(job['start'], job['fixed'], max_nfev)
    import clock_joint
    return clock_joint.solve(job['start'], job['fixed'], max_nfev)


def screen_candidate(row):
    from candidate_health import screen
    return screen(row)


def run_job(job, max_nfev, sources):
    started = time.monotonic()
    out = dict(type='result', **job, optimizer_success=False,
               accepted_numerical_joint=False, health_rejected=False, verification_queued=False)
    stage = 'source_check'
    try:
        if source_hashes() != sources:
            raise ValueError('source hashes changed; restart into a new checkpoint')
        stage = 'solve'
        row = call_solver(job, max_nfev)
        # Reject NaN/Infinity before trusting flags or writing a checkpoint.
        json.dumps(row, allow_nan=False)
        out.update(result=row, optimizer_success=row.get('optimizer_status', 0) > 0,
                   accepted_numerical_joint=row.get('accepted_numerical_joint') is True)
        if out['accepted_numerical_joint']:
            out['candidate'] = {key: row[key] for key in ('parameters', 'u1', 'f', 'j')}
            stage = 'health_screen'
            health = screen_candidate(row)
            json.dumps(health, allow_nan=False)
            if type(health.get('needs_high_precision')) is not bool:
                raise ValueError('health screen omitted its boolean queue decision')
            out.update(health=health, health_rejected=not health['needs_high_precision'],
                       verification_queued=health['needs_high_precision'])
        stage = 'source_check'
        if source_hashes() != sources:
            raise ValueError('source hashes changed while evaluating this job')
    except Exception as exc:
        out.update(failure_stage=stage, error_type=type(exc).__name__, error=str(exc),
                   verification_queued=False)
        if stage == 'source_check':
            out.update(optimizer_success=False, accepted_numerical_joint=False, health_rejected=False)
    out['elapsed_seconds'] = time.monotonic() - started
    return out


class Checkpoint:
    """One writer, exact header match, durable complete JSONL records only."""
    def __init__(self, path, header, resume):
        self.path, self.header, self.resume = Path(path), header, resume
        self.results, self.stream, self.lock = {}, None, None

    def __enter__(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.lock = self.path.with_suffix(self.path.suffix + '.lock').open('a')
        try:
            try:
                fcntl.flock(self.lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError:
                raise RuntimeError('another process holds the checkpoint writer lock')
            if self.resume:
                with self.path.open() as stream:
                    for index, line in enumerate(stream):
                        if not line.endswith('\n'):
                            raise ValueError('incomplete final checkpoint record; preserve and repair explicitly')
                        row = json.loads(line)
                        if index == 0:
                            if row != self.header:
                                raise ValueError('resume configuration, runtime, or source hashes differ')
                        elif row.get('type') != 'result' or row.get('index') in self.results:
                            raise ValueError('invalid or duplicate checkpoint record')
                        else:
                            self.results[row['index']] = row
                    if stream.tell() == 0:
                        raise ValueError('empty checkpoint cannot be resumed')
                self.stream = self.path.open('a')
            else:
                self.stream = self.path.open('x')
                self._write(self.header)
            return self
        except BaseException:
            self.__exit__(None, None, None)
            raise

    def _write(self, row):
        self.stream.write(json.dumps(row, allow_nan=False, sort_keys=True) + '\n')
        self.stream.flush()
        os.fsync(self.stream.fileno())

    def append(self, row):
        if row['index'] in self.results:
            raise ValueError('duplicate completed index')
        self._write(row)
        self.results[row['index']] = row

    def __exit__(self, *_):
        if self.stream:
            self.stream.close()
        if self.lock:
            self.lock.close()


def summary(rows):
    rows = list(rows)
    return dict(completed=len(rows), failures=sum('error' in r for r in rows),
                **{key: sum(bool(r.get(key)) for r in rows) for key in
                   ('optimizer_success', 'accepted_numerical_joint', 'health_rejected', 'verification_queued')},
                scope='Finite local necessary-condition search only; no full-theory PASS')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--starts', type=int, default=128)
    parser.add_argument('--max-nfev', type=int, default=300)
    parser.add_argument('--workers', type=int, default=DEFAULT_WORKERS)
    parser.add_argument('--seed', type=int, default=20260910)
    parser.add_argument('--resume', action='store_true')
    parser.add_argument('--export-index', type=int)
    parser.add_argument('--candidate-out', type=Path)
    args = parser.parse_args()
    if min(args.starts, args.max_nfev, args.workers) < 1:
        parser.error('starts, max-nfev, and workers must all be positive')
    sources = source_hashes()
    runtime = dict(python=sys.version, **{p: version(p) for p in ('numpy', 'scipy', 'sympy', 'mpmath')})
    config = dict(starts=args.starts, max_nfev=args.max_nfev, seed=args.seed,
                  job_design='interleaved-log-uniform-v1-control-index0', health_screen=True)
    header = dict(type='header', schema=1, config=config, sources=sources, runtime=runtime)
    if args.export_index is not None:
        if args.candidate_out is None:
            parser.error('--export-index requires --candidate-out')
        with args.output.open() as stream:
            previous = json.loads(stream.readline())
        header['config'] = previous['config']
        with Checkpoint(args.output, header, True) as ck:
            row = ck.results[args.export_index]
            if not row.get('verification_queued'):
                raise ValueError('requested result is not queued for verification')
            with args.candidate_out.open('x') as stream:
                json.dump(row['candidate'], stream, allow_nan=False)
        print(f'EXPORTED={args.candidate_out}', flush=True)
        return
    with Checkpoint(args.output, header, args.resume) as ck:
        if any(type(i) is not int or not 0 <= i < args.starts for i in ck.results):
            raise ValueError('checkpoint contains out-of-range job indices')
        jobs = iter(make_job(i, args.seed) for i in range(args.starts) if i not in ck.results)
        with ProcessPoolExecutor(max_workers=args.workers, mp_context=multiprocessing.get_context('spawn')) as pool:
            pending = {}
            def submit_one():
                job = next(jobs, None)
                if job is not None:
                    pending[pool.submit(run_job, job, args.max_nfev, sources)] = job
            for _ in range(2 * args.workers):
                submit_one()
            while pending:
                finished, _ = wait(pending, return_when=FIRST_COMPLETED)
                for future in finished:
                    job = pending.pop(future)
                    # A broken process pool is fatal; do not mark its unfinished jobs completed.
                    row = future.result()
                    ck.append(row)
                    print('PROGRESS=' + json.dumps(dict(index=job['index'], **summary(ck.results.values()))), flush=True)
                    submit_one()
        if source_hashes() != sources:
            raise ValueError('sources changed during run; checkpoint is not resumable under new sources')
        print('SUMMARY=' + json.dumps(summary(ck.results.values())), flush=True)


if __name__ == '__main__':
    main()
