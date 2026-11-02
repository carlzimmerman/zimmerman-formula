#!/usr/bin/env python3
"""FR1 step 1 (FROZEN_CRITERIA.md): measured Y500(M500) lines from pointed masses. FITTED to these data, never to a key. No eRASS1, no KiDS shear.
    python3 -I fr1_line.py   Reads GS4's inputs and HL2's parser text read only. kappa = 1/2 FITTED, unused; not theory closed."""
import csv, json, math, os, re, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); REPO = os.path.dirname(RB); OUT = []
def P(s): print(s, flush=True); OUT.append(s)
RN = 5.2715; SEED = 20261101; NB = 2000; PIV = 14.5
XT = json.load(open(os.path.join(REPO, "real_research", "data", "xcop", "xcop_r500_ettori2019.json"))); from astropy.io import fits; XC = []
for n, v in XT.items():
    p = os.path.join(REPO, "real_research", "data", "xcop", n, f"{n}_fgas_profile.fits")
    if os.path.exists(p):
        with fits.open(p) as h: XC.append((n, float(h[1].header["RA"]), float(h[1].header["DEC"]), v["z"]))
def sep(a, b, c, d):
    a, b, c, d = map(np.radians, (a, b, c, d)); return np.degrees(np.arccos(np.clip(np.sin(b) * np.sin(d) + np.cos(b) * np.cos(d) * np.cos(a - c), -1, 1)))
def isx(ra, de, z): return any(sep(ra, de, x[1], x[2]) * 60 <= 6 and abs(z - x[3]) <= .02 for x in XC)
def m_from_r(R, z, h, Om):  # R kpc at the row's h, M500 Msun at the row's h
    H = h * 100 * 1e3 / 3.0857e22; rc = 3 * H * H * (Om * (1 + z) ** 3 + 1 - Om) / (8 * math.pi * 6.674e-11); return 500 * rc * 4 / 3 * math.pi * (R * 3.0857e19) ** 3 / 1.989e30
ROWS = []
for r in csv.DictReader(open(os.path.join(RB, "GS4_pointed_gas_offset", "gs4_inputs.csv"))):
    h = float(r["h"]); z = float(r["z"]); M = float(r["M500"]) if r["M500"] not in ("", "nan") else float("nan"); Rk = float(r["R500"]); Mg = float(r["Mgas"]); Om = float(r["Om"]); via = "table"
    if r["cat"] == "E16": M = float("nan")  # GS4's M500 column for E16 is Y_X (T x Mgas), not a mass; GS4 reads only R500, so harmless there. Mass from Eckert's r500, as the paper's f_gas
    if not np.isfinite(M) or M <= 0:
        if not np.isfinite(Rk) or Rk <= 0: continue
        M = m_from_r(Rk, z, h, Om); via = "from R500"
    if not np.isfinite(Mg) or Mg <= 0: continue
    ROWS.append(dict(cat=r["cat"], name=r["name"], ra=float(r["ra"]), dec=float(r["dec"]), z=z, lgM=math.log10(M) + math.log10(h / .7), lgG=math.log10(Mg) + 2.5 * math.log10(h / .7), via=via))
P("rows by catalogue: " + ", ".join(f"{c} {sum(1 for r in ROWS if r['cat'] == c)} ({sum(1 for r in ROWS if r['cat'] == c and r['via'] != 'table')} from R500)" for c in sorted({r['cat'] for r in ROWS})))
def dedupe(rows):
    G = []
    for r in rows:
        for g in G:
            if sep(r["ra"], r["dec"], g[0]["ra"], g[0]["dec"]) * 60 <= 6 and abs(r["z"] - g[0]["z"]) <= .02: g.append(r); break
        else: G.append([r])
    return [dict(lgM=float(np.median([q["lgM"] for q in g])), lgG=float(np.median([q["lgG"] for q in g])), z=g[0]["z"], name=g[0]["name"], cats=sorted({q["cat"] for q in g}), n=len(g)) for g in G]
