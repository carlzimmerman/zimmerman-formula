#!/usr/bin/env python3
"""SR3 harvest: every front row through the frozen gates, controls, planted test, selection for RQ3, physical table. SR3_MUTATE=1 for the twin. kappa = 1/2 FITTED; not theory closed."""
import csv, glob, json, math, os, re, sys
sys.dont_write_bytecode = True
os.environ["OMP_NUM_THREADS"] = "1"; os.nice(19)
import numpy as np
import sr3_core as K
TAG = "_MUTATE" if K.MUT else ""; OUT = open(os.path.join(K.HERE, f"sr3_grade{TAG}.out"), "w")
def say(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.write(s + "\n"); OUT.flush()
CACHE = {}
def P_(job, foot):
    if (job, foot) not in CACHE:
        P = K.prep(job, foot); P["tr"] = [g for g in P["gals"] if K.is_train(g)]; P["ho"] = [g for g in P["gals"] if K.is_hold(g)]; CACHE[(job, foot)] = P
    return CACHE[(job, foot)]
LAWS = {}
def law_lines(job, foot):
    if (job, foot) not in LAWS:
        P = P_(job, foot); LAWS[(job, foot)] = dict(tr=K.free_path(P["tr"], None, P["a0"]), ho=K.free_path(P["ho"], None, P["a0"]), trf=K.fixed_path(P["tr"], None, P["a0"]), hof=K.fixed_path(P["ho"], None, P["a0"]))
    return LAWS[(job, foot)]
def limits(Hf):
    y = np.geomspace(1e-4, 1e9, 200); f0 = np.zeros_like(y)
    try: h = Hf(f0, y); d0 = float(np.max(np.abs(h - 1))) if np.all(np.isfinite(h)) else float("inf")
    except Exception: d0 = float("inf")
    pf, py = np.meshgrid([.1, .3, .5, .7, .9, 1.0], np.geomspace(1e6, 1e12, 13))
    try: h = Hf(pf.ravel(), py.ravel()); dy = float(np.max(np.abs(np.log10(h)))) if np.all(np.isfinite(h)) and np.all(h > 0) else float("inf")
    except Exception: dy = float("inf")
    return dict(F0=d0, Yinf=dy, F_LIMIT=d0 <= 1e-3, F_EXACT=d0 <= 1e-10, Y_LIMIT=dy <= 1e-3)
def gate(eq, tier, job, foot, hold_job=None):
    """Gates on the footing and job given. Train leaves carry the job's scramble; holdouts are real unless label or planted."""
    Hf = K.compile_form(eq, tier); P = P_(job, foot); a0 = P["a0"]; L = law_lines(job, foot); R = dict(eq=eq, tier=tier, job=job, foot=foot, nfit=K.n_fitted(eq))
    hj = job if job in ("label", "planted") else "real"; Q = P_(hj, foot); LH = law_lines(hj, foot)
    tr = K.free_path(P["tr"], Hf, a0); ho = K.free_path(Q["ho"], Hf, a0); xt = K.xcop_stat(P["X"], Hf, a0, 0); xh = K.xcop_stat(Q["X"], Hf, a0, 1); lt = K.lt_stat(Hf, a0, hj); ft = K.fixed_path(P["tr"], Hf, a0); fh = K.fixed_path(Q["ho"], Hf, a0)
    R.update(tr=tr, ho=ho, xt=xt, xh=xh, lt=lt, ftr=ft, fho=fh, law_tr=L["tr"]["rms"], law_ho=LH["ho"]["rms"], limits=limits(Hf))
    def disc(s, lw): return s["invalid"] == 0 and s["rms"] <= 1.05 * lw and 0.5 <= s["U"] <= 0.8 and abs(s["tilt"]) <= .15
    def soft(s): return s["invalid"] == 0 and s["rms"] <= K.L_S and 0.5 <= s["U"] <= 0.8 and abs(s["tilt"]) <= .15
    xok = lambda x: abs(x["mean"]) <= .05 and x["rms"] <= .10
    R["G1"] = xok(xt); R["G2"] = disc(tr, L["tr"]["rms"]); R["G2S"] = soft(tr); R["G3"] = xok(xh) and disc(ho, LH["ho"]["rms"]); R["G3S"] = xok(xh) and soft(ho); R["G4"] = abs(lt["E"]) <= .10
    R["label"] = "CLEAN" if R["G1"] and R["G2"] and R["G3"] and R["G4"] else "XDISC" if R["G1"] and R["G2"] and R["G3"] else "TRAIN" if R["G1"] and R["G2"] else "NEAR" if R["G1"] and R["G2S"] else "-"
    return R
def line(c, r):
    t, h = r["tr"], r["ho"]; lim = r["limits"]; return f"c{c:>3} k{r['nfit']} {r['label']:5s} X {r['xt']['mean']:+.3f},{r['xt']['rms']:.3f} | S {t['rms']:.4f}/{r['law_tr']:.4f} U {t['U']:.2f} t {t['tilt']:+.2f} bad {t['invalid']} fix {r['ftr']['rms']:.3f} || Xh {r['xh']['mean']:+.3f},{r['xh']['rms']:.3f} Sh {h['rms']:.4f}/{r['law_ho']:.4f} U {h['U']:.2f} t {h['tilt']:+.2f} fix {r['fho']['rms']:.3f} LT {r['lt']['E']:+.3f} | F0 {lim['F0']:.1e} Yinf {lim['Yinf']:.1e} | {r['eq'][:90]}"
ALL = {}; fr = sorted(glob.glob(os.path.join(K.HERE, "fronts", "hof_*.csv")))
say(f"SR3 grade{TAG}. Fronts on disk: {len(fr)}. X = mean,rms X-COP train; S = free-path rms/law, U median, t tilt; Xh, Sh held out; c complexity of tree (T1 frames +4); k fitted constants. Labels: CLEAN G1-G4, XDISC G1-G3, TRAIN G1-G2, NEAR G1 + G2-SOFT.")
for F in fr:
    tag = os.path.basename(F)[4:-4]; job, foot, tier, path = tag.split("_")[:4]; say(f"\n=== {tag} ==="); rows = []
    for r in csv.DictReader(open(F)):
        q = gate(r["equation"], tier, job, foot); q["c"] = int(r["complexity"]); q["loss"] = float(r["loss"]); rows.append(q); say(line(q["c"], q))
    ALL[tag] = rows
# planted
PLANT = {}
for tag, rows in ALL.items():
    if not tag.startswith("planted"): continue
    job, foot, tier, path = tag.split("_")[:4]; tab = K.search_table(P_(job, foot)); f, y = tab["S"][:, 0], tab["S"][:, 1]; f = np.r_[f, tab["Xf"]]; y = np.r_[y, tab["Xy"]]; best = float("inf"); bq = None
    for q in rows:
        if q["c"] > 15: continue
        d = np.max(np.abs(np.log10(K.compile_form(q["eq"], q["tier"])(f, y)) - np.log10(K.H_plant(f, y))))
        if np.isfinite(d) and d < best: best = float(d); bq = q["eq"]
    line_ = .02 if tier == "T1FY" else .05; PLANT[tier] = dict(worst_dex=best, line=line_, ok=best <= line_, eq=bq); say(f"\nPLANTED {tier}: worst |dlog10 H| {best:.4f}, line {line_}: {'PASS' if best <= line_ else 'FAIL'}; {bq}")
# label summary, real
say("\n=== labels ==="); SUM = {}
for tag, rows in ALL.items():
    c = {l: sum(q["label"] == l for q in rows) for l in ("CLEAN", "XDISC", "TRAIN", "NEAR")}; best = min((q for q in rows if q["G1"]), key=lambda q: q["tr"]["rms"], default=None); SUM[tag] = dict(counts=c, n=len(rows)); say(f"{tag:42s} {c}  G1 best SPARC train rms {best['tr']['rms']:.4f} U {best['tr']['U']:.2f} c{best['c']}" if best else f"{tag:42s} {c}  no G1 row")
# selection: frozen rule
real = [(t, q) for t, rows in ALL.items() if t.startswith("real") for q in rows]; pick = []; seen = set()
def add(t, q):
    key = tuple(t.split("_")[1:3])
    if len(pick) < 3 and key not in seen: seen.add(key); pick.append((t, q))
for t, q in sorted([x for x in real if x[1]["label"] == "CLEAN"], key=lambda x: x[1]["c"]): add(t, q)
for t, q in sorted([x for x in real if x[1]["G1"] and x[1]["c"] <= 15], key=lambda x: x[1]["loss"]): add(t, q)
say("\n=== selected for acceptance, frozen rule ==="); os.makedirs(os.path.join(K.HERE, "candidates"), exist_ok=True); SEL = []
TPL = '''"""SR3 candidate {n}: found on {t}, formula unchanged on either footing. {k} fitted constant(s), labelled fitted. A description; no action, no field equation. kappa = 1/2 FITTED."""
import math
import numpy as np
from numpy import sqrt, exp, log1p, square
NAME = "SR3 form {n}, {t}"; VERTICAL = ("R",); TRAINED_ON = ()
EQ = {eq!r}; T1 = {t1}
_C = compile(EQ.replace("^", "**"), "f", "eval")
def g(Q):
    gb = np.asarray(Q["gb"], float); a = Q["a0"]; gg = np.maximum(np.asarray(Q["gg"], float), 0.0)
    with np.errstate(all="ignore"):
        s = np.where(gb > 0, gb, 1.0); L = np.where(gb > 0, gb * (0.5 + np.sqrt(0.25 + a / s)), gb); f = np.clip(gg / s, 0.0, 1.0); y = s / a
        v = eval(_C, dict(__builtins__={{}}, f=f, y=y, yg=f * y, ys=(1 - f) * y, one=1.0, two=2.0, pii=math.pi, sqrt=sqrt, exp=exp, log1p=log1p, square=square)) * np.ones_like(y)
        H = 1 + f * v if T1 else v
    return np.where(gb > 0, L * H, L)
'''
for n, (t, q) in enumerate(pick):
    p = os.path.join(K.HERE, "candidates", f"sr3_{n}.py"); open(p, "w").write(TPL.format(n=n, t=t, k=q["nfit"], eq=q["eq"], t1=q["tier"] != "T0")); ot = "alt" if q["foot"] == "canonical" else "canonical"; o = gate(q["eq"], q["tier"], "real", ot); say(f"sr3_{n} {t}\n  {line(q['c'], q)}\n  other footing, unchanged: {line(q['c'], o)}"); SEL.append(dict(n=n, tag=t, row=q, other=o))
# cross-footing for any CLEAN
for t, q in real:
    if q["label"] == "CLEAN":
        ot = "alt" if q["foot"] == "canonical" else "canonical"; o = gate(q["eq"], q["tier"], "real", ot); say(f"CLEAN on {t} c{q['c']}: other footing label {o['label']}")
# physical table
P = P_("real", "canonical"); a0 = P["a0"]; fx, gx, ff = K.fixed_rows(P["tr"], a0); yx = fx / a0; T = P["X"]; ty = T[:, 0] / a0; tf = T[:, 2]; LTr = K.lt_rows(); ly = np.array([r[0] / a0 for r in LTr]); lf = np.array([r[2] for r in LTr]); rich = ff > .7; mf, my = [], []
for g in P["tr"]:
    if g["Vflat"] > 200: mf += list(g["fixf"][-3:]); my += list(g["fixgb"][-3:] / a0)
PTS = {"X-COP median": (np.median(tf), np.median(ty)), "X-COP inner row, x 0.1": (np.median(tf[::5]), np.median(ty[::5])), "X-COP outer row, x 0.7": (np.median(tf[4::5]), np.median(ty[4::5])), "LITTLE THINGS median": (np.median(lf), np.median(ly)), "SPARC f>0.7 median": (np.median(ff[rich]), np.median(yx[rich])), "SPARC massive, outer": (np.median(mf), np.median(my)), "Bullet gas peak, my estimate": (0.9, 14.0), "Saturn": (0.0, 6.5e-5 / a0), "f 1, y 1e4, unpinned": (1.0, 1e4)}
say("\n=== (f, y) places ===")
for k, (f, y) in PTS.items(): say(f"{k:30s} f {f:.3f} y {y:.3g}")
d = [(np.min(np.hypot(0, 0) + (np.abs(ff - tf[i]) <= .05) * (np.abs(np.log10(yx / ty[i])) <= .2) * 0 + (~((np.abs(ff - tf[i]) <= .05) & (np.abs(np.log10(yx / ty[i])) <= .2))) * 1.0)) == 0 for i in range(len(tf))]; ov = float(np.mean(d)); say(f"Overlap: {sum(d)} of {len(d)} X-COP rows ({ov:.0%}) have a SPARC train row within 0.05 in f and 0.2 dex in y, canonical, fixed U.")
says = np.geomspace
for name, sel in [(f"sr3_{s['n']}", s["row"]) for s in SEL]:
    Hf = K.compile_form(sel["eq"], sel["tier"]); say(f"{name} H: " + "; ".join(f"{k.split(',')[0]} {float(Hf(np.array([f]), np.array([y]))[0]):.3g}" for k, (f, y) in PTS.items()))
json.dump(dict(fronts=ALL, planted=PLANT, summary=SUM, selected=SEL, places={k: list(map(float, v)) for k, v in PTS.items()}, overlap=ov), open(os.path.join(K.HERE, f"sr3_grade{TAG}.json"), "w"), indent=0, sort_keys=True, default=float)
