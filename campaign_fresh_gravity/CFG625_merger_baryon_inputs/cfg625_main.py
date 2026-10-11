#!/usr/bin/env python3
"""CFG625 main (criteria FROZEN_CRITERIA.md, 9afb3f44b): CFG623's merger stopwatch with data-based progenitor baryons.
Simulator, estimator, window, stability rule, scores and verdict code are CFG623's (scoring imported read-only from
../CFG623_merger_stopwatch_v5/cfg623_main.py); only the progenitor baryons (cfg625_lib.Progenitor625) and the per-variant
calibration change.  kappa = 1/2 FITTED; footings never pooled; the cold energy's mass is an input.  Yardsticks: raw data only.

Phases (one simulation process at a time, 1 thread; run under nice -n 10):
  python3 cfg625_main.py static            -> cfg625_static.out/_results.json   (C0, static t = 0 masses: M-RAW part i)
  python3 cfg625_main.py c16               -> cfg625_c16.out/_results.json      (C1-C3, C5, C6 re-run; C4a/C4b/N_B re-read)
  python3 cfg625_main.py calib   V         -> cfg625_calib_V.out/_results.json
  python3 cfg625_main.py controls V        -> cfg625_controls_V.out/_results.json (12 runs, C7, C9, B-6 printed)
  python3 cfg625_main.py mutate  V         -> cfg625_MUTATE_V.out/_results.json   (M1, M2 = grid runs; M3 swapped)
  python3 cfg625_main.py grid    V [all]   -> cfg625_grid_V.out/_results.json     (nodes {0, 0.1, 1, inf}, or all 8)
  python3 cfg625_main.py summary           -> cfg625_summary.out/_results.json    (robustness reading, M-RAW report)
Run cache: ../../../_external_data/cfg625_work/runs (outside the repo)."""
import os
os.environ["OMP_NUM_THREADS"] = "1"
import sys, json, math, time, io, contextlib, subprocess, resource
import multiprocessing as mp
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
C623 = os.path.join(HERE, "..", "CFG623_merger_stopwatch_v5")
C621 = os.path.join(HERE, "..", "CFG621_merger_stopwatch_v3")
import cfg625_lib as CL                      # noqa: E402
sys.path.insert(0, C623)
_buf = io.StringIO()
with contextlib.redirect_stdout(_buf):
    import cfg623_main as M623               # noqa: E402 (read-only: scoring, stability rule, window)
import cfg599_lib as L                       # noqa: E402

RUNS = os.path.abspath(os.path.join(HERE, "..", "..", "..", "_external_data", "cfg625_work", "runs"))
os.makedirs(RUNS, exist_ok=True)
NODES4 = [0.0, 0.1, 1.0, math.inf]
ALPHAS = M623.ALPHAS
FEET = ["can", "alt"]
CTRL_SEEDS = [603, 604, 605]
V_TARGET, V_TOL, V_STOP = 2700.0, 200.0, 100.0
DSG_OBS, DSG_TOL, DSG_STOP = 194.0, 50.0, 25.0
ETA_RANGE = (0.1, 2.5)
astr = M623.astr
score_run = M623.score_run
OUT = []


def P(s=""):
    print(s, flush=True); OUT.append(str(s))


def finish(stem, R):
    open(os.path.join(HERE, f"cfg625_{stem}.out"), "w").write("\n".join(OUT) + "\n")
    json.dump(R, open(os.path.join(HERE, f"cfg625_{stem}_results.json"), "w"), indent=1, default=lambda o: None)


def name_of(c):
    s = f"{c['variant']}_a{astr(c['alpha'])}_{c['foot']}_v{c['v0_kms']:.1f}_eta{c['eta']:.4g}"
    if c.get("swap"):
        s += "_swap"
    if c.get("seed", 599) != 599:
        s += f"_seed{c['seed']}"
    if c.get("mode") == "calib":
        s += "_calib"
    return s


# ------------------------------------------------------------------------------------------------ machine guard + runner
def mem_ok():
    """True unless cfg596_pm.py is running and free + inactive < 6 GB."""
    busy = subprocess.run(["pgrep", "-f", "cfg596_pm.py"], capture_output=True).returncode == 0
    if not busy:
        return True, None
    vm = subprocess.run(["vm_stat"], capture_output=True, text=True).stdout
    page = int(vm.split("page size of ")[1].split()[0])
    get = lambda k: int(next(l for l in vm.splitlines() if l.startswith(k)).split(":")[1].strip(" ."))
    gb = (get("Pages free") + get("Pages inactive")) * page / 1e9
    return gb >= 6.0, gb


