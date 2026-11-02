#!/usr/bin/env python3
"""BF2 reported beside RQ3: groups at assumed f for P5-P8. Script bf2_supp.py's reading. kappa = 1/2 FITTED; not theory closed."""
import importlib.util as iu, json, os, types
from bf2_common import *
A = rq3(); O = {}
for t in ("P5", "P6", "P7", "P8"):
    sp = iu.spec_from_file_location(t, os.path.join(LANE, "candidates", t + ".py")); c0 = iu.module_from_spec(sp); sp.loader.exec_module(c0)
    for ft in FEET:
        for fx in (.3, .6, .85):
            cw = types.SimpleNamespace(g=lambda Q, fx=fx: c0.g(dict(Q, gg=fx * np.asarray(Q["gb"], float), r=np.where(np.isfinite(np.asarray(Q["r"], float)), Q["r"], 1e21))))
            r = A.rows_groups(cw, ft)["B1"]; O[f"{t}|{ft}|{fx}"] = r; print(f"{t} {ft} groups f {fx}: {r['label']} v {r.get('value'):+.3f} Z {r.get('Z'):+.2f}", flush=True)
json.dump(O, open(os.path.join(LANE, "bf2_supp2.json"), "w"), indent=0, sort_keys=True, default=float)
