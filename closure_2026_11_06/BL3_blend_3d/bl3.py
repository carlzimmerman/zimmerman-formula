#!/usr/bin/env python3
"""BL3: curved-3D (spherical switch r = 1) crossing ladder for AC21's iter_6 Pi^6 blend (criteria CRITERIA.md,
5f66d85740). AC22's scheme (ac22.py) with the cell measure X^d/d; d = 3 graded, d = 2 for the KA. Run from repo root:
  nice -n 15 python3 closure_2026_11_06/BL3_blend_3d/bl3.py [--workers 3]
Preemptible: each finished (row, d, N) job is appended to parts.jsonl (bl3_MUTATE_parts.jsonl for MUTATE);
a restart skips finished jobs; SIGTERM stops the pool and exits.
MUTATE (BL3_MUTATE=1): m5 graded by the form-row C3 line against the analytic yardstick must FAIL (exit 1).
kappa = 1/2 FITTED; not theory closed."""
import json, os, sys, time, argparse, signal
sys.dont_write_bytecode = True
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np
import sympy as sp
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
MUT = os.environ.get("BL3_MUTATE") == "1"
tag = "bl3_MUTATE" if MUT else "bl3"
PARTS = os.path.join(HERE, tag + "_parts.jsonl" if MUT else "parts.jsonl")
FORM = json.load(open(os.path.join(ROOT, "action_search_2026_11_05", "AC21_smooth_3d", "iter_6_fast_decay", "form.json")))
AC22 = json.load(open(os.path.join(ROOT, "action_search_2026_11_05", "AC22_curved_ladder", "ac22.json")))
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
    if kind == "m5": return lambda P: P ** 4
    if kind == "m6": return lambda P: P ** 5
    if kind == "v3s": return lambda P: P
    raise ValueError(kind)


def data(cfg, b):
    if cfg == "v3s": return lambda r: np.tanh(2.5 * (r - 1)) + 0.1 * np.sin(2 * (r - 1))
    if cfg == "ac2q": return lambda r: 2 * b * np.tanh(2.5 * (r - 1)) + 0.1 * b * np.sin(2 * (r - 1))
    if cfg == "compat": return lambda r: np.tanh(2.5 * (r - 1)) ** 3
    raise ValueError(cfg)


v0f = lambda r: 0.1 * np.cos(1.3 * (r - 1)) + 0.05


def lead(Xs, Vs, x0, deg):
    return float(np.polyfit(Xs - x0, Vs, deg)[0])


def run(args):
    name, kind, cfg, b, d, N = args
    hprime, Pi0f = hfun(kind, b), data(cfg, b)
    t_meas, t_max, r_lo, r_hi = 0.01, 2.0, 0.25, 3.25
    an = np.linspace(r_lo, r_hi, N + 1); am = 0.5 * (an[1:] + an[:-1]); da = an[1] - an[0]
    area0 = (an[1:] ** d - an[:-1] ** d) / d
    m = Pi0f(am) * area0; on = m > 0
    X = an.copy(); V = v0f(an)

    def acc(X):
        area = (X[1:] ** d - X[:-1] ** d) / d
        Pc = np.where(on, m / np.where(area > 0, area, np.inf), 0.0)
        h = np.where(on, hprime(np.maximum(Pc, 0.0)), 0.0)
        a_ = np.zeros_like(X); a_[1:-1] = -(h[1:] - h[:-1]) / (0.5 * (X[2:] - X[:-2]))
        return a_

    dt = 0.1 * da; nmeas = int(round(t_meas / dt)); dt_m = t_meas / nmeas
    i0 = int(round((1.0 - r_lo) / da)); assert abs(an[i0] - 1.0) < 1e-12
    near = np.abs(am - 1.0) < 0.5
    tcur, step, D, D2, D3, D4, T0, Th = 0.0, 0, None, None, None, None, None, None
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
            x0 = X[i0]
            R3, L3 = slice(i0, i0 + 13), slice(i0 - 12, i0 + 1)
            D3 = 6.0 * (lead(X[R3], V[R3], x0, 3) - lead(X[L3], V[L3], x0, 3))
            R4, L4 = slice(i0, i0 + 17), slice(i0 - 16, i0 + 1)
            D4 = 24.0 * (lead(X[R4], V[R4], x0, 4) - lead(X[L4], V[L4], x0, 4))
        J = ((X[1:] ** d - X[:-1] ** d) / d) / area0
        if Th is None and np.any(J[near] <= 0.5): Th = tcur
        if T0 is None and np.any(J[near] <= 0.0): T0 = tcur
        if T0 is not None and D is not None: break
    return dict(name=name, d=d, N=N, D=D, D2=D2, D3=D3, D4=D4, T0=T0, Th=Th)


