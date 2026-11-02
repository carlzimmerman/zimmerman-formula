#!/usr/bin/env python3
"""SY1 gate reader. Gates are BF1's, numerically unchanged. Usage: sy1_read.py MODE [--runs DIR] [--stage3] [--smoke]. MODE planted, scrambled, mutate, real.
Writes sy1_MODE_read.json and .out, named by mode. real refuses unless planted, scrambled and mutate reads exist (--smoke excepted, never on real runs' fronts). A hit is a description of data, not a theory. kappa = 1/2 FITTED; not theory closed."""
import argparse, csv, glob, json, os, subprocess, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import sy1_data as DD
from sy1_data import *
from sy1 import TAGS, MAXFLOATS
ap = argparse.ArgumentParser(); ap.add_argument("mode"); ap.add_argument("--runs", default=os.path.join(HERE, "runs")); ap.add_argument("--stage3", action="store_true"); ap.add_argument("--smoke", action="store_true"); a = ap.parse_args(); MODE = a.mode
OUT = []; 
def say(*m): s = " ".join(str(x) for x in m); print(s, flush=True); OUT.append(s)
TOL_FREE, TOL_NOISE = 1e-3, 0.01; LT = lt_rows(); FOOT = dict(canonical=A0C, alt=ALT)
def fronts(mode, arm, runs=None):
    R = []
    for d in sorted(glob.glob(os.path.join(runs or a.runs, mode, f"*_{arm}_W*_s*"))):
        p = os.path.join(d, "front.csv"); b = os.path.basename(d); tag, _, w, s = b.split("_")
        if not os.path.exists(p): continue
        for r in csv.DictReader(open(p)): R.append(dict(tag=tag, w=int(w[1:]), seed=int(s[1:]), cx=int(r["Complexity"]), loss=float(r["Loss"]), H=r["Equation"], done=os.path.exists(os.path.join(d, "DONE"))))
    return R
def leaves_of(A, scr=False):
    c = DD._cols(A)
    return c
def resid(H, w, A, a0, L=None, gobs=None):
    h = eval_H(H, L if L is not None else leaves_of(A)) * np.ones(len(A)); p = wrap(w, A[:, 0], a0, h); return np.log10((A[:, 1] if gobs is None else gobs) / p), h
def ok_H(h): return np.all(np.isfinite(h)) and np.all(h > 0)
def rms(d): return float(np.sqrt((d * d).mean()))
def law_stats(A, a0): d = np.log10(A[:, 1] / law(A[:, 0], a0)); return rms(d)
def train_L():
    """Train leaves as the search saw them."""
    if MODE == "scrambled":
        c = {k: np.r_[DD._cols(XT)[k], DD._cols(ST)[k]] for k in LEAVES}; c = scramble_y(c, len(XT)); n = len(XT); return {k: v[:n] for k, v in c.items()}, {k: v[n:] for k, v in c.items()}
    return DD._cols(XT), DD._cols(ST)
def planted():
    res = {}; say("Planted recovery, by value on train and on holdouts: rms log10(g_found/g_true) on each of X-COP train, SPARC train, X-COP unseen, SPARC unseen, at most", TOL_FREE, "noise-free,", TOL_NOISE, "at SPARC's real errors. Any seed's front. Floats and grammar as the arm's.")
    for arm in "TZ":
        F = fronts("planted", arm); arm_ok = True
        for tag in TAGS[arm]:
            p = tag[:2]; w, ex, _ = PLANT[p]; tol = TOL_FREE if tag.endswith("0") else TOL_NOISE; best = None; seeds = set(); n = 0
            for e in F:
                if e["tag"] != tag or n_floats(e["H"]) > MAXFLOATS[arm] or e["w"] != w: continue
                n += 1; v = []
                for A in (XT, ST, XH, SH):
                    h = eval_H(e["H"], DD._cols(A)) * np.ones(len(A)); v.append(rms(np.log10(wrap(w, A[:, 0], A0C, h) / planted_truth(p, A))) if ok_H(h) else np.inf)
                m = max(v)
                if best is None or m < best[0]: best = (m, e["H"], e["cx"], e["seed"])
                if m <= tol: seeds.add(e["seed"])
            rec = bool(seeds); arm_ok &= rec; res[f"{arm}|{tag}"] = dict(recovered=rec, seeds=sorted(seeds), best=best, n=n, form=ex, wrapper=w, tol=tol)
            say(f"arm {arm} {tag} W{w} {ex}: {'RECOVERED' if rec else 'NOT RECOVERED'}, seeds {sorted(seeds)}, best {best[0] if best else None}, {best[1][:80] if best else ''}, entries {n}")
        res[arm] = dict(all_recovered=bool(arm_ok)); say(f"arm {arm}: {'verdict possible' if arm_ok else 'NO VERDICT for this arm, a planted form was not recovered'}")
    return res
