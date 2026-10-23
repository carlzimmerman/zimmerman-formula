#!/usr/bin/env python3
"""Cost/footprint probe and partial resume test at a given n (FROZEN_CRITERIA.md 2.3/2.4 and 3).
A: engine --stop-after-steps S (checkpoint at step S, exit 75).  C: --stop-after-steps S/2, then --resume --stop-after-steps S.
Checkpoints A and C must be bit-identical (state arrays and metadata). Projects the full-run wall time from the timestep
rule's step count. Run: nice -n 15 /usr/bin/python3 probe.py --n 64 [--steps 200]. Writes probe_n<N>_<footing>.json."""
import argparse
import json
import re
import subprocess
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ENG = HERE / 'engine' / 'pmedium3d.py'


def predicted_steps(n, zi=1100, zend=10, cfl=.6, footing='canonical'):
    # constants only (no lattice), same formulas as Model.__init__; t0 sets ti in code units, so the alt footing takes more steps
    t0 = .012074272908402984 * (1 if footing == 'canonical' else np.sqrt(9.3603e-11 / 1.1312e-10)); H0 = 67.4 * 1000 / 3.085677581491367e22 * 365.25 * 86400 * 1e9
    Hi = H0 * np.sqrt(.315) * (1 + zi) ** 1.5 * t0; ti = 2 / (3 * Hi); ell = .0004404221297174536
    rhom = .315 * 3 * (67.4 * 1000 / 3.085677581491367e22) ** 2 / (8 * np.pi * 6.67430e-11) * 3.085677581491367e22 ** 3 / 1.98847e30
    RL = (3 * 1.0952264e7 / (4 * np.pi * rhom)) ** (1 / 3); box = 2 * np.pi * RL / (1 + zi) / ell; dx = box / n
    t = ti; end = ti * ((1 + zi) / (1 + zend)) ** 1.5; k = 0
    while t < end * (1 - 1e-12):
        A = (t / ti) ** (2 / 3); H = 2 / (3 * t); dt = min(cfl * np.sqrt(.005) / np.sqrt(1 + 12 / (A * dx) ** 2), .015 / H, end - t); t += dt; k += 1
    return k


def run(outdir, n, amp, footing, extra):
    cmd = ['/usr/bin/time', '-l', '/usr/bin/python3', str(ENG), '--n', str(n), '--amp', str(amp), '--footing', footing, '--threads', '1', '--outdir', str(outdir), *extra]
    env = {**__import__('os').environ, 'OMP_NUM_THREADS': '1', 'OPENBLAS_NUM_THREADS': '1', 'VECLIB_MAXIMUM_THREADS': '1'}
    t0 = time.time(); p = subprocess.run(cmd, capture_output=True, text=True, env=env); wall = time.time() - t0
    fp = re.search(r'(\d+)\s+peak memory footprint', p.stderr)
    init = re.search(r'initial state: .*, ([\d.]+)s', p.stdout)
    return dict(exit=p.returncode, wall=wall, peak_footprint_gb=int(fp.group(1)) / 1e9 if fp else None,
                init_seconds=float(init.group(1)) if init else None, log=p.stdout.strip().splitlines()[-3:])


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--n', type=int, default=64); ap.add_argument('--steps', type=int, default=200)
    ap.add_argument('--amp', type=float, default=.03); ap.add_argument('--footing', default='canonical'); a = ap.parse_args()
    base = HERE / 'runs' / 'probe' / f'n{a.n}_{a.footing}'
    S = a.steps
    rA = run(base / 'A', a.n, a.amp, a.footing, ['--stop-after-steps', str(S)])
    rC1 = run(base / 'C', a.n, a.amp, a.footing, ['--stop-after-steps', str(S // 2)])
    rC2 = run(base / 'C', a.n, a.amp, a.footing, ['--resume', '--stop-after-steps', str(S)])
    name = next(p.name for p in (base / 'A').iterdir())
    zA = np.load(base / 'A' / name / 'checkpoint.npz'); zC = np.load(base / 'C' / name / 'checkpoint.npz')
    same = all(np.array_equal(zA[k], zC[k]) and zA[k].dtype == zC[k].dtype for k in zA.files) and set(zA.files) == set(zC.files)
    ns = predicted_steps(a.n, footing=a.footing)
    per_step = (rA['wall'] - rA['init_seconds']) / S
    proj = rA['init_seconds'] + per_step * ns
    out = dict(criteria='FROZEN_CRITERIA.md 2.3 (partial resume) / 3 (64-cubed direct-run rule)', n=a.n, amp=a.amp, footing=a.footing, steps_probe=S,
               A=rA, C1=rC1, C2=rC2, checkpoint_bitidentical=bool(same), checkpoint_step=int(zA['step']), predicted_total_steps=ns,
               seconds_per_step=per_step, projected_full_wall_s=proj, direct_run_allowed=bool(proj <= 600 and max(rA['peak_footprint_gb'], rC2['peak_footprint_gb']) < 2))
    (HERE / f'probe_n{a.n}_{a.footing}.json').write_text(json.dumps(out, indent=1) + '\n')
    print(json.dumps({k: v for k, v in out.items() if k not in ('A', 'C1', 'C2')}, indent=1)); print(rA)


if __name__ == '__main__':
    main()
