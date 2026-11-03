#!/usr/bin/env python3
"""NP1_nonparametric_rule. Modes: controls (known answer, planted leaf form N0/N1, planted class boost, MUTATE), real (frozen train-only rules, gates 1-4, hull/reach,
CX1 lines, then gate 5 and Stage 3 through RQ3), oracle (train + holdout point rows at frozen hyperparameters, same grading, then the verdicts).
Run: PYTHONHASHSEED=0 nice -n 10 python3 -I np1.py MODE [--no-stage3]. See FROZEN_CRITERIA.md. kappa = 1/2 FITTED; not theory closed."""
import json, math, os, resource, subprocess, sys, time
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np
import np1_core as C
MODE = sys.argv[1] if len(sys.argv) > 1 else "real"; STAGE3 = "--no-stage3" not in sys.argv
OUT = []; T0 = time.time()
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
def rss(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9
def clean(o):
    if isinstance(o, dict): return {str(k): clean(v) for k, v in o.items() if not str(k).startswith("_")}
    if isinstance(o, (list, tuple)): return [clean(v) for v in o]
    if isinstance(o, (np.floating, np.integer)): return o.item()
    if isinstance(o, np.ndarray): return o.tolist()
    if isinstance(o, np.bool_): return bool(o)
    return o
def g14s(o): return (f"G1 {o['g1']['mean']:+.3f}/{o['g1']['rms']:.3f} {'P' if o['g1']['ok'] else 'F'} | G2 {o['g2']['rms']:.3f}/{o['g2']['line']:.3f} med {o['g2']['med']:+.3f} {'P' if o['g2']['ok'] else 'F'} | "
                     f"G3 S {o['g3S']['rms']:.3f}/{o['g3S']['line']:.3f} med {o['g3S']['med']:+.3f} {'P' if o['g3S']['ok'] else 'F'}, X {o['g3X']['mean']:+.3f}/{o['g3X']['rms']:.3f} {'P' if o['g3X']['ok'] else 'F'} | G4 {o['g4']['med']:+.3f} {'P' if o['g4']['ok'] else 'F'}")
def plant_H(A): c = C.DD._cols(A); return (1 + c["f"]) * np.log1p(1 / c["y"])
def plant(a0, noise, cls_boost=False):
    P_ = {}
    for k, A in (("XT", C.XT), ("ST", C.ST), ("XH", C.XH), ("SH", C.SH), ("LT", C.LTA)): P_[k] = C.law(A[:, 0], a0) * plant_H(A)
    if noise:
        for k, A, par in (("ST", C.ST, 1), ("SH", C.SH, 0)):
            e = C.DD.sparc_err(par); assert len(e) == len(A); r = np.random.default_rng(20261103 + par); P_[k] = P_[k] * 10 ** (e * r.standard_normal(len(e)))
    if cls_boost:
        for k, A in (("ST", C.ST), ("SH", C.SH)): P_[k] = P_[k] * 10 ** np.where((A[:, 4].astype(int) // 2) % 2 == 1, 0.25, -0.25)
    return P_

def controls():
    R = {}; P("NP1 controls. Gates BF1/SY1's: G1 X-COP train |mean|<=0.05 rms<=0.10; G2 SPARC train rms<=1.05 x law, |med|<=0.03; G3 same on holdouts; G4 LITTLE THINGS |med|<=0.10. Planted SPARC lines are 1.05 x the REAL law's rms.")
    xs = np.log10(C.X_ALL[:, 1] / C.law(C.X_ALL[:, 0], C.A0C)); sys.path.insert(0, C.CXD); import cx1_rows as CR
    lt = np.concatenate([np.log10(s.rows["gobs"] / CR.law(s.rows["gb"], C.A0C)) for s in CR.systems("canonical") if s.sub == "LT"]); lts = np.median(C.target(C.LTA, C.A0C))
    K = dict(xcop_mean=round(float(xs.mean()), 4), n=len(xs), lt_median_cx1=round(float(np.median(lt)), 4), lt_median_sy1_rows=round(float(lts), 4)); K["ok"] = bool(abs(K["xcop_mean"] - 0.4675) <= 5e-4 and abs(K["lt_median_cx1"] + 0.0252) <= 5e-4)
    P("Known answer, H = 1, canonical:", json.dumps(K), "(records +0.4675, -0.0252)"); R["known"] = K
    for arm in C.ARMS:
        for ft, a0 in C.FOOT.items():
            cell = {}
            for tag, kw in (("planted_N0", dict(noise=False)), ("planted_N1", dict(noise=True)), ("class_boost", dict(noise=True, cls_boost=True))):
                Pl = plant(a0, **kw); F, t, cls, sid = C.train_set(arm, a0, Pl["XT"], Pl["ST"]); rule = C.fit_rule(arm, F, t, cls, sid); o = C.gates14(rule, a0, Pl)
                ok = (o["g3"]["ok"] and o["g4"]["ok"]) if tag != "class_boost" else (not o["g3S"]["ok"])
                cell[tag] = dict(gates=o, meta=rule.meta, control_ok=bool(ok)); P(f"{arm} {ft} {tag}: lam {rule.meta['lam']}, ML ell {np.round(rule.meta['ml']['ell'], 3).tolist()} sf {rule.meta['ml']['sf']:.3f} sX {rule.meta['ml']['sX']:.3f} sS {rule.meta['ml']['sS']:.3f} | {g14s(o)} | control {'OK' if ok else 'FAILED'} [{time.time() - T0:.0f}s, RSS {rss():.2f} GB]")
            F, t, cls, sid = C.train_set(arm, a0); rng = np.random.default_rng(20261106); tm = t[rng.permutation(len(t))]; rule = C.fit_rule(arm, F, tm, cls, sid); o = C.gates14(rule, a0)
            ok = not (o["g1"]["ok"] and o["g2"]["ok"] and o["g3"]["ok"]); cell["mutate"] = dict(gates=o, meta=rule.meta, control_ok=bool(ok))
            P(f"{arm} {ft} MUTATE (log B permuted over all train rows), graded on real rows: lam {rule.meta['lam']} | {g14s(o)} | {'bites' if ok else 'FAILED: passes gates 1-3'} [{time.time() - T0:.0f}s]")
            cell["all_ok"] = bool(K["ok"] and all(v["control_ok"] for k, v in cell.items() if isinstance(v, dict))); R[f"{arm}|{ft}"] = cell; P(f"{arm} {ft}: controls {'ALL OK' if cell['all_ok'] else 'FAILED -> UNDETERMINED (controls)'}")
    return R

# ---------- shared grading for real and oracle
def write_cand(stem, title):
    d = os.path.join(HERE, "candidates"); os.makedirs(d, exist_ok=True); p = os.path.join(d, f"np1_{stem}.py")
    open(p, "w").write(f'"""NP1 {title}. Frozen Gaussian-process rule, W3, per footing. A description of data, not a theory; no action. kappa = 1/2 FITTED."""\nimport os, sys\nsys.dont_write_bytecode = True\nsys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))\nimport np1_cand as _C\n_R = _C.load({stem!r})\nNAME = {("NP1 " + title)!r}; VERTICAL = ("R",); TRAINED_ON = ("xcop_train", "sparc_train")\ndef g(Q): return _C.g_of_Q(_R, Q)\n')
    return p
def stage3(path):
    nm = os.path.basename(path)[:-3]; log = os.path.join(HERE, "results", nm + "_stage3.log"); os.makedirs(os.path.dirname(log), exist_ok=True)
    env = dict(os.environ, PYTHONHASHSEED="0", OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", MKL_NUM_THREADS="1", VECLIB_MAXIMUM_THREADS="1", PYTHONDONTWRITEBYTECODE="1")
    subprocess.run(["nice", "-n", "10", sys.executable, "-I", os.path.join(HERE, "np1_stage3.py"), path], stdout=open(log, "w"), stderr=subprocess.STDOUT, cwd=HERE, env=env)
    return json.load(open(os.path.join(HERE, "results", nm + ".json")))
POINT_RULE = ["A9", "A10", "A11", "A12", "A13", "A20", "A23a", "A23b", "A25", "A26b", "B2", "C1"]
ROWLINE = {**{k: "SPARC" for k in ("A1", "A2", "A3", "A4", "A5", "A6", "A7", "A21")}, "A9": "LT", "A10": "IC1613", "A11": "Dw", "A12": "Dw", "A13": "Dw", "A30": "L", "B1": "G", **{f"B{i}": "XCOP" for i in range(4, 26)}}
def s3_read(o, arm):
    out = {}
    for ft in C.FOOT:
        Rw = o["footings"][ft]["rows"]; fails = sorted(k for k, v in Rw.items() if v["label"] == "FAIL"); passes = sorted(k for k, v in Rw.items() if v["label"] == "PASS")
        g5 = all(Rw[k]["label"] == "PASS" for k in ("A1", "A2")) and abs(Rw["A3"].get("value", 9)) <= 0.15
        out[ft] = dict(overall=o["footings"][ft]["summary"]["overall"], counts=o["footings"][ft]["summary"]["counts"], fails=fails, passes_not_counted=[k for k in passes if arm == "L5" and k.split(":")[0] in POINT_RULE],
                       g5=dict(ok=bool(g5), A1=Rw["A1"].get("value"), A2=Rw["A2"].get("value"), A3=Rw["A3"].get("value")),
                       rows={k: dict(label=v["label"], Z=v.get("Z"), value=v.get("value") if not isinstance(v.get("value"), dict) else None) for k, v in Rw.items() if v["label"] in ("PASS", "FAIL", "FORM-DEPENDENT")})
    return out
def hull_report(rule, cx, arm, a0):
    """Fraction in hull / within reach per line; in-hull statistics for point lines; CX1 lines graded at point level (report only)."""
    rep = {}; Ztr = rule.Z if not rule.meta.get("oracle") else rule.meta["Ztrain"]
    kh = 4 if arm == "L5" else 3   # AMENDMENT_A1: L5 hull on (log y, log ell, f, s); D is a function of them
    def loc(F): Zq = rule.std(F); return C.hull_mask(Ztr[:, :kh], Zq[:, :kh]), C.reach(rule, Zq)
    for k, A in (("SPARC", C.SH), ("XCOP", C.XH), ("LT", C.LTA)):
        h, r = loc(C.feats(A, arm)); d = C.target(A, a0) - rule.m(C.feats(A, arm)); q = dict(n=len(A), in_hull=float(h.mean()), reach1=float((r <= 1).mean()), reach_med=float(np.median(r)))
        if k == "SPARC":
            line = C.SF * C.rms(C.target(A[h], a0)) if h.any() else np.nan; q.update(inhull_rms=C.rms(d[h]) if h.any() else None, inhull_line=line, inhull_med=float(np.median(d[h])) if h.any() else None, inhull_ok=bool(h.any() and C.rms(d[h]) <= line and abs(np.median(d[h])) <= C.SM))
        if k == "XCOP": q.update(inhull_mean=float(d[h].mean()) if h.any() else None, inhull_rms=C.rms(d[h]) if h.any() else None, inhull_ok=bool(h.any() and abs(d[h].mean()) <= C.XM and C.rms(d[h]) <= C.XR))
        if k == "LT": q.update(inhull_med=float(np.median(d[h])) if h.any() else None, inhull_ok=bool(h.any() and abs(np.median(d[h])) <= C.LTT))
        rep[k] = q
    F = C.cx_feats(cx, arm); h, r = loc(F); m = rule.m(F); line = np.array([q["line"] for q in cx]); lb = np.array([q["logB"] for q in cx]); sd = np.array([q["sd"] for q in cx])
    for L in C.CX_LINES:
        s = line == L
        if not s.any(): rep[L] = dict(n=0); continue
        d = lb[s] - m[s]; w = 1 / sd[s] ** 2; mu = float((w * d).sum() / w.sum()); se = float(1 / math.sqrt(w.sum())); q = dict(n=int(s.sum()), in_hull=float(h[s].mean()), reach1=float((r[s] <= 1).mean()), reach_med=float(np.median(r[s])), med_resid=float(np.median(d)), wmean_resid=mu, se=se, z=mu / se)
        hs = s & h
        if hs.any(): dh = lb[hs] - m[hs]; wh = 1 / sd[hs] ** 2; q.update(inhull_n=int(hs.sum()), inhull_wmean=float((wh * dh).sum() / wh.sum()), inhull_z=float((wh * dh).sum() / wh.sum() * math.sqrt(wh.sum())))
        rep[L] = q
    return rep
def pdep(rule, F, arm):
    names = ["log y", "log ell", "f", "s", "asinh D"][:F.shape[1]]; o = {}
    for j, nm in enumerate(names):
        g = np.quantile(F[:, j], [0.02, 0.1, 0.25, 0.5, 0.75, 0.9, 0.98]); o[nm] = []
        for v in g: G = F.copy(); G[:, j] = v; o[nm].append([float(v), float(np.mean(rule.m(G)))])
    return o
def grade(stem, title, rule, cx, arm, a0):
    o = C.gates14(rule, a0); h = hull_report(rule, cx, arm, a0); return o, h

def real():
    if not os.path.exists(os.path.join(HERE, "np1_controls.json")): sys.exit("controls unread; they read first, per FROZEN_CRITERIA")
    CT = json.load(open(os.path.join(HERE, "np1_controls.json"))); P("controls:", {k: v["all_ok"] for k, v in CT.items() if "|" in k}, "known", CT["known"]["ok"])
    os.makedirs(os.path.join(HERE, "rules"), exist_ok=True); R = {}; CX = {ft: C.cx_rows(ft) for ft in C.FOOT}; P(f"CX1 rows loaded: {[(ft, len(v)) for ft, v in CX.items()]} [{time.time() - T0:.0f}s]")
    for arm in C.ARMS:
        R[arm] = {}
        for ft, a0 in C.FOOT.items():
            F, t, cls, sid = C.train_set(arm, a0); rule = C.fit_rule(arm, F, t, cls, sid); rule.save(os.path.join(HERE, "rules", f"real_{arm}_{ft}.npz"))
            o, h = grade(f"real_{arm}", "", rule, CX[ft], arm, a0); R[arm][ft] = dict(meta=rule.meta, gates=o, hull=h, pdep=pdep(rule, F, arm))
            P(f"\n{arm} {ft}: n {rule.meta['n']}, ML ell {np.round(rule.meta['ml']['ell'], 3).tolist()} sf {rule.meta['ml']['sf']:.3f} sX {rule.meta['ml']['sX']:.3f} sS {rule.meta['ml']['sS']:.3f} conv {rule.meta['ml']['conv']}; CV {rule.meta['cv']} -> lam {rule.meta['lam']}")
            P(f"  {g14s(o)}"); P("  hull/reach:", json.dumps(clean(h))); P("  partial dependence:", json.dumps(R[arm][ft]["pdep"])); P(f"  [{time.time() - T0:.0f}s, RSS {rss():.2f} GB]")
        if STAGE3:
            p = write_cand(f"real_{arm}", f"real {arm}"); s3 = s3_read(stage3(p), arm)
            for ft in C.FOOT: R[arm][ft]["stage3"] = s3[ft]; P(f"{arm} {ft} Stage 3: {s3[ft]['overall']}, counts {s3[ft]['counts']}, FAILS {s3[ft]['fails']}; G5 {s3[ft]['g5']}; point-rule passes not counted {s3[ft]['passes_not_counted']} [{time.time() - T0:.0f}s]")
    return R

def failing_lines(G):
    """Lines the frozen rule fails: gate 3 SPARC, gate 3 X-COP, gate 4, gate 5, each computed RQ3 row that FAILS."""
    o = G["gates"]; L = []
    if not o["g3S"]["ok"]: L.append("G3-SPARC")
    if not o["g3X"]["ok"]: L.append("G3-XCOP")
    if not o["g4"]["ok"]: L.append("G4-LT")
    s3 = G.get("stage3")
    if s3:
        if not s3["g5"]["ok"]: L.append("G5")
        L += [f"RQ3:{k}" for k in s3["fails"]]
    return L
def in_hull_fail(line, G):
    h = G["hull"]
    if line == "G3-SPARC": return not h["SPARC"]["inhull_ok"]
    if line == "G3-XCOP": return not h["XCOP"]["inhull_ok"]
    if line == "G4-LT": return not h["LT"]["inhull_ok"]
    if line == "G5": return h["SPARC"]["in_hull"] >= 0.9
    k = line.split(":")[1].split(":")[0]; ln = ROWLINE.get(k)
    if ln is None: return None
    return h[ln]["in_hull"] >= 0.9 if h.get(ln, {}).get("n", 0) else None
def oracle_fails(line, O):
    o = O["gates"]
    if line == "G3-SPARC": return not o["g3S"]["ok"]
    if line == "G3-XCOP": return not o["g3X"]["ok"]
    if line == "G4-LT": return not o["g4"]["ok"]
    s3 = O.get("stage3")
    if not s3: return None
    if line == "G5": return not s3["g5"]["ok"]
    return line.split(":", 1)[1] in s3["fails"]

def oracle():
    RJ = os.path.join(HERE, "np1_real.json")
    if not os.path.exists(RJ): sys.exit("real first")
    RR = json.load(open(RJ)); R = {}; CX = {ft: C.cx_rows(ft) for ft in C.FOOT}; CT = json.load(open(os.path.join(HERE, "np1_controls.json")))
    for arm in C.ARMS:
        R[arm] = {}
        for ft, a0 in C.FOOT.items():
            Rl = dict(np.load(os.path.join(HERE, "rules", f"real_{arm}_{ft}.npz"))); base = C.Rule(arm, Rl["mu"], Rl["sd"], Rl["Z"], Rl["alpha"], Rl["ell"], float(Rl["sf2"]), RR[arm][ft]["meta"])
            base.meta["ml"]["ell"] = np.array(base.meta["ml"]["ell"]); F0, t0, c0, _ = C.train_set(arm, a0); cx = CX[ft]
            Fx = np.vstack([F0, C.feats(C.SH, arm), C.feats(C.XH, arm), C.feats(C.LTA, arm), C.cx_feats(cx, arm)])
            tx = np.r_[t0, C.target(C.SH, a0), C.target(C.XH, a0), C.target(C.LTA, a0), [q["logB"] for q in cx]]
            cx_ = np.r_[c0, np.ones(len(C.SH), int), np.zeros(len(C.XH), int), np.full(len(C.LTA) + len(cx), 2)]
            ex = np.r_[np.zeros(len(c0) + len(C.SH) + len(C.XH)), np.full(len(C.LTA), 0.075), [q["sd"] for q in cx]]
            R[arm][ft] = {}
            for lm in (1.0, 0.25):
                orc = C.refit_fixed(base, Fx, tx, cx_, ex, lm); orc.meta["Ztrain"] = base.Z; tag = "oracle" if lm == 1.0 else "oracle_lam_quarter"
                if lm == 1.0: orc.save(os.path.join(HERE, "rules", f"oracle_{arm}_{ft}.npz"))
                o, h = grade(tag, "", orc, cx, arm, a0); R[arm][ft][tag] = dict(gates=o, hull=h, n=len(tx)); P(f"{arm} {ft} {tag} (n {len(tx)}): {g14s(o)}"); P("  CX1 lines:", json.dumps({k: {q: v for q, v in h[k].items() if q in ('n', 'wmean_resid', 'z', 'med_resid')} for k in C.CX_LINES}))
        if STAGE3:
            p = write_cand(f"oracle_{arm}", f"oracle {arm} (sees holdouts; diagnostic only)"); s3 = s3_read(stage3(p), arm)
            for ft in C.FOOT: R[arm][ft]["oracle"]["stage3"] = s3[ft]; P(f"{arm} {ft} oracle Stage 3: {s3[ft]['overall']}, FAILS {s3[ft]['fails']}; G5 {s3[ft]['g5']} [{time.time() - T0:.0f}s]")
    P("\n==== VERDICTS (per arm, per footing; never pooled)")
    V = {}
    for arm in C.ARMS:
        for ft in C.FOOT:
            G = RR[arm][ft]; O = R[arm][ft]["oracle"]; fl = failing_lines(G); ok12 = G["gates"]["g1"]["ok"] and G["gates"]["g2"]["ok"]; why = []
            if not CT[f"{arm}|{ft}"]["all_ok"]: lab = "UNDETERMINED (controls)"
            elif not fl and G.get("stage3"): lab = "SMOOTH RULE EXISTS"
            elif not ok12: lab = "UNDETERMINED"; why.append("gate 1 or 2 fails on train: underfit")
            else:
                strict = []
                for l in fl:
                    ih = in_hull_fail(l, G); of = oracle_fails(l, O); why.append(f"{l}: in-hull fail {ih}, oracle fails {of}")
                    if ih and of: strict.append(l)
                inreach = [l for l in fl if in_hull_fail(l, G)]
                lab = "NO SMOOTH RULE IN LEAF SPACE" if strict else ("SMOOTH RULE EXISTS IN REACH" if G.get("stage3") and not inreach else "UNDETERMINED")   # AMENDMENT_A1
                if not inreach: why.append("every failing line is out of train's reach (NOT LOCATED, < 90 % in hull, or the in-hull subset passes)")
                if strict: why.append(f"carried by {strict}")
            V[f"{arm}|{ft}"] = dict(label=lab, failing=fl, why=why); P(f"{arm} {ft}: {lab}; failing lines {fl}"); [P("   ", w) for w in why]
    R["verdicts"] = V; return R

if __name__ == "__main__":
    R = controls() if MODE == "controls" else real() if MODE == "real" else oracle() if MODE == "oracle" else sys.exit("mode?")
    P(f"\nRSS {rss():.2f} GB, {time.time() - T0:.0f}s. kappa = 1/2 FITTED; not theory closed. A pass is a description of data, not a theory; a fail applies to these leaves at the train-chosen smoothness.")
    json.dump(clean(R), open(os.path.join(HERE, f"np1_{MODE}.json"), "w"), indent=0); open(os.path.join(HERE, f"np1_{MODE}.out"), "w").write("\n".join(OUT) + "\n")
