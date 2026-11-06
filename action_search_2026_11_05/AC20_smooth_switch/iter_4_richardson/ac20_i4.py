#!/usr/bin/env python3
"""AC20 iter_4: fresh-data Richardson C1 test (criteria iter_4_richardson/FROZEN_CRITERIA.md, 054b3bdec4).
Run from the repo root, one thread:
  OMP_NUM_THREADS=1 nice -n 15 python3 action_search_2026_11_05/AC20_smooth_switch/iter_4_richardson/ac20_i4.py
MUTATE (AC20_MUTATE=1): v3s's F through the statistic (must FAIL). kappa = 1/2 FITTED; not theory closed.
"""
import json, os, sys
sys.dont_write_bytecode = True
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from harness import ladder

MUT = os.environ.get("AC20_MUTATE") == "1"
tag = "ac20_i4_MUTATE" if MUT else "ac20_i4"
q = sp.symbols("q", positive=True)
f4 = -2 * q ** 7 + sp.Rational(15, 2) * q ** 6 - 10 * q ** 5 + 5 * q ** 4      # iter_3 m = 4 spline (scaled F/(gamma b^2))
fp4 = sp.lambdify(q, sp.diff(f4, q), "numpy")
assert abs(fp4(1.0) - 1.0) < 1e-12


def spline(bb):
    return lambda P: np.where(P >= bb, P, bb * fp4(np.minimum(np.asarray(P, float) / bb, 1.0)))


contact = lambda aa: (lambda P: P ** 3 * (P + 2 * aa) / (P + aa) ** 3)
kw = dict(Pi0f=lambda x: np.tanh(2 * x), v0f=lambda x: 0.2 * np.sin(x), t_meas=0.03)
Ns = (800, 1600, 3200, 6400, 12800)
rows = {"control_v3s": lambda P: P} if MUT else {
    "spline_b0.4": spline(0.4), "spline_b0.2": spline(0.2), "contact_a0.4": contact(0.4), "contact_a0.2": contact(0.2),
    "control_n3": lambda P: P ** 2, "control_v3s": lambda P: P}
num = {k: ladder(h, Ns=Ns, **kw) for k, h in rows.items()}
gr = {}
for k, L in num.items():
    D = [r["Dvx"] for r in L]; T = [r["t_inv"] for r in L]
    gr[k] = dict(D=D, T=T, Dinf=2 * D[-1] - D[-2], r=abs(D[-2]) / abs(D[-1]) if D[-1] else float("inf"),
                 rt=(T[-2] / T[-1]) if (T[-2] and T[-1]) else None)
ok = {}
if MUT:
    g_ = gr["control_v3s"]; yard = None
    ok["mutate_v3s_passes_C1"] = 1.6 <= g_["r"] <= 2.4 and g_["rt"] is not None and 0.9 <= g_["rt"] <= 1.1
    label = "MUTATE v3s: " + ("C1 PASS (control does NOT bite)" if ok["mutate_v3s_passes_C1"] else "C1 FAIL (bites)")
else:
    yard = abs(gr["control_n3"]["D"][-1])
    for k in ("spline_b0.4", "spline_b0.2", "contact_a0.4", "contact_a0.2"):
        g_ = gr[k]
        g_["C1"] = abs(g_["Dinf"]) <= 0.1 * yard and 1.6 <= g_["r"] <= 2.4 and g_["rt"] is not None and 0.9 <= g_["rt"] <= 1.1
        ok[f"C1_{k}"] = g_["C1"]
    c3 = gr["control_n3"]
    ok["control_n3_kink"] = 0.9 <= c3["r"] <= 1.1 and abs(c3["Dinf"]) >= 0.5 * abs(c3["D"][-1])
    ok["control_v3s_grows"] = gr["control_v3s"]["r"] < 0.9
    # S-a': contact 6, C^2 knot, degree 8
    cs = sp.symbols("c0:3"); f6 = q ** 6 * (cs[0] + cs[1] * q + cs[2] * q ** 2)
    sol = sp.solve([sp.Eq(sp.diff(f6, q, j).subs(q, 1), sp.diff(q ** 2 / 2, q, j).subs(q, 1)) for j in range(3)], cs, dict=True)
    f6s = sp.expand(f6.subs(sol[0])) if len(sol) == 1 else None
    fpp6 = sp.expand(sp.diff(f6s, q, 2))
    rts = [r for r in sp.Poly(fpp6, q).real_roots() if 0 < r < 1]
    pts = sorted(set([sp.Integer(0), sp.Integer(1)] + rts))
    convex6 = all(fpp6.subs(q, (pts[i] + pts[i + 1]) / 2) >= 0 for i in range(len(pts) - 1))
    ok["Sa6_C2_exists_unique_convex"] = len(sol) == 1 and bool(convex6)
    controls = ok["control_n3_kink"] and ok["control_v3s_grows"]
    sp_ok = ok["C1_spline_b0.4"] and ok["C1_spline_b0.2"]; ct_ok = ok["C1_contact_a0.4"] and ok["C1_contact_a0.2"]
    if not controls:
        label = "NO VERDICT (controls do not discriminate)"
    else:
        label = dict(v3s_spline="REPAIR (1D)" if sp_ok else "NOT A REPAIR",
                     AC2q_spline="REPAIR (1D)" if sp_ok else "NOT A REPAIR",
                     v3s_contact="REPAIR (1D)" if ct_ok else "NOT A REPAIR",
                     AC2q_contact="NOT A REPAIR (iter_2 C-e stands)",
                     m6_C2=dict(f=str(f6s), fpp=str(sp.factor(fpp6)), convex=bool(convex6)))
out = dict(mode="MUTATE" if MUT else "main", label=label, checks=ok, grades=gr, n3_yardstick=yard,
           note="kappa = 1/2 FITTED; not theory closed")
open(os.path.join(HERE, tag + ".json"), "w").write(json.dumps(out, indent=1, default=str) + "\n")
txt = "\n".join(f"{k}: {'ok' if v else 'FAIL'}" for k, v in ok.items())
for k, g_ in gr.items():
    txt += f"\n{k}: D " + ", ".join(f"{x:+.5f}" for x in g_["D"]) + f"; Dinf {g_['Dinf']:+.5f}; r {g_['r']:.3f}; t ratio {g_['rt']}"
txt += f"\nLABEL: {label}\n"
open(os.path.join(HERE, tag + ".out"), "w").write(txt); print(txt)
sys.exit(1 if (MUT and not ok["mutate_v3s_passes_C1"]) else 0)
