#!/usr/bin/env python3
"""ONE1 reported KiDS brackets added by AMENDMENT_A2 (1e39b56e01): X = 10.82 (PD1 A2's basin share, 5.41 x 2.0) and X = 5.41 (the cosmic
share). The frozen statistic, k fitted on the inner window, neighbours carrying the same share. Runs one1_kids.py's set-up and
known answers read-only (everything before its primary reading), then these two readings only. Reported, never graded.
    python3 one1_kids_brackets.py -> one1_kids_brackets.json / one1_kids_brackets.out
kappa = 1/2 FITTED; not theory closed. Adopts nothing."""
import os, json
HERE = os.path.dirname(os.path.abspath(__file__)); src = open(os.path.join(HERE, "one1_kids.py")).read()
pre = src[:src.index("# ---------------- primary")]
ns = {"__file__": os.path.join(HERE, "one1_kids.py"), "__name__": "one1_kids_lib"}; exec(compile(pre, "one1_kids_prefix", "exec"), ns)
P, FOOT, FS, np = ns["P"], ns["FOOT"], ns["FS"], ns["np"]; ns["OUT"].clear()
P("ONE1 reported KiDS brackets (AMENDMENT_A2): X = 10.82 (PD1 A2 basin share) and 5.41 (cosmic share); frozen statistic; known answers as in one1_kids.out")
RES = dict(lane="ONE1", row="2 KiDS, reported brackets (A2)", note="reported, never graded; adopts nothing; kappa = 1/2 FITTED; not theory closed", readings={})
for Xb in (10.82, 5.41):
    P(f"\n=== BRACKET X = {Xb} (k fitted, neighbours)  {ns['tm']()}")
    lams = ns["lam_grid"](Xb); res, NB = ns["graded_set"](Xb, lams, ns["Htab_of"](Xb)); store = RES["readings"].setdefault(f"X {Xb}", {})
    ns["summarize"](f"X {Xb}", res, FOOT, store)
    for f in FOOT:
        g = [res[f][("KO1", 1.6, s)]["nb"] for s in ("all", "late", "early")]
        qe, ql = g[2], g[1]; sd = ns["jk"](qe["diff_l"] - ql["diff_l"]); dd = qe["diff"] - ql["diff"]
        ok = all(abs(q["diff"]) <= 2 * q["s_diff"] for q in g) and g[0]["chi2"] <= 9.49 and abs(dd) <= 2 * sd
        store[f"{f}|gate_reading"] = dict(z=[q["z"] for q in g], chi2=g[0]["chi2"], type_diff_z=dd / sd, reads="PASS" if ok else "FAIL")
        P(f"[{f}] X {Xb} at 1.6 R_h: z all / late / early {g[0]['z']:+.2f} / {g[1]['z']:+.2f} / {g[2]['z']:+.2f}; chi2 {g[0]['chi2']:.1f}; type difference {dd / sd:+.2f} sigma -> the frozen gate would read {'PASS' if ok else 'FAIL'}")
P("kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
def clean(o):
    if isinstance(o, dict): return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [clean(v) for v in o]
    if isinstance(o, np.ndarray): return [clean(v) for v in o.tolist()]
    if isinstance(o, (np.floating, float)): return float(o) if np.isfinite(o) else None
    if isinstance(o, np.integer): return int(o)
    if isinstance(o, np.bool_): return bool(o)
    return o
json.dump(clean(RES), open(os.path.join(HERE, "one1_kids_brackets.json"), "w"), indent=1)
open(os.path.join(HERE, "one1_kids_brackets.out"), "w").write("\n".join(ns["OUT"]) + "\n")
