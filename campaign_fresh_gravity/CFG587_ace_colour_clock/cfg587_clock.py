"""CFG587: ACE first test — one colour clock or a class step? Criteria: FROZEN_CRITERIA.md (a15bbe272).
Executes cfg585_age.py's head (unedited; masks, colours, CFG531 estimator). MUTATE: CFG587_MUTATE=1 shuffles the colour
residual within (class x mass quintile).
"""
import os, io, json, math, contextlib
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.dirname(HERE)
MUTATE = os.environ.get("CFG587_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUTATE else ""
OUT, CHECKS = [], []


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)


def check(c, m):
    CHECKS.append((bool(c), m)); P(f"  [{'PASS' if c else 'FAIL'}] {m}"); return bool(c)


for v in ("CFG585_MUTATE", "CFG531_MUTATE"):
    os.environ.pop(v, None)
path = os.path.join(LANES, "CFG585_age_settling", "cfg585_age.py")
src = open(path).read()
ns = {"__file__": path, "__name__": "head"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src.split('P("=" * 100)')[0], path, "exec"), ns)
U, F30, TYP, LMSL, esd_loo, comps, all_bands, BANDS, CONS, FOOTS, NPATCH = (ns[k] for k in
    ("U", "F30", "TYP", "LMSL", "esd_loo", "comps", "all_bands", "BANDS", "CONS", "FOOTS", "NPATCH"))
OLD, YOUNG = ns["OLD"], ns["YOUNG"]

# colour residual at fixed mass over ALL f30 lenses
qb = np.quantile(LMSL[F30], np.linspace(0, 1, 6))
dc = np.full(len(U), np.nan); q = np.full(len(U), -1)
for i in range(5):
    m = F30 & (LMSL >= qb[i]) & (LMSL <= qb[i + 1]); dc[m] = U[m] - np.median(U[m]); q[m] = i
if MUTATE:
    rng = np.random.default_rng(587)
    for i in range(5):
        for t in (0, 1):
            m = F30 & (q == i) & (TYP == t); dc[m] = rng.permutation(dc[m])
edges = np.nanquantile(dc[F30], np.linspace(0, 1, 7)); edges[-1] += 1e-9
BINS = [F30 & (dc >= edges[k]) & (dc < edges[k + 1]) for k in range(6)]
dcb = np.array([np.median(dc[m]) for m in BINS]); fE = np.array([(TYP[m] == 1).mean() for m in BINS])

P("=" * 100)
P(f"CFG587  ACE first test: colour clock vs class step  {'*** MUTATE: colour shuffled within class x mass ***' if MUTATE else 'PRIMARY'}")
P("=" * 100)
for k, m in enumerate(BINS):
    P(f"  bin {k}: N {m.sum():6d}  median dc {dcb[k]:+.3f}  early fraction {fE[k]:.2f}  median log M* {np.median(LMSL[m]):.2f}")
P("\n--- controls")
check(sum(m.sum() for m in BINS) == F30.sum() and min(m.sum() for m in BINS) >= 8000, f"C1 bins partition f30 ({sum(m.sum() for m in BINS)} = {F30.sum()}), min N {min(m.sum() for m in BINS)}")


def eps_vec(c, foot):
    eps, loo = {b: [] for b in ("K9", "K-in")}, {b: [] for b in ("K9", "K-in")}
    for m in BINS:
        d, C, Lj = esd_loo(m); cp = comps(c, foot, m); fb = all_bands(d, C, cp)
        mM = cp["moster"][0] + cp["moster"][1]
        for b in eps:
            eps[b].append(fb[b]["eps"]); loo[b].append((Lj[:, BANDS[b]] - mM[BANDS[b]][None, :]) @ np.array(fb[b]["wvec"]))
    return {b: (np.array(eps[b]), np.array(loo[b]).T) for b in eps}


def gls(y, C, X):
    W = np.linalg.inv(C); beta = np.linalg.solve(X.T @ W @ X, X.T @ W @ y); r = y - X @ beta
    return beta, float(r @ W @ r), np.linalg.inv(X.T @ W @ X)


if not MUTATE:
    d, C, Lj = esd_loo(F30); cp = comps("A", "canonical", F30); e0 = all_bands(d, C, cp)["K9"]["eps"]
    check(abs(e0 - 0.385) < 0.005, f"C2 all-f30 eps(K9, A, canonical) {e0:+.4f} vs CFG531 base +0.3850")

