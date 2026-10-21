#!/usr/bin/env python3
"""Run the FROZEN wide_binary_pipeline.main() exactly as on release day (`--catalog CSV`), with two MEMORY-ONLY patches forced
by the 1 GB per-process cap (CFG943 FROZEN_CRITERIA.md section 3):
  1. make_population(N > 250,000) is the frozen function called in 50,000-pair chunks (statistically identical; RNG stream differs);
  2. model_medians is cfg943_common.lean_model_medians (frozen bin_medians for the grid, identical medians; the 100-resample
     bootstrap of the master drawn in batches of 2; control K6).
Unpatched, the frozen pipeline peaks at about 2.1 GB (master) plus about 0.7 GB (master bootstrap).  Nothing frozen is edited.
  python3 -B cfg943_frozen_harness.py --catalog MOCK.csv  > log      (exit code = the pipeline's own)"""
import sys
sys.dont_write_bytecode = True
import numpy as np
import cfg943_common as C

W = C.W
_orig = W.make_population


def chunked(N, rng, **kw):
    if N <= C.CHUNK:
        return _orig(N, rng, **kw)
    return C.chunked_frozen_population(N, rng, **kw)          # frozen function in 50,000-pair chunks, all keys kept


if __name__ == "__main__":
    i = sys.argv.index("--catalog")
    path = sys.argv[i + 1]
    W.make_population = chunked
    W.model_medians = C.lean_model_medians
    C.start_watchdog()
    print("[CFG943 harness] frozen wide_binary_pipeline.main() with memory-only patches (chunked master, batched master bootstrap); MOCK catalogue")
    sys.argv = ["wide_binary_pipeline.py", "--catalog", path]
    code = 0
    try:
        W.main()
    except SystemExit as e:
        code = e.code if isinstance(e.code, int) else 1
    sys.stdout.flush()
    sys.stderr.write(f"[CFG943 harness] peak RSS {C.rss_mb():.0f} MB; pipeline exit code {code}\n")
    sys.exit(code)
