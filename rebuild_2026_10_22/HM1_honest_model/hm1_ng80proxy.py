#!/usr/bin/env python3
"""HM1: no z = 0 ng 80 table exists at 1e12. Reported only: ng 80 / ng 64 ratio of ln m at z_f, X48's nine seeds each, carried onto ZN2's z = 0 row. Not a grade. kappa = 1/2 FITTED; not theory closed."""
import importlib.util, json, math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); ZD = os.path.join(RB, "ZN1_zooms_to_z0"); _s = importlib.util.spec_from_file_location("zn1_measure", os.path.join(ZD, "zn1_measure.py")); ZM = importlib.util.module_from_spec(_s); _a = sys.argv; sys.argv = [_a[0]]; _s.loader.exec_module(ZM); sys.argv = _a; XG = ZM.XG
def st(ng):
    L = []; E = []
    for s in range(1, 10):
        f = os.path.join(RB, "X48_native_cf_zoom", "runs", f"M1e12_s{s}_ng{ng}", "snap_zf.npz")
        if not os.path.exists(f): continue
        A = np.load(f, allow_pickle=False); m = json.loads(str(A["meta"])); o = ZM.measure(A["x"], float(A["m"]), m["zf"], m["eps"]); L.append(o["lnm"]); E.append(o["x_edge"])
    return np.median(np.array(L), axis=0), len(L), min(E)
a, na, ea = st(80); b, nb, eb = st(64); d = a - b; Z = json.load(open(os.path.join(RB, "ZN2_native_profile_sparc_groups", "zn2_low_shapes.json"))); assert np.allclose(Z["x"], XG)
O = dict(Z); O["1e12"] = dict(Z["1e12"]); O["1e12"]["0.00"] = dict(Z["1e12"]["0.00"]); O["1e12"]["0.00"]["lnm"] = (np.array(Z["1e12"]["0.00"]["lnm"]) + d).tolist(); os.makedirs(os.path.join(HERE, "cache_gal"), exist_ok=True); json.dump(O, open(os.path.join(HERE, "cache_gal", "shapes_ng80proxy.json"), "w"))
XV = (0.02, 0.05, 0.1, 0.2, 0.5, 1.0); s = f"ng 80 n {na}, ng 64 n {nb}; ln m(ng 80) - ln m(ng 64) at z_f, x = r/R200: " + ", ".join(f"{x}: {float(np.interp(x, XG, d)):+.3f}" for x in XV); print(s); open(os.path.join(HERE, "hm1_ng80proxy.out"), "w").write(s + "\n")