def _child(c, fn):
    os.nice(0)
    cc = dict(c); cc["v0"] = cc["v0_kms"] * L.KMS
    res = CL.run(cc)
    json.dump(M623._round(res), open(fn + ".tmp", "w")); os.replace(fn + ".tmp", fn)


def run_one(c):
    fn = os.path.join(RUNS, name_of(c) + ".json")
    if not os.path.exists(fn):
        while True:
            ok, gb = mem_ok()
            if ok:
                break
            print(f"    [guard] cfg596 running, free+inactive {gb:.1f} GB < 6: waiting", flush=True); time.sleep(120)
        t0 = time.time()
        p = mp.get_context("fork").Process(target=_child, args=(c, fn)); p.start(); p.join()
        rss = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss / 1e9
        print(f"    ran {name_of(c)} in {time.time() - t0:.0f} s (peak child RSS so far {rss:.2f} GB)", flush=True)
        if p.exitcode != 0:
            raise RuntimeError(f"run failed: {name_of(c)}")
    return json.load(open(fn))


def load_json(stem):
    fn = os.path.join(HERE, f"cfg625_{stem}_results.json")
    return json.load(open(fn)) if os.path.exists(fn) else None


def base_cfg(V):
    cal = load_json(f"calib_{V}")
    if not cal or not cal.get("ok"):
        return None
    return dict(variant=V, v0_kms=float(round(cal["v0_kms"], 1)), eta=float(f"{cal['eta']:.4g}"))


# ------------------------------------------------------------------------------------------------ static (C0, M-RAW i)
def phase_static():
    P("CFG625 static: C0 (BASE == Progenitor599) and t = 0 progenitor masses (M-RAW part i; reported, not a verdict)")
    R = {"lane": "CFG625", "phase": "static"}
    mx = 0.0
    for foot in FEET:
        for M, cl in ((1.5e15, False), (1.5e14, True)):
            for sw in (False, True):
                a = L.Progenitor599(M, foot, swap=sw, cloud=cl); b = CL.Progenitor625(M, foot, swap=sw, cloud=cl, variant="BASE")
                for k in ("r", "rho_g", "P", "rho_s", "rho_ph", "Mph", "rho_cc"):
                    x, y = getattr(a, k), getattr(b, k)
                    mx = max(mx, float(np.max(np.abs(x - y) / np.maximum(np.abs(x), 1e-300))))
    R["C0"] = dict(ok=bool(mx <= 1e-12), max_rel_diff=mx)
    P(f"  C0 max relative difference over r, rho_g, P, rho_s, rho_ph, M_ph, rho_cc (main/sub, swap/not, both footings): {mx:.3g} "
      f"-> {'PASS' if mx <= 1e-12 else 'FAIL'}")
    tab = {}
    P("\n  t = 0 progenitor masses (Msun). proj250 = projected inside 250 kpc of the centre; *100 = stars projected in 100 kpc")
    P(f"  {'var':4s} {'foot':4s} {'prog':4s} | {'M_b':>9s} {'stars':>9s} {'gas':>9s} {'cloud':>9s} {'cold':>9s} | {'b_p250':>9s} "
      f"{'cold_p250':>9s} {'tot_p250':>9s} {'P16':>8s} {'ratio':>6s} | {'*100':>8s} {'C06':>8s} | rho_m_floor ratio")
    for V in ["BASE"] + CL.VARIANTS:
        for foot in FEET:
            for M, cl, role in ((1.5e15, False, "main"), (1.5e14, True, "sub")):
                p = CL.Progenitor625(M, foot, cloud=cl, variant=V)
                s = p.static_masses()
                s["tot_proj250"] = s["Mb_proj250"] + s["Mcold_proj250"]
                s["P16"] = CL.P16_M250[role][0]; s["ratio_to_P16"] = s["tot_proj250"] / s["P16"]
                s["shortfall_P16"] = s["P16"] - s["tot_proj250"]
                if role == "main":
                    s["rho_m_floor_ratio"] = float((p.rho_g[1] + p.rho_s[1] + p.rho_ph[1] + p.rho_cc[1]) / p.rho_g[1])
                tab[f"{V}_{foot}_{role}"] = s
                P(f"  {V:4s} {foot:4s} {role:4s} | {s['Mb']:9.3e} {s['Mstars']:9.3e} {s['Mgas']:9.3e} {s['Mcloud']:9.3e} {s['Mcold']:9.3e} | "
                  f"{s['Mb_proj250']:9.3e} {s['Mcold_proj250']:9.3e} {s['tot_proj250']:9.3e} {s['P16']:8.2e} {s['ratio_to_P16']:6.3f} | "
                  f"{s['Mstars_proj100']:8.2e} {CL.C06_MSTAR100[role]:8.2e} | {s.get('rho_m_floor_ratio', '')}")
    R["masses_t0"] = tab
    finish("static", R); return 0 if R["C0"]["ok"] else 1


