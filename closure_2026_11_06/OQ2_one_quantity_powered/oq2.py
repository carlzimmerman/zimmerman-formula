#!/usr/bin/env python3
"""OQ2 (criteria 97fdee2c2e; local d0904b157c): OQ1's one-scalar door (q = Sigma / rho_DE) with ONE change, an occupancy minimum
N_min per class per bin in S1 / S3, calibrated from the M1 null before any main-data run.
    nice -n 15 python3 oq2.py --stage0   -> oq2_stage0.json / oq2_stage0.out   (M1 null ensemble; no main data touched)
    nice -n 15 python3 oq2.py --main     -> oq2.json / oq2.out ; oq2_MUTATE_M1.json, oq2_MUTATE_M2.json, oq2_MUTATE_M3.json
Imports oq1.py read-only (which itself loads GB1 / SV5 read-only). One thread. Preemptible: SIGTERM -> checkpoint, exit 3.
kappa = 1/2 FITTED; footings never pooled; not theory closed. Adopts nothing."""
import os, sys, json, math, signal, io, contextlib, time
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[v] = "1"
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
CL = os.path.join(REPO, "closure_2026_11_06"); OQ1D = os.path.join(CL, "OQ1_one_quantity_both_walls")
sys.path.insert(0, OQ1D)
_a = sys.argv; sys.argv = [os.path.join(OQ1D, "oq1.py")]
with contextlib.redirect_stdout(io.StringIO()): import oq1 as O
sys.argv = _a
OUT = []
def P(s=""): print(s, flush=True); OUT.append(str(s))
STOP = {"flag": False}
signal.signal(signal.SIGTERM, lambda *a: STOP.__setitem__("flag", True))
A0 = O.A0; GRID = [1, 2, 3, 4, 5, 6, 7, 8]; SEEDS = list(range(1001, 1021)); FALSE_MAX = 2   # <= 5 % of 40
Q1M1 = json.load(open(os.path.join(OQ1D, "oq1_MUTATE_M1.json")))["runs"]
QMED = {f: Q1M1[f"{f}|fst0"]["q_med"] for f in A0}
Q1J = json.load(open(os.path.join(OQ1D, "oq1.json")))

# ------------------------------------------------------------------ twins: OQ1's plant with the seed as the only argument
def plant_seed(pts, qmed, step, seed):
    rng = np.random.default_rng(seed); out = []
    for p in pts:
        d = dict(p); r = p["rph"]
        if r > 0:
            sq = (3 * r / math.sqrt(qmed) + math.sqrt(9 * r * r / qmed + 4 * (2 + r))) / 2; qq = sq * sq; Ft = (qq - 2) / r
        else:
            Ft = 1 + 3 * math.sqrt(2 / qmed)
        d["Ftrue"] = Ft
        if p["cls"] != "Solar System":
            e = p["err"] if p["err"] is not None else 0.05
            d["D"] = O.Dpred(p, Ft) + rng.normal(0.0, e) + (0.3 if (step and p["cls"] in O.HOT_PLANT) else 0.0)
        out.append(d)
    return out

# ------------------------------------------------------------------ the one change: voters need >= N_min points in the bin
def voters(row, N):
    return {c: v["band"] for c, v in row["classes"].items() if v["n"] >= N}
def s1_eval(res, N):
    dead = []; tested = 0
    for row in res["bins"]:
        m = voters(row, N)
        if len(m) < 2: continue
        tested += 1
        if O.intersect(list(m.values())): continue
        cl = list(m); worst = None
        for i in range(len(cl)):
            for j in range(i + 1, len(cl)):
                if not O.intersect([m[cl[i]], m[cl[j]]]):
                    g_ = O.gap_dex([m[cl[i]], m[cl[j]]]) or 0.0
                    if worst is None or g_ > worst[2]: worst = (cl[i], cl[j], g_)
        dead.append(dict(log10q=row["log10q"], gap_dex=O.gap_dex(list(m.values())), worst_pair=worst,
                         classes={c: dict(n=row["classes"][c]["n"], band=[[round(a, 4), (round(b, 4) if math.isfinite(b) else "inf")] for a, b in v]) for c, v in m.items()}))
    return dict(N_min=N, bins_tested=tested, dead_bins=dead, S1_holds=not dead)
