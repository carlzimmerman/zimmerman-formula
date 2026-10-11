"""CFG589: ACE late-type colour clock at exactly matched mass. Criteria: FROZEN_CRITERIA.md (939124651).
Executes cfg585_age.py's head (unedited). MUTATE: CFG589_MUTATE=1 shuffles delta-c within (class x mass bin).
"""
import os, io, json, math, contextlib
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.dirname(HERE)
MUTATE = os.environ.get("CFG589_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUTATE else ""
OUT, CHECKS = [], []


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)


def check(c, m):
    CHECKS.append((bool(c), m)); P(f"  [{'PASS' if c else 'FAIL'}] {m}"); return bool(c)


for v in ("CFG585_MUTATE", "CFG531_MUTATE"):
    os.environ.pop(v, None)
path = os.path.join(LANES, "CFG585_age_settling", "cfg585_age.py")
ns = {"__file__": path, "__name__": "head"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(open(path).read().split('P("=" * 100)')[0], path, "exec"), ns)
U, F30, TYP, LMSL, esd_loo, comps, all_bands, BANDS, CONS, FOOTS, NPATCH = (ns[k] for k in
    ("U", "F30", "TYP", "LMSL", "esd_loo", "comps", "all_bands", "BANDS", "CONS", "FOOTS", "NPATCH"))

