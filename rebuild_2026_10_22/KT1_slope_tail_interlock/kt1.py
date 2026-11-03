#!/usr/bin/env python3
"""KT1: measure mu's deep slope n and tail exponent p apart on SPARC. See FROZEN_CRITERIA.md."""
import glob, json, math, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "../../real_research/data/sparc_data")
MUTATE = os.environ.get("KT1_MUTATE") == "1"
kpc, KMS = 3.0857e19, 1.0e3
c_l, G = 2.99792458e8, 6.674e-11
H0 = 67.4 * 1000 / 3.0857e22
rho_crit = 3 * H0**2 / (8 * math.pi * G)
S = {"rho_DE": c_l * math.sqrt(G * 0.685 * rho_crit), "rho_crit": c_l * math.sqrt(G * rho_crit)}
NS = np.round(np.arange(0.8, 4.0001, 0.1), 3)
PS = np.round(np.arange(0.5, 8.0001, 0.25), 3)
ND = 1000


def load(fu=1.0):
    gb, go, gal = [], [], []
    i = 0
    for fn in sorted(glob.glob(os.path.join(DATA, "*_rotmod.dat"))):
        try:
            d = np.genfromtxt(fn, comments="#")
        except Exception:
            continue
        if d.ndim != 2 or d.shape[1] < 6 or len(d) < 3:
            continue
        R, Vo, eV, Vg, Vd, Vb = (d[:, j] for j in range(6))
        m = (R > 0) & (Vo > 0) & (eV > 0) & (eV / Vo < 0.10)
        if m.sum() < 3:
            continue
        R, Vo, Vg, Vd, Vb = R[m], Vo[m], Vg[m], Vd[m], Vb[m]
        Vb2 = Vg * np.abs(Vg) + fu * 0.5 * Vd * np.abs(Vd) + fu * 0.7 * Vb * np.abs(Vb)
        ok = Vb2 > 0
        if ok.sum() < 3:
            continue
        r = R[ok] * kpc
        gb.append(Vb2[ok] * KMS**2 / r)
        go.append(Vo[ok] ** 2 * KMS**2 / r)
        gal.append(np.full(ok.sum(), i))
        i += 1
    return np.concatenate(gb), np.concatenate(go), np.concatenate(gal)


def g_pred(gb, s, n, p, it=70):
    lo = gb.copy()
    hi = gb * 10 + np.sqrt(gb * s / n) * 10 + 1e-13
    for _ in range(it):
        mid = 0.5 * (lo + hi)
        f = mid * (1 - (1 + n * mid / s / p) ** (-p)) - gb
        lo = np.where(f < 0, mid, lo)
        hi = np.where(f < 0, hi, mid)
    return 0.5 * (lo + hi)


def sse_table(gb, go, gal, s):
    """galaxy-by-grid mean squared log residual"""
    ng = gal.max() + 1
    cnt = np.bincount(gal, minlength=ng)
    T = np.zeros((len(NS), len(PS), ng))
    lg = np.log10(go)
    for i, n in enumerate(NS):
        for j, p in enumerate(PS):
            r = lg - np.log10(g_pred(gb, s, n, p))
            T[i, j] = np.bincount(gal, r**2, minlength=ng) / cnt
    return T


def best(T, w=None):
    M = T.mean(axis=2) if w is None else (T * w).sum(axis=2) / w.sum()
    i, j = np.unravel_index(np.argmin(M), M.shape)
    return i, j, M[i, j]


def boot(T, seed=20261102):
    rng = np.random.default_rng(seed)
    ng = T.shape[2]
    out = np.zeros((ND, 2))
    for d in range(ND):
        w = np.bincount(rng.integers(0, ng, ng), minlength=ng).astype(float)
        i, j, _ = best(T, w)
        out[d] = NS[i], PS[j]
    return out


def q(x, a, b):
    return [float(np.percentile(x, a)), float(np.percentile(x, b))]


def label(B):
    n95, p95, d95 = q(B[:, 0], 2.5, 97.5), q(B[:, 1], 2.5, 97.5), q(B[:, 0] - B[:, 1], 2.5, 97.5)
    if p95[0] <= PS[0] or p95[1] >= PS[-1] or (p95[0] <= 1 and p95[1] >= 4):
        return "TAIL NOT MEASURED"
    if not d95[0] <= 0 <= d95[1]:
        return "INTERLOCK BROKEN"
    if n95[0] <= 2 <= n95[1] and p95[0] <= 2 <= p95[1]:
        return "INTERLOCK HOLDS AT 2"
    return "INTERLOCK HOLDS, NOT AT 2"