def dropped(res, N):
    out = {}
    for row in res["bins"]:
        for c, v in row["classes"].items():
            if v["n"] < N: out[c] = out.get(c, 0) + v["n"]
    return out
def s3_eval(pts, res, N):
    """OQ1 s3_run with the occupancy rule: nodes from voting classes only; class k graded only in its own powered bins."""
    q = np.array(res["q"]); cls = np.array([p["cls"] for p in pts]); out = {}; BW = O.BW
    for k in sorted(set(cls)):
        nodes = []
        for row in res["bins"]:
            m = {c: b for c, b in voters(row, N).items() if c != k}
            if not m: continue
            it = O.intersect(list(m.values()))
            if not it: continue
            lo, hi = it[0][0], it[-1][1]; mid = lo if not math.isfinite(hi) else 0.5 * (lo + hi)
            nodes.append(((row["bin"] + 0.5) * BW, mid))
        rows = [r for r in res["bins"] if k in r["classes"] and r["classes"][k]["n"] >= N]; graded = []; uncon = 0
        if not rows: out[k] = dict(status="NO POWERED BIN", bins=[]); continue
        if not nodes: out[k] = dict(status="UNCONSTRAINED BY OTHERS", bins=[]); continue
        xs, ys = np.array([a for a, _ in nodes]), np.array([b for _, b in nodes])
        for r in rows:
            ix = [i for i in range(len(pts)) if cls[i] == k and O.bin_of(q[i]) == r["bin"]]
            lq = float(np.median(np.log10(q[ix]))) if ix else (r["bin"] + 0.5) * BW
            dist = max(xs.min() - lq, lq - xs.max(), 0.0)
            if dist > 0.5: uncon += 1; graded.append(dict(bin=r["bin"], status="UNCONSTRAINED", dist_dex=dist)); continue
            Fp = float(np.interp(lq, xs, ys)) if len(xs) > 1 else float(ys[0])
            band = r["classes"][k]["band"]; inside = any(a <= Fp <= b for a, b in band)
            graded.append(dict(bin=r["bin"], F_pred=Fp, inside=bool(inside), dist_dex=dist))
        gr = [g for g in graded if "inside" in g]
        st = ("UNCONSTRAINED BY OTHERS" if not gr else ("PASS" if all(g["inside"] for g in gr) else "FAIL"))
        out[k] = dict(status=st, n_bins=len(rows), n_unconstrained=uncon, bins=graded)
    HOT = ("X-COP", "groups", "ellipticals", "Coma UDGs", "bright M31")
    # a class with no powered bin has nothing to grade (not a fail); a powered hot class must be constrained by others
    holds = all(v["status"] in ("PASS", "NO POWERED BIN") for v in out.values()) and not any(out.get(h, {}).get("status") == "UNCONSTRAINED BY OTHERS" for h in HOT)
    return dict(per_class={k: v["status"] for k, v in out.items()}, detail=out, S3_holds=bool(holds))
def slim(r): return {k: v for k, v in r.items() if k not in ("q", "F", "bins", "dead_bins")}

def save(path, obj): tmp = path + ".tmp"; json.dump(obj, open(tmp, "w"), indent=1, default=float); os.replace(tmp, path)

