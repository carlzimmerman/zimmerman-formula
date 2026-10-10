"""CFG588: ACE within-class colour clock. Criteria: FROZEN_CRITERIA.md (23fd031bc).
Executes cfg585_age.py's head (unedited). MUTATE: CFG588_MUTATE=1 shuffles delta-c within (class x mass quintile).
"""
import os, io, json, math, contextlib
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.dirname(HERE)
MUTATE = os.environ.get("CFG588_MUTATE", "0") == "1"
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
OLD585, YOUNG585 = ns["OLD"], ns["YOUNG"]

rng = np.random.default_rng(588)
GROUPS = []                                    # (class, tertile, mask, median dc)
for cls, t in (("early", 1), ("late", 0)):
    C = F30 & (TYP == t)
    qb = np.quantile(LMSL[C], np.linspace(0, 1, 6))
    dc = np.full(len(U), np.nan); qid = np.full(len(U), -1)
    for i in range(5):
        m = C & (LMSL >= qb[i]) & (LMSL <= qb[i + 1]); dc[m] = U[m] - np.median(U[m]); qid[m] = i
    if MUTATE:
        for i in range(5):
            m = C & (qid == i); dc[m] = rng.permutation(dc[m])
    t1, t2 = np.nanquantile(dc[C], [1 / 3, 2 / 3])
    for k, m in enumerate((C & (dc < t1), C & (dc >= t1) & (dc <= t2), C & (dc > t2))):
        GROUPS.append((cls, k, m, float(np.median(dc[m]))))

P("=" * 100)
P(f"CFG588  ACE within-class colour clock  {'*** MUTATE: dc shuffled within class x mass ***' if MUTATE else 'PRIMARY'}")
P("=" * 100)
for cls, k, m, d in GROUPS:
    P(f"  {cls:5s} tertile {k}: N {m.sum():6d}  median dc {d:+.3f}  median log M* {np.median(LMSL[m]):.3f}")
P("\n--- controls")
for cls in ("early", "late"):
    ms = [np.median(LMSL[m]) for c, k, m, d in GROUPS if c == cls]
    check(max(ms) - min(ms) < 0.05, f"C1 {cls} tertile median log M* spread {max(ms) - min(ms):.3f} (< 0.05)")
if not MUTATE:
    same = np.array_equal(GROUPS[2][2], OLD585) and np.array_equal(GROUPS[0][2], YOUNG585)
    P(f"  early top/bottom tertiles identical to CFG585 OLD/YOUNG masks: {same}")

HART = (NPATCH - 6 - 2) / (NPATCH - 1)
isE = np.array([1.0 if c == "early" else 0.0 for c, *_ in GROUPS]); dcv = np.array([d for *_, d in GROUPS])


def gls(y, Cv, X):
    W = np.linalg.inv(Cv); A = X.T @ W @ X; beta = np.linalg.solve(A, X.T @ W @ y); r = y - X @ beta
    return beta, float(r @ W @ r), np.linalg.inv(A)


res, calls = {}, {}
for c in CONS:
    for foot in FOOTS:
        Y = {b: [] for b in ("K9", "K-in")}; L = {b: [] for b in ("K9", "K-in")}
        for cls, k, m, d in GROUPS:
            dd, Cc, Lj = esd_loo(m); cp = comps(c, foot, m); fb = all_bands(dd, Cc, cp); mM = cp["moster"][0] + cp["moster"][1]
            for b in Y:
                Y[b].append(fb[b]["eps"]); L[b].append((Lj[:, BANDS[b]] - mM[BANDS[b]][None, :]) @ np.array(fb[b]["wvec"]))
        for b in ("K9", "K-in"):
            y = np.array(Y[b]); Lm = np.array(L[b]).T; dev = Lm - Lm.mean(0); Cv = (NPATCH - 1) / NPATCH * dev.T @ dev / HART
            X0 = np.column_stack([isE, 1 - isE]); X1 = np.column_stack([isE, 1 - isE, dcv]); X2 = np.column_stack([isE, 1 - isE, dcv * isE, dcv * (1 - isE)])
            b0, c0, _ = gls(y, Cv, X0); b1, c1, V1 = gls(y, Cv, X1); b2, c2, V2 = gls(y, Cv, X2)
            bE, bL = b2[2], b2[3]; sE, sL = math.sqrt(V2[2, 2]), math.sqrt(V2[3, 3]); sdiff = math.sqrt(V2[2, 2] + V2[3, 3] - 2 * V2[2, 3])
            key = f"{c}|{foot}|{b}"
            res[key] = dict(eps=y.tolist(), sig=np.sqrt(np.diag(Cv)).tolist(), chi2=[c0, c1, c2], b=b1[2], b_sig=math.sqrt(V1[2, 2]),
                            bE=bE, bE_sig=sE, bL=bL, bL_sig=sL, diff_sig=(bE - bL) / sdiff)
            if b == "K9":
                Zb, ZL, ZE = b1[2] / math.sqrt(V1[2, 2]), bL / sL, bE / sE
                if b1[2] > 0 and Zb >= 2 and bL > 0 and ZL >= 1 and abs((bE - bL) / sdiff) < 2:
                    call = "CLOCK IN BOTH CLASSES"
                elif bE > 0 and ZE >= 2 and ZL < 1:
                    call = "EARLY-ONLY CLOCK"
                elif abs(Zb) < 1:
                    call = "NO CLOCK"
                else:
                    call = "MIXED"
                calls[f"{c}|{foot}"] = call
            P(f"  [{c} {foot:9s}] {b:4s} eps early " + " ".join(f"{v:+.2f}" for v in y[:3]) + "  late " + " ".join(f"{v:+.2f}" for v in y[3:])
              + f" | common b {b1[2]:+.2f}+-{math.sqrt(V1[2, 2]):.2f} (Z {b1[2] / math.sqrt(V1[2, 2]):+.2f}); b_E {bE:+.2f}+-{sE:.2f}, b_L {bL:+.2f}+-{sL:.2f}"
              + (f" -> {calls[f'{c}|{foot}']}" if b == "K9" else ""))
if not MUTATE:
    r = res["A|canonical|K9"]["eps"]
    check(abs(r[2] - 1.197) < 0.005 and abs(r[0] - 0.256) < 0.005, f"C2 early top/bottom tertiles reproduce CFG585 OLD/YOUNG ({r[2]:+.3f} / {r[0]:+.3f})")
overall = list(calls.values())[0] if len(set(calls.values())) == 1 else "SPLIT"
P(f"\nVERDICT: {overall}   {calls}")
if MUTATE:
    zs = [res[f"{c}|{f}|K9"]["b"] / res[f"{c}|{f}|K9"]["b_sig"] for c in CONS for f in FOOTS]
    check(all(abs(z) < 2 for z in zs), f"MUTATE: common slope |Z| < 2 in every cell ({['%+.2f' % z for z in zs]})")
P(f"\nchecks: {sum(c for c, _ in CHECKS)}/{len(CHECKS)} pass")
json.dump(dict(verdict=overall, calls=calls, groups=[dict(cls=c, tertile=k, N=int(m.sum()), dc=d) for c, k, m, d in GROUPS], res=res, checks=CHECKS),
          open(os.path.join(HERE, f"cfg588_results{TAG}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg588_within{TAG}.out"), "w").write("\n".join(OUT) + "\n")
