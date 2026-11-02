#!/usr/bin/env python3
"""BF2 reported beside RQ3, never in place: groups and Milky Way, which have no gas on file, at stated assumed f. kappa = 1/2 FITTED; not theory closed."""
import importlib.util as iu, json, os, sys, types
from bf2_common import *
A = rq3(); O = {}
def load(t):
    sp = iu.spec_from_file_location(t, os.path.join(LANE, "candidates", t + ".py")); m = iu.module_from_spec(sp); sp.loader.exec_module(m); return m
for t in ("P1", "P2", "P3", "P4"):
    c0 = load(t)
    def at(fx):
        def g(Q):
            q = dict(Q); gb = np.asarray(Q["gb"], float); q["gg"] = fx * gb; q["r"] = np.where(np.isfinite(np.asarray(Q.get("r", gb * np.nan), float)), Q.get("r", gb * 0), 1e21); return c0.g(q)
        return types.SimpleNamespace(g=g, VERTICAL=("R",))
    for ft in FEET:
        for fx in (.3, .6, .85):
            r = A.rows_groups(at(fx), ft)["B1"]; O[f"{t}|{ft}|groups f{fx}"] = r; print(f"{t} {ft} groups f {fx}: {r['label']} v {r.get('value'):+.3f} Z {r.get('Z'):+.2f}", flush=True)
        for fx in (.05, .15):
            try:
                r = A.rows_mw(at(fx), ft); O[f"{t}|{ft}|MW f{fx}"] = r; print(f"{t} {ft} MW f {fx}: A15 {r['A15']['label']} K {r['A15'].get('value')} Z {r['A15'].get('Z')}; A16 {r['A16']['label']} {r['A16'].get('value')}; A17 {r['A17'].get('label')} {r['A17'].get('value')}", flush=True)
            except Exception as e: print(t, ft, fx, "MW", type(e).__name__, str(e)[:100], flush=True)
for t in ("P2", "P3"):
    c0 = load(t)
    for sc in (1.0, .5, .25):
        cw = types.SimpleNamespace(g=lambda Q, sc=sc: c0.g(dict(Q, gg=np.asarray(Q["gg"], float) * sc)))
        for ft in FEET:
            r = A.rows_lens(cw, ft)["A30"]; O[f"{t}|{ft}|A30 gas x{sc}"] = r; print(f"{t} {ft} A30 gas x {sc}: {r['label']} chi2 {r.get('value'):.1f} Z {r.get('Z'):+.2f}", flush=True)
json.dump(O, open(os.path.join(LANE, "bf2_supp.json"), "w"), indent=0, sort_keys=True, default=float)