# ------------------------------------------------------------------------------------------------ C1-C6
def phase_c16():
    P("CFG625 shared gates: C1-C3, C5, C6 re-run (CFG621 control code, unchanged); C4(a) from that code; C4(b), N_B re-read")
    R = {"lane": "CFG625", "phase": "c16"}
    src = open(os.path.join(C621, "cfg621_controls.py")).read()
    src = src[:src.index('open(os.path.join(HERE, "cfg621_controls.out")')]
    src = src.replace('HERE = os.path.dirname(os.path.abspath(__file__))', f'HERE = {C621!r}')
    ns = {"__name__": "cfg621_controls_in_cfg625", "__file__": os.path.join(C621, "cfg621_controls.py")}
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        exec(compile(src, "cfg621_controls.py[read-only]", "exec"), ns)
    c16 = ns["RES"]
    for line in ns["OUT"]:
        P("  " + line)
    c4 = M623.SA["C4b_T4"]
    P(f"  C4(b) (CFG621 stage-A T-4, re-read): {'PASS' if c4['ok'] else 'FAIL'}; N_B = {M623.N_B:.3f}")
    R.update(C1_C6=c16, C4b=c4, N_B=M623.N_B, ok=bool(c16["all_pass"] and c4["ok"] and M623.N_B <= 1))
    P(f"SHARED GATES: {'PASS' if R['ok'] else 'FAIL'}")
    finish("c16", R); return 0 if R["ok"] else 1


# ------------------------------------------------------------------------------------------------ calibration
def bracket_search(evaluate, lo, hi, target, stop, rounds=4, increasing=True, log=False):
    """CFG621's bracket_search (cfg621_main.py), verbatim."""
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


