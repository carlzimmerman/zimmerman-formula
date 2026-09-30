#!/usr/bin/env python3
"""Parse Table 1 of Ubler et al. 2018 (arXiv:1802.02135, 'Ionized and molecular gas kinematics in a z=1.4 star-forming galaxy', one galaxy = EGS_13011166 of PHIBSS) from the arXiv HTML (fetched 2026-09-29).
The table gives, for seven model setups (fiducial Halpha+CO, Halpha only, CO only, low/high concentration, free halo + B/T, two fixed disks), the priors and the posterior medians (asymmetric 1-sigma)
of log-mass parameters, R_e, B/T, inclination, sigma_0, halo mass, concentration and f_DM(<=R_e).  It is ONE galaxy: the direct Halpha-versus-CO comparison of the same disc.  No number is recomputed."""
import sys, os, json, hashlib, re
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, ".."))
from tabutil import *
SRC = os.path.join(HERE, "..", "raw_small", "arxiv_1802.02135_html_fetched_2026-09-29.html"); s = open(SRC, errors="ignore").read()
R = rows(s, "S2.T1.2"); models = ["fiducial Halpha+CO", "Halpha only", "CO only", "low c (2), Halpha+CO", "high c (8), Halpha+CO", "free halo and B/T, Halpha+CO", "2 fixed disks, Halpha+CO"]
out = []; i = 2
while i < len(R):
    lab = R[i]; name = re.sub(r"\s+", " ", lab[0]).strip()
    if name.startswith("inferred"):                                  # single row: label and posteriors together
        for k, m in enumerate(models, start=1):
            v, lo, hi, fl = val(lab[k]); out.append(dict(parameter=name, model=m, prior="", posterior=v, err_lo=lo, err_hi=hi, flag=fl, raw=lab[k]))
        i += 1; continue
    post = R[i + 1]
    for k, m in enumerate(models, start=1):
        v, lo, hi, fl = val(post[k]); out.append(dict(parameter=name, model=m, prior=lab[k], posterior=v, err_lo=lo, err_hi=hi, flag=fl, raw=post[k]))
    i += 2
write(os.path.join(HERE, "ubler2018_table1_model_results.csv"), out)
n = {(d["parameter"].split("[")[0].strip() or d["parameter"][:12]) for d in out}
fd = [d for d in out if d["parameter"].startswith("inferred")]
print(len(out), "cells;", len(R) - 2, "table rows"); print("f_DM(<=R_e):", [(d["model"], d["posterior"]) for d in fd])
open(os.path.join(HERE, "checks.txt"), "w").write(f"{len(out)} cells for 7 setups; f_DM(<=Re) fiducial {fd[0]['posterior']} (+{fd[0]['err_hi']} -{fd[0]['err_lo']})\n")
json.dump(dict(source_html_sha256=hashlib.sha256(open(SRC, "rb").read()).hexdigest(), url="https://arxiv.org/html/1802.02135", fetched="2026-09-29", bytes=os.path.getsize(SRC)), open(os.path.join(HERE, "manifest.json"), "w"), indent=1)
