#!/usr/bin/env python3
"""CO2 check (reported): the two pinned fits replayed from their stored parameters and nuisances in a fresh process.
  python3 co2_check_replay.py   -> co2_check_replay.out
kappa = 1/2 FITTED; not theory closed."""
import os, sys, json
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from co2_fit import chi2E, f1a
L = []
for ft in ("canonical", "alt"):
    F = json.load(open(os.path.join(HERE, "parts", f"fit_{ft}.json"))); D = f1a.camb_theory(**F["pars"])
    g = f1a.PA(D, {k: np.array(v) for k, v in F["chi2"]["nuis"].items()}); e = chi2E(D["ee"])
    s = (f"{ft}: PA {g['PA']:.4f} (stored {F['chi2']['PA']:.4f}, d {g['PA'] - F['chi2']['PA']:+.1e}); chi2_E {e:.4f} (stored {F['chi2']['E_exact']:.4f}, d {e - F['chi2']['E_exact']:+.1e}); "
         f"D_L^EE at L 2..6 (muK^2): " + ", ".join(f"{v:.4f}" for v in D["ee"][2:7]))
    print(s, flush=True); L.append(s)
open(os.path.join(HERE, "co2_check_replay.out"), "w").write("\n".join(L) + "\n")
