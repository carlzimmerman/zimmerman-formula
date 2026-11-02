#!/usr/bin/env python3
"""RS1 Part 2: M_x = base x T, T = a op b on a level-2 pool. Args: FOOT UPS MODE [LIM]. MODE real|shuf|planted|mutate. Resumes. kappa = 1/2 FITTED; not theory closed."""
import heapq, json, math, os, signal, sys, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.dont_write_bytecode = True
import rs1_rows as T
import numpy as np
np.seterr(all="ignore")
FOOT, UPS, MODE = sys.argv[1:4]; LIM = int(sys.argv[4]) if len(sys.argv) > 4 else 0; CAP = 6000; WALL = 3 * 3600; TAG = f"{FOOT}_{UPS}_{MODE}"; OUTJ = os.path.join(HERE, "runs", f"arm_{TAG}.json"); os.makedirs(os.path.join(HERE, "runs"), exist_ok=True)
a0 = T.A0[FOOT]; AR = T.arrays(T.table(FOOT, UPS)); L0 = T.leaves(AR, a0); LS = 1e-6 if MODE == "mutate" else 1.0; rng = np.random.default_rng(20261102); N = len(AR["r"]); CI = {c: i for i, c in enumerate(T.CLS)}
PL = "M_b * (pi * x)"
def bases(A): G = dict(M_b=A["gb"], M_gas=np.maximum(A["gg"], 0.0), M_star=np.maximum(A["gs"], 0.0), M_bt=T.G * A["Mbt"] / A["r"] ** 2); return G
BN = ["M_b", "M_gas", "M_star", "M_bt"]; BG = bases(AR)
if MODE in ("planted", "mutate"):
    add = BG["M_b"] * math.pi * L0["x"]; AR["gobs"] = T.law(AR["gb"] + add, a0) * 10 ** (0.01 * rng.standard_normal(N))
S = (AR["c"] == CI["S"]) & AR["tr"]; idx = np.nonzero(S)[0]; sub = np.zeros(N, bool); sub[rng.choice(idx, 240, replace=False)] = True
FP = AR["tr"] & (~S | sub); FA = AR["tr"]; HO = ~AR["tr"]
if MODE == "shuf":
    tri = np.nonzero(AR["tr"])[0]; p = rng.permutation(tri)
    for k in L0: L0[k] = L0[k].copy(); L0[k][tri] = L0[k][p]
def lay(M):
    """gate index for a row mask"""
    y = {}; ii = np.nonzero(M)[0]; c = AR["c"][ii]; y["ii"] = ii
    for k in ("X", "S", "LT", "G3", "G6"): y[k] = np.nonzero(c == CI[k])[0]
    y["D"] = []; y["L"] = []
    for cl in T.DW.CLASSES:
        j = np.nonzero((c == CI["Dw"]) & (AR["sub"][ii] == cl))[0]
        if len(j) >= 2: y["D"].append((cl, j, 1.2533 * float(np.sqrt(np.mean(AR["err"][ii][j] ** 2))) / math.sqrt(len(j))))
    for n in sorted(set(AR["name"][ii][c == CI["L"]])):
        j = np.nonzero((c == CI["L"]) & (AR["name"][ii] == n))[0]; y["L"].append((n, j, float(np.sqrt(np.sum(AR["err"][ii][j] ** 2))) / len(j)))
    d0 = np.log10(AR["gobs"][ii] / T.law(AR["gb"][ii], a0)); y["law_s"] = float(np.sqrt(np.mean(d0[y["S"]] ** 2))) if len(y["S"]) else 1.0; return y
