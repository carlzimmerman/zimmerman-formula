"""Optional GPU precision/timing probe, never a physical evolution run.

Default bounded set stops at16k cold-scale particles. Explicit --sizes may
probe32/64k only within the60second alarm. CPU comparison is always retained;
failure of1e-11 precision raises, rather than relaxing the requested gate.
"""
import os
for name in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS'):
    os.environ[name] = '1'
import argparse
import json
from pathlib import Path
import resource
import signal
import time

import numpy as np
from fast_gravity import gravity as cpu_gravity
from metal_gravity import gravity as gpu_gravity, backend_metadata


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--sizes', default='1024,4096,16384')
    parser.add_argument('--output')
    args = parser.parse_args()
    signal.alarm(60)
    sizes = [int(value) for value in args.sizes.split(',')]
    if min(sizes) < 2 or max(sizes) > 65536: raise ValueError('bounded sizes2..65536 required')
    metadata = backend_metadata()
    rng, rows = np.random.default_rng(99175), []
    started = time.monotonic()
    for count in sizes:
        x = rng.normal(size=(count, 3)) * [1200., 700., 400.] + [80000., -30000., 1000.]
        m = rng.uniform(.3, 3., count) * 4000.
        tick = time.perf_counter(); reference = cpu_gravity(x, m, 10., threads=4); cpu_time = time.perf_counter() - tick
        gpu_gravity(x, m, 10.)
        timings = []
        for _ in range(3):
            tick = time.perf_counter(); actual = gpu_gravity(x, m, 10.); timings.append(time.perf_counter() - tick)
        relative_force = np.linalg.norm(actual[0] - reference[0], axis=1) / np.maximum(np.linalg.norm(reference[0], axis=1), 1.e-100)
        phi_error = float(np.max(np.abs((actual[2] - reference[2]) / reference[2])))
        force_error = float(relative_force.max()); U_error = abs(actual[1] / reference[1] - 1.)
        forces = m[:, None] * actual[0]
        row = dict(N=count, cpu4_seconds=cpu_time, gpu_seconds=float(np.median(timings)),
                   speedup_over_cpu4=cpu_time / float(np.median(timings)),
                   max_vector_relative_force_error=force_error, max_relative_phi_error=phi_error,
                   relative_U_error=U_error,
                   normalized_momentum_defect=float(np.linalg.norm(forces.sum(axis=0)) / np.linalg.norm(forces, axis=1).sum()),
                   normalized_torque_defect=float(np.linalg.norm(np.cross(x - x[0], forces).sum(axis=0)) /
                        np.sum(np.linalg.norm(x - x[0], axis=1) * np.linalg.norm(forces, axis=1))),
                   precision_gate=bool(max(force_error, phi_error, U_error) < 1.e-11))
        rows.append(row)
        result = dict(backend=metadata, seed=99175, results=rows,
                      wall_seconds=time.monotonic() - started,
                      observed_peak_RSS_native_units=int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss),
                      nonclaims=['No production admission from timing alone', 'No native double precision',
                                 'No trajectory or continuum convergence result'])
        if args.output: Path(args.output).write_text(json.dumps(result, indent=2) + '\n')
        print(json.dumps(row), flush=True)
        if not row['precision_gate']: raise AssertionError('requested1e-11 precision gate FAILED')
    signal.alarm(0)


if __name__ == '__main__': main()
