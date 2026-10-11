#!/usr/bin/env python3
"""CFG623 main (criteria FROZEN_CRITERIA.md): CFG622's pipeline (simulator cfg622_sim.py with the merger-safe lensing estimator
E-M, imported read-only) with ONLY the two changes of the criteria:
  (a) the Harvey / M2 window opens once the sub's galaxy-gas separation d_SG >= 200 kpc (= 4 a_cc), and
  (b) the per-epoch stability rule is a strict-majority agreement (>= 3 of the 4 E-M variants within T_L = 24.90 kpc of the E-M
      primary) plus CFG622's edge and gas guards (75 kpc); no percentile of a merger spread is taken; checked on controls (C9).
kappa = 1/2 FITTED; footings never pooled; the cold energy's mass is an input.  Yardsticks: raw data only.

Phases (gate order, FROZEN_CRITERIA.md section 3):
  nice -n 10 python3 cfg623_main.py controls   -> cfg623_controls.out/_results.json  (C1-C3, C5, C6 re-run; C4a/C4b/N_B re-read;
                                                  12 control runs seeds 603-605; C7; C9; seed scatter; calibration check B-4)
  nice -n 10 python3 cfg623_main.py mutate     -> cfg623_MUTATE.out, cfg623_results_MUTATE.json  (M1-M3, M3-alpha0, M4)
  nice -n 10 python3 cfg623_main.py grid       -> cfg623.out, cfg623_results.json  (16-run grid, scores, verdicts, C8)
Per-run time series cached in runs/ (resumable).  <= 4 worker processes of 1 thread."""
import os
os.environ["OMP_NUM_THREADS"] = "1"
import sys, json, math, time, io, contextlib
import multiprocessing as mp
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
C622 = os.path.join(HERE, "..", "CFG622_merger_stopwatch_v4")
C621 = os.path.join(HERE, "..", "CFG621_merger_stopwatch_v3")
sys.path.insert(0, C622)
import cfg622_sim as S  # noqa: E402 (read-only; puts CFG621 and CFG599 on sys.path)
import cfg599_lib as L  # noqa: E402

RUNS = os.path.join(HERE, "runs"); os.makedirs(RUNS, exist_ok=True)
ALPHAS = [0.0, 0.03, 0.1, 0.3, 1.0, 3.0, 10.0, math.inf]
FEET = ["can", "alt"]
CTRL_SEEDS = [603, 604, 605]
V_TARGET, V_TOL = 2700.0, 200.0
DSG_OBS, DSG_TOL = 194.0, 50.0
ETA_RANGE = (0.1, 2.5)
F_OBS, SIG_F = 0.045, 0.125
HARV_B, HARV_S = -0.04, 0.07
GUARD = 75.0
A_CC = L.A_CC                      # 50 kpc, CFG599 M-3b cool-core Plummer scale
DSG_H = 4.0 * A_CC                 # (a) Harvey window opens at d_SG >= 200 kpc
N_AGREE = 3                        # (b) >= 3 of the 4 variants within T_L of the primary
SA = json.load(open(os.path.join(C621, "cfg621_stageA_results.json")))
T_L, N_B = SA["T_L"], SA["N_B"]
CAL621 = json.load(open(os.path.join(C621, "cfg621_results.json")))["calibration"]
V0, ETA = CAL621["v0_kms"], CAL621["eta"]
BASE = dict(v0_kms=float(round(V0, 1)), eta=float(f"{ETA:.4g}"))
OUT = []


def P(s=""):
    print(s, flush=True); OUT.append(str(s))


def astr(a):
    return "inf" if math.isinf(a) else f"{a:g}"


def name_of(c):
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
    import cfg622_sim as SS
    fn = os.path.join(RUNS, name_of(c) + ".json")
    if os.path.exists(fn):
        return
    cc = dict(c); cc["v0"] = cc["v0_kms"] * L.KMS
    res = SS.run(cc)
    json.dump(_round(res), open(fn + ".tmp", "w")); os.replace(fn + ".tmp", fn)


