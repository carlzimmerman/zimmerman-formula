#!/usr/bin/env python3
"""AC22: curved-interface (circle r = 1) C1/C2 ladder for AC21's iter_6 smoothing (criteria FROZEN_CRITERIA.md,
81636503ed). Scheme reused from AC21 iter_7 (axisymmetric Lagrangian charge-velocity, RK4). Run from repo root:
  nice -n 15 python3 action_search_2026_11_05/AC22_curved_ladder/ac22.py [--workers 4]
MUTATE (AC22_MUTATE=1): v3s's max form through the row C1 statistic (must FAIL, exit 1).
kappa = 1/2 FITTED; not theory closed."""
import json, os, sys, time, argparse
sys.dont_write_bytecode = True
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np
import sympy as sp
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
MUT = os.environ.get("AC22_MUTATE") == "1"
tag = "ac22_MUTATE" if MUT else "ac22"
FORM = json.load(open(os.path.join(HERE, "..", "AC21_smooth_3d", "iter_6_fast_decay", "form.json")))
q, tl = sp.Symbol("q"), sp.Symbol("t")
FP = []; acc_ = sp.Integer(0)
for lo, hi, e in [(sp.Rational(a), sp.Rational(b), sp.sympify(c, locals={"q": q})) for a, b, c in FORM["pieces"]]:
    anti = sp.integrate(e, (q, lo, q)) + acc_
    cf = [float(c) for c in sp.Poly(sp.expand(anti.subs(q, tl + lo)), tl).all_coeffs()]
    FP.append((float(lo), float(hi), cf)); acc_ = sp.expand(anti.subs(q, hi))
assert acc_ == 1


def fprime(qv):
    qv = np.asarray(qv, float); out = np.where(qv >= 1.0, qv, 0.0)
    for lo, hi, cf in FP:
        m = (qv > lo) & (qv <= hi) if lo > 0 else (qv > 0) & (qv <= hi)
        out = np.where(m, np.polyval(cf, np.clip(qv, lo, hi) - lo), out)
    return out


def hfun(kind, b):
    if kind == "form": return lambda P: b * fprime(np.asarray(P) / b)
    if kind == "n3": return lambda P: P ** 2
    if kind == "m4": return lambda P: P ** 3
    if kind == "v3s": return lambda P: P
    raise ValueError(kind)


def data(cfg, b):
    if cfg == "v3s": return lambda r: np.tanh(2.5 * (r - 1)) + 0.1 * np.sin(2 * (r - 1))
    if cfg == "ac2q": return lambda r: 2 * b * np.tanh(2.5 * (r - 1)) + 0.1 * b * np.sin(2 * (r - 1))
    if cfg == "compat": return lambda r: np.tanh(2.5 * (r - 1)) ** 3
    raise ValueError(cfg)


v0f = lambda r: 0.1 * np.cos(1.3 * (r - 1)) + 0.05


