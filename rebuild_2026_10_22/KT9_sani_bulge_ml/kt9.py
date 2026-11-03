#!/usr/bin/env python3
"""KT9: KT8's trend with a per-galaxy bulge Upsilon from Sani et al. 2011. See FROZEN_CRITERIA.md."""
import glob, json, math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(HERE, "../../real_research/data/sparc_data")
MUT = os.environ.get("KT9_MUTATE") == "1"
ND = 2000
GN, MSUN, KPC = 6.674e-11, 1.989e30, 3.0857e19
def sani(L, slope=1.18):
    return 10 ** (11.04 + slope * (math.log10(L) - 11)) / L
def galaxies():
    o = []
    for fn in sorted(glob.glob(os.path.join(D, "*_rotmod.dat"))):
        try: d = np.genfromtxt(fn, comments="#")
        except Exception: continue
        if d.ndim != 2 or d.shape[1] < 6 or len(d) < 3: continue
        o.append((os.path.basename(fn), d))
    return o
GAL = galaxies()
def load(ub):
    """ub(L) gives bulge Upsilon"""
    o, Ls = [], []; i = 0
    for name, d in GAL:
        R0, V0, e0, Vg0, Vd0, Vb0 = (d[:, j] for j in range(6))
        L = (Vb0[R0 > 0][-1] * 1e3) ** 2 * R0[R0 > 0][-1] * KPC / GN / MSUN if np.any(Vb0 != 0) else 0.0
        U = ub(L) if L > 0 else 0.7
        m = (R0 > 0) & (V0 > 0) & (e0 > 0) & (e0 / V0 < .1)
        if m.sum() < 3: continue
        R, V, Vg, Vd, Vb = R0[m], V0[m], Vg0[m], Vd0[m], Vb0[m]
        B = Vg * abs(Vg) + .5 * Vd * abs(Vd) + U * Vb * abs(Vb)
        k = B > 0
        if k.sum() < 3: continue
        r = R[k] * KPC
        o.append(np.c_[B[k] * 1e6 / r, V[k] ** 2 * 1e6 / r, np.full(k.sum(), i), np.full(k.sum(), float(L > 0))])
        if L > 0: Ls.append((name.replace("_rotmod.dat", ""), L, U))
        i += 1
    return np.vstack(o), Ls
def pred(gb, s):
    lo, hi = gb.copy(), gb * 10 + np.sqrt(gb * s) * 10
    for _ in range(70):
        mid = .5 * (lo + hi); f = mid * (1 - (1 + mid / s) ** -2.0) - gb
        lo, hi = np.where(f < 0, mid, lo), np.where(f < 0, hi, mid)
    return .5 * (lo + hi)
def groups(x, r, g): return [(x[g == u], r[g == u]) for u in np.unique(g)]
def t1(G, idx):
    A = np.zeros((2, 2)); b = np.zeros(2)
    for i in idx:
        x, r = G[i]; X = np.c_[np.ones_like(x), x]; w = 1 / len(x)
        A += w * X.T @ X; b += w * X.T @ r
    return np.linalg.solve(A, b)
def t2(G, idx):
    n = d = 0.
    for i in idx:
        x, r = G[i]; xx, rr = x - x.mean(), r - r.mean()
        n += (xx * rr).sum(); d += (xx * xx).sum()
    return n / d
def run(x, r, g, nd=ND):
    G = groups(x, r, g); ng = len(G); rng = np.random.default_rng(20261102)
    B1, B2 = np.zeros((nd, 2)), np.zeros(nd)
    for k in range(nd):
        idx = rng.integers(0, ng, ng); B1[k], B2[k] = t1(G, idx), t2(G, idx)
    c = lambda a: [round(float(np.percentile(a, 2.5)), 4), round(float(np.percentile(a, 97.5)), 4)]
    a_ = t1(G, range(ng))
    rms = math.sqrt(np.mean([np.mean(rr**2) for _, rr in G]))
    return dict(ng=ng, c0=float(a_[0]), c0_95=c(B1[:, 0]), c1=float(a_[1]), c1_95=c(B1[:, 1]), t2=float(t2(G, range(ng))), t2_95=c(B2), rms=rms)
c, Gv = 2.99792458e8, 6.674e-11
rc = 3 * (67.4e3 / 3.0857e22) ** 2 / (8 * math.pi * Gv)
S = {"rho_DE": c * math.sqrt(Gv * .685 * rc), "rho_crit": c * math.sqrt(Gv * rc)}
_, L0 = load(sani)
Ls = np.array([l for _, l, _ in L0]); Us = np.array([u for _, _, u in L0])
med = float(np.median(Us))
print(f"{len(L0)} bulge galaxies in sample; L {Ls.min():.2e} to {Ls.max():.2e}, median {np.median(Ls):.2e}; Sani Upsilon {Us.min():.2f} to {Us.max():.2f}, median {med:.3f}")
for n_, l, u in sorted(L0, key=lambda t: t[1]):
    print(f"   {n_:10s} L {l:.2e} U {u:.2f}")
rows = {"A Sani k5": sani, "B Sani k3": lambda L: .6 * sani(L), "C Sani k8/3": lambda L: (8 / 3 / 5) * sani(L), "D constant median": lambda L: med, "E 0.7": lambda L: .7}
if MUT:
    rows = {"MUT slope 0.82": lambda L: sani(L, .82), "A Sani k5": sani, "D constant median": lambda L: med}
out = {}
for f, s in S.items():
    for nm, ub in rows.items():
        a, _ = load(ub)
        x = np.log10(a[:, 0]) + 10.5
        r = np.log10(a[:, 1]) - np.log10(pred(a[:, 0], s))
        q = run(x, r, a[:, 2], nd=500 if MUT else ND)
        k = a[:, 3] == 1
        qb = run(x[k], r[k], a[k, 2], nd=500 if MUT else ND)
        print(f"{f} {nm}: c0 {q['c0']:+.4f} {q['c0_95']}; c1 {q['c1']:+.4f} {q['c1_95']}; T2 {q['t2']:+.4f} {q['t2_95']}; bulge gals T2 {qb['t2']:+.4f} {qb['t2_95']}; rms {q['rms']:.4f}", flush=True)
        out[f"{f}|{nm}"] = dict(all=q, bulge=qb)
    if MUT:
        print(f"{f}: MUT - D {out[f+'|MUT slope 0.82']['all']['t2']-out[f+'|D constant median']['all']['t2']:+.4f}; A - D {out[f+'|A Sani k5']['all']['t2']-out[f+'|D constant median']['all']['t2']:+.4f}")
        continue
    A, E = out[f + "|A Sani k5"]["all"], out[f + "|E 0.7"]["all"]
    inc = A["t2_95"][0] <= 0 <= A["t2_95"][1]
    lab = "SANI REMOVES IT" if inc and abs(A["t2"]) <= .5 * abs(E["t2"]) else "SANI WORSENS IT" if abs(A["t2"]) > abs(E["t2"]) and not inc else "NOT REMOVED"
    print(f"  LABEL {f}: {lab}"); out[f + "|label"] = lab
if MUT: sys.exit(1)
json.dump(dict(rows=out, bulges=[(n_, l, u) for n_, l, u in L0], median=med), open(os.path.join(HERE, "kt9.json"), "w"), indent=1)
