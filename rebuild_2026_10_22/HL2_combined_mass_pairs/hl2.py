#!/usr/bin/env python3
"""HL2 (FROZEN_CRITERIA.md, AMENDMENT_A1.md): every usable published M_WL, M_hydro pair, one count per cluster. LITERATURE-INPUT bracket, never a framework grade.
    python3 -I hl2.py [--mutate]   kappa = 1/2 FITTED; not theory closed."""
import json, math, os, re, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); EX = os.path.join(os.path.dirname(RB), "_external_data"); H2 = os.path.join(EX, "hl2"); MUT = "--mutate" in sys.argv; OUT = []
def P(s): print(s, flush=True); OUT.append(s)
def num(c):
    m = re.search(r"-?\d+\.?\d*", c.replace("$", "")); return float(m.group()) if m and "nodata" not in c else float("nan")
def norm(n):
    n = n.upper().replace("ABELL", "A").replace("(SOUTH)", "S").replace("(NORTH)", "N").replace("~", " ").replace("\\", ""); n = re.sub(r"\$.*?\$", "-", n); n = re.sub(r"[^A-Z0-9]", "", n); n = re.sub(r"^A0+", "A", n); n = re.sub(r"^ZW(CL)?", "Z", n); n = re.sub(r"^RXC?J", "RX", n); return n
def texrows(p): return [l for l in open(p) if "&" in l and "\\\\" in l and "colhead" not in l and "multicolumn" not in l and not l.lstrip().startswith("%")]
S = {}; SKIP = []
# Mahdavi+13
D = os.path.join(EX, "gs4", "mahdavi13", "x"); ZZ = {l.split("&")[0].strip(): num(l.split("&")[3]) for l in texrows(os.path.join(D, "table1.tex")) if len(l.split("&")) > 3}
A = []
for l in texrows(os.path.join(D, "table2.tex")):
    c = l.split("&"); a = [num(c[i]) for i in (1, 2, 3, 4)]
    if all(np.isfinite(a)) and min(a) > 0: A.append(dict(n=norm(c[0]), raw=c[0].strip(), z=ZZ[c[0].strip()], r=a[0], mw=a[1], mg=a[2], mh=a[3]))
S["Mahdavi+13"] = A
# Okabe & Smith 16, corrected table, M500 column by header
T = open(os.path.join(H2, "okabe16", "x", "tab-mass-corr.tex")).read(); hd = T[T.index("Name"):]; cols = re.findall(r"\$M_\{?([^$}]+?)\}?\$", hd[:hd.index("\\\\")]); i500 = cols.index("500") + 1; OK = {}
def okrows(f):
    t = open(os.path.join(H2, "okabe16", "x", f)).read(); t = t[t.rindex("\\hline", 0, t.index("ABELL")) + 6:t.index("\\end{tabular")]; return [c.split("&") for c in t.split("\\\\") if "&" in c and "hline" not in c]
for c in okrows("tab-mass-corr.tex"):
    if len(c) > i500 and re.search(r"\d", c[i500]): OK[norm(c[0])] = (num(c[i500]) / 0.7, c[0].strip())
ZO = {norm(c[0]): num(c[1]) for c in okrows("tab-sample.tex")}
# Martino+14, PDF tables 2, 3
L = open(os.path.join(H2, "martino14", "paper.txt")).read().split("\n"); i2 = [i for i, x in enumerate(L) if x.strip().startswith("Table 2. Hydrostatic")][0]; i3 = [i for i, x in enumerate(L) if x.strip().startswith("Table 3. Gas mass")][0]; MA = {}; MG = {}; TOK = r"(x|\d+\.\d+\s*±\s*\d+\.\d+)"
for l in L[i2:i3]:
    m = re.match(r"\s*([A-Za-z][\w\s\-\+\.−]*?)\s{2,}(\d\.\d\d)\s+(\d\.\d\d)\s+(\d\.\d\d)\s+(.*)", l)
    if not m: continue
    t = re.findall(TOK, m.group(5))
    if len(t) == 6: MA[norm(m.group(1))] = dict(raw=m.group(1).strip(), r=float(m.group(4)), c=t[2], x=t[5])
for l in L[i3:i3 + 90]:
    m = re.match(r"\s*([A-Za-z][\w\s\-\+\.−]*?)\s{2,}(.*)", l); t = re.findall(TOK, m.group(2)) if m else []
    if len(t) == 6: MG[norm(m.group(1))] = (t[2], t[5])