def pool_map(cfgs):
    todo = [c for c in cfgs if not os.path.exists(os.path.join(RUNS, name_of(c) + ".json"))]
    if todo:
        P(f"  running {len(todo)} run(s) on <= 4 processes ...")
        with mp.get_context("fork").Pool(min(4, len(todo))) as pool:
            pool.map(worker, todo, chunksize=1)
    return [json.load(open(os.path.join(RUNS, name_of(c) + ".json"))) for c in cfgs]


# ------------------------------------------------------------------------------------------------ observables
def beta_of(d, key="lens"):
    s = d["sub"]
    gal, gas, lens = np.array(s["gal"]), np.array(s["gas"]), np.array(s[key])
    e = gas - gal; n = np.linalg.norm(e)
    if n <= 0:
        return float("nan"), n
    return float(np.dot(lens - gal, e) / n ** 2), float(n)


def beta_cold(d):
    s = d["sub"]
    gal, gas, c = np.array(s["gal"]), np.array(s["gas"]), np.array(s["cold"])
    e = gas - gal; n = np.linalg.norm(e)
    return float(np.dot(c - gal, e) / n ** 2) if n > 0 else float("nan")


def n_agree(d):
    s = d["sub"]; l0 = np.array(s["lens"])
    return int(sum(np.hypot(*(np.array(x) - l0)) <= T_L for x in s["lens_alts"]))


def stab_parts(d):
    """(b) majority agreement, edge guard, gas guard (FROZEN_CRITERIA.md B-3')."""
    s = d["sub"]
    a = n_agree(d) >= N_AGREE
    b = min([s["lens_edge"]] + list(s["alts_edge"])) >= GUARD
    c = s["gas_edge"] >= GUARD
    return a, b, c


def stable(d):
    return all(stab_parts(d))


def window(diag, tp):
    """(a) Harvey window: t - t_peri in [0.1, 0.6] Gyr AND d_SG >= 200 kpc."""
    return [d for d in diag if 0.1 - 1e-9 <= d["t"] - tp <= 0.6 + 1e-9 and beta_of(d)[1] >= DSG_H]


def score_run(run):
    tp = run["t_peri"]
    if tp is None:
        return dict(scorable_B=False, scorable_H=False, status="UNSCORABLE", note="no pericentre")
    diag = run["diag"]
    ep = S.epoch(diag, tp)
    out = dict(t_peri=tp)
    if ep is None:
        out.update(scorable_B=False, note="720-kpc epoch not reached")
    else:
        i, w = ep["i_obs"], ep["w_obs"]
        b0, _ = beta_of(diag[i - 1]); b1, _ = beta_of(diag[i])
        f = b0 + w * (b1 - b0)
        u0, _ = beta_of(diag[i - 1], "lens_nomask"); u1, _ = beta_of(diag[i], "lens_nomask")
        parts = [stab_parts(diag[j]) for j in (i - 1, i)]
        st = all(all(p) for p in parts)
        fc = beta_cold(diag[i - 1]) + w * (beta_cold(diag[i]) - beta_cold(diag[i - 1]))
        out.update(t_obs_after_peri=ep["t_obs"] - tp, speed_kms=ep["v_obs_kms"], dSG=ep["dSG_obs"], f=f, f_coldpeak=fc,
                   f_nomask_reported=u0 + w * (u1 - u0),
                   n_agree_obs=[n_agree(diag[j]) for j in (i - 1, i)],
                   lens_spread_obs=[diag[j]["sub"]["lens_spread"] for j in (i - 1, i)],
                   min_lens_edge_obs=[min([diag[j]["sub"]["lens_edge"]] + diag[j]["sub"]["alts_edge"]) for j in (i - 1, i)],
                   gas_edge_obs=[diag[j]["sub"]["gas_edge"] for j in (i - 1, i)],
                   stab_parts_obs=[[bool(x) for x in p] for p in parts], scorable_B=bool(st), Z_B=(f - F_OBS) / SIG_F)
    win = window(diag, tp)
    good = [d for d in win if stable(d)]
    out["harvey_n_window"] = len(win); out["harvey_n_used"] = len(good)
    out["harvey_t_open"] = (win[0]["t"] - tp) if win else None
    out["harvey_fail_counts"] = dict(majority=sum(not stab_parts(d)[0] for d in win), edge=sum(not stab_parts(d)[1] for d in win),
                                     gas_guard=sum(not stab_parts(d)[2] for d in win))
    if len(good) >= 10 and len(good) >= 0.5 * len(win):
        bb = float(np.mean([beta_of(d)[0] for d in good]))
        out.update(scorable_H=True, beta_bar=bb, Z_H=(bb - HARV_B) / HARV_S)
    else:
        out.update(scorable_H=False)
        if good:
            out["beta_bar_reported"] = float(np.mean([beta_of(d)[0] for d in good]))
    if win:
        out["beta_bar_asrun_window"] = float(np.mean([beta_of(d)[0] for d in win]))
    q50 = [d for d in diag if 0.1 - 1e-9 <= d["t"] - tp <= 0.6 + 1e-9 and beta_of(d)[1] >= 50.0]
    if q50:
        out["beta_bar_cfg622_window_reported"] = float(np.mean([beta_of(d)[0] for d in q50]))
    for tsp in (0.5, 0.7):
        ts = [d["t"] for d in diag]; bs = [beta_of(d)[0] for d in diag]
        out[f"beta_tsp{tsp}"] = float(np.interp(tp + tsp, ts, bs)) if tp + tsp <= ts[-1] else None
    out["cap_frac"] = run["n_cap"] / max(run["n_mv"], 1)
    if out.get("scorable_B") and out.get("scorable_H"):
        out["status"] = "ALLOWED" if (abs(out["Z_B"]) < 2 and abs(out["Z_H"]) < 2) else "EXCLUDED"
    else:
        out["status"] = "UNSCORABLE"
    return out


