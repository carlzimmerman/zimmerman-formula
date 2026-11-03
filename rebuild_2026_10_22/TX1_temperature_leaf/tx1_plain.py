#!/usr/bin/env python3
"""TX1 plain question: at fixed mass, do T residuals predict law residuals across the 12? FROZEN_CRITERIA.md. python3 -I tx1_plain.py [--mutate]. --mutate permutes T across clusters: the slope must collapse and the known-identity row must fail. kappa = 1/2 FITTED; not theory closed."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tx1_lib import *
MUT = "--mutate" in sys.argv; XD = os.path.join(REPO, "real_research", "data", "xcop"); XS = (0.3, 0.5, 0.7); OUT = []; RES = {}
def P(s): print(s, flush=True); OUT.append(s)
def li(r, m, t): return float(10 ** np.interp(np.log10(t), np.log10(r), np.log10(m)))
def load():
    D = {}
    for n in NAMES12:
        with fits.open(os.path.join(XD, n, f"{n}_hydro_mass.fits")) as h: hm = h[1].data.copy(); r5 = h[1].header["R500"]; m5 = h[1].header.get("M500", tload()[n]["M500"])
        with fits.open(os.path.join(XD, n, f"{n}_fgas_profile.fits")) as h: ga = h[1].data.copy(); rg = h[1].header["R500"]
        st = None
        p = os.path.join(XD, n, f"{n}_mstar.fits")
        if os.path.exists(p):
            with fits.open(p) as h: st = h[2].data.copy()
        D[n] = dict(hm=hm, r5=float(r5), ga=ga, rg=float(rg), st=st, M500=tload()[n]["M500"])
    return D
D = load(); 
fs = {x: float(np.median([li(q["st"]["RADIUS"], q["st"][q["st"].names[1]], x * q["r5"]) / li(q["ga"]["RADIUS"] * q["rg"], q["ga"]["MGAS"], x * q["r5"]) for q in D.values() if q["st"] is not None])) for x in XS}; P("median M*/Mgas at x: " + str({k: round(v, 4) for k, v in fs.items()}))
def table(a0, sz=False):
    A = {x: [] for x in XS}; N = list(D)
    for n in N:
        q = D[n]
        for x in XS:
            r = x * q["r5"]; mh = li(q["hm"]["RADIUS"], q["hm"]["M_FORW"], r); mg = li(q["ga"]["RADIUS"] * q["rg"], q["ga"]["MGAS"], r); ms = li(q["st"]["RADIUS"], q["st"][q["st"].names[1]], r) if q["st"] is not None else fs[x] * mg; Mb = mg + ms; R = r * 1e3 * PC; gb = G * Mb * MS / R ** 2; ml = I1(gb, a0) * R ** 2 / G / MS; kt, et = T_at(n, r, sz); A[x].append((math.log10(mh / ml), math.log10(kt), math.log10(Mb), math.log10(q["M500"]), et / math.log(10)))
    return N, {x: np.array(v) for x, v in A.items()}
def fit(y, t, f, rng, nb=20000):
    """y vs residual t at fixed f; both residualised on f. Returns slope, bootstrap se, permutation p, joint Z_T Z_G."""
    def rs(a, b): p = np.polyfit(b, a, 1); return a - np.polyval(p, b)
    def sl(y_, t_, f_): ty = rs(t_, f_); yy = rs(y_, f_); return float((ty * yy).sum() / max((ty * ty).sum(), 1e-30))
    b = sl(y, t, f); n = len(y); ix = rng.integers(0, n, (4000, n)); bs = np.array([sl(y[i], t[i], f[i]) for i in ix if np.ptp(f[i]) > 0]); se = float(bs.std()); ty = rs(t, f); yy = rs(y, f); pm = np.array([(ty[rng.permutation(n)] * yy).sum() for _ in range(nb)]) / (ty * ty).sum(); p = float((np.abs(pm) >= abs(b)).mean())
    X = np.c_[np.ones(n), t, f]; XtX = np.linalg.inv(X.T @ X); c = XtX @ X.T @ y; s2 = ((y - X @ c) ** 2).sum() / (n - 3); e = np.sqrt(np.diag(XtX) * s2); return dict(b=b, se=se, p=p, Z=b / se, sd_t=float(ty.std()), r=float(np.corrcoef(ty, yy)[0, 1]), jT=float(c[1] / e[1]), jG=float(c[2] / e[2]), scat_y=float(yy.std()))
def label(o):
    if abs(o["b"]) / o["se"] < 3 or o["p"] > 0.01: return "PQ NONE"
    return "PQ IDENTITY" if abs(o["b"] - 1) < 2 * o["se"] else "PQ BEYOND IDENTITY"
for foot, a0 in A0S.items():
    RES[foot] = {}
    for sz, tg in ((False, "X-ray"), (True, "SZ x>=0.5, X-ray inside")):
        N, A = table(a0, sz); rng = np.random.default_rng(20261102); mean = np.mean([A[x] for x in XS], axis=0); rows = {f"x{x}": A[x] for x in XS}; rows["mean"] = mean
        for nm, a in rows.items():
            t = a[:, 1].copy()
            if MUT: t = t[np.random.default_rng(7).permutation(len(t))]
            for ft, f in (("M_b", a[:, 2]), ("M500", a[:, 3])):
                o = fit(a[:, 0], t, f, rng); o["label"] = label(o); RES[foot][f"{tg}|{nm}|{ft}"] = o; P(f"{foot} {tg} {nm} fixed {ft}: b {o['b']:+.2f} +- {o['se']:.2f} Z {o['Z']:+.2f} perm p {o['p']:.4f} r {o['r']:+.2f} sd(t) {o['sd_t']:.3f} sd(y|f) {o['scat_y']:.3f} joint Z_T {o['jT']:+.2f} Z_G {o['jG']:+.2f} {o['label']}")
    if not sz: pass
# mean T error next to scatter, per cluster rows
_, A = table(A0S["canonical"]); P("median T stat error dex " + " ".join(f"x{x} {np.median(A[x][:,4]):.4f}" for x in XS))
# identity known answer: at fixed gas a pure M = c T relation planted in y must return slope 1
rg = np.random.default_rng(3); a = np.mean([A[x] for x in XS], axis=0); y_id = a[:, 1] - np.polyval(np.polyfit(a[:, 2], a[:, 1], 1), a[:, 2]) + 0.0 * a[:, 2]; t_id = a[:, 1][np.random.default_rng(7).permutation(12)] if MUT else a[:, 1]; o = fit(y_id, t_id, a[:, 2], rg, 2000); ok = abs(o["b"] - 1) < 1e-6; P(f"[{'PASS' if ok else 'FAIL'}] K identity plant slope {o['b']:.6f}, label {label(o) if o['se'] > 0 else 'exact'}")
tg = "_MUTATE" if MUT else ""; open(os.path.join(LANE, f"tx1_plain{tg}.out"), "w").write("\n".join(OUT) + "\n"); json.dump(RES, open(os.path.join(LANE, f"tx1_plain{tg}.json"), "w"), indent=0); sys.exit(0 if ok else 1)
