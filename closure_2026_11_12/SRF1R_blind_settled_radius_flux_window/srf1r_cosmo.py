#!/usr/bin/env python3
"""SRF1R stage 0b: CFG556's Om and rho_m, and the linear sigma at Gaussian smoothing 0.5 Mpc/h at each DESI bin (for bracket
B8), from SRH1's executed prefix (read-only). -> tables/cosmo.json. kappa = 1/2 FITTED; not theory closed; adopts nothing."""
import os, sys, json, math, io, contextlib, warnings
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
sys.dont_write_bytecode = True; warnings.filterwarnings("ignore")
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
SRC = os.path.join(REPO, "closure_2026_11_10", "SRH1_settled_radius_history", "srh1_hm.py"); code = open(SRC).read()
cut = code.index("# ------------------------------------------------------------------ checkpointed run\n")
G = {"__file__": SRC, "__name__": "srh1_lib"}
with contextlib.redirect_stdout(io.StringIO()): exec(compile(code[:cut], SRC, "exec"), G)
L, F = G["L"], G["F"]; k = np.geomspace(1e-4, 200, 20000); out = dict(Om=float(L["Om"]), RHO_M=float(L["RHO_M"]), h=float(L["h"]), sig_lin_0p5={})
for z in G["ZB"]:
    D = F["Dgrow"](z); P = L["P_lin"](k) * D * D
    out["sig_lin_0p5"][f"{z:.1f}"] = float(math.sqrt(np.trapz(P * np.exp(-k ** 2 * 0.25) * k ** 2, k) / (2 * math.pi ** 2)))
os.makedirs(os.path.join(HERE, "tables"), exist_ok=True); json.dump(out, open(os.path.join(HERE, "tables", "cosmo.json"), "w"), indent=1); print(out)
