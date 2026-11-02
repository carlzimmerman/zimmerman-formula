#!/usr/bin/env python3
"""UL1 part 2: SPARC-independent stellar masses on disk, by V, separately. Reads Durbala+20's CSV and SPARC's table. kappa = 1/2 FITTED, unused; not theory closed."""
import csv, json, math, os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); RT = os.path.dirname(RB); OUT = []
def P(s): print(s, flush=True); OUT.append(s)
def fl(x):
    try: return float(x)
    except ValueError: return None
rows = list(csv.DictReader(open(os.path.join(RT, "data_assembly", "alfalfa_sdss_local_control", "alfalfa_sdss.csv"))))
Q0 = 0.2; BIN = ((20, 60), (60, 100), (100, 150), (150, 200), (200, 250), (250, 400)); A = []
for r in rows:
    w, w2, ba, mm, code = fl(r["w50_kms"]), fl(r["w20_kms"]), fl(r["ba_r"]), fl(r["logms_mcgaugh"]), r["hi_code"]
    if w is None or ba is None or mm is None or code != "1" or ba > 0.71 or ba < Q0: continue
    si = math.sqrt((1 - ba * ba) / (1 - Q0 * Q0))
    A.append(dict(V=w / (2 * si), V20=(w2 / (2 * si) if w2 else None), mm=mm, T=fl(r["logms_taylor"]), G=fl(r["logms_gswlc"]), D=fl(r["dist_mpc"]), gi=fl(r["gi_corr"]), iabs=fl(r["imag_abs_corr"])))
def tab(sel, vk="V", cond=lambda a: True):
    o = {}
    for lo, hi in BIN:
        a = [x for x in A if x[vk] is not None and lo <= x[vk] < hi and sel(x) and cond(x)]; e = {}
        for k, nm in (("T", "Taylor"), ("G", "GSWLC")):
            u = np.array([0.45 * 10 ** (x[k] - x["mm"]) for x in a if x[k] is not None]); v = np.array([x[vk] for x in a if x[k] is not None])
            if len(u) >= 5: p = np.percentile(u, [16, 84]); e[nm] = dict(n=len(u), mu=float(np.median(u)), p16=float(p[0]), p84=float(p[1]), sig=float(0.5 * (math.log10(p[1]) - math.log10(p[0]))), Vmed=float(np.median(v)))
            else: e[nm] = dict(n=len(u), mu=None)
        o[f"{lo}-{hi}"] = e
    return o
def show(t, l):
    P(l)
    for nm in ("Taylor", "GSWLC"): P(f"  {nm:7s} " + "  ".join((f"{b} {t[b][nm]['mu']:.3f} [{t[b][nm]['p16']:.3f},{t[b][nm]['p84']:.3f}] n{t[b][nm]['n']}" if t[b][nm]["mu"] else f"{b} -") for b in t))
ALL = lambda x: True
R = dict(primary=tab(ALL)); show(R["primary"], "PRIMARY: hi_code 1, i >= 45 by b/a, w50/(2 sin i)")
sp = json.load(open(os.path.join(RB, "SP3_starting_point", "sp3_upsilon.json")))["S2"]; d = max(abs(R["primary"][b][nm]["mu"] - sp[b][nm]["med"]) for b in sp if b in R["primary"] for nm in ("Taylor", "GSWLC")); R["K7"] = d; P(f"K7 against SP3's S2: max |d mu| {d:.2e}: {'PASS' if d <= 0.001 else 'FAIL'}")
R["w20"] = tab(ALL, "V20"); show(R["w20"], "STRESS w20/(2 sin i)")
R["D60"] = tab(lambda x: x["D"] and x["D"] > 60); show(R["D60"], "STRESS D > 60 Mpc (W1 and SDSS apertures less stretched)")
R["D30"] = tab(lambda x: x["D"] and x["D"] < 40); show(R["D30"], "STRESS D < 40 Mpc")
R["common"] = tab(lambda x: x["T"] is not None and x["G"] is not None); show(R["common"], "STRESS common sample, both estimators")
# what the estimators are: spread between them, galaxy by galaxy, and colour slope
for lo, hi in BIN[1:]:
    a = [x for x in A if lo <= x["V"] < hi and x["T"] is not None and x["G"] is not None]; dd = np.array([x["G"] - x["T"] for x in a]); g = np.array([x["gi"] for x in a]); u = np.array([x["T"] - x["mm"] for x in a]); P(f"  {lo}-{hi}: GSWLC - Taylor {np.median(dd):+.3f} dex [{np.percentile(dd, 16):+.3f},{np.percentile(dd, 84):+.3f}]; median g-i {np.median(g):.2f}")
