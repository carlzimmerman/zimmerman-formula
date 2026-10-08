#!/usr/bin/env python3
"""CFG491 POST HOC (not in FROZEN_CRITERIA): leave-one-galaxy-out range of the data beta, and beta without the
X_i covariate, to see whether the EFE-leaning data beta rests on a few galaxies.  Reuses cfg491_threeway's functions
by exec of its definitions only (the main loop is not run).  Output: cfg491_posthoc_loo_POSTHOC.out / _results.json."""
import os, json, re
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, "cfg491_threeway.py")).read()
src = src.split("# ------------------------------------------------------------------------------------------------ controls")[0]
ns = {"__file__": os.path.join(HERE, "cfg491_threeway.py")}
exec(compile(src, "cfg491_defs", "exec"), ns)
CS, AF, template, beta = ns["CS"], ns["AF"], ns["template"], ns["beta"]
SAMPLE = ns["SAMPLE"]
go = (CS["V"] * 1e3) ** 2 / CS["R"]
L, R = [], {}
for foot in ("canonical", "alt"):
    T = template(CS, AF[foot]); k = np.where(T["keep"])[0]
    b = beta(CS, go, AF[foot], T)
    loo = np.array([beta(CS, go, AF[foot], T, gal_idx=np.delete(k, j)) for j in range(len(k))])
    jmax = int(np.argmax(np.abs(loo - b)))
    _, Rm = beta(CS, go, AF[foot], T, return_all=True)
    A = np.vstack([np.ones(len(k)), T["D"][k]]).T
    b_nox = float(np.linalg.lstsq(A, Rm[k], rcond=None)[0][1])
    from scipy.stats import spearmanr
    rho, p = spearmanr(T["D"][k], Rm[k])
    R[foot] = dict(beta=b, loo_min=float(loo.min()), loo_max=float(loo.max()), most_influential=SAMPLE[k[jmax]]["name"],
                   beta_without_X=b_nox, spearman_D_R=float(rho), spearman_p=float(p))
    L.append(f"[{foot}] beta {b:+.3f}; leave-one-out range [{loo.min():+.3f}, {loo.max():+.3f}] (most influential {SAMPLE[k[jmax]]['name']});"
             f" beta without the X_i covariate {b_nox:+.3f}; Spearman(D_i, R_i) rho {rho:+.3f} p {p:.3f}")
L.append("POST HOC, not a verdict. MOND predicts beta ~ +1 (diluted by e errors; mock median +0.95..+1.17); the framework predicts 0.")
print("\n".join(L))
open(os.path.join(HERE, "cfg491_posthoc_loo_POSTHOC.out"), "w").write("\n".join(L) + "\n")
json.dump(R, open(os.path.join(HERE, "cfg491_posthoc_loo_POSTHOC_results.json"), "w"), indent=1)
