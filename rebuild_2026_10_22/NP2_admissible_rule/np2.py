#!/usr/bin/env python3
"""NP2_admissible_rule. Modes: controls (known answer, Upsilon loader, checker, zero-weight law card through RQ3, planted N0/N1, class boost, MUTATE per cell),
real (admissible train-only rules, arms L3/L5 x Upsilon modes F/U x footings; gates 1-5, checker, hull; Stage 3 through RQ3 unedited; labels).
Run: PYTHONHASHSEED=0 nice -n 10 python3 -I np2.py MODE [--only ARM] [--no-stage3]. See FROZEN_CRITERIA.md. kappa = 1/2 FITTED; not theory closed."""
import json, math, os, resource, subprocess, sys, time
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np
import np2_core as N
C = N.C
sys.path.insert(0, N.NP1D)
import np1 as N1          # NP1's s3_read, ROWLINE, POINT_RULE, plant helpers (read-only)
import np1_cand as K1     # NP1's frozen-rule loader, for checker control (c)
import np2_cand as K2
MODE = sys.argv[1] if len(sys.argv) > 1 else "real"; STAGE3 = "--no-stage3" not in sys.argv
ONLY = sys.argv[sys.argv.index("--only") + 1] if "--only" in sys.argv else None
OUT = []; T0 = time.time(); TAG = f"_{ONLY}" if ONLY else ""
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
def rss(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9
def fpk():
    try: return [l.split(":")[1].strip() for l in subprocess.run(["footprint", str(os.getpid())], capture_output=True, text=True).stdout.splitlines() if "phys_footprint_peak" in l][0]
    except Exception: return "?"
def tm(): return f"[{time.time() - T0:.0f}s, max RSS {rss():.2f} GB, phys footprint peak {fpk()}]"
clean = N1.clean; g14s = N1.g14s
def lg(s): P(s)

def cell_extra(arm, cx):
    """Rows for the checker: train, holdouts, CX1 centre rows."""
    return [("train", np.vstack([C.feats(C.XT, arm), C.feats(C.ST, arm)])), ("SPARC_even", C.feats(C.SH, arm)), ("XCOP_other", C.feats(C.XH, arm)), ("LT", C.feats(C.LTA, arm)), ("CX1", C.cx_feats(cx, arm))]
def rs_of(rule):
    os.makedirs(os.path.join(HERE, "smoke"), exist_ok=True); p = os.path.join(HERE, "smoke", f"_tmp_check_{os.getpid()}.npz"); rule.save(p); R = dict(np.load(p)); os.remove(p); return {k: R for k in K2.A0F}
def full_check(rule, a0, arm, cx, extra=None):
    return N.check(rule, a0, extra if extra is not None else cell_extra(arm, cx), cand=(rs_of(rule), K2.g_of_Q, None), cx=cx)
def write_cand(stem, title):
    d = os.path.join(HERE, "candidates"); os.makedirs(d, exist_ok=True); p = os.path.join(d, f"np2_{stem}.py")
    open(p, "w").write(f'"""NP2 {title}. Frozen admissible Gaussian-process rule, W3, per footing. A description of data, not a theory; no action. kappa = 1/2 FITTED."""\nimport os, sys\nsys.dont_write_bytecode = True\nsys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))\nimport np2_cand as _C\n_R = _C.load({stem!r})\nNAME = {("NP2 " + title)!r}; VERTICAL = ("R",); TRAINED_ON = ("xcop_train", "sparc_train")\ndef g(Q): return _C.g_of_Q(_R, Q)\n')
    return p
def stage3(path, flags=()):
    nm = os.path.basename(path)[:-3]; log = os.path.join(HERE, "results", nm + "_stage3.log"); os.makedirs(os.path.dirname(log), exist_ok=True)
    env = dict(os.environ, PYTHONHASHSEED="0", OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", MKL_NUM_THREADS="1", VECLIB_MAXIMUM_THREADS="1", PYTHONDONTWRITEBYTECODE="1")
    subprocess.run(["nice", "-n", "10", sys.executable, "-I", os.path.join(HERE, "np2_stage3.py"), path, *flags], stdout=open(log, "w"), stderr=subprocess.STDOUT, cwd=HERE, env=env)
    return json.load(open(os.path.join(HERE, "results", nm + ".json")))
def train_arrays(arm, a0, ST_, gX=None, gS=None, tgt=None):
    F = np.vstack([C.feats(C.XT, arm), C.feats(ST_, arm)]); t = np.r_[C.target(C.XT, a0, gX), C.target(ST_, a0, gS)] if tgt is None else tgt
    cls = np.r_[np.zeros(len(C.XT), int), np.ones(len(ST_), int)]; sid = np.r_[C.XT[:, 4].astype(int), ST_[:, 4].astype(int)]; return F, t, cls, sid
def fitmsg(tag, r): m = r.meta; return f"{tag}: lam {m['lam']}{' (GRID EDGE)' if m['lam_at_edge'] else ''}, ML ell {np.round(m['ml']['ell'], 3).tolist()} sf {m['ml']['sf']:.3f}; final fit conv {m['fit']['conv']} rounds {m['fit']['rounds']} active {m['fit']['active']}/{m['fit']['working']}"

# ======================================================================= controls
def controls():
    R = {}; P("NP2 controls (FROZEN_CRITERIA). Read before any real-data fit."); CX = {ft: C.cx_rows(ft) for ft in C.FOOT}
    if ONLY in (None, "L3"): R.update(base_controls(CX))
    cells(R, CX); return R
def base_controls(CX):
    R = {}
    xs = np.log10(C.X_ALL[:, 1] / C.law(C.X_ALL[:, 0], C.A0C)); sys.path.insert(0, C.CXD); import cx1_rows as CR
    lt = np.concatenate([np.log10(s.rows["gobs"] / CR.law(s.rows["gb"], C.A0C)) for s in CR.systems("canonical") if s.sub == "LT"])
    Kn = dict(xcop_mean=round(float(xs.mean()), 4), n=len(xs), lt_median=round(float(np.median(lt)), 4)); Kn["ok"] = bool(abs(Kn["xcop_mean"] - 0.4675) <= 5e-4 and abs(Kn["lt_median"] + 0.0252) <= 5e-4)
    P("1 known answer:", json.dumps(Kn)); R["known"] = Kn
    up = dict(ST=bool(np.array_equal(N.sparc_at(1), C.ST)), SH=bool(np.array_equal(N.sparc_at(0), C.SH))); up["ok"] = up["ST"] and up["SH"]; P("8 Upsilon loader reproduces BF1 at 0.5:", up); R["ups_loader"] = up
    a0 = C.A0C; arm = "L3"; mu, sd = C.feats(C.ST, arm).mean(0), C.feats(C.ST, arm).std(0); Ztr = (np.vstack([C.feats(C.XT, arm), C.feats(C.ST, arm)]) - mu) / sd
    zero = N.CRule(arm, mu, sd, Ztr, np.zeros(len(Ztr)), np.ones(3), 0.07)
    bump = N.CRule(arm, mu, sd, np.zeros((1, 3)), np.array([-1.5]), np.array([0.3, 1.0, 1.0]), 1.0)
    n1 = dict(np.load(os.path.join(N.NP1D, "rules", "real_L3_canonical.npz"))); np1r = N.CRule("L3", n1["mu"], n1["sd"], n1["Z"], n1["alpha"], n1["ell"], float(n1["sf2"]))
    ch = {}
    for tag, rule, want in (("bump", bump, False), ("zero", zero, True), ("np1_real_L3_canonical", np1r, False)):
        if tag == "np1_real_L3_canonical": o = N.check(rule, a0, cell_extra(arm, CX["canonical"]), cand=(K1.load("real_L3"), K1.g_of_Q, None), cx=CX["canonical"])
        else: o = full_check(rule, a0, arm, CX["canonical"])
        ch[tag] = dict(check=o, ok=bool(o["admissible"] == want)); P(f"3 checker on {tag}: violations {o['violations']}, admissible {o['admissible']} (want {want}) -> {'OK' if ch[tag]['ok'] else 'FAILED'}; end-to-end {o['end_to_end']}")
    R["checker"] = ch; ck_ok = all(v["ok"] for v in ch.values())
    # zero-weight rule through RQ3 unedited
    os.makedirs(os.path.join(HERE, "rules"), exist_ok=True)
    for ft in C.FOOT: zero.save(os.path.join(HERE, "rules", f"zero_{ft}.npz"))
    zr = stage3(write_cand("zero", "zero-weight control (the plain law)"), ("--no-keys", "--no-bullet")); LAW = json.load(open(os.path.join(RB_RQ3, "results", "law.json"))); zc = {}
    for ft in C.FOOT:
        A, Bq = zr["footings"][ft]["rows"], LAW["footings"][ft]["rows"]; bad = []; nc = 0; skipped = []
        for k, v in A.items():
            if k not in Bq: continue
            if v["label"] == "NOT COMPUTABLE" and ("non-finite" in v.get("why", "") or v.get("why", "") in ("keys path", "not run") or "keys path not run" in v.get("why", "")): skipped.append(k); continue   # AMENDMENT_A2: NaN inputs by frozen design, or --no-keys
            w = Bq[k]; nc += 1
            if v["label"] != w["label"]: bad.append((k, v["label"], w["label"])); continue
            for q in ("Z", "value"):
                if isinstance(v.get(q), (int, float)) and isinstance(w.get(q), (int, float)) and abs(v[q] - w[q]) > 1e-6 * max(1.0, abs(w[q])): bad.append((k, q, v[q], w[q]))
        zc[ft] = dict(compared=nc, skipped=skipped, mismatches=bad, ok=not bad); P(f"2 zero-weight rule vs RQ3 law card, {ft}: {nc} rows compared (labels, Z and value to 1e-6 relative), mismatches {bad}; skipped by design {len(skipped)}: {skipped}")
    R["zero_card"] = zc; R["base_ok"] = bool(Kn["ok"] and up["ok"] and ck_ok and all(v["ok"] for v in zc.values())); P("base controls", "ALL OK" if R["base_ok"] else "FAILED"); return R
def cells(R, CX):
    for arm in C.ARMS:
        if ONLY and arm != ONLY: continue
        for ft, a0 in C.FOOT.items():
            cell = {}; cx = CX[ft]
            for tag, kw in (("planted_N0", dict(noise=False)), ("planted_N1", dict(noise=True)), ("class_boost", dict(noise=True, cls_boost=True))):
                Pl = N1.plant(a0, **kw); F, t, cls, sid = train_arrays(arm, a0, C.ST, Pl["XT"], Pl["ST"]); rule = N.fit_admissible(arm, F, t, cls, sid, a0); o = C.gates14(rule, a0, Pl)
                ok = (o["g3"]["ok"] and o["g4"]["ok"]) if tag != "class_boost" else (not o["g3S"]["ok"]); cell[tag] = dict(gates=o, meta=rule.meta, control_ok=bool(ok))
                P(f"{arm} {ft} {fitmsg(tag, rule)} | {g14s(o)} | control {'OK' if ok else 'FAILED'} {tm()}")
                if tag == "planted_N0":
                    o7 = full_check(rule, a0, arm, cx); cell["solver_on_inadmissible_plant"] = dict(check=o7, conv=rule.meta["fit"]["conv"])   # AMENDMENT_A2: reported, not a gate
                    c7 = None
                    S = {k: N.law_slope(10 ** F[:, 0], a0) + v for k, v in planted_own_slope(F, arm).items()}; frac = {k: float(np.mean(v < N.EPS)) for k, v in S.items()}; cell["planted_own_slope_below_eps"] = frac
                    P(f"   (reported, AMENDMENT_A2) checker on the (1+f)log1p(1/y) N0 fit: conv {rule.meta['fit']['conv']}, violations {o7['violations']} {json.dumps({k: v for k, v in o7.items() if k != 'end_to_end'})}; planted form's own slope < eps on train rows: {frac}")
            for tag, kw in (("admissible_N0", dict(noise=False)), ("admissible_N1", dict(noise=True))):   # AMENDMENT_A2 control 7: g = law(g_b, a0 (1 + 0.5 f)), admissible in both directions
                Pl = plant_adm(a0, **kw); F, t, cls, sid = train_arrays(arm, a0, C.ST, Pl["XT"], Pl["ST"]); rule = N.fit_admissible(arm, F, t, cls, sid, a0); o = C.gates14(rule, a0, Pl); o7 = full_check(rule, a0, arm, cx)
                ok = bool(rule.meta["fit"]["conv"] and o7["admissible"] and o["g3"]["ok"] and o["g4"]["ok"]); cell[tag] = dict(gates=o, check=o7, meta=rule.meta, control_ok=ok)
                P(f"{arm} {ft} {fitmsg(tag, rule)} | {g14s(o)} | checker violations {o7['violations']} | control 7 {'OK' if ok else 'FAILED'} {tm()}")
            cell["solver"] = dict(control_ok=bool(cell["admissible_N0"]["control_ok"] and cell["admissible_N1"]["control_ok"]))
            # MUTATE, mode F
            F, t, cls, sid = train_arrays(arm, a0, C.ST); rng = np.random.default_rng(20261106); rule = N.fit_admissible(arm, F, t[rng.permutation(len(t))], cls, sid, a0); o = C.gates14(rule, a0)
            ok = not (o["g1"]["ok"] and o["g2"]["ok"] and o["g3"]["ok"]); cell["mutate_F"] = dict(gates=o, meta=rule.meta, control_ok=bool(ok)); P(f"{arm} {ft} {fitmsg('MUTATE F', rule)} | {g14s(o)} | {'bites' if ok else 'FAILED'} {tm()}")
            # MUTATE, mode U: U0 targets permuted, one fit, mode U gates
            U0 = N.profile(1, a0); ST0 = N.sparc_at(1, U0); F, t, cls, sid = train_arrays(arm, a0, ST0); rng = np.random.default_rng(20261106); rule = N.fit_admissible(arm, F, t[rng.permutation(len(t))], cls, sid, a0)
            o = C.gates14(rule, a0); u, _, _ = N.u_sparc_gates(rule, a0, U0, U0, arm); ok = not (o["g1"]["ok"] and u["g2U"]["ok"] and u["g3SU"]["ok"] and o["g3X"]["ok"])
            cell["mutate_U"] = dict(gates=o, ugates=u, meta=rule.meta, control_ok=bool(ok)); P(f"{arm} {ft} {fitmsg('MUTATE U', rule)} | G1 {o['g1']['mean']:+.3f}/{o['g1']['rms']:.3f} | G2U {u['g2U']['rms']:.3f}/{u['g2U']['line']:.3f} | G3SU {u['g3SU']['rms']:.3f}/{u['g3SU']['line']:.3f} | G3X {o['g3X']['mean']:+.3f} | {'bites' if ok else 'FAILED'} {tm()}")
            shared = all(cell[k]["control_ok"] for k in ("planted_N0", "planted_N1", "class_boost", "solver"))
            cell["F_ok"] = bool(shared and cell["mutate_F"]["control_ok"]); cell["U_ok"] = bool(shared and cell["mutate_U"]["control_ok"])
            R[f"{arm}|{ft}"] = cell; P(f"{arm} {ft}: cell controls F {'ALL OK' if cell['F_ok'] else 'FAILED'}, U {'ALL OK' if cell['U_ok'] else 'FAILED'}")
RB_RQ3 = os.path.join(N.RB, "RQ3_acceptance_v2")
def plant_adm(a0, noise):
    """AMENDMENT_A2 control 7: g = law(g_b, a0 (1 + 0.5 f)), increasing in g_b along stars-only and gas-only (proof in AMENDMENT_A2). Same rows and noise draw as NP1's plant."""
    P_ = {}
    for k, A in (("XT", C.XT), ("ST", C.ST), ("XH", C.XH), ("SH", C.SH), ("LT", C.LTA)): P_[k] = C.law(A[:, 0], a0 * (1 + 0.5 * A[:, 3]))
    if noise:
        for k, A, par in (("ST", C.ST, 1), ("SH", C.SH, 0)):
            e = C.DD.sparc_err(par); r = np.random.default_rng(20261103 + par); P_[k] = P_[k] * 10 ** (e * r.standard_normal(len(e)))
    return P_
def planted_own_slope(F, arm):
    """d log10[(1+f) log1p(1/y)] / d log10 y along stars, gas, share at raw leaves F (analytic)."""
    y = 10 ** F[:, 0]; f = F[:, 2]; dl = -(1 / y) / ((1 + 1 / y) * np.log1p(1 / y)); Dr = N.directions(F, arm)
    return {k: dl + v[:, 2] / ((1 + f) * N.LN10) for k, v in Dr.items()}

# ======================================================================= real
def real():
    CT = {}
    for q in ("np2_controls.json", "np2_controls_L3.json", "np2_controls_L5.json"):
        if os.path.exists(os.path.join(HERE, q)): CT.update(json.load(open(os.path.join(HERE, q))))
    if "base_ok" not in CT or not any("|" in k for k in CT): sys.exit("controls unread; they read first, per FROZEN_CRITERIA")
    P("controls read:", {k: (v["F_ok"], v["U_ok"]) for k, v in CT.items() if "|" in k}, "base", CT["base_ok"]); CX = {ft: C.cx_rows(ft) for ft in C.FOOT}; os.makedirs(os.path.join(HERE, "rules"), exist_ok=True); R = {}
    for arm in C.ARMS:
        if ONLY and arm != ONLY: continue
        for md in ("F", "U"):
            key = f"{arm}_{md}"; R[key] = {}
            for ft, a0 in C.FOOT.items():
                P(f"\n== {arm} mode {md} {ft} {tm()}"); cx = CX[ft]; G = {}
                if md == "F":
                    F, t, cls, sid = train_arrays(arm, a0, C.ST); rule = N.fit_admissible(arm, F, t, cls, sid, a0, log=lg); SHx = C.SH
                else:
                    U0 = N.profile(1, a0); ST0 = N.sparc_at(1, U0); F, t, cls, sid = train_arrays(arm, a0, ST0); P(f"  U0 (law profile): median {np.median(list(U0.values())):.2f}, n gal {len(U0)}")
                    r1 = N.fit_admissible(arm, F, t, cls, sid, a0, log=lg); P("  " + fitmsg("R1", r1))
                    U1 = N.profile(1, a0, r1, arm); dU = np.array([U1[k] - U0[k] for k in U0]); P(f"  U1 (R1 profile): median {np.median(list(U1.values())):.2f}, median |U1-U0| {np.median(np.abs(dU)):.3f}, mean U1-U0 {dU.mean():+.3f}")
                    ST1 = N.sparc_at(1, U1); F, t, cls, sid = train_arrays(arm, a0, ST1); rule = N.fit_admissible(arm, F, t, cls, sid, a0, log=lg)
                    G["ups"] = dict(U0_med=float(np.median(list(U0.values()))), U1_med=float(np.median(list(U1.values()))), med_abs_dU=float(np.median(np.abs(dU))), mean_dU=float(dU.mean()), U0=U0, U1=U1, R1=r1.meta)
                rule.save(os.path.join(HERE, "rules", f"real_{key}_{ft}.npz")); P("  " + fitmsg("frozen", rule))
                o = C.gates14(rule, a0); G.update(meta=rule.meta, gates=o); P(f"  {g14s(o)}")
                if md == "U":
                    u, Yh, SHx = N.u_sparc_gates(rule, a0, U1, U0, arm); G["ugates"] = u; G["ups"]["holdout_rule_profile_med"] = u["g3SU"]["Y_med"]
                    P(f"  mode U: G2U {u['g2U']['rms']:.3f}/{u['g2U']['line']:.3f} med {u['g2U']['med']:+.3f} {'P' if u['g2U']['ok'] else 'F'} | G3SU {u['g3SU']['rms']:.3f}/{u['g3SU']['line']:.3f} med {u['g3SU']['med']:+.3f} {'P' if u['g3SU']['ok'] else 'F'} (holdout Upsilon median rule {u['g3SU']['Y_med']:.2f}, law {u['g3SU']['Y_med_law']:.2f}); G2/G3S above at Upsilon 0.5 reported only")
                extra = [("train", F), ("SPARC_even", C.feats(SHx, arm)), ("XCOP_other", C.feats(C.XH, arm)), ("LT", C.feats(C.LTA, arm)), ("CX1", C.cx_feats(cx, arm))]
                ck = full_check(rule, a0, arm, cx, extra); G["check"] = ck; P(f"  checker: violations {ck['violations']}, admissible {ck['admissible']}; wide min slope {ck['wide']['min']:.3f}; end-to-end {ck['end_to_end']}")
                h = N.hull_report(rule, cx, arm, a0, SHx); G["hull"] = h; P("  hull:", json.dumps(clean(h))); P(f"  {tm()}")
                R[key][ft] = G
            if STAGE3:
                s3 = N1.s3_read(stage3(write_cand(f"real_{key}", f"real {arm} mode {md}")), arm)
                for ft in C.FOOT: R[key][ft]["stage3"] = s3[ft]; P(f"{arm} {md} {ft} Stage 3: {s3[ft]['overall']}, counts {s3[ft]['counts']}, FAILS {s3[ft]['fails']}; G5 {s3[ft]['g5']}; point-rule passes not counted {s3[ft]['passes_not_counted']} {tm()}")
    R["verdicts"] = verdicts(R, CT); return R

def hull_status(line, G):
    h = G["hull"]
    if line == "G3-SPARC": return "IN HULL" if not h["SPARC"]["inhull_ok"] else "OUT OF HULL (in-hull subset passes)"
    if line == "G3-XCOP": return "IN HULL" if not h["XCOP"]["inhull_ok"] else "OUT OF HULL (in-hull subset passes)"
    if line == "G4-LT": return "IN HULL" if not h["LT"]["inhull_ok"] else "OUT OF HULL (in-hull subset passes)"
    if line == "G5": ln = "SPARC"
    else: ln = N1.ROWLINE.get(line.split(":")[1])
    if ln is None or not h.get(ln, {}).get("n"): return "NOT LOCATED"
    return f"{'IN HULL' if h[ln]['in_hull'] >= 0.9 else 'OUT OF HULL'} ({ln} {h[ln]['in_hull']:.3f})"
def verdicts(R, CT):
    P("\n==== VERDICTS (per arm, mode, footing; never pooled)"); V = {}
    for key in [k for k in R if "_" in k]:
        arm, md = key.split("_")
        for ft in C.FOOT:
            G = R[key][ft]; o = G["gates"]; ctl = bool(CT.get("base_ok")) and CT.get(f"{arm}|{ft}", {}).get(f"{md}_ok", False); fl = []; rows = {}
            g2 = G["ugates"]["g2U"]["ok"] if md == "U" else o["g2"]["ok"]; g3S = G["ugates"]["g3SU"]["ok"] if md == "U" else o["g3S"]["ok"]
            if not g3S: fl.append("G3-SPARC")
            if not o["g3X"]["ok"]: fl.append("G3-XCOP")
            if not o["g4"]["ok"]: fl.append("G4-LT")
            s3 = G.get("stage3")
            if s3:
                if not s3["g5"]["ok"]: fl.append("G5")
                fl += [f"RQ3:{k}" for k in s3["fails"] if k != "C1"]
            for l in fl:
                k = l.split(":")[1] if l.startswith("RQ3:") else None; rr = s3["rows"].get(k, {}) if (k and s3) else {}
                rows[l] = dict(Z=rr.get("Z"), value=rr.get("value"), hull=hull_status(l, G), stand_in=bool(arm == "L5" and k and k.split(":")[0] in N1.POINT_RULE))
            cc = CT.get(f"{arm}|{ft}", {}); ctl4 = bool(CT.get("base_ok")) and all(cc.get(k, {}).get("control_ok", False) for k in ("planted_N1", "class_boost", "solver", f"mutate_{md}"))   # AMENDMENT_A4: control 4 without the inadmissible N0 plant
            if not ctl4: lab = "UNDETERMINED (controls)"
            elif not (G["check"]["admissible"] and G["meta"]["fit"]["conv"]): lab = "UNDETERMINED (INADMISSIBLE)"
            elif not (o["g1"]["ok"] and g2): lab = "UNDETERMINED (UNDERFIT)"
            elif not s3: lab = "UNDETERMINED (Stage 3 not run)"
            elif not fl: lab = "ADMISSIBLE RULE PASSES ALL COMPUTABLE ROWS"
            else: lab = "ADMISSIBLE RULE FAILS ON " + ", ".join(l.replace("RQ3:", "") for l in fl)
            c1 = s3["rows"].get("C1", {}).get("Z") if s3 else None
            V[f"{key}|{ft}"] = dict(label=lab, label_frozen_controls=lab if ctl else "UNDETERMINED (controls)", planted_N0_ok=cc.get("planted_N0", {}).get("control_ok"), failing=rows, C1_prior_decided_Z=c1, nc=s3["counts"].get("NOT COMPUTABLE") if s3 else None, points_not_counted=s3["passes_not_counted"] if s3 else None)
            P(f"{arm} {md} {ft}: {lab}  [under the frozen control 4 (planted N0 {'passes' if cc.get('planted_N0', {}).get('control_ok') else 'fails'}): {V[f'{key}|{ft}']['label_frozen_controls']}]"); [P(f"    {l}: Z {q['Z']} value {q['value']} | {q['hull']}{' | s = -2 stand-in' if q['stand_in'] else ''}") for l, q in rows.items()]
            if s3: P(f"    C1 prior-decided Z {c1}; NOT COMPUTABLE {s3['counts'].get('NOT COMPUTABLE')}; L5 point-rule passes not counted {s3['passes_not_counted']}")
    return V

if __name__ == "__main__":
    R = controls() if MODE == "controls" else real() if MODE == "real" else sys.exit("mode?")
    try: fp = subprocess.run(["footprint", str(os.getpid())], capture_output=True, text=True).stdout; fp = " ".join(l.strip() for l in fp.splitlines() if "phys_footprint" in l)
    except Exception: fp = "footprint unavailable"
    P(f"\nmax RSS {rss():.2f} GB (macOS counts freed MADV_FREE pages, AMENDMENT_A3); {fp}; {time.time() - T0:.0f}s. kappa = 1/2 FITTED; not theory closed. A pass is a description of data, not a theory.")
    json.dump(clean(R), open(os.path.join(HERE, f"np2_{MODE}{TAG}.json"), "w"), indent=0); open(os.path.join(HERE, f"np2_{MODE}{TAG}.out"), "w").write("\n".join(OUT) + "\n")