def stage1(arm, XM, XR, runs=None, mode=None):
    LX, LS = train_L(); RT = law_stats(ST, A0C); S = []; seen = set(); fr = fronts(mode or MODE, arm, runs); n = 0
    for e in fr:
        if n_floats(e["H"]) > MAXFLOATS[arm] or e["cx"] > 30: continue
        n += 1; dx, hx = resid(e["H"], e["w"], XT, A0C, LX); ds, hs = resid(e["H"], e["w"], ST, A0C, LS)
        if not (ok_H(hx) and ok_H(hs)): continue
        if abs(dx.mean()) > XM or rms(dx) > XR or rms(ds) > SF * RT or abs(np.median(ds)) > SM: continue
        k = (e["w"], round(rms(ds), 7), round(float(dx.mean()), 7))
        if k in seen: continue
        seen.add(k); S.append(dict(e, x_mean=float(dx.mean()), x_rms=rms(dx), s_rms=rms(ds), s_med=float(np.median(ds)), floats=n_floats(e["H"])))
    S.sort(key=lambda t: (t["cx"], t["s_rms"])); return S, n, len(fr)
def stage2(e, RQ, make):
    """Gates 3, 4, 5, per footing, cheap to dear; float values frozen from train; no refit."""
    o = {}; path = make(e)
    import importlib.util
    sp = importlib.util.spec_from_file_location("cand", path); c = importlib.util.module_from_spec(sp); sp.loader.exec_module(c)
    for ft, a0 in FOOT.items():
        ds, hs = resid(e["H"], e["w"], SH, a0); dx, hx = resid(e["H"], e["w"], XH, a0); RH = law_stats(SH, a0); r = dict(g3=False, g4=False, g5=False)
        r.update(hold_rms=rms(ds), hold_med=float(np.median(ds)), xhold=float(dx.mean()), xhold_rms=rms(dx), line=SF * RH)
        r["g3"] = bool(ok_H(hs) and ok_H(hx) and rms(ds) <= SF * RH and abs(np.median(ds)) <= SM and abs(dx.mean()) <= XM0 and rms(dx) <= XR0)
        dl, hl = resid(e["H"], e["w"], LT, a0); r["lt"] = float(np.median(dl)); r["g4"] = bool(r["g3"] and ok_H(hl) and abs(r["lt"]) <= 0.10)
        if r["g4"]:
            try:
                R = RQ["rows_sparc"](c, ft); r.update(rq_rms=R["A1"]["value"], rq_ups=R["A2"]["value"], tilt=R["A3"]["value"]); r["g5"] = bool(R["A1"]["label"] == "PASS" and R["A2"]["label"] == "PASS" and abs(R["A3"]["value"]) <= 0.15)
            except Exception as x: r["g5_error"] = str(x)[:200]
        o[ft] = r
    return o
def cand_file(i, arm):
    def make(e):
        d = os.path.join(HERE, "candidates"); os.makedirs(d, exist_ok=True); p = os.path.join(d, f"sy1_{arm}_{i(e)}.py")
        open(p, "w").write(f'"""SY1 arm {arm}, W{e["w"]}, seed {e["seed"]}, complexity {e["cx"]}, {e["floats"]} fitted floats frozen at train. A description of data, not a theory; no action. kappa = 1/2 FITTED."""\nimport os, sys\nsys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))\nimport sy1_leaves as _L\nEXPR = {e["H"]!r}; WRAP = {e["w"]}; NAME = "SY1 arm {arm} " + EXPR; VERTICAL = ("R",); TRAINED_ON = ("xcop_train", "sparc_train")\ndef g(Q): return _L.g_of_Q(EXPR, WRAP, Q)\n'); return p
    return make
