#!/usr/bin/env python3
"""EV1 grader (criteria 71bbb66c0d; readings 4aa33b53ce): environment keys M1/M2/M3 on GB1's battery + W1 SPARC Ursa Major.
    python3 ev1.py            -> ev1.json / ev1.out
    python3 ev1.py --mutate   -> ev1_MUTATE.json / .out   (inverted switches, calibrated F_env kept)
GB1 (gb1.py) executed read-only up to its main section; QX24 / GB1 JSONs read-only.
kappa = 1/2 FITTED; footings never pooled; not theory closed. One thread."""
import os, sys, json, math, csv
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
CL = os.path.join(REPO, "closure_2026_11_06"); GB1D = os.path.join(CL, "GB1_all_gates_battery")
MUT = "--mutate" in sys.argv; TAG = "ev1_MUTATE" if MUT else "ev1"; OUT = []
def P(s=""): print(s, flush=True); OUT.append(s)

# ---------------------------------------------------------------- GB1 library, read-only (its main section is not run)
src = open(os.path.join(GB1D, "gb1.py")).read(); cut = src.index("# ------------------------------------------------------------------ main")
NS = {"__file__": os.path.join(GB1D, "gb1.py"), "__name__": "gb1_lib"}
_a = sys.argv; sys.argv = [sys.argv[0]]; exec(compile(src[:cut], "gb1_lib", "exec"), NS); sys.argv = _a
A0, GATES, Missing = NS["A0"], NS["GATES"], NS["Missing"]
GB1J = json.load(open(os.path.join(GB1D, "gb1.json")))
Q24 = json.load(open(os.path.join(CL, "QX24_environment_key", "iter_1", "qx24.json")))
RD = json.load(open(os.path.join(HERE, "readings.json"))); SYS = RD["systems"]
MEAS = ("M1", "M2", "M3")

# ---------------------------------------------------------------- batteries exactly as gb1.py's main builds them
BATT = {}; SPN = {}
for f, a0 in A0.items():
    S, E, X = NS["build"](f, a0); GRp = {0: NS["groups_pts"](a0, 0.0), 1: NS["groups_pts"](a0, 1.0)}
    U = NS["udgs"](f, a0); D = NS["dsphs"](f, a0); K = NS["kids"](a0)
    st = NS["R1"][f"{f}|S4 v3 dmean L*floor E-W"]; sigU = math.hypot(st["se"], st["sigma_sys"]) / math.log(10)
    B = dict(f=f, S=S, E=E, X=X, GR=GRp, U=U, D=D, K=K, sigU=sigU); B["rms_L0"] = float(np.sqrt(np.mean([p["D"] ** 2 for p in S])))
    BATT[f] = B
    names = [g["name"] for g in NS["SP"] for _ in range(len(g["R"]))]; assert len(names) == len(S); SPN[f] = names
    unames = [r["name"] for r in NS["UROWS"] if r["footing"] == f]; assert len(unames) == len(U)
    # attach environment readings (per measure) to every feature; 'envtag' marks KiDS colours
    for p, n in zip(S, names): p["feat"]["env"] = {m: SYS["SPARC:" + n][f][m] for m in MEAS}; p["feat"]["env_maxclu"] = SYS["SPARC:" + n][f]["M1_maxclu"]; p["name"] = n
    for p in E: p["feat"]["env"] = {m: SYS["ELL:" + p["name"]][f][m] for m in MEAS}; p["feat"]["env_maxclu"] = SYS["ELL:" + p["name"]][f]["M1_maxclu"]
    for p in X: p["feat"]["env"] = dict(SYS["XCOP:*"][f])
    for fs in GRp.values():
        for g in fs:
            for p in g["pts"]: p["feat"]["env"] = dict(SYS["GROUP:*"][f])
    for p, n in zip(U, unames): p["feat"]["env"] = {m: SYS["UDG:" + n][f][m] for m in MEAS}; p["name"] = n
    for cls, pts in D.items():
        for p in pts: p["feat"]["env"] = {m: SYS["DSPH:" + p["name"]][f][m] for m in MEAS}
    for e_, l_ in zip(*K):
        e_["env"] = {m: SYS["KIDS:early"][f][m] for m in MEAS}; e_["envtag"] = "early"
        l_["env"] = {m: SYS["KIDS:late"][f][m] for m in MEAS}; l_["envtag"] = "late"