Ns = (800, 1600, 3200, 6400, 12800, 25600, 51200)
if MUT:
    ROWS = {"control_m5": ("m5", "v3s", 0.0, 3)}
else:
    ROWS = {
        "form_v3s_b0.2": ("form", "v3s", 0.2, 3), "form_v3s_b0.4": ("form", "v3s", 0.4, 3),
        "form_v3s_b0.8": ("form", "v3s", 0.8, 3), "form_ac2q_b0.2": ("form", "ac2q", 0.2, 3),
        "form_ac2q_b0.4": ("form", "ac2q", 0.4, 3),
        "count_m5": ("m5", "v3s", 0.0, 3), "count_m6": ("m6", "v3s", 0.0, 3),
        "control_n3": ("n3", "v3s", 0.0, 3), "control_m4": ("m4", "v3s", 0.0, 3),
        "control_v3s": ("v3s", "v3s", 0.0, 3), "control_compatible": ("v3s", "compat", 0.0, 3),
        "KA2d_form_v3s_b0.4": ("form", "v3s", 0.4, 2), "KA2d_control_m4": ("m4", "v3s", 0.0, 2),
        "KA2d_control_v3s": ("v3s", "v3s", 0.0, 2)}
Y3_ANALYTIC = -0.01 * 24 * 2.7 ** 4


def slope(T):
    T = T[-4:]
    if any(t_ is None for t_ in T): return None
    return float(np.polyfit(np.log(Ns[-4:]), np.log(T), 1)[0])


def grade_row(L):
    D = [x["D"] for x in L]; D2 = [x["D2"] for x in L]; D3 = [x["D3"] for x in L]; D4 = [x["D4"] for x in L]
    T0 = [x["T0"] for x in L]; Th = [x["Th"] for x in L]
    d1, d2_ = abs(D[-2] - D[-3]), abs(D[-1] - D[-2])
    return dict(D=D, D2=D2, D3=D3, D4=D4, T0=T0, Th=Th, Dinf=2 * D[-1] - D[-2],
                r=abs(D[-2]) / abs(D[-1]) if D[-1] else float("inf"),
                p=float(np.log2(d1 / d2_)) if d2_ > 0 and d1 > 0 else None, D2inf=2 * D2[-1] - D2[-2],
                r2=abs(D2[-2]) / abs(D2[-1]) if D2[-1] else float("inf"),
                D3inf=2 * D3[-1] - D3[-2], r3=abs(D3[-2]) / abs(D3[-1]) if D3[-1] else float("inf"),
                D4inf=2 * D4[-1] - D4[-2],
                sig_half=slope(Th), sig_0=slope(T0), no_half=all(t_ is None for t_ in Th[-4:]),
                no_0=all(t_ is None for t_ in T0[-4:]),
                legacy_rt=(T0[-2] / T0[-1]) if (T0[-2] and T0[-1]) else None)