v = lambda t: float("nan") if t == "x" else float(t.split("±")[0]); A = []; m2 = []
for k, q in MA.items():
    use = "c" if np.isfinite(v(q["c"])) else "x"; mh = v(q[use])
    if not np.isfinite(mh) or mh <= 0: SKIP.append(("Martino+14", q["raw"], "no mass")); continue
    m2.append((q["r"], mh, k))
    if k not in OK: SKIP.append(("Okabe+Martino", q["raw"], "no Okabe M500")); continue
    gm = MG.get(k); mg = v(gm[0 if use == "c" else 1]) if gm else float("nan"); A.append(dict(n=k, raw=q["raw"], z=ZO.get(k, float("nan")), mw=OK[k][0], mh=mh, mg=mg, r=q["r"]))
S["Okabe16+Martino14"] = A
# Zhang+10, r500^WL columns
Tz = open(os.path.join(H2, "zhang10", "x", "ms.tex")).read().split("\n"); iz = [i for i, x in enumerate(Tz) if "Cluster mass measurements" in x][0]; A = []
for l in Tz[iz:iz + 24]:
    if "\\end{tabular" in l: break
    c = l.split("&")
    if len(c) == 10 and re.search(r"\d", c[7]) and "Cluster" not in c[0]: A.append(dict(n=norm(c[0]), raw=c[0].strip(), z=float("nan"), mw=num(c[7]), mh=num(c[8]), mg=num(c[9].replace("\\\\", ""))))
S["Zhang+10"] = A
for k, a in S.items(): P(f"{k}: {len(a)} pairs")
P(f"Martino parsed: table 2 {len(MA)}, table 3 {len(MG)}; Okabe M500 {len(OK)}"); P("skipped: " + "; ".join(f"{a}: {b} ({c})" for a, b, c in SKIP))
okk = True
# K1
H0 = 70e3 / 3.0857e22; G = 6.674e-11
def k1(z, r, m): rc = 3 * H0 ** 2 * (0.3 * (1 + z) ** 3 + 0.7) / (8 * math.pi * G); d = 500 * rc * 4 / 3 * math.pi * (r * 3.0857e22) ** 3 / 1.989e44 / m - 1; return float(np.median(d)), float(np.percentile(d, 84) - np.percentile(d, 16))
a = S["Mahdavi+13"]; o, w = k1(np.array([q["z"] for q in a]), np.array([q["r"] for q in a]), np.array([q["mw"] for q in a])); P(f"K1 Mahdavi M_WL: offset {o:+.4f}, width {w:.4f}: {'PASS' if abs(o) <= 0.05 and w <= 0.03 else 'FAIL'} (HL1's AMENDMENT_A1)")
DROP = set(); a = [(ZO[k], r, m) for r, m, k in m2 if k in ZO and np.isfinite(ZO[k])]; o, w = k1(np.array([q[0] for q in a]), np.array([q[1] for q in a]), np.array([q[2] for q in a])); g_ = abs(o) <= 0.05 and w <= 0.03; P(f"K1 Martino M_hydro, n {len(a)}: offset {o:+.4f}, width {w:.4f}: {'PASS' if g_ else 'FAIL'}")
if not g_: DROP.add("Okabe16+Martino14")
# K3
LH = np.array([math.log10(q["mw"] / q["mh"]) for q in S["Mahdavi+13"]]); HL = json.load(open(os.path.join(RB, "HL1_lensing_vs_hydrostatic_pairs", "hl1_results.json"))); g_ = abs(float(np.median(LH)) - HL["g"]) < 1e-9; okk &= g_; P(f"K3 Mahdavi alone reproduces HL1's g: {np.median(LH):+.4f}: {'PASS' if g_ else 'FAIL'}")
g_ = len(S["Okabe16+Martino14"]) >= 30 and len(S["Zhang+10"]) >= 10 and len(MA) >= 40; okk &= g_; P(f"K2 parse: {'PASS' if g_ else 'FAIL'}")
if not okk: P("K FAILED: no verdict"); open(os.path.join(HERE, "hl2.out"), "w").write("\n".join(OUT) + "\n"); sys.exit(1)
# K4 agreement per pair of sources, same mass
K = list(S)
for i in range(3):
    for j in range(i + 1, 3):
        a = {q["n"]: q for q in S[K[i]]}; b = {q["n"]: q for q in S[K[j]]}; c = sorted(set(a) & set(b))
        if c:
            dw = [math.log10(a[n]["mw"] / b[n]["mw"]) for n in c]; dh = [math.log10(a[n]["mh"] / b[n]["mh"]) for n in c]; P(f"K4 {K[i]} vs {K[j]}: n {len(c)}, M_WL median {np.median(dw):+.3f} (|d| {np.median(np.abs(dw)):.3f}), M_hydro median {np.median(dh):+.3f} (|d| {np.median(np.abs(dh)):.3f})" + (" FLAG" if abs(np.median(dw)) > .1 or abs(np.median(dh)) > .1 else ""))
def bs(x, seed=1):
    r = np.random.default_rng([20261031, seed]); return float(np.std([np.median(x[r.integers(0, len(x), len(x))]) for _ in range(5000)], ddof=1))
