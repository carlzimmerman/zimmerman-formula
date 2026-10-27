"""CFG406: re-score CFG687's outer-lensing mass slope (T2, Part A) and X43's cluster keys (Part B) with CFG816's Eddington-corrected eRASS1
gas masses. Criteria: FROZEN_CRITERIA.md (3e2e282e11). Bins and slope x-axes stay on OBSERVED Mgas500; only predictions change.
Run:  nice python3 cfg406_rescore.py            -> Part A + Part B (X43 run three times in subprocesses: E0, Eh, E1)
      MUTATE=1 nice python3 cfg406_rescore.py   -> Part A with the sign-flipped correction (|ds| must grow on both footings; rc 1)
      python3 cfg406_rescore.py --x43 E1        -> internal: one X43 run with the gas-mass injection (called by the main run)
Single thread. kappa = 1/2 FITTED; not theory closed."""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ[_v] = "1"
import sys, math, json, time, io, contextlib, subprocess, numpy as np
from scipy.interpolate import CubicSpline

HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES)
REB = os.path.join(REPO, "rebuild_2026_10_22"); EXT = os.path.abspath(os.path.join(LANES, "..", "..", "_external_data"))
TSV = os.path.join(EXT, "cfg687_inputs", "erass1_main.tsv")
X43SRC = os.path.join(REB, "X43_collapse_core_floor", "x43_collapse_core.py")
ALPHA = float(json.load(open(os.path.join(LANES, "CFG816_erass1_eddington", "cfg816_results.json")))["alpha"])
POW = {"E0": 0.0, "Eh": 0.5, "E1": 1.0}

def sigma_by_name():
    s = {}
    for l in open(TSV):
        r = l.rstrip("\n").split("\t")
        try: mg, lo, hi = float(r[5]), float(r[6]), float(r[7])
        except Exception: continue
        if mg > 0 and lo > 0 and hi > 0: s.setdefault(r[0].strip(), 0.5 * (math.log(hi) - math.log(lo)))
    return s

# =============================================================== Part B child: one X43 run with the injection
if "--x43" in sys.argv:
    etag = sys.argv[sys.argv.index("--x43") + 1]; pw = POW[etag]; SIG = sigma_by_name(); miss = []
    def EF(CL):
        for c in CL:
            if c["name"] not in SIG: miss.append(c["name"]); continue
            c["Mgas500"] = c["Mgas500"] * math.exp(-pw * ALPHA * SIG[c["name"]] ** 2)
    src = open(X43SRC).read()
    reps = [('HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE)', f'HERE = {HERE!r}; REB = {REB!r}'),
            ('TAG = "_MUTATE" if MUTATE else ""', f'TAG = {"_" + etag!r}'),
            ('NX = {"__file__": X30SRC, "__name__": "x30_ro"}; sys.argv = [X30SRC]',
             'assert codeX.count(\'CL = NS2["CL"];\') == 1; codeX = codeX.replace(\'CL = NS2["CL"];\', \'CL = NS2["CL"]; __EF__(CL);\'); '
             'NX = {"__file__": X30SRC, "__name__": "x30_ro", "__EF__": __EF__}; sys.argv = [X30SRC]')]
    for o, n in reps:
        assert src.count(o) == 1, o
        src = src.replace(o, n)
    G = {"__file__": X43SRC, "__name__": "x43_cfg406", "__EF__": EF}; sys.argv = [X43SRC]; rc = 0
    try: exec(compile(src, X43SRC, "exec"), G)
    except SystemExit as e: rc = e.code
    NX = G["NX"]; arr = {"T3M": np.asarray(NX["T3M"]), "I": np.asarray(NX["I"]), "TID": np.asarray(NX["TID"])}
    for (f, hk), c in NX["MEAS"].items(): arr[f"d__{f}__{hk}"] = np.asarray(c["d"])
    np.savez(os.path.join(HERE, f"cfg406_x43_{etag}_arrays.npz"), **arr)
    json.dump({"etag": etag, "x43_rc": rc, "missing_names": miss, "M": NX["M"], "names": [c["name"] for c in NX["CL"]],
               "Mgas500_used": [float(c["Mgas500"]) for c in NX["CL"]]},
              open(os.path.join(HERE, f"cfg406_x43_{etag}_meas.json"), "w"), default=float)
    sys.exit(0)

