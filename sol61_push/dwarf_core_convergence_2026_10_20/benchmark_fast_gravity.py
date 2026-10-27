"""Bounded force-kernel timing/accuracy probe, with no physical time evolution.

Set FAST_GRAVITY_LIBRARY to an explicitly built fast_gravity library. This
script never compiles or installs dependencies. Default sizes include stars
at the historical cold-to-star particle count ratio. Thirty-second alarm cap.
"""
import os
for name in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS'):
    os.environ[name] = '1'
import argparse
import ctypes
import json
from pathlib import Path
import platform
import resource
import signal
import time

import numpy as np
from fast_gravity import gravity, backend_metadata, G


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--sizes', default='2304,4608,9216')
    parser.add_argument('--repeats', type=int, default=3)
    parser.add_argument('--output')
    args = parser.parse_args()
    signal.alarm(30)
    sizes = [int(value) for value in args.sizes.split(',')]
    if min(sizes) < 2 or max(sizes) > 20000 or not 1 <= args.repeats <= 5:
        raise ValueError('bounded sizes2..20000 and repeats1..5 required')
    old_path = Path(__file__).resolve().parent.parent / 'isolated_host_dwarf_2026_10_19' / 'direct_gravity.dylib'
    old = ctypes.CDLL(str(old_path))
    array = np.ctypeslib.ndpointer(dtype=np.float64, flags='C_CONTIGUOUS')
    old.gravity_kernel.argtypes = [array, array, ctypes.c_size_t, ctypes.c_double,
                                  ctypes.c_double, array, ctypes.POINTER(ctypes.c_double)]
    old.gravity_kernel.restype = ctypes.c_int
    rng, results = np.random.default_rng(9547), []
    started = time.monotonic()
    for count in sizes:
        x = rng.normal(size=(count, 3)) * [1200., 700., 400.]
        m = rng.uniform(.3, 3., count) * 4000.
        aold, Uold = np.empty_like(x), ctypes.c_double()
        timings = []
        for _ in range(args.repeats):
            tick = time.perf_counter()
            status = old.gravity_kernel(x, m, count, 20., G, aold, ctypes.byref(Uold))
            timings.append(time.perf_counter() - tick)
            if status: raise RuntimeError('historical reference failed')
        historical = float(np.median(timings))
        for threads in (1, 2, 4):
            gravity(x, m, 20., threads=threads)  # One unmeasured warm call.
            timings = []
            for _ in range(args.repeats):
                tick = time.perf_counter()
                a, U, phi = gravity(x, m, 20., threads=threads)
                timings.append(time.perf_counter() - tick)
            elapsed = float(np.median(timings))
            per_particle = np.linalg.norm(a - aold, axis=1) / np.maximum(np.linalg.norm(aold, axis=1), 1.e-300)
            maximum_error = float(np.max(per_particle))
            energy_error = abs(U / Uold.value - 1.)
            forces = m[:, None] * a
            force_scale = np.sum(np.linalg.norm(forces, axis=1))
            torque_scale = np.sum(np.linalg.norm(x, axis=1) * np.linalg.norm(forces, axis=1))
            row = dict(N=count, threads=threads, historical_seconds=historical,
                       seconds=elapsed, speedup_vs_historical=historical / elapsed,
                       max_vector_relative_force_error=maximum_error,
                       relative_potential_energy_error=energy_error,
                       normalized_momentum_force_defect=float(np.linalg.norm(forces.sum(axis=0)) / force_scale),
                       normalized_torque_defect=float(np.linalg.norm(np.cross(x, forces).sum(axis=0)) / torque_scale))
            if maximum_error >= 1.e-12 or energy_error >= 1.e-12:
                raise AssertionError('force/potential accuracy gate failed')
            results.append(row)
    result = dict(kind='bounded synthetic full-3D force benchmark; no time evolution',
                  backend=backend_metadata(), reference_library=str(old_path),
                  seed=9547, repeats=args.repeats, results=results,
                  wall_seconds=time.monotonic() - started,
                  observed_peak_RSS_native_units=int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss),
                  RSS_units='bytes on Darwin, KiB on Linux',
                  software=dict(python=platform.python_version(), numpy=np.__version__),
                  nonclaims=['No end-to-end simulation speed guarantee', 'No bitwise historical trajectory identity',
                             'No continuum or physical convergence result'])
    encoded = json.dumps(result, indent=2, allow_nan=False) + '\n'
    if args.output: Path(args.output).write_text(encoded)
    print(encoded)
    signal.alarm(0)


if __name__ == '__main__':
    main()