def phase_calib(V):
    P(f"CFG625 calibration, variant {V}: CFG621's procedure (serial), alpha = 0, canonical, seed 599, calib mode; "
      f"K1 2700 +- 200 km/s, G1 194 +- 50 kpc, eta in [0.1, 2.5]")
    cc = lambda v0, eta: dict(variant=V, alpha=0.0, foot="can", v0_kms=float(round(v0, 1)), eta=float(f"{eta:.4g}"), mode="calib")
    log = {"rounds": []}
    eta = 1.0; v0 = None
    for rnd in range(2):
        def ev_v(xs, eta=eta):
            out = []
            for x in xs:
                r = run_one(cc(x, eta)); out.append(r.get("v_obs_kms", float("nan")))
                P(f"    K1  v0 = {x:7.1f} km/s, eta = {eta:.4g}: speed {r.get('v_obs_kms', float('nan')):7.1f} km/s, d_SG {r.get('dSG_obs', float('nan')):6.1f} kpc")
            return out
        P(f"  round {rnd + 1}: v0 bracketing on [0, 4000] km/s at eta = {eta:.4g}")
        v0, vbest, hv, okv = bracket_search(ev_v, 0.0, 4000.0, V_TARGET, V_STOP)
        r0 = run_one(cc(0.0, eta))
        if r0.get("v_obs_kms", 0) > V_TARGET + V_TOL:
            R = dict(ok=False, reason="K1 infeasible: v0 = 0 already exceeds 2900 km/s", log=log); finish(f"calib_{V}", R); return 1

        def ev_e(xs, v0=v0):
            out = []
            for x in xs:
                r = run_one(cc(v0, x)); out.append(r.get("dSG_obs", float("nan")))
                P(f"    G1  v0 = {v0:7.1f} km/s, eta = {x:.4g}: d_SG {r.get('dSG_obs', float('nan')):6.1f} kpc, speed {r.get('v_obs_kms', float('nan')):7.1f} km/s")
            return out
        P(f"  round {rnd + 1}: eta bracketing on [0.03, 10] (log) at v0 = {v0:.1f} km/s")
        eta, dbest, he, oke = bracket_search(ev_e, 0.03, 10.0, DSG_OBS, DSG_STOP, log=True)
        eta = float(f"{eta:.4g}")
        rf = run_one(cc(v0, eta))
        k1 = abs(rf["v_obs_kms"] - V_TARGET) <= V_TOL; g1 = abs(rf["dSG_obs"] - DSG_OBS) <= DSG_TOL
        log["rounds"].append(dict(v0_history=hv, eta_history=he, v0=v0, eta=eta, final_speed=rf.get("v_obs_kms"),
                                  final_dSG=rf.get("dSG_obs"), v_bracket_ok=okv, eta_bracket_ok=oke))
        P(f"  round {rnd + 1} result: v0 = {v0:.1f} km/s, eta = {eta:.4g} -> speed {rf['v_obs_kms']:.1f} km/s (K1 {'in' if k1 else 'OUT'}), "
          f"d_SG {rf['dSG_obs']:.1f} kpc (G1 {'in' if g1 else 'OUT'})")
        if k1 and g1:
            break
    inr = ETA_RANGE[0] <= eta <= ETA_RANGE[1]
    ok = bool(k1 and g1 and inr)
    R = dict(lane="CFG625", phase="calib", variant=V, ok=ok, v0_kms=v0, eta=eta, speed_kms=rf["v_obs_kms"], dSG=rf["dSG_obs"],
             K1=bool(k1), G1=bool(g1), eta_in_range=bool(inr), Mproj_obs=rf.get("Mproj_obs"), log=log,
             reason=None if ok else ("eta outside [0.1, 2.5]" if (k1 and g1) else "K1/G1 not met after two rounds"))
    P(f"CALIBRATION {V}: {'PASS' if ok else 'FAIL (variant VOID): ' + R['reason']}  (CFG623: v0 2666.7, eta 1.132)")
    finish(f"calib_{V}", R); return 0 if ok else 1


# ------------------------------------------------------------------------------------------------ controls (C7, C9)
def phase_controls(V):
    B = base_cfg(V)
    P(f"CFG625 controls, variant {V}: alpha {{0, inf}} x seeds {CTRL_SEEDS} x both footings; C7, C9 (CFG623 rule); B-6 printed")
    R = {"lane": "CFG625", "phase": "controls", "variant": V}
    if B is None:
        P("calibration not passed: variant VOID"); R["status"] = "VOID"; finish(f"controls_{V}", R); return 1
    cfgs = [dict(alpha=a, foot=f, seed=sd, **B) for f in FEET for a in (0.0, math.inf) for sd in CTRL_SEEDS]
    runs = [run_one(c) for c in cfgs]
    c7 = [float(np.hypot(*(np.array(r["diag"][0]["sub"]["lens"]) - np.array(r["diag"][0]["sub"]["lens_nomask"])))) for r in runs]
    c7ok = max(c7) <= 3.0
    P(f"  C7 max |E-M - unmasked| at t = 0 = {max(c7):.3f} kpc -> {'PASS' if c7ok else 'FAIL'}")
    sc = {f"{astr(c['alpha'])}_{c['foot']}_seed{c['seed']}": score_run(r) for c, r in zip(cfgs, runs)}
    c9 = {}
    for f in FEET:
        for a in (0.0, math.inf):
            ks = [f"{astr(a)}_{f}_seed{sd}" for sd in CTRL_SEEDS]
            nb = sum(bool(sc[k].get("scorable_B")) for k in ks); nh = sum(bool(sc[k].get("scorable_H")) for k in ks)
            c9[f"{astr(a)}_{f}"] = dict(n_bullet_stable=nb, n_harvey_scorable=nh, ok=bool(nb >= 2 and nh >= 2),
                                        harvey_used=[f"{sc[k].get('harvey_n_used')}/{sc[k].get('harvey_n_window')}" for k in ks],
                                        f=[sc[k].get("f") for k in ks], beta_bar=[sc[k].get("beta_bar", sc[k].get("beta_bar_reported")) for k in ks],
                                        status=[sc[k]["status"] for k in ks])
            d = c9[f"{astr(a)}_{f}"]
            P(f"  C9 alpha {astr(a):>3s} {f}: Bullet stable {nb}/3, Harvey scorable {nh}/3 ({d['harvey_used']}) -> {'PASS' if d['ok'] else 'FAIL'}; "
              f"f {[None if x is None else round(x, 3) for x in d['f']]}, beta-bar {[None if x is None else round(x, 3) for x in d['beta_bar']]}")
    c9ok = all(v["ok"] for v in c9.values())
    R.update(C7=dict(ok=bool(c7ok), max_kpc=max(c7)), C9=dict(ok=bool(c9ok), cells=c9), control_scores=sc,
             status="PASS" if (c7ok and c9ok) else "VOID")
    P(f"CONTROLS {V}: {R['status']}")
    finish(f"controls_{V}", R); return 0 if R["status"] == "PASS" else 1


