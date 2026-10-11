#!/usr/bin/env python3
"""CFG599 main: C4(b) isolated halos, M-6 calibration (K1 speed, G1 gas geometry), the 16-run alpha grid, observables (section 3),
scores and verdicts (section 4).  Criteria: FROZEN_CRITERIA.md (8a10775bd).  kappa = 1/2 FITTED; footings never pooled; the
cold energy's mass is an input.  Yardsticks: raw data only.

Order:  nice -n 10 python3 cfg599_controls.py                  -> cfg599_controls.out/_results.json (C1-C3, C4a, C5, C6)
        nice -n 10 python3 cfg599_main.py                      -> cfg599.out, cfg599_results.json (C4b, K1, G1, grid, verdicts)
        CFG599_MUTATE=1 nice -n 10 python3 cfg599_main.py      -> cfg599_MUTATE.out, cfg599_results_MUTATE.json (M1-M4)
        nice -n 10 python3 cfg599_main.py                      (re-run from the run cache to fold the M1-M3 gate into the verdicts)
Per-run time series are cached in runs/ (resumable).  4 worker processes of 1 thread."""
import os
os.environ["OMP_NUM_THREADS"] = "1"
import sys, json, math, time, io, contextlib
import multiprocessing as mp
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import cfg599_lib as L

