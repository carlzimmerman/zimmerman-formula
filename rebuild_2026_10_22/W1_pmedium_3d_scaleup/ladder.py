#!/usr/bin/env python3
"""Direct ladder runs (FROZEN_CRITERIA.md section 3) and the ENQUEUE commands for the rest.
  nice -n 15 /usr/bin/python3 ladder.py --direct     # every direct run, sequentially, one thread, peak footprint logged
  /usr/bin/python3 ladder.py --enqueue               # print the heavyq commands (this lane never runs them)"""
import argparse
import json
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
    for n, amp, footing, th, prio in QUEUED:
        nm = name(n, amp, footing)
        base = f"/usr/bin/python3 engine/pmedium3d.py --n {n} --amp {amp} --footing {footing} --threads {th} --outdir runs/ladder"
        print(f'python3 compute_queue/heavyq.py add --id W1_{nm} --cwd rebuild_2026_10_22/W1_pmedium_3d_scaleup \\\n'
              f'    --cmd "{base}" \\\n    --resume-cmd "{base} --resume" \\\n'
              f'    --est-gb EST --threads {th} --priority {prio} --done-file runs/ladder/{nm}/result.json \\\n'
              f'    --note "W1 lane ladder {nm}; ckpt CK MB"\n')


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--direct', action='store_true'); ap.add_argument('--enqueue', action='store_true'); a = ap.parse_args()
    if a.direct: direct()
    if a.enqueue: enqueue()
