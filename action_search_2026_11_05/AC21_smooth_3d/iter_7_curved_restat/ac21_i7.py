#!/usr/bin/env python3
"""AC21 iter_7 (corrected statistic, fresh data; criteria iter_7_curved_restat/FROZEN_CRITERIA.md). Based on iter_2: curved switch surface (circle r = 1) in an axisymmetric 2D Lagrangian scheme; Richardson C1 statistic
with AC20 iter_4's lines (criteria ../FROZEN_CRITERIA.md 3891804624; rows amended to the iter_6 winner, 3ed022ae9f).
Run from the repo root, one thread:
  OMP_NUM_THREADS=1 nice -n 15 python3 action_search_2026_11_05/AC21_smooth_3d/iter_2_curved_numerics/ac21_i2.py
MUTATE (AC21_MUTATE=1): v3s's max form through the row statistic (must FAIL). kappa = 1/2 FITTED; not theory closed.
"""
import json, os, sys, time
sys.dont_write_bytecode = True
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
MUT = os.environ.get("AC21_MUTATE") == "1"
tag = "ac21_i7_MUTATE" if MUT else "ac21_i7"
form = json.load(open(os.path.join(HERE, "..", "iter_6_fast_decay", "form.json")))   # iter_6 winner
q = sp.Symbol("q")
# exact f'(q) piecewise: f'(q) = int_0^q f''
pieces = [(sp.Rational(lo), sp.Rational(hi), sp.sympify(e, locals={"q": q})) for lo, hi, e in form["pieces"]]
# f' per piece as an exact polynomial in the local variable t = q - lo, evaluated by Horner (np.polyval) in floats:
# the expanded global polynomial loses ~1e-4 to cancellation (smoke test before any graded run), the local form does not.
fp_pieces, acc = [], sp.Integer(0)
tl = sp.Symbol("t")
for lo, hi, e in pieces:
    anti = sp.integrate(e, (q, lo, q)) + acc
    loc = sp.Poly(sp.expand(anti.subs(q, tl + lo)), tl)
    coeffs = [float(c) for c in loc.all_coeffs()]
    fp_pieces.append((float(lo), float(hi), (lambda cf, lo_: (lambda qv: np.polyval(cf, qv - lo_)))(coeffs, float(lo))))
    acc = sp.expand(anti.subs(q, hi))
assert acc == 1, acc


def fprime(qv):
    qv = np.asarray(qv, float); out = np.where(qv >= 1.0, qv, 0.0)
    for lo, hi, fn in fp_pieces:
        m = (qv > lo) & (qv <= hi) if lo > 0 else (qv > 0) & (qv <= hi)
        out = np.where(m, fn(np.clip(qv, lo, hi)), out)
    return out


def form_h(bb):
    return lambda P: bb * fprime(np.asarray(P, float) / bb)


def run(N, hprime, Pi0f, v0f, t_meas=0.01, t_max=2.0, ncell=4, r_lo=0.25, r_hi=3.25):
    an = np.linspace(r_lo, r_hi, N + 1); am = 0.5 * (an[1:] + an[:-1]); da = an[1] - an[0]
    m = Pi0f(am) * (an[1:] ** 2 - an[:-1] ** 2) / 2          # area-weighted cell charge (per 2 pi)
    on = m > 0
    X = an.copy(); V = v0f(an)

    def acc(X):
        area = (X[1:] ** 2 - X[:-1] ** 2) / 2
        Pc = np.where(on, m / np.where(area > 0, area, np.inf), 0.0)
        h = np.where(on, hprime(np.maximum(Pc, 0.0)), 0.0)
        a_ = np.zeros_like(X)
        dxn = 0.5 * (X[2:] - X[:-2])
        a_[1:-1] = -(h[1:] - h[:-1]) / dxn
        return a_

    dt = 0.1 * da; nmeas = int(round(t_meas / dt)); dt_m = t_meas / nmeas
    tcur, t_inv, Dvx, step = 0.0, None, None, 0
    i0 = int(round((1.0 - r_lo) / da)); assert abs(an[i0] - 1.0) < 1e-12
    near = np.abs(am - 1.0) < 0.5
    while tcur < t_max - 1e-14:
        hs = dt_m if step < nmeas else dt
        k1x, k1v = V, acc(X)
        k2x, k2v = V + 0.5 * hs * k1v, acc(X + 0.5 * hs * k1x)
        k3x, k3v = V + 0.5 * hs * k2v, acc(X + 0.5 * hs * k2x)
        k4x, k4v = V + hs * k3v, acc(X + hs * k3x)
        X = X + hs / 6 * (k1x + 2 * k2x + 2 * k3x + k4x); V = V + hs / 6 * (k1v + 2 * k2v + 2 * k3v + k4v)
        tcur += hs; step += 1
        if step == nmeas:
            Rr = slice(i0, i0 + ncell + 1); L = slice(i0 - ncell, i0 + 1)
            Dvx = float(np.polyfit(X[Rr], V[Rr], 1)[0] - np.polyfit(X[L], V[L], 1)[0])
        if t_inv is None and np.any(np.diff(X)[near] <= 0):
            t_inv = tcur
        if t_inv is not None and Dvx is not None:
            break
    return dict(N=N, Dvx=Dvx, t_inv=t_inv)


