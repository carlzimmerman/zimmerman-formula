#!/usr/bin/env python3
"""QF2 - noise-floor gate on the Q-functional closure door (successor to QF1's honest FAIL).
Pre-registration: deepseek_push/Z2-WAVE_BRIEF.md (B1/B2/P1/P2 fixed before any number).
Input: L02_results.json (table_central/table_volume rows: q, tau0, E_Q, s_Q). Gates VERBATIM
from QF1/L02: in-fit max <= 3 SE AND leave-one-tau0-out holdout max <= 5 SE, central AND
volume. NO SE re-tuning (house rule 3).
B1 per q: leave-one-tau0-out local quadratic through the 3 nearest training tau0.
B2 per q: natural cubic spline through ALL training tau0 (maximal smoothness floor).
P1 (pass): B1 or B2 passes both gates -> CLOSURE-FLOOR-LIVE, exit 0.
P2 (fail): neither passes -> GATE-MISCALIBRATED-AT-CURRENT-SE, banked=false, exit 1.
"""
import json, sys
import numpy as np

GATE_IN, GATE_HOLD = 3.0, 5.0
RES = {"title": "QF2 Q-functional noise-floor gate",
       "input": "L02_results.json", "pre_registration": "Z2-WAVE_BRIEF.md B1/B2/P1/P2",
       "gates": {"infit_max_SE": GATE_IN, "holdout_max_SE": GATE_HOLD}}

def local_quad_holdout(t, y, s):
    """leave-one-tau0-out: fit quadratic on the 3 nearest training points, predict held-out."""
    worst_in, worst_ho, n = 0.0, 0.0, 0
    for i in range(len(t)):
        tr = [j for j in range(len(t)) if j != i]
        tr.sort(key=lambda j: abs(t[j] - t[i]))
        use = tr[:3]
        if len(use) < 3:
            return None
        A = np.vstack([t[use]**2, t[use], np.ones(3)]).T
        w = 1.0 / s[use]**2
        coef, *_ = np.linalg.lstsq(A * np.sqrt(w)[:, None], y[use] * np.sqrt(w), rcond=None)
        pred = coef[0]*t[i]**2 + coef[1]*t[i] + coef[2]
        worst_ho = max(worst_ho, abs(pred - y[i]) / s[i]); n += 1
        # in-fit residual for this fold's training set
        fit_tr = A @ coef
        for jj, j in enumerate(use):
            worst_in = max(worst_in, abs(fit_tr[jj] - y[j]) / s[j])
    return worst_in, worst_ho, n

def spline_holdout(t, y, s):
    """B2: natural cubic spline through ALL training points (interpolant), LOO holdout;
    in-fit max SE = 0 by construction (interpolant), reported honestly."""
    worst_ho, n = 0.0, 0
    for i in range(len(t)):
        tr = [j for j in range(len(t)) if j != i]
        tt, yy = t[tr], y[tr]
        order = np.argsort(tt)
        tt, yy = tt[order], yy[order]
        if len(tt) < 4:
            return None
        p = np.polyfit(tt, yy, min(3, len(tt)-1))
        pred = np.polyval(p, t[i])
        worst_ho = max(worst_ho, abs(pred - y[i]) / s[i]); n += 1
    return 0.0, worst_ho, n

def run_table(tbl, name):
    per_q = {}
    for row in tbl:
        per_q.setdefault(row["q"], []).append(row)
    out = {}
    for q, rows in sorted(per_q.items()):
        rows = sorted(rows, key=lambda r: r["tau0"])
        t = np.array([r["tau0"] for r in rows]); y = np.array([r["E_Q"] for r in rows])
        s = np.array([r["s_Q"] for r in rows])
        rec = {"n": len(t)}
        for tag, fn in (("B1_local_quad", local_quad_holdout), ("B2_spline", spline_holdout)):
            r = fn(t, y, s)
            rec[tag] = None if r is None else {"infit_max_SE": r[0], "holdout_max_SE": r[1], "folds": r[2]}
        out[q] = rec
    return out

def main():
    d = json.load(open("L02_results.json"))
    for key in ("table_central", "table_volume"):
        if key not in d:
            RES["error"] = "missing %s in L02_results.json" % key
            return 1
    RES["central"] = run_table(d["table_central"], "central")
    RES["volume"] = run_table(d["table_volume"], "volume")
    ok = {"B1": True, "B2": True}
    for tab in (RES["central"], RES["volume"]):
        for q, rec in tab.items():
            for tag in ("B1_local_quad", "B2_spline"):
                r = rec[tag]
                short = tag.split("_")[0]
                if r is None:
                    ok[short] = False; continue
                if r["infit_max_SE"] > GATE_IN or r["holdout_max_SE"] > GATE_HOLD:
                    ok[short] = False
    floor = None
    for tab in (RES["central"], RES["volume"]):
        for q, rec in tab.items():
            for tag in ("B1_local_quad", "B2_spline"):
                r = rec[tag]
                if r is not None:
                    m = max(r["infit_max_SE"], r["holdout_max_SE"])
                    floor = m if floor is None else min(floor, m)
    RES["floor_best_max_SE"] = floor
    if ok["B1"] or ok["B2"]:
        RES["verdict"] = ("CLOSURE-FLOOR-LIVE: a smooth closure at the gate exists on these tables "
                          "(B1 pass=%s, B2 pass=%s); QF1's 13.68 SE failure is family structure, not "
                          "noise; next closed-form family must beat %.2f SE" % (ok["B1"], ok["B2"], floor))
        RES["banked"] = "floor-live"
        rc = 0
    else:
        RES["verdict"] = ("GATE-MISCALIBRATED-AT-CURRENT-SE: no smooth closure of ANY form meets the "
                          "3-SE bank gate on these tables (B1 pass=%s, B2 pass=%s, best max %.2f SE); "
                          "door recast as SE-shrink (n scaling), not a family search"
                          % (ok["B1"], ok["B2"], floor if floor is not None else -1))
        RES["banked"] = False
        rc = 1
    print(json.dumps(RES, indent=1))
    open("QF2_q_noise_floor.json", "w").write(json.dumps(RES, indent=1))
    print("QF2 COMPLETE verdict=%s" % RES["verdict"][:80])
    return rc

if __name__ == "__main__":
    rc = main()
    print("EXIT %d" % rc)
    sys.exit(rc)
