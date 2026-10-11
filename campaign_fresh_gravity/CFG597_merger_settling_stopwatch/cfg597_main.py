#!/usr/bin/env python3
"""CFG597 main: calibration (M-6), control C4, the run grid (M-7), observables (section 3), scores and verdicts (section 4).
Criteria: FROZEN_CRITERIA.md (ae49ff4d7).  kappa = 1/2 FITTED; footings never pooled; cold energy's mass is an input.

Run (repository root or this folder):   nice -n 10 python3 cfg597_main.py            -> cfg597.out, cfg597_results.json
                                         CFG597_MUTATE=1 nice -n 10 python3 cfg597_main.py  -> cfg597_MUTATE.out, cfg597_results_MUTATE.json
Per-run time series are cached in runs/ (resumable).  4 worker processes, 1 thread each."""
import os
os.environ["OMP_NUM_THREADS"] = "1"
import sys, json, math, time
import multiprocessing as mp
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import cfg597_lib as L

MUT = os.environ.get("CFG597_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
RUNS = os.path.join(HERE, "runs"); os.makedirs(RUNS, exist_ok=True)
ALPHAS = [0.0, 0.1, 0.3, 1.0, 3.0, 10.0, math.inf]
FEET = ["can", "alt"]
V_TARGET = 2700.0          # km/s (Springel & Farrar 2007 bulk speed, as quoted in the record's Bullet table)
SEP_OBS = 720.0            # kpc (BCG-BCG, Clowe+06 Table 2 coordinates; recomputed below)
F_OBS, SIG_F = 0.045, 0.125
F_OBS_MAIN = 0.042
HARV_B, HARV_S = -0.04, 0.07
OUT = []


def P(s=""):
    print(s, flush=True); OUT.append(str(s))


def astr(a):
    return "inf" if math.isinf(a) else (f"{a:g}")


def name_of(c):
    s = f"r{c['ratio']}_{c['case']}_{c.get('rule', '2S')}_a{astr(c['alpha'])}_{c['foot']}"
    if c.get("swap"):
        s += "_swap"
    if c.get("mode", "full") != "full":
        s += "_" + c["mode"]
    if c.get("mode") == "calib":
        s += f"_obs_v{c['v0'] / L.KMS:.0f}"
    return s


def _round(o):
    if isinstance(o, float):
        return round(o, 3)
    if isinstance(o, list):
        return [_round(x) for x in o]
    if isinstance(o, dict):
        return {k: _round(v) for k, v in o.items()}
    return o


def worker(c):
    import cfg597_sim as S
    fn = os.path.join(RUNS, name_of(c) + ".json")
    if os.path.exists(fn):
        return json.load(open(fn))
    os.nice(0)
    res = S.run(c)
    json.dump(_round(res), open(fn, "w"))
    return json.load(open(fn))


def pool_map(cfgs):
    todo = [c for c in cfgs if not os.path.exists(os.path.join(RUNS, name_of(c) + ".json"))]
    if todo:
        P(f"  running {len(todo)} runs on 4 processes ...")
        ctx = mp.get_context("fork")
        with ctx.Pool(4) as pool:
            pool.map(worker, todo, chunksize=1)
    return [json.load(open(os.path.join(RUNS, name_of(c) + ".json"))) for c in cfgs]


# ------------------------------------------------------------------------------------------------ observables
def series(run, who="sub"):
    """beta(t) for the 100 and 150 kpc lensing apertures; signed galaxy separation (sub - main) along x."""
    t, b100, b150, sep, dsg, bng = [], [], [], [], [], []
    for d in run["diag"]:
        s = d[who]
        gal, gas = np.array(s["gal"]), np.array(s["gas"])
        e = gas - gal; nrm = np.linalg.norm(e)
        t.append(d["t"]); sep.append(d["sub"]["gal"][0] - d["main"]["gal"][0]); dsg.append(nrm)
        if nrm > 0:
            b100.append(float(np.dot(np.array(s["lens100"]) - gal, e) / nrm ** 2))
            b150.append(float(np.dot(np.array(s["lens150"]) - gal, e) / nrm ** 2))
            bng.append(float(np.dot(np.array(s["cold150"]) - gal, e) / nrm ** 2))
        else:
            b100.append(np.nan); b150.append(np.nan); bng.append(np.nan)
    return {k: np.array(v) for k, v in dict(t=t, b100=b100, b150=b150, sep=sep, dsg=dsg, bcold=bng).items()}


def bullet_stat(run, who="sub"):
    S = series(run, who); tp = run["t_peri"]
    if tp is None:
        return None
    post = S["t"] > tp
    idx = np.where(post & (S["sep"] <= -SEP_OBS))[0]
    if len(idx) == 0:
        return dict(reached=False)
    i = idx[0]
    w = (S["sep"][i - 1] + SEP_OBS) / (S["sep"][i - 1] - S["sep"][i])
    lin = lambda a: float(a[i - 1] + w * (a[i] - a[i - 1]))
    f150, f100 = lin(S["b150"]), lin(S["b100"])
    fobs = F_OBS if who == "sub" else F_OBS_MAIN
    sn = abs(f100 - f150)
    return dict(reached=True, t_obs_after_peri=lin(S["t"]) - tp, f150=f150, f100=f100, sig_num=sn, dSG_kpc=lin(S["dsg"]),
                f_cold150=lin(S["bcold"]), Z=(f150 - fobs) / math.hypot(SIG_F, sn))


def harvey_stat(run):
    S = series(run, "sub"); tp = run["t_peri"]
    if tp is None:
        return None
    w = (S["t"] >= tp + 0.05) & (S["t"] <= tp + 0.6) & (S["dsg"] >= 25.0)
    if w.sum() < 3:
        return dict(n=int(w.sum()))
    b150, b100 = float(np.nanmean(S["b150"][w])), float(np.nanmean(S["b100"][w]))
    sn = abs(b150 - b100)
    return dict(n=int(w.sum()), beta150=b150, beta100=b100, sig_num=sn, Z=(b150 - HARV_B) / math.hypot(HARV_S, sn))


def at_tsp(run, tsp):
    S = series(run, "sub"); tp = run["t_peri"]
    if tp is None or tp + tsp > S["t"][-1]:
        return None
    return float(np.interp(tp + tsp, S["t"], S["b150"]))


def gamma_over_alpha_core(ratio, case, foot, r=100.0):
    """Gamma/alpha = (rho_c/rho_m) sqrt(4 pi G rho_m) of the SETTLED cold energy at r = 100 kpc in the sub's IC (Gyr^-1)."""
    import cfg597_sim as S
    p = L.Progenitor(S.M_SUB[ratio], foot, case)
    rc = np.interp(r, p.r, p.rho_ph); rm = rc + np.interp(r, p.r, p.rho_g + p.rho_s + p.rho_u)
    return float(rc / rm * math.sqrt(4 * math.pi * L.G * rm))


# ------------------------------------------------------------------------------------------------ main
def main():
    T0 = time.time()
    P("CFG597: cluster mergers as a stopwatch for cold-energy settling" + ("  [MUTATE]" if MUT else ""))
    P("criteria FROZEN_CRITERIA.md (ae49ff4d7); kappa = 1/2 FITTED; footings 9.3603e-11 / 1.1312e-10 never pooled; nu_mono; candidate B;")
    P("G9; no EFE; cold energy's mass required (an input); no particle species; yardsticks = raw data only (no LCDM, no MOND force law).")
    R = {"lane": "CFG597", "mutate": MUT, "criteria_commit": "ae49ff4d7"}

    # ---- D1 the record's Bullet table (exec'd read-only): offsets and BCG-BCG separation
    REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
    bt = os.path.join(REPO, "opus_48_extended_research", "reviews", "bullet", "bullet_data_table.py")
    import io, contextlib
    ns = {"__name__": "bullet_readonly"}
    with contextlib.redirect_stdout(io.StringIO()):
        exec(open(bt).read(), ns)
    d1 = dict(kpc_main=float(ns["kpc_main"]), kpc_sub=float(ns["kpc_sub"]), kpc_bcg=float(ns["kpc_bcg"]), kpc_per_arcsec=ns["KPC_PER_ARCSEC"])
    P(f"\nD1 Bullet (Clowe+06 Table 2 via the record script, read-only): galaxy-plasma {d1['kpc_main']:.1f} (main) / {d1['kpc_sub']:.1f} (sub) kpc; "
      f"BCG-BCG {d1['kpc_bcg']:.1f} kpc; 2'' = {2 * d1['kpc_per_arcsec']:.1f} kpc")
    P(f"   f_obs sub = {2 * d1['kpc_per_arcsec'] / d1['kpc_sub']:.3f}, main = {2 * d1['kpc_per_arcsec'] / d1['kpc_main']:.3f}; sigma_f = 1/8 = 0.125 "
      f"(PROVISIONAL, from the 8-sigma offset)")
    R["D1"] = d1
    P(f"D2 Harvey+15: beta = {HARV_B} +- {HARV_S} (72 substructures; record L370/L371)")

    # ---- M-6 calibration of v0 per (ratio, case)
    P("\nM-6 CALIBRATION (as disclosed in README D-1): v0 per (mass ratio, case) so that the galaxy-centroid speed at the 720-kpc post-pericentre epoch is 2700 +- 200 km/s (alpha = 0, canonical; v0 >= 0)")
    v0 = {}
    calib_log = {}
    keys = [(ratio, case) for ratio in ("10", "4") for case in ("L", "U")]
    # Disclosure 2026-10-10 (README D-1): the frozen pericentre target is infeasible (from rest the cores meet at 3600-7100 km/s);
    # the 2700 km/s of SF07 is the bullet's speed at the observed epoch, so v0 is calibrated on the galaxy-centroid relative speed at
    # the 720-kpc post-pericentre epoch, v0 >= 0; if v0 = 0 is still too fast, v0 = 0 (the slowest the frozen 2.3-Mpc start allows).
    # Initial guesses from the pre-pericentre speeds of the first (pericentre-target) calibration runs: sqrt(2700^2 - (v720^2 - 1500^2)).
    cur = {("10", "L"): 1691.0, ("4", "L"): 548.0, ("10", "U"): 0.0, ("4", "U"): 0.0}
    hist = {k: [] for k in keys}; done = set()
    for it in range(4):
        todo = [k for k in keys if k not in done]
        if not todo:
            break
        cs = [dict(ratio=k[0], case=k[1], rule="2S", alpha=0.0, foot="can", v0=cur[k] * L.KMS, mode="calib") for k in todo]
        rs = pool_map(cs)
        for k, r in zip(todo, rs):
            vp = r["v_obs_kms"]; hist[k].append((cur[k], vp))
            P(f"  {k[0]}:1 {k[1]}: v0 = {cur[k]:.0f} km/s -> speed at the 720-kpc epoch = {vp:.0f} km/s (t_peri {r['t_peri']:.3f} Gyr)")
            if abs(vp - V_TARGET) <= 200.0 or (cur[k] == 0.0 and vp > V_TARGET):
                done.add(k)
            else:
                cur[k] = math.sqrt(max(cur[k] ** 2 + (V_TARGET ** 2 - vp ** 2), 0.0))
    for k in keys:
        v0[k] = hist[k][-1][0]
        calib_log[f"{k[0]}_{k[1]}"] = dict(v0_kms=hist[k][-1][0], v_peri_kms=hist[k][-1][1], history=hist[k],
                                          within_200=abs(hist[k][-1][1] - V_TARGET) <= 200.0)
    R["calibration"] = calib_log

    # ---- the run grid
    cfgs = []
    if not MUT:
        cfgs.append(dict(ratio="10", case="L", rule="2S", alpha=1.0, foot="can", mode="isolated", t_iso=0.6))
        for foot in FEET:
            for a in ALPHAS:
                for case in ("L", "U"):
                    cfgs.append(dict(ratio="10", case=case, rule="2S", alpha=a, foot=foot))
                if 0 < a < math.inf:
                    cfgs.append(dict(ratio="10", case="L", rule="1S", alpha=a, foot=foot))
        for a in ALPHAS:
            for case in ("L", "U"):
                cfgs.append(dict(ratio="4", case=case, rule="2S", alpha=a, foot="can"))
    else:
        cfgs += [dict(ratio="10", case="L", rule="2S", alpha=math.inf, foot="can"),
                 dict(ratio="10", case="L", rule="2S", alpha=0.0, foot="can"),
                 dict(ratio="10", case="L", rule="2S", alpha=math.inf, foot="can", swap=True),
                 dict(ratio="10", case="L", rule="2S", alpha=0.0, foot="can", swap=True)]
    for c in cfgs:
        if c.get("mode") != "isolated":
            c["v0"] = v0[(c["ratio"], c["case"])] * L.KMS
    P(f"\nRUN GRID: {len(cfgs)} runs")
    runs = pool_map(cfgs)
    RUN = {name_of(c): r for c, r in zip(cfgs, runs)}

    if MUT:
        return mutate_block(R, RUN, cfgs, T0)

    # ---- C4 isolated progenitor
    iso = RUN[name_of(cfgs[0])]
    offs = []; M300 = []
    for d in iso["diag"]:
        m = d["main"]; gal = np.array(m["gal"])
        offs.append(max(np.linalg.norm(np.array(m["gas"]) - gal), np.linalg.norm(np.array(m["lens150"]) - gal)))
        M300.append(m["M300"])
    c4 = (max(offs) <= 15.0) and (abs(M300[-1] / M300[0] - 1) <= 0.10)
    P(f"\nC4 isolated main (L-2S, alpha 1, can, 0.6 Gyr): max gas/lens-galaxy offset {max(offs):.1f} kpc (<= 15); "
      f"M(<300 kpc) drift {M300[-1] / M300[0] - 1:+.4f} (<= 10%): {'PASS' if c4 else 'FAIL'}")
    R["C4"] = dict(ok=bool(c4), max_offset_kpc=float(max(offs)), M300_drift=float(M300[-1] / M300[0] - 1))
    ctl = json.load(open(os.path.join(HERE, "cfg597_controls_results.json")))
    R["controls_C1_C3_C5_all_pass"] = ctl["all_pass"]
    P(f"C1-C3, C5 (cfg597_controls_results.json): {'ALL PASS' if ctl['all_pass'] else 'SOME FAIL'}")

    # ---- per-cell scores
    P("\nSCORES (sub = the bullet; f at the 720-kpc epoch; Harvey beta-bar over 0.05-0.6 Gyr after pericentre)")
    P(f"{'cell':34s} {'t_obs':>6s} {'dSG':>6s} {'f150':>7s} {'f100':>7s} {'Z_B':>6s} | {'bbar150':>7s} {'Z_H':>6s} | {'f_main':>6s} {'Z_Bm':>6s} | cap  ok")
    cells = {}
    for c in cfgs[1:]:
        nm = name_of(c); r = RUN[nm]
        b = bullet_stat(r, "sub"); bm = bullet_stat(r, "main"); h = harvey_stat(r)
        ok = bool(b and b.get("reached") and h and "Z" in h and abs(b["Z"]) < 2 and abs(h["Z"]) < 2)
        cap = r["n_cap"] / max(r["n_mv"], 1)
        cells[nm] = dict(cfg={k: (astr(v) if k == "alpha" else v) for k, v in c.items() if k != "v0"}, v0_kms=c["v0"] / L.KMS,
                         t_peri=r["t_peri"], bullet=b, bullet_main=bm, harvey=h, allowed=ok, cap_frac=cap,
                         f_tsp05=at_tsp(r, 0.5), f_tsp07=at_tsp(r, 0.7), u_frac=r["u_frac"], Mph_over_Mb=[a / bb for a, bb in zip(r["Mph_tot"], r["Mb"])])
        if b and b.get("reached") and h and "Z" in h:
            P(f"{nm:34s} {b['t_obs_after_peri']:6.3f} {b['dSG_kpc']:6.0f} {b['f150']:+7.3f} {b['f100']:+7.3f} {b['Z']:+6.2f} | "
              f"{h['beta150']:+7.3f} {h['Z']:+6.2f} | {bm['f150'] if bm and bm.get('reached') else float('nan'):+6.3f} "
              f"{bm['Z'] if bm and bm.get('reached') else float('nan'):+6.2f} | {cap:.3f} {'Y' if ok else 'n'}")
        else:
            P(f"{nm:34s} NOT SCORABLE (pericentre or 720-kpc epoch not reached): bullet {b}, harvey {h}")
    R["cells"] = cells

    # ---- allowed ranges and verdicts
    def grid_of(ratio, case, rule, foot):
        out = []
        for a in ALPHAS:
            nm = name_of(dict(ratio=ratio, case=case, rule=rule, alpha=a, foot=foot))
            if nm in cells:
                out.append((a, cells[nm]))
        return out

    def alpha_max(gr):
        """largest alpha before |Z_B| or |Z_H| first crosses 2 (linear in log alpha; alpha = 0 placed at 0.03)."""
        xs, zs = [], []
        for a, cc in gr:
            b, h = cc["bullet"], cc["harvey"]
            if not (b and b.get("reached") and h and "Z" in h):
                continue
            xs.append(math.log10(a) if 0 < a < math.inf else (math.log10(0.03) if a == 0 else 2.0))
            zs.append(max(abs(b["Z"]), abs(h["Z"])))
        if not zs or zs[0] >= 2:
            return None, xs, zs
        for i in range(1, len(zs)):
            if zs[i] >= 2:
                x = xs[i - 1] + (2 - zs[i - 1]) * (xs[i] - xs[i - 1]) / (zs[i] - zs[i - 1])
                return 10 ** x, xs, zs
        return math.inf, xs, zs

    P("\nALLOWED alpha (|Z_B| < 2 and |Z_H| < 2) per (ratio, case, rule, footing)")
    allowed = {}
    for (ratio, case, rule, feet) in [("10", "L", "2S", FEET), ("10", "L", "1S", FEET), ("10", "U", "2S", FEET),
                                       ("4", "L", "2S", ["can"]), ("4", "U", "2S", ["can"])]:
        for foot in feet:
            gr = grid_of(ratio, case, rule, foot)
            ok = [astr(a) for a, cc in gr if cc["allowed"]]
            am, xs, zs = alpha_max(gr)
            key = f"{ratio}_{case}_{rule}_{foot}"
            allowed[key] = dict(allowed_grid=ok, alpha_max=(astr(am) if am is not None else None),
                                maxZ_by_alpha={astr(a): (max(abs(cc["bullet"]["Z"]), abs(cc["harvey"]["Z"])) if cc["bullet"] and cc["bullet"].get("reached") and cc["harvey"] and "Z" in cc["harvey"] else None) for a, cc in gr})
            P(f"  {key:16s} allowed {ok}  alpha_max {allowed[key]['alpha_max']}")
    R["allowed"] = allowed

    def zb(ratio, case, rule, a, foot):
        cc = cells.get(name_of(dict(ratio=ratio, case=case, rule=rule, alpha=a, foot=foot)))
        return cc["bullet"]["Z"] if cc and cc["bullet"] and cc["bullet"].get("reached") else None

    V = {}
    zinf = [zb("10", "L", "2S", math.inf, f) for f in FEET]
    V["V1_instant_resettling"] = "EXCLUDED" if all(z is not None and z >= 3 for z in zinf) else "NOT EXCLUDED"
    a0ok = [cells[name_of(dict(ratio="10", case="L", rule="2S", alpha=0.0, foot=f))]["allowed"] for f in FEET]
    V["V2_pure_collisionless"] = "ALLOWED" if all(a0ok) else "NOT ALLOWED"

    def v3(key):
        am = allowed[key]["alpha_max"]
        if am is None:
            return "INCOMPATIBLE (no alpha allowed)"
        amv = math.inf if am == "inf" else float(am)
        return "COMPATIBLE" if amv >= 1 else ("TENSION" if amv >= 0.5 else "INCOMPATIBLE")
    v3p = [v3(f"10_L_2S_{f}") for f in FEET]
    V["V3_galaxy_settling"] = v3p[0] if v3p[0] == v3p[1] else f"FOOTING-DEPENDENT ({v3p[0]} / {v3p[1]})"

    def verdicts_for(case, rule):
        z = [zb("10", case, rule, math.inf, f) for f in FEET]
        v1 = ("EXCLUDED" if all(x is not None and x >= 3 for x in z) else "NOT EXCLUDED") if rule == "2S" else "n/a (no alpha = inf for 1S)"
        nm0 = [name_of(dict(ratio="10", case=case, rule=rule, alpha=0.0, foot=f)) for f in FEET]
        v2 = ("ALLOWED" if all(cells[n]["allowed"] for n in nm0) else "NOT ALLOWED") if all(n in cells for n in nm0) else "n/a (alpha = 0 shared with L-2S)"
        v3v = [v3(f"10_{case}_{rule}_{f}") for f in FEET]
        return dict(V1=v1, V2=v2, V3=v3v[0] if v3v[0] == v3v[1] else f"FOOTING-DEPENDENT ({v3v[0]} / {v3v[1]})")
    VL1 = verdicts_for("L", "1S"); VU = verdicts_for("U", "2S")
    VL2 = dict(V1=V["V1_instant_resettling"], V2=V["V2_pure_collisionless"], V3=V["V3_galaxy_settling"])
    diff = []
    for nm, vv in (("L-1S", VL1), ("U-2S", VU)):
        for k in ("V1", "V2", "V3"):
            if not vv[k].startswith("n/a") and vv[k] != VL2[k]:
                diff.append(f"{nm} {k}: {vv[k]} (L-2S {VL2[k]})")
    V["V4_robustness"] = "ROBUST" if not diff else "VARIANT-DEPENDENT"
    V["V4_differences"] = diff
    V["variant_verdicts"] = {"L-2S": VL2, "L-1S": VL1, "U-2S": VU}
    if V["V2_pure_collisionless"] == "ALLOWED" and V["V1_instant_resettling"] == "EXCLUDED":
        V["V5_cold_energy"] = "collisionless fluid that re-settles slowly in mergers"
    elif V["V1_instant_resettling"] == "NOT EXCLUDED":
        V["V5_cold_energy"] = "the data do not distinguish 'locked to baryons' from 'collisionless'"
    elif V["V2_pure_collisionless"] != "ALLOWED" and all(v["allowed_grid"] == [] for k, v in allowed.items() if k.startswith("10_L_2S")):
        V["V5_cold_energy"] = "NO alpha works (a real failure)"
    else:
        V["V5_cold_energy"] = "mixed (see allowed ranges)"
    goa = gamma_over_alpha_core("10", "L", "can")
    tob = cells[name_of(dict(ratio="10", case="L", rule="2S", alpha=0.0, foot="can"))]["bullet"]["t_obs_after_peri"]
    am = allowed["10_L_2S_can"]["alpha_max"]
    V["Gamma_over_alpha_sub_core_per_Gyr"] = goa
    V["t_obs_after_peri_Gyr_alpha0_can"] = tob
    V["Gamma_tobs_at_alpha_max_can"] = (None if am in (None, "inf") else float(am) * goa * tob)
    R["verdicts"] = V
    P("\nVERDICTS (frozen rules V1-V5, primary L-2S, both footings)")
    for k, v in V.items():
        P(f"  {k}: {v}")

    # ---- D3 sign-level context
    P("\nD3 (sign level, not scored): predicted sub f at TSP 0.5 / 0.7 Gyr, L-2S canonical 10:1 and 4:1")
    d3 = {}
    for ratio in ("10", "4"):
        for a in ALPHAS:
            cc = cells.get(name_of(dict(ratio=ratio, case="L", rule="2S", alpha=a, foot="can")))
            if cc:
                d3[f"{ratio}_{astr(a)}"] = (cc["f_tsp05"], cc["f_tsp07"])
                P(f"  {ratio}:1 alpha {astr(a):>4s}: f(0.5) {cc['f_tsp05'] if cc['f_tsp05'] is not None else float('nan'):+.3f}  "
                  f"f(0.7) {cc['f_tsp07'] if cc['f_tsp07'] is not None else float('nan'):+.3f}")
    R["D3_sign_level"] = d3
    R["wall_s"] = time.time() - T0
    finish(R)
    return 0


def mutate_block(R, RUN, cfgs, T0):
    P("\nMUTATE M1-M3 (L-2S canonical, 10:1)")
    def fb(c):
        b = bullet_stat(RUN[name_of(c)], "sub"); h = harvey_stat(RUN[name_of(c)])
        return b, h
    b1, h1 = fb(cfgs[0]); b2, h2 = fb(cfgs[1]); b3, h3 = fb(cfgs[2]); b4, h4 = fb(cfgs[3])
    m1 = bool(b1 and b1.get("reached") and b1["f150"] >= 0.5)
    m2 = bool(b2 and b2.get("reached") and abs(b2["f150"]) <= 0.25 and h2 and "beta150" in h2 and h2["beta150"] <= 0.10)
    m3 = bool(b3 and b3.get("reached") and b3["f150"] <= 0.25)
    P(f"  M1 alpha = inf puts lensing on the gas (f >= 0.5): f150 = {b1.get('f150') if b1 else None}  -> {'PASS' if m1 else 'FAIL'}")
    P(f"  M2 alpha = 0, no drift/OU: |f| <= 0.25 and beta-bar <= 0.10: f150 = {b2.get('f150') if b2 else None}, beta-bar = {h2.get('beta150') if h2 else None}"
      f"  -> {'PASS' if m2 else 'FAIL'}")
    P(f"  M3 roles swapped (hydro 0.13 M_b), alpha = inf: lensing on the collisionless baryons (f <= 0.25): f150 = {b3.get('f150') if b3 else None}"
      f"  -> {'PASS' if m3 else 'FAIL'}")
    P(f"  (reported) swapped roles at alpha = 0: f150 = {b4.get('f150') if b4 else None}")
    R["M1"] = dict(ok=m1, bullet=b1, harvey=h1); R["M2"] = dict(ok=m2, bullet=b2, harvey=h2)
    R["M3"] = dict(ok=m3, bullet=b3, harvey=h3); R["M3_alpha0_reported"] = dict(bullet=b4, harvey=h4)
    R["all_pass"] = m1 and m2 and m3
    P(f"\nMUTATE: {'ALL PASS (the machinery sees settling; collisionless and role-swap behave as expected)' if R['all_pass'] else 'SOME FAIL'}")
    R["wall_s"] = time.time() - T0
    finish(R)
    return 0 if R["all_pass"] else 1


def finish(R):
    open(os.path.join(HERE, f"cfg597{TAG}.out"), "w").write("\n".join(OUT) + "\n")
    json.dump(R, open(os.path.join(HERE, f"cfg597_results{TAG}.json"), "w"), indent=1, default=lambda o: None)


if __name__ == "__main__":
    sys.exit(main())