_ss = NS["ss_feat"]
def ss_feat_env(a0, r):
    d = _ss(a0, r); f = [k for k, v in A0.items() if v == a0][0]; d["env"] = {m: SYS["SS:Sun"][f][m] for m in MEAS}; return d
NS["ss_feat"] = ss_feat_env          # g_ss looks ss_feat up in the GB1 namespace
_filled = NS["filled"]
def filled_env(ft, fill):
    if not fill or "env" not in fill: return _filled(ft, fill)
    d = dict(ft); m = fill["meas"]; ev = dict(d.get("env") or {})
    if ev.get(m) is None:
        v = fill["env"]; ev[m] = v[d.get("envtag", "default")] if isinstance(v, dict) else v
    d["env"] = ev; return d
NS["filled"] = filled_env

# ---------------------------------------------------------------- the key
def key(meas, Fenv, invert=False, reading="noclu"):
    def c(ft):
        if reading == "maxclu" and meas == "M1" and "env_maxclu" in ft: s = ft["env_maxclu"]
        else: s = (ft.get("env") or {}).get(meas)
        if s is None: raise Missing("env_" + meas)
        if invert: s = 1 - s
        return dict(b=1.0, F=(Fenv if s == 1 else 1.0), T=0.0)
    return c
def ENV_FILLS(meas):
    if meas == "M3": return [dict(meas=meas, env=v) for v in ({"early": 1, "late": 0, "default": 1}, {"early": 0, "late": 0, "default": 0}, {"early": 1, "late": 1, "default": 1})]
    return [dict(meas=meas, env=v) for v in (0, 1)]

def run_gate(fn, c, B, a0, meas):
    try: ok, num = fn(c, B, a0); st = "PASS" if ok else "FAIL"; miss = None
    except Missing as e: st, num, miss = "NO VERDICT", None, str(e)
    br = None
    if st == "NO VERDICT":
        outs = []
        for fl in ENV_FILLS(meas):
            try: ok2, n2 = fn(c, B, a0, fl); outs.append(dict(fill=fl["env"], ok=bool(ok2), num=n2))
            except Missing as e2: outs.append(dict(fill=fl["env"], ok=None, missing=str(e2)))
        oks = [o["ok"] for o in outs]
        br = dict(reading="PASS for all" if all(o is True for o in oks) else ("FAIL for all" if all(o is False for o in oks) else "MIXED"), runs=outs)
    return dict(status=st, num=num, missing=miss, bracket=br)

def sat_pts(B): return B["D"]["MW classical"] + B["D"]["bright M31"]
def calib_h(meas, F, B, a0, reading="noclu"):
    c = key(meas, F, reading=reading)
    sat = np.array([p["D"] - NS["delta"](c, p["feat"], a0) for p in sat_pts(B)])
    anc = NS["g_sparc"](c, B, a0)[1]["Z"]
    return float(np.median(sat) - anc)
def calibrate(meas, B, a0, reading="noclu"):
    if all((p["feat"]["env"].get(meas) or 0) == 0 for p in sat_pts(B)): return None, "no satellite has S = 1"
    lo, hi = 1.0, 100.0; hl, hh = calib_h(meas, lo, B, a0, reading), calib_h(meas, hi, B, a0, reading)
    if hl * hh > 0: return None, f"no root in [1, 100] (h(1) {hl:+.4f}, h(100) {hh:+.4f})"
    for _ in range(60):
        mid = math.sqrt(lo * hi); hm = calib_h(meas, mid, B, a0, reading)
        if hm * hl > 0: lo, hl = mid, hm
        else: hi = mid
    return math.sqrt(lo * hi), "bisection"