HART = (NPATCH - 6 - 2) / (NPATCH - 1)
res, calls = {}, {}
P("\n--- per cell (K9 primary): eps by bin, then GLS chi2 (6 bins)")
for c in CONS:
    for foot in FOOTS:
        ev = eps_vec(c, foot)
        for b in ("K9", "K-in"):
            y, L = ev[b]
            dev = L - L.mean(0); Cv = (NPATCH - 1) / NPATCH * dev.T @ dev / HART
            X_ace = np.column_stack([np.ones(6), dcb]); X_step = np.column_stack([np.ones(6), fE]); X_both = np.column_stack([np.ones(6), dcb, fE])
            ba, ca, Va = gls(y, Cv, X_ace); bs, cs, _ = gls(y, Cv, X_step); bb, cb, _ = gls(y, Cv, X_both)
            key = f"{c}|{foot}|{b}"
            res[key] = dict(eps=y.tolist(), sig=np.sqrt(np.diag(Cv)).tolist(), chi2_ace=ca, chi2_step=cs, chi2_both=cb,
                            ace=dict(a=ba[0], b=ba[1], b_sig=math.sqrt(Va[1, 1])), step=dict(a=bs[0], delta=bs[1]))
            if b == "K9":
                call = ("ACE FAVOURED" if (cs - ca >= 4 and ca - cb < 4) else "STEP FAVOURED" if (ca - cs >= 4 and cs - cb < 4) else "UNDECIDED")
                calls[f"{c}|{foot}"] = call
                # P3(i): predicted old-young difference from the ACE slope at CFG585's dc medians
                pred = ba[1] * (np.median(dc[OLD]) - np.median(dc[YOUNG])) if not MUTATE else float("nan")
                res[key]["P3_pred_old_minus_young"] = pred
            P(f"  [{c} {foot:9s}] {b:4s} eps " + " ".join(f"{v:+.2f}" for v in y) + f" | chi2 ACE {ca:5.2f} STEP {cs:5.2f} BOTH {cb:5.2f}"
              + (f" | slope b {ba[1]:+.2f} +- {math.sqrt(Va[1, 1]):.2f} /mag -> {calls[f'{c}|{foot}']}" if b == "K9" else ""))
overall = list(calls.values())[0] if len(set(calls.values())) == 1 else "MIXED"
P(f"\nVERDICT: {overall}   {calls}")
if not MUTATE:
    r586 = json.load(open(os.path.join(LANES, "CFG586_age_environment", "cfg586_results.json")))["D_env"]
    P("\n--- P3(i): ACE-predicted OLD-YOUNG difference vs CFG586's measured D_env (K9)")
    for c in CONS:
        for foot in FOOTS:
            pr = res[f"{c}|{foot}|K9"]["P3_pred_old_minus_young"]; me = r586[f"{c}|{foot}|K9"]
            ok = abs(pr - me["D"]) <= 2 * me["sig"]
            P(f"  [{c} {foot:9s}] predicted {pr:+.3f}  measured {me['D']:+.3f} +- {me['sig']:.3f}  -> {'consistent' if ok else 'INCONSISTENT'}")
    P("\n--- declared variant (report only): log-age clock tau ~ 10^(dc / 1.0 mag)")
    for c in CONS[:1]:
        for foot in FOOTS:
            y = np.array(res[f"{c}|{foot}|K9"]["eps"]); ev = eps_vec(c, foot)["K9"]; L = ev[1]
            dev = L - L.mean(0); Cv = (NPATCH - 1) / NPATCH * dev.T @ dev / HART
            tau = 10 ** (dcb / 1.0); bt, ct, _ = gls(y, Cv, np.column_stack([np.ones(6), tau]))
            P(f"  [{c} {foot:9s}] chi2 log-age {ct:.2f} (ACE-linear {res[f'{c}|{foot}|K9']['chi2_ace']:.2f}, STEP {res[f'{c}|{foot}|K9']['chi2_step']:.2f})")
if MUTATE:
    check(all(v != "ACE FAVOURED" for v in calls.values()), f"MUTATE: ACE not FAVOURED in any cell ({calls})")
P(f"\nchecks: {sum(c for c, _ in CHECKS)}/{len(CHECKS)} pass")
json.dump(dict(verdict=overall, calls=calls, bins=dict(dc=dcb.tolist(), fE=fE.tolist(), N=[int(m.sum()) for m in BINS]), res=res, checks=CHECKS),
          open(os.path.join(HERE, f"cfg587_results{TAG}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg587_clock{TAG}.out"), "w").write("\n".join(OUT) + "\n")
