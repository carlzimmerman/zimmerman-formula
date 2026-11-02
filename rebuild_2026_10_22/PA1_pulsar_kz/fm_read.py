#!/usr/bin/env python3
"""PA1 A1 stage 2: forward model labels. python3 -I fm_read.py [--post]. Footings never pooled. kappa = 1/2 FITTED; not theory closed."""
import sys, os, json, math
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, H); import fm_lib as FL
import numpy as np
from scipy.optimize import minimize_scalar, minimize
R0 = FL.R0; K1 = 66.4; KE = 2.2; O = []; RES = {}
def P(s): O.append(s); print(s)
def design(s, nuis):
    R, z, n, x, y = FL.geom(s["l"], s["b"], s["d"])
    X = np.c_[n[:, 0], n[:, 1], n[:, 2], np.abs(z) * n[:, 2]] if nuis == "N1" else np.zeros((len(z), 0))
    return X, R, z, n, x, y
def wls(y, m, X, v):
    r = y - m
    if X.shape[1] == 0: return r
    w = 1 / np.sqrt(v); c = np.linalg.lstsq(X * w[:, None], r * w, rcond=None)[0]; return r - X @ c
def gaussL(y, m, X, e):
    def f(ls):
        v = e ** 2 + math.exp(2 * ls); r = wls(y, m, X, v); return 0.5 * np.sum(r ** 2 / v + np.log(v))
    q = min(((f(a), a) for a in np.linspace(-5, 3, 17)))[1]
    o = minimize_scalar(f, bounds=(q - .5, q + .5), method="bounded", options=dict(xatol=1e-5))
    return -o.fun, math.exp(o.x)
def lorL(y, m, X):
    def f(p):
        xi = math.exp(p[-1]); r = y - m - (X @ p[:-1] if X.shape[1] else 0); return np.sum(np.log1p(r ** 2 / xi ** 2)) + len(y) * math.log(math.pi * xi)
    c0 = np.linalg.lstsq(X, y - m, rcond=None)[0] if X.shape[1] else np.zeros(0)
    o = minimize(f, np.r_[c0, 0.3], method="Nelder-Mead", options=dict(maxiter=2500, xatol=1e-4, fatol=1e-6)); return -o.fun
def losm(cf, form, s, off, n_cat, x, y, n):
    """cf row, form key; off: offset of this sample in the combined position list; last entry = Sun."""
    aR = np.array(cf[form][0]); az = np.array(cf[form][1]); N = len(x); return FL.alos(aR[off:off + N], az[off:off + N], aR[-1], az[-1], x, y, n)
def lam(y, cf, form, s, off, X, x, Yg, n, e, sc):
    """K_est: lambda on the vertical field. model = radial part + lam*vertical part."""
    aR = np.array(cf[form][0]); az = np.array(cf[form][1]); N = len(x); m0 = FL.alos(aR[off:off + N], 0 * x, aR[-1], 0.0, x, Yg, n); mz = (az[off:off + N] - az[-1]) * n[:, 2]
    v = e ** 2 + sc ** 2; w = 1 / np.sqrt(v); A = np.c_[mz, X] * w[:, None]; c, *_ = np.linalg.lstsq(A, (y - m0) * w, rcond=None); C = np.linalg.inv(A.T @ A); return float(c[0]), float(math.sqrt(C[0, 0]))
def label(dls, dlor, jk, power):
    dls = np.array(dls); med = float(np.median(np.abs(dls))); same = (dls > 0).all() or (dls < 0).all()
    sgn = np.sign(np.median(dls))
    if abs(dls).min() >= 9 and same and np.sign(dlor) == sgn and np.abs(jk).min() >= 9 and (np.array(jk) * sgn > 0).all() and power >= 0.5: return "SEPARATED"
    return "LEAN" if med >= 4 else "NOT SEPARATED"
