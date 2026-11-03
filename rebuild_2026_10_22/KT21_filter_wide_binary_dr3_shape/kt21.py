#!/usr/bin/env python3
"""KT21: DR3 inner wide-binary shape, plain QUMOND vs KT17's filter (eps 0.55) vs Newton. Q = ln median vtilde(2<=y<10) -
ln median vtilde(y>=10). python3 kt21.py [--mutate]. kappa = 1/2 FITTED and held fixed; not theory closed."""
import json, math, os, sys
import numpy as np
from scipy.special import erf
HERE = os.path.dirname(os.path.abspath(__file__)); MUT = "--mutate" in sys.argv; OUT = []; RES = {}; fail = 0
CSV = os.path.join(HERE, "../../real_research/data/widebinaries/dr3_extract/wide_binaries_dr3.csv")
def P(s): print(s, flush=True); OUT.append(s)
G, MS, AU = 6.6743e-11, 1.98892e30, 1.495978707e11; A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}; EPS = 0.55; SSYS = 0.020; K = 40
nu = (lambda y: np.ones_like(np.asarray(y, float))) if MUT else (lambda y: 0.5 + np.sqrt(0.25 + 1 / np.maximum(y, 1e-300)))
def gam(r, M, a0, ge, xi):
    """KT20's 1D external-field form; r in m, M in kg; xi 0 = plain."""
    gN = G * M / r ** 2
    if np.isscalar(xi) and xi <= 0: h = gN
    else: x = r / xi; h = gN * (erf(x / math.sqrt(2)) - math.sqrt(2 / math.pi) * x * np.exp(-x * x / 2))
    return (gN + (nu(np.sqrt(ge * ge + h * h) / a0) - 1) * h) / gN
d = np.genfromtxt(CSV, delimiter=",", names=True); s = d["sep_kAU"] * 1e3 * AU; M = (d["M1_msun"] + d["M2_msun"]) * MS; vp = d["v_perp_kms"] * 1e3
vt = vp / np.sqrt(G * M / s); n = len(s); P(f"pairs {n}, s {d['sep_kAU'].min():.2f}-{d['sep_kAU'].max():.2f} kAU, median M_tot {np.median(M / MS):.2f} Msun")
# C1 against KT20
k20 = json.load(open(os.path.join(HERE, "../KT20_filter_wide_binaries/kt20.json"))); e1 = 0.0
if not MUT:
    for foot, a0 in A0.items():
        for m in (1.0, 1.5):
            r = k20[f"{foot}|M{m}|ge1.9e-10"]; ss = np.array(r["s_kAU"]) * 1e3 * AU; xi = EPS * math.sqrt(G * m * MS / a0)
            e1 = max(e1, float(np.max(np.abs(gam(ss, m * MS, a0, 1.9e-10, 0.0) / np.array(r["gamma_plain"]) - 1))), float(np.max(np.abs(gam(ss, m * MS, a0, 1.9e-10, xi) / np.array(r["gamma_filter"]) - 1))))
    ok = e1 <= 1e-10; fail += not ok; P(f"C1 gamma vs KT20, max rel {e1:.1e}: {'PASS' if ok else 'FAIL'}")
def orbits(rng, alpha, m):
    e = rng.uniform(0, 1, m) ** (1 / (alpha + 1)); Mn = rng.uniform(0, 2 * math.pi, m); E = Mn.copy()
    for _ in range(60): E = E - (E - e * np.sin(E) - Mn) / (1 - e * np.cos(E))
    r = 1 - e * np.cos(E); x = np.cos(E) - e; y = np.sqrt(1 - e * e) * np.sin(E); vx = -np.sin(E) / r; vy = np.sqrt(1 - e * e) * np.cos(E) / r
    ci = rng.uniform(-1, 1, m); w = rng.uniform(0, 2 * math.pi, m)
    X = x * np.cos(w) - y * np.sin(w); Y = x * np.sin(w) + y * np.cos(w); VX = vx * np.cos(w) - vy * np.sin(w); VY = vx * np.sin(w) + vy * np.cos(w)
    rs = np.hypot(X, Y * ci); vs = np.hypot(VX, VY * ci); return rs, vs * np.sqrt(rs), r / rs   # r_sky, vtilde, r3d/r_sky
def Q(v, y): return math.log(np.median(v[(y >= 2) & (y < 10)])) - math.log(np.median(v[y >= 10]))
def preds(a0, ge, alpha, seed):
    rng = np.random.default_rng(seed); idx = np.repeat(np.arange(n), K); _, vN, ratio = orbits(rng, alpha, n * K)
    r3 = s[idx] * ratio; Mi = M[idx]; y = (G * M / (a0 * s * s))[idx]; xi = EPS * np.sqrt(G * Mi / a0); out = {}
    out["Newton"] = Q(vN, y); out["plain"] = Q(vN * np.sqrt(gam(r3, Mi, a0, ge, 0.0)), y); out["filter"] = Q(vN * np.sqrt(gam(r3, Mi, a0, ge, xi)), y)
    return out