MUT = os.environ.get("MUTATE") == "1"
OUT, CONTROLS = [], {"A": [], "B": []}
def P(s=""): print(s, flush=True); OUT.append(str(s))
def K(part, name, ok, val): CONTROLS[part].append({"name": name, "pass": bool(ok), "value": val}); P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {val}")
T0 = time.time()
P("CFG406 Eddington re-score of CFG687 T2 (Part A) and X43's cluster keys (Part B)" + ("  [MUTATE: sign-flipped correction, Part A only]" if MUT else ""))
P("=" * 110); P(f"alpha (CFG816 committed) = {ALPHA:.4f}")

# =============================================================== Part A: CFG687 T2 on its own estimator
SRC6 = os.path.join(LANES, "CFG686_cluster_shear_vs_law", "cfg686_shear.py"); T6 = open(SRC6).read()
code6 = (T6[:T6.index("# ---- sources ----")] + "EDGES = np.logspace(np.log10(0.15), np.log10(3.0), 9); RC = np.sqrt(EDGES[1:]*EDGES[:-1])\n"
         + T6[T6.index("# ---- the law's prediction from ACCEPT gas ----"):T6.index("# ---- measure ----")])
g6 = {"__file__": SRC6, "__name__": "cfg686_ro"}; argv0 = sys.argv; sys.argv = [SRC6, "unused (no KiDS columns loaded)"]
with contextlib.redirect_stdout(io.StringIO()): exec(compile(code6, SRC6, "exec"), g6)
sys.argv = argv0
S7 = open(os.path.join(LANES, "CFG687_erass1_shear_stack", "cfg687_stack.py")).read()
L = dict(np=np, RGRID=g6["RGRID"], MPC=g6["MPC"], G=g6["G"], MSUN=g6["MSUN"], nu_mono=g6["nu_mono"], sigma_proj=g6["sigma_proj"], RC=g6["RC"], KG=g6["KG_PER_MSUN_PC2"])
exec(S7[S7.index("def law("):S7.index("BR = [")], L); law = L["law"]; A0 = g6["A0"]
d = np.load(os.path.join(LANES, "CFG687_erass1_shear_stack", "cfg687_percluster.npz"))
D, E, PLs, PNs, mg, ra, dec, R5 = (d[k] for k in ("D", "E", "PL", "PN", "mg", "ra", "dec", "R500")); n = len(mg)
W = np.where(E > 0, 1 / E ** 2, 0); J = [6, 7]
order = np.argsort(ra); patch = np.empty(n, int); patch[order] = np.arange(n) * 30 // n
q = np.quantile(mg, [0, 1 / 3, 2 / 3, 1]); tid = np.clip(np.digitize(mg, q[1:-1]), 0, 2)

# sigma: CFG816's matching verbatim (nearest in RA cos(dec), dec over rows with Mgas and bounds)
rows = []
for l in open(TSV):
    r = l.rstrip("\n").split("\t")
    try: rr = (float(r[1]), float(r[2]), float(r[3]), float(r[5]), float(r[6]), float(r[7]))
    except Exception: continue
    if rr[3] > 0 and rr[4] > 0 and rr[5] > 0: rows.append(rr)
C = np.array(rows); sig = np.zeros(n)
for i in range(n):
    dd = (C[:, 0] - ra[i]) ** 2 * np.cos(np.radians(dec[i])) ** 2 + (C[:, 1] - dec[i]) ** 2
    j = int(np.argmin(dd)); sig[i] = 0.5 * (np.log(C[j, 5]) - np.log(C[j, 4]))

def preds(fac, foot):
    a0 = 0.0 if foot == "newton" else A0[foot]
    return np.array([law(dict(Mgas500=float(mg[i] * fac[i]), R500=float(R5[i])), a0, 2 / 3, 0.15, 0.20) for i in range(n)])
