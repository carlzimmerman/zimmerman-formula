#!/usr/bin/env python3
"""Jones+2021 (ALPINE-ALMA [CII] kinematics, arXiv:2104.03099): Table 1 (34 rows: z, PA and inclination from moment map and 3DBarolo, kinematic-classification flags, L20 and J21 classes) and Appendix Table A3 (per-ring R, v_rot, sigma_v, M_dyn)
parsed from the arXiv HTML fetched 2026-09-30.  The tables carry NO stellar or gas masses (those are in Faisst+2020 and Dessauges-Zavadsky+2020); nothing is recomputed."""
import sys, os, re, csv
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, ".."))
from tabutil import *
s = open(os.path.join(HERE, "..", "raw_small", "arxiv_2104.03099_html_fetched_2026-09-30.html"), errors="ignore").read(); LOG = []
T1 = []
for r in rows(s, "S3.T1.6")[2:]:
    if len(r) < 13 or not re.match(r"^[A-Z]{2}\d*", r[0].strip()): continue
    d = {"name": r[0].strip()}
    for k, nm in ((1, "z"), (2, "PA_moment"), (3, "PA_3DBarolo"), (4, "inc_moment"), (5, "inc_3DBarolo")):
        v, lo, hi, fl = val(r[k]); d[nm] = v; d[nm + "_err"] = lo
    d["criteria_W15_1to5"] = "".join("Y" if "checkmark" in r[k] else "N" for k in range(6, 11)) if len(r) > 10 else ""
    d["KC1"] = r[11] if len(r) > 11 else ""; d["class_L20"] = r[11].strip() if len(r) > 11 else ""; d["class_J21"] = r[12].strip() if len(r) > 12 else ""
    T1.append(d)
A = []; cur = None
for r in rows(s, "A3.T2.4")[2:]:
    if len(r) < 5: continue
    if r[0].strip(): cur = r[0].strip()
    d = {"name": cur}
    for k, nm in ((1, "R_kpc"), (2, "vrot_kms"), (3, "sigma_kms"), (4, "Mdyn_Msun")):
        v, lo, hi, fl = val(r[k]); d[nm] = v; d[nm + "_err"] = lo
        if nm == "Mdyn_Msun":
            m = re.search(r"\(([\d.]+)\\pm\s*([\d.]+)\)\\times\s*10\^\{?(\d+)", r[k]); 
            if m: d["Mdyn_Msun"] = float(m.group(1)) * 10 ** int(m.group(3)); d["Mdyn_Msun_err"] = float(m.group(2)) * 10 ** int(m.group(3))
    A.append(d)
write(os.path.join(HERE, "jones2021_table1_sample_classes.csv"), T1); write(os.path.join(HERE, "jones2021_tableA3_rings.csv"), A)
n_rot = sum(1 for d in T1 if d["class_J21"] == "ROT"); gal = {d["name"] for d in A}
LOG.append(f"Table 1: {len(T1)} galaxies, J21 classes {sorted({d['class_J21'] for d in T1})}, ROT = {n_rot}; z {min(d['z'] for d in T1):.3f}-{max(d['z'] for d in T1):.3f}")
LOG.append(f"Table A3: {len(A)} ring rows for {len(gal)} galaxies; R range {min(d['R_kpc'] for d in A):.2f}-{max(d['R_kpc'] for d in A):.2f} kpc")
print("\n".join(LOG)); open(os.path.join(HERE, "checks.txt"), "w").write("\n".join(LOG) + "\n")