# W1: SPARC Ursa Major vs field
UMA = {k[6:] for k, d in SYS.items() if k.startswith("SPARC:") and d["fD"] == 4}
def w1(c, B, a0, f, seed=7):
    per = {}
    for p in B["S"]: per.setdefault(p["name"], []).append((p["D"], NS["delta"](c, p["feat"], a0)))
    g = {n: (float(np.mean([v[0] for v in vs])), float(np.mean([v[1] for v in vs]))) for n, vs in per.items()}
    u = [n for n in g if n in UMA]; o = [n for n in g if n not in UMA]
    ru, ro = np.array([g[n][0] for n in u]), np.array([g[n][0] for n in o])
    d = float(ru.mean() - ro.mean()); Pk = float(np.mean([g[n][1] for n in u]) - np.mean([g[n][1] for n in o]))
    rng = np.random.default_rng(seed)
    bs = [ru[rng.integers(0, len(ru), len(ru))].mean() - ro[rng.integers(0, len(ro), len(ro))].mean() for _ in range(4000)]
    sb = float(np.std(bs)); s = float(math.hypot(sb, 0.060))
    free = "STEP IN UMa" if d / s >= 3 else ("NO STEP" if abs(d) < 2 * s else "NO VERDICT")
    if abs(Pk) < 2 * s: lab = "no switch in UMa (|P| < 2 sigma)"
    else: lab = "KILLS" if abs(d - Pk) >= 3 * s else ("COMPATIBLE" if abs(d - Pk) < 2 * s else "NO VERDICT")
    return dict(N_uma=len(u), N_field=len(o), d=d, sigma_boot=sb, sigma=s, z=d / s, key_free=free, P=Pk, label=lab,
                uma_mean=float(ru.mean()), field_mean=float(ro.mean()))

def short(g, r):
    n = r["num"]
    if n is None: return f"NO VERDICT (needs {r['missing']}; bracket {r['bracket']['reading']})"
    return NS["short"](g, r) if "short" in NS else str(n)
def gshort(g, r):
    n = r["num"]
    if n is None: return f"NV ({r['missing']}; bracket {r['bracket']['reading']})"
    if g.startswith("G1"): return f"Z {n['Z']:+.4f} rms {n['rms']:.4f} (line {n['rms_line']:.4f})"
    if g.startswith("G2"): return f"mean {n['mean']:+.4f} rms {n['rms']:.4f}"
    if g.startswith("G3"): return f"pass f*0 {n['fst0']['n_pass']}/20 f*1 {n['fst1']['n_pass']}/20"
    if g.startswith("G4"): return f"mean {n['mean']:+.4f}"
    if g.startswith("G5"): return f"mean {n['mean']:+.4f} ({n['z']:+.2f} sigma_U)"
    if g.startswith("G6"): return "; ".join(f"{k} {v['median_minus_anchor']:+.3f} [{v['ci'][0]:+.3f},{v['ci'][1]:+.3f}]" for k, v in n.items() if v["graded"])
    if g.startswith("G7"): return f"D_cand {n['D_cand']:+.4f} R {n['R']:+.4f} ({n['z']:+.2f} sigma)"
    if g.startswith("G8"): return f"worst planet use {n['worst_planet_use']:.3g}, Cassini use {n['cassini_use']:.3g}"

def cmp(a, b, path=""):
    """max |diff| over numeric leaves of b found in a."""
    if isinstance(b, dict): return max([cmp(a[k], v, path + "/" + k) for k, v in b.items() if k in a] + [0.0])
    if isinstance(b, list): return max([cmp(x, y) for x, y in zip(a, b)] + [0.0])
    if isinstance(b, bool) or b is None: return 0.0 if a == b else float("inf")
    if isinstance(b, (int, float)): return abs(float(a) - float(b))
    return 0.0