def outer_stack(sel, arr): return (W[sel][:, J] * arr[sel][:, J]).sum() / W[sel][:, J].sum()
def slope(sel, arr):
    xs, ys = [], []
    for t in range(3):
        s = sel & (tid == t); v = outer_stack(s, arr)
        if v <= 0: return np.nan
        xs.append(np.log10(np.median(mg[s]))); ys.append(np.log10(v))
    return float(np.polyfit(xs, ys, 1)[0])
def jk(fun):
    full = fun(np.ones(n, bool)); reps = np.array([fun(patch != p) for p in range(30)])
    return float(full), float(np.sqrt(29 / 30 * np.sum((reps - reps.mean()) ** 2)))
def A_out(sel, Pm): return (W[sel][:, J] * D[sel][:, J]).sum() / (W[sel][:, J] * Pm[sel][:, J]).sum()
def T2cls(so, se, sl, sn):
    return "FOLLOWS THE LAW" if (abs(so - sl) < 2 * se and abs(so - sn) >= 2 * se) else ("FOLLOWS NEWTON" if (abs(so - sn) < 2 * se and abs(so - sl) >= 2 * se) else "NOT DECIDED")

so, se = jk(lambda s: slope(s, D)); ALL = np.ones(n, bool)
P("\nPART A: CFG687 T2 (318 clusters; data stack from cfg687_percluster.npz; law() verbatim; bins on observed Mgas500)")
fac = {k: np.exp(-p * ALPHA * sig ** 2) for k, p in POW.items()}
if MUT: fac = {"E0": fac["E0"], "E1m": np.exp(+ALPHA * sig ** 2)}
PR = {k: {foot: preds(fk, foot) for foot in ("canonical", "alt", "newton")} for k, fk in fac.items()}
P("\nCONTROLS (A)")
k1p = float(max(np.max(np.abs(PR["E0"]["canonical"] / PLs - 1)), np.max(np.abs(PR["E0"]["newton"] / PNs - 1))))
sl0, sn0 = slope(ALL, PR["E0"]["canonical"]), slope(ALL, PR["E0"]["newton"])
k1 = k1p <= 1e-9 and round(sl0, 2) == 0.47 and round(sn0, 2) == 0.84 and (round(so, 2), round(se, 2)) == (0.90, 0.21) and T2cls(so, se, sl0, sn0) == "FOLLOWS NEWTON"
K("A", "K1 E0 reproduces stored PL/PN (<= 1e-9 rel), s_law 0.47, s_N 0.84, s_obs 0.90 +- 0.21, T2 FOLLOWS NEWTON (canonical)", k1,
  f"max rel {k1p:.1e}; s_law {sl0:.4f}, s_N {sn0:.4f}, s_obs {so:.4f} +- {se:.4f}, T2 {T2cls(so, se, sl0, sn0)}")
q816 = np.quantile(mg, [1 / 3, 2 / 3]); T816 = [mg <= q816[0], (mg > q816[0]) & (mg <= q816[1]), mg > q816[1]]
c1 = np.exp(-ALPHA * sig ** 2)
ms, mc = [f"{np.median(sig[t]):.3f}" for t in T816], [f"{np.median(c1[t]):.3f}" for t in T816]
o816 = open(os.path.join(LANES, "CFG816_erass1_eddington", "cfg816.out")).read()
k2 = ("median sigma per (observed) tercile: " + " / ".join(ms) + "; median M_true/M_obs: " + " / ".join(mc)) in o816
K("A", "K2 CFG816's matching code verbatim reproduces its printed per-tercile median sigma and M_true/M_obs (CFG816 stored no per-cluster sigma)", k2,
  f"sigma {' / '.join(ms)}; corr {' / '.join(mc)}")

def summary(k):
    o = {}
    for foot in ("canonical", "alt"):
        sl, sn = slope(ALL, PR[k][foot]), slope(ALL, PR[k]["newton"])
        At = [jk(lambda s, t=t: A_out(s & (tid == t), PR[k][foot])) for t in range(3)]
        o[foot] = dict(s_law=sl, s_newton=sn, ds=so - sl, T2=T2cls(so, se, sl, sn), A_outer=At)
    return o
