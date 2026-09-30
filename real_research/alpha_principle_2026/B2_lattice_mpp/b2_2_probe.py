#!/usr/bin/env python3
"""B2.2 stage-2 probe: can plain Metropolis tunnel between the three phases near the SU(2) triple point on a 4^4 lattice?  Phases classified per measurement:
I: X_A < 0.5 ; II: X_A >= 0.5 and X_F < 0.55 ; III: X_A >= 0.5 and X_F >= 0.55  (thresholds fixed here, before looking at the output, from the stage-1H table:
phase I has X_A about 0.3-0.45, phase II has X_A about 0.63-0.66 and X_F about 0.2-0.4, phase III has X_A about 0.6-0.7 and X_F about 0.75-0.9)."""
import sys
sys.dont_write_bytecode = True
import numpy as np
import b2_lib as B
GRP = sys.argv[5] if len(sys.argv) > 5 else "su2"
exe = B.build(GRP)
bF = float(sys.argv[1]) if len(sys.argv) > 1 else 0.54
grid = [float(x) for x in sys.argv[2].split(",")] if len(sys.argv) > 2 else [2.30, 2.35, 2.40, 2.45, 2.50, 2.55, 2.60]
L = int(sys.argv[3]) if len(sys.argv) > 3 else 4
nsw = int(sys.argv[4]) if len(sys.argv) > 4 else 50000
jobs = []
for bA in grid:
    for cold in (0, 1):
        jobs.append((exe, B.nonab_args(GRP, L, bF, bA, nsw, 2000, 999 + cold + int(bA * 1000), cold, 6, False), "su2probe"))
paths = B.run_many(jobs, 12, verbose=False)
k = 0
print(f"probe L={L} beta_F={bF}: fractions of measurements in phases I/II/III and number of phase changes (start hot/cold)")
for bA in grid:
    for cold in (0, 1):
        d = B.load(paths[k]); k += 1
        ph = np.where(d[:, 1] < 0.5, 0, np.where(d[:, 0] < 0.55, 1, 2))
        fr = [np.mean(ph == i) for i in range(3)]
        nch = int(np.sum(ph[1:] != ph[:-1]))
        print(f"  beta_A={bA:.3f} {'cold' if cold else 'hot '}: I {fr[0]:.3f}  II {fr[1]:.3f}  III {fr[2]:.3f}   changes {nch}")