# the W1 shortfall test: at fixed V, does M_X/M_W1 depend on distance? and on M_i (mass) at fixed V
P("Taylor/W1 Upsilon by distance tercile at fixed V (rise toward small D would be W1 shortfall on extended galaxies):")
R["byD"] = {}
for lo, hi in BIN[1:]:
    a = [x for x in A if lo <= x["V"] < hi and x["T"] is not None and x["D"]]; D = np.array([x["D"] for x in a]); u = 0.45 * 10 ** np.array([x["T"] - x["mm"] for x in a]); g = np.array([x["gi"] for x in a]); t = np.percentile(D, [33, 67]); s = [D <= t[0], (D > t[0]) & (D <= t[1]), D > t[1]]; R["byD"][f"{lo}-{hi}"] = [float(np.median(u[q])) for q in s]; P(f"  {lo}-{hi}: D {t[0]:.0f}, {t[1]:.0f} Mpc: " + ", ".join(f"{np.median(u[q]):.3f} (g-i {np.median(g[q]):.2f})" for q in s))
# on SPARC's own L[3.6], where AGC = UGC: no W1 at all
S = {}
for l in open(os.path.join(RT, "real_research", "data", "SPARC_Lelli2016c.mrt")):
    p = l.split()
    if len(p) < 18: continue
    try: S[p[0]] = dict(D=float(p[2]), inc=float(p[5]), L=float(p[7]), vf=float(p[15]), Q=int(p[17]), T=float(p[1]))
    except ValueError: pass
by = {}
for r in rows:
    try: by[int(r["agc"])] = r
    except ValueError: pass
Pz = []
for n, s in S.items():
    if not n.startswith("UGC"): continue
    try: g = by.get(int(n[3:]))
    except ValueError: continue
    if not g or s["L"] <= 0 or not fl(g["dist_mpc"]): continue
    dd = fl(g["dist_mpc"]); e = dict(name=n, vf=s["vf"], Q=s["Q"], inc=s["inc"], DS=s["D"], DA=dd, w50=fl(g["w50_kms"]), w20=fl(g["w20_kms"]), hc=g["hi_code"])
    for k, c in (("T", "logms_taylor"), ("G", "logms_gswlc"), ("M", "logms_mcgaugh")):
        v = fl(g[c]); e[k] = None if v is None else float(10 ** v * (s["D"] / dd) ** 2 / (s["L"] * 1e9))
    Pz.append(e)
R["pairs"] = Pz; P(f"\nSPARC UGC with an AGC row: {len(Pz)}. M_X at SPARC's D over SPARC's L[3.6]; McG col should read 0.45 x L_W1/L_3.6")
for lo, hi in ((20, 60), (60, 100), (100, 150), (150, 250), (250, 400)):
    a = [e for e in Pz if lo <= e["vf"] < hi and abs(math.log10(e["DS"] / e["DA"])) < 0.2]; P(f"  V_flat {lo}-{hi} n {len(a)}: " + "; ".join(f"{nm} {np.median([e[k] for e in a if e[k]]):.3f} (n {sum(1 for e in a if e[k])})" for k, nm in (("T", "Taylor"), ("G", "GSWLC"), ("M", "McG")) if any(e[k] for e in a)))
b = [e for e in Pz if e["vf"] > 0 and e["w50"] and e["inc"] >= 30]; rw = [e["w50"] / (2 * math.sin(math.radians(e["inc"]))) / e["vf"] for e in b]; rw2 = [e["w20"] / (2 * math.sin(math.radians(e["inc"]))) / e["vf"] for e in b if e["w20"]]; R["w50_over_vf"] = dict(n=len(b), med=float(np.median(rw)), p16=float(np.percentile(rw, 16)), p84=float(np.percentile(rw, 84)), w20=float(np.median(rw2))); P(f"bin mapping: w50/(2 sin i_SPARC)/V_flat, n {len(b)}: median {np.median(rw):.3f} [{np.percentile(rw, 16):.3f},{np.percentile(rw, 84):.3f}]; w20: {np.median(rw2):.3f}")
json.dump(R, open(os.path.join(HERE, "ul1_est.json"), "w"), indent=1); open(os.path.join(HERE, "ul1_est.out"), "w").write("\n".join(OUT) + "\n")
