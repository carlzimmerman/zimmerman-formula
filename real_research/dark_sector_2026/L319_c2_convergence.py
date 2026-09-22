#!/usr/bin/env python3
# L319 control C2 convergence: the v_k = 0 triggered-decay deviation from LCDM at z = 0 vs grid resolution N_A.
# Expected first-order discretisation (error ~ 1/N_A). Run from the repository root.
import os, sys, runpy, numpy as np
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "L319_lambda_triggered_kicked_decay.py")).read()
cut = src.split("# ============================================================================================ controls")[0]
for na in (300, 420, 600):
    os.environ["L319_NA"] = str(na)
    g = {"__name__": "c2", "__file__": os.path.join(os.path.dirname(os.path.abspath(__file__)), "L319_lambda_triggered_kicked_decay.py")}
    import io, contextlib
    with contextlib.redirect_stdout(io.StringIO()):
        exec(cut, g)
        one = np.ones(g["N_A"]); LC = g["run"](one, 0.0)
        sT, _ = g["surv_triggered"](0.9, 1); NK = g["run"](sT, 0.0)
    j = g["idx_z"](0.0)
    print(na, "max|ratio-1| at z=0:", float(np.max(np.abs(NK[:, j]/LC[:, j]-1))))