SUM = {k: summary(k) for k in PR}
for k, o in SUM.items():
    for foot, x in o.items():
        P(f"  {k:3s} {foot:9s}: s_obs {so:.2f} +- {se:.2f} | s_law {x['s_law']:.3f}  s_N {x['s_newton']:.3f}  ds {x['ds']:+.3f} -> {x['T2']} | A_OUTER by observed tercile "
          + " / ".join(f"{a:.2f}+-{b:.2f}" for a, b in x["A_outer"]))

if MUT:
    ok = all(abs(SUM["E1m"][f]["ds"]) > abs(SUM["E0"][f]["ds"]) for f in ("canonical", "alt"))
    K("A", "MUTATE sign-flipped correction: |ds| grows on both footings", ok,
      {f: (round(SUM['E0'][f]['ds'], 3), round(SUM['E1m'][f]['ds'], 3)) for f in ("canonical", "alt")})
    json.dump({"lane": "CFG406", "mutate": True, "summary": SUM, "controls": CONTROLS}, open(os.path.join(HERE, "cfg406_results_MUTATE.json"), "w"), indent=1, default=float)
    open(os.path.join(HERE, "cfg406_MUTATE.out"), "w").write("\n".join(OUT) + "\n")
    sys.exit(1)

# null: sigma permuted across clusters (E1), per-cluster cubic spline in ln(factor), validated against direct law() (K3)
lfmin = float(np.min(-ALPHA * sig ** 2)); nodes = np.linspace(lfmin * 1.0001, 0.0, 41)
SPL = {}
for foot in ("canonical", "alt"):
    grid = np.array([preds(np.full(n, math.exp(x)), foot) for x in nodes])            # (41, n, 8)
    SPL[foot] = CubicSpline(nodes, grid, axis=0)
def interp(lf, foot):
    v = SPL[foot](lf)                                                                   # (n_lf, n, 8) for per-cluster lf
    return v[np.arange(n), np.arange(n)]
k3 = max(float(np.max(np.abs(interp(-ALPHA * sig ** 2, f) / PR["E1"][f] - 1))) for f in ("canonical", "alt"))
K("A", "K3 null interpolation within 0.2% of direct law() at E1 (every cluster and bin, both footings)", k3 <= 2e-3, f"max rel {k3:.2e}")
rng = np.random.default_rng(406); NULL = {f: [] for f in ("canonical", "alt")}
for _ in range(200):
    sp = rng.permutation(sig); lf = -ALPHA * sp ** 2
    for f in ("canonical", "alt"):
        NULL[f].append(abs(so - slope(ALL, interp(lf, f))))
special = all(abs(SUM["E1"][f]["ds"]) < np.percentile(NULL[f], 5) for f in ("canonical", "alt"))
P("\nNULL (sigma permuted, 200 draws, E1)")
for f in ("canonical", "alt"):
    pc = np.percentile(NULL[f], [5, 16, 50, 84, 95])
    P(f"  {f}: |ds_E1| {abs(SUM['E1'][f]['ds']):.3f} vs null |ds| pct 5/16/50/84/95 = " + " / ".join(f"{x:.3f}" for x in pc)
      + f"; frac of null <= |ds_E1|: {np.mean(np.array(NULL[f]) <= abs(SUM['E1'][f]['ds'])):.3f}")
P(f"  -> E1 SPECIAL: {special}")
validA = all(c["pass"] for c in CONTROLS["A"])
t2 = {k: {f: SUM[k][f]["T2"] for f in ("canonical", "alt")} for k in SUM}
if not validA: readA = "INVALID (a Part A control failed)"
elif all(t2["E1"][f] == "FOLLOWS THE LAW" for f in t2["E1"]) and all(t2["Eh"][f] != "FOLLOWS NEWTON" for f in t2["Eh"]) and special: readA = "SELECTION RESOLVES T2"
elif all(t2["E1"][f] != "FOLLOWS NEWTON" for f in t2["E1"]):
    why = [w for w, c in (("E1 not FOLLOWS THE LAW on both footings", not all(t2["E1"][f] == "FOLLOWS THE LAW" for f in t2["E1"])),
                          ("E1/2 still FOLLOWS NEWTON on a footing", not all(t2["Eh"][f] != "FOLLOWS NEWTON" for f in t2["Eh"])),
                          ("E1 not SPECIAL vs the shuffle null", not special)) if c]
    readA = "SELECTION PARTLY (" + "; ".join(why) + ")"