rng = np.random.default_rng(589)
GROUPS = {}
for cls, t in (("early", 1), ("late", 0)):
    C = F30 & (TYP == t)
    qb = np.quantile(LMSL[C], np.linspace(0, 1, 11)); qb[-1] += 1e-9
    ter = np.full(len(U), -1); dcs = np.full(len(U), np.nan)
    for i in range(10):
        idx = np.where(C & (LMSL >= qb[i]) & (LMSL < qb[i + 1]))[0]
        dc = U[idx] - np.median(U[idx])
        if MUTATE:
            dc = rng.permutation(dc)
        dcs[idx] = dc
        o = np.argsort(dc, kind="stable"); n = len(idx)
        for k in range(3):
            ter[idx[o[k * n // 3:(k + 1) * n // 3]]] = k
    GROUPS[cls] = [(ter == k) & C for k in range(3)], [float(np.median(dcs[(ter == k) & C])) for k in range(3)]

P("=" * 100)
P(f"CFG589  late-type colour clock at matched mass (stratified tertiles)  {'*** MUTATE: dc shuffled within class x mass bin ***' if MUTATE else 'PRIMARY'}")
P("=" * 100)
P("\n--- groups and C1")
for cls in ("early", "late"):
    masks, dmed = GROUPS[cls]
    ms = [np.median(LMSL[m]) for m in masks]
    for k, m in enumerate(masks):
        P(f"  {cls:5s} tertile {k}: N {m.sum():6d}  median dc {dmed[k]:+.3f}  median log M* {ms[k]:.3f}")
    check(max(ms) - min(ms) < 0.02, f"C1 {cls} tertile median log M* spread {max(ms) - min(ms):.3f} (< 0.02)")

HART3 = (NPATCH - 3 - 2) / (NPATCH - 1); HART6 = (NPATCH - 6 - 2) / (NPATCH - 1)


def gls(y, Cv, X):
    W = np.linalg.inv(Cv); A = X.T @ W @ X; beta = np.linalg.solve(A, X.T @ W @ y)
    return beta, np.linalg.inv(A)


res, calls = {}, {}
for c in CONS:
    for foot in FOOTS:
        Y = {b: [] for b in ("K9", "K-in")}; L = {b: [] for b in ("K9", "K-in")}
        for cls in ("early", "late"):
            for m in GROUPS[cls][0]:
                dd, Cc, Lj = esd_loo(m); cp = comps(c, foot, m); fb = all_bands(dd, Cc, cp); mM = cp["moster"][0] + cp["moster"][1]
                for b in Y:
                    Y[b].append(fb[b]["eps"]); L[b].append((Lj[:, BANDS[b]] - mM[BANDS[b]][None, :]) @ np.array(fb[b]["wvec"]))
        for b in ("K9", "K-in"):
            y = np.array(Y[b]); Lm = np.array(L[b]).T; dev = Lm - Lm.mean(0)
            C6 = (NPATCH - 1) / NPATCH * dev.T @ dev
            out = {}
            for j, cls in enumerate(("early", "late")):
                sl = slice(3 * j, 3 * j + 3); d = np.array(GROUPS[cls][1])
                bb, V = gls(y[sl], C6[sl, sl] / HART3, np.column_stack([np.ones(3), d]))
                out[cls] = (bb[1], math.sqrt(V[1, 1]))
            dE, dL = np.array(GROUPS["early"][1]), np.array(GROUPS["late"][1])
            X = np.zeros((6, 4)); X[:3, 0] = 1; X[3:, 1] = 1; X[:3, 2] = dE; X[3:, 3] = dL
            bj, Vj = gls(y, C6 / HART6, X)
            zdiff = (bj[2] - bj[3]) / math.sqrt(Vj[2, 2] + Vj[3, 3] - 2 * Vj[2, 3])
            key = f"{c}|{foot}|{b}"
            res[key] = dict(eps=y.tolist(), bE=out["early"][0], bE_sig=out["early"][1], bL=out["late"][0], bL_sig=out["late"][1], zdiff=zdiff)
            zE, zL = out["early"][0] / out["early"][1], out["late"][0] / out["late"][1]
            if b == "K9":
                if out["late"][0] > 0 and zL >= 2:
                    call = "SAME CLOCK IN LATE TYPES" if abs(zdiff) < 2 else "LATE CLOCK, DIFFERENT SLOPE"
                elif zL < 1 and zdiff >= 2:
                    call = "NO LATE CLOCK"
                else:
                    call = "UNDECIDED"
                calls[f"{c}|{foot}"] = call
            P(f"  [{c} {foot:9s}] {b:4s} early " + " ".join(f"{v:+.2f}" for v in y[:3]) + "  late " + " ".join(f"{v:+.2f}" for v in y[3:])
              + f" | b_E {out['early'][0]:+.2f}+-{out['early'][1]:.2f} (Z {zE:+.2f})  b_L {out['late'][0]:+.2f}+-{out['late'][1]:.2f} (Z {zL:+.2f})"
              + f"  diff {zdiff:+.2f}s" + (f" -> {calls[f'{c}|{foot}']}" if b == "K9" else ""))
zE_all = [res[f"{c}|{f}|K9"]["bE"] / res[f"{c}|{f}|K9"]["bE_sig"] for c in CONS for f in FOOTS]
if not MUTATE:
    check(all(z >= 2 for z in zE_all), f"C2 early slope Z >= 2 in every cell ({['%+.2f' % z for z in zE_all]})")
overall = list(calls.values())[0] if len(set(calls.values())) == 1 else "SPLIT"
P(f"\nVERDICT: {overall}   {calls}")
if MUTATE:
    zL_all = [res[f"{c}|{f}|K9"]["bL"] / res[f"{c}|{f}|K9"]["bL_sig"] for c in CONS for f in FOOTS]
    check(all(abs(z) < 2 for z in zL_all), f"MUTATE: late slope |Z| < 2 in every cell ({['%+.2f' % z for z in zL_all]})")
P(f"\nchecks: {sum(c for c, _ in CHECKS)}/{len(CHECKS)} pass")
json.dump(dict(verdict=overall, calls=calls, res=res, groups={k: dict(N=[int(m.sum()) for m in v[0]], dc=v[1]) for k, v in GROUPS.items()}, checks=CHECKS),
          open(os.path.join(HERE, f"cfg589_results{TAG}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg589_late{TAG}.out"), "w").write("\n".join(OUT) + "\n")