# ---------------------------------------------------------------- known answers
RES = dict(tag=TAG, criteria="71bbb66c0d", readings="4aa33b53ce", note="kappa = 1/2 FITTED; not theory closed", KA={}, keys={})
P(f"EV1 environment re-read {'MUTATE (inverted switches)' if MUT else 'MAIN'}. kappa = 1/2 FITTED; not theory closed; footings never pooled.")
sys.path.insert(0, os.path.join(REPO, "gext_vectors_2026", "src")); import gext_estimator as GE
est = GE.GextEstimator(os.path.join(REPO, "gext_vectors_2026", "data", "raw", "2mpp_vizier.tsv"),
                       os.path.join(REPO, "gext_vectors_2026", "data", "raw", "mcxc.tsv"), catalog_mode="ks115")
L0 = NS["L0"]; kaok = True
for f, a0 in A0.items():
    B = BATT[f]; d1 = 0.0
    for gname, fn, _ in GATES:
        ok, num = fn(L0(f, a0), B, a0); d1 = max(d1, cmp(num, GB1J["cands"]["L0"][f][gname]["num"]))
    d3 = 0.0
    for m in MEAS:
        c = key(m, 1.0)
        for gname, fn, _ in GATES:
            try: ok, num = fn(c, B, a0); d3 = max(d3, cmp(num, GB1J["cands"]["L0"][f][gname]["num"]))
            except Missing: pass
    # KA2: QX24 Delta_s, x_c recomputed; ellipticals' x_e recomputed with the estimator
    ps = NS["LW"]["footings"][f]["per_system"]; X1 = {r["name"]: r for r in csv.DictReader(open(os.path.join(REPO, "rebuild_2026_10_22", "X1_hosted_recount", "x1_per_system.csv"))) if r["footing"] == f}
    nm = [n for n in ps if n in X1]; gr = [n for n in nm if ps[n]["cls"] in ("MW classical", "bright M31")]; fl = [n for n in nm if ps[n]["cls"] == "LG field"]
    Ds = float(np.median([ps[n]["plain"] for n in gr]) - NS["Q20"][f]["sparc_mean"])
    xc = float(math.sqrt(max(float(X1[n]["x_e_mid"]) for n in fl) * np.median([float(X1[n]["x_e_mid"]) for n in gr])))
    d2a = max(abs(Ds - Q24["foot"][f]["key"]["Delta_s"]), abs(xc - Q24["foot"][f]["key"]["x_c"]))
    d2b = 0.0
    for en, (ra, de, _) in Q24["ell_positions"].items():
        Dm = SYS["ELL:" + en]["D"]; q = Q24["foot"][f]["T2"]["per"][en]
        no = est.eN_at(ra, de, Dm)["eN"] * GE.A0 / a0; mx = est.eN_at(ra, de, Dm, completeness=True, missing_baryons_x8=True)["eN"] * GE.A0 / a0
        d2b = max(d2b, abs(no / q["x_e_noclu"] - 1), abs(mx / q["x_e_maxclu"] - 1))
    ka = dict(KA1=dict(maxdiff=d1, ok=d1 <= 1e-9), KA2=dict(Delta_s=Ds, x_c=xc, maxdiff_key=d2a, maxrel_ell_xe=d2b, ok=d2a <= 1e-9 and d2b <= 1e-9),
              KA3=dict(maxdiff=d3, ok=d3 <= 1e-12))
    RES["KA"][f] = ka; kaok &= all(v["ok"] for v in ka.values())
    P(f"[{f}] KA1 GB1 L0 rows vs gb1.json: max|d| {d1:.1e} -> {'PASS' if ka['KA1']['ok'] else 'FAIL'}")
    P(f"[{f}] KA2 QX24 Delta_s {Ds:+.6f} x_c {xc:.6f} (max|d| {d2a:.1e}); ellipticals x_e noclu/maxclu recomputed, max rel {d2b:.1e} -> {'PASS' if ka['KA2']['ok'] else 'FAIL'}")
    P(f"[{f}] KA3 keys at F_env = 1 vs L0 (gradable rows): max|d| {d3:.1e} -> {'PASS' if ka['KA3']['ok'] else 'FAIL'}")