# ------------------------------------------------------------------------------------------------ MUTATE
def phase_mutate(V):
    B = base_cfg(V)
    P(f"CFG625 MUTATE, variant {V}: M1 (alpha = inf, grid run), M2 (alpha = 0, grid run), M3 (roles swapped, alpha = inf)")
    R = {"lane": "CFG625", "phase": "MUTATE", "variant": V}
    ctl = load_json(f"controls_{V}")
    if B is None or not ctl or ctl.get("status") != "PASS":
        P("calibration/controls not passed: MUTATE not run"); R["all_pass"] = False; finish(f"MUTATE_{V}", R); return 1
    cfgs = {"M1": dict(alpha=math.inf, foot="can", **B), "M2": dict(alpha=0.0, foot="can", **B),
            "M3": dict(alpha=math.inf, foot="can", swap=True, **B)}
    sc = {k: score_run(run_one(c)) for k, c in cfgs.items()}
    m1 = bool(sc["M1"].get("f") is not None and sc["M1"]["f"] >= 0.5)
    bb2 = sc["M2"]["beta_bar"] if sc["M2"].get("scorable_H") else sc["M2"].get("beta_bar_asrun_window")
    m2 = bool(sc["M2"].get("f") is not None and abs(sc["M2"]["f"]) <= 0.25 and bb2 is not None and bb2 <= 0.10)
    m3 = bool(sc["M3"].get("f") is not None and sc["M3"]["f"] <= 0.25)
    P(f"  M1 alpha = inf: f = {sc['M1'].get('f')} (>= 0.5) -> {'PASS' if m1 else 'FAIL'}")
    P(f"  M2 alpha = 0: f = {sc['M2'].get('f')} (|f| <= 0.25), beta-bar = {bb2} (<= 0.10; {sc['M2'].get('harvey_n_used')}/"
      f"{sc['M2'].get('harvey_n_window')}) -> {'PASS' if m2 else 'FAIL'}")
    P(f"  M3 swapped alpha = inf: f = {sc['M3'].get('f')} (<= 0.25) -> {'PASS' if m3 else 'FAIL'}")
    R.update(M1=dict(ok=m1, score=sc["M1"]), M2=dict(ok=m2, beta_bar_used=bb2, score=sc["M2"]), M3=dict(ok=m3, score=sc["M3"]),
             all_pass=bool(m1 and m2 and m3))
    P(f"MUTATE {V}: {'ALL PASS' if R['all_pass'] else 'SOME FAIL (variant VOID)'}")
    finish(f"MUTATE_{V}", R); return 0


# ------------------------------------------------------------------------------------------------ grid
def epoch_mass(run):
    tp = run["t_peri"]; ep = M623.S.epoch(run["diag"], tp) if tp is not None else None
    if ep is None:
        return None
    i, w = ep["i_obs"], ep["w_obs"]; out = {}
    for nm in ("main", "sub"):
        for R in (250, 300):
            a, b = run["diag"][i - 1][nm][f"Mproj{R}"], run["diag"][i][nm][f"Mproj{R}"]
            out[f"{nm}_{R}"] = dict(zip(("total", "baryons", "cold"), [x + w * (y - x) for x, y in zip(a, b)]))
    return out


