#!/usr/bin/env python3
"""Direct ladder runs (FROZEN_CRITERIA.md section 3) and the ENQUEUE commands for the rest.
  nice -n 15 /usr/bin/python3 ladder.py --direct     # every direct run, sequentially, one thread, peak footprint logged
  /usr/bin/python3 ladder.py --enqueue               # print the heavyq commands (this lane never runs them)"""
import argparse
import json
import math
import re
import subprocess
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / 'runs' / 'ladder'
DIRECT = [(n, amp, 'canonical') for n in (8, 12, 16, 32, 64) for amp in (.001, .03)] + \
         [(n, amp, 'alt') for n in (8, 12, 16, 32) for amp in (.001, .03)]
QUEUED = [(64, .03, 'alt', 4, 259), (64, .001, 'alt', 4, 258), (128, .03, 'canonical', 8, 257), (128, .03, 'alt', 8, 256),
          (128, .001, 'canonical', 8, 255), (128, .001, 'alt', 8, 254)]


def name(n, amp, footing):
    return f"n{n}_{'weak' if amp == .001 else 'strong'}_{'can' if footing == 'canonical' else 'alt'}"


def direct():
    OUT.mkdir(parents=True, exist_ok=True); logf = OUT / 'ladder_log.json'
    log = json.loads(logf.read_text()) if logf.exists() else {}
    env = {**__import__('os').environ, 'OMP_NUM_THREADS': '1', 'OPENBLAS_NUM_THREADS': '1', 'VECLIB_MAXIMUM_THREADS': '1'}
    for n, amp, footing in DIRECT:
        nm = name(n, amp, footing)
        if (OUT / nm / 'result.json').exists() and nm in log: continue
        cmd = ['/usr/bin/time', '-l', '/usr/bin/python3', str(HERE / 'engine' / 'pmedium3d.py'), '--n', str(n), '--amp', str(amp),
               '--footing', footing, '--threads', '1', '--outdir', str(OUT)]
        t0 = time.time(); p = subprocess.run(cmd, capture_output=True, text=True, env=env); wall = time.time() - t0
        fp = re.search(r'(\d+)\s+peak memory footprint', p.stderr)
        log[nm] = dict(exit=p.returncode, wall_s=wall, peak_footprint_gb=int(fp.group(1)) / 1e9 if fp else None, tail=p.stdout.strip().splitlines()[-1:])
        logf.write_text(json.dumps(log, indent=1) + '\n')
        print(nm, log[nm], flush=True)


def enqueue():
    """est-gb = 1.2 x measured peak footprint (64^3: the canonical 64^3 full runs; 128^3: linear in n^3 through the
    32^3 and 64^3 peaks of every measured run: ladder, resume tests, probes), per FROZEN_CRITERIA.md 2.4. Checkpoint = 20 n^3 doubles."""
    log = json.loads((OUT / 'ladder_log.json').read_text())
    extra = {32: [v['peak_footprint_gb'] for v in json.loads((HERE / 'resume_test_n32.json').read_text())['runs'].values()],
             64: [json.loads((HERE / f'probe_n64_{fo}.json').read_text())[k]['peak_footprint_gb'] for fo in ('canonical', 'alt') for k in ('A', 'C1', 'C2')]}
    pk = lambda n: max([v['peak_footprint_gb'] for k, v in log.items() if k.startswith(f'n{n}_')] + extra[n])
    p32, p64 = pk(32), pk(64); slope = (p64 - p32) / (64 ** 3 - 32 ** 3); scaled = {64: p64, 128: p64 + slope * (128 ** 3 - 64 ** 3)}
    print(f'# measured peak footprint (ladder, resume tests, probes): 32^3 {p32:.3f} GB, 64^3 {p64:.3f} GB; 128^3 scaled {scaled[128]:.3f} GB\n')
    for n, amp, footing, th, prio in QUEUED:
        nm = name(n, amp, footing); est = math.ceil(12 * scaled[n]) / 10; ck = 20 * n ** 3 * 8 / 1e6
        # SIGTERM is honoured at step boundaries (the initial state is checkpointed at step 0). The three initial L-BFGS solves
        # took 17.7 s at 64^3 and are expected to take minutes at 128^3, which could outlast the default 300 s grace, so the
        # 128^3 jobs ask for 900 s.
        grace = ' --grace 900' if n >= 128 else ''
        base = f"/usr/bin/python3 engine/pmedium3d.py --n {n} --amp {amp} --footing {footing} --threads {th} --outdir runs/ladder"
        print(f'python3 compute_queue/heavyq.py add --id W1_{nm} --cwd rebuild_2026_10_22/W1_pmedium_3d_scaleup \\\n'
              f'    --cmd "{base}" \\\n    --resume-cmd "{base} --resume" \\\n'
              f'    --est-gb {est:.1f} --threads {th} --priority {prio} --done-file runs/ladder/{nm}/result.json{grace} \\\n'
              f'    --note "W1 lane ladder {nm}; checkpoint {ck:.0f} MB (+ final_state.npz {ck:.0f} MB)"\n')


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--direct', action='store_true'); ap.add_argument('--enqueue', action='store_true'); a = ap.parse_args()
    if a.direct: direct()
    if a.enqueue: enqueue()
