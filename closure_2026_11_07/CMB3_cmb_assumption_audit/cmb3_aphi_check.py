#!/usr/bin/env python3
"""CMB3 post-run check (reported, not graded): chi2 at the F1A cold best fit vs A_phi 0.9-1.1 on the A2-T path. Usage: cmb3_aphi_check.py <lane dir>. kappa = 1/2 FITTED; not theory closed."""
import sys, json, numpy as np
sys.path.insert(0, sys.argv[1]); import cmb3
out = {}
for foot in ("canonical", "alt"):
    st = cmb3.stored(foot, "cold"); pr = st["pars"]; x0 = {k: np.array(v) for k, v in st["chi2"]["nuis"].items()}
    out[foot] = {a: cmb3.PA(cmb3.theory(pr, lens="tmpl", Aphi=a, foot=foot), x0)["PA"] - st["chi2"]["PA"] for a in (0.9, 0.95, 1.05, 1.1)}
    print(foot, out[foot], flush=True)
cmb3.dump("a2t_aphi_scan.json", dict(scan=out, note=cmb3.NOTE + "; post-run check of the A2-T cold fits, reported"))
