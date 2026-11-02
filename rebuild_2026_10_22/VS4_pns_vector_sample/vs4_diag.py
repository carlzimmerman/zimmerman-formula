# VS4 diagnostic, reported and not graded: why NGC 3608 and NGC 1023 differ between CFG492 and the figure.
import json, os, re
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE)); D = f"{REPO}/real_research/data"
g = json.load(open(f"{REPO}/campaign_fresh_gravity/CFG492_multisource_synthesis/cfg492_gc_vs_pn_results.json"))["per_galaxy"]["canonical"]
v = json.load(open(f"{HERE}/vs4.json"))
for n in ("3608", "1023", "4374", "5846", "4494"):
    print(n, "CFG492 R", np.round(g[n]["RPN"], 1).tolist(), "S", np.round(g[n]["SPN"], 0).tolist(), "Re", round(g[n]["Re"], 2), "| figure (R/Re, sigma, err)", [[round(x, 1) for x in p] for p in v["points"][n]])
def hms(s):
    p = [float(x) for x in s.split()]; return 15 * (p[0] + p[1] / 60 + p[2] / 3600)
def dms(s):
    p = [float(x) for x in s.replace("+", "").replace("-", "").split()]; return (-1 if s.strip()[0] == "-" else 1) * (p[0] + p[1] / 60 + p[2] / 3600)
R = []
for l in open(f"{D}/pn_coccato2009_sampleA.tsv"):
    x = l.rstrip("\n").split("\t")
    if len(x) > 5 and x[1].startswith("NGC3608"): R.append((hms(x[2]), dms(x[3]), float(x[4])))
R = np.array(R)
C = {"3608": (169.246, 18.149, 1226), "3607": (169.228, 18.052, 935)}
cd = np.cos(np.radians(18.1)); d8 = np.hypot((R[:, 0] - C["3608"][0]) * cd, R[:, 1] - C["3608"][1]) * 60; d7 = np.hypot((R[:, 0] - C["3607"][0]) * cd, R[:, 1] - C["3607"][1]) * 60
print("NGC 3608 catalogue: N", len(R), "median v", np.median(R[:, 2]), "std v", round(R[:, 2].std(ddof=1), 1), "separation of the two centres", round(np.hypot((C["3608"][0] - C["3607"][0]) * cd, C["3608"][1] - C["3607"][1]) * 60, 2), "arcmin")
for lab, s in (("closer to 3608", d8 < d7), ("closer to 3607", d7 <= d8)):
    print(" ", lab, int(s.sum()), "median v", np.median(R[s, 2]), "std", round(R[s, 2].std(ddof=1), 1))
for lo, hi in ((0, 1), (1, 2), (2, 4), (4, 9)):
    s = (d8 >= lo) & (d8 < hi)
    if s.sum() > 2: print(f"  {lo}-{hi} arcmin from 3608: N {s.sum()} median v {np.median(R[s,2]):.0f} std {R[s,2].std(ddof=1):.0f}, median distance to 3607 {np.median(d7[s]):.1f}")
print("velocity histogram, bins of 100 km/s from 600:", np.histogram(R[:, 2], bins=np.arange(600, 1900, 100))[0].tolist())