def gates(d, y):
    """d m x rows. dict of value/line arrays."""
    out = {}; x = d[:, y["X"]]; out["Xm"] = np.abs(x.mean(1)) / (0.05 * LS); out["Xr"] = np.sqrt((x * x).mean(1)) / (0.10 * LS)
    s = d[:, y["S"]]; out["Sr"] = np.sqrt((s * s).mean(1)) / (1.05 * y["law_s"] * LS); out["Sm"] = np.abs(np.median(s, 1)) / (0.03 * LS)
    out["LT"] = np.abs(np.median(d[:, y["LT"]], 1)) / (0.10 * LS)
    for k in ("G3", "G6"):
        g = d[:, y[k]]; se = g.std(1, ddof=1) / math.sqrt(g.shape[1]); out[k] = np.abs(g.mean(1)) / (2 * np.sqrt(se * se + 0.01) * LS)
    for cl, j, sd in y["D"]: out["D:" + cl] = np.abs(np.median(d[:, j], 1)) / (2 * sd * LS)
    for n, j, se in y["L"]: out["L:" + n] = np.abs(d[:, j].mean(1)) / (2 * math.hypot(se, 0.05) * LS)
    return out
GROUPS = {"X": ("Xm", "Xr"), "S": ("Sr", "Sm"), "LT": ("LT",), "G": ("G3", "G6"), "D": None, "L": None}
def gkeys(g, nm): return [k for k in g if k.startswith(nm + ":")] if GROUPS[nm] is None else list(GROUPS[nm])
def dmat(add, M): r = AR["gb"][M][None, :] + add; return np.log10(AR["gobs"][M][None, :] / T.law(r, a0))
# ---- pool
U = {"sqrt": np.sqrt, "log1p": np.log1p, "inv1p": lambda x: 1 / (1 + x), "sq": lambda x: x * x}; OP = {"+": np.add, "-": np.subtract, "*": np.multiply, "/": np.divide}
def ev(s, Lv): e = dict(Lv); e.update(sqrt=np.sqrt, log1p=np.log1p, inv1p=lambda x: 1 / (1 + x), sq=lambda x: x * x, pi=math.pi); return eval(s, {"__builtins__": {}}, e) * np.ones(N)
def closure():
    leaf = [(k, 1) for k in ("y_g", "y_s", "f", "ell", "mu", "x")] + [("1.0", 1), ("2.0", 1), ("0.5", 1), ("pi", 1)]; seen = set()
    def add(s, n, v, out):
        if not np.all(np.isfinite(v)) or np.max(np.abs(v)) > 1e30: return
        m = np.abs(v).max() + 1e-300; k = (np.round(v / m, 9).tobytes(), round(math.log(m), 6))
        if k in seen: return
        seen.add(k); out.append((s, n, v))
    fp = FP; L = []
    for s, n in leaf: add(s, n, ev(s, L0)[fp], L)
    sets = [L]; prev = L
    for lvl in (1, 2):
        new = []; pool = [t for st in sets for t in st]
        for s, n, v in prev:
            for u, fn in U.items(): add(f"{u}({s})", n + 1, fn(v), new)
        for s1, n1, v1 in prev:
            for s2, n2, v2 in pool:
                for o, fn in OP.items():
                    add(f"({s1}{o}{s2})", n1 + n2 + 1, fn(v1, v2), new)
                    if o in "-/": add(f"({s2}{o}{s1})", n1 + n2 + 1, fn(v2, v1), new)
            if len(new) > 4 * CAP: break
        new.sort(key=lambda t: (t[1], t[0])); sets.append(new); prev = new
    al = [t for st in sets for t in st]; al.sort(key=lambda t: (t[1], t[0])); return al[:CAP], len(al)
pool, ntot = closure(); PS = [t[0] for t in pool]; PV = np.array([t[2] for t in pool]); NP = len(PS); print(TAG, "pool", NP, "of", ntot, "rows FP", int(FP.sum()), flush=True)
yFP = lay(FP); YX = yFP["X"]; bgFP = {b: BG[b][FP] for b in BN}
ck = dict(next=0, exprs=0, precut=0, hits=[], gate_pass={}, top=[], drop={}, t=0.0)
if os.path.exists(OUTJ): ck = json.load(open(OUTJ))
stop = {"f": False}; signal.signal(signal.SIGTERM, lambda *a: stop.update(f=True))
def fullscore(g): return np.max(np.array(list(g.values())), axis=0)
def rec_top(name, val, gd):
    ck["top"].append([float(val), name, {k: float(v) for k, v in gd.items()}]); ck["top"] = sorted(ck["top"], key=lambda t: t[0])[:50]