def verdicts(cells, fv, nodes):
    def st(a, f):
        k = f"{astr(a)}_{f}"
        if k not in cells:
            return "NOT RUN"
        return "VOID" if not fv[f]["valid"] else cells[k]["status"]
    allowed = {f: [astr(a) for a in nodes if st(a, f) == "ALLOWED"] for f in FEET}
    excluded = {f: [astr(a) for a in nodes if st(a, f) == "EXCLUDED"] for f in FEET}
    unsc = {f: [astr(a) for a in nodes if st(a, f) in ("UNSCORABLE", "VOID")] for f in FEET}
    V = {}
    zinf = [cells.get(f"inf_{f}", {}) for f in FEET]
    if all(fv[f]["valid"] and z.get("scorable_B") for f, z in zip(FEET, zinf)):
        V["V1_instant_resettling"] = "EXCLUDED" if all(z["Z_B"] >= 3 for z in zinf) else "NOT EXCLUDED"
    else:
        V["V1_instant_resettling"] = "UNDETERMINED (alpha = inf unscorable or a footing VOID)"
    s0 = [st(0.0, f) for f in FEET]
    V["V2_pure_collisionless"] = ("ALLOWED" if all(s == "ALLOWED" for s in s0) else
                                  ("NOT ALLOWED" if all(s in ("ALLOWED", "EXCLUDED") for s in s0) else "UNDETERMINED"))
    both = lambda a: all(st(a, f) == "ALLOWED" for f in FEET)
    tag = "" if len(nodes) == 8 else " [4-node]"
    if both(1.0):
        V["V3_galaxy_side"] = "COMPATIBLE" + tag
    elif any(both(a) for a in (3.0, 10.0, math.inf) if a in nodes):
        V["V3_galaxy_side"] = "PARTIAL (alpha = 1 not allowed; only nodes outside the causality bound alpha <~ 1)" + tag
    else:
        V["V3_galaxy_side"] = "INCOMPATIBLE (no node alpha >= 1 allowed on both footings)" + tag
    if V["V2_pure_collisionless"] == "ALLOWED" and V["V1_instant_resettling"] == "EXCLUDED":
        V["V4_summary"] = "collisionless component that re-settles slowly; allowed nodes listed"
    elif V["V1_instant_resettling"] == "NOT EXCLUDED":
        V["V4_summary"] = "merger data do not separate 'locked to baryons' from 'collisionless'"
    elif V["V2_pure_collisionless"] == "NOT ALLOWED" and not any(allowed[f] for f in FEET):
        V["V4_summary"] = "NO alpha works (a real failure)"
    else:
        V["V4_summary"] = "mixed; see the per-node table"
    return V, allowed, excluded, unsc