# ------------------------------------------------------------------ stage 0
def stage0():
    CK = os.path.join(HERE, "oq2_stage0_ckpt.json")
    S = json.load(open(CK)) if os.path.exists(CK) else dict(runs={})
    P("OQ2 stage 0: M1 null ensemble (no main data touched). kappa = 1/2 FITTED; not theory closed.")
    P(f"q_med from OQ1 M1 (committed): {QMED}; seeds 21 (all starts) + {SEEDS[0]}-{SEEDS[-1]} (F0 = 1); grid N_min {GRID}")
    for f, a0 in A0.items():
        for fst in (0, 1):
            pts, _ = O.points(f, a0, fst)
            jobs = [(21, F0) for F0 in (0, 1, 10)] + [(s, 1) for s in SEEDS]
            for seed, F0 in jobs:
                key = f"{f}|fst{fst}|seed{seed}|F0={F0}"
                if key in S["runs"]: continue
                t = time.time()
                pp = plant_seed(pts, QMED[f], False, seed); cx = O.ctx_for(pp, f, Q1J["foot"][f]["web"]["Fweb_max"], planted=True)
                r = O.s1_run(pp, cx, F0, None)
                ev = {}
                for N in GRID:
                    e = s1_eval(r, N); d = dict(S1_holds=e["S1_holds"], n_dead=len(e["dead_bins"]), bins_tested=e["bins_tested"],
                                               max_gap=max([x["gap_dex"] or 0 for x in e["dead_bins"]] or [0]),
                                               dead=[dict(log10q=x["log10q"], pair=x["worst_pair"], n={c: v["n"] for c, v in x["classes"].items()}) for x in e["dead_bins"]])
                    if seed == 21: s3 = s3_eval(pp, r, N); d["S3_holds"] = s3["S3_holds"]; d["S3"] = s3["per_class"]
                    ev[str(N)] = d
                S["runs"][key] = dict(iterations=r["iterations"], converged=r["converged"], cycled=r["cycled"], by_N=ev)
                save(CK, S)
                P(f"  {key}: {r['iterations']} it ({time.time() - t:.0f} s); conflicts by N_min " + " ".join(f"{N}:{ev[str(N)]['n_dead']}" for N in GRID)
                  + ("; S3 by N_min " + " ".join(f"{N}:{'Y' if ev[str(N)]['S3_holds'] else 'n'}" for N in GRID) if seed == 21 else ""))
                if STOP["flag"]: P("SIGTERM: checkpoint written, exit 3"); sys.exit(3)
    # calibration table and N_min*
    tab = {}
    for f in A0:
        tab[f] = {}
        for N in GRID:
            ens = [v["by_N"][str(N)] for k, v in S["runs"].items() if k.startswith(f + "|") and "|seed21|" not in k]
            s21 = [v["by_N"][str(N)] for k, v in S["runs"].items() if k.startswith(f + "|") and "|seed21|" in k]
            nf = sum(1 for e in ens if not e["S1_holds"])
            tab[f][str(N)] = dict(ensemble_runs=len(ens), false_conflict_runs=nf, false_rate=nf / len(ens),
                                  seed21_no_conflict=all(e["S1_holds"] for e in s21), seed21_S3_holds=all(e["S3_holds"] for e in s21),
                                  ok=bool(nf <= FALSE_MAX and all(e["S1_holds"] and e["S3_holds"] for e in s21)))
    Nstar = next((N for N in GRID if all(tab[f][str(N)]["ok"] for f in A0)), None)
    P("calibration (false-conflict runs of 40; seed 21 no conflict; seed 21 S3):")
    for N in GRID:
        P(f"  N_min {N}: " + "; ".join(f"[{f}] {tab[f][str(N)]['false_conflict_runs']}/40, s21 {'Y' if tab[f][str(N)]['seed21_no_conflict'] else 'n'}, S3 {'Y' if tab[f][str(N)]['seed21_S3_holds'] else 'n'}" for f in A0)
          + ("  <- N_min*" if N == Nstar else ""))
    P(f"N_min* = {Nstar}" + ("" if Nstar else " (none passes: NO VERDICT, main data reported at N_min 8 without a label)"))
    J = dict(lane="OQ2 stage 0", criteria="97fdee2c2e", q_med=QMED, seeds=dict(main=21, ensemble=SEEDS), grid=GRID, false_max=FALSE_MAX,
             calibration=tab, N_min_star=Nstar, runs=S["runs"], note="kappa = 1/2 FITTED; not theory closed")
    save(os.path.join(HERE, "oq2_stage0.json"), J); open(os.path.join(HERE, "oq2_stage0.out"), "w").write("\n".join(OUT) + "\n")
    os.remove(CK)