for foot, a0 in A0.items():
    y = G * M / (a0 * s * s); nM, nH = int(np.sum((y >= 2) & (y < 10))), int(np.sum(y >= 10)); ok3 = min(nM, nH) >= 500; fail += not ok3
    qo = Q(vt, y); bs = []
    for seed in (11, 12):
        rng = np.random.default_rng(seed); b = []
        for _ in range(2000): i = rng.integers(0, n, n); b.append(Q(vt[i], y[i]))
        bs.append(float(np.std(b)))
    ok4 = abs(bs[1] / bs[0] - 1) <= 0.2; fail += not ok4; sig = math.sqrt(bs[0] ** 2 + SSYS ** 2)
    pr = preds(a0, 1.9e-10, 1.2, 2026110302); R = dict(n_M=nM, n_H=nH, Q_obs=qo, sigma_stat=bs[0], sigma_stat_seed2=bs[1], sigma=sig, med_M=float(np.median(vt[(y >= 2) & (y < 10)])), med_H=float(np.median(vt[y >= 10])), pred=pr)
    P(f"\n[{foot}] C3 bins M {nM}, H {nH}: {'PASS' if ok3 else 'FAIL'}; C4 sigma_stat {bs[0]:.4f} / {bs[1]:.4f}: {'PASS' if ok4 else 'FAIL'}")
    P(f"[{foot}] median vtilde M {R['med_M']:.4f}, H {R['med_H']:.4f}; Q_obs {qo:+.4f} +- {sig:.4f} (stat {bs[0]:.4f}, sys {SSYS})")
    if MUT: P(f"[{foot}] MUTATE Q_pred " + ", ".join(f"{k} {v:+.4f}" for k, v in pr.items())); RES[foot] = R; continue
    ok2 = abs(pr["Newton"]) <= 0.005; fail += not ok2; P(f"[{foot}] C2 Newton Q_pred {pr['Newton']:+.4f}: {'PASS' if ok2 else 'FAIL'}")
    lab = {}
    for k in ("Newton", "plain", "filter"):
        z = (qo - pr[k]) / sig; lab[k] = "CONSISTENT" if abs(z) <= 2 else "TENSION" if abs(z) <= 3 else "EXCLUDED"; R[f"z_{k}"] = z
        P(f"[{foot}] {k:7s} Q_pred {pr[k]:+.4f}  z {z:+.2f}  {lab[k]}")
    R["labels"] = lab; bes = {}
    for tag, ge, al in (("ge2.32e-10", 2.32e-10, 1.2), ("alpha1.0", 1.9e-10, 1.0), ("alpha1.4", 1.9e-10, 1.4)):
        p2 = preds(a0, ge, al, 2026110303); bes[tag] = {k: dict(Q_pred=v, z=(qo - v) / sig) for k, v in p2.items()}
        P(f"[{foot}] beside {tag}: " + "; ".join(f"{k} {v:+.4f} (z {(qo - v) / sig:+.2f})" for k, v in p2.items()))
    R["beside"] = bes; RES[foot] = R
if not MUT:
    L = [RES[f]["labels"] for f in A0]
    if all(l["plain"] == "EXCLUDED" and l["filter"] == "CONSISTENT" for l in L): h = "FILTER FAVOURED OVER PLAIN"
    elif all(l["filter"] == "EXCLUDED" and l["plain"] == "CONSISTENT" for l in L): h = "PLAIN FAVOURED OVER FILTER"
    elif all(l["plain"] == "CONSISTENT" and l["filter"] == "CONSISTENT" for l in L): h = "BOTH CONSISTENT"
    elif all(l["plain"] == "EXCLUDED" and l["filter"] == "EXCLUDED" for l in L): h = "BOTH EXCLUDED"
    else: h = "NO VERDICT"
    RES["headline"] = h; P(f"\nHEADLINE: {h}  (Newton: " + ", ".join(f"{f} {RES[f]['labels']['Newton']}" for f in A0) + ")")
RES["fail"] = fail; P(f"failed checks: {fail}")
sfx = "_MUTATE" if MUT else ""; open(os.path.join(HERE, f"kt21{sfx}.out"), "w").write("\n".join(OUT) + "\n"); json.dump(RES, open(os.path.join(HERE, f"kt21{sfx}.json"), "w"), indent=1)
sys.exit(1 if (MUT or fail) else 0)
