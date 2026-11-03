#!/usr/bin/env python3
"""BF3 report: H as f -> 0+ for selected forms, at Saturn's ell and a disc's ell. Gate 0 tests f = 0 exactly; this tests a trace of gas. kappa = 1/2 FITTED; not theory closed."""
import json, os
from bf3_common import *
sel = json.load(open(os.path.join(LANE, "bf3_final.json")))["selection"]; o = {}
for ft in FEET:
    a = A0[ft]; es = 9.58 * 149597870700.0 * a / C ** 2; ys = 1.32712440018e20 / (9.58 * 149597870700.0) ** 2 / a; ed = 5 * 3.0857e19 * a / C ** 2
    for x in sel:
        row = {}
        for lab, e, y in (("Saturn", es, ys), ("disc 5 kpc, y 1", ed, 1.0)):
            row[lab] = {f"{f:g}": float(H_of(x["s"], np.array([y]), np.array([e]), np.array([f]), x["fam"])[0]) for f in (0.0, 1e-15, 1e-12, 1e-6, 1e-3, 1e-2)}
        o[f"{ft}|W{x['w']} {x['fam']} {x['s']}"] = row; print(ft, x["s"][:60], {k: {q: round(v, 4) for q, v in r.items()} for k, r in row.items()})
json.dump(o, open(os.path.join(LANE, "bf3_fzero.json"), "w"), indent=0, sort_keys=True)