def finish(R, tag):
    open(os.path.join(HERE, f"cfg623{tag}.out"), "w").write("\n".join(OUT) + "\n")
    fn = {"_controls": "cfg623_controls_results.json", "_MUTATE": "cfg623_results_MUTATE.json", "": "cfg623_results.json"}[tag]
    json.dump(R, open(os.path.join(HERE, fn), "w"), indent=1, default=lambda o: None)


def header(extra=""):
    P("CFG623: merger stopwatch v5 (CFG622 + Harvey window from d_SG >= 4 a_cc + majority-agreement stability rule)" + extra)
    P("criteria FROZEN_CRITERIA.md; kappa = 1/2 FITTED; footings 9.3603e-11 / 1.1312e-10 never pooled; candidate B; G9; no EFE;")
    P("cold energy's mass required (an input); no particle species; yardsticks = raw data only.")
    P(f"inherited calibration (CFG621): v0 = {V0} km/s, eta = {ETA}; T_L = {T_L:.2f} kpc; majority >= {N_AGREE}/4; guards {GUARD} kpc; "
      f"Harvey d_SG >= {DSG_H:.0f} kpc")


def load_ctrl():
    fn = os.path.join(HERE, "cfg623_controls_results.json")
    return json.load(open(fn)) if os.path.exists(fn) else None