def evalT(a, o, b, flip, base):
    return f"{base} * ({PS[b]} {o} {PS[a]})" if flip else f"{base} * ({PS[a]} {o} {PS[b]})"
t0 = time.time(); start_t = ck["t"]; end = LIM or NP
law_g = gates(np.log10(AR["gobs"][FP] / T.law(AR["gb"][FP], a0))[None, :], yFP); ck["law"] = {k: float(v[0]) for k, v in law_g.items()}
for a in range(ck["next"], end):
    if stop["f"] or start_t + time.time() - t0 > WALL: break
    full = a % 100 == 0
    for o, fn in OP.items():
        for flip in ((False, True) if o in "-/" else (False,)):
            Tm = fn(PV, PV[a][None, :]) if flip else fn(PV[a][None, :], PV)
            ok = np.all(np.isfinite(Tm), 1)
            for bn in BN:
                add = bgFP[bn][None, :] * Tm; okb = ok & np.all(add >= 0, 1); ck["exprs"] += int(ok.size)
                sel = np.nonzero(okb)[0]
                if not len(sel): continue
                dx = np.log10(AR["gobs"][FP][YX][None, :] / T.law(AR["gb"][FP][YX][None, :] + add[sel][:, YX], a0)); m = dx.mean(1); r = np.sqrt((dx * dx).mean(1))
                keep = sel[(np.abs(m) <= 0.30) & (r <= 0.35)] if not full else sel
                if not len(keep): continue
                ck["precut"] += int(len(keep)); dd = dmat(add[keep], FP); g = gates(dd, yFP); sc = fullscore(g)
                for nm in GROUPS:
                    ks = gkeys(g, nm)
                    if not ks: continue
                    pg = np.max(np.array([g[k] for k in ks]), 0) <= 1
                    if not full: continue
                    ck["gate_pass"][nm] = ck["gate_pass"].get(nm, 0) + int(pg.sum()); ks0 = [k for q in GROUPS if q != nm for k in gkeys(g, q)]; dr = np.max(np.array([g[k] for k in ks0]), 0); i = int(np.argmin(dr))
                    if nm not in ck["drop"] or dr[i] < ck["drop"][nm][0]:
                        b = int(keep[i]); ck["drop"][nm] = [float(dr[i]), evalT(a, o, b, flip, bn), {k: float(v[i]) for k, v in g.items()}]
                order = np.argsort(sc)[:3]
                for i in order:
                    if len(ck["top"]) < 50 or sc[i] < ck["top"][-1][0]:
                        rec_top(evalT(a, o, int(keep[i]), flip, bn), sc[i], {k: v[i] for k, v in g.items()})
                for i in np.nonzero(sc <= 1)[0]:
                    ck["hits"].append(evalT(a, o, int(keep[i]), flip, bn))
    ck["next"] = a + 1
    if a % 20 == 0:
        ck["t"] = start_t + time.time() - t0; json.dump(ck, open(OUTJ + ".tmp", "w")); os.replace(OUTJ + ".tmp", OUTJ); print(a, ck["exprs"], ck["precut"], len(ck["hits"]), round(ck["top"][0][0], 3) if ck["top"] else None, round(ck["t"]), flush=True)
ck["t"] = start_t + time.time() - t0; ck["pool_total"] = ntot; ck["pool"] = NP; ck["done"] = ck["next"] >= end; json.dump(ck, open(OUTJ, "w")); print("END", TAG, ck["next"], ck["exprs"], len(ck["hits"]), flush=True)