# ------------------------------------------------------------------ main
def main():
    S0 = json.load(open(os.path.join(HERE, "oq2_stage0.json"))); Nstar = S0["N_min_star"]; N = Nstar if Nstar else 8
    P(f"OQ2 main. N_min* = {Nstar} from oq2_stage0.json (committed before this run). kappa = 1/2 FITTED; not theory closed; adopts nothing.")
    RES = dict(lane="OQ2", criteria="97fdee2c2e", N_min_star=Nstar, N_used=N, KA={}, foot={}, note="kappa = 1/2 FITTED; not theory closed")
    NS = O.NS
    for f, a0 in A0.items():   # KA1, KA2 (as OQ1)
        S_, E, X = NS["build"](f, a0)
        cm = dict(X=np.mean([p["D"] for p in X]), E=np.mean([p["D"] for p in E]), S=np.mean([p["D"] for p in S_]))
        d1 = max(abs(cm[k] - O.KA20[f][k]) for k in cm)
        e_l1 = float(np.mean([p["D"] - NS["delta"](NS["L1"](f, a0), p["feat"], a0) for p in E])); d2 = abs(e_l1 - O.Q26["foot"][f]["ellipticals"]["D_imf"])
        RES["KA"][f] = dict(KA1=dict(maxdiff=float(d1), ok=bool(d1 <= 1e-6)), KA2=dict(diff=d2, ok=bool(d2 <= 1e-6)))
        P(f"[{f}] KA1 max|d| {d1:.1e} {'PASS' if d1 <= 1e-6 else 'FAIL'}; KA2 |d| {d2:.1e} {'PASS' if d2 <= 1e-6 else 'FAIL'}")
    a0c = A0["canonical"]; Mb = 1e10 * O.MS; rM = math.sqrt(O.G * Mb / a0c); rr = 100 * rM
    ratio = O.rho_ph_local(O.G * Mb / rr ** 2 / a0c, 0.0, rr, a0c) * 4 * math.pi * O.G * rr ** 2 / math.sqrt(a0c * O.G * Mb)
    RES["KA"]["KA4_pointmass_ratio"] = dict(ratio=ratio, ok=bool(abs(ratio - 1) <= 1e-4)); P(f"KA4 point-mass phantom ratio {ratio:.5f}")
    SVd = os.path.join(CL, "SV5_growth_mechanism"); sys.path.insert(0, SVd)
    _a = sys.argv; sys.argv = [os.path.join(SVd, "sv5_web.py")]
    with contextlib.redirect_stdout(io.StringIO()): import sv5_web as SV
    sys.argv = _a
    W, dV = SV.realise(5)
    S2J = json.load(open(os.path.join(SVd, "iter_2_charge_switched_sound_speed", "sv5_iter2.json")))
    S1J = json.load(open(os.path.join(SVd, "iter_1_law_on_web", "sv5_iter1.json")))
    WEB = {}; CELLS = {}
    for f in A0:
        w, cells = O.web_pass(f, A0[f], W, dV, SV); WEB[f] = w; CELLS[f] = cells
        dr = abs(w["r_F1"] / S1J["foot"][f]["proj"]["r"] - 1)
        ds = abs(w["Sigma_star_over_rhoDE"] - S2J["foot"][f]["Sigma_star_over_rhoDE"]) / S2J["foot"][f]["Sigma_star_over_rhoDE"]
        dfz = max(abs(w["frac"][z] - S2J["foot"][f]["F"][z]) for z in S2J["foot"][f]["F"])
        RES["KA"][f]["KA3"] = dict(r_F1=w["r_F1"], sv5=S1J["foot"][f]["proj"]["r"], rel=dr, ok=bool(dr <= 1e-3))
        RES["KA"][f]["KA4"] = dict(rel=ds, frac_maxdiff=dfz, ok=bool(ds <= 1e-3 and dfz <= 1e-3))
        qweb_max = max(float(np.max(w["Fweb_max"] * rp.astype(np.float64) + 2.0)) for rp, _ in cells.values())
        w["q_web_max_at_Fmax"] = qweb_max
        P(f"[{f}] KA3 r(F=1) {w['r_F1']:.4f} vs SV5 {S1J['foot'][f]['proj']['r']:.4f} rel {dr:.1e}; KA4 rel {ds:.1e} frac {dfz:.1e}; "
          f"F_web,max {w['Fweb_max']:.5g} (r {w['r_at_Fmax']:.4f} at line {w['r_line']:.4f}); max web q at F_web,max {qweb_max:.3f}")
        if STOP["flag"]: P("SIGTERM after web pass: exit 3 (rerun recomputes; no partial label written)"); sys.exit(3)
    kaok = all(RES["KA"][f][k]["ok"] for f in A0 for k in ("KA1", "KA2", "KA3", "KA4")) and RES["KA"]["KA4_pointmass_ratio"]["ok"]
    RES["KA_all"] = bool(kaok)
    if not kaok: P("KA FAIL: stop; nothing graded."); save(os.path.join(HERE, "oq2.json"), RES); open(os.path.join(HERE, "oq2.out"), "w").write("\n".join(OUT) + "\n"); sys.exit(2)
    MUTS = {"M1": {}, "M2": {}, "M3": {}}
    for f, a0 in A0.items():
        w = WEB[f]; wh = O.web_hist_factory(CELLS[f]); FR = dict(web={k: v for k, v in w.items() if k != "side"}); dead_any = False; host_min = []; hostF0 = {}
        for fst in (0, 1):
            pts, _ = O.points(f, a0, fst); ctx = O.ctx_for(pts, f, w["Fweb_max"]); runs = {}
            for F0 in (0, 1, 10):
                r = O.s1_run(pts, ctx, F0, wh); e = s1_eval(r, N); dr_ = dropped(r, N)
                rec = dict(slim(r), N_min=N, bins_tested=e["bins_tested"], dead_bins=e["dead_bins"], S1_holds=e["S1_holds"], never_vote_points=dr_)
                if e["S1_holds"]: rec["S3"] = s3_eval(pts, r, N); rec["S2"] = "OWED (not built in this lane)"
                runs[str(F0)] = rec; dead_any = dead_any or not e["S1_holds"]
                P(f"[{f}] f*={fst} F0={F0}: {r['iterations']} it (conv {r['converged']}); tested {e['bins_tested']} bins; "
                  + ("S1 HOLDS" if e["S1_holds"] else f"S1 EMPTY in {len(e['dead_bins'])} bins, max gap {max((d['gap_dex'] or 0) for d in e['dead_bins']):.3f} dex")
                  + f"; never-vote points {dr_}")
                for d in e["dead_bins"]:
                    P(f"     DEAD log q {d['log10q']}: gap {d['gap_dex']:.3f} dex; pair {d['worst_pair'][0]} vs {d['worst_pair'][1]}; "
                      + ", ".join(f"{c}(n {v['n']}, F {v['band']})" for c, v in d["classes"].items()))
                if F0 == 1:
                    for c, v in r["q_range"].items():
                        if c != "Solar System" and v["log10q_min"] is not None: host_min.append(v["log10q_min"])
                    hostF0[f"fst{fst}"] = {c: sum(1 for i, p in enumerate(pts) if p["cls"] == c and r["F"][i] == 0.0) for c in r["q_range"] if c != "Solar System"}
            FR[f"fst{fst}"] = runs
            for M, step in (("M1", False), ("M2", True)):
                pp = plant_seed(pts, QMED[f], step, 21); cx = O.ctx_for(pp, f, w["Fweb_max"], planted=True); mr = {}
                for F0 in (0, 1, 10):
                    r = O.s1_run(pp, cx, F0, None); e = s1_eval(r, N)
                    mr[str(F0)] = dict(slim(r), dead_bins=e["dead_bins"], S1_holds=e["S1_holds"], **({"S3": s3_eval(pp, r, N)} if M == "M1" else {}))
                    P(f"[{f}] {M} f*={fst} F0={F0}: " + ("S1 HOLDS" if e["S1_holds"] else f"S1 EMPTY ({len(e['dead_bins'])} bins, max gap {max((d['gap_dex'] or 0) for d in e['dead_bins']):.3f})")
                      + (f"; S3 {'HOLDS' if mr[str(F0)]['S3']['S3_holds'] else 'FAILS'} {mr[str(F0)]['S3']['per_class']}" if M == "M1" else ""))
                MUTS[M][f"{f}|fst{fst}"] = dict(runs=mr)
            if fst == 0:
                sp = [p for p in pts if p["cls"] == "SPARC"]
                Zb = float(np.mean([p["D"] - math.log10(p["x"] / O.glaw(p["x"], 1.0)) for p in sp]))
                MUTS["M3"][f] = dict(G1_Z_newton=Zb, G1_fails=bool(abs(Zb) > 0.057)); P(f"[{f}] M3 Newton SPARC Z {Zb:+.4f} -> G1 {'FAILS (bites)' if abs(Zb) > 0.057 else 'PASSES'}")
            if STOP["flag"]: P("SIGTERM: exit 3 (rerun recomputes)"); sys.exit(3)
        FR["S1_label"] = "DEAD" if dead_any else "S1 HOLDS, S2 OWED"
        FR["web_row"] = dict(F_web_max=w["Fweb_max"], phantom_off_needed=bool(w["Fweb_max"] < 1))
        FR["separated_row"] = dict(q_web_max=w["q_web_max_at_Fmax"], log10_q_web_max=math.log10(w["q_web_max_at_Fmax"]), lowest_host_log10q=min(host_min),
                                   separated=bool(math.log10(w["q_web_max_at_Fmax"]) < min(host_min)), host_points_at_F0_in_F0eq1_run=hostF0)
        P(f"[{f}] S1 label {FR['S1_label']}; web row: F_web,max {w['Fweb_max']:.5g} -> phantom off on web needed: {'YES' if w['Fweb_max'] < 1 else 'NO'}; "
          f"SEPARATED: web log q max {FR['separated_row']['log10_q_web_max']:.3f} vs lowest host {min(host_min):.3f} -> {'YES' if FR['separated_row']['separated'] else 'NO'}")
        RES["foot"][f] = FR; del CELLS[f]
    m1 = all(all(r["S1_holds"] and r["S3"]["S3_holds"] for r in v["runs"].values()) for v in MUTS["M1"].values())
    m2 = all(any(not r["S1_holds"] for r in v["runs"].values()) for v in MUTS["M2"].values())
    m3 = all(v["G1_fails"] for v in MUTS["M3"].values())
    RES["MUTATE"] = dict(M1_no_conflict_S3=bool(m1), M2_dead=bool(m2), M3_G1_fails=bool(m3))
    s1 = "DEAD" if any(RES["foot"][f]["S1_label"] == "DEAD" for f in A0) else "S1 HOLDS, S2 OWED"
    if Nstar is None: lab = "NO VERDICT (no N_min passes the M1 null calibration)"
    elif not (m1 and m2 and m3): lab = "NO VERDICT (power check failed: " + ", ".join(k for k, v in RES["MUTATE"].items() if not v) + ")"
    else: lab = s1
    RES["S1_reading"] = s1; RES["label"] = lab
    RES["web_row"] = dict(phantom_off_needed="YES" if all(RES["foot"][f]["web_row"]["phantom_off_needed"] for f in A0) else "NO",
                          F_web_max={f: RES["foot"][f]["web_row"]["F_web_max"] for f in A0})
    RES["separated_row"] = "YES" if all(RES["foot"][f]["separated_row"]["separated"] for f in A0) else "NO"
    P(f"MUTATE at N_min {N}: M1 no conflict + S3 {m1}; M2 DEAD {m2}; M3 G1 fails {m3}")
    P(f"OQ2 LABEL: {lab} (S1 reading {s1}); WEB ROW phantom off on web needed: {RES['web_row']['phantom_off_needed']}; SEPARATED: {RES['separated_row']}")
    P("kappa = 1/2 FITTED; not theory closed.")
    for M, v in MUTS.items(): save(os.path.join(HERE, f"oq2_MUTATE_{M}.json"), dict(lane="OQ2 MUTATE " + M, criteria="97fdee2c2e", N_min=N, runs=v, verdict=RES["MUTATE"]))
    save(os.path.join(HERE, "oq2.json"), RES); open(os.path.join(HERE, "oq2.out"), "w").write("\n".join(OUT) + "\n")

if __name__ == "__main__":
    if "--stage0" in sys.argv: stage0()
    elif "--main" in sys.argv: main()
    else: print(__doc__)