# ------------------------------------------------------------------------------------------------ phase 1: controls
def phase_controls():
    T0 = time.time()
    header("  [controls]")
    R = {"lane": "CFG623", "phase": "controls", "inherited_calibration": dict(v0_kms=V0, eta=ETA), "T_L": T_L, "N_B": N_B,
         "DSG_H": DSG_H, "N_AGREE": N_AGREE}
    src = open(os.path.join(C621, "cfg621_controls.py")).read()
    src = src[:src.index('open(os.path.join(HERE, "cfg621_controls.out")')]
    src = src.replace('HERE = os.path.dirname(os.path.abspath(__file__))', f'HERE = {C621!r}')
    ns = {"__name__": "cfg621_controls_in_cfg623", "__file__": os.path.join(C621, "cfg621_controls.py")}
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        exec(compile(src, "cfg621_controls.py[read-only]", "exec"), ns)
    c16 = ns["RES"]
    for line in ns["OUT"]:
        P("  " + line)
    R["C1_C6"] = c16
    c4 = SA["C4b_T4"]
    P(f"  C4(b) (CFG621 stage-A T-4, re-read): {'PASS' if c4['ok'] else 'FAIL'}; N_B = {N_B:.3f} ({'<= 1' if N_B <= 1 else '> 1'})")
    R["C4b"] = c4
    gate1 = bool(c16["all_pass"] and c4["ok"] and N_B <= 1)
    R["gate1"] = gate1
    if not gate1:
        P("GATE 1 FAILED: VOID"); R["status"] = "VOID"; finish(R, "_controls"); return 1

    cfgs = [dict(alpha=a, foot=f, seed=sd, **BASE) for f in FEET for a in (0.0, math.inf) for sd in CTRL_SEEDS]
    P(f"\nCONTROL ENSEMBLE: alpha {{0, inf}} x seeds {CTRL_SEEDS} x both footings ({len(cfgs)} runs; the grid uses seed 599 only)")
    runs = pool_map(cfgs)
    c7 = []
    for c, r in zip(cfgs, runs):
        d0 = r["diag"][0]["sub"]
        c7.append(float(np.hypot(*(np.array(d0["lens"]) - np.array(d0["lens_nomask"])))))
    c7ok = max(c7) <= 3.0
    P(f"  C7 mask null test at t = 0: max |E-M - unmasked| sub lensing peak = {max(c7):.3f} kpc (<= 3) -> {'PASS' if c7ok else 'FAIL'}")
    R["C7"] = dict(ok=bool(c7ok), max_kpc=max(c7), per_run=c7)
    sc = {}
    for c, r in zip(cfgs, runs):
        sc[f"{astr(c['alpha'])}_{c['foot']}_seed{c['seed']}"] = score_run(r)
    R["control_scores"] = sc
    # C9: the stability rule on controls (Bullet stable and Harvey scorable in >= 2 of 3 seeds per alpha x footing)
    c9 = {}
    for f in FEET:
        for a in (0.0, math.inf):
            ks = [f"{astr(a)}_{f}_seed{sd}" for sd in CTRL_SEEDS]
            nb = sum(bool(sc[k].get("scorable_B")) for k in ks); nh = sum(bool(sc[k].get("scorable_H")) for k in ks)
            c9[f"{astr(a)}_{f}"] = dict(n_bullet_stable=nb, n_harvey_scorable=nh, ok=bool(nb >= 2 and nh >= 2),
                                        harvey_used=[f"{sc[k].get('harvey_n_used')}/{sc[k].get('harvey_n_window')}" for k in ks],
                                        harvey_t_open=[sc[k].get("harvey_t_open") for k in ks])
            P(f"  C9 alpha {astr(a):>3s} {f}: Bullet stable {nb}/3, Harvey scorable {nh}/3 (used/window {c9[f'{astr(a)}_{f}']['harvey_used']}; "
              f"window opens at t-t_peri {[None if x is None else round(x, 2) for x in c9[f'{astr(a)}_{f}']['harvey_t_open']]}) -> "
              f"{'PASS' if c9[f'{astr(a)}_{f}']['ok'] else 'FAIL'}")
    c9ok = all(v["ok"] for v in c9.values())
    R["C9"] = dict(ok=bool(c9ok), cells=c9)
    # reported: two-peak epochs (primary > 300 kpc from the sub galaxies) and how the rule treats them
    tp_rows = []
    for c, r in zip(cfgs, runs):
        for d in r["diag"]:
            if r["t_peri"] is None or not (0.1 - 1e-9 <= d["t"] - r["t_peri"] <= 0.6 + 1e-9):
                continue
            s = d["sub"]
            if np.hypot(*(np.array(s["lens"]) - np.array(s["gal"]))) > 300.0:
                tp_rows.append(dict(run=name_of(c), t_after=round(d["t"] - r["t_peri"], 3), n_agree=n_agree(d), stable=bool(stable(d))))
    R["two_peak_epochs_reported"] = dict(n=len(tp_rows), n_flagged_unstable=sum(not x["stable"] for x in tp_rows), rows=tp_rows)
    P(f"  reported: {len(tp_rows)} control epochs with the primary > 300 kpc from the sub galaxies; flagged unstable: "
      f"{sum(not x['stable'] for x in tp_rows)}")
    B6 = {}
    for f in FEET:
        for a in (0.0, math.inf):
            ks = [f"{astr(a)}_{f}_seed{sd}" for sd in CTRL_SEEDS]
            fs = [sc[k].get("f") for k in ks]; bs = [sc[k].get("beta_bar", sc[k].get("beta_bar_reported")) for k in ks]
            sf = float(np.std([x for x in fs if x is not None], ddof=1)) if sum(x is not None for x in fs) >= 2 else None
            sb = float(np.std([x for x in bs if x is not None], ddof=1)) if sum(x is not None for x in bs) >= 2 else None
            B6[f"{astr(a)}_{f}"] = dict(f=fs, beta_bar=bs, sigma_seed_f=sf, sigma_seed_beta=sb, N_M=None if sf is None else sf / SIG_F,
                                       status=[sc[k]["status"] for k in ks])
            P(f"  seed scatter alpha {astr(a):>3s} {f}: f {[None if x is None else round(x, 3) for x in fs]} sigma {sf if sf is None else round(sf, 3)} "
              f"(N_M {None if sf is None else round(sf / SIG_F, 2)}); beta-bar {[None if x is None else round(x, 3) for x in bs]}; "
              f"status {B6[f'{astr(a)}_{f}']['status']}")
    R["B6_seed_scatter"] = B6
    R["B6_flag_footings"] = [f for f in FEET if any((B6[f"{astr(a)}_{f}"]["N_M"] or 0) > 1 for a in (0.0, math.inf))]
    if not c7ok or not c9ok:
        P(f"{'C7' if not c7ok else 'C9'} FAILED: VOID"); R["status"] = "VOID"; finish(R, "_controls"); return 1

    P("\nB-4 CALIBRATION CHECK (alpha = 0, canonical, seed 599, CFG621's v0 and eta; calib mode)")
    rc = pool_map([dict(alpha=0.0, foot="can", mode="calib", **BASE)])[0]
    k1 = abs(rc["v_obs_kms"] - V_TARGET) <= V_TOL; g1 = abs(rc["dSG_obs"] - DSG_OBS) <= DSG_TOL
    inr = ETA_RANGE[0] <= ETA <= ETA_RANGE[1]
    P(f"  speed {rc['v_obs_kms']:.1f} km/s (K1 {'in' if k1 else 'OUT of'} 2700 +- 200); d_SG {rc['dSG_obs']:.1f} kpc (G1 {'in' if g1 else 'OUT of'} "
      f"194 +- 50); eta {ETA} in [0.1, 2.5]: {inr}  (CFG621: {CAL621['speed_kms']:.1f} / {CAL621['dSG']:.1f})")
    R["calibration_check"] = dict(ok=bool(k1 and g1 and inr), speed_kms=rc["v_obs_kms"], dSG=rc["dSG_obs"], K1=bool(k1), G1=bool(g1),
                                  cfg621_speed=CAL621["speed_kms"], cfg621_dSG=CAL621["dSG"])
    if not R["calibration_check"]["ok"]:
        P("CALIBRATION CHECK FAILED: VOID"); R["status"] = "VOID"; finish(R, "_controls"); return 1
    R["status"] = "PASS"; R["wall_s"] = time.time() - T0
    P("\nGATES 1-3 (controls, C4, control ensemble + C7 + C9, calibration check): ALL PASS")
    finish(R, "_controls"); return 0