def c1(g, yard):
    order_ok = (g["p"] is not None and g["p"] >= 0.8) or abs(g["D"][-1]) <= 1e-6
    half_ok = g["no_half"] or (g["sig_half"] is not None and g["sig_half"] >= -0.15)
    zero_ok = g["no_0"] or (g["sig_0"] is not None and g["sig_0"] > -0.35)
    return dict(jump=abs(g["Dinf"]) <= 0.1 * yard, order=order_ok, cross_half=half_ok, cross_0=zero_ok,
                all=abs(g["Dinf"]) <= 0.1 * yard and order_ok and half_ok and zero_ok)


def load_parts():
    res = {}
    if os.path.exists(PARTS):
        for ln in open(PARTS):
            ln = ln.strip()
            if ln:
                o = json.loads(ln); res.setdefault(o["name"], {})[o["N"]] = o
    return res


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--workers", type=int, default=3); a = ap.parse_args()
    T0_ = time.time()
    res = load_parts()
    jobs = [(k, *v, N) for N in sorted(Ns, reverse=True) for k, v in ROWS.items() if N not in res.get(k, {})]
    print(f"{len(jobs)} jobs to run ({sum(len(v) for v in res.values())} on disk)", flush=True)
    if jobs:
        pool = Pool(a.workers)

        def stop(sig, frm):
            pool.terminate(); print("SIGTERM: pool stopped; finished jobs are in", PARTS, flush=True); sys.exit(143)
        signal.signal(signal.SIGTERM, stop)
        with open(PARTS, "a") as fh:
            for o in pool.imap_unordered(run, jobs):
                fh.write(json.dumps(o) + "\n"); fh.flush()
                res.setdefault(o["name"], {})[o["N"]] = o
                print(o["name"], o["N"], {k: o[k] for k in ("D", "D2", "D3", "T0", "Th")}, round(time.time() - T0_, 1),
                      flush=True)
        pool.close(); pool.join()
    gr = {k: grade_row([res[k][N] for N in Ns]) for k in ROWS}
    ok = {}
    if MUT:
        g = gr["control_m5"]
        ok["mutate_m5_passes_C3_analytic"] = abs(g["D3inf"]) <= 0.1 * abs(Y3_ANALYTIC)
        label = "MUTATE m5: " + ("C3 PASS (statistic blind)" if ok["mutate_m5_passes_C3_analytic"] else "C3 FAIL (bites)")
    else:
        # KA: d = 2 rows against AC22's ac22.json
        ka = {}
        for k in ROWS:
            if not k.startswith("KA2d_"): continue
            ref = AC22["grades"][k[len("KA2d_"):]]; g = gr[k]
            rel = lambda x, y: abs(x - y) / max(abs(y), 1e-300)
            dmax = max(rel(x, y) for x, y in zip(g["D"] + g["D2"], ref["D"] + ref["D2"]))
            tmax = max(abs(x - y) for x, y in zip(g["Th"] + g["T0"], ref["Th"] + ref["T0"]))
            ka[k] = dict(max_rel_D_D2=dmax, max_abs_T=tmax, ok=dmax <= 1e-8 and tmax <= 1e-9)
            ok["KA_" + k] = ka[k]["ok"]
        yard = abs(gr["control_n3"]["D"][-1]); y2 = abs(gr["control_m4"]["D2inf"]); y3 = abs(gr["count_m5"]["D3inf"])
        for k in ROWS:
            if k.startswith("form") or k == "count_m6":
                c = c1(gr[k], yard); gr[k]["c1"] = c
                pre = "C" if k.startswith("form") else "m6_C"
                ok[f"{pre}1_{k}"] = c["all"]; ok[f"{pre}2_{k}"] = abs(gr[k]["D2inf"]) <= 0.1 * y2
                ok[f"{pre}3_{k}"] = abs(gr[k]["D3inf"]) <= 0.1 * y3
        n3 = gr["control_n3"]; ok["control_n3_kink"] = 0.9 <= n3["r"] <= 1.1 and abs(n3["Dinf"]) >= 0.5 * abs(n3["D"][-1])
        m4 = gr["control_m4"]; c4 = c1(m4, yard); m4["c1"] = c4
        ok["control_m4_C1_not_C2"] = c4["all"] and 0.8 <= m4["r2"] <= 1.25 and abs(m4["D2inf"]) >= 0.5 * abs(m4["D2"][-1])
        m5 = gr["count_m5"]; c5 = c1(m5, yard); m5["c1"] = c5
        m5["D3inf_vs_analytic"] = m5["D3inf"] / Y3_ANALYTIC
        ok["control_m5_C1_C2_not_C3"] = (c5["all"] and abs(m5["D2inf"]) <= 0.1 * y2 and 0.8 <= m5["r3"] <= 1.25
                                         and abs(m5["D3inf"]) >= 0.5 * abs(m5["D3"][-1])
                                         and abs(m5["D3inf"] / Y3_ANALYTIC - 1) <= 0.15)
        v = gr["control_v3s"]
        ok["control_v3s_collapse"] = ((v["sig_half"] is not None and v["sig_half"] <= -0.35) or
                                      (v["sig_0"] is not None and v["sig_0"] <= -0.35) or v["r"] < 0.9)
        ok["control_compatible"] = abs(gr["control_compatible"]["D"][-1]) <= 0.1 * yard
        ka_ok = all(ok[k] for k in ok if k.startswith("KA_"))
        controls = all(ok[k] for k in ok if k.startswith("control"))
        m6_ok = all(ok[k] for k in ok if k.startswith("m6_C"))
        forms = [k for k in ok if k[:2] in ("C1", "C2", "C3")]
        failing = [k for k in forms if not ok[k]]
        if not ka_ok: label = "NO VERDICT (KA: AC22 2D rows not reproduced)"
        elif not controls: label = "NO VERDICT (a control fails: " + ", ".join(k for k in ok if k.startswith("control") and not ok[k]) + ")"
        elif not m6_ok: label = "NO VERDICT (m6 pure fails: C3 count not resolved at N <= 51200)"
        elif failing: label = "FAIL 3D as frozen: " + ", ".join(failing)
        else: label = "PASS 3D (curved 3D spherical switch, C1 C2 C3 all form rows; MUTATE separate)"
        ok_ka = ka
    out = dict(mode="MUTATE" if MUT else "main", label=label, checks=ok, grades=gr, ladder=Ns,
               Y3_analytic=Y3_ANALYTIC, elapsed_s=round(time.time() - T0_, 1),
               note="kappa = 1/2 FITTED; not theory closed")
    if not MUT: out["KA"] = ok_ka
    open(os.path.join(HERE, tag + ".json"), "w").write(json.dumps(out, indent=1, default=str) + "\n")
    f = lambda x: "None" if x is None else f"{x:+.3e}"
    txt = "\n".join(f"{k}: {'ok' if v_ else 'FAIL'}" for k, v_ in ok.items())
    for k, g in gr.items():
        txt += (f"\n{k}: D " + ", ".join(f(x) for x in g["D"]) + f" | Dinf {f(g['Dinf'])} r {g['r']:.3f} p {g['p']}"
                + f"\n   D2 " + ", ".join(f(x) for x in g["D2"]) + f" | D2inf {f(g['D2inf'])} r2 {g['r2']:.3f}"
                + f"\n   D3 " + ", ".join(f(x) for x in g["D3"]) + f" | D3inf {f(g['D3inf'])} r3 {g['r3']:.3f}"
                + f"\n   D4 " + ", ".join(f(x) for x in g["D4"]) + f" | D4inf {f(g['D4inf'])} (report only)"
                + f"\n   T_half {g['Th']} sigma {g['sig_half']}\n   T0 {g['T0']} sigma {g['sig_0']} LEGACY ratio {g['legacy_rt']}")
    txt += f"\nLABEL: {label}\n"
    open(os.path.join(HERE, tag + ".out"), "w").write(txt); print(txt)
    if MUT: sys.exit(1 if label.endswith("(bites)") else 0)
