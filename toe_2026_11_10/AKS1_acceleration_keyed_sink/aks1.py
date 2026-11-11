#!/usr/bin/env python3
"""AKS1 main: the whole lane in order (FROZEN_CRITERIA.md s. 10, AMENDMENT_A1.md).

    nice python3 aks1.py              # symbolic part, rows (resumable), known answers, grade (about 1 h on 5 workers)
    python3 aks1.py --grade-only      # re-grade from runs/*.json, aks1_sym.json, aks1_ka.json (seconds)
Set AKS1_SNAP to a folder outside the repo to keep the snapshots. Adopts nothing. kappa = 1/2 FITTED; not theory closed.
"""
import os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))


def sh(*args):
    print('+', ' '.join(args), flush=True)
    subprocess.run([sys.executable, *args], cwd=HERE, check=True)


if __name__ == '__main__':
    if '--grade-only' not in sys.argv:
        sh('aks1_sym.py')
        sh('aks1_run.py', '--workers', os.environ.get('AKS1_WORKERS', '5'))
        sh('aks1_ka.py')
    sh('aks1_grade.py')