# ------------------------------------------------------------------------------------------------ phase 2: MUTATE
def phase_mutate():
    T0 = time.time()
    header("  [MUTATE]")
    ctl = load_ctrl()
    if not ctl or ctl.get("status") != "PASS":
        P("controls not passed: MUTATE not run"); return 1
    R = {"lane": "CFG623", "phase": "MUTATE"}
    cfgs = {"M1": dict(alpha=math.inf, foot="can", **BASE), "M2": dict(alpha=0.0, foot="can", **BASE),
            "M3": dict(alpha=math.inf, foot="can", swap=True, **BASE), "M3_a0": dict(alpha=0.0, foot="can", swap=True, **BASE),
            "M4": dict(alpha=0.0, foot="can", seed=600, **BASE)}
    rr = dict(zip(cfgs, pool_map(list(cfgs.values()))))
    sc = {k: score_run(v) for k, v in rr.items()}
    m1 = bool(sc["M1"].get("f") is not None and sc["M1"]["f"] >= 0.5)
    bb2 = sc["M2"]["beta_bar"] if sc["M2"].get("scorable_H") else sc["M2"].get("beta_bar_asrun_window")
    m2 = bool(sc["M2"].get("f") is not None and abs(sc["M2"]["f"]) <= 0.25 and bb2 is not None and bb2 <= 0.10)
    m3 = bool(sc["M3"].get("f") is not None and sc["M3"]["f"] <= 0.25)
    P(f"  M1 alpha = inf: f = {sc['M1'].get('f')} (>= 0.5; Bullet stable {sc['M1'].get('scorable_B')}) -> {'PASS' if m1 else 'FAIL'}")
    P(f"  M2 alpha = 0: f = {sc['M2'].get('f')} (|f| <= 0.25), beta-bar = {bb2} (<= 0.10; Harvey scorable {sc['M2'].get('scorable_H')}, "
      f"{sc['M2'].get('harvey_n_used')}/{sc['M2'].get('harvey_n_window')} epochs) -> {'PASS' if m2 else 'FAIL'}")
    P(f"  M3 roles swapped, alpha = inf: f = {sc['M3'].get('f')} (<= 0.25) -> {'PASS' if m3 else 'FAIL'}   [swapped alpha = 0: f = {sc['M3_a0'].get('f')}]")
    df = None if sc["M4"].get("f") is None or sc["M2"].get("f") is None else sc["M4"]["f"] - sc["M2"]["f"]
    P(f"  M4 seed 600 vs 599 at alpha = 0 (reported): delta f = {df}; beta-bar {sc['M4'].get('beta_bar')} vs {sc['M2'].get('beta_bar')}")
    R.update(M1=dict(ok=m1, score=sc["M1"]), M2=dict(ok=m2, beta_bar_used=bb2, score=sc["M2"]), M3=dict(ok=m3, score=sc["M3"]),
             M3_alpha0_reported=sc["M3_a0"], M4_reported=dict(score=sc["M4"], delta_f=df))
    R["all_pass"] = m1 and m2 and m3
    P(f"\nMUTATE M1-M3: {'ALL PASS' if R['all_pass'] else 'SOME FAIL (every verdict VOID)'}")
    R["wall_s"] = time.time() - T0
    finish(R, "_MUTATE"); return 0


