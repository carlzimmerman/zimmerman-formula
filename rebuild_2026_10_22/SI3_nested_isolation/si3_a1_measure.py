#!/usr/bin/env python3
"""SI3 AMENDMENT A1 (post-result, reported only): the frozen I points re-stacked with their sums kept per bin of source coverage c. si3_hole.py's own text with asserted replacements.
    OMP_NUM_THREADS=1 nice -n 15 python3 si3_a1_measure.py <kids_source_cache> <work_dir> north|south
kappa = 1/2 FITTED; footings never pooled."""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
import numpy as np
AHERE = os.path.dirname(os.path.abspath(__file__)); SH = os.path.join(AHERE, "si3_hole.py")
CEDGES = np.array([0, 0.2, 0.4, 0.5, 0.6, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1.0, 1.05, 1.1, 1.15, 1.2, 1.3, 1.4, 1.6, 2.0, np.inf]); NC = len(CEDGES) - 1


def a1_nbar(lz, lM, LBIN, ldec, NNtot):
    """mean background-source pair count per cell (0.01 in z, 0.1 dex in M_gal) over S10 lenses; field factors making lenses average 1 in north and south."""
    cell = np.clip((lz / 0.01).astype(int), 0, 59) * 40 + np.clip(((np.log10(lM) - 8.0) / 0.1).astype(int), 0, 39); ok = (LBIN >= 0) & (LBIN < 4); n = np.bincount(cell[ok], minlength=2400).astype(float); s = np.bincount(cell[ok], NNtot[ok], minlength=2400)
    NBAR = np.where(n > 0, s / np.where(n > 0, n, 1.0), np.nan); north = ldec > -15.0; f = NNtot / NBAR[cell]
    return NBAR, cell, {"north": float(np.mean(f[ok & north])), "south": float(np.mean(f[ok & ~north]))}


if __name__ == "__main__":
    src = open(SH).read(); src = src[:src.index('if __name__ == "__main__":')]
    def rep(a, b):
        global src
        assert src.count(a) == 1, a[:80]; src = src.replace(a, b)
    rep('WF = os.path.join(WORK, f"si3_hole_{REGION}.npz"); CATS = [f"I_{s}" for s in SAMPLES] + [f"R_{s}" for s in SAMPLES]',
        'WF = os.path.join(WORK, f"si3_a1_{REGION}.npz"); CATS = [f"I_{s}" for s in SAMPLES]; NBAR, LCELL, FREG = a1_nbar(lz, lM, LBIN, ldec, np.load(os.path.join(DATA, "cfg110_perlens.npz"))["NN"].sum(1))')
    rep('SUM.setdefault(f"{name}_{k}", np.zeros((2, 50, 4, 15)))', 'SUM.setdefault(f"{name}_{k}", np.zeros((2, 50, 4, NC, 15)))')
    rep('        for c0 in range(start, len(ra), CH):\n', '        SUM.setdefault(f"{name}_n", np.zeros((2, 50, 4, NC)))\n        for c0 in range(start, len(ra), CH):\n')
    rep('ix = (half[c0:c1], pa[c0:c1], lb[c0:c1])\n', 'cj = np.digitize(m["NN"].sum(1) / (NBAR[LCELL[j]] * FREG[REGION]), CEDGES) - 1; ix = (half[c0:c1], pa[c0:c1], lb[c0:c1], cj); np.add.at(SUM[f"{name}_n"], ix, 1.0)\n')
    G = {"__file__": SH, "__name__": "si3_hole_a1", "a1_nbar": a1_nbar, "CEDGES": CEDGES, "NC": NC}; exec(compile(src, SH, "exec"), G)
    G["run_measure"](sys.argv[1], sys.argv[2], sys.argv[3])