def run(args):
    name, kind, cfg, b, N = args
    hprime, Pi0f = hfun(kind, b), data(cfg, b)
    t_meas, t_max, r_lo, r_hi = 0.01, 2.0, 0.25, 3.25
    an = np.linspace(r_lo, r_hi, N + 1); am = 0.5 * (an[1:] + an[:-1]); da = an[1] - an[0]
    area0 = (an[1:] ** 2 - an[:-1] ** 2) / 2
    m = Pi0f(am) * area0; on = m > 0
    X = an.copy(); V = v0f(an)

    def acc(X):
        area = (X[1:] ** 2 - X[:-1] ** 2) / 2
        Pc = np.where(on, m / np.where(area > 0, area, np.inf), 0.0)
        h = np.where(on, hprime(np.maximum(Pc, 0.0)), 0.0)
        a_ = np.zeros_like(X); a_[1:-1] = -(h[1:] - h[:-1]) / (0.5 * (X[2:] - X[:-2]))
        return a_

    dt = 0.1 * da; nmeas = int(round(t_meas / dt)); dt_m = t_meas / nmeas
    i0 = int(round((1.0 - r_lo) / da)); assert abs(an[i0] - 1.0) < 1e-12
    near = np.abs(am - 1.0) < 0.5
    tcur, step, D, D2, T0, Th = 0.0, 0, None, None, None, None
    while tcur < t_max - 1e-14:
        hs = dt_m if step < nmeas else dt
        k1x, k1v = V, acc(X)
        k2x, k2v = V + 0.5 * hs * k1v, acc(X + 0.5 * hs * k1x)
        k3x, k3v = V + 0.5 * hs * k2v, acc(X + 0.5 * hs * k2x)
        k4x, k4v = V + hs * k3v, acc(X + hs * k3x)
        X = X + hs / 6 * (k1x + 2 * k2x + 2 * k3x + k4x); V = V + hs / 6 * (k1v + 2 * k2v + 2 * k3v + k4v)
        tcur += hs; step += 1
        if step == nmeas:
            R, L = slice(i0, i0 + 5), slice(i0 - 4, i0 + 1)
            D = float(np.polyfit(X[R], V[R], 1)[0] - np.polyfit(X[L], V[L], 1)[0])
            R2, L2 = slice(i0, i0 + 9), slice(i0 - 8, i0 + 1)
            D2 = float(2 * (np.polyfit(X[R2], V[R2], 2)[0] - np.polyfit(X[L2], V[L2], 2)[0]))
        J = ((X[1:] ** 2 - X[:-1] ** 2) / 2) / area0
        if Th is None and np.any(J[near] <= 0.5): Th = tcur
        if T0 is None and np.any(J[near] <= 0.0): T0 = tcur
        if T0 is not None and D is not None: break
    return dict(name=name, N=N, D=D, D2=D2, T0=T0, Th=Th)


Ns = (800, 1600, 3200, 6400, 12800, 25600, 51200)
ROWS = ({"control_v3s": ("v3s", "v3s", 0.0)} if MUT else {
    "form_v3s_b0.2": ("form", "v3s", 0.2), "form_v3s_b0.4": ("form", "v3s", 0.4), "form_v3s_b0.8": ("form", "v3s", 0.8),
    "form_ac2q_b0.2": ("form", "ac2q", 0.2), "form_ac2q_b0.4": ("form", "ac2q", 0.4),
    "control_n3": ("n3", "v3s", 0.0), "control_m4": ("m4", "v3s", 0.0), "control_v3s": ("v3s", "v3s", 0.0),
    "control_compatible": ("v3s", "compat", 0.0)})


def slope(T):
    T = T[-4:]
    if any(t_ is None for t_ in T): return None
    return float(np.polyfit(np.log(Ns[-4:]), np.log(T), 1)[0])


def grade_row(L):
    D = [x["D"] for x in L]; D2 = [x["D2"] for x in L]; T0 = [x["T0"] for x in L]; Th = [x["Th"] for x in L]
    d1, d2_ = abs(D[-2] - D[-3]), abs(D[-1] - D[-2])
    return dict(D=D, D2=D2, T0=T0, Th=Th, Dinf=2 * D[-1] - D[-2], r=abs(D[-2]) / abs(D[-1]) if D[-1] else float("inf"),
                p=float(np.log2(d1 / d2_)) if d2_ > 0 and d1 > 0 else None, D2inf=2 * D2[-1] - D2[-2],
                r2=abs(D2[-2]) / abs(D2[-1]) if D2[-1] else float("inf"),
                sig_half=slope(Th), sig_0=slope(T0), no_half=all(t_ is None for t_ in Th[-4:]),
                no_0=all(t_ is None for t_ in T0[-4:]),
                legacy_rt=(T0[-2] / T0[-1]) if (T0[-2] and T0[-1]) else None)


