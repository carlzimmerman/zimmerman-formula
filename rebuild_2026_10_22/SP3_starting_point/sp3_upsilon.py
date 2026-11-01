#!/usr/bin/env python3
"""SP3 S2-S3 (FROZEN_CRITERIA.md): SPARC-independent stellar masses on disk. Reads only. kappa = 1/2 FITTED, unused; not theory closed."""
import csv, json, math, os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); RT = os.path.dirname(os.path.dirname(HERE)); OUT = []
def P(s): print(s, flush=True); OUT.append(s)
def fl(x):
    try: return float(x)
    except ValueError: return None
rows = list(csv.DictReader(open(os.path.join(RT, "data_assembly", "alfalfa_sdss_local_control", "alfalfa_sdss.csv"))))
Q0 = 0.2; A = []
for r in rows:
    w, ba, mm, code = fl(r["w50_kms"]), fl(r["ba_r"]), fl(r["logms_mcgaugh"]), r["hi_code"]
    if w is None or ba is None or mm is None or code != "1" or ba > 0.71 or ba < Q0: continue
    s2 = (1 - ba * ba) / (1 - Q0 * Q0); V = w / (2 * math.sqrt(s2))
    A.append(dict(V=V, mm=mm, T=fl(r["logms_taylor"]), G=fl(r["logms_gswlc"]), agc=int(r["agc"]), D=fl(r["dist_mpc"]), gi=fl(r["gi_corr"])))
P(f"SP3 S2: Durbala+20, hi_code 1, i >= 45, w50/(2 sin i); n {len(A)}. Upsilon_W1 = 0.45 x 10^(logM_X - logM_McGaugh). W1 stands in for 3.6 micron. Models with an IMF, not a measurement of stars.")
RES = dict(S2={})
for lo, hi in ((60, 100), (100, 150), (150, 250), (150, 200), (200, 250), (250, 400)):
    a = [x for x in A if lo <= x["V"] < hi]; o = dict(n=len(a))
    for k, nm in (("G", "GSWLC"), ("T", "Taylor")):
        u = np.array([0.45 * 10 ** (x[k] - x["mm"]) for x in a if x[k] is not None])
        o[nm] = dict(n=len(u), med=float(np.median(u)), p16=float(np.percentile(u, 16)), p84=float(np.percentile(u, 84)), f_le_040=float(np.mean(u <= 0.40)))
    RES["S2"][f"{lo}-{hi}"] = o; P(f"  V {lo}-{hi}: " + "; ".join(f"{n} n {o[n]['n']} median {o[n]['med']:.3f} [{o[n]['p16']:.3f}, {o[n]['p84']:.3f}], share <= 0.40 {o[n]['f_le_040']:.2f}" for n in ("GSWLC", "Taylor")))
m = RES["S2"]["150-250"]; meds = [m[n]["med"] for n in ("GSWLC", "Taylor")]; rd = "NOT BROKEN" if min(meds) <= 0.40 else "BROKEN" if min(meds) >= 0.45 else "BETWEEN"; RES["S2_reading"] = rd; P(f"S2 reading, frozen rule, 150-250 km/s: 0.30-0.40 {rd} by these stellar masses. Medians {meds}")
# bluer vs redder at fixed V: population does move it
a = [x for x in A if 150 <= x["V"] < 250 and x["G"] is not None and x["gi"] is not None]; g = np.array([x["gi"] for x in a]); u = np.array([0.45 * 10 ** (x["G"] - x["mm"]) for x in a]); t = np.percentile(g, [33, 67]); P(f"  reported, GSWLC by g-i tercile at 150-250: {np.median(u[g <= t[0]]):.3f}, {np.median(u[(g > t[0]) & (g <= t[1])]):.3f}, {np.median(u[g > t[1]]):.3f}")
# S3
MRT = os.path.join(RT, "real_research", "data", "SPARC_Lelli2016c.mrt"); S = {}
for l in open(MRT):
    p = l.split()
    if len(p) < 18: continue
    try: S[p[0]] = dict(D=float(p[2]), inc=float(p[5]), einc=float(p[6]), L=float(p[7]), vf=float(p[15]), Q=int(p[17]))
    except ValueError: pass
byagc = {int(r["agc"]): r for r in rows}; P3 = []
for n, s in S.items():
    if not n.startswith("UGC"): continue
    try: ag = int(n[3:])
    except ValueError: continue
    r = byagc.get(ag)
    if not r or s["L"] <= 0: continue
    d = fl(r["dist_mpc"])
    if not d: continue
    e = dict(name=n, vf=s["vf"], Q=s["Q"], inc=s["inc"], DS=s["D"], DA=d)
    for k, c in (("G", "logms_gswlc"), ("T", "logms_taylor"), ("M", "logms_mcgaugh")):
        v = fl(r[c]); e[k] = None if v is None else float(10 ** v * (s["D"] / d) ** 2 / (s["L"] * 1e9))
    P3.append(e)
RES["S3"] = P3; P(f"\nS3: SPARC UGC names with an AGC row: {len(P3)}; catalogue M* at SPARC's D over SPARC's L[3.6]")
for lo, hi in ((60, 150), (150, 250), (250, 400)):
    a = [e for e in P3 if lo <= e["vf"] < hi and abs(math.log10(e["DS"] / e["DA"])) < 0.2]
    P(f"  V_flat {lo}-{hi}: n {len(a)}; " + "; ".join(f"{nm} {np.median([e[k] for e in a if e[k]]):.3f} (n {sum(1 for e in a if e[k])})" for k, nm in (("G", "GSWLC"), ("T", "Taylor"), ("M", "McGaugh W1 0.45")) if any(e[k] for e in a)))
json.dump(RES, open(os.path.join(HERE, "sp3_upsilon.json"), "w"), indent=1); open(os.path.join(HERE, "sp3_upsilon.out"), "w").write("\n".join(OUT) + "\n")