# ------------------------------------------------------------------------------------------------ phase 3: grid + verdicts
def phase_grid():
    T0 = time.time()
    header()
    ctl = load_ctrl()
    mutf = os.path.join(HERE, "cfg623_results_MUTATE.json")
    mut = json.load(open(mutf)) if os.path.exists(mutf) else None
    R = {"lane": "CFG623", "phase": "grid", "void_reasons": []}
    if not ctl or ctl.get("status") != "PASS":
        R["void_reasons"].append("controls not passed")
    if not (mut and mut.get("all_pass")):
        R["void_reasons"].append("MUTATE M1-M3 not all passing" if mut else "MUTATE not run")
    R["MUTATE_gate"] = dict(all_pass=bool(mut and mut.get("all_pass")), M=({k: mut[k]["ok"] for k in ("M1", "M2", "M3")} if mut else None))
    cfgs = [dict(alpha=a, foot=f, **BASE) for f in FEET for a in ALPHAS]
    P(f"\nRUN GRID: {len(cfgs)} runs")
    runs = pool_map(cfgs)
    cells = {f"{astr(c['alpha'])}_{c['foot']}": score_run(r) for c, r in zip(cfgs, runs)}
    R["cells"] = cells
    # C8 reproduction vs CFG622 runs (reported): every diagnostic key of the sub, max over epochs
    c8 = {}
    extra = [dict(alpha=0.0, foot="can", mode="calib", **BASE), dict(alpha=math.inf, foot="can", swap=True, **BASE),
             dict(alpha=0.0, foot="can", swap=True, **BASE), dict(alpha=0.0, foot="can", seed=600, **BASE)]
    for c in cfgs + extra:
        fo = os.path.join(C622, "runs", name_of(c) + ".json"); fn = os.path.join(RUNS, name_of(c) + ".json")
        if not (os.path.exists(fo) and os.path.exists(fn)):
            continue
        o, r = json.load(open(fo)), json.load(open(fn))
        if "diag" not in o:
            c8[name_of(c)] = dict(v_obs_kms=abs(o["v_obs_kms"] - r["v_obs_kms"]), dSG_obs=abs(o["dSG_obs"] - r["dSG_obs"])); continue
        n = min(len(o["diag"]), len(r["diag"]))
        mx = 0.0
        for i in range(n):
            for key in ("gal", "gas", "lens", "lens_nomask"):
                mx = max(mx, float(np.hypot(*(np.array(r["diag"][i]["sub"][key]) - np.array(o["diag"][i]["sub"][key])))))
            for a, b in zip(r["diag"][i]["sub"]["lens_alts"], o["diag"][i]["sub"]["lens_alts"]):
                mx = max(mx, float(np.hypot(*(np.array(a) - np.array(b)))))
        c8[name_of(c)] = dict(n_epochs=[len(o["diag"]), len(r["diag"])], max_diff_kpc=mx)
    R["C8_reproduction_vs_CFG622"] = c8
    if c8:
        P("C8 reproduction vs CFG622 runs (max over epochs of gal/gas/lens/unmasked/variants, kpc): %.3g over %d runs" % (
            max(v.get("max_diff_kpc", max(v.get("v_obs_kms", 0), v.get("dSG_obs", 0))) for v in c8.values()), len(c8)))
    fv = {}
    for f in FEET:
        s0 = cells[f"0_{f}"]
        okf = (s0.get("speed_kms") is not None and abs(s0["speed_kms"] - V_TARGET) <= V_TOL and abs(s0["dSG"] - DSG_OBS) <= DSG_TOL)
        fv[f] = dict(valid=bool(okf), speed_kms=s0.get("speed_kms"), dSG=s0.get("dSG"))
    R["footing_validity_alpha0"] = fv
    P("FOOTING VALIDITY at alpha = 0: " + json.dumps({f: {k: (round(v, 1) if isinstance(v, float) else v) for k, v in d.items()} for f, d in fv.items()}))
    P("\nPER-NODE SCORES (sub; E-M; stability = >= 3/4 variants within T_L & edge guard & gas guard; Harvey window d_SG >= 200 kpc)")
    P(f"{'alpha':>6s} {'foot':>4s} | {'f':>7s} {'Z_B':>6s} {'agree':>6s} {'edge':>12s} {'stabB':>16s} | {'n_H':>8s} {'open':>5s} {'bbar':>7s} {'Z_H':>6s} | status")
    for f in FEET:
        for a in ALPHAS:
            s = cells[f"{astr(a)}_{f}"]
            stt = s["status"] if fv[f]["valid"] else s["status"] + " (footing VOID)"
            P(f"{astr(a):>6s} {f:>4s} | {s.get('f', float('nan')):+7.3f} {s.get('Z_B', float('nan')):+6.2f} {str(s.get('n_agree_obs')):>6s} "
              f"{str([round(x) for x in s.get('min_lens_edge_obs', [])]):>12s} {str(s.get('stab_parts_obs')):>16s} | "
              f"{s.get('harvey_n_used', 0):2d}/{s.get('harvey_n_window', 0):2d} {(s.get('harvey_t_open') or float('nan')):5.2f} "
              f"{s.get('beta_bar', s.get('beta_bar_reported', float('nan'))):+7.3f} {s.get('Z_H', float('nan')):+6.2f} | {stt}")

    def st(a, f):
        return "VOID" if not fv[f]["valid"] else cells[f"{astr(a)}_{f}"]["status"]
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
    P(f"\nALLOWED: can {allowed['can']} alt {allowed['alt']}; EXCLUDED: can {excluded['can']} alt {excluded['alt']}; "
      f"UNSCORABLE/VOID: can {unsc['can']} alt {unsc['alt']}")
    P("\nVERDICTS (frozen V-1..V-4)" + ("" if R["status"] == "VALID" else f"  -- STATUS VOID: {R['void_reasons']}"))
    for k, v in V.items():
        P(f"  {k}: {v}")
    R["D3_sign_level"] = {astr(a): (cells[f'{astr(a)}_can'].get('beta_tsp0.5'), cells[f'{astr(a)}_can'].get('beta_tsp0.7')) for a in ALPHAS}
    R["wall_s"] = time.time() - T0
    finish(R, ""); return 0


if __name__ == "__main__":
    ph = sys.argv[1] if len(sys.argv) > 1 else ""
    sys.exit({"controls": phase_controls, "mutate": phase_mutate, "grid": phase_grid}[ph]())
