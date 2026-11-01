#!/usr/bin/env python3
"""BR1 (FROZEN_CRITERIA.md): RC3 bar family against TP1's per-galaxy Upsilon. kappa = 1/2 FITTED, unused; not theory closed."""
import json, os, re, sys
import numpy as np
from scipy.stats import rankdata
H = os.path.dirname(os.path.abspath(__file__)); RT = os.path.join(H, "..", ".."); OUT = []
def P(s): print(s); OUT.append(s)
def norm(s):
    m = re.match(r"\s*(NGC|UGC|IC|DDO|ESO|UGCA|CGCG|MCG|PGC)\s*([0-9]+)(?:[- ]+G?\s*0*([0-9]+))?", s)
    if not m: return s.replace(" ", "").upper()
    return f"{m[1]}{int(m[2])}" + (f"-{int(m[3])}" if m[3] else "")
RC = {}
for l in open(os.path.join(RT, "_external_data", "br1_bars", "rc3.tsv")):
    p = l.rstrip("\n").split("\t")
    if len(p) < 4 or l.startswith("#") or p[0].startswith(("name", "---")): continue
    fam = p[2][1:3]; f = {"SA": "SA", "SB": "SB", "SX": "SAB"}.get(fam)
    for n in p[:2]:
        if n.strip(): RC.setdefault(norm(n), (f, p[2]))
J = json.load(open(os.path.join(H, "..", "TP1_trough_predictor", "tp1_results.json"))); G = []
for l in open(os.path.join(RT, "real_research", "data", "SPARC_Lelli2016c.mrt")):
    p = l.split()
    if len(p) < 18: continue
    try: t = dict(n=p[0], inc=float(p[5]), vf=float(p[15]), Q=int(p[17]))
    except ValueError: continue
    if p[0] in J["blum"] and t["vf"] > 0 and t["Q"] <= 2 and t["inc"] >= 30:
        r = RC.get(norm(p[0]), (None, "")); t.update(fam=r[0], rc3=r[1], ub=J["blum"][p[0]], uo=J["off"][p[0]]); G.append(t)
json.dump(G, open(os.path.join(H, "br1_matched.json"), "w"), indent=0)
BN = [(20, 60), (60, 100), (100, 150), (150, 200), (200, 250), (250, 400)]; P("Match, family known / n by bin: " + ", ".join(f"{a}-{b} {sum(1 for g in G if a <= g['vf'] < b and g['fam'])}/{sum(1 for g in G if a <= g['vf'] < b)}" for a, b in BN))
for n in ("NGC3198", "NGC2403", "NGC1300", "NGC2841", "NGC7331"): P(f"  spot {n}: {RC.get(norm(n))}")
rng = np.random.default_rng(20261101); arr = lambda L, k: np.array([g[k] for g in L])
def test(L, A, Bc, key, lab):
    a = [g for g in L if g["fam"] in A]; b = [g for g in L if g["fam"] in Bc]
    if not a or not b: P(f"{lab}: empty"); return None
    x, y = arr(a, key), arr(b, key); z = np.r_[x, y]; rk = rankdata(z); obs = rk[:len(x)].mean() - rk[len(x):].mean(); D = np.array([(lambda q: q[:len(x)].mean() - q[len(x):].mean())(rng.permutation(rk)) for _ in range(20000)]); p = float((np.sum(D >= obs) + 1) / 20001); g = np.median(x) - np.median(y); bs = np.median(x[rng.integers(0, len(x), (20000, len(x)))], axis=1) - np.median(y[rng.integers(0, len(y), (20000, len(y)))], axis=1); ci = np.percentile(bs, [2.5, 97.5])
    P(f"{lab}: barred n {len(x)} median {np.median(x):.2f} (at floor {np.mean(x <= .3):.2f}); other n {len(y)} median {np.median(y):.2f} (at floor {np.mean(y <= .3):.2f}); gap {g:+.3f} [{ci[0]:+.3f}, {ci[1]:+.3f}]; p {p:.4f}"); return dict(nb=len(x), no=len(y), gap=float(g), ci=ci.tolist(), p=p)
W = lambda a, b: [g for g in G if a <= g["vf"] < b]; R = {}
R["primary"] = test(W(150, 250), {"SB"}, {"SA"}, "ub", "PRIMARY 150-250 SB vs SA U_Blum")
test(W(150, 250), {"SB", "SAB"}, {"SA"}, "ub", "150-250 SB+SAB vs SA U_Blum"); test(W(150, 250), {"SB"}, {"SA"}, "uo", "150-250 SB vs SA U_off"); test(W(150, 250), {"SB"}, {"SAB", "SA"}, "ub", "150-250 SB vs SA+SAB U_Blum"); test(W(150, 200), {"SB"}, {"SA"}, "ub", "150-200"); test(W(200, 250), {"SB"}, {"SA"}, "ub", "200-250")
L = [g for g in W(100, 400) if g["fam"] in ("SB", "SA")]; lv = np.log10(arr(L, "vf")); u = rankdata(arr(L, "ub")); c = np.polyfit(lv, u, 1); ru = u - np.polyval(c, lv); fb = arr(L, "fam") == "SB"; o = ru[fb].mean() - ru[~fb].mean(); D = np.array([(lambda q: q[fb].mean() - q[~fb].mean())(rng.permutation(ru)) for _ in range(20000)]); P(f"100-400 at fixed lg V_flat, rank residual gap {o:+.2f}, one-sided p {(np.sum(D >= o) + 1) / 20001:.4f}, n {len(L)}")
m = dict(W(150, 250)[0]); pm = []; L = [g for g in W(150, 250) if g["fam"] in ("SB", "SA")]; rk = rankdata(arr(L, "ub")); fb = arr(L, "fam") == "SB"; obsn = []
for i in range(200):
    q = rng.permutation(fb); o = rk[q].mean() - rk[~q].mean(); D = np.array([(lambda s: s[q].mean() - s[~q].mean())(rng.permutation(rk)) for _ in range(500)]); pm.append((np.sum(D >= o) + 1) / 501)
P(f"MUTATE shuffled flags: p quartiles {np.percentile(pm, [25, 50, 75]).round(2).tolist()}")
r = R["primary"]; lab = "UNDERPOWERED" if r["nb"] < 5 or r["no"] < 5 else "BARS SEPARATE" if r["p"] < .05 and r["gap"] >= .05 else "BARS DON'T SEPARATE"; P("LABEL: " + lab); P("per galaxy 150-250: " + "; ".join(f"{g['n']} {g['fam']} {g['ub']:.2f}" for g in sorted(W(150, 250), key=lambda g: str(g["fam"]))))
open(os.path.join(H, "br1.out"), "w").write("\n".join(OUT) + "\n")