def fit(x, y, piv=PIV, inj=None):
    x = np.asarray(x); y = np.asarray(y); b, a = np.polyfit(x - piv, y, 1); rg = np.random.default_rng(SEED); n = len(x); ix = rg.integers(0, n, (NB, n)); B = np.array([np.polyfit(x[i] - piv, y[i], 1) for i in ix])
    return dict(a=float(a), b=float(b), sa=float(B[:, 1].std()), sb=float(B[:, 0].std()), cov=np.cov(B[:, 1], B[:, 0]).tolist(), n=n, rms=float(np.std(y - a - b * (x - piv))), piv=piv)
def se_at(F, x): c = np.array(F["cov"]); d = x - F["piv"]; return float(math.sqrt(c[0, 0] + 2 * d * c[0, 1] + d * d * c[1, 1]))
lgY0 = lambda lgG, lgM: lgG - lgM + math.log10(1 + RN)   # gas only; add lg(1 + f*)
def bins(C, key="lgM"):
    for lo, hi in ((13, 13.5), (13.5, 14), (14, 14.5), (14.5, 15), (15, 16)):
        v = [lgY0(c["lgG"], c["lgM"]) for c in C if lo <= c[key] < hi]
        if v: P(f"    lg M {lo}-{hi}: n {len(v)}, median lg Y (gas only, h 0.7) {np.median(v):+.3f} +- {1.253 * np.std(v) / math.sqrt(len(v)):.3f}, f_gas {10 ** (np.median(v)) / (1 + RN):.3f}")
RES = {}
Hset = ("L20", "L15", "S09", "L13")
def lineH(cats, lab, drop_x=True):
    r = [q for q in ROWS if q["cat"] in cats]; nx = sum(isx(q["ra"], q["dec"], q["z"]) for q in r); r = [q for q in r if not (drop_x and isx(q["ra"], q["dec"], q["z"]))]; C = dedupe(r); F = fit([c["lgM"] for c in C], [lgY0(c["lgG"], c["lgM"]) for c in C]); F["n_x_removed"] = nx
    P(f"{lab}: rows {len(r)} (X-COP rows removed {nx}), clusters {len(C)}, a {F['a']:+.4f} +- {F['sa']:.4f}, b {F['b']:+.4f} +- {F['sb']:.4f} (gas only, h 0.7), rms {F['rms']:.3f}, lg M range {min(c['lgM'] for c in C):.2f}-{max(c['lgM'] for c in C):.2f}, below 14.3: {sum(c['lgM'] < 14.3 for c in C)}"); return F, C
F, CH = lineH(Hset, "Line H, PRIMARY"); RES["H"] = F; bins(CH)
for lab, c in (("H without L20", ("L15", "S09", "L13")), ("H without L15, S09", ("L20", "L13")), ("L20 alone", ("L20",)), ("L15, S09 alone", ("L15", "S09"))):
    k = lab.replace(" ", "_").replace(",", ""); RES[k], _ = lineH(c, lab)
Fx, _ = lineH(Hset, "H with X-COP's own rows left in (sensitivity)", drop_x=False); RES["H_withx"] = Fx
# HG: lg Y on lg M_gas, pivot 13.5
g = fit([c["lgG"] for c in CH], [lgY0(c["lgG"], c["lgM"]) for c in CH], piv=13.5); RES["HG"] = g; P(f"Line HG, lg Y on lg M_gas500 (pivot 13.5): a {g['a']:+.4f} +- {g['sa']:.4f}, b {g['b']:+.4f} +- {g['sb']:.4f}, n {g['n']}")
Gb = fit([c["lgM"] + .031 for c in CH], [lgY0(c["lgG"], c["lgM"] + .031) for c in CH]); RES["Hg"] = Gb; P(f"Line H+g: a {Gb['a']:+.4f}, b {Gb['b']:+.4f}")
# Y_X, reported only
for lab, c in (("Y_X rows, C08, M08, V09, reported, excluded", ("C08", "M08", "V09")),): lineH(c, lab)
# W: HL2's parser, text read only, cut before K1
T = open(os.path.join(RB, "HL2_combined_mass_pairs", "hl2.py")).read(); T = T[:T.index("okk = True")].replace('"""HL2', '"""HL2 parse'); ns = {"__file__": os.path.join(RB, "HL2_combined_mass_pairs", "hl2.py"), "__name__": "hl2p", "P": None}; _sv = sys.stdout; sys.stdout = open(os.devnull, "w"); exec(compile(T, "hl2p", "exec"), ns); sys.stdout = _sv; S = ns["S"]; norm = ns["norm"]
XN = {norm(n) for n in XT}; W = {}
for src in ("Mahdavi+13", "Zhang+10", "Okabe16+Martino14"):
    for q in S[src]:
        if q["n"] in XN or not np.isfinite(q.get("mg", float("nan"))) or q["mg"] <= 0 or q["mw"] <= 0: continue
        W.setdefault(q["n"], []).append((src, math.log10(q["mw"]) + 14, math.log10(q["mg"]) + 14))
