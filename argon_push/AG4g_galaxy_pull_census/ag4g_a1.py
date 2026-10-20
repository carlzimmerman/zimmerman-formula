#!/usr/bin/env python3
"""AG4g ADDENDUM A1 (POST HOC): stage 2 with a mock-calibrated null (ADDENDUM_A1_POST_HOC.md, committed alone first).
The frozen ag4g.py definitions (data, fit, mock, props) are executed read-only; ag4g.py and its outputs are not touched.
Run: OMP_NUM_THREADS=1 nice -n 10 python3 ag4g_a1.py  ->  ag4g_a1.out, ag4g_a1_results.json.  kappa = 1/2 fitted; not theory closed."""
import json, math, os, sys
import numpy as np
from scipy.stats import rankdata

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = open(os.path.join(HERE, "ag4g_a1.out"), "w")
def P(*a):
    s = " ".join(str(x) for x in a); print(s); OUT.write(s + "\n"); OUT.flush()
src = open(os.path.join(HERE, "ag4g.py")).read()
body = src[src.index("LN10 = math.log(10.0)"):src.index("PR = props(D_)")]
pre = src[:src.index("MUT = os.environ.get")]                       # imports + CFG4_common path (no file writes)
ns = {"__file__": os.path.join(HERE, "ag4g.py"), "__name__": "ag4g_frozen", "P": P, "MUT": False, "FAILS": [], "check": None}
exec(compile(pre, "ag4g_head", "exec"), ns); ns["P"] = P; ns["MUT"] = False
exec(compile(body, "ag4g_body", "exec"), ns)
fit, mock, props, D_, NU1, A0C, NG = ns["fit"], ns["mock"], ns["props"], ns["D_"], ns["NU1"], ns["A0C"], ns["NG"]
P("AG4g A1 (POST HOC): stage 2 against a null calibrated on 200 law-true mocks; Holm 0.05")


def rho(x, y):
    ok = np.isfinite(x) & np.isfinite(y); x, y = x[ok], y[ok]
    rx = rankdata(x); ry = rankdata(y); rx = (rx - rx.mean()) / rx.std(); ry = (ry - ry.mean()) / ry.std()
    return float(np.mean(rx * ry))


PR = props(D_); TESTS = [(k, s) for k in PR for s in ("signed", "|pull|")]
def rhos(pulls):
    return np.array([rho(PR[k], pulls if s == "signed" else np.abs(pulls)) for k, s in TESTS])


def holm(p):
    order = np.argsort(p); m = len(p); adj = np.empty(m); run = 0.0
    for i, j in enumerate(order):
        run = max(run, min(1.0, (m - i) * p[j])); adj[j] = run
    return adj


def emp_p(rd, RM):
    med = np.median(RM, axis=0)
    return (1 + np.sum(np.abs(RM - med) >= np.abs(rd - med) - 1e-15, axis=0)) / (RM.shape[0] + 1)


pd = fit(D_, NU1, A0C); rd = rhos(pd)
RM = np.array([rhos(fit(mock(NU1, A0C, s), NU1, A0C)) for s in range(1, 201)])
p = emp_p(rd, RM); ph = holm(p)
P(f"\n{'property':18s} {'stat':7s} {'rho_data':>8s} {'mock median':>11s} {'mock sd':>7s} {'p_emp':>6s} {'Holm':>6s}")
rows = []
for i in np.argsort(p):
    k, s = TESTS[i]; lead = ph[i] < 0.05
    rows.append(dict(prop=k, stat=s, rho=float(rd[i]), mock_median=float(np.median(RM[:, i])), mock_sd=float(np.std(RM[:, i])), p=float(p[i]), p_holm=float(ph[i]), lead=bool(lead)))
    P(f"{k:18s} {s:7s} {rd[i]:+8.3f} {np.median(RM[:, i]):+11.3f} {np.std(RM[:, i]):7.3f} {p[i]:6.3f} {ph[i]:6.3f}{'  <- A1 LEAD' if lead else ''}")
leads = [f"{r['prop']} ({r['stat']})" for r in rows if r["lead"]]
fw = 0
for s in range(1001, 1051):
    fw += bool(np.any(holm(emp_p(rhos(fit(mock(NU1, A0C, s), NU1, A0C)), RM)) < 0.05))
k3 = fw / 50 <= 0.10
P(f"\nK3-A1: family-wise false-positive rate of the A1 null on 50 fresh law-true mocks = {fw}/50 -> {'PASS' if k3 else 'FAIL (A1 reading VOID)'}")
P(f"A1 leads: {leads or 'none'}" + ("" if k3 else "  (VOID: K3-A1 failed)"))
json.dump(dict(lane="AG4g-A1", post_hoc=True, rows=rows, leads=leads, K3_A1=fw / 50, K3_A1_pass=k3), open(os.path.join(HERE, "ag4g_a1_results.json"), "w"), indent=1)
OUT.close()
sys.exit(0 if k3 else 1)
