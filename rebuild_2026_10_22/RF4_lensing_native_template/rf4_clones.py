#!/usr/bin/env python3
"""RF4 (criteria 5632124ef4): more per-lens clones. SI3's si3_a2.py text with asserted replacements: clone count per sample, new seed, own file names. Nothing is written into SI3.
    OMP_NUM_THREADS=1 nice -n 15 python3 rf4_clones.py cat <work_dir>
    OMP_NUM_THREADS=1 nice -n 15 python3 rf4_clones.py measure <kids_source_cache> <work_dir> north|south
kappa = 1/2 FITTED; footings never pooled; cold dark energy is never a particle; not theory closed."""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
HERE = os.path.dirname(os.path.abspath(__file__)); SI3 = os.path.join(os.path.dirname(HERE), "SI3_nested_isolation"); A2 = os.path.join(SI3, "si3_a2.py"); sys.path.insert(0, SI3)
T = open(A2).read()
def rep(a, b, n=1):
    global T
    assert T.count(a) == n, (a[:80], T.count(a)); T = T.replace(a, b)
rep("AH = os.path.dirname(os.path.abspath(__file__))", f"AH = {SI3!r}")
rep("np.random.SeedSequence(SEED + 3).spawn(5))); KEEP, CAP = 4, 100000", 'np.random.SeedSequence(SEED + 44).spawn(5))); KEEPS, CAP = dict(S10=8, S20=4, S30=12, S_strict=16, S_x300=16), 100000')
rep("        rng = np.random.default_rng(SS[s]); idx = np.where(SAMP[s] & OKL)[0]; W, hw = VETO[s];", "        KEEP = KEEPS[s]; rng = np.random.default_rng(SS[s]); idx = np.where(SAMP[s] & OKL)[0]; W, hw = VETO[s];")
rep('amendment="A2"', 'amendment="RF4"')
T = T.replace("si3_cats_a2", "rf4_cats").replace('si3_a2_{REGION}', 'rf4_meas_{REGION}')
assert "rf4_meas_" in T and "rf4_cats" in T
sys.argv = [A2] + sys.argv[1:]
exec(compile(T[:T.index("else:\n    gs = open(SG).read()")], A2, "exec"), {"__file__": A2, "__name__": "__main__"})