def phase_grid(V, full=False):
    B = base_cfg(V)
    nodes = ALPHAS if full else NODES4
    P(f"CFG625 grid, variant {V}: nodes {[astr(a) for a in nodes]} x both footings (seed 599)")
    R = {"lane": "CFG625", "phase": "grid", "variant": V, "void_reasons": [], "nodes": [astr(a) for a in nodes]}
    if B is None:
        R["void_reasons"].append("calibration failed"); R["status"] = "VOID"; finish(f"grid_{V}", R); return 1
    ctl = load_json(f"controls_{V}"); mut = load_json(f"MUTATE_{V}"); c16 = load_json("c16"); stc = load_json("static")
    if not (c16 and c16.get("ok") and stc and stc["C0"]["ok"]):
        R["void_reasons"].append("shared gates (C1-C6, C4, C0) not passed")
    if not ctl or ctl.get("status") != "PASS":
        R["void_reasons"].append("controls (C7/C9) not passed")
    if not (mut and mut.get("all_pass")):
        R["void_reasons"].append("MUTATE M1-M3 not all passing" if mut else "MUTATE not run")
    R["calibration"] = B
    order = [(a, f) for a in nodes for f in FEET]
    cells, runs = {}, {}
    for a, f in order:
        r = run_one(dict(alpha=a, foot=f, **B)); runs[f"{astr(a)}_{f}"] = r
        cells[f"{astr(a)}_{f}"] = score_run(r)
    R["cells"] = cells
    fv = {}
    for f in FEET:
        s0 = cells[f"0_{f}"]
        okf = (s0.get("speed_kms") is not None and abs(s0["speed_kms"] - V_TARGET) <= V_TOL and abs(s0["dSG"] - DSG_OBS) <= DSG_TOL)
        fv[f] = dict(valid=bool(okf), speed_kms=s0.get("speed_kms"), dSG=s0.get("dSG"))
    R["footing_validity_alpha0"] = fv
    R["epoch_masses_alpha0"] = {f: epoch_mass(runs[f"0_{f}"]) for f in FEET}
    R["Mph_tot"] = runs["0_can"].get("Mph_tot"); R["Mb"] = runs["0_can"].get("Mb")
    P("FOOTING VALIDITY at alpha = 0: " + json.dumps({f: {k: (round(v, 1) if isinstance(v, float) else v) for k, v in d.items()} for f, d in fv.items()}))
    ref = json.load(open(os.path.join(C623, "cfg623_results.json")))["cells"]
    P(f"\n{'alpha':>6s} {'foot':>4s} | {'f':>7s} {'Z_B':>6s} {'agree':>6s} {'stabB':>22s} | {'n_H':>6s} {'bbar':>7s} {'Z_H':>6s} | status   (CFG623)")
    for f in FEET:
        for a in nodes:
            k = f"{astr(a)}_{f}"; s = cells[k]
            stt = s["status"] if fv[f]["valid"] else s["status"] + " (footing VOID)"
            P(f"{astr(a):>6s} {f:>4s} | {s.get('f', float('nan')):+7.3f} {s.get('Z_B', float('nan')):+6.2f} {str(s.get('n_agree_obs')):>6s} "
              f"{str(s.get('stab_parts_obs')):>22s} | {s.get('harvey_n_used', 0):2d}/{s.get('harvey_n_window', 0):2d} "
              f"{s.get('beta_bar', s.get('beta_bar_reported', float('nan'))):+7.3f} {s.get('Z_H', float('nan')):+6.2f} | {stt}   ({ref[k]['status']})")
    Vd, allowed, excluded, unsc = verdicts(cells, fv, nodes)
    R.update(verdicts=Vd, allowed_set=allowed, excluded_set=excluded, unscorable_or_void=unsc)
    R["status"] = "VALID" if not R["void_reasons"] else "VOID"
    P(f"\nALLOWED: can {allowed['can']} alt {allowed['alt']}; EXCLUDED: can {excluded['can']} alt {excluded['alt']}; "
      f"UNSCORABLE/VOID: can {unsc['can']} alt {unsc['alt']}")
    P("VERDICTS" + ("" if R["status"] == "VALID" else f"  -- STATUS VOID: {R['void_reasons']}"))
    for k, v in Vd.items():
        P(f"  {k}: {v}")
    em = R["epoch_masses_alpha0"]
    for f in FEET:
        if em[f]:
            P(f"  M-RAW (alpha = 0 {f}, Bullet epoch) projected M(<250): main {em[f]['main_250']['total']:.3e} (P16 2.5e14), sub "
              f"{em[f]['sub_250']['total']:.3e} (P16 2.0e14); M(<300): main {em[f]['main_300']['total']:.3e} (R26 3.5e14), sub "
              f"{em[f]['sub_300']['total']:.3e} (R26 2.3e14)")
    finish(f"grid_{V}", R); return 0


