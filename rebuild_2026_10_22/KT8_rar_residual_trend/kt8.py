#!/usr/bin/env python3
"""KT8: trend of SPARC residuals against OR mu_2. See FROZEN_CRITERIA.md."""
import glob, json, math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(HERE, "../../real_research/data/sparc_data")
MUT = os.environ.get("KT8_MUTATE") == "1"
ND = 2000
def load(fd=1.0, fb=1.0):
    o = []; i = 0
    for fn in sorted(glob.glob(os.path.join(D, "*_rotmod.dat"))):
        try: d = np.genfromtxt(fn, comments="#")
        except Exception: continue
        if d.ndim != 2 or d.shape[1] < 6 or len(d) < 3: continue
        R, V, e, Vg, Vd, Vb = (d[:, j] for j in range(6))
        m = (R > 0) & (V > 0) & (e > 0) & (e / V < .1)
        if m.sum() < 3: continue
        R, V, Vg, Vd, Vb = R[m], V[m], Vg[m], Vd[m], Vb[m]
        B = Vg * abs(Vg) + fd * .5 * Vd * abs(Vd) + fb * .7 * Vb * abs(Vb)
        k = B > 0
        if k.sum() < 3: continue
        r = R[k] * 3.0857e19
        o.append(np.c_[B[k] * 1e6 / r, V[k] ** 2 * 1e6 / r, np.full(k.sum(), i), np.full(k.sum(), float(np.any(Vb != 0)))]); i += 1
    return np.vstack(o)
def pred(gb, s):
    lo, hi = gb.copy(), gb * 10 + np.sqrt(gb * s) * 10
    for _ in range(70):
        mid = .5 * (lo + hi); f = mid * (1 - (1 + mid / s) ** -2.0) - gb
        lo, hi = np.where(f < 0, mid, lo), np.where(f < 0, hi, mid)
    return .5 * (lo + hi)
def groups(x, r, g):
    return [(x[g == u], r[g == u]) for u in np.unique(g)]
def fit_t1(G, idx):
    A = np.zeros((3, 3)); b = np.zeros(3)
    for i in idx:
        x, r = G[i]
        X = np.c_[np.ones_like(x), x, x * x]
        w = 1 / len(x)
        A += w * X.T @ X; b += w * X.T @ r
    return np.linalg.solve(A, b)
def fit_t2(G, idx):
    n = 0.; d = 0.
    for i in idx:
        x, r = G[i]
        xx, rr = x - x.mean(), r - r.mean()
        n += (xx * rr).sum(); d += (xx * xx).sum()
    return n / d
def run(x, r, g, seed=20261102, nd=ND):
    G = groups(x, r, g); ng = len(G); rng = np.random.default_rng(seed)
    t1, t2 = fit_t1(G, range(ng)), fit_t2(G, range(ng))
    B1, B2 = np.zeros((nd, 3)), np.zeros(nd)
    for d in range(nd):
        idx = rng.integers(0, ng, ng)
        B1[d], B2[d] = fit_t1(G, idx), fit_t2(G, idx)
    c = lambda a: [float(np.percentile(a, 2.5)), float(np.percentile(a, 97.5))]
    size = {str(v): float(np.mean([b[0] + b[1] * v + b[2] * v * v for b in [t1]])) for v in (-1.5, 0, 1.5)}
    return dict(ng=ng, c0=float(t1[0]), c1=float(t1[1]), c2=float(t1[2]), c0_95=c(B1[:, 0]), c1_95=c(B1[:, 1]), c2_95=c(B1[:, 2]), t2=float(t2), t2_95=c(B2), size=size)
def show(tag, q):
    print(f"{tag}: {q['ng']} gal; c0 {q['c0']:+.4f} {np.round(q['c0_95'],4)}; c1 {q['c1']:+.4f} {np.round(q['c1_95'],4)}; c2 {q['c2']:+.4f} {np.round(q['c2_95'],4)}; T2 {q['t2']:+.4f} {np.round(q['t2_95'],4)}; at x -1.5,0,1.5: {[round(v,3) for v in q['size'].values()]}", flush=True)
c, Gv = 2.99792458e8, 6.674e-11
rc = 3 * (67.4e3 / 3.0857e22) ** 2 / (8 * math.pi * Gv)
S = {"rho_DE": c * math.sqrt(Gv * .685 * rc), "rho_crit": c * math.sqrt(Gv * rc)}
a = load()
def res(a_, s): return np.log10(a_[:, 1]) - np.log10(pred(a_[:, 0], s))
xv = np.log10(a[:, 0]) + 10.5
if MUT:
    r0, r1 = res(a, S["rho_DE"]), res(a, S["rho_DE"] * 2)
    print("c0 normal", fit_t1(groups(xv, r0, a[:, 2]), range(155))[0], "a0 doubled", fit_t1(groups(xv, r1, a[:, 2]), range(155))[0])
    print("MUTATE bites" if fit_t1(groups(xv, r0, a[:, 2]), range(155))[0] - fit_t1(groups(xv, r1, a[:, 2]), range(155))[0] >= .1 else "MUTATE weak: a0 doubling lowers c0 by less than 0.1 dex")
    sys.exit(1)
out = {}
r = res(a, S["rho_DE"])
rng = np.random.default_rng(1)
sh = r.copy()
for u in np.unique(a[:, 2]):
    k = a[:, 2] == u; sh[k] = rng.permutation(r[k])
p0 = run(xv, sh, a[:, 2], nd=500); show("planted null", p0)
ok0 = p0["t2_95"][0] <= 0 <= p0["t2_95"][1]
p1 = run(xv, sh + .03 * xv, a[:, 2], nd=500); show("planted +0.03 x", p1)
ok1 = p1["t2_95"][0] <= .03 <= p1["t2_95"][1]
print("planted null", ok0, "planted trend", ok1)
out["planted"] = [bool(ok0), bool(ok1)]
for f, s in S.items():
    r = res(a, s)
    q = run(xv, r, a[:, 2]); show(f"PRIMARY {f}", q); out[f] = q
    k = a[:, 3] == 0
    q3 = run(xv[k], r[k], a[k, 2]); show(f"bulgeless {f}", q3); out[f + "_bulgeless"] = q3
    t2x = not (q["t2_95"][0] <= 0 <= q["t2_95"][1]); t2b = not (q3["t2_95"][0] <= 0 <= q3["t2_95"][1])
    t1x = not (q["c1_95"][0] <= 0 <= q["c1_95"][1]); c0x = not (q["c0_95"][0] <= 0 <= q["c0_95"][1])
    lab = "TREND" if t2x and t2b else "TREND, BULGE-DEPENDENT" if t2x else "OFFSET ONLY" if c0x and not t1x else "NONE" if not c0x and not t1x else "UNLISTED: T1 only"
    print(f"  LABEL {f}: {lab}"); out[f + "_label"] = lab
    for tag, fd, fb in (("U x0.8", .8, .8), ("U x1.25", 1.25, 1.25), ("bulge 0.5", 1, .5 / .7), ("bulge 1.0", 1, 1 / .7)):
        a2 = load(fd, fb); x2 = np.log10(a2[:, 0]) + 10.5
        q4 = run(x2, res(a2, s), a2[:, 2], nd=500); show(f"  {tag} {f}", q4); out[f"{tag}_{f}"] = q4
json.dump(out, open(os.path.join(HERE, "kt8.json"), "w"), indent=1)
