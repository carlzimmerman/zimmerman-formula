#!/usr/bin/env python3
"""BT1 read, per FROZEN_CRITERIA.md. BT1_MUTATE=1 shuffles F, exit 1. kappa = 1/2 FITTED, unused; not theory closed."""
import json, os, re, sys
import numpy as np
H = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(H); MUT = os.environ.get("BT1_MUTATE") == "1"; OUT = []
def P(s): print(s); OUT.append(s)
R = json.load(open(os.path.join(H, "bt1_RUN_results.json"))); N3 = json.load(open(os.path.join(RB, "NR3_ur1_on_nr2", "nr3_MEDIAN_results.json")))["runs"]["EM1|blum"]["sparc"]; TG = list(R["U"]["blum"])
S = {}
for l in open(os.path.join(RB, "..", "real_research", "data", "s4g_morph_buta2015_cvrhs.tsv")):
    p = l.split("\t")
    if len(p) >= 6 and p[0].strip() and not l.startswith(("#", "Name", "-")) and p[4].strip():
        try: S[re.sub(r"\s+", "", p[0])] = float(p[4])
        except ValueError: pass
def F(n): return S.get(n, S.get(re.sub(r"^(NGC|UGC|IC|ESO|DDO|PGC)0*", r"\1", n)))
tb = R["tb"]; good = lambda n: n in tb and tb[n]["Q"] <= 2 and tb[n]["inc"] >= 30
def band(l, h, ref=R["U"]["blum"][TG[0]]): return [n for n in ref if good(n) and l <= tb[n]["vf"] < h]
FS = {n: F(n) for n in band(150, 250) + band(100, 150) + band(250, 400)}; F0 = dict(FS)
if MUT:
    k = sorted(FS); v = [FS[n] for n in k]; np.random.default_rng(1).shuffle(v); FS = dict(zip(k, v))
FL = 0.30 + 1e-9
def split(U, names, lo, hi, tag):
    a = np.array([U[n] for n in names if FS[n] is not None and lo(FS[n])]); b = np.array([U[n] for n in names if FS[n] is not None and hi(FS[n])])
    if len(a) < 1 or len(b) < 1: P(f"  {tag}: n {len(a)}, {len(b)}; too few"); return dict(na=len(a), nb=len(b))
    obs = abs(np.median(a) - np.median(b)); rg = np.random.default_rng(20261101); c = np.r_[a, b]; hit = 0
    for _ in range(20000):
        rg.shuffle(c); hit += abs(np.median(c[:len(a)]) - np.median(c[len(a):])) >= obs - 1e-12
    p = (hit + 1) / 20001; P(f"  {tag}: unbarred n {len(a)} median {np.median(a):.2f} at floor {(a <= FL).sum()}; barred n {len(b)} median {np.median(b):.2f} at floor {(b <= FL).sum()}; p {p:.3f}")
    return dict(na=len(a), nb=len(b), ma=float(np.median(a)), mb=float(np.median(b)), p=p)
lo = lambda x: x < 0.5; hi = lambda x: x >= 0.5; st = lambda x: x > 0.5; G = {}
for m in ("blum", "off"):
    for t in TG:
        U = R["U"][m][t]; nm = band(150, 250, U); P(f"\n{m}, {t}")
        G[f"{m}|{t}"] = split(U, nm, lo, hi, "150-250 primary F<0.5 vs F>=0.5"); split(U, nm, lo, st, "150-250 strict F<0.5 vs F>0.5")
        split(U, band(150, 200, U), lo, hi, "150-200"); split(U, band(200, 250, U), lo, hi, "200-250"); split(U, band(100, 150, U), lo, hi, "100-150 (reported)"); split(U, band(250, 400, U), lo, hi, "250-400 (reported)")
def lab(g): return "BAR-CARRIED MISS" if g["ma"] >= 0.50 and g["mb"] < 0.40 and g["p"] < 0.05 else "UNBARRED SHARE THE MISS" if g["ma"] < 0.40 else "NOT SEPARATED"
LA = [lab(G[f"blum|{t}"]) for t in TG]; L = LA[0] if len(set(LA)) == 1 else "NOT SEPARATED (A, B differ: " + ", ".join(LA) + ")"
U = R["U"]["blum"][TG[0]]; k1 = all(abs(np.median([U[n] for n in band(l, h, U)]) - N3[TG[0]]["bins"][f"{l}-{h}"]) <= 1e-6 for l, h in ((150, 200), (200, 250)))
nb = band(150, 250, U); k2 = len(nb) == 43 and sum(F0[n] is not None for n in nb) == 23 and all(abs((FS[n] or 0) - (F0[n] or 0)) < 1e-12 for n in nb); k3 = all(x is None or 0 <= x <= 1 for x in F0.values())
P("\nunclassified in band, not imputed: " + ", ".join(n for n in nb if F0[n] is None)); P(f"\n=== LABEL: {L}\nK1 {k1}; K2 {k2}; K3 {k3}")
open(os.path.join(H, "bt1_MUTATE.out" if MUT else "bt1.out"), "w").write("\n".join(OUT) + "\n"); sys.exit(0 if k1 and k2 and k3 else 1)