# ------------------------------------------------------------------------------------------------ summary
def phase_summary():
    P("CFG625 summary: robustness of CFG623's alpha verdicts under data-based baryons (FROZEN_CRITERIA.md section 6); M-RAW report")
    ref = json.load(open(os.path.join(C623, "cfg623_results.json")))
    refc, refV = ref["cells"], ref["verdicts"]
    R = {"lane": "CFG625", "phase": "summary", "variants": {}}
    for V in CL.VARIANTS:
        g = load_json(f"grid_{V}")
        if not g or g.get("status") != "VALID":
            R["variants"][V] = dict(tested=False, reason=(g or {}).get("void_reasons", "not run"))
            P(f"  {V}: NOT TESTED ({R['variants'][V]['reason']})"); continue
        flips, lost, new = [], [], []
        for k, s in g["cells"].items():
            a, f = k.split("_")
            st = s["status"] if g["footing_validity_alpha0"][f]["valid"] else "UNSCORABLE"
            r0 = refc[k]["status"]
            if {st, r0} == {"ALLOWED", "EXCLUDED"}:
                flips.append(f"{k}: {r0} -> {st}")
            elif r0 in ("ALLOWED", "EXCLUDED") and st == "UNSCORABLE":
                lost.append(f"{k}: {r0} -> UNSCORABLE")
            elif r0 == "UNSCORABLE" and st in ("ALLOWED", "EXCLUDED"):
                new.append(f"{k}: UNSCORABLE -> {st}")
        Vd = g["verdicts"]
        for key in ("V1_instant_resettling", "V2_pure_collisionless", "V4_summary"):
            if Vd[key] != refV[key]:
                flips.append(f"{key}: '{refV[key]}' -> '{Vd[key]}'")
        if not Vd["V3_galaxy_side"].startswith("INCOMPATIBLE"):
            flips.append(f"V3: -> {Vd['V3_galaxy_side']}")
        reading = "NOT ROBUST" if flips else ("ROBUST WITH WEAKENING" if lost else "VERDICTS ROBUST")
        R["variants"][V] = dict(tested=True, nodes=g["nodes"], flips=flips, lost=lost, newly_scored=new, reading=reading,
                                allowed=g["allowed_set"], excluded=g["excluded_set"], verdicts=Vd)
        P(f"  {V} (nodes {g['nodes']}): {reading}; allowed {g['allowed_set']}; excluded {g['excluded_set']}")
        for x in flips:
            P(f"     FLIP  {x}")
        for x in lost:
            P(f"     LOST  {x}")
        for x in new:
            P(f"     NEW   {x}")
    tested = [v for v in R["variants"].values() if v["tested"]]
    if not tested:
        R["lane_reading"] = "NO VARIANT TESTED"
    elif any(v["reading"] == "NOT ROBUST" for v in tested):
        R["lane_reading"] = "NOT ROBUST"
    elif any(v["reading"] == "ROBUST WITH WEAKENING" for v in tested):
        R["lane_reading"] = "ROBUST WITH WEAKENING"
    else:
        R["lane_reading"] = "VERDICTS ROBUST"
    R["coverage"] = {V: (v.get("nodes") if v["tested"] else None) for V, v in R["variants"].items()}
    P(f"\nLANE READING (over the valid variants and nodes run): {R['lane_reading']}; coverage {R['coverage']}")
    # M-RAW anchor rule (section 4.5): Bullet-epoch projected M(<250) of the alpha = 0 run vs P16 - 2 sigma
    P("\nM-RAW anchor (projected total M(<250 kpc) at the Bullet epoch, alpha = 0 grid run; MET iff >= P16 - 2 sigma)")
    anc = {}
    for V in CL.VARIANTS:
        g = load_json(f"grid_{V}")
        if not g or not g.get("epoch_masses_alpha0"):
            continue
        for f in FEET:
            em = g["epoch_masses_alpha0"][f]
            if not em:
                continue
            for nm in ("main", "sub"):
                m, s = CL.P16_M250[nm]; tot = em[f"{nm}_250"]["total"]
                anc[f"{V}_{f}_{nm}"] = dict(model=tot, baryons=em[f"{nm}_250"]["baryons"], cold=em[f"{nm}_250"]["cold"], P16=m,
                                            met=bool(tot >= m - 2 * s), shortfall=m - tot, ratio=tot / m,
                                            M300=em[f"{nm}_300"]["total"], R26=CL.R26_M300[nm])
                a = anc[f"{V}_{f}_{nm}"]
                P(f"  {V} {f} {nm}: model {tot:.3e} (baryons {a['baryons']:.3e}, cold {a['cold']:.3e}) vs P16 {m:.2e}: "
                  f"{'MET' if a['met'] else 'NOT MET'}, ratio {a['ratio']:.3f}, shortfall {a['shortfall']:.3e}; M(<300) {a['M300']:.3e} vs R26 {a['R26']:.2e}")
    R["M_RAW_anchor"] = anc
    finish("summary", R); return 0


if __name__ == "__main__":
    ph = sys.argv[1]
    arg = sys.argv[2] if len(sys.argv) > 2 else None
    if ph == "grid":
        sys.exit(phase_grid(arg, full=(len(sys.argv) > 3 and sys.argv[3] == "all")))
    fn = {"static": phase_static, "c16": phase_c16, "summary": phase_summary,
          "calib": phase_calib, "controls": phase_controls, "mutate": phase_mutate}[ph]
    sys.exit(fn(arg) if arg else fn())