else: readA = "NOT RESOLVED"
P(f"\nPART A READING (frozen): {readA}   [{time.time() - T0:.0f} s]")

# =============================================================== Part B: X43's cluster keys (three child runs)
P("\nPART B: X43 cluster keys (326 clusters via X30/X7), injection after X30's CL; groups key out of scope")
SIGN = sigma_by_name(); x7n = [str(x).strip() for x in np.load(os.path.join(REB, "X7_cluster_core_significance", "x7_measure_percluster.npz"), allow_pickle=True)["name"]]
nmatch = sum(nm in SIGN for nm in x7n)
P(f"  name match to erass1_main.tsv: {nmatch}/{len(x7n)} (fallback by position not needed)" if nmatch == len(x7n) else f"  name match {nmatch}/{len(x7n)}: Part B INVALID")
env = dict(os.environ, PYTHONHASHSEED="0")
for etag in ("E0", "Eh", "E1"):
    t1 = time.time()
    r = subprocess.run([sys.executable, os.path.abspath(__file__), "--x43", etag], env=env, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
    P(f"  X43 child {etag}: rc {r.returncode} [{time.time() - t1:.0f} s]" + (f"  stderr tail: {r.stderr.strip()[-300:]}" if r.returncode else ""))
RX = {e: json.load(open(os.path.join(HERE, f"x43_collapse_core_results_{e}.json"))) for e in ("E0", "Eh", "E1")}
MX = {e: json.load(open(os.path.join(HERE, f"cfg406_x43_{e}_meas.json"))) for e in ("E0", "Eh", "E1")}
AX = {e: np.load(os.path.join(HERE, f"cfg406_x43_{e}_arrays.npz")) for e in ("E0", "Eh", "E1")}
REF = json.load(open(os.path.join(REB, "X43_collapse_core_floor", "x43_collapse_core_results.json")))
FEET, HKS, BN = ("canonical", "alt"), ("h0672", "h0686"), ("INNER", "MID", "OUTER")
P("\nCONTROLS (B)")
K("B", "names: all 326 X7/X30 clusters matched to the catalogue with valid bounds; no injection misses", nmatch == len(x7n) and not any(MX[e]["missing_names"] for e in MX),
  f"{nmatch}/{len(x7n)}; misses {[len(MX[e]['missing_names']) for e in MX]}")
dev4 = 0.0
for f in FEET:
    for hk in HKS:
        for k, c in REF["footings"][f]["clusters"]["cells"][hk].items():
            for fld in ("meas", "s", "pred", "Z"):
                dev4 = max(dev4, abs(RX["E0"]["footings"][f]["clusters"]["cells"][hk][k][fld] - c[fld]))
K("B", "K4 E0 through the injection reproduces every committed X43 cluster cell (meas, s, pred, Z; both footings, both h cells) to <= 1e-9", dev4 <= 1e-9, f"max |diff| {dev4:.2e}")
T3M = AX["E0"]["T3M"]; I = AX["E0"]["I"]; TID = AX["E0"]["TID"]
def R_of(e, f, hk, sel, bi):
    d0, de_ = AX["E0"][f"d__{f}__{hk}"], AX[e][f"d__{f}__{hk}"]; return float(d0[sel, bi].sum() / de_[sel, bi].sum())
devA = devS = 0.0
for f in FEET:
    for hk in HKS:
        cl = f"{f}|{hk}"
        for b in BN:
            bi = BN.index(b)
            for t in range(3):
                for key, sel in ((f"KT_terc|{b}", I[TID == t]), (f"M_terc|{b}", np.where(T3M == t)[0])):
                    R = R_of("E1", f, hk, sel, bi); o0, o1 = MX["E0"]["M"][cl][key][t], MX["E1"]["M"][cl][key][t]
                    devA = max(devA, abs(o1["A"] / (o0["A"] * R) - 1)); devS = max(devS, abs(o1["s"] / (o0["s"] * R) - 1))
k5 = devA <= 1e-6 and devS <= 1e-6
K("B", "K5 X30 in-run KT/M_terc measured A and s under E1 equal E0 x R (<= 1e-6); failure marks the stored-X7 keys APPROXIMATE", k5,
  f"max rel dev A {devA:.2e}, s {devS:.2e}")
X7KEYS = {"G-OUT-Mall": None, "G-OUT-M1": 0, "G-OUT-M2": 1, "G-OUT-M3": 2}
def grade(e):
    out = {}
    for f in FEET:
        cells = {hk: {} for hk in HKS}
        for hk in HKS:
            for k, c in RX[e]["footings"][f]["clusters"]["cells"][hk].items():
                meas, s, pred = c["meas"], c["s"], c["pred"]
                if k in X7KEYS and e != "E0":
                    t = X7KEYS[k]; sel = np.arange(len(T3M)) if t is None else np.where(T3M == t)[0]
                    R = R_of(e, f, hk, sel, 2); meas, s = meas * R, s * R
                cells[hk][k] = dict(meas=meas, s=s, pred=pred, Z=(meas - pred) / s)
        keys = list(cells["h0672"]); ok = {k: all(abs(cells[hk][k]["Z"]) <= 2 for hk in HKS) for k in keys}
        fails = [k for k in keys if not ok[k]]
        out[f] = dict(cells=cells, fails=fails, sign={k: ("OVER" if cells["h0672"][k]["pred"] > cells["h0672"][k]["meas"] else "UNDER") for k in fails},
                      groups_Z=RX[e]["footings"][f]["groups"]["Z"])
    return out
GB = {e: grade(e) for e in ("E0", "Eh", "E1")}
refF = {f: sorted(x.split(" ")[0] for x in REF["footings"][f]["clusters"]["fails"]) for f in FEET}
for e in ("E0", "Eh", "E1"):
    for f in FEET:
        g = GB[e][f]
        P(f"  {e} {f:9s}: cluster fails {[k + ' (' + g['sign'][k] + ')' for k in g['fails']] or 'none'} | groups Z {g['groups_Z']:+.2f} (unchanged, out of scope)")
        for k in g["cells"]["h0672"]:
            c0, c1_ = g["cells"]["h0672"][k], g["cells"]["h0686"][k]
            P(f"       {k:10s} h0672 meas {c0['meas']:+.3f}+-{c0['s']:.3f} pred {c0['pred']:+.3f} Z {c0['Z']:+.2f} | h0686 Z {c1_['Z']:+.2f}"
              + ("  FAIL" if k in g["fails"] else "") + ("  [APPROX]" if (k in X7KEYS and e != "E0" and not k5) else ""))
validB = all(c["pass"] for c in CONTROLS["B"] if not c["name"].startswith("K5"))
def readB(f):
    new, ref = set(GB["E1"][f]["fails"]), set(refF[f])
    return "X43 GAINS" if (new < ref) else ("X43 HOLDS" if new == ref else "X43 LOSES (new: " + ", ".join(f"{k} ({GB['E1'][f]['sign'][k]})" for k in sorted(new - ref)) + ")")
RB = {f: readB(f) for f in FEET} if validB else {f: "INVALID (a Part B control failed)" for f in FEET}
P(f"\nPART B READING (frozen, E1): canonical {RB['canonical']} | alt {RB['alt']}   (X43 committed fails: {refF})")
P(f"\nPART A READING (frozen): {readA}")
P(f"controls A {sum(c['pass'] for c in CONTROLS['A'])}/{len(CONTROLS['A'])}, B {sum(c['pass'] for c in CONTROLS['B'])}/{len(CONTROLS['B'])}; runtime {time.time() - T0:.0f} s")
json.dump({"lane": "CFG406", "mutate": False, "alpha": ALPHA, "controls": CONTROLS, "partA": {"summary": SUM, "s_obs": [so, se], "null": NULL, "special": special, "reading": readA,
           "sigma": sig.tolist()}, "partB": {"grades": GB, "reading": RB, "ref_fails": refF, "K5_dev": [devA, devS]}},
          open(os.path.join(HERE, "cfg406_results.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, "cfg406.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if (validA and validB) else 2)
