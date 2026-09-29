#!/usr/bin/env python3
# POST-HOC (after the C2 numbers were seen; not frozen): per (k, amplitude, IC) breakdown of the C2 (z = 1100) screen for the CENTRAL parameter set,
# because C_cosmology_growth.py prints only the first six detail lines per case.  Reports |delta_pol/delta_D| and the medium growth deviation.
import os, sys, math
import numpy as np
import cfg121_common as C
HERE = C.HERE
src = open(os.path.join(HERE, "C_cosmology_growth.py")).read().split("def load_pstar")[0]
ns = {"__name__": "c_solver", "__file__": os.path.join(HERE, "C_cosmology_growth.py")}
exec(compile(src, "C_cosmology_growth.py(solver part)", "exec"), ns)
run, OC = ns["run"], ns["OC"]
out = ["POST-HOC C2 by amplitude (central Q = kappa_I = 1); columns: |delta_pol/delta_D| (cold/eq), medium growth deviation (cold/eq)"]
for variant in ("V_U", "V_B"):
    for k in (0.01, 0.1, 1.0):
        for A in (1e-5, 1e-4, 1e-3):
            rf = run(k, A, "V_B", 0.0, 1.0, "cold", 5000.0, 1100.0)
            row = []
            for ic in ("cold", "eq"):
                r0 = run(k, A, variant, 1.0, 1.0, ic, 5000.0, 1100.0)
                rat = abs(r0["a"] ** 2 * r0["Ps"] / (1.5 * OC * r0["aD"]))
                row.append((rat, abs(r0["aD"] / rf["aD"] - 1)))
            line = f"  {variant} k={k:5.2f} A={A:.0e}: " + "  ".join(f"{ic}: {r[0]:.3e} / {r[1]:.2e}" for ic, r in zip(("cold", "eq"), row))
            print(line)
            out.append(line)
open(os.path.join(HERE, "posthoc_C2_by_amplitude.out"), "w").write("\n".join(out) + "\n")