def summary(tag, T, B):
    i, j, m = best(T)
    n68, p68 = q(B[:, 0], 16, 84), q(B[:, 1], 16, 84)
    n95, p95, d95 = q(B[:, 0], 2.5, 97.5), q(B[:, 1], 2.5, 97.5), q(B[:, 0] - B[:, 1], 2.5, 97.5)
    ii, jj = np.argmin(abs(NS - 2)), np.argmin(abs(PS - 2))
    print(f"{tag}: best n {NS[i]} p {PS[j]} rms {math.sqrt(m):.4f}; rms at (2,2) {math.sqrt(T[ii, jj].mean()):.4f}")
    print(f"   n 68% {n68} 95% {n95}; p 68% {p68} 95% {p95}; n-p 95% {d95}; kappa=1/n 68% [{1/n68[1]:.3f}, {1/n68[0]:.3f}]")
    print(f"   label {label(B)}")
    return dict(n=float(NS[i]), p=float(PS[j]), rms=math.sqrt(m), rms22=math.sqrt(T[ii, jj].mean()), n68=n68, n95=n95,
                p68=p68, p95=p95, d95=d95, label=label(B))


gb, go, gal = load()
print(f"loaded {gal.max()+1} galaxies, {len(gb)} points; Y=g/s max rho_DE {go.max()/S['rho_DE']:.1f}; N(Y>10) {(go/S['rho_DE']>10).sum()}")
res = {}
if MUTATE:
    rng = np.random.default_rng(7)
    T0 = sse_table(gb, go, gal, S["rho_DE"])
    Tm = sse_table(gb, rng.permutation(go), gal, S["rho_DE"])
    r0, rm = math.sqrt(best(T0)[2]), math.sqrt(best(Tm)[2])
    print(f"real best rms {r0:.4f}; shuffled best rms {rm:.4f}; {'MUTATE bites' if rm - r0 >= 0.1 else 'MUTATE FAILED'}")
    json.dump({"real": r0, "shuffled": rm}, open(os.path.join(HERE, "kt1_MUTATE.json"), "w"), indent=1)
    sys.exit(1)

# planted controls on real g_bar with the real residuals at each galaxy's point
planted_ok = True
s0 = S["rho_DE"]
scatter = np.log10(go) - np.log10(g_pred(gb, s0, 2.0, 2.0))
res["planted"] = {}
for pp in (2.0, 4.0):
    mock = g_pred(gb, s0, 2.0, pp) * 10 ** (scatter - scatter.mean())
    Tp = sse_table(gb, mock, gal, s0)
    Bp = boot(Tp)
    h = q(Bp[:, 1], 16, 84)
    hit = h[0] <= pp <= h[1]
    planted_ok &= hit
    print(f"PLANTED p={pp}: recovered p 68% {h}, n 68% {q(Bp[:,0],16,84)} {'PASS' if hit else 'FAIL'}")
    res["planted"][str(pp)] = dict(p68=h, hit=bool(hit))
print("Planted controls:", "PASS" if planted_ok else "FAIL, real run reads NO VERDICT")
for f, s in S.items():
    T = sse_table(gb, go, gal, s)
    res[f] = summary(f"PRIMARY {f}", T, boot(T))
    i = np.argmin(abs(PS - 2))
    print("   integer family n=p rms:", {k: round(math.sqrt(T[np.argmin(abs(NS-k)), np.argmin(abs(PS-k))].mean()), 4) for k in (1, 2, 3, 4)})
for fu in (0.8, 1.25):
    a, b, c = load(fu)
    for f, s in S.items():
        T = sse_table(a, b, c, s)
        res[f"U{fu}_{f}"] = summary(f"Upsilon x{fu} {f}", T, boot(T))
res["planted_ok"] = bool(planted_ok)
json.dump(res, open(os.path.join(HERE, "kt1.json"), "w"), indent=1)
sys.exit(0 if planted_ok else 2)
