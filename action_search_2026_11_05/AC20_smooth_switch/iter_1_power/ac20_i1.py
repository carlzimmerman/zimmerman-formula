#!/usr/bin/env python3
"""AC20 iter_1: pure-power stiffness F = (gamma_n/n) max(Pi,0)^n, n = 3, 4 (criteria iter_1_power/FROZEN_CRITERIA.md).
Run from the repo root, one thread:
  OMP_NUM_THREADS=1 nice -n 15 python3 action_search_2026_11_05/AC20_smooth_switch/iter_1_power/ac20_i1.py
MUTATE (AC20_MUTATE=1): n = 2 through the same grader; (a) must FAIL. Outputs ac20_i1[_MUTATE].json/.out.
kappa = 1/2 FITTED; not theory closed.
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
tag = "ac20_i1_MUTATE" if MUT else "ac20_i1"
NS = (2,) if MUT else (3, 4)
ok, res = {}, {}

# ---------------- P-a, P-b: sympy ----------------
x, xs = sp.symbols("x x_s", real=True)   # real, as AC16 (positive x, x_s made sympy drop the Heaviside jump: bookkeeping fix)
c1, g, Pi = sp.symbols("c1 gamma_n Pi", positive=True)
for n in (2, 3, 4):
    Fp = g * sp.Max(c1 * (x - xs), 0) ** (n - 1)          # F'(Pi(x)) at a transverse zero
    fx = -sp.diff(Fp, x)
    jump = sp.limit(fx, x, xs, "+") - sp.limit(fx, x, xs, "-")
    res[f"Pa_jump_n{n}"] = str(sp.simplify(jump))
    ok[f"Pa_n{n}"] = (sp.simplify(jump) == 0) if n >= 3 else (sp.simplify(jump + g * c1) == 0)
    F = g / n * Pi ** n
    p = sp.simplify(Pi * sp.diff(F, Pi) - F)
    c2 = sp.simplify(Pi * sp.diff(F, Pi, 2))
    c = sp.sqrt(c2)
    w = sp.simplify(2 * c / (n - 1)) if n > 1 else None
    # (v, w) system: w_t + v w_x + (Pi w'(Pi)) v_x = 0 ; v_t + v v_x + (dF'/dw) w_x = 0
    Piw = sp.simplify(Pi * sp.diff(w, Pi))
    dFdw = sp.simplify(sp.diff(sp.diff(F, Pi), Pi) / sp.diff(w, Pi))
    kexp = sp.Rational(n - 1, 2)
    ok[f"Pb_n{n}"] = (sp.simplify(p - g * sp.Rational(n - 1, n) * Pi ** n) == 0
                      and sp.simplify(c2 - g * (n - 1) * Pi ** (n - 1)) == 0
                      and sp.simplify(Piw - kexp * w) == 0 and sp.simplify(dFdw - kexp * w) == 0)
    res[f"Pb_n{n}"] = dict(p=str(p), c2=str(c2), w=str(w), Pi_dw=str(Piw), dFp_dw=str(dFdw), k=str(kexp))
ok["Pb_n3_burgers"] = sp.Rational(3 - 1, 2) == 1          # k = 1: lambda_+- = v +- w = r, s exactly

# ---------------- P-c: numerics ----------------
d = np.sqrt(2.0)                    # n = 3, gamma_3 = 1, c1 = tanh'(0) = 1
pred_dvx = -d ** 2 * 0.05 / (1 - d ** 2 * 0.05 ** 2)
pred_tinv = 1 / d
hp = {2: lambda P: P, 3: lambda P: P ** 2, 4: lambda P: P ** 3}
num = {n: ladder(hp[n]) for n in sorted(set(NS) | {2})}
res["numerics"] = {str(k): v for k, v in num.items()}
res["pred_n3"] = dict(dvx=pred_dvx, t_inv=pred_tinv)


def ratio_last(lst, key):
    a_, b_ = lst[-2][key], lst[-1][key]
    return (a_ / b_) if (a_ and b_) else None


A = {}
for n in NS:
    L = num[n]
    dv = [r["Dvx"] for r in L]; ti = [r["t_inv"] for r in L]
    rt = ratio_last(L, "t_inv")
    tconv = rt is not None and 0.9 <= rt <= 1.1
    if n == 3:
        c_dv = abs(dv[-1] - pred_dvx) <= 0.15 * abs(pred_dvx) and abs(dv[-1] - dv[-2]) <= 0.05 * abs(dv[-2])
        c_t = tconv and 0.6 <= ti[-1] <= 0.85
        ok["Pc_n3_kink"] = c_dv; ok["Pc_n3_tinv"] = c_t
        A[n] = "FAIL (Lipschitz only: velocity-slope jump at the switch label for t > 0)" if (c_dv and ok["Pa_n3"]) else "UNDECIDED"
    elif n == 4:
        c_dv = abs(dv[-1]) <= 0.1 * abs(pred_dvx) and abs(dv[-1]) < abs(dv[-2])
        ok["Pc_n4_smooth"] = c_dv; ok["Pc_n4_tinv"] = tconv
        A[n] = "PASS (1D C1)" if (c_dv and tconv and ok["Pa_n4"] and ok["Pb_n4"]) else "FAIL"
    elif n == 2:   # MUTATE run: n = 2 through the n = 4 smoothness test
        c_dv = abs(dv[-1]) <= 0.1 * abs(pred_dvx) and abs(dv[-1]) < abs(dv[-2])
        A[n] = "PASS (1D C1)" if (c_dv and tconv) else "FAIL"
# control (always): n = 2 t_inv falls by sqrt 2
t2 = [r["t_inv"] for r in num[2]]
rat2 = [t2[i] / t2[i + 1] for i in range(len(t2) - 1)] if all(t2) else []
ok["Pc_control_n2_sqrt2"] = bool(rat2) and all(1.2 <= r <= 1.7 for r in rat2)
res["control_n2_ratios"] = rat2

# ---------------- P-d: statics (linearised screening length vs charge) ----------------
sites = {"floor_globular_minDP_inside_Lstar": 0.084, "cassini_min_canonical": 0.0055, "cassini_min_alt": 0.0062,
         "sun_canonical": 0.0447, "sun_alt": 0.0514, "NGC2419_inside_Lstar": 2.5}
Bd = {}
for n in NS:
    rows = {}
    for k, P_ in sites.items():
        # L_eff^2 / L_v3s^2 with gamma_n fixed so L_eff(0.084) = floor:  (Pi/Pi_ref)^(n-2)
        rows[k] = (P_ / 0.084) ** ((n - 2) / 2.0) - 1.0
    worst = max(abs(v) for v in rows.values())
    Bd[n] = dict(rel_change_L_eff=rows, worst=worst, label="PRESERVED" if worst <= 1e-3 else "CHANGED")
res["Pd"] = {str(k): v for k, v in Bd.items()}

labels = {str(n): dict(a=A[n], b=Bd[n]["label"],
                       repair=(A[n].startswith("PASS") and Bd[n]["label"] == "PRESERVED")) for n in NS}
out = dict(mode="MUTATE" if MUT else "main", labels=labels, checks=ok, results=res,
           note="kappa = 1/2 FITTED; not theory closed")
open(os.path.join(HERE, tag + ".json"), "w").write(json.dumps(out, indent=1, default=str) + "\n")
txt = "\n".join(f"{k}: {'ok' if v else 'FAIL'}" for k, v in ok.items())
for n in sorted(num):
    txt += f"\nn={n}: " + "; ".join(f"N{r['N']} dvx {r['Dvx']:.5f} t_inv {r['t_inv']}" for r in num[n])
txt += f"\npred n=3: dvx {pred_dvx:.5f}, t_inv {pred_tinv:.4f}; control n=2 ratios {rat2}\n"
txt += "\n".join(f"LABEL n={n}: (a) {labels[n]['a']}; (b) statics {labels[n]['b']} (worst {Bd[int(n)]['worst']:.3g}); repair {labels[n]['repair']}"
                 for n in labels) + "\n"
open(os.path.join(HERE, tag + ".out"), "w").write(txt)
print(txt)
fail_a = all(not labels[str(n)]["a"].startswith("PASS") for n in NS)
sys.exit(1 if (MUT and fail_a) else 0)