CW = [dict(lgM=float(np.median([v[1] for v in a])), lgG=float(np.median([v[2] for v in a])), src=a[0][0]) for a in W.values()]; nwl = len(CW)
for q in ROWS:
    if q["cat"] == "E16" and not isx(q["ra"], q["dec"], q["z"]): CW.append(dict(lgM=q["lgM"], lgG=q["lgG"], src="E16"))
Fw = fit([c["lgM"] for c in CW], [lgY0(c["lgG"], c["lgM"]) for c in CW]); RES["W"] = Fw; P(f"Line W, lensing or lensing-calibrated T: clusters {len(CW)} ({nwl} pairs, {len(CW) - nwl} XXL), a {Fw['a']:+.4f} +- {Fw['sa']:.4f}, b {Fw['b']:+.4f} +- {Fw['sb']:.4f}, rms {Fw['rms']:.3f}, below 14.3: {sum(c['lgM'] < 14.3 for c in CW)}"); bins(CW)
Cn = [c for c in CW if c["src"] != "E16"]; Fn = fit([c["lgM"] for c in Cn], [lgY0(c["lgG"], c["lgM"]) for c in Cn]); RES["W_noE16"] = Fn; P(f"  W pairs only (no XXL): n {len(Cn)}, a {Fn['a']:+.4f} +- {Fn['sa']:.4f}, b {Fn['b']:+.4f} +- {Fn['sb']:.4f}")
Ce = [c for c in CW if c["src"] == "E16"]; Fe = fit([c["lgM"] for c in Ce], [lgY0(c["lgG"], c["lgM"]) for c in Ce]); RES["W_E16"] = Fe; P(f"  XXL alone: n {len(Ce)}, a {Fe['a']:+.4f} +- {Fe['sa']:.4f}, b {Fe['b']:+.4f} +- {Fe['sb']:.4f}, median lg M {np.median([c['lgM'] for c in Ce]):.2f}")
# K2: synthetic line recovered through fit; one point per cluster
rg = np.random.default_rng(1); xs = np.array([c["lgM"] for c in CH]); ys = -.1 + .15 * (xs - PIV) + rg.normal(0, .08, len(xs)); Fs = fit(xs, ys); kk = abs(Fs["a"] + .1) < 3 * Fs["sa"] and abs(Fs["b"] - .15) < 3 * Fs["sb"] and len({c["name"] for c in CH}) == len(CH) and RES["H"]["n_x_removed"] > 0; P(f"K2 injected a -0.1, b 0.15 recovered {Fs['a']:+.4f}, {Fs['b']:+.4f}; one point per cluster, X-COP rows removed {RES['H']['n_x_removed']}: {'PASS' if kk else 'FAIL'}"); RES["K2"] = bool(kk)
for x in (14.0, 14.2, 14.4, 14.8): P(f"H at lg M500 {x}: lg Y gas only, h 0.7, {RES['H']['a'] + RES['H']['b'] * (x - PIV):+.3f} +- {se_at(RES['H'], x):.3f}; W {Fw['a'] + Fw['b'] * (x - PIV):+.3f} +- {se_at(Fw, x):.3f}")
RES["CH"] = [dict(lgM=c["lgM"], lgG=c["lgG"], cats=c["cats"], name=c["name"], z=c["z"]) for c in CH]
json.dump(RES, open(os.path.join(HERE, "fr1_line.json"), "w"), indent=0)
open(os.path.join(HERE, "fr1_line.out"), "w").write("\n".join(OUT) + "\n")
