#!/usr/bin/env python3
"""CFG191_s5c_picard_check -- convergence check of the tier-2 AQUAL Picard solver (s5b uses 140 iterations; its own residual does not reach 2e-4).
Loads the solver definitions from CFG191_s5b_pipeline_tier2.py (my own file, text up to its 'run' marker) and compares the radial boost after
60 / 140 / 300 / 600 iterations, for every (kernel, footing) at g_ext 1.778e-10.  Pass: max relative change of B_r between 140 and 600 iterations
< 0.5% for 1e-2 < r < 1e2 r_M (the range where wide-binary separations live).  MUTATE=1: 3 iterations only -> must fail."""
import warnings; warnings.filterwarnings("ignore")
import sys, os
sys.dont_write_bytecode = True
import numpy as np
from CFG191_common import Run, HERE
src = (HERE/"CFG191_s5b_pipeline_tier2.py").read_text().split("# ---------------------------------------------------------------- run")[0]
_mut = os.environ.pop("MUTATE", None)          # the s5b head must not think it is in MUTATE mode
exec(compile(src, "s5b_head", "exec"))
if _mut is not None: os.environ["MUTATE"] = _mut
R = Run("CFG191_s5c_picard_check", "AQUAL Picard convergence of the tier-2 solver")
NIT = 3 if R.mutate else 140
worst = 0.0
for ker in (KP2, KRAR):
    for foot, a0 in A0.items():
        ye = float(ker.y_of_x(1.778e-10/a0)); ref = boost_r(solve_aqual(ker, ye, n_iter=600, tol=1e-12)[0]); m = (r > 1e-2) & (r < 1e2)
        out = {}
        for n in (60, NIT, 300):
            out[n] = float(np.max(np.abs(boost_r(solve_aqual(ker, ye, n_iter=n, tol=1e-12)[0])[m]/ref[m] - 1)))
        R.p(f"  {ker.name:7s} {foot:9s}: max |B(n)/B(600)-1| for 1e-2<r<1e2: " + ", ".join(f"n={n}: {v:.2e}" for n, v in out.items()))
        worst = max(worst, out[NIT])
R.check("Picard solutions at %d iterations agree with 600 iterations to < 0.5%% in 1e-2 < r < 1e2 r_M" % NIT, worst < 5e-3, f"worst {worst:.2e}")
R.finish()