MUT = os.environ.get("CFG599_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
RUNS = os.path.join(HERE, "runs"); os.makedirs(RUNS, exist_ok=True)
ALPHAS = [0.0, 0.03, 0.1, 0.3, 1.0, 3.0, 10.0, math.inf]
FEET = ["can", "alt"]
V_TARGET, V_TOL, V_STOP = 2700.0, 200.0, 100.0
DSG_OBS, DSG_TOL, DSG_STOP = 194.0, 50.0, 25.0
ETA_RANGE = (0.1, 2.5)
F_OBS, SIG_F = 0.045, 0.125
HARV_B, HARV_S = -0.04, 0.07
OUT = []


def P(s=""):
    print(s, flush=True); OUT.append(str(s))


def astr(a):
    return "inf" if math.isinf(a) else f"{a:g}"


def name_of(c):
    if c.get("mode") == "isolated":
        return f"iso_{c['iso_which']}_a{astr(c['alpha'])}_{c['foot']}"
    s = f"a{astr(c['alpha'])}_{c['foot']}_v{c['v0_kms']:.1f}_eta{c['eta']:.4g}"
    if c.get("swap"):
        s += "_swap"
    if c.get("seed", 599) != 599:
        s += f"_seed{c['seed']}"
    if c.get("mode") == "calib":
        s += "_calib"
    return s


def _round(o):
    if isinstance(o, float):
        return round(o, 4)
    if isinstance(o, list):
        return [_round(x) for x in o]
    if isinstance(o, dict):
        return {k: _round(v) for k, v in o.items()}
    return o


def worker(c):
    import cfg599_sim as S
    fn = os.path.join(RUNS, name_of(c) + ".json")
    if os.path.exists(fn):
        return
    cc = dict(c)
    if "v0_kms" in cc:
        cc["v0"] = cc["v0_kms"] * L.KMS
    res = S.run(cc)
    json.dump(_round(res), open(fn + ".tmp", "w")); os.replace(fn + ".tmp", fn)


def pool_map(cfgs):
    todo = [c for c in cfgs if not os.path.exists(os.path.join(RUNS, name_of(c) + ".json"))]
    if todo:
        P(f"  running {len(todo)} run(s) on <= 4 processes ...")
        with mp.get_context("fork").Pool(min(4, len(todo))) as pool:
            pool.map(worker, todo, chunksize=1)
    return [json.load(open(os.path.join(RUNS, name_of(c) + ".json"))) for c in cfgs]


def calib_cfg(v0, eta, foot="can"):
    return dict(alpha=0.0, foot=foot, v0_kms=float(round(v0, 1)), eta=float(f"{eta:.4g}"), mode="calib")


# ------------------------------------------------------------------------------------------------ M-6 calibration
def bracket_search(evaluate, lo, hi, target, stop, rounds=4, increasing=True, log=False):
    """parallel 4-way bracketing (README D-1): round 1 evaluates lo, hi and 2 interior points; later rounds 3 interior points of the
    sub-bracket holding the target. Returns (best_x, best_y, history, bracket_ok)."""
    tf = (lambda x: math.log(x)) if log else (lambda x: x)
    itf = (lambda u: math.exp(u)) if log else (lambda u: u)
    a, b = tf(lo), tf(hi)
    xs = [itf(a + (b - a) * k / 3) for k in range(4)]
    hist = []
    for rnd in range(rounds):
        ys = evaluate(xs)
        hist += list(zip(xs, ys))
        pts = sorted(set(hist))
        best = min(pts, key=lambda p: abs(p[1] - target))
        if rnd == 0:
            yl, yh = ys[0], ys[-1]
            ok = (yl <= target <= yh) if increasing else (yh <= target <= yl)
            if not ok and abs(best[1] - target) > stop:
                return best[0], best[1], hist, False
        if abs(best[1] - target) <= stop:
            return best[0], best[1], hist, True
        # sub-bracket: adjacent pair (in x) straddling the target
        sub = None
        for (x1, y1), (x2, y2) in zip(pts[:-1], pts[1:]):
            if (y1 - target) * (y2 - target) <= 0:
                sub = (tf(x1), tf(x2)); break
        if sub is None:
            return best[0], best[1], hist, False
        a, b = sub
        xs = [itf(a + (b - a) * k / 4) for k in (1, 2, 3)]
    pts = sorted(set(hist))
    best = min(pts, key=lambda p: abs(p[1] - target))
    return best[0], best[1], hist, True


def calibrate():
    log = {"rounds": []}
    eta = 1.0
    v0 = None
    for rnd in range(2):
        def ev_v(xs, eta=eta):
            rs = pool_map([calib_cfg(x, eta) for x in xs])
            for x, r in zip(xs, rs):
                P(f"    K1  v0 = {x:7.1f} km/s, eta = {eta:.4g}: speed at the 720-kpc epoch {r.get('v_obs_kms', float('nan')):7.1f} km/s, "
                  f"d_SG {r.get('dSG_obs', float('nan')):6.1f} kpc")
            return [r.get("v_obs_kms", float("nan")) for r in rs]
        P(f"  round {rnd + 1}: v0 bracketing on [0, 4000] km/s at eta = {eta:.4g}")
        v0, vbest, hv, okv = bracket_search(ev_v, 0.0, 4000.0, V_TARGET, V_STOP)
        r0 = pool_map([calib_cfg(0.0, eta)])[0]
        if r0.get("v_obs_kms", 0) > V_TARGET + V_TOL:
            log["rounds"].append(dict(stage="K1", eta=eta, history=hv, infeasible_v0_0=True))
            return dict(ok=False, reason="K1 infeasible: v0 = 0 already exceeds 2900 km/s", log=log)

        def ev_e(xs, v0=v0):
            rs = pool_map([calib_cfg(v0, x) for x in xs])
            for x, r in zip(xs, rs):
                P(f"    G1  v0 = {v0:7.1f} km/s, eta = {x:.4g}: d_SG at the 720-kpc epoch {r.get('dSG_obs', float('nan')):6.1f} kpc, "
                  f"speed {r.get('v_obs_kms', float('nan')):7.1f} km/s")
            return [r.get("dSG_obs", float("nan")) for r in rs]
        P(f"  round {rnd + 1}: eta bracketing on [0.03, 10] (log) at v0 = {v0:.1f} km/s")
        eta, dbest, he, oke = bracket_search(ev_e, 0.03, 10.0, DSG_OBS, DSG_STOP, log=True)
        eta = float(f"{eta:.4g}")
        rf = pool_map([calib_cfg(v0, eta)])[0]
        log["rounds"].append(dict(v0_history=hv, eta_history=he, v0=v0, eta=eta, final_speed=rf.get("v_obs_kms"),
                                  final_dSG=rf.get("dSG_obs"), v_bracket_ok=okv, eta_bracket_ok=oke))
        k1 = abs(rf["v_obs_kms"] - V_TARGET) <= V_TOL
        g1 = abs(rf["dSG_obs"] - DSG_OBS) <= DSG_TOL
        P(f"  round {rnd + 1} result: v0 = {v0:.1f} km/s, eta = {eta:.4g} -> speed {rf['v_obs_kms']:.1f} km/s (K1 {'in' if k1 else 'OUT of'} "
          f"2700 +- 200), d_SG {rf['dSG_obs']:.1f} kpc (G1 {'in' if g1 else 'OUT of'} 194 +- 50)")
        if k1 and g1:
            break
    inr = ETA_RANGE[0] <= eta <= ETA_RANGE[1]
    ok = bool(k1 and g1 and inr)
    return dict(ok=ok, v0_kms=v0, eta=eta, speed_kms=rf["v_obs_kms"], dSG=rf["dSG_obs"], K1=bool(k1), G1=bool(g1),
                eta_in_plausible_range=bool(inr), log=log,
                reason=None if ok else ("eta outside [0.1, 2.5]" if (k1 and g1) else "K1/G1 not met after two rounds"))


# ------------------------------------------------------------------------------------------------ observables
def beta_of(d):
    s = d["sub"]
    gal, gas, lens = np.array(s["gal"]), np.array(s["gas"]), np.array(s["lens"])
    e = gas - gal; n = np.linalg.norm(e)
    if n <= 0:
        return float("nan"), n
    return float(np.dot(lens - gal, e) / n ** 2), float(n)


def beta_cold(d):
    s = d["sub"]
    gal, gas, c = np.array(s["gal"]), np.array(s["gas"]), np.array(s["cold"])
    e = gas - gal; n = np.linalg.norm(e)
    return float(np.dot(c - gal, e) / n ** 2) if n > 0 else float("nan")


def stable(d):
    _, n = beta_of(d)
    return d["sub"]["lens_spread"] <= max(20.0, 0.1 * n)


def score_run(run):
    import cfg599_sim as S
    tp = run["t_peri"]
    if tp is None:
        return dict(scorable_B=False, scorable_H=False, note="no pericentre")
    diag = run["diag"]
    ep = S.epoch(diag, tp)
    out = dict(t_peri=tp)
    if ep is None:
        out.update(scorable_B=False, note="720-kpc epoch not reached")
    else:
        i, w = ep["i_obs"], ep["w_obs"]
        b0, _ = beta_of(diag[i - 1]); b1, _ = beta_of(diag[i])
        f = b0 + w * (b1 - b0)
        st = stable(diag[i - 1]) and stable(diag[i])
        fc = beta_cold(diag[i - 1]) + w * (beta_cold(diag[i]) - beta_cold(diag[i - 1]))
        out.update(t_obs_after_peri=ep["t_obs"] - tp, speed_kms=ep["v_obs_kms"], dSG=ep["dSG_obs"], f=f, f_coldpeak=fc,
                   lens_spread_obs=[diag[i - 1]["sub"]["lens_spread"], diag[i]["sub"]["lens_spread"]], scorable_B=bool(st),
                   Z_B=(f - F_OBS) / SIG_F)
    win = [d for d in diag if 0.1 - 1e-9 <= d["t"] - tp <= 0.6 + 1e-9]
    good = [d for d in win if beta_of(d)[1] >= 50.0 and stable(d)]
    out["harvey_n_window"] = len(win); out["harvey_n_used"] = len(good)
    if len(good) >= 10 and len(good) >= 0.5 * len(win):
        bb = float(np.mean([beta_of(d)[0] for d in good]))
        out.update(scorable_H=True, beta_bar=bb, Z_H=(bb - HARV_B) / HARV_S)
    else:
        out.update(scorable_H=False)
        if good:
            out["beta_bar_reported"] = float(np.mean([beta_of(d)[0] for d in good]))
    for tsp in (0.5, 0.7):
        ts = [d["t"] for d in diag]; bs = [beta_of(d)[0] for d in diag]
        out[f"beta_tsp{tsp}"] = float(np.interp(tp + tsp, ts, bs)) if tp + tsp <= ts[-1] else None
    out["cap_frac"] = run["n_cap"] / max(run["n_mv"], 1)
    sc = out.get("scorable_B") and out.get("scorable_H")
    if sc:
        out["status"] = "ALLOWED" if (abs(out["Z_B"]) < 2 and abs(out["Z_H"]) < 2) else "EXCLUDED"
    else:
        out["status"] = "UNSCORABLE"
    return out


def read_D1():
    REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
    bt = os.path.join(REPO, "opus_48_extended_research", "reviews", "bullet", "bullet_data_table.py")
    ns = {"__name__": "bullet_readonly"}
    with contextlib.redirect_stdout(io.StringIO()):
        exec(open(bt).read(), ns)
    return dict(kpc_main=float(ns["kpc_main"]), kpc_sub=float(ns["kpc_sub"]), kpc_bcg=float(ns["kpc_bcg"]), kpc_per_arcsec=ns["KPC_PER_ARCSEC"])


def finish(R):
    open(os.path.join(HERE, f"cfg599{TAG}.out"), "w").write("\n".join(OUT) + "\n")
    json.dump(R, open(os.path.join(HERE, f"cfg599_results{TAG}.json"), "w"), indent=1, default=lambda o: None)


# ------------------------------------------------------------------------------------------------ main
def main():
    T0 = time.time()
    P("CFG599: merger stopwatch v2 for cold-energy settling (valid rerun of CFG597)" + ("  [MUTATE]" if MUT else ""))
    P("criteria FROZEN_CRITERIA.md (8a10775bd); kappa = 1/2 FITTED; footings 9.3603e-11 / 1.1312e-10 never pooled; candidate B; G9; no EFE;")
    P("cold energy's mass required (an input); no particle species; yardsticks = raw data only (no LCDM, no MOND force law).")
    R = {"lane": "CFG599", "mutate": MUT, "criteria_commit": "8a10775bd", "void_reasons": []}
    d1 = read_D1(); R["D1"] = d1
    P(f"\nD1 Bullet (Clowe+06 Table 2 via the record script, read-only): galaxy-plasma {d1['kpc_main']:.1f} (main) / {d1['kpc_sub']:.1f} (sub) kpc; "
      f"BCG-BCG {d1['kpc_bcg']:.1f} kpc; f_obs = {2 * d1['kpc_per_arcsec'] / d1['kpc_sub']:.3f}; sigma_f = 0.125 (PROVISIONAL)")
    P(f"D2 Harvey+15: beta = {HARV_B} +- {HARV_S}")

    ctl = json.load(open(os.path.join(HERE, "cfg599_controls_results.json")))
    R["controls_C1_C3_C4a_C5_C6_all_pass"] = ctl["all_pass"]
    P(f"\nC1-C3, C4(a), C5, C6 (cfg599_controls_results.json): {'ALL PASS' if ctl['all_pass'] else 'SOME FAIL'}")
    if not ctl["all_pass"]:
        R["void_reasons"].append("controls C1-C6 failed"); R["status"] = "VOID"; finish(R); return 1

    # ---- C4(b) isolated halos before any merger number
    isos = [dict(alpha=1.0, foot="can", mode="isolated", iso_which=w, t_iso=0.6) for w in ("main", "sub")]
    P("\nC4(b) isolated halos (L-2S, alpha 1, canonical, 0.6 Gyr)")
    rs = pool_map(isos)
    c4 = {}
    for c, r in zip(isos, rs):
        w = c["iso_which"]
        og = [float(np.hypot(*(np.array(d[w]["gas"]) - np.array(d[w]["gal"])))) for d in r["diag"]]
        ol = [float(np.hypot(*(np.array(d[w]["lens"]) - np.array(d[w]["gal"])))) for d in r["diag"]]
        m3 = [d[w]["M300"] for d in r["diag"]]
        drift = m3[-1] / m3[0] - 1
        ok = max(og) <= 15.0 and max(ol) <= 15.0 and abs(drift) <= 0.10
        c4[w] = dict(ok=bool(ok), max_gas_gal=max(og), max_lens_gal=max(ol), M300_drift=drift, n_epochs=len(og))
        P(f"  {w:4s}: max gas-galaxy {max(og):5.2f} kpc, max lensing-galaxy {max(ol):5.2f} kpc (<= 15); M(<300) drift {drift:+.4f} (<= 10%): "
          f"{'PASS' if ok else 'FAIL'}")
    R["C4b"] = c4
    if not all(v["ok"] for v in c4.values()):
        R["void_reasons"].append("C4(b) failed"); R["status"] = "VOID"
        P("\nC4(b) FAILED: no merger number is computed (section 5). STATUS: VOID"); finish(R); return 1

    # ---- M-6 calibration
    P("\nM-6 CALIBRATION (alpha = 0, canonical): K1 speed at the 720-kpc epoch 2700 +- 200 km/s; G1 d_SG 194 +- 50 kpc; eta in [0.1, 2.5]")
    cal = calibrate()
    R["calibration"] = cal
    P(f"  CALIBRATION {'PASS' if cal['ok'] else 'FAIL'}: " + json.dumps({k: (round(v, 3) if isinstance(v, float) else v) for k, v in cal.items() if k != 'log'}))
    if not cal["ok"]:
        R["void_reasons"].append("calibration K1/G1 failed: " + str(cal.get("reason"))); R["status"] = "VOID"; finish(R); return 1
    v0, eta = cal["v0_kms"], cal["eta"]

    base = dict(v0_kms=float(round(v0, 1)), eta=float(f"{eta:.4g}"))
    if MUT:
        cfgs = {"M1": dict(alpha=math.inf, foot="can", **base), "M2": dict(alpha=0.0, foot="can", **base),
                "M3": dict(alpha=math.inf, foot="can", swap=True, **base), "M3_a0": dict(alpha=0.0, foot="can", swap=True, **base),
                "M4": dict(alpha=0.0, foot="can", seed=600, **base)}
        P(f"\nMUTATE runs ({len(cfgs)})")
        rr = dict(zip(cfgs, pool_map(list(cfgs.values()))))
        sc = {k: score_run(v) for k, v in rr.items()}
        m1 = bool(sc["M1"].get("f") is not None and sc["M1"]["f"] >= 0.5)
        m2 = bool(sc["M2"].get("f") is not None and abs(sc["M2"]["f"]) <= 0.25 and sc["M2"].get("beta_bar") is not None and sc["M2"]["beta_bar"] <= 0.10)
        m3 = bool(sc["M3"].get("f") is not None and sc["M3"]["f"] <= 0.25)
        P(f"  M1 alpha = inf: f = {sc['M1'].get('f')} (>= 0.5) -> {'PASS' if m1 else 'FAIL'}")
        P(f"  M2 alpha = 0: f = {sc['M2'].get('f')} (|f| <= 0.25), beta-bar = {sc['M2'].get('beta_bar')} (<= 0.10) -> {'PASS' if m2 else 'FAIL'}")
        P(f"  M3 roles swapped, alpha = inf: f = {sc['M3'].get('f')} (<= 0.25) -> {'PASS' if m3 else 'FAIL'}   "
          f"[swapped alpha = 0 reported: f = {sc['M3_a0'].get('f')}]")
        df = None if sc["M4"].get("f") is None or sc["M2"].get("f") is None else sc["M4"]["f"] - sc["M2"]["f"]
        db = None if sc["M4"].get("beta_bar") is None or sc["M2"].get("beta_bar") is None else sc["M4"]["beta_bar"] - sc["M2"]["beta_bar"]
        P(f"  M4 seed 600 vs 599 at alpha = 0 (reported): delta f = {df}, delta beta-bar = {db}; d_SG {sc['M4'].get('dSG')} vs {sc['M2'].get('dSG')}")
        R.update(M1=dict(ok=m1, score=sc["M1"]), M2=dict(ok=m2, score=sc["M2"]), M3=dict(ok=m3, score=sc["M3"]),
                 M3_alpha0_reported=sc["M3_a0"], M4_reported=dict(score=sc["M4"], delta_f=df, delta_beta_bar=db))
        R["all_pass"] = m1 and m2 and m3
        P(f"\nMUTATE M1-M3: {'ALL PASS' if R['all_pass'] else 'SOME FAIL (every verdict VOID)'}")
        R["wall_s"] = time.time() - T0
        finish(R); return 0

    # ---- the grid
    cfgs = [dict(alpha=a, foot=f, **base) for f in FEET for a in ALPHAS]
    P(f"\nRUN GRID: {len(cfgs)} runs (10:1, L, 2S; v0 = {v0:.1f} km/s, eta = {eta:.4g}, both footings)")
    runs = pool_map(cfgs)
    cells = {}
    for c, r in zip(cfgs, runs):
        cells[f"{astr(c['alpha'])}_{c['foot']}"] = score_run(r)
    R["cells"] = cells

    # alt footing validity at alpha = 0
    fv = {}
    for f in FEET:
        s0 = cells[f"0_{f}"]
        okf = (s0.get("speed_kms") is not None and abs(s0["speed_kms"] - V_TARGET) <= V_TOL and abs(s0["dSG"] - DSG_OBS) <= DSG_TOL)
        fv[f] = dict(valid=bool(okf), speed_kms=s0.get("speed_kms"), dSG=s0.get("dSG"))
    R["footing_validity_alpha0"] = fv
    P("\nFOOTING VALIDITY at alpha = 0 (speed 2700 +- 200, d_SG 194 +- 50): " + json.dumps({f: {k: (round(v, 1) if isinstance(v, float) else v) for k, v in d.items()} for f, d in fv.items()}))

    P("\nPER-NODE SCORES (sub; f at the 720-kpc epoch; Harvey beta-bar over 0.1-0.6 Gyr after pericentre)")
    P(f"{'alpha':>6s} {'foot':>4s} | {'t_obs':>6s} {'speed':>6s} {'dSG':>6s} {'f':>7s} {'Z_B':>6s} {'spread':>11s} | {'n_H':>5s} {'bbar':>7s} {'Z_H':>6s} | {'f_cold':>6s} {'cap':>5s} | status")
    for f in FEET:
        for a in ALPHAS:
            s = cells[f"{astr(a)}_{f}"]
            st = s["status"] if fv[f]["valid"] else s["status"] + " (footing VOID)"
            P(f"{astr(a):>6s} {f:>4s} | {s.get('t_obs_after_peri', float('nan')):6.3f} {s.get('speed_kms', float('nan')):6.0f} {s.get('dSG', float('nan')):6.1f} "
              f"{s.get('f', float('nan')):+7.3f} {s.get('Z_B', float('nan')):+6.2f} {str([round(x, 1) for x in s.get('lens_spread_obs', [])]):>11s} | "
              f"{s.get('harvey_n_used', 0):2d}/{s.get('harvey_n_window', 0):2d} {s.get('beta_bar', s.get('beta_bar_reported', float('nan'))):+7.3f} "
              f"{s.get('Z_H', float('nan')):+6.2f} | {s.get('f_coldpeak', float('nan')):+6.3f} {s.get('cap_frac', 0):5.3f} | {st}")

    # ---- gates and verdicts
    mutf = os.path.join(HERE, "cfg599_results_MUTATE.json")
    mut = json.load(open(mutf)) if os.path.exists(mutf) else None
    mut_ok = bool(mut and mut.get("all_pass") and mut.get("calibration", {}).get("v0_kms") == v0 and mut.get("calibration", {}).get("eta") == eta)
    R["MUTATE_gate"] = dict(present=mut is not None, all_pass=mut_ok,
                            M=({k: mut[k]["ok"] for k in ("M1", "M2", "M3")} if mut and "M1" in mut else None))
    if not mut_ok:
        R["void_reasons"].append("MUTATE M1-M3 not (yet) all passing" if mut else "MUTATE not yet run")

    def st(a, f):
        if not fv[f]["valid"]:
            return "VOID"
        return cells[f"{astr(a)}_{f}"]["status"]

    allowed = {f: [astr(a) for a in ALPHAS if st(a, f) == "ALLOWED"] for f in FEET}
    excluded = {f: [astr(a) for a in ALPHAS if st(a, f) == "EXCLUDED"] for f in FEET}
    unsc = {f: [astr(a) for a in ALPHAS if st(a, f) in ("UNSCORABLE", "VOID")] for f in FEET}
    R["allowed_set"] = allowed; R["excluded_set"] = excluded; R["unscorable_or_void"] = unsc
    V = {}
    zinf = [cells[f"inf_{f}"] for f in FEET]
    if all(fv[f]["valid"] and z.get("scorable_B") for f, z in zip(FEET, zinf)):
        V["V1_instant_resettling"] = "EXCLUDED" if all(z["Z_B"] >= 3 for z in zinf) else "NOT EXCLUDED"
    else:
        V["V1_instant_resettling"] = "UNDETERMINED (alpha = inf unscorable or a footing VOID)"
    V["V1_Z_B_inf"] = [z.get("Z_B") for z in zinf]; V["V1_Z_H_inf_reported"] = [z.get("Z_H") for z in zinf]
    s0 = [st(0.0, f) for f in FEET]
    V["V2_pure_collisionless"] = ("ALLOWED" if all(s == "ALLOWED" for s in s0) else
                                  ("NOT ALLOWED" if all(s in ("ALLOWED", "EXCLUDED") for s in s0) else "UNDETERMINED"))
    both = lambda a: all(st(a, f) == "ALLOWED" for f in FEET)
    if both(1.0):
        V["V3_galaxy_side"] = "COMPATIBLE"
    elif any(both(a) for a in (3.0, 10.0, math.inf)):
        V["V3_galaxy_side"] = "PARTIAL (alpha = 1 not allowed; only nodes outside the causality bound alpha <~ 1)"
    else:
        V["V3_galaxy_side"] = "INCOMPATIBLE (no node alpha >= 1 allowed on both footings)"
    if V["V2_pure_collisionless"] == "ALLOWED" and V["V1_instant_resettling"] == "EXCLUDED":
        V["V4_summary"] = "collisionless component that re-settles slowly; allowed nodes listed"
    elif V["V1_instant_resettling"] == "NOT EXCLUDED":
        V["V4_summary"] = "merger data do not separate 'locked to baryons' from 'collisionless'"
    elif V["V2_pure_collisionless"] == "NOT ALLOWED" and not any(allowed[f] for f in FEET):
        V["V4_summary"] = "NO alpha works (a real failure)"
    else:
        V["V4_summary"] = "mixed; see the per-node table"
    R["verdicts"] = V
    R["status"] = "VALID" if not R["void_reasons"] else "VOID"
    P(f"\nALLOWED nodes: can {allowed['can']}  alt {allowed['alt']};  EXCLUDED: can {excluded['can']}  alt {excluded['alt']};  "
      f"UNSCORABLE/VOID: can {unsc['can']}  alt {unsc['alt']}")
    P("\nVERDICTS (frozen V-1..V-4)" + ("" if R["status"] == "VALID" else f"  -- STATUS VOID: {R['void_reasons']}"))
    for k, v in V.items():
        P(f"  {k}: {v}")
    P("\nD3 (sign level, not scored): sub beta at TSP 0.5 / 0.7 Gyr, canonical")
    R["D3_sign_level"] = {astr(a): (cells[f'{astr(a)}_can'].get('beta_tsp0.5'), cells[f'{astr(a)}_can'].get('beta_tsp0.7')) for a in ALPHAS}
    for a in ALPHAS:
        b5, b7 = R["D3_sign_level"][astr(a)]
        P(f"  alpha {astr(a):>4s}: {b5 if b5 is None else round(b5, 3)} / {b7 if b7 is None else round(b7, 3)}")
    R["wall_s"] = time.time() - T0
    finish(R)
    return 0


if __name__ == "__main__":
    sys.exit(main())