if not kaok:
    P("KA FAIL: stop; nothing graded."); json.dump(RES, open(os.path.join(HERE, TAG + ".json"), "w"), indent=1, default=float)
    open(os.path.join(HERE, TAG + ".out"), "w").write("\n".join(OUT) + "\n"); sys.exit(2)

# ---------------------------------------------------------------- calibrate, grade
base = json.load(open(os.path.join(HERE, "ev1.json"))) if MUT else None
FGRID = np.exp(np.linspace(0, math.log(100), 25))
for m in MEAS:
    RES["keys"][m] = {}
    for f, a0 in A0.items():
        B = BATT[f]
        if MUT: Fe = base["keys"][m][f]["F_env"]; how = "from ev1.json (main)"
        else: Fe, how = calibrate(m, B, a0)
        R = dict(F_env=Fe, calib=how, rows={})
        if Fe is None:
            R["label"] = "NOT GRADABLE (no amplitude)"; RES["keys"][m][f] = R; P(f"[{f}] {m}: no amplitude ({how})"); continue
        c = key(m, Fe, invert=MUT)
        if not MUT:
            sat = np.array([p["D"] - NS["delta"](c, p["feat"], a0) for p in sat_pts(B)])
            R["calib_check"] = dict(sat_median=float(np.median(sat)), anchor=NS["g_sparc"](c, B, a0)[1]["Z"])
        P(f"\n[{f}] key {m}{' INVERTED' if MUT else ''}: F_env {Fe:.4f} ({how})")
        for gname, fn, _ in GATES:
            r = run_gate(fn, c, B, a0, m); R["rows"][gname] = r
            P(f"[{f}] {m} {gname:17s} {r['status']:10s} {gshort(gname, r)}")
        R["rows"]["G9 CMB lensing + growth"] = dict(status="NOT EVALUATED")
        R["W1"] = w1(c, B, a0, f)
        w = R["W1"]
        P(f"[{f}] {m} W1 UMa vs field: N {w['N_uma']}/{w['N_field']}; d {w['d']:+.4f} +- {w['sigma']:.4f} (boot {w['sigma_boot']:.4f}) z {w['z']:+.2f} "
          f"-> key-free {w['key_free']}; key P {w['P']:+.4f} -> {w['label']}")
        # W2 report: NGC 720 and the Virgo pair under the key
        R["W2"] = {}
        for p in B["E"]:
            if p["name"] in ("NGC720", "NGC4472", "NGC4649"):
                R["W2"].setdefault(p["name"], []).append(p["D"] - NS["delta"](c, p["feat"], a0))
        R["W2"] = {k: float(np.mean(v)) for k, v in R["W2"].items()}
        P(f"[{f}] {m} W2 mean residual over 2/4/8 Re: " + ", ".join(f"{k} {v:+.3f}" for k, v in R["W2"].items()))
        sts = [r["status"] for g, r in R["rows"].items() if g.startswith("G") and not g.startswith("G9")]
        fails = [g.split()[0] for g, r in R["rows"].items() if r["status"] == "FAIL"]
        nvs = [g.split()[0] for g, r in R["rows"].items() if r["status"] == "NO VERDICT"]
        R["fails"], R["nvs"] = fails, nvs
        if not MUT:
            # section 6: verify each FAIL / NV (bracket already stored): feasibility over F_env in [1, 100] (statement only)
            feas = {}
            for gname, fn, _ in GATES:
                if R["rows"][gname]["status"] == "PASS": continue
                okF = []
                for Fg in FGRID:
                    try: ok, _n = fn(key(m, float(Fg)), B, a0)
                    except Missing:
                        oks = []
                        for fl in ENV_FILLS(m):
                            try: oks.append(bool(fn(key(m, float(Fg)), B, a0, fl)[0]))
                            except Missing: oks.append(False)
                        ok = any(oks)
                    if ok: okF.append(float(Fg))
                feas[gname] = dict(any_F_passes=bool(okF), F_passing=[min(okF), max(okF)] if okF else None)
            R["feasibility"] = feas
            P(f"[{f}] {m} feasibility (any F_env in [1,100] passes the row, others' S kept): " + "; ".join(f"{g.split()[0]} {'yes ' + str([round(x, 2) for x in v['F_passing']]) if v['any_F_passes'] else 'no'}" for g, v in feas.items()))
        RES["keys"][m][f] = R
    if all(RES["keys"][m][f]["F_env"] is not None for f in A0):
        fl = sorted({x for f in A0 for x in RES["keys"][m][f]["fails"]}); nv = sorted({x for f in A0 for x in RES["keys"][m][f]["nvs"]})
        w1k = any(RES["keys"][m][f]["W1"]["label"] == "KILLS" for f in A0)
        lab = ("PASSES ALL STATIC GATES" if not fl and not nv and not w1k else
               (f"FAIL ({', '.join(fl + (['W1'] if w1k else []))})" + (f"; NO VERDICT ({', '.join(nv)})" if nv else "")) if (fl or w1k) else f"NOT GRADABLE ({', '.join(nv)})")
    else: lab = "NOT GRADABLE (no amplitude)"
    RES["keys"][m]["label"] = lab; P(f"LABEL {m}{' INVERTED' if MUT else ''}: {lab}")