def cl(g, s): return "NOT POWERED" if s > 0.04 else "NO GAP" if abs(g) <= 2 * s else "REVERSED" if g < -2 * s else "GAP AS LARGE" if abs(g - 0.12) <= 2 * s else "GAP SMALLER" if g + 2 * s < 0.12 else "GAP LARGER"
def combine(srcs, off=0.0):
    u = {}
    for k in srcs:
        for q in S[k]:
            x = math.log10(q["mw"] / q["mh"]) + (off if k == "Mahdavi+13" else 0); u.setdefault(q["n"], []).append(x)
    return {k: float(np.mean(v)) for k, v in u.items()}
USE = [k for k in S if k not in DROP]; U = combine(USE); L_ = np.array(list(U.values())); g = float(np.median(L_)); s = bs(L_); C = cl(g, s)
if MUT:
    a = np.array(list({k: -v for k, v in U.items()}.values())); P(f"MUTATE swap flips g: {'BITES' if abs(np.median(a) + g) < 1e-12 else 'FAIL'}")
    mw = np.array([q["mw"] for k in USE for q in S[k]]); mh = np.array([q["mh"] for k in USE for q in S[k]]); x = np.log10(mw / mh); y = np.log10(mw / np.random.default_rng(1).permutation(mh)); P(f"MUTATE shuffle rms {x.std():.3f} -> {y.std():.3f}: {'BITES' if y.std() > x.std() else 'FAIL'}"); open(os.path.join(HERE, "hl2_MUTATE.out"), "w").write("\n".join(OUT) + "\n"); sys.exit(0)
P(f"g over {len(L_)} unique clusters: {g:+.3f} +- {s:.3f}, mean {L_.mean():+.3f}, rms {L_.std():.3f}: {C}")
tags = []; drops = {}
for k in USE:
    r = [q for q in USE if q != k]; x = np.array(list(combine(r).values())); drops[k] = (float(np.median(x)), bs(x), cl(float(np.median(x)), bs(x)), len(x)); P(f"  drop {k}: n {len(x)}, g {drops[k][0]:+.3f} +- {drops[k][1]:.3f}: {drops[k][2]}")
if any(v[2] != C for v in drops.values()): tags.append("[SOURCE-DEPENDENT]")
oc = {cl(float(np.median(list(combine(USE, o_).values()))), s) for o_ in (-.014, .014)} | {C}
if len(oc) > 1: tags.append("[OFFSET-DEPENDENT]")
P(f"VERDICT, conditional on HL1's AMENDMENT_A1: {C} {' '.join(tags)}")
for k in USE:
    x = np.array([math.log10(q["mw"] / q["mh"]) for q in S[k]]); P(f"  {k}: n {len(x)}, g {np.median(x):+.3f} +- {bs(x):.3f}, mean {x.mean():+.3f}")
    yy = [(math.log10(q["mg"] * 1.034 / q["mw"] / .15945), math.log10(q["mg"] * 1.034 / q["mh"] / .15945)) for q in S[k] if np.isfinite(q["mg"]) and q["mg"] > 0]
    if yy: yy = np.array(yy); P(f"    f* 0.034, n {len(yy)}: log Y_WL {np.median(yy[:, 0]):+.3f} +- {bs(yy[:, 0]):.3f}, log Y_hyd {np.median(yy[:, 1]):+.3f} +- {bs(yy[:, 1]):.3f}")
zz = {}; 
for k in USE:
    for q in S[k]:
        if np.isfinite(q["z"]): zz[q["n"]] = q["z"]
mhm = {}
for k in USE:
    for q in S[k]: mhm.setdefault(q["n"], []).append(q["mh"])
n_ = [k for k in U if k in zz]; zv = np.array([zz[k] for k in n_]); lv = np.array([U[k] for k in n_]); zm = np.median(zv)
for t, se in (("above", zv >= zm), ("below", zv < zm)): P(f"  z {t} {zm:.3f}: n {se.sum()}, g {np.median(lv[se]):+.3f} +- {bs(lv[se]):.3f}")
hv = np.array([np.mean(mhm[k]) for k in U]); lv = np.array([U[k] for k in U]); hm = np.median(hv)
for t, se in (("above", hv >= hm), ("below", hv < hm)): P(f"  M_hydro {t} {hm:.2f}e14: n {se.sum()}, g {np.median(lv[se]):+.3f} +- {bs(lv[se]):.3f}")
json.dump(dict(n=len(L_), g=g, se=s, cls=C, tags=tags, mean=float(L_.mean()), rms=float(L_.std()), drops=drops, sources=USE, dropped=sorted(DROP)), open(os.path.join(HERE, "hl2_results.json"), "w"), indent=1); open(os.path.join(HERE, "hl2.out"), "w").write("\n".join(OUT) + "\n")