def run_real():
    RQ = None; res = {}
    for arm in "TZ":
        S, n, nf = stage1(arm, XM0, XR0); say(f"arm {arm}: front entries {nf}, in grammar {n}, Stage 1 distinct {len(S)}"); ids = {}; rows = []
        if S and RQ is None:
            import sy1_stage3 as ST3; RQ = ST3.load()
        for j, e in enumerate(S[:200]):
            ids[id(e)] = j; e["stage2"] = stage2(e, RQ, cand_file(lambda q: ids[id(q)], arm)); rows.append(e); say(f"  W{e['w']} cx {e['cx']} floats {e['floats']} {e['H'][:90]} | train X {e['x_mean']:+.3f},{e['x_rms']:.3f} S {e['s_rms']:.3f} {e['s_med']:+.3f} | " + " ".join(f"{ft}: G3 {r['g3']} hold {r['hold_rms']:.3f}/{r['line']:.3f} {r['hold_med']:+.3f} X {r['xhold']:+.3f},{r['xhold_rms']:.3f}; G4 {r['g4']} {r['lt']:+.3f}; G5 {r['g5']}" for ft, r in e["stage2"].items()))
        lab = {}
        for ft in FOOT:
            l = "NO HIT"
            if S: l = "TRAIN ONLY"
            if any(e["stage2"][ft]["g3"] for e in rows): l = "X-COP AND DISCS ONLY"
            s2 = [e for e in rows if e["stage2"][ft]["g3"] and e["stage2"][ft]["g4"] and e["stage2"][ft]["g5"]]
            if s2: l = "HOLDS OUT, FAILS ACCEPTANCE (stage 3 pending)"
            lab[ft] = l
        s3 = []
        if a.stage3:
            for e in rows:
                if any(e["stage2"][ft]["g5"] for ft in FOOT):
                    p = cand_file(lambda q: ids[id(q)], arm)(e); nm = os.path.basename(p)[:-3]; subprocess.run([sys.executable, os.path.join(HERE, "sy1_stage3.py"), p], stdout=open(os.path.join(HERE, f"{nm}_stage3.log"), "w"), stderr=subprocess.STDOUT, cwd=HERE); o = json.load(open(os.path.join(HERE, "results", nm + ".json"))); s3.append({ft: o["footings"][ft]["summary"]["overall"] for ft in FOOT}); e["stage3"] = s3[-1]; e["stage3_counts"] = {ft: o["footings"][ft]["summary"]["counts"] for ft in FOOT}; e["point_rule_rows"] = sorted({"A9", "A10", "A11", "A12", "A13", "A20", "A23a", "A23b", "A25", "A26b", "B2", "C1"}) if reads(e["H"]) & {"s", "D"} else []; say(f"  Stage 3 {nm}: {e['stage3']}, counts {e['stage3_counts']}; rows on the point rule, no pass for s: {e['point_rule_rows']}")
                    for ft in FOOT:
                        if e["stage2"][ft]["g5"]: lab[ft] = "SURVIVOR" if not e["stage3"][ft].startswith("REJECTED") else "HOLDS OUT, FAILS ACCEPTANCE"  # RQ3 can't read ACCEPTED while action rows are NOT COMPUTABLE; SURVIVOR = no computed row FAILS, NOT COMPUTABLE counts stated
        say(f"arm {arm} label by footing: {lab}. Floats allowed {MAXFLOATS[arm]}."); res[arm] = dict(stage1=len(S), entries=nf, labels=lab, rows=rows)
    return res
if MODE == "planted": R = planted()
elif MODE == "mutate":
    R = {}; 
    for arm in "TZ":
        S, n, nf = stage1(arm, 1e-6, 1e-6); Sr, nr, _ = stage1(arm, 1e-6, 1e-6, mode="real") if os.path.isdir(os.path.join(a.runs, "real")) else ([], 0, 0); R[arm] = dict(stage1=len(S), entries=n, real_fronts_stage1=len(Sr), real_entries=nr, ok=not S and not Sr); say(f"MUTATE arm {arm}, gate 1 at 1e-6: own fronts {len(S)} of {n}, real fronts {len(Sr)} of {nr}; {'returns nothing, as it must' if R[arm]['ok'] else 'FAILED: it must return nothing'}")
elif MODE == "scrambled":
    R = {}
    for arm in "TZ": S, n, nf = stage1(arm, XM0, XR0); R[arm] = dict(stage1=len(S), entries=n, rows=S[:200]); say(f"scrambled arm {arm}: Stage 1 distinct {len(S)} of {n}")
elif MODE == "real":
    if not a.smoke:
        miss = [m for m in ("planted", "scrambled", "mutate") if not os.path.exists(os.path.join(HERE, f"sy1_{m}_read.json"))]
        if miss: sys.exit(f"controls unread: {miss}; they read first, per FROZEN_CRITERIA")
        P = json.load(open(os.path.join(HERE, "sy1_planted_read.json"))); say("planted:", {k: P[k]["all_recovered"] for k in "TZ"}); C = json.load(open(os.path.join(HERE, "sy1_scrambled_read.json"))); say("scrambled Stage 1:", {k: C[k]["stage1"] for k in "TZ"})
    R = run_real()
    if not a.smoke:
        for arm in "TZ":
            if not P[arm]["all_recovered"]: R[arm]["labels"] = {f: "NO VERDICT" for f in FOOT}; say(f"arm {arm}: NO VERDICT, a planted form was not recovered; its hits, if any, stay listed without a label")
else: sys.exit("mode?")
say("kappa = 1/2 FITTED; not theory closed. A hit is a description of data, not a theory; a null applies to this grammar, these leaves, this run length.")
tag = "smoke_" if a.smoke else ""
json.dump(R, open(os.path.join(HERE, f"sy1_{tag}{MODE}_read.json"), "w"), indent=0, default=float); open(os.path.join(HERE, f"sy1_{tag}{MODE}_read.out"), "w").write("\n".join(OUT) + "\n")