# ---------------------------------------------------------------- M1 maxclu reading (reported; recalibrated by the same rule)
if not MUT:
    RES["M1_maxclu"] = {}
    for f, a0 in A0.items():
        B = BATT[f]; Fe, how = calibrate("M1", B, a0, reading="maxclu"); c = key("M1", Fe, reading="maxclu"); row = {}
        nS = sum(1 for p in B["S"] if p["feat"]["env_maxclu"] == 1); nE = sorted({p["name"] for p in B["E"] if p["feat"]["env_maxclu"] == 1})
        for gname, fn, _ in GATES:
            r = run_gate(fn, c, B, a0, "M1"); row[gname] = dict(status=r["status"], num=r["num"], bracket=(r["bracket"] or {}).get("reading"))
        RES["M1_maxclu"][f] = dict(F_env=Fe, sparc_points_S1=nS, ellipticals_S1=nE, rows=row, W1=w1(c, B, a0, f))
        P(f"[{f}] M1 maxclu (reported): F_env {Fe:.4f}; SPARC points with S=1 {nS}; ellipticals S=1 {nE}; "
          + "; ".join(f"{g.split()[0]} {v['status']}" for g, v in row.items()) + f"; G4 {gshort('G4', dict(num=row['G4 ellipticals']['num']))}")

if MUT:
    bites = {}
    for m in MEAS:
        if RES["keys"][m]["label"].startswith("NOT GRADABLE (no amplitude)"): bites[m] = None; continue
        bites[m] = all(any(RES["keys"][m][f]["rows"][g]["status"] == "FAIL" for g in ("G1 SPARC", "G6 dSph classes")) for f in A0)
        P(f"MUTATE {m}: {'FAILS G1 or G6 on both footings -> BITES' if bites[m] else 'NO BITE (no power for this key)'}")
    RES["MUTATE_bites"] = bites
else:
    win = [m for m in MEAS if RES["keys"][m]["label"] == "PASSES ALL STATIC GATES"]
    RES["winners"] = win; P(f"PASSES ALL STATIC GATES: {', '.join(win) if win else 'none'}. G9 NOT EVALUATED.")
P("kappa = 1/2 FITTED; not theory closed.")
json.dump(RES, open(os.path.join(HERE, TAG + ".json"), "w"), indent=1, default=float)
open(os.path.join(HERE, TAG + ".out"), "w").write("\n".join(OUT) + "\n")