Ns = (800, 1600, 3200, 6400, 12800)
Pi0 = lambda r: np.tanh(3 * (r - 1.0)); v0 = lambda r: 0.1 * np.cos(r - 1.0)
Pi0c = lambda r: np.tanh(3 * (r - 1.0)) ** 3
rows = ({"control_v3s": (lambda P: P, Pi0)} if MUT else
        {"form_b0.4": (form_h(0.4), Pi0), "form_b0.8": (form_h(0.8), Pi0), "control_n3": (lambda P: P ** 2, Pi0),
         "control_v3s": (lambda P: P, Pi0), "control_compatible_v3s": (lambda P: P, Pi0c)})
T0 = time.time(); gr = {}
for k, (h, p0) in rows.items():
    L = [run(N, h, p0, v0) for N in Ns]
    D = [r["Dvx"] for r in L]; T = [r["t_inv"] for r in L]
    gr[k] = dict(D=D, T=T, Dinf=2 * D[-1] - D[-2], r=abs(D[-2]) / abs(D[-1]) if D[-1] else float("inf"),
                 rt=(T[-2] / T[-1]) if (T[-2] and T[-1]) else None, no_crossing=all(t_ is None for t_ in T[-2:]))
    print(k, gr[k], round(time.time() - T0, 1), flush=True)


def c1_pass(g_, yard):
    tconv = g_["no_crossing"] or (g_["rt"] is not None and 0.9 <= g_["rt"] <= 1.1)
    return abs(g_["Dinf"]) <= 0.1 * yard and g_["r"] >= 1.6 and tconv


ok = {}
if MUT:
    g_ = gr["control_v3s"]
    tconv = g_["no_crossing"] or (g_["rt"] is not None and 0.9 <= g_["rt"] <= 1.1)
    ok["mutate_v3s_passes_C1_shape"] = g_["r"] >= 1.6 and tconv
    label = "MUTATE v3s: " + ("C1 PASS (control does NOT bite)" if ok["mutate_v3s_passes_C1_shape"] else "C1 FAIL (bites)")
else:
    yard = abs(gr["control_n3"]["D"][-1])
    for k in ("form_b0.4", "form_b0.8"):
        ok[f"C1_{k}"] = c1_pass(gr[k], yard)
    c3 = gr["control_n3"]
    ok["control_n3_kink"] = 0.9 <= c3["r"] <= 1.1 and abs(c3["Dinf"]) >= 0.5 * abs(c3["D"][-1])
    cv = gr["control_v3s"]
    ok["control_v3s_N3b_or_grows"] = (cv["rt"] is not None and 1.2 <= cv["rt"] <= 1.7) or cv["r"] < 0.9
    ok["control_compatible"] = abs(gr["control_compatible_v3s"]["D"][-1]) <= 0.1 * yard
    controls = ok["control_n3_kink"] and ok["control_v3s_N3b_or_grows"] and ok["control_compatible"]
    label = ("NO VERDICT (controls do not discriminate)" if not controls else
             ("C1 PASS on the curved interface, both rows" if ok["C1_form_b0.4"] and ok["C1_form_b0.8"] else "C1 FAIL on the curved interface"))
out = dict(mode="MUTATE" if MUT else "main", label=label, checks=ok, grades=gr, elapsed_s=round(time.time() - T0, 1),
           note="kappa = 1/2 FITTED; not theory closed")
open(os.path.join(HERE, tag + ".json"), "w").write(json.dumps(out, indent=1, default=str) + "\n")
txt = "\n".join(f"{k}: {'ok' if v else 'FAIL'}" for k, v in ok.items())
for k, g_ in gr.items():
    txt += f"\n{k}: D " + ", ".join(f"{x_:+.5f}" for x_ in g_["D"]) + f"; Dinf {g_['Dinf']:+.5f}; r {g_['r']:.3f}; t ratio {g_['rt']}; T {g_['T']}"
txt += f"\nLABEL: {label}\n"
open(os.path.join(HERE, tag + ".out"), "w").write(txt)
print(txt)
if MUT:
    sys.exit(1 if label.endswith("(bites)") else 0)