def run(foot, sample, nuis, y_mod=None, plant=None, rng=None, tag="", npow=200):
    s = FL.load(sample); bn = len(FL.load("binary")["y"]); off = 0 if sample == "binary" else bn
    X, R, z, n, x, Yg = design(s, nuis); y = s["y"].copy(); e = s["e"].copy()
    if y_mod == "shuffle": p = rng.permutation(len(y)); y = y[p]; e = e[p]
    rows = [json.loads(l) for l in open(os.path.join(H, "cache", f"field_{foot}.jsonl"))]
    dA, dQ, sA, sR, K = [], [], [], [], {f: [] for f in "AQR"}; LA = []
    for c in rows:
        ma = losm(c, "A", s, off, 0, x, Yg, n); mr = losm(c, "R", s, off, 0, x, Yg, n); mq = losm(c, "Q", s, off, 0, x, Yg, n)
        yy = y; ee = e
        if plant is not None: ee = e / 20; yy = ma + plant.normal(0, ee)
        la, ssa = gaussL(yy, ma, X, ee); lr, ssr = gaussL(yy, mr, X, ee); lq, _ = gaussL(yy, mq, X, ee)
        dA.append(2 * (la - lr)); dQ.append(2 * (lq - lr)); sA.append(ssa); sR.append(ssr); LA.append(la)
        for f, kk, sc in (("A", c["KA"], ssa), ("Q", c["KQ"], ssa), ("R", c["KR"], ssr)):
            l_, se = lam(yy, c, f, s, off, X, x, Yg, n, ee, sc); K[f].append((l_ * kk, se * kk))
    dA = np.array(dA); im = int(np.argsort(dA)[len(dA) // 2]); c = rows[im]
    ma = losm(c, "A", s, off, 0, x, Yg, n); mr = losm(c, "R", s, off, 0, x, Yg, n)
    yy = y; ee = e
    if plant is not None: ee = e / 20; yy = ma + plant.normal(0, ee)
    # Lorentzian at the median cell
    dl = 2 * (lorL(yy, ma, X) - lorL(yy, mr, X))
    jk = []
    for i in range(len(y)):
        k = np.arange(len(y)) != i; jk.append(2 * (gaussL(yy[k], ma[k], X[k], ee[k])[0] - gaussL(yy[k], mr[k], X[k], ee[k])[0]))
    # mock power at the median cell
    r2 = np.random.default_rng(20261102); pw = {}
    for f, mt, sg, sc in (("A", ma, +1, sA[im]), ("R", mr, -1, sR[im])):
        hits = 0; ds = []
        for _ in range(npow):
            ym = mt + r2.normal(0, np.sqrt(ee ** 2 + sc ** 2)); d = 2 * (gaussL(ym, ma, X, ee)[0] - gaussL(ym, mr, X, ee)[0]); ds.append(d); hits += d * sg >= 9
        pw[f] = dict(power=hits / max(npow, 1), med=float(np.median(ds)) if ds else 0.0)
    p = min(pw["A"]["power"], pw["R"]["power"]) if npow else 0
    lab = label(dA, dl, jk, p)
    KS = {f: dict(med=float(np.median([a for a, _ in K[f]])), lo=float(min(a for a, _ in K[f])), hi=float(max(a for a, _ in K[f])), err=float(np.median([b for _, b in K[f]]))) for f in K}
    for f in KS: KS[f]["Z_line"] = (KS[f]["med"] - K1) / math.hypot(KS[f]["err"], KE); KS[f]["tension"] = "TENSION" if abs(KS[f]["Z_line"]) >= 3 else "NO TENSION"
    res = dict(n=len(y), cells=len(rows), dL_med=float(np.median(dA)), dL_min=float(dA.min()), dL_max=float(dA.max()), dLQ_med=float(np.median(dQ)), s_A=float(np.median(sA)), s_R=float(np.median(sR)), dL_lor=float(dl), jk_lo=float(min(jk)), jk_hi=float(max(jk)), power=pw, label=lab, K=KS, lnL_A_med=float(np.median(LA)))
    P(f"{tag}[{foot}] {sample} {nuis}: n {len(y)}, cells {len(rows)}; dL A-R med {res['dL_med']:+.2f} [{res['dL_min']:+.2f},{res['dL_max']:+.2f}], Q-R med {res['dLQ_med']:+.2f}, Lor {dl:+.2f}, jk [{min(jk):+.2f},{max(jk):+.2f}], s {res['s_A']:.2f}/{res['s_R']:.2f}; power A {pw['A']['power']:.3f} (med {pw['A']['med']:+.1f}) R {pw['R']['power']:.3f} (med {pw['R']['med']:+.1f}); {lab}")
    for f in "AQR": P(f"    K_est form {f}: {KS[f]['med']:.1f} [{KS[f]['lo']:.1f},{KS[f]['hi']:.1f}] +- {KS[f]['err']:.1f}; Z vs 66.4 {KS[f]['Z_line']:+.2f} {KS[f]['tension']}")
    return res
# checks
def check_geom():
    rng = np.random.default_rng(1); l = rng.uniform(0, 360, 200); b = rng.uniform(-80, 80, 200); d = rng.uniform(.1, 3, 200); V, al = 233., 3000.; R, z, n, x, y = FL.geom(l, b, d)
    C = (1 / (3.0856775814913673e19)) * 1e6 / (1e-3 / (365.25 * 86400)); aR = -V ** 2 / R * C; az = -al / 1.02271 ** 2 * z * C; m = FL.alos(aR, az, -V ** 2 / R0 * C, 0.0, x, y, n)
    L, B = np.radians(l), np.radians(b); beta = d / R0 * np.cos(B) - np.cos(L); an = -np.cos(B) * (V ** 2 / R0) * C * (np.cos(L) + beta / (np.sin(L) ** 2 + beta ** 2)) - al / 1.02271 ** 2 * C * z * np.sin(B)
    return float(np.max(np.abs(m - an)))
g = check_geom(); P(f"CHECK geometry vs textbook planar formula, max |d| {g:.2e} mm/s/yr: {'PASS' if g < 1e-6 else 'FAIL'}"); RES["geom"] = g
import csv
wr = []
for r in csv.DictReader(open(os.path.join(H, "data", "binary_only.csv"), newline="")):
    try: v = (float(r["PBDOT"]) - float(r["PBDOT_SHK"]) - float(r["PBDOT_GR"] or 0)) / (float(r["PB"]) * 86400) * 299792458 / (1e-3 / (365.25 * 86400)); wr.append((abs(v - float(r["ALOS_PB"])) / float(r["ALOS_PB_ERR"]), r["NAME"], v, float(r["ALOS_PB"])))
    except (ValueError, TypeError): pass
wr.sort(reverse=True); P(f"CHECK ALOS_PB recomputed, n {len(wr)}, worst |d|/err {wr[0][0]:.3f} ({wr[0][1]}), ratio median v/ALOS {np.median([a[2] / a[3] for a in wr]):.3f}"); RES["alos_worst"] = wr[0][:2]
s = FL.load("binary"); X, R, z, n, x, Yg = design(s, "N0"); rc = json.loads(open(os.path.join(H, "cache", "field_canonical.jsonl")).readline()); mA = losm(rc, "A", s, 0, 0, x, Yg, n); cc = float(np.corrcoef(mA, s["y"])[0, 1]); P(f"CHECK sign: corr(data, form A) binary N0 {cc:+.3f}: {'PASS' if cc > 0 else 'FAIL'}"); RES["corr"] = cc
for f in ("canonical", "alt"):
    Fd = json.load(open(os.path.join(H, f"fm_field_{f}.json"))); rs = [json.loads(l) for l in open(os.path.join(H, "cache", f"field_{f}.jsonl"))]
    da = max(abs(r["KA"] - r["c"]) for r in rs); dr = max(abs(r["KR"] - r["cR"]) for r in rs); ch = abs(Fd["KA_mut"] / Fd["KN"] - 1)
    P(f"CHECK [{f}] UX5 K(1.1): A {da:.4f}, R {dr:.4f}; AQUAL nu->1, density x 1e8: K {Fd['KA_mut']:.3f} vs Newton {Fd['KN']:.3f}, frac {ch:.2e}, cached A {Fd['KA_cached']:.2f}, res {Fd['res']:.1e}: {'PASS' if ch < 0.005 else 'FAIL'}"); RES[f"mutA_{f}"] = Fd
# primary and reported runs
for foot in ("canonical", "alt"):
    RES[foot] = {}
    for sm, nu in (("binary", "N1"), ("binary", "N0"), ("all", "N1"), ("all", "N0")):
        RES[foot][f"{sm}_{nu}"] = run(foot, sm, nu, npow=200 if nu == "N1" else 50)
ov = "DECIDED" if all(RES[f]["binary_N1"]["label"] == "SEPARATED" for f in ("canonical", "alt")) and np.sign(RES["canonical"]["binary_N1"]["dL_med"]) == np.sign(RES["alt"]["binary_N1"]["dL_med"]) else "CANNOT DECIDE"
P(f"OVERALL: {ov}"); RES["overall"] = ov
# MUTATE
for foot in ("canonical", "alt"):
    r = run(foot, "binary", "N1", y_mod="shuffle", rng=np.random.default_rng(7), tag="MUTATE shuffle ", npow=0)
    real = RES[foot]["binary_N1"]["K"]["A"]["med"]; sh = r["K"]["A"]; ok = abs(sh["med"]) <= 0.5 * abs(real) or abs(sh["med"]) / sh["err"] < 2
    P(f"  shuffle K_est A {sh['med']:.1f} +- {sh['err']:.1f} vs real {real:.1f}: {'PASS' if ok else 'FAIL'}"); RES[f"shuffle_{foot}"] = dict(ok=bool(ok), r=r)
    r = run(foot, "binary", "N1", plant=np.random.default_rng(11), tag="MUTATE plant A err/20 ", npow=30)
    P(f"  plant label {r['label']}: {'PASS' if r['label'] == 'SEPARATED' else 'FAIL'}"); RES[f"plant_{foot}"] = r
open(os.path.join(H, "fm_read.out"), "w").write("\n".join(O) + "\n"); json.dump(RES, open(os.path.join(H, "fm_read.json"), "w"), indent=1, sort_keys=True, default=float)