def c1(g, yard):
    order_ok = (g["p"] is not None and g["p"] >= 0.8) or abs(g["D"][-1]) <= 1e-6
    half_ok = g["no_half"] or (g["sig_half"] is not None and g["sig_half"] >= -0.15)
    zero_ok = g["no_0"] or (g["sig_0"] is not None and g["sig_0"] > -0.35)
    return dict(jump=abs(g["Dinf"]) <= 0.1 * yard, order=order_ok, cross_half=half_ok, cross_0=zero_ok,
                all=abs(g["Dinf"]) <= 0.1 * yard and order_ok and half_ok and zero_ok)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--workers", type=int, default=4); a = ap.parse_args()
    T0_ = time.time()
    jobs = [(k, *v, N) for k, v in ROWS.items() for N in sorted(Ns, reverse=True)]
    res = {}
    with Pool(a.workers) as pool:
        for o in pool.imap_unordered(run, jobs):
            res.setdefault(o["name"], {})[o["N"]] = o
            print(o["name"], o["N"], {k: o[k] for k in ("D", "D2", "T0", "Th")}, round(time.time() - T0_, 1), flush=True)
    gr = {k: grade_row([res[k][N] for N in Ns]) for k in ROWS}
    ok = {}
    if MUT:
        g = gr["control_v3s"]; yard = 1.0
        c = c1(g, abs(g["D"][-1]) * 10)   # yardstick irrelevant for shape lines; order/crossing must fail
        ok["mutate_v3s_passes_C1"] = c["order"] and c["cross_half"] and c["cross_0"]
        label = "MUTATE v3s: " + ("C1 PASS (control does NOT bite)" if ok["mutate_v3s_passes_C1"] else "C1 FAIL (bites)")
    else:
        yard = abs(gr["control_n3"]["D"][-1]); y2 = abs(gr["control_m4"]["D2inf"])
        for k in ROWS:
            if k.startswith("form"):
                c = c1(gr[k], yard); gr[k]["c1"] = c
                ok[f"C1_{k}"] = c["all"]; ok[f"C2_{k}"] = abs(gr[k]["D2inf"]) <= 0.1 * y2
        n3 = gr["control_n3"]; ok["control_n3_kink"] = 0.9 <= n3["r"] <= 1.1 and abs(n3["Dinf"]) >= 0.5 * abs(n3["D"][-1])
        v = gr["control_v3s"]
        ok["control_v3s_collapse"] = ((v["sig_half"] is not None and v["sig_half"] <= -0.35) or
                                      (v["sig_0"] is not None and v["sig_0"] <= -0.35) or v["r"] < 0.9)
        ok["control_compatible"] = abs(gr["control_compatible"]["D"][-1]) <= 0.1 * yard
        m4 = gr["control_m4"]; c4 = c1(m4, yard); m4["c1"] = c4
        ok["control_m4_C1_not_C2"] = c4["all"] and 0.8 <= m4["r2"] <= 1.25 and abs(m4["D2inf"]) >= 0.5 * abs(m4["D2"][-1])
        controls = all(ok[k] for k in ok if k.startswith("control"))
        forms = all(ok[k] for k in ok if k.startswith("C1_") or k.startswith("C2_"))
        failing = [k for k in ok if (k.startswith("C1_") or k.startswith("C2_")) and not ok[k]]
        label = ("NO VERDICT (a control fails)" if not controls else
                 "PASS (curved 2D, C1 and C2, all form rows)" if forms else "FAIL as frozen: " + ", ".join(failing))
    out = dict(mode="MUTATE" if MUT else "main", label=label, checks=ok, grades=gr, ladder=Ns,
               elapsed_s=round(time.time() - T0_, 1), note="kappa = 1/2 FITTED; not theory closed")
    open(os.path.join(HERE, tag + ".json"), "w").write(json.dumps(out, indent=1, default=str) + "\n")
    f = lambda x: "None" if x is None else f"{x:+.3e}"
    txt = "\n".join(f"{k}: {'ok' if v_ else 'FAIL'}" for k, v_ in ok.items())
    for k, g in gr.items():
        txt += (f"\n{k}: D " + ", ".join(f(x) for x in g["D"]) + f" | Dinf {f(g['Dinf'])} r {g['r']:.3f} p {g['p']}"
                + f"\n   D2 " + ", ".join(f(x) for x in g["D2"]) + f" | D2inf {f(g['D2inf'])} r2 {g['r2']:.3f}"
                + f"\n   T_half {g['Th']} sigma {g['sig_half']}\n   T0 {g['T0']} sigma {g['sig_0']} LEGACY ratio {g['legacy_rt']}")
    txt += f"\nLABEL: {label}\n"
    open(os.path.join(HERE, tag + ".out"), "w").write(txt); print(txt)
    if MUT: sys.exit(1 if label.endswith("(bites)") else 0)
